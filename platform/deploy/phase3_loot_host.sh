#!/usr/bin/env bash
# prepare freezes a tested client and backs up VM data; install is operator-only.
set -euo pipefail
action=${1:?prepare, check or install}
id=${2:?release id}
[[ "$id" =~ ^[0-9]{8}-[0-9]{6}$ ]] || exit 2
here="/home/m2web/phase3-$id"
stage="/usr/metin2-phase3-$id"
vm=(ssh -o BatchMode=yes -i /root/.ssh/metin2_vm root@192.168.122.10)
cd "$here"
exec 9>/home/m2web/dev/client-build.lock
flock -n 9 || { echo 'Client build running'; exit 1; }

check() {
    test -f BUNDLE_READY
    test ! -e INSTALLED
    sha256sum --quiet -c bundle.sha256
    sha256sum --quiet -c baseline-site.sha256
    python3 /home/m2web/publish_engine_check.py client-site/corpus /home/m2web/www/corpus
    "${vm[@]}" "sh '$stage/phase3_loot_vm.sh' check '$stage'"
}

case "$action" in
prepare)
    test ! -e BUNDLE_READY
    test "$(cat /home/m2web/dev/protocol)" = source
    reuse=${3:-}
    if [ -n "$reuse" ]; then
        [[ "$reuse" =~ ^[0-9]{8}-[0-9]{6}$ ]] && [ "$reuse" != "$id" ] || exit 2
        source="/home/m2web/phase3-$reuse"
        test -f "$source/BUNDLE_READY"
        (cd "$source" && sha256sum --quiet -c bundle.sha256)
        echo "REUSING FROZEN CLIENT: $reuse; no rebuild or test execution"
    else
        docker exec m2web-build bash /work/gameplay_client_build.sh
        source=/home/m2web/kit/dist/site
    fi
    if [ -n "$reuse" ]; then source="$source/client-site"; fi
    python3 /home/m2web/publish_engine_check.py "$source/corpus" /home/m2web/www/corpus
    mkdir client-site
    rsync -a "$source/" client-site/
    # Freeze current site hashes, so another publish requires a fresh candidate.
    find /home/m2web/www -type f ! -path '*/corpus/*' ! -path '*/asan/*' -print0 |
        sort -z | xargs -0 sha256sum >baseline-site.sha256
    "${vm[@]}" "mkdir -p '$stage/input'; chmod 700 '$stage'"
    scp -q -i /root/.ssh/metin2_vm input/*.txt "root@192.168.122.10:$stage/input/"
    scp -q -i /root/.ssh/metin2_vm phase3_loot_vm.sh "root@192.168.122.10:$stage/"
    "${vm[@]}" "sh '$stage/phase3_loot_vm.sh' prepare '$stage'"
    find client-site input -type f -print0 | sort -z | xargs -0 sha256sum >bundle.sha256
    sha256sum phase3_loot_vm.sh phase3_loot_host.sh phase3_loot.json >>bundle.sha256
    touch BUNDLE_READY
    check
    echo "BUNDLE_READY: $id; operator install: bash $here/phase3_loot_host.sh install $id --operator-maintenance"
    ;;
check) check ;;
install)
    [ "${3:-}" = --operator-maintenance ] || { echo 'Requires --operator-maintenance'; exit 2; }
    check
    backup=$(mktemp -d /home/m2web/backups/phase3-XXXXXXXX)
    mkdir "$backup/site"
    rsync -a --exclude=/corpus/ --exclude=/asan/ /home/m2web/www/ "$backup/site/"
    rollback() {
        local status=$?
        trap - EXIT
        local failed=0
        rsync -a --delete --exclude=/corpus/ --exclude=/asan/ "$backup/site/" /home/m2web/www/ || failed=1
        "${vm[@]}" "if [ -f '$stage/INSTALL_STARTED' ]; then sh '$stage/phase3_loot_vm.sh' rollback '$stage'; fi" || failed=1
        [ "$failed" = 0 ] || echo "ROLLBACK INCOMPLETE: $backup; $stage/previous" >&2
        exit "$status"
    }
    trap rollback EXIT
    trap 'exit 130' HUP INT TERM
    "${vm[@]}" "sh '$stage/phase3_loot_vm.sh' install '$stage'"
    rsync -a --delete --exclude=/corpus/ --exclude=/asan/ --exclude=/client.html client-site/ /home/m2web/www/
    rsync -a client-site/client.html /home/m2web/www/client.html
    cmp client-site/client.wasm /home/m2web/www/client.wasm
    cmp client-site/client.html /home/m2web/www/client.html
    touch INSTALLED
    trap - EXIT HUP INT TERM
    echo "INSTALLED: $id; reload client; site backup $backup; VM backup $stage/previous"
    ;;
*) exit 2 ;;
esac
