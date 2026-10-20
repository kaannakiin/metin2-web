#!/usr/bin/env python3
"""Audit the deployed game binary against the current staged web engine ABI."""
import argparse
import hashlib
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
HOST = 'root@88.99.1.151'
SSH = ['ssh', '-o', 'BatchMode=yes', '-o', 'ConnectTimeout=15']
SCP = ['scp', '-q', '-o', 'BatchMode=yes', '-o', 'ConnectTimeout=15']


def run(command):
    subprocess.run([str(value) for value in command], check=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', default=str(ROOT / 'build/protocol'))
    parser.add_argument('--strict', action='store_true')
    parser.add_argument('--candidate', help='Isolated gameplay release id; compare its binary instead of live')
    args = parser.parse_args()
    if args.candidate and not re.fullmatch(r'\d{8}-\d{6}', args.candidate):
        parser.error('candidate must be YYYYMMDD-HHMMSS')
    output = Path(args.output).resolve()
    output.mkdir(parents=True, exist_ok=True)
    run(SCP + [ROOT / 'platform/web-kit/tools/packet_abi_export.py', HOST + ':/home/m2web/kit/tools/'])
    run(SCP + [ROOT / 'platform/deploy/packet_abi_export.sh', ROOT / 'platform/deploy/packet_audit_host.sh',
               HOST + ':/home/m2web/'])
    remote_command = 'bash /home/m2web/packet_audit_host.sh' + (' ' + args.candidate if args.candidate else '')
    result = subprocess.run(SSH + [HOST, remote_command],
                            capture_output=True, text=True)
    if result.returncode:
        raise SystemExit((result.stdout + result.stderr)[-4000:])
    print(result.stdout.strip())
    match = re.search(r'^SERVER_BINARY_SHA256=([0-9a-f]{64})$', result.stdout, re.M)
    if not match:
        raise SystemExit('Missing live server binary fingerprint')
    binary = output / 'server-game.elf'
    if not binary.is_file() or hashlib.sha256(binary.read_bytes()).hexdigest() != match[1]:
        run(SCP + [HOST + ':/home/m2web/dev/packet-audit/server-game.elf', binary])
    if hashlib.sha256(binary.read_bytes()).hexdigest() != match[1]:
        raise SystemExit('Downloaded binary fingerprint mismatch')
    client = output / 'client-layout.json'
    run(SCP + [HOST + ':/home/m2web/dev/packet-audit/client-layout.json', client])
    command = [sys.executable, ROOT / 'platform/tools/packet_abi_audit.py', '--server', binary,
               '--client', client, '--output', output / 'audit.json']
    if args.strict:
        command.append('--strict')
    run(command)


if __name__ == '__main__':
    main()
