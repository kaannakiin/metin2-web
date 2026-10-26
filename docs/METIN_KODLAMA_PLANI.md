# Oyun metinleri: kodlama teşhisi ve geçiş planı

Tarih: 2026-10-21. Durum: ilk web uygulaması kullanıcının talebiyle canlıya
yayınlandı; özel önizleme kapatıldı. Tarayıcı/oyun kabul testi kullanıcıda.

Son düzeltme: ilk yayındaki Python import çöküşü üzerine eski site geri
yüklendi; collections/JSON import kancası onarıldı ve `1792612335` sürümü
yeniden yayınlandı. Gerçek Python 3.13 açılış testi ve 31 yerel test başarılı.

## Resimdeki sorun

Bu örnek harf silinmesi değil, UTF-8 baytlarının eski bir kod sayfasıyla
okunmasıyla oluşan metin bozulmasıdır. Ayrı yerlerde gerçekten silinmiş veya
`?` ile değiştirilmiş harfler bulunabilir; bunlar kaynak kontrolünden geri alınır,
ekrandaki metne uygulanan bir dönüşümle güvenilir şekilde kurtarılamaz.

`content/client/packs/root/uiminimap.py:895` doğrudan `Savaş Bileti Seçiniz`,
896. satır ise `Ücretsiz` gönderiyor. Çeviri anahtarı kullanılmıyor.
UTF-8 baytlarını cp1254 ile okumak `SavaÅŸ Bileti SeÃ§iniz` ve `Ãœcretsiz`
sonucunu verir. Bu, ekran görüntüsündeki bozulma türünü yeniden üretir.
İlk teşhisteki bu sınır daha sonra build hostunda doğrulandı: üretilen
`scripts3/uiMiniMap.py` ve paketlenen kopyadaki metin doğru UTF-8; eski
`PythonPackModule.cpp` yaması bütün dosyaları görüntüleme kod sayfasıyla
çözüyordu. Üretilen betik daha `compile()` çağrısından önce bozuluyordu.

## Kaynaktan doğrulanan bulgular

| Katman | Bulgu | Sonuç |
| --- | --- | --- |
| Web betik üretimi | `platform/web-kit/tools/rewrite_scripts.py:106` karma cp1254/CP949 kaynakları satır bazında çözüp UTF-8 üretir. | Kaynağı topluca başka kodlamaya kaydetmek çözüm değil. |
| Python → çizici | `apps/client/source/EterPythonLib/PythonGraphicTextModule.cpp:61` metni `PyTuple_GetString` ile alıp `SetValue` çağırır. | Python 3 katmanından hangi baytların çıktığı denetlenmeli. |
| Çizici | `apps/client/source/EterLib/GrpTextInstance.cpp:156` varsayılan kod sayfasını kullanır; 218. satırda baytlar Unicode'a çevrilir. | Giriş kodlaması ile çizicinin beklentisi eşleşmeli. |
| Dil seçimi | `platform/web-kit/compat/runtime.js:915` dil başına 1252/1250/1254 gibi kod sayfaları seçer. | UTF-8 dosyaları bu sayfalara göre doğrudan okumak güvenli değil. |
| UTF-8 bayrağı | `apps/client/source/UserInterface/Locale.cpp:72` ve `:145`, `ENABLE_UTF8_ENCODING` açıkken 65001'i 1254'e zorlar. | Sadece bayrağı açmak veya locale.cfg'ye 65001 yazmak yetmez. |
| Dil dosyaları | İncelenen 11 dilin `locale_game.txt` ve `locale_interface.txt` dosyalarında Türkçe UTF-8 değil; diğer 10 dil UTF-8. Türkçe örnekler cp1254 ile doğru okunur. | Dosya kodlaması dilin eski kod sayfasından ayrı tanımlanmalı. |
| Çeviri yükleyicileri | `localeinfo.py:249` ve `uiscriptlocale.py:14` ayrı yükleyiciler kullanır; `line[:-1]` ile son karakteri atarlar. | Ortak yükleyici; LF, CRLF ve sonunda satır sonu olmayan dosyalar için test gerekir. |
| Sunucu | `apps/server/game/src/locale.cpp` dil başına sözlük tutar; çalışma notlarında cp1254'e çevrilmiş Türkçe sunucu mesajları kayıtlıdır. | Ağdaki her metnin UTF-8 olduğu varsayılamaz. |
| Portal | `apps/portal/src/server/context.ts` DB bağlantısı utf8mb4; `validation.ts` oyun parola baytlarıyla uyum için ASCII sınırı koyar. | UI kodlaması, hesap/parola protokolünden ayrı tutulmalı. |
| Eski dönüştürücü | `content/client/packs/root/convert_encoding.py:13` cp1254'ten önce latin-1 dener; 53. satırda `errors='replace'` kullanır. | Bu araç çok dilli toplu dönüşüm için kullanılmamalı. |

## “Tek fonksiyon” nasıl olmalı?

Ortaklaştırılacak şey, metnin **bilinen kaynak kodlamasından Unicode'a alınması**
ve bunun doğrulama kurallarıdır. Her girdide kodlama tahmini yapan veya bozuk
harfleri `replace` ile onaran genel bir fonksiyon olmamalı.

Hedef sözleşme: kaynak kimliği ve açık kodlama bilgisiyle metni çöz;
hatalı baytta dosya/satır veya mesaj türüyle hata bildir; içeride Unicode,
metin dosyaları ve web sınırlarında UTF-8 kullan. UTF-8 doğrulaması, NFC
normalizasyonu ve çeviri seçimi ayrı işlemlerdir. Hesap adı, parola, komut,
dosya yolu ve ikili paketlere genel metin normalizasyonu uygulanmaz.

Python, C++ ve TypeScript süreçleri fiziksel olarak aynı fonksiyonu çağırmaz.
Tek bir kodlama manifesti ve ortak test verileri kullanır; her süreç kendi
sınır adaptörünü uygular. Eski ağ metinleri yalnız kaynağı belli olan
alım/gönderim noktalarında dönüştürülür. Paket biçimi ve ağ/veri bayrakları
bu geçişte değiştirilmez.

## Uygulama sırası

1. **Envanter ve test verileri.** Dil dosyaları, Python metinleri, sunucu
   sözlükleri/quest çıktıları, proto isimleri ve sohbet için ayrı kodlama
   kayıtları oluştur. UTF-8 olmayan Türkçe dosyalar için açık cp1254 kaydı
   kullan; karma Python kaynaklarını topluca dönüştürme. Şüpheli bozuk metinleri
   raporla, otomatik düzeltme yapma.
2. **Ortak dil yükleyicisi.** İki Python locale yükleyicisini ortak çözümleme
   katmanına bağla. UTF-8 ve kayıtlı eski kodlamayı kesin kuralla çöz.
   Satır sonlarını güvenli ayır; çeviri anahtarlarını, tekrarları ve `%s`,
   `%d`, `{}` biçimlendirme alanlarını denetle. Eksik çeviri için açık bir
   yedek dil politikası ve geliştirici tanı kaydı kullan.
3. **Bu pencereyi düzelt.** Üç sabit etiketi çeviri anahtarlarına taşı;
   incelenen 11 dile ekle. Python 3 Unicode metninin çiziciye UTF-8 olarak
   işaretlenerek veya açık bir Unicode giriş noktasıyla verilmesini sağla.
   Çizicinin mevcut `@9999` UTF-8 belirteci olası bir geçiş aracıdır;
   metin birleştirme, mevcut kod sayfası etiketleri, kesme ve tıklama
   hesapları doğrulanmadan genel çözüm diye uygulanmaz.
4. **Sunucu ve diğer çizim yolları.** Sunucu sözlükleri, quest, bilgi mesajı,
   sohbet, eşya/canavar adları ve metin kuyruğu için kaynak kodlamasını
   açıkça bağla. Kişiden kişiye sohbeti alıcının diline göre tahminen çözme;
   gönderenin gerçek kodlamasını takip et. UTF-8'e geçişte karakter sayısı
   ile bayt sayısını ayır; paket uzunlukları ve kesme sınırlarını doğrula.
5. **Derleme ve yayın.** İstemci motoru değişirse engine ve bağımlı web
   adımlarını derle; yalnız metin değişikliğiyle sınırlı kalırsa gerekli
   pack/scripts/rewrite/uiscript/data/link/package adımlarını çalıştır.
   `patchcheck.py` geçmeli. Kaynakları ve kit değişikliklerini canlı
   kopyalarına eşle; çalışma notlarını güncelle. Sunucu değişikliklerini
   ayrı derleyip paketle. Canlı servis yeniden başlatma adımı mevcut
   depo kuralına göre kullanıcıya hazırlanmış komutla verilir.

## Kabul testleri

- **Bayt doğruluğu:** her kayıtlı kodlamada örnek baytlar → beklenen Unicode;
  yanlış/eksik UTF-8 dizisi ve kayıplı dönüşüm sessizce kabul edilmez.
  Aynı metni ikinci kez işlemek ek kodlama/dönüşüm üretmez.
- **Dil kapsamı:** tr, en, de, pl, cz, hu, pt, ro, fr, es, it için yeni
  anahtarlar ve biçim alanları doğrulanır. Mevcut anahtar eksikleri ayrıca
  başlangıç raporuna alınır; yeni değişiklik bunları artırmaz. Çeviri
  doğruluğu ayrıca dil incelemesi gerektirir.
- **Örnek harfler:** `İı Şş Ğğ Üü Öö Çç`, `äöüß`, `ąęłńśźż`, `čřěů`,
  `őű`, `ăâîșț`, `éèêç`, `ñá¿¡`, `ãõç`, `àèìòù`. Görünmeyen glifler
  kodlama testinden ayrı, yazı tipi kapsamı olarak raporlanır.
- **Dosya sınırları:** BOM, LF, CRLF, son satırda satır sonu olmaması;
  çok satırlı metin, renk/köprü etiketleri ve yer tutucular korunur.
- **Çalışan web istemcisi:** her dilde giriş, karakter seçimi, savaş bileti,
  eşya ipucu, quest, sunucu bilgi mesajı, sohbet ve duyuru görüntülenir.
  Türkçe savaş bileti başlığı ve `Ücretsiz` birebir doğru görünmeli.
  Metnin Python değeri, C++ giriş baytları ve çözülen Unicode değeri
  test modunda karşılaştırılır; parola veya özel sohbet içeriği loglanmaz.
- **Ağ uyumu:** eski/yeni istemciyle aynı sunucuya giriş; karakter adları,
  dil değişimi, çok baytlı mesajların uzunluk sınırında kesilmesi ve diğer
  dile sahip oyuncuya sohbet sınanır. Hesap/parola davranışı korunur.
- **Yayın kabulü:** build + patchcheck sonrası temiz önbellek ve mevcut
  önbellekle tarayıcı denemesi. Ekran görüntüsüyle kabul ve kullanıcı oyun
  testi tamamlanmadan “tüm diller düzeldi” denmez.

## İlk uygulama — 2026-10-21

- `platform/web-kit/compat/text_encoding.json`: üretilen Python betikleri
  UTF-8; 22 ana locale tablosu için açık dosya kodlaması. Görüntüleme ve ağ
  kod sayfası bu dosya kodlamalarından bağımsız tutulur.
- `compat/textcodec.py`: kayıtlı dosyalarda strict çözümleme, kaynak/offset
  hatası, ortak satır ayrıştırıcı ve yeni arayüz anahtarları için İngilizce
  yedek dil. Kayıtsız eski `.txt` dosyaları geçiş tamamlanana kadar önceki
  kod sayfası/replace politikasını açık bir uyumluluk kuralıyla korur.
- `compat/pack_text.h` ve stage yaması: bütün üretilen `.py` dosyalarını
  doğrudan UTF-8 çözer; locale tablosu çözümlemesini ortak Python katmanına
  bağlar. Betik hızlı yolu decoder import etmez: ilk önizlemede görülen
  `json → collections → pack.Get → yarım yüklenmiş textcodec` döngüsü bu
  şekilde giderildi; native regresyon testi bu durumu kapsar.
- İki locale yükleyicisi ve kule tablosu ortak satır ayrıştırıcısını kullanır.
  `line[:-1]` kaynaklı son harf kaybı önlenir. Değişiklikler Python 3 web
  üretiminde uygulanır; eski Windows kaynaklarının cp1254/CRLF baytları korunur.
- Savaş bileti üç sabit etiketten çeviri anahtarlarına geçti. `text_labels.json`
  aynı anahtarları 11 dilde sağlar. Dil çevirileri kullanıcı kabulüne tabidir.
- Üretilen Python dosyalarının eski `coding:` başlıkları UTF-8 ile eşleştirilir.
- `tools/audit_text_encoding.py`: salt okunur kodlama, yinelenen anahtar ve
  Türkçe sözlüğe göre eksik anahtar envanteri. İlk 22 dosyada çözümleme hatası
  ve U+FFFD yok; 654 yinelenen satır mevcut. Eksik/yinelenen eski anahtarlar
  başlangıç envanteridir; bu aşamada otomatik çevrilmedi veya silinmedi.
- Veri paketleme, gerçek `scripts3` girdilerindeki 22 tabloyu ve 11 dilin yeni
  anahtarlarını önce doğrular; hata varsa önceki data çıktısı silinmez.
- Dev eşitlemesi çözücüyü, sözleşmeleri, yeni kontrolleri ve değişen üretim
  araçlarını `/home/m2web/kit` kopyasına da taşır. Paketlenen çözücü/sözleşme
  kopyaları kaynaklarıyla karşılaştırıldı.

Doğrulama: 29 yerel araç testi geçti; C++ üzerinden gerçek CPython çağrısı,
paket importer bootstrap döngüsü, 11 dil örnekleri, hatalı baytlar, BOM ve
satır sonları dahil. Build hostunda 80/80 stage yaması, WASM engine,
protokol/RESP kontrolleri, data ve link başarılı; Python dönüşümünden sonra
parse edilemeyen dosya sayısı 0.

İlk tarayıcı açılışında bulunan bootstrap hatası düzeltildikten sonra
engine/data yeniden derlendi. Kullanıcının isteğiyle son tarayıcı doğrulaması
kullanıcıya bırakıldı; bu derleme için görsel kabul iddiası yok.

### Canlı yayın ve önizlemenin kapanması

- `platform/deploy/publish_text_encoding.sh` public paketi özel giriş
  dosyaları/preview HTML'si olmadan üretir; protokol, metin girdileri ve
  önizleme motor hash'ini doğrular. Önceki siteyi yedekler; hata halinde geri
  yükler. `publish.sh --engine-only` ile corpus'u değiştirmeden yayınlar.
- İlk hash kapısı yeniden linkteki girdi sırası farkını yakaladı ve yayını
  canlı dosyalara dokunmadan durdurdu. `link_client.py` artık `main_web.o` ve
  `link_data.o` dosyalarını genel object listesinden çıkarır; bunlar her
  seferinde `compile_entry` tarafından sona eklenir. Cache'de bulunmalarının
  sıralamayı değiştirmediğini doğrulayan regresyon testi eklendi. Yeni link ve
  public package önceki motorla birebir eşleşti.
- Link sırası testi dahil son yerel araç testleri: 30/30 başarılı.
- Yayın başarılı: 28 aday/canlı public dosya hash'i eşleşti. Motor SHA-256:
  `7bd48809cd6e2f6dc266193df9ae42bf833e1523473acdbe06dfa170298d10e7`.
  Yedek: `/home/m2web/backups/text-encoding-7pcQ09rg/site`.
- Public HTML ve sürümlü WASM HTTP 200. HTML `no-cache`; sürüm `1792611852`.
  Public WASM hash'i de adayla aynı; HTML'de özel önizleme ayarı yok.
- Özel HTTP önizlemesi ve dev bridge `dev_client.py stop` ile kapatıldı;
  bu oturumun yerel SSH tüneli sonlandırıldı. Localhost 18731 yanıt vermiyor.
  Snapshot dosyaları sonraki inceleme için duruyor; çalışan özel önizleme yok.

Sonraki kapsam: diğer `.txt`/quest kaynaklarının kaydı, sunucu mesaj ve sohbet
sınırları, Unicode'un eski çizici/kod sayfası üzerinden kayıpsız taşınması,
Windows yolu, mevcut eksik çeviriler ve biçim alanı uyumu. Mevcut ağ paketleri,
sunucu servisleri ve portal bu ilk uygulamada değiştirilmedi. Bu aşama bütün
dillerin bütün ekranlarda sorunsuz olduğu anlamına gelmez.

## Açılış regresyonu ve ikinci yayın

İlk canlı yayında root pack'teki Python 2 `collections.py`, Python 3 standart
paketini gölgeledi. Yeni çözücünün JSON import'u, import kancasının paket
fromlist davranışındaki eski sorunu da tetikledi. `traceback` yüklenemediği
için kullanıcı asıl hata yerine `collections.abc` hatasını gördü.

Önce çalışan eski site geri yüklendi. Ardından data üretiminde root
`collections.py` dışlandı; import kancası `collections` ve `__path__` taşıyan
paketleri standart Python yükleyicisine bırakacak şekilde düzeltildi.
Yalnız metadata/HTTP kontrolünün açılış başarısını kanıtlamadığı doğrulandı.

Yeni zorunlu test, gerçek dönüştürülmüş `system.py` import kancasını temiz
`-I -S` Python oturumunda çalıştırır. Pack'teki eski collections yoluna
girilmediğini, JSON'un paket alt modüllerini, textcodec'i, collections.abc'yi,
traceback'i ve bir oyun modülünü birlikte yükler; orijinal istisnanın görünür
kaldığını doğrular. Hem yerelde hem build container'ındaki Python 3.13 ile
geçti; tüm yerel araç testleri 31/31 başarılı.

Düzeltilmiş yayın yedeği: `/home/m2web/backups/text-encoding-DQsglLWg/site`.
Public sürüm `1792612335`; 28 aday/canlı dosya hash'i eşleşti. İnternetten
JS ve data HTTP 200 ile alındı; hash'leri canlı dosyalarla birebir aynı.
WASM `7bd48809...` olarak kaldı. Özel önizleme yeniden açılmadı;
`build_text_startup.sh` yalnız betikleri ve açılış testini çalıştırır.
Son görsel/oyun kabulü kullanıcıdadır.
