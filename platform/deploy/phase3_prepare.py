#!/usr/bin/env python3
"""Freeze the phase3 client and loot candidate; never restart live services."""
import argparse
import datetime
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[2]
HOST = 'root@88.99.1.151'
SSH = ['ssh', '-o', 'BatchMode=yes', '-o', 'ConnectTimeout=10']
SCP = ['scp', '-q', '-o', 'BatchMode=yes', '-o', 'ConnectTimeout=10']


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--id', default=datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%d-%H%M%S'))
    parser.add_argument('--client-from', help='Reuse an already frozen client candidate without rebuilding or rerunning tests')
    args = parser.parse_args()
    if not re.fullmatch(r'\d{8}-\d{6}', args.id):
        parser.error('id must be YYYYMMDD-HHMMSS')
    if args.client_from and (not re.fullmatch(r'\d{8}-\d{6}', args.client_from) or args.client_from == args.id):
        parser.error('client-from must name a different YYYYMMDD-HHMMSS candidate')
    destination = '/home/m2web/phase3-' + args.id
    subprocess.run(SSH + [HOST, 'mkdir -m 700 ' + destination + ' && mkdir ' + destination + '/input'], check=True)
    scripts = [ROOT / 'platform/deploy' / name for name in ('phase3_loot_host.sh', 'phase3_loot_vm.sh')]
    subprocess.run(SCP + [str(p) for p in scripts] + [HOST + ':' + destination + '/'], check=True)
    locale = ROOT / 'runtime/freebsd/share/locale/europe'
    subprocess.run(SCP + [str(locale / name) for name in ('mob_drop_item.txt', 'special_item_group.txt')]
                   + [HOST + ':' + destination + '/input/'], check=True)
    subprocess.run(SCP + [str(ROOT / 'platform/gameplay/phase3_loot.json')]
                   + [HOST + ':' + destination + '/'], check=True)
    command = 'bash ' + destination + '/phase3_loot_host.sh prepare ' + args.id
    if args.client_from:
        command += ' ' + args.client_from
    subprocess.run(SSH + [HOST, command], check=True)
    print('Operator maintenance: ssh ' + HOST + " 'bash " + destination
          + '/phase3_loot_host.sh install ' + args.id + " --operator-maintenance'")


if __name__ == '__main__':
    main()
