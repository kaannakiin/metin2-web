#!/usr/bin/env python3
"""Validate the approved independent Metin regen additions without changing data."""
import argparse
from collections import Counter
import hashlib
import json
import math
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]
MARKER = '// Mid-easy Metin density x4: independent regen records for RESP tracking.'


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
    original_lines = lines[:start - 1] + lines[end:]
    baseline_times = iter(spec['baseline_respawn'])
    timed_stones = []
    for i, line in enumerate(original_lines):
        parsed = records(line)
        if not parsed or not is_metin(parsed[0]):
            continue
        row = parsed[0]
        original_time = next(baseline_times)
        if not re.fullmatch(r'[0-9]+s', original_time):
            raise ValueError('Baseline respawn must be explicit seconds')
        expected = str(math.ceil(int(original_time[:-1]) / 2)) + 's'
        if row[7] != expected:
            raise ValueError('Metin respawn is not half the approved baseline')
        timed_stones.append(row)
        original_lines[i] = re.sub(r'^(\s*(?:\S+\s+){7})\S+',
                                   lambda match: match[1] + original_time, line, count=1)
    if next(baseline_times, None) is not None:
        raise ValueError('Unused baseline respawn entries')
    baseline = ''.join(original_lines).encode('utf-8')
    if hashlib.sha256(baseline).hexdigest() != spec['baseline_sha256']:
        raise ValueError('Original map data changed beyond approved respawn timing')
    before = records(baseline.decode('utf-8'))
    stones = [row for row in before if is_metin(row)]
    if Counter(added) != Counter(timed_stones * 3):
        raise ValueError('Each existing Metin area must get three independent copies')
    if any(row[9] != '1' or int(row[3]) <= 0 or int(row[4]) <= 0 for row in added):
        raise ValueError('Each independent record needs one stone and a nonzero spawn area')
    after = records(text)
    old_capacity = sum(int(row[9]) for row in stones)
    new_capacity = sum(int(row[9]) for row in after if is_metin(row))
    if old_capacity != spec['base_capacity'] or new_capacity != 4 * old_capacity:
        raise ValueError('Capacity is not exactly four times the approved baseline')
    if Counter(row for row in before if not is_metin(row)) != Counter(row for row in after if not is_metin(row)):
        raise ValueError('Non-Metin regen records changed')
    return {'path': spec['path'], 'before': old_capacity, 'after': new_capacity,
            'added_records': len(added), 'baseline_sha256': spec['baseline_sha256'],
            'sha256': hashlib.sha256(data).hexdigest()}


def check(root=ROOT):
    policy = json.loads((root / 'platform/gameplay/metin_density.json').read_text())
    if policy['version'] != 2 or policy['multiplier'] != 4 or policy['respawn_multiplier'] != 0.5:
        raise ValueError('Expected approved x4 capacity and half respawn policy')
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
    print('METIN DENSITY: %d maps, %d -> %d independent spawn capacity; half respawn, non-Metin rows preserved' %
          (len(report['maps']), report['before'], report['after']))
