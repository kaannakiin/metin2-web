#!/usr/bin/env python3
"""Render only the approved classic metin Magic Metal additions to stdout."""
import json
import re
import drop_catalogue as catalogue


def render():
    policy = json.loads(catalogue.POLICY_PATH.read_text())['metin_magic_metal']
    mobs, items = catalogue.proto('mob'), catalogue.proto('item')
    vnum, count = policy['vnum'], policy['count']
    if vnum not in items or count < 1:
        raise ValueError('Invalid Magic Metal item/count')
    levels = {}
    for band in policy['bands']:
        for level in range(band['min'], band['max'] + 1):
            if level in levels or not 0 < band['pct'] <= 100:
                raise ValueError('Invalid or overlapping Magic Metal bands')
            levels[level] = band['pct'] * 4
    source = (catalogue.LOCALE / 'mob_drop_item.txt').read_text()

    def group(match):
        block = match.group(0)
        name = re.match(r'Group\s+MetinLv(\d+)_(\d+)', block)
        if not name:
            return block
        level, mob_id = map(int, name.groups())
        mob = mobs.get(mob_id, {})
        body_mob = re.search(r'^\s*Mob\s+(\d+)\s*$', block, re.M)
        if (mob.get('Type') != 'STONE' or int(mob['Level']) != level
                or not body_mob or int(body_mob[1]) != mob_id):
            raise ValueError('Metin group/proto mismatch: ' + name[0])
        lines = []
        for line in block.splitlines():
            row = re.match(r'^\s*\d+\s+(\d+)\s+\d+\s+[\d.]+\s*$', line)
            if not row or int(row[1]) != vnum:
                lines.append(line)
        if level in levels:
            indices = [int(row[1]) for line in lines
                       if (row := re.match(r'^\s*(\d+)\s+\d+\s+\d+\s+[\d.]+\s*$', line))]
            index = max(indices, default=0) + 1
            lines.insert(-1, '\t%d\t%d\t%d\t%d' % (index, vnum, count, levels[level]))
        return '\n'.join(lines)

    return re.sub(r'(?ms)^Group\s+[^\n]+\n\{\n.*?^\}', group, source)


if __name__ == '__main__':
    print(render(), end='')
