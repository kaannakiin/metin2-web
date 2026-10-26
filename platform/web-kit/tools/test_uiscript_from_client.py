"""Regression coverage for layouts below UIScript/advanced_game_options/."""
import contextlib
import importlib.util
import io
from pathlib import Path
import sys
import tempfile
import types
import unittest
from unittest.mock import Mock, patch


class NestedLayoutTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.source = self.root / 'source'
        self.source.mkdir()
        self.scripts = self.root / 'scripts'
        self.scripts.mkdir()
        self.division = types.ModuleType('division')
        self.division.convert_divisions = Mock(
            side_effect=lambda text: (text.replace(' / 2', ' // 2'), 1, 0, set()))
        workspace = types.SimpleNamespace(PYTHON_2TO3=sys.executable, GAME_FILES='')
        spec = importlib.util.spec_from_file_location(
            'nested_layout_tool', Path(__file__).with_name('uiscript_from_client.py'))
        self.tool = importlib.util.module_from_spec(spec)
        with patch.dict(sys.modules, division=self.division, workspace=workspace):
            spec.loader.exec_module(self.tool)
        self.tool.ROOT = str(self.root)
        self.tool.SCRIPTS3 = str(self.scripts)
        self.tool.TARGET = str(self.root / 'result')

    def run_tool(self):
        rewrite = types.SimpleNamespace(
            normalize_utf8_cookie=lambda text: text,
            _decode_line=lambda line: line.decode('cp1254'))
        result = types.SimpleNamespace(returncode=0, stderr='')
        with patch.dict('os.environ', M2W_UISCRIPT_SOURCE=str(self.source)), \
                patch.dict(sys.modules, rewrite_scripts=rewrite), \
                patch.object(self.tool.subprocess, 'run', return_value=result), \
                contextlib.redirect_stdout(io.StringIO()):
            return self.tool.main()

    def test_nested_layouts_keep_paths_encoding_and_integer_coordinates(self):
        nested = self.source / 'advanced_game_options'
        nested.mkdir()
        (self.source / 'game_option_0.py').write_text('x = 4 / 2\n')
        (nested / 'game_option_0.py').write_bytes('title = "Seçenekler"\nx = 8 / 2\n'.encode('cp1254'))
        (nested / 'description.txt').write_bytes(b'\xfe\xff\x00')
        (self.scripts / 'options.py').write_text(
            'path = "UIScript/advanced_game_options/game_option_0.py"\n')
        self.assertIn('advanced_game_options/game_option_0.py', self.tool.spellings_from_client())
        self.assertEqual(self.run_tool(), 0)
        output = Path(self.tool.TARGET) / 'UIScript'
        self.assertEqual((output / 'game_option_0.py').read_text(), 'x = 4 // 2\n')
        generated = (output / 'advanced_game_options/game_option_0.py').read_text()
        namespace = {}
        exec(compile(generated, 'nested_layout', 'exec'), namespace)
        self.assertEqual(namespace['title'], 'Seçenekler')
        self.assertEqual(namespace['x'], 4)
        self.assertEqual(self.division.convert_divisions.call_count, 2)
        self.assertEqual((output / 'advanced_game_options/description.txt').read_bytes(), b'\xfe\xff\x00')

    def test_nested_syntax_error_fails_build(self):
        nested = self.source / 'advanced_game_options'
        nested.mkdir()
        (nested / 'broken.py').write_text('window = {\n')
        self.assertEqual(self.run_tool(), 1)

    def test_bytecode_is_excluded(self):
        cache = self.source / '__pycache__'
        cache.mkdir()
        (cache / 'cached.pyc').write_bytes(b'cache')
        (self.source / 'old.pyc').write_bytes(b'cache')
        self.assertEqual(self.tool.relative_files(str(self.source)), [])


if __name__ == '__main__':
    unittest.main()
