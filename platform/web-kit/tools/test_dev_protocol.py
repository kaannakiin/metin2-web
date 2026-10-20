from pathlib import Path
import tempfile
import unittest

import dev_protocol


class ProtocolTests(unittest.TestCase):
    def test_source_profile_preserves_bytes(self):
        with tempfile.TemporaryDirectory() as temporary:
            header = Path(temporary) / 'UserInterface/Locale_inc.h'
            header.parent.mkdir()
            original = b'#pragma once\r\n// cp1254: \xfd\xfe\r\n'
            header.write_bytes(original)
            dev_protocol.apply(temporary, 'source')
            self.assertEqual(header.read_bytes(), original)

    def test_live_profile_prefixes_only_staged_header(self):
        with tempfile.TemporaryDirectory() as temporary:
            header = Path(temporary) / 'UserInterface/Locale_inc.h'
            header.parent.mkdir()
            original = b'#pragma once\r\n//#define ENABLE_YOHARA_SYSTEM\r\n// \xfd\r\n'
            header.write_bytes(original)
            dev_protocol.apply(temporary, 'live-yohara')
            result = header.read_bytes()
            self.assertTrue(result.endswith(original))
            self.assertLess(result.index(b'#define ENABLE_YOHARA_SYSTEM\n'), result.index(b'#pragma once'))

    def test_unknown_profile_rejected(self):
        with self.assertRaises(ValueError):
            dev_protocol.apply('/unused', 'guess')


if __name__ == '__main__':
    unittest.main()
