"""Overlay unpacked root/locale sources before the kit's Python conversion."""

import json
from pathlib import Path
import shutil
import sys


def main():
    inputs, scripts, state = map(Path, sys.argv[1:])
    if not (scripts / 'system.py').is_file():
        raise SystemExit('Run the kit scripts/unpack step once before using ui mode')
    current = {}
    for pack, prefix in (('root', ''), ('locale', 'locale')):
        source = inputs / pack
        if not source.is_dir():
            raise SystemExit('Missing unpacked input: ' + str(source))
        for f in source.rglob('*'):
            if f.is_file():
                relative = (Path(prefix) / f.relative_to(source)).as_posix()
                current[relative] = f
    previous = json.loads(state.read_text()) if state.is_file() else []
    for relative in previous:
        target = scripts / relative
        if relative not in current and target.resolve().is_relative_to(scripts.resolve()):
            target.unlink(missing_ok=True)
    for relative, source in current.items():
        target = scripts / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
    state.parent.mkdir(parents=True, exist_ok=True)
    state.write_text(json.dumps(sorted(current)), encoding='utf-8')
    print('UI INPUTS: %d unpacked root/locale files; no pack rebuild' % len(current))


if __name__ == '__main__':
    main()
