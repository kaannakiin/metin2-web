#!/bin/sh
# Compile quests off-line, then install only this release's data and quest namespaces.
set -eu
action=${1:?prepare or install}
stage=${2:?release directory}
case "$stage" in /usr/metin2-progression-[0-9]*-[0-9]*) ;; *) exit 2 ;; esac
cd "$stage"
locale=/usr/home/share/locale/europe
names='deviltower_zone devilcatacomb_zone dragonlair spider_dungeon midpvp_progression'
if test -f data-only; then names=''; fi
if test -f starter-ring; then names='starter_ring'; fi
if test -f npc-support; then names='starter_support'; fi
if test -f support-only; then names='starter_support'; fi
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
wait_stopped() {
    pattern=$1
    attempt=0
    while test "$attempt" -lt 60; do
        if ! pgrep -u metin2 -f "$pattern" >/dev/null; then return 0; fi
        sleep 1
        attempt=$((attempt + 1))
    done
    return 1
}
stop_game() {
    games='^\./(auth|game|game99)( \(game\))?$'
    database='^\./db( \(db\))?$'
    pkill -TERM -u metin2 -f "$games" || true
    wait_stopped "$games" || return 1
    pkill -TERM -u metin2 -f "$database" || true
    wait_stopped "$database"
}
quest_files() {
    for name in $names; do
        find "$1" -type f \( -name "$name" -o -name "$name.*" \)
    done | LC_ALL=C sort
}
remove_objects() {
    quest_files "$locale/quest/object" >remove-objects.txt
    while IFS= read -r file; do rm -f "$file"; done <remove-objects.txt
}
snapshot() {
    while IFS= read -r file; do
        if test -f "$locale/$file"; then sha256 "$locale/$file"; else echo "ABSENT $file"; fi
    done <install-files.txt
    quest_files "$locale/quest/object" | while IFS= read -r file; do sha256 "$file"; done
}
install_files() {
    while IFS= read -r file; do
        mkdir -p "$locale/$(dirname "$file")"
        cp -p "input/$file" "$locale/$file"
        chown metin2:metin2 "$locale/$file"
        chmod 644 "$locale/$file"
    done <install-files.txt
}
restore() {
    stop_game </dev/null >rollback-stop.log 2>&1 || return 1
    if test -f DATABASE_CHANGED; then
        mariadb player <previous-database.sql >rollback-database.log 2>&1 || return 1
    fi
    remove_objects || return 1
    while IFS= read -r file; do rm -f "$locale/$file"; done <install-files.txt
    tar -xpf previous.tar -C "$locale" || return 1
    service metin2 start </dev/null >rollback-start.log 2>&1 || return 1
    wait_health
}
case "$action" in
prepare)
    test ! -e READY
    test ! -e INSTALL_STARTED
    sha256 -q payload.tar.gz | cmp payload.sha256 -
    tar -xzf payload.tar.gz
    if test -f data-only; then names=''; fi
    if test -f starter-ring; then names='starter_ring'; fi
    if test -f npc-support; then names='starter_support'; fi
    if test -f support-only; then names='starter_support'; fi
    while IFS= read -r file; do sha256 "$locale/$file"; done <expected-files.txt | cmp expected.sha256 -
    if test -f new-files.txt; then
        while IFS= read -r file; do test ! -e "$locale/$file"; done <new-files.txt
    fi
    health
    if test -n "$names"; then
    mkdir compile
    cp -p "$locale/quest/qc" "$locale/quest/quest_functions" compile/
    chmod 700 compile/qc
    for optional in quest_functions_ex questlib.lua locale.lua; do
        if test -f "$locale/quest/$optional"; then cp -p "$locale/quest/$optional" compile/; fi
    done
    cp -R input/quest/quest_tr compile/
    mkdir compile/object
    for name in $names; do
        (cd compile && ./qc "quest_tr/_midpvp/$name.lua") >"compile-$name.log" 2>&1
        test -s "compile/object/state/$name"
        if grep -Ei '(^|[[:space:]])(error|fatal)[[:space:]:]' "compile-$name.log"; then exit 1; fi
    done
    quest_files compile/object >compiled-files.txt
    test -s compiled-files.txt
    while IFS= read -r file; do
        relative=${file#compile/}
        mkdir -p "input/quest/$(dirname "$relative")"
        cp -p "$file" "input/quest/$relative"
        echo "quest/$relative" >>install-files.txt
    done <compiled-files.txt
    fi
    snapshot >baseline.sha256
    : >previous-files.txt
    while IFS= read -r file; do test ! -f "$locale/$file" || echo "$file" >>previous-files.txt; done <install-files.txt
    quest_files "$locale/quest/object" | sed "s|^$locale/||" >>previous-files.txt
    LC_ALL=C sort -u previous-files.txt >previous-sorted.txt
    tar -cpf previous.tar -C "$locale" -T previous-sorted.txt
    while IFS= read -r file; do sha256 "input/$file"; done <install-files.txt >candidate.sha256
    if test -n "$names"; then (cd compile && tar -czf ../compiled.tar.gz object); fi
    touch READY
    echo 'READY: payload and rollback archived; requested quest builds complete; live unchanged.'
    ;;
install)
    test -f READY
    test ! -e INSTALL_STARTED
    snapshot >current.sha256
    cmp baseline.sha256 current.sha256
    while IFS= read -r file; do sha256 "input/$file"; done <install-files.txt | cmp candidate.sha256 -
    health
    touch INSTALL_STARTED
    trap 'status=$?; trap - EXIT HUP INT TERM; restore || echo "ROLLBACK FAILED: operator required" >&2; exit "$status"' EXIT
    trap 'exit 130' HUP INT TERM
    stop_game </dev/null >install-stop.log 2>&1
    if test -f npc-support; then
        # Only the five legacy shop registrations and two global event flags.
        # Players, inventories and all other quest flags are excluded.
        {
            echo 'USE player; START TRANSACTION;'
            echo 'DELETE FROM shop_item WHERE shop_vnum IN (1,2,3,6,7);'
            echo 'DELETE FROM shop WHERE vnum IN (1,2,3,6,7);'
            echo "DELETE FROM quest WHERE dwPID=0 AND szName IN ('mob_gold','mob_gold_buyer');"
            mariadb-dump --compact --skip-add-locks --no-create-info --skip-lock-tables player shop \
                --where='vnum IN (1,2,3,6,7)'
            mariadb-dump --compact --skip-add-locks --no-create-info --skip-lock-tables player shop_item \
                --where='shop_vnum IN (1,2,3,6,7)'
            mariadb-dump --compact --skip-add-locks --no-create-info --skip-lock-tables player quest \
                --where="dwPID=0 AND szName IN ('mob_gold','mob_gold_buyer')"
            echo 'COMMIT;'
        } >previous-database.sql
        test -s previous-database.sql
        touch DATABASE_CHANGED
        mariadb player <database.sql >install-database.log 2>&1
        shop_count=$(mariadb -N -B player -e 'SELECT COUNT(*) FROM shop WHERE vnum IN (1,2,3,6,7)')
        gold_query="SELECT COUNT(*) FROM quest WHERE dwPID=0 AND szName IN ('mob_gold','mob_gold_buyer') AND lValue=400"
        gold_count=$(mariadb -N -B player -e "$gold_query")
        test "$shop_count" = 0
        test "$gold_count" = 2
    fi
    remove_objects
    install_files
    service metin2 start </dev/null >install-start.log 2>&1
    wait_health
    while IFS= read -r file; do cmp "input/$file" "$locale/$file"; done <install-files.txt
    touch INSTALLED
    trap - EXIT HUP INT TERM
    echo 'INSTALLED: selected data and quest namespaces; six processes and ports healthy.'
    ;;
*) exit 2 ;;
esac
