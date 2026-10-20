#!/usr/bin/env python3
"""Render all current normal/rare attribute pools from the verified SQL seed."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SETS = ['weapon', 'body', 'wrist', 'foots', 'neck', 'head', 'shield', 'ear',
        'pendant', 'costume_body', 'costume_hair', 'costume_weapon']
TITLES = ['Silah', 'Gövde', 'Bilezik', 'Ayakkabı', 'Kolye', 'Kask', 'Kalkan',
          'Küpe', 'Tılsım', 'Kostüm', 'Saç', 'Silah kostümü']
LABELS = {
    'MAX_HP': 'Maks. HP', 'MAX_SP': 'Maks. SP', 'CON': 'Canlılık',
    'INT': 'Zekâ', 'STR': 'Güç', 'DEX': 'Çeviklik', 'ATT_SPEED': 'Saldırı hızı %',
    'MOV_SPEED': 'Hareket hızı %', 'CAST_SPEED': 'Büyü hızı %',
    'HP_REGEN': 'HP yenileme %', 'SP_REGEN': 'SP yenileme %',
    'POISON_PCT': 'Zehirleme %', 'STUN_PCT': 'Sersemletme %', 'SLOW_PCT': 'Yavaşlatma %',
    'CRITICAL_PCT': 'Kritik %', 'PENETRATE_PCT': 'Delici %',
    'ATTBONUS_HUMAN': 'Yarı insanlara karşı %', 'ATTBONUS_ANIMAL': 'Hayvanlara karşı %',
    'ATTBONUS_ORC': 'Orklara karşı %', 'ATTBONUS_MILGYO': 'Mistiklere karşı %',
    'ATTBONUS_UNDEAD': 'Ölümsüzlere karşı %', 'ATTBONUS_DEVIL': 'Şeytanlara karşı %',
    'STEAL_HP': 'HP emme %', 'STEAL_SP': 'SP emme %', 'MANA_BURN_PCT': 'SP çalma %',
    'BLOCK': 'Yakın dövüş bloklama %', 'DODGE': 'Oklardan korunma %',
    'RESIST_SWORD': 'Kılıç savunması %', 'RESIST_TWOHAND': 'Çift el savunması %',
    'RESIST_DAGGER': 'Bıçak savunması %', 'RESIST_BELL': 'Çan savunması %',
    'RESIST_FAN': 'Yelpaze savunması %', 'RESIST_BOW': 'Ok savunması %',
    'RESIST_FIRE': 'Ateş direnci %', 'RESIST_ELEC': 'Şimşek direnci %',
    'RESIST_MAGIC': 'Büyü direnci %', 'RESIST_WIND': 'Rüzgâr direnci %',
    'REFLECT_MELEE': 'Yakın dövüş yansıtma %', 'POISON_REDUCE': 'Zehir direnci %',
    'EXP_DOUBLE_BONUS': 'EXP bonusu %', 'GOLD_DOUBLE_BONUS': 'Yang çift düşme şansı %',
    'ITEM_DROP_BONUS': 'Eşya düşürme bonusu %', 'IMMUNE_STUN': 'Sersemliğe bağışıklık',
    'IMMUNE_SLOW': 'Yavaşlığa bağışıklık', 'ATT_GRADE_BONUS': 'Saldırı değeri',
    'DEF_GRADE_BONUS': 'Savunma değeri', 'SKILL_DAMAGE_BONUS': 'Beceri hasarı %',
    'NORMAL_HIT_DAMAGE_BONUS': 'Ortalama zarar %', 'SKILL_DEFEND_BONUS': 'Beceri direnci %',
    'NORMAL_HIT_DEFEND_BONUS': 'Ortalama zarar direnci %',
    'ATTBONUS_WARRIOR': 'Savaşçıya karşı %', 'ATTBONUS_ASSASSIN': 'Ninjaya karşı %',
    'ATTBONUS_SURA': 'Suraya karşı %', 'ATTBONUS_SHAMAN': 'Şamana karşı %',
    'RESIST_WARRIOR': 'Savaşçı direnci %', 'RESIST_ASSASSIN': 'Ninja direnci %',
    'RESIST_SURA': 'Sura direnci %', 'RESIST_SHAMAN': 'Şaman direnci %',
    'ATTBONUS_MONSTER': 'Canavarlara karşı %',
}


def pools():
    text = (ROOT / 'content/server/sql/seed_item_attr.sql').read_text()
    parts = text.split('INSERT INTO `item_attr_rare`', 1)
    result = []
    for part in parts:
        rows = []
        for match in re.finditer(r"\('([^']+)',\s*([^;]+?)\)(?:,|;)", part):
            numbers = [int(value.strip()) for value in match.group(2).split(',')]
            rows.append(dict(apply=match.group(1), weight=numbers[0], values=numbers[1:6],
                             caps=dict(zip(SETS, numbers[6:]))))
        result.append(rows)
    return result


def matrix(rows, sets):
    output = ['| Efsun | 5 değer kademesi | ' + ' | '.join(TITLES[SETS.index(s)] for s in sets) + ' |',
              '| --- | --- | ' + ' | '.join('---' for s in sets) + ' |']
    for row in rows:
        if not any(row['caps'].get(s, 0) and row['weight'] for s in sets):
            continue
        cells = []
        for s in sets:
            cap = row['caps'].get(s, 0)
            cells.append(str(row['values'][min(cap, 5) - 1]) if cap and row['weight'] else '—')
        output.append('| %s | %s | %s |' % (LABELS.get(row['apply'], row['apply']),
                      ' / '.join(map(str, row['values'])), ' | '.join(cells)))
    return '\n'.join(output)


def render():
    normal, rare = pools()
    lines = ['# Efsunlanabilen eşyalar ve bütün mevcut efsun havuzları', '',
             '20 Ekim 2026. Bu belge **bizim dosyaların gerçek durumudur**; klasik',
             'Metin2 ile aynı olduğu iddia edilmez. Normal tablonun 59 satırı canlı DB',
             'ile bütün değer/yuva izinleri üzerinden eşleşti. 6–7 tablosunda 39 satır var.', '',
             '## Hangi eşyalar efsunlanabiliyor?', '',
             '| Eşya grubu | Sistem | Açıklama |', '| --- | --- | --- |',
             '| Kılıç, çift el, hançer, yay, çan, yelpaze | Normal 1–5 | Aynı silah havuzu; sabit proto bonusları tekrar gelmez |',
             '| Gövde, kask, kalkan | Normal 1–5 | Her yuvanın izinleri ayrı |',
             '| Bilezik, kolye, küpe, ayakkabı | Normal 1–5 | Her yuvanın izinleri ayrı |',
             '| Tılsım | Ayrı normal havuz | Kod desteği açık; 1–99 içerikte her tılsım erişilebilir değildir |',
             '| Gövde kostümü, saç, silah kostümü | Kostüm efsunu | Ayrı DB sütunları ve özel efsun araçları |',
             '| Ok | Normal havuz yok | Mühimmat |',
             '| Kemer, yüzük türü, kuşak, aura, binek/pet eşyası, olta/kazma | Normal 1–5 havuzu yok | Kendi proto, emiş veya sistem özellikleri olabilir |',
             '| Simya taşları | Ayrı sistem | Ejderha taşı tablosu/arıtma; normal 1–5 tablosu değildir |', '',
             'GM komutuyla zorla bonus basılabilmesi normal oyuncu efsunlama izni sayılmaz.',
             'Kuşağa emilen silah özellikleri ve sokete takılan taşlar da normal efsunla',
             'karıştırılmamalı. Tek tek eşyada efsun aracının ilave tür/seviye koşulları olabilir.', '',
             '## Dolunay neden “Metinlere karşı güçlü” gösteriyordu?', '',
             '- Sunucu APPLY 119 = `ATTBONUS_MEDI_PVM`: yalnız NPC hedeflerinde çalışan',
             '  PvM ortalama zararı. Metinlere özel bir bonus değildir.',
             '- Eski istemci APPLY 119 = `ATTBONUS_STONE`: aynı sayı farklı isimle çiziliyordu.',
             '- Asıl metin bonusu sunucuda 112; eski istemcide 119 idi. 92 sonrası',
             '  başka bonuslar da kaymıştı. İstemci kimlikleri sunucuyla hizalandı;',
             '  paket biçimi/feature flag değiştirilmedi, oyuncu bonusları DB’den silinmedi.',
             '- Sunucudaki `ENABLE_AVG_PVM_DISABLE` yolu, ortalamalı silahların doğal',
             '  ortalamasını 72 yerine 119 ile üretiyor. Yani görüntü hatası dışında',
             '  **klasik ortalama yerine PvM ortalama kullanan özel bir kural da var.**',
             '  Bu yayında saldırı formülü veya mevcut item değerleri topluca değiştirilmedi.', '',
             '[Resmî Dolunay sayfası](https://tr-wiki.metin2.gameforge.com/index.php?redirect=no&stable=0&title=Dolunay_K%C4%B1l%C4%B1c%C4%B1)',
             'doğal ortalama/beceri çiftini açıklıyor. Güncel resmî oyunda',
             '[Metin Taşı Karşısında Güçlü](https://tr-wiki.metin2.gameforge.com/index.php/Metin_Ta%C5%9F%C4%B1_Kar%C5%9F%C4%B1s%C4%B1nda_G%C3%BC%C3%A7l%C3%BC)',
             'ayrı sistemlerde ve 6–7 efsunlarda bulunabiliyor; Dolunay’ın klasik',
             'normal 1–5 havuzunda rastgele aynı şekilde bulunmasıyla eşdeğer değil.', '',
             '## Tablo nasıl okunur?', '',
             'Sayı: o eşya grubuna tablodan gelebilen **en yüksek değer**. “—”: bu',
             'havuzdan gelemez. Soldaki beş değer, düşükten yükseğe efsun kademeleri;',
             'bazı yuvalar üçüncü/dördüncü kademede sınırlandığı için daha düşük kalır.',
             'Bağışıklıkta 1, özelliğin açık olmasıdır. Bir eşyanın protosunda zaten',
             'bulunan veya mevcut normal efsunlarında bulunan aynı tür tekrar seçilmez.',
             'Tablo bir eşyaya hepsinin birlikte gelebileceği anlamına gelmez: normal',
             'slot toplamı 5. Doğal ortalama/beceri çifti de bu slotları kullanır.',
             'Efsun seçim ağırlığı gerçek yüzde değildir; eldeki diğer efsunlar havuzu değiştirir.', '',
             '## Normal 1–5: bütün ekipman yuvaları', '', matrix(normal, SETS[:9]), '',
             '## Kostüm havuzları', '', matrix(normal, SETS[9:]), '',
             'Kostümde kod desteği ve DB izinleri mevcut. “Kostüm güç vermez” tasarım',
             'hedefiyle bu gerçek izinler aynı şey değildir; erişilebilir kostüm araçları',
             'ayrı kontrol edilmeden bu sütunlar yokmuş gibi kabul edilmemeli.', '',
             '## Klasik düzenden sapan ve ayrıca karar gerekenler', '',
             '- Normal havuzda beceri hasarı ve ortalama zarar çoğu yuvaya açılmış.',
             '  Bu yüzden doğal ortalamalı silahlar dışında da bu türler seçilebilir.',
             '- Birçok tür neredeyse bütün ekipman yuvalarında serbest: HP, stat,',
             '  hız, yarı insan ve yaratık bonusları gibi. Klasik yuva sınırları değil.',
             '- Sınıfa karşı saldırı ve sınıf direnci normal 1–5 havuzunda bulunuyor.',
             '  Klasik düzenle karşılaştırılması gereken ayrı bir PvP güç katmanı.',
             '- Metin/boss bonusu normal DB havuzunda yok. Dolunay’daki metin yazısı',
             '  yukarıdaki kimlik uyuşmazlığı; böyle bir normal satırın kanıtı değil.',
             '- Seed içinde birçok satır `approx` olarak işaretli. Canlıyla eşleşmesi',
             '  bu kuralların klasik wikiye uygun olduğu anlamına gelmez.', '',
             'Bu inceleme sırasında oyuncu efsunları ve normal/rare izin tablosu topluca',
             'silinmedi veya değişmedi. Klasik havuza geçiş, mevcut eşyalara ne olacağı',
             'ile birlikte ayrı bir dengeleme kararı gerektiriyor.', '',
             '## 6–7 efsun: yapılandırılmış havuz', '',
             'Tasarım hedefinde kapalı. Kod/DB tablosunun varlığı tek başına normal',
             'oyuncuya erişim verildiğini göstermez; GM/özel araç yolları ayrıdır.',
             'Aşağıdaki 39 satır normal 1–5 tablosuna karıştırılmamalı.', '',
             matrix(rare, SETS[:9]), '',
             '## Teknik dayanak', '',
             '`seed_item_attr.sql`; `CItem::GetAttributeSetIndex`, `HasAttr`,',
             '`PutAttributeWithLevel`, `ChangeAttribute`; `item_addon.cpp`;',
             'sunucu `length.h` ve istemci `GameLib/ItemData.h`. Canlı normal',
             'tablo TSV SHA256: `dfe1f1ac3eae6233fb1d3c0b8311d742de33804fde07e5a7bd12f33d38fdbf3c`.',
             'Üretim: `python3 platform/tools/attribute_catalogue.py`.', '']
    return '\n'.join(lines)


if __name__ == '__main__':
    print(render(), end='')
