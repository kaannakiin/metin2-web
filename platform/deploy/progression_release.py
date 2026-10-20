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
    scope = parser.add_mutually_exclusive_group()
    scope.add_argument('--spawns-only', action='store_true', help='Install only the two access-boss spawn timers')
    scope.add_argument('--starter-ring', action='store_true', help='Install only the one-time starter ring quest')
    scope.add_argument('--npc-support', action='store_true', help='Install shops, support skills, horse and Yang profile')
    scope.add_argument('--support-only', action='store_true', help='Update only the support quest after the NPC release')
    args = parser.parse_args()
    release = datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S')
    remote = '/home/m2web/progression-' + release
    stage = '/usr/metin2-progression-' + release
    files = ['mob_drop_item.txt', 'quest/quest_list'] + [
        'quest/quest_tr/_midpvp/' + name + '.lua' for name in NAMES]
    existing = ['mob_drop_item.txt', 'quest/quest_list']
    baseline = BASE_COMMIT
    if args.starter_ring:
        files = ['quest/quest_list', 'quest/quest_tr/_midpvp/starter_ring.lua']
        existing = ['quest/quest_list']
        baseline = '52531594b'
    if args.spawns_only:
        files = ['map/metin2_map_spiderdungeon/boss.txt', 'map/metin2_map_skipia_dungeon_02/boss.txt']
        existing = list(files)
    if args.npc_support:
        files = ['mob_drop_item.txt', 'quest/quest_list', 'shop_table_ex.txt',
                 'quest/quest_tr/_midpvp/starter_support.lua']
        existing = ['mob_drop_item.txt', 'quest/quest_list']
        baseline = 'b05e59f48'
    if args.support_only:
        files = ['quest/quest_tr/_midpvp/starter_support.lua']
        existing = []
    expected = []
    if args.support_only:
        expected = ['SHA256 (/usr/home/share/locale/europe/quest/quest_tr/_midpvp/starter_support.lua) = '
                    'bc7654b6a2c5eeb66c573f599e59c74ca7e6871e28b7daf1985d6be9cf73af62\n']
        existing = list(files)
    for name in existing:
        if args.support_only:
            continue
        previous = subprocess.check_output(['git', 'show', baseline + ':runtime/freebsd/share/locale/europe/' + name], cwd=ROOT)
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
        if args.starter_ring:
            metadata['starter-ring'] = 'one-time ring delivery\n'
        if args.npc_support:
            metadata['npc-support'] = 'ShopEx and support skills\n'
            metadata['new-files.txt'] = 'shop_table_ex.txt\nquest/quest_tr/_midpvp/starter_support.lua\n'
            metadata['database.sql'] = (ROOT / 'content/server/sql/migrations/20261020_npc_support.sql').read_text()
        if args.support_only:
            metadata['support-only'] = 'support skills independent of book inventory space\n'
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
