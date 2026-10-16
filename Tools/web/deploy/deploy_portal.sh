#!/bin/bash
# Runs on the host after web/portal is synced to /home/m2web/portal-src
# (rsync without node_modules, dist and .env*). Builds in a scratch copy and
# swaps it in only after the tests and the build pass.
set -euo pipefail
SRC=/home/m2web/portal-src
APP=/home/m2web/portal
ENV=/root/.metin2/portal.env
IMAGE=node:22-alpine

[ -s "$ENV" ] || { echo "no $ENV - not deploying"; exit 1; }
rm -rf "$APP.new"
cp -a "$SRC" "$APP.new"
docker run --rm -v "$APP.new":/app -w /app "$IMAGE" sh -c \
    "npm ci --no-audit --no-fund && npm test && npm run build && npm prune --omit=dev --no-audit --no-fund"
chown -R 1000:1000 "$APP.new"

rm -rf "$APP.old"
[ -d "$APP" ] && mv "$APP" "$APP.old"
mv "$APP.new" "$APP"

# host network: the portal reaches MariaDB on the libvirt VM, which the coolify network cannot
docker rm -f m2web-portal >/dev/null 2>&1 || true
docker run -d --name m2web-portal --restart unless-stopped --network host --user 1000:1000 --read-only \
    --env-file "$ENV" -v "$APP":/app:ro -w /app "$IMAGE" node server.ts

# UFW lets only this address reach 11496/11497; if Coolify recreates the proxy
# with another IP, the site goes dark until both rules are moved.
TRAEFIK_IP=10.0.1.6
live_ip=$(docker inspect coolify-proxy --format '{{(index .NetworkSettings.Networks "coolify").IPAddress}}')
[ "$live_ip" = "$TRAEFIK_IP" ] || echo "WARNING: coolify-proxy is $live_ip, UFW allows $TRAEFIK_IP - move the 11496/11497 rules"

for i in 1 2 3 4 5 6 7 8 9 10; do
    curl -fsS -o /dev/null "http://10.0.1.1:11497/" && { echo PORTAL_DEPLOYED; exit 0; }
    sleep 1
done
docker logs --tail 30 m2web-portal
echo "portal did not answer"
exit 1

# one-time, already applied:
#   ufw allow from 10.0.1.6 to 10.0.1.1 port 11497 proto tcp comment "metin2 portal, traefik only"
