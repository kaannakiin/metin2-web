#!/bin/sh
set -eu
stage=${1:?absolute candidate directory required}
case "$stage" in /usr/metin2-gameplay-[0-9]*-[0-9]*) ;; *) exit 2 ;; esac
cd "$stage"
test ! -e READY
tar -xzf source.tar.gz
mkdir -p out quest-check
cd apps/server
gmake -j4 all "GAMEDIR=$stage/out" "DBDIR=$stage/out"
test -x "$stage/out/game"
test -x "$stage/out/db"
cd "$stage"
c++ -std=c++20 -Iapps/server/game/src platform/tests/detector_fixture.cpp -o out/detector-test
out/detector-test
c++ -std=c++20 -Iapps/server/library/liblua/include platform/tests/lua_fixture.cpp \
    apps/server/library/liblua/lib/liblualib.a apps/server/library/liblua/lib/liblua.a -lm -o out/lua-test
cp /usr/home/share/locale/europe/quest/qc /usr/home/share/locale/europe/quest/quest_functions quest-check/
cd quest-check
chmod 755 qc
./qc "$stage/runtime/freebsd/share/locale/europe/quest/quest_tr/_npc_talk_mission/welcome.lua"
test -s object/notarget/login/welcome.start
"$stage/out/lua-test" "$stage/platform/tests/gameplay_fixture.lua" object/notarget/login/welcome.start
cd "$stage/apps/server/game/src"
c++ -std=c++20 -DNDEBUG -D_LIBCPP_HARDENING_MODE=_LIBCPP_HARDENING_MODE_NONE \
    -I. -I/usr/local/include -I/usr/local/include/mysql -I../../library/liblua/include -I../../library \
    -w "$stage/platform/deploy/login_server_layout.cpp" -o "$stage/out/layout-test"
"$stage/out/layout-test" >"$stage/layout.txt"
grep -q 'TPacketGCLoginSuccess=594' "$stage/layout.txt"
cat "$stage/layout.txt"
cd "$stage"
sha256 out/game out/db
touch READY
echo 'READY: candidate binaries, compiled quest, detector and eight starter scenarios passed.'
echo 'A matching source-profile client is required before operator installation.'
