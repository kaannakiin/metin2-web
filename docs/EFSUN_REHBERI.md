# Efsunlanabilen eşyalar ve bütün mevcut efsun havuzları

20 Ekim 2026. Bu belge **bizim dosyaların gerçek durumudur**; klasik
Metin2 ile aynı olduğu iddia edilmez. Normal tablonun 59 satırı canlı DB
ile bütün değer/yuva izinleri üzerinden eşleşti. 6–7 tablosunda 39 satır var.

## Hangi eşyalar efsunlanabiliyor?

| Eşya grubu | Sistem | Açıklama |
| --- | --- | --- |
| Kılıç, çift el, hançer, yay, çan, yelpaze | Normal 1–5 | Aynı silah havuzu; sabit proto bonusları tekrar gelmez |
| Gövde, kask, kalkan | Normal 1–5 | Her yuvanın izinleri ayrı |
| Bilezik, kolye, küpe, ayakkabı | Normal 1–5 | Her yuvanın izinleri ayrı |
| Tılsım | Ayrı normal havuz | Kod desteği açık; 1–99 içerikte her tılsım erişilebilir değildir |
| Gövde kostümü, saç, silah kostümü | Kostüm efsunu | Ayrı DB sütunları ve özel efsun araçları |
| Ok | Normal havuz yok | Mühimmat |
| Kemer, yüzük türü, kuşak, aura, binek/pet eşyası, olta/kazma | Normal 1–5 havuzu yok | Kendi proto, emiş veya sistem özellikleri olabilir |
| Simya taşları | Ayrı sistem | Ejderha taşı tablosu/arıtma; normal 1–5 tablosu değildir |

GM komutuyla zorla bonus basılabilmesi normal oyuncu efsunlama izni sayılmaz.
Kuşağa emilen silah özellikleri ve sokete takılan taşlar da normal efsunla
karıştırılmamalı. Tek tek eşyada efsun aracının ilave tür/seviye koşulları olabilir.

## Dolunay neden “Metinlere karşı güçlü” gösteriyordu?

- Sunucu APPLY 119 = `ATTBONUS_MEDI_PVM`: yalnız NPC hedeflerinde çalışan
  PvM ortalama zararı. Metinlere özel bir bonus değildir.
- Eski istemci APPLY 119 = `ATTBONUS_STONE`: aynı sayı farklı isimle çiziliyordu.
- Asıl metin bonusu sunucuda 112; eski istemcide 119 idi. 92 sonrası
  başka bonuslar da kaymıştı. İstemci kimlikleri sunucuyla hizalandı;
  paket biçimi/feature flag değiştirilmedi, oyuncu bonusları DB’den silinmedi.
- Sunucudaki `ENABLE_AVG_PVM_DISABLE` yolu, ortalamalı silahların doğal
  ortalamasını 72 yerine 119 ile üretiyor. Yani görüntü hatası dışında
  **klasik ortalama yerine PvM ortalama kullanan özel bir kural da var.**
  Bu yayında saldırı formülü veya mevcut item değerleri topluca değiştirilmedi.

[Resmî Dolunay sayfası](https://tr-wiki.metin2.gameforge.com/index.php?redirect=no&stable=0&title=Dolunay_K%C4%B1l%C4%B1c%C4%B1)
doğal ortalama/beceri çiftini açıklıyor. Güncel resmî oyunda
[Metin Taşı Karşısında Güçlü](https://tr-wiki.metin2.gameforge.com/index.php/Metin_Ta%C5%9F%C4%B1_Kar%C5%9F%C4%B1s%C4%B1nda_G%C3%BC%C3%A7l%C3%BC)
ayrı sistemlerde ve 6–7 efsunlarda bulunabiliyor; Dolunay’ın klasik
normal 1–5 havuzunda rastgele aynı şekilde bulunmasıyla eşdeğer değil.

## Tablo nasıl okunur?

Sayı: o eşya grubuna tablodan gelebilen **en yüksek değer**. “—”: bu
havuzdan gelemez. Soldaki beş değer, düşükten yükseğe efsun kademeleri;
bazı yuvalar üçüncü/dördüncü kademede sınırlandığı için daha düşük kalır.
Bağışıklıkta 1, özelliğin açık olmasıdır. Bir eşyanın protosunda zaten
bulunan veya mevcut normal efsunlarında bulunan aynı tür tekrar seçilmez.
Tablo bir eşyaya hepsinin birlikte gelebileceği anlamına gelmez: normal
slot toplamı 5. Doğal ortalama/beceri çifti de bu slotları kullanır.
Efsun seçim ağırlığı gerçek yüzde değildir; eldeki diğer efsunlar havuzu değiştirir.

## Normal 1–5: bütün ekipman yuvaları

| Efsun | 5 değer kademesi | Silah | Gövde | Bilezik | Ayakkabı | Kolye | Kask | Kalkan | Küpe | Tılsım |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Maks. HP | 500 / 1000 / 1500 / 2000 / 2500 | 2500 | 2500 | 2500 | 2500 | 2500 | 2500 | 2500 | 2500 | 2500 |
| Maks. SP | 10 / 20 / 30 / 40 / 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 |
| Canlılık | 2 / 4 / 6 / 8 / 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 |
| Zekâ | 2 / 4 / 6 / 8 / 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 |
| Güç | 2 / 4 / 6 / 8 / 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 |
| Çeviklik | 2 / 4 / 6 / 8 / 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 |
| Saldırı hızı % | 1 / 2 / 3 / 5 / 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 |
| Hareket hızı % | 2 / 4 / 6 / 10 / 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 |
| Büyü hızı % | 2 / 4 / 6 / 10 / 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 |
| HP yenileme % | 5 / 10 / 15 / 20 / 30 | — | 30 | 30 | 30 | 30 | 30 | 30 | 30 | 30 |
| SP yenileme % | 5 / 10 / 15 / 20 / 30 | — | 30 | 30 | 30 | 30 | 30 | 30 | 30 | 30 |
| Zehirleme % | 1 / 2 / 3 / 5 / 8 | 8 | — | — | — | — | — | — | — | — |
| Sersemletme % | 1 / 2 / 3 / 5 / 8 | 8 | — | — | — | — | — | — | — | — |
| Yavaşlatma % | 1 / 2 / 3 / 5 / 8 | 8 | — | — | — | — | — | — | — | — |
| Kritik % | 1 / 2 / 3 / 5 / 10 | 10 | 10 | 10 | 10 | 10 | 10 | 10 | 10 | 10 |
| Delici % | 1 / 2 / 3 / 5 / 10 | 10 | 10 | 10 | 10 | 10 | 10 | 10 | 10 | 10 |
| Yarı insanlara karşı % | 1 / 2 / 3 / 5 / 10 | 10 | 10 | 10 | 10 | 10 | 10 | 10 | 10 | 10 |
| Hayvanlara karşı % | 2 / 4 / 6 / 10 / 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 |
| Orklara karşı % | 2 / 4 / 6 / 10 / 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 |
| Mistiklere karşı % | 2 / 4 / 6 / 10 / 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 |
| Ölümsüzlere karşı % | 2 / 4 / 6 / 10 / 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 |
| Şeytanlara karşı % | 2 / 4 / 6 / 10 / 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 |
| HP emme % | 1 / 2 / 3 / 5 / 8 | 8 | — | — | — | — | — | — | — | — |
| SP emme % | 1 / 2 / 3 / 5 / 8 | 8 | — | — | — | — | — | — | — | — |
| SP çalma % | 1 / 2 / 3 / 5 / 8 | 8 | — | — | — | — | — | — | — | — |
| Yakın dövüş bloklama % | 2 / 4 / 6 / 8 / 10 | — | 10 | 10 | 10 | 10 | 10 | 10 | 10 | 10 |
| Oklardan korunma % | 2 / 4 / 6 / 8 / 10 | — | 10 | 10 | 10 | 10 | 10 | 10 | 10 | 10 |
| Kılıç savunması % | 1 / 2 / 3 / 5 / 10 | — | 10 | 10 | 10 | 10 | 10 | 10 | 10 | 10 |
| Çift el savunması % | 1 / 2 / 3 / 5 / 10 | — | 10 | 10 | 10 | 10 | 10 | 10 | 10 | 10 |
| Bıçak savunması % | 1 / 2 / 3 / 5 / 10 | — | 10 | 10 | 10 | 10 | 10 | 10 | 10 | 10 |
| Çan savunması % | 1 / 2 / 3 / 5 / 10 | — | 10 | 10 | 10 | 10 | 10 | 10 | 10 | 10 |
| Yelpaze savunması % | 1 / 2 / 3 / 5 / 10 | — | 10 | 10 | 10 | 10 | 10 | 10 | 10 | 10 |
| Ok savunması % | 1 / 2 / 3 / 5 / 10 | — | 10 | 10 | 10 | 10 | 10 | 10 | 10 | 10 |
| Ateş direnci % | 1 / 2 / 3 / 5 / 10 | — | 10 | 10 | 10 | 10 | 10 | 10 | 10 | 10 |
| Şimşek direnci % | 1 / 2 / 3 / 5 / 10 | — | 10 | 10 | 10 | 10 | 10 | 10 | 10 | 10 |
| Büyü direnci % | 1 / 2 / 3 / 5 / 10 | — | 10 | 10 | 10 | 10 | 10 | 10 | 10 | 10 |
| Rüzgâr direnci % | 1 / 2 / 3 / 5 / 10 | — | 10 | 10 | 10 | 10 | 10 | 10 | 10 | 10 |
| Yakın dövüş yansıtma % | 1 / 2 / 3 / 5 / 10 | — | 10 | — | 10 | — | 10 | 10 | — | 10 |
| Zehir direnci % | 1 / 2 / 3 / 5 / 10 | — | 10 | 10 | 10 | 10 | 10 | 10 | 10 | 10 |
| EXP bonusu % | 1 / 2 / 3 / 4 / 5 | — | — | — | 3 | 3 | 3 | 3 | 3 | 3 |
| Yang çift düşme şansı % | 1 / 2 / 3 / 4 / 5 | — | — | — | 3 | 3 | 3 | 3 | 3 | 3 |
| Eşya düşürme bonusu % | 1 / 2 / 3 / 4 / 5 | — | — | — | 3 | 3 | 3 | 3 | 3 | 3 |
| Sersemliğe bağışıklık | 1 / 1 / 1 / 1 / 1 | — | 1 | — | 1 | 1 | 1 | — | — | — |
| Yavaşlığa bağışıklık | 1 / 1 / 1 / 1 / 1 | — | 1 | — | 1 | 1 | 1 | — | — | — |
| Saldırı değeri | 5 / 10 / 15 / 20 / 30 | 30 | — | 30 | — | — | 30 | 30 | — | 30 |
| Savunma değeri | 5 / 10 / 15 / 20 / 30 | — | 30 | 30 | — | 30 | 30 | — | 30 | — |
| Beceri hasarı % | 2 / 4 / 6 / 8 / 10 | 10 | 10 | 10 | 10 | 10 | 10 | 10 | 10 | 10 |
| Ortalama zarar % | 2 / 4 / 6 / 8 / 10 | 10 | 10 | 10 | 10 | 10 | 10 | 10 | 10 | 10 |
| Beceri direnci % | 2 / 4 / 6 / 8 / 10 | — | 10 | 10 | 10 | 10 | 10 | 10 | 10 | 10 |
| Ortalama zarar direnci % | 2 / 4 / 6 / 8 / 10 | — | 10 | 10 | 10 | 10 | 10 | 10 | 10 | 10 |
| Savaşçıya karşı % | 1 / 2 / 3 / 5 / 10 | 10 | — | — | — | 10 | 10 | 10 | — | 10 |
| Ninjaya karşı % | 1 / 2 / 3 / 5 / 10 | 10 | — | — | — | 10 | 10 | 10 | — | 10 |
| Suraya karşı % | 1 / 2 / 3 / 5 / 10 | 10 | — | — | — | 10 | 10 | 10 | — | 10 |
| Şamana karşı % | 1 / 2 / 3 / 5 / 10 | 10 | — | — | — | 10 | 10 | 10 | — | 10 |
| Savaşçı direnci % | 1 / 2 / 3 / 5 / 10 | — | 10 | 10 | 10 | 10 | 10 | 10 | 10 | 10 |
| Ninja direnci % | 1 / 2 / 3 / 5 / 10 | — | 10 | 10 | 10 | 10 | 10 | 10 | 10 | 10 |
| Sura direnci % | 1 / 2 / 3 / 5 / 10 | — | 10 | 10 | 10 | 10 | 10 | 10 | 10 | 10 |
| Şaman direnci % | 1 / 2 / 3 / 5 / 10 | — | 10 | 10 | 10 | 10 | 10 | 10 | 10 | 10 |
| Canavarlara karşı % | 2 / 4 / 6 / 10 / 20 | 20 | — | — | — | 20 | 20 | 20 | — | 20 |

## Kostüm havuzları

| Efsun | 5 değer kademesi | Kostüm | Saç | Silah kostümü |
| --- | --- | --- | --- | --- |
| Maks. HP | 500 / 1000 / 1500 / 2000 / 2500 | 2500 | 2500 | 2500 |
| Maks. SP | 10 / 20 / 30 / 40 / 50 | 50 | 50 | 50 |
| Canlılık | 2 / 4 / 6 / 8 / 12 | 12 | 12 | 12 |
| Zekâ | 2 / 4 / 6 / 8 / 12 | 12 | 12 | 12 |
| Güç | 2 / 4 / 6 / 8 / 12 | 12 | 12 | 12 |
| Çeviklik | 2 / 4 / 6 / 8 / 12 | 12 | 12 | 12 |
| Saldırı hızı % | 1 / 2 / 3 / 5 / 8 | 8 | 8 | 8 |
| Hareket hızı % | 2 / 4 / 6 / 10 / 20 | 20 | 20 | 20 |
| Büyü hızı % | 2 / 4 / 6 / 10 / 20 | 20 | 20 | 20 |
| HP yenileme % | 5 / 10 / 15 / 20 / 30 | 30 | 30 | — |
| SP yenileme % | 5 / 10 / 15 / 20 / 30 | 30 | 30 | — |
| Zehirleme % | 1 / 2 / 3 / 5 / 8 | — | — | 8 |
| Sersemletme % | 1 / 2 / 3 / 5 / 8 | — | — | 8 |
| Yavaşlatma % | 1 / 2 / 3 / 5 / 8 | — | — | 8 |
| Kritik % | 1 / 2 / 3 / 5 / 10 | 10 | 10 | 10 |
| Delici % | 1 / 2 / 3 / 5 / 10 | 10 | 10 | 10 |
| HP emme % | 1 / 2 / 3 / 5 / 8 | — | — | 8 |
| SP emme % | 1 / 2 / 3 / 5 / 8 | — | — | 8 |
| SP çalma % | 1 / 2 / 3 / 5 / 8 | — | — | 8 |
| Yakın dövüş bloklama % | 2 / 4 / 6 / 8 / 10 | 10 | 10 | — |
| Oklardan korunma % | 2 / 4 / 6 / 8 / 10 | 10 | 10 | — |
| Canavarlara karşı % | 2 / 4 / 6 / 10 / 20 | — | — | 20 |

Kostümde kod desteği ve DB izinleri mevcut. “Kostüm güç vermez” tasarım
hedefiyle bu gerçek izinler aynı şey değildir; erişilebilir kostüm araçları
ayrı kontrol edilmeden bu sütunlar yokmuş gibi kabul edilmemeli.

## Klasik düzenden sapan ve ayrıca karar gerekenler

- Normal havuzda beceri hasarı ve ortalama zarar çoğu yuvaya açılmış.
  Bu yüzden doğal ortalamalı silahlar dışında da bu türler seçilebilir.
- Birçok tür neredeyse bütün ekipman yuvalarında serbest: HP, stat,
  hız, yarı insan ve yaratık bonusları gibi. Klasik yuva sınırları değil.
- Sınıfa karşı saldırı ve sınıf direnci normal 1–5 havuzunda bulunuyor.
  Klasik düzenle karşılaştırılması gereken ayrı bir PvP güç katmanı.
- Metin/boss bonusu normal DB havuzunda yok. Dolunay’daki metin yazısı
  yukarıdaki kimlik uyuşmazlığı; böyle bir normal satırın kanıtı değil.
- Seed içinde birçok satır `approx` olarak işaretli. Canlıyla eşleşmesi
  bu kuralların klasik wikiye uygun olduğu anlamına gelmez.

Bu inceleme sırasında oyuncu efsunları ve normal/rare izin tablosu topluca
silinmedi veya değişmedi. Klasik havuza geçiş, mevcut eşyalara ne olacağı
ile birlikte ayrı bir dengeleme kararı gerektiriyor.

## 6–7 efsun: yapılandırılmış havuz

Tasarım hedefinde kapalı. Kod/DB tablosunun varlığı tek başına normal
oyuncuya erişim verildiğini göstermez; GM/özel araç yolları ayrıdır.
Aşağıdaki 39 satır normal 1–5 tablosuna karıştırılmamalı.

| Efsun | 5 değer kademesi | Silah | Gövde | Bilezik | Ayakkabı | Kolye | Kask | Kalkan | Küpe | Tılsım |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Maks. HP | 500 / 1000 / 1500 / 2000 / 2500 | 2500 | 2500 | 2500 | 2500 | 2500 | 2500 | 2500 | 2500 | 2500 |
| Maks. SP | 10 / 20 / 30 / 40 / 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 |
| Canlılık | 2 / 4 / 6 / 8 / 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 |
| Zekâ | 2 / 4 / 6 / 8 / 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 |
| Güç | 2 / 4 / 6 / 8 / 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 |
| Çeviklik | 2 / 4 / 6 / 8 / 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 |
| Saldırı hızı % | 1 / 2 / 3 / 5 / 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 |
| Hareket hızı % | 2 / 4 / 6 / 10 / 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 |
| Büyü hızı % | 2 / 4 / 6 / 10 / 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 |
| HP yenileme % | 5 / 10 / 15 / 20 / 30 | — | 30 | 30 | 30 | 30 | 30 | 30 | 30 | 30 |
| SP yenileme % | 5 / 10 / 15 / 20 / 30 | — | 30 | 30 | 30 | 30 | 30 | 30 | 30 | 30 |
| Zehirleme % | 1 / 2 / 3 / 5 / 8 | 8 | — | — | — | — | — | — | — | — |
| Sersemletme % | 1 / 2 / 3 / 5 / 8 | 8 | — | — | — | — | — | — | — | — |
| Yavaşlatma % | 1 / 2 / 3 / 5 / 8 | 8 | — | — | — | — | — | — | — | — |
| Kritik % | 1 / 2 / 3 / 5 / 10 | 10 | 10 | 10 | 10 | 10 | 10 | 10 | 10 | 10 |
| Delici % | 1 / 2 / 3 / 5 / 10 | 10 | 10 | 10 | 10 | 10 | 10 | 10 | 10 | 10 |
| Yarı insanlara karşı % | 1 / 2 / 3 / 5 / 10 | 10 | 10 | 10 | 10 | 10 | 10 | 10 | 10 | 10 |
| Hayvanlara karşı % | 2 / 4 / 6 / 10 / 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 |
| Orklara karşı % | 2 / 4 / 6 / 10 / 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 |
| Mistiklere karşı % | 2 / 4 / 6 / 10 / 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 |
| Ölümsüzlere karşı % | 2 / 4 / 6 / 10 / 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 |
| Şeytanlara karşı % | 2 / 4 / 6 / 10 / 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 |
| HP emme % | 1 / 2 / 3 / 5 / 8 | 8 | — | — | — | — | — | — | — | — |
| SP emme % | 1 / 2 / 3 / 5 / 8 | 8 | — | — | — | — | — | — | — | — |
| SP çalma % | 1 / 2 / 3 / 5 / 8 | 8 | — | — | — | — | — | — | — | — |
| Yakın dövüş bloklama % | 2 / 4 / 6 / 8 / 10 | — | 10 | 10 | 10 | 10 | 10 | 10 | 10 | 10 |
| Oklardan korunma % | 2 / 4 / 6 / 8 / 10 | — | 10 | 10 | 10 | 10 | 10 | 10 | 10 | 10 |
| Kılıç savunması % | 1 / 2 / 3 / 5 / 10 | — | 10 | 10 | 10 | 10 | 10 | 10 | 10 | 10 |
| Çift el savunması % | 1 / 2 / 3 / 5 / 10 | — | 10 | 10 | 10 | 10 | 10 | 10 | 10 | 10 |
| Bıçak savunması % | 1 / 2 / 3 / 5 / 10 | — | 10 | 10 | 10 | 10 | 10 | 10 | 10 | 10 |
| Çan savunması % | 1 / 2 / 3 / 5 / 10 | — | 10 | 10 | 10 | 10 | 10 | 10 | 10 | 10 |
| Yelpaze savunması % | 1 / 2 / 3 / 5 / 10 | — | 10 | 10 | 10 | 10 | 10 | 10 | 10 | 10 |
| Ok savunması % | 1 / 2 / 3 / 5 / 10 | — | 10 | 10 | 10 | 10 | 10 | 10 | 10 | 10 |
| Ateş direnci % | 1 / 2 / 3 / 5 / 10 | — | 10 | 10 | 10 | 10 | 10 | 10 | 10 | 10 |
| Şimşek direnci % | 1 / 2 / 3 / 5 / 10 | — | 10 | 10 | 10 | 10 | 10 | 10 | 10 | 10 |
| Büyü direnci % | 1 / 2 / 3 / 5 / 10 | — | 10 | 10 | 10 | 10 | 10 | 10 | 10 | 10 |
| Rüzgâr direnci % | 1 / 2 / 3 / 5 / 10 | — | 10 | 10 | 10 | 10 | 10 | 10 | 10 | 10 |
| Yakın dövüş yansıtma % | 1 / 2 / 3 / 5 / 10 | — | 10 | — | 10 | — | 10 | 10 | — | 10 |
| Zehir direnci % | 1 / 2 / 3 / 5 / 10 | — | 10 | 10 | 10 | 10 | 10 | 10 | 10 | 10 |

## Teknik dayanak

`seed_item_attr.sql`; `CItem::GetAttributeSetIndex`, `HasAttr`,
`PutAttributeWithLevel`, `ChangeAttribute`; `item_addon.cpp`;
sunucu `length.h` ve istemci `GameLib/ItemData.h`. Canlı normal
tablo TSV SHA256: `dfe1f1ac3eae6233fb1d3c0b8311d742de33804fde07e5a7bd12f33d38fdbf3c`.
Üretim: `python3 platform/tools/attribute_catalogue.py`.
