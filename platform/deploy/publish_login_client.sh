#!/usr/bin/env bash
set -euo pipefail
cd /home/m2web
exec 9>dev/client-build.lock
flock -n 9 || { echo 'A development build is running'; exit 1; }
python3 publish_engine_check.py kit/dist/site/corpus www/corpus
mkdir -p backups
backup=$(mktemp -d /home/m2web/backups/client-login-XXXXXXXX)
mkdir "$backup/site"
rsync -a --exclude=/corpus/ --exclude=/asan/ www/ "$backup/site/"
cp -p publish.sh "$backup/publish.sh.previous"
echo "BACKUP: $backup"
install -m 755 publish-login-candidate.sh publish.sh
if ! ./publish.sh --engine-only; then
    rsync -a --delete --exclude=/corpus/ --exclude=/asan/ "$backup/site/" www/
    cp -p "$backup/publish.sh.previous" publish.sh
    echo 'Publish failed; previous site and publisher restored' >&2
    exit 1
fi
cmp kit/dist/site/client.wasm www/client.wasm
cmp kit/dist/site/client.html www/client.html
echo 'PUBLISHED: matching public client; corpus unchanged; no service restart'
