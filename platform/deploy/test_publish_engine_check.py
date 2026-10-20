from pathlib import Path
import shutil
import tempfile
import unittest

from publish_engine_check import check


class PublishEngineTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.source = Path(self.temporary.name) / 'source'
        self.published = Path(self.temporary.name) / 'published'
        self.source.mkdir()
        for name in ('manifest.bin', 'groups.txt'):
            (self.source / name).write_bytes(b'current')
        for number in range(1001):
            (self.source / ('%032x.bin' % number)).write_bytes(b'x')
        shutil.copytree(self.source, self.published)

    def test_identical_corpus_allowed(self):
        check(self.source, self.published)

    def test_changed_manifest_rejected(self):
        (self.source / 'manifest.bin').write_bytes(b'new')
        with self.assertRaises(ValueError):
            check(self.source, self.published)

    def test_missing_chunk_rejected(self):
        (self.published / ('%032x.bin' % 500)).unlink()
        with self.assertRaises(ValueError):
            check(self.source, self.published)

    def test_changed_chunk_length_rejected(self):
        (self.published / ('%032x.bin' % 500)).write_bytes(b'short')
        with self.assertRaises(ValueError):
            check(self.source, self.published)


if __name__ == '__main__':
    unittest.main()
