#!/usr/bin/env bash
set -euo pipefail
source /work/emsdk/emsdk_env.sh >/dev/null 2>&1
cd /work/kit
export M2W_DEV_PROTOCOL=live-yohara
python3.13 tools/login_packet_layout.py
python3.13 tools/resp_packet_layout.py
python3.13 webclient.py package
python3.13 tools/bridge_config.py --site https://metin2.kaanakin.dev
python3.13 - <<'PY'
from pathlib import Path
site = Path('/work/kit/dist/site')
page = (site / 'client.html').read_text()
for forbidden in ('m2wDevVersions', '127.0.0.1:1873', 'localhost:1873'):
    if forbidden in page:
        raise SystemExit('Refusing a private preview setting in the public package')
if b'loginInfo.xml' in (site / 'client.js').read_bytes():
    raise SystemExit('Refusing private login files in the public package')
print('PUBLIC PACKAGE: no preview bridge override or private login data')
PY
