const { test } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const code = fs.readFileSync(path.join(__dirname, '../compat/web_ux.js'), 'utf8');
const runtime = fs.readFileSync(path.join(__dirname, '../compat/runtime.js'), 'utf8');

function context(extra = {}) {
    const c = { m2w: {}, TextDecoder, console, ...extra };
    vm.runInNewContext(code, c);
    return c;
}

function manifest() {
    const header = Buffer.alloc(28);
    header.write('M2WF');
    header.writeUInt32LE(1, 4);
    header.writeUInt32LE(4, 8);
    header.writeUInt32LE(3, 12);
    header.writeUInt32LE(1, 16);
    header.writeUInt32LE(2, 20);
    const chunks = [3, 4, 4].map((size, i) => {
        const b = Buffer.alloc(20, i + 1);
        b.writeUInt32LE(size, 16);
        return b;
    });
    function file(name, chunk, offset, size) {
        const n = Buffer.from(name), b = Buffer.alloc(16);
        b.writeUInt32LE(chunk, 2);
        b.writeUInt32LE(offset, 6);
        b.writeUInt32LE(size, 10);
        b.writeUInt16LE(n.length, 14);
        return Buffer.concat([b, n]);
    }
    const b = Buffer.concat([header, ...chunks, Buffer.alloc(2),
        file('ymir work/ui/intro/login/background.png', 0, 2, 4),
        file('ymir work/monster/not_needed.gr2', 2, 0, 4)]);
    return b.buffer.slice(b.byteOffset, b.byteOffset + b.byteLength);
}

test('login preparation follows real short-chunk spans and excludes gameplay', () => {
    const menu = context().m2w.loginManifest(manifest());
    assert.equal(menu.files, 1);
    assert.equal(menu.names.size, 2);
    assert.ok(menu.names.has('01'.repeat(16) + '.bin'));
    assert.ok(menu.names.has('02'.repeat(16) + '.bin'));
    assert.ok(!menu.names.has('03'.repeat(16) + '.bin'));
});

test('a corrupt manifest cannot silently release engine startup', () => {
    const b = manifest();
    new Uint8Array(b)[0] = 0;
    assert.throws(() => context().m2w.loginManifest(b), /Invalid corpus manifest/);
});

test('Tab emits the IME character event and page controls retain their keys', () => {
    const handlers = {}, canvas = { addEventListener() {}, style: {} };
    const c = context({ Module: { canvas }, document: { addEventListener() {}, getElementById: () => canvas },
        addEventListener(name, fn) { (handlers[name] ||= []).push(fn); } });
    const start = runtime.indexOf('m2w.eventsStart =');
    const end = runtime.indexOf('/// Next queued event', start);
    vm.runInNewContext(runtime.slice(start, end), c);
    c.m2w.eventsStart();
    const fire = (key, extra = {}) => handlers.keydown.forEach(fn => fn({ key, preventDefault() {}, ...extra }));
    fire('Tab');
    assert.deepEqual(Array.from(c.m2w.events.queue, x => [x.k, x.w]), [[256, 9], [258, 9]]);
    c.m2w.events.queue.length = 0;
    fire('Tab', { shiftKey: true });
    assert.equal(c.m2w.events.queue[1].w, 9);
    c.m2w.events.queue.length = 0;
    fire('r', { metaKey: true });
    fire('Tab', { target: { closest: () => ({}) } });
    assert.equal(c.m2w.events.queue.length, 0);
});

test('username storage confirms writes and never persists a password', () => {
    const files = new Map(), stored = new Map();
    let tick;
    const c = context({ Module: { FS: {
        writeFile(p, t) { files.set(p, t); }, readFile(p) { if (!files.has(p)) throw Error(); return files.get(p); }
    } }, localStorage: { getItem: k => stored.get(k) ?? null, setItem: (k, v) => stored.set(k, v) },
    setInterval(fn) { tick = fn; } });
    c.m2w.startBrowserBridge();
    files.set('/m2w_browser_request', JSON.stringify({ id: '1', action: 'remember', slot: 0, login: 'test_user', password: 'must_never_persist' }));
    tick();
    assert.equal(JSON.parse(files.get('/m2w_browser_reply')).ok, true);
    assert.equal(JSON.parse(files.get('/m2w_browser_state')).accounts[0], 'test_user');
    assert.ok(!JSON.stringify([...stored]).includes('must_never_persist'));
    files.set('/m2w_browser_request', JSON.stringify({ id: '2', action: 'forget', slot: 0 }));
    tick();
    assert.equal(JSON.parse(files.get('/m2w_browser_state')).accounts[0], '');
});

test('denied browser storage reports failure instead of success', () => {
    const files = new Map();
    let tick;
    const c = context({ Module: { FS: { writeFile: (p, t) => files.set(p, t), readFile: p => files.get(p) } },
        localStorage: { getItem() { throw Error('denied'); }, setItem() { throw Error('denied'); } },
        setInterval(fn) { tick = fn; } });
    c.m2w.startBrowserBridge();
    files.set('/m2w_browser_request', JSON.stringify({ id: '1', action: 'remember', slot: 0, login: 'test_user' }));
    tick();
    assert.equal(JSON.parse(files.get('/m2w_browser_reply')).ok, false);
});

test('the full logical desktop fits after width or height shrinks', () => {
    const c = context();
    for (const [w, h] of [[900, 700], [600, 700], [1200, 300], [400, 800], [1920, 1080]]) {
        const r = c.m2w.fitViewportRect(1760, 1080, w, h, 0, 0);
        assert.ok(r.left >= -1e-8 && r.top >= -1e-8);
        assert.ok(r.left + r.width <= w + 1e-8);
        assert.ok(r.top + r.height <= h + 1e-8);
        assert.ok(Math.abs(r.width / r.height - 1760 / 1080) < 1e-8);
        // The original bottom taskbar and right inventory stay on the canvas.
        const scale = r.width / 1760;
        assert.ok(r.top + 1080 * scale <= h + 1e-8);
        assert.ok(r.left + (1760 - 212 + 212) * scale <= w + 1e-8);
    }
});

test('resize and fullscreen retain game resolution and hidden-tab state', () => {
    const events = {}, canvas = { style: {} };
    let hidden = 0;
    const c = context({ Module: { canvas }, innerWidth: 1200, innerHeight: 736,
        document: { addEventListener: (k, f) => { events[k] = f; } },
        addEventListener: (k, f) => { events[k] = f; },
        m2w: { windowSize: h => h ? 1080 : 1760, uiScale: () => 1,
               maxBuffer: { w: 1920, h: 1080 }, canvasState: () => hidden } });
    c.m2w.startViewportFit();
    c.innerWidth = 600;
    c.innerHeight = 350;
    events.resize();
    assert.equal(c.m2w.windowSize(0), 1760);
    assert.equal(c.m2w.canvasState(1), 1080);
    assert.ok(parseFloat(canvas.style.width) <= 600);
    assert.ok(parseFloat(canvas.style.height) <= 350);
    hidden = 1;
    assert.equal(c.m2w.canvasState(2), 1);
    c.innerWidth = 1920;
    c.innerHeight = 1080;
    events.fullscreenchange();
    assert.ok(Math.abs(parseFloat(canvas.style.height) - 1080) < 1e-8);
    // Retry of startup must not install duplicate listeners or recapture size.
    c.m2w.startViewportFit();
    assert.equal(c.m2w.windowSize(0), 1760);
});

test('a small initial browser gets a usable desktop without exceeding render caps', () => {
    const c = context({ Module: { canvas: { style: {} } }, innerWidth: 400, innerHeight: 300,
        document: { addEventListener() {} }, addEventListener() {},
        m2w: { windowSize: h => h ? 600 : 800, uiScale: () => 1,
               maxBuffer: { w: 1920, h: 1080 }, canvasState: () => 0 } });
    c.m2w.startViewportFit();
    assert.equal(c.m2w.windowSize(0), 800);
    assert.equal(c.m2w.windowSize(1), 640);
    assert.ok(c.m2w.viewportFitState.rect.height <= 300);
});
