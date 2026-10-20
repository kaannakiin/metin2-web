# Oyun paketi doğrulaması — 2026-10-20

## Canlı klasik zincirler ve loot v4

**20261020-153340**: beş gerçek qc görev derlemesi ve loot v4 kuruldu.
**20261020-153638**: yalnız iki erişim bossunun doğma süresi 15 dakikaya indirildi.
Günlük kota yok; başarılı zindan kesiminde 10 dakika cooldown. Oranlar ve oyuncu
akışı [MID_PVP_FAZ3_ZINCIR.md](../../docs/MID_PVP_FAZ3_ZINCIR.md) içinde.

Kurucu `progression_release.py --install` kaynak/drop paketi, gerçek VM qc
derlemesi, kapsamlı önceki dosya arşivi ve hash koruması kullanır. Bu v4 geçişinin
baseline'ı `8ae9aadb3` olup canlıda bulunmayan opsiyonel ödül kaydı korunur.
`--spawns-only --install` yalnız Kraliçe ve Komutan boss.txt dosyalarını kurar.
Eski sürümü rastgele yeniden kurmak yerine yeni sürüm için baseline güncellenir.

Oyun/regresyon testi çalıştırılmadı. Kurulumlar altı süreç/altı port ve dosya
eşleşmeleriyle tamamlandı. VM `previous.tar` arşivleri ve `INSTALLED` kayıtları
aynı sürüm dizinlerindedir. İstemci/engine/corpus değişmedi.

## Varsayılan dört envanter sayfası

**Canlı sürüm: `20261020-142312`.** Mevcut beş karakter ve yeni karakter
varsayılanı 4 sayfa / 180 hücre; servis süreç/port koşulları tamamlandı.

`python3 platform/deploy/inventory_defaults_release.py` standart envanteri tüm
mevcut ve yeni karakterler için 4 sayfa / 180 hücre açar. İstemci/sunucu zaten
bu kapasiteyi destekler; sadece `player.player.inventory_0` varsayılanı ve
mevcut değerleri 18 yapılır. Özel envanterler değişmez.

Kurucu önce Metin2 game/db servislerini durdurur, eski karakter değerlerini
`rollback.sql` ve eski varsayılanı `previous-default.txt` olarak VM sürüm
dizinine yazar. SQL migration sonrası servisleri başlatır; hatada eski değerleri
geri yükler. İç SSH çağrıları `-n` kullanır; başarı VM `INSTALLED` kaydıyla
doğrulanmadan host başarı yazmaz. Derleme veya oyun/regresyon testi gerekmez.

Canlı durum ve sürüm/yedek yolları `CALISMA_NOTLARI.md` içinde.

## Metin yoğunluğu 4× / yarım süre

**Canlı sürüm: `20261020-140835`.** Güncel politika `platform/gameplay/metin_density.json` v2: 13 haritada ilk
97 kapasite yerine 388; ilk yeniden doğma süreleri yarıya iner (yukarı saniyeye
yuvarlanır). Önceki 2× canlı kapasite 194'tü. Bölgeler ve metin türleri korunur.

Yeni bağımsız bakım yolu: `python3 platform/deploy/density_release.py --install`.
13 dosyanın canlı 2× SHA'sı eşleşmeden kurulmaz; önce VM üzerinde yedek alınır.
Kurulum yalnız `map/*/stone.txt` dosyalarını değiştirip Metin2 servisini yeniden
başlatır. Hata halinde önceki dosyalar geri yüklenir. Client/corpus yeniden
derlenmez. Yeni oyun veya regresyon testi çalıştırılmadı.

Geri alma: host üzerinden VM'de `sh /usr/metin2-density-<sürüm>/density_install_vm.sh rollback /usr/metin2-density-<sürüm>`.
Canlı kurulum sonucu `CALISMA_NOTLARI.md` içinde tutulur. Aşağıdaki 2× sayıları
önceki dondurulmuş sürümün tarihsel kaydıdır.

## Canlı — loot v3 / 20261020-134850

**KURULDU.** Kullanıcı açıkça canlı kurulumu ve main commit'ini istedi; oyun
testini kendisi üstlendi. Bu tur yeni unit/regresyon/oyun testi çalıştırılmadı.
Kurulumun hash, dosya eşleşmesi ve servis süreç/port koşulları tamamlandı.

- Son aday: `/home/m2web/phase3-20261020-134850` ve VM
  `/usr/metin2-phase3-20261020-134850`; ikisinde de `INSTALLED` var.
- Web istemcisi, önceden derlenmiş `20261020-125412` paketinden yeniden test veya
  build yapılmadan alındı. Toplama tuşu ve Space/binek düzeltmeleri dahil.
- Loot v3: 23 metin grubu, 13 bossun 12 kendi sandığı ve 7 bossun doğrudan
  tablosu. Önceki rehberde eksik görünen 10 klasik boss tamamlandı.
- Lusifer: 75 silah %30 (6 × %5), 70 silah %15 (5 × %3), 65 silah %7,
  66 zırh %12, diğer ödüller %36. Barones 75 silahları doğrudan %3'er verir.
- Azrail kendi 50186 sandığını verir; Güçlü Buz Cadısı silah yerine zırh/kalkan/
  takı/+4 taş, ağaç bossları ruh taşı ve Kharoon takı/inci verir.
- Corpus değişmedi; CDN yüklemesi yapılmadı. Game/db binary, harita, spawn,
  respawn ve Traefik değişmedi.
- Site yedeği: `/home/m2web/backups/phase3-finish-FO7RZ482/site`.
  VM eski loot: `/usr/metin2-phase3-20261020-134850/previous`.

VM kurulumu bittikten sonra servislerin devraldığı stdout kanalı ilk SSH
oturumunu açık tuttu. `phase3_finish_host.sh`, VM `INSTALLED`/dosya hash'leri
doğrulandıktan sonra yalnız komut/PID/ebeveyni eşleşen eski kurulum kabuğu ve
bekleyen SSH istemcisini sonlandırıp web yayınını tamamladı; oyun tekrar
başlatılmadı. Son yayın komutu 0 ile çıktı. Gelecek kurulumlar için VM servis
çıktıları log dosyalarına yönlendirildi. Geri alma yedekleri korundu.

Tam güncel tablo: [Metin ve Boss Drop Rehberi](../../docs/DROP_REHBERI.md).
Oyuncu tarayıcı sayfasını yenileyip oyun içi kabulü yapar. Aşağıdaki eski adaylar
ve eski komutlar tarihsel kayıttır; tekrar kurulmaz.

---

## Güncel loot v2 — önceki aday geçersiz

**`20261020-125412` ve `20261020-125127` adaylarını kurmayın:** ikisi de son silah
revizyonundan öncedir. Aşağıdaki v1 bakım komutu tarihsel kayıttır; v2 için yeni
aday hazırlanıp dondurulmadan kullanılmaz. Canlı oyun bu revizyonda değiştirilmedi.

Güncel tam tablo: [Metin ve Boss Drop Rehberi](../../docs/DROP_REHBERI.md).
Rehber bütün 23 metin grubunu, 9 klasik boss sandığını ve önceki özette atlanan
diğer doğrudan drop gruplarını gerçek eşya adı / VNUM / seviye / adet / oranla
listeler. Üretici: `platform/tools/drop_catalogue.py`; `--check` veri ile belge
eşleşmesini denetler.

V2 değişikliği: diğer sandıklar %28 65 silah + %12 zırh içerir; Lusifer %30 gerçek
75 silah, %14 65 silah ve %16 66 zırh verir. Altı gerçek 75 silahın her biri %5:
Zehir 180, Aslan 190, Şeytan Kanadı 1130, Havalı Çelik 2170, Kin 3160, Orkide 5120.
Zehir ve Orkide 85/90 metinlerden taşındı; Siam/Şeytani/Yarı-İnsan/Mutluluk 70
oldukları için metinde kaldı. Ödül çıktısı tek satırdır, listelenenlerin hepsi
aynı sandıktan birden verilmez. V2 için yerel 42 test geçti; canlı kabul bekleniyor.

---

## Yeni Faz 3 revizyonu — bakım adımı

**Yeni değişiklikler henüz canlıda değil.** Aday `20261020-125412`;
host `/home/m2web/phase3-20261020-125412`, VM `/usr/metin2-phase3-20261020-125412`.
Bu aday önceki deneme adayı `20261020-125127` yerine kullanılır.

- `"` tuşu tarayıcının karakter bilgisinden toplama tuşuna bağlanır; Shift önce
  bırakılırsa tuş takılı kalmaz. Mevcut fiziksel tuşlar ve Z korunur.
- Space, mouse saldırısının kullandığı `CInstanceBase::CanAttack` kararını kullanır;
  item bineklerde eski 107/109 at becerisi engeli kaldırıldı.
- Metin BK sayısı 5–20 / 25–45 / 50–70 / 75–90 için 6 / 10 / 12 / 14.
  Unutma kağıdı + münzevi malzemeleri, 40+ artan ruh taşı ve 90 metinde 66 zırh +0.
- 10 klasik boss için 9 sandık tanımı: her sandık tek ağırlıklı ödül verir.
  Boss spawn/respawn, haritalar, seviye/yang ve zindan mekanikleri değişmez.

Sayıların tamamı ve kaynak karşılaştırması `PVP_HEDEF.md` içinde. 40 Python
testi, 3 JS klavye testi, 13 ekonomi kontrolü geçti. Gerçek web build'inde
80/80 stage patch, sıfır derleme hatası, 594 bayt login ve 20 bayt RESP
regresyonları geçti. Corpus aynı; CDN yüklemesi gerekmiyor. Oyun içi davranış
bu kontrollerle kanıtlanmış sayılmaz.

### Kurulum

Repo `AGENTS.md` satır 49, otomatik modda VM servis restart'ı yerine bakım
betiğinin kullanıcıya verilmesini ister. Bu komut **oyuncuları oyundan düşürür**;
uygun bakım anında kullanıcı çalıştırır:

```sh
ssh root@88.99.1.151 'bash /home/m2web/phase3-20261020-125412/phase3_loot_host.sh install 20261020-125412 --operator-maintenance'
```

Betik önce dondurulmuş istemci/dosya hash'lerini ve canlı dosyaların hazırlıktan
beri değişmediğini kontrol eder. Siteyi yedekler; VM'de yalnız iki loot dosyasını
değiştirir, metin2 servislerini yeniden başlatır; altı süreç/altı portu doğrular;
eşleşen istemciyi HTML en son olacak şekilde kurar. Başarısızlıkta eski site ve
iki loot dosyası geri alınır. Game/db binary, protolar, questler, harita/regen,
Traefik ve corpus bu kurulumda değişmez. Kurulumun yazdırdığı site yedeği yolunu
saklayın; VM önceki tabloları adayın `previous/` dizinindedir.

### Oyunda kabul

1. Sayfayı yenileyin. Türkçe klavyede `"` ve Z ile yakındaki yang/item toplayın;
   Shift'i önce bırakmayı ve pencere değiştirip geri dönmeyi deneyin.
2. Aynı silahla yaya ve başlangıç aslanı üstünde durarak/yürüyerek Space tutun;
   mouse saldırısıyla kıyaslayın. Skill/at becerisi olmayan diğer item binekleri
   de deneyin; tuş bırakınca ve tarayıcı odağı kaybolunca saldırı bitmeli.
3. Yakın seviyeli karakterle metin 20/35/60/70/90 örnekleri kesin. 6/10/12/12/14
   bağımsız BK, doğru okuma malzemeleri ve ruh taşı bandını doğrulayın.
   Baz ruh taşı olasılığı 60/65/70 için %30/%40/%50; tek kesim kanıt değildir.
4. 65–70 hedefi için normal farm rotasında metin sayısını, geçen süreyi, Master
   olmuş becerileri ve G'ye kadar kullanılan kitapları kaydedin. Hızlı okuma
   ekranını malzemelerle deneyin; seviye almak tek başına G garantisi değildir.
5. Kızıl Orman 90 metninden 66 taban zırh +0, Ork Reisi/orta boss/yüksek boss/
   Lusifer sandıklarından tek ödül çıktığını doğrulayın. Boş/yanlış sandık
   görülürse VM syslog/syserr ile birlikte geri alma değerlendirin.

---

## Önceki kurulu paket

Canlı: `20261019-213727` game/db ve eşleşen 594 bayt login istemcisi kuruldu;
drop, başlangıç bonusları, sınırsız dedektör ve 2× metin verisi aktif.
Kullanıcı bu dağıtımın Metin2 servis bakımı için açık istisna verdi.
Kurulum site yedeği `/home/m2web/backups/gameplay-d6P0bSAs`;
VM runtime/binary yedeği `/usr/metin2-gameplay-20261019-213727/previous`.
Ardından klasik karakter penceresindeki tuple/liderlik/pasif kontrol eksikleri
UI paketiyle düzeltildi; engine ve corpus değişmedi. Son site yedeği:
`/home/m2web/backups/character-window-15Z0ltU0`.

Kurulan paket: drop, sınıfa uygun başlangıç efsunları, sınırsız 27989 dedektörü ve
13 açık dünya haritasında **97 → 194 metin kapasitesi**.
VM: `/usr/metin2-gameplay-20261019-213727`.
Host: `/home/m2web/gameplay-20261019-213727`.
`READY` ve `BUNDLE_READY` mevcut. Game/db build, gerçek `qc`, sunucu Lua ile
sekiz başlangıç senaryosu ve 10.000 dedektör kullanımı geçti. İstemci paketinde
594 bayt login, 20 bayt RESP yapıları, frame regresyonu, Python syntax ve
yerelleştirilmiş sınırsız dedektör metni doğrulandı. Mevcut fontta ∞ glifi
bulunmadığından, 11 dildeki mevcut “Unlimited/Sınırsız” çevirisi kullanılır.

Aday raporu: `build/protocol-candidate/audit.json`; 164 ortak yapıda boyut
uyuşmazlığı yok, 146'sının alan offset'leri tam kontrol edildi; 18 kısmi,
125 eşleşmeyen kayıt ve 20 eşleşmeyen GC header kapsam dışında. 145 ortak GC
numarası eşleşti. Gerçek server/wasm SHA'ları dondurulmuş paketle karşılaştırıldı.
Canlı runtime dosyaları ve channel CONFIG'leri VM adayının `previous/` dizinine
yalnız root erişimiyle yedeklendi; kurulum tamamlandı. Corpus aynı kaldı.

Yoğunluk eklentisi host ve VM'de `DENSITY_READY` aldı; 13 canlı harita da aynı
geri alma listesine eklendi. Son paket kontrolü haritaların ve adayın hash'lerini,
canlı runtime'ın ilk yedekle eşleştiğini ve oyun süreç/port sağlığını doğruladı.
Hazırlık aşamasında game/public WASM değişmedi; son kurulumda ikisi birlikte
eşleşen source profiline geçti. Aşağıdaki kurulum komutu yoğunluğu da içerir;
mevcut kurulu sürümde yeniden çalıştırılması gerekmez.

## Her değişiklikte kontrol

Son yerel sonuç: 31 oyun/ABI/kurulum/yoğunluk + 14 dev-tool + 4 publish + 3 bridge testi
geçti (52 test). Ekonomi kontrolü 13/13. Kurulum testleri geçici dosyalar ve
sahte servisle çalışır: gerçek VM restart'ını veya oyun içi kabulü kanıtlamaz.

1. `python3 -m unittest discover -s platform/tests -p 'test_*.py'`.
   Boş/eksik ABI ölçümü, yanlış offset, 20/24 bayt RESP regresyonu, header
   alias'ları, kısmi eşleşme, 23 metin drop grubu ve gerçek tooltip kodu.
2. `python3 platform/deploy/dev_client.py cpp --protocol live-yohara`:
   canlı eski sunucu için 619 bayt login; `source`: yeni kaynak sunucusu için
   594 bayt login. `patchcheck`, gerçek Emscripten struct ölçümü ve RESP
   fixture (parçalı/bozuk payload, signed timestamp, arkasından PING) zorunlu.
3. `python3 platform/deploy/packet_audit.py --strict` çalışan binary ile
   staged istemciyi karşılaştırır. `--candidate 20261019-213727 --output
   build/protocol-candidate --strict` izole sunucu adayını karşılaştırır.
   Aday karşılaştırılırken istemci de `source` profiliyle derlenmiş olmalı.
4. `gameplay_vm.sh` gerçek FreeBSD build, gerçek `qc` derlemesi, gerçek
   sunucu Lua kütüphanesiyle dört sınıf × iki cinsiyet başlangıç senaryosu ve
   10.000 dedektör kullanımı fixture'ını çalıştırır. Sadece tümü geçince `READY`.

ABI raporunda `compatible_records` toplam boyut uyumluluğunu da kapsar;
`fully_compared_records` eksiksiz alan-offset kontrolü yapılan alt kümedir.
`partial_field_records`, `unmapped_client_records`, `unmapped_gc_headers`
başarılı sayılmaz. `--strict` bilinen uyuşmazlıkları ve boş karşılaştırmayı
reddeder; oyun içi davranışın tümü için garanti vermez.

## Oyunda kabul tablosu

Henüz yapılmamış satırları geçti diye işaretleme. Console açık tutulmalı;
aynı anda game syserr ve bridge kapanış nedeni ilişkilendirilmeli.

| Senaryo | Beklenen | Durum |
| --- | --- | --- |
| Giriş → karakter seçimi → harita | Takılma/yeniden giriş yok | 2026-10-20 özel önizleme + canlı: deneme lv22 Pyungmoo giriş ve karakter penceresi geçti |
| Art arda en az 10 metin kesimi, özellikle Hırs Metini | Login'e dönme / unknown packet yok | Bekliyor |
| Düşen BK ve diğer eşyaları yerden alma | Envanter doğru, kopma yok | Bekliyor |
| Taş torbası açma | Geçerli +3/+4 taş/malzeme, kopma yok | Bekliyor |
| 13 haritada metin yoğunluğu | Aynı doğma bölgelerinde yaklaşık 2× taş; süreler aynı, madenler aynı | Veri/native parser geçti; oyun içi kontrol bekliyor |
| Dört sınıfta yeni karakter | Doğru iki/tek silah, doğru efsunlar, dedektör | İzole quest fixture + oyun içi kontrol gerekli |
| Dedektörü en az 7 kez kullanma, çıkıp tekrar girme | 27989 kaybolmaz; 76006 sınırlı kalır | Fixture + oyun içi kontrol gerekli |
| Harita/kanal değiştirme ve yeniden giriş | Veri/efsun/sayaç korunur | Bekliyor |
| Ekipman tak/çıkar, efsunla, geliştir, NPC alış/satış, ticaret/depo | Eşya ve para kaybı/kopma yok | Bekliyor |
| 30–60 dakika normal oyun | Yeni syserr/packet/ASan hatası yok | Bekliyor |

İki gerçek metin kesiminin kopması yeniden üretildi; önceki başarılı giriş
testi bu hatayı kapsamadı. Bu nedenle yalnız build/ABI başarısı “oyun hazır”
sonucu olarak kullanılmaz.

## Kurulum sınırı

`AGENTS.md`: “Auto mode refuses VM service restarts and Traefik/IaC changes …
prepare a script and hand those steps to the user.” Sunucu servisi bakım
penceresinde operatör tarafından değiştirilir. Kaynak sunucusu Yohara kapalı
594 bayt login kullanır ve şu an canlıdadır; eski sunucu + 619 bayt istemci
yalnız birlikte geri alınabilecek önceki çifttir. Bu dağıtımda kullanıcı
istisnayı açıkça onayladı ve bakım tamamlandı.
Yeni binary tek başına kurulmaz. Özellikle eski `login_fix_vm.sh install`
komutu bu oyun paketi için kullanılmaz: runtime drop/quest ve eşleşen web
istemcisini içermez.

Operatör bakım penceresinde hostta **tek komut** çalıştırır:

```sh
bash /home/m2web/gameplay-20261019-213727/gameplay_install_host.sh 20261019-213727 --operator-maintenance
```

Komut paket hash'lerini, corpus eşitliğini ve canlı runtime dosyalarının hazırlık
sonrası değişmediğini kontrol eder. Siteyi yedekler; game/db, drop, derlenmiş
welcome ve onun kaynak dosyasını birlikte kurar; channel CONFIG'lerinde yalnız
MAX_LEVEL'ı 99 yapar. Eklenen 13 harita dosyasını da kurar ve geri alma kapsamına
alır. Sonra eşleşen 594 bayt istemciyi HTML en son olacak şekilde
yayınlar. VM install veya web sync başarısızsa önceki dosyaları geri yüklemeyi
dener; geri alma tamamlanamazsa açık hata ve yedek konumlarıyla durur.
Geri alma dizinleri çıktıda yazılır; karakter/veritabanı içeriği geri sarılmaz.

Mevcut rc betiğinin `status` kodu güvenilir sağlık kanıtı değildir. Kurulum ve
geri alma ayrıca db/auth/üç game core/game99 süreçlerinin tümünü ve altı IPv4
portunu denetler; eksik süreç veya portta kurulum başarılı sayılmaz. Bu kontrol
mevcut VM'de salt okunur çalıştırılıp doğrulandı.

Kurulumdan sonra açık oyun sekmelerini yeniden yükle ve yukarıdaki oyun kabul
tablosunu tamamla. Derleme başarısı veya `BUNDLE_READY`, oynanış kabulü değildir.

Drop sayıları `PVP_HEDEF.md` kilididir; düşük seviye farm cezası mevcut
sunucu kodunda korunur. 400 drop ağırlığı seviyeye yakın temel durumda yaklaşık
%100'dür, her karakter seviyesinde mutlak garanti değildir. Mevcut hesapların
tamamladığı welcome quest sıfırlanmaz, eşyalar otomatik yeniden yazılmaz.

Yoğunluk politikası `platform/gameplay/metin_density.json` içindedir. Mevcut
regen bölgeleri ve süreleri korunur; her metne bağımsız bir kayıt eklenir.
`python3 platform/tools/metin_density.py` orijinal dosya SHA'sını ve metin
çoğaltmalarını denetler. `metin_density_native.py`, gerçek sunucu lexer/parser'ı
ile 194 metin ve 194 ayrı takip kimliği okur; arazi üzerinde gerçek spawn testi
değildir. `gameplay_density_prepare.py` yalnız kurulmamış bu adaya veri ekler;
iki kez çalıştırılarak yoğunluk 4× yapılamaz. `density-report.json` aday dizininde
önce/sonra sayılarını ve SHA'ları taşır; `DENSITY_READY` ile hash korumasına dahildir.
