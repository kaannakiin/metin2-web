#!/usr/bin/env bash
# Finish publication after a completed VM install whose SSH output pipe stayed open.
set -euo pipefail
id=${1:?release id}
parent=${2:?hung installer pid}
child=${3:?hung VM ssh pid}
[[ "$id" =~ ^[0-9]{8}-[0-9]{6}$ && "$parent" =~ ^[0-9]+$ && "$child" =~ ^[0-9]+$ ]] || exit 2
here="/home/m2web/phase3-$id"
stage="/usr/metin2-phase3-$id"
cd "$here"
test -f BUNDLE_READY
test ! -e INSTALLED
sha256sum --quiet -c bundle.sha256
sha256sum --quiet -c baseline-site.sha256
vm=(ssh -o BatchMode=yes -i /root/.ssh/metin2_vm root@192.168.122.10)
"${vm[@]}" "test -f '$stage/INSTALLED' && cmp '$stage/input/mob_drop_item.txt' /usr/home/share/locale/europe/mob_drop_item.txt && cmp '$stage/input/special_item_group.txt' /usr/home/share/locale/europe/special_item_group.txt"
python3 - "$parent" "$child" "$here" "$stage" <<'PY'
import os, pathlib, signal, sys
parent, child = map(int, sys.argv[1:3])
here, stage = sys.argv[3:]
def args(pid):
    return pathlib.Path('/proc/%d/cmdline' % pid).read_bytes().split(b'\0')[:-1]
assert args(parent) == [b'bash', (here+'/phase3_loot_host.sh').encode(), b'install', here.rsplit('-',2)[-2].encode()+b'-'+here.rsplit('-',1)[-1].encode(), b'--operator-maintenance']
c = args(child)
assert c[:7] == [b'ssh', b'-o', b'BatchMode=yes', b'-i', b'/root/.ssh/metin2_vm', b'root@192.168.122.10', ("sh '%s/phase3_loot_vm.sh' install '%s'" % (stage,stage)).encode()]
status = pathlib.Path('/proc/%d/status' % child).read_text()
assert next(s.split()[1] for s in status.splitlines() if s.startswith('PPid:')) == str(parent)
# Only the deployment shell and its waiting SSH client. Game processes are on the VM.
# SIGKILL avoids firing the old shell's rollback trap after its VM install succeeded.
os.kill(parent, signal.SIGKILL)
os.kill(child, signal.SIGKILL)
PY
exec 9>/home/m2web/dev/client-build.lock
flock -w 10 9
backup=$(mktemp -d /home/m2web/backups/phase3-finish-XXXXXXXX)
mkdir "$backup/site"
rsync -a --exclude=/corpus/ --exclude=/asan/ /home/m2web/www/ "$backup/site/"
rollback() {
    local status=$?
    trap - EXIT
    rsync -a --delete --exclude=/corpus/ --exclude=/asan/ "$backup/site/" /home/m2web/www/ || true
    "${vm[@]}" "sh '$stage/phase3_loot_vm.sh' rollback '$stage' >'$stage/finish-rollback.log' 2>&1 </dev/null" || true
    exit "$status"
}
trap rollback EXIT
trap 'exit 130' HUP INT TERM
rsync -a --delete --exclude=/corpus/ --exclude=/asan/ --exclude=/client.html client-site/ /home/m2web/www/
rsync -a client-site/client.html /home/m2web/www/client.html
cmp client-site/client.wasm /home/m2web/www/client.wasm
cmp client-site/client.html /home/m2web/www/client.html
touch INSTALLED
trap - EXIT HUP INT TERM
echo "INSTALLED: $id; client and v3 loot published; site backup $backup; VM backup $stage/previous"
