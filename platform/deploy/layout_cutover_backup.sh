#!/bin/bash
# Phase-2 helper (run on the host as root, before server_release.sh install).
# Creates tarball backups of the live VM source tree and share/bin binaries.
# Does NOT restart services.
set -euo pipefail

STAMP=${1:-$(date +%Y%m%d)}
BACKUP_DIR=${BACKUP_DIR:-/root/backups}
VM="ssh -o BatchMode=yes -i /root/.ssh/metin2_vm root@192.168.122.10"

mkdir -p "$BACKUP_DIR"

echo "Backing up /usr/metin2 on the VM -> $BACKUP_DIR/metin2-tree-$STAMP.tar"
$VM "tar -C /usr -cf - metin2" > "$BACKUP_DIR/metin2-tree-$STAMP.tar"

echo "Backing up /usr/home/share/bin on the VM -> $BACKUP_DIR/metin2-bin-$STAMP.tar"
$VM "tar -C /usr/home/share -cf - bin" > "$BACKUP_DIR/metin2-bin-$STAMP.tar"

if [ -f /root/metin2-release/COMMIT ]; then
    cp /root/metin2-release/COMMIT "$BACKUP_DIR/metin2-release-COMMIT-$STAMP"
    echo "Noted release COMMIT $(cat /root/metin2-release/COMMIT)"
fi

ls -lh "$BACKUP_DIR/metin2-tree-$STAMP.tar" "$BACKUP_DIR/metin2-bin-$STAMP.tar"
echo "OK. Next: platform/deploy/server_release.sh stage && build && (maintenance) install"
