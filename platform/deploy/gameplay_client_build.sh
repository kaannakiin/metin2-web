#!/usr/bin/env bash
set -euo pipefail
source /work/emsdk/emsdk_env.sh >/dev/null 2>&1
cd /work/kit
export M2W_DEV_PROTOCOL=source
node --test tools/test_prefetch.js
python3.13 tools/login_packet_layout.py
python3.13 tools/resp_packet_layout.py
python3.13 - <<'PY'
import ast
from pathlib import Path
root = Path('build/port/scripts3')
tooltip = next(path for path in root.iterdir() if path.name.lower() == 'uitooltip.py')
text = tooltip.read_text()
ast.parse(text)
assert 'elif 76006 == itemVnum:' in text
assert 'itemDesc = itemDesc.replace("6", localeInfo.TOOLTIP_POTION_UNLIMITED' in text
assert 'TOOLTIP_REST_USABLE_COUNT.replace("%d", "%s")' in text
print('DETECTOR UI: rewritten Python parses; ordinary unlimited and alternate charge branches present')
PY
python3.13 webclient.py package
python3.13 tools/bridge_config.py --site https://metin2.kaanakin.dev
python3.13 - <<'PY'
from pathlib import Path
site = Path('dist/site')
page = (site / 'client.html').read_text()
for forbidden in ('m2wDevVersions', '127.0.0.1:1873', 'localhost:1873'):
    assert forbidden not in page, forbidden
assert b'loginInfo.xml' not in (site / 'client.js').read_bytes()
print('CANDIDATE PACKAGE: source protocol, no preview override or private login data')
PY
