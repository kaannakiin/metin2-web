#!/usr/bin/env python3
"""Back up and install the four-page inventory default on the live VM."""
from datetime import datetime, timezone
import hashlib
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]
HOST = 'root@88.99.1.151'


def main():
    release = datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S')
    remote = '/home/m2web/inventory-' + release
    stage = '/usr/metin2-inventory-' + release
    migration = ROOT / 'content/server/sql/migrations/20261020_default_inventory.sql'
    installer = ROOT / 'platform/deploy/inventory_defaults_vm.sh'
    subprocess.run(['ssh', '-o', 'BatchMode=yes', HOST, 'mkdir -m 700 ' + remote], check=True)
    with tempfile.TemporaryDirectory(prefix='m2-inventory-') as temporary:
        checksum = Path(temporary) / 'migration.sha256'
        checksum.write_text(hashlib.sha256(migration.read_bytes()).hexdigest() + '\n')
        subprocess.run(['scp', '-q', str(migration), str(installer), str(checksum),
                        HOST + ':' + remote + '/'], check=True)
    vm = 'ssh -n -o BatchMode=yes -i /root/.ssh/metin2_vm root@192.168.122.10'
    command = ('set -eu\ncd ' + remote + '\n'
               'exec 9>/home/m2web/dev/client-build.lock\nflock -n 9\n'
               + vm + " 'mkdir -m 700 " + stage + "'\n"
               'scp -q -i /root/.ssh/metin2_vm 20261020_default_inventory.sql '
               'inventory_defaults_vm.sh migration.sha256 root@192.168.122.10:' + stage + '/\n'
               + vm + " 'sh " + stage + '/inventory_defaults_vm.sh ' + stage + "'\n"
               + vm + " 'test -f " + stage + "/INSTALLED'\n"
               'touch INSTALLED\n')
    subprocess.run(['ssh', '-o', 'BatchMode=yes', HOST, 'bash -s'], input=command, text=True, check=True)
    print('INVENTORY RELEASE INSTALLED: ' + release)


if __name__ == '__main__':
    main()
