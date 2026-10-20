# Silahçı, zırhçı ve market — ayrı NPC tasarımı

20 Ekim 2026. Hedef: klasik 1–99 orta-kolay; başlangıç rahat, üst ekipman farmda.
**Mağaza tabloları öneridir; henüz shop SQL'ine veya canlı mağazalara uygulanmadı.**
Işınlanma yüzüğünün başlangıç teslimi ise ayrı bir düzeltme olarak canlıdır.

## Araştırma ve görsel referans

![Turks2 tanıtımında ayrı silahçı, zırhçı ve satıcı pencereleri](https://www.itempol.com/upload/Haberler/turks2/11.png)

[Turks2 tanıtımı](https://www.itempol.com/haber/815-turks2-1-99-orta-emek-12-12-2025-de-aciliyor.html)
NPC görseli tarayıcıda açılıp incelendi. Ekipman ve tüketim pencereleri ayrı;
ikonlardan kesin eşya adı, seviye veya fiyat çıkarılmadı. Bu bir tanıtım
görüntüsüdür; sunucunun bugünkü canlı stokunu kanıtlamaz.

| Kaynak                                                                                                                                 | Doğrudan görülen yapı                                                                                                                                                    | Bizim için sonuç                                                                                        |
| -------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------- |
| [Narnia'nın kendi tanıtımı](https://www.narniamt2.com/) ve [mağaza verisi](https://www.narniamt2.com/themes/default/js/market_data.js) | Zırhçı 36 satır, ayrı Takı Satıcısı 29 satır, Satıcı 30 satır. Takıcıda düşük kademe +9 ekipman; markette hız iksirleri, yüzük, dedektör, pelerin ve efsun araçları var. | Ekipman ve günlük sarf ayrımı kullanışlı. Fiyatları ve satılan zindan biletlerini kopyalamayalım.       |
| [MarkMt2 kendi NPC rehberi](https://wiki.markmt2.com/Detail/Npc/zirh-saticisi/9002)                                                    | Zırhçıda düşük seviye +0 gövdeler listeleniyor.                                                                                                                          | Her PvP aynı modeli kullanmıyor; +0 satışı bizim erken +9 hedefimize uymaz.                             |
| [Faraza2 kendi tanıtımı](https://tanitim.faraza2.com/)                                                                                 | Üst takılar ve özel farm ekipmanı üretim paneline bağlanmış.                                                                                                             | Üst takıları dükkândan ayrı edinim hattında tutma örneği. Özel itemlerini ve para ölçeğini taşımayalım. |
| [Resmî Zırh Satıcısı](https://tr-wiki.metin2.gameforge.com/index.php/Z%C4%B1rh_Sat%C4%B1c%C4%B1s%C4%B1)                                | Klasik ekipman tüccarı referansı.                                                                                                                                        | NPC kimliği korunur; resmî zor başlangıç ekonomisi aynen alınmaz.                                       |

Arama sonucunda görünen bazı eski Harbi/Hard görselleri doğrudan açıldığında
404 veya park sayfası döndü. Bunlar kullanılabilir görsel kanıt sayılmadı.

## 1. Silah Satıcısı — 9001 / shop 1; 9007 / shop 6

Canlı DB ile SQL eşleşiyor: ana silahçı **10 satır**, ikinci silahçı **9 satır**.
İkinci NPC'nin ürünleri ana NPC'de görünmüyor. Aynı tüccara gidip sonraki
silahı bulamama sorununun bir kısmı bu bölünmeden kaynaklanıyor.

| Silah türü | Ana silahçıdaki +9                      | İkinci silahçıdaki +9              |
| ---------- | --------------------------------------- | ---------------------------------- |
| Tek el     | Bambu Kılıcı, 49 / seviye 15            | Geniş Kılıç, 59 / seviye 20        |
| Hançer     | Kobra Hançeri, 1019 / seviye 10         | Makas Hançer, 1029 / seviye 20     |
| Yay        | Harp Yayı, 2039 / seviye 15             | Atsırtı Uzun Yay, 2049 / seviye 20 |
| Çift el    | Örümcek Mızrağı, 3039 / seviye 15       | Kargı, 3049 / seviye 20            |
| Çan        | Gümüş Çan, 5019 / seviye 15             | Altın Çan, 5029 / seviye 20        |
| Yelpaze    | Turna Kanadı, 7039 / seviye 15          | Tavuskuşu, 7049 / seviye 20        |
| Ek kayıt   | Amija, 4009 / seviye 5; proto'da hançer | Yok                                |
| Mühimmat   | Tahta/Bambu/Taş Ok ×50                  | Demir/Çelik/Gümüş Ok ×50           |

“Ana silahçı yalnız 15 seviye” açıklaması da tam doğru değil: Kobra 10,
Amija 5 seviye. Amija ayrı bir silah sınıfı değildir; yinelenen düşük kademe
hançer olarak stoktan çıkarılması değerlendirilebilir.

### PvP karşılaştırması ve öneri

[Narnia'nın mağaza verisi](https://www.narniamt2.com/themes/default/js/market_data.js)
silahları iki gruba ayırıyor: 43 satırlık ilk grup ve 41 satırlık 32–60 grubu.
Normal silahları +9 satıyor; Dolunay ve Kırmızı Demir de ilk grupta.
[MarkMt2 rehberi](https://wiki.markmt2.com/Detail/Npc/silah-saticisi/9001)
aynı erken silah ailelerini +0 listeliyor.
[Rohan2 rehberi](https://wiki.rohan2.global/Detail/Npc/silah-saticisi/9001)
erken silahları ve 200'lük okları listeliyor; görünen adlarda +9 yazmasa da
bağlantı VNUM'ları 49/69/5029 gibi +9 kayıtlarına gidiyor. Yalnız görünen ada
bakarak geliştirme seviyesi çıkarmamak gerekiyor.

**Önerim:** tek ana silahçıda başlangıç ve 20–25 kademe seçenekleri erişilebilir
olsun. Ayrı konuşma/mağaza sayfaları: “Başlangıç”, “20–25 seviye”, “Oklar”.
Mevcut altı silah ailesi korunur; yalnız kılıç ve çift el çalışılmaz.

| Önerilen ek +9 silah | VNUM | Seviye |
| -------------------- | ---- | ------ |
| Gümüş Kılıç          | 69   | 25     |
| Kısa Bıçak           | 4029 | 25     |
| Atsırtı Savaş yayı   | 2059 | 25     |
| Savaş Tırpanı        | 3059 | 25     |
| Su Yelpazesi         | 7059 | 25     |

Çanda bu protoda 25 seviye karşılık yok; Altın Çan 20'de kalır. Sırf tabloyu
eşitlemek için yeni item veya seviye icat edilmez. Bütün ürünler efsunsuz +9;
ortalama/beceri bonusu üretilmez. Okları 200'lük paketlere çıkarmayı öneriyorum.

Dolunay, Kırmızı Demir, Siyah Yaprak, Antik Çan ve diğer 30 ortalamalı aileler
farmda kalmalı. 65/70 silahlar ve Zehir dahil 75 ailesi de mevcut metin/boss
ediniminde kalmalı. Bu, Narnia'nın daha geniş stokundan bilinçli ayrıldığımız
tasarım önerisidir; diğer PvP'lerin ortak kuralı gibi sunulmamalı.

## 2. Zırh Satıcısı — 9002 / shop 2

Canlı DB, seed ve +9 güncelleme SQL'i karşılaştırıldı. **19 satır mevcut.**

| Grup     | Şu an satılan                     |
| -------- | --------------------------------- |
| Gövde    | Dört sınıfın 18 seviye gövdesi +9 |
| Kask     | Dört sınıfın başlangıç kaskı +9   |
| Kalkan   | Savaş Kalkanı +9                  |
| Bilezik  | Tahta, Bakır, Gümüş +9            |
| Ayakkabı | Deri, Bambu Derisi, Tahta +9      |
| Kolye    | Tahta, Bakır +9                   |
| Küpe     | Tahta, Bakır +9                   |

İç item tamamen eksik değil; seçenekler çok erken seviyede kalıyor.
9008 / shop 7'de ayrıca Demir/Zincir/Alaycı/Anka kaskları, Beşgen ve Parlak
kalkanlar, Altın Bilezik, Gümüş/Altın Kolye ve Küpe +9 var. Önce bunu hesaba
katalım; aynı stokları iki ayrı NPC'ye yaymak oyuncuya arama işi çıkarıyor.

### Gövde zırhları — dört sınıfın tüm basamakları

Önceki sürüm bu kısmı eksik bıraktı. “Mevcut gövde bandı korunsun” önerisi,
oyuncuyu 18 seviye zırhta bıraktığı için yeniden değerlendirildi.
**Yeni önerim: dört sınıfta 18, 26, 34 ve 42 seviye zırhlar efsunsuz +9
satılsın; 48 ve sonrası farmda kalsın.** Böylece zırhçı gerçek yükseltme sunar,
üst içerikteki zırh ödülleri de değerini korur.

| Seviye | Savaşçı         | Ninja                  | Sura           | Şaman                 | Önerilen erişim   |
| ------ | --------------- | ---------------------- | -------------- | --------------------- | ----------------- |
| 18     | Kaplan Plaka    | Koyu Kırmızı Takım     | Kötü Şans      | Pembe Elbise          | NPC +9; zaten var |
| 26     | Aslan Plaka     | Kırmızı Karınca Takım  | Hayalet Plaka  | Sevgi Elbisesi        | NPC +9; eklenecek |
| 34     | Ölümcül Plaka   | Karınca Aslan Takımı   | Yin-Yang       | Sema Elbisesi         | NPC +9; eklenecek |
| 42     | Ejderha Plaka   | Ninja Takımı           | Mistik Plaka   | Güneş Elbisesi        | NPC +9; eklenecek |
| 48     | Mavi Taş        | Genç Ejderha Takımı    | Belirsiz Plaka | Manevi Elbise         | Farm              |
| 54     | Altın Taş       | Öldürücü Rüzgâr Takımı | Hayalet Surat  | Turuncu Kedi Elbisesi | Farm              |
| 61     | Ejderha Tanrısı | Küpeçiçeği Takım       | Ruh Plaka      | Soylu Kadın Elbisesi  | Farm              |

Adlar ve seviyeler bizim protodan alındı. Eklenecek +9 VNUM'lar:
26 için `11239 / 11439 / 11639 / 11839`; 34 için
`11249 / 11449 / 11649 / 11849`; 42 için `11259 / 11459 / 11659 / 11859`.
Üst 66 ailesi de dükkâna alınmaz; mevcut metin/boss ilerlemesi korunur.

Alternatif daha kolay PvP düzeni, zırhları 61'e kadar +9 satmaktır. Narnia'nın
tanıtım verisinde böyle geniş bir stok var. Bizde 48–61 ekipman avını önemli
ölçüde azaltacağı için **ilk önerim 42 tavanı**; 61 satışı ayrı tasarım kararıdır.

### Kask ve kalkan — gövdeden ayrı değerlendirme

| Grup         | NPC önerisi                                                                                          | Farmda kalacak                             |
| ------------ | ---------------------------------------------------------------------------------------------------- | ------------------------------------------ |
| Kask         | Dört sınıfın başlangıç ve 21 seviye kaskları +9; 21'likler shop 7'den ana zırhçıya erişilebilir olur | 41 ve üstü                                 |
| Kalkan       | Savaş Kalkanı ve Beşgen Kalkan +9; Beşgen shop 7'de mevcut                                           | Siyah Yuvarlak 41, dört 61 kalkanı ve üstü |
| Eski ek ürün | Shop 7'deki Parlak Kalkan ayrıca incelensin                                                          | Otomatik olarak yeni seçkiye taşınmasın    |

### İç itemler — takı ve ayakkabı seçkisi

Gövde/kask/kalkan yukarıdaki ayrı tablolara göre ele alınır. İç item kısmını
aşağıdaki hedef seçkiye çıkaralım. Tüm +9'lar **rastgele efsunsuz**, takma seviyeleri aynı olur.
Başlangıç hediyesindeki özel bonuslar dükkân ürünlerine taşınmaz.

| Yuva     | Hedef stok                                             | Değişiklik                                                |
| -------- | ------------------------------------------------------ | --------------------------------------------------------- |
| Bilezik  | Tahta, Bakır, Gümüş, Altın, Yeşim Taşı +9              | Altın shop 7'de; ana zırhçıya taşınabilir. Yeşim eklenir. |
| Kolye    | Tahta, Bakır, Gümüş, Altın, Yeşim Taşı +9              | Gümüş/Altın shop 7'de. Yeşim eklenir.                     |
| Küpe     | Tahta, Bakır, Gümüş, Altın, Yeşim Taşı, Abanoz +9      | İlk iki zaten var. Son iki yeni seçenek.                  |
| Ayakkabı | Deri, Bambu Derisi, Tahta, Altın Bezeli, Deri Çizme +9 | İlk üç zaten var. Son iki eklenir.                        |

**Abanoz STR/HP, Altın INT, Yeşim Taşı DEX/SP seçeneği sunar.** Tek bir takıyı
bütün sınıfların zorunlu başlangıcı yapmayalım.
Gümüş Bilezik de düşük seviyede kullanışlı bir HP seçeneği olarak kalır.

Uygulama adayı kimlikler sunucunun gerçek protosundan doğrulandı:

| Yeni ürün                | VNUM  | Takma seviyesi |
| ------------------------ | ----- | -------------- |
| Yeşim Taşı Bilezik +9    | 14089 | 28             |
| Altın Bezeli Ayakkabı +9 | 15069 | 23             |
| Deri Çizme +9            | 15089 | 29             |
| Yeşim Taşı Kolye +9      | 16089 | 28             |
| Yeşim Taşı Küpe +9       | 17089 | 28             |
| Abanoz Küpe +9           | 17109 | 33             |

Bu belge mevcut “25+ yalnız drop” kilidini değiştirecek öneriler içerir:
normal silahlar 25, gövdeler 42, takılar 33 seviyeye kadar NPC erişimi.
Karar verilince önce `PVP_HEDEF.md` güncellenmeli; henüz yürürlüğe girmedi.
Abanoz +9'u doğrudan satmak fazla rahat gelirse,
ikinci seçenek Abanoz/Yeşim'i +6 satıp +9 geliştirmesini oyuncuya bırakmaktır.
Ben orta-kolay hedef için efsunsuz +9 seçeneğini öneriyorum.

### Farmda kalmasını önerdiklerim

| Grup                                          | Gerekçe                                 |
| --------------------------------------------- | --------------------------------------- |
| Beyaz Altın ve üst orta kademe takılar        | Başlangıçtan sonraki yükseltme hedefi   |
| Cennetin Gözyaşı ailesi                       | Metin/boss ödülünün ve ticaretin değeri |
| Ruh Kristali ailesi                           | Üst ekipman hedefi                      |
| Mest Eden, Anka, Ateş Kuşu ve üst ayakkabılar | Duruma göre ekipman arama ve geliştirme |
| 61 kalkanları, üst kasklar, 61/66 gövdeler    | Mevcut içerik ve ilerleme bandı         |

Satış fiyatlarını bu tur kesinleştirmedim. Yeni adayların mevcut proto
alış/satış değerleri oyuncu ekonomisi için hazırlanmış bir mağaza tarifesi
sayılmaz. Mağaza uygulanırken geri satış hesabı, adet ve başlangıç Yang'ı
birlikte kontrol edilmeli; rastgele “diğer PvP'de 1M” kopyalanmamalı.

### Mağazaya sığma ve oyuncunun erişimi

Standart mağaza penceresi 40 hücre; eşyalar boyları kadar hücre kullanıyor.
16 gövde zırhı 32 hücre kullanır ve tek pencereye sığar. Kask, kalkan ve
takılar da aynı pencereye eklenince sınır aşılır; bütün önerileri bir SQL
listesine doldurmak ürünlerin kaybolmasına yol açabilir.
Ana zırhçıda ayrı konuşma/mağaza sayfaları öneriyorum:
“Zırhlar”, “Kask ve kalkan”, “İç itemler”.
Gerçek proto boylarıyla önerilen seçki: gövdeler 16 ürün / 32 hücre,
kask-kalkan 10 ürün / 10 hücre, iç itemler 21 ürün / 21 hücre.
Silahçının 20–25 seçkisi 11 ürün / 19 hücre kullanır.
Her sayfa kurulmadan gerçek item boylarıyla yerleşimi hesaplanmalı.
Mevcut istemciye yeni bir sekme sistemi gerekmeden NPC konuşmasından ayrı
shop kimlikleri açılabilir; shop kimlikleri uygulamada çakışmasız seçilmeli.
9008 ürünleri taşınacaksa önce yeni erişim tamamlanmalı, ardından eski stok
kararı verilmeli. Bu araştırmada hiçbir mağaza veya NPC kaldırılmadı.

## 3. Satıcı / market — 9003 / shop 3

Canlıda **9 satır**: Şehre Dönüş, Geri Dönüş; küçük/orta/büyük kırmızı ve mavi
iksirler; Paket. Her ürün bir adet satılıyor. Başlangıçta verilen hız iksirleri,
pelerin ve dedektör için burada devam/yedek erişimi yok.

| Grup                | Önerilen ürün                           | Paket / erişim önerisi                                                         |
| ------------------- | --------------------------------------- | ------------------------------------------------------------------------------ |
| Günlük sarf         | Büyük kırmızı/mavi iksir, 27003 / 27006 | 200'lük paket; mevcut küçük/orta seçenekler kalabilir                          |
| Hareket ve saldırı  | Büyük yeşil/mor iksir, 27102 / 27105    | 50'lik; başlangıçta verilen aynı aile                                          |
| Ulaşım              | Şehre/Geri Dönüş, 22000 / 22010         | 10'luk                                                                         |
| Başlangıç kolaylığı | Cesaret Pelerini, 70038                 | Önce gerçek kullanım/tüketim davranışına uygun adet; sonsuz olduğu varsayılmaz |
| Kayıp araç yedeği   | Işınlanma Yüzüğü 40004, dedektör 27989  | Birer adet, düşük sabit Yang; ilk ücretsiz teslimden ayrı                      |
| Ticaret             | Paket, 50200                            | Bir adet; mevcut erişim korunur                                                |
| Geliştirme          | Kutsama Kağıdı, 25040                   | Pahalı bir güvence seçeneği olarak ayrıca değerlendirilsin                     |

**Efsun Nesnesi 71084 ve Arttırma Kağıdı 71085** başka PvP marketlerinde var;
bizde doğrudan ucuz/sınırsız satış metin farmının değerini düşürür. İlk mağaza
revizyonunda eklememeyi öneriyorum. Gerekirse sınırlı rahatlık ve Yang gideri
olarak ayrıca fiyatlandırırız.

BK, Ruh Taşı, Münzevi, Kötü Ruh Kovma ve zindan anahtarlarını aynı sepete
koymayalım. Bunlar G/P hızını ve az önce kurulan boss zincirini değiştirir.
Özellikle Kıvrık Anahtar, Küçülen Kafa, Kraliçe Zehri ve Kan Taşı için son
belirlenen boss kaynakları korunmalı. Karar verilmeden markete eklenmedi.

## 4. Işınlanma yüzüğü — uygulanan düzeltme

Eksik, yüzüğün kullanılmasında değildi: 40004 için `move_ring` görevi canlıda
derlenmişti, ancak `welcome` hediyeleri arasında yüzük yoktu. Proto'daki
görünen adı “Eekin Yüzüğü”; kullanım menüsü mevcut ışınlanma menüsüdür.

`starter_ring` ayrı teslim görevi yeni/eski bütün karakterleri kapsar:

- Girişten üç saniye sonra kontrol; yüzük varsa ikinci kopya verilmez.
- Yüzük yoksa ve bir hücre boşsa bir adet verir, envantere geçtiğini kontrol eder.
- Teslim tamamlanınca görev kapanır; satıp/atıp tekrar girişte bedava çoğaltılamaz.
- Envanter doluysa sonraki girişte veya Satıcı'nın “Isinlanma yuzugumu al”
  konuşmasında tekrar denenir. Eski başlangıç ekipmanı yeniden verilmez.
- Haritalar, yüzüğün mevcut menüsü ve zindan erişim zinciri değişmez.

**Canlı sürüm:** `20261020-165717`. Kaynak + derlenmiş görev yedeklenerek
kuruldu. Altı servis süreci ve altı port sağlıklı; oyun testi kullanıcıda.

## Ayrı çalışma sırası

1. Silahçı: altı silah ailesi, 20–25 normal silah tavanı ve 200'lük oklar.
   Ortalamalı 30 silahların farmda kalmasını netleştir.
2. Zırhçı: dört sınıf için 42 seviye gövde tavanı; kask/kalkan ve iç item
   sayfalarını ayrı netleştir. 9008'in rolü ve gerçek hücre yerleşimi hesaplansın.
3. Market: günlük paketler, kayıp araç yedekleri ve Yang giderlerini netleştir.
4. Her NPC için yalnız ilgili shop satırlarını yedekle/güncelle; diğer
   tüccarları topluca seed SQL'i ile sıfırlama.

Yerel dayanak: `seed_shop_refine_pet.sql`, `update_mid_pvp_shop_plus9.sql`,
sunucu item protosu, `welcome.lua`, `move_ring.quest` ve canlı salt okunur
`player.shop` / `shop_item` karşılaştırması. Bu belge üç ana NPC için tasarım
çalışmasıdır; Faz 3'ün tamamını bitmiş saymaz.
