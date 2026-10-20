#!/bin/bash
# Rebuild web client with ServerStateChecker handshake skip + CH1 default open.
set -euo pipefail
cd /work/kit
source /work/emsdk/emsdk_env.sh

python3.13 webclient.py build --only stage
python3.13 webclient.py build --only engine
python3.13 webclient.py build --only scripts

python3 - <<'PY'
from pathlib import Path
p = Path("/work/kit/build/port/scripts/serverinfo.py")
t = p.read_text(encoding="latin1", errors="replace")
idx = t.find("SERVER1_CHANNEL_DICT")
if idx < 0:
    raise SystemExit("SERVER1_CHANNEL_DICT missing")
needle = '\t\t"state" : STATE_NONE,'
j = t.find(needle, idx)
if j >= 0:
    t = t[:j] + '\t\t"state" : STATE_DICT[1],' + t[j + len(needle):]
    p.write_text(t, encoding="latin1")
    print("patched scripts/serverinfo.py")
elif "STATE_DICT[1]" in t[idx:idx+400]:
    print("scripts/serverinfo.py already open-default")
else:
    raise SystemExit("could not patch SERVER1 state")
PY

cp -f /work/kit/build/port/scripts/serverinfo.py /work/kit/build/port/scripts3/serverinfo.py
python3.13 webclient.py build --only rewrite
python3.13 webclient.py build --only uiscript
python3.13 webclient.py build --only data
python3.13 webclient.py build --only link
python3.13 webclient.py build --only package
echo CHSTATUS_BUILD_OK
