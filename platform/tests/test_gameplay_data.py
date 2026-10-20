import ast
import importlib.util
from pathlib import Path
import re
import textwrap
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location('patches', ROOT / 'platform/web-kit/tools/script_patches.py')
patches = importlib.util.module_from_spec(spec)
spec.loader.exec_module(patches)


def groups():
    text = (ROOT / 'runtime/freebsd/share/locale/europe/mob_drop_item.txt').read_text()
    result = {}
    for name, body in re.findall(r'Group\s+(\S+)\s*\{([^{}]*)\}', text):
        if not name.startswith('MetinLv'):
            continue
        match = re.fullmatch(r'MetinLv(\d+)_(\d+)', name)
        assert match and name not in result
        mob = re.search(r'^\s*Mob\s+(\d+)\s*$', body, re.M)
        assert mob and int(mob[1]) == int(match[2])
        rows = [tuple(map(int, row)) for row in re.findall(
            r'^\s*(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s*$', body, re.M)]
        assert [row[0] for row in rows] == list(range(1, len(rows) + 1))
        assert re.search(r'^\s*Type\s+drop\s*$', body, re.M)
        result[name] = (int(match[1]), int(match[2]), [row[1:] for row in rows])
    return result


class GameplayDataTests(unittest.TestCase):
    def test_legacy_server_tooltip_keeps_finite_detector(self):
        with mock.patch.dict('os.environ', {'M2W_LEGACY_DETECTOR': '1'}):
            legacy = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(legacy)
        self.assertTrue(legacy.MID_PVP_DETECTOR_PATCHES)
        for rule in legacy.MID_PVP_DETECTOR_PATCHES:
            self.assertNotIn(rule, legacy.PATCHES_SCRIPTS)

    def test_all_23_metin_groups_have_independent_book_rolls(self):
        data = groups()
        self.assertEqual(len(data), 23)
        self.assertEqual({mob for _, mob, _ in data.values()},
                         set(range(8001, 8020)) | set(range(8024, 8028)))
        for level, mob, rows in data.values():
            count = 6 if level <= 20 else 10 if level <= 45 else 12 if level <= 70 else 14
            self.assertEqual([row for row in rows if row[0] == 50300], [(50300, 1, 400)] * count, mob)

    def test_bags_scrolls_and_progression_supplies(self):
        managed = {50300, 27999, 25040, 71084, 71085, 50513, 71001, 71094}
        for level, mob, rows in groups().values():
            if level <= 20:
                expected = [(27999,1,400), (25040,1,200), (71084,10,200), (71085,5,200)]
            elif level <= 70:
                expected = [(27999,2,400), (25040,1,400), (71084,15,240), (71085,8,240)]
            else:
                expected = [(27999,3,400), (25040,2,400), (71084,20,300), (71085,10,300)]
            supplies = 2 if level <= 20 else 4 if level <= 45 else 5 if level <= 70 else 6
            expected = [(71001,supplies,400), (71094,supplies,400)] + expected
            soul_pct = {40:20, 45:20, 50:60, 55:60, 60:120, 65:160, 70:200,
                        75:240, 80:240, 85:280, 90:320}
            if level in soul_pct:
                expected += [(50513,1,soul_pct[level])]
            actual = [row for row in rows if row[0] in managed and row[0] != 50300]
            self.assertEqual(actual, expected, mob)

    def detector_branch(self):
        old, new = next((old, new) for name, old, new, why in patches.PATCHES_SCRIPTS
                        if 'ordinary Metin detector' in why)
        original = (ROOT / 'content/client/packs/root/uitooltip.py').read_bytes().decode('latin1').replace('\r\n', '\n')
        self.assertEqual(original.count(old), 1)
        start = original.index(old)
        end = original.index('\n\t\t\telif 50004', start)
        branch = textwrap.dedent(original[start:end].replace(old, new, 1))
        return compile(ast.parse(branch), '<detector-tooltip>', 'exec')

    def test_unlimited_tooltip_and_alternate_charges(self):
        class Tooltip:
            NORMAL_COLOR = 'normal'
            def __init__(self): self.lines = []
            def AppendSpace(self, size): pass
            def AppendTextLine(self, text, color): self.lines.append(text)
        class Locale:
            TOOLTIP_REST_USABLE_COUNT = 'Kalan kullanım: %d'
            TOOLTIP_POTION_UNLIMITED = 'Süre: Sınırsız'
        branch = self.detector_branch()
        for vnum, socket, expected in [(27989,0,'Sınırsız'), (27989,5,'Sınırsız'), (76006,0,'6'), (76006,5,'1')]:
            tooltip = Tooltip()
            exec(branch, {'self': tooltip, 'localeInfo': Locale, 'itemVnum': vnum, 'metinSlot': [socket,0,0]})
            self.assertEqual(tooltip.lines, ['Kalan kullanım: ' + expected])

    def test_decoded_description_only_changes_ordinary_detector(self):
        old, new = next((old,new) for name,old,new,why in patches.PATCHES_SCRIPTS
                       if 'obsolete six-use description' in why)
        original = (ROOT / 'content/client/packs/root/uitooltip.py').read_bytes().decode('latin1').replace('\r\n','\n')
        self.assertEqual(original.count(old), 1)
        class Item:
            @staticmethod
            def GetItemDescription(): return '6 kez kullanılabilir.'
            @staticmethod
            def GetItemSummary(): return ''
        class Locale:
            TOOLTIP_POTION_UNLIMITED = 'Süre: Sınırsız'
        for vnum, expected in [(27989,'Sınırsız kez kullanılabilir.'), (76006,'6 kez kullanılabilir.')]:
            scope = {'item': Item, 'itemVnum': vnum, 'localeInfo': Locale}
            exec(compile(ast.parse(textwrap.dedent(new)), '<detector-description>', 'exec'), scope)
            self.assertEqual(scope['itemDesc'], expected)


if __name__ == '__main__':
    unittest.main()
