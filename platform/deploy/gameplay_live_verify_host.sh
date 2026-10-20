#!/usr/bin/env bash
set -euo pipefail
id=${1:?release id required}
[[ "$id" =~ ^[0-9]{8}-[0-9]{6}$ ]] || exit 2
cd "/home/m2web/gameplay-$id"
test -f INSTALLED
sha256sum --quiet -c release.sha256
sha256sum --quiet -c client-site.sha256
python3 /home/m2web/publish_engine_check.py client-site/corpus /home/m2web/www/corpus
python3 - <<'PY'
import hashlib, json
from pathlib import Path
site = Path('/home/m2web/www')
report = json.loads(Path('audit.json').read_text())
for path in Path('client-site').rglob('*'):
    if 'corpus' in path.parts or not path.is_file():
        continue
    live = site / path.relative_to('client-site')
    assert live.is_file() and hashlib.sha256(path.read_bytes()).digest() == hashlib.sha256(live.read_bytes()).digest(), str(live)
actual = hashlib.sha256((site / 'client.wasm').read_bytes()).hexdigest()
assert actual == report['client_provenance']['client_wasm_sha256']
print('LIVE CLIENT: all published files match the frozen candidate and ABI-audited WASM')
if Path('density-report.json').is_file():
    density = json.loads(Path('density-report.json').read_text())
    print('METIN DENSITY: %d maps, %d -> %d capacity' % (len(density['maps']), density['before'], density['after']))
PY
vm=(ssh -o BatchMode=yes -i /root/.ssh/metin2_vm root@192.168.122.10)
scp -q -i /root/.ssh/metin2_vm gameplay_live_verify_vm.sh "root@192.168.122.10:/usr/metin2-gameplay-$id/"
"${vm[@]}" "sh '/usr/metin2-gameplay-$id/gameplay_live_verify_vm.sh' '/usr/metin2-gameplay-$id'"
echo 'LIVE RELEASE VERIFIED'
