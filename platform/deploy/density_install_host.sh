#!/usr/bin/env bash
set -euo pipefail
id=${1:?release id}
action=${2:?prepare or install}
[[ "$id" =~ ^[0-9]{8}-[0-9]{6}$ ]] || exit 2
[[ "$action" == prepare || "$action" == install ]] || exit 2
cd "/home/m2web/density-$id"
exec 9>/home/m2web/dev/client-build.lock
flock -n 9 || { echo 'Another build or install is running'; exit 1; }
test ! -e INSTALLED
sha256sum --quiet -c payload.sha256
python3 - <<'PY'
import re, tarfile
with tarfile.open('payload.tar.gz') as archive:
    members = archive.getmembers()
    allowed = {'files.txt', 'expected.sha256', 'candidate.sha256', 'report.json'}
    assert len(members) == 17 and len({item.name for item in members}) == 17
    assert all(item.isfile() and (item.name in allowed or re.fullmatch(r'input/map/[a-z0-9_]+/stone\.txt', item.name)) for item in members)
PY
stage="/usr/metin2-density-$id"
vm=(ssh -o BatchMode=yes -i /root/.ssh/metin2_vm root@192.168.122.10)
"${vm[@]}" "mkdir -m 700 '$stage'"
scp -q -i /root/.ssh/metin2_vm payload.tar.gz density_install_vm.sh "root@192.168.122.10:$stage/"
"${vm[@]}" "cd '$stage' && tar -xzf payload.tar.gz && sh density_install_vm.sh prepare '$stage'"
touch READY
if [[ "$action" == install ]]; then
    "${vm[@]}" "sh '$stage/density_install_vm.sh' install '$stage'"
    touch INSTALLED
fi
echo "DENSITY $action COMPLETE: $id"
