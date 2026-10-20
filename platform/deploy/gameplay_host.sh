#!/usr/bin/env bash
set -euo pipefail
id=${1:?release id required}
[[ "$id" =~ ^[0-9]{8}-[0-9]{6}$ ]] || exit 2
here="/home/m2web/gameplay-$id"
stage="/usr/metin2-gameplay-$id"
vm=(ssh -o BatchMode=yes -i /root/.ssh/metin2_vm root@192.168.122.10)
"${vm[@]}" "mkdir -p -m 700 '$stage' && test ! -e '$stage/READY'"
scp -q -i /root/.ssh/metin2_vm "$here/source.tar.gz" "$here/manifest.json" "root@192.168.122.10:$stage/"
"${vm[@]}" "cd '$stage' && tar -xzf source.tar.gz platform/deploy/gameplay_vm.sh && nohup /bin/sh platform/deploy/gameplay_vm.sh '$stage' >build.log 2>&1 </dev/null &"
echo "Build started: $stage/build.log"
echo 'No live service restarted.'
