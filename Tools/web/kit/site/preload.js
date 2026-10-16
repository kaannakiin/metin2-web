// preload.js - a download bar in the corner while the game data comes.
// Loaded by site/client.html.
//
// The prefetch itself is compat/runtime.js (m2w.prefetchStart, groups.txt):
// the start-up groups from page load, then the map being entered. Here we
// only show `m2w.prefetch`; everything else is fetched on demand.
(function () {
    // --- Service Worker -----------------------------------------------------
    if ('serviceWorker' in navigator) {
        navigator.serviceWorker.register('sw.js').then(function (r) {
            console.log('[sw] registered, scope ' + r.scope);
        }).catch(function (e) {
            console.warn('[sw] no Service Worker (' + e + ') - chunks will come from the network on every start');
        });
    }

    // --- the corner bar ----------------------------------------------------
    var bar = document.createElement('div');
    bar.id = 'm2w_download';
    bar.style.cssText = 'position:fixed;right:10px;bottom:10px;z-index:20;min-width:230px;padding:8px 10px;' +
        'background:rgba(16,13,10,.85);border:1px solid #3a2f22;border-radius:6px;color:#e8d9b8;' +
        'font:12px/1.4 system-ui,sans-serif;pointer-events:none;display:none';
    bar.innerHTML = '<div id="m2w_download_text">Game data</div>' +
        '<div style="margin-top:5px;height:6px;background:#2a2218;border-radius:3px;overflow:hidden">' +
        '<div id="m2w_download_fill" style="height:100%;width:0;background:#c9a24a"></div></div>' +
        '<div id="m2w_download_detail" style="margin-top:3px;color:#9a8f7c;font-size:11px"></div>';
    document.body.appendChild(bar);
    var elText = bar.querySelector('#m2w_download_text');
    var elFill = bar.querySelector('#m2w_download_fill');
    var elDetail = bar.querySelector('#m2w_download_detail');
    var m2w = globalThis.m2w = globalThis.m2w || {};

    /// Shows the bar with `text`, the fill `fraction` (0..1) and a smaller `detail` line.
    function show(text, fraction, detail) {
        bar.style.display = 'block';
        elText.textContent = text;
        elFill.style.width = Math.round(Math.max(0, Math.min(1, fraction)) * 100) + '%';
        elDetail.textContent = detail || '';
    }

    // --- prefetch progress from compat --------------------------------------
    var TEXT = {
        tr: { start: 'Oyun verileri', map: 'Harita indiriliyor', ready: 'hazır', disk: 'diskten' },
        en: { start: 'Game data', map: 'Downloading the map', ready: 'ready', disk: 'from disk' }
    };
    /// Start-up groups done/total chunks, or null before groups.txt arrives.
    function startProgress(w) {
        if (!w.groups) return null;
        var done = 0, total = 0;
        ['meta', 'motion', 'boot'].forEach(function (name) {
            var g = w.groups[name];
            if (!g) return;
            total += g.names.length;
            g.names.forEach(function (n) { if (w.fetched.has(n) || (m2w.chunks && m2w.chunks.map.has(n))) ++done; });
        });
        return { done: done, total: total };
    }
    var hideAt = 0;
    /// Polls `m2w.prefetch` twice a second for the rest of the session.
    function watch() {
        var t = TEXT[(m2w.config && m2w.config.lang) === 'tr' ? 'tr' : 'en'];
        var w = m2w.prefetch;
        if (w && w.urgent && w.urgent.total) {
            show(t.map, w.urgent.done / w.urgent.total, w.urgent.done + ' / ' + w.urgent.total);
            hideAt = performance.now() + 1500;
        } else if (w && !w.disabled) {
            var s = startProgress(w);
            if (s && s.total && s.done < s.total) {
                show(t.start, s.done / s.total, s.done + ' / ' + s.total +
                     (w.fromStorage ? ' (' + w.fromStorage + ' ' + t.disk + ')' : ''));
                hideAt = performance.now() + 1500;
            } else if (bar.style.display !== 'none' && performance.now() > hideAt) {
                bar.style.display = 'none';
            }
        }
        setTimeout(watch, 500);
    }
    setTimeout(watch, 1000);
})();
