# Anka2 – 1–99 Orta-Kolay PvP Roadmap

Son güncelleme: 2026-10-19.

Bu dosya **geliştirme sırası ve faz çıkış kriterleri**. Sayılar, ekonomi ve “yapılmayacaklar” kilidi: [`PVP_HEDEF.md`](../PVP_HEDEF.md). Web/VM günlük log: [`CALISMA_NOTLARI.md`](../CALISMA_NOTLARI.md). Ağaç haritası: [`ARCHITECTURE.md`](ARCHITECTURE.md).

## İlişki

```text
PVP_HEDEF.md              ← tasarım kilidi (exp, yang, shop, özellik Açık/Kapalı)
docs/ROADMAP_PVP.md       ← fazlar, sırası, çıkış kriteri (bu dosya)
docs/MID_PVP_FAZ0_1.md    ← Faz 0+1 yapılanlar (tekrar etme)
docs/MID_PVP_FAZ2.md      ← Faz 2 QoL yapılanlar (tekrar etme)
CALISMA_NOTLARI.md        ← web/deploy/VM ne yapıldı / ne açık
```

Kural: çoğu “özellik” Anka2 `service.h` içinde **zaten kodda**. İş çoğu zaman yeni sistem yazmak değil; **aç/kapa + denge + drop/quest omurgası**.

Her özellik için dört soru:

1. Kodda var mı? (`service.h` / quest / locale)
2. Güç mü, QoL mu? Güç ise early +9 kilidini bozar mı?
3. ~10 kişide ekonomi yaşar mı?
4. Web client’a paket / UI / paket maliyeti var mı?

Paralel öncelik: web stabilite (ASan vb.) oyun içeriğiyle birlikte yürür; çökük client’ta denge ölçülmez.

---

## Özet omurga (hedef ürün)

Klasik dört karakter + basit pet/binek + ücretsiz oto av + ~10 alan bossu + 4 ana zindan + 75 silah farmı + biyolog + Battle Pass (power yok) + offline pazar + PvP turnuvaları.

**İlk sürümde yok / ertele:** simya güç farkı, kuşak güç, 6–7 efsun, aura güç, Yohara/şampiyon olduğu gibi, cash power, 10 özel farm adası, Razador/Nemere/Meley’nin 100+ halleri.

Güç cümlesi: early +9 herkes; fark = mid/end base + average + skill P + poly + oyun becerisi.

---

## Faz 0 — Envanter ve kilitleme

**Süre tahmini:** 3–5 gün  
**Durum:** tamam (2026-10-19) — VM/web publish kullanıcı checklist’inde

### İşler

1. Flag matrisi: `platform/tools/mid_pvp_flag_matrix.py` yeşil.
2. Yohara kapalı (`//#define ENABLE_YOHARA_SYSTEM` service.h + Locale_inc.h). ACCE/Aura flag açık, güç içerikte yok.
3. `MAX_LEVEL: 99` tüm channel CONFIG; `gPlayerMaxLevel` default 99; level-up duyurusu `case 99`.
4. Doküman senkron: `PVP_HEDEF.md` + bu dosya.

### Çıkış kriteri

Flag matrix yeşil; CONFIG 99; Yohara kapalı. **Karşılandı (offline).**

---

## Faz 1 — Çekirdek döngü (`PVP_HEDEF` kalanı)

**Süre tahmini:** 1–2 hafta  
**Durum:** repo tamam (2026-10-19); canlı VM uygulaması [`platform/deploy/VM_MID_PVP_APPLY.md`](../platform/deploy/VM_MID_PVP_APPLY.md)

| # | İş | Durum | Nerede |
|---|-----|--------|--------|
| 1 | Hedef kilidi | tamam | `PVP_HEDEF.md` |
| 2 | Exp bandları 1–99 | sim yeşil (~10.9h) | `GetMidPvpMobExpRate` 35/38/140/220× |
| 3 | Drop + yang | assert yeşil; VM sync | mid-pvp gold + economy_check |
| 4 | NPC early +9 + welcome | assert yeşil; VM SQL | `update_mid_pvp_*.sql`, welcome |
| 5 | Refine % | assert yeşil; VM SQL | `update_mid_pvp_refine.sql` |
| 6 | Safe vs free-PvP | tamam | `pvp_safe_maps.h` + `pvp.cpp` |
| 7 | War ödül + MAX 99 | tamam | `mid_pvp_rewards.lua`, CONFIG |
| 8 | Ölüm: EXP/item drop yok | tamam (assert) | `char_battle.cpp` |

### Çıkış kriteri

Offline: dört `platform/tools/mid_pvp_*.py` yeşil. Canlı: VM checklist uygulandı.

---

## Faz 2 — QoL’u çalışır hale getir

**Süre tahmini:** 1–2 hafta  
**Durum:** tamam (2026-10-19) — done log: [`MID_PVP_FAZ2.md`](MID_PVP_FAZ2.md); VM/web sync checklist’te

### Yapılanlar (özet)

- Biolog client alias (`ENABLE_BIOLOG_SYSTEM`)
- Free `battlepass_config.txt` + login seed; level mission gate 250→1; bonus affects 0
- Teleport maxLevel 99; Yohara/100+ warp boards boş
- Growth pet PASSIVE combat kapalı
- Assert: `platform/tools/mid_pvp_qol_check.py`

### Çıkış kriteri

Offline: beş `mid_pvp_*.py` yeşil. **Karşılandı (repo).** Canlı: VM_MID_PVP_APPLY + pack/Locale rebuild.

---

## Faz 3 — İçerik omurgası (harita / metin / boss / zindan) — **sıradaki**

**Süre tahmini:** 2–3 hafta  
**Durum:** sürüyor (2026-10-20). Önceki drop / başlangıç / dedektör / 2× yoğunluk
paketi canlıda. Yeni revizyon: klavye toplama ve binek saldırısı düzeltmesi;
6/10/12/14 BK, okuma malzemeleri, kademeli ruh taşı ve klasik boss sandıkları.
`platform/gameplay/phase3_loot.json` sayıların makine tarafından doğrulanan kopyası;
asıl tasarım kilidi `PVP_HEDEF.md`. Haritalar ve doğma bölgeleri korunur.
Son kullanıcı kararı: metin sayısı başlangıcın 4 katı, yeniden doğma süreleri yarısı;
13 haritada toplam kapasite 388, `20261020-140835` ile canlıda.
Sayılar `metin_density.json` v2 içinde.
Loot v3 ve web tuş düzeltmeleri **20261020-134850 ile canlıya kuruldu**.
Kullanıcı oyun kabulünü üstlendi; bu tur yeni test çalıştırılmadı. Kayıt ve yedekler
`platform/deploy/GAMEPLAY_RELEASE.md` içinde. Boss notice/izleme ve zindan
instance/reentry omurgası tamamlanmadı; faz çıkış kriteri henüz sağlanmadı.

Silah revizyonu (loot v2): Lusifer sandığı 6 gerçek 75 silahı içerir; diğer klasik
sandıklara 65 silah/54–61 zırh eklendi. Zehir/Orkide 85/90 metinlerden taşındı.
Loot v3 ile Lusifer'in 70 silahları da eklendi; önceki rehberde eksik olan 10
klasik boss tamamlandı (Barones, Azrail ve diğerleri). Tam envanter
`docs/DROP_REHBERI.md` içinde. Önceki v1/v2 adaylar kullanılmaz; güncel v3
kuruludur. Instance/reentry ve canlı oyuncu kabulü faz çıkışı için hâlâ açık.

1. Level akışı: 1–20 köy → 2. köy → Seungryong → Hwang → Yongbi/Örümcek → Sohan/Doyyum → Kızıl Orman → Sürgün 1–2 → opsiyonel 1 end map.
2. Metin: band drop (küratörlü gear) + yüksek level’ın düşük farm tekeline engel.
3. Açık dünya boss havuzu (ör. Vahşi Yüzbaşı → General): respawn 15–120 dk, sandık önizleme, hasar/notice; her boss loot’u mid/end veya malzeme sink’ine bağlı.
4. Zindanlar: Şeytan Kulesi, Barones, Azrail, Beran — instance + reentry; mekanikleri koru.
5. Razador / Nemere / Meley: **bu fazda yok** (veya Faz 6’da 95–99’a yeniden dengeli).

Önerilen respawn bandı (nüfusla ayarla): düşük 15–30 dk, orta 30–60, yüksek 60–120.

### Çıkış kriteri

Her level bandında “bu hafta ne farmlarım?” net; boss sandığı ekonomiye bağlı.

---

## Faz 4 — Uzun vade meta

**Süre tahmini:** ~2 hafta (+ sürekli ince ayar)  
**Durum:** planlandı

- Mid/end base yalnızca metin/boss (NPC’de yok — kilit)
- Average üst sınırları açık tablo (`item_attr` gerçek değerler)
- Craft: boss materyali → sandık / binek görünüm / pet kademe (güç değil)
- Binek: hız → zırhlı → asker; PvM bonus tavanı düşük (%5–10)
- Günlük/haftalık görevler (`ENABLE_HUNTING_SYSTEM` vb.)
- Ekonomi takibi: günlük yang girişi, refine sink, pazar vergisi

### Çıkış kriteri

Early +9 evrensel; sıralama farkı avg + mid/end + skill’de.

---

## Faz 5 — PvP sezonu ve etkinlikler

**Süre tahmini:** sürekli  
**Durum:** planlandı

| Ritim       | İçerik                                         |
| ----------- | ---------------------------------------------- |
| Haftalık    | OX, metin yağmuru veya boss istilası, 1v1 / WS |
| İki haftada | Lonca savaşı                                   |
| Aylık       | Sezon / ünvan / kozmetik                       |

İleri (isteğe bağlı): eşit itemli ranked arena (dünya PvP ≠ ranked). Replay yok.

---

## Faz 6 — Bilinçli “sonra”

Açma ta ki Faz 1–4 oturana kadar:

- Simya (güç), kuşak güç, 6–7 efsun, aura güç
- Full resmi pet grind (ölüm/besleme/100 lv)
- Çok sayıda özel farm adası
- 100+ Razador/Nemere/Meley olduğu gibi
- Cash shop power item
- Lycan (istersen ayrı denge dalı)

---

## Yakın 4 hafta (önerilen sıra)

1. ~~Faz 0~~ **tamam**
2. ~~Faz 1~~ **repo tamam** → VM sync
3. ~~Faz 2 QoL~~ **repo tamam** ([`MID_PVP_FAZ2.md`](MID_PVP_FAZ2.md)) → Locale/pack + BP config sync
4. Faz 3 — ilk 5 alan bossu + 2 zindan drop omurgası

Web ASan / publish stabilitesi paralel.

---

## Teknik not (modül ipuçları)

| Alan                                            | Tipik yer                                                             |
| ----------------------------------------------- | --------------------------------------------------------------------- |
| Flag’ler                                        | `apps/server/common/service.h`, client `Locale_inc.h`                 |
| Exp/yang mid-pvp                                | `constants.cpp` (`GetMidPvp*`), `char_battle.cpp`                     |
| Shop / refine SQL                               | `content/server/sql/update_mid_pvp_*.sql`, `seed_shop_refine_pet.sql` |
| Drop                                            | `runtime/freebsd/share/locale/europe/mob_drop_item.txt`               |
| Welcome                                         | quest `welcome` (`quest_tr` / object)                                 |
| Oto av / switchbot / offlineshop / BP / biyolog | ilgili `ENABLE_*` + locale `battlepass/`, quest                       |
| PvP harita                                      | `pvp.cpp`, map index / CONFIG                                         |

Detaylı özellik kararları: `PVP_HEDEF.md` § Özellik seçimi.
