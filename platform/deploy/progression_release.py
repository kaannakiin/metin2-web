#!/usr/bin/env python3
"""Stage/compile and install the repeatable classic mid-PvP progression release."""
import argparse
from datetime import datetime, timezone
import hashlib
import io
from pathlib import Path
import subprocess
import tarfile
import tempfile

ROOT = Path(__file__).resolve().parents[2]
LOCALE = ROOT / 'runtime/freebsd/share/locale/europe'
HOST = 'root@88.99.1.151'
NAMES = ['deviltower_zone', 'devilcatacomb_zone', 'dragonlair', 'spider_dungeon', 'midpvp_progression']
BASE_COMMIT = '8ae9aadb3'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--install', action='store_true')
    parser.add_argument('--spawns-only', action='store_true', help='Install only the two access-boss spawn timers')
    args = parser.parse_args()
    release = datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S')
    remote = '/home/m2web/progression-' + release
    stage = '/usr/metin2-progression-' + release
    files = ['mob_drop_item.txt', 'quest/quest_list'] + [
        'quest/quest_tr/_midpvp/' + name + '.lua' for name in NAMES]
    existing = ['mob_drop_item.txt', 'quest/quest_list']
    if args.spawns_only:
        files = ['map/metin2_map_spiderdungeon/boss.txt', 'map/metin2_map_skipia_dungeon_02/boss.txt']
        existing = list(files)
    expected = []
    for name in existing:
        previous = subprocess.check_output(['git', 'show', BASE_COMMIT + ':runtime/freebsd/share/locale/europe/' + name], cwd=ROOT)
        if name == 'quest/quest_list':
            # Read-only live comparison found this optional reward quest absent.
            # Preserve the live selection instead of enabling unrelated rewards.
            previous = previous.replace(b'quest_tr/_guildsystems/mid_pvp_rewards.lua\n', b'')
        expected.append('SHA256 (/usr/home/share/locale/europe/%s) = %s\n' %
                        (name, hashlib.sha256(previous).hexdigest()))
    subprocess.run(['ssh', '-o', 'BatchMode=yes', HOST, 'mkdir -m 700 ' + remote], check=True)
    with tempfile.TemporaryDirectory(prefix='m2-progression-') as temporary:
        archive = Path(temporary) / 'payload.tar.gz'
        metadata = {'install-files.txt': '\n'.join(files) + '\n',
                    'expected-files.txt': '\n'.join(existing) + '\n', 'expected.sha256': ''.join(expected)}
        if args.spawns_only:
            metadata['data-only'] = 'access boss spawn timers\n'
        with tarfile.open(archive, 'w:gz') as output:
            for name in files:
                output.add(LOCALE / name, arcname='input/' + name, recursive=False)
            for name, value in metadata.items():
                data = value.encode()
                member = tarfile.TarInfo(name)
                member.size = len(data)
                member.mode = 0o600
                output.addfile(member, io.BytesIO(data))
        checksum = Path(temporary) / 'payload.sha256'
        checksum.write_text(hashlib.sha256(archive.read_bytes()).hexdigest() + '\n')
        subprocess.run(['scp', '-q', str(archive), str(checksum), str(ROOT / 'platform/deploy/progression_vm.sh'),
                        HOST + ':' + remote + '/'], check=True)
    vm = 'ssh -n -o BatchMode=yes -i /root/.ssh/metin2_vm root@192.168.122.10'
    command = ('set -eu\ncd ' + remote + '\nexec 9>/home/m2web/dev/client-build.lock\nflock -n 9\n'
               + vm + " 'mkdir -m 700 " + stage + "'\n"
               'scp -q -i /root/.ssh/metin2_vm payload.tar.gz payload.sha256 progression_vm.sh '
               'root@192.168.122.10:' + stage + '/\n'
               + vm + " 'sh " + stage + '/progression_vm.sh prepare ' + stage + "'\n"
               'touch READY\n')
    if args.install:
        command += (vm + " 'sh " + stage + '/progression_vm.sh install ' + stage + "'\n"
                    + vm + " 'test -f " + stage + "/INSTALLED'\ntouch INSTALLED\n")
    subprocess.run(['ssh', '-o', 'BatchMode=yes', HOST, 'bash -s'], input=command, text=True, check=True)
    print('PROGRESSION RELEASE: ' + release + (' INSTALLED' if args.install else ' READY'))
    print('VM backups and build logs: ' + stage)


if __name__ == '__main__':
    main()
