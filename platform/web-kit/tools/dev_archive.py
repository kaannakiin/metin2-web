"""Reuse a kit archive only while its actual compiler dependencies match."""

import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

import workspace
from incremental_compile import ObjectCache


def main():
    step = sys.argv[1]
    if step not in ('eterbase', 'eterpack'):
        raise SystemExit('Expected eterbase or eterpack')
    root = Path(__file__).resolve().parents[1]
    port = root / 'build/port'
    archive = port / 'lib' / ('lib' + step + '.a')
    stamp = port / ('dev-' + step + '.json')
    cache = ObjectCache(shutil.which('em++') or 'em++')
    signature = hashlib.sha256(json.dumps([
        cache.identity, sys.version, cache.digest(root / 'tools' / ('build_' + step + '.py')),
        cache.digest(workspace.__file__),
        [cache.inventory(p) for p in (port / 'stage', workspace.COMPAT, workspace.EXTERN_INCLUDE)],
    ], sort_keys=True).encode()).hexdigest()
    try:
        saved = json.loads(stamp.read_text())
        if (saved['signature'] == signature and saved['archive'] == cache.digest(archive)
                and saved['dependencies']
                and all(cache.digest(p) == h for p, h in saved['dependencies'].items())):
            print('ARCHIVE CACHE: %s reused' % step)
            return 0
    except (OSError, ValueError, KeyError, TypeError):
        pass
    stamp.unlink(missing_ok=True)
    env = dict(os.environ)
    env['EMCC_CFLAGS'] = env.get('EMCC_CFLAGS', '') + ' -MD'
    subprocess.run([sys.executable, str(root / 'webclient.py'), 'build', '--only', step],
                   env=env, check=True)
    dependencies = set()
    for depfile in (port / 'obj' / step).glob('*.d'):
        dependencies.update(ObjectCache.dependencies(depfile))
    if not dependencies:
        print('ARCHIVE CACHE: %s built; no dependency files, cache disabled' % step)
        return 0
    saved = {'signature': signature, 'archive': cache.digest(archive),
             'dependencies': {os.path.abspath(p): cache.digest(p) for p in dependencies}}
    temporary = stamp.with_suffix('.tmp')
    temporary.write_text(json.dumps(saved, sort_keys=True))
    temporary.replace(stamp)
    print('ARCHIVE CACHE: %s built; %d dependencies recorded' % (step, len(dependencies)))
    return 0


if __name__ == '__main__':
    sys.exit(main())
