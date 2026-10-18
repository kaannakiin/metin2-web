# Repository architecture

Canonical layout after the 2026-10 layout migration. Old path names remain as **compat symlinks** for one cycle; edit the real paths only.

## Tree

```text
apps/
  server/                 # game / db / auth (C++)
  client/                 # Windows + WASM client engine
  portal/                 # TanStack Start site
content/
  client/
    packs/                # unpacked assets (icons, maps, root UI, …)
    runtime/              # Client/ pack tree + configs for the kit
  server/
    sql/                  # schema, migrations, seeds
runtime/
  freebsd/                # VM /usr/home mirror (main + share)
platform/
  web-kit/                # Metin2-WebClient kit forks
  deploy/                 # Traefik, publish, server_release
  cdn/                    # corpus Worker
  make_eterpacks.py
vendor/                   # jpeg-9d, FoxFS_Src, DumpProto
Tools/
  archiver/               # pack XML (still uses ../binary_unpack via symlink)
  dump_proto/
```

## Compat symlinks

| Symlink | Target |
|---------|--------|
| `Source/Server` | `apps/server` |
| `Source/Binary` | `apps/client` |
| `Client` | `content/client/runtime` |
| `Tools/binary_unpack` | `content/client/packs` |
| `Tools/web/kit` | `platform/web-kit` |
| `Tools/web/deploy` | `platform/deploy` |
| `Tools/web/cdn` | `platform/cdn` |
| `web/portal` | `apps/portal` |
| `home` | `runtime/freebsd` |
| `sql` | `content/server/sql` |

`git archive` does **not** dereference symlinks. `platform/deploy/release_upload.sh` therefore lists `apps/server` and `platform/…` explicitly.

## Where to change what

| Goal | Path |
|------|------|
| Combat / skills / items logic | `apps/server/game/` |
| Client C++ / Python UI engine | `apps/client/source/` |
| Item icons, maps, `root/*.py` | `content/client/packs/` |
| Drop tables, item_proto text | `runtime/freebsd/share/` (and `main/db/`) |
| SQL seeds | `content/server/sql/` |
| Portal register/login | `apps/portal/` |
| WASM kit / bridge / publish | `platform/` |

## VM cutover

Until the first `server_release.sh install` from this layout, the live FreeBSD tree may still be `/usr/metin2/Source/Server`. Staging uses `/usr/metin2-next/apps/server` and adds `Source/Server` → `apps/server` on the next tree. Backup helper: `platform/deploy/layout_cutover_backup.sh` (host, as root).

## Follow-ups (not done yet)

- Remove compat symlinks once muscle memory and host mounts use real paths.
- Split `runtime/freebsd/share/{locale,conf}` into `content/server/` and generate the runtime tree.
- Rewrite `Tools/archiver/xml/*` to point at `content/client/packs` without the symlink.
