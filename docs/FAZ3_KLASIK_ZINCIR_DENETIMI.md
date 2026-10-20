# Metin2 klasik ilerleme zinciri ve Faz 3 eksikleri

20 Ekim 2026. Dosya inceleme tabanı: `a45daa62f`.

Bossların ödül tablosunun olması, ilerleme zincirinin tamam olduğu anlamına gelmiyor.
Oyuncunun elde edebildiği bir malzeme, onu kullanan bir görev veya NPC ve bu yolla
ulaşılan bir sonraki içerik birlikte çalışmalı. Başlıca kopukluklar Lusifer–Katakomb
ve Örümcek–Barones hatlarında. General–Beran hattının anahtar bağlantısı mevcut.

## Orta kolay sunucunun kuralları

Wiki, eşyanın kaynağını, kullanımını, NPC'yi ve zindan aşamalarını belirlemek için
referanstır. Giriş adedi, üretim başarısı, malzeme miktarı, bekleme ve drop oranı
sunucunun orta-kolay ekonomisine göre ayarlanır.

- Boss farmı tekrar edilebilir olmalı. Beran için günde bir giriş gibi sınırlar konmaz.
- Güncel resmî sürümün Nesne Market biletleri ve günlük hak yükleme sistemi taşınmaz.
- Mevcut yerleşimler korunur. Bir bossun malzemesi rastgele başka haritaya dağıtılmaz.
- Giriş malzemesi sandıktaki rastgele bir ödüle bağlanıp zincir tesadüfe bırakılmaz.
- Anahtar/zehir gibi zorunlu ilerleme eşyaları, tekrarlanabilir farmı besleyecek kadar
  erişilebilir olmalı. Ekipman nadirliği ile giriş bileti erişimi ayrı dengelenir.
- Kule, Barones, Azrail ve Beran Faz 3 kapsamındadır. Razador, Nemere, Meley ve
  Yohara'nın mevcut yüksek seviye halleri bu araştırma nedeniyle açılmaz.

Bu sınırlar [PVP_HEDEF.md](../PVP_HEDEF.md) ve
[ROADMAP_PVP.md](ROADMAP_PVP.md) ile birlikte uygulanır. Aşağıdaki düzeltmeler
araştırma sonucudur; bu belge oyun verisini veya canlı servisi değiştirmez.

## Ana ilerleme yolları

| Yol | Elde edilen şey | Kullanıldığı yer | Repo durumu |
|---|---|---|---|
| Buz Cadısı / General / Beran | Kan Taşı | Koe-Pung üzerinden Sürgün | Drop ve tüketim var; ayrıca yang ile satış var |
| Sürgün 2 Komutan / General | Kıvrık Anahtar | Sura Ruhu üzerinden Beran | Kaynak ve 3 anahtarlı giriş var |
| Şeytan Kulesi katları | Harita ve kat anahtarları | Bir sonraki kule katı | Görev içinde üretiliyor ve tüketiliyor |
| Lusifer | Küçülen Kafa | Katakomb üzerinden Azrail | Kaynak yok; tüketim var |
| Kraliçe Örümcek ve normal örümcekler | Zehir ve beş malzeme | Uriel'de Arachnida Anahtarı üretimi | Üretim ve zehir kaynağı yok; normal malzeme drop yolu da eksik |
| Örümcek Baronu | Arachnida Flütü | Barones'i çağırma | Mevcut zindan bu aşamayı atlıyor |
| Metinler ve bosslar | BK / Ruh Taşı / ekipman | Beceri ve karakter gelişimi | Küratörlü drop tabloları var; seviye cezası sonucu etkiliyor |
| Bölgesel yaratıklar ve bosslar | Biyolog malzemeleri | Kalıcı karakter gelişimi | Biyolog sistemi mevcut; malzeme kaynağı ayrı denetlenmeli |

## Sürgün ve Beran Setaou

### Wiki bağlantısı

Kan Taşı, Sürgün giriş eşyasıdır; resmî eşya sayfası General, Beran ve Güçlü Buz
Cadısı'nı kaynak gösterir. Kıvrık Anahtar General'den gelir ve Sürgün 2'deki Sura
Ruhu üzerinden Mavi Ejderha Odası'na erişim sağlar.
[Kan Taşı](https://tr-wiki.metin2.gameforge.com/index.php/Kan_Ta%C5%9F%C4%B1),
[Kıvrık Anahtar](https://tr-wiki.metin2.gameforge.com/index.php/K%C4%B1vr%C4%B1k_anahtar).

Güncel wiki Beran için 75 seviye, 2–8 karakter, ilk günlük girişte 5 anahtar ve
sonraki girişlerde ayrı bilet yükleme sistemi anlatıyor. İçeride metinler ejderhanın
hasar almasını ve özelliklerini etkiliyor. Günlük hak ve bilet modeli bizim
orta-kolay sunucunun hedefi değildir.
[Mavi Ejderha Odası](https://tr-wiki.metin2.gameforge.com/index.php/Mavi_Ejderha_Odas%C4%B1).

### Dosyalardaki karşılığı

`mob_drop_item.txt` içinde aşağıdaki doğrudan düşüşler zaten var. Yüzdeler seviye
farkı, sunucu item rate'i ve ek bonuslar uygulanmadan önceki baz olasılıktır.

| Yaratık VNUM | Kıvrık Anahtar | Kan Taşı |
|---:|---|---|
| 2491 | 1 adet, baz %100 | Yok |
| 2494 | 1 adet, baz %100 | Yok |
| 2492 | 2 adet, baz %25 | 1 adet, baz %25 |
| 2495 | 3 adet, baz %25 | 1 adet, baz %25 |
| 1191 | Yok | 1 adet, baz %100 |
| 1192 | Yok | 1 adet, baz %40 |
| 2493 | Yok | 2 adet, baz %12,5 |

2491 ve 2492 aynı yaratık değildir: proto seviyeleri 93 ve 95, rank'ları
S_KNIGHT ve BOSS. 2494 ve 2495 de 88 ve 90 seviyelik ayrı kayıtlardır. Yerelleştirilmiş
isimlerin benzer olması kaynak denetiminde bu ayrımı ortadan kaldırmaz.
Wiki de 90 ve 95 seviye Generalleri ayrı tanımlar.
[General 90](https://tr-wiki.metin2.gameforge.com/index.php/General_%2890%29),
[General 95](https://tr-wiki.metin2.gameforge.com/index.php/General_%2895%29).

Mevcut `dragonlair.lua` Sura Ruhu `30121` için 75 seviye ve giriş başına 3 adet
`30179` ister. Solo ve grup yolları var. Harita 73'te NPC ve 20 dakikalık 2491
doğuş kaydı mevcut. Oda akışı dört `8034` metini, ara Komutan dalgaları ve son
olarak 2430 grubu üzerinden Beran `2493` şeklindedir. Süre sınırı 30 dakikadır.
Bu akış güncel wiki'deki sekiz metinli odanın birebir kopyası değildir.

`char_battle.cpp:3301` ayrıca 208 instance'ında 8031–8034 metinleri varken Beran'a
hasarı bloklar. Bu, anahtar düşüşünden ayrı bir zindan kuralıdır.

**Düzeltme yönü:** mevcut anahtar bağlantısını koru; anahtar başına beklenen General
kesim sayısını ve grup tüketimini orta-kolay farm için ayarla. Günlük kota ekleme.
Sadece boss sandığını zenginleştirerek giriş hattının dengelendiğini varsayma.

### Kan Taşı ile ilk giriş

`check_trans_ticket.quest:69` Koe-Pung `20093` üzerinden 75 seviye kontrolü yapar ve
`30190` veya `30191` tüketir. `npc_talk.quest:374` aynı NPC'de 5.000.000 yang'a
`30190` satar. Dolayısıyla ilk Sürgün girişi yalnız içerideki General'e bağlı değil;
yang ile mevcut bir başlangıç kaynağı var.

Wiki'nin Kan Taşı sayfasındaki Mağara'nın İçi görev bağlantısı araştırma tarihinde
kırmızı bağlantıdır; görev sayfası 404 döndü. Bu repo içinde Fosil Gözyaşı, Obsidyen
ve Kan Damlası zincirinin görev kaynağı bulunmadı. Resmî eşya bağlantısı ile bu
görevin burada çalıştığı sonucu çıkarılamaz.

## Şeytan Kulesi Lusifer Katakomb ve Azrail

### Wiki bağlantısı

Kule 40 seviyeden itibaren kat mekanikleriyle Lusifer'e ulaştırır. Metinler,
Kilit Açma Taşı, kat haritası ve Zin-Bong-In Anahtar birbirinden farklı aşamalardır.
[Şeytan Kulesi](https://tr-wiki.metin2.gameforge.com/index.php/%C5%9Eeytan_Kulesi).

Küçülen Kafa doğrudan Lusifer kaynaklıdır; sıradan kule sandığı ödülü olarak
tanımlanmıyor. Katakomb için wiki 75 seviye ve en az bir kule tamamlama şartı
belirtir. İlk katta Ruh Kristali Anahtarı kullanılır; ikinci kattan sonraki geçişte
her üyenin kafası gerekir. Sonraki aşamalarda gerçek metin, Tartarus ve Surat Totemi,
Charon ve Azrail bağlantıları vardır.
[Küçülen Kafa](https://tr-wiki.metin2.gameforge.com/index.php/K%C3%BC%C3%A7%C3%BClen_Kafa),
[Şeytan Katakombu](https://tr-wiki.metin2.gameforge.com/index.php/%C5%9Eeytan_Katakombu).

### Kesin eksikler ve farklılıklar

- Lusifer `1093` için `Phase3Boss_1093` yalnız `50082` sandığını içeriyor. `30319`
  mob drop tablosunda yok; aktif görevlerde bunu üreten bir yol da bulunmadı.
- `devilcatacomb_zone.lua:34` solo girişte kafa kontrol eder, satır 41'de tüketir.
  Grup yolu da kontrol ve tüketim yapar. Aynı zindanın `459–474` bölümündeki oda
  geçişi tekrar bir kafa ister ve tüketir. Bazı yolların toplam maliyeti iki kafadır.
- Aynı quest'in Kud Heykeli `30101.take` yolu Ruh Kristali Anahtarı `30311` ile
  instance'a geçer. İlk NPC yolundan farklı tüketim akışı var. Tek bir standart
  giriş kabul edilip yalnız drop eklemek bu farkı düzeltmez.
- Lusifer kill handler'ı `deviltower_zone.lua:479` kule durumunu ve cooldown'u
  güncelliyor; Katakomb girişinde kullanılacak kalıcı kule tamamlama koşulu yok.
- Katakomb'da mevcut cooldown başarılı kesimde 60 dakika olarak yazılıyor. Wiki'deki
  30 dakika ve çıkıştan başlama kuralıyla aynı değil. Orta-kolay için süre ve başlangıç
  olayı açıkça seçilmeli; günlük sınır eklenmemeli.

Kulenin kendi kat eşyaları ise yok değil: görev `50084` Kilit Açma Taşı,
`30302` Zin-Sa-Gui Kale Haritası ve `30304` Zin-Bong-In Anahtar üretip tüketiyor.
Zindana özgü anahtarları genel boss sandığına koymak yerine kendi katında tutmak gerekir.

**Düzeltme yönü:** Lusifer'den erişilebilir doğrudan kafa kaynağı, tek ve tutarlı
tüketim noktası, kule tamamlama kaydı ve onunla uyumlu giriş. Kat içindeki anahtar,
metin ve boss sırasını koruyarak mükerrer masrafı kaldır. Azrail sandığı bu zincirin
son ödülüdür; giriş anahtarının yerine geçmez.

## Örümcek Kraliçe Uriel Baron ve Barones

### Wiki bağlantısı

Örümcek 2'ye Shuk-Sal üzerinden Geçit Bileti ile girilir.
[Örümcek Zindanı 2](https://tr-wiki.metin2.gameforge.com/index.php/%C3%96r%C3%BCmcek_Zindan%C4%B1_2._Kat).

Barones'e Giriş Görevi, Yüzbaşı–Mezar Taşı–Uriel görüşmelerini içerir; Uriel'in
Mektubu üretim hakkını açar. Arachnida Anahtarı doğrudan boss ganimeti değildir.
Uriel'de Kraliçe Örümcek Zehri, Örümceğin Zehir Kesesi, Bacakları, Yumurta Kesesi,
Gözleri ve Ağı ile üretilir. Wiki tarifi her birinden bir adet ve %50 üretim şansıdır.
Bu %50 bizim sunucunun zorunlu üretim oranı değildir.
[Giriş görevi](https://tr-wiki.metin2.gameforge.com/index.php/Barones%27e_Giri%C5%9F_G%C3%B6revi),
[Uriel'in Mektubu](https://tr-wiki.metin2.gameforge.com/index.php/Uriel%27in_Mektubu),
[Arachnida Anahtarı](https://tr-wiki.metin2.gameforge.com/index.php/Arachnida_Anahtar%C4%B1).

Yuvasında önce Baron kesilir; düşen Flüt ile Barones çağrılır. Yumurtalar,
Barones'in aldığı hasarı ve saldırısını değiştirir. Wiki girişte 50 seviye, her
üyede anahtar ve içeride 20 dakika belirtir.
[Barones'in Yuvası](https://tr-wiki.metin2.gameforge.com/index.php/%C3%96r%C3%BCmcek_Barones%27in_Yuvas%C4%B1),
[Arachnida Flütü](https://tr-wiki.metin2.gameforge.com/index.php/Arachnida_Fl%C3%BCt%C3%BC).

### Malzeme kaynakları

| Eşya | VNUM | Wiki'deki klasik kaynak örneği | Repo bağlantısı |
|---|---:|---|---|
| Kraliçe Örümcek Zehri | 30326 | Kraliçe Örümcek | Proto var; drop ve üretim kaynağı yok |
| Örümceğin Zehir Kesesi | 30025 | Kırmızı Zehirli / Pençe Örümcek | 2003 ve 2053 proto bağlantısı var |
| Örümcek Ağı | 30056 | Zehirli Örümcek | 2002 ve 2052 proto bağlantısı var |
| Örümcek Gözleri | 30057 | Yavru Örümcek | 2001 ve 2051 proto bağlantısı var |
| Örümcek Yumurta Kesesi | 30058 | Zehirli Pençe / Pençe Örümcek | 2004 ve 2054 proto bağlantısı var |
| Örümcek Bacakları | 30059 | Asker Örümcek | 2005 ve 2055 proto bağlantısı var |

Kaynaklar: [Kraliçe zehri](https://tr-wiki.metin2.gameforge.com/index.php/Krali%C3%A7e_%C3%96r%C3%BCmcek_Zehri),
[Zehir kesesi](https://tr-wiki.metin2.gameforge.com/index.php/%C3%96r%C3%BCmce%C4%9Fin_Zehir_Kesesi),
[Ağ](https://tr-wiki.metin2.gameforge.com/index.php/%C3%96r%C3%BCmcek_A%C4%9F%C4%B1),
[Gözler](https://tr-wiki.metin2.gameforge.com/index.php/%C3%96r%C3%BCmcek_G%C3%B6zleri),
[Yumurta kesesi](https://tr-wiki.metin2.gameforge.com/index.php/%C3%96r%C3%BCmcek_Yumurta_Kesesi),
[Bacaklar](https://tr-wiki.metin2.gameforge.com/index.php/%C3%96r%C3%BCmcek_Bacaklar%C4%B1).

Normal örümceklerin `DropItemGroup` alanları bu beş malzemeye bağlı. Fakat
`etc_drop_item.txt` boş. `item_manager.cpp:1160` ilgili olasılık kaydı bulunmadan
bu proto malzemesini üretmiyor. `mob_drop_item.txt` içinde de alternatifleri yok.
Protoya bir eşya numarası yazılmış olması çalışır drop yolu anlamına gelmiyor.

`30324/30325` anahtar için cube tarifi veya üretim görevi bulunmadı.
`30326` zehri ve `30327` flütünü üreten görev/drop kaydı da yok. Sadece
`spider_dungeon.lua` anahtarı kontrol edip tüketiyor.

Mevcut zindan doğrudan Barones `2092` ve dokuz yumurta `2095` çıkarıyor; Baron ve
Flüt aşaması bulunmuyor. Giriş handler'ının üstündeki seviye şartı 70, grup içindeki
kontrollerden biri 50. Bu da tek ve tutarlı seviye kuralı değil.

Anahtar `30324` ve zehir `30326` protoda 24 saatlik, flüt `30327` 5 dakikalık
gerçek zaman ömrüne sahip. Tarif eklenirken süreli eşya kaybı da hesaba katılmalı.

**Düzeltme yönü:** beş malzemeyi kendi örümceklerinden, zehri Kraliçe'den erişilebilir
yap; Uriel üretimini bağla; giriş seviyesini tekleştir; Baron → Flüt → Barones
sırasını tamamla. Hazır anahtarı rastgele başka bir bossa dağıtmak zinciri kurmaz.

## Beceri biyolog ve at gelişimi

Metin farmı beceri gelişimini besler. Resmî temel modelde M'den G'ye 55 başarılı
kitap okuması gerekir; G'den P'ye geçiş Ruh Taşı kullanır. Buradaki skill Ruh Taşı
`50513`, kulede kullanılan Ruh Kristali Anahtarı ve biyolog bitirme taşları farklı
eşyalardır. Sunucudaki BK, okuma malzemesi ve Ruh Taşı akışı bu ayrım korunarak
dengelenmeli.
[Beceri Kitabı](https://tr-wiki.metin2.gameforge.com/index.php/Beceri_Kitab%C4%B1),
[Büyülü Keskinlik gelişimi](https://tr-wiki.metin2.gameforge.com/index.php/B%C3%BCy%C3%BCl%C3%BC_Keskinlik_Becerisi).

Biyolog, yalnız teslim penceresinden ibaret değildir. Klasik malzeme sırası:

| Seviye | Ana malzeme | İstenen adet |
|---:|---|---:|
| 30 | Ork Dişi | 10 |
| 40 | Lanet Kitabı | 15 |
| 50 | Şeytan Hatırası | 15 |
| 60 | Buz Topu | 20 |
| 70 | Zelkova Dalı | 25 |
| 80 | Tugyis Tabelası | 30 |
| 85 | Kırmızı Hayalet Ağaç Dalı | 40 |
| 90 | Liderin Notları | 50 |
| 92 | Kem Göz Mücevheri | 10 |
| 94 | Bilgelik Mücevheri | 20 |

Çoğu basamakta ayrıca kendi bitirme taşı bulunur; 94 zinciri Beran-Setaou Ruh
Taşı'na bağlanır. Günlük teslim modeli ve süreler orta-kolay profile ayrıca uyarlanır.
Repo `constants.cpp:1558` içinde bu ana malzeme/adet dizisini taşıyan C++ biyolog
sistemi var. Quest listesinde klasik biyolog dosyası olmaması bu sistemin yok
olduğu anlamına gelmez. Malzeme ve bitirme taşı kaynaklarının tam denetimi Faz 4
işidir.
[Biyolog görevleri](https://tr-wiki.metin2.gameforge.com/index.php/Biyolog_G%C3%B6revleri).

Klasik at hattı Maymun Zindanı → At Madalyonu → Seyis → at görevleri şeklindedir.
Bizdeki basitleştirilmiş binek kararına göre bu hattın hangi kısmının kullanılacağı
belirlenir; wiki'nin tüm eğitim süresi ve zahmeti otomatik eklenmez.
[At Madalyonu](https://tr-wiki.metin2.gameforge.com/index.php/At_Madalyonu).

## Boss düşüşlerini seyrekleştiren seviye cezası

`item_manager.cpp:961` boss için seviye farkı tablosunu seçer. `constants.h:129`
indeksi `(boss seviyesi + 15) - oyuncu seviyesi` üzerinden sınırlar;
`constants.cpp:335` en düşük boss katsayısını 1 olarak tanımlar.

Örnek: 99 seviyelik karakter, 78 seviye Lusifer'de 1 katsayısına düşer. Bazı 400
olan sandık kaydı, item rate 100 ve ek drop bonusu yokken yaklaşık %1 olur.
Tabloya sandık eklenmiş olsa da oyuncu çok sayıda boş kesim yaşayabilir.
99 seviyede 95'lik General için katsayı 94, 90'lık General için 60'tır.

Bu, eksik Küçülen Kafa kaydından ayrı bir sorundur: kaydı olmayan eşya hiç bu
hesaba girmez. Orta-kolay farm tasarımında zorunlu biletler için seviye cezasından
bağımsız erişim ve boss ekipmanı için ayrı oran politikası gerekir. Bu karar
uygulanmadan 400 yazan her satırı her oyuncu için garantili diye tanımlamamak gerekir.

## Düzeltme sırası ve tamamlanma ölçütü

1. **Lusifer–Azrail:** doğrudan kafa kaynağı, tek tüketim, kule tamamlama kaydı ve
   giriş yollarının aynı kurala bağlanması.
2. **Örümcek–Barones:** malzeme drop olasılıkları, Kraliçe zehri, Uriel üretimi,
   tutarlı giriş şartı, Baron ve Flüt aşaması.
3. **General–Beran:** mevcut kaynakları koruyarak gereken anahtarın makul kesim
   sayısında edinilmesi; solo/grup tüketimi ve tekrar girişin birlikte dengelenmesi.
4. **Farm temposu:** günlük kota olmadan kısa bekleme, yeniden bağlantıda ikinci
   bilet kesilmemesi ve GM/normal oyuncu ayrımının açık olması.
5. **Drop kapsamı:** zorunlu bilet, doğrudan ekipman, sandık ödülü, refine malzemesi
   ve biyolog eşyası için ayrı kaynak listeleri. Eksik giriş zincirini sandıkla örtme.

Her ana zindan için tamamlanma ölçütü: oyuncu malzemeyi GM komutu kullanmadan
edinir, doğru NPC'ye gider, maliyet bir kez kesilir, kat mekaniklerini tamamlar,
ödülünü alır ve bir sonraki farm turuna dönebilir. Grup ve yeniden giriş yolları
da aynı bütünün parçalarıdır. Yalnız Lua dosyasının veya boss sandığının mevcut
olması bu ölçütü karşılamaz.

## Uygulama dosyaları

- Drop: `runtime/freebsd/share/locale/europe/mob_drop_item.txt`, `etc_drop_item.txt`.
- Üretim: aynı locale altındaki `cube.txt`; görev kaynakları `quest/quest_tr`.
- Ana görevler: `quest_tr/_alldungeons/{deviltower_zone,devilcatacomb_zone,dragonlair,spider_dungeon}.lua`.
- Geçit ve Kan Taşı: `quest_tr/_npc_talk_mission/{check_trans_ticket,npc_talk}.quest`.
- Derlenen görev seçimi: `quest/quest_list`; çalışan handler verisi: `quest/object`.
- Proto: `runtime/freebsd/share/conf/{item,mob}_proto.txt`.
- Drop hesabı: `apps/server/game/src/item_manager.cpp`, `constants.cpp`, `constants.h`.
- Mevcut ödül politikası: `platform/gameplay/phase3_loot.json`.
- Ayrıntılı ganimet tabloları: [DROP_REHBERI.md](DROP_REHBERI.md).

Bu araştırmada canlı drop, quest, cooldown veya giriş sınırı değiştirilmedi.
