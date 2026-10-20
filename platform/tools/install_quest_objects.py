#!/usr/bin/env python3
"""Sync compiled build artifacts for the five owned progression quest namespaces."""
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
    args = parser.parse_args()
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
    print('Synced %d compiled artifacts across five quest namespaces' % len(outputs))


if __name__ == '__main__':
    main()
