#!/usr/bin/env bash
# Back up, build and publish the options layout fix without service changes.
set -euo pipefail
cd /home/m2web
exec 9>dev/client-build.lock
flock -n 9 || { echo 'Another client build is running'; exit 1; }
test "$(cat dev/protocol)" = source
mkdir -p backups
backup=$(mktemp -d /home/m2web/backups/options-XXXXXXXX)
mkdir -p "$backup/site" "$backup/inputs"
rsync -a --exclude=/corpus/ --exclude=/asan/ www/ "$backup/site/"
cp -p kit/tools/uiscript_from_client.py "$backup/inputs/uiscript_from_client.py"
printf '%s\n' "$backup" >dev/options-release
echo "OPTIONS BACKUP: $backup"
cp options_layout_tool.py kit/tools/uiscript_from_client.py
cp test_uiscript_from_client.py kit/tools/test_uiscript_from_client.py
docker exec -e M2W_OPTIONS_BASELINE_SITE="/work/${backup#/home/m2web/}/site" \
    m2web-build bash /work/release_options_build.sh
python3 publish_engine_check.py kit/dist/site/corpus www/corpus
python3 - "$backup/site" <<'PY'
from pathlib import Path
import hashlib
import json
import sys

def package_files(base):
    script = (base / 'client.js').read_text()
    offset = script.find('{"files":')
    assert offset >= 0, 'Missing Emscripten file index'
    metadata = json.JSONDecoder().raw_decode(script[offset:])[0]
    data = (base / 'client.data').read_bytes()
    return {row['filename']: hashlib.sha256(data[row['start']:row['end']]).digest()
            for row in metadata['files']}

baseline, candidate = Path(sys.argv[1]), Path('kit/dist/site')
before, after = package_files(baseline), package_files(candidate)
assert not (before.keys() - after.keys()), 'Existing package files removed'
changed = [name for name in before if before[name] != after[name]]
assert not changed, 'Existing package files changed: ' + repr(changed)
expected = {'/UIScript/advanced_game_options/game_option_%d.py' % i for i in range(7)}
expected.add('/UIScript/advanced_game_options/game_option_filter.py')
assert after.keys() - before.keys() == expected, 'Unexpected added package files'
assert hashlib.file_digest((baseline / 'client.wasm').open('rb'), 'sha256').digest() == hashlib.file_digest((candidate / 'client.wasm').open('rb'), 'sha256').digest(), 'Engine changed'
print('OPTIONS SCOPE: existing files unchanged; only 8 options layouts added')
PY
python3 - "$backup/site" <<'PY'
from pathlib import Path
import hashlib
import sys
old, live = Path(sys.argv[1]), Path('www')
files = [p for p in old.rglob('*') if p.is_file()]
for path in files:
    current = live / path.relative_to(old)
    assert current.is_file(), current
    assert hashlib.file_digest(path.open('rb'), 'sha256').digest() == hashlib.file_digest(current.open('rb'), 'sha256').digest(), 'Concurrent publish: ' + str(current)
print('LIVE BASELINE: unchanged since options backup')
PY
rollback() {
    rsync -a --delete --exclude=/corpus/ --exclude=/asan/ --exclude=/client.html "$backup/site/" www/
    rsync -a "$backup/site/client.html" www/client.html
    echo "OPTIONS ROLLBACK: $backup" >&2
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
print('OPTIONS PUBLIC: %d candidate/live hashes match' % len(names))
PY
trap - ERR
echo "OPTIONS PUBLISHED; rollback site: $backup/site"
