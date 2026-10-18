# Layout cutover (VM) — run by hand

Repo side is done on `main` (tag `pre-layout-20261018` = pre-move). Live FreeBSD tree is still `/usr/metin2/Source/Server` until you install.

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
# Source/Server is a symlink to apps/server
```
