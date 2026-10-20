#!/usr/bin/env bash
set -euo pipefail
cd /home/m2web
mkdir -p dev/packet-audit
exec 9>dev/client-build.lock
flock -n 9 || { echo 'A client build is running; retry after it finishes'; exit 1; }
vm=(ssh -o BatchMode=yes -i /root/.ssh/metin2_vm root@192.168.122.10)
binary=/usr/home/share/bin/game
if [ -n "${1:-}" ]; then
    [[ "$1" =~ ^[0-9]{8}-[0-9]{6}$ ]] || exit 2
    candidate="/usr/metin2-gameplay-$1"
    "${vm[@]}" "test -f '$candidate/READY'"
    binary="$candidate/out/game"
fi
actual=$("${vm[@]}" "sha256 -q '$binary'")
[[ "$actual" =~ ^[a-f0-9]{64}$ ]] || { echo 'Invalid server binary fingerprint'; exit 1; }
cached=''
if [ -f dev/packet-audit/server-game.elf ]; then
    cached=$(sha256sum dev/packet-audit/server-game.elf | cut -d' ' -f1)
fi
if [ "$cached" != "$actual" ]; then
    scp -q -i /root/.ssh/metin2_vm "root@192.168.122.10:$binary" dev/packet-audit/server-game.elf
fi
cached=$(sha256sum dev/packet-audit/server-game.elf | cut -d' ' -f1)
[ "$cached" = "$actual" ] || { echo 'Server binary changed during read; retry audit'; exit 1; }
docker exec m2web-build bash /work/packet_abi_export.sh
echo "SERVER_BINARY_SHA256=$actual"
