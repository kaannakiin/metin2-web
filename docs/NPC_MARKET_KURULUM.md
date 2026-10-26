# Satıcı revizyonu — kuruluma hazır

22 Ekim 2026. Aday gerçek FreeBSD game derlemesinden geçti; canlı satıcı
henüz değiştirilmedi. Tarayıcı/oyun testini kullanıcı yapacak.

- Kutsama Küresi `70024`: bir adet **1.000.000 Yang**.
- 14 kalıcı başlangıç desteği: her birinden bir adet **1.000 Yang**.
- Küçük/orta HP-SP, süreli yeşil/mor iksirler ve iki dönüş kâğıdı kaldırılır.
- Büyük HP-SP ve Güneş/Ay özütleri kalır. Market tek sayfa, 24 ürün.
- Silahçı/zırhçı stokları, oyuncu envanterleri ve başlangıç teslimi değişmez.
- Kürenin eski 30 milyon Yang geri satış değeri, sunucuda en fazla
  **500.000 Yang** olur. Satın al/sat döngüsü para üretemez.

## Canlıya kurulum

Mac terminalinde çalıştır:

```sh
ssh root@88.99.1.151 'bash /home/m2web/install_npc_market_host.sh'
```

Bu adım oyunun hizmetlerini kısa süre durdurur; yedekli kaynak/binary ve
satıcı SQL değişimini yapıp oyunu yeniden başlatır. Satırların fiyat/adet/
soket/efsunları doğrulanamazsa önceki sürüme döner. Diğer host hizmetlerine,
istemci paketine ve corpus'a dokunmaz.

Otomatik yeniden başlatma yapılmamasının nedeni [AGENTS.md](../AGENTS.md):
“Auto mode refuses VM service restarts and Traefik/IaC changes even with
allow rules; prepare a script and hand those steps to the user.”

## Doğrulama ve geri dönüş

- VM adayı: `/usr/metin2-progression-20261022-202621` (`READY`).
- Kaynak tabanı: kurulu kalıcı destek sürümünün
  `/usr/metin2-support-20261022-190014/apps/server` ağacı. Eski ana kaynak
  ağacından derlenmedi; kalıcı destek düzeltmeleri korunur.
- Yerel üç test geçti: 24 ürün/fiyat/kaldırılanlar; diğer dört mağazanın
  korunması; gerçek geri satış metodunun 32/64 bit Yang varyantları.
- Fresh seed ve iki SQL dosyası kanonik stokla tutarlı; gerçek VM game
  derlemesi tamamlandı. Beş mağazada toplam 110 ürün.
- Hazırlık kaynak/binary/SQL başlangıç durumunu sabitler; kurulumdan önce
  değişmişlerse kurulum reddedilir. Kurulumda önceki binary ve 13 sahip olunan
  shop kaydının yedeği aynı aday dizininde tutulur.
- Oyunda satıcıyı aç; Küre/kalıcı destek fiyatlarını, iksir seçkisini ve bir
  kalıcı desteğin satın alınmasını doğrula. Chrome testi kullanıcıdadır.
