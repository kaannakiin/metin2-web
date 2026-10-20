import os
import hashlib
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]


class GameplayInstallTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix='m2-install-test-')
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.home = self.root / 'home'
        self.stage = self.root / 'metin2-gameplay-20261019-213727'
        self.stage.mkdir()
        self.bin = self.root / 'bin'
        self.bin.mkdir()
        self.env = dict(os.environ, PATH=str(self.bin) + os.pathsep + os.environ['PATH'],
                        EVENTS=str(self.root / 'events'), FAIL_ONCE=str(self.root / 'fail-once'),
                        GAME_FILE=str(self.home / 'share/bin/game'))
        self.write(self.bin / 'sha256', '#!' + sys.executable + '\n'
                   'import hashlib, sys\n'
                   'for name in sys.argv[1:]:\n'
                   ' print("SHA256 (%s) = %s" % (name, hashlib.sha256(open(name,"rb").read()).hexdigest()))\n', 0o755)
        self.write(self.bin / 'service', '#!/bin/sh\n'
                   'echo "$2" >>"$EVENTS"\n'
                   'if [ "$2" = start ] && [ -f "$FAIL_ONCE" ]; then rm "$FAIL_ONCE"; exit 1; fi\n'
                   'exit 0\n', 0o755)
        self.write(self.bin / 'ps', '#!' + sys.executable + '\n'
                   'import os\n'
                   'candidate=open(os.environ["GAME_FILE"]).read().startswith("candidate:")\n'
                   'names=["./db","./auth (game)","./game","./game","./game","./game99 (game)"]\n'
                   'if candidate and os.environ.get("FAIL_PROCESS_HEALTH"): names.pop()\n'
                   'print("\\n".join(names))\n', 0o755)
        self.write(self.bin / 'sockstat', '#!' + sys.executable + '\n'
                   'import os\n'
                   'candidate=open(os.environ["GAME_FILE"]).read().startswith("candidate:")\n'
                   'ports=[15000,30001,30003,30101,30103,30105]\n'
                   'if candidate and os.environ.get("FAIL_SOCKET_HEALTH"): ports.pop()\n'
                   'for port in ports: print("metin2 game 100 3 tcp4 127.0.0.1:%d *:*" % port)\n', 0o755)
        text = (ROOT / 'platform/deploy/gameplay_install_vm.sh').read_text()
        text = text.replace('/usr/metin2-gameplay-', str(self.root / 'metin2-gameplay-'))
        text = text.replace('/usr/home', str(self.home))
        text = text.replace('sleep 1', 'sleep 0')
        self.script = self.stage / 'install.sh'
        self.write(self.script, text)
        self.write(self.stage / 'READY', '')
        locale = 'share/locale/europe/'
        self.sources = {
            'share/bin/game': 'out/game',
            'share/bin/db': 'out/db',
            locale + 'mob_drop_item.txt': 'runtime/freebsd/' + locale + 'mob_drop_item.txt',
            locale + 'quest/object/notarget/login/welcome.start': 'quest-check/object/notarget/login/welcome.start',
            locale + 'quest/object/state/welcome': 'quest-check/object/state/welcome',
            locale + 'quest/quest_tr/_npc_talk_mission/welcome.lua': 'runtime/freebsd/' + locale + 'quest/quest_tr/_npc_talk_mission/welcome.lua',
        }
        for target, source in self.sources.items():
            self.write(self.home / target, 'previous:' + target, 0o755 if '/bin/' in target else 0o644)
            self.write(self.stage / source, 'candidate:' + target, 0o755 if '/bin/' in target else 0o644)
        self.config = self.home / 'main/channels/channel1/core1/CONFIG'
        self.write(self.config, 'SQL_PASSWORD: fixture-only\nMAX_LEVEL: 105\nPORT: 30101\n')
        self.auth = self.home / 'main/auth/CONFIG'
        self.write(self.auth, 'AUTH_SERVER: master\n')
        self.original = {path: path.read_bytes() for path in self.home.rglob('*') if path.is_file()}

    def write(self, path, text, mode=0o644):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)
        path.chmod(mode)

    def run_action(self, action):
        return subprocess.run(['/bin/sh', str(self.script), action, str(self.stage)],
                              env=self.env, text=True, capture_output=True)

    def assert_original(self):
        for path, content in self.original.items():
            self.assertEqual(path.read_bytes(), content, str(path))

    def seed_density_maps(self):
        self.maps = ['map/test_map1/stone.txt', 'map/test_map2/stone.txt']
        for relative in self.maps:
            path = self.home / 'share/locale/europe' / relative
            self.write(path, 'm\t100\t100\t50\t50\t0\t0\t1800s\t100\t1\t8001\n')
            self.original[path] = path.read_bytes()

    def density_payload(self):
        self.write(self.stage / 'density-files.txt', '\n'.join(self.maps) + '\n')
        desired, baseline = [], []
        for relative in self.maps:
            live = self.home / 'share/locale/europe' / relative
            data = live.read_bytes() * 2
            source = self.stage / 'density' / relative
            self.write(source, data.decode())
            desired.append('SHA256 (density/%s) = %s' % (relative, hashlib.sha256(data).hexdigest()))
            baseline.append('SHA256 (%s) = %s' % (live, hashlib.sha256(live.read_bytes()).hexdigest()))
        self.write(self.stage / 'density.sha256', '\n'.join(desired) + '\n')
        self.write(self.stage / 'density-baseline.sha256', '\n'.join(baseline) + '\n')

    def test_prepare_does_not_touch_live_files_or_services(self):
        result = self.run_action('prepare')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assert_original()
        self.assertFalse((self.root / 'events').exists())

    def test_install_then_rollback_restores_all_files(self):
        self.assertEqual(self.run_action('prepare').returncode, 0)
        result = self.run_action('install')
        self.assertEqual(result.returncode, 0, result.stderr)
        for target, source in self.sources.items():
            self.assertEqual((self.home / target).read_bytes(), (self.stage / source).read_bytes())
        self.assertIn('MAX_LEVEL: 99', self.config.read_text())
        self.assertIn('SQL_PASSWORD: fixture-only', self.config.read_text())
        self.assertEqual(self.auth.read_bytes(), self.original[self.auth])
        result = self.run_action('rollback')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assert_original()
        self.assertFalse((self.stage / 'INSTALLED').exists())

    def test_changed_live_data_blocks_install_before_service_stop(self):
        self.assertEqual(self.run_action('prepare').returncode, 0)
        self.config.write_text('operator changed config\n')
        result = self.run_action('install')
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(self.config.read_text(), 'operator changed config\n')
        self.assertFalse((self.root / 'events').exists())

    def test_failed_start_rolls_back(self):
        self.assertEqual(self.run_action('prepare').returncode, 0)
        self.write(self.root / 'fail-once', '')
        result = self.run_action('install')
        self.assertNotEqual(result.returncode, 0)
        self.assert_original()
        self.assertFalse((self.stage / 'INSTALL_STARTED').exists())
        self.assertEqual((self.root / 'events').read_text().splitlines(),
                         ['stop', 'start', 'stop', 'start', 'status'])

    def test_missing_backup_is_reported_without_truncating_live_file(self):
        self.assertEqual(self.run_action('prepare').returncode, 0)
        self.assertEqual(self.run_action('install').returncode, 0)
        (self.stage / 'previous/2').unlink()
        current = (self.home / 'share/bin/db').read_bytes()
        result = self.run_action('rollback')
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('ROLLBACK INCOMPLETE', result.stderr)
        self.assertEqual((self.home / 'share/bin/db').read_bytes(), current)
        self.assertTrue((self.stage / 'INSTALL_STARTED').exists())

    def test_successful_rc_status_cannot_hide_missing_game_core(self):
        self.assertEqual(self.run_action('prepare').returncode, 0)
        self.env['FAIL_PROCESS_HEALTH'] = '1'
        result = self.run_action('install')
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('HEALTH FAILED', result.stderr)
        self.assert_original()

    def test_all_processes_without_all_ports_trigger_rollback(self):
        self.assertEqual(self.run_action('prepare').returncode, 0)
        self.env['FAIL_SOCKET_HEALTH'] = '1'
        result = self.run_action('install')
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('HEALTH FAILED', result.stderr)
        self.assert_original()

    def test_density_stage_is_read_only_and_install_rollback_restores_maps(self):
        self.seed_density_maps()
        self.assertEqual(self.run_action('prepare').returncode, 0)
        self.density_payload()
        result = self.run_action('append-density')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assert_original()
        self.assertFalse((self.root / 'events').exists())
        self.assertTrue((self.stage / 'DENSITY_READY').exists())
        result = self.run_action('install')
        self.assertEqual(result.returncode, 0, result.stderr)
        for relative in self.maps:
            live = self.home / 'share/locale/europe' / relative
            self.assertEqual(live.read_bytes(), (self.stage / 'density' / relative).read_bytes())
            self.assertNotIn('MAX_LEVEL', live.read_text())
        self.assertEqual(self.run_action('rollback').returncode, 0)
        self.assert_original()

    def test_density_changed_live_baseline_blocks_staging(self):
        self.seed_density_maps()
        self.assertEqual(self.run_action('prepare').returncode, 0)
        self.density_payload()
        target = self.home / 'share/locale/europe' / self.maps[0]
        target.write_text('operator changed map\n')
        paths = (self.stage / 'previous/paths').read_bytes()
        result = self.run_action('append-density')
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse((self.stage / 'DENSITY_READY').exists())
        self.assertEqual((self.stage / 'previous/paths').read_bytes(), paths)
        self.assertEqual(target.read_text(), 'operator changed map\n')

    def test_density_path_traversal_is_rejected(self):
        self.seed_density_maps()
        self.assertEqual(self.run_action('prepare').returncode, 0)
        self.density_payload()
        self.write(self.stage / 'density-files.txt', 'map/../stone.txt\n')
        self.assertNotEqual(self.run_action('append-density').returncode, 0)
        self.assert_original()

    def test_density_candidate_edit_after_stage_blocks_install(self):
        self.seed_density_maps()
        self.assertEqual(self.run_action('prepare').returncode, 0)
        self.density_payload()
        self.assertEqual(self.run_action('append-density').returncode, 0)
        self.write(self.stage / 'density' / self.maps[0], 'changed candidate\n')
        self.assertNotEqual(self.run_action('install').returncode, 0)
        self.assert_original()
        self.assertFalse((self.root / 'events').exists())

    def test_density_map_change_after_stage_blocks_install(self):
        self.seed_density_maps()
        self.assertEqual(self.run_action('prepare').returncode, 0)
        self.density_payload()
        self.assertEqual(self.run_action('append-density').returncode, 0)
        target = self.home / 'share/locale/europe' / self.maps[0]
        target.write_text('changed live map\n')
        self.assertNotEqual(self.run_action('install').returncode, 0)
        self.assertEqual(target.read_text(), 'changed live map\n')
        self.assertFalse((self.root / 'events').exists())


if __name__ == '__main__':
    unittest.main()
