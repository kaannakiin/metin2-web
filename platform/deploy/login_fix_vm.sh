#!/bin/sh
set -eu
action=${1:?build or install}
stage=${2:?absolute build directory required}
case "$stage" in /usr/metin2-login-fix-[0-9]*-[0-9]*) ;; *) exit 2 ;; esac
case "$action" in
build)
    cd "$stage"
    test ! -e READY
    tar -xzf source.tar.gz
    mkdir -p out
    cd apps/server
    gmake -j4 all "GAMEDIR=$stage/out" "DBDIR=$stage/out"
    test -x "$stage/out/game"
    test -x "$stage/out/db"
    sha256 "$stage/out/game" "$stage/out/db"
    touch "$stage/READY"
    echo "READY: game + db built; live services untouched."
    ;;
install)
    # Deliberately manual: run by the operator during a maintenance window.
    test -f "$stage/READY"
    test ! -e "$stage/INSTALLED"
    test -x "$stage/out/game"
    test -x "$stage/out/db"
    backup="$stage/previous-bin"
    mkdir -m 700 "$backup"
    cp -p /usr/home/share/bin/game /usr/home/share/bin/db "$backup/"
    service metin2 stop </dev/null >/dev/null 2>&1
    restore() {
        cp -p "$backup/game" "$backup/db" /usr/home/share/bin/
        service metin2 start </dev/null >/dev/null 2>&1 || true
    }
    trap 'restore' HUP INT TERM
    if ! cp "$stage/out/game" "$stage/out/db" /usr/home/share/bin/; then
        restore
        exit 1
    fi
    chmod 755 /usr/home/share/bin/game /usr/home/share/bin/db
    if ! service metin2 start </dev/null >"$stage/start.log" 2>&1; then
        restore
        echo "Start failed; previous binaries restored. See $stage/start.log" >&2
        exit 1
    fi
    trap - HUP INT TERM
    touch "$stage/INSTALLED"
    service metin2 status
    echo "Installed both matching binaries. Previous copies: $backup"
    ;;
*) exit 2 ;;
esac
