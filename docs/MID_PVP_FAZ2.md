# Mid-PvP Faz 2 — QoL bağlama (tekrar etme)

Son güncelleme: 2026-10-19.

Faz 0+1: [`MID_PVP_FAZ0_1.md`](MID_PVP_FAZ0_1.md). Bu dosya **Faz 2 tamamlanan işler**. Sıra: [`ROADMAP_PVP.md`](ROADMAP_PVP.md).

**Durum:** Repo tamam. Canlı: CONFIG/locale sync + client/web rebuild (Locale_inc biolog alias) → [`../platform/deploy/VM_MID_PVP_APPLY.md`](../platform/deploy/VM_MID_PVP_APPLY.md).

---

## Tekrar etme

| Ne | Nerede |
|----|--------|
| Biolog client alias | `Locale_inc.h`: `ENABLE_BIOLOG_SYSTEM` under `BIOLOGIST` |
| Free BP config | `runtime/.../battlepass_config.txt` (materials only, bonus 0) |
| BP login seed / clear | `char_pass.cpp` `ExternBattlePass` clear + `Load_BattlePass` auto-seed |
| BP level mission gate | `char.cpp` type-1 missions: `val >= 1` (was 250) |
| Teleport mid-pvp | `uiteleport.py` maxLevel 99; Yohara/100+ boards empty |
| Pet passive combat off | `growth_pet.cpp` PASSIVE `UseSkill` → `return false` |
| QoL assert | `platform/tools/mid_pvp_qol_check.py` |

Zaten vardı (dokunma): oto av / switchbot / offlineshop / `do_biyolog` / multi-farm 2.

---

## Offline assert

```sh
python3 platform/tools/mid_pvp_flag_matrix.py
python3 platform/tools/mid_pvp_exp_sim.py
python3 platform/tools/mid_pvp_economy_check.py
python3 platform/tools/mid_pvp_pvp_maps_check.py
python3 platform/tools/mid_pvp_qol_check.py
```

Hepsi exit 0.

---

## Battle Pass notları

- Sunucu token formatı `battlepass_config.txt` (Group `normal.txt` UI referansı; sunucu onu okumaz).
- `REWARDS_BONUS` hep 0 — kalıcı combat affect yok.
- Ödül: BK `50300`, efsun `71084`/`71085`, iksir, vs.
- Progress: type 1 = level-up; type 32 = fishing. İlk login’de player dosyası otomatik seed (ücretsiz track).
- Premium config **yok** → premium track boş kalır.

---

## Pet notları

- Passive combat bonusları kapalı; heal/cleanse auto skill’ler açık.
- Enum/kitap sync hâlâ backlog (CALISMA_NOTLARI).

---

## Sıradaki

**Faz 3** — harita/metin/boss/zindan omurgası (`ROADMAP_PVP.md`). Önce VM’de Faz 0–2 sync önerilir.
