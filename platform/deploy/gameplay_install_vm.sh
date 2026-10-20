#!/bin/sh
# Operator-only maintenance step. prepare is read-only against the live tree.
set -eu
action=${1:?prepare, append-density, check, check-density, install or rollback}
stage=${2:?candidate directory required}
case "$stage" in /usr/metin2-gameplay-[0-9]*-[0-9]*) ;; *) exit 2 ;; esac
cd "$stage"
test -f READY
locale=/usr/home/share/locale/europe

fingerprint_paths() {
    while IFS= read -r file; do sha256 "$file"; done <"$1"
}

fingerprint() {
    fingerprint_paths previous/paths
}

validate_density_paths() {
    test -s density-files.txt || return 1
    awk 'seen[$0]++ { exit 1 }' density-files.txt || return 1
    while IFS= read -r relative; do
        case "$relative" in map/*/stone.txt) ;; *) return 1 ;; esac
        map_name=${relative#map/}
        map_name=${map_name%/stone.txt}
        case "$map_name" in ''|*[!a-z0-9_]*) return 1 ;; esac
    done <density-files.txt
}

base_candidate_fingerprint() {
    sha256 out/game out/db runtime/freebsd/share/locale/europe/mob_drop_item.txt \
        runtime/freebsd/share/locale/europe/quest/quest_tr/_npc_talk_mission/welcome.lua \
        quest-check/object/notarget/login/welcome.start quest-check/object/state/welcome
}

candidate_fingerprint() {
    base_candidate_fingerprint
    if [ -f density-files.txt ]; then
        validate_density_paths || return 1
        while IFS= read -r relative; do sha256 "density/$relative"; done <density-files.txt
    fi
}

health() {
    # The installed rc status returns success even when no game process exists.
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
    echo 'HEALTH FAILED: require db, auth, three game cores, game99 and all six listening ports.' >&2
    return 1
}

restore() {
    index=0
    while IFS= read -r file; do
        index=$((index + 1))
        if [ ! -r "previous/$index" ]; then
            echo "ROLLBACK INCOMPLETE: missing backup $stage/previous/$index" >&2
            return 1
        fi
    done <previous/paths
    service metin2 stop </dev/null >/dev/null 2>&1 || true
    index=0
    failed=0
    while IFS= read -r file; do
        index=$((index + 1))
        cat "previous/$index" >"$file" || failed=1
    done <previous/paths
    if [ "$failed" != 0 ]; then
        echo "ROLLBACK INCOMPLETE: file restore failed; inspect $stage/previous before starting services." >&2
        return 1
    fi
    service metin2 start </dev/null >rollback-start.log 2>&1 || return 1
    wait_health || return 1
    service metin2 status || return 1
    rm -f INSTALL_STARTED INSTALLED
}

case "$action" in
check-density)
    test -f DENSITY_READY
    validate_density_paths
    candidate_fingerprint | cmp candidate.sha256 -
    fingerprint | cmp previous/live.sha256 -
    echo 'DENSITY CHECK: staged maps intact; live runtime unchanged.'
    ;;
check)
    if ! health; then
        echo 'Current game processes and listening endpoints:' >&2
        ps -U metin2 -o command= >&2
        sockstat -4 -l | awk '$1 == "metin2" { print $2, $6 }' >&2
        exit 1
    fi
    echo 'HEALTH PASS: all six game-service processes and six IPv4 ports present.'
    ;;
prepare)
    test ! -e density-files.txt
    test ! -e previous
    mkdir -m 700 previous
    {
        echo /usr/home/share/bin/game
        echo /usr/home/share/bin/db
        echo "$locale/mob_drop_item.txt"
        echo "$locale/quest/object/notarget/login/welcome.start"
        echo "$locale/quest/object/state/welcome"
        echo "$locale/quest/quest_tr/_npc_talk_mission/welcome.lua"
        find /usr/home/main/channels -name CONFIG -print | sort
    } >previous/paths
    index=0
    while IFS= read -r file; do
        test -f "$file"
        index=$((index + 1))
        cp -p "$file" "previous/$index"
    done <previous/paths
    fingerprint >previous/live.sha256
    candidate_fingerprint >candidate.sha256
    chmod -R go-rwx previous
    echo 'PREPARED: live files backed up, fingerprints recorded; no service change.'
    ;;
append-density)
    test ! -e INSTALL_STARTED
    test ! -e INSTALLED
    test ! -e DENSITY_READY
    test ! -e previous-density-next
    test ! -e previous-before-density
    validate_density_paths
    base_candidate_fingerprint | cmp candidate.sha256 -
    fingerprint | cmp previous/live.sha256 -
    while IFS= read -r relative; do sha256 "density/$relative"; done <density-files.txt | cmp density.sha256 -
    while IFS= read -r relative; do sha256 "$locale/$relative"; done <density-files.txt | cmp density-baseline.sha256 -
    cp -Rp previous previous-density-next
    index=$(wc -l <previous/paths)
    while IFS= read -r relative; do
        index=$((index + 1))
        cp -p "$locale/$relative" "previous-density-next/$index"
        printf '%s\n' "$locale/$relative" >>previous-density-next/paths
    done <density-files.txt
    chmod -R go-rwx previous-density-next
    fingerprint_paths previous-density-next/paths >previous-density-next/live.sha256
    candidate_fingerprint >candidate-density-next.sha256
    mv previous previous-before-density
    mv previous-density-next previous
    mv candidate-density-next.sha256 candidate.sha256
    touch DENSITY_READY
    echo 'DENSITY READY: candidate maps and live backups extended; live files unchanged.'
    ;;
install)
    test -f previous/live.sha256
    test ! -e INSTALL_STARTED
    fingerprint >live-now.sha256
    cmp previous/live.sha256 live-now.sha256
    if [ -f density-files.txt ]; then test -f DENSITY_READY; fi
    candidate_fingerprint >candidate-now.sha256
    cmp candidate.sha256 candidate-now.sha256
    touch INSTALL_STARTED
    trap 'result=$?; trap - 0; restore || echo "Automatic rollback needs operator attention: $stage" >&2; exit "$result"' 0
    trap 'exit 130' HUP INT TERM
    service metin2 stop </dev/null >stop.log 2>&1
    cp -p out/game out/db /usr/home/share/bin/
    cat runtime/freebsd/share/locale/europe/mob_drop_item.txt >"$locale/mob_drop_item.txt"
    cat quest-check/object/notarget/login/welcome.start >"$locale/quest/object/notarget/login/welcome.start"
    cat quest-check/object/state/welcome >"$locale/quest/object/state/welcome"
    cat runtime/freebsd/share/locale/europe/quest/quest_tr/_npc_talk_mission/welcome.lua \
        >"$locale/quest/quest_tr/_npc_talk_mission/welcome.lua"
    if [ -f density-files.txt ]; then
        validate_density_paths
        while IFS= read -r relative; do cat "density/$relative" >"$locale/$relative"; done <density-files.txt
    fi
    while IFS= read -r config; do
        case "$config" in */CONFIG) ;; *) continue ;; esac
        awk 'BEGIN { found=0 } /^MAX_LEVEL:/ { print "MAX_LEVEL: 99"; found=1; next }
             { print } END { if (!found) print "MAX_LEVEL: 99" }' "$config" >config-next
        cat config-next >"$config"
    done <previous/paths
    service metin2 start </dev/null >start.log 2>&1
    wait_health
    service metin2 status
    touch INSTALLED
    trap - 0
    trap - HUP INT TERM
    echo 'INSTALLED: matching game/db, drops, starter quest, detector and MAX_LEVEL 99.'
    ;;
rollback)
    test -f INSTALL_STARTED
    restore
    echo 'ROLLED BACK: previous binaries, runtime data and CONFIG files restored.'
    ;;
*) exit 2 ;;
esac
