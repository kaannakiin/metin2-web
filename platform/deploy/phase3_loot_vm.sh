#!/bin/sh
# Data-only release. prepare/check are safe online; install/rollback are operator maintenance.
set -eu
action=${1:?prepare, check, install or rollback}
stage=${2:?absolute stage required}
case "$stage" in /usr/metin2-phase3-[0-9]*-[0-9]*) ;; *) exit 2 ;; esac
cd "$stage"
locale=/usr/home/share/locale/europe
files='mob_drop_item.txt special_item_group.txt'

health() {
    ps -U metin2 -o command= | awk '
        { gsub(/^[ \t]+|[ \t]+$/, ""); sub(/ \(game\)$/, "") }
        $0 == "./db" { db++ } $0 == "./auth" { auth++ }
        $0 == "./game" { game++ } $0 == "./game99" { game99++ }
        END { exit !(db == 1 && auth == 1 && game == 3 && game99 == 1) }' || return 1
    sockstat -4 -l | awk '
        BEGIN { split("15000 30001 30003 30101 30103 30105", ports, " ") }
        $1 == "metin2" { count=split($6, address, ":"); seen[address[count]]=1 }
        END { for (i in ports) if (!seen[ports[i]]) exit 1 }'
}

wait_health() {
    for attempt in 1 2 3 4 5 6 7 8 9 10 11 12; do
        if health; then return 0; fi
        sleep 1
    done
    echo 'HEALTH FAILED: six game processes and six listening ports required.' >&2
    return 1
}

live_hashes() {
    for file in $files; do sha256 -q "$locale/$file"; done
}

candidate_hashes() {
    for file in $files; do sha256 -q "input/$file"; done
}

check() {
    test -f READY
    candidate_hashes >current-candidate.sha256
    cmp candidate.sha256 current-candidate.sha256
    live_hashes >current-live.sha256
    cmp baseline.sha256 current-live.sha256
    for file in $files; do cmp "$locale/$file" "previous/$file"; done
    health
}

restore() {
    for file in $files; do test -s "previous/$file" || return 1; done
    service metin2 stop </dev/null >rollback-stop.log 2>&1 || return 1
    for file in $files; do cp -p "previous/$file" "$locale/$file" || return 1; done
    service metin2 start </dev/null >rollback-start.log 2>&1 || return 1
    wait_health || return 1
}

case "$action" in
prepare)
    test ! -e READY
    test ! -e INSTALL_STARTED
    mkdir -m 700 previous
    for file in $files; do
        test -s "input/$file"
        test -s "$locale/$file"
        cp -p "$locale/$file" "previous/$file"
    done
    candidate_hashes >candidate.sha256
    live_hashes >baseline.sha256
    health
    touch READY
    echo 'READY: two loot tables backed up; live files and services unchanged.'
    ;;
check) check ;;
install)
    test ! -e INSTALL_STARTED
    check
    touch INSTALL_STARTED
    # A failure after stop restores both tables before starting the old game.
    trap 'status=$?; trap - EXIT HUP INT TERM; restore || echo "ROLLBACK FAILED: operator required" >&2; exit "$status"' EXIT
    trap 'exit 130' HUP INT TERM
    service metin2 stop </dev/null >install-stop.log 2>&1
    for file in $files; do
        cp "input/$file" "$locale/$file"
        chown "$(stat -f %u "previous/$file"):$(stat -f %g "previous/$file")" "$locale/$file"
        chmod "$(stat -f %Lp "previous/$file")" "$locale/$file"
    done
    service metin2 start </dev/null >install-start.log 2>&1
    wait_health
    for file in $files; do cmp "input/$file" "$locale/$file"; done
    touch INSTALLED
    trap - EXIT HUP INT TERM
    echo 'INSTALLED: phase3 loot; complete in-game acceptance.'
    ;;
rollback)
    test -f INSTALL_STARTED
    restore
    rm -f INSTALLED
    echo 'ROLLED BACK: previous loot tables restored.'
    ;;
*) exit 2 ;;
esac
