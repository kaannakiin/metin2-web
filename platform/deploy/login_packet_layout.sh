#!/usr/bin/env bash
set -euo pipefail
source /work/emsdk/emsdk_env.sh >/dev/null 2>&1
cd /work/kit
python3.13 tools/login_packet_layout.py
