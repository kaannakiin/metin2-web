#!/usr/bin/env python3
"""Sync compiled build artifacts for the selected owned quest namespaces."""
import argparse
from pathlib import Path, PurePosixPath
import tarfile

ROOT = Path(__file__).resolve().parents[2]
OBJECT = ROOT / 'runtime/freebsd/share/locale/europe/quest/object'
NAMES = {'deviltower_zone', 'devilcatacomb_zone', 'dragonlair', 'spider_dungeon', 'midpvp_progression'}


def owned(name):
    return any(name == quest or name.startswith(quest + '.') for quest in NAMES)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('archive', type=Path)
    parser.add_argument('--starter-ring', action='store_true', help='Sync only the starter ring build')
    parser.add_argument('--npc-support', action='store_true', help='Sync only the support skills and horse build')
    args = parser.parse_args()
    if args.starter_ring:
        NAMES.clear()
        NAMES.add('starter_ring')
    if args.npc_support:
        NAMES.clear()
        NAMES.add('starter_support')
    outputs = {}
    with tarfile.open(args.archive) as archive:
        for member in archive.getmembers():
            path = PurePosixPath(member.name)
            if path.is_absolute() or '..' in path.parts or path.parts[0] != 'object':
                raise SystemExit('Unsafe compiled artifact path')
            if member.isdir():
                continue
            if not member.isfile() or not owned(path.name) or member.size > 2 * 1024 * 1024:
                raise SystemExit('Unexpected compiled artifact')
            target = OBJECT.joinpath(*path.parts[1:])
            if target in outputs:
                raise SystemExit('Duplicate compiled artifact')
            outputs[target] = archive.extractfile(member).read()
    for quest in NAMES:
        if not outputs.get(OBJECT / 'state' / quest):
            raise SystemExit('Missing compiled quest state: ' + quest)
    for path in OBJECT.rglob('*'):
        if path.is_file() and owned(path.name) and path not in outputs:
            path.unlink()
    for path, data in outputs.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
    print('Synced %d compiled artifacts across %d quest namespaces' % (len(outputs), len(NAMES)))


if __name__ == '__main__':
    main()
