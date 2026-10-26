# Klasik dışı rastgele efsun izinleri — 22 Ekim 2026

Kullanıcı: hiçbir bonus normal edinim/ekipman sınırlarının dışında gelmemeli.
Önceki çalışmada ayrı bırakılan 14 tür artık rastgele normal havuzdan kapalı.

## Uygulanan değişiklik

- Dört sınıfa karşı güç ve dört sınıf direnci.
- Genel canavarlara karşı güç.
- Ortalama/beceri hasarı ve bu ikisine direnç.
- Düz savunma değeri.

Bu türlerin normal `item_attr` tablosundaki silah, gövde, bilezik, ayakkabı,
kolye, kask, kalkan, küpe, tılsım ve üç kostüm izin sütunu sıfırlandı.
Efsun ekleme/yenileme kodu sıfır izinli türleri seçilebilir havuza almıyor.
Kalkan dahil hiçbir normal yuvada bu türler rastgele seçilemez.

Silahın doğal ortalama/beceri üretimi, sabit proto bonusları ve ayrı nadir
6–7 tablosu korunur. Diğer 45 türün klasik yuva dağılımı ve sabit değerleri
korunur. Bunların seçim ağırlıkları ve değer kademeleri değiştirilmedi.

## Canlı durum

**Canlı DB'ye uygulandı ve sonraki yetkili eşya temizliği bakımında bütün oyun
süreçleri yeniden başladığı için tablo core'lara alındı.** Aşağıdaki GM
yenileme yolu gelecekteki tablo değişiklikleri içindir.
GM karakterinden `/reload p` çalıştır; bütün core'ların `RELOAD: ItemAtt: 59`
kaydını verdiği doğrulanmalı. Bu komut diğer protoları da yeniler. Alternatif,
operatörün koordineli game/db yeniden başlatmasıdır. Otomatik servis restart'ı
ve Chrome/oyun testi yapılmadı.

- Yedek: host `/home/m2web/backups/classic-attributes-rp0lju4k`.
- `before.json`, `after.json`, `rare.json`: tam karşılaştırma kayıtları.
- `rollback.sql`: yalnız sahip olunan 14 satırın eski izinlerini geri yükler.
- Gerçek MariaDB'de önce bağlantıya özel geçici tabloda denendi; sadece
  beklenen 14 satır/12 izin sütunu değiştiği doğrulandı.
- Canlı uygulamada aynı kontrol tekrar geçti. Diğer 45 satır, bütün değerler,
  ağırlıklar ve nadir tablo önceki snapshot ile birebir eşleşti.
- Kaynak seed ile sınırlı geçiş aynı politikayı taşır; yerel regresyon
  kontrolleri yeni kapatma ve önceki 45 tür için geçer.

## Mevcut oyuncu eşyaları

Salt okunur taramada ilk beş efsun slotunda bu türleri taşıyan **11 mevcut
eşya** bulundu; bunların **1'i kalkan**. Doğal efsunlu silahlardaki **13
ortalama/beceri slotu** bu sayımdan hariç tutuldu. Oyuncu kimlikleri rapora
yazılmadı. Henüz hiçbir mevcut eşyanın efsunu silinmedi/dönüştürülmedi.

Tarama normal 1–5 slotları içindir. Eski eşyalar yeni üretim havuzundan
bağımsız saklanır; bu geçiş eski eşyaları kendiliğinden temizlemez.

Kullanıcı daha sonra 11 eşyanın temizlenmesini onayladı. Eşya bazında liste,
hazır bakım komutu ve korunan alanlar: [eski eşya temizliği](EFSUN_ESKI_ESYA_TEMIZLIGI.md).

Kaynaklar: [geçiş SQL'i](../content/server/sql/migrations/20261022_classic_attribute_permissions.sql),
[yedekli uygulayıcı](../platform/deploy/apply_classic_attributes.py),
[kaynak seed](../content/server/sql/seed_item_attr.sql),
[testler](../platform/tools/test_normal_attributes.js),
[önceki canlı izin listesi](EFSUN_ANOMALI_LISTESI.md).
