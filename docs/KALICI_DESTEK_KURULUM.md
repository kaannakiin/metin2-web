# Kalıcı destek sürümü — kuruluma hazır

22 Ekim 2026. **Kod, sunucu ve web istemcisi derlendi; testler geçti ve canlı
dosyaların yedekleri alındı. Canlı oyun henüz değiştirilmedi.**

## İçerik

- Dört Ejderha Tanrı desteği, kritik/delici, altı şebnem ve iki yeni kalıcı
  iksir: toplam **14 farklı nesneden birer adet**, seviye **1**.
- Kalıcı yeşil iksir `72737`: saldırı hızı +30. Mor iksir `72738`: hareket
  hızı +40. Kullanım adet tüketmez; ikinci tıklama kapatır/açar.
- Aktiflik nesnede saklanır, login sırasında tek etki olarak geri kurulur.
  Ölümde korunur; süre tüketmez. Aktif nesne kilitlidir. Aynı ailede süreli
  bonusla katlanmaz. Sarı şebnem ayrı +8 saldırı hızı olarak kalır.
- Yeni/eski karakter teslimi nesne başına işaretlidir; dolu envanterde sonraki
  giriş/seviye artışında devam eder. Eski süreli stoklar silinmez.
- Ek güç ekipmanlarında tılsım, saç/kuşak/aura kostümü, kemer/yüzük, simya ve
  büyüyen pet edinimi/kullanımı engellenir. Binek, gövde/silah kostümü ve basit
  pet korunur. Eski yasak ekipman silinmez, bonus vermez ve UI'da çıkarılabilir.
- 45 normal efsun türü sabit değer/klasik ekipman izinlerine geçer; HP **3000**.
  Önceden konuşulan 14 anomali ve nadir efsun havuzu korunur. Var olan oyuncu
  eşyalarının efsunları ve başlangıç ekipmanının elle yazılmış bonusları
  topluca yeniden yazılmaz.

## Tek komutla etkinleştirme

Bu komut hazır istemciyi yayımlar, oyun hizmetini kısa süre durdurur, sınırlı
SQL geçişini ve sunucu/quest dosyalarını kurar, yeniden başlatır. Başarısızlıkta
istemci ile sunucu/quest/efsun tablosu geri alınır. Diğer hizmetlere dokunmaz.

```sh
ssh root@88.99.1.151 'bash /home/m2web/permanent_support_install_host.sh /usr/metin2-support-20261022-190014'
```

Operatör adımının gerekçesi: [AGENTS.md satır 49](../AGENTS.md#L49),
“Auto mode refuses VM service restarts ... prepare a script and hand those
steps to the user.” Otomatik yeniden başlatma çalıştırılmadı.

## Hazır dosyalar ve yedekler

| Yer | İçerik |
| --- | --- |
| VM `/usr/metin2-support-20261022-190014/out` | Derlenmiş game/db ve test çalıştırıcıları |
| VM aynı dizinde `READY` | Son kaynaklarla derleme ve quest testleri tamamlandı |
| VM aynı dizinde `previous/` | Canlı game/db, ilgili quest dosyaları ve item_attr veri yedeği |
| VM aynı dizinde `candidate.sha256`, `data.sha256` | Kurulacak dosyaların bütünlük kontrolü |
| Host `/home/m2web/kit/dist/site` | Eşleşen, özel giriş dosyası içermeyen web paketi |
| Host `/home/m2web/dev/support-client.sha256` | Test edilmiş istemcinin sabitlenmiş hash listesi |
| Host `/home/m2web/dev/logs/permanent-support-client.log` | İstemci build/patchcheck ve paket doğrulaması |

Kurulum başka bir derlemenin üzerine sessizce yazmaz: istemci hash'leri,
sunucu hash'leri, canlı dosya ve efsun tablosu başlangıç durumunu kontrol eder.
Corpus değişmedi: **1370 immutable parça aynı**, CDN yüklemesi gerekmez.

## Tamamlanan doğrulamalar

- FreeBSD game/db derlemesi başarılı; web istemcisinde 359 C++ nesnesi,
  sıfır derleme hatası. `patchcheck` sıfır kaçırılan yama.
- Üretim kalıcı destek kodunu kullanan C++ testi: aç/kapat, ikinci kopya,
  süreli etki değişimi, şebnem+iksir beraberliği, yeniden giriş, sahipsiz etki,
  ölümde kullanım engeli ve seviye sınırları.
- Gerçek quest derleyicisinin çıktısıyla Lua testi: dolu envanter, kısmi
  teslimin tamamlanması, 14 nesne, tekrar teslim engeli, mevcut kalıcı nesne.
- UI/politika testleri: izinli yuvalar, eski takılı eşyanın erişilebilirliği,
  yeni iksir simgeleri, istemci/sunucu proto politikasının birebir eşitliği.
- Sekiz normal efsun regresyon testi ve MariaDB geçici tablosunda geçiş,
  idempotans/eksik satır kontrolü. Gerçek tablo bu testlerde değiştirilmedi.
- Gerçek üretilmiş Python başlangıç/import testi ve public paket kontrolü.
- Eski kaynak string'lerinin derlenen baytları korundu; git diff boşluk kontrolü temiz.

## Kurulumdan sonra oyun içi kontrol

Tarayıcıyı yenile. Bir karakterle giriş yap; 14 desteği açıp bonusları kontrol
et. Öl/diril, çık/gir ve kanal değiştir; etkilerin korunduğunu doğrula. Tekrar
tıklayıp kapatma/açmayı ve süreli iksirle katlanmadığını kontrol et. Bu gerçek
oyun içi kabul testi henüz yapılmadı; derleme/birim testleri bunun yerine geçmez.

Uygulama kaynakları: [destek davranışı](../apps/server/game/src/pvp_support.h),
[proto politikası](../apps/server/common/pvp_support_proto.h),
[başlangıç teslimi](../runtime/freebsd/share/locale/europe/quest/quest_tr/_npc_talk_mission/permanent_support.quest),
[kurulum betiği](../platform/deploy/permanent_support_install_host.sh).
