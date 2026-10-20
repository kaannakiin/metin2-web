# Zırhçı ve market — ayrı NPC tasarımı

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

## 1. Zırh Satıcısı — 9002 / shop 2

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

### Önerim: tek zırhçıda işe yarayan başlangıç takıları

Mevcut gövde/kask/kalkan bandı korunabilir. İç item kısmını aşağıdaki hedef
seçkiye çıkaralım. Tüm +9'lar **rastgele efsunsuz**, takma seviyeleri aynı olur.
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

Bu öneri mevcut “25+ yalnız drop” kilidinde **takılara özel 33 seviyeye kadar
bir istisna** gerektirir. Karar verilince önce `PVP_HEDEF.md` güncellenmeli.
Silah/gövde bandı genişlemez. Abanoz +9'u doğrudan satmak fazla rahat gelirse,
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

## 2. Satıcı / market — 9003 / shop 3

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

## 3. Işınlanma yüzüğü — uygulanan düzeltme

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

1. Zırhçı: Abanoz/Yeşim tavanı ve +9/+6 tercihini netleştir; hedef stok/fiyat
   tablosu çıkar. 9008'de kalan ürünlerin rolünü açıkça belirle.
2. Market: günlük paketler, kayıp araç yedekleri ve Yang giderlerini netleştir.
3. Her NPC için yalnız ilgili shop satırlarını yedekle/güncelle; diğer
   tüccarları topluca seed SQL'i ile sıfırlama.

Yerel dayanak: `seed_shop_refine_pet.sql`, `update_mid_pvp_shop_plus9.sql`,
sunucu item protosu, `welcome.lua`, `move_ring.quest` ve canlı salt okunur
`player.shop` / `shop_item` karşılaştırması. Bu belge ilk iki NPC için tasarım
çalışmasıdır; Faz 3'ün tamamını bitmiş saymaz.
