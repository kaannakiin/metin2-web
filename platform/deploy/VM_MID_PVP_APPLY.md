# VM uygulama checklist — mid-pvp Faz 0/1

Agent VM’de `service metin2 restart` çalıştırmaz. Host/VM’de sırayla:

## 1. Kaynak sync + derleme (FreeBSD VM)

```sh
# host → VM: apps/server (service.h, constants.cpp, pvp.cpp, pvp_safe_maps.h, config.cpp, char.cpp)
cd /usr/metin2/apps/server && gmake -j4 all
# binary’ler share/bin’e kopyalanır (mevcut release akışın)
```

## 2. CONFIG

Repo’da `runtime/freebsd/main/**/CONFIG` ve `main/config/*` içinde `MAX_LEVEL: 99`.
Canlı ağaca sync et (ch1 + ch99 yeterli).

## 3. SQL (player DB)

```sh
mysql -u … -p player < update_mid_pvp_refine.sql
mysql -u … -p player < update_mid_pvp_shop_plus9.sql
# trim opsiyonel: update_mid_pvp_shop_trim.sql
```

Dosyalar: `content/server/sql/`.

## 4. Quest / locale

- `welcome.lua` (zaten listede)
- `mid_pvp_rewards.lua` + `quest_list` satırı
- Quest compile (`qc` / mevcut `make_sg` akışı) sonra game restart

## 5. Drop / proto (önceki mid-pvp işi)

`mob_drop_item.txt` vb. sync + db proto reload ihtiyacına göre.

## 6. Servis

```sh
service metin2 restart
service metin2 status
```

## 7. PvP ödül (opsiyonel)

War/arena günü: ` /e mid_pvp_pay 1 ` — oyuncular letter’dan günde bir kez 500k yang + 3×50300 alır. Kapat: `/e mid_pvp_pay 0`.

## 8. Client / web

`Locale_inc.h` Yohara kapalı → web client yeniden `stage`+`engine` (veya ilgili adımlar) + `publish` gerekir.

## Offline doğrulama (Mac, restart yok)

```sh
python3 platform/tools/mid_pvp_flag_matrix.py
python3 platform/tools/mid_pvp_exp_sim.py
python3 platform/tools/mid_pvp_economy_check.py
python3 platform/tools/mid_pvp_pvp_maps_check.py
```
