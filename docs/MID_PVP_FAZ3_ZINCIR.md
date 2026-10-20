# Faz 3 orta kolay zindan zincirleri

20 Ekim 2026. Loot v4 ve görevler **20261020-153340**, iki kaynak bossun süreleri
**20261020-153638** ile canlıda. Günlük giriş kotası yoktur.

## Farm ve giriş malzemeleri

| Kaynak | Düşüş | Şans |
|---|---|---:|
| Komutan/General 2491, 2492, 2494, 2495 | 3 Kıvrık Anahtar | %100 |
| Lusifer 1093 | 2 Küçülen Kafa | %100 |
| Kraliçe Örümcek 2091 | 1 Kraliçe Örümcek Zehri | %100 |
| Buz Cadısı 1191/1192, General 2492/2495, Beran 2493 | 1 Kan Taşı | %100 |
| Beş normal örümcek türü 2001–2005 ve 2051–2055 | Kendi üretim malzemesi, 1 adet | %25 |
| 13 klasik sandıklı boss | Kendi sandığı, 1 adet | %100 |

Bu kayıtlar mevcut sunucunun `Type limit`, `level_limit 0` yolunu kullanır:
yüzdeler seviye cezasından bağımsızdır. Diğer ekipman ve metin kayıtları kendi
eski seviye/drop politikasını korur. Sandık içi silah/zırh ağırlıkları v3 ile aynıdır.

Kraliçe'nin mevcut 2019 grubu 15400 saniye yerine 900 saniyede; Sürgün 2'nin
mevcut Komutan 2491 kaydı 1200 yerine 900 saniyede doğar. Yer, alan ve adet aynı.

## Beran Setaou

75 seviye, kişi başına 3 Kıvrık Anahtar. Solo veya grup girişi mümkündür;
solo girişte gruptan ayrılmak gerekir. Grup lideri başlatır, tüm üyelerin yakında,
aynı haritada ve şartları tamamlamış olması gerekir. Önce tüm üyeler kontrol
edilir, ardından maliyet kişi başına bir kez alınır.

Mevcut metin/Komutan dalgaları ve Beran sırası korunur. Başarılı kesim sonrası
bekleme 10 dakikadır; günlük kota veya EP bileti eklenmez.

## Lusifer ve Katakomb

Kuledeki normal Lusifer tamamlaması, içerideki oyuncular için kalıcı
`midpvp_progression.tower_done` kaydı oluşturur. Katakomb 75 seviye ve bu kaydı ister.

Katakomb Bekçisi'nin mevcut orta-kolay instance başlangıcı korunur. Alternatif
Kud Heykeli yolu da aynı seviye/tamamlama kontrolünü kullanır; o yolda liderden
yalnız 1 Ruh Kristali Anahtarı alınır, bütün anahtar yığını silinmez.

Küçülen Kafa girişte alınmaz. İkinci kat geçişinde içerideki her katılımcı için
1 kafa kontrol edilir; herkes uygunsa birer tane alınır ve geçiş açılır.
Altıncı kat oda kapısı ikinci kafa istemez. Mevcut katlar ve Azrail sırası korunur.
Kule ve Katakomb başarılı kesim sonrası 10 dakika bekler.

## Uriel ve Barones

50 seviyeden itibaren bir defalık hazırlık:

1. Köyde Yüzbaşı'ndan **Barones icin hazirlik** konuşmasını aç. İlk görüşmede
   1 Geçit Bileti verilir; tekrar konuşarak ödül çoğaltılamaz.
2. Örümcek 3'te Mezar Taşı'ndan **Mezar tasini incele** konuşmasını aç.
3. Uriel'de **Barones hazirligini tamamla** ile üretim iznini al.

Uriel'in **Arachnida Anahtari uret** seçeneği aşağıdakilerin her birinden 1 adet
alarak %100 başarıyla 1 anahtar verir: Kraliçe zehri 30326, zehir kesesi 30025,
ağ 30056, gözler 30057, yumurta kesesi 30058, bacaklar 30059. Yang ücreti yoktur.
Eksik malzemede veya boş yer yoksa malzeme alınmaz.

Barones girişi her yolda 50 seviye, üretim hazırlığı ve kişi başına 1 anahtar ister.
Zindan önce Baron 2094'ü çıkarır. Baronun Flütü 30327 kullanıldığında Barones 2092
ve yumurtalar çıkar. Flüt yalnız bu instance'da Baron öldükten sonra kullanılabilir;
ikinci kullanım ikinci bir Barones çıkarmaz. Yumurta mekaniği ve 20 dakikalık toplam
süre korunur. Başarılı kesim sonrası bekleme 10 dakikadır.

## Kaynaklar ve derlenmiş görevler

Aktif dört kaynak `quest/quest_tr/_midpvp` altındadır. Eski cp1254
`_alldungeons` varyantları korunur; `quest_list` aynı quest isimlerinin yalnız yeni
profilini seçer. `midpvp_progression.lua` hazırlık ve Uriel üretimini yönetir.
`platform/tools/progression_profile.py` eski mekanikleri ASCII uyumlu aktif
profil olarak üretir; girişler atomik grup kontrolüyle yenilenir.

Beş görev VM'nin gerçek `qc` derleyicisiyle hazırlık dizininde derlendi. Canlıdaki
102 derlenmiş dosya `platform/tools/install_quest_objects.py` ile repoya eşlendi.
Yalnız bu beş quest namespace'i değiştirildi. Canlı listede bulunmayan opsiyonel
`mid_pvp_rewards.lua` araştırma dalındaki listeye rağmen etkinleştirilmedi.

Client/engine/protokol flag'i değiştirilmedi; yeni istemci derlemesi gerekmedi.
Unit/regresyon veya oyun testi çalıştırılmadı. Oyun kabulünü kullanıcı yapacak.
Faz 3'ün genel boss izleme ve tüm uç durum kabulü bu kayıtla kapanmış sayılmaz.

## Yayın ve geri alma kayıtları

- Görev/drop yayını: host `/home/m2web/progression-20261020-153340`,
  VM `/usr/metin2-progression-20261020-153340`.
- İki spawn süresi: host `/home/m2web/progression-20261020-153638`,
  VM `/usr/metin2-progression-20261020-153638`.
- İki sürümde de `INSTALLED`, önceki dosyalar için `previous.tar`, kurulum
  öncesi/sonrası hash kayıtları ve servis logları bulunur. Kurucu yalnız Metin2
  kullanıcısının süreçlerini kayıtlar yazılana kadar bekleyerek durdurur;
  başarısız kurulumda önceki dosyaları geri yükler.
- İki kurulumdan sonra altı süreç ve altı port sağlıklıdır. Başarı yalnız yerel
  komut çıkışından değil VM `INSTALLED` kaydından da doğrulandı.

[Önceki wiki denetimi](FAZ3_KLASIK_ZINCIR_DENETIMI.md) ·
[Güncel tam düşüş rehberi](DROP_REHBERI.md).
