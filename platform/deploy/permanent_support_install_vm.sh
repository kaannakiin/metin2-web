#!/bin/sh
# Run by the operator. Only this game's services/files/attribute table are touched.
set -eu
action=${1:?prepare or install or rollback}
stage=${2:?candidate directory}
case "$stage" in /usr/metin2-support-[0-9]*-[0-9]*) ;; *) exit 2 ;; esac
cd "$stage"
test -f READY
locale=/usr/home/share/locale/europe
quest=$locale/quest

health() {
    ps -U metin2 -o command= | awk '
      {gsub(/^[ \t]+|[ \t]+$/, ""); sub(/ \(game\)$/, "")}
      $0=="./db" {d++} $0=="./auth" {a++} $0=="./game" {g++} $0=="./game99" {s++}
      END {exit !(d==1 && a==1 && g==3 && s==1)}'
}
wait_health() {
    for attempt in 1 2 3 4 5 6 7 8 9 10 11 12; do
        if health; then return 0; fi
        sleep 1
    done
    return 1
}
fingerprint() {
    while IFS= read -r file; do
        if [ -f "$file" ]; then sha256 "$file"; else printf 'MISSING %s\n' "$file"; fi
    done <previous/paths
}
restore() {
    service metin2 stop </dev/null >rollback-stop.log 2>&1 || true
    index=0
    while IFS= read -r file; do
        index=$((index+1))
        if [ -f "previous/$index" ]; then
            cat "previous/$index" >"$file"
        else
            rm -f "$file"
        fi
    done <previous/paths
    mysql player <previous/item_attr.sql
    service metin2 start </dev/null >rollback-start.log 2>&1
    wait_health
}
case "$action" in
prepare)
    test ! -e previous
    sha256 out/game out/db | cmp candidate.sha256 -
    mkdir -m 700 previous
    {
        echo /usr/home/share/bin/game
        echo /usr/home/share/bin/db
        echo "$quest/quest_tr/_npc_talk_mission/welcome.lua"
        echo "$quest/object/notarget/login/welcome.start"
        echo "$quest/object/state/welcome"
        echo "$quest/quest_tr/_npc_talk_mission/permanent_support.quest"
        echo "$quest/object/notarget/login/permanent_support.start"
        echo "$quest/object/notarget/levelup/permanent_support.start"
        echo "$quest/object/state/permanent_support"
    } >previous/paths
    index=0
    while IFS= read -r file; do
        index=$((index+1))
        if [ -f "$file" ]; then cp -p "$file" "previous/$index"; fi
    done <previous/paths
    fingerprint >previous/live.sha256
    # A data-only rollback; no DROP TABLE and no player item/character changes.
    printf 'START TRANSACTION;\nDELETE FROM item_attr;\n' >previous/item_attr.sql
    mysqldump --no-create-info --skip-triggers --skip-add-locks --skip-disable-keys --compact player item_attr >>previous/item_attr.sql
    printf '\nCOMMIT;\n' >>previous/item_attr.sql
    mysql -N -B player -e 'SELECT * FROM item_attr ORDER BY apply' >previous/item_attr.tsv
    sha256 quest-check/object/notarget/login/welcome.start quest-check/object/state/welcome \
      quest-check/object/notarget/login/permanent_support.start \
      quest-check/object/notarget/levelup/permanent_support.start quest-check/object/state/permanent_support \
      runtime/freebsd/share/locale/europe/quest/quest_tr/_npc_talk_mission/welcome.lua \
      runtime/freebsd/share/locale/europe/quest/quest_tr/_npc_talk_mission/permanent_support.quest \
      content/server/sql/migrations/20261022_normal_attributes.sql >data.sha256
    chmod -R go-rwx previous
    echo 'PREPARED: binary/quest/SQL backups saved; live game unchanged.'
    ;;
install)
    test -f previous/live.sha256
    test ! -f INSTALLED
    sha256 out/game out/db | cmp candidate.sha256 -
    fingerprint | cmp previous/live.sha256 -
    mysql -N -B player -e 'SELECT * FROM item_attr ORDER BY apply' | cmp previous/item_attr.tsv -
    while IFS= read -r line; do
        file=${line#SHA256 (}; file=${file%%)*}
        sha256 "$file"
    done <data.sha256 | cmp data.sha256 -
    trap 'result=$?; trap - 0; restore || echo "ROLLBACK NEEDS ATTENTION: $stage" >&2; exit "$result"' 0
    trap 'exit 130' HUP INT TERM
    service metin2 stop </dev/null >stop.log 2>&1
    mysql <content/server/sql/migrations/20261022_normal_attributes.sql
    cat out/game >/usr/home/share/bin/game
    cat out/db >/usr/home/share/bin/db
    for name in welcome.lua permanent_support.quest; do
        cat "runtime/freebsd/share/locale/europe/quest/quest_tr/_npc_talk_mission/$name" >"$quest/quest_tr/_npc_talk_mission/$name"
    done
    for relative in notarget/login/welcome.start state/welcome notarget/login/permanent_support.start notarget/levelup/permanent_support.start state/permanent_support; do
        mkdir -p "$quest/object/$(dirname "$relative")"
        cat "quest-check/object/$relative" >"$quest/object/$relative"
    done
    # New objects must be readable by the metin2 service user.
    chmod 644 "$quest/object/notarget/login/permanent_support.start" \
      "$quest/object/notarget/levelup/permanent_support.start" "$quest/object/state/permanent_support"
    service metin2 start </dev/null >start.log 2>&1
    wait_health
    hp_rows=$(mysql -N -B player -e "SELECT COUNT(*) FROM item_attr WHERE apply='MAX_HP' AND lv1=3000 AND lv5=3000")
    test "$hp_rows" = 1
    touch INSTALLED
    trap - 0 HUP INT TERM
    echo 'INSTALLED: permanent support + level 1 dews/potions + normal attributes HP 3000.'
    ;;
rollback)
    test -f previous/live.sha256
    restore
    echo 'Previous binaries, quests and normal attribute table restored.'
    ;;
*) exit 2 ;;
esac
