#!/bin/bash
# Runs inside the m2web-build container: /work/anka2/apps/client -> /work/websrc
set -euo pipefail
cd /work
[ -d websrc ] || cp -aL anka2/apps/client websrc

L=websrc/source/UserInterface/Locale_inc.h
for f in ENABLE_FOXFS_ENCRYPT ENABLE_DIRECTX9_UPDATE ENABLE_LOAD_INDEX_BINARY \
         ENABLE_FIX_MOBS_LAG FPS_APPLICATON_DEVICE_LIMITATION; do
    sed -i -E "s|^#define $f\b|//#define $f|" "$L"
done
grep -naE '^(//)?#define (ENABLE_FOXFS_ENCRYPT|ENABLE_DIRECTX9_UPDATE|ENABLE_LOAD_INDEX_BINARY|ENABLE_FIX_MOBS_LAG|FPS_APPLICATON_DEVICE_LIMITATION)\b' "$L" | cut -c1-70

# the repo's `Debug/` ignore rule also swallowed boost/preprocessor/debug
B=websrc/extern/include/boost/preprocessor/debug
if [ ! -f "$B/error.hpp" ]; then
    mkdir -p "$B"
    for h in assert error line; do
        curl -fsSL "https://raw.githubusercontent.com/boostorg/preprocessor/boost-1.67.0/include/boost/preprocessor/debug/$h.hpp" -o "$B/$h.hpp"
    done
fi
ls "$B"
