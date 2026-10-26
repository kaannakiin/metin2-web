# Efsunlanabilen eşyalar ve bütün mevcut efsun havuzları

22 Ekim 2026. Bu belge **repo seed verisini** gösterir; canlıya kurulum
kanıtı değildir. 45 normal efsun klasik yuvalara ve sabit değerlere
çekildi; HP 3000. 14 klasik dışı türün rastgele izinleri kapatıldı;
39 nadir satır korundu. Kalan 45 türün kostüm/tılsım izinleri korunur; değerleri bu
yuvalarda da sabittir. Ayrıntı: [uygulama notu](EFSUN_NORMAL_DUZENLEME.md).

Sonraki tasarım kararı tılsım ve saç kostümünü kapatıyor; tabloda
bu sütunların bulunması oynanışta açık olacakları anlamına gelmez.
[Yeni kapsam](BASLANGIC_KALICI_DESTEK_TASARIMI.md).

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
havuzdan gelemez. Soldaki beş değer efsun kademeleridir. Düzeltilen
45 normal türde beşi de aynıdır; seçilen kademe sonucu değiştirmez.
Kapalı 14 türün eski değerleri saklanır; hiçbir normal yuvada seçilmezler.
Nadir havuz kendi kademelerini korur.
Bağışıklıkta 1, özelliğin açık olmasıdır. Bir eşyanın protosunda zaten
bulunan veya mevcut normal efsunlarında bulunan aynı tür tekrar seçilmez.
Tablo bir eşyaya hepsinin birlikte gelebileceği anlamına gelmez: normal
slot toplamı 5. Doğal ortalama/beceri çifti de bu slotları kullanır.
Efsun seçim ağırlığı gerçek yüzde değildir; eldeki diğer efsunlar havuzu değiştirir.

## Normal 1–5: bütün ekipman yuvaları

| Efsun | 5 değer kademesi | Silah | Gövde | Bilezik | Ayakkabı | Kolye | Kask | Kalkan | Küpe | Tılsım |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Maks. HP | 3000 / 3000 / 3000 / 3000 / 3000 | — | 3000 | 3000 | 3000 | 3000 | — | — | — | 3000 |
| Maks. SP | 80 / 80 / 80 / 80 / 80 | — | 80 | 80 | 80 | 80 | — | — | — | 80 |
| Canlılık | 12 / 12 / 12 / 12 / 12 | 12 | — | — | — | — | — | 12 | — | 12 |
| Zekâ | 12 / 12 / 12 / 12 / 12 | 12 | — | — | — | — | — | 12 | — | 12 |
| Güç | 12 / 12 / 12 / 12 / 12 | 12 | — | — | — | — | — | 12 | — | 12 |
| Çeviklik | 12 / 12 / 12 / 12 / 12 | 12 | — | — | — | — | — | 12 | — | 12 |
| Saldırı hızı % | 8 / 8 / 8 / 8 / 8 | — | — | — | 8 | — | 8 | — | — | 8 |
| Hareket hızı % | 20 / 20 / 20 / 20 / 20 | — | — | — | — | — | — | — | 20 | 20 |
| Büyü hızı % | 20 / 20 / 20 / 20 / 20 | 20 | 20 | — | — | — | — | — | — | 20 |
| HP yenileme % | 30 / 30 / 30 / 30 / 30 | — | — | — | — | 30 | 30 | — | — | 30 |
| SP yenileme % | 30 / 30 / 30 / 30 / 30 | — | — | — | — | 30 | 30 | — | — | 30 |
| Zehirleme % | 8 / 8 / 8 / 8 / 8 | 8 | — | — | — | — | 8 | — | — | — |
| Sersemletme % | 8 / 8 / 8 / 8 / 8 | 8 | — | — | 8 | 8 | — | — | — | — |
| Yavaşlatma % | 8 / 8 / 8 / 8 / 8 | 8 | — | — | 8 | — | — | — | — | — |
| Kritik % | 10 / 10 / 10 / 10 / 10 | 10 | — | — | 10 | 10 | — | — | — | 10 |
| Delici % | 10 / 10 / 10 / 10 / 10 | 10 | — | 10 | — | 10 | — | — | — | 10 |
| Yarı insanlara karşı % | 10 / 10 / 10 / 10 / 10 | 10 | — | 10 | — | — | 10 | 10 | 10 | 10 |
| Hayvanlara karşı % | 20 / 20 / 20 / 20 / 20 | 20 | — | 20 | — | — | 20 | 20 | 20 | 20 |
| Orklara karşı % | 20 / 20 / 20 / 20 / 20 | 20 | — | 20 | — | — | 20 | 20 | 20 | 20 |
| Mistiklere karşı % | 20 / 20 / 20 / 20 / 20 | 20 | — | 20 | — | — | 20 | 20 | 20 | 20 |
| Ölümsüzlere karşı % | 20 / 20 / 20 / 20 / 20 | 20 | — | 20 | — | — | 20 | 20 | 20 | 20 |
| Şeytanlara karşı % | 20 / 20 / 20 / 20 / 20 | 20 | — | 20 | — | — | 20 | 20 | 20 | 20 |
| HP emme % | 10 / 10 / 10 / 10 / 10 | — | 10 | 10 | — | — | — | — | — | — |
| SP emme % | 10 / 10 / 10 / 10 / 10 | — | 10 | — | — | 10 | 10 | — | — | — |
| SP çalma % | 10 / 10 / 10 / 10 / 10 | — | — | 10 | — | 10 | — | — | 10 | — |
| Yakın dövüş bloklama % | 15 / 15 / 15 / 15 / 15 | — | — | — | — | — | — | 15 | — | 15 |
| Oklardan korunma % | 15 / 15 / 15 / 15 / 15 | — | — | — | 15 | — | 15 | — | — | 15 |
| Kılıç savunması % | 15 / 15 / 15 / 15 / 15 | — | 15 | — | 15 | 15 | — | — | 15 | 15 |
| Çift el savunması % | 15 / 15 / 15 / 15 / 15 | — | 15 | — | 15 | 15 | — | — | 15 | 15 |
| Bıçak savunması % | 15 / 15 / 15 / 15 / 15 | — | 15 | — | 15 | 15 | — | — | 15 | 15 |
| Çan savunması % | 15 / 15 / 15 / 15 / 15 | — | 15 | — | 15 | 15 | — | — | 15 | 15 |
| Yelpaze savunması % | 15 / 15 / 15 / 15 / 15 | — | 15 | — | 15 | 15 | — | — | 15 | 15 |
| Ok savunması % | 15 / 15 / 15 / 15 / 15 | — | 15 | — | 15 | 15 | — | — | 15 | 15 |
| Ateş direnci % | 15 / 15 / 15 / 15 / 15 | — | 15 | 15 | — | — | 15 | — | — | 15 |
| Şimşek direnci % | 15 / 15 / 15 / 15 / 15 | — | 15 | 15 | — | — | 15 | — | — | 15 |
| Büyü direnci % | 15 / 15 / 15 / 15 / 15 | — | 15 | 15 | — | — | 15 | — | — | 15 |
| Rüzgâr direnci % | 15 / 15 / 15 / 15 / 15 | — | 15 | 15 | — | — | 15 | — | — | 15 |
| Yakın dövüş yansıtma % | 10 / 10 / 10 / 10 / 10 | — | 10 | — | — | — | — | 10 | — | 10 |
| Zehir direnci % | 5 / 5 / 5 / 5 / 5 | — | — | — | — | — | — | — | 5 | 5 |
| EXP bonusu % | 20 / 20 / 20 / 20 / 20 | — | — | — | 20 | 20 | — | 20 | — | 20 |
| Yang çift düşme şansı % | 20 / 20 / 20 / 20 / 20 | — | — | — | 20 | 20 | — | 20 | — | 20 |
| Eşya düşürme bonusu % | 20 / 20 / 20 / 20 / 20 | — | — | 20 | — | — | — | — | 20 | 20 |
| Sersemliğe bağışıklık | 1 / 1 / 1 / 1 / 1 | — | — | — | — | — | — | 1 | — | — |
| Yavaşlığa bağışıklık | 1 / 1 / 1 / 1 / 1 | — | — | — | — | — | — | 1 | — | — |
| Saldırı değeri | 50 / 50 / 50 / 50 / 50 | — | 50 | — | — | — | — | — | — | 50 |

## Kostüm havuzları

| Efsun | 5 değer kademesi | Kostüm | Saç | Silah kostümü |
| --- | --- | --- | --- | --- |
| Maks. HP | 3000 / 3000 / 3000 / 3000 / 3000 | 3000 | 3000 | 3000 |
| Maks. SP | 80 / 80 / 80 / 80 / 80 | 80 | 80 | 80 |
| Canlılık | 12 / 12 / 12 / 12 / 12 | 12 | 12 | 12 |
| Zekâ | 12 / 12 / 12 / 12 / 12 | 12 | 12 | 12 |
| Güç | 12 / 12 / 12 / 12 / 12 | 12 | 12 | 12 |
| Çeviklik | 12 / 12 / 12 / 12 / 12 | 12 | 12 | 12 |
| Saldırı hızı % | 8 / 8 / 8 / 8 / 8 | 8 | 8 | 8 |
| Hareket hızı % | 20 / 20 / 20 / 20 / 20 | 20 | 20 | 20 |
| Büyü hızı % | 20 / 20 / 20 / 20 / 20 | 20 | 20 | 20 |
| HP yenileme % | 30 / 30 / 30 / 30 / 30 | 30 | 30 | — |
| SP yenileme % | 30 / 30 / 30 / 30 / 30 | 30 | 30 | — |
| Zehirleme % | 8 / 8 / 8 / 8 / 8 | — | — | 8 |
| Sersemletme % | 8 / 8 / 8 / 8 / 8 | — | — | 8 |
| Yavaşlatma % | 8 / 8 / 8 / 8 / 8 | — | — | 8 |
| Kritik % | 10 / 10 / 10 / 10 / 10 | 10 | 10 | 10 |
| Delici % | 10 / 10 / 10 / 10 / 10 | 10 | 10 | 10 |
| HP emme % | 10 / 10 / 10 / 10 / 10 | — | — | 10 |
| SP emme % | 10 / 10 / 10 / 10 / 10 | — | — | 10 |
| SP çalma % | 10 / 10 / 10 / 10 / 10 | — | — | 10 |
| Yakın dövüş bloklama % | 15 / 15 / 15 / 15 / 15 | 15 | 15 | — |
| Oklardan korunma % | 15 / 15 / 15 / 15 / 15 | 15 | 15 | — |

Kostümde kod desteği ve DB izinleri mevcut. “Kostüm güç vermez” tasarım
hedefiyle bu gerçek izinler aynı şey değildir; erişilebilir kostüm araçları
ayrı kontrol edilmeden bu sütunlar yokmuş gibi kabul edilmemeli.

## Klasik dışı rastgele efsunların kapatılması

- Normal havuzdan ortalama/beceri hasarı ve dirençleri rastgele gelmez.
  Silahların doğal ortalama/beceri üretimi ayrı mekanizma olarak korunur.
- 45 normal türün izinleri düzeltildi; örneğin HP yalnız zırh,
  bilezik, ayakkabı ve kolyede; bağışıklık yalnız kalkanda.
- Dört sınıfa karşı saldırı ve dört sınıf direnci normal 1–5 havuzunda kapalıdır.
- Metin/boss bonusu normal DB havuzunda yok. Dolunay’daki metin yazısı
  yukarıdaki kimlik uyuşmazlığı; böyle bir normal satırın kanıtı değil.
- Genel canavar gücü ve düz savunma değeri normal rastgele havuzda kapalıdır.
- Bu 14 tür kostüm/tılsım dahil 12 ekipman sütununda sıfır izin taşır.
- Sabit proto bonusları ve ayrı 6–7 tablosu bu kapatmayla değişmez.

Mevcut oyuncu eşyaları değiştirilmez. Yeni efsun ekleme/yenileme
yeni tabloyu kullanır; 6–7 havuzu ve doğal ortalama üretimi korunur.

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
sunucu `length.h` ve istemci `GameLib/ItemData.h`. Tarihsel 20 Ekim
canlı tablo SHA256 (22 Ekim seedine ait değildir):
`dfe1f1ac3eae6233fb1d3c0b8311d742de33804fde07e5a7bd12f33d38fdbf3c`.
Üretim: `python3 platform/tools/attribute_catalogue.py`.
