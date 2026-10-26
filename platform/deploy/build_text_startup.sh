#!/usr/bin/env bash
# Refresh Python-only release inputs without starting a private preview.
set -euo pipefail
source /work/emsdk/emsdk_env.sh >/dev/null 2>&1
cd /work/kit
export M2W_DEV_PROTOCOL=source
export M2W_LEGACY_DETECTOR=0
log=/work/dev/logs/text-startup-rewrite.log
if ! python3.13 webclient.py build --only rewrite >"$log" 2>&1; then
    tail -20 "$log"
    exit 1
fi
grep -E 'NOT parsing after|stdlib collections|semantic patches:' "$log" || true
M2W_BOOT_SYSTEM=/work/kit/build/port/scripts3/system.py \
    python3.13 -B -m unittest discover -s tools -p test_python_startup.py
