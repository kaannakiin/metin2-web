#!/usr/bin/env python3
"""Test a 14-row attribute migration, back up its masks, apply and verify it."""
import argparse
import copy
import json
from pathlib import Path
import re
import subprocess
import tempfile

VM = ['ssh', '-o', 'BatchMode=yes', '-i', '/root/.ssh/metin2_vm',
      'root@192.168.122.10', 'mariadb -B player']
MASKS = ['weapon', 'body', 'wrist', 'foots', 'neck', 'head', 'shield', 'ear',
         'pendant', 'costume_body', 'costume_hair', 'costume_weapon']


def query(sql):
    return subprocess.check_output(VM, input=sql, text=True)


def table(name):
    assert name in ('item_attr', 'item_attr_rare')
    lines = query('SELECT * FROM ' + name + ';\n').strip().splitlines()
    fields = lines[0].split('\t')
    return {row['apply']: row for row in
            (dict(zip(fields, line.split('\t'))) for line in lines[1:])}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--apply', action='store_true')
    args = parser.parse_args()
    path = Path(__file__).with_name('20261022_classic_attribute_permissions.sql')
    sql = path.read_text()
    ids = re.findall(r"\('([A-Z_]+)'\)", sql)
    assert len(ids) == len(set(ids)) == 14
    before, rare = table('item_attr'), table('item_attr_rare')
    assert len(before) == 59 and set(ids) <= before.keys()
    expected = copy.deepcopy(before)
    for name in ids:
        for field in MASKS:
            expected[name][field] = '0'

    # Exercise the exact migration against a connection-local copy first.
    sandbox = re.sub(r'\bitem_attr\b', 'attribute_sandbox', sql)
    result = query('CREATE TEMPORARY TABLE attribute_sandbox LIKE item_attr;\n'
                   'INSERT INTO attribute_sandbox SELECT * FROM item_attr;\n' +
                   sandbox + '\nSELECT * FROM attribute_sandbox;\n')
    lines = result.strip().splitlines()
    fields = lines[0].split('\t')
    tested = {row['apply']: row for row in
              (dict(zip(fields, line.split('\t'))) for line in lines[1:])}
    assert tested == expected, 'Sandbox migration changed unexpected data'
    print('SANDBOX PASS: only 14 rows / 12 permission masks changed')
    if not args.apply:
        return
    backup = Path(tempfile.mkdtemp(prefix='classic-attributes-', dir='/home/m2web/backups'))
    (backup / 'before.json').write_text(json.dumps(before, indent=2))
    (backup / 'rare.json').write_text(json.dumps(rare, indent=2))
    rollback = 'USE player;\n' + '\n'.join(
        'UPDATE item_attr SET ' + ','.join(field + '=' + before[name][field] for field in MASKS)
        + " WHERE `apply`='" + name + "';" for name in ids) + '\n'
    (backup / 'rollback.sql').write_text(rollback)
    assert table('item_attr') == before, 'Concurrent normal attribute change'
    assert table('item_attr_rare') == rare, 'Concurrent rare attribute change'
    try:
        query(sql)
        assert table('item_attr') == expected, 'Live migration mismatch'
        assert table('item_attr_rare') == rare, 'Rare pool changed'
    except Exception:
        query(rollback)
        print('ROLLED BACK permission masks; backup:', backup)
        raise
    (backup / 'after.json').write_text(json.dumps(expected, indent=2))
    print('LIVE DB VERIFIED: 14 masks closed; other 45 rows, values, weights and rare pool unchanged')
    print('BACKUP:', backup)
    print('GAME CORES MUST RELOAD: GM /reload p (or the operator maintenance restart)')


if __name__ == '__main__':
    main()
