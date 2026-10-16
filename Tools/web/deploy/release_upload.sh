#!/bin/bash
# Runs on the developer machine from the repo: sends the committed server
# sources, bridge and deploy scripts to the host for server_release.sh.
set -euo pipefail

HOST=root@88.99.1.151
PATHS=(
    Source/Server
    Tools/web/kit/bridge/src
    Tools/web/kit/tools/bridge_config.py
    Tools/web/kit/webclient.toml
    Tools/web/deploy/deploy.sh
    Tools/web/deploy/server_release.sh
)

cd "$(git rev-parse --show-toplevel)"

if [ -n "$(git status --porcelain -- "${PATHS[@]}")" ]; then
    echo "uncommitted changes under the release paths; commit them first:" >&2
    git status --short -- "${PATHS[@]}" >&2
    exit 1
fi

commit=$(git rev-parse --short HEAD)
git archive --format=tar HEAD "${PATHS[@]}" | ssh -o BatchMode=yes "$HOST" "
    set -e
    rm -rf /root/metin2-release
    mkdir -p /root/metin2-release
    tar -x -C /root/metin2-release
    echo $commit > /root/metin2-release/COMMIT
    chmod 700 /root/metin2-release/Tools/web/deploy/server_release.sh
    echo uploaded $commit"
