#!/bin/bash
# Runs inside the m2web-build container: giflib 5.2.2 (the version of
# extern/include/gif_lib.h) -> /work/kit/build/port/lib/libgif.a
set -euo pipefail
source /work/emsdk/emsdk_env.sh >/dev/null 2>&1
V=giflib-5.2.2
W=/work/vendor/giflib
OUT=/work/kit/build/port/lib/libgif.a
mkdir -p "$W" && cd "$W"
if [ ! -d "$V" ]; then
    curl -fsSL "https://downloads.sourceforge.net/project/giflib/giflib-5.x/$V.tar.gz" -o sf.tar.gz
    curl -fsSL "https://deb.debian.org/debian/pool/main/g/giflib/giflib_5.2.2.orig.tar.gz" -o deb.tar.gz
    a=$(sha256sum sf.tar.gz | cut -d' ' -f1); b=$(sha256sum deb.tar.gz | cut -d' ' -f1)
    echo "sha256 sourceforge=$a debian=$b"
    [ "$a" = "$b" ] && [ "$a" = be7ffbd057cadebe2aa144542fd90c6838c6a083b5e8a9048b8ee3b66b29d5fb ] || { echo "MISMATCH - not building"; exit 1; }
    tar xzf sf.tar.gz
fi
cd "$V"
rm -f *.o
for f in dgif_lib egif_lib gifalloc gif_err gif_font gif_hash openbsd-reallocarray; do
    emcc -c -O2 -w "$f.c" -o "$f.o"
done
rm -f "$OUT"
emar rcs "$OUT" *.o
/work/emsdk/upstream/bin/llvm-nm "$OUT" | grep -E ' T (DGifSlurp|DGifOpenFileName|DGifCloseFile|DGifSavedExtensionToGCB|GifErrorString)$'
