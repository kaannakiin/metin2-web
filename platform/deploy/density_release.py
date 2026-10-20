#!/usr/bin/env python3
"""Release only the approved x4 Metin density / half-respawn map files."""
import argparse
from datetime import datetime, timezone
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import subprocess
import tarfile
import tempfile

ROOT = Path(__file__).resolve().parents[2]
HOST = 'root@88.99.1.151'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--install', action='store_true', help='Restart game services and install')
    args = parser.parse_args()
    spec = importlib.util.spec_from_file_location('density', ROOT / 'platform/tools/metin_density.py')
    density = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(density)
    report = density.check()
    policy = json.loads((ROOT / 'platform/gameplay/metin_density.json').read_text())
    release = datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S')
    remote = '/home/m2web/density-' + release
    with tempfile.TemporaryDirectory(prefix='m2-density-release-') as temporary:
        archive = Path(temporary) / 'payload.tar.gz'
        metadata = {
            'files.txt': ''.join(row['path'] + '\n' for row in report['maps']),
            'expected.sha256': ''.join('SHA256 (/usr/home/share/locale/europe/%s) = %s\n' %
                                      (row['path'], row['previous_sha256']) for row in policy['maps']),
            'candidate.sha256': ''.join('SHA256 (input/%s) = %s\n' %
                                       (row['path'], row['sha256']) for row in report['maps']),
            'report.json': json.dumps(report, indent=2) + '\n',
        }
        with tarfile.open(archive, 'w:gz') as output:
            for row in report['maps']:
                output.add(ROOT / 'runtime/freebsd/share/locale/europe' / row['path'],
                           arcname='input/' + row['path'], recursive=False)
            for name, text in metadata.items():
                data = text.encode()
                item = tarfile.TarInfo(name)
                item.size = len(data)
                item.mode = 0o600
                output.addfile(item, io.BytesIO(data))
        checksum = Path(temporary) / 'payload.sha256'
        checksum.write_text(hashlib.sha256(archive.read_bytes()).hexdigest() + '  payload.tar.gz\n')
        subprocess.run(['ssh', '-o', 'BatchMode=yes', HOST, 'mkdir -m 700 ' + remote], check=True)
        paths = [archive, checksum, ROOT / 'platform/deploy/density_install_host.sh',
                 ROOT / 'platform/deploy/density_install_vm.sh']
        subprocess.run(['scp', '-q'] + [str(path) for path in paths] + [HOST + ':' + remote + '/'], check=True)
    action = 'install' if args.install else 'prepare'
    subprocess.run(['ssh', '-o', 'BatchMode=yes', HOST,
                    'bash ' + remote + '/density_install_host.sh ' + release + ' ' + action], check=True)
    print('DENSITY RELEASE: ' + release + ' ' + action + ' complete')


if __name__ == '__main__':
    main()
