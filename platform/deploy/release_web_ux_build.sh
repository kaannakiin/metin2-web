#!/usr/bin/env bash
# Container-side candidate build; invoked as a file, no VM/service changes.
set -euo pipefail
source /work/emsdk/emsdk_env.sh >/dev/null 2>&1
cd /work/kit
export M2W_DEV_PROTOCOL=source
export M2W_LEGACY_DETECTOR=0
node --test tools/test_prefetch.js tools/test_web_ux.js
python3.13 -B -m unittest discover -s tools -p test_web_ux.py
python3.13 -I patchcheck.py /work/kit /work/websrc/source
python3.13 webclient.py build --only rewrite
M2W_BOOT_SYSTEM=/work/kit/build/port/scripts3/system.py \
    python3.13 -B -m unittest discover -s tools -p test_python_startup.py
python3.13 tools/login_packet_layout.py
python3.13 tools/resp_packet_layout.py
python3.13 webclient.py package
python3.13 tools/bridge_config.py --site https://metin2.kaanakin.dev
python3.13 - <<'PY'
from pathlib import Path
import ast
site = Path('dist/site')
page = (site / 'client.html').read_text()
glue = (site / 'client.js').read_text()
assert 'm2w.prepareStartup()' in page
assert 'tabindex="0"' in page
for marker in ('m2w.loginManifest =', 'm2w.prepareLoginResources =', 'm2w.startViewportFit =', 'state.pinned.has(k)', 'push(0x0102, 9)'):
    assert marker in glue, marker
assert 'state.map.has(n) || p.fetched.has(n)' not in glue
assert (Path('compat/web_ux.py').read_bytes() == Path('build/port/data/web_ux.py').read_bytes())
login = next(p for p in Path('build/port/scripts3').iterdir() if p.name.lower() == 'intrologin.py')
ast.parse(login.read_text())
assert 'web_ux.install(LoginWindow)' in login.read_text()
assert b'loginInfo.xml' not in (site / 'client.js').read_bytes()
for forbidden in ('m2wDevVersions', '127.0.0.1:1873', 'localhost:1873'):
    assert forbidden not in page, forbidden
print('WEB UX CANDIDATE: startup gate, IME Tab, RAM readiness and username-only bridge present')
PY
# Use the existing private preview transport for browser acceptance.
python3.13 tools/dev_preview.py snapshot --root /work/dev/site --build-root /work/kit/build/port
echo 'WEB UX BUILD COMPLETE'
