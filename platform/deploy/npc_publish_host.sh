#!/usr/bin/env bash
# Final combined publication of the prepared VM profile and built client.
set -euo pipefail
release=${1:?release timestamp}
[[ "$release" =~ ^[0-9]{8}-[0-9]{6}$ ]] || exit 2
stage=/home/m2web/progression-$release
vmstage=/usr/metin2-progression-$release
cd "$stage"
exec 9>/home/m2web/dev/client-build.lock
flock -n 9
test -f READY
test ! -f INSTALLED
site=/home/m2web/kit/dist/site
for file in client.html client.js client.wasm client.data preload.js sw.js; do
    test -s "$site/$file"
done
python3 /home/m2web/publish_engine_check.py "$site/corpus" /home/m2web/www/corpus
mkdir -m 700 previous-client
rsync -a --exclude=/corpus/ --exclude=/asan/ /home/m2web/www/ previous-client/
ssh -n -o BatchMode=yes -i /root/.ssh/metin2_vm root@192.168.122.10 \
    "sh $vmstage/progression_vm.sh install $vmstage"
ssh -n -o BatchMode=yes -i /root/.ssh/metin2_vm root@192.168.122.10 \
    "test -f $vmstage/INSTALLED"
if ! /home/m2web/publish.sh --engine-only; then
    rsync -a --delete --exclude=/corpus/ --exclude=/asan/ previous-client/ /home/m2web/www/
    echo 'Client publication failed; previous client restored. VM profile remains installed.' >&2
    exit 1
fi
for file in client.html client.js client.wasm client.data preload.js sw.js; do
    cmp "$site/$file" "/home/m2web/www/$file"
done
touch INSTALLED
echo "INSTALLED $release: NPC/horse/skills/Yang/metin profile and corrected client; corpus unchanged."
