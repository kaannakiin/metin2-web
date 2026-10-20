#!/usr/bin/env bash
set -euo pipefail
id=${1:?release id required}
[[ "$id" =~ ^[0-9]{8}-[0-9]{6}$ ]] || exit 2
cd "/home/m2web/gameplay-$id"
test -f BUNDLE_READY
test ! -e INSTALLED
sha256sum --quiet -c release.sha256
sha256sum --quiet -c client-site.sha256
python3 /home/m2web/publish_engine_check.py client-site/corpus /home/m2web/www/corpus
python3 - <<'PY'
from pathlib import Path
assert Path('/home/m2web/dev/protocol').read_text().strip() == 'live-yohara'
root = Path('/home/m2web/kit/build/port/scripts3')
tooltip = next(p for p in root.iterdir() if p.name.lower() == 'uitooltip.py').read_text()
assert 'if 27989 == itemVnum or 76006 == itemVnum:' in tooltip
print('DEV PREVIEW: legacy live protocol and finite detector UI restored')
PY
vm=(ssh -o BatchMode=yes -i /root/.ssh/metin2_vm root@192.168.122.10)
"${vm[@]}" "sh '/usr/metin2-gameplay-$id/gameplay_install_vm.sh' check '/usr/metin2-gameplay-$id'"
if [ -f DENSITY_READY ]; then
    "${vm[@]}" "sh '/usr/metin2-gameplay-$id/gameplay_install_vm.sh' check-density '/usr/metin2-gameplay-$id'"
    python3 - <<'PY'
import json
from pathlib import Path
report = json.loads(Path('density-report.json').read_text())
assert report['before'] == 97 and report['after'] == 194 and len(report['maps']) == 13
print('METIN DENSITY: 13 maps, 97 -> 194; included in candidate integrity checks')
PY
fi
echo 'LIVE GAME SHA256:'
"${vm[@]}" 'sha256 -q /usr/home/share/bin/game'
echo 'PUBLIC WASM SHA256:'
sha256sum /home/m2web/www/client.wasm
echo 'VERIFIED: frozen candidate intact and not installed; live preview healthy.'
