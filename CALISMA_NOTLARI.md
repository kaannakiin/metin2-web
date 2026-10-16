# Anka2 – Sunucu + Web (WASM) Çalışma Notları

Son güncelleme: 2026-10-15. Hobi amaçlı, ~10 kişilik sunucu. **Ana hedef: oyunun tarayıcıda (WebAssembly) oynanması.**

Bu dosya, yapılanları ve kaldığımız yeri kaydeder. Şifreler burada YOK; nerede durdukları yazılı.

---

## 1. Mimari (hepsi tek makinede)

```
Oyuncu tarayıcısı
   │  https://metin2.kaanakin.dev            (TLS: Coolify/Traefik — HENÜZ KURULMADI)
   ▼
Host 88.99.1.151  (Hetzner dedicated, Ubuntu 24.04, Coolify + mailcow)
   ├─ Docker "m2web-build"  → web client derleme ortamı (/home/m2web ↔ /work)
   ├─ (yapılacak) web dosyaları + bridge (Node, WS→TCP)
   │        │ düz TCP, sadece makine içi ağ (virbr0 192.168.122.0/24)
   ▼        ▼
KVM VM "metin2"  192.168.122.10  — FreeBSD 14.5 i386
   ├─ MariaDB 10.11 (127.0.0.1)
   └─ db, auth, ch1 (3 core), ch99
```

Oyun portları internete açık DEĞİL; tarayıcı yalnızca bridge üzerinden ulaşacak.

---

## 2. Erişim

| Ne                     | Komut / yer                                                                         |
| ---------------------- | ----------------------------------------------------------------------------------- |
| Host                   | `ssh root@88.99.1.151`                                                              |
| VM                     | `ssh root@88.99.1.151` → `ssh -i /root/.ssh/metin2_vm root@192.168.122.10`          |
| VM ekranı (SSH yokken) | host'ta `virsh screenshot metin2 /home/vms/m2.ppm` (çıktı aslında PNG)              |
| VM'e klavyeden yazma   | host'ta `python3 /home/vms/vtype.py` (stdin satırlarını `virsh send-key` ile yazar) |
| Build container        | `ssh root@88.99.1.151 'docker exec m2web-build bash /work/<script>.sh'`             |

Şifreler (sohbete/repoya yazılmadı), VM içinde root-only:

- `/root/.metin2_db_pass` → MariaDB `metin2` kullanıcısı
- `/root/.metin2_admin_pass` → CONFIG'lerdeki `ADMINPAGE_PASSWORD`

GM hesabı: login `kaannakiin`, karakter `numan` (IMPLEMENTOR), silme kodu `1234567`. Şifre kullanıcıda; sohbette geçti → **canlıya açmadan önce değiştir**.

Arkadaşlar için 10 GM hesabı: `gm01`…`gm10`, yetki **GOD**. GM yetkisi hesap + karakter adına bağlı (`gm.cpp`), bu yüzden karakter tam olarak `GM01`…`GM10` adıyla açılmalı. Şifreler kullanıcıda (sohbette verildi). Silme kodu `1234567`.

---

## 3. Sunucu (VM) — ÇALIŞIYOR ✅

- FreeBSD 14.5 i386 (i386 → en fazla 4 GB RAM görür; VM'e 8 GB verildi, sorun değil).
- Disk: host'ta `/home/vms/metin2-fbsd.qcow2` (40 GB). Sabit IP: DHCP rezervasyonu, MAC `52:54:00:4d:32:01`. VM autostart açık.
- Paketler: mariadb1011-server/client, boost-libs, cryptopp, devil, lzo2, gmake, makedepend, libmng, png, tiff, jpeg-turbo, rsync.
- Kaynak: `/usr/metin2/Source/Server` → `cd /usr/metin2/Source/Server && gmake -j4 all`
- Binary'ler: `/usr/home/share/bin/{db,game}`. `/home` → `/usr/home`.
- Düzen: `/usr/home/main/{db,auth,channels/channel1/core1..3,channels/channel99}`; her dizinde `game`/`auth`/`game99` → `share/bin/game` symlink, ayrıca `locale` → `/usr/home/share/locale`, `data` → `/usr/home/share/data` symlink.
- Servis: `/usr/local/etc/rc.d/metin2` → `service metin2 start|stop|status`. `metin2` kullanıcısıyla çalışır, açılışta otomatik.
- Portlar: db 15000, auth 30001, ch99 30003, ch1 core1/2/3 = 30101/30103/30105 (+1 = P2P).
- Sadece channel1 + ch99 açılıyor (ch2-4 config'leri duruyor ama başlatılmıyor).

### Sunucuyu ayağa kaldırırken yapılan düzeltmeler (repoda, commit'lenmedi)

- `library/rapidjson/document.h`: const üyeye atama yapan `operator=` → `= delete` (clang 21).
- Makefile'lar (db, game, libgame, libsql, libpoly): `-D_LIBCPP_HARDENING_MODE=_LIBCPP_HARDENING_MODE_NONE` — FreeBSD 14 libc++ boş vector'de `&v[0]`'da `ud2` ile duruyordu.
- Eksik `return` (clang `ud2` tuzağı): `char_gem.cpp` (CheckSlotGemMarket), `char_item.cpp` (IsEmptyItemGrid), `sectree_manager.cpp` (GetSungmaValueAffectByRegion), `stone_event.cpp` (GetStoneEventPoint).
- `char_gem.cpp` LoadGemSystem: `fopen` NULL kontrolü.
- `home/main/db` + `home/share/conf`: `item_proto/mob_proto/*_names` → `Tools/dump_proto` sürümü (client ile birebir: 10874 item, 3295 mob; eski dosyada `HIT_RANGE` kolonu yoktu).
- Yeni: `home/share/locale/europe/attendance_reward.txt` (yoksa core kapanıyordu), `home/share/locale/europe/gem.txt` (Gaya market).
- Config'lerdeki public DB şifresi (`beststudio …`) VM'de yeni rastgele şifreyle değiştirildi (repodaki dosyalar hâlâ eski haliyle!).

---

## 4. Veritabanı — `sql/`

Orijinal dump yoktu; şema C++ sorgularından çıkarıldı. Hepsi `utf8mb4` (client çok dilli modda UTF-8 gönderiyor).

| Dosya                      | İçerik                                                                                               |
| -------------------------- | ---------------------------------------------------------------------------------------------------- |
| `account.sql`              | 1 tablo (`PASSWORD()` hash'i ile login)                                                              |
| `common.sql`               | locale (LOCALE=europe, skill gücü), gmlist (seed YOK, güvenlik), gmhost, spam_db                     |
| `player.sql`               | 53 tablo                                                                                             |
| `log.sql`                  | 22 tablo                                                                                             |
| `seed_item_attr.sql`       | 59 + 39 bonus (bazıları `-- approx`)                                                                 |
| `seed_skill_proto.sql`     | 97 skill (`setFlag` SET, `eSkillType` ENUM; çoğu formül client skilldesc'ten, bir kısmı `-- approx`) |
| `seed_shop_refine_pet.sql` | 407 refine, 10 shop/123 item, 252 pet skill                                                          |

VM'de hepsi yüklü. Coolify'daki test MariaDB'si kapatıldı (6671 kapalı).

---

## 5. Web client (WASM) — DERLENDİ ✅

Kullanılan kit: <https://github.com/nairoad/Metin2-WebClient> (GPL-2.0, TMP4 client için yazılmış). Kod tarandı: ağ erişimi yalnızca LZO + CPython indirmesi (SHA-256 sabit), şüpheli bir şey yok.

### Build container `m2web-build` (host'ta, `python:3.13-bookworm`)

| Yol (container içi)             | Ne                                                                                                                          |
| ------------------------------- | --------------------------------------------------------------------------------------------------------------------------- |
| `/work/emsdk`                   | Emscripten 6.0.8 (`source /work/emsdk/emsdk_env.sh`, **bash** ile)                                                          |
| `/work/kit`                     | kit, yerel `anka2` branch'i (değişiklikler aşağıda)                                                                         |
| `/work/anka2`                   | bu repo'nun GitHub'dan shallow clone'u                                                                                      |
| `/work/websrc`                  | `Source/Binary` kopyası, `Tools/web/kit/prep_websrc.sh` ile hazırlanır (aşağıdaki flag'ler kapalı + eksik boost başlıkları) |
| `/work/packs`                   | 26 EIX/EPK pack + `Index` (5.1 GB), `make_eterpacks.py` ile üretildi                                                        |
| `/work/tools/make_eterpacks.py` | pack üretici kopyası                                                                                                        |

Font: `/usr/share/wine/fonts/tahoma.ttf` (fonts-wine, LGPL). Python 2→3 için `/usr/bin/python3` (3.11, lib2to3).

### Web build'de kapatılan flag'ler

Kural: sunucuyla konuşulan paketleri ya da oyun verisini değiştiren flag **kapatılmaz** (client ile sunucu aynı paketleri beklemeli), derlenmiyorsa kod yamalanır. Sadece Windows/D3D çizim katmanını etkileyen flag kapatılır, çünkü kit o katmanı WebGL ile tamamen değiştiriyor.

| Flag                               | Ne yapıyordu                     | Web'de kayıp                                     |
| ---------------------------------- | -------------------------------- | ------------------------------------------------ |
| `ENABLE_FOXFS_ENCRYPT`             | pack şifreleme                   | yok, pack'leri kendimiz üretiyoruz               |
| `ENABLE_DIRECTX9_UPDATE`           | D3D9 renderer                    | yok, kit D3D8'i WebGL'e çeviriyor                |
| `ENABLE_LOAD_INDEX_BINARY`         | binary Index formatı             | yok                                              |
| `ENABLE_FIX_MOBS_LAG`              | D3D vertex buffer/yazı batching  | yok (GL katmanı kendi çiziyor)                   |
| `FPS_APPLICATON_DEVICE_LIMITATION` | ayrı `Process()` + busy-wait FPS | yok; açık kalırsa kitin tarayıcı döngüsü atlanır |

Kapatılmayıp yamalanan Windows'a özel kısımlar: görev çubuğu gruplama (kaldırıldı), ekrandan renk okuma `GetColorAtPosition` (hata döner), `ShellExecute` (http(s) linki yeni sekmede), rastgele Python modül isimleri (anti-cheat; web'de gerçek isimler `net`, `chr`…).

**Tuzak:** repodaki `.gitignore` `Debug/` kuralı macOS'ta büyük/küçük harf duyarsız eşleşip `extern/include/boost/preprocessor/debug/` klasörünü repodan düşürmüş. `prep_websrc.sh` bu 3 başlığı boost 1.67'den indiriyor.

### Kit üzerindeki değişikliklerimiz (kopyaları: `Tools/web/kit/`)

- `tools/stage_port.py`:
  - 76 TMP4 yamasından 72'si Anka2 koduna uyarlandı, 4'ü gereksiz (açıklamalı).
  - Ek yamalar: `<SSTREAM>`→`<sstream>`; `EterPackManager::isExist` FoxFS yokken de `_access` kullansın (yoksa corpus dosyaları "yok" görünür); `GrpImageTexture.h` çift `CreateDDSTexture` bildirimi kaldırıldı.
  - Linux için büyük/küçük harf: klasörleri case-insensitive kopyalama + `align_case()` alias symlink'leri (includer dizini önce).
  - Kontrol: `python3 -I Tools/web/kit/patchcheck.py <kit_dir> Source/Binary/source` → şu an `patches=75 hit=75`.
  - Fork eklemeleri için 20 yama daha (bozuk `#else`, D3D9'a özel kod, `std::string`→variadic, Python 3 frame erişimi, `size_t`/`long` genişlikleri, `minIni` yolu, `GetCodePage` adı).
- `compat/` (kopyaları `Tools/web/kit/compat/`): `d3dx8.h`'ye `D3DXMatrixTransformation`, `win32_compat.h`'ye `_countof`/`memcpy_s`, yeni `shellapi.h`.
- `tools/build_python.py`: `DISABLED_MODULES`'e `_lzma`, `_uuid`, `_ctypes` eklendi (Debian host kütüphaneleri wasm build'ini bozuyordu). CPython **python.org kaynağından** derlendi (hazır binary kullanılmadı).
- `webclient.toml`: kaynak/pack/font yolları, sunucu `192.168.122.10`, bridge hedefleri (30001/30003/30101/30103/30105).

### Python script adımları (fork uyarlamaları, `Tools/web/kit/tools/`)

- `unpack_packs.py`: `TO_UNPACK = ('root', 'locale')` (kit `locale_en`/`locale_pl` bekliyordu).
- `rewrite_scripts.py`:
  - **Kodlama satır satır seçiliyor.** Fork'ta Türkçe metinler cp1254, orijinal Korece yorumlar ve metinler CP949; bazı dosyalarda ikisi bir arada. Kitin "UTF-8 değilse CP949" kuralı Türkçeyi sessizce bozuyordu.
  - Fork bazı modülleri iki yazımla import ediyor (`interfaceModule`/`interfacemodule`…). En çok kullanılan yazım kanonik; diğerleri `import uiToolTip as uitooltip` biçimine çevriliyor, böylece modül tek kalıyor.
  - Dosyalar yeniden adlandırıldıktan sonra liste tazeleniyor.
- `script_patches.py`: 16 TMP4 yamasının 6'sı fork yazımına göre `FORK_ANCHORS` ile yeniden bağlandı. Dosya adları büyük/küçük harf duyarsız eşleşiyor.
- `uiscript_from_client.py`: aynı satır bazlı kodlama çözücüsünü kullanıyor.
- Dil: `?deflang=tr` → `locale.cfg` = `10002 1254 tr`. Fork'ta Türkçe dışındaki diller UTF-8; o dillerde karakter bozulması olabilir.

### Build adımları durumu

| Adım                                             | Durum                                                                                 |
| ------------------------------------------------ | ------------------------------------------------------------------------------------- |
| lzo, cryptopp, python, stage, eterbase, eterpack | ✅                                                                                    |
| engine, unpack, scripts, rewrite, uiscript       | ✅                                                                                    |
| corpus, data, link, package                      | ✅                                                                                    |
| trees, gr2                                       | atlanacak (SpeedTree/Granny DLL'leri yok — ağaç yok, modellerin ~%1'i eksik olabilir) |

Komutlar (container içinde): `cd /work/kit && source /work/emsdk/emsdk_env.sh && python3.13 webclient.py build --only <adım>` (`--only` tek adım alır). Log: `/work/step_<adım>.log`. Toplu script: `/work/build1.sh`.

### Engine'de beklenen sorunlar (fork'a özel Windows başlıkları)

`Shellapi.h`, `Shobjidl.h`, `wingdi.h`, `wrl/client.h`, `specstrings.h`, `strsafe.h`/`psapi.h` (Discord), `msctf.h`; kitin `compat/movie_web.cpp`'si `UserInterface/MovieMan.h` istiyor (bizde yok). DX9 kapatıldığı için eski D3D8 yollarında başka "bitrot" çıkabilir.

---

## 6. Yayın — CANLI ✅ <https://metin2.kaanakin.dev>

```
tarayıcı ─https─▶ Traefik (coolify-proxy, Let's Encrypt)
                   ├─ /        ─▶ m2web-site  (nginx:1.27-alpine, coolify ağı, dist/site salt okunur)
                   └─ /to/...  ─▶ m2web-bridge (node:20-alpine, --network host, 10.0.1.1:11496)
                                   └─ TCP ─▶ VM 192.168.122.10 (sadece 30001/30003/30101/30103/30105)
```

- `/` → `/client.html?deflang=tr` (Türkçe).
- Bridge sadece `https://metin2.kaanakin.dev` origin'ini kabul ediyor, izin listesi dışındaki adresleri TCP açmadan reddediyor (test edildi: `:22` → `unknown_target`, yabancı origin → 401).
- Bridge host ağında, çünkü coolify ağındaki container'lar libvirt VM'ine ulaşamıyor (test edildi).
- UFW: `10.0.1.6 → 10.0.1.1:11496` (sadece Traefik container'ı `coolify-proxy`; internetten ve coolify ağındaki diğer container'lardan kapalı).
- Traefik: `/data/coolify/proxy/dynamic/metin2.yaml` (yeni dosya, diğer servislere dokunulmadı).
- Sunucu adresi/portları client'a stage yamasıyla gömülü (`ENABLE_BINARY_SERVERINFO`): `webclient.toml` `[server] address/ch1_port/auth_port`.
- Kopyalar: `Tools/web/deploy/` (`deploy.sh`, `site-nginx.conf`, `metin2.yaml`). Yeniden yayın: container'da `webclient.py package` + `tools/bridge_config.py --site https://metin2.kaanakin.dev`, host'ta `deploy.sh`.
- Container'lar `--restart unless-stopped`; VM autostart açık → host yeniden başlarsa her şey kalkar.

### Cloudflare (2026-10-16) — proxy açık

Zone `kaanakin.dev`, **Free plan**; sadece ücretsiz özellikler (fatura riski yok). Zone'da tek kayıt var: `A metin2 → 88.99.1.151`, proxied.

- Cache Rules (`http_request_cache_settings`), ikisi birbirini dışlıyor:
  1. `/corpus/*.bin` (`manifest.bin` hariç) + `?v=` ile istenen `client.js/.wasm/.data` → cache, edge ve tarayıcı TTL'i origin'den (1 yıl).
  2. metin2 host'unda geri kalan her şey (html, `manifest.bin`, `order.txt`, `sw.js`, `preload.js`, `/to/` bridge, `/asan/`) → cache yok.
- Zone ayarları: SSL **Full (strict)** (origin'de Let's Encrypt), min TLS 1.2, Browser Cache TTL **0 = origin başlıklarına uy** (4 saat kalsaydı yeni `client.html` geç gelirdi), Smart Tiered Cache açık.
- **Always Use HTTPS kapalı kalmalı**: Traefik Let's Encrypt'i HTTP-01 ile (port 80) yeniliyor, yönlendirmeyi Traefik yapıyor.
- Doğrulandı: html/manifest/order/sw → `DYNAMIC`; wasm/data/chunk → `MISS` sonra `HIT`; WebSocket site origin'i `101`, yabancı origin `401`.
- Yayında purge gerekmez: değişen motor dosyaları yeni `?v=` alır, chunk adları içerik hash'i.

### Corpus Cloudflare Workers'ta (2026-10-16)

- `/corpus/*` → Worker `metin2-corpus` (sadece static assets, script yok). Ücretsiz ve sınırsız; ölçüldü: 150+ corpus isteğinde Worker invocation sayısı 0, yani günlük 100k limitine sayılmıyor. Kart yok → fatura mümkün değil.
- Neden R2 değil: kart istiyor ve harcama üst sınırı yok. Workers assets Free planda: sürüm başına 20.000 dosya, dosya başına 25 MiB (bizde 1371 dosya, en büyüğü 6.5 MB `manifest.bin`).
- İstemci değişmedi: aynı origin'in `corpus/` yolu. Rota silinirse istekler anında Hetzner'deki kopyaya döner.
- Dosyalar: repo `Tools/web/cdn/` (`wrangler.jsonc`, `_headers`), host `/home/m2web/cdn/`. Token: host `/root/.cloudflare/metin2-cdn.env` (Workers Scripts Edit, Workers Routes Edit, Zone Read; sadece kaanakin.dev).
- Yayın: `publish.sh` önce `publish_cdn.sh` (wrangler@4.146.0, `node:22-alpine`), sonra site rsync. Sadece güncel build yayında; eski sayfayla oyunda olan yenilemeli (2 kişiyiz, bilinçli tercih).
- Test (curl + Playwright): parçalar origin ile bayt bayt aynı (adlar `sha256[:32]`, md5 değil), parça `immutable`, `manifest.bin`/`order.txt` `no-cache`, olmayan parça 404, giriş ekranı açılıyor, konsolda hata yok, deploy sonrası origin'e corpus isteği düşmüyor. Cache'siz ilk indirme ~9 MB/s (20 parça, 80 MB).
- `?fetch=1` (tüm corpus'u arka planda indirme) kaldırıldı: `site/preload.js` artık sadece `order.txt` prefetch ilerlemesini gösteriyor. `compat/runtime.js` seçenek tablosundaki `nofetch` satırı sadece açıklama; bir sonraki motor derlemesinde silinecek.
- Risk: Cloudflare CDN şartları büyük non-HTML dosya sunumunu kısıtlayabiliyor; Workers assets Developer Platform ürünü olduğu için önerilen yol bu. Cloudflare yine de itiraz ederse çözüm: corpus'u gri bulutlu bir subdomain'den Hetzner'den sunmak (Cloudflare'in kendi önerisi).

### Portal ve otomatik giriş (2026-10-16)

- Portal: `web/portal` (TanStack Start + Tailwind + react-hook-form/zod), kayıt/giriş sunucu fonksiyonları `account` DB'sine doğrudan bağlanır. **CANLI ✅** `https://metin2.kaanakin.dev/`.
- Yayın düzeni: container `m2web-portal` (host ağı, `10.0.1.1:11497`, salt okunur, uid 1000), UFW `10.0.1.6 → 10.0.1.1:11497`. Traefik: `/` portal, `/client.*` `/preload.js` `/sw.js` `/asan/` nginx, `/to/` bridge; hepsinde Cloudflare IP allowlist (doğrudan origin → 403, test edildi). Cloudflare cache kuralına portalın `/assets/*` dosyaları eklendi (`MISS` → `HIT`).
- MariaDB artık `127.0.0.1,192.168.122.10` dinliyor (`zz-metin2.cnf`, yedek `zz-metin2.cnf.bak-portal`); `portal@192.168.122.1` sadece `account.account` SELECT/INSERT. Script: `Tools/web/deploy/vm_portal_db.sh` (oyunu durdurup MariaDB'yi yeniden başlatır).
- Gizli değerler sadece host'ta: `/root/.metin2/portal.env` + `portal-db.pw` (root, 600). Turnstile secret sohbete girmedi: host'ta üretilen RSA anahtarıyla şifrelenip orada çözüldü, anahtar silindi.
- Uçtan uca test (canlı, Playwright, `webtest02`, sonra silindi): gerçek Turnstile ile kayıt → yanlış şifre mesajı → doğru şifre → oyun giriş ekranını atlayıp krallık seçimine geçti.
- Otomatik giriş akışı: portal girişten sonra `sessionStorage["m2w.autologin"]` = `{login, password, expires: +60 s}` → `client.html` okur ve hemen siler, `Module.preRun`'da motorun bellek dosya sistemine `/m2w_autologin` (iki satır) yazar → `intrologin.py` `Open()` sonunda dosyayı okur ve siler, ilk `OnUpdate`'te alanları doldurup giriş butonunu çağırır (F1–F4 hızlı girişiyle aynı yol, hata pencereleri aynen çalışır). Windows'ta dosya hiç olmaz.
- Motor derlenmedi: sadece root pack + `scripts rewrite uiscript data link` + `package` (host `/home/m2web/autologin.sh`). `link` şart: yeni `?v=` ile tarayıcılar yeni `client.data`'yı alır.
- Şablon: `kit/site/client.html` (repo kopyası `Tools/web/kit/site/client.html`; `__BRIDGE__`/`__VERSION__` link adımında doluyor).
- Test (canlı, Playwright, geçici `webtest01` hesabı, sonra silindi): giriş ekranı atlandı, krallık seçimine geçti; `sessionStorage`, sayfa değişkeni ve `/m2w_autologin` boş kaldı; konsolda hata yok. Kayıt yokken normal giriş ekranı açılıyor; `client.data` ikinci açılışta cache'ten (transfer 0).

### Canlı testte bulunan ve düzeltilen sorunlar (tarayıcıda, sırayla)

1. `__builtin__` → `builtins` (fork aynı satırı `UserInterface.cpp`'de de kullanıyor).
2. Fork `OpenLogFile` stderr'i `./syserr/` klasörüne yönlendiriyordu → klasör yok, stderr kapanıyordu, hiçbir hata görünmüyordu. Web'de stderr = konsol.
3. `locale.cfg`: fork iki alan okuyor (`1254 tr`), kit üç alan yazıyordu → "cp10002" hatası (`compat/locale_web.cpp`).
4. `introLogin.py` Windows kayıt defteri (`winreg`) kullanıyor → yoksa "kayıtlı hesap yok" ("hesabı hatırla" web'de çalışmaz).
5. PNG desteği (fork arayüzü PNG; kit sadece TGA/BMP/JPEG/DDS) → `compat/d3d8_image.cpp` + `-sUSE_LIBPNG=1`. TGA/BMP/PNG'ye 8192 px boyut sınırı (güvenlik).
6. **Kod sayfası 1254 tablosu yoktu** → bütün Türkçe metinler boş çiziliyordu (`compat/codepages.cpp`, Python cp1254 codec'inden üretildi).
7. `serverInfo.py`: yazarın test sunucuları (192.168.1.156) çıkarıldı, tek kanal; `channel.inf` hatırlanan sunucu yoksa 1/1. Silme yamalarının "zaten var" sanılması hatası (`script_patches.apply_all`) düzeltildi.
8. Tam ekran: açılışta tarayıcı penceresi boyutu `metin2.cfg`'ye yazılıyor; 7 px başlık çubuğu kırpması kaldırıldı.
9. **Fontlar:** Windows GDI yerine FreeType mono+hinting ile `TMP4FNT1` bin'leri (`tools/bake_fonts_ft.py`, OS/2 win metrikleri, wine `tahoma.ttf`/`tahomabd.ttf`; container'a `freetype-py==2.5.1` kuruldu) → orijinal piksel font görünümü. Canvas yedeği için glif kapsamı = alfa.
10. Girişte `std::thread` çökmesi (`ENABLE_CLIENT_PERFORMANCE` ön yükleme) → ana döngüde senkron `Load()` (girişten sonra ~5000 dosya; bu sürede donma var).
11. **Granny `.gr2` sürüm 7 (Granny 2.11):** modellerin yarısı (8434/16347) reddediliyordu (karakter animasyonları, canavarlar, haritalar, kostümler).
    - Okuyucu v7 magic/sürümünü kabul ediyor (`compat/gr2_file.cpp`, `tools/gr2.py`); veri düzeni aynı.
    - BitKnit2 sıkıştırmalı 4032 dosya `Tools/web/kit/gr2_bitknit/gr2_unbitknit` ile sıkıştırmasız yazılıp `build/port/repaired_gr2/`'ye konuyor (corpus overlay). Çözücü libbg3/ooz (GPL-3.0, sadece build aracı).
    - Sonuç: reddedilen 422 → 22 (kalan 22 = kitin Oodle1 çözücüsünün açamadığı dosyalar: bazı emote'lar, `damage`, `skill_charge`, `jumagap`).
    - `gr2_file.cpp` relocation/kök pointer sınırları 64 bit kontrol (güvenlik).
12. `numan` yanlışlıkla `gm01` hesabında oluşmuştu → kullanıcı onayıyla `kaannakiin`'e taşındı (player.account_id=1, player_index id1 pid1=1 empire=3).
13. `uiresp.py` pickle'ı metin modunda açıyordu → arayüz yarım kalıyordu; `uiDungeonTrack`/`uiSwitchbot` pickle'ları sağlamlaştırıldı.
14. `best_system` pack'i (`System/Dungeon/script/tabledungeon.py`) script adımına eklendi (`TO_UNPACK`).
15. `CWindowManager::DestroyWindow` aynı karede iki kez çağrılırsa yok sayılıyor (tetiklendiği görülmedi; zararsız koruma).
16. `GetPixelColor` surface sızıntısı kapatıldı.

**Şu anki durum:** giriş ✅, karakter seçimi ✅ (numan modeli görünüyor), oyuna giriş ✅ (harita, karakter, arayüz, sohbet görüldü). **Ama birkaç saniye/dakika içinde çöküyor.**

### Bellek bozulması — ÇÖZÜLDÜ (2026-10-15/16)

ASan (`/asan/`, `build_asan.sh`, `publish_asan.sh`) ile bulunup düzeltilen hatalar:

- `TraceError`: 1 KB'tan uzun mesajlar `szBuf[len]` ile yığın tamponunun dışına yazıyordu (C99 `vsnprintf` tam uzunluk döndürür). Asıl rastgele bozulma buydu. compat'ta `_vsnprintf`/`_snprintf` artık MSVC gibi kesilince -1 döner.
- `CDXTCImage::Copy`: DDS'in bildirdiği `dwLinearSize` gerçek blok boyutundan büyükse doku tamponu taşıyordu.
- DDS başlığı 128 bayttan küçük dosyalarda tampon dışından okunuyordu (sihirli sayı kontrolü fork'ta yorumda).
- `ReservingMotionProcess`: `pop_front` sonrası silinmiş düğüm okunuyordu.
- `CAniImageBox`: ayarlar heap'teki `std::function` yerine düz değerler (oyun içi `~CAniImageBox` çökmesi).
- `DestroyWindow`: aynı karede ve sonraki karede ikinci silmeye karşı koruma (loga Python yığını basar).

ASan notları: seçenekler `compat/stubs.cpp` içinde `__asan_default_options` ile gömülü (sayfa `ENV`'i geç kalıyor). `malloc_context_size=0` olmadan açılış ~8 dk. `MAXIMUM_MEMORY` 2 GB olmalı: 2 GB üstü adresleri JS köprüsü bozuyor (dosyalar gölge bellek baytlarıyla geliyordu).

### Yamaların kaynağa taşınması

- `stage_port.py` 129 → 77 yama. 26 gerçek hata koşulsuz, 26 web uyarlaması `#ifdef __EMSCRIPTEN__` ile kaynakta. Kalanlar: kitin TMP4 temel yamaları, sunucu adresi/portları (derleme anında `webclient.toml`'dan), kitin sabit listesindeki `Stl.h` ve bir kit yamasına bağlı `PythonPackModule`.
- Taşıma betiği: scratchpad `migrate_patches.py` (yama metni + açıklama ile eşleşir, `--ifdef`, önce kontrol modu). Önişlemci satırı içeren desenlerde elle kontrol gerek (`minIni.c`, `EterPackManager::isExist` bozulmuştu, düzeltildi).
- Stage artık yamalı dosyaları `latin-1` okuyup yazıyor; önceden `utf-8 errors=ignore` cp1254 Türkçe karakterleri siliyordu.
- Sunucudaki derleme kaynağı `/home/m2web/websrc` (public klondan bir kez kopyalandı). Kaynakta değişen dosyalar oraya `scp` ile eşitlenmeli (`Locale_inc.h` hariç: web'de kapatılan flag'ler orada).
- `script_patches.py` 29 → 24: kalanlar Python 3'e özel (Windows istemcisi Python 2.7). `serverInfo`, `introLogin` kanal yedeği, `localeInfo` kaçış hatası Python 2 kaynağına (`Tools/binary_unpack/root`) taşındı.
- `pyflakes` taramasıyla bulunan script hataları kaynakta düzeltildi: `FASLE`, `apply`, `dstSlotPos`, `tchat`, `RACE_FLAG_DICT`, eksik `import shop/item/chat/skill`. Ölü kod (`guildbank`, `uiPickETC`, `uiEvent.DeleteButton`) bırakıldı.

### Haritada binalar yoktu — düzeltildi

`property_create.xml` eskiydi: `property/` klasöründeki 10081 dosyanın 5713'ü pakete girmiyordu (binalar `property/b`, `property/c`). Henüz hiçbir dosyanın sağlamadığı CRC'leri getiren 2007 dosya XML'e eklendi (mevcut 88 CRC çakışması değişmesin diye). Dizin 4366 → 6374 kayıt; haritanın istediği eksik 127 binanın hepsi geldi. Yeniden üretim: `make_eterpacks.py --only property`, ardından property paketini `client_files`'a açma (`/home/m2web/props2.py`), sonra `corpus` ve `data` adımları.

Bu yetmedi: binaların **modelleri** de yoktu. Upstream'in `ced4250af` ("Full client update") commit'i `binary_unpack`'ten 3691 dosya silmiş (`zone/b` 754, `zone/n` 668, `property/n` 774…), XML'ler ise hâlâ bunları listeliyordu. Pyungmoo'daki 601 binanın 546'sının `.gr2`'si eksikti; bütün haritalarda 33427 binanın 16470'i.

- `ced4250af^`'ten geri getirildi: `zone/b/obj` (758), eksik CRC'leri karşılayan 221 property dosyası (`property/n/obj`, `property/ghost/obj`, `shadow_devil_tower`) ve kullandıkları modeller (838). Property dosyaları XML'e eklendi (213).
- Paketlerden açarken **`node build/port/obj/unpack_pack.js . <pack> client_files`** kullan: pack içindeki adlar `d:/ymir work/...`, kendi açıcım (`props2.py`) bunları `client_files/d:/` altına yazıyordu.
- Geri gelen modellerin 635'i BitKnit2 → `gr2_unbitknit client_files repaired_gr2` (4032 → 4667), sonra `corpus` + `package`.
- Sonuç: Pyungmoo 601/601 binanın modeli var; tüm haritalarda modelsiz bina 16470 → 141, CRC'si bulunamayan nesne 4972 → 391 (kalan 74 CRC ve 27 model eski commit'te de yok). Kontrol betiği: `/home/m2web/propcheck.py [harita]`.

**Asıl kök neden (binalar ve ağaçlar):** `CProperty::ReadFromMemory` `YPRT`'den sonra `\r\n` şart koşuyordu. Repo `.gitattributes` `* text=auto` ile metni LF saklıyor, paketler Linux'ta üretildiği için bütün `.prb`/`.prt` dosyaları `YPRT\n` ile başlıyor → hepsi "File format error after FourCC" ile reddediliyordu (oyunda 871 `CArea::LoadObject Property(N) Load ERROR`). `GameLib/Property.cpp` artık LF ve CRLF'i kabul ediyor.

### Dururken karakterin bozulması — düzeltildi

Granny 2.11 (sürüm 7) dosyaları animasyon eğrilerini sıkıştırılmış `curve2` biçimlerinde tutuyor; kit yalnızca eski `Degree/Knots/Controls` biçimini okuyordu. Okunamayan eğri dinlenme pozuna düşüyordu (savaşçı `general/wait.gr2` sürüm 7, `run.gr2` sürüm 6). `compat/gr2_to_granny.cpp` `DecodeCurve2`: DaIdentity, sabitler, DaK32fC32f, DaKeyframes32f, DaK16u/8u, D3K16u/8u, D3I1K*, D9I1/I3K*, D4nK16uC15u/D4nK8uC7u (quaternion açma LSLib ile aynı). Keyframe eğrilerinin zaman birimi (`TimeStep` varsayıldı) oyunda doğrulanmadı.

### Diğer açık işler (yayına etkisi küçük)

- Yüklemede fare donuyor → donanım imlecine geç (`metin2.cfg` `SOFTWARE_CURSOR 0` ya da `?cursor=hardware`).
- "İstemci yükleniyor"/"bağlanıyorsun" kutusundaki **kara bant**: 4'ün katı olmayan DXT texture'ı WebGL reddediyor (`glCompressedTexImage2D ... not multiples of 4`) → compat'ta bu boyutlarda CPU'da açıp RGBA yükle (`compat/dxt.cpp` var).
- Ana döngü yükleme sırasında bloklanınca auth WebSocket'i zaman aşımına düşebiliyor ("Sunucuya bağlanıyorsun" takılması) → tekrar deneyince geçiyor.
- Ağaçlar: SpeedTree `.spt` (Windows'a özel SpeedTreeRT) → Windows'ta kitin `trees` adımı ya da açık kaynak okuyucu. `property/shyeonline/trees/*.prt` "File format error" bununla ilgili.
- Harita adı Almanca görünüyor ("Gebiet Pyungmoo") → harita adları locale dosyası (de/tr) kontrol edilmeli.
- Kalan 22 Oodle1 `.gr2` (kitin çözücüsü açamıyor).
- Python: `OnRecvEventInformation` arayüzden önce gelirse `wndEvent` yok hatası (zararsız).
- Sunucu: `INSERT DELAYED` MariaDB'de desteklenmiyor (log/loginlog tabloları yazılmıyor) → `DELAYED` kaldırılmalı.

## 7. Sıradaki adımlar

1. ASan ile heap taşmasını bul ve düzelt (yukarıdaki "AÇIK SORUN").
2. Normal kütüphaneleri yeniden derle + yayınla; `kaannakiin`/`numan` ile oyuna girip birkaç dakika stabil kaldığını doğrula.
3. Fare/kara bant/DXT, ağaçlar, harita adı dili.
4. GM şifresini değiştir (sohbette geçti).
5. Oyun içi özellikleri adım adım test et (switchbot, wiki, pet, gaya, aura, kuşak…).

### Bilinen eksikler (sonra)

- `zone` pack'inde hâlâ eksik dosyalar var (ör. `plechi_env`); bir kısmı `ced4250af`'te silinmiş, haritaların kullandıkları geri getirildi.
- ~90 üst seviye refine seti yok (Zodyak, Kyanite, pendant vb.).
- Pet auto skill'leri: sunucu/client enum sırası ile kitap ID'leri uyuşmuyor.
- Sunucu: `roulette_items.txt` yok, `blend.txt`'te `ATTACK_SPEED` → `ATT_SPEED` olmalı, koleksiyon tabloları boş.
- `skill_proto` / `item_attr` değerlerinin bir kısmı yaklaşık.
- Repodaki CONFIG'lerde ve `Bilgi.txt`'te hâlâ public şifreler var (VM'dekiler değiştirildi).

---

## 8. Dikkat / tuzaklar

- Kaynaklar **cp1254**: `grep` binary sanıp atlar → `LC_ALL=C grep -a`. Edit aracı bu dosyalara yazamaz; `perl -i` ile satır ekle (CRLF'i koru).
- Host SSH ara ara zaman aşımına düşüyor (fail2ban aktif). Bekleme döngüleri seyrek olsun (≥2 dk).
- `docker exec` heredoc için `-i` gerekir; izin kuralı `docker exec m2web-build` ile başlayan komutları kapsıyor → script'i önce `/home/m2web/` altına yaz, sonra `docker exec m2web-build bash /work/x.sh`.
- `~/.claude/settings.json`'a eklenen izin kuralı: `Bash(ssh -o BatchMode=yes root@88.99.1.151 'docker exec m2web-build:*)`.
- Host'ta canlı servisler var (mailcow, Coolify, foodhunch tunnel'ları) — onlara dokunma.
- Build scriptleri (host `/home/m2web/`, container'da `/work/`): `build9.sh` (adım listesi `for s in ...` satırında, `sed` ile değiştiriliyor), `build_asan.sh`, `publish.sh` (canlı), `publish_asan.sh`. Uzun işler: `(nohup bash -c 'docker exec m2web-build bash /work/X.sh && /home/m2web/publish.sh ...' &)`.
- Kit değişikliklerinin repo kopyaları `Tools/web/kit/{stage_port.py,compat/,tools/,site/,gr2_bitknit/}`; sunucudaki kit `/home/m2web/kit` (= container `/work/kit`). Değişikliği hem scratchpad/repo'ya hem `scp` ile sunucuya koy.
- Tarayıcı testi (1920×899 pencere): kullanıcı adı alanı (958,395), şifre (958,465), giriş butonu (960,523), karakter seçiminde başlat (1020,788). Tıklamalar `mouse.down`/`up` arasında ~100 ms beklemeyle; hızlı tıklama algılanmıyor. Ekran görüntüsü aracı bazen eski kareyi döndürüyor → tekrar al.
- zsh'de `$c:refs` gibi ifadeler `:r` değiştiricisi olarak yorumlanıyor → `${c}` yaz ya da bash script kullan.
- Kaynak dosyalar stage'de UTF-8 okunuyor (`errors='ignore'`) → yama desenleri ASCII olmalı.

### UFW: portal ve bridge sadece Traefik'e açık (2026-10-16)

- Güvenlik incelemesi: `10.0.1.0/24` kuralı coolify ağındaki ~30 başka container'ın portala Traefik'i atlayıp doğrudan ulaşmasına ve sahte `CF-Connecting-IP` ile IP başına sınırı aşmasına izin veriyordu (bridge'de de aynısı).
- Kurallar `10.0.1.6` (`coolify-proxy`'nin coolify ağındaki IP'si) ile değiştirildi, `/24` kuralları silindi.
- Doğrulandı: Cloudflare üzerinden portal 200, oyun 200, bridge 426 (WebSocket bekliyor); doğrudan origin 403; Traefik container'ından portal 200 / bridge 426; `m2web-site` container'ından portal zaman aşımı; diğer Coolify siteleri yanıt veriyor (502/504 yok), Traefik logunda hata yok.
- Risk: Coolify proxy'yi yeniden oluşturursa IP değişebilir ve site kapanır. `deploy_portal.sh` her deploy'da bunu kontrol edip uyarıyor; o durumda iki UFW kuralını yeni IP'ye taşı.

### Akıcı yükleme: gruplu corpus, harita ön-yüklemesi, dil paketleri (2026-10-16)

Ölçülen sorun: girişte ~360 MB iniyordu. Fork'un `ENABLE_CLIENT_PERFORMANCE` ön-yüklemesi (`net.LoadResourcesInCache`) 8 ırkın bütün hareketlerini girişte zorla yüklüyor. Corpus alfabetik olduğu için 500 baytlık `.msa` dosyaları megabaytlık zırh `.dds`'leriyle aynı 4 MB parçalarda duruyordu. Kayıtlı 90 parçanın ~55'i `pc`/`pc2` klasörlerindendi. Karakter seçince harita, `MAIN_CHARACTER` paketi işlenirken senkron yükleniyor ve ekran donuyordu.

- **Corpus düzeni** (`tools/build_corpus.py`, `tools/corpus_groups.py`):
  - Her biri kendi parçalarında olmak üzere `meta` (küçük tanım dosyaları, 66.6 MB / 17 parça), `motion` (bütün ırkların hareket `.gr2`'leri, 73 MB / 19 parça) ve `boot` (`tools/data/boot_files.txt`, kayıtlı ilk oturum; henüz boş).
  - Sonra her haritanın dosyaları bir arada (önce köyler), en sonda kalanlar alfabetik.
  - `corpus/groups.txt` (`order.txt`'nin yerine, `no-cache`) her grubun ve her `map:<klasör>`'ün parçalarını listeliyor.
  - Harita grubu statik çıkarılıyor: klasör, textureset, ortam ve alanlardaki nesneler (CRC → property → model → `gr2.py` ile doku).
  - Simülasyonda köylerin parça ihtiyacı alfabetik düzene göre 88/124/88 MB'tan 36/76/48 MB'a indi. Gerçek build'de: a1 48 MB, b1 96 MB, c1 72 MB.
- **Ön-yükleme** (`compat/runtime.js` `m2w.prefetchStart`):
  - `meta`/`motion`/`boot` sayfa açılınca arka planda iner.
  - Seçim ekranında hesabın karakterlerinin bulunduğu haritalar sıraya girer (`PythonNetworkStreamPhaseSelect.cpp`, x/y → `AtlasInfo`).
  - Yüklemede girilen harita öne alınır. `MAIN_CHARACTER` paketi, harita bellekte olana kadar ya da en fazla 1 dk bekletilir (`__WebMapPrefetched`, `m2w.mapReady`). Ekran donmaz, köşede "Harita indiriliyor" çubuğu görünür.
  - Bellek bütçesi 512 MB (8 GB+ cihazda 768).
  - Cache Storage'daki eski build parçaları siliniyor.
- **Girişteki zorla yükleme** (sadece web): hareketler kaydediliyor ama yüklenmiyor. `CPythonPlayerSettingsModule::ProcessDeferredCache` her karede 4 ms, parçası bellekte olanları önbelleğe alıyor (5 s bekleyen dosya yine yüklenir).
- **Dil paketleri:** `locale/<dil>/` artık `client.data`'da değil (133 MB → 59 MB). Her dil `client.locale_<dil>.data/.js` (tr 17.6 MB, diğerleri ~5.6 MB). `client.html` dili seçer (`?lang` → localStorage → `?deflang` → tarayıcı → en), sadece o paketi yükler ve motora `m2w.config.lang` ile iletir.
- **Font:** Wine Tahoma'nın `İ`'si 1 px'lik çıplak bir çizgi ama `I` kadar yer kaplıyordu ("İ stemci"). `bake_fonts_ft.py` `İ`'yi `I` + kendi noktasından oluşturuyor.
- Kaydedilecek: `boot_files.txt` (Playwright ile ilk oturum: `m2w.corpus.files`), ardından corpus yeniden kurulup yayınlanacak.
- Açık: in-game dil bayrakları Windows'taki gibi `locale.cfg` yazıp `app.Exit()` yapıyor; web'de sayfanın `?lang=` ile yenilenmesi gerek.
- `boot` kaydedildi (`tools/data/boot_files.txt`, ilk oturumdan 7386 dosya; meta/motion/harita dosyaları çıkınca 1516 dosya, 99.8 MB / 25 parça, 40 MB'ı girişte önbelleğe alınan `effect/sword`). Sıra: boot → meta → motion.
- Ölçüm (Playwright, önbellek temiz, `webtest03`):
  - Seçim ekranına kadar 150 MB (önce ~360) ve 30 senkron indirme (önce 112).
  - Oyuna giriş ~4 s, senkron indirme 0. Önce ~50 s sürüyordu, iki uzun donmayla.
  - İkinci ziyarette ağdan 6 MB.
  - Kalan: açılışta motor başlangıcı + giriş tanımları ~14 s donma.
- Dil paketleri Cloudflare cache kuralına ve nginx'in 1 yıllık `Cache-Control`'una eklendi (`/client.locale_*`).
- `?return=` artık sadece aynı origin'e yönlendiriyor (açık yönlendirme bulgusu); başka site için `m2w.config.returnUrl`.
- Türkçe yazma: gerçek `keydown` olaylarıyla sohbet doğru (`hadı şşş ççç ğüö İı ŞĞÜÖÇ`). Playwright'ın `keyboard.type`'ı ABD klavyesinde olmayan harflere `keydown` göndermediği için yanıltıcı.
- Sunucuda UTF-8 Türkçe metinler (`SnakeLair.cpp`, `soulroulette.cpp`, `WhiteDragon.cpp`, `item_attribute.cpp`) cp1254'e çevrildi: istemci cp1254 çiziyor, bu mesajlar `Ä±`/`ÅŸ` görünüyordu. Sunucu derlemesi gerekiyor.
- Açık: `[WİKİ] mesaj gönderdi` hâlâ `WÄ°KÄ°` görünüyor (Python tarafında metin doğru, kaynak bulunamadı); `/b` duyurusundaki bozulma GM olmadan yeniden üretilemedi.

### Güvenlik ve kararlılık düzeltmeleri (2026-10-16)

- Plan ve durum tablosu (fazlar F0–F4, açık ayrıntılar orada, repoda değil): <https://claude.ai/code/artifact/d1cd7bf2-4024-462d-8172-403fad8de3e5>
- F0 (client) yerelde hazır, henüz yayında değil: `LOCALE_CHAT`/`LOCALE_WHISPER`/`WHISPER` dinamik paket olarak kayıtlı (metin keserken `memory access out of bounds` çökmesinin muhtemel kök nedeni), `recv` -1'de okuma pozisyonu geri sarılmıyor, bozuk akışta client çökmek yerine giriş ekranına dönüyor, FPS sayacında sıfıra bölme düzeltildi.
- Server + bridge yayını tek adımda (bridge PROXY satırı yazıyor, server onu bekliyor; biri yalnız giderse herkes düşer): Mac'te `Tools/web/deploy/release_upload.sh` (commit'lenmiş hali host'ta `/root/metin2-release`'e), host'ta `server_release.sh stage` → `build` → bakım penceresinde `install` (geri alma: `rollback`). Makefile'lar binary'yi her zaman `/usr/home/share/bin`'e taşıyor; `build` bu yüzden `GAMEDIR`/`DBDIR`'i `/usr/metin2-next/out`'a yönlendiriyor. VM CONFIG'lerine dosya kopyalanmaz (DB şifreleri farklı), sadece `TRUSTED_PROXY_IP` satırı eklenir.
