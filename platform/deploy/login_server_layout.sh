#!/usr/bin/env bash
# Compile a size-only probe in VM /tmp; never attach to/restart game services.
set -euo pipefail
# Measures the VM source headers, NOT the already-running binary. Old installed
# binaries can have a different layout; inspect their DWARF or the wire too.
vm=(ssh -o BatchMode=yes -i /root/.ssh/metin2_vm root@192.168.122.10)
probe=$("${vm[@]}" mktemp -d /tmp/m2-login-layout.XXXXXX)
trap '"${vm[@]}" "rm -rf -- ${probe}"' EXIT
scp -q -i /root/.ssh/metin2_vm /home/m2web/login_server_layout.cpp "root@192.168.122.10:${probe}/sizes.cpp"
"${vm[@]}" "cd /usr/metin2/apps/server/game/src && c++ -std=c++20 -DNDEBUG -D_LIBCPP_HARDENING_MODE=_LIBCPP_HARDENING_MODE_NONE -I. -I/usr/local/include -I/usr/local/include/mysql -I../../library/liblua/include -I../../library -w ${probe}/sizes.cpp -o ${probe}/sizes && ${probe}/sizes"
