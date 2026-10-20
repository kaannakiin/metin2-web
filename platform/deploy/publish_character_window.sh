#!/usr/bin/env bash
# UI-only repair on the already installed source-protocol release.
set -euo pipefail
cd /home/m2web
exec 9>dev/client-build.lock
flock -n 9 || { echo 'A development build is running'; exit 1; }
test "$(cat dev/protocol)" = source
test "$(sha256sum www/client.wasm | cut -d ' ' -f 1)" = 8db82fe2e68ac06f548e14187cc0b9b8a3849135cee4e766cc80a67cad153d5d
layout=$(find kit/build/port/uiscript3/UIScript -maxdepth 1 -iname characterwindow.py -printf '/work/%p\n')
test -n "$layout"
docker exec -e M2W_DEV_PROTOCOL=source -e M2_CHARACTER_LAYOUT="$layout" \
    -e M2_CHARACTER_BINDING=/work/kit/build/port/scripts3/uiCharacter.py \
    m2web-build python3.13 /work/test_character_window.py
docker exec m2web-build bash /work/gameplay_client_build.sh
cmp kit/dist/site/client.wasm www/client.wasm
python3 publish_engine_check.py kit/dist/site/corpus www/corpus
backup=$(mktemp -d /home/m2web/backups/character-window-XXXXXXXX)
mkdir "$backup/site"
rsync -a --exclude=/corpus/ --exclude=/asan/ www/ "$backup/site/"
rollback() {
    rsync -a --delete --exclude=/corpus/ --exclude=/asan/ "$backup/site/" www/
}
trap rollback ERR
bash publish.sh --engine-only
cmp kit/dist/site/client.data www/client.data
cmp kit/dist/site/client.html www/client.html
trap - ERR
echo "PUBLISHED: character layout fix; engine/corpus unchanged; backup $backup"
