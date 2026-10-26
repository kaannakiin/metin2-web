# Anka2 – Sunucu + Web (WASM) Çalışma Notları

### BK okuma penceresinde beceriye göre adet — 2026-10-23 (canlı)

- `uibkoku.py` bütün `50300` kitaplarını `GetItemCountByVnum` ile sayıyordu.
  Kitabın beceri kimliği `socket[0]` içinde; farklı becerilerin kitapları aynı
  eşya vnum'unu kullanır. Pencere bu ayrımı göstermediği için sayı yanıltıcıydı.
- Sayaç artık seçilen Master becerinin kimliğiyle eşleşen kitapları, bütün
  normal envanter slotlarında yığın adetleriyle toplar. Seçim yoksa, kitap
  kalmadıysa veya beceri artık Master değilse kitap slotu temizlenir.
- Sunucudaki `BKBul`, `/bkoku` tekli ve toplu okuma yolları zaten hem `50300`
  hem beceri soketini kontrol ediyor; incelenen bu yollarda başka becerinin
  kitabını tüketen bir eşleşme bulunmadı. Sunucu davranışı değiştirilmedi.
- Python UI dosyası UTF-8 kaynak bildirimiyle kaydedildi; Türkçe mesajlar
  korundu. Sekiz karışık envanter senaryosu yerelde ve host üzerinde geçti.
- **Canlı sürüm `1792749080`:** kullanıcı yayını yetkilendirdi. Çalışan
  `client.data` içindeki 2.224 dosya karşılaştırıldı; yalnız `/uibkoku.py`
  değişti. `client.js` içinde yalnız paket metadata'sı (ofsetler/boyut),
  HTML'de yalnız sürüm etiketleri güncellendi. Motor yeniden derlenmedi;
  WASM SHA-256 `8779c916b81863e65cba21b8da17852cb0dde1ecbf5eced25c137e7b95f3937a`
  aynı. Mevcut seçenek/karakter layout'ları birebir korundu.
- Patchcheck 81/81, JS sözdizimi ve gerçek CPython 3.13 modül sözdizimi
  kontrolü geçti. Public HTML 200/no-cache ve yeni sürüm; public JS 200;
  public data içindeki düzeltilmiş modül doğrulanan adayla birebir eşleşti.
  Kaynak overlay/scripts/scripts3/data kopyaları sonraki build için eşitlendi.
  VM, corpus ve servisler değişmedi. Gerçek oyun testi kullanıcıda.
- Yedek: `/home/m2web/backups/bk-count-8ryxb3q5/site` (üç yayın dosyası).
  Yayın aracı: `platform/deploy/release_bk_count.py`; hata durumunda kaynak
  girdileri ve yayın dosyalarını geri alır. Ruh taşı kontrolünde bulunan
  ayrı sunucu doğrulama eksiği `docs/BECERI_OKUMA_INCELEMESI.md` içinde;
  bu yayında sunucu davranışı değiştirilmedi.

### Eski 11 eşyanın uygunsuz efsun temizliği — 2026-10-22 (uygulandı)

- **SON DURUM — uygulandı:** kullanıcı “uygula bunları” diyerek hazırlanmış
  kısa bakımı yetkilendirdi. 11 eşyadan 15 hatalı normal efsun kaldırıldı;
  doğal Dolunay çifti, diğer geçerli efsunlar ve tüm diğer eşya alanları
  önce/sonra tam satır karşılaştırmasıyla korundu. Canlı yeniden okumada
  hedef 11 eşyada hatalı tür kalmadı. Yeni welcome görevi kuruldu ve kaynak
  adayla eşleşti. Altı süreç ve altı port sağlıklı; 14 kapalı efsun izni
  yeniden başlatma ile core'lara alındı. Yedek:
  `/home/m2web/backups/item-attribute-cleanup-q4lv7_si`.
- Servis açılışından sonra bakım SSH istemcisi kapanışta takıldı. Oyun
  sağlığı bağımsız doğrulandı; yalnız bu bakım istemcisi kapatıldı. Kurulum
  yeniden doğrulanıp tamamlandı işareti yazıldı. Bakım araçlarında SSH stdin
  ve servis log yönlendirmesi düzeltildi. Tekrar oyun restart'ı gerekmedi.

- Kullanıcı mevcut 11 eşyanın da temizlenmesini onayladı. Karakter/eşya/
  uygunsuz bonus listesi `docs/EFSUN_ESKI_ESYA_TEMIZLIGI.md` içinde.
- Hedef ID'ler sabit; bakım sırasında son kaydedilen efsunlar yeniden okunur.
  Yalnız 14 kapalı türe ait hatalı normal bonuslar kaldırılır. Doğal Dolunay
  çifti, geçerli bonuslar, soket/taş, nadir slotlar ve diğer alanlar korunur.
  Boşluk bırakmadan normal slotları sıkıştırır; başka efsun üretmez.
- Üç başlangıç silahı bonusunun görevdeki `63,10` çiftinden geldiği görüldü.
  Kaynak/aday farkının yalnız bu üç çiftin kaldırılması olduğu doğrulandı;
  gerçek qc derlemesi geçti. Yeni karakterlere tekrar genel canavar efsunu
  verilmez. Görev adayı `/usr/home/attribute-cleanup-welcome-20261022`.
- 5 yerel test geçti. Canlı eşya satırları salt okunur incelendi; **henüz
  temizlenmedi**. Takılı/switchbot eşyaları bellekteyken DB'yi değiştirmek
  güvenli değil; yedek/geri dönüş ve kısa bakım sağlayan tek komut hazır.
  AGENTS.md otomatik VM restart'ını yasakladığı için operatör çalıştıracak.
  Chrome testi yapılmadı. Satıcı paketi bu bakımdan bağımsız kalır.

### Klasik dışı 14 efsunun rastgele havuzdan kapatılması — 2026-10-22

- Kullanıcı hiçbir bonusun normal edinim/ekipman sınırları dışında gelmesini
  istemiyor. Önceki 45 satırlık normalleştirmede bırakılan 14 türün tüm 12
  normal/kostüm/tılsım izin sütunu sıfırlandı. Doğal silah ortalama/beceri
  üretimi, sabit proto bonusları, diğer 45 tür ve 6–7 tablosu korunur.
- Seed ve sınırlı geçiş aynı. Gerçek MariaDB geçici tablo testi ve canlı
  uygulama öncesi/sonrası tam tablo karşılaştırması geçti. Canlı DB uygulandı;
  bütün oyun core'larının yeni tabloyu alması için **GM `/reload p` gerekli**.
  Otomatik VM restart'ı veya Chrome testi yapılmadı.
- Yedek host `/home/m2web/backups/classic-attributes-rp0lju4k`:
  before/after/rare JSON snapshot'ları ve yalnız 14 satırlık geri dönüş SQL'i.
- Mevcut ilk beş slot taramasında 11 eşya (1 kalkan) bu türleri taşıyor.
  Doğal silah ortalama/beceri slotlarının 13'ü hariç tutuldu. Mevcut eşyalara
  dokunulmadı. Ayrıntı: `docs/EFSUN_KLASIK_IZINLER.md`.

### Satıcı: Küre ve kalıcı destek yedekleri — 2026-10-22 (kuruluma hazır)

- Kullanıcının son fiyatı: Kutsama Küresi `70024` **1.000.000 Yang**;
  başlangıçtaki 14 kalıcı desteğin her biri **1.000 Yang**. Küçük/orta HP-SP,
  süreli yeşil/mor ve iki dönüş kâğıdı kaldırılır; büyük HP-SP ve özütler kalır.
- Market 24 ürün; diğer dört mağaza aynı. Beş mağazada 110 ürün. Profil,
  iki SQL, fresh seed, hedef ve stok rehberi güncellendi.
- Kürenin eski NPC geri satışı 30 milyondu. `CItem::GetShopBuyPrice` yalnız
  bu vnum için mevcut değer ile 500.000'in küçüğünü kullanır; al-sat açığı
  kapanır. İstemci paketi ve eski binary protolar değiştirilmez.
- Üç yerel test ve gerçek FreeBSD game derlemesi geçti. Aday:
  `/usr/metin2-progression-20261022-202621` (`READY`). Kurulu kalıcı destek
  binary'sinin kaynak ağacı kullanıldı ve önceki binary ile eşleşmesi
  doğrulandı; `/usr/metin2/apps/server` eski kaldığından kullanılmadı.
- **Canlı satıcı henüz değişmedi.** `AGENTS.md` gereği restart operatör adımı:
  `docs/NPC_MARKET_KURULUM.md` ve host `install_npc_market_host.sh`.
  Browser testi kullanıcının isteğiyle kullanıcıda.

### Seçenekler panelinin eksik web dosyaları — 2026-10-22

- **SON DURUM — yeniden canlı:** yapı `1792700594`. Aşağıdaki geri alma
  sonrasında, çalışan paketin 166 layout'u birebir korundu; yalnız sekiz
  seçenek layout'u eklendi. Tüm 2.216 eski data dosyasının hash'i aynı,
  eklenenler tam sekiz dosya; WASM aynı. Patchcheck 81/81, 178 sözdizimi
  kontrolü, 8 layout yürütme, Python açılışı ve protokol kontrolü geçti.
  28 aday/canlı dosya eşleşti. Yedek: `/home/m2web/backups/options-I8lX62jP/site`.
  Oyunda karakter girişi ve Seçenekler açma testi kullanıcıda; yeni Chrome
  testi yapılmadı. Yayın scripti eski paket dosyalarının değişmesini reddeder.

- **GERİ ALINDI:** kullanıcı `1792700164` sonrası karakter seçiminden dünyaya
  giremediğini bildirdi. Önceki `/home/m2web/backups/options-Ltk1V6WH/site`
  geri yüklendi; 29 dosyanın yedek/canlı hash eşitliği doğrulandı. Hatalı
  paket `/home/m2web/backups/options-failed-KcjXBxow` içinde korundu.
  Satıcı çalışması durduruldu; tekrar yayın yapmadan giriş regresyonunun
  nedeni belirlenmeli. Chrome/oyun testi kullanıcının isteğiyle kullanıcıda.
- Paketlerin dosya bazında karşılaştırması kök nedeni gösterdi: mevcut
  `/UIScript/CharacterWindow.py` yeniden üretim sırasında eski corpus
  kaynağından geldi; `leader_board` / `passive_expanded_btn` eklemesi ve
  title kontrollerindeki tuple→list düzeltmesi kayboldu. `content/client/packs/root/uiscript/characterwindow.py`
  bu düzeltmeyi içeriyor; yeniden üretimde doğru kaynak/overlay korunmalı.
  Ayrıca istek dışında dört `UIScript/track/*` layout'u eklenmişti.
  Yerel yayın scriptine tüm mevcut data dosyalarının hash'ini koruyan ve
  yalnız sekiz seçenek layout'u eklenmesine izin veren kapsam kontrolü
  eklendi. Hatalı aday bu kontrolden geçemez; yeni yayın yapılmadı.

- Kullanıcı: oyun içinde Ayarlar → Seçenekler'e basınca oyun kapanıyor.
  `uisystem.py` gelişmiş paneli açıyor; panel ilk oluşturulurken
  `UIScript/advanced_game_options/game_option_0.py` ve diğer kategorileri okuyor.
- Build hostunda `build/port/uiscript3/UIScript/advanced_game_options/game_option_0.py`
  bulunmadığı doğrulandı. `uiscript_from_client.py` yalnız üst dizindeki
  dosyaları alıyordu; alt dizinler hem kopyalama hem bölme/sözdizimi
  denetimi dışında kalıyordu. `ui.py` layout okuma hatasında `exception.Abort`
  çağırdığı için bu eksik, bildirilen kapanmanın güçlü adayıdır.
- Yerel düzeltme: alt dizinleri yollarını koruyarak dahil et; Python 2→3,
  tamsayı bölme ve sözdizimi denetimini tüm layout'lara uygula. Bytecode
  dosyalarını dışarıda bırak; lib2to3 başarısızlığında build'i durdur.
- Üç yerel regresyon testi geçti: iç içe layout/aynı adlı dosyalar/kodlama/
  koordinat dönüşümü, alt dizinde sözdizimi hatası ve bytecode dışlama.
  Bu testlerde dönüştürücü bağımlılıkları taklittir; gerçek container build'i
  veya oyun içi kabul testi yerine geçmez.
- Durum: **canlıya yayınlandı**, yapı `1792700164`. Gerçek container'da
  patchcheck 81/81, 178 layout sözdizimi kontrolü, 8 gelişmiş ayar layout'unun
  yürütülmesi, Python başlangıç testi ve source protokol kontrolü geçti.
  Sekiz dosyanın public data ve dosya indeksinde bulunduğu doğrulandı;
  28 aday/canlı dosya hash'i eşleşti. Public HTML 200/no-cache ve yeni sürüm
  etiketi doğrulandı. WASM aynı kaldı: `8779c916b81863e65cba21b8da17852cb0dde1ecbf5eced25c137e7b95f3937a`.
  Yedek: `/home/m2web/backups/options-Ltk1V6WH/site`.
  Corpus, VM ve servisler değişmedi. Yayın scriptleri `release_options_*.sh`.
  **Oyun içi/Chrome testi kullanıcıda**; kullanıcı testin kendisine bırakılmasını
  istedi. Gerçek kapanma hata yığını henüz alınmadı.

### Kalıcı destek uygulaması — 2026-10-22 (kuruluma hazır)

- Kullanıcı hazır sürüm koşulunu kaldırdı: yeşil/mor kalıcı iksir de oluşturuluyor.
  `72737` saldırı hızı +30, `72738` hareket hızı +40; toplam 14 destek, hepsi
  seviye 1. Eski süreli nesneler silinmiyor. Şebnem/iksir değerleri ayrı korunuyor.
- DB ve istemci yükleyicileri aynı `pvp_support_proto.h` politikasını uygular;
  eski kodlamalı/binary protolar değişmeden altı şebnemin sınırı 1 olur ve iki
  yeni iksir oluşturulur. İki header byte eşitliği kontrol edilmelidir.
- `USE_AFFECT_PLUS` yanlış Value1 indekslemesi düzeltildi. Kalıcı etkiler
  aktif envanter nesnesinden geri kurulur, yinelenen/orphan etkiler temizlenir.
  Ölüm temizliği mevcut 549/550 korumasını kullanır; bu iki tür süre tüketmez.
- Ayrı `permanent_support` quest'i yeni/eski karaktere nesne başına bir kez
  verir; boş yer yoksa sonraki login/levelup'ta devam eder. `welcome` eski
  süreli destekleri ve saç kostümünü artık vermez.
- İzole VM adayı: `/usr/metin2-support-20261022-190014`; son kaynaklarla game/db
  ve gerçek quest derlemesi/testi geçti. Web: 359 nesne, sıfır hata; patchcheck,
  Python başlangıç/import ve paket kontrolleri geçti. Corpus 1370 parça aynı.
  İstemci hash'leri `/home/m2web/dev/support-client.sha256` ile sabitlendi.
- `previous/` içinde canlı binary/quest/efsun tablosu yedeği hazır. **Canlı
  henüz değiştirilmedi.** AGENTS.md 49. satır gereği otomatik VM restart yok.
  Operatörün tek kurulum komutu ve doğrulama: `docs/KALICI_DESTEK_KURULUM.md`.
  Gerçek ölüm/dirilme/relogin kabulü kurulum sonrası yapılmalı.
- `char_item.cpp` / `char_affect.cpp` eski çoklu kodlamalı string baytları
  aynı derlenmiş baytları üreten üç haneli octal kaçışlarla yazıldı; yeni kod
  native edit aracıyla düzenlenebilir. Oyun metinleri yeniden kodlanmadı.

### Önceki sade ekipman tasarımı — 2026-10-22 (yukarıdaki uygulamayla güncellendi)

- Kullanıcı son kararı: standart ekipmana ek yalnız binek, gövde kostümü,
  silah kostümü ve çağrılan basit pet. Tılsım/saç ve diğer ek güç yuvaları kapalı.
  Önceki tılsım onayı geçersiz. Paket/enum değiştiren flag kapatılmayacak.
- Başlangıçtaki dört Ejderha Tanrı desteği + kritik/delici otuzluk yerine
  `72731–72736` birer adet; altı `50827–50832` şebnem de birer kalıcı nesne.
  Ölüm/login/kanal değişiminde aktiflik korunacak, tekrar kullanım katlamayacak.
- Proto incelemesi: hazır + ailesi var; şebnemler şu an level 55. Başlangıçta
  kullanım için level 1'e çekilecek. Mor/yeşil iksirin hazır perması bulunmadı;
  kullanıcının “varsa” koşulu nedeniyle yeni perma iksir bu kapsama eklenmedi.
- Kanıt: `USE_AFFECT_PLUS`, etki 549/550, ölümde korunan 500–599 aralığı.
  Uygulama öncesi `char_item.cpp` ön kontrolündeki Value1/Value0 ayrımı,
  60 yıllık süre sabiti, nesne/etki/kilit senkronu ve teslim tekilliği ele alınacak.
- O andaki durum: tasarım hazırdı, yeni davranışlar henüz uygulanmamıştı.
  `PVP_HEDEF.md` güncellendi; ayrıntı `docs/BASLANGIC_KALICI_DESTEK_TASARIMI.md`.

### Normal efsun dağılımı / sabit değerler — 2026-10-22

- Kullanıcı kararı: sekiz ekipmanın normal efsun izinleri klasik referansa;
  değerler sabit, HP 3000. Kostüm/tılsım da sabit değerleri kullanır, izinleri korunur.
- `seed_item_attr.sql` içinde 45 tür düzeltildi. 14 anomali satırı, 39 nadir satır,
  seçim ağırlıkları ve doğal ortalama/beceri üretimi korundu. Oyuncu eşyaları
  topluca değiştirilmez. Ayrıntı: `docs/EFSUN_NORMAL_DUZENLEME.md`.
- Mevcut DB için `content/server/sql/migrations/20261022_normal_attributes.sql`;
  bootstrap seed canlıda çalıştırılmaz. Yerel regresyon: 8/8 başarılı.
- MariaDB 10.11.19 üzerinde yalnız geçici tabloyla geçiş, tekrar uygulama ve
  eksik satırda durma testleri başarılı. Canlı normal tablonun 59 satırı önce/sonra
  aynı; 14 ertelenen satır ve 59 satırın ağırlık/ek yuva izinleri korunuyor.
- Durum: **repo hazır, canlıya uygulanmadı**. Canlı MariaDB sürümü 10.11.19,
  normal satır sayısı 59 salt okunur sorguyla görüldü. SQL sonrası mevcut
  `/reload p` akışı efsun tablolarını da core'lara taşır; `/reload a` taşımaz.
  Servis restartı / otomatik yayın yapılmadı.

### Tarayıcı küçülünce envanter / skill barının kırpılması — 2026-10-22

- Neden: taskbar `SCREEN_HEIGHT - 37`, envanter `SCREEN_WIDTH - 212` /
  `SCREEN_HEIGHT - 610` ile ilk yüklemede yerleşir. `OnSizeChange` C++ ekran
  ölçülerini değiştirir, fakat bu Python pencerelerinin yerleşimini yenilemez.
- Web'de mantıksal oyun masaüstü başlangıçta sabitlenir; canvas tarayıcının
  güncel alanına en-boy oranı korunarak sığdırılır ve ortalanır. Yeniden
  boyutlandırma, fullscreen ve visualViewport değişimleri aynı yolu kullanır.
  Yeni pencere oranında kenarlarda boşluk olabilir; HUD ekran dışına çıkmaz.
- Fare mevcut canvas rect'i / buffer / UI scale dönüşümünü kullanır; yeni
  canvas konumu ve ölçeğiyle eşleşmeye devam eder. Gizli sekmenin duraklatma
  davranışı ve mevcut render cap / UI scale seçimi korunur.
- Başlangıçta küçük tarayıcı için, render cap izin verdiği ölçüde en az
  800×640 mantıksal alan seçilir. C++ veya cp1254 pack kaynağı değiştirilmedi.
- Durum: **canlıda**, yapı `v=1792692377`. 22 Node, 4 Python testi,
  81/81 stage yaması, Python 3.13 açılışı ve protokol kontrolleri başarılı;
  28 aday/canlı dosyanın hash'i eşleşti. Corpus ve servisler değişmedi.
- Özel önizlemede 900×650, 600×650, 1200×300, 400×800 ve eski boyuta dönüş
  doğrulandı. Fare %90 noktasında aynı mantıksal koordinatları verdi.
  İlk açılış 400×300 olduğunda 800×640 mantıksal masaüstü 375×300 CSS alana
  sığdı. Public adreste 650×650 → 1200×300 → 1200×736 geçişlerinde mantıksal
  alan 1200×736 kaldı; canvas tamamı görünürdü, motor hata katmanı boştu.
  Envanter/taskbar ilk konumlarının sınır içinde kalması regresyon testiyle
  kontrol edildi; gerçek hesapla envanter açma testi henüz yapılmadı.
- Geri dönüş yedeği: `/home/m2web/backups/web-ux-qLXUVIvx/site`.

### Web giriş UX'i ve ilk ziyaret yüklemesi — 2026-10-22

- Durum: **canlıya yayınlandı ve public adreste boş önbellekle doğrulandı**.
- `runtime.js` Tab için eksik `WM_CHAR(9)` mesajını gönderir. HTML yardım
  kontrolleri ve tarayıcı Cmd/Ctrl kısayolları oyun tarafından yutulmaz.
- `compat/web_ux.js` manifestten giriş ekranının çalışma kümesini çıkarıp
  **asenkron** hazırlar; manifest ve bu parçalar hazır olmadan motor başlamaz.
  Mevcut corpus'ta 6 parça / 24 MiB; önce başlangıçta 61 parça / 239,4 MiB
  geliyordu. Corpus yerleşimi/hash'leri değişmedi. Boot/meta/motion, giriş
  isteğinde hazırlanır; Python auth bağlantısını RAM hazır olana kadar bekletir.
- Web hesap yuvaları yalnız kullanıcı adı saklar; şifreler saklanmaz.
  localStorage yazımı doğrulanmadan başarı mesajı verilmez. Kaydet/yükle/sil
  tooltip'leri ve Mac Fn/Globe, Tab/Enter, tarayıcı kısayolları yardımı eklendi.
  `compat/web_ux.py` sadece üretilen web LoginWindow'a bağlanır; cp1254 kaynak
  pack'leri değiştirilmez. Bridge dosyaları şifre içermez.
- Harita hazır kontrolü indirme geçmişi yerine anlık RAM'i denetler; gereken
  parçalar korunur. 60 saniye sonunda körlemesine senkron okumaya geçilmez;
  indirme hatası/yeniden deneme çubukta gösterilir.
- Yerel ve son container testleri: 19 Node, 4 Python; patchcheck 81/81;
  üretilmiş Python 3.13 açılış testi ve source protokol kontrolleri başarılı.
- Önizlemede kullanıcı adı → Tab → şifre gerçek tuşlarla doğrulandı.
  Kullanıcı adı localStorage yazma/silme doğrulaması geçti; hazırlık tamamlanana
  kadar auth bağlantısı açılmadı. Sahte hesapla beklenen giriş hatası alındı;
  bu akış boyunca senkron XHR 0. Corpus grup indeksi de 20 s süre sınırı ve
  yeniden denemeyle korunur.
- Son public yapı `v=1792689159`; 28 aday/canlı dosyanın hash'i eşleşti.
  Cache Storage boşaltıldı, HTTP cache kapatıldı ve SW atlandı: ilk ekran
  motor+dil+corpus transferi **303.386.639 → 85.878.887 bayt** (yaklaşık %71,7
  azalma). İlk ekranda RAM'de 8 parça / 32 MiB; bunun 6 parça / 24 MiB'ı
  zorunlu küme, kalanı mevcut C++ komşu-parça ön-yüklemesi. Senkron XHR 0;
  corpus/motor HTTP hatası 0. Eski `/favicon.ico` 404'ü bu kapsamda değişmedi.
  İlk motor hazırlığında 1.641 ms ana-thread görevi hâlâ var; ağ beklemesi
  kaldırıldı, bütün CPU/GPU hazırlama işi sıfırlanmış sayılmaz.
- Public adreste de gerçek Tab/Enter, asenkron 61-parça hazırlığı ve sahte
  hesapla beklenen auth hatası doğrulandı; hazırlık+auth boyunca senkron XHR 0.
  Kalan boot/meta/motion verisi silinmedi: kullanıcı giriş yaptığında hazırlanır.
  Gerçek hesapla harita/oynanış testi henüz yapılmadı.
- Yayın: `platform/deploy/release_web_ux_build.sh` + `release_web_ux_host.sh`.
  Geri dönüş yedeği `/home/m2web/backups/web-ux-7Pdnfdvm/site`.
  Aday WASM SHA-256:
  `8c9c66220c47e3b932f9be64e7e3a32a6795516f121ef22755a2c4396d779d36`.
  Engine-only yayın, 1370 değişmemiş corpus parçasını korur; CDN yüklemesi,
  VM veya production servis restart'ı gerektirmez.

### Askerî atta becerilerin sessizce engellenmesi — 2026-10-21

- Kullanıcı Sura, askerî at ve kılıç ile at becerilerinin animasyon bile
  başlatmadığını; kombonun çalıştığını doğruladı.
- `PythonPlayerSkill.cpp::__CanUseSkill` eski 107/109 yuvalarını binicilik
  sanıyordu. Yohara kapalı olduğundan 109 okunuyor; gerçek C++ destek
  tablosunda 109 = At Çağırma (131), seviyesi 10. Eski koşul 20 beklediği
  için tüm at üstü becerileri kullanım denetiminden önce reddediyordu.
- Web stage düzeltmesi bu eski genel kontrolü kaldırır. Actor, observer,
  beceriye özel at/silah, güvenli alan, SP ve sunucu yetki kontrolleri korunur.
  cp1254 kaynak dosyası dönüştürülmedi; Windows kaynak düzeltmesi açık kalır.
  Sura için yay gerektiren Ok Sağanağı kısıtlaması değiştirilmedi.
- Regresyon testi gerçek C++ fonksiyonunu önce/sonra derleyip mevcut
  109 = 131 eşlemesini ve 10 seviyelik çağırma ile eski ret/yeni geçişi
  doğrular; observer modunda, actorsüz veya kullanım kilitli durumda ret verir.
- **Canlı:** `release_horse_skills.sh` ile derlendi ve sürüm `1792614571`
  yayımlandı. Patchcheck 81/81; link `UNEXPECTED: none`; gerçek Python 3.13
  açılış testi geçti. 28 aday/canlı dosyanın hash'i eşleşti. Public HTML,
  JS, WASM ve preload HTTP 200; public WASM SHA-256
  `8c9c66220c47e3b932f9be64e7e3a32a6795516f121ef22755a2c4396d779d36`.
  Yedek `/home/m2web/backups/text-encoding-gp13cKLh/site`.
- Corpus değişmedi; CDN yüklemesi ve servis restartı yapılmadı.
  `M2W_PUBLIC_CANDIDATE=1` yalnız önizleme bridge config üretimini atlar;
  aday dosyalar yayın karşılaştırması için saklanır. Özel önizlemenin
  18731/18732 portları kapalı doğrulandı. Oyun içi doğrulama kullanıcıda.

### Oyun verileri 60/61 çubuğu: sonlanmayan ön yükleme — 2026-10-21

- Kullanıcı oyun çalışırken yalnız `Oyun verileri 60/61 (75 diskten)`
  çubuğunun kaldığını doğruladı. Bu bir oyun/ana döngü donması değildi.
- Başlangıç grupları meta 17 + motion 19 + boot 25 = 61 farklı chunk.
  Public uçta 61 HEAD isteğinin tamamı HTTP 200; her gruptan birer tam
  4 MB chunk GET ile indirildi ve adındaki SHA-256 önekiyle eşleşti.
  Kalıcı eksik/engelli Cloudflare dosyası bulunmadı. HEAD yanıtında
  Content-Length olmaması boş dosya olarak yorumlanmadı. Kullanıcının
  önceki isteğinin tam hata sebebi bu incelemede yakalanmadı.
- İstemcide yeniden üretilebilir açıklar bulundu: başarısız prefetch tekrar
  kuyruğa alınmıyordu; ağ/cache isteğinin süre sınırı yoktu; başka bir
  background isteğinde görülen chunk kuyruktan düşüyordu ve o istek
  başarısızsa tamamlanamıyordu. Background başarıları da fetched set'inde
  tutulmadığından bellekten atılınca ilerleme kaybolabiliyordu.
- Ortak `loadChunk` cache açılışı/okumasına 2 s, tüm HTTP gövdesine 20 s
  sınır koyar. Bozuk/okunamayan cache ağdan denenir; başarısız cache yazımı
  indirme slotunu tutmaz. Prefetch en fazla üç deneme yapar; başarısızlık
  kalırsa açık hata ve `Tekrar dene` düğmesi gösterir. Slot/bellek rezervi
  her sonuçta bırakılır; başka isteğin kuyruğu kaybolmaz.
- Çubuktaki disk sayısı artık yalnız başlangıç grubundaki farklı başarılı
  chunk'ları sayar. Harita grubunun disk okumaları 61 toplamına karışmaz.
- Dokuz Node regresyon testi: geçici/kalıcı hata, takılan HTTP gövdesi,
  cache open/read, boş cache, reddedilen cache yazımı, ortak background
  isteği, eviction ve hata/yeniden deneme arayüzü. Yerelde ve public
  package kapısında 9/9 geçti; gerçek Python 3.13 açılış testi de geçti.
- **Canlı:** sürüm `1792614094`; 28 dosya aday/canlı hash eşleşmesi,
  public JS/preload HTTP 200 ve hash doğrulaması. Yedek:
  `/home/m2web/backups/text-encoding-jIjWJkUb/site`. Yalnız JS/ön yükleme
  değişti; WASM `7bd48809...`, corpus, Cloudflare ayarları ve servisler aynı.
  Özel önizleme kapalı kaldı. Yeni davranış için açık oyun sayfası yenilenmeli.

### Canlı açılış hatası: collections/JSON import onarımı — 2026-10-21

- Kullanıcı ilk metin yayınının `RunMain Error` ile açılmadığını bildirdi.
  Önce `/home/m2web/backups/text-encoding-7pcQ09rg/site` geri yüklendi;
  önceki `8bc22aa3...` motor/site eşleşmeleri doğrulandı. Servis restartı yok.
- Kök neden: root pack'teki Python 2 `collections.py`, Python 3'ün
  `collections` paketini gölgeliyordu. Ayrıca pack import kancası
  `from json import scanner` gibi paket içi fromlist importlarında cache'deki
  üst modülü erken döndürüyordu. JSON'u erken yükleyen yeni çözücü bu iki
  eski uyumsuzluğu açılışta tetikledi; traceback import'u da asıl hatayı örttü.
- Data üretimi root `collections.py` dosyasını artık kopyalamaz. Import
  kancası `collections`, dotted/relative importlar ve `__path__` taşıyan
  gerçek paketleri CPython'a bırakır. Oyun modüllerinin pack yolu korunur.
- `test_python_startup.py`, gerçek dönüştürülmüş `system.py` import kancasını
  temiz `-I -S` oturumunda çalıştırır: pack'te eski collections varmış gibi
  davranırken textcodec/JSON/collections.abc/traceback ve oyun fixture'ı
  birlikte yüklenir; asıl istisnanın gösterilebildiği de doğrulanır.
  31 yerel test ve container'daki gerçek Python 3.13 testi başarılı.
- `build_text_startup.sh` özel önizleme açmadan betikleri yeniler. Yayın
  betiği artık bu açılış testini zorunlu çalıştırır ve pakette eski
  collections dosyasının bulunmadığını denetler.
- **Düzeltilmiş canlı yayın:** yedek
  `/home/m2web/backups/text-encoding-DQsglLWg/site`; 28 aday/canlı dosya
  hash'i eşleşti. Public sürüm `1792612335`. İnternetten alınan HTML/JS/data
  HTTP 200; JS SHA-256 `0f4a2b021e7f8388f8bdc77c99a4395723de2c733d941ae0d54f1b60a3a7399e`,
  data `e5781e078539835689cfc26b752a7e50c0b3c067662c9b8579594630a9e7fa68`.
  WASM değişmedi (`7bd48809...`); corpus aynı, CDN yüklemesi yok.
- Özel önizleme kapalı kaldı; localhost 18731 yanıt vermiyor. Kullanıcı
  tarayıcı/oyun kabulünü yapacak; HTTP/hash testi görsel oyun kabulü değildir.

### Metin kodlama geçişi: ilk web paketi — 2026-10-21

- Savaş bileti örneğinin kaynağı doğrulandı: üretilen `uiMiniMap.py` UTF-8
  doğruydu; `pack.Get` dosyayı cp1254 çözüp Python `compile()` öncesinde
  `SavaÅŸ` / `Ãœcretsiz` biçiminde bozuyordu. Dosya kodlaması görüntüleme
  kod sayfasından ayrıldı; ağ protokolü aynı kaldı.
- Ortak `compat/textcodec.py` ve `text_encoding.json`: UTF-8 üretilen betikler,
  cp1254 Türkçe ve UTF-8 diğer 10 dilin 22 ana tablosu. Kayıtlı metin hatalıysa
  kaynak/offset ile durur. Henüz taşınmayan eski `.txt` dosyaları önceki
  kod sayfası/replace davranışını açık geçiş kuralıyla korur.
- `.py` native hızlı yolu decoder import etmez. İlk önizlemede görülen
  `json → collections → pack.Get` bootstrap döngüsü giderildi; native
  C++/CPython testi bu yükleme sırasını kapsar. Son WASM/data tekrar derlendi.
- Locale yükleyicileri ortak satır ayrıştırıcısına geçti: son satırda LF yoksa
  `line[:-1]` yüzünden harf silinmez. LF/CRLF/BOM ve eski coding başlıklarının
  UTF-8 üretimle uyumu testli. Kaynak cp1254/CRLF dosyaları topluca çevrilmedi.
- Savaş bileti başlığı/Ücretsiz/Premium artık anahtar; `text_labels.json`
  11 dilde karşılık verir. Web semantic patch'leri yalnız Python 3 çıktısını
  değiştirir. Sunucu ve Windows yolu sonraki kapsamda.
- Salt okunur `tools/audit_text_encoding.py` ilk envanteri çıkarır: 22 tabloda
  kodlama hatası/U+FFFD yok; 654 yinelenen satır ve dil başına çok sayıda
  eksik anahtar mevcut. Bunlar otomatik düzeltilmedi. Data build gerçek
  girdilerde kodlamayı/yeni çeviri anahtarlarını kontrol eder; hata varsa
  önceki data çıktısını silmeden durur.
- İlk 29 araç testi, 80/80 stage yaması, WASM engine, protokol/RESP,
  data/link başarılı. Repo ve `/home/m2web/kit` değişiklikleri eşitlendi.
- Kullanıcı canlı yayın ve özel önizlemenin kapanmasını istedi. İlk yayın
  kontrolü public package yeniden link edildiğinde hash farkıyla durdu;
  canlı dosyalar değişmedi. Neden: cache'deki `main_web.o` / `link_data.o`
  ilk linkte sona eklenirken sonraki linkte genel listeden başka sırayla
  giriyordu. `collect_objects` bu ikisini artık hariç tutar; `compile_entry`
  her seferinde sona ekler. Ek regresyon testi ve yeniden link başarılı;
  public paket ile önizleme motoru artık birebir aynı. Son araç testi toplamı
  30/30 başarılı; diff whitespace kontrolü temiz.
- **Canlı:** `platform/deploy/publish_text_encoding.sh` ile yedekli yayın
  tamamlandı. Önceki site: `/home/m2web/backups/text-encoding-7pcQ09rg/site`.
  28 public dosyanın aday/canlı hash'i eşleşti; WASM SHA-256
  `7bd48809cd6e2f6dc266193df9ae42bf833e1523473acdbe06dfa170298d10e7`.
  1370 immutable corpus chunk aynı; CDN yüklemesi ve servis restartı yok.
- Public HTML ve sürümlü WASM HTTP 200; HTML `no-cache`, sürüm `1792611852`.
  İnternetten indirilen WASM hash'i de aynı. Public HTML'de preview ayarı yok.
- Özel HTTP önizlemesi, dev bridge ve yerel SSH tüneli kapatıldı;
  localhost 18731 artık yanıt vermiyor. Kullanıcı tarayıcı/oyun doğrulamasını
  kendisi yapacak. Ayrıntı ve sonraki kapsam: `docs/METIN_KODLAMA_PLANI.md`.

### Sınırsız metin dedektörü gerçek canlı onarımı — 2026-10-21

- Kullanıcı başlangıç dedektörünün bittiğini bildirdi. Canlı derlenmiş welcome
  gerçekten 27989 veriyor. Repodaki `item.cpp` SetSocket koruması ve
  `mid_pvp_detector.h` 1022da374'ten beri var; ancak canlı item.cpp hash'i eski
  d23c6f2f9 ile eşleşti ve header yoktu. Kaynakta var demek canlıda var demek değildi.
- Mevcut koruma yalnız 27989'un socket0 sayacını 0 tutar; 76006 ve diğer
  socket/eşyalar aynı. Bu iki gerçek kaynak game derlemesine dahil edilir.
- Destek görevi, ilk-login hediyelerinden sonraki döngüde eksik dedektörü bir
  kez tamamlar. Elde varsa çoğaltmaz; dolu çantada işaret koymadan tekrar dener.
  Kullanılmış ama silinmemiş dedektör ilk kullanımda yeni sınırsız kurala geçer.
- Sunucu kaynak yayını ortak `server-update` yoluna bağlandı. `--server-baseline`
  açıkça eski canlı kaynak sürümünü doğrular. Her seçili CPP `gmake -W` ile
  zorunlu derlenir; eski dosya mtime'ı yüzünden cached objenin kalması engellenir.
  `--detector` yalnız bu iki kaynak/binary ve starter_support namespace'ini taşır.
  Diğer oyun ayarları, SQL ve başlangıç hediyeleri korunur. Oyun testi kullanıcıda.
- Canlı sürüm `20261021-114558`: gerçek game ve qc derlemeleri tamamlandı;
  kaynak/binary/quest aday eşleşmeleri ve altı süreç/port doğrulandı. Eski
  kaynak/binary `previous-game` / `previous-server-src`, görevler `previous.tar`
  içinde; VM `/usr/metin2-progression-20261021-114558`.

### Harita Yang tabanları 2× — 2026-10-21

- Kullanıcı mevcut harita Yang miktarlarını ikiye katlamamızı istedi. Aynı
  17 haritanın normal yaratık/metin min/max değerlerinin tamamı 2× yapıldı.
  Metinsiz örümcek/sürgün girdileri 0 kalır; yeni harita veya kaynak eklenmez.
- Eski 400.000 tavanında Kızıl Orman ve diğer yüksek metin artışı kırpılacağı
  için yalnız harita tabanlı ödemelerde tavan 800.000 oldu. Boss ve kapsam
  dışındaki ödemeler eski 400.000 tavanını korur. Normal ödeme, para patlaması
  parça sınırları ve toplam kaydı aynı seçilmiş tavanı kullanır.
- Global miktar flagleri 400; olasılık/seviye farkı, kişisel bonuslar, NPC
  fiyatları, droplar ve diğer sistemler aynı. Hedef ve rehberler güncellendi.
  Yayın yolu `--map-yang`; ayrı kopyada game derlemesi, kaynak/binary/flag
  değişiklik koruması ve önceki kaynak/binary yedeği. Oyun testi kullanıcıda.
- Canlı sürüm `20261021-113900`: game derlemesi başarılı; kaynaklar ve binary
  adayla birebir eşleşti, altı süreç/port sağlıklı. Önceki dosyalar aynı VM
  sürüm dizininde `previous-game` ve `previous-server-src` içinde.

### Silahçı/zırhçı tek sayfa — 2026-10-21

- Kullanıcı gizli sekmeleri ve ara seviyeleri istemedi. Silahlar yalnız
  başlangıç/15/30 +9; zırhlar başlangıç/34/48 +9. İstenen 49 aile seviyesi
  gerçek protoda 48. Başlangıçların proto sınırı 0; ilk seviyede kullanılabilir.
  Kask/kalkan/takıların azaltılmış seçkisi kullanıcı tarafından ayrıca onaylandı.
- Silahçı: beş başlangıç ailesi, altı 15 ve altı 30 ailesi, 200 normal ok.
  Başlangıç çanı yok; 15 hançeri gerçek 4019, önceki 1019 ise 10 seviyedir.
  Zırhçı: 12 gövde, dört 21 kaskı ve Beşgen Kalkan, sekiz takı/ayakkabı.
  Ana/ikinci köy aynı seçkide ve her NPC tek sayfa. Market 17 ürünüyle aynı.
- Gerçek DB item_vnum sırasındaki yerleşim: silahçı 18 ürün/30 hücre,
  zırhçı 25 ürün/37 hücre. Toplam beş sayfa/103 ürün. +9, doğal ortalama
  üretimi ve geri satıştan yüksek fiyat ilkeleri korunur.
- Sabit sahip olunan 13 shop kimliğiyle eski sekmeler SQL'den temizlenir;
  doğrulama sorgusu emekli sekmeleri de tarar. Böylece yalnız yeni beş kaydı
  kontrol edip eski gizli sekmeleri yanlışlıkla canlı bırakmaz.
  Tam/onarım SQL, fresh seed ve oyuncu stok rehberi tek kaynaktan yenilendi.
  Yayın `--npc-stock`; görev/binary/istemci/drop/Yang değişikliği yok.
- Canlı sürüm `20261021-085048`: beş sayfa/103 ürün kurulum içinde tüm
  fiyat/adet/efsun/soketleriyle birebir doğrulandı; altı süreç/port sağlıklı.
  Önceki 13 sayfa/169 ürün aynı VM sürüm dizininde `previous-database.sql`
  içinde. Oyun içi pencere/satın alma testi kullanıcıda.

### Harita bazlı Yang tabanları — 2026-10-21

- Kullanıcı harita bazlı normal yaratık/metin aralıklarını onayladı; kesin tablo
  `PVP_HEDEF.md` Harita bazlı Yang bölümünde. Canlı mob proto hash'i repo ile
  aynı; 1–99 normal rank kayıtlarının 743/771'inde MaxGold=0. Global iki miktar
  flag'i gerçekten 400, ancak sıfır proto tabanı bu artıştan yararlanmıyordu.
- `mid_pvp_yang.h` 17 haritayı kapsar. Ölümün gerçekleştiği harita kullanılır;
  özel indeksler ana haritaya indirgenir. 1–99 normal mob/metinler hedef tabandan
  ödeme alır. Boss/king ve diğer kaynaklar eski hesapta kalır. Şans/seviye cezası,
  kişisel ve nadir bonuslar, 400.000 toplam tavanı korunur.
- Onaylı rakamlar mevcut flag=400'de doğrudan temel ödemedir; %50 × %400
  ikinci kez uygulanmaz. Miktar flag'i daha sonra değiştirilirse 400'e göre
  ölçeklenir. Para patlaması/normal ödeme yolları aynı tabanı kullanır.
- Legacy `char_battle.cpp` düzenlenebilir UTF-8'e taşındı; eski C++ metin/karakter
  literal byte'ları octal escape ile aynen korundu. Statik literal karşılaştırması
  birebir eşleşti. İstemci/packet/proto/SQL değişikliği yok.
- `--map-yang` yalnız sahip olunan iki sunucu kaynağını ayrı kopyada derler;
  canlı kaynak/binary/flag değişikliği engellenir. Kaynak ve önceki binary
  yedeklenir, servisler durduktan sonra kurulur; hata halinde geri dönülür.
  Oyun testi kullanıcıda.

- Canlı sürüm `20261021-081923`: ayrı kopyada gerçek FreeBSD game derlemesi
  başarılı; iki kaynak ve binary kurulum sonrası adayla birebir eşleşti.
  Altı süreç/port sağlıklı. Önceki binary `previous-game`, önceki kaynaklar
  `previous-server-src` içinde; VM `/usr/metin2-progression-20261021-081923`.

### Market: büyük boy otomatik HP/SP özütleri — 2026-10-21

- Kullanıcı markette büyük boy Güneş/Ay Özütü istedi. Gerçek proto ve sunucu
  sabitleri doğrulandı: 72725 Güneş (7.000.000 HP), 72729 Ay (700.000 SP).
  Her satın alım 1 adet, tanesi 100.000 Yang. Item manager yeni eşyada socket2'ye
  dolu kapasiteyi atar; mevcut ShopEx sıfır soket şablonu bunu silmez.
- Tek stok kaynağı `npc_profile.py stock()` güncellendi; tam/onarım SQL'leri,
  fresh seed ve stok rehberi aynı profilden yenilendi. 13 sekme/169 ürün;
  mevcut 167 ürünün fiyat/adet ve NPC eşleşmeleri aynı kalır.
- `--npc-stock`, yalnız aktif SQL profilini kurar; görev/binary/istemci taşınmaz.
  Önce canlı eski stok 13/167 birebir doğrulandı. Hazırlık/kurulum arası DB
  değişikliği engellenir, sahip olunan 13 mağaza yedeklenir. SQL kurulduktan sonra
  tüm satırlar kaynakla eşleşmeden sunucu başlatılmaz; hata halinde geri dönülür.
  Oyun testi kullanıcıda.
- Canlı kurulum `20261021-080602` tamamlandı. Kurulum içinde 13 sekme/169
  ürün tüm fiyat/adet/efsun/soketleriyle doğrulandı; altı süreç/port sağlıklı.
  Önceki SQL aynı VM sürüm dizininde `previous-database.sql` içinde.

### Büyülü Metal metin dropları — 2026-10-21

- Kullanıcı ilk etapta 55–60 metinlere %5, 65–75'e %8, 80–90'a %12
  temel oranla birer Büyülü Metal (25041) eklenmesini onayladı. Karakter
  seviyesi değil metin seviyesi esas alınır. 400 ölçeğinde ham değerler 20/32/48.
- Önce `PVP_HEDEF.md` kilidi ve loot politikası v6 güncellendi.
  `metin_metal.py` yalnız mevcut klasik `MetinLv*` gruplarını işler;
  metin kimliği/seviyesi gerçek proto ile doğrulanır. 12 grup kapsamda.
  Boss/sandık ödülleri, diğer droplar ve harita doğma ayarları korunur.
- Rehber gerçek runtime tablosundan yenilenir. `--metin-metal` yayın modu
  yalnız `mob_drop_item.txt` taşır; önceki canlı dosya hash'i `4f0c9a16b`
  üzerinden korunur. Derleme/istemci paketi gerekmez; oyun testi kullanıcıda.
- Canlı kurulum `20261021-073648` tamamlandı. Aday/canlı dosya birebir aynı;
  SHA256 `70e6f344d1ad93aabce6140774380872c3942f0caf972bd302e73fdec102b7ae`.
  Altı süreç/port sağlıklı. Önceki dosya aynı VM sürüm dizininde `previous.tar`
  içinde. Statik karşılaştırmada yalnız 12 metin grubu değişti, diğer 79 grup aynı.

### Aktif mağaza yolu ve destek becerisi onarımı — 2026-10-21

- Kullanıcı 5. seviyede destek/at becerilerinin gelmediğini ve silahçı/zırhçının
  açılmadığını bildirdi; eski yapıları kaldırmamızı istedi. Önceki yayında
  dosya/süreç kontrolü geçti, fakat bu mağazaların çalıştığı kanıtlanmış değildi.
- Kök neden: açık `ENABLE_RENEWAL_SHOPEX`, DB `shopex` / `shopex_item` okuyor;
  dosya okuyucusuna girmiyor. Bu tablolar boşken eski standart kayıtlar silinmişti.
  `npc_profile.py stock()` artık aktif SQL stoklarını üretir. Metin mağazası,
  eski +9/trim SQL girişleri ve tek seferlik NPC yayın betikleri kaldırıldı.
  Fresh seed de eski stokları kurup silmek yerine aynı aktif 13 sekme/167 ürünü içerir.
- Beceri görevi login ve levelup'ta doğrudan çalışır; gerçek `loop_timer` kullanır.
  Standart/at becerileri 5. seviyede açılır; ana beceriler BK/G/P kalır.
  Önceden teslim işareti olan karakterlerde eksik at seviyesi de 30'a onarılır.
- Aktif ShopEx satın alma kodu boş SQL efsun şablonuyla doğal ortalama/beceri
  zararını siliyordu. Doğal addon korunur; normal ekipman boş, açık SQL şablonu
  öncelikli kalır. Paket/protokol değişmez; istemciyi tekrar yayımlamak gerekmez.
- Kurulum `progression_release.py --npc-profile`: gerçek qc ve ayrı kopyada game
  derlemesi, kaynak/binary/SQL hash koruması, yalnız sahip olunan tabloların yedeği,
  eski dosyanın kaldırılması ve hata halinde geri dönüş. Diğer NPC'ler korunur.
  `npc_profile_verify.py` canlı satırların fiyat/adet/efsun/soketleriyle tamamını
  kanonik kaynakla karşılaştırır. Oyun testi kullanıcıda.
- Canlı sürüm `20261021-072726`: gerçek qc ve game derlemesi tamamlandı;
  dosya/binary ve altı süreç/port kontrolü geçti. Salt okunur DB karşılaştırması
  13 sekme/167 ürünün tüm alanlarını birebir doğruladı; standart shop çakışması yok.
  Yedekler aynı VM sürüm dizininde. İşletim rehberi: `docs/NPC_KURULUMU.md`.

### NPC, kalıcı at/standart beceriler, Yang ve APPLY düzeltmesi — 2026-10-20

- Kullanıcı araştırılan mağazaların uygulanıp bütün işlerin canlıya alınmasını
  istedi. Kesin ek karar: 30 seviye altı klasik silah ailesi NPC +9, aynı
  ailelerin +0…+9 sürümleri metinlerden çıkarılır. Ana beceriler BK/G/P olarak
  kalır; yalnız standart/at becerileri maksimum. Kalıcı saldırabilen at da istenir.
- `npc_profile.py` gerçek protodan 13 ShopEx sekmesi üretir: ana/ikinci köy
  silahçı ve zırhçıları, ayrı market. Ekipman 2×, sarf en az 1,25× geri satış
  bedeli; fiyat alt sınırları vardır. Eski NPC satışında ShopBuyPrice bölünmediği
  için yalnız liste/proto satış fiyatına güvenmek satın al/sat döngüsü yaratabilir.
  Her sekmenin yerleşimi 40 paket hücresi içinde hesaplandı. Diğer NPC'ler aynı.
- `starter_support`: yeni/eski karaktere kalıcı seviye 30 askeri at ve 50053
  çağırma kitabı; sınıf seçimi sonrası destek/at becerileri. Ana becerilere
  dokunulmaz. Beş saniyelik kontrol sınıf sıfırlamasından sonra da eksikleri kapatır.
- Yang: `mob_gold` ve `mob_gold_buyer` 400. Temel %50 ve 400.000 kill tavanı
  aynı; tavan altında önceki miktarın 4 katı. Şans/seviye cezası ve proto'su
  sıfır olan sıradan mob'lar aynı. Metin 30/50/70/90 ödeme tabanı
  10.000/16.000/22.000/28.000; ±%20 ve diğer çarpanlar ayrı.
- Dolunay görünümü: sunucu 119 PvM ortalaması, eski istemci 119 metin bonusu.
  İstemci 92 sonrası APPLY değerleri sunucuyla hizalandı; aynı protokolde
  121 ortak isimde numara farkı kalmadığı preprocessor üzerinden doğrulandı.
  Paket/feature flag değiştirilmedi. Asıl metin bonusu sunucuda 112.
  Mevcut PvM ortalama saldırı formülü veya oyuncu efsunları topluca değiştirilmedi.
- **20261020-172132 canlı:** VM gerçek qc derlemesi, kaynak/nesne ve scoped SQL
  kuruldu; ardından engine-only istemci yayını. Host/VM `INSTALLED`; altı süreç
  ve altı port sağlıklı, site dosyaları paketle aynı. 1370 corpus chunk aynı,
  CDN yükleme gerekmiyor. Host `/home/m2web/progression-20261020-172132`, VM
  `/usr/metin2-progression-20261020-172132`; `previous.tar`, `previous-database.sql`
  ve host `previous-client` yedekleri var. İlk 172047 hazırlığı FreeBSD sh iç içe
  tırnak sözdiziminde canlı değişmeden durdu; düzeltilip yeni sürüm hazırlandı.
- Efsun rehberi 59 normal satırın canlıyla tüm değer/izinlerinin eşleşmesine
  dayanır; 39 rare satırı ayrı gösterir. Klasik dışı yuva izinleri ve normal
  havuzdaki ortalama/beceri/sınıf bonusları ayrıca işaretlendi; toplu silme yok.
  Belgeler: `EFSUN_REHBERI.md`, `NPC_CANLI_STOK.md`, güncel loot v5 rehberi.
- **20261020-172626 canlı ek düzeltme:** yalnız starter_support namespace'i
  tekrar derlendi/kuruldu. Envanter doluysa at kitabı teslimi bekleyebilir;
  standart beceriler artık bu beklemeden bağımsız açılır. SQL ve istemci aynı.
  Host/VM `progression-20261020-172626`; altı süreç/port sağlıklı.
- Oyun testi yapılmadı. İstemci ve qc derlemesi, derlemenin protokol düzeni
  denetimleri, statik veri/enum eşleştirmesi ve yayın dosyası/servis kontrolleri
  yapıldı; oyun kabulü kullanıcıda.

### NPC araştırması ve başlangıç yüzüğü — 2026-10-20

- Kullanıcı eksik kapsamı belirtti: araştırma silahçı ve gövde zırhlarını da
  kapsayacak şekilde tamamlandı. Canlı shop 1/6 stokları ve bütün ekipman
  seviyeleri protodan doğrulandı. Belgede altı silah ailesi, dört sınıfın
  18–61 zırh matrisi, kask/kalkan, takılar ve 40 hücre sınırı ayrı ele alındı.
  Öneri tavanları normal silah 25, gövde 42, takı 33; henüz tasarım kilidine
  uygulanmadı. Bu ek çalışma yalnız belge; mağaza SQL'i ve canlı stok aynı.

- Zırhçı/market ayrı incelendi. Canlı 9002/shop2 19, 9003/shop3 9 satır;
  9008/shop7'de ek erken ekipman var. `docs/NPC_MAGAZA_TASARIMI.md` görsel
  referans, doğrudan PvP mağaza kaynakları ve ayrı içerik önerilerini toplar.
  Yeni shop içeriği/fiyatı henüz uygulanmadı; Abanoz/Yeşim tavanı öneridir.
- 40004 `move_ring` canlı derlenmişti; başlangıç teslimi yoktu. Ayrı
  `starter_ring` yeni ve mevcut karakterlerde bir defa teslim eder; mevcut
  yüzüğü çoğaltmaz, envanter doluysa Satıcı konuşması veya sonraki girişe kalır.
  `welcome` ekipmanı tekrar verilmez; yüzük menüsü ve zindan koşulları aynı.
- **20261020-165717 canlı:** yalnız quest_list + yeni görev ve derlenmiş
  namespace. Host `/home/m2web/progression-20261020-165717`, VM
  `/usr/metin2-progression-20261020-165717`; previous.tar ve hash kayıtları var.
  Gerçek VM qc derlemesi, dosya eşleşmesi, altı süreç/port sağlıklı. Oyun testi
  yapılmadı. Client/engine/corpus ve mağaza SQL'i değişmedi.

### CANLI klasik zincirler ve loot v4 — 2026-10-20

- Kullanıcı araştırmanın ardından doğrudan canlıya alınmasını istedi. Tasarım
  önce `PVP_HEDEF.md`'ye işlendi: günlük kota yok; 13 boss sandığı garantili,
  General/Komutan 3 Kıvrık, Lusifer 2 kafa, Kraliçe 1 zehir, normal örümceklerin
  üretim malzemeleri %25, uygun kaynaklardan 1 Kan Taşı garantili. Bunlar mevcut
  `Type limit` yoluyla seviye cezasından ayrıldı; diğer ekipman/metin politikası aynı.
- `quest_tr/_midpvp` aktif kaynakları: kule tamamlama kaydı, 75 seviye Katakomb ve
  tek kafa tüketimi, 50 seviye Uriel hazırlığı/%100 üretimi, Baron–Flüt–Barones,
  atomik parti doğrulaması ve kişi başına tek giriş maliyeti. Dört ana zindanın
  başarı cooldown'u 10 dakika. Mevcut katlar ve reentry kancaları korundu.
- **20261020-153340 canlı:** VM'nin gerçek qc derleyicisiyle beş görev derlendi,
  eski beş namespace temizlenerek yeni 102 derlenmiş dosya kuruldu. Aynı çıktılar
  repoya byte olarak eşlendi; qc'nin token sonu boşlukları yalnız generated object
  yolu için Git whitespace denetiminden ayrıldı. Host `/home/m2web/progression-20261020-153340`, VM
  `/usr/metin2-progression-20261020-153340`.
- **20261020-153638 canlı:** Kraliçe'nin grup 2019 doğuşu 15400 → 900 saniye,
  Sürgün 2 Komutan doğuşu 1200 → 900 saniye. Yer/adet aynı; yalnız iki boss.txt.
  Host/VM aynı `progression-20261020-153638` adını taşır.
- Hazırlıkta canlı quest_list'in yalnız opsiyonel `mid_pvp_rewards.lua` kaydının
  yokluğu ile repodan ayrıldığı görüldü. Bu seçim korundu, ilgisiz ödül açılmadı.
  İlk hash koruması ve sonra qc'nin eski 644 izinli kopyası kurulum başlamadan
  hazırlığı durdurdu; yalnız hazırlık qc kopyası 700 yapılıp derleme tamamlandı.
- Her iki kurulumda VM/host `INSTALLED`, önceki dosyalar `previous.tar` içinde.
  Dosya/hash eşleşmesi, altı süreç ve altı port sağlıklı. Oyun/regresyon testi
  çalıştırılmadı; qc derlemesi gerekli yayın adımıydı. Engine, client ve corpus aynı.
- Açıklamalar: `docs/MID_PVP_FAZ3_ZINCIR.md`, güncel `docs/DROP_REHBERI.md` v4.
  Önceki wiki denetimi uygulama öncesi durum olarak işaretlendi. Faz 3'ün tüm
  izleme/instance kabul maddeleri tamamlanmış sayılmadı; oyun kabulü kullanıcıda.

### Klasik ilerleme zinciri wiki denetimi — 2026-10-20

- Kullanıcı bossları yalnız sandık içeriğiyle değil sonraki içeriği açan
  kaynaklarıyla ele almamızı istedi. Resmî wiki'nin eşya, görev, NPC ve zindan
  sayfaları repo drop/proto/quest/üretim akışıyla karşılaştırıldı.
- Sonuç: `docs/FAZ3_KLASIK_ZINCIR_DENETIMI.md`. General → Kıvrık → Beran hattı
  mevcut; Lusifer kafası yok. Katakomb giriş yolları farklı tüketim yapıyor,
  bazıları iki kafa istiyor. Barones anahtar üretimi ve Kraliçe zehri kaynağı yok;
  normal örümceklerin malzeme proto bağları var ama `etc_drop_item.txt` boş.
  Zindan doğrudan Barones çıkarıyor; Baron–Flüt aşaması yok.
- Biyolog sistemi C++ içinde mevcut; quest listesinde dosyası olmaması yokluğu
  anlamına gelmiyor. BK/G/P ve at hattı da rapordaki yan ilerleme kapsamına alındı.
- Seviye cezası ayrı: normal item rate ve ek bonus yokken 99 oyuncunun 78 Lusifer
  sandığı baz %100'den yaklaşık %1'e iner. Bossun ödülü ile zorunlu giriş
  malzemesinin erişimi ayrı politika gerektiriyor.
- Kullanıcı açıkça orta-kolay tekrarlı farm istedi: güncel wiki'nin günlük giriş
  kotası/EP bileti kopyalanmaz. Bu karar `PVP_HEDEF.md`'ye yazıldı.
- Bu tur yalnız araştırma/tasarım belgeleri değişti. Canlı drop, quest, cooldown
  veya günlük hak güncellenmedi; servis yeniden başlatılmadı, oyun testi yok.

### Her oyuncuya dört envanter sayfası — 2026-10-20

- Kullanıcı mevcut ve yeni tüm karakterlerde dört standart envanter sayfası
  istedi. Sunucu/istemci zaten 4 sayfa / 180 hücre destekliyor; son iki sayfa
  `inventory_0` açılmış satır sayısı ile kilitli. Tam açılım değeri 18.
- Canlı salt okunur inceleme: beş karakterin tamamı 0; kolon varsayılanı 0.
  Yeni karakter INSERT'i bu kolonu belirtmediğinden DB varsayılanı uygulanır.
- Tasarım kilidi ve `player.sql` varsayılanı güncellendi. Migration mevcut
  karakterlere 18 verir ve varsayılanı 18 yapar. Özel envanter alanları aynı.
- Bakım: `python3 platform/deploy/inventory_defaults_release.py`; game/db
  durduktan sonra mevcut değerler yedeklenir, migration uygulanır ve servisler
  açılır. Dosya hash'i ve süreç/port koşulları kontrol edilir. Engine/protokol
  değişikliği, client build ve oyun/regresyon testi yok.
- **Canlı:** `20261020-142312` kuruldu. Beş mevcut karakterin tamamında
  `inventory_0 = 18`, kolon varsayılanı 18. Altı süreç ve altı port sağlıklı.
  Host `/home/m2web/inventory-20261020-142312`, VM/yedekler
  `/usr/metin2-inventory-20261020-142312` (`rollback.sql`,
  `previous-default.txt`). İki uçta `INSTALLED`. Oyun testi kullanıcıda.
- Hazırlık sırasında iki bakım sorunu düzeltildi: `bash -s` içindeki SSH
  stdin'i tüketebildiğinden iç SSH çağrıları `-n` kullanıyor; başarı ayrıca VM
  `INSTALLED` kaydıyla doğrulanıyor. İlk deneme (`20261020-141958`) yalnız boş
  sürüm dizinleri oluşturdu, DB/servis değişmedi. Sonraki deneme
  (`20261020-142058`) kalan süreç kontrolünde DB'ye dokunmadan geri döndü.
- Canlı rc durdurucunun regex'i `./auth (game)` ve `./game99 (game)` adlarını
  kaçırıyor. Bu kurucu yalnız metin2 kullanıcısının bu altı sürecine TERM gönderip
  oyun süreçlerinin kapanmasını ve kayıtlarını yazmasını bekler, sonra DB'yi
  durdurur. Canlı rc dosyası değiştirilmedi; diğer bakım kurucuları için bu
  eski durdurucuyu kullanmadan önce aynı süreç adı ayrıntısı dikkate alınmalı.

### Metin yoğunluğu 4× / yarım süre — 2026-10-20

- Kullanıcı 2× sayıyı az buldu; başlangıca göre 4× metin ve daha kısa yeniden
  doğma süresi istedi. Sayılar önce `PVP_HEDEF.md`'ye işlendi.
- 13 açık dünya haritasında kapasite 194 → 388 (ilk baseline 97). İlk süreler
  yarıya indirildi; kesirli saniyeler yukarı yuvarlandı. Bölgeler, taş türleri,
  maden kayıtları ve kayıt başına `max_count=1` korundu.
- Politika `metin_density.json` v2; denetleyici başlangıç SHA'sını eski süreleri
  geri koyarak doğrular. Yeni bakım yolu `python3 platform/deploy/density_release.py --install`:
  sadece 13 `stone.txt`, canlı 2× SHA eşleşmesi, yedek, geri alma ve servis
  süreç/port koşulları. Yeni client build veya oyun/regresyon testi yok.
- **Canlı:** `20261020-140835` kuruldu. Host kayıtları
  `/home/m2web/density-20261020-140835`, VM kayıt/yedeği
  `/usr/metin2-density-20261020-140835/previous`. İki uçta `INSTALLED`.
  Canlı 2× dosya hash'leri kurulum öncesinde eşleşti; kurulum sonrası 13 dosya
  adayla aynı, altı servis süreci ve altı port sağlıklı. Oyun testi kullanıcıda.

### CANLI — loot v3, wiki boss omurgası ve web tuşları (2026-10-20)

Kullanıcı bu tur açıkça “hepsini canlıya al, main'e commit et, test etme; ben
test edeceğim” dedi. Ardından deploy'dan önce Lusifer'e 70 silahlarını da ve
rehberde eksik kalan klasik bosslara ortalama wiki tabanlı loot istedi.
Son sürüm **20261020-134850** canlıya kuruldu; önceki adaylar kullanılmaz.

- Lusifer: 75 aile %30, 70 aile %15, 65 aile %7, 66 zırh %12. Tam tablolar
  `phase3_loot.json` v3 ve `docs/DROP_REHBERI.md` içinde.
- Önceki rehberde eksik 10 bossun hepsi tamamlandı: Vahşi Yüzbaşı, Dev Hastalık
  Taşıyıcı, Güçlü Buz Cadısı, Barones, Dev Çöl Kaplumbağası, Kırmızı Ejderha,
  iki ağaç bossu, Kharoon ve Azrail. 13 boss / 12 kendi sandığı, 7 doğrudan
  boss tablosu; metin grupları 23. Kaynaklar rehberde; yüzdeler bizim orta-kolay
  ayarımız, eşya aileleri wiki/proto tabanlı. 100+ ekipman taşınmadı.
- İstemci 20261020-125412 dondurulmuş derlemesinden alındı. Yeni engine build,
  unit/regresyon veya oyun testi çalıştırılmadı. Kurulum hash/dosya eşleşmesi ve
  servis süreç/port koşulları tamamlandı. Corpus değişmedi, CDN upload yok.
- Kurulum VM loot'unu başarıyla yükledi ancak başlatılan servislerin devraldığı
  stdout SSH kanalını açık tuttu. Oyun tekrar başlatılmadan, INSTALLED ve canlı
  tablolar doğrulanıp yalnız eşleşen eski kurulum kabuğu/bekleyen SSH istemcisi
  `phase3_finish_host.sh` ile kapatıldı; web yayını tamamlandı, komut exit 0.
  Gelecek kurulumlar için servis stdout/stderr dosyaya, stdin /dev/null'a alındı.
- Host `/home/m2web/phase3-20261020-134850`, VM
  `/usr/metin2-phase3-20261020-134850`; `INSTALLED` mevcut. Site yedeği
  `/home/m2web/backups/phase3-finish-FO7RZ482/site`, VM eski tablolar `previous/`.
- Main'e ilgili birikmiş istemci/sunucu/runtime/deploy/rehber değişiklikleri
  birlikte kaydedilir; yerel bridge node_modules dışarıda tutulur. Kullanıcı
  sayfayı yenileyip kabul testini kendi yapacak. Faz 3 loot omurgası ilerledi;
  instance/reentry ve canlı oyuncu kabulü ayrıca izlenecek, faz bütünü kapatılmadı.

### Loot v2 — eksik boss silahları ve tam drop rehberi (2026-10-20)

Kullanıcı önceki sandıkların sadece malzemeye yaslandığını düzeltti; gerçek 75
silahların Lusifer sandığında olmasını ve metin/bossların tam dökümünü istedi.
Resmî Lusifer/Ork/Hayalet Lider/Kraliçe Örümcek/Dokuz Kuyruk/Kaplan/Alev/Şeytan
Kral sandık listeleri ve PvP ilerleme rehberleri karşılaştırıldı. Kaynaklar ve
kararların sınırları `docs/DROP_REHBERI.md` içinde; yayımlanmayan resmî yüzdeler
taklit edilmedi. Bu projedeki yüzdeler kendi orta-kolay denge ayarıdır.

- `PVP_HEDEF.md` önce güncellendi; `phase3_loot.json` v2 ve gerçek iki loot tablosu
  eşlendi. Diğer sandıklarda %28 65 silah + %12 zırh; Hayalet Lider 54, Kraliçe
  Örümcek 61 zırh ailesini kullanır. Lusifer'de %30 75 silah, %14 65 silah,
  %16 66 zırh; malzemeler kalan ağırlığı paylaşır.
- Gerçek 75 ailesi: Zehir 180, Aslan 190, Şeytan Kanadı 1130, Havalı Çelik 2170,
  Kin 3160, Orkide 5120. Her biri +0, %5. Havalı Çelik ID'si 2150 değildir;
  2150 Geyik Boynuzu Yay (30) olduğundan ayrı regresyonla korunur.
- 85/90 metinlerden Zehir ve Orkide Lusifer sandığına taşındı. Siam, Şeytani Pala,
  Yarı-İnsan ve Mutluluk 70 seviyedir; metinde kaldı. Harita/regen/respawn, binek
  tuş düzeltmesi, BK/ruh taşı ayarı ve sunucu protokolü bu revizyonda değişmedi.
- `platform/tools/drop_catalogue.py` yalnız stdout'a rehber üretir; `--check`
  kayıtlı belgenin tablolar ve protolarla eşleşmesini denetler. Türkçe isimleri
  UTF-8/cp1254 okur; seviye gerçek proto'dan gelir. `docs/DROP_REHBERI.md` tüm
  23 metin grubunu, 9 sandığı, değişmeyen diğer mob/boss gruplarını, taş kesesini,
  ters eşya-kaynak indeksini, koşullu motor kancalarını ve eksik loot'ları listeler.
- Yeni testler tüm 6 silahın seviye 75 ve AddonType=-1 olduğunu, yanlış yay ID'si
  kullanılmadığını, metinlere 75 silah geri sızmadığını ve her sandığın silah/zırh
  içerdiğini denetler. Yerel 42 Python testi geçti; rehber eşleşme kontrolü eklendi.
- Canlı dosya/servis değiştirilmedi. `20261020-125412` / `20261020-125127` eski v1
  adayları bu revizyonu kapsamaz, kurulmamalı; v2 için yeni paket gerekir.
  Barones/Azrail'in özel statik loot'u hâlâ eksik; Faz 3 tamamlandı sayılmadı.

### Faz 3 — klasik akışta loot ve tuş düzeltmeleri (2026-10-20)

**Hazır aday: `20261020-125412`; henüz canlıya kurulmadı.** Host
`/home/m2web/phase3-20261020-125412`, VM `/usr/metin2-phase3-20261020-125412`.
`BUNDLE_READY` / `READY` doğrulandı; hazırlık canlı dosyaları ve servisleri değiştirmedi.
Önceki hazırlık `20261020-125127` yerine bu son aday kullanılmalı.

- Kullanıcı kilidi: haritalar ve metin/boss yerleşimleri klasik akışta kalacak.
  Bu revizyon mevcut 2× metin yoğunluğunu, spawn sürelerini ve zindanları değiştirmez.
- Tarayıcı DirectInput tablosu fiziksel `Backquote` dışında Türkçe `"` karakterini
  de toplama koduna eşler. Tuş basılırken seçilen kod keyup'a kadar tutulur;
  Shift önce bırakılırsa yanlış tuşun bırakılması/takılı kalması önlenir.
- `PythonPlayerInput.cpp` içindeki ek 107/109 at becerisi engeli kaldırıldı.
  Space ve mouse saldırısı mevcut `CInstanceBase::CanAttack` kararını paylaşır;
  özel shop, observer ve emotion kontrolleri korunur. Bu dosya mevcut halinde
  ASCII/LF idi; diğer cp1254/CRLF istemci kaynakları dönüştürülmedi. Dosya canlı
  kitin kaynak kopyasına da eşlendi ve gerçek Emscripten build'inden geçti.
- BK 6/10/12/14 bağımsız satır, unutma+münzevi malzemeleri, 40+ kademeli ruh
  taşı; 90 metinde 66 taban zırh +0. Sayılar önce `PVP_HEDEF.md` içinde kilitlendi;
  makine politikası `platform/gameplay/phase3_loot.json`. G hedefi, o seviyede
  Master olmuş beceriler içindir; bütün skill'leri o seviyede Master yapma yok.
- Fork'ta M1→G 10 başarılı okuma; münzevisiz %35. Resmî oyunun 55 kitap hesabı
  buraya taşınmadı. 48 eşit beceri ve 12 BK/metin varsayımında destekli tek
  skill'in 60 metinde G olasılığı %93,2; 80'de %99,5. Bu, 65–70 seviye-zaman
  kabul testinin yerine geçmez. Hesap: `build/phase3-progression.json`.
- 10 klasik boss için kendi 9 sandığı tanımlandı. Eksik special_item_group
  içerikleri tamamlandı; tek ağırlıklı ödül verir. Erken sandıkta aynı becerinin
  10 BK'sı, orta/yüksek/Lusifer'de 3/5/8 ruh taşı seçeneği ve malzeme/66 zırh
  ödülleri var. Başka bossların var olan dropları korunur.
- Araştırma resmî metin/ruh taşı listeleri ile PvP tanıtım örneklerini karşılaştırdı.
  Kamuya açık tanıtımlar kesin server drop yüzdeleri sayılmadı; kaynaklar ve
  bize ait denge kararları `PVP_HEDEF.md` içinde ayrı belirtiliyor.
- Doğrulama: 40 Python testi (veri/proto/sandık ve izole bakım/geri alma dahil),
  3 JS klavye testi, 13/13 ekonomi. Gerçek web build: 80/80 patchcheck,
  sıfır derleme hatası, source login 594, RESP 20/20 ve bozuk/parçalı paket
  regresyonları geçti. Corpus değişmedi (1370 immutable chunk); CDN yüklemesi yok.
- Bakım: `phase3_loot_host.sh install ... --operator-maintenance`, VM'de yalnız
  iki loot tablosunu değiştirip servisleri başlatır ve eşleşen istemciyi kurar.
  Dondurulmuş hash, canlı drift kontrolü, yedek, süreç/port sağlığı ve hata halinde
  geri alma var. `AGENTS.md` otomatik VM restart yerine kullanıcı bakım adımı
  istediği için kurulum çalıştırılmadı. Tam komut ve oyun kabul listesi:
  `platform/deploy/GAMEPLAY_RELEASE.md`. Faz 3 tamamlandı sayılmadı.

### Canlı kurulum ve karakter penceresi engeli (2026-10-20)

- Kullanıcı bu dağıtım için Metin2 servislerinin durdurulup başlatılmasına
  açıkça istisna verdi. `20261019-213727` game/db + source-profile 594 bayt login
  istemcisi birlikte kuruldu. Drop, sınıfa uygun başlangıç quest'i, sınırsız
  normal dedektör, MAX_LEVEL 99 ve 13 haritada 97 → 194 metin kapasitesi canlıda.
  Aşağıdaki önceki "henüz canlı değil" kayıtları hazırlık anını anlatır.
- Kurulum sonrası gerçek dosya SHA'ları, altı süreç ve altı oyun portu doğrulandı.
  VM yedeği `/usr/metin2-gameplay-20261019-213727/previous`, site yedeği
  `/home/m2web/backups/gameplay-d6P0bSAs`. Public WASM SHA'sı adayla eşleşti:
  `8db82fe2e68ac06f548e14187cc0b9b8a3849135cee4e766cc80a67cad153d5d`.
- Oyun kabul testinde `deneme` karakteri seçimden sonra giriş ekranına döndü.
  Tarayıcıda doğrudan yeniden üretildi: `CharacterWindow.py` yüklenirken
  `AttributeError: 'tuple' object has no attribute 'append'`. Yohara kapalı
  klasik karakter sayfasının children alanı tuple; unvan sistemi liste bekliyor.
  Pack kaynağında unvan kontrolleri eklenmeden önce listeye çevrildi.
- `platform/tests/test_character_window.py` gerçek pencere dosyasını dört
  özellik bayrağının 16 kombinasyonunda çalıştırır; unvan kontrollerinin yalnız
  açıkken ve birer kez eklendiğini denetler. Yerel test geçti. Düzeltilmiş
  paket ve tarayıcıda dünya girişinin kabul testi şu aşamada devam ediyor.
- Yayın öncesi aynı test dönüştürülmüş `uiscript3/UIScript/CharacterWindow.py`
  üzerinde çalıştırılınca eski dosyayı yakaladı ve yayını durdurdu. Dev UI akışı
  `scripts` ağacını güncelliyor, pencere dönüştürücüsü ise eski corpus unpack
  ağacını okuyordu. `M2W_UISCRIPT_SOURCE` ile UI modunda doğrudan güncel
  `/work/dev/inputs/root/uiscript` kullanılır; araç da dev sync listesine eklendi.
  Normal corpus tabanlı derlemenin varsayılan kaynağı değişmedi.
- Güncel gerçek `uiscript3` dosyasında 16 kombinasyon geçti. Source login 594,
  RESP 20 bayt ve detector UI kontrolleri geçti. `publish_character_window.sh`
  ile yalnız istemci paketi yayınlandı; WASM byte olarak aynı, corpusun 1370
  chunk'ı aynı. VM yeniden başlatılmadı. Yeni site yedeği:
  `/home/m2web/backups/character-window-ZEKJZSIS`.
- Canlı ikinci denemede tuple hatası kalktı; sonraki engel
  `KeyError: leader_board` oldu. Klasik layout liderlik panelini ve pasif
  butonunu hiç tanımlamıyordu, controller ise Yohara'dan bağımsız bağlıyordu.
  Klasik pencereye aynı liderlik kontrolleri ve pasif butonu eklendi; özellik
  bayrakları değiştirilmedi. Test artık 32 layout kombinasyonunu çalıştırır;
  canlıda açık genişletilmiş emotion sayfasıyla controller'daki sabit GetChild
  bağlarının tamamını da denetler. Emotion kapalı controller dalının ayrı
  eksikleri bu kabul testinin kapsamına alınmadı.
- Son paket `/home/m2web/backups/character-window-15Z0ltU0` site yedeğiyle
  yayınlandı. 2026-10-20 11:50 UTC özel önizleme ve ardından 11:52 UTC civarı
  gerçek `https://metin2.kaanakin.dev/client.html?lang=tr` üzerinde `deneme`
  lv22 ile Pyungmoo'ya giriş ve C karakter penceresi açılışı doğrulandı.
  Aynı anda eski tuple/KeyError/Abort/unknown-packet hataları görülmedi.
  Oyun sekmesi kullanıcıya açık bırakıldı, geçici önizleme sekmesi ve SSH
  tüneli kapatıldı. Bu kabul yalnız giriş/pencereyi kanıtlar; art arda metin
  kesimi ve diğer oynanış senaryoları GAMEPLAY_RELEASE kabul tablosunda bekler.

### Açık dünya metin yoğunluğu 2× (2026-10-20)

- Kullanıcı mevcut bölgelerde yaklaşık iki kat metin istedi. Sayılar önce
  `PVP_HEDEF.md`'ye yazıldı: 13 klasik açık dünya haritasında kapasite **97 → 194**.
  Köy 1/2'ler, Seungryong, Yongbi, Sohan, Doyyum, iki orman ve map 70.
- Düzenlemeden önce bu 13 `stone.txt` dosyasının canlı SHA'ları repo ile eşleşti.
  Yalnız `m` türündeki 8001–8027 metin satırları birer kez kopyalandı; mevcut
  satırlar, doğma bölgeleri ve süreleri byte olarak korundu. Aynı dosyalardaki
  `r` türü maden grupları artırılmadı. Zindan/event/100+ haritalar değişmedi.
- `max_count=2` yapılmadı: RESP takibi tek regen kimliğini kullandığından iki taş
  aynı kimliği paylaşacaktı. Yeni bağımsız satırlarda `max_count=1`; sunucunun
  gerçek `get_word/read_line` koduyla native fixture 194 farklı metin/RESP ID'sini
  okudu. Bölge içi gerçek doğma konumunu ve araziye uygunluğu oyun motoru seçer.
- Politika/baseline SHA'ları: `platform/gameplay/metin_density.json`.
  Kontrol: `python3 platform/tools/metin_density.py` ve
  `python3 platform/tools/metin_density_native.py`. Yeni veri ve bakım testleriyle
  `platform/tests` toplam 31 test geçti; önceki dev/publish/bridge testleriyle 52.
- Veri adayı mevcut `20261019-213727` paketine `gameplay_density_prepare.py` ile
  eklendi; host ve VM'de `DENSITY_READY`, hostta yeniden `BUNDLE_READY` var.
  Bu işlem game/db/istemciyi yeniden derlemedi veya yayınlamadı. Harita
  kaynakları ve ilk canlı SHA'ları denetlenir; 13 canlı dosya da geri alma
  kapsamına eklenir. Kurulum harita dosyalarını CONFIG olarak işleyemez.
- Son `gameplay_verify_host.sh` geçti: yoğunluk ve paket hash'leri doğru,
  canlı runtime ilk yedek SHA'larıyla aynı, altı süreç/port sağlıklı; public WASM
  ve canlı game SHA'ları önceki sürümde. 13 haritada 123 satır eklendi, satır
  silinmedi; yoğunluk dosyalarında whitespace kontrolü temiz.
- **Henüz canlı harita veya servis değiştirilmedi.** Aynı operatör kurulum
  komutu drop/başlangıç/dedektör ile 2× yoğunluğu birlikte kurar. Ayrıntılar:
  `platform/deploy/GAMEPLAY_RELEASE.md`.

### Metin kesiminde kopma ve oyun doğrulaması (2026-10-20)

- Arc'ta seviye 21 `deneme`, seviye 20 Hırs Metini kesince login'e döndü.
  Console: `RecvMountUpGrade invalid subHeader: 73`, ardından
  `Unknown packet header: 246, last: 49 155`. Game süreci çökmedi.
- Kök neden: RESP list/refresh içindeki `nextRespTime` wire üzerinde 32 bit;
  FreeBSD i386 canlı ELF DWARF'ında kayıtlar 20 bayt. Emscripten `time_t`
  64 bit olduğundan eski web istemcisi 24 bayt okuyup sonraki pakete taşıyordu.
  Gerçek `Packet.h` alanları `int32_t` ve 20 bayt static assertion ile düzeltildi.
- İlk düzeltme **yayında**, canlı Yohara protokolüne uygun 619 bayt login
  korundu. Site yedeği: `/home/m2web/backups/client-login-6OJjljaT`.
  Corpus değişmedi; VM servisi yeniden başlatılmadı. Yayından sonra gerçek
  metin kesimi henüz doğrulanmadı; eski açık sekme yeniden yüklenmeli.
- `resp_packet_layout.py` gerçek Emscripten ölçümü ve WASM fixture çalıştırır.
  Refresh sonrası PING sınırı, signed timestamp, parçalı ve bozuk frame testleri
  geçti. Frame korumalı ikinci engine de yayında; son site yedeği
  `/home/m2web/backups/client-login-BwbaHNjW`. Patchcheck 80/80.
- `python3 platform/deploy/packet_audit.py`: çalışan ELF SHA'sı + gerçek
  staged client header'larından ABI raporu, `build/protocol/audit.json`.
  İlk ölçüm: 165 ortak yapı boyutunda ve 146 GC header numarasında uyuşmazlık yok;
  147 yapının alan offset'leri tam karşılaştırıldı; 18 yapı kısmi kaldı,
  125 client kaydı ve 20 GC header eşleştirilemedi.
  Bunlar tam protokol doğrulaması sayılmaz. Rapor semantik değer/signedness,
  dinamik payload ve handler tüketimini kanıtlamaz; RESP ayrıca fixture ile sınanır.
- Oyun tasarımı sayıları önce `PVP_HEDEF.md`'ye yazıldı. 23 metin grubuna
  seviyeye göre 5/8/10 ayrı BK, taş torbası, kutsama ve efsun malzemeleri;
  50+ ruh taşı eklendi. Harita yoğunluğu sonraki kullanıcı kararıyla üstteki
  2× revizyonuna alındı; bu değişiklik de adayda, henüz canlıda değil.
- Başlangıç quest'i: dört sınıfa STR/DEX/INT ve uygun saldırı/büyü hızı,
  silahlarda beş efsun; başlangıç ölümsüz/şeytan/mistik bonusları kaldırıldı.
  Ninja 8000 normal ok, şaman 5009 çan ve 7009 yelpaze alır.
  Mevcut DB `item_attr` izinleri/tavanları salt okunur sorguyla kontrol edildi.
- Normal dedektör 27989 her yeni karaktere bir adet; `CItem::SetSocket` yalnız
  onun 0. socket sayacını sıfırda tutar. Alternatif 76006 ve diğer socket'ler
  korunur. Web tooltip değişimi mevcut Python 2→3 semantic patch adımındadır;
  karışık kodlamalı pack kaynakları dönüştürülmedi.
- **Drop, quest ve sınırsız dedektör henüz canlıda değil.** İzole aday:
  `/usr/metin2-gameplay-20261019-213727` (VM),
  `/home/m2web/gameplay-20261019-213727` (host). `READY` ve `BUNDLE_READY` var:
  game/db derlendi, gerçek `qc` + sunucu Lua ile 4 sınıf × 2 cinsiyet fixture'ı
  ve FreeBSD'de 10.000 dedektör kullanımı geçti. Derlenen welcome handler'ı
  repoya aynen alındı; COMPLETE state kimliği değişmedi.
  Aday ABI: 164 ortak yapı boyutunda ve 145 GC header'da fark yok;
  146 tam alan karşılaştırması, 18 kısmi, 125 eşleşmeyen kayıt, 20 eşleşmeyen header.
  Game SHA: `258e81399200bb6c5186866464a66d64673a66ac09d5a4ae6af883a10bc533a3`.
  Kurulum/kabul adımları: `platform/deploy/GAMEPLAY_RELEASE.md`.
  Yeni kaynak sunucusu 594 bayt login kullanır; yalnız eşleşen source-profile
  web istemcisiyle birlikte kurulabilir. AGENTS gereği VM servis restart'ı
  operatör adımıdır. Eski `login_fix_vm.sh install` tek başına çalıştırılmamalı.
- Yerel kontroller: 21 oyun/ABI/kurulum testi + 14 dev-tool testi + 4 publish testi +
  3 bridge testi geçti; ekonomi kontrolü 13/13. Yeni loot mevcut gear satırlarını
  ve metin dışındaki tüm grupları koruyor. `qc` çıktısı kendi trailing-space
  biçimiyle saklandı; `git diff --check` yalnız bu üretilen satırları bildiriyor.
- Bakım betikleri yedi izole dosya/sahte servis senaryosunda doğrulandı:
  salt okunur hazırlık, kurulum+geri alma, değişen canlı dosyada durma,
  başarısız start'ta geri alma, eksik yedekte dosyayı kesmeden açık hata,
  eksik core ve eksik portta geri alma.
  Gerçek VM restart/kurulum çalıştırılmadı. İstemci/sunucu adayları donduruldu;
  geliştirme önizlemesi tekrar eski canlı `live-yohara` profiline döndürüldü.
- Mevcut rc betiğinin `status`'ü süreç yokken dahi 0 dönüyor. Bakım script'i
  bu sonucu sağlık kanıtı saymaz; db/auth/3 core/game99 süreç sayısını ve
  15000/30001/30003/30101/30103/30105 portlarını ayrıca denetler. Bu salt okunur
  kontrol gerçek VM'de geçti. FreeBSD `ps` auth/game99 için ` (game)` eki ekler;
  yalnız bu bilinen kernel-name eki normalize edilir.

### Hızlı web client geliştirme (2026-10-19)

- Yeni giriş noktası: `python3 platform/deploy/dev_client.py cpp|ui|link|clean`.
  Kullanım/kapsam: `platform/deploy/DEV_CLIENT.md`. C++ kaynakları web build
  ağacına byte olarak eşitlenir; web'e özel `Locale_inc.h` korunur.
- Engine `.o` klasörünü artık her build'de silmez. `tools/incremental_compile.py`
  kaynak/header içeriklerini, derleyici/seçenekleri ve include dosya listesini
  doğrular; değişmeyen object'leri kullanır, eski/başarısız object'leri temizler.
  İlk çalışma cache'i doldurur. O2 korunur; `clean` zorla yeniden derler.
- Stage case-alias dizin listeleri gerçek dizin yoluyla ortak cache kullanır;
  aynı dizinin `eterBase`/`EterBase` yazımlarından alias eklerken ortaya çıkan
  `FileExistsError` düzeltildi.
- Önizleme `/home/m2web/dev/site/current` altında; `package`/`publish`/Cloudflare
  adımları yok. Veri bir kez hazırlanır ve tek link yapılır; corpus tekrar
  paketlenmez/yüklenmez. Eterbase/eterpack arşivleri `tools/dev_archive.py`
  üzerinden gerçek `-MD` bağımlılıkları değişmedikçe tekrar kullanılır.
- `python3 platform/deploy/dev_client.py tunnel` iki loopback portunu açar:
  HTTP `18731`, ayrı geliştirme bridge'i `18732`. Tarayıcı adresi
  `http://127.0.0.1:18731/client.html?lang=tr`. `stop` yalnız geliştirme süreçlerini kapatır.
- Bu client önizlemesi **mevcut oyun sunucusuna/DB'ye bağlanır**; ayrı bir test
  VM/DB değildir. VM servis restart'ı, Traefik/UFW değişikliği veya canlı yayın
  yapılmaz. Geliştirme ve release build'i ortak kit ağacında eşzamanlı çalıştırılmaz.
- Önizleme HTML/manifest için `no-store`, engine/data/diller için içerik hash'li
  immutable URL kullanır; değişmeyen büyük `.data` paketi her build'de yeniden
  indirilmez. Gzip hazır kopyaları HTTP tarafından desteklenir; eski asset
  sürümüne istek `409` döner ve sayfanın yenilenmesi gerekir.
- Doğrulama: 14 yerel Python testi ve 3 Node bridge testi; gerçek C++ compiler cache, snapshot/HTTP/gzip/
  sürümleme, UI overlay silme ve stage alias regresyonu. Hostta `patchcheck`
  77/77, link `UNEXPECTED: none`. İlk `cpp` 248,6 s (engine 205 s); cache'li,
  kaynak değişikliği olmayan `cpp` 31,6 s (engine 15 s, 359 object ve iki arşiv
  kullanıldı). `ui` 60,5 s; `link` 13,6 s. Tarayıcının ilk indirmesi bu sürelerde yok.
- Snapshot corpus bağlantısı container `/work` ve host `/home/m2web` mount
  farkı nedeniyle **göreli** olmalı; absolute symlink hostta 404 veriyordu.
  Düzeltildi ve HTTP/yerel testle doğrulandı. Tarayıcıda Türkçe giriş ekranı
  açıldı, CH1 çevrimiçi. İngilizce locale'deki mevcut eksik
  `TOOLTIP_MALL_EXPBONUS_P_STATIC` anahtarı ayrı bir veri sorunu; kullanım URL'si
  bu nedenle `?lang=tr`.
- Hesapla giriş testi iki sorun buldu: SSH tünelindeki localhost PROXY kaynak
  adresi sunucuda reddediliyordu; geliştirme bridge'i artık yalnız doğrulanmış
  SSH peer genel IPv4 adresini kullanır. Üretim bridge'inin adres çözümü aynı.
  İkinci sorun: çalışan `/usr/home/share/bin/game` binary'si eski Yohara açık
  sürüm (`SSimplePlayer=105`, login=619 bayt; DWARF ve disassembly ile ölçüldü).
  Güncel kaynaklardan probe 100/594; bu kaynaklar henüz çalışan binary değil.
  594 bayt okuyan client sonraki paketi yanlış başlıktan okuyor ve login'de
  bekliyordu. Sadece stage'de uygulanan `--protocol live-yohara` önizlemeyi eski
  server'la eşler; başarılı seçim `dev/protocol` içinde saklanır. Kaynak/PvP
  flag'leri değiştirilmez. Güncel server kurulunca `--protocol source` gerekir.
  Her dev build'de Emscripten ile gerçek paket boyutu ölçülür ve profil doğrulanır.
- Ayrı server derlemesi `/usr/metin2-login-fix-20261019-204458` altında tamamlandı (`READY`);
  kaynak anlık görüntüsü çalışma ağacındaki server değişikliklerini içerir.
  `login_fix_prepare.py` yalnız ayrı build hazırlar. `login_fix_vm.sh install`
  game/db'yi birlikte yedekleyip değiştirir ve restart yapar; **operatör adımıdır**.
  Otomatik kurulum/restart yapılmadı. Henüz prod client uyumu test edilmeden
  bu server derlemesini kurma; eşleşen client release'iyle koordine edilmeli.
- Giriş düzeltmesi **canlıda doğrulandı**: uyumlu 619 baytlık engine ile normal
  `webclient.py package` (özel dosyasız public paket) hazırlandı. Yerel preview
  bridge override'ı ve `loginInfo.xml` bulunmadığı doğrulandı. Canlı hesaptan
  `numan`/`deneme` karakter seçim ekranı açıldı; sonra test sekmesi kapatıldı.
  Bu test dünya/oyun içi stabilite testi değildir. `101 Switching Protocols`
  ve açık WebSocket'in pending görünmesi normal; hatanın nedeni paket uyumsuzluğuydu.
- `publish.sh --engine-only`: manifest/groups içerikleri ve 1370 chunk'ın
  ad/boyut envanteri aynı değilse yayın reddedilir. Aynıysa CDN yüklemesi
  yapılmadan engine/data/diller eşitlenir, HTML en son alınır; corpus ve ASan
  korunur. Yardımcı `publish_engine_check.py` hostta publish.sh yanında olmalı.
  Dört yayın koruması testi geçti; öncesinde site yedeği
  `/home/m2web/backups/client-login-AVXsRkPs` alındı. Site/bridge/VM restart'ı,
  Traefik değişikliği veya yeni Cloudflare deployment yapılmadı.

Son güncelleme: 2026-10-19. Hobi amaçlı, ~10 kişilik sunucu. **Ana hedef: oyunun tarayıcıda (WebAssembly) oynanması.**

Bu dosya, yapılanları ve kaldığımız yeri kaydeder. Şifreler burada YOK; nerede durdukları yazılı. 1–99 PvP tasarım/fazlar: `PVP_HEDEF.md` + `docs/ROADMAP_PVP.md`.

### Repo klasör düzeni (2026-10-18)

- Kaynak ağaç (hard-cut, tek isim): `apps/`, `content/`, `runtime/freebsd/`, `platform/`, `vendor/` — özet: `docs/ARCHITECTURE.md`, agent kuralları: `AGENTS.md`.
- Compat symlink yok. Eski isimler (`Source/`, `Client/`, `home/`, `sql/`, `Tools/binary_unpack`, `Tools/web/`, `web/portal`) kaldırıldı.
- Tag'ler: `pre-layout-20261018` (taşıma öncesi), `pre-hardcut-20261018` (symlink drop öncesi).
- **VM hard-cut canlı (2026-10-18, commit `8cceb8e22`)**: live `/usr/metin2/apps/server`; eski ağaç saklandı `/usr/metin2-prev-20261018-102041`; host tarball `/root/backups/metin2-{tree,bin}-20261018-hardcut.tar`. Geri alma: `platform/deploy/LAYOUT_CUTOVER.md`.
- Release script path'leri: `platform/deploy/release_upload.sh`, `platform/deploy/server_release.sh`.

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

**Oyun dengesi / 1–99 PvP** (web’den ayrı omurga): kilidi `PVP_HEDEF.md`, fazlar `docs/ROADMAP_PVP.md`, done-log `docs/MID_PVP_FAZ0_1.md` + `docs/MID_PVP_FAZ2.md`. Sıradaki: Faz 3 içerik/boss. Canlıya alma: `platform/deploy/VM_MID_PVP_APPLY.md`. Bu bölümde yalnızca web/VM işleri.

1. ASan ile heap taşmasını bul ve düzelt (yukarıdaki "AÇIK SORUN").
2. Normal kütüphaneleri yeniden derle + yayınla; `kaannakiin`/`numan` ile oyuna girip birkaç dakika stabil kaldığını doğrula.
3. Fare/kara bant/DXT, ağaçlar, harita adı dili.
4. GM şifresini değiştir (sohbette geçti).
5. Oyun içi QoL smoke (roadmap Faz 2): switchbot, oto av, offline pazar, biyolog, battle pass — güç veren aura/kuşak/simya 1. sürümde kapalı (`PVP_HEDEF` özellik seçimi).

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
- Server + bridge yayını tek adımda (bridge PROXY satırı yazıyor, server onu bekliyor; biri yalnız giderse herkes düşer): Mac'te `platform/deploy/release_upload.sh` (commit'lenmiş hali host'ta `/root/metin2-release`'e), host'ta `/root/metin2-release/platform/deploy/server_release.sh stage` → `build` → bakım penceresinde `install` (geri alma: `rollback`). Layout cutover öncesi: `platform/deploy/layout_cutover_backup.sh`. Makefile'lar binary'yi her zaman `/usr/home/share/bin`'e taşıyor; `build` bu yüzden `GAMEDIR`/`DBDIR`'i `/usr/metin2-next/out`'a yönlendiriyor. VM CONFIG'lerine dosya kopyalanmaz (DB şifreleri farklı), sadece `TRUSTED_PROXY_IP` satırı eklenir.
