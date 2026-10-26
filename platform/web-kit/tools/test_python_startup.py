import ast
import contextlib
import io
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

import script_patches
from test_text_encoding import KIT, REPO, load_tool


class PythonStartupTests(unittest.TestCase):
    def test_real_pack_importer_keeps_python3_collections_and_traceback(self):
        source_path = REPO / 'content/client/packs/root/system.py'
        generated_path = os.environ.get('M2W_BOOT_SYSTEM')
        if not generated_path and not source_path.exists():
            self.skipTest('source system.py is not present on the build host')
        # Apply the actual Python-2-to-3 conversion and the actual system.py
        # patches, then execute the resulting import hook in a fresh Python.
        if generated_path:
            converted = Path(generated_path).read_text(encoding='utf-8')
        else:
            from lib2to3.refactor import RefactoringTool, get_fixers_from_package
            converted = str(RefactoringTool(get_fixers_from_package('lib2to3.fixes')).refactor_string(
                source_path.read_bytes().decode('latin1').replace('\r\n', '\n'), 'system.py'))
        data = load_tool('tools/build_client_data')
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            scripts = root / 'scripts'
            target = root / 'data'
            scripts.mkdir()
            target.mkdir()
            (scripts / 'system.py').write_text(converted, encoding='utf-8')
            entries = [entry for entry in script_patches.PATCHES_SCRIPTS if entry[0] == 'system.py']
            if not generated_path:
                with patch.object(script_patches, 'PATCHES_SCRIPTS', entries), contextlib.redirect_stdout(io.StringIO()):
                    script_patches.apply_all(str(scripts))
            tree = ast.parse((scripts / 'system.py').read_text())
            functions = [node for node in tree.body if isinstance(node, ast.FunctionDef)
                         and node.name in ('__pack_import', '_process_result')]
            hook = '\n\n'.join(ast.unparse(node) for node in functions)
            self.assertEqual(len(functions), 2)
            (scripts / 'collections.py').write_text('raise RuntimeError("legacy collections loaded")\n')
            (scripts / 'game_fixture.py').write_text('VALUE = "Savaş"\n', encoding='utf-8')
            data.SCRIPTS = str(scripts)
            data.TARGET = str(target)
            data.copy_scripts()
            data.copy_text_codec()
            self.assertFalse((target / 'collections.py').exists())
            self.assertTrue((target / 'game_fixture.py').exists())
            program = '''
import sys, os, builtins, types, io
sys.path.insert(0, os.getcwd())
assert 'collections' not in sys.modules
class Pack:
    def Exist(self, filename):
        if filename == 'collections.py':
            raise RuntimeError('legacy collections reached through pack importer')
        return os.path.isfile(filename)
pack = Pack()
def pack_file(filename, mode):
    with open(filename, encoding='utf-8') as source:
        return io.StringIO(source.read())
dbg = types.SimpleNamespace(Trace=lambda *args: None)
_ModuleType = type(sys)
module_do = lambda module: None
__USE_DYNAMIC_MODULE__ = False
old_import = builtins.__import__
''' + hook + '''
builtins.__import__ = __pack_import
import textcodec
import json
import collections.abc
import traceback
import game_fixture
assert game_fixture.VALUE == 'Savaş'
assert textcodec.ui_labels('locale/tr')['BATTLEPASS_FREE'] == 'Ücretsiz'
assert hasattr(sys.modules['collections'], '__path__')
try:
    raise ValueError('original startup exception remains visible')
except ValueError:
    message = traceback.format_exc()
assert 'ValueError: original startup exception remains visible' in message
print('pack importer + json + collections.abc + traceback: PASS')
'''
            result = subprocess.run([sys.executable, '-I', '-S', '-c', program],
                                    cwd=target, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
