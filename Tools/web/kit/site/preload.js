// preload.js - a download bar in the corner for the essential game data.
// Loaded by site/client.html.
//
// `corpus/order.txt` (the recorded order of use: login + village) is fetched by
// `m2w_prefetch_start` in compat/webfs_web.cpp (a window in memory + Cache
// Storage); here we only show its progress. Everything else is fetched on
// demand when the game needs it - nothing downloads the whole corpus.
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
    var lastDone = -1, lastChange = 0;
    /// Polls `m2w.prefetch` every 500 ms until it is done, has stalled for
    /// 10 s, or turns out not to exist (no order.txt).
    function watch() {
        var w = m2w.prefetch;
        if (w && w.total > 0) {
            if (w.done !== lastDone) { lastDone = w.done; lastChange = performance.now(); }
            // The prefetch waits for room in memory (a sliding window) and stalls
            // when the game leaves the recorded path; the game then fetches on demand.
            var bStalled = performance.now() - lastChange > 10000;
            if (w.done < w.total && !bStalled) {
                show('Essential data: ' + w.done + ' / ' + w.total, w.done / w.total,
                     (w.fromStorage ? w.fromStorage + ' from disk' : ''));
            } else {
                show('Essential data: ready', 1, '');
                setTimeout(function () { bar.style.display = 'none'; }, 1500);
                return;
            }
        } else if (!w && performance.now() > 20000) {
            return;
        }
        setTimeout(watch, 500);
    }
    setTimeout(watch, 1000);
})();
