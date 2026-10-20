#!/usr/bin/env bash
set -euo pipefail
id=${1:?release id required}
[[ "$id" =~ ^[0-9]{8}-[0-9]{6}$ ]] || exit 2
cd "/home/m2web/gameplay-$id"
test -f BUNDLE_READY
test ! -e INSTALLED
exec 9>/home/m2web/dev/client-build.lock
flock -n 9 || { echo 'Client build running'; exit 1; }
grep -E '  (audit.json|manifest.json)$' release.sha256 | sha256sum --quiet -c -
vm=(ssh -o BatchMode=yes -i /root/.ssh/metin2_vm root@192.168.122.10)
"${vm[@]}" "test ! -e '/usr/metin2-gameplay-$id/INSTALL_STARTED'"
scp -q -i /root/.ssh/metin2_vm gameplay_install_vm.sh "root@192.168.122.10:/usr/metin2-gameplay-$id/"
"${vm[@]}" "sh '/usr/metin2-gameplay-$id/gameplay_install_vm.sh' check '/usr/metin2-gameplay-$id'"
files=(audit.json manifest.json gameplay_install_host.sh gameplay_install_vm.sh)
if [ -f DENSITY_READY ]; then
    files+=(density.tar.gz density-files.txt density.sha256 density-baseline.sha256 density-report.json)
fi
sha256sum "${files[@]}" >release.sha256.next
mv release.sha256.next release.sha256
echo 'Installer checksums refreshed; frozen binaries and client unchanged.'
