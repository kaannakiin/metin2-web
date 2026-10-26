#!/usr/bin/env python3
"""Build the permanent-support candidate in isolation; never restart live services."""
import datetime
import argparse
import hashlib
import json
import re
from pathlib import Path
import subprocess
import tarfile
import tempfile

ROOT = Path(__file__).resolve().parents[2]
HOST = 'root@88.99.1.151'

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--resume')
    args = parser.parse_args()
    if args.resume and not re.fullmatch(r'\d{8}-\d{6}', args.resume):
        parser.error('invalid release id')
    release = args.resume or datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%d-%H%M%S')
    remote = '/home/m2web/support-' + release
    stage = '/usr/metin2-support-' + release
    names = subprocess.check_output(['git','ls-files','--cached','--others','--exclude-standard','-z','--','apps/server'], cwd=ROOT).decode().split('\0')
    names += [
        'runtime/freebsd/share/locale/europe/quest/quest_tr/_npc_talk_mission/welcome.lua',
        'runtime/freebsd/share/locale/europe/quest/quest_tr/_npc_talk_mission/permanent_support.quest',
        'platform/tests/permanent_support_fixture.cpp', 'platform/tests/permanent_support_fixture.lua',
        'platform/tests/lua_fixture.cpp', 'platform/deploy/permanent_support_vm.sh',
        'content/server/sql/migrations/20261022_normal_attributes.sql',
    ]
    names = sorted({p for p in names if p and (ROOT/p).is_file() and not p.endswith(('.o','.a','.d','.core'))})
    with tempfile.TemporaryDirectory(prefix='m2-support-') as directory:
        archive = Path(directory)/'source.tar.gz'
        with tarfile.open(archive,'w:gz') as out:
            for name in names:
                out.add(ROOT/name,arcname=name,recursive=False)
        manifest = Path(directory)/'manifest.json'
        manifest.write_text(json.dumps({'release':release,'files':{p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in names}},indent=2)+'\n')
        subprocess.run(['ssh','-o','BatchMode=yes',HOST,('test -d ' if args.resume else 'mkdir -m 700 ')+remote],check=True)
        subprocess.run(['scp','-q',str(archive),str(manifest),HOST+':'+remote+'/'],check=True)
    command = (
        'ssh -o BatchMode=yes -i /root/.ssh/metin2_vm root@192.168.122.10 "'+('test -d ' if args.resume else 'mkdir -m 700 ')+stage+'" && '
        'scp -q -i /root/.ssh/metin2_vm '+remote+'/source.tar.gz '+remote+'/manifest.json root@192.168.122.10:'+stage+'/ && '
        'ssh -o BatchMode=yes -i /root/.ssh/metin2_vm root@192.168.122.10 '
        '"cd '+stage+' && tar -xzf source.tar.gz platform/deploy/permanent_support_vm.sh && '
        'nohup sh platform/deploy/permanent_support_vm.sh '+stage+' >build.log 2>&1 </dev/null &"'
    )
    subprocess.run(['ssh','-o','BatchMode=yes',HOST,command],check=True)
    print('BUILD STARTED:',stage)
    print('Live binaries, SQL and quests unchanged.')

if __name__ == '__main__':
    main()
