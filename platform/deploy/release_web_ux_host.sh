#!/usr/bin/env bash
# Host-side release of the web UX candidate. Leaves corpus, VM and services alone.
set -euo pipefail
cd /home/m2web
exec 9>dev/client-build.lock
flock -n 9 || { echo 'Another client build is running'; exit 1; }
state=dev/web-ux-release
case ${1:-} in
    prepare)
        mkdir -p backups
        backup=$(mktemp -d /home/m2web/backups/web-ux-XXXXXXXX)
        mkdir -p "$backup/site" "$backup/inputs"
        rsync -a --exclude=/corpus/ --exclude=/asan/ www/ "$backup/site/"
        for file in compat/runtime.js compat/web_ux.js compat/web_ux.py \
            site/client.html site/preload.js tools/script_patches.py \
            tools/build_client_data.py tools/link_client.py tools/test_prefetch.js \
            tools/test_web_ux.js tools/test_web_ux.py; do
            if [ -f "kit/$file" ]; then
                mkdir -p "$backup/inputs/$(dirname "$file")"
                cp -p "kit/$file" "$backup/inputs/$file"
            fi
        done
        printf '%s\n' "$backup" >"$state"
        sha256sum www/client.wasm | cut -d ' ' -f 1 >"$backup/previous-wasm"
        echo "WEB UX BACKUP: $backup"
        ;;
    build)
        test -s "$state"
        test "$(cat dev/protocol)" = source
        docker exec m2web-build bash /work/release_web_ux_build.sh
        python3 publish_engine_check.py kit/dist/site/corpus www/corpus
        sha256sum kit/dist/site/client.wasm
        ;;
    publish)
        backup=$(cat "$state")
        test -d "$backup/site"
        test "$(sha256sum www/client.wasm | cut -d ' ' -f 1)" = "$(cat "$backup/previous-wasm")" || {
            echo 'Live engine changed after backup; prepare a fresh release'; exit 1;
        }
        python3 - "$backup/site" <<'PY'
from pathlib import Path
import hashlib
import sys
old, live = Path(sys.argv[1]), Path('www')
names = ['client.html', 'client.js', 'client.wasm', 'client.data', 'preload.js', 'sw.js']
names += sorted(p.name for p in old.glob('client.locale_*') if p.is_file())
for name in names:
    assert hashlib.file_digest((old / name).open('rb'), 'sha256').digest() == hashlib.file_digest((live / name).open('rb'), 'sha256').digest(), 'Concurrent publish: ' + name
print('LIVE BASELINE: unchanged since release backup')
PY
        python3 publish_engine_check.py kit/dist/site/corpus www/corpus
        rollback() {
            rsync -a --delete --exclude=/corpus/ --exclude=/asan/ "$backup/site/" www/
            echo "WEB UX ROLLBACK: $backup" >&2
        }
        trap rollback ERR
        bash publish.sh --engine-only
        python3 - <<'PY'
from pathlib import Path
import hashlib
candidate, live = Path('kit/dist/site'), Path('www')
names = ['client.html', 'client.js', 'client.wasm', 'client.data', 'preload.js', 'sw.js']
names += sorted(p.name for p in candidate.glob('client.locale_*') if p.is_file())
for name in names:
    assert hashlib.file_digest((candidate / name).open('rb'), 'sha256').digest() == hashlib.file_digest((live / name).open('rb'), 'sha256').digest(), name
print('WEB UX PUBLIC: %d candidate/live hashes match' % len(names))
PY
        trap - ERR
        echo "WEB UX PUBLISHED; rollback site: $backup/site"
        ;;
    *) echo 'usage: release_web_ux_host.sh prepare|build|publish' >&2; exit 2 ;;
esac
