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
    var retry = document.createElement('button');
    retry.style.cssText = 'display:none;margin-top:5px;pointer-events:auto;cursor:pointer;' +
        'background:#33291a;border:1px solid #8e764c;border-radius:3px;color:#e8d9b8;padding:3px 8px';
    bar.appendChild(retry);
    retry.addEventListener('mousedown', function (event) { event.stopPropagation(); });
    retry.addEventListener('click', function (event) {
        event.stopPropagation();
        if (m2w.retryPrefetchFailed) m2w.retryPrefetchFailed();
        retry.style.display = 'none';
    });
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
        tr: { login: 'Giriş ekranı hazırlanıyor', start: 'Oyun verileri hazırlanıyor', map: 'Harita indiriliyor', ready: 'hazır', disk: 'diskten',
              failed: 'dosya indirilemedi', retry: 'Tekrar dene', retrying: 'yeniden deneniyor' },
        en: { login: 'Preparing sign-in screen', start: 'Preparing game data', map: 'Downloading the map', ready: 'ready', disk: 'from disk',
              failed: 'file(s) unavailable', retry: 'Retry', retrying: 'retrying' }
    };
    /// Start-up groups done/total chunks, or null before groups.txt arrives.
    function startProgress(w) {
        if (!w.groups) return null;
        var done = 0, total = 0, failed = 0, disk = 0;
        var seen = new Set();
        ['boot', 'meta', 'motion'].forEach(function (name) {
            var g = w.groups[name];
            if (!g) return;
            g.names.forEach(function (n) {
                if (seen.has(n)) return;
                seen.add(n);
                ++total;
                var ready = w.fetched.has(n) || (m2w.chunks && m2w.chunks.map.has(n));
                if (ready) ++done;
                if (!ready && w.failed && w.failed.has(n)) ++failed;
                if (ready && w.storageHits && w.storageHits.has(n)) ++disk;
            });
        });
        return { done: done, total: total, failed: failed, disk: disk };
    }
    var hideAt = 0;
    /// Polls `m2w.prefetch` twice a second for the rest of the session.
    function watch() {
        var t = TEXT[(m2w.config && m2w.config.lang) === 'tr' ? 'tr' : 'en'];
        var w = m2w.prefetch;
        retry.textContent = t.retry;
        retry.style.display = 'none';
        if (m2w.startupProgress) {
            var initial = m2w.startupProgress;
            show(t.login, initial.total ? initial.done / initial.total : 0, initial.total ? initial.done + ' / ' + initial.total : '');
            hideAt = performance.now() + 1500;
        } else if (w && w.login) {
            show(t.start, w.login.total ? w.login.done / w.login.total : 0,
                 w.login.done + ' / ' + w.login.total + (w.login.failed ? ' — ' + t.failed : ''));
            if (w.login.failed) retry.style.display = 'inline-block';
            hideAt = performance.now() + 1500;
        } else if (w && w.urgent && w.urgent.total) {
            show(t.map, w.urgent.done / w.urgent.total, w.urgent.done + ' / ' + w.urgent.total);
            var missing = w.urgent.names && w.failed && Array.from(w.urgent.names).some(function (n) { return w.failed.has(n); });
            if (missing || w.urgent.timedOut) {
                elDetail.textContent += ' — ' + t.failed;
                retry.style.display = 'inline-block';
            }
            hideAt = performance.now() + 1500;
        } else if (w && !w.disabled && !m2w.startupStaged) {
            var s = startProgress(w);
            if (s && s.total && s.done < s.total) {
                show(t.start, s.done / s.total, s.done + ' / ' + s.total +
                     (s.failed ? ' — ' + s.failed + ' ' + t.failed :
                      (w.waiting && w.waiting.size ? ' — ' + t.retrying : '')) +
                     (s.disk ? ' (' + s.disk + ' ' + t.disk + ')' : ''));
                if (s.failed) retry.style.display = 'inline-block';
                hideAt = performance.now() + 1500;
            } else if (bar.style.display !== 'none' && performance.now() > hideAt) {
                bar.style.display = 'none';
            }
        } else if (bar.style.display !== 'none' && performance.now() > hideAt) {
            bar.style.display = 'none';
        }
        setTimeout(watch, 500);
    }
    setTimeout(watch, 1000);
})();
