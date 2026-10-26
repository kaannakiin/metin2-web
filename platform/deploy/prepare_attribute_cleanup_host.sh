#!/usr/bin/env bash
# Prepare only: compare source, compile quest and inspect approved item rows.
set -euo pipefail
cd /home/m2web
exec 9>dev/client-build.lock
flock -n 9 || { echo 'Another release is running'; exit 1; }
python3 - <<'PY'
from pathlib import Path
import subprocess
command = ['ssh', '-n', '-o', 'BatchMode=yes', '-i', '/root/.ssh/metin2_vm',
           'root@192.168.122.10', 'cat /usr/home/share/locale/europe/quest/quest_tr/_npc_talk_mission/welcome.lua']
old = subprocess.check_output(command)
new = Path('cleanup_welcome.lua').read_bytes()
assert old.count(b',63,10') == 3
assert new == old.replace(b',63,10', b''), 'Unrelated welcome source changes'
print('WELCOME SCOPE VERIFIED: only the 3 forced monster-bonus pairs removed')
PY
scp -q -o BatchMode=yes -i /root/.ssh/metin2_vm \
    cleanup_invalid_attributes_vm.sh cleanup_welcome.lua root@192.168.122.10:/usr/home/
ssh -n -o BatchMode=yes -i /root/.ssh/metin2_vm root@192.168.122.10 \
    'sh /usr/home/cleanup_invalid_attributes_vm.sh prepare'
python3 cleanup_invalid_attributes.py
echo 'ITEM ATTRIBUTE CLEANUP READY; live items and services unchanged'
