# AGENTS.md

Guidance for coding agents working in this repository.

## What this is

A Metin2 server + client fork, self-hosted for ~10 players. The main goal is playing the game **in the browser**: the Windows client (`apps/client`) is compiled to WebAssembly with a third-party port kit (nairoad/Metin2-WebClient, GPL-2.0) and talks to an unmodified-protocol FreeBSD server through a WebSocket→TCP bridge.

`CALISMA_NOTLARI.md` (Turkish) is the running log: what was done, why, what is still open. Read it before touching the web build, the deployment or the VM; update it when you change any of them. It deliberately holds no passwords, only where they live. Map of the tree: `docs/ARCHITECTURE.md`.

## Layout that matters

Real paths (edit these):

- `apps/server` — game/db/auth servers (C++20, 32-bit, FreeBSD, `gmake`). Lua quests, `libthecore`, `libsql`.
- `apps/client` — client engine (C++, Python 2.7 UI, D3D8). Built for Windows with `client.sln`; for the web it is copied to the build container and compiled by the kit.
- `apps/portal` — site in front of the game: TanStack Start (React 19, SSR) + Tailwind 4 + react-hook-form/zod. Register/login talk to the `account` DB; production runs `node server.ts` as container `m2web-portal`.
- `content/client/packs` — unpacked client data (`root`, `locale`, `property`, `zone`…) that becomes EIX/EPK packs via `platform/make_eterpacks.py`.
- `content/client/runtime` — Windows/runtime client tree (configs, `pack/`, …) used by the web kit as `client =`.
- `content/server/sql` — schema/seeds (utf8mb4), reconstructed from the C++ queries.
- `runtime/freebsd` — server runtime tree (configs, `share/locale`, `share/data`, protos) mirrored onto the VM under `/usr/home`.
- `platform/web-kit` — **repo copies** of our kit changes (`stage_port.py`, `compat/`, `tools/`, `site/`, `gr2_bitknit/`, `webclient.toml`). Live kit: `/home/m2web/kit` (= `/work/kit` in the container). A change must land in both places (`scp`).
- `platform/deploy` — Traefik route (`metin2.yaml`), nginx, `deploy.sh`, `publish.sh`, `publish_cdn.sh`, `release_upload.sh`, `server_release.sh`.
- `platform/cdn` — the `metin2-corpus` Worker (assets only); host copy in `/home/m2web/cdn/`.
- `vendor/` — third-party / unused-in-day-to-day (`jpeg-9d`, `FoxFS_Src`, `DumpProto`).
- `Tools/archiver`, `Tools/dump_proto` — pack XML / proto dump tools (archiver CDATA paths point at `content/client/packs`).

No old-name aliases (`Source/`, `Client/`, `home/`, `sql/`, `web/portal`, `Tools/binary_unpack`, `Tools/web/`). Rollback tags: `pre-layout-20261018`, `pre-hardcut-20261018`.

- Portal → game auto-login: `sessionStorage["m2w.autologin"]` (portal `src/lib/launch.ts`) → `client.html` (template `platform/web-kit/site/client.html`) moves it into `/m2w_autologin` in the engine's memory FS in `Module.preRun` → `content/client/packs/root/intrologin.py` reads, deletes and logs in. Changing either side needs no engine rebuild: root pack + `scripts rewrite uiscript data link` + `package`.

## Runtime topology (one Hetzner host, 88.99.1.151)

```text
browser ─https─▶ Cloudflare ─┬─ /corpus/* ─▶ Worker metin2-corpus (static assets, never reaches the host)
                              └─ the rest ──▶ Traefik (coolify-proxy, Cloudflare IPs only)
                                               ├─ /client.*, /preload.js, /sw.js, /asan/ ─▶ m2web-site   (nginx, /home/m2web/www)
                                               ├─ /to/…                                  ─▶ m2web-bridge (node, host network, 10.0.1.1:11496) ─TCP─┐
                                               └─ everything else                        ─▶ m2web-portal (node, host network, 10.0.1.1:11497) ─SQL─┤
                                                                                                                                                    ▼
                                         KVM VM 192.168.122.10 (FreeBSD 14.5 i386): MariaDB 127.0.0.1 + 192.168.122.10 (portal user only),
                                         db 15000, auth 30001, ch99 30003, ch1 30101/30103/30105
```

- Routes: `platform/deploy/metin2.yaml` (live copy `/data/coolify/proxy/dynamic/metin2.yaml`, install with `apply_traefik.sh`, which rolls back if the site stops answering). Every router has an `ipAllowList` of Cloudflare's ranges: the portal trusts `CF-Connecting-IP`, so a direct hit on the origin must get 403. Refresh the ranges from `GET /client/v4/ips` if Cloudflare changes them. UFW lets only `coolify-proxy` (10.0.1.6 on the coolify network) reach 10.0.1.1:11496/11497; if Coolify recreates the proxy with another IP, move both rules (`deploy_portal.sh` warns).
- Portal deploy: sync `apps/portal` to `/home/m2web/portal-src` (no `node_modules`, `dist`, `.env*`), then `/home/m2web/deploy_portal.sh` (tests + build in a scratch copy, then swaps). Secrets live only in `/root/.metin2/portal.env` (root, 600): DB password (`portal@192.168.122.1`, SELECT/INSERT on `account.account` only) and the Turnstile secret (widget `metin2-portal`, site key `0x4AAAAAAFYZbZBCwl5IYp-B`).
- Auto mode refuses VM service restarts and Traefik/IaC changes even with allow rules; prepare a script and hand those steps to the user.

- `metin2.kaanakin.dev` is **proxied by Cloudflare** (Free plan, zone `kaanakin.dev`), managed through the Cloudflare MCP server (`.mcp.json`). Settings and why: `CALISMA_NOTLARI.md` §6.
- Cloudflare: stay on free features only. Never enable anything metered (Argo, Load Balancing, paid add-ons, R2/Workers beyond free limits) without the user's explicit OK. Keep "Always Use HTTPS" off at the edge: Traefik renews Let's Encrypt with the HTTP-01 challenge on port 80.
- The host also runs unrelated production services (mailcow, Coolify apps, tunnels). Never touch them; add new Traefik config as separate files under `/data/coolify/proxy/dynamic/`.
- Game ports are not reachable from the internet; the bridge only accepts the site origin and an allowlist of `ip:port` targets.

## Web client asset/caching model

Understand this before changing nginx, the service worker or adding a CDN:

- `client.html` is `no-cache` and stamps `client.js/.wasm/.data` and `preload.js` with `?v=<build time>`; those are cached for a year. A new build is picked up because the HTML changes.
- Game files are packed into a content-addressed **corpus**: `corpus/<sha256[:32]>.bin` 4 MB chunks (`immutable`), plus `corpus/manifest.bin` (the engine adds `?t=`) and `corpus/groups.txt` (not hashed, so `no-cache`). ~5.4 GB, ~1370 files.
- Corpus layout (`tools/build_corpus.py` + `tools/corpus_groups.py`): `meta` (small descriptors: `.msa .msm .mse .txt`…), `motion` (all races' motion `.gr2`), `boot` (`tools/data/boot_files.txt`, a recorded first session), each in its own chunks; then each map's files together (villages first); then the rest by path. `groups.txt` lists the chunks of those groups and of every `map:<dir>` (its directory, texture set, environment and the property → model → texture closure of its areas).
- `/corpus/*` is served by the `metin2-corpus` Worker (assets only, no script, so requests are free and do not count toward the Workers daily limit; headers from `platform/cdn/_headers`). The client is unaware: it reads the same-origin `corpus/` path (`?corpus=` is ignored on the real site by design). The origin still has a copy; deleting the Worker route falls back to it instantly.
- Cloudflare cache rules for the origin: `?v=` engine files cached at the edge, everything else never cached. Nothing needs purging on publish.
- Only the current build's corpus is deployed (no previous chunks kept): after a publish, players with the game open must reload.
- The engine reads chunks with **synchronous XHR** (`compat/webfs_web.cpp`), which bypasses the service worker and freezes the frame. Only a chunk already in page memory (`m2w.chunks`, budget `?corpusMB`, default 512/768 MB) avoids that, so `compat/runtime.js` `m2w.prefetchStart` fetches groups asynchronously: `meta`/`motion`/`boot` from page load, the maps of the account's characters on the select screen (`PythonNetworkStreamPhaseSelect.cpp`), and the map being entered first. The loading phase holds the main-character packet until that map is in memory or a minute has passed (`__WebMapPrefetched`, `m2w.mapReady`), so the loading screen keeps drawing. Chunks also go to Cache Storage (`m2w-corpus`; chunks of older builds are pruned). There is no whole-corpus download.
- The fork's `ENABLE_CLIENT_PERFORMANCE` login preload (`net.LoadResourcesInCache`) only registers motions on the web; `CPythonPlayerSettingsModule::ProcessDeferredCache` caches them a few ms per frame once their chunks are in memory.
- Languages: `locale/<lang>/` is not in `client.data`; each is `client.locale_<lang>.data/.js` (`build_client_data.py` `split_languages`, `link_client.py` `package_languages`). `client.html` picks the language (`?lang` → localStorage `m2/lang` → `?deflang` → browser → `en`), loads only that package and hands the choice to the engine (`m2w.config.lang`).

## Commands

There is no automated test suite. Verification is: build succeeds, `patchcheck.py` passes, then the user plays in the browser.

Server (on the VM):

```sh
ssh root@88.99.1.151                                   # host
ssh -i /root/.ssh/metin2_vm root@192.168.122.10        # VM, from the host
# Until first layout install, live tree may still be /usr/metin2/Source/Server on the VM.
cd /usr/metin2/apps/server && gmake -j4 all            # binaries -> /usr/home/share/bin/{db,game}
service metin2 start|stop|status
```

Server release (from Mac, committed tree): `platform/deploy/release_upload.sh` → on host `platform/deploy/server_release.sh stage|build|install`. Before first layout install on the VM: `platform/deploy/layout_cutover_backup.sh`.

Web client (in container `m2web-build` on the host; bash, not sh):

```sh
cd /work/kit && source /work/emsdk/emsdk_env.sh && python3.13 webclient.py build --only <step>
# steps: lzo cryptopp python stage eterbase eterpack engine unpack scripts rewrite uiscript corpus data link package
# log: /work/step_<step>.log; trees and gr2 steps are skipped (no SpeedTree/Granny DLLs)
python3 -I platform/web-kit/patchcheck.py <kit_dir> apps/client/source   # every stage patch must still hit
```

Run container scripts as files: write to `/home/m2web/x.sh`, then `ssh -o BatchMode=yes root@88.99.1.151 'docker exec m2web-build bash /work/x.sh'` (this form is allowlisted). Long jobs: `nohup` + `publish.sh`.

Publish: `webclient.py package` and `tools/bridge_config.py --site https://metin2.kaanakin.dev` in the container, then `/home/m2web/publish.sh` on the host (refuses to sync an incomplete package). It runs `publish_cdn.sh` first (wrangler in a `node:22-alpine` container, token in `/root/.cloudflare/metin2-cdn.env`; only changed chunks upload, the first full upload took ~10 min) and then syncs the site. `deploy.sh` recreates the site and bridge containers.

Portal (`apps/portal`, Node ≥ 22.18, no build step for `server.ts`):

```sh
npm install
npm run dev         # vite dev on :3000 with .env.development (Turnstile test keys); register/login also need DB_* vars
npm run build       # dist/client + dist/server
npm run typecheck
npm test            # node --test over test/**/*.test.ts (no DB needed); one file: node --test test/server.test.ts
npm run format      # Prettier + Tailwind class sorting; run after every change (format:check to verify)
npm start           # node server.ts; HOST/PORT plus every var in src/server/config.ts, read at runtime
```

All env vars, including `TURNSTILE_SITE_KEY`, are read at runtime by the server (the site key reaches the page through a route loader), so one build serves every environment.

ASan build: `build_asan.sh` / `publish_asan.sh` on the host, served under `/asan/`. Keep `MAXIMUM_MEMORY` at 2 GB and `malloc_context_size=0` (see notes).

## Rules and traps

- **Never disable a feature flag that changes network packets or game data** for the web build; client and server must agree. Only Windows/D3D-rendering flags may be turned off (list in `CALISMA_NOTLARI.md` §5). If something does not compile, patch the code.
- Prefer fixing in the source over adding stage patches. Real bugs go in unconditionally; web-only changes go in `#ifdef __EMSCRIPTEN__`. `stage_port.py` patterns must be ASCII.
- Client sources are **cp1254 with CRLF**. `grep` treats them as binary → `LC_ALL=C grep -a`. The Edit tool cannot write them; use `perl -i` and preserve CRLF. Python UI scripts mix cp1254 and CP949 line by line.
- After changing client source, sync the file to `/home/m2web/websrc` on the host (except `Locale_inc.h`, which holds the web-only flag changes).
- Unpack packs with `node build/port/obj/unpack_pack.js . <pack> client_files` (pack names are `d:/ymir work/...`).
- `.gitattributes` stores text as LF; the engine's text-format loaders must accept LF (this broke every property file once).
- Upstream commit `ced4250af` deleted ~3700 client data files still referenced by the XML indexes; missing models/props are usually restored from `ced4250af^`.
- The host SSH has fail2ban: keep polling loops sparse (≥2 min).
- zsh expands `$c:r` modifiers; use `${c}` or a bash script.
