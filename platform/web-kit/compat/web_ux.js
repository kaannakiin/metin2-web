// Browser-only login preparation and username storage. No account passwords
// cross this bridge. Included after runtime.js, before Emscripten preRun.

/// Legacy Python windows are positioned once against SCREEN_WIDTH/HEIGHT.
/// Preserve that logical desktop and fit its complete rectangle to the browser
/// instead of shrinking the desktop underneath inventory/taskbar coordinates.
m2w.fitViewportRect = function (width, height, viewportWidth, viewportHeight, left, top) {
    var scale = Math.min(viewportWidth / width, viewportHeight / height);
    return { width: width * scale, height: height * scale,
             left: (left || 0) + (viewportWidth - width * scale) / 2,
             top: (top || 0) + (viewportHeight - height * scale) / 2 };
};

m2w.startViewportFit = function () {
    if (m2w.viewportFitState || !globalThis.document) return;
    var canvas = Module.canvas;
    if (!canvas) return;
    var width = m2w.windowSize(0), height = m2w.windowSize(1);
    if (!(width > 0 && height > 0)) throw new Error('Browser viewport unavailable');
    var scale = m2w.uiScale(), cap = m2w.maxBuffer || { w: 0, h: 0 };
    // Allow the inventory's 573 px board plus the taskbar to fit when the
    // browser itself starts small. Explicit rendering caps remain respected.
    width = Math.max(width, Math.floor(Math.min(800, cap.w > 0 ? cap.w / scale : 800)));
    height = Math.max(height, Math.floor(Math.min(640, cap.h > 0 ? cap.h / scale : 640)));
    var state = m2w.viewportFitState = { width: width, height: height, rect: null };
    var previousCanvasState = m2w.canvasState;
    m2w.windowSize = function (isHeight) { return isHeight ? state.height : state.width; };
    m2w.canvasState = function (what) {
        if (what === 2) return previousCanvasState(what);
        return what === 1 ? state.height : state.width;
    };
    m2w.fitCanvasToViewport = function () {
        var visual = globalThis.visualViewport;
        var w = visual && visual.width > 0 ? visual.width : globalThis.innerWidth;
        var h = visual && visual.height > 0 ? visual.height : globalThis.innerHeight;
        if (!(w > 0 && h > 0)) return;
        var r = m2w.fitViewportRect(state.width, state.height, w, h,
                                  visual && visual.offsetLeft, visual && visual.offsetTop);
        state.rect = r;
        canvas.style.position = 'absolute';
        canvas.style.left = r.left + 'px';
        canvas.style.top = r.top + 'px';
        canvas.style.width = r.width + 'px';
        canvas.style.height = r.height + 'px';
        // Mouse input already converts through the live canvas rectangle,
        // including its new offsets, into buffer / GUI-scale coordinates.
    };
    globalThis.addEventListener('resize', m2w.fitCanvasToViewport);
    document.addEventListener('fullscreenchange', m2w.fitCanvasToViewport);
    if (globalThis.visualViewport)
        globalThis.visualViewport.addEventListener('resize', m2w.fitCanvasToViewport);
    m2w.fitCanvasToViewport();
};

m2w.gameKeyEvent = function (e) {
    var target = e.target;
    if (target && target.closest && target.closest('input,textarea,select,button,a,details,[contenteditable="true"]')) return false;
    if (e.metaKey || (e.ctrlKey && /^(l|r|t|w|n|f|p|d|\+|-|0)$/i.test(e.key))) return false;
    return true;
};

/// Derive the login working set from this exact manifest. Chunk boundaries,
/// including short chunks and files spanning chunks, come from the manifest.
m2w.loginManifest = function (buffer) {
    var data = new DataView(buffer), raw = new Uint8Array(buffer), pos = 28;
    if (raw.length < 28 || String.fromCharCode.apply(null, raw.subarray(0, 4)) !== 'M2WF' || data.getUint32(4, true) !== 1)
        throw new Error('Invalid corpus manifest');
    var chunks = [], names = new Set(), count = data.getUint32(12, true);
    var packs = data.getUint32(16, true), files = data.getUint32(20, true);
    var decoder = new TextDecoder('utf-8', { fatal: true });
    for (var i = 0; i < count; ++i) {
        var hash = Array.from(raw.subarray(pos, pos + 16), function (b) { return b.toString(16).padStart(2, '0'); }).join('');
        chunks.push({ name: hash + '.bin', size: data.getUint32(pos + 16, true) });
        pos += 20;
    }
    for (var j = 0; j < packs; ++j) pos += 2 + data.getUint16(pos, true);
    var selected = 0;
    for (var k = 0; k < files; ++k) {
        var chunk = data.getUint32(pos + 2, true), offset = data.getUint32(pos + 6, true);
        var size = data.getUint32(pos + 10, true), length = data.getUint16(pos + 14, true);
        pos += 16;
        var name = decoder.decode(raw.subarray(pos, pos + length)).toLowerCase();
        pos += length;
        var login = /^ymir work\/ui\/intro\/login\/(background|input_(down|norm|over)|account\/(account_board|button_(delete|save)_(down|norm|over)|flag)|arrow\/arrow_down_(down|norm|over)|channel\/(channel_board|offline|online)|connect\/(button_login_(down|norm|over)|input|server_list|server_select))\.png$/.test(name);
        login = login || /^ymir work\/ui\/(intro\/common\/exit_button_0[123]\.png$|game\/flags\/flag_[a-z]{2}_(down|norm|over)\.tga$|cursor(?:\.dds$|\/)|pattern\/(board_|thinboardnew\/)|public\/acceptbutton0[012]\.sub$|public_newbutton_01\.dds$)/.test(name);
        login = login || /^ymir work\/special\/spheremap(?:01)?\.jpg$/.test(name);
        login = login || /^(bgm\/login_window\.mp3|sound\/ui\/(click|loginok)\.wav)$/.test(name);
        login = login || /^ymir work\/effect\/etc\/(dropitem\/dropitem|forked_load\/victory|masic_camp\/masic_camp_(loop|vanish))\.mse$/.test(name);
        if (!login) continue;
        ++selected;
        while (size > 0) {
            if (!chunks[chunk] || offset >= chunks[chunk].size) throw new Error('Invalid login file span');
            names.add(chunks[chunk].name);
            var take = Math.min(size, chunks[chunk].size - offset);
            size -= take;
            offset = 0;
            ++chunk;
        }
    }
    if (pos !== raw.length || !selected || !names.size) throw new Error('Incomplete login manifest');
    return { chunks: chunks, names: names, files: selected };
};

m2w.prepareLoginResources = function () {
    var p = m2w.prefetch, state = m2w.chunks;
    if (!p || !state) return Promise.reject(new Error('Client preparation not ready'));
    if (!p.groups && m2w.reloadGroups) m2w.reloadGroups();
    var login = p.login = { names: new Set(), total: 0, done: 0, failed: 0 };
    return new Promise(function (resolve, reject) {
        var started = performance.now(), queued = false;
        function check() {
            if (p.groupError) { login.failed = 1; reject(new Error('Game index unavailable')); return; }
            if (p.groups && !queued) {
                var bytes = 0;
                for (var i = 0; i < 3; ++i) {
                    var group = p.groups[['boot', 'meta', 'motion'][i]];
                    if (!group) { reject(new Error('Missing startup group')); return; }
                    group.names.forEach(function (n) { login.names.add(n); });
                    bytes += group.bytes || 0;
                }
                if (bytes > state.budget) { reject(new Error('Startup exceeds memory budget')); return; }
                login.total = login.names.size;
                state.pinned = new Set(login.names);
                m2w.retryPrefetchFailed();
                ['motion', 'meta', 'boot'].forEach(function (g) { m2w.want(g, true); });
                queued = true;
            }
            login.done = 0;
            login.failed = 0;
            login.names.forEach(function (n) {
                if (state.map.has(n)) ++login.done;
                else if (p.failed.has(n)) ++login.failed;
            });
            if (queued && login.done === login.total) { p.login = null; resolve(); return; }
            if (login.failed || performance.now() - started > 120000) {
                login.failed = Math.max(login.failed, 1);
                reject(new Error('Game data could not be prepared; retry the download'));
                return;
            }
            setTimeout(check, 100);
        }
        check();
    });
};

m2w.startBrowserBridge = function () {
    var fs = Module.FS, handled = null, key = 'm2w.usernames.v1';
    var state = { accounts: ['', '', '', ''], canRemember: false };
    function clean(values) {
        return [0, 1, 2, 3].map(function (i) {
            return values && typeof values[i] === 'string' && /^[A-Za-z0-9_]{1,30}$/.test(values[i]) ? values[i] : '';
        });
    }
    function store(values) {
        var text = JSON.stringify(clean(values));
        localStorage.setItem(key, text);
        if (localStorage.getItem(key) !== text) throw new Error('Username storage unavailable');
        return JSON.parse(text);
    }
    try {
        var existing = localStorage.getItem(key);
        state.accounts = clean(existing ? JSON.parse(existing) : []);
        // Probe the actual key without keeping unrelated test entries.
        state.accounts = store(state.accounts);
        state.canRemember = true;
    } catch (e) { }
    function publish() { fs.writeFile('/m2w_browser_state', JSON.stringify(state)); }
    function reply(id, ok) { fs.writeFile('/m2w_browser_reply', JSON.stringify({ id: id, ok: ok })); }
    publish();
    m2w.browserBridgeTimer = setInterval(function () {
        var command;
        try { command = JSON.parse(fs.readFile('/m2w_browser_request', { encoding: 'utf8' })); } catch (e) { return; }
        if (!command || typeof command.id !== 'string' || command.id === handled) return;
        handled = command.id;
        if (command.action === 'prepare_login') {
            m2w.prepareLoginResources().then(function () { reply(command.id, true); }, function () { reply(command.id, false); });
            return;
        }
        try {
            if (!state.canRemember || !Number.isInteger(command.slot) || command.slot < 0 || command.slot > 3)
                throw new Error('Invalid username slot');
            var next = state.accounts.slice();
            if (command.action === 'forget') next[command.slot] = '';
            else if (command.action === 'remember' && typeof command.login === 'string' && /^[A-Za-z0-9_]{1,30}$/.test(command.login))
                next[command.slot] = command.login;
            else throw new Error('Invalid username action');
            state.accounts = store(next);
            publish();
            reply(command.id, true);
        } catch (e) { reply(command.id, false); }
    }, 100);
};

m2w.prepareStartup = function () {
    m2w.startViewportFit();
    m2w.startupStaged = true;
    m2w.chunkCacheStart(m2w.corpusBudget());
    var base = m2w.corpusUrl(), state = m2w.chunks;
    m2w.startupProgress = { done: 0, total: 0 };
    var controller = new AbortController();
    return m2w.chunkTask(function () {
        return fetch(base + 'manifest.bin', { cache: 'no-cache', signal: controller.signal }).then(function (r) {
            if (!r.ok) throw new Error('Manifest HTTP ' + r.status);
            return r.arrayBuffer();
        });
    }, 20000, 'startup manifest', controller).then(function (buffer) {
        var menu = m2w.loginManifest(buffer);
        m2w.startupManifest = new Uint8Array(buffer);
        m2w.corpus.all = menu.chunks.map(function (c) { return c.name.slice(0, 32); });
        m2w.prefetchStart(base);
        var required = menu.chunks.filter(function (c) { return menu.names.has(c.name); });
        state.pinned = new Set(menu.names);
        m2w.startupProgress.total = required.length;
        var next = 0;
        function worker() {
            if (next >= required.length) return Promise.resolve();
            var chunk = required[next++];
            if (state.map.has(chunk.name)) { ++m2w.startupProgress.done; return worker(); }
            return state.storage.then(function (storage) {
                return m2w.loadChunk(base + chunk.name, storage);
            }).then(function (result) {
                if (result.buffer.byteLength !== chunk.size) throw new Error('Invalid startup chunk length');
                m2w.chunkCachePut(chunk.name, new Uint8Array(result.buffer));
                ++m2w.startupProgress.done;
                return worker();
            });
        }
        return Promise.all([worker(), worker(), worker()]);
    }).then(function () {
        m2w.startupProgress = null;
        m2w.startBrowserBridge();
    });
};
