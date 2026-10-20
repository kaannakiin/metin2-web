# Metin2 web client: hızlı geliştirme

Komutları Mac'te repository kökünde çalıştır. Mevcut `m2web-build`
container'ını kullanır; test çıktısı `/home/m2web/dev/site/current` altında.
Canlı yayın komutları bu akışta çalışmaz.

## Günlük kullanım

Bir terminalde `python3 platform/deploy/dev_client.py tunnel` çalıştır ve açık tut.
Tarayıcıda <http://127.0.0.1:18731/client.html?lang=tr> aç.

Başka terminalde değişikliğine uygun komutu çalıştır, bitince sayfayı yenile:

| Komut | Ne zaman? | Çalışan işler |
|---|---|---|
| `python3 platform/deploy/dev_client.py cpp` | Client C++ kaynak/header değişti | Kaynak eşitleme, patchcheck, artımlı engine, eterbase/eterpack, data, tek link, önizleme |
| `python3 platform/deploy/dev_client.py ui` | `content/client/packs/root` veya `locale` değişti | Açılmış scriptleri eşitleme, Python dönüşümü, uiscript, data, tek link; engine derlenmez |
| `python3 platform/deploy/dev_client.py link` | Build girdileri zaten hostta hazır | Data, tek link, önizleme |
| `python3 platform/deploy/dev_client.py serve` | Hazır önizlemeyi tekrar aç | Özel HTTP/bridge süreçlerini başlat |
| `python3 platform/deploy/dev_client.py clean` | Engine cache'ini kullanmadan yeniden derle | `cpp` ile aynı; tüm engine object'leri yeniden derlenir |
| `python3 platform/deploy/dev_client.py stop` | Önizlemeyi kapat | Yalnız geliştirme HTTP/bridge süreçlerini durdur |

İlk `cpp`, bağımlılık kayıtlarını oluşturmak için tam engine derlemesi yapar.
Sonraki derlemeler değişmeyen `.o` dosyalarını kullanır. `OBJECT CACHE` satırı
derlenen/kullanılan/hatalı/temizlenen dosya sayılarını verir. Eterbase/eterpack
arşivleri de kendi `-MD` header/kaynak bağımlılıkları değişmedikçe kullanılır;
`ARCHIVE CACHE` satırı arşivin yeniden yapılıp yapılmadığını gösterir.

## Neler hızlandı?

- Engine başlangıçta object klasörünü silmez. Derleyicinin `-MD` bağımlılık
  listesiyle kaynak ve header içerikleri takip edilir. Stage dosyaları aynı
  içerikle yeniden oluşturduğunda cache bozulmaz.
- Derleyici, seçenekler, ilgili ortam değişkenleri veya include dizinindeki
  dosya listesi değişince ilgili object yeniden derlenir. Silinen/derleme dışına
  alınan dosyaların eski object'leri link ve sembol sayımından önce temizlenir.
- Başarısız derleme eski object'i kullanamaz. Paralel engine çalıştırmaları
  ortak stage ağacını bozmasın diye engine kilidi vardır.
- `package.py` çağrılmaz: onun iki ek data/link geçişi ve corpus paketlemesi yok.
  Başlangıç verileri bir kez, özel autologin dosyaları olmadan hazırlanır ve tek
  link yapılır. Python değişikliğinde link hâlâ gereklidir; data loader mevcut
  kitte engine JS ile birlikte üretilir.
- Önizleme engine/data dosyalarını ayrı bir snapshot'a kopyalar; corpus'a
  yerel symlink verir. Cloudflare/CDN upload yok. HTML ve manifest `no-store`;
  engine/data/dil paketleri içerik hash'iyle sürümlenir ve değişmedikçe tarayıcı
  cache'inden gelir. Eski bir sayfanın güncel olmayan asset isteği `409` döner;
  sayfayı yenilemek gerekir. Corpus chunk'ları da hash'leriyle cache'lenir.
  Geliştirme service worker'ı kendini kaldırır. Engine/data/dil paketleri SSH
  üzerinden daha hızlı yüklenmesi için gzip olarak da hazırlanır.

## Bağlantı ve kapsam

Host HTTP: `127.0.0.1:18731`; ayrı geliştirme bridge'i:
`127.0.0.1:18732`, container adı `m2web-dev-bridge`. İki port tek SSH
tünelinden açılır. Origin allowlist yalnız localhost önizleme adresleridir.
Üretim bridge'inin ayarları ve origin listesi değiştirilmez. PROXY protocol
ve oyun hedefleri mevcut kit ayarlarından alınır. SSH tüneli oyuncu adresini
localhost'a çevirdiğinden, geliştirme bridge'i PROXY kaynak IP'si olarak build'i
başlatan SSH bağlantısının gerçek genel IPv4 adresini kullanır. `src/dev.js`
yalnız loopback dinleme ve localhost origin'leriyle çalışır; tarayıcıdan gelen
IP başlıklarını kullanmaz. IPv6-only bağlantı bu geliştirme yolunda desteklenmez.

**Bu bir client önizlemesidir; mevcut oyun sunucusuna ve onun veritabanına
bağlanır.** Oyun içindeki testler normal hesap verisini etkiler. Server
packet/proto değişiklikleri hâlâ uyumlu bir server build'i gerektirir.
Bu araç VM servislerini veya oyun verisini değiştirmez.

Mevcut İngilizce locale'de `TOOLTIP_MALL_EXPBONUS_P_STATIC` anahtarı
eksik olduğu için İngilizce başlangıcı kapanıyor; bu geliştirme altyapısı
değişikliğinin kapsamında çeviri verileri tamamlanmadı. Bu yüzden kullanım
bağlantısı açıkça `?lang=tr` içerir.

### Çalışan sunucunun protokolü

2026-10-19 hesap testi eski server binary'sinin hâlâ Yohara açık derlendiğini
gösterdi. Binary DWARF kaydı: `SSimplePlayer=105`, `packet_login_success=619`.
Güncel kaynak/PvP build'i: `100` ve `594` bayt. İstemci 25 bayt erken bitirip
sonraki paketi yanlış okuduğu için “Giriş işlemi yapılıyor” ekranında kalıyordu.
VM'deki kaynak dosyalara bakmak yeterli değil; çalışan binary kontrol edilmeli.

Eski canlı sunucuyla özel önizleme için:

```sh
python3 platform/deploy/dev_client.py cpp --protocol live-yohara
```

Bu açık seçim yalnız oluşturulan **stage** header'ına Yohara define'ı ekler.
Repo ve websrc header'larını değiştirmez. Paket boyutu 619 değilse build durur.
Seçim başarılı build'den sonra hostta `dev/protocol` içinde tutulur; günlük
`cpp`, `ui`, `link` komutları aynı profille devam eder. İlk profil değişimi
header'lara bağlı object'leri yeniden derler; sonraki işler cache kullanır.

Game ve db güncel PvP kaynaklarıyla birlikte kurulduktan sonra:

```sh
python3 platform/deploy/dev_client.py cpp --protocol source
```

Bu, kaynak flag'lerini aynen kullanır (mevcut login paketi 594 bayt).
`tools/login_packet_layout.py` her dev build'de gerçek staged header'ları
Emscripten ile ölçer. Yeni packet düzeni geliştirirken bu doğrulamayı ve server
profilini birlikte güncelle. `live-yohara` bir oyun tasarımı değişikliği değildir;
eski çalışan server'a uyumluluk seçimidir. Production release'de de çalışan
server'ın protokolüne uyan engine gerekir. Kaynak profiline dönüşü game/db
kurulumuyla koordine et; eski server çalışırken 594 baytlık engine yayınlama.

`live-yohara`, eski canlı sunucuda normal dedektör hâlâ altı kullanımlık olduğu
için UI rewrite'a `M2W_LEGACY_DETECTOR=1` de verir. `source` adayda sınırsız
dedektör metni açılır. Bu geçici uyumluluk seçimi mevcut sunucu davranışını
arayüzde doğru göstermek içindir; kaynak oyun tasarımı sınırsız dedektördür.

2026-10-19'da 619 baytlık uyumlu engine normal `webclient.py package` ile
özel dosyasız public pakete alındı ve canlıya yayınlandı. Preview klasörü
kopyalanmadı. Hem localhost hem `https://metin2.kaanakin.dev/client.html?lang=tr`
üzerinde gerçek hesapla `numan`/`deneme` karakter seçimi doğrulandı; test
oturumları kapatıldı. Dünya/oyun içi stabilite bu giriş testinin kapsamı değildi.

`cpp`, `apps/client/source` ağacını web build kaynağına eşitler;
`UserInterface/Locale_inc.h` mevcut web flag uyarlamalarını korumak için
hariçtir. Yeni feature flag/extern/toolchain değişikliklerinde mevcut manuel
eşitleme ve uyumluluk kontrolleri gerekir. Kaynaklar byte olarak aktarılır;
cp1254/CRLF dönüştürülmez.

`ui`, root ve locale kaynaklarını mevcut unpack sonucunun üzerine koyar;
Python 2→3 ve web semantic patch'leri normal kit araçları uygular. İlk kullanımda
kitin `scripts`/unpack çıktısı bulunmalıdır. Önceki `ui` çalışmasında yönetilen
bir dosya kaynakta silinirse overlay'den de kaldırılır. Model/texture/harita veya
runtime `uiscript` değişiklikleri bu komutun kapsamında değildir; ilgili corpus
veya runtime veri adımları ayrıca çalıştırılmalıdır.

Build ara çıktıları halen ortak kit ağacındadır. Geliştirme ve release build'ini
aynı anda çalıştırma. Önizleme snapshot'ı ancak tüm build adımları başarılı
olduğunda değiştirilir; başarısız build önceki önizlemeyi korur.

## Log ve doğrulama

Protokol ve oyun kabul kapıları: [GAMEPLAY_RELEASE.md](GAMEPLAY_RELEASE.md).
`resp_packet_layout.py` her build'de gerçek WASM fixture çalıştırır; genel
ABI denetimi `python3 platform/deploy/packet_audit.py --strict` ile yapılır.
Boyut uyumu, dinamik payload ve oyun senaryolarının yerine geçmez.

Host logları: `/home/m2web/dev/logs/{patchcheck,engine,eterbase,eterpack,data,link}.log`.
HTTP logu `/home/m2web/dev/preview.log`; bridge logu `docker logs m2web-dev-bridge`.

Yerel testler: `python3 -B -m unittest discover -s platform/web-kit/tools -p 'test_*.py'`.
Object cache testleri sistemdeki `clang++` veya `c++` ile gerçek derleme yapar.

Release için mevcut `package` → `publish` akışı kullanılır. Önizleme klasörü
canlıya kopyalanmaz.

Corpus değişmediyse hostta `/home/m2web/publish.sh --engine-only` kullanılabilir.
Yanındaki `publish_engine_check.py`, paket ile canlı corpus'un manifest/groups
baytlarını ve chunk ad/boyut envanterini karşılaştırır; fark varsa yayın başlamaz.
Bu mod corpus/CDN yüklemesini atlar, HTML'yi en son günceller ve ASan'ı korur.
Normal publish'in CDN önce sıralaması değişmedi. Giriş düzeltmesinde kullanılan
`publish_login_client.sh` ayrıca eski siteyi yedekler ve yayın başarısız olursa
geri alır. Bunlar hostta çalıştırılan release araçlarıdır; dev komutları otomatik
olarak yayın yapmaz.

## Ölçüm (2026-10-19)

Gerçek hostta ilk tam geliştirme döngüsü 248,6 saniye sürdü (engine 205 s).
Cache'ler hazırken, kaynak değişikliği olmayan `cpp` döngüsü 31,6 saniye
sürdü (engine 15 s, 359 object ve iki arşiv kullanıldı). Değişen dosyanın
derleme süresi buna eklenir; ortak header değişikliği daha çok dosyayı etkiler.
Root/locale `ui` döngüsü 60,5 saniye; bunun 39 saniyesi Python dönüşümüydü.
Yalnız `link` döngüsü 13,6 saniye. Süreler tarayıcının ilk asset indirmesini
içermez; o ilk açılışta gerekir, sonraki açılışlarda aynı hash'ler cache'lenir.
