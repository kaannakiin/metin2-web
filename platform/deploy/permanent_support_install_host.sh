#!/usr/bin/env bash
# Operator entry point: matching client + VM release, with scoped rollback.
set -euo pipefail
cd /home/m2web
stage=${1:?VM candidate directory}
[[ "$stage" =~ ^/usr/metin2-support-[0-9]{8}-[0-9]{6}$ ]] || exit 2
exec 9>dev/client-build.lock
flock -n 9 || { echo 'Client build is still running'; exit 1; }
test -f dev/support-client.sha256
sha256sum -c dev/support-client.sha256
vm=(ssh -o BatchMode=yes -i /root/.ssh/metin2_vm root@192.168.122.10)
"${vm[@]}" "test -f '$stage/READY' && test -f '$stage/previous/live.sha256'"
python3 publish_engine_check.py kit/dist/site/corpus www/corpus
backup=$(mktemp -d /home/m2web/backups/permanent-support-XXXXXXXX)
mkdir "$backup/site"
rsync -a --exclude=/corpus/ --exclude=/asan/ www/ "$backup/site/"
rollback_site() {
    rsync -a --delete --exclude=/corpus/ --exclude=/asan/ "$backup/site/" www/
    echo "Client rolled back: $backup" >&2
}
trap rollback_site ERR
bash publish.sh --engine-only
"${vm[@]}" "sh '$stage/permanent_support_install_vm.sh' install '$stage'"
trap - ERR
echo "INSTALLED. Client backup: $backup. VM backup: $stage/previous."
echo 'Reload the browser, log in, then test activation, death/revive and relog.'
