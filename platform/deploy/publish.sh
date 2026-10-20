#!/bin/bash
set -euo pipefail
S=/home/m2web/kit/dist/site
for f in client.html client.js client.wasm client.data preload.js sw.js; do
    [ -s "$S/$f" ] || { echo "missing $f - not publishing"; exit 1; }
done
n=$(ls "$S/corpus" 2>/dev/null | wc -l)
[ "$n" -gt 1000 ] || { echo "corpus has $n files - not publishing"; exit 1; }
case "${1:-}" in
    --engine-only)
        # Safe only when the client references exactly the already-published corpus.
        python3 /home/m2web/publish_engine_check.py "$S/corpus" /home/m2web/www/corpus
        # Keep corpus, including its inode/mtime, entirely out of this sync.
        rsync -a --delete --exclude=/corpus/ --exclude=/asan/ --exclude=/client.html "$S/" /home/m2web/www/
        rsync -a "$S/client.html" /home/m2web/www/client.html
        ;;
    '')
        # The CDN goes first: a new client.html must never point at chunks it does not have yet.
        /home/m2web/publish_cdn.sh
        rsync -a --delete "$S/" /home/m2web/www/
        ;;
    *) echo 'usage: publish.sh [--engine-only]' >&2; exit 2 ;;
esac
echo SYNCED
