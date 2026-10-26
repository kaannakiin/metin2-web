#!/usr/bin/env bash
# Restore only the site replaced by publish_text_encoding.sh.
set -euo pipefail
cd /home/m2web
exec 9>dev/client-build.lock
flock -n 9 || { echo 'A client build is running'; exit 1; }
backup=/home/m2web/backups/text-encoding-7pcQ09rg/site
test -s "$backup/client.html"
test -s "$backup/client.wasm"
test "$(sha256sum www/client.wasm | cut -d ' ' -f 1)" = 7bd48809cd6e2f6dc266193df9ae42bf833e1523473acdbe06dfa170298d10e7
rsync -a --delete --exclude=/corpus/ --exclude=/asan/ --exclude=/client.html "$backup/" www/
rsync -a "$backup/client.html" www/client.html
cmp "$backup/client.wasm" www/client.wasm
cmp "$backup/client.data" www/client.data
cmp "$backup/client.html" www/client.html
echo 'ROLLED BACK: previous site restored; corpus and services unchanged'
sha256sum www/client.wasm
