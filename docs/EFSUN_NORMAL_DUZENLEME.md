# Normal efsun düzeltmesi — 22 Ekim 2026

> **Sonraki karar:** aşağıda “ayrı karar bekleyen” olarak anlatılan 14 türün
> rastgele izinleri de kapatıldı; yalnız bu 14 satırın 12 izin sütununa dokunan
> geçiş canlı DB'ye uygulandı. GM `/reload p` ile bütün core'lara alınmalıdır.
> [Yeni uygulama notu](EFSUN_KLASIK_IZINLER.md). Belgenin devamı ilk 45 satırlık
> düzenlemenin tarihsel kapsamını açıklar.

> **Sonraki kapsam kararı:** Tılsım ve saç kostümü oyundan çıkarılacak.
> Önceki tılsım onayı artık geçerli değil. Aşağıdaki SQL normalleştirmesinde
> korunan sütunlar bu sistemleri açık tutma kararı değildir; kapatma işi
> [kalıcı başlangıç/sade ekipman tasarımında](BASLANGIC_KALICI_DESTEK_TASARIMI.md).

**Durum: repo değişikliği hazır; canlı tablolara uygulanmadı.** Kullanıcı normal
efsun dağılımının düzeltilmesini, değerlerin sabit olmasını ve HP'nin 3000 olmasını
istedi. Kostüm ve tılsımda da aynı sabit değerleri ayrıca onayladı.

## Yapılan değişiklik

- 45 normal efsunun sekiz ekipmandaki izinleri araştırmadaki klasik referansa
  çekildi. Bütün beş değer kademesi aynı: ekleme ve değiştirme hangi kademeyi
  seçerse seçsin aynı bonus değeri oluşur.
- HP **3000**; zehirleme/sersemletme/yavaşlatma %8; kritik/delici %10;
  statlar +12; yarı insan %10; beş yaratık ırkı %20; savunmalar %15.
  Tam sabit değerler ve yuvalar [güncel rehberde](EFSUN_REHBERI.md).
- Bağışıklık kalkana, zehirleme silah/kaska, saldırı değeri zırha taşındı.
  HP zırh/bilezik/ayakkabı/kolyeye; statlar silah/kalkana sınırlandı.
- Kostüm ve tılsımda **izinler korunuyor**, düzeltilen efsunların değerleri
  sabitleniyor. Efsun seçim ağırlıkları ve normal beş slot sınırı korunuyor.
- Araştırmadaki sürüm farkları için güncel resmî referans seçildi: zırhta SP,
  kolyede SP üretimi/emmesi/çalması açık; küpede zehir direnci %5.

## Ayrı karar bekleyen 14 satır

Bu satırların hem izinleri hem değerleri eski haliyle duruyor; sabitleme bu
gruba uygulanmadı. Dolayısıyla bütün efsun havuzunun temizlenmesi henüz bitmiş
sayılmaz: bu bonuslar mevcut izinlerine göre hâlâ gelebilir.

| Grup | Satırlar |
| --- | --- |
| Sınıfa karşı güç | `ATTBONUS_WARRIOR`, `ATTBONUS_ASSASSIN`, `ATTBONUS_SURA`, `ATTBONUS_SHAMAN` |
| Sınıf direnci | `RESIST_WARRIOR`, `RESIST_ASSASSIN`, `RESIST_SURA`, `RESIST_SHAMAN` |
| Genel canavar gücü | `ATTBONUS_MONSTER` |
| Ortalama / beceri direnci | `NORMAL_HIT_DEFEND_BONUS`, `SKILL_DEFEND_BONUS` |
| Normal havuzdaki ortalama / beceri hasarı | `NORMAL_HIT_DAMAGE_BONUS`, `SKILL_DAMAGE_BONUS` |
| Düz savunma değeri | `DEF_GRADE_BONUS` |

Son üç satır da klasik normal listede bulunmadığından anomali kararı kapsamında
korundu. Doğal ortalama/beceri üretimi (`item_addon.cpp`) ayrı mekanizmadır ve
değişmedi. Nadir 6–7 havuzunun 39 satırı değişmedi.

## Mevcut eşyalara etkisi

SQL geçişi `player.item` tablosuna dokunmaz. Mevcut eşyalar ve başlangıç questinin
elle bastığı bonuslar topluca dönüştürülmez. Yeni normal efsun ekleme/yenileme,
sunucu yeni tabloyu aldıktan sonra yeni izin ve değerleri kullanır. Sadece yeni
bir slot eklemek önceki slotları düzeltmez; efsun yenilemek normal slotları yeniden
üretir. Eşyanın kendi proto özellikleri ve doğal ortalama/beceri çifti ayrı kalır.

## Dosyalar ve doğrulama

- Hedef karar: [PVP_HEDEF.md](../PVP_HEDEF.md).
- Yeni kurulum verisi: [seed_item_attr.sql](../content/server/sql/seed_item_attr.sql).
- Mevcut DB için sınırlı geçiş: [20261022_normal_attributes.sql](../content/server/sql/migrations/20261022_normal_attributes.sql).
- Tekrarlanabilir kontroller: [test_normal_attributes.js](../platform/tools/test_normal_attributes.js).
- Rehber üreticisi: [attribute_catalogue.py](../platform/tools/attribute_catalogue.py).

Yerel kontrol: `node --test platform/tools/test_normal_attributes.js` — **8/8**.
Kontroller: izinler, HP 3000, bütün kademe/yuvada sabit değer, seed/geçiş uyumu,
14 ertelenen satırın ve 39 nadir satırın korunması, seçim ağırlıkları ve
kostüm/tılsım izinlerinin korunması, SQL güncellemesinin kapsam sınırı.

MariaDB **10.11.19** üzerinde bağlantı ömürlü geçici tablo testi de geçti:
45 sabit satır, HP 3000, korunan 14 satır, korunan 59 satırın ağırlık/ek yuva
izinleri ve ikinci uygulamada aynı sonuç. Gerçek `player.item_attr` tablosunun
59 satırı önce/sonra eşleşti. Ayrı geçici tabloda HP satırı çıkarıldığında
ön kontrol hatası istemciyi durdurdu; UPDATE ve devam işareti çalışmadı.
Geçici tablolar bağlantı kapanınca silindi; canlı oyun verisi değiştirilmedi.
Üretilen rehber kaynakla eşleşiyor; `git diff --check` temiz.

## Canlıya alma

Motor/istemci derlemesi gerekmez. **Bootstrap seedini canlıda çalıştırma:** normal
ve nadir tabloları silip yeniden doldurur. Mevcut DB için yalnız tarihli geçiş
dosyası kullanılmalı; `mysql`/`mariadb` istemcisi `--force` olmadan çalıştırılmalı.
Geçişte eksik normal satır varsa ön kontrol güncellemeden önce durur.

1. `player.item_attr` tablosunu yedekle; yedeğin geri okunabildiğini doğrula.
2. Tarihli SQL geçişini uygula. Yalnız 45 satırın değerleri ve sekiz standart
   ekipman sütunu güncellenir. Tekrar çalıştırmak aynı sonucu verir.
3. Mevcut GM **`/reload p`** yoluyla bütün game core'larının yeni tabloyu aldığını
   doğrula. Kaynakta DB `QUERY_RELOAD_PROTO` normal/nadir efsunları gönderir,
   game `CInputDB::ReloadProto` haritaları yeniden kurar. Bu komut diğer proto
   tablolarını da yeniler; bekleyen başka DB/proto değişiklikleri kontrol edilmeli.
   `/reload a` efsun değil, yönetici bilgisidir.
4. Core loglarında `RELOAD: ItemAtt: 59` görülmeli. Oyunda HP'nin yalnız dört
   standart yuvada 3000, zehrin silah/kaskta %8 ve bağışıklığın kalkanda geldiği
   yeni üretilen deneme eşyalarıyla kontrol edilmeli.
5. GM yenileme yolu kullanılamıyorsa koordineli game/db bakım yeniden başlatması
   kullanıcı adımıdır; [AGENTS.md](../AGENTS.md) otomatik VM servis restartını
   yasaklar. Bu çalışma servisleri yeniden başlatmadı.

Geri alma: yalnız `item_attr` yedeğini geri yükle, ardından tabloyu aynı yenileme
yoluyla core'lara gönder. Geçişten sonra üretilen eşyalar da otomatik geri alınmaz;
oyuncu eşyalarının toplu dönüşümü bu işin kapsamı dışında.
