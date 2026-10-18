# Layout cutover (VM) — run by hand

Repo is hard-cut (tags: `pre-layout-20261018` = pre-move, `pre-hardcut-20261018` = pre-symlink-drop). Live FreeBSD tree may still be `/usr/metin2/Source/Server` until you install; after install it is only `/usr/metin2/apps/server`.

Do **not** skip the backup. `install` restarts `metin2` and the bridge.

```sh
# 1) Mac — upload committed release tree
cd /path/to/metin2
platform/deploy/release_upload.sh

# 2) Host — backup (no service restart)
scp platform/deploy/layout_cutover_backup.sh root@88.99.1.151:/root/
ssh root@88.99.1.151 'bash /root/layout_cutover_backup.sh'

# 3) Host — stage + build (live binaries untouched)
ssh root@88.99.1.151 '/root/metin2-release/platform/deploy/server_release.sh stage'
ssh root@88.99.1.151 '/root/metin2-release/platform/deploy/server_release.sh build'

# 4) Maintenance window — install (interactive: confirms webclient.toml)
ssh root@88.99.1.151 '/root/metin2-release/platform/deploy/server_release.sh install'

# 5) Smoke: browser login; bridge logs show real client IPs
# Rollback if needed:
#   ssh root@88.99.1.151 '/root/metin2-release/platform/deploy/server_release.sh rollback'
```

After a successful install, `gmake` on the VM:

```sh
cd /usr/metin2/apps/server && gmake -j4 all
```

## Rollback (keep old tree)

Install already renames the previous live tree to `/usr/metin2-prev-<timestamp>` and copies `game.bak-*` / `db.bak-*` under `/usr/home/share/bin`. Host tarballs from `layout_cutover_backup.sh` live in `/root/backups/`.

Quick rollback (VM, as root) — swap trees + restore binaries, no need for the tarball unless the prev dir is gone:

```sh
# on VM
ts=20261018-102041   # use the stamp from ls /usr/metin2-prev-*
service metin2 stop || true
mv /usr/metin2 /usr/metin2-failed-hardcut
mv /usr/metin2-prev-$ts /usr/metin2
cd /usr/home/share/bin
cp -p game.bak-$ts game
cp -p db.bak-$ts db
service metin2 start
```

Tarball restore (host → VM) if prev dir is missing:

```sh
# on host
ssh -i /root/.ssh/metin2_vm root@192.168.122.10 'service metin2 stop || true; rm -rf /usr/metin2; tar -C /usr -xf -' \
  < /root/backups/metin2-tree-20261018-hardcut.tar
ssh -i /root/.ssh/metin2_vm root@192.168.122.10 'tar -C /usr/home/share -xf -; service metin2 start' \
  < /root/backups/metin2-bin-20261018-hardcut.tar
```

## Status 2026-10-18

Hard-cut install of `8cceb8e22` succeeded:

- Live: `/usr/metin2/apps/server` (no `Source/`)
- Kept: `/usr/metin2-prev-20261018-102041` (old `Source/Server` tree)
- Host backups: `/root/backups/metin2-{tree,bin}-20261018-hardcut.tar`
- Bin bak: `game.bak-20261018-102041`, `db.bak-20261018-102041`
- Smoke: auth/ch1/ch99 ports up; `https://metin2.kaanakin.dev/` and `/client.html` → 200; bridge sessions with real client IPs
