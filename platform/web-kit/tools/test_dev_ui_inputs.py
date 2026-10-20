from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

import dev_ui_inputs


class UiInputTests(unittest.TestCase):
    def test_overlay_and_deletion_preserve_other_unpacked_packs(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            inputs, scripts, state = root / 'inputs', root / 'scripts', root / 'state.json'
            (inputs / 'root').mkdir(parents=True)
            (inputs / 'locale' / 'tr').mkdir(parents=True)
            scripts.mkdir()
            (scripts / 'system.py').write_text('baseline')
            (scripts / 'other_pack.py').write_text('keep')
            source = inputs / 'root' / 'uiwindow.py'
            source.write_text('window')
            (inputs / 'locale' / 'tr' / 'locale_game.txt').write_text('translation')
            with patch.object(sys, 'argv', ['dev_ui_inputs.py', str(inputs), str(scripts), str(state)]):
                dev_ui_inputs.main()
                self.assertEqual((scripts / 'uiwindow.py').read_text(), 'window')
                self.assertEqual((scripts / 'locale/tr/locale_game.txt').read_text(), 'translation')
                source.unlink()
                dev_ui_inputs.main()
            self.assertFalse((scripts / 'uiwindow.py').exists())
            self.assertEqual((scripts / 'other_pack.py').read_text(), 'keep')
            self.assertEqual((scripts / 'system.py').read_text(), 'baseline')
