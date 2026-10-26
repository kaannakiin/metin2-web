#!/usr/bin/env bash
# Refresh nested layouts using the existing production engine and game scripts.
set -euo pipefail
source /work/emsdk/emsdk_env.sh >/dev/null 2>&1
cd /work/kit
export M2W_DEV_PROTOCOL=source M2W_LEGACY_DETECTOR=0
python3.13 -B -m unittest discover -s tools -p test_uiscript_from_client.py
python3.13 -I patchcheck.py /work/kit /work/websrc/source
python3.13 webclient.py build --only uiscript
python3.13 - <<'PY'
from pathlib import Path
import json
import os
import shutil
import tempfile

# Preserve the exact working layouts, including existing CharacterWindow fixes.
# Only the eight newly converted options layouts enter this release.
baseline = Path(os.environ['M2W_OPTIONS_BASELINE_SITE'])
script = (baseline / 'client.js').read_text()
metadata = json.JSONDecoder().raw_decode(script[script.index('{"files":'):])[0]
data = (baseline / 'client.data').read_bytes()
root = Path('build/port/uiscript3')
options = root / 'UIScript/advanced_game_options'
with tempfile.TemporaryDirectory() as temporary:
    saved = Path(temporary) / 'options'
    shutil.copytree(options, saved)
    shutil.rmtree(root)
    root.mkdir()
    count = 0
    for row in metadata['files']:
        if not row['filename'].startswith('/UIScript/'):
            continue
        relative = Path(row['filename'].lstrip('/'))
        assert '..' not in relative.parts
        destination = root / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(data[row['start']:row['end']])
        count += 1
    options.mkdir(parents=True, exist_ok=True)
    for name in ['game_option_%d.py' % i for i in range(7)] + ['game_option_filter.py']:
        assert not (options / name).exists(), 'Options layout already exists in baseline'
        shutil.copy2(saved / name, options / name)
print('OPTIONS BASELINE: preserved %d working layouts; added only 8 options layouts' % count)
PY
python3.13 - <<'PY'
from pathlib import Path
import sys
import types

locale = types.ModuleType('uiScriptLocale')
locale.__getattr__ = lambda name: name
sys.modules['uiScriptLocale'] = locale
root = Path('build/port/uiscript3/UIScript/advanced_game_options')
required = [root / ('game_option_%d.py' % i) for i in range(7)]
required.append(root / 'game_option_filter.py')
for path in required:
    scope = {'SCREEN_WIDTH': 1280, 'SCREEN_HEIGHT': 800}
    exec(compile(path.read_text(encoding='utf-8'), str(path), 'exec'), scope)
    assert isinstance(scope['window'], dict), path
print('OPTIONS LAYOUTS: all 8 generated layouts execute successfully')
PY
M2W_BOOT_SYSTEM=/work/kit/build/port/scripts3/system.py \
    python3.13 -B -m unittest discover -s tools -p test_python_startup.py
python3.13 tools/login_packet_layout.py
python3.13 tools/resp_packet_layout.py
python3.13 webclient.py package
python3.13 tools/bridge_config.py --site https://metin2.kaanakin.dev
python3.13 - <<'PY'
from pathlib import Path
import hashlib
import re

site = Path('dist/site')
generated = Path('build/port/uiscript3/UIScript/advanced_game_options')
data_root = Path('build/port/data/UIScript/advanced_game_options')
glue = (site / 'client.js').read_text()
for path in generated.glob('*.py'):
    assert path.read_bytes() == (data_root / path.name).read_bytes(), path
    assert '/UIScript/advanced_game_options/' + path.name in glue, path
page = (site / 'client.html').read_text()
for forbidden in ('m2wDevVersions', '127.0.0.1:1873', 'localhost:1873'):
    assert forbidden not in page, forbidden
assert b'loginInfo.xml' not in (site / 'client.js').read_bytes()
print('OPTIONS PACKAGE: nested layouts present in public data and file index')
print('VERSION:', re.search(r'preload\.js\?v=(\d+)', page).group(1))
print('WASM:', hashlib.sha256((site / 'client.wasm').read_bytes()).hexdigest())
PY
echo 'OPTIONS BUILD COMPLETE'
