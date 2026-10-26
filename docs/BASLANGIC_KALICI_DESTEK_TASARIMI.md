# Sade ekipman ve kalıcı başlangıç desteği

22 Ekim 2026. **Kod uygulandı; izole sunucu ve istemci adayları doğrulanıyor.
Canlı etkinleştirme durumu çalışma notlarında tutulur.** Son karar önceki
tılsım onayını geçersiz kılar. Normal efsunların 3000 HP ile sabitlenmesi
aynı kurulumun sınırlı SQL geçişine dahil edildi.

## Ekipman kapsamı

Standart silah, zırh, bilezik, kalkan, kask, ayakkabı, küpe ve kolye kalır.
Ek sistemlerde yalnız şu dört kategori bulunur:

| Kalacak | Mevcut dayanak |
| --- | --- |
| Binek | Genç Aslan `52034`, klasik at/binek hattı |
| Zırh/gövde kostümü | Başlangıçtaki `41003` / `41004` |
| Silah kostümü | Kullanılan silah türüne uygun kostüm |
| Çağrılan basit pet | Bambi `53007` gibi mevcut basit pet hattı |

Tılsım, Ateş/Karanlık Tılsımı gibi **`ARMOR_PENDANT` ekipmanıdır**.
Ejderha Tanrı destek nesneleri tılsım ekipmanı değildir; destek setinde kalır.
Saç kostümü, element tılsımı, kuşak, aura, simya, güç yüzüğü/kemeri ve diğer
ilave güç yuvaları kapalı olacak. Ayrı büyüyen pet/besleme/ölüm sistemi yok.
Başlangıçtaki saç kostümleri `45005` / `45006` çıkarılacak.

Binek/pet/kostüm süreleri bu destek nesneleri talebiyle otomatik süresiz olmaz.
Silah kostümünde sınıf/silah uyumu korunur; bu tasarım yeni görsel seçmiyor.
Işınlanma yüzüğü gibi ulaşım araçları takılan güç yüzüğüyle karıştırılmaz.

Kapatma shop/drop/quest/ödül edinimi, sunucuda takma/kullanma ve UI yuvalarını
birlikte kapsar. Mevcut takılı yasak eşya yeniden girişte bonus vermemeli;
eşyalar sessizce silinmeden güvenli çıkarma/teslim yolu hazırlanmalı.
Paket/enum uyumunu değiştiren feature flag'ler kapatılmayacak.

## Dört “muska” ve kritik/delici

`welcome` şu altı süreli destekten otuzar adet veriyor. Her birinin mevcut
kalıcı `+` karşılığından **bir adet** verilecek:

| Nesne | Eski → yeni vnum | Adet | Mevcut `+` bonusu |
| --- | --- | ---: | --- |
| Ejderha Tanrı Yaşamı | `71027` → `72731` | 1 | Maks. HP +%20 |
| Ejderha Tanrı Saldırısı | `71028` → `72732` | 1 | Saldırı bonusu +%20 |
| Ejderha Tanrı Zekâsı | `71029` → `72733` | 1 | Maks. SP +%20; düz INT değil |
| Ejderha Tanrı Savunması | `71030` → `72734` | 1 | Savunma bonusu +%20 |
| Kritik Vuruş | `71044` → `72735` | 1 | Kritik +%20 |
| Delici Vuruş | `71045` → `72736` | 1 | Delici +%20 |

Değerler mevcut `+` protolarından alındı; bu talepte yeni sayısal değer
istenmedi. Normal ekipman HP efsununun 3000 olmasıyla yaşam desteğinin +%20
HP vermesi ayrı şeylerdir.

## Altı kalıcı şebnem

| Nesne | Vnum | Adet | Mevcut `+` bonusu |
| --- | ---: | ---: | --- |
| Kırmızı Şebnem+ | 50827 | 1 | Kritik +%20 |
| Turuncu Şebnem+ | 50828 | 1 | Delici +%20 |
| Sarı Şebnem+ | 50829 | 1 | Saldırı hızı +%8 |
| Yeşil Şebnem+ | 50830 | 1 | Büyü direnci +%20 |
| Mavi Şebnem+ | 50831 | 1 | Saldırı değeri +120 |
| Beyaz Şebnem+ | 50832 | 1 | Savunma değeri +200 |

Altı `+` şebnem şu an 55 seviye istiyor. Başlangıçta kullanılabilmesi için
**bu altı kalıcı nesne 1. seviyeye çekilecek**; süreli şebnemlerin seviye
sınırları topluca değiştirilmez. İki yeni iksirle toplam: **14 ayrı nesne × 1**.

Kritik/Delici Vuruş+ ile kırmızı/turuncu şebnem ayrı etki aileleridir.
Mevcut değerlerle birlikte açık olduklarında **kritik +%40 ve delici +%40**
verirler; ekipman/beceri bonusları buna dahil değildir. Aynı nesneyi tekrar
kullanarak bonus katlama olmayacak.

## Kalıcılığın davranışı

- İlk kullanım etkinleştirir; adet tüketilmez, süre dolmaz. Nesne envanterde
  kalır. Mevcut `+` sistemi gibi tekrar tıklamak isteğe bağlı kapatır/açar.
- Ölüm/dirilme, çıkış/giriş, kanal/harita değişimi ve sunucu yeniden başlaması
  etkin desteği kendiliğinden kapatmaz. Oyuncu kapattıysa girişte açılmaz.
- İkinci kopya veya tekrar kullanım aynı desteği katlamaz.
- Kalıcı ve süreli aynı aile/aynı bonus birlikte istiflenmez. Kalıcıya geçerken
  yalnız ilgili süreli etki değiştirilir; diğer etkiler silinmez.
- Aktif nesne taşıma/ticaret/depo yoluyla iki karaktere bonus bırakamaz.
  Nesne kilidi ve karakter etkisi birlikte yönetilir.
- Tooltip ve etki simgesi “Süresiz” gösterir; yanıltıcı sayaç olmaz.
- Yeni ve mevcut karakterlere yalnız bir teslim yapılır. Envanter doluysa
  kalan hak kaybolmaz; yeniden girişte tamamlanır ve kopya üretilmez.

## Mor / yeşil iksir

Büyük yeşil iksir `27102`: saldırı hızı +30, 600 saniye. Büyük mor iksir
`27105`: hareket hızı +40, 600 saniye. Şu an başlangıçta ellişer tane var.

Son kullanıcı onayı hazır sürüm koşulunu kaldırdı. Yeni kalıcı yeşil iksir
`72737` saldırı hızı +30, mor iksir `72738` hareket hızı +40 verir. Birer adet,
seviye 1; süreli başlangıç iksirlerinin yerini alırlar. Eski oyuncu stokları
silinmez. Kalıcı iksiri açınca aynı türün süreli etkisi kaldırılır; aktifken
süreli karşılığı kullanılamaz. Sarı şebnem +8 saldırı hızı ayrı ailede kalır;
kalıcı yeşil iksirle birlikte +38 sağlar. Yeşil Şebnem büyü direnci verir.

Sunucu DB ve istemci item yükleyicileri aynı `pvp_support_proto.h` politikasını
uygular. Eski CP1254 metin/binary protoları değişmeden altı şebnemin seviyesi
1 olur; `72731` şablonundan iki yeni nesne yaratılır. İstemci mevcut yeşil/mor
iksir ikonlarını kullanır. Proto yeniden yükleme bu politikayı da uygular.

## Kod bulguları ve uygulama işleri

Hazır altyapı: `ENABLE_RENEWAL_AFFECT` açık. `USE_AFFECT_PLUS`, `72731–72736`
nesnelerinde `AFFECT_MALL_PLUS = 549`, `50827–50832` nesnelerinde
`AFFECT_BLEND_PLUS = 550` kullanıyor. `socket1` aktiflik durumunu tutuyor;
aktif nesne kilitleniyor. İstemcide etki türleri ve `+` tooltip desteği var.

Ölüm temizliği 500–599 aralığını koruyor, dolayısıyla 549/550 kapsamda.
Bu türler kaydetmeme listesinde de yok. Ölüm/relogin için altyapı uygun;
uçtan uca test olmadan yeni tasarım tamamlanmış sayılmayacak.

1. `welcome`: altı otuzluk desteği altı birer `+` nesneye çevir; altı şebnem
   ekle, iki saç kostümü satırını çıkar. Mevcut karakterlere bağımsız ve
   tekrarlanamayan teslim işaretiyle ver. Eski stokları topluca silme.
2. Altı kalıcı şebnemin level sınırını 1 yap; istemci/sunucu protoları eşleşsin.
3. `char_item.cpp` ön çakışma kontrolünü düzelt: `USE_AFFECT_PLUS` bonus türü
   `Value0` iken ortak dal şu anda `Value1` okuyor. `Value1` bonus miktarıdır.
4. Aktif nesne, kaydedilmiş etki ve kullanım kilidini yeniden girişte eşleştir;
   tek kopya/tek etki kuralını envanter hareketlerinde de doğrula.
5. `INFINITE_AFFECT_DURATION` şu an 60 yıllık sayaç. Bu 12 desteğin süresizlik
   sözleşmesi için kalıcı etkiler süre tüketmemeli; geçici etkilerin zamanlayıcısı
   korunmalı. Yeni ağ paketi/feature flag gerektirmeyen yol kullanılmalı.
6. Kapalı güç ekipmanlarının edinimi, takılması, takılı bonusu ve UI'sını birlikte
   kapat; mevcut eşyalar için kayıpsız çıkarma yolu hazırla.
7. Quest nesnelerini derle; server, istemci proto ve pack güncellemesini eşleştir.

## Kabul kontrolleri

| Kontrol | Beklenen |
| --- | --- |
| Yeni karakter | 14 kalıcı nesneden birer; saç/tılsım yok |
| Eski karakter / tekrar giriş / dolu envanter | Tek teslim; eksik teslim tamamlanır |
| 1. seviye şebnem | Altı kalıcı şebnem kullanılabilir |
| Etkinleştir / kapat / aç / ikinci kopya | Tek bonus; adet düşmez; kilit doğru |
| Süreli + kalıcı aynı aile | Katlama yok |
| Kritik nesnesi + kırmızı şebnem | Toplam +%40; girişte katlanmaz |
| Ölüm / dirilme | Etki ve değer korunur |
| Login / kanal / harita / kontrollü restart | Aktiflik tercihi korunur |
| Uzun süre / sayaç sınırı | Kalıcı bitmez; geçici normal sona erer |
| Aktif nesneyi taşıma / ticaret / depo | İki karaktere bonus bırakamaz |
| Eski tılsım/saç ile deneme | Sunucu takmayı engeller; bonus işlemez |
| Tarayıcı | Süresiz etiketi/simge doğru; kapalı yuvalar yok |

## Kaynaklar

- [Başlangıç quest](../runtime/freebsd/share/locale/europe/quest/quest_tr/_npc_talk_mission/welcome.lua)
- [Sunucu protoları](../runtime/freebsd/share/conf/item_proto.txt) ve [nesne adları](../runtime/freebsd/share/conf/item_names.txt)
- [Kullanım/çakışma kontrolü](../apps/server/game/src/char_item.cpp)
- [Kalıcı nesne tanıma/kilit](../apps/server/game/src/item.cpp)
- [Etki kimlikleri/süre](../apps/server/game/src/affect.h) ve [ölüm/kayıt](../apps/server/game/src/char_affect.cpp)
- [İstemci tooltip](../content/client/packs/root/uitooltip.py)
- [Güncel tasarım kilidi](../PVP_HEDEF.md)

Yerel üretim kodu geçiş testi: aç/kapat, ikinci kopya, süreli etkiyi değiştirme,
şebnem+iksir beraberliği, yeniden giriş, sahipsiz etki temizliği, ölümde kullanım
engeli ve seviye sınırları geçti. UI testi izinli yuvaları, eski takılı eşyanın
çıkarılabilir kalmasını ve sunucu/istemci politika eşitliğini doğrular.
Gerçek ölüm/dirilme ve yeniden giriş kabulü, canlı kurulum sonrası oyun içinde
tamamlanmalıdır; birim testi bu uçtan uca kontrol yerine geçmez.
