#!/bin/sh
# Data-only maintenance: unlock the two existing standard inventory pages.
set -eu
stage=${1:?release directory}
case "$stage" in /usr/metin2-inventory-[0-9]*-[0-9]*) ;; *) exit 2 ;; esac
cd "$stage"
test ! -e INSTALL_STARTED
sha256 -q 20261020_default_inventory.sql | cmp migration.sha256 -
sql() { mariadb --batch --skip-column-names -e "$1"; }
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
    # The legacy rc script misses FreeBSD's " (game)" process-title suffix.
    # Stop only Metin2 processes; let game cores flush before stopping db.
    games='^\./(auth|game|game99)( \(game\))?$'
    database='^\./db( \(db\))?$'
    pkill -TERM -u metin2 -f "$games" || true
    wait_stopped "$games" || return 1
    pkill -TERM -u metin2 -f "$database" || true
    wait_stopped "$database"
}
previous_default=$(sql "SELECT COLUMN_DEFAULT FROM information_schema.COLUMNS WHERE TABLE_SCHEMA='player' AND TABLE_NAME='player' AND COLUMN_NAME='inventory_0'")
case "$previous_default" in ''|*[!0-9]*) exit 2 ;; esac
test "$previous_default" -le 18
health
touch INSTALL_STARTED
restore() {
    stop_game </dev/null >rollback-stop.log 2>&1 || return 1
    if test -f BACKUP_READY; then
        mariadb <rollback.sql || return 1
        sql "ALTER TABLE player.player ALTER COLUMN inventory_0 SET DEFAULT $previous_default" || return 1
    fi
    service metin2 start </dev/null >rollback-start.log 2>&1 || return 1
    wait_health
}
trap 'status=$?; trap - EXIT HUP INT TERM; restore || echo "ROLLBACK FAILED: operator required" >&2; exit "$status"' EXIT
trap 'exit 130' HUP INT TERM
stop_game </dev/null >install-stop.log 2>&1
# Refuse a database update if any game process survived the stop.
if ps -U metin2 -o command= | awk '{ gsub(/^[ \t]+|[ \t]+$/, ""); sub(/ \(game\)$/, "") } $0 ~ /^\.\/(db|auth|game|game99)$/ { found=1 } END { exit !found }'; then
    echo 'Metin2 processes still running; refusing database update.' >&2
    exit 1
fi
sql "SELECT CONCAT('UPDATE player.player SET inventory_0 = ',inventory_0,' WHERE id = ',id,';') FROM player.player ORDER BY id" >rollback.sql
printf '%s\n' "$previous_default" >previous-default.txt
touch BACKUP_READY
mariadb <20261020_default_inventory.sql
test "$(sql 'SELECT COUNT(*) FROM player.player WHERE inventory_0 <> 18')" = 0
test "$(sql "SELECT COLUMN_DEFAULT FROM information_schema.COLUMNS WHERE TABLE_SCHEMA='player' AND TABLE_NAME='player' AND COLUMN_NAME='inventory_0'")" = 18
service metin2 start </dev/null >install-start.log 2>&1
wait_health
sql 'SELECT COUNT(*) AS characters_with_four_pages FROM player.player WHERE inventory_0 = 18' >result.txt
touch INSTALLED
trap - EXIT HUP INT TERM
echo "INSTALLED: four inventory pages, new-character default 18; $(cat result.txt) existing characters; six processes and ports healthy."
