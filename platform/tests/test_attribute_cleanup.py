import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location('cleanup', ROOT / 'platform/deploy/cleanup_invalid_attributes.py')
cleanup = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cleanup)


def item(vnum, pairs):
    row = {'id': '1', 'owner_id': '2', 'vnum': str(vnum), 'socket0': '123',
           'attrtype5': '80', 'attrvalue5': '10', 'attrtype6': '1', 'attrvalue6': '3000'}
    for i, (kind, value) in enumerate(pairs):
        row['attrtype' + str(i)] = str(kind)
        row['attrvalue' + str(i)] = str(value)
    return row


class CleanupTests(unittest.TestCase):
    def test_shield_keeps_valid_bonuses_and_compacts_normal_slots(self):
        old = item(13029, [(78, 5), (79, 3), (5, 12), (62, 5), (48, 1)])
        new, removed = cleanup.clean(old)
        self.assertEqual(removed, [(78, 5), (79, 3), (62, 5)])
        self.assertEqual([(new['attrtype'+str(i)], new['attrvalue'+str(i)]) for i in range(5)],
                         [('5', '12'), ('48', '1'), ('0', '0'), ('0', '0'), ('0', '0')])
        for field in ('socket0', 'attrtype5', 'attrvalue5', 'attrtype6', 'attrvalue6'):
            self.assertEqual(new[field], old[field])

    def test_natural_full_moon_addon_is_preserved(self):
        old = item(299, [(119, 35), (71, -8), (72, 10), (17, 10), (62, 3)])
        new, removed = cleanup.clean(old)
        self.assertEqual(removed, [(62, 3)])
        for i in range(4):
            self.assertEqual(new['attrtype'+str(i)], old['attrtype'+str(i)])
            self.assertEqual(new['attrvalue'+str(i)], old['attrvalue'+str(i)])

    def test_average_on_armor_is_removed_and_second_run_is_stable(self):
        old = item(11649, [(1, 3000), (72, 6), (17, 10), (73, 6), (48, 1)])
        new, removed = cleanup.clean(old)
        self.assertEqual(removed, [(72, 6), (73, 6)])
        self.assertEqual(cleanup.clean(new), (new, []))

    def test_no_invalid_bonuses_leaves_existing_slots_exactly_unchanged(self):
        old = item(13029, [(5, 12), (0, 0), (48, 1), (0, 0), (0, 0)])
        self.assertEqual(cleanup.clean(old), (old, []))

    def test_new_starter_weapons_do_not_force_monster_bonus(self):
        source = (ROOT / 'runtime/freebsd/share/locale/europe/quest/quest_tr/_npc_talk_mission/welcome.lua').read_text()
        self.assertNotIn(',63,10', source)
        self.assertIn('local weapon_bonus = {primary_stat,8,7,5,15,5,16,5}', source)


if __name__ == '__main__':
    unittest.main()
