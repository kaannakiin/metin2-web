#!/bin/bash
# Deploys the corpus to the metin2-corpus Worker (static assets on
# metin2.kaanakin.dev/corpus/*). Runs on the host before the site sync.
# Only the current build is deployed: players on an older page must reload.
set -euo pipefail
S=/home/m2web/kit/dist/site/corpus
C=/home/m2web/cdn
ENV=/root/.cloudflare/metin2-cdn.env
WRANGLER=wrangler@4.146.0

[ -s "$ENV" ] || { echo "no $ENV - not deploying"; exit 1; }
[ -s "$S/manifest.bin" ] && [ -s "$S/order.txt" ] || { echo "no corpus in $S - not deploying"; exit 1; }
n=$(ls "$S" | grep -cE '^[0-9a-f]{32}\.bin$')
[ "$n" -gt 1000 ] || { echo "corpus has $n chunks - not deploying"; exit 1; }

rm -rf "$C/public"
mkdir -p "$C/public"
cp -al "$S" "$C/public/corpus"
cp "$C/_headers" "$C/public/_headers"

echo "deploying $n chunks ($(du -sh "$C/public/corpus" | cut -f1))"
docker run --rm -v "$C":/cdn -w /cdn --env-file "$ENV" node:22-alpine npx --yes "$WRANGLER" deploy
echo CDN_DEPLOYED
