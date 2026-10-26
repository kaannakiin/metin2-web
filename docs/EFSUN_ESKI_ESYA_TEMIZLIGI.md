# Uygunsuz efsun taşıyan 11 eşya ve temizlik

22 Ekim 2026. Kullanıcı bu eşyalardaki uygunsuz efsunların kaldırılmasını
onayladı ve ardından açıkça uygulanmasını istedi. **Canlıya uygulandı: 11
eşyadan 15 hatalı normal efsun temizlendi.** Canlı satırlar yeniden okundu;
hedef eşyalarda kapalı tür kalmadığı ve diğer alanların korunduğu doğrulandı.
Başlangıç görevi kuruldu; altı süreç ve altı port sağlıklı. Eşya yedeği:
`/home/m2web/backups/item-attribute-cleanup-q4lv7_si`.

## Hangi eşyalar?

Aşağıdaki efsunlar son hazırlık taramasındandır. Karakterler/switchbot oyun
içinde değiştirebildiği için temizlik, bakımda son kaydedilen değerleri yeniden
okur. Yalnız bu 11 eşya kimliği işleme alınır.

| Karakter | Eşya | Kaldırılacak uygunsuz efsunlar | Eşya ID |
| --- | --- | --- | ---: |
| sura | Dolunay Kılıcı+9 | Şamanlara karşı güçlü %3 | 20000685 |
| numan2 | Kılıç+9 | Canavarlara karşı güçlü %10 | 60000075 |
| numan2 | Geniş Mızrak+9 | Canavarlara karşı güçlü %10 | 60000076 |
| numan | Siyah Rüzgar Takımı+0 | Düz savunma +10 | 60001096 |
| numan | Cennetin Gözyaşı Kolye+0 | Beceri hasarına direniş %2 | 60001206 |
| numann | Kılıç+9 | Canavarlara karşı güçlü %10 | 60001230 |
| sura | Yin-Yang Zırh+9 | Düz savunma +15, ortalama zarar %8 | 60001358 |
| sura | Abanoz Küpe+9 | Sura direnci %2, şaman direnci %3 | 60001359 |
| sura | Deri Çizme+9 | Beceri hasarı %6 | 60001360 |
| sura | Beşgen Kalkan+9 | Savaşçı direnci %5, ninja direnci %3, şamanlara karşı güçlü %5 | 60001361 |
| sura | Alaycı Kask+9 | Canavarlara karşı güçlü %10 | 60001362 |

Dolunay'ın doğal PvM ortalaması/ortalama ve beceri çifti korunur. Eşya
silinmez; soket, taş, artı seviyesi, nadir 6–7, konum/sahip ve geçerli normal
efsunlar korunur. Kaldırılan normal efsunlardan sonra kalanlar boşluk
bırakmadan ilk slotlara alınır. Yeni bir efsun rastgele üretilmez.

## Uygulanan bakım komutu

Mac terminalinde:

```sh
ssh root@88.99.1.151 'python3 /home/m2web/cleanup_invalid_attributes.py --apply'
```

Bu komut yalnız bu oyunu kısa süre bakıma alır. Önce game/auth ve oyun DB-cache
süreçleri kayıtlarını bitirip kapanır; MariaDB çalışmaya devam eder. Güncel
11 satırın tam yedeği alınır. Yalnız hatalı ilk beş slot bonusları temizlenir;
sonuç bütün satır alanlarıyla karşılaştırılır. Başarısızlıkta bonuslar geri
yüklenir. Oyun yeniden açılır ve altı süreç/port doğrulanır.

Başlangıç silahlarına elle verilen `Canavarlara karşı güçlü %10` da görevden
kaldırılır. Canlı başlangıç kaynağıyla adayın tek farkının bu üç ekleme
olduğu doğrulandı; gerçek `qc` ile görev derlendi. Görev dosyaları ayrıca
yedeklenir; kurulum hatasında eski görev de geri yüklenir.

Yeniden başlatma, canlı DB'de kapatılmış 14 rastgele efsun iznini de bütün
core'lara yükler. Satıcı adayı bu komutla kurulmaz; ayrı hazırlanmış satıcı
kurulum komutu aynı kalır.

## Bakım yetkisi ve mevcut durum

[AGENTS.md](../AGENTS.md) ilk hazırlıkta bakım komutunun operatöre verilmesini
gerektiriyordu. Kullanıcı daha sonra incelenebilir bakım için açıkça
“uygula bunları” talimatını verdi; bakım bu yetkiyle çalıştırıldı. Bazı eşyalar
takılı veya switchbot'ta olduğundan süreçler kayıtlarını bitirip kapandıktan
sonra DB temizlendi. Yeniden başlatma, kapalı efsun izinlerini de core'lara aldı.

Başlangıç sırasında SSH bağlantısı kapanışta takıldı; oyun süreçlerinin sağlıklı
olduğu doğrulanıp yalnız bekleyen bakım SSH istemcisi kapatıldı. Eşya ve görev
kurulumu sonrasında yeniden doğrulandı, tamamlanma işareti yazıldı. Bakım
aracında stdin ve servis log yönlendirmeleri düzeltildi. Tekrar çalıştırma
tamamlanmış işaretini görüp veri değiştirmeden durur.

## Hazırlık ve testler

- 5 yerel test: kalkanın seçici temizliği, slotların sıkıştırılması, doğal
  Dolunay bonuslarının korunması, zırhtaki ortalamanın kaldırılması,
  tekrar uygulamada kararlılık ve başlangıç bonusu kontrolü.
- Gerçek VM quest derlemesi: `/usr/home/attribute-cleanup-welcome-20261022`.
- Host araçları: `/home/m2web/cleanup_invalid_attributes.py` ve
  `/home/m2web/prepare_attribute_cleanup_host.sh`.
- VM yardımcı: `/usr/home/cleanup_invalid_attributes_vm.sh`.
- Uygulama yedeği çalıştırma sırasında hostta
  `/home/m2web/backups/item-attribute-cleanup-*` altında oluşur: tam önce/sonra
  JSON, plan ve yalnız sahip olunan alanlara ait `apply.sql` / `rollback.sql`.
- Görev yedeği VM hazırlık dizininde `previous-source.lua` ve
  `previous-objects.tar` olarak alındı; yeni görev canlıya kuruldu.
