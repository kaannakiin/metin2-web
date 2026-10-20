#!/usr/bin/env bash
# Host-side, private preview only. Never runs publish/deploy or changes VM services.
set -euo pipefail
cd /home/m2web
mkdir -p dev
exec 9>dev/client-build.lock
flock -n 9 || { echo 'Another development build is running'; exit 1; }
action=${1:-cpp}
protocol=${2:-}
if [ -z "$protocol" ]; then
    protocol=source
    [ ! -f dev/protocol ] || protocol=$(cat dev/protocol)
fi
case "$protocol" in source|live-yohara) ;; *) echo 'Invalid development protocol preset'; exit 2 ;; esac
if [ "$action" = stop ]; then
    docker rm -f m2web-dev-bridge >/dev/null 2>&1 || true
    if [ -f dev/preview.pid ]; then
        pid=$(cat dev/preview.pid)
        if [[ "$pid" =~ ^[0-9]+$ ]] && [ -r "/proc/${pid}/cmdline" ] && \
            tr '\0' ' ' <"/proc/${pid}/cmdline" | grep -q 'tools/dev_preview.py serve'; then
            kill "$pid"
        fi
        rm -f dev/preview.pid
    fi
    echo 'Development preview stopped'
    exit 0
fi
if [ "$action" != serve ]; then
    client_ip=${SSH_CONNECTION-}
    client_ip=${client_ip%% *}
    [ -n "$client_ip" ] || { echo 'Run the development build through SSH from your Mac'; exit 1; }
    legacy_detector=0
    [ "$protocol" != live-yohara ] || legacy_detector=1
    docker exec -e M2W_DEV_CLIENT_IP="$client_ip" -e M2W_DEV_PROTOCOL="$protocol" \
        -e M2W_LEGACY_DETECTOR="$legacy_detector" \
        m2web-build bash /work/dev_client_build.sh "$action"
    printf '%s\n' "$protocol" >dev/protocol
fi
[ -f dev/site/current/client.html ] || { echo 'Build a preview first (cpp/ui/link)'; exit 1; }
[ -f dev/bridge.json ] || { echo 'Missing development bridge config'; exit 1; }
[ -d /home/m2web/bridge/node_modules/ws ] || { echo 'Missing existing bridge dependency ws'; exit 1; }

# A separate loopback bridge; production origins/configuration stay intact.
if [ "$action" != serve ]; then
    docker rm -f m2web-dev-bridge >/dev/null 2>&1 || true
fi
if ! docker inspect -f '{{.State.Running}}' m2web-dev-bridge 2>/dev/null | grep -qx true; then
    docker rm -f m2web-dev-bridge >/dev/null 2>&1 || true
    docker run -d --name m2web-dev-bridge --network host --user 1000:1000 --read-only \
        --cap-drop ALL --security-opt no-new-privileges --env NODE_PATH=/deps \
        -v /home/m2web/kit/bridge:/app:ro \
        -v /home/m2web/bridge/node_modules:/deps:ro \
        -v /home/m2web/dev/bridge.json:/config/bridge.json:ro \
        -w /app node:20-alpine node src/dev.js /config/bridge.json >/dev/null
fi
if ! python3 -c 'import json,urllib.request; assert json.load(urllib.request.urlopen("http://127.0.0.1:18731/__dev_health", timeout=2))["preview"] is True' >/dev/null 2>&1; then
    nohup python3 /home/m2web/kit/tools/dev_preview.py serve \
        --root /home/m2web/dev/site/current >dev/preview.log 2>&1 </dev/null 9>&- &
    echo "$!" >dev/preview.pid
fi
python3 -c 'import socket,time
for port in (18731,18732):
 for attempt in range(30):
  try:
   with socket.create_connection(("127.0.0.1",port),timeout=1): pass
   break
  except OSError:
   if attempt == 29: raise
   time.sleep(0.1)'
python3 -c 'import json,urllib.request; assert json.load(urllib.request.urlopen("http://127.0.0.1:18731/__dev_health", timeout=2))["preview"] is True'
docker inspect -f '{{.State.Running}}' m2web-dev-bridge | grep -qx true
echo 'READY: SSH-forward ports 18731 and 18732; open http://127.0.0.1:18731/client.html'
