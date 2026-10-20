#!/usr/bin/env bash
set -euo pipefail
source /work/emsdk/emsdk_env.sh >/dev/null 2>&1
cd /work/kit
python3.13 tools/packet_abi_export.py --output /work/dev/packet-audit/client-layout.json
