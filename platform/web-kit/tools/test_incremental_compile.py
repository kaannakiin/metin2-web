"""Run with python3 -m unittest discover -s tools -p 'test_incremental_compile.py'."""

from pathlib import Path
import tempfile
import unittest

from incremental_compile import ObjectCache


@unittest.skipUnless(__import__('shutil').which('clang++') or __import__('shutil').which('c++'),
                     'A native C++ compiler is needed')
class ObjectCacheTests(unittest.TestCase):
    def setUp(self):
        import shutil
        self.compiler = shutil.which('clang++') or shutil.which('c++')
        self.temp = tempfile.TemporaryDirectory(prefix='m2-cache-test-')
        self.root = Path(self.temp.name) / 'source'
        self.root.mkdir()
        self.header = self.root / 'a header.h'
        self.source = self.root / 'main.cpp'
        self.output = Path(self.temp.name) / 'objects' / 'main.o'
        self.header.write_text('#define VALUE 1\n')
        self.source.write_text('#include "a header.h"\nint answer() { return VALUE; }\n')

    def tearDown(self):
        self.temp.cleanup()

    def build(self, flags=(), clean=False):
        cache = ObjectCache(self.compiler, clean=clean)
        result = cache.run([self.compiler, '-c', *flags, str(self.source), '-o', str(self.output)],
                           capture_output=True, text=True)
        return cache, result

    def test_unchanged_and_recreated_stage_are_reused(self):
        self.assertEqual(self.build()[1].returncode, 0)
        self.assertEqual(self.build()[0].reused, 1)
        content = self.source.read_bytes()
        self.source.unlink()
        self.source.write_bytes(content)
        self.assertEqual(self.build()[0].reused, 1)

    def test_source_header_and_flags_invalidate(self):
        self.build()
        self.header.write_text('#define VALUE 2\n')
        self.assertEqual(self.build()[0].compiled, 1)
        self.source.write_text(self.source.read_text() + 'int extra = 3;\n')
        self.assertEqual(self.build()[0].compiled, 1)
        self.assertEqual(self.build(['-O2'])[0].compiled, 1)
        self.assertEqual(self.build(['-O2'])[0].reused, 1)

    def test_failed_compile_removes_old_object(self):
        self.build()
        self.header.unlink()
        cache, result = self.build()
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse(self.output.exists())
        self.assertFalse(Path(str(self.output) + '.cache.json').exists())

    def test_prune_excluded_objects_and_force_clean(self):
        self.build()
        self.assertEqual(self.build(clean=True)[0].compiled, 1)
        obsolete = self.output.with_name('excluded.o')
        obsolete.write_bytes(b'old')
        cache, _ = self.build()
        self.assertEqual(cache.prune(self.output.parent), [str(self.output.resolve())])
        self.assertFalse(obsolete.exists())

    def test_new_local_header_invalidates_lookup(self):
        self.build()
        (self.root / 'new.h').write_text('#pragma once\n')
        self.assertEqual(self.build()[0].compiled, 1)

    def test_corrupt_object_or_stamp_is_rebuilt(self):
        self.build()
        self.output.write_bytes(b'corrupt')
        self.assertEqual(self.build()[0].compiled, 1)
        Path(str(self.output) + '.cache.json').write_text('{}')
        self.assertEqual(self.build()[0].compiled, 1)


if __name__ == '__main__':
    unittest.main()
