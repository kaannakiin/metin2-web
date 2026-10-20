import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]


class Phase3InstallTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix='m2-phase3-install-')
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.stage = self.root / 'metin2-phase3-20261020-000000'
        self.locale = self.root / 'home/share/locale/europe'
        self.bin = self.root / 'bin'
        self.bin.mkdir()
        self.env = dict(os.environ, PATH=str(self.bin) + os.pathsep + os.environ['PATH'],
                        EVENTS=str(self.root / 'events'), FAIL_ONCE=str(self.root / 'fail'))
        self.write(self.bin / 'sha256', '#!' + sys.executable + '\n'
                   'import hashlib,sys\n'
                   'for p in sys.argv[1:]:\n'
                   ' if p != "-q": print(hashlib.sha256(open(p,"rb").read()).hexdigest())\n', 0o755)
        self.write(self.bin / 'service', '#!/bin/sh\n'
                   'echo "$2" >>"$EVENTS"\n'
                   'if [ "$2" = start ] && [ -f "$FAIL_ONCE" ]; then rm "$FAIL_ONCE"; exit 1; fi\n', 0o755)
        self.write(self.bin / 'ps', '#!/bin/sh\n'
                   'printf "./db\\n./auth (game)\\n./game\\n./game\\n./game\\n./game99 (game)\\n"\n', 0o755)
        self.write(self.bin / 'sockstat', '#!/bin/sh\n'
                   'for port in 15000 30001 30003 30101 30103 30105; do\n'
                   ' echo "metin2 game 100 3 tcp4 127.0.0.1:$port *:*"\ndone\n', 0o755)
        self.write(self.bin / 'stat', '#!/bin/sh\n'
                   'case "$2" in %u|%g) id -u ;; %Lp) echo 644 ;; esac\n', 0o755)
        # chown is outside the test's concern; real ownership is preserved by the installer.
        self.write(self.bin / 'chown', '#!/bin/sh\nexit 0\n', 0o755)
        script = (ROOT / 'platform/deploy/phase3_loot_vm.sh').read_text()
        script = script.replace('/usr/metin2-phase3-', str(self.root / 'metin2-phase3-'))
        script = script.replace('/usr/home', str(self.root / 'home')).replace('sleep 1', 'sleep 0')
        self.script = self.stage / 'install.sh'
        self.write(self.script, script)
        self.files = ('mob_drop_item.txt', 'special_item_group.txt')
        for filename in self.files:
            self.write(self.locale / filename, 'old:' + filename)
            self.write(self.stage / 'input' / filename, 'new:' + filename)

    def write(self, path, text, mode=0o644):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)
        path.chmod(mode)

    def run_action(self, action):
        return subprocess.run(['/bin/sh', str(self.script), action, str(self.stage)],
                              env=self.env, capture_output=True, text=True)

    def assert_success(self, action):
        result = self.run_action(action)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_prepare_then_install_then_rollback(self):
        self.assert_success('prepare')
        self.assertFalse((self.root / 'events').exists())
        self.assert_success('install')
        for filename in self.files:
            self.assertEqual((self.locale / filename).read_text(), 'new:' + filename)
        self.assert_success('rollback')
        for filename in self.files:
            self.assertEqual((self.locale / filename).read_text(), 'old:' + filename)

    def test_live_drift_or_candidate_tamper_stops_before_maintenance(self):
        self.assert_success('prepare')
        self.write(self.locale / self.files[0], 'changed while prepared')
        self.assertNotEqual(self.run_action('install').returncode, 0)
        self.assertFalse((self.root / 'events').exists())
        self.write(self.locale / self.files[0], 'old:' + self.files[0])
        self.write(self.stage / 'input' / self.files[1], 'tampered candidate')
        self.assertNotEqual(self.run_action('install').returncode, 0)
        self.assertFalse((self.root / 'events').exists())

    def test_failed_start_restores_both_tables(self):
        self.assert_success('prepare')
        self.write(self.root / 'fail', '')
        self.assertNotEqual(self.run_action('install').returncode, 0)
        for filename in self.files:
            self.assertEqual((self.locale / filename).read_text(), 'old:' + filename)
        self.assertFalse((self.stage / 'INSTALLED').exists())

    def test_missing_backup_blocks_install_before_stop(self):
        self.assert_success('prepare')
        (self.stage / 'previous' / self.files[1]).unlink()
        self.assertNotEqual(self.run_action('install').returncode, 0)
        self.assertFalse((self.root / 'events').exists())


if __name__ == '__main__':
    unittest.main()
