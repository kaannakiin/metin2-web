#!/usr/bin/env bash
# Container-side build. Called as a file by dev_client_host.sh.
set -euo pipefail
source /work/emsdk/emsdk_env.sh >/dev/null 2>&1
cd /work/kit
mode=${1:-cpp}
mkdir -p /work/dev/logs
run_step() {
    local label=$1
    shift
    local started=$SECONDS
    if "$@" >"/work/dev/logs/${label}.log" 2>&1; then
        echo "${label}: $((SECONDS - started))s"
        grep -E 'OBJECT CACHE:|ARCHIVE CACHE:|LINKED|UNEXPECTED|patches=|UI INPUTS:|PREVIEW READY:|DEV BRIDGE:' \
            "/work/dev/logs/${label}.log" || true
    else
        echo "FAILED: ${label}; /home/m2web/dev/logs/${label}.log"
        tail -12 "/work/dev/logs/${label}.log"
        exit 1
    fi
}
case "$mode" in
    cpp|clean)
        run_step patchcheck python3.13 -I patchcheck.py /work/kit /work/websrc/source
        grep -Eq '^patches=[0-9]+ hit=[0-9]+ miss=0$' /work/dev/logs/patchcheck.log || {
            echo 'Stage patch validation failed; see /home/m2web/dev/logs/patchcheck.log'
            exit 1
        }
        # engine stages internally. Preserve O2: unoptimized skinning is too slow.
        extra=()
        [ "$mode" != clean ] || extra=(--clean)
        run_step engine python3.13 tools/build_gamelib.py "${extra[@]}"
        run_step eterbase python3.13 tools/dev_archive.py eterbase
        run_step eterpack python3.13 tools/dev_archive.py eterpack
        ;;
    ui)
        run_step ui-inputs python3.13 tools/dev_ui_inputs.py /work/dev/inputs \
            /work/kit/build/port/scripts /work/dev/ui-inputs.json
        run_step rewrite python3.13 webclient.py build --only rewrite
        run_step uiscript env M2W_UISCRIPT_SOURCE=/work/dev/inputs/root/uiscript \
            python3.13 webclient.py build --only uiscript
        ;;
    link) ;;
    *) echo 'Expected cpp, clean, ui or link'; exit 2 ;;
esac
run_step protocol python3.13 tools/login_packet_layout.py
run_step resp-wire python3.13 tools/resp_packet_layout.py
# One data assembly and one link. package.py would link twice more.
run_step data python3.13 tools/build_client_data.py --no-private
run_step link python3.13 webclient.py build --only link
run_step snapshot python3.13 tools/dev_preview.py snapshot --root /work/dev/site \
    --build-root /work/kit/build/port
if [ "${M2W_PUBLIC_CANDIDATE:-0}" != 1 ]; then
    run_step bridge-config python3.13 tools/dev_preview.py config --root /work/dev/bridge.json
fi
