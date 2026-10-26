#!/bin/sh
# Called only by the operator's item-cleanup entry point.
set -eu
games='^\./(auth|game|game99)( \(game\))?$'
database='^\./db( \(db\))?$'
quest=/usr/home/share/locale/europe/quest
work=/usr/home/attribute-cleanup-welcome-20261022
owned() {
    find object -type f \( -name welcome -o -name 'welcome.*' \) | LC_ALL=C sort
}
stopped() {
    ! pgrep -u metin2 -f "$games" >/dev/null
    ! pgrep -u metin2 -f "$database" >/dev/null
}
health() {
    ps -U metin2 -o command= | awk '
      { gsub(/^[ \t]+|[ \t]+$/, ""); sub(/ \(game\)$/, "") }
      $0=="./db" {d++} $0=="./auth" {a++} $0=="./game" {g++} $0=="./game99" {s++}
      END {exit !(d==1 && a==1 && g==3 && s==1)}' || return 1
    sockstat -4 -l | awk '
      BEGIN {split("15000 30001 30003 30101 30103 30105",ports," ")}
      $1=="metin2" {n=split($6,address,":");seen[address[n]]=1}
      END {for(i in ports) if(!seen[ports[i]]) exit 1}'
}
wait_exit() {
    pattern=$1
    for attempt in $(jot 60); do
        if ! pgrep -u metin2 -f "$pattern" >/dev/null; then return 0; fi
        sleep 1
    done
    return 1
}
case ${1:-} in
    ready)
        test -f "$work/READY"
        test ! -f "$work/INSTALLED"
        test ! -f "$work/QUEST_CHANGED"
        ;;
    prepare)
        test ! -f "$work/READY"
        test ! -f "$work/QUEST_CHANGED"
        mkdir -p "$work"
        cp "$quest/qc" "$quest/quest_functions" "$work/"
        chmod 755 "$work/qc"
        cd "$work"
        sha256 "$quest/quest_tr/_npc_talk_mission/welcome.lua" >source-baseline.sha256
        ./qc /usr/home/cleanup_welcome.lua
        test -s object/state/welcome
        sha256 /usr/home/cleanup_welcome.lua >candidate-source.sha256
        owned >candidate-files.txt
        while IFS= read -r file; do sha256 "$file"; done <candidate-files.txt >candidate.sha256
        touch READY
        echo 'WELCOME QUEST READY: compiled; live unchanged'
        ;;
    health) health ;;
    stop)
        pkill -TERM -u metin2 -f "$games" || true
        wait_exit "$games"
        pkill -TERM -u metin2 -f "$database" || true
        wait_exit "$database"
        ;;
    stopped)
        stopped
        ;;
    quest-install)
        stopped
        test -f "$work/READY"
        cd "$work"
        sha256 "$quest/quest_tr/_npc_talk_mission/welcome.lua" | cmp source-baseline.sha256 -
        sha256 /usr/home/cleanup_welcome.lua | cmp candidate-source.sha256 -
        while IFS= read -r file; do sha256 "$file"; done <candidate-files.txt | cmp candidate.sha256 -
        cp "$quest/quest_tr/_npc_talk_mission/welcome.lua" previous-source.lua
        cd "$quest"
        owned >"$work/previous-files.txt"
        tar -cpf "$work/previous-objects.tar" -T "$work/previous-files.txt"
        touch "$work/QUEST_CHANGED"
        while IFS= read -r file; do rm -f "$file"; done <"$work/previous-files.txt"
        while IFS= read -r file; do
            mkdir -p "$(dirname "$file")"
            cp "$work/$file" "$file"
        done <"$work/candidate-files.txt"
        cp /usr/home/cleanup_welcome.lua "$quest/quest_tr/_npc_talk_mission/welcome.lua"
        echo 'WELCOME QUEST INSTALLED: no forced monster bonus on starter weapons'
        ;;
    quest-rollback)
        if test -f "$work/QUEST_CHANGED"; then
            stopped
            cd "$quest"
            owned >"$work/remove-files.txt"
            while IFS= read -r file; do rm -f "$file"; done <"$work/remove-files.txt"
            tar -xpf "$work/previous-objects.tar"
            cp "$work/previous-source.lua" "$quest/quest_tr/_npc_talk_mission/welcome.lua"
            rm -f "$work/QUEST_CHANGED"
        fi
        ;;
    quest-commit)
        rm -f "$work/QUEST_CHANGED"
        touch "$work/INSTALLED"
        ;;
    start)
        stopped
        service metin2 start </dev/null >"$work/restart.log" 2>&1
        for attempt in $(jot 20); do
            if health; then exit 0; fi
            sleep 1
        done
        exit 1
        ;;
    *) exit 2 ;;
esac
