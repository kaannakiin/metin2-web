#!/usr/bin/env bash
set -euo pipefail
id=${1:?build id required}
[[ "$id" =~ ^[0-9]{8}-[0-9]{6}$ ]] || exit 2
here="/home/m2web/login-fix-$id"
stage="/usr/metin2-login-fix-$id"
vm=(ssh -o BatchMode=yes -i /root/.ssh/metin2_vm root@192.168.122.10)
"${vm[@]}" "mkdir -m 700 '$stage'"
scp -q -i /root/.ssh/metin2_vm "$here/source.tar.gz" "$here/login_fix_vm.sh" "root@192.168.122.10:$stage/"
"${vm[@]}" "nohup /bin/sh '$stage/login_fix_vm.sh' build '$stage' >'$stage/build.log' 2>&1 </dev/null &"
echo "Build started separately: $stage/build.log"
echo "No live binary replaced; no service restarted."
