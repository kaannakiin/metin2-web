#!/usr/bin/env bash
# Operator entry point: installs the tested market candidate with VM rollback.
set -euo pipefail
cd /home/m2web
stage=/usr/metin2-progression-20261022-202621
release=progression-20261022-202621
exec 9>dev/client-build.lock
flock -n 9 || { echo 'Another client build/release is running'; exit 1; }
test -f "$release/READY"
ssh -n -o BatchMode=yes -i /root/.ssh/metin2_vm root@192.168.122.10 \
    "sh $stage/progression_vm.sh install $stage"
ssh -n -o BatchMode=yes -i /root/.ssh/metin2_vm root@192.168.122.10 \
    "test -f $stage/INSTALLED"
touch "$release/INSTALLED"
echo "NPC MARKET INSTALLED: $stage"
