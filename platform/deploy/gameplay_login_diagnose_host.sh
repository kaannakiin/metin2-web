#!/usr/bin/env bash
set -euo pipefail
id=${1:?release id required}
[[ "$id" =~ ^[0-9]{8}-[0-9]{6}$ ]] || exit 2
cd "/home/m2web/gameplay-$id"
scp -q -i /root/.ssh/metin2_vm gameplay_login_diagnose_vm.sh "root@192.168.122.10:/usr/metin2-gameplay-$id/"
ssh -o BatchMode=yes -i /root/.ssh/metin2_vm root@192.168.122.10 "sh '/usr/metin2-gameplay-$id/gameplay_login_diagnose_vm.sh'"
