#!/usr/bin/env python3
"""Stage/compile and install the repeatable classic mid-PvP progression release."""
import argparse
from datetime import datetime, timezone
import hashlib
import io
from pathlib import Path
import re
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
    parser.add_argument('--server-baseline', help='Git source baseline for server updates; defaults to HEAD')
    parser.add_argument('--npc-resale-baseline', help='SHA-256 of the installed item.cpp before the sphere resale fix')
    parser.add_argument('--npc-server-root', help='Source tree of the installed permanent-support game build')
    scope = parser.add_mutually_exclusive_group()
    scope.add_argument('--spawns-only', action='store_true', help='Install only the two access-boss spawn timers')
    scope.add_argument('--starter-ring', action='store_true', help='Install only the one-time starter ring quest')
    scope.add_argument('--npc-profile', action='store_true', help='Install the active renewed SQL shops and support quest')
    scope.add_argument('--metin-metal', action='store_true', help='Install only the approved Magic Metal metin drops')
    scope.add_argument('--npc-stock', action='store_true', help='Update only renewed NPC SQL stock; preserve quests and binaries')
    scope.add_argument('--npc-market', action='store_true', help='Update NPC stock and build the sphere resale cap')
    scope.add_argument('--map-yang', action='store_true', help='Build/install only the approved map Yang server sources')
    scope.add_argument('--detector', action='store_true', help='Install unlimited detector server code and one-time recovery quest')
    args = parser.parse_args()
    if args.npc_market:
        if not re.fullmatch(r'[a-f0-9]{64}', args.npc_resale_baseline or ''):
            parser.error('--npc-market requires --npc-resale-baseline SHA256')
        if not re.fullmatch(r'/usr/metin2-support-\d{8}-\d{6}/apps/server', args.npc_server_root or ''):
            parser.error('--npc-market requires --npc-server-root /usr/metin2-support-ID/apps/server')
        args.npc_stock = True
    elif args.npc_resale_baseline or args.npc_server_root:
        parser.error('--npc-resale-baseline/--npc-server-root require --npc-market')
    if args.server_baseline and not (args.map_yang or args.detector):
        parser.error('--server-baseline requires --map-yang or --detector')
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
    if args.npc_profile:
        files = ['quest/quest_tr/_midpvp/starter_support.lua']
        existing = files + ['shop_table_ex.txt']
        baseline = 'faaf95e85'
    if args.metin_metal:
        files = ['mob_drop_item.txt']
        existing = list(files)
        baseline = '4f0c9a16b'
    if args.npc_stock:
        files = []
        existing = []
    if args.map_yang:
        files = []
        existing = []
    if args.detector:
        files = ['quest/quest_tr/_midpvp/starter_support.lua']
        existing = list(files)
        baseline = 'HEAD'
    expected = []
    for name in existing:
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
        metadata = {'install-files.txt': ''.join(name + '\n' for name in files),
                    'expected-files.txt': ''.join(name + '\n' for name in existing), 'expected.sha256': ''.join(expected)}
        if args.spawns_only or args.metin_metal or args.npc_stock or args.map_yang:
            metadata['data-only'] = 'selected runtime data; no quest or binary change\n'
        if args.map_yang:
            metadata['map-yang'] = 'map-specific Yang game binary and owned sources\n'
            metadata['data-only'] = 'no quest or locale data; game binary updated\n'
        if args.detector:
            metadata['detector'] = 'unlimited normal detector and one-time missing-item recovery\n'
        if args.map_yang or args.detector:
            metadata['server-update'] = 'owned server sources and game binary\n'
            sources = (['char_battle.cpp', 'mid_pvp_yang.h'] if args.map_yang
                       else ['item.cpp', 'mid_pvp_detector.h'])
            source_ref = args.server_baseline or 'HEAD'
            subprocess.run(['git', 'rev-parse', '--verify', source_ref + '^{commit}'],
                           cwd=ROOT, check=True, capture_output=True)
            source_existing, source_new, source_hashes = [], [], []
            for name in sources:
                previous = subprocess.run(['git', 'show', source_ref + ':apps/server/game/src/' + name],
                                          cwd=ROOT, capture_output=True)
                if previous.returncode == 0:
                    source_existing.append(name)
                    source_hashes.append('SHA256 (/usr/metin2/apps/server/game/src/%s) = %s\n' %
                                         (name, hashlib.sha256(previous.stdout).hexdigest()))
                else:
                    source_new.append(name)
            metadata['server-source-files.txt'] = ''.join(name + '\n' for name in sources)
            metadata['server-existing-files.txt'] = ''.join(name + '\n' for name in source_existing)
            metadata['server-new-files.txt'] = ''.join(name + '\n' for name in source_new)
            metadata['server-expected.sha256'] = ''.join(source_hashes)
        if args.npc_market:
            sources = ['item.cpp']
            metadata.update({
                'server-update': 'sphere NPC resale cap and game binary\n',
                'data-only': 'NPC SQL and game binary; no quest or locale changes\n',
                'server-source-files.txt': 'item.cpp\n',
                'server-existing-files.txt': 'item.cpp\n',
                'server-new-files.txt': '',
                'server-root.txt': args.npc_server_root + '\n',
                'server-expected.sha256': 'SHA256 (' + args.npc_server_root + '/game/src/item.cpp) = ' + args.npc_resale_baseline + '\n',
            })
        if args.npc_stock:
            metadata['npc-stock'] = 'active renewed NPC SQL stock only\n'
            for target, filename in [('repair_sql', 'database.sql'), ('snapshot', 'expected-database.tsv'),
                                     ('snapshot_sql', 'database-verify.sql')]:
                metadata[filename] = subprocess.check_output(
                    ['python3', str(ROOT / 'platform/tools/npc_profile.py'), target], cwd=ROOT, text=True)
        if args.starter_ring:
            metadata['starter-ring'] = 'one-time ring delivery\n'
        if args.npc_profile:
            metadata['npc-profile'] = 'ENABLE_RENEWAL_SHOPEX SQL profile\n'
            metadata['remove-files.txt'] = 'shop_table_ex.txt\n'
            metadata['database.sql'] = (ROOT / 'content/server/sql/migrations/20261021_npc_profile.sql').read_text()
            previous_source = subprocess.check_output(
                ['git', 'show', baseline + ':apps/server/game/src/shopEx.cpp'], cwd=ROOT)
            metadata['server-source.sha256'] = hashlib.sha256(previous_source).hexdigest() + '\n'
        with tarfile.open(archive, 'w:gz') as output:
            for name in files:
                output.add(LOCALE / name, arcname='input/' + name, recursive=False)
            if args.npc_profile:
                output.add(ROOT / 'apps/server/game/src/shopEx.cpp', arcname='server-source/shopEx.cpp', recursive=False)
            if args.map_yang or args.detector or args.npc_market:
                for name in sources:
                    output.add(ROOT / 'apps/server/game/src' / name, arcname='server-source/' + name, recursive=False)
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
