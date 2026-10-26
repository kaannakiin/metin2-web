import importlib.util
from pathlib import Path
import sys
import tempfile
import types
import unittest
from unittest.mock import patch


class LinkInputTests(unittest.TestCase):
    def test_cached_entry_objects_do_not_change_link_order(self):
        workspace = types.ModuleType('workspace')
        for name in ('COMPAT', 'EXTERN_INCLUDE', 'SITE', 'EMSDK'):
            setattr(workspace, name, '')
        spec = importlib.util.spec_from_file_location(
            'link_inputs_test', Path(__file__).with_name('link_client.py'))
        link = importlib.util.module_from_spec(spec)
        with patch.dict(sys.modules, workspace=workspace):
            spec.loader.exec_module(link)
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / 'engine').mkdir()
            for name in ('game.o', 'engine/ui.o', 'engine/main_web.o'):
                (root / name).touch()
            link.OBJDIR = temp
            first = link.collect_objects()
            for name in ('main_web.o', 'link_data.o'):
                (root / name).touch()
            self.assertEqual(link.collect_objects(), first)
            self.assertIn(str(root / 'engine/main_web.o'), first)
            self.assertEqual(len(first), 3)
