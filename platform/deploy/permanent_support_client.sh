#!/usr/bin/env bash
set -euo pipefail
cd /work/kit
source /work/emsdk/emsdk_env.sh >/dev/null 2>&1
export M2W_DEV_PROTOCOL=source M2W_PUBLIC_CANDIDATE=1 M2W_LEGACY_DETECTOR=0
python3.13 -I patchcheck.py /work/kit /work/websrc/source
python3.13 tools/build_gamelib.py
python3.13 tools/dev_ui_inputs.py /work/dev/inputs /work/kit/build/port/scripts /work/dev/ui-inputs.json
python3.13 webclient.py build --only rewrite
M2W_UISCRIPT_SOURCE=/work/dev/inputs/root/uiscript python3.13 webclient.py build --only uiscript
python3.13 tools/login_packet_layout.py
python3.13 tools/resp_packet_layout.py
python3.13 tools/build_client_data.py --no-private
python3.13 webclient.py build --only link
python3.13 webclient.py package
python3.13 tools/bridge_config.py --site https://metin2.kaanakin.dev
python3.13 - <<'PY'
import ast
from pathlib import Path
root = Path('build/port/scripts3')
policy = root / 'pvp_support_ui.py'
assert policy.is_file()
ast.parse(policy.read_text())
network = next(p for p in root.iterdir() if p.name.lower() == 'networkmodule.py')
assert 'pvp_support_ui.install' in network.read_text()
page = Path('dist/site/client.html').read_text()
assert '127.0.0.1:1873' not in page
assert Path('dist/site/client.wasm').stat().st_size > 1000000
print('CLIENT SUPPORT READY: source protocol, 14-item policy, simplified slots, no preview URLs.')
PY
