#!/usr/bin/env bash
set -euo pipefail
cd /home/m2web
exec 9>dev/client-build.lock
flock -n 9 || { echo 'Another client build is running'; exit 1; }
backup=/home/m2web/backups/options-Ltk1V6WH/site
test -s "$backup/client.html"
failed=$(mktemp -d /home/m2web/backups/options-failed-XXXXXXXX)
rsync -a --exclude=/corpus/ --exclude=/asan/ www/ "$failed/"
rsync -a --delete --exclude=/corpus/ --exclude=/asan/ --exclude=/client.html "$backup/" www/
rsync -a "$backup/client.html" www/client.html
python3 - "$backup" <<'PY'
from pathlib import Path
import hashlib
import sys
backup, live = Path(sys.argv[1]), Path('www')
count = 0
for path in backup.rglob('*'):
    if path.is_file():
        restored = live / path.relative_to(backup)
        assert hashlib.file_digest(path.open('rb'), 'sha256').digest() == hashlib.file_digest(restored.open('rb'), 'sha256').digest(), restored
        count += 1
print('OPTIONS ROLLBACK VERIFIED:', count, 'files')
PY
echo "FAILED PACKAGE SAVED: $failed"
echo "RESTORED PACKAGE: $backup"
