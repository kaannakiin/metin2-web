#!/usr/bin/env python3
"""Sync and test the Metin2 web client without publishing it."""

import argparse
from pathlib import Path
import shlex
import subprocess
import sys
import time


ROOT = Path(__file__).resolve().parents[2]
HOST = 'root@88.99.1.151'
PREVIEW_URL = 'http://127.0.0.1:18731/client.html?lang=tr'
SSH = ['ssh', '-o', 'BatchMode=yes', '-o', 'ConnectTimeout=10']
SCP = ['scp', '-q', '-o', 'BatchMode=yes', '-o', 'ConnectTimeout=10']
KIT_FILES = ('patchcheck.py', 'tools/build_gamelib.py', 'tools/incremental_compile.py',
             'tools/bridge_config.py', 'tools/dev_preview.py', 'tools/dev_ui_inputs.py',
             'tools/dev_archive.py', 'tools/dev_protocol.py', 'tools/login_packet_layout.py',
             'tools/resp_packet_layout.py', 'tools/test_resp_wire.cpp', 'compat/resp_wire.h',
             'compat/runtime.js',
             'tools/script_patches.py', 'tools/uiscript_from_client.py',
             'bridge/test/dev.test.js')


def run(args):
    subprocess.run([str(a) for a in args], check=True)


def sync():
    run(SSH + [HOST, 'mkdir -p /home/m2web/dev/inputs/root /home/m2web/dev/inputs/locale'])
    # One SSH connection for the tool set, rather than one connection per file.
    subprocess.run(['rsync', '-az', '--files-from=-', '-e',
                    'ssh -o BatchMode=yes -o ConnectTimeout=10',
                    str(ROOT / 'platform/web-kit') + '/', HOST + ':/home/m2web/kit/'],
                   input='\n'.join(KIT_FILES) + '\n', text=True, check=True)
    run(SCP + [ROOT / 'platform/web-kit/stage_port.py',
         HOST + ':/home/m2web/kit/tools/stage_port.py'])
    run(['rsync', '-az', '--delete', '-e', 'ssh -o BatchMode=yes -o ConnectTimeout=10',
         str(ROOT / 'platform/web-kit/bridge/src') + '/',
         HOST + ':/home/m2web/kit/bridge/src/'])
    run(SCP + [ROOT / 'platform/deploy/dev_client_host.sh',
               ROOT / 'platform/deploy/dev_client_build.sh', HOST + ':/home/m2web/'])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=('cpp', 'clean', 'ui', 'link', 'serve', 'stop', 'tunnel'))
    parser.add_argument('--protocol', choices=('source', 'live-yohara'),
                        help='Explicit server protocol preset; remembered after a successful cpp/clean build')
    args = parser.parse_args()
    if args.protocol and args.action not in ('cpp', 'clean'):
        parser.error('--protocol requires cpp or clean (it changes engine headers)')
    if args.action == 'tunnel':
        print('Open ' + PREVIEW_URL + '; Ctrl+C closes the tunnel.', flush=True)
        run(SSH + ['-N', '-o', 'ExitOnForwardFailure=yes', '-o', 'ServerAliveInterval=30',
                   '-L', '127.0.0.1:18731:127.0.0.1:18731',
                   '-L', '127.0.0.1:18732:127.0.0.1:18732', HOST])
        return
    started = time.monotonic()
    if args.action not in ('stop', 'serve'):
        sync()
        if args.action in ('cpp', 'clean'):
            # Keep the existing web-only Locale_inc.h flag adaptations.
            run(['rsync', '-az', '--delete', '--exclude=UserInterface/Locale_inc.h',
                 '-e', 'ssh -o BatchMode=yes -o ConnectTimeout=10',
                 str(ROOT / 'apps/client/source') + '/', HOST + ':/home/m2web/websrc/source/'])
        elif args.action == 'ui':
            for pack in ('root', 'locale'):
                run(['rsync', '-az', '--delete', '-e', 'ssh -o BatchMode=yes -o ConnectTimeout=10',
                     str(ROOT / 'content/client/packs' / pack) + '/',
                     HOST + ':/home/m2web/dev/inputs/' + pack + '/'])
    command = 'bash /home/m2web/dev_client_host.sh ' + shlex.quote(args.action)
    if args.protocol:
        command += ' ' + shlex.quote(args.protocol)
    run(SSH + [HOST, command])
    print('Total: %.1fs' % (time.monotonic() - started))
    if args.action != 'stop':
        print('Tunnel: python3 platform/deploy/dev_client.py tunnel')
        print('Preview: ' + PREVIEW_URL)


if __name__ == '__main__':
    try:
        main()
    except (subprocess.CalledProcessError, KeyboardInterrupt) as error:
        sys.exit(error.returncode if isinstance(error, subprocess.CalledProcessError) else 130)
