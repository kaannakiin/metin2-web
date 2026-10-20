#!/usr/bin/env python3
"""Refuse an engine-only publish unless the published corpus is unchanged."""
from pathlib import Path
import re
import sys


def check(source, published):
    source, published = Path(source), Path(published)
    for name in ('manifest.bin', 'groups.txt'):
        if not (source / name).is_file() or (source / name).read_bytes() != (published / name).read_bytes():
            raise ValueError('Corpus %s changed; use the full CDN publish' % name)
    def chunks(root):
        return {p.name: p.stat().st_size for p in root.iterdir()
                if p.is_file() and re.fullmatch(r'[0-9a-f]{32}\.bin', p.name)}
    new, old = chunks(source), chunks(published)
    if len(new) <= 1000 or new != old:
        raise ValueError('Corpus chunk inventory changed; use the full CDN publish')
    print('UNCHANGED CORPUS: %d immutable chunks; CDN upload skipped' % len(new))


if __name__ == '__main__':
    try:
        check(*sys.argv[1:])
    except (OSError, ValueError, TypeError) as error:
        raise SystemExit(str(error))
