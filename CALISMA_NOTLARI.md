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
- UFW: `10.0.1.0/24 → 10.0.1.1:11496` (sadece Traefik'in ağı; internetten kapalı).
- Traefik: `/data/coolify/proxy/dynamic/metin2.yaml` (yeni dosya, diğer servislere dokunulmadı).
- Sunucu adresi/portları client'a stage yamasıyla gömülü (`ENABLE_BINARY_SERVERINFO`): `webclient.toml` `[server] address/ch1_port/auth_port`.
- Kopyalar: `Tools/web/deploy/` (`deploy.sh`, `site-nginx.conf`, `metin2.yaml`). Yeniden yayın: container'da `webclient.py package` + `tools/bridge_config.py --site https://metin2.kaanakin.dev`, host'ta `deploy.sh`.
- Container'lar `--restart unless-stopped`; VM autostart açık → host yeniden başlarsa her şey kalkar.

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

### AÇIK SORUN: bellek bozulması (heap corruption)

- Belirtiler değişken: `free()` içinde abort (texture bırakılırken), Python GC'de `memory access out of bounds` (`deduce_unreachable`, `dict_dealloc`), `~CAniImageBox`, `malloc` içinde OOB.
- `/dbg/client.html` (canlı client + `PYTHONMALLOC=debug`, `PYTHONTRACEMALLOC=8`; `www/dbg/` sembolik bağlantılar, `publish.sh` siler) ile: çökme **oyuna girmeden, girişten sonraki ön yükleme sırasında `malloc` içinde** → dlmalloc kayıtları eziliyor = **C/C++ heap taşması**, Python refcount hatası değil.
- Elenen şüpheliler: Oodle1 çözücü (yazmalar sınırlı), baked font yapıştırma (sınırlı), `SaveColorMap`, `UnloadGif`, `CreateFromTexturePointer`, `pSrcInfo`.
- **Sıradaki adım:** ASan sürümü güncel kodla derlendi ve `/asan/client.html?deflang=tr` adresinde (EMCC_CFLAGS=`-fsanitize=address -sMAXIMUM_MEMORY=4294967296`, `/home/m2web/build_asan.sh`, `publish_asan.sh`). Açılışı ~10 dk. Giriş yapıp ön yüklemeyi bekle; konsolda `AddressSanitizer: heap-buffer-overflow` satırı ve yığın izi taşan yeri gösterecek.
- **DİKKAT:** ASan derlemesi `libeterbase.a`, `libeterpack.a` ve `obj/gamelib`'i ASan'lı bıraktı. Normal yayından önce `eterbase eterpack engine link` normal (EMCC_CFLAGS'siz) yeniden derlenmeli (`/home/m2web/build9.sh` adımlarına ekle).

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

- `zone` pack'inde 1888 dosya `binary_unpack`'te yok (ör. `plechi_env`); LFS'teki orijinal pack'lerde olabilir.
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
