#!/usr/bin/env python3
"""Validate the approved independent Metin regen additions without changing data."""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MARKER = '// Mid-easy Metin density x2: independent regen records for RESP tracking.'


def records(text):
    result = []
    for line in text.splitlines():
        if not line.strip() or line.lstrip().startswith(('//', '#')):
            continue
        row = tuple(line.split())
        if len(row) != 11:
            raise ValueError('Regen row must have exactly 11 fields')
        result.append(row)
    return result


def is_metin(row):
    return row[0] == 'm' and 8001 <= int(row[10]) <= 8027


def validate(spec, data):
    text = data.decode('utf-8')
    lines = text.splitlines(keepends=True)
    markers = [i for i, line in enumerate(lines) if line.rstrip('\r\n') == MARKER]
    if len(markers) != 1:
        raise ValueError('Expected one density block')
    start = markers[0]
    if start == 0 or lines[start - 1].strip():
        raise ValueError('Missing separator before density block')
    end = start + 1 + spec['added_records']
    added = records(''.join(lines[start + 1:end]))
    baseline = ''.join(lines[:start - 1] + lines[end:]).encode('utf-8')
    if hashlib.sha256(baseline).hexdigest() != spec['baseline_sha256']:
        raise ValueError('Original map data or respawn timing changed')
    before = records(baseline.decode('utf-8'))
    stones = [row for row in before if is_metin(row)]
    if Counter(added) != Counter(stones):
        raise ValueError('Each existing Metin area must get exactly one independent copy')
    if any(row[9] != '1' or int(row[3]) <= 0 or int(row[4]) <= 0 for row in added):
        raise ValueError('Each independent record needs one stone and a nonzero spawn area')
    after = records(text)
    old_capacity = sum(int(row[9]) for row in stones)
    new_capacity = sum(int(row[9]) for row in after if is_metin(row))
    if old_capacity != spec['base_capacity'] or new_capacity != 2 * old_capacity:
        raise ValueError('Capacity is not exactly twice the approved baseline')
    if Counter(row for row in before if not is_metin(row)) != Counter(row for row in after if not is_metin(row)):
        raise ValueError('Non-Metin regen records changed')
    return {'path': spec['path'], 'before': old_capacity, 'after': new_capacity,
            'added_records': len(added), 'baseline_sha256': spec['baseline_sha256'],
            'sha256': hashlib.sha256(data).hexdigest()}


def check(root=ROOT):
    policy = json.loads((root / 'platform/gameplay/metin_density.json').read_text())
    rows = [validate(spec, (root / 'runtime/freebsd/share/locale/europe' / spec['path']).read_bytes())
            for spec in policy['maps']]
    return {'maps': rows, 'before': sum(row['before'] for row in rows),
            'after': sum(row['after'] for row in rows), 'base_release': policy['base_release']}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    report = check()
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(report, indent=2) + '\n')
    print('METIN DENSITY: %d maps, %d -> %d independent spawn capacity; timing and non-Metin rows preserved' %
          (len(report['maps']), report['before'], report['after']))
