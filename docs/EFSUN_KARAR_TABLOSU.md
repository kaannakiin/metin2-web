# Ekipman efsunları — karar tablosu

> **Güncel durum (22 Ekim):** Aşağıdaki geniş tablo değişiklik öncesi kayıt olarak
> korunuyor. Kullanıcı normal efsunların düzeltilmesini, HP 3000 ve kostüm/tılsımda
> da sabit değerleri kabul etti. Yeni repo tablosu: [EFSUN_REHBERI.md](EFSUN_REHBERI.md).
> Kapsam, ertelenen satırlar ve canlı kurulum durumu: [uygulama notu](EFSUN_NORMAL_DUZENLEME.md).

22 Ekim 2026. Kapsam: silah, zırh, bilezik, kalkan, kask, ayakkabı, küpe, kolye için normal 1–5 efsun havuzu.

Bu tablo **bizim sunucunun repo verisini** gösterir; klasik Metin2 kuralları değildir. `seed_item_attr.sql` içindeki 59 satır, mevcut `EFSUN_REHBERI.md` ile bütün değer kademeleri ve ekipman izinleri açısından karşılaştırıldı: fark yok. Önceki rehber 20 Ekim'de canlı DB ile doğrulanmış; bu çalışma sırasında canlı DB yeniden sorgulanmadı.

## Nasıl karar vereceğiz?

Klasik PvP karşılaştırması: [Ekipman dağılımları, özel sunucu örnekleri ve sabit değer önerisi](EFSUN_PVP_KARSILASTIRMASI.md). Bu karşılaştırmadaki öneriler henüz aşağıdaki mevcut havuzu değiştirmez.

- Her satırdaki ekipman sayısı, şu anda gelebilen **en yüksek değerdir**; her seferinde bu değer gelmez. `—` o ekipmanda kapalı demektir.
- “Mevcut kademeler”, sistemde tanımlı beş değerdir. Ekleme ve değiştirme farklı kademe olasılıkları kullanır; her işlemde bütün kademeler seçilmez.
- “Yeni sabit” sütunundaki `?` henüz karar verilmediğini belirtir. Mevcut tavanı otomatik olarak yeni sabit kabul etmiyoruz.
- Kullanıcının hedefi: seçilecek efsunların değerleri sabit olsun; bazı ekipmanlarda bazı efsunlar yasaklansın. “Zehirleme %8” şimdilik verilen örnektir, kesin karar değildir.
- Ekipman başına ilerleme sırası: **silah → zırh → bilezik → kalkan → kask → ayakkabı → küpe → kolye**. Her biri için yasaklanacak efsunlar ve kalanların sabit değerleri belirlenecek.

| Ekipman | Mevcut havuzdaki efsun türü sayısı |
| --- | ---: |
| Silah | 31 |
| Zırh | 44 |
| Bilezik | 42 |
| Kalkan | 50 |
| Kask | 53 |
| Ayakkabı | 46 |
| Küpe | 44 |
| Kolye | 51 |

Bu sayılar aynı anda bir eşyada bulunan efsun sayısı değildir. Normal slot sınırı 5'tir. Eşyanın kendi sabit özelliği veya mevcut efsunuyla aynı tür, normal rastgele seçimde tekrar seçilmez. Dolayısıyla tek bir eşyanın kullanılabilir havuzu daha küçük olabilir.

## Bütün efsunlar ve mevcut ekipman izinleri

Yüzde işareti efsun adındaysa değerler yüzdedir. HP/SP, statlar, saldırı ve savunma değeri düz puandır. Bağışıklıkta `1` özelliğin açık olmasıdır.

| Efsun | Mevcut kademeler | Silah | Zırh | Bilezik | Kalkan | Kask | Ayakkabı | Küpe | Kolye | Yeni sabit |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| Maks. HP | 500 / 1000 / 1500 / 2000 / 2500 | 2500 | 2500 | 2500 | 2500 | 2500 | 2500 | 2500 | 2500 | ? |
| Maks. SP | 10 / 20 / 30 / 40 / 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | 50 | ? |
| Canlılık | 2 / 4 / 6 / 8 / 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | ? |
| Zekâ | 2 / 4 / 6 / 8 / 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | ? |
| Güç | 2 / 4 / 6 / 8 / 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | ? |
| Çeviklik | 2 / 4 / 6 / 8 / 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | ? |
| Saldırı hızı % | 1 / 2 / 3 / 5 / 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | ? |
| Hareket hızı % | 2 / 4 / 6 / 10 / 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | ? |
| Büyü hızı % | 2 / 4 / 6 / 10 / 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | ? |
| HP yenileme % | 5 / 10 / 15 / 20 / 30 | — | 30 | 30 | 30 | 30 | 30 | 30 | 30 | ? |
| SP yenileme % | 5 / 10 / 15 / 20 / 30 | — | 30 | 30 | 30 | 30 | 30 | 30 | 30 | ? |
| Zehirleme şansı % | 1 / 2 / 3 / 5 / 8 | 8 | — | — | — | — | — | — | — | ? |
| Sersemletme şansı % | 1 / 2 / 3 / 5 / 8 | 8 | — | — | — | — | — | — | — | ? |
| Yavaşlatma şansı % | 1 / 2 / 3 / 5 / 8 | 8 | — | — | — | — | — | — | — | ? |
| Kritik vuruş şansı % | 1 / 2 / 3 / 5 / 10 | 10 | 10 | 10 | 10 | 10 | 10 | 10 | 10 | ? |
| Delici vuruş şansı % | 1 / 2 / 3 / 5 / 10 | 10 | 10 | 10 | 10 | 10 | 10 | 10 | 10 | ? |
| Yarı insanlara karşı % | 1 / 2 / 3 / 5 / 10 | 10 | 10 | 10 | 10 | 10 | 10 | 10 | 10 | ? |
| Hayvanlara karşı % | 2 / 4 / 6 / 10 / 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | ? |
| Orklara karşı % | 2 / 4 / 6 / 10 / 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | ? |
| Mistiklere karşı % | 2 / 4 / 6 / 10 / 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | ? |
| Ölümsüzlere karşı % | 2 / 4 / 6 / 10 / 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | ? |
| Şeytanlara karşı % | 2 / 4 / 6 / 10 / 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | 20 | ? |
| HP emme % | 1 / 2 / 3 / 5 / 8 | 8 | — | — | — | — | — | — | — | ? |
| SP emme % | 1 / 2 / 3 / 5 / 8 | 8 | — | — | — | — | — | — | — | ? |
| SP çalma % | 1 / 2 / 3 / 5 / 8 | 8 | — | — | — | — | — | — | — | ? |
| Yakın dövüş bloklama % | 2 / 4 / 6 / 8 / 10 | — | 10 | 10 | 10 | 10 | 10 | 10 | 10 | ? |
| Oklardan korunma % | 2 / 4 / 6 / 8 / 10 | — | 10 | 10 | 10 | 10 | 10 | 10 | 10 | ? |
| Kılıç savunması % | 1 / 2 / 3 / 5 / 10 | — | 10 | 10 | 10 | 10 | 10 | 10 | 10 | ? |
| Çift el savunması % | 1 / 2 / 3 / 5 / 10 | — | 10 | 10 | 10 | 10 | 10 | 10 | 10 | ? |
| Bıçak savunması % | 1 / 2 / 3 / 5 / 10 | — | 10 | 10 | 10 | 10 | 10 | 10 | 10 | ? |
| Çan savunması % | 1 / 2 / 3 / 5 / 10 | — | 10 | 10 | 10 | 10 | 10 | 10 | 10 | ? |
| Yelpaze savunması % | 1 / 2 / 3 / 5 / 10 | — | 10 | 10 | 10 | 10 | 10 | 10 | 10 | ? |
| Ok savunması % | 1 / 2 / 3 / 5 / 10 | — | 10 | 10 | 10 | 10 | 10 | 10 | 10 | ? |
| Ateş direnci % | 1 / 2 / 3 / 5 / 10 | — | 10 | 10 | 10 | 10 | 10 | 10 | 10 | ? |
| Şimşek direnci % | 1 / 2 / 3 / 5 / 10 | — | 10 | 10 | 10 | 10 | 10 | 10 | 10 | ? |
| Büyü direnci % | 1 / 2 / 3 / 5 / 10 | — | 10 | 10 | 10 | 10 | 10 | 10 | 10 | ? |
| Rüzgâr direnci % | 1 / 2 / 3 / 5 / 10 | — | 10 | 10 | 10 | 10 | 10 | 10 | 10 | ? |
| Yakın dövüş yansıtma % | 1 / 2 / 3 / 5 / 10 | — | 10 | — | 10 | 10 | 10 | — | — | ? |
| Zehir direnci % | 1 / 2 / 3 / 5 / 10 | — | 10 | 10 | 10 | 10 | 10 | 10 | 10 | ? |
| EXP bonusu % | 1 / 2 / 3 / 4 / 5 | — | — | — | 3 | 3 | 3 | 3 | 3 | ? |
| Yang çift düşme şansı % | 1 / 2 / 3 / 4 / 5 | — | — | — | 3 | 3 | 3 | 3 | 3 | ? |
| Eşya düşürme bonusu % | 1 / 2 / 3 / 4 / 5 | — | — | — | 3 | 3 | 3 | 3 | 3 | ? |
| Sersemliğe bağışıklık | 1 / 1 / 1 / 1 / 1 | — | 1 | — | — | 1 | 1 | — | 1 | ? |
| Yavaşlığa bağışıklık | 1 / 1 / 1 / 1 / 1 | — | 1 | — | — | 1 | 1 | — | 1 | ? |
| Saldırı değeri | 5 / 10 / 15 / 20 / 30 | 30 | — | 30 | 30 | 30 | — | — | — | ? |
| Savunma değeri | 5 / 10 / 15 / 20 / 30 | — | 30 | 30 | — | 30 | — | 30 | 30 | ? |
| Beceri hasarı % | 2 / 4 / 6 / 8 / 10 | 10 | 10 | 10 | 10 | 10 | 10 | 10 | 10 | ? |
| Ortalama zarar % | 2 / 4 / 6 / 8 / 10 | 10 | 10 | 10 | 10 | 10 | 10 | 10 | 10 | ? |
| Beceri direnci % | 2 / 4 / 6 / 8 / 10 | — | 10 | 10 | 10 | 10 | 10 | 10 | 10 | ? |
| Ortalama zarar direnci % | 2 / 4 / 6 / 8 / 10 | — | 10 | 10 | 10 | 10 | 10 | 10 | 10 | ? |
| Savaşçıya karşı % | 1 / 2 / 3 / 5 / 10 | 10 | — | — | 10 | 10 | — | — | 10 | ? |
| Ninjaya karşı % | 1 / 2 / 3 / 5 / 10 | 10 | — | — | 10 | 10 | — | — | 10 | ? |
| Suraya karşı % | 1 / 2 / 3 / 5 / 10 | 10 | — | — | 10 | 10 | — | — | 10 | ? |
| Şamana karşı % | 1 / 2 / 3 / 5 / 10 | 10 | — | — | 10 | 10 | — | — | 10 | ? |
| Savaşçı direnci % | 1 / 2 / 3 / 5 / 10 | — | 10 | 10 | 10 | 10 | 10 | 10 | 10 | ? |
| Ninja direnci % | 1 / 2 / 3 / 5 / 10 | — | 10 | 10 | 10 | 10 | 10 | 10 | 10 | ? |
| Sura direnci % | 1 / 2 / 3 / 5 / 10 | — | 10 | 10 | 10 | 10 | 10 | 10 | 10 | ? |
| Şaman direnci % | 1 / 2 / 3 / 5 / 10 | — | 10 | 10 | 10 | 10 | 10 | 10 | 10 | ? |
| Canavarlara karşı % | 2 / 4 / 6 / 10 / 20 | 20 | — | — | 20 | 20 | — | — | 20 | ? |

## İlk adım: silah

Kılıç, çift el, hançer, yay, çan ve yelpaze normal efsun seçiminde aynı silah havuzunu kullanır. Ok mühimmatı bu kapsamda değildir.

Silah için mevcut 31 tür, karar vermeyi kolaylaştırmak için aşağıda gruplandı. Parantezdeki değerler mevcut tavandır:

- **HP / SP / stat:** Maks. HP (2500), Maks. SP (50), Canlılık (12), Zekâ (12), Güç (12), Çeviklik (12).
- **Hız:** Saldırı hızı (%8), Hareket hızı (%20), Büyü hızı (%20).
- **Vuruş / durum etkisi:** Zehirleme (%8), Sersemletme (%8), Yavaşlatma (%8), Kritik (%10), Delici (%10).
- **Hedefe karşı güç:** Yarı insan (%10), Hayvan (%20), Ork (%20), Mistik (%20), Ölümsüz (%20), Şeytan (%20), Canavar (%20).
- **Sınıfa karşı güç:** Savaşçı (%10), Ninja (%10), Sura (%10), Şaman (%10).
- **Emme / çalma:** HP emme (%8), SP emme (%8), SP çalma (%8).
- **Hasar:** Saldırı değeri (30), Beceri hasarı (%10), Ortalama zarar (%10).

Karar verirken “Silah: HP ve hareket hızı yasak; zehirleme %8, kritik %10 sabit” biçimi yeterlidir. Söylenmeyen efsunlar kararsız kalır. Bir efsuna ekipmana göre farklı sabit değer istenirse ayrıca kaydedilecek.

## Dengeleme öncesi bilinmesi gerekenler

- **Bağışıklık kalkan havuzunda kapalı.** Mevcut tabloda sersemlik/yavaşlık bağışıklığı zırh, kask, ayakkabı ve kolyeye açık. Bunun istenen düzen olup olmadığına karar verilecek.
- **Ortalama ve beceri hasarı sekiz ekipmana da açık.** Ayrıca Dolunay gibi doğal ortalamalı silahların `item_addon.cpp` üzerinden ayrı rastgele üretimi var. Buradaki %10 tavan o özel üretimin tavanı değildir. “Bütün bonuslar sabit” hedefinde doğal ortalama/beceri çiftinin nasıl davranacağı ayrıca kararlaştırılmalı.
- **Metin ve boss gücü bu normal havuzda yok.** Başka sistemde bir özelliğin bulunması, normal efsunla gelebileceği anlamına gelmez.
- **Efsun ekleme ve değiştirme şu anda sabit değer vermiyor.** Varsayılan ekleme kademe ağırlıkları `40 / 50 / 10 / 0 / 0`; varsayılan değiştirme ağırlıkları `0 / 5 / 30 / 40 / 25`. Bunlar efsun türünün gelme ihtimali değil, değer kademesi ağırlıklarıdır.
- **6–7 efsun, kostüm, tılsım ve eşyanın kendi proto bonusları ayrı kapsamdır.** İlk sürüm hedefinde 6–7 efsun kapalı tutuluyor. Bu belge istenen sekiz ekipmanın normal havuzunu ele alır.
- Yeni izinler ve sabit değerler kesinleşince önce `PVP_HEDEF.md` güncellenecek. Ardından uygulama hazırlanacak. Mevcut eşyalardaki eski efsunların korunması/dönüştürülmesi ayrıca belirlenecek; havuzu değiştirmek eski eşyaları kendiliğinden düzeltmez.

## Kaynaklar

- [Normal ve nadir efsun verisi](../content/server/sql/seed_item_attr.sql)
- [20 Ekim efsun rehberi](EFSUN_REHBERI.md)
- [Ekipman havuzu, tekrar kontrolü, kademe seçimi](../apps/server/game/src/item_attribute.cpp)
- [Doğal ortalama / beceri üretimi](../apps/server/game/src/item_addon.cpp)
- [PvP hedefleri](../PVP_HEDEF.md)

Durum: araştırma ve karar hazırlığı. Oyun kodu, efsun verisi ve canlı sunucu değiştirilmedi.
