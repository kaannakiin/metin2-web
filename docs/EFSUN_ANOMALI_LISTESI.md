# Karar bekleyen 14 efsun — canlı durum

> **Son kullanıcı kararı uygulandı:** aşağıdaki tablo kapatma öncesindeki
> durumu kaydeder. Bu 14 türün normal/kostüm/tılsım rastgele havuzlarındaki
> 12 izin sütunu canlı DB'de sıfırlandı. Oyun süreçlerine yansıması için GM
> `/reload p` veya operatör bakım restart'ı gerekir. Yeni durum ve yedek:
> [klasik izin uygulaması](EFSUN_KLASIK_IZINLER.md).

22 Ekim 2026. Canlı `player.item_attr` tablosunun 59 satırı salt okunur
kontrol edildi. Aşağıdaki 14 satırın değerleri ve sekiz standart ekipman
izni repo ile eşleşiyor. İnceleme sırasında oyun verisi değiştirilmedi.

Önceki düzenlemede 45 normal efsunun dağılımı/değerleri düzeltildi; bu 14
satır ayrı karar beklendiği için eski izinleriyle bırakıldı. Bu yüzden
**kalkana ortalama zarar gelmesi, şu anki normal efsun havuzunda mümkün**.

## Liste

Tablodaki değerler üst değerdir; bu 14 satır hâlâ değişken kademelidir.

- **Tüm 8 ekipman:** silah, gövde zırhı, bilezik, ayakkabı, kolye, kask,
  kalkan ve küpe.
- **Silah dışındaki 7 ekipman:** gövde zırhı, bilezik, ayakkabı, kolye,
  kask, kalkan ve küpe.

| # | Efsun | Üst değer | Şu an gelebilen ekipmanlar | Kalkana gelir mi? |
| --- | --- | ---: | --- | --- |
| 1 | Ortalama zarar | %10 | Tüm 8 ekipman | **Evet** |
| 2 | Beceri hasarı | %10 | Tüm 8 ekipman | **Evet** |
| 3 | Ortalama zarara direniş | %10 | Silah dışındaki 7 ekipman | **Evet** |
| 4 | Beceri hasarına direniş | %10 | Silah dışındaki 7 ekipman | **Evet** |
| 5 | Savaşçılara karşı güçlü | %10 | Silah, kolye, kask, kalkan | **Evet** |
| 6 | Ninjalara karşı güçlü | %10 | Silah, kolye, kask, kalkan | **Evet** |
| 7 | Suralara karşı güçlü | %10 | Silah, kolye, kask, kalkan | **Evet** |
| 8 | Şamanlara karşı güçlü | %10 | Silah, kolye, kask, kalkan | **Evet** |
| 9 | Savaşçı saldırılarına direnç | %10 | Silah dışındaki 7 ekipman | **Evet** |
| 10 | Ninja saldırılarına direnç | %10 | Silah dışındaki 7 ekipman | **Evet** |
| 11 | Sura saldırılarına direnç | %10 | Silah dışındaki 7 ekipman | **Evet** |
| 12 | Şaman saldırılarına direnç | %10 | Silah dışındaki 7 ekipman | **Evet** |
| 13 | Canavarlara karşı güçlü | %20 | Silah, kolye, kask, kalkan | **Evet** |
| 14 | Düz savunma değeri | +30 | Gövde zırhı, bilezik, kolye, kask, küpe | Hayır |

**Bu listedeki 14 türün 13'ü kalkana açıktır.** Listedeki saldırı/direnç
türlerinin ekipmanlara dağıtılması önceki fork profilinden geliyor; hangilerinin
kapatılacağı veya yalnız belirli ekipmanda kalacağı henüz kararlaştırılmadı.

## Değer kademeleri

| Grup | Şu an seçilebilen değerler |
| --- | --- |
| Ortalama/beceri hasarı ve dirençleri | %2 / %4 / %6 / %8 / %10 |
| Dört sınıfa karşı güç ve dört sınıf direnci | %1 / %2 / %3 / %5 / %10 |
| Genel canavar gücü | %2 / %4 / %6 / %10 / %20 |
| Düz savunma | +5 / +10 / +15 / +20 / +30 |

## Kapsam

Bu liste normal **1–5 efsun havuzu** içindir. Nadir 6–7 havuzu ayrı tutuluyor.
Dolunay gibi silahların doğal ortalama/beceri çifti de `item_addon.cpp` ile
üretilen ayrı bir mekanizma; bu tablodaki rastgele normal efsun izinleriyle
birlikte değerlendirilmemeli.

Yarı insanlara karşı güçlü ile dört sınıfa özel güç ayrı efsunlardır.
Yarı insan ve hayvan/ork/mistik/ölümsüz/şeytan bonusları önceki 45 normal
satır içinde düzenlendi; yukarıdaki 14 karar bekleyen türe dahil değiller.

Mevcut oyuncu eşyalarına önceden yazılmış efsunlar ayrıca saklanır. Yeni
üretim havuzunun değiştirilmesi bu eski efsunları kendiliğinden kaldırmaz.

## Teknik kimlikler

| Efsun | DB kimliği |
| --- | --- |
| Ortalama zarar | `NORMAL_HIT_DAMAGE_BONUS` |
| Beceri hasarı | `SKILL_DAMAGE_BONUS` |
| Ortalama zarara direniş | `NORMAL_HIT_DEFEND_BONUS` |
| Beceri hasarına direniş | `SKILL_DEFEND_BONUS` |
| Savaşçılara karşı güçlü | `ATTBONUS_WARRIOR` |
| Ninjalara karşı güçlü | `ATTBONUS_ASSASSIN` |
| Suralara karşı güçlü | `ATTBONUS_SURA` |
| Şamanlara karşı güçlü | `ATTBONUS_SHAMAN` |
| Savaşçı direnci | `RESIST_WARRIOR` |
| Ninja direnci | `RESIST_ASSASSIN` |
| Sura direnci | `RESIST_SURA` |
| Şaman direnci | `RESIST_SHAMAN` |
| Genel canavar gücü | `ATTBONUS_MONSTER` |
| Düz savunma | `DEF_GRADE_BONUS` |

Kaynaklar: [önceki düzenlemenin kapsamı](EFSUN_NORMAL_DUZENLEME.md),
[güncel efsun rehberi](EFSUN_REHBERI.md),
[kaynak havuz](../content/server/sql/seed_item_attr.sql) ve canlı
`player.item_attr` salt okunur sorgusu.
