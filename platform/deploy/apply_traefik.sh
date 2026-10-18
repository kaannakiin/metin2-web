#!/bin/bash
# Runs on the host: installs /home/m2web/metin2.yaml as the Traefik route and
# rolls back by itself if the site stops answering through Cloudflare.
set -euo pipefail
LIVE=/data/coolify/proxy/dynamic/metin2.yaml
NEW=/home/m2web/metin2.yaml
SITE=https://metin2.kaanakin.dev

cp -p "$LIVE" "$LIVE.bak"
cp "$NEW" "$LIVE"
sleep 5

code() { curl -s -o /dev/null -w '%{http_code}' --max-time 15 "$@"; }
portal=$(code "$SITE/")
game=$(code "$SITE/client.html")
direct=$(code --resolve metin2.kaanakin.dev:443:88.99.1.151 "$SITE/")
echo "via cloudflare: portal=$portal game=$game; direct to origin: $direct"

if [ "$portal" != 200 ] || [ "$game" != 200 ]; then
    cp -p "$LIVE.bak" "$LIVE"
    echo "ROLLED BACK"
    exit 1
fi
[ "$direct" = 403 ] || echo "WARNING: direct origin request was not refused"
echo TRAEFIK_APPLIED
