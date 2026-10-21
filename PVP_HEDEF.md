# Anka2 – 1–99 Orta-Kolay PvP Hedefi

Son güncelleme: 2026-10-20. ~10 kişilik hobi sunucu. Bu dosya **tasarım kilidi** (sayılar, ekonomi, özellik Açık/Kapalı); sayılar değişirse burayı güncelle, sonra koda geç.

Fazlar ve çıkış kriterleri: [`docs/ROADMAP_PVP.md`](docs/ROADMAP_PVP.md). Web/VM log: [`CALISMA_NOTLARI.md`](CALISMA_NOTLARI.md).

## Çizgi

**Orta-kolay: sıkılmadan gir, erken VS at.**  
99 hızlı; **başlangıç +9 set + NPC’den erken band +9** ile oyuncu hemen savaşabilsin.  
Asıl fark / uzun vade: daha iyi base (FMS→mid→end), average, skill, poly, stall — “wallet wins” yok, cash power yok.

Slogan: hızlı VS, orta meta, cash power yok.

Güç cümlesi: early +9 herkes; fark = mid/end base + average + skill P + poly + oyun becerisi.

> Not: Klasik TR “orta emek grind” (NPC’de sadece +0, her şey drop) **bilinçli terk edildi** — hedef eğlence + 10 kişilik tempo.

> Not: Dış kataloglar (Mandes2 / M2Hype tarzı özellik listeleri) ilham kaynağıdır; Anka2’de çoğu sistem `service.h` içinde **zaten kodda** — iş yeni yazmak değil aç/kapa + denge.

---

## Level (99 ≈ 8–12 saat aktif)

| Band  | Hedef süre  | Not                                |
| ----- | ----------- | ---------------------------------- |
| 1–30  | ~1–1.5 saat | Tutorial + ilk silah, sıkılma yok  |
| 30–70 | ~3–4 saat   | İlk gerçek farm, metin + mob       |
| 70–99 | ~4–6 saat   | Yavaşlar ama hafta sonuna yayılmaz |

- Exp ayarı seviye bandına göre (düşük level yüksek, 90+ kontrollü).
- Offline / AFK exp yok veya çok düşük.
- Ölümde exp kaybı yok veya çok az (PvP’den korkulmasın).

### Uygulanan exp ayarı (2026-10-19, offline sim)

Kod: `GetMidPvpMobExpRate` (`constants.cpp`) → `GiveExp` içinde, `mob_exp` flag’inden sonra, kill başı %10 cap’ten önce.

Doğrulama: `python3 platform/tools/mid_pvp_exp_sim.py` (mob_proto median + 1500 kill/saat + early pad 0.8h). Oyunda ölçüm yok.

| Oyuncu level | Çarpan | Sim süre (2026-10-19) |
| ------------ | ------ | --------------------- |
| 1–29         | 35×    | ~1.1h (pad dahil)     |
| 30–69        | 38×    | ~3.9h                 |
| 70–89        | 140×   | ~3.0h                 |
| 90–98        | 220×   | ~2.8h                 |
| 99+          | 1×     | MAX_LEVEL 99          |

Toplam sim ≈ **10.9 saat** (hedef 8–12). `event_flag mob_exp` varsayılan 100 kalsın; oran değişince sim’i yeniden çalıştır.

Ölümde EXP kaybı kapalı; `ItemDropPenalty` çağrısı comment (`char_battle.cpp`). Assert: `mid_pvp_economy_check.py`.

---

## Ekonomi

| Kaynak         | Politika                                                         |
| -------------- | ---------------------------------------------------------------- |
| Yang           | Orta-kolay farmı karşılar; miktar önceki sürümün 4 katı, kill tavanı korunur. |
| Stone / refine | Early +9 NPC/starter. Mid/end base basınca +9 uğraş.             |
| Market         | NPC fiyatları yüksek; oyuncu stall yaşasın.                      |
| Cash shop      | Power item yok.                                                  |

10 kişide enflasyon hızlı gelir → drop’u baştan kıs, sonra aç.

### Uygulanan ekonomi ayarı (2026-10-17)

| Ayar                      | Değer                                          | Nerede                                             |
| ------------------------- | ---------------------------------------------- | -------------------------------------------------- |
| Yang amount               | %50 (proto’nun yarısı)                         | `GetMidPvpGoldAmountRate`                          |
| Kill başı yang tavanı     | 400.000                                        | `GetMidPvpGoldKillCap` (boss bomb parçaları dahil) |
| Metin yang (proto 0 iken) | `500 + level×150` (±%20)                       | `GetMidPvpMetinYang` → `RewardGold`                |
| Ruh taşı kesesi (27999)   | drop pct 50 → **75** (~%12.5 → ~%18.8 / metin) | `mob_drop_item.txt`                                |

Farm mob'ların çoğu proto'da zaten 0 Yang; asıl Yang metin + (tavanlı) boss.
2026-10-20 kullanıcı revizyonu: `mob_gold=400`, `mob_gold_buyer=400`.
Miktar, tavan altında öncekinin 4 katıdır. Normal/premium aynı miktar katsayısı;
düşme ihtimali, seviye cezası ve 400.000 kill tavanı korunur. Temel %50
fonksiyonu değişmez; toplam bonussuz miktar proto'nun %200'üdür.
Metin ödeme tabanı seviye 10/30/50/70/90 için yaklaşık
4.000/10.000/16.000/22.000/28.000 (±%20); ödeme gerçekleşmesi ayrı olasılıktır.

---

## Ekipman bandı (PvP gücü)

| Katman   | Ne                             | Erişim                               |
| -------- | ------------------------------ | ------------------------------------ |
| Start    | **+9 başlangıç seti** (job)    | İlk login `welcome` quest — hemen VS |
| Early    | NPC silah 30 / gövde 42 / takı 33 **+9** | ShopEx; ana ve ikinci köy tüccarları |
| Bridge   | 30 seviye silahlar +9        | Silahçı; bu aileler metinlerden çıkarılır |
| Mid      | Mid base + upgrade / avg       | Metin 55–70 + stall                  |
| Soft end | End base +9 avg                | 70–99 asıl fark                      |
| Flex     | Spirit / sash / poly           | Haftalık, şart değil                 |

- **Başlangıç + NPC early = +9** → sıkılmadan VS; emek mid/end base + average’da.
- **Average = zorunlu endgame bandı.**
- **Spirit = opsiyonel flex** (stall ölmesin).
- Hedef: herkes erken +9 early set; iyi oyuncu mid/end +9 avg.

### Uygulanan upgrade + average (2026-10-17)

**Refine (başarı %)** — fail hâlâ itemi yok eder. Klasik +0→+9 eğrisi:

| Adım  | Eski %                | Yeni %         | His              |
| ----- | --------------------- | -------------- | ---------------- |
| +0…+3 | 90                    | 95             | çok rahat        |
| +4    | 80                    | 90             | rahat            |
| +5→+6 | 60                    | 80             | rahat            |
| +6→+7 | 50                    | 70             | rahat (hedef +7) |
| +7→+8 | 40                    | 55             | orta             |
| +8→+9 | 30 (sert zincirde 10) | 35 (sertte 25) | uğraş            |

Dosyalar: `content/server/sql/seed_shop_refine_pet.sql`, `content/server/sql/update_mid_pvp_refine.sql` (canlı DB), `content/client/packs/locale/common/refine_table.txt` (client %).

**Average (efsun):**

- `ENABLE_MULTI_AFFIX_APPLY_SYSTEM` zaten açık → add attribute ile 5 bonus tek seferde.
- Enchant reroll (71084): metin drop pct 20→**35**.
- Reroll seviye dağılımı lv4/lv5’e kaydırıldı (`item_attribute.cpp` ChangeAttribute).
- Doğal high/low attr tabloları hafif iyileştirildi (`constants.cpp`).

### Shop / drop matrisi (orta-kolay, 2026-10-17)

**2026-10-20 kullanıcı revizyonu:** NPC silahları normal 25 ve altı +
altı klasik 30 silah ailesi **+9**; dört sınıfın 18/26/34/42 gövdeleri +9;
takılarda Abanoz/Yeşim tavanı (33), kask/kalkan 21 tavanı. 48+ gövdeler,
üst takılar ve 65/70/75 silah edinimi mevcut farm hattında kalır.
30 aileleri: Dolunay, Siyah Yaprak, Geyik Boynuzu, Kırmızı Demir, Antik Çan,
Sonbahar Yelpazesi. Bu ailelerin +0…+9 sürümleri metinlerden çıkarılır;
boss tabloları bu istekle topluca silinmez. İsimsiz/hiçbir sınıfın kullanamadığı
6010 ailesi mağazaya eklenmez. Ortalama/beceri zararı doğal üretim kuralıyla gelir.
Mağaza eşyalarına elle başlangıç bonusu veya sabit yüksek ortalama eklenmez.

ShopEx, ana/ikinci köy silahçı ve zırhçılarını ayrı NPC kimlikleriyle aynı
seçkiye bağlar: silah 3, zırh 3 sekme, market 1. Her sekme ilk 40 hücreye
sığar. Fiyatlar satın al/sat döngüsünden Yang üretmez: en az ürün geri satışının
2 katı (ekipman), 1,25 katı (sarf), ayrıca seçilen taban fiyat.
İlk ücretsiz yüzük/dedektör/at kitabından ayrı, markette ücretli yedekleri vardır.
BK, Ruh Taşı ve zindan anahtarları markete konmaz.

Standart/at becerileri: 5. seviyede liderlik/madencilik/dönüşüm 40,
kombo 2, diller 20, at çağırma 10, dört at saldırı becerisi 40. Ana sınıf
becerileri değiştirilmez; BK → G → P hedefi korunur. Mevcut karakterler ve
aynı oturumda grup değişimi de kapsanır. Yeni/eski karaktere kalıcı seviye 30
askeri (zırhlı, saldırabilen) at ve 50053 çağırma kitabı bir defa verilir.
Süreli 52034 bineği ve süresi değişmez. Atın klasik bakım/ölüm davranışı korunur.

| Band           | Erişim                                                           | Ne kalır                                                                 |
| -------------- | ---------------------------------------------------------------- | ------------------------------------------------------------------------ |
| Start          | `welcome`                                                        | Job +9 set                                                               |
| Early NPC      | Silahçı başlangıç, 20–25 ve 30+ok; zırhçı 18–42 gövdeler +9 | Sekmeler gerçek hücre sınırında |
| Late-early     | İkinci köy silahçı/zırhçı aynı seçki | Ayrı NPC kimliği korunur |
| Bridge 25–35   | NPC normal silah/takı ve 30 ortalamalı aileler +9 | Altı 30 silah ailesi metinlerden çıkarılır |
| Mid 50–70      | metin                                                            | Flying Wizard, Rib, Unicorn… + Scale/Fog body **+0**                     |
| Soft end 75–90 | metin + Lusifer sandığı                                           | metinde 65/70 silah ve 61/66 zırh; gerçek 75 silah ailesi Lusifer sandığında |
| Flex           | stall / boss                                                     | spirit, sash, poly                                                       |

### Başlangıç seti (`welcome` quest)

Kaynak: `quest_tr/_npc_talk_mission/welcome.lua` → `object/notarget/login/welcome.start`.

| Job      | Silah (+9)                        | Body / Helm  |
| -------- | --------------------------------- | ------------ |
| Warrior  | 19, 3009                          | 11209, 12209 |
| Assassin | 1009, 2009; normal ok 8000 ×200   | 11409, 12349 |
| Sura     | 19                                | 11609, 12489 |
| Shaman   | 5009, 7009                        | 11809, 12629 |
| Hepsi    | aks 13009…17009 + mount/pet/iksir |              |

#### Başlangıç bonusları ve dedektör — 2026-10-20 revizyonu

Kullanıcı kararı: sınıfa uygun oynanış bonusları; sınıflara karşı güç bonusu değil.
Başlangıçta ölümsüz/şeytan/esoterik gibi ileri alan bonusları verilmez. Ölümsüz
bonusu 50+ içerik/efsun arayışına bırakılır. Silahlar artık boş bonuslu verilmez.

| Sınıf | Silah bonusları (her başlangıç silahında) |
|---|---|
| Savaşçı | STR +8, saldırı hızı +5, kritik %5, delici %5, canavar %10 |
| Ninja | DEX +8, saldırı hızı +5, kritik %5, delici %5, canavar %10 |
| Sura | INT +8, büyü hızı +10, kritik %5, delici %5, canavar %10 |
| Şaman | INT +8, büyü hızı +20, kritik %5, delici %5, canavar %10 |

Zırh: HP +1000, büyü hızı +10, kılıç savunması %10, çift el savunması %10.
Kask: HP yenileme %20, SP yenileme %20, hayvan %10, zehir direnci %8.
Kalkan: sınıf statı +8, blok %5, hayvan %10.
Bilezik: HP +1000, delici %5, hayvan %10. Kolye: HP +1000, kritik %5, delici %5.
Ayakkabı: HP +1000, kritik %5, hareket hızı +10. Küpe: sınıf statı +8, hareket hızı +10, hayvan %10.
Bonus/slot izinleri canlı `item_attr` tablosuyla doğrulanır; zorla geçersiz
sersemletme/bağışıklık kombinasyonları üretilmez.
Var olan +9 base'ler ve zırh taşı korunur; güç farkı mid/end ekipman ve geliştirmede kalır.
Ninja oku mühimmattır: 8000 ×200 verilir, efsun uygulanmaz. Şamana yelpaze ve çan
birlikte verilir; iki oynanış için de başlangıç seçeneği bulunur.

Her yeni karaktere **1 × Metin Taşı Dedektörü (27989), sınırsız kullanım**.
Normal dedektörün kullanım sayacı 0'da tutulur; altı kullanımlık yok edilme koşuluna
ulaşmaz. 76006 numaralı diğer dedektörün davranışı değişmez. İlk-login quest'i
tamamlanmış mevcut karakterlerin eşyaları otomatik yeniden yazılmaz.

### NPC (trim)

#### Başlangıç ulaşımı — 2026-10-20

Her karaktere bir defa **1 × Işınlanma Yüzüğü (40004)** verilir. Yeni karakterler
ilk girişte; mevcut karakterler yüzükleri yoksa sonraki girişte alır. Envanterde
yüzük varsa ikinci kopya verilmez. Yer yoksa teslim sonraki girişe veya
Satıcı (9003) üzerindeki teslim konuşmasına kalır. Başlangıç ekipmanı yeniden
verilmez. Mevcut yüzüğün harita seçenekleri ve zindan giriş koşulları korunur.
Silahçı, zırhçı ve marketin uygulanan içerikleri `docs/NPC_CANLI_STOK.md` içinde;
araştırma geçmişi `docs/NPC_MAGAZA_TASARIMI.md` içinde tutulur.

| Shop | Satılan                                             |
| ---- | --------------------------------------------------- |
| 101–103 / 111–113 | Ana/ikinci köy silahçıları; başlangıç, 20–25, 30+ok |
| 201–203 / 211–213 | Ana/ikinci köy zırhçıları; gövde, kask-kalkan, iç item |
| 301 | Market; günlük sarf ve yüzük/dedektör/at kitabı yedekleri |
| 11   | boş                                                 |

Güncel kaynak: `npc_profile.py stock()` → `shopex` / `shopex_item` tabloları
(`20261020_npc_support.sql`; mevcut kurulum onarımı `20261021_npc_profile.sql`).
Eski 1/2/3/6/7 standart shop kayıtları aynı NPC'de ShopEx ile çakışmaması için
silinir; diğer mağazalar korunur. Seed aynı aktif SQL stoklarını içerir.
Dosya tabanlı `shop_table_ex.txt` kullanılmaz ve dağıtılmaz.

### Metin bereketi — 2026-10-20 (400 ≈ %100)

**Büyülü Metal — 2026-10-21:** 25041, her başarılı düşüşte 1 adet.
Eşik karakter seviyesi değil, metin seviyesidir. 55–60 metinlerde %5,
65–75 metinlerde %8, 80–90 metinlerde %12 temel oran uygulanır.
Mevcut 400 ölçeğinde ham değerler sırasıyla 20/32/48'dir. 55 altına eklenmez.
Kapsam mevcut klasik `MetinLv*` gruplarıdır; aynı seviyedeki tüm bu metinler
aynı oranı kullanır. Mevcut boss/sandık ödülleri ve diğer metin dropları korunur.
Oyunun seviye farkı, düşürme bonusları ve drop hesaplamaları geçerlidir;
bu oranlar her kesimde garanti veya oyuncuya günlük kota değildir.

**Son revizyon — loot v3:** Kullanıcı Lusifer'e 70 silahları da ve eksik klasik
bossların loot'unu istedi. Lusifer'de 6 gerçek 75 silah × %5 = %30; 5 mevcut
70 silah (170/250/1120/3150/7150) × %3 = %15; 7 klasik 65 silah × %1 = %7;
4 sınıfın 66 zırhı × %3 = %12. Kalan %36: 8 ruh taşı %16, 2 beyaz inci %6,
mavi inci %4, kırmızı inci %2, 25 kutsama %8. Aşağıdaki v2 oranları tarihsel
açıklamadır; v3 bunların yerini alır. Güncel eksiksiz sayı kaynağı
`platform/gameplay/phase3_loot.json`, dökümü `docs/DROP_REHBERI.md`.

Eksik 10 klasik boss da tamamlanır: Vahşi Yüzbaşı 36 silah/zırh + kutsama + tali
ruh taşı; Dev Hastalık Taşıyıcı ruh taşı/malzeme; Güçlü Buz Cadısı 66 zırh,
61 kalkan, cennetin gözü takı, +4 soket taşları, kan taşı ve ruh taşı; Barones
doğrudan 75 silah (her biri %3), 66 zırh (%6), 61 kalkan (%4), kristal takı
(%4), 2 ruh taşı @400. Dev Çöl Kaplumbağası kendi sandığı 50076 (65 silah/61
zırh), Kırmızı Ejderha kendi sandığı 50080 (yüksek boss havuzu), Azrail kendi
sandığı 50186 (70 silah/66 zırh/60 kask/81 Titan kalkan/takı). Azrail sandığı
silah %25, zırh/kask/kalkan/takı %49 ve malzeme %26; tek sonuç seçilir.
Ağaç bosslarında 2/3 ruh taşı; Kharoon'da ruh kristali takı ve mavi/kırmızı inci
ile ruh taşı. Tam adet ve oranlar makine politikasındadır. Wiki'nin yeni 100+
ödülleri ve pet kitapları otomatik taşınmaz; gear +0 base/refine ekonomisi korunur.
Harita/regen/respawn ve dungeon mekanikleri değişmez. Kullanıcı bu revizyon için
oyun testini üstlendi; yeni test çalıştırmadan, mevcut derlenmiş istemci ve
kurulum hash/servis kontrolleriyle yayın yapılır.

Yakın seviyeli standart drop ölçeğinde 400 yaklaşık %100'dür. Seviye farkı,
etkinlik ve drop bonusları motorun mevcut kurallarına tabidir; yüksek seviyenin
düşük metin tekeline yönelik cezası kaldırılmaz. BK'lar aynı becerinin tek bir
yığını olarak değil, **bağımsız 1 adetlik satırlar** halinde oluşturulur.

| Metin seviyesi | BK `50300` | Ruh taşı kesesi `27999` | Kutsama `25040` | Efsun `71084` | Arttırma `71085` | Ruh taşı `50513` |
|---|---|---|---|---|---|---|
| 5–20 | 6 ayrı ×1 @400 | 1 @400 | 1 @200 | 10 @200 | 5 @200 | yok |
| 25–45 | 10 ayrı ×1 @400 | 2 @400 | 1 @400 | 15 @240 | 8 @240 | 40/45: 1 @20 |
| 50–70 | 12 ayrı ×1 @400 | 2 @400 | 1 @400 | 15 @240 | 8 @240 | 50/55: @60, 60: @120, 65: @160, 70: @200 |
| 75–90 | 14 ayrı ×1 @400 | 3 @400 | 2 @400 | 20 @300 | 10 @300 | 75/80: @240, 85: @280, 90: @320 |

**Faz 3 revizyonu:** Harita, metin yerleşimi, respawn ve seviye akışı değiştirilmez.
Amaç, oyuncunun 65–70 bandına kadar Master yaptığı ana becerilerini metin farmıyla
G yapabilmesi; bütün becerileri o seviyede Master yapabilmesi anlamına gelmez.
Bu fork `LearnSkillByBook` içinde kademe başına tek başarılı okuma kullanır:
M1→G1 için 10 başarı, yalın okumada %35 başarı. Klasik 55 kitap hesabı uygulanmaz.
Unutma kağıdı `71001` ve münzevi tavsiyesi `71094` her metinden aynı miktarda
gelir: 5–20'de 2'şer, 25–45'te 4'er, 50–70'te 5'er, 75–90'da 6'şar @400.
Mevcut hızlı BK okuma sistemi bu malzemeleri tüketir; skiller doğrudan verilmez.
Kitap becerileri mevcut rastgele havuzdan seçilir; oyuncular arası takas anlamlıdır.
Bu hedef farm tercihine bağlıdır; sadece seviye almak G garantisi değildir.

Ruh taşı normal kaynaklarında kalır: 40/45 metinlerde tali (%5), 50/55'te %15,
60'ta %30, 65'te %40, 70'te %50, 75/80'de %60, 85'te %70, 90'da %80 baz şans.
Kızıl Orman sonu 90 metin (`8027`) ayrıca her sınıfın **66 taban zırhını +0**
%6 bağımsız şansla verir (`11290/11490/11690/11890`); piyasada “70'lik” diye
anılan bu aile proto'da +0 için 66 seviyedir. Önceki 61 zırh satırları korunur.
Bu son ekleme talep edilen PvP ödülüdür; resmî dropla birebir aynı olduğu iddia edilmez.

Klasik boss→kendi sandığı: Ork Reisi `691→50070`, Karanlık Lider `791→50071`,
Karanlık Hayalet Lider `792→50072`, Kraliçe Örümcek `2091→50073`,
Dokuz Kuyruk `1901→50077`, Sarı Kaplan `1304→50078`, Alev Kral `2206→50079`,
Şeytan Kral / Kibirli Şeytan Kral `1091/1092→50081`, Lusifer `1093→50082`.
Her biri yakın seviye bazında bir sandık @400; içinden tek ağırlıklı ödül çıkar.
**Silah ödülü revizyonu — 2026-10-20:** Önceki malzeme ağırlıklı sandık taslağı
yerine klasik ekipman omurgası uygulanır. Erken/orta/yüksek sandıkta toplam
%28 silah (7 farklı 65 taban silahın her biri %4), %12 zırh (4 sınıfın her biri
%3) ve %60 malzeme vardır. Ork/Karanlık Lider ve Hayalet Lider zırhı 54;
Kraliçe Örümcek ve yüksek boss zırhı 61 tabandır. Tüm ekipman +0'dır.
Bu silah aileleri resmî sandık listelerinden seçilir; yüzdeler bize aittir.

Lusifer sandığı: gerçek 75 silah ailesi toplam %30 (Zehir `180`, Aslan `190`,
Şeytan Kanadı `1130`, Havalı Çelik `2170`, Kin `3160`, Orkide `5120`: her biri %5);
65 silah ailesi toplam %14 (7 silah × %2); 66 zırh toplam %16 (4 × %4);
8 ruh taşı %20, 2 beyaz inci %6, 1 mavi inci %4, 1 kırmızı inci %2,
25 kutsama %8. Tek açılış tek sonuçtur. Aynı 75 silah her sandıkta garanti
değildir: Zehir için ortalama 20 sandık, yaklaşık %95 en az bir Zehir şansı
için 59 sandık gerekir; ticaret bu süreyi kısaltabilir.

75 silahların ana ilerleme yeri Lusifer'dir: 85/90 metinlerden Zehir `180`
ve Orkide `5120` kaldırılır. Siam `1120`, Şeytani Pala `250`, Yarı-İnsan `3150`
ve Mutluluk `7150` proto'da 70 seviyedir; metinlerde kalır. Havalı Çelik Yay
`2170`'dir; `2150` 30 seviye Geyik Boynuzu Yay'dır, birbirine karıştırılmaz.
Sandık ağırlıkları toplam 100; mevcut diğer boss dropları korunur. Boss canı,
spawn yeri/süresi, zindan girişleri ve mekaniği bu revizyonda değiştirilmez.
Tam sayılar: `platform/gameplay/phase3_loot.json`.

Araştırma dayanağı: [resmî metin listesi](https://en-wiki.metin2.gameforge.com/index.php/Metin:List)
ve [Kızıl Orman 90 metin](https://en-wiki.metin2.gameforge.com/index.php/Metin_Jeon-Un)
mevcut harita/ödül bağını doğrular. [Resmî BK açıklaması](https://fr-wiki.metin2.gameforge.com/index.php/Livre_de_comp%C3%A9tence)
55 başarı ister; bu fork'un 10 başarı davranışı ayrı incelendi.
[PvP tanıtım örneği](https://www.elitepvpers.com/forum/metin2-pserver-advertising/4221546-turkish-pvp-server.html)
3–5 BK ve 45+ metinlerde seviye ile artan ruh taşı yaklaşımını anlatır;
[Lova2](https://lovamt2.com/tanitim.html?source=pvpserverci) klasik haritalı metin
ödül döngüsü için ikinci karşılaştırmadır. Bunlar dağıtılabilir server kaynakları
veya yayımlanmış kesin yüzdeler değildir; buradaki sayılar 10 kişilik orta-kolay
hedef için bize ait ayarlardır. 48 eşit olasılıklı beceri ve 12 BK/metin varsayımıyla,
münzevi destekli tek bir M1 becerinin 60 yakın-seviye metinde G olma olasılığı
yaklaşık %93'tür; 80 metinde %99'un üstündedir. Münzevisiz aynı hedef belirgin
uzar. Seviye-zaman kabulü gerçek oynanışla ölçülecek; matematik tek başına
“70 olunca kesin G” kanıtı sayılmaz.

Bu revizyonda taşınan iki 75 silah dışında küratörlü base satırları ve yang politikası korunur. Her metin grubunun
adı Mob vnum'u ile benzersiz olmalı; aynı seviyedeki farklı taşların grupları
aynı adı paylaşmaz.

#### Varsayılan envanter — 2026-10-20

Her oyuncuda standart envanterin **4 sayfası (180 hücre)** ücretsiz açık olur.
Mevcut karakterler de kapsanır; envanter genişletme anahtarı gerekmez.
Mevcut dört sayfalık düzen ve eşya hücre numaraları korunur. Bunun veri karşılığı
`player.player.inventory_0 = 18` (iki ek sayfadaki 18 satır); yeni karakterlerde
kolon varsayılanı da 18'dir. Özel envanterlerin kilitleri değişmez.

#### Açık dünya metin yoğunluğu — 2026-10-20

Kullanıcı kararı: başlangıca göre **4 kat metin**, yeniden doğma süreleri
başlangıcın **yarısı** (kesirli saniyeler yukarı yuvarlanır). Mevcut doğma
bölgeleri korunur. Her başlangıç metin kaydının üç bağımsız kopyası eklenir;
kayıt başına `max_count=1` kalır. Böylece RESP
takibinde taşlar aynı regen kimliğini paylaşmaz. Aynı bölge içinde motor
her taş için ayrı rastgele konum seçer; arazi engelleri gerçek sayıyı etkileyebilir.

| Harita | Başlangıç metin kapasitesi | Yeni kapasite |
| --- | ---: | ---: |
| Shinsoo / Chunjo / Jinno 1. köy (1 / 21 / 41) | 12 / 12 / 12 | 48 / 48 / 48 |
| Shinsoo / Chunjo / Jinno 2. köy (3 / 23 / 43) | 10 / 9 / 10 | 40 / 36 / 40 |
| Seungryong (64) | 3 | 12 |
| Yongbi Çölü (63) | 10 | 40 |
| Sohan (61) | 5 | 20 |
| Doyyum (62) | 4 | 16 |
| Hayalet Orman / Kızıl Orman (67 / 68) | 4 / 4 | 16 / 16 |
| `metin2_map_nusluck01` (70) | 2 | 8 |
| **Toplam — 13 harita** | **97** | **388** |

Yalnız bu haritalardaki 8001–8027 metin kayıtları değiştirilir. Madenler,
normal yaratıklar, bosslar, zindan/etkinlik kayıtları ve 100+ haritalar aynı kalır.
Bu yoğunluk artışı loot artışından bağımsızdır; yeniden doğma süresi kısaltılmaz.

Dosya: `runtime/freebsd/share/locale/europe/mob_drop_item.txt` — +1/+2 çöp zırh ve maymun map gear drop’ları temizlendi.

**Küratörlü gear pct:** silah ~10–12, zırh ~8.

**VM:** `mob_drop_item` + `item_proto` sync; güncel `shopex` migration; db/game restart.

---

## At / binek / skill (notlar + kilit)

### Notlar (takip)

- Welcome `52034` Young Lion → mount mob **20204** (Lion Lv1).
- Eski hali: sunucu `MOUNT_TYPE_NORMAL` = **no skill / no atk**; client `CanAttack` level≤1 engeli. PvP’de binek üstünde hasar yok gibi hissediliyordu.
- Klasik at quest (Bo/Chuong) orta-kolayda zorunlu değil; mount QoL yeter.
- Skill P: bedava değil, BK bol + yumuşak okuma → birkaç oturumda P (sonra ayarlanacak).

### Uygulanan binek hasar fix (2026-10-17)

**Hedef:** PvP’deki tüm bineklerde normal saldırı + job skill hasarı.

| Yer                                    | Değişiklik                                                                |
| -------------------------------------- | ------------------------------------------------------------------------- |
| `char_skill.cpp` `GetMountLevelByVnum` | Lv1 binekler (20201–20204…) → `MILITARY`; bilinmeyen 20100–20300 → combat |
| `CanUseSkill`                          | Item mount varken skill check atlanır / `NONE` değilse skill OK           |
| `ComputeSkill` / UseSkill              | `GetMountVnum()!=0` → standing mount gibi job skill (horse skill kapalı)  |
| `char_horse.cpp` `CanUseHorseSkill`    | Item mount’ta false (job skill yolu); sadece klasik grade3 at horse skill |
| Client `InstanceBase.cpp`              | `CanAttack` / `CanUseSkill` her zaman true                                |

**VM:** game rebuild + client/web rebuild (client tarafı da şart).

---

## Skill / book / poly

- Skill book: metinde bol (orta-kolay); stall yine live.
- Master / grand master: birkaç oturum aktif oyun.
- Poly: PvP eğlencesi; ulaşılabilir ama pahalı (yang veya boss).

---

## PvP kuralları

| Yer            | Kural                                  |
| -------------- | -------------------------------------- |
| Köy / safe map | Saldırı yok (`CanAttack` allowlist)    |
| Farm map’ler   | Free PvP (risk / reward)               |
| Arena / duel   | Düzenli dövüş, ceza düşük              |
| Guild war      | Haftada 1–2; ödül: yang + stone + book |

Ölüm: orta yang kaybı; item drop yok (küçük toplulukta toxic).

---

## Boss / metin

- Metin: ana stone + mid item kaynağı.
- Boss: günlük/haftalık 1–2; drop’ta 1–2 aranan item, çöp yığını değil.
- Session hedefi: 2–3 saat yeter; 8 saat metin şartı yok.

---

## Yapılmayacaklar

- 1 günde full **end** +9 avg (early +9 bilerek serbest)
- NPC’de FMS / mid / end base
- Sınırsız yang / GM shop’tan her şey
- Sürekli exp event
- Ölümde item drop
- Cash shop power item
- İlk sürümde: simya güç farkı, kuşak güç, 6–7 efsun, aura güç, Yohara/şampiyon olduğu gibi, 100+ zindanlar (Razador/Nemere/Meley) yeniden dengelenmeden

---

## Özellik seçimi (ilk sürüm)

Durum: **Açık** = 1. sürümde olsun · **Kapalı** = bilerek yok · **Sonra** = Faz 6+ · **Bağla** = kodda var, smoke test / denge lazım.

Kaynak bayraklar çoğunlukla `apps/server/common/service.h` (+ client `Locale_inc.h`). Faz sırası: [`docs/ROADMAP_PVP.md`](docs/ROADMAP_PVP.md).

### Temel yapı

| Özellik                       | Karar            | Not                                                       |
| ----------------------------- | ---------------- | --------------------------------------------------------- |
| 1–99, dört klasik karakter    | Açık             | Lycan: Sonra / isteğe bağlı                               |
| Başlangıç +9 + level ödülleri | Açık / Bağla     | welcome + NPC early; level sandıkları Faz 2–3             |
| M/G/P beceri                  | Açık             | P bedava değil; BK bol                                    |
| Uzaktan biyolog               | Bağla            | `ENABLE_BIOLOGIST_SYSTEM`; 96/98 varsa yalnızca küçük PvM |
| MAX_LEVEL 99                  | Açık             | CONFIG `MAX_LEVEL: 99` + default `gPlayerMaxLevel` 99      |
| Yohara / şampiyon             | Kapalı           | `//#define ENABLE_YOHARA_SYSTEM` (service + Locale_inc)   |
| ACCE / Aura flag              | Açık (güç yok) | Compile açık; shop/BP power vermez                        |

### Farm ve boss

20 Ekim 2026 kullanıcı kararı: wiki, klasik kaynak → anahtar/malzeme → NPC →
zindan bağlantısı için referanstır. Güncel resmî sürümün günlük giriş kotası,
Nesne Market bileti ve uzun bekleme modeli kopyalanmaz. Orta-kolay sunucuda
General → Kıvrık Anahtar → Beran ve Lusifer → Küçülen Kafa → Azrail hatları
tekrar farm yapılabilecek şekilde dengelenir; Beran günde bir kesime sınırlandırılmaz.
Malzeme adedi, üretim/düşüş şansı ve bekleme süreleri bu hedefe göre seçilir.
Mevcut zincirlerin kaynaklı denetimi: [Faz 3 klasik zincir denetimi](docs/FAZ3_KLASIK_ZINCIR_DENETIMI.md).

Canlıya alınacak orta-kolay zincir profili:

- 13 klasik bossun sandığı kesim başına 1 adet, seviye cezasından bağımsız.
- Komutan/General 2491/2492/2494/2495 kesiminden 3 Kıvrık Anahtar garantili;
  Beran giriş maliyeti kişi başına 3 anahtar kalır.
- Lusifer 2 Küçülen Kafa, Kraliçe Örümcek 1 zehir garantili verir.
- Mevcut yerindeki Kraliçe grubu 2019 ve Sürgün 2 Komutan 2491 doğma süresi
  15 dakikadır; yeni doğma noktası eklenmez.
- Normal örümceklerin kendi beş üretim malzemesi ayrı ayrı %25 düşer.
  Uriel 50 seviyede bir defalık Yüzbaşı–Mezar Taşı–Uriel hazırlığından sonra
  her malzemeden 1 adet ve 1 Kraliçe zehri ile %100 Arachnida Anahtarı üretir.
- Buz Cadısı/Güçlü Buz Cadısı, iki General ve Beran 1 Kan Taşı garantili verir.
- Bu sandık ve giriş/üretim malzemeleri mevcut `Type limit` drop yolu ile
  seviye cezasından ayrılır. Metin ve diğer ekipman düşüşünün seviye politikası aynı.
- Kule, Katakomb, Barones ve Beran başarılı kesim sonrası 10 dakika bekler;
  günlük giriş kotası yoktur. Katakomb'da kule tamamlama kaydı gerekir, kafa
  her katılımcıdan yalnız ikinci kattan üçüncü kata geçişte bir kez tüketilir.
- Barones giriş seviyesi her yolda 50, kişi başına 1 Arachnida Anahtarıdır.
  Zindanda Baron → Flüt → Barones sırası ve yumurta mekaniği korunur.

| Özellik                               | Karar | Not                                    |
| ------------------------------------- | ----- | -------------------------------------- |
| Klasik haritalar + metin              | Açık  | küratörlü drop matrisi yukarıda        |
| Klasik alan bossları (~10)            | Açık  | Faz 3; loot ekonomiye bağlı            |
| Şeytan Kulesi, Barones, Azrail, Beran | Açık  | Faz 3                                  |
| 1–99’a uyarlanmış Razador/Nemere      | Sonra | 100+ olduğu gibi koyma                 |
| Boss / zindan takip UI                | Bağla | `ENABLE_DUNGEON_*` / track / NPC trace |
| Özel son seviye farm haritası         | Sonra | en fazla 1; popülasyonu dağıtma        |

### Binek ve pet

| Özellik                                | Karar  | Not                                                                |
| -------------------------------------- | ------ | ------------------------------------------------------------------ |
| Normal / Zırhlı / Asker At             | Açık   | klasik quest zorunlu değil (orta-kolay)                            |
| Özel binek + görünüm                   | Bağla  | `ENABLE_MOUNT_*`, change look; PvM tavan düşük                     |
| Basitleştirilmiş pet                   | Bağla  | `ENABLE_GROWTH_PET_SYSTEM`; enum/kitap bug’ı düzelt veya skill kıs |
| Full resmi pet 100 lv / ölüm / besleme | Kapalı | gereksiz karmaşa                                                   |

### Ekipman

| Özellik                          | Karar  | Not                                   |
| -------------------------------- | ------ | ------------------------------------- |
| Switchbot / otomatik efsun (1–5) | Bağla  | `ENABLE_RENEWAL_SWITCHBOT`            |
| +9 refine (fail yok eder)        | Açık   | mid-pvp % tablosu                     |
| Kostüm / saç / silah kostüm      | Açık   | görünüm ağırlıklı                     |
| Kuşak (güç)                      | Kapalı | kozmetik istersen Sonra               |
| Simya (güç)                      | Kapalı |                                       |
| 6–7 efsun                        | Kapalı |                                       |
| Aura (güç)                       | Kapalı | flag’li kod var; 1. sürümde güç verme |
| PvM/PvP set ayrımı               | Sonra  |                                       |

### Ekonomi ve modern sistemler

| Özellik                       | Karar | Not                                          |
| ----------------------------- | ----- | -------------------------------------------- |
| Ücretsiz oto av               | Bağla | `__AUTO_HUNT__`; multi-farm limiti           |
| Offline pazar + arama         | Bağla | `ENABLE_RENEWAL_OFFLINESHOP` + search; vergi |
| Craft (boss → sandık/görünüm) | Sonra | güç craft’ı değil                            |
| Battle Pass (ücretsiz)        | Bağla | `ENABLE_BATTLE_PASS`; power ödül yok         |
| Günlük / haftalık görev       | Bağla | hunting / event                              |
| Hızlı ışınlanma               | Bağla | `ENABLE_RENEWAL_TELEPORT_SYSTEM`             |
| Otomatik balıkçılık           | Sonra | etkinliklerde yeter                          |

### PvP ve yönetim

| Özellik                | Karar | Not                                        |
| ---------------------- | ----- | ------------------------------------------ |
| 1v1, 2v2, lonca savaşı | Açık  | Faz 1 ödül iskeleti; Faz 5 ritim           |
| Dereceli PvP           | Sonra |                                            |
| Eşit itemli arena      | Sonra | dünya ≠ ranked                             |
| Etkinlik takvimi       | Bağla | `ENABLE_EVENT_SYSTEM`                      |
| GM / güvenlik / HWID   | Açık  | mevcut fix’ler                             |
| Çok dilli istemci      | Açık  | zaten web + `ENABLE_MULTI_LANGUAGE_SYSTEM` |

### İçerik iskeleti (özet)

| Konu        | Hedef (detay Faz 3+)                                   |
| ----------- | ------------------------------------------------------ |
| Level akışı | 1–20 köy → … → Sürgün 1–2 → opsiyonel 1 end map        |
| Alan boss   | Vahşi Yüzbaşı … General; respawn 15–120 dk bandı       |
| Zindan      | Kule, Barones, Azrail, Beran                           |
| Binek bandı | Lv1 hız → 35 zırhlı → 50 asker → yüksekte düşük PvM %  |
| Pet         | bir aktif; ticaret OK; PvP bonus ciddi fark yaratmasın |

---

## Offline doğrulama

```sh
python3 platform/tools/mid_pvp_flag_matrix.py
python3 platform/tools/mid_pvp_exp_sim.py
python3 platform/tools/mid_pvp_economy_check.py
python3 platform/tools/mid_pvp_pvp_maps_check.py
```

VM uygulaması: [`platform/deploy/VM_MID_PVP_APPLY.md`](platform/deploy/VM_MID_PVP_APPLY.md).

## Uygulama sırası

Kısa checklist (detay: [`docs/ROADMAP_PVP.md`](docs/ROADMAP_PVP.md)):

1. Bu hedef kilidi (bu dosya) — **tamam**
2. Exp 1–99 — **sim yeşil (~10.9h); oranlar 35/38/140/220×**
3. Drop + yang — **kod + assert yeşil; VM sync checklist**
4. NPC shop + early +9 + welcome — **economy_check yeşil; VM SQL**
5. Upgrade % + average — **refine SQL assert yeşil; VM SQL**
6. PvP safe map listesi — **tamam** (`pvp_safe_maps.h` + `pvp.cpp`)
7. War/arena ödül + MAX_LEVEL 99 — **tamam** (`mid_pvp_rewards.lua`, CONFIG 99)
8. Faz 0 flag matrisi — **tamam** (Yohara kapalı; matrix script yeşil)
9. Faz 2 QoL smoke — **açık**
10. Faz 3 boss/zindan — **açık**
