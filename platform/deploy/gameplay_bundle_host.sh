#!/usr/bin/env bash
set -euo pipefail
id=${1:?release id required}
[[ "$id" =~ ^[0-9]{8}-[0-9]{6}$ ]] || exit 2
here="/home/m2web/gameplay-$id"
stage="/usr/metin2-gameplay-$id"
cd "$here"
test ! -e BUNDLE_READY
exec 9>/home/m2web/dev/client-build.lock
flock -n 9 || { echo 'Client build running'; exit 1; }
vm=(ssh -o BatchMode=yes -i /root/.ssh/metin2_vm root@192.168.122.10)
"${vm[@]}" "test -f '$stage/READY'"
python3 /home/m2web/publish_engine_check.py /home/m2web/kit/dist/site/corpus /home/m2web/www/corpus
mkdir client-site
rsync -a --exclude=/corpus/ --exclude=/asan/ /home/m2web/kit/dist/site/ client-site/
cp -al /home/m2web/www/corpus client-site/corpus
server_sha=$("${vm[@]}" "sha256 -q '$stage/out/game'")
export M2_GAMEPLAY_SERVER_SHA="$server_sha"
python3 - <<'PY'
import hashlib, json, os
from pathlib import Path
report = json.loads(Path('audit.json').read_text())
assert not report['validation_errors']
assert not report['record_mismatches'] and not report['header_mismatches']
assert report['server_binary_sha256'] == os.environ['M2_GAMEPLAY_SERVER_SHA']
assert report['client_provenance']['client_wasm_sha256'] == hashlib.sha256(Path('client-site/client.wasm').read_bytes()).hexdigest()
page = Path('client-site/client.html').read_text()
assert '127.0.0.1:1873' not in page and 'm2wDevVersions' not in page
assert b'loginInfo.xml' not in Path('client-site/client.js').read_bytes()
print('BUNDLE: actual server/client fingerprints agree with ABI audit')
PY
scp -q -i /root/.ssh/metin2_vm gameplay_install_vm.sh "root@192.168.122.10:$stage/"
"${vm[@]}" "sh '$stage/gameplay_install_vm.sh' prepare '$stage'"
scp -q -i /root/.ssh/metin2_vm "root@192.168.122.10:$stage/quest-check/object/notarget/login/welcome.start" welcome.start
scp -q -i /root/.ssh/metin2_vm "root@192.168.122.10:$stage/quest-check/object/state/welcome" welcome.state
scp -q -i /root/.ssh/metin2_vm "root@192.168.122.10:$stage/build.log" build.log
find client-site -path client-site/corpus -prune -o -type f -print0 | sort -z | xargs -0 sha256sum >client-site.sha256
sha256sum audit.json manifest.json gameplay_install_host.sh gameplay_install_vm.sh >release.sha256
touch BUNDLE_READY
echo "BUNDLE READY: $here; operator install only."
