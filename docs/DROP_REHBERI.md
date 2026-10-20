# Metin ve Boss Drop Rehberi — Anka2

Tarih: **20 Ekim 2026** · Loot politikası: **v3**

**Durum:** Bu rehber repodaki güncel loot verisini anlatır; tek başına canlı kurulum kanıtı değildir. Önceki malzeme ağırlıklı sandık özeti geçersizdir. Yayın adayının durumu [kurulum belgesinde](../platform/deploy/GAMEPLAY_RELEASE.md) takip edilir.

## 1. En önemli düzeltmeler

- **Lusifer Sandığı 65 / 70 / 75 silah içerir.** Altı gerçek 75 silahın her biri %5 (toplam %30), beş doğrulanmış 70 silahın her biri %3 (toplam %15), yedi 65 silah her biri %1 (toplam %7). Hepsi +0. Barones de 75 silahları doğrudan her biri %3 verir.
- 85/90 metinlerden Zehir ve Orkide kaldırıldı. Diğer 75 silahlar da bu metin havuzuna eklenmedi.
- **Siam Bıçağı, Şeytani Pala, Yarı-İnsan Kılıç ve Mutluluk Yelpazesi 70 seviyedir.** Önceki özette 75 ailesiyle karıştırılmışlardı. Metinlerde kalırlar.
- Havalı Çelik Yay **2170**; Geyik Boynuzu Yay **2150** ve 30 seviyedir. ID ve seviye ayrımı gerçek item_proto üzerinden denetlendi.
- Diğer klasik boss sandıkları da artık silah ve zırh içerir; sadece tüketim malzemesi vermez.
- Önceki rehberde ayrı dengeleme bekleyen 10 klasik bossun tamamına özel loot eklendi. Azrail kendi sandığını verir; Barones/Cadı/Ağaç bossları/Kharoon doğrudan düşürür.
- Haritalar ve doğma bölgeleri korunur; metin yoğunluğu başlangıcın 4 katı, yeniden doğma süreleri yarısıdır. Exp ve zindan mekaniği değiştirilmedi.

## 2. Oranlar nasıl okunur?

Metin ve doğrudan boss tablolarındaki oranlar, yakın seviyede standart item-drop ayarındaki **baz oranlardır**: dosyadaki 400 yaklaşık %100, 24 yaklaşık %6 eder. Seviye farkı, sunucu oranı, çift drop ve motor bonusları gerçek sonucu değiştirebilir. Her satır bağımsızdır; aynı kesimde birden fazla eşya düşebilir. BK satırları ayrı rastgele beceriler üretir.

Sandık içi oranlar ise ağırlık/toplam hesabıdır. **Bir sandık yalnız bir sonuç satırı seçer**; o satırdaki adet kadar eşya verir. Silah/zırh satırında adet 1. 10 BK sonucu, aynı rastgele becerinin 10 kitaplık yığınıdır. Sandıktaki oranlar seviye drop cezasıyla tekrar çarpılmaz.

Bu dosya tüm mob_drop_item statik satırlarını ve ilgili sandık/taş kesesi içeriklerini kapsar. Aktif quest, event flag, premium ve özel C++ drop kancaları koşulludur; bu statik liste tek başına her canlı etkinlik ödülünü garanti etmez. common_drop_item, etc_drop_item ve drop_item_group dosyaları mevcut repoda boştur.

## 3. Aranan eşyalar: nereden düşer?

| Eşya | VNUM | Gerçek seviye | Güncel statik kaynaklar |
|---|---:|---:|---|
| Zehir Kılıcı+0 | 180 | 75 | Lusifer → Lusifer Sandığı: %5; Örümcek Barones doğrudan: %3. İkisinde de 1 adet +0 |
| Aslan Kılıcı+0 | 190 | 75 | Lusifer → Lusifer Sandığı: %5; Örümcek Barones doğrudan: %3. İkisinde de 1 adet +0 |
| Şeytan Kanadı Çakram+0 | 1130 | 75 | Lusifer → Lusifer Sandığı: %5; Örümcek Barones doğrudan: %3. İkisinde de 1 adet +0 |
| Havalı Çelik Yay+0 | 2170 | 75 | Lusifer → Lusifer Sandığı: %5; Örümcek Barones doğrudan: %3. İkisinde de 1 adet +0 |
| Kin Kılıcı+0 | 3160 | 75 | Lusifer → Lusifer Sandığı: %5; Örümcek Barones doğrudan: %3. İkisinde de 1 adet +0 |
| Orkide Çan+0 | 5120 | 75 | Lusifer → Lusifer Sandığı: %5; Örümcek Barones doğrudan: %3. İkisinde de 1 adet +0 |
| Azap Kılıcı+0 | 170 | 70 | Lusifer → Lusifer Sandığı; Azrail → Azrail'in Sandığı |
| Şeytani Pala+0 | 250 | 70 | Metin 85; Metin 90; Lusifer → Lusifer Sandığı; Azrail → Azrail'in Sandığı |
| Siam Bıçağı+0 | 1120 | 70 | Metin 85; Metin 90; Lusifer → Lusifer Sandığı; Azrail → Azrail'in Sandığı |
| Yarı-İnsan Kılıç+0 | 3150 | 70 | Metin 85; Metin 90; Lusifer → Lusifer Sandığı; Azrail → Azrail'in Sandığı |
| Mutluluk Yelpazesi+0 | 7150 | 70 | Metin 85; Metin 90; Lusifer → Lusifer Sandığı; Azrail → Azrail'in Sandığı |
| Siyah Çelik Zırh+0 | 11290 | 66 | Metin 90; Güçlü Buz Cadısı; Örümcek Barones; Lusifer → Lusifer Sandığı; Azrail → Azrail'in Sandığı |
| Siyah Rüzgar Takımı+0 | 11490 | 66 | Metin 90; Güçlü Buz Cadısı; Örümcek Barones; Lusifer → Lusifer Sandığı; Azrail → Azrail'in Sandığı |
| Kara Büyü Zırh+0 | 11690 | 66 | Metin 90; Güçlü Buz Cadısı; Örümcek Barones; Lusifer → Lusifer Sandığı; Azrail → Azrail'in Sandığı |
| Siyah Elbise+0 | 11890 | 66 | Metin 90; Güçlü Buz Cadısı; Örümcek Barones; Lusifer → Lusifer Sandığı; Azrail → Azrail'in Sandığı |
| Beceri Kitabı | 50300 | — | Aşağıdaki metin/sandık tabloları; her kaynağın miktarı ve şansı ayrı |
| Ruh Taşı | 50513 | — | Aşağıdaki metin/sandık tabloları; her kaynağın miktarı ve şansı ayrı |

Zehir için %5, ortalamada 20 sandık demektir; 20 sandıkta garanti anlamına gelmez. En az bir Zehir olasılığı 20 sandıkta yaklaşık %64,2; 59 sandıkta yaklaşık %95,2. Herhangi bir 75 silah için ortalama 3,33 sandık gerekir. Ticaret sınıfa uygun silaha erişimi kolaylaştırır.

## 4. Metinlerin eksiksiz statik drop tabloları

Toplam **23 metin drop grubu**. İçeriği aynı olan gruplar birlikte gösterildi; başlıklar metin seviyesidir, çıkan eşyanın giyme seviyesi ayrı sütundadır. Mevcut eski/alternatif metin VNUM’ları haritaya yeni taş eklendiği anlamına gelmez.

### Metin seviyesi 5 / 10 / 15 / 20

Taşlar: Üzüntü Metini (`8001`); Dövüş Metini (`8002`); Savaş Metini (`8003`); Hırs Metini (`8004`).

| Eşya | VNUM | Giyme/kullanım seviyesi | Adet | Baz düşme şansı |
|---|---:|---:|---:|---:|
| Beceri Kitabı | 50300 | — | 6 ayrı × 1 | 100% |
| Kötü Ruh Kovma Kağıdı | 71001 | — | 2 | 100% |
| Münzevi Tavsiyesi | 71094 | — | 2 | 100% |
| Zihin Taşı Kesesi | 27999 | — | 1 | 100% |
| Kutsama Kağıdı | 25040 | — | 1 | 50% |
| Efsun Nesnesi | 71084 | — | 10 | 50% |
| Arttırma Kağıdı | 71085 | — | 5 | 50% |

### Metin seviyesi 25

Taşlar: Siyah Metin (`8005`).

| Eşya | VNUM | Giyme/kullanım seviyesi | Adet | Baz düşme şansı |
|---|---:|---:|---:|---:|
| Beceri Kitabı | 50300 | — | 10 ayrı × 1 | 100% |
| Kötü Ruh Kovma Kağıdı | 71001 | — | 4 | 100% |
| Münzevi Tavsiyesi | 71094 | — | 4 | 100% |
| Zihin Taşı Kesesi | 27999 | — | 2 | 100% |
| Kutsama Kağıdı | 25040 | — | 1 | 100% |
| Efsun Nesnesi | 71084 | — | 15 | 60% |
| Arttırma Kağıdı | 71085 | — | 8 | 60% |
| Gümüş Kılıç+0 | 60 | 25 | 1 | 3% |
| Atsırtı Savaş+0 | 2050 | 25 | 1 | 3% |
| Savaş Tırpanı+0 | 3050 | 25 | 1 | 3% |
| Kısa Bıçak+0 | 4020 | 25 | 1 | 3% |
| Su Yelpazesi+0 | 7050 | 25 | 1 | 3% |

### Metin seviyesi 30

Taşlar: Karanlık Metin (`8006`).

| Eşya | VNUM | Giyme/kullanım seviyesi | Adet | Baz düşme şansı |
|---|---:|---:|---:|---:|
| Beceri Kitabı | 50300 | — | 10 ayrı × 1 | 100% |
| Kötü Ruh Kovma Kağıdı | 71001 | — | 4 | 100% |
| Münzevi Tavsiyesi | 71094 | — | 4 | 100% |
| Zihin Taşı Kesesi | 27999 | — | 2 | 100% |
| Kutsama Kağıdı | 25040 | — | 1 | 100% |
| Efsun Nesnesi | 71084 | — | 15 | 60% |
| Arttırma Kağıdı | 71085 | — | 8 | 60% |
| Dolunay Kılıcı+0 | 290 | 30 | 1 | 3% |
| Siyah Yaprak Hançeri+0 | 1170 | 30 | 1 | 3% |
| Geyik Boynuzu Yay+0 | 2150 | 30 | 1 | 3% |
| Kırmızı Demir Pala+0 | 3210 | 30 | 1 | 3% |
| Antik Çan+0 | 5110 | 30 | 1 | 3% |
| Sonbahar Yelpazesi+0 | 7160 | 30 | 1 | 3% |
| Aslan Plaka Zırh+0 | 11230 | 26 | 1 | 2% |
| Kırmızı Karınca Takım+0 | 11430 | 26 | 1 | 2% |
| Hayalet Plaka Zırh+0 | 11630 | 26 | 1 | 2% |
| Sevgi Elbisesi+0 | 11830 | 26 | 1 | 2% |

### Metin seviyesi 35

Taşlar: Kıskançlık Metini (`8007`).

| Eşya | VNUM | Giyme/kullanım seviyesi | Adet | Baz düşme şansı |
|---|---:|---:|---:|---:|
| Beceri Kitabı | 50300 | — | 10 ayrı × 1 | 100% |
| Kötü Ruh Kovma Kağıdı | 71001 | — | 4 | 100% |
| Münzevi Tavsiyesi | 71094 | — | 4 | 100% |
| Zihin Taşı Kesesi | 27999 | — | 2 | 100% |
| Kutsama Kağıdı | 25040 | — | 1 | 100% |
| Efsun Nesnesi | 71084 | — | 15 | 60% |
| Arttırma Kağıdı | 71085 | — | 8 | 60% |
| Dolunay Kılıcı+0 | 290 | 30 | 1 | 3% |
| Siyah Yaprak Hançeri+0 | 1170 | 30 | 1 | 3% |
| Geyik Boynuzu Yay+0 | 2150 | 30 | 1 | 3% |
| Kırmızı Demir Pala+0 | 3210 | 30 | 1 | 3% |
| Antik Çan+0 | 5110 | 30 | 1 | 3% |
| Sonbahar Yelpazesi+0 | 7160 | 30 | 1 | 3% |
| Aslan Plaka Zırh+0 | 11230 | 26 | 1 | 2% |
| Kırmızı Karınca Takım+0 | 11430 | 26 | 1 | 2% |
| Hayalet Plaka Zırh+0 | 11630 | 26 | 1 | 2% |
| Sevgi Elbisesi+0 | 11830 | 26 | 1 | 2% |
| YeşimTaşı Bilezik+0 | 14080 | 28 | 1 | 2% |
| Altın Bezeli Ayakkabı+0 | 15060 | 23 | 1 | 2% |
| Deri çizme+0 | 15080 | 29 | 1 | 2% |
| YeşimTaşı Kolye+0 | 16080 | 28 | 1 | 2% |
| YeşimTaşı Küpe+0 | 17080 | 28 | 1 | 2% |

### Metin seviyesi 40 / 45

Taşlar: Ruh Metini (`8008`); Gölge Metini (`8009`).

| Eşya | VNUM | Giyme/kullanım seviyesi | Adet | Baz düşme şansı |
|---|---:|---:|---:|---:|
| Beceri Kitabı | 50300 | — | 10 ayrı × 1 | 100% |
| Kötü Ruh Kovma Kağıdı | 71001 | — | 4 | 100% |
| Münzevi Tavsiyesi | 71094 | — | 4 | 100% |
| Zihin Taşı Kesesi | 27999 | — | 2 | 100% |
| Kutsama Kağıdı | 25040 | — | 1 | 100% |
| Efsun Nesnesi | 71084 | — | 15 | 60% |
| Arttırma Kağıdı | 71085 | — | 8 | 60% |
| Dolunay Kılıcı+0 | 290 | 30 | 1 | 3% |
| Siyah Yaprak Hançeri+0 | 1170 | 30 | 1 | 3% |
| Geyik Boynuzu Yay+0 | 2150 | 30 | 1 | 3% |
| Kırmızı Demir Pala+0 | 3210 | 30 | 1 | 3% |
| Antik Çan+0 | 5110 | 30 | 1 | 3% |
| Sonbahar Yelpazesi+0 | 7160 | 30 | 1 | 3% |
| Aslan Plaka Zırh+0 | 11230 | 26 | 1 | 2% |
| Kırmızı Karınca Takım+0 | 11430 | 26 | 1 | 2% |
| Hayalet Plaka Zırh+0 | 11630 | 26 | 1 | 2% |
| Sevgi Elbisesi+0 | 11830 | 26 | 1 | 2% |
| YeşimTaşı Bilezik+0 | 14080 | 28 | 1 | 2% |
| Altın Bezeli Ayakkabı+0 | 15060 | 23 | 1 | 2% |
| Deri çizme+0 | 15080 | 29 | 1 | 2% |
| YeşimTaşı Kolye+0 | 16080 | 28 | 1 | 2% |
| YeşimTaşı Küpe+0 | 17080 | 28 | 1 | 2% |
| Ruh Taşı | 50513 | — | 1 | 5% |

### Metin seviyesi 50 / 55

Taşlar: Dayanıklılık Metini (`8010`); Şeytan Metini (`8011`); Dayanıklılık Metini (`8015`); Şeytan Metini (`8016`).

| Eşya | VNUM | Giyme/kullanım seviyesi | Adet | Baz düşme şansı |
|---|---:|---:|---:|---:|
| Beceri Kitabı | 50300 | — | 12 ayrı × 1 | 100% |
| Kötü Ruh Kovma Kağıdı | 71001 | — | 5 | 100% |
| Münzevi Tavsiyesi | 71094 | — | 5 | 100% |
| Zihin Taşı Kesesi | 27999 | — | 2 | 100% |
| Kutsama Kağıdı | 25040 | — | 1 | 100% |
| Efsun Nesnesi | 71084 | — | 15 | 60% |
| Arttırma Kağıdı | 71085 | — | 8 | 60% |
| Uçan Büyücü Kılıcı+0 | 120 | 55 | 1 | 3% |
| Kaburga Bıçak+0 | 1080 | 55 | 1 | 3% |
| Tek Boynuzlu Yay+0 | 2110 | 55 | 1 | 3% |
| Kurtuluş Palası+0 | 3110 | 55 | 1 | 3% |
| Altın Böcek Çanı+0 | 5070 | 55 | 1 | 3% |
| Kaş Yelpaze+0 | 7110 | 55 | 1 | 3% |
| Mavi Taş Zırh+0 | 11260 | 48 | 1 | 2% |
| Genç Ejderha Takımı +0 | 11460 | 48 | 1 | 2% |
| Belirsiz Plaka Zırh+0 | 11660 | 48 | 1 | 2% |
| Manevi Elbise+0 | 11860 | 48 | 1 | 2% |
| Ruh Taşı | 50513 | — | 1 | 15% |

### Metin seviyesi 60

Taşlar: Lanet Metini (`8012`); Lanet Metini (`8017`).

| Eşya | VNUM | Giyme/kullanım seviyesi | Adet | Baz düşme şansı |
|---|---:|---:|---:|---:|
| Beceri Kitabı | 50300 | — | 12 ayrı × 1 | 100% |
| Kötü Ruh Kovma Kağıdı | 71001 | — | 5 | 100% |
| Münzevi Tavsiyesi | 71094 | — | 5 | 100% |
| Zihin Taşı Kesesi | 27999 | — | 2 | 100% |
| Kutsama Kağıdı | 25040 | — | 1 | 100% |
| Efsun Nesnesi | 71084 | — | 15 | 60% |
| Arttırma Kağıdı | 71085 | — | 8 | 60% |
| Uçan Büyücü Kılıcı+0 | 120 | 55 | 1 | 3% |
| Kaburga Bıçak+0 | 1080 | 55 | 1 | 3% |
| Tek Boynuzlu Yay+0 | 2110 | 55 | 1 | 3% |
| Kurtuluş Palası+0 | 3110 | 55 | 1 | 3% |
| Altın Böcek Çanı+0 | 5070 | 55 | 1 | 3% |
| Kaş Yelpaze+0 | 7110 | 55 | 1 | 3% |
| Mavi Taş Zırh+0 | 11260 | 48 | 1 | 2% |
| Genç Ejderha Takımı +0 | 11460 | 48 | 1 | 2% |
| Belirsiz Plaka Zırh+0 | 11660 | 48 | 1 | 2% |
| Manevi Elbise+0 | 11860 | 48 | 1 | 2% |
| Ruh Taşı | 50513 | — | 1 | 30% |

### Metin seviyesi 65

Taşlar: Ölüm Metini (`8013`); Ölüm Metini (`8018`).

| Eşya | VNUM | Giyme/kullanım seviyesi | Adet | Baz düşme şansı |
|---|---:|---:|---:|---:|
| Beceri Kitabı | 50300 | — | 12 ayrı × 1 | 100% |
| Kötü Ruh Kovma Kağıdı | 71001 | — | 5 | 100% |
| Münzevi Tavsiyesi | 71094 | — | 5 | 100% |
| Zihin Taşı Kesesi | 27999 | — | 2 | 100% |
| Kutsama Kağıdı | 25040 | — | 1 | 100% |
| Efsun Nesnesi | 71084 | — | 15 | 60% |
| Arttırma Kağıdı | 71085 | — | 8 | 60% |
| Uçan Büyücü Kılıcı+0 | 120 | 55 | 1 | 3% |
| Kaburga Bıçak+0 | 1080 | 55 | 1 | 3% |
| Tek Boynuzlu Yay+0 | 2110 | 55 | 1 | 3% |
| Kurtuluş Palası+0 | 3110 | 55 | 1 | 3% |
| Altın Böcek Çanı+0 | 5070 | 55 | 1 | 3% |
| Kaş Yelpaze+0 | 7110 | 55 | 1 | 3% |
| Mavi Taş Zırh+0 | 11260 | 48 | 1 | 2% |
| Genç Ejderha Takımı +0 | 11460 | 48 | 1 | 2% |
| Belirsiz Plaka Zırh+0 | 11660 | 48 | 1 | 2% |
| Manevi Elbise+0 | 11860 | 48 | 1 | 2% |
| Ruh Taşı | 50513 | — | 1 | 40% |

### Metin seviyesi 70

Taşlar: Katil Metini (`8014`); Katil Metini (`8019`).

| Eşya | VNUM | Giyme/kullanım seviyesi | Adet | Baz düşme şansı |
|---|---:|---:|---:|---:|
| Beceri Kitabı | 50300 | — | 12 ayrı × 1 | 100% |
| Kötü Ruh Kovma Kağıdı | 71001 | — | 5 | 100% |
| Münzevi Tavsiyesi | 71094 | — | 5 | 100% |
| Zihin Taşı Kesesi | 27999 | — | 2 | 100% |
| Kutsama Kağıdı | 25040 | — | 1 | 100% |
| Efsun Nesnesi | 71084 | — | 15 | 60% |
| Arttırma Kağıdı | 71085 | — | 8 | 60% |
| Uçan Büyücü Kılıcı+0 | 120 | 55 | 1 | 3% |
| Kaburga Bıçak+0 | 1080 | 55 | 1 | 3% |
| Tek Boynuzlu Yay+0 | 2110 | 55 | 1 | 3% |
| Kurtuluş Palası+0 | 3110 | 55 | 1 | 3% |
| Altın Böcek Çanı+0 | 5070 | 55 | 1 | 3% |
| Kaş Yelpaze+0 | 7110 | 55 | 1 | 3% |
| Mavi Taş Zırh+0 | 11260 | 48 | 1 | 2% |
| Genç Ejderha Takımı +0 | 11460 | 48 | 1 | 2% |
| Belirsiz Plaka Zırh+0 | 11660 | 48 | 1 | 2% |
| Manevi Elbise+0 | 11860 | 48 | 1 | 2% |
| Ruh Taşı | 50513 | — | 1 | 50% |

### Metin seviyesi 75 / 80

Taşlar: Metin Pung-Ma (`8024`); Metin Ma-An (`8025`).

| Eşya | VNUM | Giyme/kullanım seviyesi | Adet | Baz düşme şansı |
|---|---:|---:|---:|---:|
| Beceri Kitabı | 50300 | — | 14 ayrı × 1 | 100% |
| Kötü Ruh Kovma Kağıdı | 71001 | — | 6 | 100% |
| Münzevi Tavsiyesi | 71094 | — | 6 | 100% |
| Zihin Taşı Kesesi | 27999 | — | 3 | 100% |
| Kutsama Kağıdı | 25040 | — | 2 | 100% |
| Efsun Nesnesi | 71084 | — | 20 | 75% |
| Arttırma Kağıdı | 71085 | — | 10 | 75% |
| Su Perisi Kılıcı+0 | 160 | 65 | 1 | 2,5% |
| Şeytan Çıkarma Kılıcı+0 | 240 | 65 | 1 | 2,5% |
| Şimşek Bıçağı+0 | 1110 | 65 | 1 | 2,5% |
| Kutsal Sert Yay+0 | 2130 | 65 | 1 | 2,5% |
| Elektromanyetik Pala+0 | 3140 | 65 | 1 | 2,5% |
| Cennet ve Dünya Çanı+0 | 5100 | 65 | 1 | 2,5% |
| Kurtuluş Yelpazesi+0 | 7140 | 65 | 1 | 2,5% |
| Ejderha Tanrısı Zırhı+0 | 11280 | 61 | 1 | 2% |
| Küpeçiçeği Takım+0 | 11480 | 61 | 1 | 2% |
| Ruh Plaka Zırh+0 | 11680 | 61 | 1 | 2% |
| Soylu Kadın Elbisesi+0 | 11880 | 61 | 1 | 2% |
| Ruh Taşı | 50513 | — | 1 | 60% |

### Metin seviyesi 85

Taşlar: Metin Tu-Young (`8026`).

| Eşya | VNUM | Giyme/kullanım seviyesi | Adet | Baz düşme şansı |
|---|---:|---:|---:|---:|
| Beceri Kitabı | 50300 | — | 14 ayrı × 1 | 100% |
| Kötü Ruh Kovma Kağıdı | 71001 | — | 6 | 100% |
| Münzevi Tavsiyesi | 71094 | — | 6 | 100% |
| Zihin Taşı Kesesi | 27999 | — | 3 | 100% |
| Kutsama Kağıdı | 25040 | — | 2 | 100% |
| Efsun Nesnesi | 71084 | — | 20 | 75% |
| Arttırma Kağıdı | 71085 | — | 10 | 75% |
| Su Perisi Kılıcı+0 | 160 | 65 | 1 | 2,5% |
| Şeytan Çıkarma Kılıcı+0 | 240 | 65 | 1 | 2,5% |
| Şimşek Bıçağı+0 | 1110 | 65 | 1 | 2,5% |
| Kutsal Sert Yay+0 | 2130 | 65 | 1 | 2,5% |
| Elektromanyetik Pala+0 | 3140 | 65 | 1 | 2,5% |
| Cennet ve Dünya Çanı+0 | 5100 | 65 | 1 | 2,5% |
| Kurtuluş Yelpazesi+0 | 7140 | 65 | 1 | 2,5% |
| Ejderha Tanrısı Zırhı+0 | 11280 | 61 | 1 | 2% |
| Küpeçiçeği Takım+0 | 11480 | 61 | 1 | 2% |
| Ruh Plaka Zırh+0 | 11680 | 61 | 1 | 2% |
| Soylu Kadın Elbisesi+0 | 11880 | 61 | 1 | 2% |
| Şeytani Pala+0 | 250 | 70 | 1 | 2,5% |
| Siam Bıçağı+0 | 1120 | 70 | 1 | 2,5% |
| Sarı EjderhaYayı+0 | 2140 | 65 | 1 | 2,5% |
| Yarı-İnsan Kılıç+0 | 3150 | 70 | 1 | 2,5% |
| Mutluluk Yelpazesi+0 | 7150 | 70 | 1 | 2,5% |
| Ruh Taşı | 50513 | — | 1 | 70% |

### Metin seviyesi 90

Taşlar: Metin Jeon-Un (`8027`).

| Eşya | VNUM | Giyme/kullanım seviyesi | Adet | Baz düşme şansı |
|---|---:|---:|---:|---:|
| Beceri Kitabı | 50300 | — | 14 ayrı × 1 | 100% |
| Kötü Ruh Kovma Kağıdı | 71001 | — | 6 | 100% |
| Münzevi Tavsiyesi | 71094 | — | 6 | 100% |
| Zihin Taşı Kesesi | 27999 | — | 3 | 100% |
| Kutsama Kağıdı | 25040 | — | 2 | 100% |
| Efsun Nesnesi | 71084 | — | 20 | 75% |
| Arttırma Kağıdı | 71085 | — | 10 | 75% |
| Su Perisi Kılıcı+0 | 160 | 65 | 1 | 2,5% |
| Şeytan Çıkarma Kılıcı+0 | 240 | 65 | 1 | 2,5% |
| Şimşek Bıçağı+0 | 1110 | 65 | 1 | 2,5% |
| Kutsal Sert Yay+0 | 2130 | 65 | 1 | 2,5% |
| Elektromanyetik Pala+0 | 3140 | 65 | 1 | 2,5% |
| Cennet ve Dünya Çanı+0 | 5100 | 65 | 1 | 2,5% |
| Kurtuluş Yelpazesi+0 | 7140 | 65 | 1 | 2,5% |
| Ejderha Tanrısı Zırhı+0 | 11280 | 61 | 1 | 2% |
| Küpeçiçeği Takım+0 | 11480 | 61 | 1 | 2% |
| Ruh Plaka Zırh+0 | 11680 | 61 | 1 | 2% |
| Soylu Kadın Elbisesi+0 | 11880 | 61 | 1 | 2% |
| Şeytani Pala+0 | 250 | 70 | 1 | 2,5% |
| Siam Bıçağı+0 | 1120 | 70 | 1 | 2,5% |
| Sarı EjderhaYayı+0 | 2140 | 65 | 1 | 2,5% |
| Yarı-İnsan Kılıç+0 | 3150 | 70 | 1 | 2,5% |
| Mutluluk Yelpazesi+0 | 7150 | 70 | 1 | 2,5% |
| Ruh Taşı | 50513 | — | 1 | 80% |
| Siyah Çelik Zırh+0 | 11290 | 66 | 1 | 6% |
| Siyah Rüzgar Takımı+0 | 11490 | 66 | 1 | 6% |
| Kara Büyü Zırh+0 | 11690 | 66 | 1 | 6% |
| Siyah Elbise+0 | 11890 | 66 | 1 | 6% |

Yang bu statik eşya tablosundan ayrıdır. Sıfır gold tanımlı metin için kaynak formülü `500 + metin_seviyesi × 150` kullanılır; üstüne mevcut yang miktarı/bonus kuralları uygulanır. Buradaki formül ekranda kesin görülecek toplam yang diye okunmamalıdır.

## 5. Boss → sandık ve toplam ekipman şansı

| Boss | Boss VNUM / seviyesi | Sandık | Sandık VNUM | Silah | Zırh | Diğer |
|---|---|---|---:|---:|---:|---:|
| Ork Reisi | 691 / 50 | Ork Başkanının Sandığı | 50070 | 28% | 12% | 60% |
| Karanlık Lider | 791 / 54 | Öğreti Lideri Sandığı | 50071 | 28% | 12% | 60% |
| Karanlık Hayalet Lider | 792 / 62 | Hayalet Lideri Sandığı | 50072 | 28% | 12% | 60% |
| Kraliçe Örümcek | 2091 / 60 | Kraliçe Örümcek Sandığı | 50073 | 28% | 12% | 60% |
| Dokuz Kuyruk | 1901 / 72 | Dokuz Kuyruk Sandığı | 50077 | 28% | 12% | 60% |
| Sarı Kaplan Hayaleti | 1304 / 75 | Sarı Kaplan H. Sandığı | 50078 | 28% | 12% | 60% |
| Alev Kral | 2206 / 73 | Ateş Kral Sandığı | 50079 | 28% | 12% | 60% |
| Şeytan Kralı | 1091 / 75 | Şeytan Kral Sandığı | 50081 | 28% | 12% | 60% |
| Kibirli Şeytan Kralı | 1092 / 75 | Şeytan Kral Sandığı | 50081 | 28% | 12% | 60% |
| Lusifer | 1093 / 78 | Lusifer Sandığı | 50082 | 52% | 12% | 36% |
| Dev Çöl Kaplumbağası | 2191 / 67 | DevÇölkaplumbağa Sandığı | 50076 | 28% | 12% | 60% |
| Kırmızı Ejderha | 2291 / 75 | Kırmızı Ejderha Sandığı | 50080 | 28% | 12% | 60% |
| Azrail | 2598 / 91 | Azrail'in Sandığı | 50186 | 25% | 49% | 26% |

Bu 13 boss için doğrudan 1 kendi sandığı satırı @400 vardır: standart yakın seviye bazında yaklaşık %100. Aynı sandığı paylaşan iki boss (Şeytan Kral/Kibirli Şeytan Kral) aynı içeriği kullanır. Sandık içindeki ekipman oranları yukarıda; aşağıdaki listelerde tek tek eşya oranları bulunur.

## 6. Klasik boss sandıklarının tam içerikleri

### Ork Başkanının Sandığı — 50070

Kaynak: Ork Reisi. Her açılışta aşağıdaki satırlardan **bir tanesi** seçilir.

| Eşya | VNUM | Giyme/kullanım seviyesi | Adet | Sandık içi şans |
|---|---:|---:|---:|---:|
| Su Perisi Kılıcı+0 | 160 | 65 | 1 | 4% |
| Şeytan Çıkarma Kılıcı+0 | 240 | 65 | 1 | 4% |
| Şimşek Bıçağı+0 | 1110 | 65 | 1 | 4% |
| Kutsal Sert Yay+0 | 2130 | 65 | 1 | 4% |
| Elektromanyetik Pala+0 | 3140 | 65 | 1 | 4% |
| Cennet ve Dünya Çanı+0 | 5100 | 65 | 1 | 4% |
| Kurtuluş Yelpazesi+0 | 7140 | 65 | 1 | 4% |
| Altın Taş Zırh+0 | 11270 | 54 | 1 | 3% |
| Öldürücü Rüzgar Takımı+0 | 11470 | 54 | 1 | 3% |
| Hayalet Surat Zırh+0 | 11670 | 54 | 1 | 3% |
| Turuncu Kedi Elbisesi+0 | 11870 | 54 | 1 | 3% |
| Beceri Kitabı | 50300 | — | 10 | 15% |
| Kötü Ruh Kovma Kağıdı | 71001 | — | 20 | 10% |
| Münzevi Tavsiyesi | 71094 | — | 20 | 10% |
| Kutsama Kağıdı | 25040 | — | 10 | 10% |
| Efsun Nesnesi | 71084 | — | 100 | 10% |
| Arttırma Kağıdı | 71085 | — | 50 | 5% |

### Öğreti Lideri Sandığı — 50071

Kaynak: Karanlık Lider. Her açılışta aşağıdaki satırlardan **bir tanesi** seçilir.

| Eşya | VNUM | Giyme/kullanım seviyesi | Adet | Sandık içi şans |
|---|---:|---:|---:|---:|
| Su Perisi Kılıcı+0 | 160 | 65 | 1 | 4% |
| Şeytan Çıkarma Kılıcı+0 | 240 | 65 | 1 | 4% |
| Şimşek Bıçağı+0 | 1110 | 65 | 1 | 4% |
| Kutsal Sert Yay+0 | 2130 | 65 | 1 | 4% |
| Elektromanyetik Pala+0 | 3140 | 65 | 1 | 4% |
| Cennet ve Dünya Çanı+0 | 5100 | 65 | 1 | 4% |
| Kurtuluş Yelpazesi+0 | 7140 | 65 | 1 | 4% |
| Altın Taş Zırh+0 | 11270 | 54 | 1 | 3% |
| Öldürücü Rüzgar Takımı+0 | 11470 | 54 | 1 | 3% |
| Hayalet Surat Zırh+0 | 11670 | 54 | 1 | 3% |
| Turuncu Kedi Elbisesi+0 | 11870 | 54 | 1 | 3% |
| Beceri Kitabı | 50300 | — | 10 | 15% |
| Kötü Ruh Kovma Kağıdı | 71001 | — | 20 | 10% |
| Münzevi Tavsiyesi | 71094 | — | 20 | 10% |
| Kutsama Kağıdı | 25040 | — | 10 | 10% |
| Efsun Nesnesi | 71084 | — | 100 | 10% |
| Arttırma Kağıdı | 71085 | — | 50 | 5% |

### Hayalet Lideri Sandığı — 50072

Kaynak: Karanlık Hayalet Lider. Her açılışta aşağıdaki satırlardan **bir tanesi** seçilir.

| Eşya | VNUM | Giyme/kullanım seviyesi | Adet | Sandık içi şans |
|---|---:|---:|---:|---:|
| Su Perisi Kılıcı+0 | 160 | 65 | 1 | 4% |
| Şeytan Çıkarma Kılıcı+0 | 240 | 65 | 1 | 4% |
| Şimşek Bıçağı+0 | 1110 | 65 | 1 | 4% |
| Kutsal Sert Yay+0 | 2130 | 65 | 1 | 4% |
| Elektromanyetik Pala+0 | 3140 | 65 | 1 | 4% |
| Cennet ve Dünya Çanı+0 | 5100 | 65 | 1 | 4% |
| Kurtuluş Yelpazesi+0 | 7140 | 65 | 1 | 4% |
| Altın Taş Zırh+0 | 11270 | 54 | 1 | 3% |
| Öldürücü Rüzgar Takımı+0 | 11470 | 54 | 1 | 3% |
| Hayalet Surat Zırh+0 | 11670 | 54 | 1 | 3% |
| Turuncu Kedi Elbisesi+0 | 11870 | 54 | 1 | 3% |
| Ruh Taşı | 50513 | — | 3 | 20% |
| Kötü Ruh Kovma Kağıdı | 71001 | — | 30 | 10% |
| Münzevi Tavsiyesi | 71094 | — | 30 | 10% |
| Kutsama Kağıdı | 25040 | — | 15 | 10% |
| Efsun Nesnesi | 71084 | — | 150 | 5% |
| Arttırma Kağıdı | 71085 | — | 75 | 5% |

### Kraliçe Örümcek Sandığı — 50073

Kaynak: Kraliçe Örümcek. Her açılışta aşağıdaki satırlardan **bir tanesi** seçilir.

| Eşya | VNUM | Giyme/kullanım seviyesi | Adet | Sandık içi şans |
|---|---:|---:|---:|---:|
| Su Perisi Kılıcı+0 | 160 | 65 | 1 | 4% |
| Şeytan Çıkarma Kılıcı+0 | 240 | 65 | 1 | 4% |
| Şimşek Bıçağı+0 | 1110 | 65 | 1 | 4% |
| Kutsal Sert Yay+0 | 2130 | 65 | 1 | 4% |
| Elektromanyetik Pala+0 | 3140 | 65 | 1 | 4% |
| Cennet ve Dünya Çanı+0 | 5100 | 65 | 1 | 4% |
| Kurtuluş Yelpazesi+0 | 7140 | 65 | 1 | 4% |
| Ejderha Tanrısı Zırhı+0 | 11280 | 61 | 1 | 3% |
| Küpeçiçeği Takım+0 | 11480 | 61 | 1 | 3% |
| Ruh Plaka Zırh+0 | 11680 | 61 | 1 | 3% |
| Soylu Kadın Elbisesi+0 | 11880 | 61 | 1 | 3% |
| Ruh Taşı | 50513 | — | 3 | 20% |
| Kötü Ruh Kovma Kağıdı | 71001 | — | 30 | 10% |
| Münzevi Tavsiyesi | 71094 | — | 30 | 10% |
| Kutsama Kağıdı | 25040 | — | 15 | 10% |
| Efsun Nesnesi | 71084 | — | 150 | 5% |
| Arttırma Kağıdı | 71085 | — | 75 | 5% |

### Dokuz Kuyruk Sandığı — 50077

Kaynak: Dokuz Kuyruk. Her açılışta aşağıdaki satırlardan **bir tanesi** seçilir.

| Eşya | VNUM | Giyme/kullanım seviyesi | Adet | Sandık içi şans |
|---|---:|---:|---:|---:|
| Muharebe Kılıcı+0 | 140 | 65 | 1 | 4% |
| Hortlak Dişi Kılıcı+0 | 150 | 65 | 1 | 4% |
| Ejderha Bıçağı+0 | 1100 | 65 | 1 | 4% |
| Sarı EjderhaYayı+0 | 2140 | 65 | 1 | 4% |
| Partizan+0 | 3130 | 65 | 1 | 4% |
| Yıldırım Kuşu Çanı+0 | 5090 | 65 | 1 | 4% |
| Cennet Kuşu Yelpaze+0 | 7130 | 65 | 1 | 4% |
| Ejderha Tanrısı Zırhı+0 | 11280 | 61 | 1 | 3% |
| Küpeçiçeği Takım+0 | 11480 | 61 | 1 | 3% |
| Ruh Plaka Zırh+0 | 11680 | 61 | 1 | 3% |
| Soylu Kadın Elbisesi+0 | 11880 | 61 | 1 | 3% |
| Ruh Taşı | 50513 | — | 5 | 25% |
| Kutsama Kağıdı | 25040 | — | 20 | 10% |
| Efsun Nesnesi | 71084 | — | 200 | 10% |
| Arttırma Kağıdı | 71085 | — | 100 | 5% |
| Beyaz İnci | 27992 | — | 1 | 6% |
| Mavi İnci | 27993 | — | 1 | 3% |
| Kankırmızı İnci | 27994 | — | 1 | 1% |

### Sarı Kaplan H. Sandığı — 50078

Kaynak: Sarı Kaplan Hayaleti. Her açılışta aşağıdaki satırlardan **bir tanesi** seçilir.

| Eşya | VNUM | Giyme/kullanım seviyesi | Adet | Sandık içi şans |
|---|---:|---:|---:|---:|
| Muharebe Kılıcı+0 | 140 | 65 | 1 | 4% |
| Hortlak Dişi Kılıcı+0 | 150 | 65 | 1 | 4% |
| Ejderha Bıçağı+0 | 1100 | 65 | 1 | 4% |
| Sarı EjderhaYayı+0 | 2140 | 65 | 1 | 4% |
| Partizan+0 | 3130 | 65 | 1 | 4% |
| Yıldırım Kuşu Çanı+0 | 5090 | 65 | 1 | 4% |
| Cennet Kuşu Yelpaze+0 | 7130 | 65 | 1 | 4% |
| Ejderha Tanrısı Zırhı+0 | 11280 | 61 | 1 | 3% |
| Küpeçiçeği Takım+0 | 11480 | 61 | 1 | 3% |
| Ruh Plaka Zırh+0 | 11680 | 61 | 1 | 3% |
| Soylu Kadın Elbisesi+0 | 11880 | 61 | 1 | 3% |
| Ruh Taşı | 50513 | — | 5 | 25% |
| Kutsama Kağıdı | 25040 | — | 20 | 10% |
| Efsun Nesnesi | 71084 | — | 200 | 10% |
| Arttırma Kağıdı | 71085 | — | 100 | 5% |
| Beyaz İnci | 27992 | — | 1 | 6% |
| Mavi İnci | 27993 | — | 1 | 3% |
| Kankırmızı İnci | 27994 | — | 1 | 1% |

### Ateş Kral Sandığı — 50079

Kaynak: Alev Kral. Her açılışta aşağıdaki satırlardan **bir tanesi** seçilir.

| Eşya | VNUM | Giyme/kullanım seviyesi | Adet | Sandık içi şans |
|---|---:|---:|---:|---:|
| Muharebe Kılıcı+0 | 140 | 65 | 1 | 4% |
| Hortlak Dişi Kılıcı+0 | 150 | 65 | 1 | 4% |
| Ejderha Bıçağı+0 | 1100 | 65 | 1 | 4% |
| Sarı EjderhaYayı+0 | 2140 | 65 | 1 | 4% |
| Partizan+0 | 3130 | 65 | 1 | 4% |
| Yıldırım Kuşu Çanı+0 | 5090 | 65 | 1 | 4% |
| Cennet Kuşu Yelpaze+0 | 7130 | 65 | 1 | 4% |
| Ejderha Tanrısı Zırhı+0 | 11280 | 61 | 1 | 3% |
| Küpeçiçeği Takım+0 | 11480 | 61 | 1 | 3% |
| Ruh Plaka Zırh+0 | 11680 | 61 | 1 | 3% |
| Soylu Kadın Elbisesi+0 | 11880 | 61 | 1 | 3% |
| Ruh Taşı | 50513 | — | 5 | 25% |
| Kutsama Kağıdı | 25040 | — | 20 | 10% |
| Efsun Nesnesi | 71084 | — | 200 | 10% |
| Arttırma Kağıdı | 71085 | — | 100 | 5% |
| Beyaz İnci | 27992 | — | 1 | 6% |
| Mavi İnci | 27993 | — | 1 | 3% |
| Kankırmızı İnci | 27994 | — | 1 | 1% |

### Şeytan Kral Sandığı — 50081

Kaynak: Şeytan Kralı, Kibirli Şeytan Kralı. Her açılışta aşağıdaki satırlardan **bir tanesi** seçilir.

| Eşya | VNUM | Giyme/kullanım seviyesi | Adet | Sandık içi şans |
|---|---:|---:|---:|---:|
| Muharebe Kılıcı+0 | 140 | 65 | 1 | 4% |
| Hortlak Dişi Kılıcı+0 | 150 | 65 | 1 | 4% |
| Ejderha Bıçağı+0 | 1100 | 65 | 1 | 4% |
| Sarı EjderhaYayı+0 | 2140 | 65 | 1 | 4% |
| Partizan+0 | 3130 | 65 | 1 | 4% |
| Yıldırım Kuşu Çanı+0 | 5090 | 65 | 1 | 4% |
| Cennet Kuşu Yelpaze+0 | 7130 | 65 | 1 | 4% |
| Ejderha Tanrısı Zırhı+0 | 11280 | 61 | 1 | 3% |
| Küpeçiçeği Takım+0 | 11480 | 61 | 1 | 3% |
| Ruh Plaka Zırh+0 | 11680 | 61 | 1 | 3% |
| Soylu Kadın Elbisesi+0 | 11880 | 61 | 1 | 3% |
| Ruh Taşı | 50513 | — | 5 | 25% |
| Kutsama Kağıdı | 25040 | — | 20 | 10% |
| Efsun Nesnesi | 71084 | — | 200 | 10% |
| Arttırma Kağıdı | 71085 | — | 100 | 5% |
| Beyaz İnci | 27992 | — | 1 | 6% |
| Mavi İnci | 27993 | — | 1 | 3% |
| Kankırmızı İnci | 27994 | — | 1 | 1% |

### Lusifer Sandığı — 50082

Kaynak: Lusifer. Her açılışta aşağıdaki satırlardan **bir tanesi** seçilir.

| Eşya | VNUM | Giyme/kullanım seviyesi | Adet | Sandık içi şans |
|---|---:|---:|---:|---:|
| Zehir Kılıcı+0 | 180 | 75 | 1 | 5% |
| Aslan Kılıcı+0 | 190 | 75 | 1 | 5% |
| Şeytan Kanadı Çakram+0 | 1130 | 75 | 1 | 5% |
| Havalı Çelik Yay+0 | 2170 | 75 | 1 | 5% |
| Kin Kılıcı+0 | 3160 | 75 | 1 | 5% |
| Orkide Çan+0 | 5120 | 75 | 1 | 5% |
| Azap Kılıcı+0 | 170 | 70 | 1 | 3% |
| Şeytani Pala+0 | 250 | 70 | 1 | 3% |
| Siam Bıçağı+0 | 1120 | 70 | 1 | 3% |
| Yarı-İnsan Kılıç+0 | 3150 | 70 | 1 | 3% |
| Mutluluk Yelpazesi+0 | 7150 | 70 | 1 | 3% |
| Muharebe Kılıcı+0 | 140 | 65 | 1 | 1% |
| Hortlak Dişi Kılıcı+0 | 150 | 65 | 1 | 1% |
| Ejderha Bıçağı+0 | 1100 | 65 | 1 | 1% |
| Sarı EjderhaYayı+0 | 2140 | 65 | 1 | 1% |
| Partizan+0 | 3130 | 65 | 1 | 1% |
| Yıldırım Kuşu Çanı+0 | 5090 | 65 | 1 | 1% |
| Cennet Kuşu Yelpaze+0 | 7130 | 65 | 1 | 1% |
| Siyah Çelik Zırh+0 | 11290 | 66 | 1 | 3% |
| Siyah Rüzgar Takımı+0 | 11490 | 66 | 1 | 3% |
| Kara Büyü Zırh+0 | 11690 | 66 | 1 | 3% |
| Siyah Elbise+0 | 11890 | 66 | 1 | 3% |
| Ruh Taşı | 50513 | — | 8 | 16% |
| Beyaz İnci | 27992 | — | 2 | 6% |
| Mavi İnci | 27993 | — | 1 | 4% |
| Kankırmızı İnci | 27994 | — | 1 | 2% |
| Kutsama Kağıdı | 25040 | — | 25 | 8% |

### DevÇölkaplumbağa Sandığı — 50076

Kaynak: Dev Çöl Kaplumbağası. Her açılışta aşağıdaki satırlardan **bir tanesi** seçilir.

| Eşya | VNUM | Giyme/kullanım seviyesi | Adet | Sandık içi şans |
|---|---:|---:|---:|---:|
| Su Perisi Kılıcı+0 | 160 | 65 | 1 | 4% |
| Şeytan Çıkarma Kılıcı+0 | 240 | 65 | 1 | 4% |
| Şimşek Bıçağı+0 | 1110 | 65 | 1 | 4% |
| Kutsal Sert Yay+0 | 2130 | 65 | 1 | 4% |
| Elektromanyetik Pala+0 | 3140 | 65 | 1 | 4% |
| Cennet ve Dünya Çanı+0 | 5100 | 65 | 1 | 4% |
| Kurtuluş Yelpazesi+0 | 7140 | 65 | 1 | 4% |
| Ejderha Tanrısı Zırhı+0 | 11280 | 61 | 1 | 3% |
| Küpeçiçeği Takım+0 | 11480 | 61 | 1 | 3% |
| Ruh Plaka Zırh+0 | 11680 | 61 | 1 | 3% |
| Soylu Kadın Elbisesi+0 | 11880 | 61 | 1 | 3% |
| Ruh Taşı | 50513 | — | 3 | 20% |
| Kötü Ruh Kovma Kağıdı | 71001 | — | 30 | 10% |
| Münzevi Tavsiyesi | 71094 | — | 30 | 10% |
| Kutsama Kağıdı | 25040 | — | 15 | 10% |
| Efsun Nesnesi | 71084 | — | 150 | 5% |
| Arttırma Kağıdı | 71085 | — | 75 | 5% |

### Kırmızı Ejderha Sandığı — 50080

Kaynak: Kırmızı Ejderha. Her açılışta aşağıdaki satırlardan **bir tanesi** seçilir.

| Eşya | VNUM | Giyme/kullanım seviyesi | Adet | Sandık içi şans |
|---|---:|---:|---:|---:|
| Muharebe Kılıcı+0 | 140 | 65 | 1 | 4% |
| Hortlak Dişi Kılıcı+0 | 150 | 65 | 1 | 4% |
| Ejderha Bıçağı+0 | 1100 | 65 | 1 | 4% |
| Sarı EjderhaYayı+0 | 2140 | 65 | 1 | 4% |
| Partizan+0 | 3130 | 65 | 1 | 4% |
| Yıldırım Kuşu Çanı+0 | 5090 | 65 | 1 | 4% |
| Cennet Kuşu Yelpaze+0 | 7130 | 65 | 1 | 4% |
| Ejderha Tanrısı Zırhı+0 | 11280 | 61 | 1 | 3% |
| Küpeçiçeği Takım+0 | 11480 | 61 | 1 | 3% |
| Ruh Plaka Zırh+0 | 11680 | 61 | 1 | 3% |
| Soylu Kadın Elbisesi+0 | 11880 | 61 | 1 | 3% |
| Ruh Taşı | 50513 | — | 5 | 25% |
| Kutsama Kağıdı | 25040 | — | 20 | 10% |
| Efsun Nesnesi | 71084 | — | 200 | 10% |
| Arttırma Kağıdı | 71085 | — | 100 | 5% |
| Beyaz İnci | 27992 | — | 1 | 6% |
| Mavi İnci | 27993 | — | 1 | 3% |
| Kankırmızı İnci | 27994 | — | 1 | 1% |

### Azrail'in Sandığı — 50186

Kaynak: Azrail. Her açılışta aşağıdaki satırlardan **bir tanesi** seçilir.

| Eşya | VNUM | Giyme/kullanım seviyesi | Adet | Sandık içi şans |
|---|---:|---:|---:|---:|
| Azap Kılıcı+0 | 170 | 70 | 1 | 5% |
| Şeytani Pala+0 | 250 | 70 | 1 | 5% |
| Siam Bıçağı+0 | 1120 | 70 | 1 | 5% |
| Yarı-İnsan Kılıç+0 | 3150 | 70 | 1 | 5% |
| Mutluluk Yelpazesi+0 | 7150 | 70 | 1 | 5% |
| Siyah Çelik Zırh+0 | 11290 | 66 | 1 | 4% |
| Siyah Rüzgar Takımı+0 | 11490 | 66 | 1 | 4% |
| Kara Büyü Zırh+0 | 11690 | 66 | 1 | 4% |
| Siyah Elbise+0 | 11890 | 66 | 1 | 4% |
| Korku Maskesi +0 | 12260 | 60 | 1 | 3% |
| Ork Kapşonu +0 | 12390 | 60 | 1 | 3% |
| Boynuzlu Kask +0 | 12530 | 60 | 1 | 3% |
| Kardinal Şapkası +0 | 12670 | 60 | 1 | 3% |
| Titan Kalkanı+0 | 13140 | 81 | 1 | 3% |
| Ruh Kristali Bilekliği+0 | 14220 | 58 | 1 | 3% |
| Ruh Kristali Kolyesi+0 | 16220 | 60 | 1 | 3% |
| Ruh Kristali Küpeleri+0 | 17220 | 62 | 1 | 3% |
| Cennetin Gözy. Bilezik+0 | 14200 | 54 | 1 | 3% |
| Cennetin Gözyaşı Kolye+0 | 16200 | 54 | 1 | 3% |
| Cennetin Gözyaşı Küpe+0 | 17200 | 54 | 1 | 3% |
| Ruh Taşı | 50513 | — | 8 | 10% |
| Kutsama Kağıdı | 25040 | — | 25 | 8% |
| Beyaz İnci | 27992 | — | 1 | 4% |
| Mavi İnci | 27993 | — | 1 | 3% |
| Kankırmızı İnci | 27994 | — | 1 | 1% |

## 7. Doğrudan boss ve diğer yaratık dropları — tam listeler

Önceki kısa özette bu gruplar gösterilmemişti. Aşağıdaki satırlar sandıklara dönüştürülmedi. `Phase3Direct_` grupları yeni v3 boss ödülleridir; diğerleri mevcut korunmuş satırlardır. Kaptan, normal yaratık ve maymun grupları da kaynak dosyanın tamamı görülebilsin diye dahil edildi; hepsinin boss olduğu iddia edilmez. Bu kayıtların bulunması ilgili yaratığın canlı haritada spawn edildiğini tek başına kanıtlamaz.

### Zayıf Maymun Asker — 5101

Grup: `GibonSoldat` · Proto seviye: 22 · Rütbe: `PAWN`.

| Eşya | VNUM | Giyme/kullanım seviyesi | Adet | Baz düşme şansı |
|---|---:|---:|---:|---:|
| Beceri Kitabı | 50300 | — | 1 | 50% |
| Zihin Taşı Kesesi | 27999 | — | 1 | 20% |
| Efsun Nesnesi | 71084 | — | 3 | 12,5% |
| Arttırma Kağıdı | 71085 | — | 2 | 10% |

### Zayıf Maymun Atıcı — 5102

Grup: `GibonGrenadier` · Proto seviye: 25 · Rütbe: `S_PAWN`.

| Eşya | VNUM | Giyme/kullanım seviyesi | Adet | Baz düşme şansı |
|---|---:|---:|---:|---:|
| Beceri Kitabı | 50300 | — | 1 | 50% |
| Zihin Taşı Kesesi | 27999 | — | 1 | 20% |
| Efsun Nesnesi | 71084 | — | 3 | 12,5% |
| Arttırma Kağıdı | 71085 | — | 2 | 10% |

### Zayıf Maymun Savaşçı — 5103

Grup: `GibonLuptator` · Proto seviye: 27 · Rütbe: `KNIGHT`.

| Eşya | VNUM | Giyme/kullanım seviyesi | Adet | Baz düşme şansı |
|---|---:|---:|---:|---:|
| Beceri Kitabı | 50300 | — | 1 | 50% |
| Zihin Taşı Kesesi | 27999 | — | 1 | 20% |
| Efsun Nesnesi | 71084 | — | 3 | 12,5% |
| Arttırma Kağıdı | 71085 | — | 2 | 10% |

### Zayıf Maymun General — 5104

Grup: `GibonGeneral` · Proto seviye: 29 · Rütbe: `S_KNIGHT`.

| Eşya | VNUM | Giyme/kullanım seviyesi | Adet | Baz düşme şansı |
|---|---:|---:|---:|---:|
| Beceri Kitabı | 50300 | — | 1 | 50% |
| Zihin Taşı Kesesi | 27999 | — | 1 | 20% |
| Efsun Nesnesi | 71084 | — | 3 | 12,5% |
| Arttırma Kağıdı | 71085 | — | 2 | 10% |

### Maymun Asker — 5111

Grup: `MaimutaSoldat` · Proto seviye: 35 · Rütbe: `PAWN`.

| Eşya | VNUM | Giyme/kullanım seviyesi | Adet | Baz düşme şansı |
|---|---:|---:|---:|---:|
| Beceri Kitabı | 50300 | — | 1 | 50% |
| Zihin Taşı Kesesi | 27999 | — | 1 | 20% |
| Efsun Nesnesi | 71084 | — | 3 | 12,5% |
| Arttırma Kağıdı | 71085 | — | 2 | 10% |

### Maymun Atıcı — 5112

Grup: `MaimutaGrenadier` · Proto seviye: 37 · Rütbe: `S_PAWN`.

| Eşya | VNUM | Giyme/kullanım seviyesi | Adet | Baz düşme şansı |
|---|---:|---:|---:|---:|
| Beceri Kitabı | 50300 | — | 1 | 50% |
| Zihin Taşı Kesesi | 27999 | — | 1 | 20% |
| Efsun Nesnesi | 71084 | — | 3 | 12,5% |
| Arttırma Kağıdı | 71085 | — | 2 | 10% |

### Maymun Savaşçı — 5113

Grup: `MaimutaLuptator` · Proto seviye: 39 · Rütbe: `KNIGHT`.

| Eşya | VNUM | Giyme/kullanım seviyesi | Adet | Baz düşme şansı |
|---|---:|---:|---:|---:|
| Beceri Kitabı | 50300 | — | 1 | 50% |
| Zihin Taşı Kesesi | 27999 | — | 1 | 20% |
| Efsun Nesnesi | 71084 | — | 3 | 12,5% |
| Arttırma Kağıdı | 71085 | — | 2 | 10% |

### Maymun General — 5114

Grup: `MaimutaGeneral` · Proto seviye: 40 · Rütbe: `S_KNIGHT`.

| Eşya | VNUM | Giyme/kullanım seviyesi | Adet | Baz düşme şansı |
|---|---:|---:|---:|---:|
| Beceri Kitabı | 50300 | — | 1 | 50% |
| Zihin Taşı Kesesi | 27999 | — | 1 | 20% |
| Efsun Nesnesi | 71084 | — | 3 | 12,5% |
| Arttırma Kağıdı | 71085 | — | 2 | 10% |

### Taş Maymun — 5115

Grup: `MaimutaDePiatra` · Proto seviye: 41 · Rütbe: `S_KNIGHT`.

| Eşya | VNUM | Giyme/kullanım seviyesi | Adet | Baz düşme şansı |
|---|---:|---:|---:|---:|
| Beceri Kitabı | 50300 | — | 1 | 50% |
| Zihin Taşı Kesesi | 27999 | — | 1 | 20% |
| Efsun Nesnesi | 71084 | — | 3 | 12,5% |
| Arttırma Kağıdı | 71085 | — | 2 | 10% |

### Güçlü Maymun Asker — 5121

Grup: `MaimutaConducator` · Proto seviye: 45 · Rütbe: `PAWN`.

| Eşya | VNUM | Giyme/kullanım seviyesi | Adet | Baz düşme şansı |
|---|---:|---:|---:|---:|
| Beceri Kitabı | 50300 | — | 1 | 50% |
| Zihin Taşı Kesesi | 27999 | — | 1 | 20% |
| Efsun Nesnesi | 71084 | — | 3 | 12,5% |
| Arttırma Kağıdı | 71085 | — | 2 | 10% |

### Güçlü Maymun Atıcı — 5122

Grup: `GorilaGrenadier` · Proto seviye: 47 · Rütbe: `S_PAWN`.

| Eşya | VNUM | Giyme/kullanım seviyesi | Adet | Baz düşme şansı |
|---|---:|---:|---:|---:|
| Beceri Kitabı | 50300 | — | 1 | 50% |
| Zihin Taşı Kesesi | 27999 | — | 1 | 20% |
| Efsun Nesnesi | 71084 | — | 3 | 12,5% |
| Arttırma Kağıdı | 71085 | — | 2 | 10% |

### Güçlü Maymun Savaşçı — 5123

Grup: `GorilaLuptator` · Proto seviye: 49 · Rütbe: `KNIGHT`.

| Eşya | VNUM | Giyme/kullanım seviyesi | Adet | Baz düşme şansı |
|---|---:|---:|---:|---:|
| Beceri Kitabı | 50300 | — | 1 | 50% |
| Zihin Taşı Kesesi | 27999 | — | 1 | 20% |
| Efsun Nesnesi | 71084 | — | 3 | 12,5% |
| Arttırma Kağıdı | 71085 | — | 2 | 10% |

### Güçlü Maymun General — 5124

Grup: `GorilaGeneral` · Proto seviye: 52 · Rütbe: `S_KNIGHT`.

| Eşya | VNUM | Giyme/kullanım seviyesi | Adet | Baz düşme şansı |
|---|---:|---:|---:|---:|
| Beceri Kitabı | 50300 | — | 1 | 50% |
| Zihin Taşı Kesesi | 27999 | — | 1 | 20% |
| Efsun Nesnesi | 71084 | — | 3 | 12,5% |
| Arttırma Kağıdı | 71085 | — | 2 | 10% |

### Güçlü Taş Maymun — 5125

Grup: `GorilaDePiatra` · Proto seviye: 53 · Rütbe: `S_KNIGHT`.

| Eşya | VNUM | Giyme/kullanım seviyesi | Adet | Baz düşme şansı |
|---|---:|---:|---:|---:|
| Beceri Kitabı | 50300 | — | 1 | 50% |
| Zihin Taşı Kesesi | 27999 | — | 1 | 20% |
| Efsun Nesnesi | 71084 | — | 3 | 12,5% |
| Arttırma Kağıdı | 71085 | — | 2 | 10% |

### Güçlü Altın Maymun — 5126

Grup: `GorilaDeAur` · Proto seviye: 54 · Rütbe: `S_KNIGHT`.

| Eşya | VNUM | Giyme/kullanım seviyesi | Adet | Baz düşme şansı |
|---|---:|---:|---:|---:|
| Beceri Kitabı | 50300 | — | 1 | 50% |
| Zihin Taşı Kesesi | 27999 | — | 1 | 20% |
| Efsun Nesnesi | 71084 | — | 3 | 12,5% |
| Arttırma Kağıdı | 71085 | — | 2 | 10% |

### Buz Cadı — 1191

Grup: `IceWitch` · Proto seviye: 74 · Rütbe: `BOSS`.

| Eşya | VNUM | Giyme/kullanım seviyesi | Adet | Baz düşme şansı |
|---|---:|---:|---:|---:|
| Siyah Çelik Zırh+2 | 11292 | 66 | 1 | 12,5% |
| Siyah Rüzgar Takımı+2 | 11492 | 66 | 1 | 12,5% |
| Kara Büyü Zırh+2 | 11692 | 66 | 1 | 12,5% |
| Siyah Elbise+2 | 11892 | 66 | 1 | 12,5% |
| Şahin Kalkanı+3 | 13063 | 61 | 1 | 12,5% |
| Kaplan Kalkanı+3 | 13083 | 61 | 1 | 12,5% |
| Aslan Ağzı Kalkan+3 | 13103 | 61 | 1 | 12,5% |
| Ejderha Pulu Kalkan+3 | 13123 | 61 | 1 | 12,5% |
| Işık Saçan Çizme+5 | 15185 | 51 | 1 | 12,5% |
| Mest Eden Ayakkabı+5 | 15165 | 47 | 1 | 12,5% |
| Anka Ayakkabı+5 | 15205 | 55 | 1 | 12,5% |
| Ateş Kuşu Çizmesi+5 | 15225 | 59 | 1 | 12,5% |
| Cennetin Gözyaşı Kolye+5 | 16205 | 54 | 1 | 12,5% |
| Ametist Kolye+5 | 16185 | 50 | 1 | 12,5% |
| Beyaz Altın Küpe+5 | 17145 | 42 | 1 | 12,5% |
| Kristal Küpe+5 | 17165 | 46 | 1 | 12,5% |
| Ametist Küpe+5 | 17185 | 50 | 1 | 12,5% |
| Cennetin Gözyaşı Küpe+5 | 17205 | 54 | 1 | 12,5% |
| Eskrim Broşürü | 70031 | — | 1 | 12,5% |
| Kan Taşı | 30190 | — | 1 | 100% |

### Kırmızı Hayalet Ağaç — 2311

Grup: `Refine_2311` · Proto seviye: 80 · Rütbe: `S_PAWN`.

| Eşya | VNUM | Giyme/kullanım seviyesi | Adet | Baz düşme şansı |
|---|---:|---:|---:|---:|
| Büyülü Tohum | 30197 | — | 1 | 2% |

### Kırm.Hayalet Ağaç Kökü — 2312

Grup: `Refine_2312` · Proto seviye: 82 · Rütbe: `KNIGHT`.

| Eşya | VNUM | Giyme/kullanım seviyesi | Adet | Baz düşme şansı |
|---|---:|---:|---:|---:|
| Büyülü Tohum | 30197 | — | 1 | 2% |

### Kırmızı Orman Perisi — 2313

Grup: `Refine_2313` · Proto seviye: 83 · Rütbe: `KNIGHT`.

| Eşya | VNUM | Giyme/kullanım seviyesi | Adet | Baz düşme şansı |
|---|---:|---:|---:|---:|
| Büyülü Tohum | 30197 | — | 1 | 2% |

### Kırmızı Hayalet Söğüt — 2314

Grup: `Refine_2314` · Proto seviye: 86 · Rütbe: `S_KNIGHT`.

| Eşya | VNUM | Giyme/kullanım seviyesi | Adet | Baz düşme şansı |
|---|---:|---:|---:|---:|
| Büyülü Tohum | 30197 | — | 1 | 2% |

### Yeraltı Buz Parçası — 1131

Grup: `Refine_1131` · Proto seviye: 81 · Rütbe: `S_PAWN`.

| Eşya | VNUM | Giyme/kullanım seviyesi | Adet | Baz düşme şansı |
|---|---:|---:|---:|---:|
| Su Kristali | 30198 | — | 1 | 2% |

### Yeraltı Buz Golemi — 1137

Grup: `Refine_1137` · Proto seviye: 85 · Rütbe: `S_KNIGHT`.

| Eşya | VNUM | Giyme/kullanım seviyesi | Adet | Baz düşme şansı |
|---|---:|---:|---:|---:|
| Su Kristali | 30198 | — | 1 | 2% |

### Taş Golemi — 1501

Grup: `Refine_1501` · Proto seviye: 69 · Rütbe: `S_PAWN`.

| Eşya | VNUM | Giyme/kullanım seviyesi | Adet | Baz düşme şansı |
|---|---:|---:|---:|---:|
| Kuvars Kumu | 30195 | — | 1 | 2% |

### Setaou Lideri — 2404

Grup: `Refine_2404` · Proto seviye: 90 · Rütbe: `S_PAWN`.

| Eşya | VNUM | Giyme/kullanım seviyesi | Adet | Baz düşme şansı |
|---|---:|---:|---:|---:|
| Mavi Kristal | 30199 | — | 1 | 2% |

### Setaou Yargıcı — 2413

Grup: `Refine_2413` · Proto seviye: 95 · Rütbe: `KNIGHT`.

| Eşya | VNUM | Giyme/kullanım seviyesi | Adet | Baz düşme şansı |
|---|---:|---:|---:|---:|
| Mavi Kristal | 30199 | — | 1 | 2% |
| Şeytan Külü | 30196 | — | 1 | 2% |

### Setaou Komutanı — 2414

Grup: `Refine_2414` · Proto seviye: 97 · Rütbe: `S_KNIGHT`.

| Eşya | VNUM | Giyme/kullanım seviyesi | Adet | Baz düşme şansı |
|---|---:|---:|---:|---:|
| Mavi Kristal | 30199 | — | 1 | 2% |
| Şeytan Külü | 30196 | — | 1 | 2% |

### Komutan — 2491

Grup: `YonghanCaptain` · Proto seviye: 93 · Rütbe: `S_KNIGHT`.

| Eşya | VNUM | Giyme/kullanım seviyesi | Adet | Baz düşme şansı |
|---|---:|---:|---:|---:|
| Kıvrık Anahtar | 30179 | — | 1 | 100% |
| Şeytan Külü | 30196 | — | 1 | 0,25% |

### General — 2492

Grup: `YonghanGeneral` · Proto seviye: 95 · Rütbe: `BOSS`.

| Eşya | VNUM | Giyme/kullanım seviyesi | Adet | Baz düşme şansı |
|---|---:|---:|---:|---:|
| Kıvrık Anahtar | 30179 | — | 2 | 25% |
| Kan Taşı | 30190 | — | 1 | 25% |
| Şahin Kalkanı+3 | 13063 | 61 | 1 | 25% |
| Cennetin Gözy. Bilezik+6 | 14206 | 54 | 1 | 12,5% |
| İstiridye | 27987 | — | 1 | 25% |
| Kaplan Kalkanı+3 | 13083 | 61 | 1 | 25% |
| Aslan Ağzı Kalkan+3 | 13103 | 61 | 1 | 25% |
| Mest Eden Ayakkabı+5 | 15165 | 47 | 1 | 7,5% |
| Cennetin Gözyaşı Kolye+3 | 16203 | 54 | 1 | 12,5% |
| Ametist Küpe+4 | 17184 | 50 | 1 | 12,5% |
| Cennetin Gözyaşı Küpe+3 | 17203 | 54 | 1 | 7,5% |
| Ejderha Pulu Kalkan+3 | 13123 | 61 | 1 | 12,5% |
| Beyaz Altın Bilezik+3 | 14143 | 42 | 1 | 7,5% |
| Anka Ayakkabı+4 | 15204 | 55 | 1 | 7,5% |
| Ametist Kolye+4 | 16184 | 50 | 1 | 12,5% |

### Beran-Setaou — 2493

Grup: `BlueDragon` · Proto seviye: 97 · Rütbe: `KING`.

| Eşya | VNUM | Giyme/kullanım seviyesi | Adet | Baz düşme şansı |
|---|---:|---:|---:|---:|
| Kan Taşı | 30190 | — | 2 | 12,5% |
| Usta Savaşçı Kaskı +4 | 12284 | 80 | 1 | 5% |
| Örümcek Kapşon +4 | 12404 | 80 | 1 | 5% |
| Büyülü Kask +4 | 12544 | 80 | 1 | 5% |
| Ruh Yongası Şapkası +4 | 12684 | 80 | 1 | 5% |
| Coşku Ayakkabısı +4 | 15374 | 69 | 1 | 5% |
| Şöhret Çizmesi +4 | 15394 | 69 | 1 | 5% |
| Kirin Ayakkabı +4 | 15414 | 69 | 1 | 5% |
| Yalıçapkını Ayyakkabı +4 | 15434 | 69 | 1 | 5% |
| İstiridye | 27987 | — | 15 | 18,75% |
| Ejderha Pulu | 71123 | — | 1 | 1,25% |
| Ejderha Pençesi | 71129 | — | 1 | 1,25% |
| Taş Sanatı Kitabı | 71083 | — | 1 | 0,25% |
| Büyülü Metal | 25041 | — | 5 | 3,75% |
| Efsun Nesnesi | 71084 | — | 250 | 10% |
| Ruh Taşı | 50513 | — | 2 ayrı × 1 | 3,75% |
| Beyaz İnci | 27992 | — | 1 | 5% |
| Mavi İnci | 27993 | — | 1 | 2,5% |
| Kankırmızı İnci | 27994 | — | 1 | 1,25% |
| Kutsama Küresi | 70024 | — | 1 | 3,75% |
| Arttırma Kağıdı | 71085 | — | 5 | 10% |

### General — 2494

Grup: `HuashinCaptain` · Proto seviye: 88 · Rütbe: `S_KNIGHT`.

| Eşya | VNUM | Giyme/kullanım seviyesi | Adet | Baz düşme şansı |
|---|---:|---:|---:|---:|
| Kıvrık Anahtar | 30179 | — | 1 | 100% |

### General — 2495

Grup: `HuashinGeneral` · Proto seviye: 90 · Rütbe: `BOSS`.

| Eşya | VNUM | Giyme/kullanım seviyesi | Adet | Baz düşme şansı |
|---|---:|---:|---:|---:|
| Kıvrık Anahtar | 30179 | — | 3 | 25% |
| Kan Taşı | 30190 | — | 1 | 25% |
| Kara Büyü Zırh+1 | 11691 | 66 | 1 | 7,5% |
| Siyah Rüzgar Takımı+1 | 11491 | 66 | 1 | 7,5% |
| Siyah Elbise+1 | 11891 | 66 | 1 | 7,5% |
| Siyah Çelik Zırh+1 | 11291 | 66 | 1 | 7,5% |
| Şahin Kalkanı+4 | 13064 | 61 | 1 | 25% |
| Kaplan Kalkanı+4 | 13084 | 61 | 1 | 7,5% |
| Aslan Ağzı Kalkan+4 | 13104 | 61 | 1 | 25% |
| Cennetin Gözyaşı Kolye+4 | 16204 | 54 | 1 | 12,5% |
| Cennetin Gözyaşı Küpe+4 | 17204 | 54 | 1 | 7,5% |
| Ejderha Pulu Kalkan+4 | 13124 | 61 | 1 | 25% |
| Anka Ayakkabı+5 | 15205 | 55 | 1 | 7,5% |
| İstiridye | 27987 | — | 1 | 25% |

### Vahşi Yüzbaşı — 591

Grup: `Phase3Direct_591` · Proto seviye: 42 · Rütbe: `BOSS`.

| Eşya | VNUM | Giyme/kullanım seviyesi | Adet | Baz düşme şansı |
|---|---:|---:|---:|---:|
| Kedi Isırığı Bıçak+0 | 1040 | 36 | 1 | 20% |
| Kara Yıkım Yayı+0 | 2070 | 36 | 1 | 20% |
| Kırmızı Karınca Takım+0 | 11430 | 26 | 1 | 20% |
| Kutsama Kağıdı | 25040 | — | 2 | 50% |
| Ruh Taşı | 50513 | — | 1 | 10% |

### Dev Hastalık Taşıyıcısı — 993

Grup: `Phase3Direct_993` · Proto seviye: 61 · Rütbe: `KING`.

| Eşya | VNUM | Giyme/kullanım seviyesi | Adet | Baz düşme şansı |
|---|---:|---:|---:|---:|
| Ruh Taşı | 50513 | — | 2 | 100% |
| Kutsama Kağıdı | 25040 | — | 3 | 50% |

### Güçlü Buz Cadısı — 1192

Grup: `Phase3Direct_1192` · Proto seviye: 89 · Rütbe: `BOSS`.

| Eşya | VNUM | Giyme/kullanım seviyesi | Adet | Baz düşme şansı |
|---|---:|---:|---:|---:|
| Siyah Çelik Zırh+0 | 11290 | 66 | 1 | 12% |
| Siyah Rüzgar Takımı+0 | 11490 | 66 | 1 | 12% |
| Kara Büyü Zırh+0 | 11690 | 66 | 1 | 12% |
| Siyah Elbise+0 | 11890 | 66 | 1 | 12% |
| Şahin Kalkanı+0 | 13060 | 61 | 1 | 8% |
| Kaplan Kalkanı+0 | 13080 | 61 | 1 | 8% |
| Aslan Ağzı Kalkan+0 | 13100 | 61 | 1 | 8% |
| Ejderha Pulu Kalkan+0 | 13120 | 61 | 1 | 8% |
| Cennetin Gözyaşı Küpe+0 | 17200 | 54 | 1 | 8% |
| Cennetin Gözyaşı Kolye+0 | 16200 | 54 | 1 | 8% |
| Ruh Taşı | 50513 | — | 2 | 100% |
| Kan Taşı | 30190 | — | 1 | 40% |
| Kavrama Taşı+4 | 28430 | — | 1 | 2% |
| Öldürücü Darbe Taşı+4 | 28431 | — | 1 | 2% |
| Soğutma Taşı+4 | 28432 | — | 1 | 2% |
| Savaşcıdan Koruyan Taş+4 | 28433 | — | 1 | 2% |
| Ninjadan Koruyan Taş+4 | 28434 | — | 1 | 2% |
| Suradan KoruyanTaş+4 | 28435 | — | 1 | 2% |
| Şamandan Koruyan Taş+4 | 28436 | — | 1 | 2% |
| Canavardan Koruyan Taş+4 | 28437 | — | 1 | 2% |
| Savuşturma Taşı+4 | 28438 | — | 1 | 2% |
| Kurnazlık Taşı+4 | 28439 | — | 1 | 2% |
| Sihir Taşı+4 | 28440 | — | 1 | 2% |
| Yaşam Taşı +4 | 28441 | — | 1 | 2% |
| Savunma Taşı+4 | 28442 | — | 1 | 2% |
| Hız Taşı+4 | 28443 | — | 1 | 2% |

### Örümcek Barones — 2092

Grup: `Phase3Direct_2092` · Proto seviye: 75 · Rütbe: `KING`.

| Eşya | VNUM | Giyme/kullanım seviyesi | Adet | Baz düşme şansı |
|---|---:|---:|---:|---:|
| Zehir Kılıcı+0 | 180 | 75 | 1 | 3% |
| Aslan Kılıcı+0 | 190 | 75 | 1 | 3% |
| Şeytan Kanadı Çakram+0 | 1130 | 75 | 1 | 3% |
| Havalı Çelik Yay+0 | 2170 | 75 | 1 | 3% |
| Kin Kılıcı+0 | 3160 | 75 | 1 | 3% |
| Orkide Çan+0 | 5120 | 75 | 1 | 3% |
| Siyah Çelik Zırh+0 | 11290 | 66 | 1 | 6% |
| Siyah Rüzgar Takımı+0 | 11490 | 66 | 1 | 6% |
| Kara Büyü Zırh+0 | 11690 | 66 | 1 | 6% |
| Siyah Elbise+0 | 11890 | 66 | 1 | 6% |
| Şahin Kalkanı+0 | 13060 | 61 | 1 | 4% |
| Kaplan Kalkanı+0 | 13080 | 61 | 1 | 4% |
| Aslan Ağzı Kalkan+0 | 13100 | 61 | 1 | 4% |
| Ejderha Pulu Kalkan+0 | 13120 | 61 | 1 | 4% |
| Kristal Bilezik+0 | 14160 | 46 | 1 | 4% |
| Kristal Kolye+0 | 16160 | 46 | 1 | 4% |
| Kristal Küpe+0 | 17160 | 46 | 1 | 4% |
| Ruh Taşı | 50513 | — | 2 | 100% |
| Kutsama Kağıdı | 25040 | — | 5 | 40% |

### Dev Hayalet Ağaç — 2306

Grup: `Phase3Direct_2306` · Proto seviye: 84 · Rütbe: `BOSS`.

| Eşya | VNUM | Giyme/kullanım seviyesi | Adet | Baz düşme şansı |
|---|---:|---:|---:|---:|
| Ruh Taşı | 50513 | — | 2 | 80% |

### Hayalet Ağaç Lordu — 2307

Grup: `Phase3Direct_2307` · Proto seviye: 86 · Rütbe: `KING`.

| Eşya | VNUM | Giyme/kullanım seviyesi | Adet | Baz düşme şansı |
|---|---:|---:|---:|---:|
| Ruh Taşı | 50513 | — | 3 | 100% |

### Kharoon — 2597

Grup: `Phase3Direct_2597` · Proto seviye: 91 · Rütbe: `KING`.

| Eşya | VNUM | Giyme/kullanım seviyesi | Adet | Baz düşme şansı |
|---|---:|---:|---:|---:|
| Ruh Kristali Bilekliği+0 | 14220 | 58 | 1 | 10% |
| Ruh Kristali Kolyesi+0 | 16220 | 60 | 1 | 10% |
| Ruh Kristali Küpeleri+0 | 17220 | 62 | 1 | 10% |
| Mavi İnci | 27993 | — | 1 | 8% |
| Kankırmızı İnci | 27994 | — | 1 | 4% |
| Ruh Taşı | 50513 | — | 2 | 100% |

## 8. Klasik boss kapsaması — açık bırakılan loot yok

| İçerik | VNUM | Bu revizyonda statik özel loot durumu |
|---|---:|---|
| Vahşi Yüzbaşı | 591 | Doğrudan eşya/ruh taşı tablosu |
| Ork Reisi | 691 | Kendi sandığı: Ork Başkanının Sandığı |
| Karanlık Lider | 791 | Kendi sandığı: Öğreti Lideri Sandığı |
| Karanlık Hayalet Lider | 792 | Kendi sandığı: Hayalet Lideri Sandığı |
| Dev Hastalık Taşıyıcısı | 993 | Doğrudan eşya/ruh taşı tablosu |
| Şeytan Kralı | 1091 | Kendi sandığı: Şeytan Kral Sandığı |
| Kibirli Şeytan Kralı | 1092 | Kendi sandığı: Şeytan Kral Sandığı |
| Lusifer | 1093 | Kendi sandığı: Lusifer Sandığı |
| Güçlü Buz Cadısı | 1192 | Doğrudan eşya/ruh taşı tablosu |
| Sarı Kaplan Hayaleti | 1304 | Kendi sandığı: Sarı Kaplan H. Sandığı |
| Dokuz Kuyruk | 1901 | Kendi sandığı: Dokuz Kuyruk Sandığı |
| Kraliçe Örümcek | 2091 | Kendi sandığı: Kraliçe Örümcek Sandığı |
| Örümcek Barones | 2092 | Doğrudan eşya/ruh taşı tablosu |
| Dev Çöl Kaplumbağası | 2191 | Kendi sandığı: DevÇölkaplumbağa Sandığı |
| Alev Kral | 2206 | Kendi sandığı: Ateş Kral Sandığı |
| Kırmızı Ejderha | 2291 | Kendi sandığı: Kırmızı Ejderha Sandığı |
| Dev Hayalet Ağaç | 2306 | Doğrudan eşya/ruh taşı tablosu |
| Hayalet Ağaç Lordu | 2307 | Doğrudan eşya/ruh taşı tablosu |
| Kharoon | 2597 | Doğrudan eşya/ruh taşı tablosu |
| Azrail | 2598 | Kendi sandığı: Azrail'in Sandığı |

Önceki sürümde eksik olan Vahşi Yüzbaşı, Dev Hastalık Taşıyıcı, Güçlü Buz Cadısı, Barones, Dev Çöl Kaplumbağası, Kırmızı Ejderha, iki Ağaç bossu, Kharoon ve Azrail artık tanımlıdır. Zindan kill handler’larına ek eşya verme kodu konmadı; motorun mevcut mob_drop_item yolu kullanılır. Instance/reentry, boss izleme ve oyuncu kabulü ayrı konulardır; loot tamamlanması Faz 3’ün bütün mekaniklerinin bittiği anlamına gelmez.

## 9. Taş Kesesi (27999) açılınca ne çıkar?

Bu kese **beceriyi G’den P’ye çıkaran Ruh Taşı değildir**. Silah/zırh soket taşları ve Taş Sanatı Kitabı havuzudur. Tek açılış tek sonuç; aşağıdaki oranlar 637 toplam ağırlıktan hesaplanır.

| Eşya | VNUM | Giyme/kullanım seviyesi | Adet | Sandık içi şans |
|---|---:|---:|---:|---:|
| Kavrama Taşı+3 | 28330 | — | 1 | 5,49451% |
| Öldürücü Darbe Taşı+3 | 28331 | — | 1 | 5,49451% |
| Soğutma Taşı+3 | 28332 | — | 1 | 5,49451% |
| Savaşcıdan Koruyan Taş+3 | 28333 | — | 1 | 5,49451% |
| Ninjadan Koruyan Taş+3 | 28334 | — | 1 | 5,49451% |
| Suradan KoruyanTaş+3 | 28335 | — | 1 | 5,49451% |
| Şamandan Koruyan Taş+3 | 28336 | — | 1 | 5,49451% |
| Canavardan Koruyan Taş+3 | 28337 | — | 1 | 5,49451% |
| Savuşturma Taşı+3 | 28338 | — | 1 | 5,49451% |
| Kurnazlık Taşı+3 | 28339 | — | 1 | 5,49451% |
| Sihir Taşı+3 | 28340 | — | 1 | 5,49451% |
| Yaşam Taşı +3 | 28341 | — | 1 | 5,49451% |
| Savunma Taşı+3 | 28342 | — | 1 | 5,49451% |
| Hız Taşı+3 | 28343 | — | 1 | 5,49451% |
| Kavrama Taşı+4 | 28430 | — | 1 | 1,56986% |
| Öldürücü Darbe Taşı+4 | 28431 | — | 1 | 1,56986% |
| Soğutma Taşı+4 | 28432 | — | 1 | 1,56986% |
| Savaşcıdan Koruyan Taş+4 | 28433 | — | 1 | 1,56986% |
| Ninjadan Koruyan Taş+4 | 28434 | — | 1 | 1,56986% |
| Suradan KoruyanTaş+4 | 28435 | — | 1 | 1,56986% |
| Şamandan Koruyan Taş+4 | 28436 | — | 1 | 1,56986% |
| Canavardan Koruyan Taş+4 | 28437 | — | 1 | 1,56986% |
| Savuşturma Taşı+4 | 28438 | — | 1 | 1,56986% |
| Kurnazlık Taşı+4 | 28439 | — | 1 | 1,56986% |
| Sihir Taşı+4 | 28440 | — | 1 | 1,56986% |
| Yaşam Taşı +4 | 28441 | — | 1 | 1,56986% |
| Savunma Taşı+4 | 28442 | — | 1 | 1,56986% |
| Hız Taşı+4 | 28443 | — | 1 | 1,56986% |
| Taş Sanatı Kitabı | 71083 | — | 1 | 1,0989% |

## 10. Koşullu motor ve quest ekleri

- Seviye 40+ bosslarda C++ `three_skill_item` kuralı ek Ruh Taşı üretebilir. Bu, sandıktaki Ruh Taşı satırından bağımsızdır; sabit sandık yüzdesiyle karıştırılmaz.
- `CreateQuestDropItem`, seviye/etkinlik flag’lerine göre başka eşyalar ekleyebilir. Biyolog görevleri, etkinlikler ve at üzerindeyken kitap kancaları herkese her kesimde açık ödül değildir.
- Motorda doğrudan soket taşı için ayrı `GetDropMetinStoneVnum/Pct` yolu bulunur. Bu rehber, canlıda hangi runtime değerinin atandığını ölçmeden buna sabit bir yüzde yazmaz.
- Görevlerin kurulmuş/derlenmiş hali ve aktif event flag’leri canlı oyun testiyle ayrıca doğrulanır. Bu belge kaynak/runtime statik konfigürasyonunu doğrular; canlı kabul testini ikame etmez.

## 11. Araştırma: resmî akış ve PvP karşılaştırması

Resmî wiki eşyanın hangi sandık ailesinde olduğunu belirlemek için kullanıldı. **Resmî ve özel sunucu yüzdeleri yayımlanmıyorsa oran uydurulmadı:** bu projedeki yüzdeler 10 kişilik orta-kolay hedef için kendi denge kararımızdır. Resmî oyundaki modern 100+ içerik, lycan ekipmanı ve istemediğimiz yan sistemler bu yüzden otomatik taşınmadı.

| Kaynak | Doğrulanan karar |
|---|---|
| [Resmî Lusifer Sandığı](https://tr-wiki.metin2.gameforge.com/index.php/Lusifer_Sand%C4%B1%C4%9F%C4%B1) | Gerçek 75 silah ailesi bu sandıkta bulunur; yalnız malzemeli taslak eksikti. |
| [Resmî Zehir Kılıcı](https://en-wiki.metin2.gameforge.com/index.php/Poison_Sword) | Giyme seviyesi 75 ve Lusifer sandığı kaynak ilişkisi. |
| [Resmî Ork Reisi kutusu](https://en-wiki.metin2.gameforge.com/index.php/Chief_Orc%27s_Box) | 65 silah ve 54 zırh ailesi; erken boss = yalnız düşük seviye silah varsayımı yapılmadı. |
| [Resmî Hayalet Lider kutusu](https://en-wiki.metin2.gameforge.com/index.php/Ghost_Leader%27s_Box) | 65 silah ve 54 zırh havuzu. |
| [Resmî Kraliçe Örümcek kutusu](https://en-wiki.metin2.gameforge.com/index.php/Queen_Spider_Box) | 65 silah ve 61 zırh havuzu. |
| [Resmî Dokuz Kuyruk sandığı](https://en-wiki.metin2.gameforge.com/index.php/Nine_Tails%27_Chest) | 65 silah ve 61 zırh havuzu. |
| [Resmî Sarı Kaplan sandığı](https://en-wiki.metin2.gameforge.com/index.php/Yellow_Tiger%27s_Chest) | 65 silah ve 61 zırh havuzu. |
| [Resmî Alev Kral sandığı](https://en-wiki.metin2.gameforge.com/index.php/Flame_King%27s_Chest) | 65 silah ve 61 zırh havuzu. |
| [Resmî Şeytan Kral sandığı](https://en-wiki.metin2.gameforge.com/index.php/Demon_King%27s_Chest) | 65 silah ve 61 zırh havuzu. |
| [M2-Board yönetim rehberi](https://forum.m2-board.com/threads/ileri-seviye-gelisim-rehberi.151/) | PvP örneği: 75 sonrası Şeytan Kulesi/Lusifer sandığı üzerinden 75 silah ilerlemesi ve sandık ticareti. |
| [Resmî Barones](https://tr-wiki.metin2.gameforge.com/index.php/%C3%96r%C3%BCmcek_Barones) | 75 silah, 66 zırh, kalkan ve takı doğrudan ödül; proje +0 base ve kendi şanslarını kullanır. |
| [Resmî Azrail sandığı](https://tr-wiki.metin2.gameforge.com/index.php/Azrailin_Sand%C4%B1%C4%9F%C4%B1) | 70 silah, 66 zırh, 60 kask, Titan kalkanı ve takı ailesi. |
| [Resmî Güçlü Buz Cadısı](https://en-wiki.metin2.gameforge.com/index.php/Mighty_Ice_Witch) | Silah verilmedi: zırh, kalkan, takı, +4 soket taşı, ruh taşı ve kan taşı seçildi. |
| [Resmî Vahşi Yüzbaşı](https://en-wiki.metin2.gameforge.com/index.php/Bestial_Captain) | Kedi Isırığı/karartma yayı ve Kırmızı Karınca kıyafeti ailesi; projede +0. |
| [Resmî Dev Hastalık Taşıyıcı](https://en-wiki.metin2.gameforge.com/index.php/Giant_Plague_Carrier) | Ruh taşı ana ödül; kutsama orta-kolay destek ödülü olarak bize ait ekleme. |
| [Resmî Çöl Kaplumbağası sandığı](https://en-wiki.metin2.gameforge.com/index.php/Desert_Tortoise_Chest) | 65 silah ve 61 zırh ailesi. |
| [Resmî Kırmızı Ejderha](https://en-wiki.metin2.gameforge.com/index.php/Red_Dragon) | Güncel wiki listesi sınırlı; projedeki 50080 eski sandık için yüksek boss havuzu bilinçli PvP uyarlaması. |
| [Resmî Hayalet Ağaç](https://en-wiki.metin2.gameforge.com/index.php/Giant_Ghost_Tree) | Ana ödül ruh taşı; yeni silah havuzu uydurulmadı. |
| [Resmî Ağaç Lordu](https://en-wiki.metin2.gameforge.com/index.php/Ghost_Tree_Lord) | Ana ödül ruh taşı. |
| [Resmî Kharoon](https://en-wiki.metin2.gameforge.com/index.php/Charon) | Ruh kristali takıları, mavi/kırmızı inci ve ruh taşı seçildi. |
| [NirvanaMt2 sandık veritabanı](https://nirvanamt2.com/wiki/sandik/lusifer-sandigi) | Arama dizinindeki PvP listesi aynı altı 75 silahı, 65 silahları ve 66 zırhı ayırıyor. Doğrudan sayfa isteği 500 verdi; yayımlanmamış yüzdeleri kaynak alınmadı. |

Eski Esoteric Leader kutusunun İngilizce sayfası 404 verdi; bu kutunun birebir resmî içeriği doğrulandı diye yazılmadı. Projedeki Karanlık Lider sandığı, erken boss havuzunu paylaşan açık bir PvP denge kararıdır. Resmî +1/+2/+3 rastgeleleri yerine mevcut +0 base/refine ekonomisi korundu; oyuncu geliştirme zinciri atlanmadı.

## 12. Kaynak dosyalar ve doğrulama

Bu belge `python3 platform/tools/drop_catalogue.py` çıktısıdır. `python3 platform/tools/drop_catalogue.py --check` kayıtlı belgenin verilerle aynı olduğunu denetler.

| Dosya | SHA-256 |
|---|---|
| `platform/gameplay/phase3_loot.json` | `08c8ca6a0f952153a1c6b8b85695cd75c9264c71626a808c6a5fb83ecc0a1e4e` |
| `runtime/freebsd/share/locale/europe/mob_drop_item.txt` | `d02e1a60a3df125f7c293e5c8a3e16c162926deaffad6d666b3467ca91ee1103` |
| `runtime/freebsd/share/locale/europe/special_item_group.txt` | `af4371b9ca4c88b5993e10d569848a228002c5ed55738dc868de2adeb7ffa288` |
| `runtime/freebsd/share/conf/item_proto.txt` | `bc6ea5af8df343a71e518cd89bada151c3703d0924d135b3f46542649f7e5270` |
| `runtime/freebsd/share/conf/mob_proto.txt` | `b66a8c263ce7c7d3426ff415d9563292c3fa8830f47d5973b4f16581a8387718` |

Kontroller: bütün ödül VNUM’ları gerçek proto’da bulunmalı; sandık ağırlıkları 100 olmalı; gerçek 75 silah ailesi eksiksiz ve doğru seviyede olmalı; Havalı Çelik yanlışlıkla 2150 olmamalı; 75 silahlar metin havuzuna geri sızmamalı. Oyun içi drop/ortalama-beceri üretimi, sandık açma ve envanter davranışı bakım kurulumu ardından oynanarak doğrulanır.

