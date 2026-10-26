#!/bin/sh
set -eu
stage=${1:?candidate path}
case "$stage" in /usr/metin2-support-[0-9]*-[0-9]*) ;; *) exit 2 ;; esac
cd "$stage"
test ! -e previous
rm -f READY
tar -xzf source.tar.gz
mkdir -p out quest-check
cd apps/server
gmake -j4 all "GAMEDIR=$stage/out" "DBDIR=$stage/out"
cd "$stage"
c++ -std=c++17 platform/tests/permanent_support_fixture.cpp -o out/support-test
out/support-test
c++ -std=c++20 -Iapps/server/library/liblua/include platform/tests/lua_fixture.cpp \
    apps/server/library/liblua/lib/liblualib.a apps/server/library/liblua/lib/liblua.a -lm -o out/lua-test
cp /usr/home/share/locale/europe/quest/qc /usr/home/share/locale/europe/quest/quest_functions quest-check/
cd quest-check
chmod 755 qc
./qc "$stage/runtime/freebsd/share/locale/europe/quest/quest_tr/_npc_talk_mission/welcome.lua"
./qc "$stage/runtime/freebsd/share/locale/europe/quest/quest_tr/_npc_talk_mission/permanent_support.quest"
"$stage/out/lua-test" "$stage/platform/tests/permanent_support_fixture.lua" object/notarget/login/permanent_support.start
test -s object/notarget/login/welcome.start
cd "$stage"
test -x out/game
test -x out/db
sha256 out/game out/db >candidate.sha256
touch READY
echo 'READY: game/db built; support transitions and compiled grant quest passed.'
