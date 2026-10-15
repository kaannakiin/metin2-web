#!/bin/bash
# Runs on the host (88.99.1.151) after `webclient.py package` and
# `tools/bridge_config.py --site https://metin2.kaanakin.dev` in m2web-build.
set -euo pipefail

rm -rf /home/m2web/bridge && mkdir -p /home/m2web/bridge
cp -a /home/m2web/kit/bridge/package.json /home/m2web/kit/bridge/package-lock.json /home/m2web/kit/bridge/src /home/m2web/bridge/
cp /home/m2web/kit/build/port/private/bridge-site.json /home/m2web/bridge/
docker run --rm -v /home/m2web/bridge:/app -w /app node:20-alpine npm ci --omit=dev --ignore-scripts
chown -R 1000:1000 /home/m2web/bridge && chmod 640 /home/m2web/bridge/bridge-site.json

# host network: containers on the coolify network cannot reach the libvirt VM
docker rm -f m2web-bridge >/dev/null 2>&1 || true
docker run -d --name m2web-bridge --restart unless-stopped --network host --user 1000:1000 --read-only \
    -v /home/m2web/bridge:/app:ro -w /app node:20-alpine node src/index.js bridge-site.json

# the site serves /home/m2web/www, filled only by publish.sh (checks the package first)
/home/m2web/publish.sh

docker rm -f m2web-site >/dev/null 2>&1 || true
docker run -d --name m2web-site --restart unless-stopped --network coolify \
    -v /home/m2web/www:/usr/share/nginx/html:ro \
    -v /home/m2web/site-nginx.conf:/etc/nginx/conf.d/default.conf:ro nginx:1.27-alpine

# one-time, already applied:
#   ufw allow from 10.0.1.0/24 to 10.0.1.1 port 11496 proto tcp comment "metin2 bridge, traefik only"
#   cp metin2.yaml /data/coolify/proxy/dynamic/metin2.yaml
