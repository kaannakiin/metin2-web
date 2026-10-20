#!/bin/sh
set -eu
action=${1:?prepare, install or rollback}
stage=${2:?stage directory}
case "$stage" in /usr/metin2-density-[0-9]*-[0-9]*) ;; *) exit 2 ;; esac
cd "$stage"
locale=/usr/home/share/locale/europe
test "$(wc -l <files.txt | tr -d ' ')" = 13
if grep -vE '^map/[a-z0-9_]+/stone\.txt$' files.txt; then exit 2; fi

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
    return 1
}
check_input() {
    while IFS= read -r file; do sha256 "input/$file"; done <files.txt | cmp candidate.sha256 -
}
check_live() {
    while IFS= read -r file; do sha256 "$locale/$file"; done <files.txt | cmp expected.sha256 -
}
restore() {
    while IFS= read -r file; do test -s "previous/$file" || return 1; done <files.txt
    service metin2 stop </dev/null >rollback-stop.log 2>&1 || return 1
    while IFS= read -r file; do cp -p "previous/$file" "$locale/$file" || return 1; done <files.txt
    service metin2 start </dev/null >rollback-start.log 2>&1 || return 1
    wait_health
}
case "$action" in
prepare)
    test ! -e READY
    test ! -e INSTALL_STARTED
    check_input
    check_live
    health
    while IFS= read -r file; do
        mkdir -p "previous/$(dirname "$file")"
        cp -p "$locale/$file" "previous/$file"
    done <files.txt
    touch READY
    echo 'READY: 13 map files backed up; live data unchanged.'
    ;;
install)
    test -f READY
    test ! -e INSTALL_STARTED
    check_input
    check_live
    health
    touch INSTALL_STARTED
    trap 'status=$?; trap - EXIT HUP INT TERM; restore || echo "ROLLBACK FAILED: operator required" >&2; exit "$status"' EXIT
    trap 'exit 130' HUP INT TERM
    service metin2 stop </dev/null >install-stop.log 2>&1
    while IFS= read -r file; do
        cp "input/$file" "$locale/$file"
        chown "$(stat -f %u "previous/$file"):$(stat -f %g "previous/$file")" "$locale/$file"
        chmod "$(stat -f %Lp "previous/$file")" "$locale/$file"
    done <files.txt
    service metin2 start </dev/null >install-start.log 2>&1
    wait_health
    while IFS= read -r file; do cmp "input/$file" "$locale/$file"; done <files.txt
    touch INSTALLED
    trap - EXIT HUP INT TERM
    echo 'INSTALLED: 388 Metin capacity, half respawn, six processes and ports healthy.'
    ;;
rollback)
    test -f INSTALL_STARTED
    restore
    rm -f INSTALLED
    echo 'ROLLED BACK: previous density restored.'
    ;;
*) exit 2 ;;
esac
