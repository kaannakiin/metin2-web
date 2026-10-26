# Web istemcisi: UX ve dosya yükleme incelemesi

Tarih: 22 Ekim 2026, Türkiye saati. Durum: uygulandı, canlıya yayınlandı.

Kapsam: oyunun kendi giriş ekranında Tab, hesap kaydetme alanları, Mac ve diğer cihazlarda yönlendirme; haritaya girişte/ışınlanırken ve oyun içinde yeni içerik görünürken donma. Kullanıcının son açıklaması: sorun özellikle **daha önce hiç girmemiş oyuncunun ilk girişinde** belirgin. İlk inceleme sonrasında kullanıcı uygulama ve canlı yayını istedi. Aşağıdaki ilk inceleme bulguları korunuyor; uygulama sonucu bu bölümde kayıtlı.

## Canlı uygulama sonucu

Pencere boyutu ek düzeltmesi: `v=1792692377` canlıda. Mantıksal oyun alanı
korunur, canvas yeni tarayıcı alanına orantılı sığdırılır; ilk konumlarına göre
çizilen envanter ve taskbar yeniden boyutlandırmayla kırpılmaz. 22 Node ve
4 Python testi geçti. Dar/kısa/dikey pencere, boyuta geri dönüş, küçük ilk
açılış ve fare koordinatı önizlemede; dar/kısa/geri dönüş public adreste
doğrulandı. Gerçek hesapla envanter açma henüz test edilmedi. Bu yayının geri
dönüş yedeği `/home/m2web/backups/web-ux-qLXUVIvx/site`.

- Public yapı: `v=1792689159`. 28 aday/canlı dosyanın hash'i eşleşti. Yedek: `/home/m2web/backups/web-ux-7Pdnfdvm/site`.
- Tab, eksik `WM_CHAR(9)` iletimi düzeltilerek gerçek tarayıcıda doğrulandı. Kaydet/yükle/sil açıklamaları ve Mac/Windows/Linux kontrol yardımı eklendi; HTML kontrolleri ve tarayıcı kısayolları oyun tuş yakalamasından ayrıldı.
- Web hesap yuvaları **yalnız kullanıcı adını** hatırlar. Şifre kalıcı depolamaya veya hazırlık bridge dosyalarına yazılmaz. Saklama sonucu localStorage'dan geri okunup doğrulanmadan başarı mesajı verilmez.
- Motor başlamadan manifest ve giriş ekranının altı zorunlu parçası asenkron hazırlanır. Boot/meta/motion grupları giriş isteğine ertelendi; auth bağlantısı bu parçalar RAM'de hazır olana kadar açılmaz. Bu veriler kaldırılmadı; yükleme zamanı değiştirildi.
- Harita hazır kontrolü tarihsel indirmeyi yeterli saymaz. Etkin parçalar RAM'de korunur; 60 saniye sonunda senkron yola kör geçiş kaldırıldı. İndirme/grup indeksi hataları süre sınırı ve yeniden denemeyle ele alınır.
- Doğrulama: 19 Node ve 4 Python testi, 81/81 stage yaması, üretilmiş CPython 3.13 açılışı ve source protokol kontrolleri başarılı. Özel önizleme ve public adreste gerçek Tab/Enter ile sahte hesap üzerinden beklenen auth hatası görüldü; hazırlık sırasında senkron XHR 0.
- Public boş önbellek testi: HTTP cache kapalı, SW bypass, Cache Storage boş. Giriş ekranına kadar motor+dil+corpus transferi **303.386.639 → 85.878.887 bayt**, yaklaşık **%71,7 daha az**. Zorunlu corpus kümesi 24 MiB; mevcut C++ komşu okumasıyla ekranda ölçülen RAM kümesi 32 MiB. Corpus/motor HTTP hatası yok. İlk motor hazırlığında **1.641 ms ana iş parçacığı görevi kaldı**; bütün hazırlama maliyetinin bittiği iddia edilmiyor.
- 1370 corpus parçası ve grup/manifest içeriği değişmedi. Engine-only yayın yapıldı; Cloudflare ayarı, CDN corpus yüklemesi, VM veya production servis restart'ı gerekmedi.
- Gerçek hesapla harita içi oynanış profili henüz alınmadı. Aşağıdaki oyun içi bağımlılık/GPU incelemesi önerileri bu doğrulamanın yerini tutmaz. Yayın sonrası ek çalışma gerekirse aynı cihaz ve rota üzerinde ölçülmeli.

## Sonuç

İlk ziyaretin yükü yüksek: Türkçe giriş ekranı ve başlangıç grupları için, henüz hesaba/haritaya girmeden yaklaşık **303,4 MB ağ transferi** ölçüldü. Aynı temiz önbellek testinde **2.334 ms ana iş parçacığı blokajı** ve toplam **855 ms senkron XHR** vardı. Kullanıcının anlattığı senaryo için ilk öncelik bu başlangıç yükünü aşamalara ayırmak.

Dosyaları ihtiyaca göre, gruplar halinde indirme yaklaşımı mevcut. Cloudflare üzerinden sunum ve tarayıcıdaki disk önbelleği örnek kontrollerde çalışıyor. Ayrıca **indirilmiş olmak ile motorun senkron erişebileceği RAM'de bulunmak aynı sayılıyor**. Bu, özellikle sonraki harita geçişleri için ayrı bir doğrulanmış hata; ilk ziyaret sorununun tek açıklaması olarak görülmemeli.

RAM'de bulunmayan bir parça gerektiğinde motor hâlâ senkron XHR kullanıyor. Ana iş parçacığı bu okumayı bitirene kadar çizim duruyor. Oyun içinde yeni görünen oyuncu, yaratık veya efektlerin bağımlılık kapsamı da ayrıca ölçülmeli. Her donmanın ağ kaynaklı olduğu henüz gösterilmiş değil; model açma, doku hazırlama ve GPU'ya yükleme de ayrı ölçülmeli.

## Doğrulanan bulgular

| ID | Bulgu ve kanıt | Etki / öncelik |
|---|---|---|
| UX-1 | Canlı tarayıcıda Tab, yalnızca `WM_KEYDOWN` (`k=256, w=9`) üretiyor. `WM_CHAR(9)` yok. Python giriş ekranındaki `SetTabEvent` doğru bağlı; C++ IME ise Tab geçişini `WM_CHAR` üzerinden tetikliyor. | Kullanıcı adı → şifre geçişi çalışmıyor. Yüksek. |
| UX-2 | Hesap yuvaları F1–F4 ve disk ikonlarıyla gösteriliyor. Kaydet/yükle düğmelerinde açıklayıcı tooltip tanımı yok. Web uyarlaması Windows registry olmadığında yazmayı `FALSE` ile atlıyor; `SaveAccount` dönüş değerini denetlemeden başarı mesajı veriyor. | Sorun yalnızca etiket eksikliği değil; saklanmayan hesap için başarı bildirimi riski var. Yüksek. |
| UX-3 | Sayfa canvas ağırlıklı; oyun giriş alanları HTML input değil. Şablonda platforma göre kontrol yardımı yok. Tuş yakalama kodu document/window seviyesinde geniş `preventDefault` kullanıyor. | Mac işlev tuşları ve tarayıcı kısayolları açıklanmıyor; odağa göre tuş yakalama ayrıca ele alınmalı. Orta. |
| START-1 | Temiz önbellekte yalnız giriş + başlangıç için motor/dil dosyaları 45,8 MB, corpus istekleri 257,6 MB transfer yaptı. İlk oturumdan kaydedilmiş boot, tüm meta ve motion grupları beraber başlatılıyor. | Yeni oyuncunun ilk deneyiminde yüksek indirme ve hazırlama maliyeti. Kullanıcının bildirdiği ana senaryo; yüksek. |
| FS-1 | `mapReady`, RAM kontrolüne ek olarak tarihsel `p.fetched` kümesini de hazır kabul ediyor. Aynı fonksiyon canlı pakette mevcut. İzole simülasyonda parça indirilip RAM'den çıkarıldı: `inRAM=false`, `historicallyFetched=true`, `mapReady=1`. | Özellikle haritaya geri dönüşte, arka plan okuması tamamlanmadan motor yüklemeye başlayabilir. Yüksek. |
| FS-2 | C++ parça önbelleği ve JS RAM önbelleğinde bulunmayan veri `m2w.fetchSync` → `xhr.open('GET', url, false)` yoluna düşüyor. Senkron XHR, Cache Storage'ı doğrudan okuyamıyor. | Diskte veya Cloudflare'da bulunması tek başına kare donmasını önlemiyor. Yüksek. |
| FS-3 | `mapReady` 60 saniye dolunca veya harita grubu tanınmıyorsa hazır dönebiliyor. `ProcessDeferredCache`, veri hazır olmasa da 5 saniye sonunda `LoadStaticCache` çağırabiliyor. Kare başına 4 ms kontrolü tek bir bloklayan yüklemeyi bölemiyor. | Yavaş/başarısız indirmede akıcı bekleme tekrar bloklayan yüklemeye dönüşebilir. Kod yolu doğrulandı; kullanıcı oturumundaki sıklığı ölçülmedi. Yüksek. |

Kaynak konumları:

- `platform/web-kit/compat/runtime.js:584–608`: DOM → Windows tuş mesajları.
- `content/client/packs/root/intrologin.py:548–552`: Tab bağlantıları; `:688–700`: koşulsuz kayıt başarı mesajı.
- `apps/client/source/UserInterface/PythonIME.cpp:71–85`: `WM_CHAR` / Tab işleme.
- `content/client/packs/root/uiscript/loginwindow.py:241–409`: hesap yuvaları ve ikonlar.
- `platform/web-kit/tools/script_patches.py:277–292`: web'de registry yazma/okuma davranışı.
- `platform/web-kit/compat/runtime.js:1573–1596`: hazır kontrolü; `:1179–1199`: senkron XHR.
- `platform/web-kit/compat/webfs_web.cpp:186–220`: RAM kaçırma, senkron indirme ve komşu parça ön-yüklemesi.
- `apps/client/source/UserInterface/PythonPlayerSettingsModule.cpp:124–142`: ertelenmiş yükleme.

## Ölçülenler ve sınırlar

Canlı `client.html`, Mac üzerinde Chrome 155 ile incelendi. Yapı sürümü `?v=1792614571`; HTML `Last-Modified` 21 Ekim 2026. Hesapla oyuna giriş yapılmadı; gerçek harita rotası ve yeni varlık belirmesi profili henüz alınmadı.

İlk iki açılışta tüm önbelleklerin başlangıç durumu doğrulanmadı. Sonrasında ayrı bir temiz önbellek testi yapıldı: `m2w-corpus` silindi ve boş olduğu doğrulandı; HTTP cache kapatıldı, service worker atlandı. CDP yanıtlarında corpus için `fromDiskCache=0`, `fromServiceWorker=0`; grup ön-yükleyicisinde disk isabeti 0 doğrulandı. Cloudflare edge önbelleği temizlenmedi. Bu test ağ hızı sınırlandırılmadan yapıldı; service worker atlama ayarı sadece ölçüm oturumundaydı.

| Ölçüm | Sonuç | Yorum |
|---|---|---|
| Temiz önbellek: ağ transferi | Motor/dil 45.798.920 + corpus 257.587.719 = 303.386.639 bayt | Yaklaşık 303,4 MB / 289,3 MiB. CDP aktarım sayacı; giriş ekranı ve başlangıç grupları, harita hariç. |
| Temiz önbellek: blokaj | En uzun görev 2.334 ms; 4 senkron XHR toplam 855 ms | XHR süreleri 303 / 259 / 153 / 140 ms. Görevin tamamı ağ maliyeti değil. |
| Temiz önbellek: tamamlanma | Son kaynak yanıtı yaklaşık 8,8 saniyede | Bu test bağlantısının sonucu; oynanabilir olma veya yavaş bağlantı süresi değil. 56 grup ağ okuması, 0 grup disk isabeti, 0 hata. Diğer parçalar senkron/komşu okuma yoluyla tamamlanıyor. |
| İlk incelenen açılışın en uzun ana iş parçacığı görevi | Yaklaşık 2.900 ms | Yalnızca ağ süresi değil; başlangıç işleme maliyetini de içerir. |
| Aynı açılışta senkron XHR | 4 çağrı, toplam yaklaşık 689 ms | Manifest 596 ms; üç parça 29 / 33 / 31 ms. |
| Yeniden yüklemede en uzun görev | Yaklaşık 1.339 ms | Önbellek kullanılsa da ana iş parçacığı işi sürüyor. Tek örnek; p95 değil. |
| Yeniden yüklemede senkron XHR | 4 çağrı, toplam yaklaşık 344 ms | Sıcak önbellekte de senkron yol mevcut. |
| Yeniden yüklemede ön-yükleyici | 56 disk isabeti, 0 ağ okuması, 0 hata | Bu sayaç yalnızca grup ön-yükleyicisine ait; tüm sayfanın ağ trafiği değil. |
| Başlangıç grupları | boot 25, meta 17, motion 19; toplam 61 parça | RAM'de toplam 251.014.894 bayt, yaklaşık 239,4 MiB. |
| Köy haritası grupları | a1 12, b1 24, c1 18 parça | 4 MiB parça boyuna göre üst sınırlar 48 / 96 / 72 MiB. |
| En büyük mevcut harita grubu | 51 parça; en fazla 204 MiB | Tek başına hiçbir harita grubu 512 MiB'ı aşmıyor. |

JS parça bütçesi cihaz bilgisine göre 512 veya 768 MiB. Buna ek olarak C++ önbelleğinde en fazla 16 parça, WASM belleği, açılmış dosyalar ve doku/model belleği bulunuyor. Toplam bellek ölçülmedi. Bu nedenle ilk çözüm olarak RAM bütçesini artırmak için kanıt yok.

Mevcut `tools/test_prefetch.js` Node ile çalıştırıldı: **9 test geçti**. Bu testler yeniden deneme, zaman aşımı ve önbellek hatalarını kapsıyor. RAM'den çıkarılmış bir haritanın erken hazır sayılmasını yakalayan test yok; yukarıdaki ayrı simülasyon bu açığı doğruladı. Mevcut testte tarihsel indirme durumunun korunması bekleniyor: ilerleme sayacı için bu davranış korunabilir; harita hazır koşulu ayrı olmalı.

Ölçüm sırasında dışa aktarılmamış `Module.HEAPU8` özelliğini sorgulamak tanılama sekmesini durdurdu. Sekme yeniden yüklendi; bu olay üründe kendiliğinden oluşan hata olarak sınıflandırılmadı.

## Cloudflare MCP ve canlı HTTP kontrolü

| Kontrol | Canlı durum |
|---|---|
| DNS | `metin2.kaanakin.dev` proxied; zone planı Free Website. |
| Corpus rotası | `metin2.kaanakin.dev/corpus/*` → `metin2-corpus`. |
| Cache kuralları | Hash'li corpus parçaları, `?v=` motor/dil dosyaları ve portal asset'leri cache edilebilir; diğer yollar için bypass kuralı var. |
| Motor dosyası örneği | Sürümlü WASM: `200`, `CF-Cache-Status: HIT`, bir yıllık TTL. |
| Corpus parçası örneği | `200`, bir yıllık `immutable`; sorgulanan örnekte edge `MISS`. Tek MISS genel cache sorunu göstermez. |
| Manifest / groups | `200`, `Cache-Control: no-cache`; Worker yanıtında `CF-Cache-Status: HIT` görülebildi. `no-cache` depolamayı tamamen yasaklamaz, yeniden doğrulama ister. Bu başlık tek başına eski veri kanıtı değil. |
| HTML / service worker | `no-cache`, `DYNAMIC`. |
| Protokol ve dönüşüm | HTTP/2, HTTP/3, Brotli açık; ölçülen motor istekleri h3. Rocket Loader kapalı; SSL strict. |

Zone kuralları, Worker statik varlık sunumunun bütün cache davranışını tek başına açıklamaz; gerçek yanıt başlıkları da kontrol edildi. Hesap genelinde veya oyuncuların farklı bölgelerinde cache isabet oranı / gecikme dağılımı ölçülmedi. Ücretli özellik açmak veya CDN mimarisini değiştirmek için bu aşamada gerekçe bulunmadı.

## Oyun içi donmalar için henüz doğrulanmayanlar

1. Harita grupları, harita klasörü → property → model → doku zincirinden statik çıkarılıyor. Sunucudan sonradan gelen oyuncu ekipmanları, yaratıklar ve efektlerin tamamını kapsadığı gösterilmiş değil. İlk oturumdan kaydedilmiş boot listesi her oyun senaryosunu temsil etmeyebilir.
2. `corpus_groups.py`, Granny doku çözümlemesindeki hataları sessizce geçiyor. Eksik bağımlılık sayısı ölçülmeden tüm haritalar için “tam ön-yükleme” denemez.
3. Eviction kodu, okunmuş parçaları önce atıyor; etkin haritanın sıcak parçaları için kesin koruma görünmüyor. Farklı haritalar/karakterler için ön-yükleme RAM baskısını ve yeniden okumaları artırabilir.
4. Senkron ağ çağrısı olmadan oluşan model/doku açma, GPU yükleme veya oyun güncellemesi kaynaklı kare sıçramaları henüz ayrıştırılmadı. Sunucu tick/gecikmesi için veri toplanmadı.
5. Yayında yalnız güncel corpus tutulması, eski sürüm açık kalan sekmeler için yeniden yükleme ihtiyacı yaratıyor. Sürüm değişimini algılama ve kullanıcı bildirimi ayrıca doğrulanmalı.

## Önerilen çözüm sırası

Bu sıra tartışmaya açık uygulama taslağıdır. İlk iki iş kolu küçük ve bağımsız ilerleyebilir; dosya yerleşimi/çok iş parçacığı değişikliği ölçümden sonra seçilir.

### 1. Ölçüm ve yeniden üretim

- Kullanıcının cihaz/tarayıcısı, örnek haritası ve tetikleyici eylemiyle tekrarlanabilir rota seç.
- Aynı rota için ilk ziyaret, tekrar ziyaret, haritadan çıkıp geri dönüş, yeni oyuncu/yaratık/efekt ve sınırlı bellek senaryolarını kaydet.
- Parça okumasında kaynak, süre, RAM isabeti/çıkarma, ön-yükleme nedeni ve harita durumunu ölç. Ağ bekleme ile dosya açma/doku hazırlamayı ayrı zamanla.
- Hesap adı/şifre içermeyen yerel tanılama çıktısı üret. Başarı ölçütleri ve pilot cihaz listesi bu baseline'dan sonra kesinleşsin.

### 2. Giriş ekranı ve doğru geri bildirim

- Web köprüsünde Tab karakter mesajını doğru ilet; Tab, Shift+Tab, Enter ve odak kaybını gerçek tarayıcıda doğrula. Tuş yakalamayı oyun odağıyla sınırla.
- Kaydet / yükle / sil işlemlerine metin ve tooltip ekle. Başarısız saklamada başarı mesajı verme.
- Web'de “hesabı hatırla” kapsamını belirle: kullanıcı adı mı, portal oturumu mu? Şifreyi kalıcı tarayıcı depolamasına yazmayı varsayılan çözüm seçme.
- Mac ve Windows/Linux için kısa kontrol yardımı ekle. Mac'te F tuşları için ayara göre Fn/Globe gerekebileceğini belirt; temel işlemlerin görünür tıklanabilir karşılığı bulunsun. Mobil için destek durumunu gerçek cihaz testiyle belirle.

### 3. Hazır olma ve önbellek doğruluğu

- Tarihsel indirme ilerlemesini anlık RAM'de okunabilirlikten ayır. `mapReady`, gerekli parça motorun erişebileceği bellekteyken izin versin.
- Diskteki parçaları harita bekleme evresinde asenkron olarak RAM'e geri getir; bu işlem bitmeden hazır deme.
- Geçiş süresince kritik parçaları koru; etkin harita, ortak sıcak kaynaklar ve arka plan işleri arasında açık öncelik uygula. Bütçeye sığmayan çalışma kümesi için ayrı davranış tasarla.
- Zaman aşımı/kalıcı hata durumunu yükleme ekranında göster; tekrar deneme sun. Körlemesine senkron yüklemeye geçişi kaldırmak için motorun devam akışı ve ağ paket kuyruğunu birlikte değerlendir.
- Geçmiş indirme korunurken RAM'den çıkarma → geri dönüş, disk okuması devam ederken hazır kontrolü, indirme hatası ve 60 saniye sınırı için regresyon testleri ekle.

### 4. İlk ziyaret yükü ve oyun sırasında ihtiyaç duyulan içerik

- Başlangıçta beraber gelen yaklaşık 239,4 MiB boot/meta/motion içeriğini giriş ekranı, karakter seçimi, harita ve savaş aşamalarına ayır. İlk kayıttaki boot listesini yeniden ölç; girişten önce gerekmeyen kaynakları sonraki aşamaya taşı.
- Motion ve diğer ortak kaynakları karakter/ırk ve gerçekten görülecek içerik temelinde önceliklendir. Seçili karakter ve çevresi için gerekli güvenli bağımlılık kümesini belirlemeden kaynakları körlemesine erteleme.
- Başlangıç veri paketindeki 58,9 MB açılmış `client.data` ile Türkçe dil paketinin 17,7 MB içeriğini incele; mevcut paket ayırma düzeninde hâlâ ilk ekran için gerekmeyen dosyalar var mı belirle. Bu boyutlar açılmış veri boyutu; ağ transferiyle karıştırılmamalı.
- Gerçek rotanın dosya erişim kaydını statik harita grubuyla karşılaştır; eksikleri dosya türü ve tetikleyiciye göre çıkar.
- Önce görülecek NPC/yaratık, oyuncu görünümü, ekipman ve efekt bağımlılıklarını uygun noktada asenkron sırala. Ağ protokolünü değiştirmeden istemcinin bildiği bilgilerle başla.
- Statik bağımlılık çözümleme hatalarını say ve raporla. Sıcak ortak kaynakları hedefli tut; her oturumda bütün corpus'u indirme.
- 4 MiB parça yerleşimini yalnız erişim kayıtları gerektiriyorsa değiştir. Arka plan komşu-parça okumalarının yararını/israfını ölç.
- Ağ kaynaklı blokaj giderildikten sonra kalan model/doku işini karelere böl veya önceden hazırla. Motoru Worker'a taşıma / Asyncify gibi büyük değişiklikleri ancak kalan veriler gerektirirse ayrı tasarla.

### 5. Doğrulama ve yayın

- Pilot masaüstü tarayıcıları: Mac Chrome/Safari, Windows Chrome/Edge, Linux Chrome/Firefox; nihai liste kullanıcı cihazına göre daraltılabilir. Mobil destek ayrıca karar gerektirir.
- Sıcak rotada kritik senkron corpus indirmesi hedefi sıfır. İlk geçişte indirme boyunca yükleme animasyonu ve hata/yeniden deneme akışı yanıt verebilmeli.
- 100 ms üstü kare duraklamalarını kaydet; kaynağı ağ, kaynak hazırlama veya oyun güncellemesi olarak ayır. Performans iddiasını aynı cihaz/rota öncesi-sonrası ölçümüne dayandır.
- Değişen kapsam için build ve `patchcheck.py`; kit değişiklikleri repo + canlı kit eşlemesi. Client C++ değişirse cp1254/CRLF ve websrc senkron kurallarını koru.
- Yayından önce `CALISMA_NOTLARI.md` güncelle. Mevcut sunucu/Traefik değişikliği gerektirmeyen bir istemci yayını hedefle; gerekli olursa o kapsamı ayrıca değerlendir.

## Açık kullanıcı bilgisi

Öncelikli yeniden üretim koşulu net: daha önce hiç girmemiş oyuncu / boş asset önbelleği. Kullanıcının cihaz/tarayıcısı henüz belirtilmedi; bu bilgi sonraki gerçek cihaz karşılaştırması için yararlı. Harita/eylem örneği, oyun içi ikinci ölçüm aşamasında alınabilir.

## Resmî kaynaklar

- [MDN: senkron XHR ve arayüzün bloklanması](https://developer.mozilla.org/en-US/docs/Web/API/XMLHttpRequest_API/Synchronous_and_Asynchronous_Requests).
- [Cloudflare: Workers Static Assets yanıt başlıkları](https://developers.cloudflare.com/workers/static-assets/headers/).
- [Cloudflare: Static Assets cache davranışı](https://developers.cloudflare.com/workers/static-assets/).
- [Apple: Mac'te işlev tuşları ve Fn/Globe](https://support.apple.com/en-us/102439).

Cloudflare kaynakları MCP doküman aramasıyla; hesap durumu MCP API GET çağrılarıyla incelendi. Canlı HTTP başlıkları ayrıca örneklendi.
