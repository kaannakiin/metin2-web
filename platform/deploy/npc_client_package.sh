#!/usr/bin/env bash
# Package the already built APPLY-ID fix. Publication is a separate final step.
set -euo pipefail
source /work/emsdk/emsdk_env.sh >/dev/null 2>&1
cd /work/kit
export M2W_DEV_PROTOCOL=source
python3.13 webclient.py package >/work/dev/logs/npc-package.log 2>&1
python3.13 tools/bridge_config.py --site https://metin2.kaanakin.dev
echo 'NPC CLIENT PACKAGE READY: APPLY identifiers match the server; corpus reused.'
