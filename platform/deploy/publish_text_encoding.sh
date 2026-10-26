#!/usr/bin/env bash
# Publish the already-built text encoding candidate, with rollback and no VM restart.
set -euo pipefail
cd /home/m2web
expected_wasm=${1:?Pass the SHA-256 of the tested preview engine}
[[ "$expected_wasm" =~ ^[a-f0-9]{64}$ ]] || { echo 'Invalid engine hash'; exit 2; }
exec 9>dev/client-build.lock
flock -n 9 || { echo 'A development build is running'; exit 1; }
test "$(cat dev/protocol)" = source
test "$(sha256sum kit/build/port/client.wasm | cut -d ' ' -f 1)" = "$expected_wasm"
cmp kit/build/port/client.wasm dev/site/current/client.wasm

# Exercise the actual generated import hook in CPython 3.13 before packaging.
docker exec -e M2W_BOOT_SYSTEM=/work/kit/build/port/scripts3/system.py \
    m2web-build python3.13 -B -m unittest discover -s /work/kit/tools -p test_python_startup.py

# Build a public package from the engine and UI inputs. package.py rebuilds
# data with --no-private; never copy the private preview HTML into production.
log=/home/m2web/dev/logs/text-encoding-package.log
if ! docker exec m2web-build bash /work/gameplay_client_build.sh >"$log" 2>&1; then
    tail -20 "$log"
    exit 1
fi
grep -E 'TEXT ENCODING:|CANDIDATE PACKAGE:|DETECTOR UI:|UNEXPECTED:' "$log" || true
test "$(sha256sum kit/dist/site/client.wasm | cut -d ' ' -f 1)" = "$expected_wasm"
python3 - <<'PY'
from pathlib import Path
import json
kit = Path('/home/m2web/kit')
for name in ('textcodec.py', 'text_encoding.json', 'text_labels.json'):
    assert (kit / 'compat' / name).read_bytes() == (kit / 'build/port/data' / name).read_bytes(), name
root = kit / 'build/port/scripts3'
system = (root / 'system.py').read_text()
assert 'or name == "collections" or hasattr(sys.modules.get(name), "__path__")' in system
assert not (kit / 'build/port/data/collections.py').exists()
mini = next(p for p in root.iterdir() if p.name.lower() == 'uiminimap.py').read_text()
for key in ('BATTLEPASS_SELECT_PASS', 'BATTLEPASS_FREE', 'BATTLEPASS_PREMIUM'):
    assert 'uiScriptLocale.' + key in mini, key
labels = json.loads((kit / 'compat/text_labels.json').read_text())
assert len(labels) == 11
assert labels['tr']['BATTLEPASS_SELECT_PASS'] == 'Savaş Bileti Seçiniz'
assert labels['tr']['BATTLEPASS_FREE'] == 'Ücretsiz'
assert 'if (pythonSource)' in (kit / 'compat/pack_text.h').read_text()
assert 'retryPrefetchFailed' in (kit / 'dist/site/client.js').read_text()
assert (kit / 'site/preload.js').read_bytes() == (kit / 'dist/site/preload.js').read_bytes()
print('TEXT CANDIDATE: shared codec and all 11 label dictionaries match package inputs')
PY
python3 publish_engine_check.py kit/dist/site/corpus www/corpus

mkdir -p backups
backup=$(mktemp -d /home/m2web/backups/text-encoding-XXXXXXXX)
mkdir "$backup/site"
rsync -a --exclude=/corpus/ --exclude=/asan/ www/ "$backup/site/"
echo "BACKUP: $backup"
rollback() {
    rsync -a --delete --exclude=/corpus/ --exclude=/asan/ "$backup/site/" www/
    echo "Publish failed; previous site restored from $backup" >&2
}
trap rollback ERR
bash publish.sh --engine-only
python3 - <<'PY'
from pathlib import Path
import hashlib
candidate = Path('/home/m2web/kit/dist/site')
live = Path('/home/m2web/www')
names = ['client.html', 'client.js', 'client.wasm', 'client.data', 'preload.js', 'sw.js']
names += sorted(p.name for p in candidate.glob('client.locale_*') if p.is_file())
def digest(path):
    h = hashlib.sha256()
    with path.open('rb') as source:
        for block in iter(lambda: source.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()
for name in names:
    assert digest(candidate / name) == digest(live / name), name
print('PUBLIC FILES: %d candidate/live hashes match' % len(names))
print('LIVE WASM:', digest(live / 'client.wasm'))
PY
trap - ERR
echo "PUBLISHED: text encoding; corpus unchanged; no service restart; backup $backup"
