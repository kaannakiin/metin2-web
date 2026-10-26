const { test } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');

const runtime = fs.readFileSync(path.join(__dirname, '../compat/runtime.js'), 'utf8');
const code = runtime.slice(runtime.indexOf('m2w.chunkTask ='), runtime.indexOf('m2w.chunkList ='));
const a = 'a'.repeat(32) + '.bin';
const b = 'b'.repeat(32) + '.bin';
const bytes = () => new Uint8Array([1, 2, 3, 4]).buffer;
const never = () => new Promise(() => {});
const flush = async () => { for (let i = 0; i < 60; ++i) await Promise.resolve(); };

function clock() {
    let now = 0, next = 0;
    const timers = new Map();
    return {
        now: () => now,
        setTimeout(fn, delay) { const id = ++next; timers.set(id, { fn, at: now + delay }); return id; },
        clearTimeout(id) { timers.delete(id); },
        async advance(ms) {
            const end = now + ms;
            for (let guard = 0; guard < 10000; ++guard) {
                const due = [...timers].filter(([, x]) => x.at <= end).sort((x, y) => x[1].at - y[1].at)[0];
                if (!due) { now = end; await flush(); return; }
                now = due[1].at;
                timers.delete(due[0]);
                due[1].fn();
                await flush();
            }
            throw new Error('runaway timer');
        }
    };
}

function response(buffer = bytes(), extra = {}) {
    return { ok: true, status: 200, headers: { get: () => 'application/octet-stream' },
        arrayBuffer: async () => buffer, clone: () => response(buffer), ...extra };
}

function setup(options = {}) {
    const time = clock();
    const calls = [];
    const storage = { match: async () => null, put: async () => {}, delete: async () => {}, keys: async () => [],
        ...options.storage };
    const m2w = { options: { get: () => null }, corpus: { all: [] } };
    const context = { m2w, Promise, Map, Set, Uint8Array, AbortController,
        console: { log() {}, warn() {} },
        performance: { now: time.now, setResourceTimingBufferSize() {} },
        setTimeout: time.setTimeout, clearTimeout: time.clearTimeout,
        caches: { open: options.open || (async () => storage) },
        fetch: async (url, init) => {
            if (url.endsWith('groups.txt') && options.groupsFetch) return options.groupsFetch();
            if (url.endsWith('groups.txt')) return { ok: true, text: async () =>
                options.groups ?? ('boot 8 ' + a.slice(0, 32) + ' ' + b.slice(0, 32)) };
            calls.push(url);
            return options.fetch ? options.fetch(url, init, calls) : response();
        } };
    vm.runInNewContext(code, context);
    m2w.chunkCacheStart(64);
    const start = () => m2w.prefetchStart('https://game.test/corpus/');
    if (options.start !== false) start();
    return { m2w, time, calls, start };
}

test('transient failure retries the missing chunk and completes progress', async () => {
    let first = true;
    const t = setup({ fetch(url) {
        if (url.endsWith(a) && first) { first = false; throw new Error('temporary network error'); }
        return response();
    } });
    await flush();
    assert.equal(t.m2w.prefetch.fetched.size, 1);
    await t.time.advance(1000);
    assert.equal(t.m2w.prefetch.fetched.size, 2);
    assert.equal(t.m2w.prefetch.active, 0);
    assert.equal(t.m2w.chunks.inFlight.size, 0);
    assert.equal(t.m2w.chunks.bytes, 8);
});

test('permanent failure stops after three attempts and can be retried manually', async () => {
    let broken = true;
    const t = setup({ fetch() { if (broken) throw new Error('HTTP 503'); return response(); } });
    await flush();
    await t.time.advance(3000);
    assert.equal(t.calls.length, 6);
    assert.equal(t.m2w.prefetch.failed.size, 2);
    assert.equal(t.m2w.prefetch.active, 0);
    assert.equal(t.m2w.prefetch.waiting.size, 0);
    assert.equal(t.m2w.chunks.bytes, 0);
    broken = false;
    t.m2w.retryPrefetchFailed();
    await flush();
    assert.equal(t.m2w.prefetch.failed.size, 0);
    assert.equal(t.m2w.prefetch.fetched.size, 2);
});

test('a hanging HTTP body is aborted and cannot occupy slots forever', async () => {
    const signals = [];
    const t = setup({ fetch(_, init) { signals.push(init.signal); return response(bytes(), { arrayBuffer: never }); } });
    await flush();
    await t.time.advance(64000);
    assert.equal(t.m2w.prefetch.active, 0);
    assert.equal(t.m2w.chunks.inFlight.size, 0);
    assert.equal(t.m2w.prefetch.failed.size, 2);
    assert.equal(signals.length, 6);
    assert.ok(signals.every(signal => signal.aborted));
});

test('hanging cache open falls back to network', async () => {
    const t = setup({ open: never });
    await flush();
    await t.time.advance(2000);
    assert.equal(t.m2w.prefetch.fetched.size, 2);
});

test('hanging or empty cache entries fall back to network', async () => {
    for (const match of [never, async () => response(new ArrayBuffer(0))]) {
        const t = setup({ storage: { match } });
        await flush();
        await t.time.advance(2000);
        assert.equal(t.m2w.prefetch.fetched.size, 2);
        assert.equal(t.calls.length, 2);
        assert.equal(t.m2w.prefetch.fromStorage, 0);
    }
});

test('a failed shared background read does not discard queued prefetch work', async () => {
    let rejectBackground;
    const t = setup({ start: false, fetch(url) {
        if (url.endsWith(a) && !rejectBackground) return new Promise((_, reject) => { rejectBackground = reject; });
        return response();
    } });
    t.m2w.chunkInBackground('https://game.test/corpus/' + a, a);
    await flush();
    t.start();
    await flush();
    assert.ok(t.m2w.prefetch.queue.includes(a));
    rejectBackground(new Error('background failed'));
    await flush();
    await t.time.advance(200);
    assert.equal(t.m2w.prefetch.fetched.size, 2);
    assert.equal(t.m2w.chunks.background, 0);
});

test('successful background reads remain completed after memory eviction', async () => {
    const t = setup({ groups: '' });
    await flush();
    t.m2w.chunkInBackground('https://game.test/corpus/' + a, a);
    await flush();
    t.m2w.chunks.map.delete(a);
    assert.ok(t.m2w.prefetch.fetched.has(a));
});

test('a rejected cache write does not fail or hang downloaded chunks', async () => {
    const t = setup({ storage: { put: async () => { throw new Error('disk quota'); } } });
    await flush();
    assert.equal(t.m2w.prefetch.fetched.size, 2);
    assert.equal(t.m2w.prefetch.errors, 0);
});

test('an evicted map is not ready until its chunks return to RAM', async () => {
    const t = setup({ groups: 'map:demo 4 ' + a.slice(0, 32) });
    await flush();
    t.m2w.want('map:demo', true);
    await flush();
    t.m2w.chunks.bytes -= t.m2w.chunks.map.get(a).length;
    t.m2w.chunks.map.delete(a);
    assert.ok(t.m2w.prefetch.fetched.has(a));
    assert.equal(t.m2w.mapReady('demo'), 0);
    await flush();
    assert.equal(t.m2w.mapReady('demo'), 1);
    assert.ok(t.m2w.chunks.map.has(a));
});

test('a map timeout cannot release a blocking load of unavailable chunks', async () => {
    const t = setup({ groups: 'map:demo 4 ' + a.slice(0, 32), fetch: never });
    await flush();
    assert.equal(t.m2w.mapReady('demo'), 0);
    await t.time.advance(61000);
    assert.equal(t.m2w.mapReady('demo'), 0);
    assert.equal(t.m2w.prefetch.urgent.timedOut, true);
});

test('a pinned working set survives ordinary cache eviction', async () => {
    const t = setup({ groups: '' });
    await flush();
    t.m2w.chunks.budget = 4;
    t.m2w.chunkCachePut(a, new Uint8Array([1, 2, 3, 4]));
    t.m2w.chunks.pinned.add(a);
    t.m2w.chunks.used.add(a);
    t.m2w.chunkCachePut(b, new Uint8Array([5, 6, 7, 8]));
    const c = 'c'.repeat(32) + '.bin';
    t.m2w.chunkCachePut(c, new Uint8Array([9]));
    assert.ok(t.m2w.chunks.map.has(a));
    assert.ok(!t.m2w.chunks.map.has(b));
});

test('staged startup defers gameplay groups until sign-in, then waits for RAM', async () => {
    const groups = ['boot 4 ' + a.slice(0, 32), 'meta 4 ' + b.slice(0, 32), 'motion 4 ' + b.slice(0, 32)].join('\n');
    const t = setup({ groups, start: false });
    t.m2w.startupStaged = true;
    t.start();
    await flush();
    assert.equal(t.calls.length, 0);
    vm.runInNewContext(fs.readFileSync(path.join(__dirname, '../compat/web_ux.js'), 'utf8'), {
        m2w: t.m2w, performance: { now: t.time.now }, setTimeout: t.time.setTimeout
    });
    let ready = false;
    const preparing = t.m2w.prepareLoginResources().then(() => { ready = true; });
    assert.equal(ready, false);
    await flush();
    await t.time.advance(100);
    await preparing;
    assert.equal(ready, true);
    assert.equal(t.calls.length, 2);
    assert.ok(t.m2w.chunks.map.has(a) && t.m2w.chunks.map.has(b));
});

test('a hanging group index times out and can be retried', async () => {
    let broken = true;
    const t = setup({ groupsFetch: () => broken ? never() : Promise.resolve({ ok: true, text: async () => 'boot 4 ' + a.slice(0, 32) }) });
    await flush();
    await t.time.advance(20000);
    assert.equal(t.m2w.prefetch.groups, null);
    assert.match(t.m2w.prefetch.groupError, /timeout/);
    broken = false;
    t.m2w.retryPrefetchFailed();
    await flush();
    assert.equal(t.m2w.prefetch.groupError, null);
    assert.ok(t.m2w.prefetch.groups.boot);
    assert.ok(t.m2w.chunks.map.has(a));
});

test('the bar reports a failed file and only counts startup disk hits', async () => {
    const time = clock();
    const node = () => ({ style: { display: 'none' }, handlers: {},
        addEventListener(name, fn) { this.handlers[name] = fn; }, appendChild() {} });
    const nodes = { '#m2w_download_text': node(), '#m2w_download_fill': node(), '#m2w_download_detail': node() };
    const bar = node(), button = node();
    bar.querySelector = name => nodes[name];
    const c = 'c'.repeat(32) + '.bin';
    const prefetch = { groups: { boot: { names: [a, b, c] } }, fetched: new Set([a, b]),
        failed: new Map([[c, 'HTTP 503']]), storageHits: new Set([a, b, 'other-map.bin']),
        fromStorage: 75, waiting: new Set() };
    let retries = 0;
    vm.runInNewContext(fs.readFileSync(path.join(__dirname, '../site/preload.js'), 'utf8'), {
        m2w: { config: { lang: 'tr' }, prefetch, retryPrefetchFailed() { ++retries; } },
        document: { createElement: tag => tag === 'button' ? button : bar, body: { appendChild() {} } },
        navigator: {}, Set, console, performance: { now: time.now }, setTimeout: time.setTimeout
    });
    await time.advance(1000);
    assert.match(nodes['#m2w_download_detail'].textContent, /2 \/ 3.*1 dosya indirilemedi.*2 diskten/);
    assert.equal(button.style.display, 'inline-block');
    button.handlers.click({ stopPropagation() {} });
    assert.equal(retries, 1);
    prefetch.fetched.add(c);
    prefetch.failed.clear();
    await time.advance(2000);
    assert.equal(bar.style.display, 'none');
});
