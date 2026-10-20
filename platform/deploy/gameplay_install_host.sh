#!/usr/bin/env bash
# Run manually during maintenance; never called by the agent's build flow.
set -euo pipefail
id=${1:?release id required}
[[ "$id" =~ ^[0-9]{8}-[0-9]{6}$ ]] || exit 2
[ "${2:-}" = --operator-maintenance ] || { echo 'Requires --operator-maintenance'; exit 2; }
here="/home/m2web/gameplay-$id"
stage="/usr/metin2-gameplay-$id"
cd "$here"
test -f BUNDLE_READY
test ! -e INSTALLED
exec 9>/home/m2web/dev/client-build.lock
flock -n 9 || { echo 'Client build running'; exit 1; }
sha256sum --quiet -c client-site.sha256
sha256sum --quiet -c release.sha256
python3 /home/m2web/publish_engine_check.py client-site/corpus /home/m2web/www/corpus
vm=(ssh -o BatchMode=yes -i /root/.ssh/metin2_vm root@192.168.122.10)
backup=$(mktemp -d /home/m2web/backups/gameplay-XXXXXXXX)
mkdir "$backup/site"
rsync -a --exclude=/corpus/ --exclude=/asan/ /home/m2web/www/ "$backup/site/"
echo "SITE BACKUP: $backup"
restore() {
    local status=$?
    trap - EXIT
    local failed=0
    rsync -a --delete --exclude=/corpus/ --exclude=/asan/ "$backup/site/" /home/m2web/www/ || failed=1
    "${vm[@]}" "if [ -f '$stage/INSTALL_STARTED' ]; then sh '$stage/gameplay_install_vm.sh' rollback '$stage'; fi" || failed=1
    if [ "$failed" != 0 ]; then
        echo "ROLLBACK INCOMPLETE: operator attention required; site backup $backup; VM backup $stage/previous" >&2
    fi
    exit "$status"
}
trap restore EXIT
trap 'exit 130' HUP INT TERM
"${vm[@]}" "sh '$stage/gameplay_install_vm.sh' install '$stage'"
rsync -a --delete --exclude=/corpus/ --exclude=/asan/ --exclude=/client.html client-site/ /home/m2web/www/
rsync -a client-site/client.html /home/m2web/www/client.html
cmp client-site/client.wasm /home/m2web/www/client.wasm
cmp client-site/client.html /home/m2web/www/client.html
touch INSTALLED
trap - EXIT
trap - HUP INT TERM
echo "INSTALLED: $id; reload client tabs and complete GAMEPLAY_RELEASE.md acceptance tests."
echo "Rollback site backup: $backup; VM backups: $stage/previous"
