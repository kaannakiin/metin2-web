import importlib.util
from pathlib import Path
import sys
import tempfile
import types
import unittest
from unittest.mock import patch


class StageAliasTests(unittest.TestCase):
    def test_creating_entry_invalidates_all_directory_aliases(self):
        workspace = types.ModuleType('workspace')
        workspace.SOURCE_LIBRARIES = ''
        workspace.TREE = ''
        workspace.server_address = lambda: ''
        workspace.setting = lambda *args, default=None: default
        spec = importlib.util.spec_from_file_location(
            'stage_under_test', Path(__file__).resolve().parents[1] / 'stage_port.py')
        stage = importlib.util.module_from_spec(spec)
        with patch.dict(sys.modules, workspace=workspace):
            spec.loader.exec_module(stage)
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            real = root / 'real'
            real.mkdir()
            alias = root / 'alias'
            alias.symlink_to(real, target_is_directory=True)
            target = real / 'target.h'
            target.write_text('header')
            stage._listing(str(alias))
            self.assertEqual(stage._make_alias(str(root), str(real / 'new.h'), str(target)), 1)
            self.assertEqual(stage._make_alias(str(root), str(alias / 'new.h'), str(target)), 0)
            self.assertIn('new.h', stage._listing(str(alias)))
