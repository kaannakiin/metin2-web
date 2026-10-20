#!/bin/sh
set -eu
stage=${1:?candidate directory required}
case "$stage" in /usr/metin2-gameplay-[0-9]*-[0-9]*) ;; *) exit 2 ;; esac
cd "$stage"
test -f INSTALLED
locale=/usr/home/share/locale/europe
cmp out/game /usr/home/share/bin/game
cmp out/db /usr/home/share/bin/db
cmp runtime/freebsd/share/locale/europe/mob_drop_item.txt "$locale/mob_drop_item.txt"
cmp quest-check/object/notarget/login/welcome.start "$locale/quest/object/notarget/login/welcome.start"
cmp quest-check/object/state/welcome "$locale/quest/object/state/welcome"
cmp runtime/freebsd/share/locale/europe/quest/quest_tr/_npc_talk_mission/welcome.lua \
    "$locale/quest/quest_tr/_npc_talk_mission/welcome.lua"
maps=0
if [ -f DENSITY_READY ]; then
    while IFS= read -r relative; do
        cmp "density/$relative" "$locale/$relative"
        maps=$((maps + 1))
    done <density-files.txt
fi
configs=0
while IFS= read -r config; do
    case "$config" in */CONFIG) ;; *) continue ;; esac
    awk '/^MAX_LEVEL:/ { count++; if ($2 != 99) bad=1 } END { exit (count != 1 || bad) }' "$config"
    configs=$((configs + 1))
done <previous/paths
sh gameplay_install_vm.sh check "$stage"
echo "LIVE RUNTIME: matching game/db, drop, compiled starter quest, $maps map files and $configs MAX_LEVEL configs verified."
sha256 -q /usr/home/share/bin/game
