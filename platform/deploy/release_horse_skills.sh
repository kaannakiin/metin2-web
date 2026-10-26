#!/usr/bin/env bash
# Host-side release: build a candidate, check the staged gate, use guarded publisher.
# No preview server, bridge, VM restart, or Cloudflare configuration changes.
set -euo pipefail
cd /home/m2web
(
    flock -n 9 || { echo 'Another client build is running'; exit 1; }
    test "$(cat dev/protocol)" = source
    log=/home/m2web/dev/logs/horse-skills-build.log
    if ! docker exec -e M2W_DEV_PROTOCOL=source -e M2W_LEGACY_DETECTOR=0 \
        -e M2W_PUBLIC_CANDIDATE=1 \
        m2web-build bash /work/dev_client_build.sh cpp >"$log" 2>&1; then
        tail -20 "$log"
        exit 1
    fi
    cat "$log"
    python3 - <<'PY'
from pathlib import Path
source = Path('/home/m2web/kit/build/port/stage/UserInterface/PythonPlayerSkill.cpp')
if not source.exists():
    matches = list(Path('/home/m2web/kit/build/port').rglob('PythonPlayerSkill.cpp'))
    assert len(matches) == 1, matches
    source = matches[0]
text = source.read_text(encoding='latin-1')
gate = text.split('bool CPythonPlayer::__CanUseSkill()', 1)[1].split('bool CPythonPlayer::__UseSkill', 1)[0]
assert 'GetSkillGrade(107)' not in gate and 'GetSkillGrade(109)' not in gate
assert 'return pkInstMain->CanUseSkill();' in gate
assert 'if (IsObserverMode())' in gate
assert 'CanUseWeaponType' in text and '"HAVE_TO_RIDE"' in text
print('HORSE SKILL GATE: actor/observer/weapon/mount checks retained; stale slots absent')
PY
) 9>dev/client-build.lock
expected=$(sha256sum kit/build/port/client.wasm | cut -d ' ' -f 1)
bash publish_text_encoding.sh "$expected"
