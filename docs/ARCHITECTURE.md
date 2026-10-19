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

| Goal                          | Path                                      |
| ----------------------------- | ----------------------------------------- |
| Combat / skills / items logic | `apps/server/game/`                       |
| Client C++ / Python UI engine | `apps/client/source/`                     |
| Item icons, maps, `root/*.py` | `content/client/packs/`                   |
| Drop tables, item_proto text  | `runtime/freebsd/share/` (and `main/db/`) |
| SQL seeds                     | `content/server/sql/`                     |
| Portal register/login         | `apps/portal/`                            |
| WASM kit / bridge / publish   | `platform/`                               |

## VM cutover

Until the first `server_release.sh install` from this layout, the live FreeBSD tree may still be `/usr/metin2/Source/Server`. Staging uses only `/usr/metin2-next/apps/server`. Backup helper: `platform/deploy/layout_cutover_backup.sh` (host, as root). After install: `/usr/metin2/apps/server`.

## Design docs (PvP / content)

| Doc | Role |
|-----|------|
| [`../PVP_HEDEF.md`](../PVP_HEDEF.md) | 1–99 mid-easy design lock: exp/yang/shop, feature Açık/Kapalı |
| [`ROADMAP_PVP.md`](ROADMAP_PVP.md) | Phases 0–6, exit criteria, near-term order |
| [`MID_PVP_FAZ0_1.md`](MID_PVP_FAZ0_1.md) | **Done log** for Faz 0+1 — do not re-implement |
| [`../CALISMA_NOTLARI.md`](../CALISMA_NOTLARI.md) | Web / deploy / VM running log (not game balance) |
| [`../platform/deploy/VM_MID_PVP_APPLY.md`](../platform/deploy/VM_MID_PVP_APPLY.md) | Host/VM apply checklist for Faz 0/1 |
| [`../platform/tools/mid_pvp_*.py`](../platform/tools/) | Offline sim / flag / economy / safe-map asserts |

## Follow-ups (not done yet)

- Split `runtime/freebsd/share/{locale,conf}` into `content/server/` and generate the runtime tree.
