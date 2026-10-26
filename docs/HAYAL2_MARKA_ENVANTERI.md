# Hayal2 marka dönüşümü — Anka2 envanteri

Tarih: 22 Ekim 2026. Hedef ürün adı: **Hayal2**.

Bu çalışma yerel depodaki marka izlerini bulur. Kaynak, görsel, paket, canlı sunucu veya veritabanı değiştirilmedi. Değişiklik öncesindeki çalışma ağacında başka çalışmalar vardı; bunlara dokunulmadı.

## Sonuç

- Git tarafından izlenen ve ignore dışında kalan toplam **156.167 dosyanın** yol envanteri çıkarıldı. Metinler `Anka2`, `Anka 2`, `Anka-2`, `Anka_Project`, `BestStudio` ve ilgili yazım biçimleriyle tarandı. İzlenen dosyalar ayrıca Git ignore kurallarından bağımsız okundu; böylece `Locale_inc.h` de kapsandı.
- **46 metin/kaynak dosyasında 65 satırda doğrudan Anka2 eşleşmesi** var. Bunun 45 dosya / 64 satırı ana ağaçta, 1 dosya / 1 satırı `vendor` altında. Bunlar kelime sayısı değil, eşleşen satır sayısıdır.
- **16 görsel dosyasında eski A amblemi gözle doğrulandı:** 2 Windows ikonu ve 14 yükleme animasyonu karesi. Dosya adına bakmak bu 14 kareyi bulmaya yetmiyor.
- Ayrıca başka sunucu logosu taşıyan eski giriş arka planı, Metin2 yazılı atlas, resme gömülü panel yazıları ve portalın genel Metin2 kimliği var.
- **75 dosyada** eski proje yolu veya BestStudio bağlantısı/kredisi bulundu; doğrudan Anka2 listesindeki bazı dosyalarla örtüşür. Bu sayı üçüncü taraf `vendor` dosyasını içermez.
- `property.xml` içinde **10.799 satır** `C:\Anka_Project_2025\...` yolu içeriyor.
- 4 eski derleme/araç çıktısında da Anka2 dizeleri doğrulandı. Bunlar kaynak metni değiştirerek temizlenmez.

Tam dosya/satır listesi: [HAYAL2_MARKA_ENVANTERI.tsv](HAYAL2_MARKA_ENVANTERI.tsv). TSV'deki yollar depo köküne göredir. `eslesme_sayisi`, metin sınıflarında eşleşen satır sayısıdır; görsel satırlarında uygulanmaz.

## 1. Oyuncunun doğrudan gördüğü yazılar

| Yer | Dosya ve satır | Bulgu / dönüşüm kapsamı |
| --- | --- | --- |
| Pencere başlığı | `apps/client/source/UserInterface/Locale_inc.h:3` | `Anka2.com # Gerçek Rekabet Burada Başlar! \| [Best Studio]`. Hayal2 adı, slogan ve görünür stüdyo eki birlikte ele alınmalı. |
| Sunucu adı | `apps/client/source/UserInterface/PythonNetworkStreamModule.cpp:2306` | `net.GetServer_IPNAME()` tarafından kullanılan sunucu adı `Anka2`. `root/serverinfo.py:11` bu değeri alıyor. |
| Giriş ekranı alt yazısı | `content/client/packs/root/uiscript/loginwindow.py:25` | `© 2025 · BestStudio Production — Anka2 Project`. |
| Karakter seçimi alt yazısı | `content/client/packs/root/uiscript/selectcharacterwindow.py:47` | Aynı eski proje/stüdyo metni. |
| Karakter oluşturma alt yazısı | `content/client/packs/root/uiscript/createcharacterwindow.py:48` | Aynı eski proje/stüdyo metni. |
| Krallık seçimi alt yazısı | `content/client/packs/root/uiscript/selectempirewindow.py:25` | Aynı eski proje/stüdyo metni. |
| Sistem mesajı etiketi | `content/client/packs/locale/*/locale_game.txt` | 11 dilde `SYSTEM_WHISPER [Anka2]`. Diller: `tr`, `en`, `es`, `fr`, `de`, `hu`, `pt`, `ro`, `cz`, `it`, `pl`. |
| Türkçe unvan | `content/client/packs/locale/tr/locale_game.txt:4330` | `TITLE_SYSTEM_NAME_16`: `Anka2 Development`. |
| Türkçe wiki etiketi | `content/client/packs/locale/tr/locale_game.txt:4857` | `WIKI_GUIDES2`: `Anka2 bilgi`. |
| Türkçe wiki karşılama | `content/client/packs/locale/tr/locale_game.txt:4999` | `Anka2 ekibi keyifli oyunlar diler!`. |
| Wiki kostüm açıklaması | `content/client/packs/locale/tr/wiki/systems/costume.txt:17,22` | İki yerde `Anka2.com`. |
| Wiki drop açıklaması | `content/client/packs/locale/tr/wiki/drops.txt:17` | `Anka2.` ile başlayan dünya açıklaması. Dosyada ayrıca bozuk Türkçe kodlama var. |
| Mağaza bağlantısı | `content/client/packs/root/uiitemshopnew.py:100` | `https://anka2.com/gateway`. Hayal2 için kullanılacak gerçek mağaza adresi henüz verilmedi; varsayımsal `hayal2.com` adresine çevrilmemeli. |

### Eşya adı

Vnum **77924** adı `Anka2 Sandık` olarak üç metin kopyasında bulunuyor:

- `Tools/dump_proto/tr/item_names.txt:10388`
- `runtime/freebsd/share/conf/item_names.txt:10388`
- `runtime/freebsd/main/db/item_names.txt:10388`

İlgili proto kaydı `runtime/freebsd/share/conf/item_proto.txt:10768` satırında. Dönüşümde **vnum korunarak görünen ad** değişmeli; istemci proto/paket çıktısı ve sunucudaki gerçek adın eşleşmesi ayrıca doğrulanmalı. Canlı veritabanı bu taramada sorgulanmadı.

## 2. Görseller ve amblemler

### Kesin eski marka: 16 dosya

| Dosya / seri | Gözle doğrulanan içerik | Teknik not |
| --- | --- | --- |
| `apps/client/source/UserInterface/anka2.ico` | Kahverengi/kırmızı zeminde altın A amblemi. | ICO, 128×128, tek kare. |
| `apps/client/source/UserInterface/anka2_block.ico` | Aynı eski A ambleminin diğer durumu. | ICO, 128×128, tek kare. |
| `content/client/packs/etc/ui/intro/loading/0.tga` … `13.tga` | A amblemi etrafında dönen/ışıldayan halka, toplam 14 kare. | **Uzantıları `.tga`, gerçek içerikleri PNG, 380×380.** Yeni dosyalarda biçim, alfa ve animasyon geometrisi bilinçli korunmalı. |

Windows ikonları `apps/client/source/UserInterface/UserInterface.rc:117–118` üzerinden bağlanıyor. İkon dosyaları yeniden adlandırılırsa bu kaynak referansları da güncellenmeli.

Yükleme kareleri **aktif kod tarafından kullanılıyor**: `content/client/packs/root/networkmodule.py:213–214`, `xrange(14)` ile `d:/ymir work/ui/intro/loading/%d.tga` dosyalarını yüklüyor. Bu yol harita geçişindeki `isWarp` dalında çalışıyor. Sadece giriş ekranının logosunu değiştirmek eski amblemi kaldırmaz.

### Diğer eski kimlik / resme gömülü yazılar

| Dosya | Gözle doğrulanan içerik | Durum |
| --- | --- | --- |
| `content/client/packs/etc/ui/intro/login/background.tga` | Başka bir sunucunun yazılı logosunu taşıyan mavi giriş resmi. | 1920×1080. İncelenen güncel `uiscript/loginwindow.py:19`, bunun yerine `background.png` kullanıyor; eski görsel yine de depoda duruyor. |
| `content/client/packs/etc/ui/intro/login/bg_bg.png` | Resme gömülü `LOGIN`, `SELECT CHANNEL`, `SAVED ACCOUNTS` yazıları. | Marka adı yok; Hayal2 arayüzünün yazı/dil bütünlüğü kapsamında ele alınabilir. |
| `content/client/packs/etc/ui/intro/login/bg_bg - Copy.png` | Aynı başlıkların farklı tasarım kopyası. | Marka adı yok, eski alternatif varlık. |
| `content/client/packs/etc/ui/intrologin.dds` | Metin2 logosu ve orijinal yayıncı/telif yazısı olan eski atlas. | 512×512. `intro/login/metin2_logo_1.sub`, `metin2_logo_2.sub`, `background_alpha.sub`, `IntroLogin.dds` içindeki alanları referanslıyor. |
| `content/client/packs/etc/ui/introloading.dds` | `Loading...` yazısı ve yükleme simgeleri içeren atlas. | 512×512. Anka2 adı görülmedi; genel yükleme arayüzü adayı. |
| `content/client/packs/etc/ui/intro/login/logo_background.tga` | Beyaz fırça darbesi şeklinde dekor. | 627×121. Dosya adında `logo` var ama görselde marka yazısı/amblem yok. |

### Kontrol edilen, üzerinde eski marka görülmeyen ana arka planlar

- `content/client/packs/etc/ui/intro/login/background.png` — mor kıyafetli karakter ve mavi tapınak.
- `content/client/packs/etc/ui/intro/common/background.png` — savaş sahnesi; karakter seçimi/oluşturma bunu kullanıyor.
- `content/client/packs/etc/ui/intro/empire/background.png` — ejderha ve krallık adası.
- `content/client/packs/locale/tr/ui/background.tga` — iç mekân sahnesi.
- `content/client/packs/locale/tr/ui/select/empire/background/*.jpg` — kontrol edilen krallık arka planlarında Anka2 yazısı/amblem görülmedi.

Bunların tamamının yeniden tasarlanması marka temizliği için zorunlu değil. Hayal2'ye ait yeni sanat yönü ayrıca belirlenebilir.

## 3. Portal ve tarayıcı kimliği

| Dosya | Bulgu |
| --- | --- |
| `apps/portal/src/site.ts:2` | Ortak site adı `Metin2`. Hayal2 ürün adı burada merkezi olarak tanımlanmalı. |
| `apps/portal/src/routes/__root.tsx:21` | Sayfa başlığı `SITE.name` değerinden geliyor. |
| `apps/portal/public/favicon.svg:1` | Mevcut portal favicon'u. Hayal2 amblemiyle uyumlu hâle getirilecek görsel nokta. |
| `platform/web-kit/site/client.html:6` | Oyun sekmesinin başlığı `<title>Metin2</title>`. |

Bu portal/site kaynaklarında Anka2 veya mevcut Hayal2 markası bulunmadı; genel Metin2 kimliği kullanılıyor. `metin2.kaanakin.dev` mevcut erişim alan adı. Kullanıcı yeni alan adı vermedi; DNS, origin, bridge origin kontrolü ve Turnstile yapılandırması bu raporda değiştirilmedi.

`root/intrologo.py:26` ayrıca `logo1.avi` ve `logo2.avi` adlarını listeliyor. Yerel izlenen/ignore dışı envanterde AVI/MP4/WMV dosyası yok; canlı pakette bulunup bulunmadığı doğrulanmadı.

## 4. Yeniden derlemenin eski adı geri getirebileceği yerler

| Dosya | Bulgu / bağımlılık |
| --- | --- |
| `platform/web-kit/stage_port.py:950–951` | Sunucu adresi yamasının hem arama hem değiştirme metninde `Anka2` var. C++ sunucu adı değişirse iki taraf aynı değişiklikte uyarlanmalı; yoksa yama eşleşmesi kırılabilir. |
| `platform/web-kit/webclient.toml:3` | `client = "/work/anka2/content/client/runtime"`. Bu ürün metni değil, gerçek derleme dizini. Dizin/bind mount ile birlikte ele alınmalı. |
| `platform/web-kit/prep_websrc.sh:2,5` | `anka2/apps/client` kaynak dizini. Sadece ismi değiştirmek derlemeyi bozabilir. |
| `platform/web-kit/compat/{shellapi.h,locale_web.cpp,d3d8_image.cpp,stubs.cpp}` | Anka2 forkunu tarif eden yorumlar. |
| `platform/web-kit/tools/{rewrite_scripts.py,script_patches.py}` | Forka özgü işlemleri tarif eden Anka2 yorumları. Özellikle mevcut kodlama çalışmasıyla çakışmadan ele alınmalı. |
| `apps/client/build_client.{bat,ps1}` | Derleme araçlarının başlıkları `Anka2 Client Build System`. |
| `apps/client/clear_vsfiles.{bat,ps1}` | Temizlik araçlarında eski proje adı. |
| `platform/tools/drop_catalogue.py:107` | Ürettiği drop rehberinin başlığı Anka2; sadece rehberi elle düzeltmek kalıcı çözüm olmaz. |
| `apps/server/common/service.h:2,10` | Üst başlık/yorumlarda `ANKA2 SYSTEM INFO GAME`, `Anka2Project`. Oyun özelliği bayrağı değil. |

## 5. Belgeler, eski yollar ve stüdyo kredileri

Anka2 adı `README.md`, `CALISMA_NOTLARI.md`, `PVP_HEDEF.md`, `docs/ROADMAP_PVP.md`, `docs/DROP_REHBERI.md` içinde geçiyor. Güncel ürün başlıkları Hayal2 olmalı; geçmiş işlem kaydındaki tarihsel adlar otomatik değişiklikten ayrı değerlendirilmeli.

`content/client/packs/root/property.xml:3` ve sonraki kayıtlarda 10.799 eski `C:\Anka_Project_2025\...` yolu var. Bunlar `filename` metaverisinde görüldü. Oyundaki `buildingfile`, CRC ve paket yollarını toplu metin değiştirmeyle bozmamak gerekiyor; bu yolların tüketicisi incelenerek taşınmalı veya temizlenmeli.

BestStudio / Best Studio / ybeststudio eşleşmeleri şuralarda bulundu; tam dosyalar TSV'de:

- Oyuncuya görünen dört giriş/seçim ekranı alt yazısı ve `APP_TITLE`.
- `apps/server/{game,db}/src/version.cpp` içindeki açılış/sürüm çıktıları.
- `runtime/freebsd/admin.sh`, auth/db/channel yapılandırmalarının yorum başlıkları ve bazı `version.txt` dosyaları.
- 11 dilin `country/*/translate.lua` dosyaları ve Türkçe `translate2.lua`.
- 29 Lua görev dosyasının yazar/GitHub başlıkları.
- README katkı/yazar bölümü, çalışma notu ve archiver çıktısı.
- Üçüncü taraf `vendor/FoxFS_Src/FoxFSArchiver/main.cc:403,410` içindeki proje adı/kredisi.

Görünür ürün markasıyla kaynak yazar/telif atfı aynı şey değil. Yazar, lisans ve üçüncü taraf kaynak atıfları Hayal2 yazarıymış gibi yeniden adlandırılmamalı; görünür arayüz markası ayrı temizlenmeli.

## 6. Eski üretilmiş dosyalar

| Dosya | Doğrulama |
| --- | --- |
| `apps/client/binary/Metin2Release.map` | 7 ASCII Anka2 eşleşmesi. |
| `apps/client/binary/Metin2Debug.bsc` | 1.735 ASCII Anka2 eşleşmesi. |
| `apps/client/binary/Client.lnk` | 2 ASCII ve 1 UTF-16LE Anka2 eşleşmesi; Windows kısayolu. |
| `Tools/archiver/tools/Python27/Lib/posixpath.pyc` | 48 ASCII Anka2 eşleşmesi; araç önbelleği/eski derleme yolları. |

Bu sayılar dize eşleşmesi sayısıdır. Kaynak düzeltmesinden sonra ilgili çıktılar yeniden üretilmeli veya gerçekten gereksizse ayrı temizlenmeli. Binary dosyalara düz metin değiştirme uygulanmamalı.

## 7. Yanlış eşleşmeler

- `Anka Yayı`, `Anka Kuşu Şişi`, `Anka Kuşu Yelpaze` gibi eşya adları ve Anka Kuşu soruları oyun içeriğidir; yalnız `anka` kelimesi geçtiği için Hayal2'ye çevrilmemeli.
- `Lonca banka` gibi yorumlardaki `anka` alt dizisi marka değildir.
- `Ateş Hayaleti`, hayalet canavar/efekt adları Hayal2 markası değildir.
- `ENABLE_*` bayrakları veya ağ/protokol sistemleri bu marka dönüşümü nedeniyle kapatılmamalı.
- Lonca işaretleri, görev soru işaretleri ve `buff_emblem` gibi genel oyun amblemleri eski marka sanılarak kaldırılmamalı. Anka2'ye ait 16 amblem yukarıda gözle doğrulanan dosyalardır.

## 8. Dönüşüm sırası ve doğrulama

1. Hayal2 yazımını sabitle; yeni ana logo, küçük amblem/favicon ve yükleme amblemini hazırla. Mağaza için kullanılacak gerçek bağlantıyı belirle.
2. Oyuncuya görünen metinleri, 11 dildeki sistem etiketini, eşya adını, portal adını ve oyun sekmesi başlığını değiştir.
3. İki Windows ikonunu ve 14 yükleme karesini değiştir; eski giriş görseli ve kullanılmayan alternatifleri referans kontrolüyle temizle.
4. C++ sunucu adı ile stage yamasını birlikte değiştir. Derleme dizini adlarını gerçek mount/dizin düzenine göre ele al. Rapor üreticisini ve güncel belge başlıklarını güncelle.
5. Client kaynaklarında cp1254/CRLF, karma kodlamalı Python/dil dosyaları ve resim alfa/formatı korunmalı. Bu çalışma sırasında süren metin kodlama değişiklikleriyle birleştirme yapılmalı.
6. Değişen client kaynaklarını host `websrc` kopyasına, kit değişikliklerini hem depo hem canlı kit kopyasına taşı. `Locale_inc.h` için web bayrak farklarını koru.
7. Değişikliğin türüne göre root/locale/etc paketlerini, dil paketlerini ve corpus'u yeniden üret; C++/ikon değişikliği için ilgili client derlemesini yap. Statik metin değişiklikleri için gereksiz engine derlemesi yapma.
8. Stage değiştiğinde `patchcheck.py`; portal değiştiğinde format, typecheck, test ve build; ardından tarayıcıda giriş, krallık/karakter seçimi, harita geçişi, sistem mesajı, wiki, mağaza ve 77924 eşya adı kontrolü.
9. Yeniden taramada eski oyuncu metni/amblem kalmadığını doğrula; tutulacak tarihsel kayıt, yazar atfı ve üçüncü taraf dosyalarını açık istisna olarak listele.

## Kapsam sınırı

Bu rapor yerel çalışma ağacını kapsar. Görsel incelemesi giriş/seçim arka planları, iki ikon, 14 yükleme karesi ve ilgili logo atlasları üzerinde yapıldı; bütün oyun dokularına OCR uygulanmadı. Sıkıştırılmış protoların/paketlerin içeriği, canlı host/kit/www/CDN kopyaları, VM ve canlı DB ayrıca incelenmedi. Bu nedenle rapor **dönüşümün tamamlandığı anlamına gelmez**; uygulanacak değişikliklerin doğrulanmış başlangıç envanteridir.
