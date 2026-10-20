#!/usr/bin/env python3
"""Attach validated map-density data to an uninstalled gameplay candidate."""
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import re
import subprocess
import tarfile
import tempfile

ROOT = Path(__file__).resolve().parents[2]
HOST = 'root@88.99.1.151'
spec = importlib.util.spec_from_file_location('density', ROOT / 'platform/tools/metin_density.py')
density = importlib.util.module_from_spec(spec)
spec.loader.exec_module(density)


def main():
    report = density.check()
    release = report['base_release']
    if not re.fullmatch(r'\d{8}-\d{6}', release):
        raise SystemExit('Invalid base release')
    remote = '/home/m2web/gameplay-' + release
    with tempfile.TemporaryDirectory(prefix='m2-density-') as temporary:
        archive = Path(temporary) / 'density.tar.gz'
        names = [row['path'] for row in report['maps']]
        metadata = {
            'density-files.txt': '\n'.join(names) + '\n',
            'density.sha256': ''.join('SHA256 (density/%s) = %s\n' % (row['path'], row['sha256']) for row in report['maps']),
            'density-baseline.sha256': ''.join('SHA256 (/usr/home/share/locale/europe/%s) = %s\n' %
                                              (row['path'], row['baseline_sha256']) for row in report['maps']),
            'density-report.json': json.dumps(report, indent=2) + '\n',
        }
        with tarfile.open(archive, 'w:gz') as output:
            for row in report['maps']:
                output.add(ROOT / 'runtime/freebsd/share/locale/europe' / row['path'],
                           arcname='density/' + row['path'], recursive=False)
            for name, text in metadata.items():
                encoded = text.encode()
                item = tarfile.TarInfo(name)
                item.size = len(encoded)
                item.mode = 0o600
                output.addfile(item, io.BytesIO(encoded))
        checksum = Path(temporary) / 'density-payload.sha256'
        checksum.write_text(hashlib.sha256(archive.read_bytes()).hexdigest() + '  density.tar.gz\n')
        files = [archive, checksum] + [ROOT / 'platform/deploy' / name for name in (
            'gameplay_install_vm.sh', 'gameplay_density_stage_host.sh', 'gameplay_density_vm.sh')]
        subprocess.run(['scp', '-q'] + [str(path) for path in files] + [HOST + ':' + remote + '/'], check=True)
    subprocess.run(['ssh', '-o', 'BatchMode=yes', HOST,
                    'bash ' + remote + '/gameplay_density_stage_host.sh ' + release], check=True)
    print('Prepared %d maps: %d -> %d Metins; no live data changed.' %
          (len(report['maps']), report['before'], report['after']))


if __name__ == '__main__':
    main()
