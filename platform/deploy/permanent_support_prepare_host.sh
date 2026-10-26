#!/usr/bin/env bash
set -euo pipefail
cd /home/m2web
stage=${1:?VM candidate directory}
[[ "$stage" =~ ^/usr/metin2-support-[0-9]{8}-[0-9]{6}$ ]] || exit 2
exec 9>dev/client-build.lock
flock -n 9 || { echo 'Client build still running'; exit 1; }
grep -q '^CLIENT SUPPORT READY:' dev/logs/permanent-support-client.log
grep -Eq '^patches=[0-9]+ hit=[0-9]+ miss=0$' dev/logs/permanent-support-client.log
python3 publish_engine_check.py kit/dist/site/corpus www/corpus
docker exec -e M2W_BOOT_SYSTEM=/work/kit/build/port/scripts3/system.py \
    m2web-build python3.13 -B -m unittest discover -s /work/kit/tools -p test_python_startup.py
sha256sum kit/dist/site/client.* kit/dist/site/preload.js kit/dist/site/sw.js >dev/support-client.sha256
vm=(ssh -o BatchMode=yes -i /root/.ssh/metin2_vm root@192.168.122.10)
"${vm[@]}" "test -f '$stage/READY'"
scp -q -i /root/.ssh/metin2_vm permanent_support_install_vm.sh "root@192.168.122.10:$stage/"
"${vm[@]}" "sh '$stage/permanent_support_install_vm.sh' prepare '$stage'"
echo 'RELEASE PREPARED: tested client hashes and VM backups saved. Live game unchanged.'
