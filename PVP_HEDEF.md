# Anka2 – 1–99 Orta-Kolay PvP Hedefi

Son güncelleme: 2026-10-19. ~10 kişilik hobi sunucu. Bu dosya **tasarım kilidi** (sayılar, ekonomi, özellik Açık/Kapalı); sayılar değişirse burayı güncelle, sonra koda geç.

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
| Yang           | Kıt. Upgrade, stall, book’un ana maliyeti. Mob’dan bol yang yok. |
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

Farm mob’ların çoğu proto’da zaten 0 yang; asıl yang metin + (kaplı) boss. `mob_gold` event flag varsayılan 100 kalsın.

---

## Ekipman bandı (PvP gücü)

| Katman   | Ne                             | Erişim                               |
| -------- | ------------------------------ | ------------------------------------ |
| Start    | **+9 başlangıç seti** (job)    | İlk login `welcome` quest — hemen VS |
| Early    | Aynı early base’ler **NPC +9** | Shop 1/2/6/7 (lv≤22); yedek / alt    |
| Bridge   | Daha iyi base (FMS vb.)        | Metin 25–35 drop                     |
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

**Kilit kural:** Early **+9** (welcome + NPC). Gereksiz ara silah/zırh **silindi**. Lv25+ sadece **küratörlü** base’ler metinde. Consumable bol → hızlı cas.

| Band           | Erişim                                                           | Ne kalır                                                                 |
| -------------- | ---------------------------------------------------------------- | ------------------------------------------------------------------------ |
| Start          | `welcome`                                                        | Job +9 set                                                               |
| Early NPC      | shop1 = **yalnız lv15 +9** + ok; shop2 = lv18 body + aks/helm +9 | ara basamak yok                                                          |
| Late-early     | shop6/7 **+9** lv≤22                                             | FMS yok                                                                  |
| Bridge 25–35   | metin                                                            | Silver / **FMS 290** / Hornbow / Lion plate / jade aks                   |
| Mid 50–70      | metin                                                            | Flying Wizard, Rib, Unicorn… + Scale/Fog body **+0**                     |
| Soft end 75–90 | metin                                                            | Nymph, Exorcism, Lightning Knife… + Dragon God body; 85+ Poison/Siamese… |
| Flex           | stall / boss                                                     | spirit, sash, poly                                                       |

### Başlangıç seti (`welcome` quest)

Kaynak: `quest_tr/_npc_talk_mission/welcome.lua` → `object/notarget/login/welcome.start`.

| Job      | Silah (+9)                        | Body / Helm  |
| -------- | --------------------------------- | ------------ |
| Warrior  | 19, 3009                          | 11209, 12209 |
| Assassin | 1009, 2009, 8009                  | 11409, 12349 |
| Sura     | 19                                | 11609, 12489 |
| Shaman   | 7009                              | 11809, 12629 |
| Hepsi    | aks 13009…17009 + mount/pet/iksir |              |

### NPC (trim)

| Shop | Satılan                                             |
| ---- | --------------------------------------------------- |
| 1    | Bamboo/Battle/… **lv15 +9** + ok (lv0/5/10 silindi) |
| 2    | **lv18 body +9** + early helm/shield/aks +9         |
| 6    | Broad/Scissor/… **lv20 +9** + ok                    |
| 7    | helm/kalkan/aks ~lv22 +9                            |
| 11   | boş                                                 |

SQL: `seed_shop_refine_pet.sql` + `update_mid_pvp_shop_plus9.sql`.

### Metin consumable (400 ≈ %100)

| Item                    | Erken (≤20) | Mid (≤70) | Yüksek (75+) |
| ----------------------- | ----------- | --------- | ------------ |
| Beceri kitabı `50300`   | 280 (~%70)  | 400       | 400          |
| Ruh taşı kesesi `27999` | 100 (~%25)  | 100       | 100          |
| Efsun nesnesi `71084`   | 5× @90      | 12× @100  | 16× @100     |
| Arttırma kağıdı `71085` | 3× @75      | 8× @80    | 10× @80      |

Dosya: `home/share/locale/europe/mob_drop_item.txt` — +1/+2 çöp zırh ve maymun map gear drop’ları temizlendi.

**Küratörlü gear pct:** silah ~10–12, zırh ~8.

**VM:** `mob_drop_item` + `item_proto` sync; `update_mid_pvp_shop_plus9.sql`; db/game restart.

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
