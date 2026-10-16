#!/bin/bash
# Runs on the host as root, from /root/metin2-release (filled by release_upload.sh).
#   stage    copy the server sources to the VM (/usr/metin2-next) and list what differs
#   build    compile there; binaries go to /usr/metin2-next/out, the live ones are untouched
#   install  maintenance window: swap binaries, add TRUSTED_PROXY_IP, restart, then the bridge
#   rollback previous binaries and a bridge without the PROXY line
set -euo pipefail

RELEASE=/root/metin2-release
VM="ssh -o BatchMode=yes -i /root/.ssh/metin2_vm root@192.168.122.10"
KIT=/home/m2web/kit
TRUSTED_PROXY_IP=192.168.122.1

[ -f "$RELEASE/COMMIT" ] || { echo "no release in $RELEASE; run release_upload.sh first" >&2; exit 1; }
echo "release $(cat "$RELEASE/COMMIT")"

stage() {
    tar -C "$RELEASE" -cf - Source/Server | $VM '
        set -e
        rm -rf /usr/metin2-next
        mkdir -p /usr/metin2-next/out
        tar -x -C /usr/metin2-next -f -
        cd /usr/metin2-next/Source/Server
        echo "--- files that differ from the live tree /usr/metin2/Source/Server:"
        diff -rq -x "*.o" -x "*.d" -x "*.a" -x ".obj" -x "Depend" -x "*.core" \
            /usr/metin2/Source/Server . | sed "s|/usr/metin2/Source/Server/||" || true'
    echo "Check the list: every file should be one this release changed. Anything else means the VM tree has local changes the release would drop."
}

build() {
    $VM '
        set -e
        cd /usr/metin2-next/Source/Server
        if ! gmake -j4 all GAMEDIR=/usr/metin2-next/out DBDIR=/usr/metin2-next/out > /usr/metin2-next/build.log 2>&1; then
            grep -E "error|Error" /usr/metin2-next/build.log | head -40
            echo "BUILD FAILED, full log: /usr/metin2-next/build.log on the VM"
            exit 1
        fi
        ls -l /usr/metin2-next/out'
}

install_kit() {
    echo "--- webclient.toml changes:"
    diff -u "$KIT/webclient.toml" "$RELEASE/Tools/web/kit/webclient.toml" || true
    read -r -p "Apply this webclient.toml? [y/N] " answer
    [ "$answer" = y ] || { echo "stopped before touching the host kit" >&2; exit 1; }

    cp -a "$RELEASE/Tools/web/kit/bridge/src/." "$KIT/bridge/src/"
    cp "$RELEASE/Tools/web/kit/tools/bridge_config.py" "$KIT/tools/bridge_config.py"
    cp "$RELEASE/Tools/web/kit/webclient.toml" "$KIT/webclient.toml"
    chown -R --reference="$KIT" "$KIT/bridge/src" "$KIT/tools/bridge_config.py" "$KIT/webclient.toml"
    cp "$RELEASE/Tools/web/deploy/deploy.sh" /home/m2web/deploy.sh
    chmod 755 /home/m2web/deploy.sh

    docker exec m2web-build bash -c 'cd /work/kit && python3.13 tools/bridge_config.py --site https://metin2.kaanakin.dev'
    grep -q '"proxyProtocol": true' "$KIT/build/port/private/bridge-site.json" ||
        { echo "bridge-site.json has no proxyProtocol: true" >&2; exit 1; }
}

install() {
    $VM 'test -x /usr/metin2-next/out/game && test -x /usr/metin2-next/out/db' ||
        { echo "no built binaries on the VM; run build first" >&2; exit 1; }

    # Before the restart: a mistake here must not leave the server down.
    install_kit

    $VM "
        set -e
        ts=\$(date +%Y%m%d-%H%M%S)
        cd /usr/home/share/bin
        cp -p game game.bak-\$ts
        cp -p db db.bak-\$ts
        for f in \$(find /usr/home/main -name CONFIG); do
            grep -q '^TRUSTED_PROXY_IP:' \$f || printf '\nTRUSTED_PROXY_IP: $TRUSTED_PROXY_IP\n' >> \$f
        done
        service metin2 stop || true
        owner=\$(stat -f %u:%g game.bak-\$ts)
        cp /usr/metin2-next/out/game game
        cp /usr/metin2-next/out/db db
        chown \$owner game db
        chmod 755 game db
        service metin2 start
        mv /usr/metin2 /usr/metin2-prev-\$ts
        mv /usr/metin2-next /usr/metin2
        echo binaries replaced, backups: game.bak-\$ts db.bak-\$ts"

    /home/m2web/deploy.sh
    sleep 5
    docker logs --tail 20 m2web-bridge
    echo "Log in from the browser now. Bridge log lines should carry real player addresses."
}

rollback() {
    $VM '
        set -e
        cd /usr/home/share/bin
        game=$(ls -t game.bak-* | head -1)
        db=$(ls -t db.bak-* | head -1)
        service metin2 stop || true
        cp -p "$game" game
        cp -p "$db" db
        service metin2 start
        echo "restored $game $db"'
    sed -i 's/"proxyProtocol": true/"proxyProtocol": false/' /home/m2web/bridge/bridge-site.json
    sed -i 's/^proxy_protocol = true$/proxy_protocol = false/' "$KIT/webclient.toml"
    grep -q '"proxyProtocol": false' /home/m2web/bridge/bridge-site.json &&
        grep -q '^proxy_protocol = false$' "$KIT/webclient.toml" ||
        { echo "could not turn the PROXY line off in bridge-site.json or webclient.toml" >&2; exit 1; }
    docker restart m2web-bridge
    echo "Bridge restarted without the PROXY line; webclient.toml now says proxy_protocol = false, so a later bridge_config.py keeps it off."
    echo "TRUSTED_PROXY_IP stays in the CONFIGs; the old binaries ignore it."
}

case "${1:-}" in
    stage) stage ;;
    build) build ;;
    install) install ;;
    rollback) rollback ;;
    *) echo "usage: $0 stage|build|install|rollback" >&2; exit 2 ;;
esac
