# Repository architecture

Canonical layout after the 2026-10 hard-cut. There are no compat symlinks for old names — edit these paths only. Rollback tag: `pre-hardcut-20261018`.

## Tree

```text
apps/
  server/                 # game / db / auth (C++)
  client/                 # Windows + WASM client engine
  portal/                 # TanStack Start site
content/
  client/
    packs/                # unpacked assets (icons, maps, root UI, …)
    runtime/              # pack output tree + configs for the kit
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
  archiver/               # pack XML → ../../content/client/packs
  dump_proto/
```

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

Until the first `server_release.sh install` from this layout, the live FreeBSD tree may still be `/usr/metin2/Source/Server`. Staging uses only `/usr/metin2-next/apps/server`. Backup helper: `platform/deploy/layout_cutover_backup.sh` (host, as root). After install: `/usr/metin2/apps/server`.

## Follow-ups (not done yet)

- Split `runtime/freebsd/share/{locale,conf}` into `content/server/` and generate the runtime tree.
