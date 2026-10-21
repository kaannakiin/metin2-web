#!/usr/bin/env python3
"""Render the approved NPC stock, scoped DB migration, or metin-only exclusions."""
import argparse
import json
import re
from pathlib import Path
import drop_catalogue as catalogue

ROOT = Path(__file__).resolve().parents[2]
LOCALE = ROOT / 'runtime/freebsd/share/locale/europe'
WEAPONS_30 = [299, 1179, 2159, 3219, 5119, 7169]
BASES_30 = [v - 9 for v in WEAPONS_30]
OWNED_SHOPS = (101, 102, 103, 111, 112, 113, 201, 202, 203, 211, 212, 213, 301)
P = catalogue.proto('item')


def entries(ids, minimum, count=1):
    rows = []
    for vnum in ids:
        proto = P[vnum]
        if count > 1 and 'ITEM_STACKABLE' not in proto['Flags']:
            raise ValueError('Nonstackable package: %s' % vnum)
        resale = int(proto['ShopBuyPrice']) * count
        # Existing NPC resale uses ShopBuyPrice without a divisor. Every new
        # shop must cost more than resale, including randomly rolled weapons.
        price = max(minimum, resale * (2 if proto['Type'] in ('ITEM_WEAPON', 'ITEM_ARMOR') else 125) //
                    (1 if proto['Type'] in ('ITEM_WEAPON', 'ITEM_ARMOR') else 100))
        rows.append((vnum, count, price))
    return rows


def stock():
    weapons = entries([19, 1009, 2009, 3009, 7009], 10000)
    weapons += entries([49, 4019, 2039, 3039, 5019, 7039], 25000)
    weapons += entries(WEAPONS_30, 500000)
    weapons += entries([8000], 1000, 200)
    bodies = []
    for offset, price in [(9, 25000), (49, 250000), (69, 750000)]:
        bodies += entries([base + offset for base in [11200, 11400, 11600, 11800]], price)
    defensive = entries([12229, 12369, 12509, 12649, 13029], 75000)
    jewels = entries([14009, 14089, 16009, 16089, 17009, 17109, 15009, 15089], 25000)
    market = entries([27001, 27002, 27004, 27005], 1000, 50)
    market += entries([27003, 27006], 10000, 200)
    market += entries([72725, 72729], 100000)
    market += entries([27102, 27105], 50000, 50)
    market += entries([22000, 22010], 10000, 10)
    market += entries([50200, 70038], 10000)
    market += entries([40004, 27989], 50000)
    market += entries([50053], 10000)
    tabs = []
    for npc, base in [(9001, 100), (9007, 110)]:
        tabs += [(npc, base + 1, 'Silahlar', weapons)]
    for npc, base in [(9002, 200), (9008, 210)]:
        tabs += [(npc, base + 1, 'Zirhlar', bodies + defensive + jewels)]
    tabs += [(9003, 301, 'Market', market)]
    for npc, shop, name, rows in tabs:
        # ShopEx's 5x9 grid writes into a 40-entry packet. Keep every placed
        # cell inside the safe first 40 cells, not just the total item count.
        grid = [False] * 40
        for vnum, count, price in sorted(rows):
            height = int(P[vnum]['Size'])
            positions = [[pos + 5 * y for y in range(height)] for pos in range(40)]
            cells = next((cells for cells in positions if cells[-1] < 40 and
                          all(not grid[cell] for cell in cells)), None)
            if not cells:
                raise ValueError('Shop does not fit: %s' % shop)
            for cell in cells:
                grid[cell] = True
            if price <= int(P[vnum]['ShopBuyPrice']) * count:
                raise ValueError('Shop resale loop: %s' % vnum)
    return tabs


def drops():
    text = (LOCALE / 'mob_drop_item.txt').read_text()
    mobs = catalogue.proto('mob')
    removed = []
    pattern = re.compile(r'(?ms)^Group\s+([^\n]+)\n\{\n.*?^\}')

    def group(match):
        block = match.group(0)
        mob = re.search(r'^\s*Mob\s+(\d+)', block, re.M)
        if not mob or mobs.get(int(mob.group(1)), {}).get('Type') != 'STONE':
            return block
        lines = []
        for line in block.splitlines():
            row = re.match(r'^\s*\d+\s+(\d+)\s+\d+\s+[\d.]+', line)
            if row and any(base <= int(row.group(1)) <= base + 9 for base in BASES_30):
                removed.append((int(mob.group(1)), int(row.group(1))))
                continue
            lines.append(line)
        return '\n'.join(lines)

    result = pattern.sub(group, text)
    return result


def sql():
    return '''-- Active ENABLE_RENEWAL_SHOPEX reads shopex/shopex_item, not a text file.
USE player;
START TRANSACTION;
DELETE FROM shop_item WHERE shop_vnum IN (1,2,3,6,7);
DELETE FROM shop WHERE vnum IN (1,2,3,6,7);
''' + shop_inserts() + '''
REPLACE INTO quest (dwPID,szName,szState,lValue) VALUES
(0,'mob_gold','',400),(0,'mob_gold_buyer','',400);
COMMIT;
'''


def shop_inserts():
    tabs = stock()
    # Retired tabs are owned too: remove them so they cannot remain visible.
    ids = ','.join(map(str, OWNED_SHOPS))
    lines = ['DELETE FROM shopex_item WHERE shop_vnum IN (%s);' % ids,
             'DELETE FROM shopex WHERE vnum IN (%s);' % ids,
             'INSERT INTO shopex (vnum,name,npc_vnum) VALUES']
    lines.append(',\n'.join("(%d,'%s',%d)" % (shop, name, npc)
                            for npc, shop, name, rows in tabs) + ';')
    lines.append('INSERT INTO shopex_item (shop_vnum,item_vnum,`count`,price,price_vnum,price_type) VALUES')
    lines.append(',\n'.join("(%d,%d,%d,%d,0,'GOLD')" % (shop, vnum, count, price)
                            for npc, shop, name, rows in tabs for vnum, count, price in rows) + ';')
    return '\n'.join(lines) + '\n'


def repair_sql():
    return ('-- Correct the active renewed shop backend; unrelated shops and Yang unchanged.\n'
            'USE player;\nSTART TRANSACTION;\n' + shop_inserts() + 'COMMIT;\n')


def snapshot():
    tabs = sorted(stock(), key=lambda tab: tab[1])
    rows = [['S', shop, name, npc] for npc, shop, name, items in tabs]
    rows += [['I', shop, vnum, count, price, 0, 1] + [0] * 17
             for npc, shop, name, items in tabs
             for vnum, count, price in sorted(items)]
    return '\n'.join('\t'.join(map(str, row)) for row in rows) + '\n'


def snapshot_sql():
    ids = ','.join(map(str, OWNED_SHOPS))
    attrs = ','.join('attrtype%d,attrvalue%d' % (i, i) for i in range(7))
    return (
        "SELECT 'S',vnum,name,npc_vnum FROM shopex WHERE vnum IN (%s) ORDER BY vnum;\n"
        "SELECT 'I',shop_vnum,item_vnum,`count`,price,price_vnum,price_type+0,"
        "socket0,socket1,socket2,%s FROM shopex_item WHERE shop_vnum IN (%s) "
        "ORDER BY shop_vnum,item_vnum;\n"
        "SELECT 'CONFLICT',vnum,npc_vnum FROM shop WHERE npc_vnum IN (9001,9002,9003,9007,9008);\n"
    ) % (ids, attrs, ids)


def policy():
    data = json.loads((ROOT / 'platform/gameplay/phase3_loot.json').read_text())
    data['version'] = max(data['version'], 5)
    data['npc_30_weapons'] = BASES_30
    data['metin_excluded_weapons'] = sorted(set(data['metin_excluded_weapons'] + BASES_30))
    return json.dumps(data, ensure_ascii=False, indent=2) + '\n'


def report():
    names = catalogue.read_names('item', 'tr')
    lines = ['# NPC stokları — uygulanan orta-kolay profil', '',
             'Silahçı 9001 ve 9007 aynı seçki; zırhçı 9002 ve 9008 aynı seçki.',
             'Her NPC tek sayfa açar; Market 9003 ayrı kalır.',
             'Silahlar 1/15/30; gövde zırhları 1/34/48 +9. Başlangıç proto sınırı 0’dır.',
             'Azaltılmış kask/kalkan/takılar zırhlarla aynı sayfadadır.',
             'Fiyatlar paket toplamıdır; standart geri satıştan yüksektir.', '',
             '30 seviye altı klasik silah ailesi yalnız +9 stoklanır. Ortalama/beceri',
             'zararı mevcut doğal üretim kuralından gelir; sabit yüksek ortalama basılmaz.',
             'Aynı ailelerin +0…+9 sürümleri metin drop gruplarından kaldırıldı.',
             'Üst silah/zırh/takılar ve zindan giriş malzemeleri farmda kaldı.', '']
    for npc, shop, name, rows in stock():
        if npc in (9007, 9008):
            continue
        lines += ['## %s — NPC %d / shop %d' % (name, npc, shop), '',
                  '| Ürün | VNUM | Seviye | Adet | Yang |', '| --- | --- | --- | --- | --- |']
        for vnum, count, price in rows:
            level = P[vnum]['LimitValue0'] if P[vnum]['LimitType0'] == 'LEVEL' else '—'
            lines.append('| %s | %d | %s | %d | %s |' %
                         (names.get(vnum, 'VNUM %d' % vnum), vnum, level, count,
                          format(price, ',').replace(',', '.')))
        lines.append('')
    lines += ['## Destek, at ve Yang', '',
              '- Ana beceriler BK → G → P. Standart/at becerileri 5. seviyeye ulaşınca',
              '  doğrudan tamamlanır; sınıf sıfırlamasından sonra en geç beş saniyede yenilenir.',
              '- Kalıcı seviye 30 askeri at ve bir çağırma kitabı (50053). Süreli',
              '  bineğin yedi günlük süresi değiştirilmez. Kitap kaybolursa markette yedeği var.',
              '- Yang, onaylı 17 haritada yaratık/metin türüne göre hesaplanır;',
              '  aralıklar `PVP_HEDEF.md` Harita bazlı Yang bölümündedir.',
              '  Global miktar flagleri 400; düşüş ihtimali, seviye cezası ve 400.000 tavanı korunur.',
              '- Kutsama/efsun, BK/Ruh Taşı ve zindan anahtarları bu markete eklenmedi.', '',
              'Kaynak: `npc_profile.py` → `shopex` / `shopex_item` SQL tabloları;',
              'standart beceri/at teslimi: `starter_support.lua`.', '']
    return '\n'.join(lines)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('target', choices=['drops', 'sql', 'repair_sql', 'snapshot', 'snapshot_sql', 'policy', 'report'])
    args = parser.parse_args()
    print(globals()[args.target](), end='')
