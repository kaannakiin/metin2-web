# Mid-PvP Faz 0 + Faz 1 — Yapılanlar (tekrar etme)

Son güncelleme: 2026-10-19.

Bu dosya **tamamlanan işlerin envanteri**. Faz 0/1’i yeniden planlama veya yeniden kodlama. Sayılar: [`../PVP_HEDEF.md`](../PVP_HEDEF.md). Sıra: [`ROADMAP_PVP.md`](ROADMAP_PVP.md). Canlıya alma: [`../platform/deploy/VM_MID_PVP_APPLY.md`](../platform/deploy/VM_MID_PVP_APPLY.md).

**Durum:** Repo tarafı tamam. Canlı VM sync / `gmake` / restart / web publish → kullanıcı checklist.

---

## Tekrar etme — dokunma listesi

Aşağıdakiler bilerek yapıldı; aynı işi ikinci kez yapma:

| Ne | Nerede | Not |
|----|--------|-----|
| Yohara kapalı | `apps/server/common/service.h`, `apps/client/source/UserInterface/Locale_inc.h` | `//#define ENABLE_YOHARA_SYSTEM` (CRLF koru) |
| MAX_LEVEL 99 | `runtime/freebsd/main/**/CONFIG` + `main/config/*` (26 dosya) | `MAX_LEVEL: 99` |
| Default max level | `apps/server/game/src/config.cpp` | `gPlayerMaxLevel = 99` |
| Level-up duyurusu | `apps/server/game/src/char.cpp` | `case 99` (`ENABLE_ANNONUNCEMENT_LEVELUP`) |
| Exp oranları | `apps/server/game/src/constants.cpp` `GetMidPvpMobExpRate` | 35× / 38× / 140× / 220× (sim ~10.9h) |
| Safe PvP maps | `apps/server/game/src/pvp_safe_maps.h` + `pvp.cpp` | köy/guild/OX/duel/trade; farm free |
| PvP ödül stub | `…/quest_tr/_guildsystems/mid_pvp_rewards.lua` + `quest_list` | `/e mid_pvp_pay 1` |
| Offline assert’ler | `platform/tools/mid_pvp_*.py` | aşağıda |
| VM checklist | `platform/deploy/VM_MID_PVP_APPLY.md` | restart agent yapmaz |

Önceden (Faz 1 öncesi) repo’da zaten vardı — yeniden yazma:

- Welcome +9 / shop plus9 SQL / refine SQL / yang %50 + kill cap / death EXP=0 / ItemDropPenalty comment

---

## Offline assert (yeşil kabul)

```sh
python3 platform/tools/mid_pvp_flag_matrix.py
python3 platform/tools/mid_pvp_exp_sim.py          # ~10.9h, 8–12 hedef
python3 platform/tools/mid_pvp_economy_check.py
python3 platform/tools/mid_pvp_pvp_maps_check.py
```

Hepsi 0 exit ile geçmeli. Exp oranı değişirse önce sim, sonra `PVP_HEDEF` tablosu.

---

## Exp bandı (kilit — sim çıktısı)

| Level | Çarpan | Sim saat |
|-------|--------|----------|
| 1–29 | 35× | ~1.1 (pad dahil) |
| 30–69 | 38× | ~3.9 |
| 70–89 | 140× | ~3.0 |
| 90–98 | 220× | ~2.8 |
| 99+ | 1× | MAX 99 |

---

## Safe map index’leri

`IsMidPvpSafeMap`: 1, 21, 41, 6, 26, 46, 4, 24, 44, 81, 112, 113, 200, 230, 231.

Farm haritaları bu listede **yok** → mevcut PK ile free PvP.

---

## Bilinçli açık bırakılanlar (Faz 0 kararı)

- ACCE / Aura / Dragon Soul: **flag açık**, güç shop/BP’de yok (içerik filtresi Faz 2+)
- Simya / kuşak güç / 6–7 efsun / Yohara zindanları: kapalı veya ertele
- Oyunda playtest yok — doğrulama sadece script

---

## Hâlâ kullanıcıda (repo dışı)

1. VM: `VM_MID_PVP_APPLY.md` (gmake, SQL, quest qc, CONFIG sync, restart)
2. Web: `Locale_inc.h` Yohara → client/engine rebuild + publish
3. Sonra: Faz 2 (aşağıya bak)

---

## Sıradaki faz önerisi

**Faz 2 — QoL’u çalışır hale getir** (`ROADMAP_PVP.md`).

Neden şimdi boss (Faz 3) değil: kodda oto av / switchbot / offlineshop / biyolog / BP / teleport zaten var; yeni oyuncu akışı kırıkken drop omurgası boşa gider. ~10 kişide önce “gir → kas → sat → efsun” hattı.

Faz 2 kapsamı (yeni sistem yazma, bağla + assert + power’sız ödül):

1. Oto av + multi-farm limiti smoke (flag/config)
2. Switchbot 1–5 hedef-dur
3. Offline pazar + arama + vergi (yang sink)
4. Uzaktan biyolog (30→94)
5. Işınlanma + NPC/boss trace
6. Battle Pass ücretsiz track — yalnızca malzeme/kozmetik
7. Pet: enum/kitap bug veya skill kıs; düşük bonus

Paralel (Faz 2’den önce veya birlikte): VM_MID_PVP_APPLY — aksi halde canlıda Faz 0/1 görünmez.
