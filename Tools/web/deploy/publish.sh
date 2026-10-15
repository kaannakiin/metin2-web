#!/bin/bash
set -euo pipefail
S=/home/m2web/kit/dist/site
for f in client.html client.js client.wasm client.data preload.js sw.js; do
    [ -s "$S/$f" ] || { echo "missing $f - not publishing"; exit 1; }
done
n=$(ls "$S/corpus" 2>/dev/null | wc -l)
[ "$n" -gt 1000 ] || { echo "corpus has $n files - not publishing"; exit 1; }
rsync -a --delete "$S/" /home/m2web/www/
echo SYNCED
