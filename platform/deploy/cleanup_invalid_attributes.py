#!/usr/bin/env python3
"""Inspect 11 approved items; operator mode clears only invalid normal bonuses."""
import argparse
import fcntl
import json
from pathlib import Path
import subprocess
import tempfile

ITEMS = {20000685: 299, 60000075: 19, 60000076: 3009, 60001096: 11490,
         60001206: 16200, 60001230: 19, 60001358: 11649, 60001359: 17109,
         60001360: 15089, 60001361: 13029, 60001362: 12509}
BLOCKED = {54, 71, 72, 73, 74, 59, 60, 61, 62, 78, 79, 80, 81, 63}
VM = ['ssh', '-o', 'BatchMode=yes', '-i', '/root/.ssh/metin2_vm', 'root@192.168.122.10']
FIELDS = [field + str(i) for i in range(5) for field in ('attrtype', 'attrvalue')]


def query(sql):
    return subprocess.check_output(VM + ['mariadb -B player'], input=sql, text=True)


def fetch():
    lines = query('SELECT * FROM item WHERE id IN (' + ','.join(map(str, ITEMS)) + ') ORDER BY id;\n').strip().splitlines()
    columns = lines[0].split('\t')
    rows = [dict(zip(columns, line.split('\t'))) for line in lines[1:]]
    assert len(rows) == len(ITEMS), 'An approved item was deleted; inspect before continuing'
    assert all(int(row['vnum']) == ITEMS[int(row['id'])] for row in rows), 'Item identity changed'
    return rows


def clean(row):
    pairs = [(int(row['attrtype' + str(i)]), int(row['attrvalue' + str(i)])) for i in range(5)]
    # The approved Full Moon Sword has a natural addon; keep its damage pair.
    def invalid(pair):
        return pair[0] in BLOCKED and not (int(row['vnum']) == 299 and pair[0] in (71, 72))
    removed = [pair for pair in pairs if invalid(pair)]
    if not removed:
        return dict(row), []
    kept = [pair for pair in pairs if pair[0] and not invalid(pair)]
    kept += [(0, 0)] * (5 - len(kept))
    after = dict(row)
    for i, (kind, value) in enumerate(kept):
        after['attrtype' + str(i)] = str(kind)
        after['attrvalue' + str(i)] = str(value)
    return after, removed


def update(row, previous=None):
    assignment = ','.join(field + '=' + row[field] for field in FIELDS)
    where = 'id=' + row['id'] + ' AND vnum=' + row['vnum'] + ' AND owner_id=' + row['owner_id']
    if previous:
        where += ' AND ' + ' AND '.join(field + '=' + previous[field] for field in FIELDS)
    return 'UPDATE item SET ' + assignment + ' WHERE ' + where + ';\n'


def control(action):
    subprocess.run(VM[:1] + ['-n'] + VM[1:] +
                   ['sh /usr/home/cleanup_invalid_attributes_vm.sh ' + action], check=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--apply', action='store_true', help='Operator maintenance: stop/save, clean, restart')
    args = parser.parse_args()
    if not args.apply:
        for row in fetch():
            _, removed = clean(row)
            print(json.dumps({'id': row['id'], 'vnum': row['vnum'], 'remove': removed}))
        return
    with open('/home/m2web/dev/client-build.lock', 'w') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        control('health')
        control('ready')
        backup = Path(tempfile.mkdtemp(prefix='item-attribute-cleanup-', dir='/home/m2web/backups'))
        stopped = False
        rollback = None
        changed = False
        succeeded = False
        try:
            # All game and DB-cache processes must exit after saving their data.
            stopped = True
            control('stop')
            control('stopped')
            before = fetch()
            expected, changes, report = [], [], []
            for row in before:
                after, removed = clean(row)
                expected.append(after)
                if removed:
                    changes.append((row, after))
                    report.append({'id': row['id'], 'vnum': row['vnum'], 'removed': removed})
            (backup / 'before.json').write_text(json.dumps(before, indent=2))
            (backup / 'plan.json').write_text(json.dumps(report, indent=2))
            rollback = 'USE player;\nSTART TRANSACTION;\n' + ''.join(update(row) for row, _ in changes) + 'COMMIT;\n'
            (backup / 'rollback.sql').write_text(rollback)
            sql = 'USE player;\nCREATE TEMPORARY TABLE item_cleanup_guard (valid tinyint CHECK (valid=1));\nSTART TRANSACTION;\n'
            for old, new in changes:
                sql += update(new, old) + 'INSERT INTO item_cleanup_guard SELECT ROW_COUNT()=1;\n'
            sql += 'COMMIT;\n'
            (backup / 'apply.sql').write_text(sql)
            changed = True
            query(sql)
            assert fetch() == expected, 'Unexpected item field changes'
            control('quest-install')
            (backup / 'after.json').write_text(json.dumps(expected, indent=2))
            print('CLEANED:', len(changes), 'items;', sum(len(row['removed']) for row in report), 'invalid normal bonus slots')
            print('BACKUP:', backup)
            succeeded = True
        except Exception:
            if changed and rollback:
                query(rollback)
                print('RESTORED original attributes:', backup)
            control('quest-rollback')
            raise
        finally:
            if stopped:
                control('start')
        if succeeded:
            control('quest-commit')


if __name__ == '__main__':
    main()
