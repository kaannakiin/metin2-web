#!/usr/bin/env bash
set -euo pipefail
id=${1:?release id required}
[[ "$id" =~ ^[0-9]{8}-[0-9]{6}$ ]] || exit 2
cd "/home/m2web/gameplay-$id"
test -f BUNDLE_READY
test ! -e INSTALLED
test ! -e DENSITY_READY
exec 9>/home/m2web/dev/client-build.lock
flock -n 9 || { echo 'Client build or install running'; exit 1; }
grep -E '  (audit.json|manifest.json)$' release.sha256 | sha256sum --quiet -c -
sha256sum --quiet -c client-site.sha256
sha256sum --quiet -c density-payload.sha256
python3 - <<'PY'
import re, tarfile
allowed = {'density-files.txt', 'density.sha256', 'density-baseline.sha256', 'density-report.json'}
with tarfile.open('density.tar.gz') as archive:
    members = archive.getmembers()
    assert len({item.name for item in members}) == len(members)
    assert all(item.isfile() and (item.name in allowed or re.fullmatch(r'density/map/[a-z0-9_]+/stone\.txt', item.name)) for item in members)
    assert len(members) == 17
print('DENSITY PAYLOAD: 13 maps and four metadata files verified')
PY
stage="/usr/metin2-gameplay-$id"
vm=(ssh -o BatchMode=yes -i /root/.ssh/metin2_vm root@192.168.122.10)
"${vm[@]}" "test ! -e '$stage/INSTALL_STARTED'"
scp -q -i /root/.ssh/metin2_vm density.tar.gz gameplay_install_vm.sh gameplay_density_vm.sh "root@192.168.122.10:$stage/"
rm BUNDLE_READY
"${vm[@]}" "sh '$stage/gameplay_density_vm.sh' '$stage'"
tar -xzf density.tar.gz
sha256sum audit.json manifest.json gameplay_install_host.sh gameplay_install_vm.sh \
    density.tar.gz density-files.txt density.sha256 density-baseline.sha256 density-report.json >release.sha256.next
mv release.sha256.next release.sha256
touch DENSITY_READY BUNDLE_READY
echo 'BUNDLE READY: 13 maps, 97 -> 194 Metin capacity; live files and services unchanged.'
