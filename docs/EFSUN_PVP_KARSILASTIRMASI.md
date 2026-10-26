# Klasik PvP efsun düzeni — bizim havuzla karşılaştırma

> **Araştırma sonrası karar:** Normal dağılım düzeltilecek, HP **3000** olacak;
> sabit değerler kostüm/tılsımda da geçerli. Anomali grupları ayrı görüşülecek.
> Aşağıdaki 2000 HP dahil referans/öneri değerleri araştırma tarihçesidir.
> Güncel uygulama: [EFSUN_NORMAL_DUZENLEME.md](EFSUN_NORMAL_DUZENLEME.md).

Araştırma tarihi: **22 Ekim 2026**. İstenen sekiz ekipmanın normal 1–5 efsunları incelendi. Kod ve canlı sunucu değiştirilmedi; aşağıdaki öneriler henüz oyun tasarımı kararı değildir.

## Sonuç

**Bizim mevcut havuz, klasik ekipman dağılımından belirgin biçimde farklı.** Sadece değerleri sabitlemek bu farkı gidermez: fazla izinleri kapatmanın yanında kalkana bağışıklık, kaska zehirleme, zırha saldırı değeri/HP emme gibi eksik izinleri de değerlendirmek gerekiyor.

“Normal PvP” için tek bir standart yok. Klasik 1–99 düzenini esas almak için resmî oyunun normal efsun tablolarını, 1–99 olduğunu belirten EmekPvP'nin kendi rehberini ve diğer sunucuların yayımladığı kuralları karşılaştırdım. Bu bir sunucu pazarı istatistiği veya canlı sunucularda oynayarak yapılmış test değildir.

**Benim önerim:** klasik ekipman sınırları + seçtiğimiz tek sabit değer. Doğal ortalama/beceri çifti için ayrı karar. Kullanıcının 1–99 orta-kolay PvP hedefi açısından bu, her ekipmanın işlevini korurken değer tutturma tekrarını azaltır. Bu cümle araştırma sonucu çıkan tasarım önerisidir, uygulanmış kural değildir.

## En önemli farklar

“Klasik referans” aşağıdaki resmî normal efsun tablolarına dayanır; bütün özel sunucular için zorunlu bir kural anlamına gelmez. Eşyanın kendi sabit özellikleri, taşlar, 6–7 efsun ve diğer sistemler bu karşılaştırmaya dahil değildir.

| Konu | Bizim mevcut normal havuz | Klasik referans |
| --- | --- | --- |
| Sersemlik / yavaşlık bağışıklığı | Zırh, kask, ayakkabı, kolye açık; kalkan kapalı | Kalkan |
| Zehirleme | Yalnız silah | Silah ve kask; üst değer %8 |
| Sersemletme | Yalnız silah | Silah, ayakkabı, kolye; üst değer %8 |
| Yavaşlatma | Yalnız silah | Silah ve ayakkabı; üst değer %8 |
| Maks. HP | Sekiz ekipmanın hepsi; 2500 tavan | Zırh, bilezik, ayakkabı, kolye; 2000 referans tavan |
| Güç / zekâ / çeviklik / canlılık | Sekiz ekipmanın hepsi | Silah ve kalkan; +12 |
| Saldırı hızı | Sekiz ekipmanın hepsi | Kask ve ayakkabı; %8 |
| Hareket hızı | Sekiz ekipmanın hepsi | Küpe; %20 |
| Büyü hızı | Sekiz ekipmanın hepsi | Silah ve zırh; %20 |
| Kritik | Sekiz ekipmanın hepsi | Silah, ayakkabı, kolye; %10 |
| Delici | Sekiz ekipmanın hepsi | Silah, bilezik, kolye; %10 |
| Yarı insan ve beş yaratık ırkına karşı güç | Sekiz ekipmanın hepsi | Silah, kask, kalkan, bilezik, küpe |
| Kılıç / çift el / bıçak / ok / çan / yelpaze savunmaları | Silah hariç bütün ekipmanlar; %10 | Zırh, ayakkabı, kolye, küpe; %15 |
| Ateş / rüzgâr / şimşek / büyü direnci | Silah hariç bütün ekipmanlar; %10 | Zırh, kask, bilezik; %15 |
| HP emme | Yalnız silah; %8 | Zırh ve bilezik; %10 |
| Saldırı değeri | Silah, bilezik, kask, kalkan; +30 | Zırh; +50 |
| Yakın dövüş bloklama | Silah hariç bütün ekipmanlar; %10 | Kalkan; %15 |
| Yakın dövüş yansıtma | Zırh, kalkan, kask, ayakkabı | Zırh ve kalkan; %10 |
| Ortalama / beceri hasarı | Sekiz ekipmanın hepsinde normal havuzda var | Uygun silahlarda özel ortalama/beceri üretimi; bütün ekipmana rastgele eklenen ortak bonus değil |
| Sınıflara karşı güç / sınıf direnci | Birçok ekipmanda normal havuzda var | İncelenen resmî normal havuzlarda yok; başka sistemlerde veya eşyanın sabit özelliğinde bulunması ayrı konu |
| Genel canavar gücü / ortalama direnci / beceri direnci | Normal havuzda var | İncelenen resmî normal havuzlarda yok; özel eşyaların temel özellikleriyle karıştırılmamalı |

Kaynaklar: aşağıdaki sekiz resmî ekipman tablosu; [EmekPvP'nin efsun rehberi](https://emekpvp.com/efsunlar); bizim [mevcut karar tablomuz](EFSUN_KARAR_TABLOSU.md).

## Ekipman ekipman referans liste

Aşağıdaki sayılar **referans üst değerlerdir**, “her PvP'de her seferinde bu değer gelir” demek değildir. Güncel resmî tablolardaki kanama, pençe savunması ve engelleme nüfuzu eski dört sınıflı 1–99 önerisinden bilinçli olarak ayrı tutuldu. Bunların kaldırılması/eklenmesi bu çalışmada uygulanmadı.

Kısaltmalar:

- **Irk gücü:** hayvan, ork, mistik, ölümsüz, şeytan; her biri ayrı efsun, %20.
- **Silah savunmaları:** kılıç, çift el, bıçak, ok, çan, yelpaze; her biri ayrı efsun, %15.
- **Element/büyü dirençleri:** ateş, rüzgâr, şimşek ve büyü; her biri ayrı efsun, %15.
- **Stat:** güç, zekâ, çeviklik, canlılık; her biri ayrı efsun, +12.

### Silah

- Dört stat +12; büyü hızı %20.
- Kritik ve delici %10; zehirleme, sersemletme ve yavaşlatma %8.
- Yarı insan %10; beş ırk gücü %20.
- Uygun silahlarda ayrıca doğal ortalama/beceri çifti bulunur. Resmî kaynak bunu belirli 30/75/105 seviye silahlar ve Çakır Kuşu ile sınırlar; bizim 1–99 çizgimizde eşya listesi ayrıca esas alınmalı.
- HP, hareket/saldırı hızı, HP/SP emme ve düz saldırı değeri bu normal silah listesinde yok.

[Kaynak: resmî silah bonusları](https://tr-wiki.metin2.gameforge.com/index.php/Şablon:Silah_Bonusları).

### Zırh

- HP 2000; güncel resmî tabloda SP 80; büyü hızı %20.
- Saldırı değeri +50; HP ve SP emme %10; yakın dövüş yansıtma %10.
- Altı silah savunması ve dört element/büyü direnci %15.
- Kritik, delici, yarı insan, dört stat ve rastgele ortalama/beceri hasarı bu listede yok.

[Kaynak: resmî zırh bonusları](https://tr-wiki.metin2.gameforge.com/index.php/Şablon:Zırh_Bonusları). **Varyant:** EmekPvP'nin 2008 düzeninde zırha SP ekleme kapalı; SP satırı evrensel eski sunucu kuralı olarak alınmamalı.

### Bilezik

- HP 2000; SP 80; delici %10; HP emme %10; SP çalma %10.
- Yarı insan %10; beş ırk gücü %20.
- Dört element/büyü direnci %15; eşya düşürme şansı %20.
- Kritik ve altı silah savunması normal listede yok.

[Kaynak: resmî bilezik bonusları](https://tr-wiki.metin2.gameforge.com/index.php/Şablon:Bilezik_Bonusları). Güncel tabloda ayrıca bulunan engelleme nüfuzu, bu eski düzen önerisine dahil edilmedi.

### Kalkan

- Dört stat +12; yarı insan %10; beş ırk gücü %20.
- Sersemlik ve yavaşlama bağışıklığı.
- Yakın dövüş bloklama %15; yakın dövüş yansıtma %10.
- EXP bonus şansı ve iki kat Yang şansı %20.
- HP, kritik, delici ve altı silah savunması normal listede yok. Bir kalkanın doğuştan verdiği sınıf direnci ayrı özelliktir.

[Kaynak: resmî kalkan bonusları](https://tr-wiki.metin2.gameforge.com/index.php/Şablon:Kalkan_Bonusları).

### Kask

- Yarı insan %10; beş ırk gücü %20.
- Saldırı hızı %8; zehirleme %8; HP/SP üretimi %30; SP emme %10.
- Dört element/büyü direnci %15; okları savuşturma %15.
- HP, kritik, delici, bağışıklık ve altı silah savunması normal listede yok.

[Kaynak: resmî kask bonusları](https://tr-wiki.metin2.gameforge.com/index.php/Şablon:Kask_Bonusları).

### Ayakkabı

- HP 2000; SP 80; saldırı hızı %8; kritik %10.
- Sersemletme ve yavaşlatma %8; okları savuşturma %15.
- Altı silah savunması %15; EXP bonus şansı ve iki kat Yang şansı %20.
- Delici, zehirleme, yarı insan ve bağışıklık normal listede yok. Ayakkabının kendi hareket hızı, ayrıca eklenen hareket hızı efsunu değildir.

[Kaynak: resmî ayakkabı bonusları](https://tr-wiki.metin2.gameforge.com/index.php/Şablon:Ayakkabı_Bonusları).

### Küpe

- Hareket hızı %20; yarı insan %10; beş ırk gücü %20.
- Altı silah savunması %15; eşya düşürme şansı %20; SP çalma %10.
- Zehir direnci: güncel resmî tabloda %1–5; özel sunucu değeri farklı olabilir.
- HP, dört stat, kritik ve delici normal listede yok. Abanoz gibi küpelerin kendi HP/stat özellikleri bu yasaklarla karıştırılmamalı.

[Kaynak: resmî küpe bonusları](https://tr-wiki.metin2.gameforge.com/index.php/Şablon:Küpe_Bonusları).

### Kolye

- HP 2000; SP 80; kritik ve delici %10; sersemletme %8.
- Altı silah savunması %15; HP/SP üretimi %30.
- Güncel resmî tabloda SP emme ve SP çalma %10.
- EXP bonus şansı ve iki kat Yang şansı %20.
- Yarı insan, dört stat ve bağışıklık normal listede yok. Kolyenin kendi büyü hızı ayrıca eklenen efsun değildir.

[Kaynak: resmî kolye bonusları](https://tr-wiki.metin2.gameforge.com/index.php/Şablon:Kolye_Bonusları). Rohan2'nin yayımladığı kolye havuzu daha dar; bu liste bütün özel sunucular için aynen geçerli değildir.

## Özel sunucular gerçekten ne yapıyor?

| Kaynak | Yayımlanan uygulama | Bizim için anlamı |
| --- | --- | --- |
| [EmekPvP — 2008 / 1–99 rehberi](https://emekpvp.com/efsunlar) | Ekipmana özgü izinler ve kademeli değerler; HP zırh/bilezik/ayakkabı/kolyede, stat silah/kalkanda; bağışıklık kalkanda | Klasik yuva sınırlarını destekleyen bir özel sunucu örneği |
| [Sofi2 — 1–99 orta emek](https://www.sofi2.com/) | “Sabit” ifadesini **iki değer** için kullanıyor: HP 2000 veya 3000, zehir/sersem/yavaş 5 veya 8, kritik/delici 5 veya 10, yarı insan 10 veya 15, savunmalar 10 veya 15 | Tanıtımda sabit yazması her zaman tek değer demek değil |
| [Maraz2 — 1–99 old school](https://maraz2.com/site/tanitim/) | Değerler sabit değil; beş yerine dört değer kullanıldığını belirtiyor | Değer arama kısmını koruyan sunucular da var |
| [Rohan2 — sunucunun kendi wiki tablosu](https://wiki.rohan2.global/Attr) | Kritik/delici 3/3/5/5/10; savunmalar 6/6/10/10/15 gibi kademeler. Küpede zehir direnci %8'e çıkıyor | Hem kademeler hem bazı izinler/değerler değişebiliyor; 1–99 standardının kanıtı olarak kullanılmadı |

Nutuk2 için üçüncü taraf ilanlarda tek sabit efsun iddiası bulundu; kendi tanıtımı ağırlıkla görsel olduğu ve değer tablosu bu çalışmada doğrulanmadığı için sayısal referansa alınmadı. Yukarıdaki değerlendirme sunucuların yayımladığı kurallarla sınırlı; çalışırlıkları ve oyuncu sayıları değerlendirilmedi.

## Bizim sabit değerler için başlangıç önerim

**Henüz kabul edilmedi veya uygulanmadı.** Ekipman izinlerini yukarıdaki klasik dağılıma yaklaştırdıktan sonra konuşulabilecek başlangıç değerleri:

| Efsun grubu | Önerilen tek değer |
| --- | ---: |
| Maks. HP | 2000 |
| Maks. SP | 80 |
| Güç / zekâ / çeviklik / canlılık | 12 |
| Kritik / delici | %10 |
| Zehirleme / sersemletme / yavaşlatma | %8 |
| Yarı insan | %10 |
| Beş yaratık ırkına karşı güç | %20 |
| Altı silah savunması | %15 |
| Ateş / rüzgâr / şimşek / büyü direnci | %15 |
| Saldırı hızı | %8 |
| Hareket / büyü hızı | %20 |
| HP / SP üretimi | %30 |
| HP emme / SP emme / SP çalma | %10 |
| Yakın dövüş bloklama / okları savuşturma | %15 |
| Yakın dövüş yansıtma | %10 |
| Saldırı değeri | 50 |
| EXP / Yang / eşya düşürme şansı | %20 |
| Bağışıklık | Var / yok |
| Zehir direnci | %5 veya özel sunucu tercihi %8 — karar gerekli |
| Doğal ortalama / beceri hasarı | Ayrı karar; bu tablo otomatik sabitlemez |

Bu öneride “sabit”, **efsun seçilirse değerinin aynı olması** demektir. Efsun türü ve beşli kombinasyon yine rastgele olabilir; zehirleme değerini %8 yapmak, zehirleme efsununun seçilme ihtimalini %8 yapmak değildir.

## Karar gerektiren noktalar

1. **Klasik izin dağılımını ne kadar koruyacağız?** Özellikle silah HP'si, bütün ekipmanlara kritik/delici/stat, sınıfa karşı güç ve genel canavar gücü açık kalacak mı?
2. **Doğal ortalama/beceri çifti:** rastgele mi kalacak, sınırlanacak mı, sabit mi olacak? Dolunay/zehir kılıcı gibi eşyaların arayışını doğrudan etkiler.
3. **Kaynak farkları:** zırhta SP, kolyede SP emme/çalma ve küpede zehir direnci. Evrensel PvP kuralı varsaymak yerine açık seçim yapılmalı.
4. **Mevcut eşyalar:** yeni izinler eski bonusları kendiliğinden temizlemez. Geçiş şekli ayrıca seçilmeli.

Kullanıcı kararları geldikçe [karar tablosuna](EFSUN_KARAR_TABLOSU.md) işlenecek. Kesinleşen oyun değerleri uygulamadan önce `PVP_HEDEF.md` içine kaydedilecek.
