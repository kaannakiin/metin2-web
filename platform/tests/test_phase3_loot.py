"""Loot integrity: real proto references, chest selection and progression gates."""
import csv
import json
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[2]
LOCALE = ROOT / 'runtime/freebsd/share/locale/europe'
POLICY = json.loads((ROOT / 'platform/gameplay/phase3_loot.json').read_text())


def groups(filename):
    return list(re.finditer(r'Group\s+(\S+)\s*\{([^{}]*)\}', (LOCALE / filename).read_text()))


def rows(body):
    return [tuple(map(int, m)) for m in re.findall(
        r'^\s*(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s*$', body, re.M)]


class Phase3LootTests(unittest.TestCase):
    def setUp(self):
        with (ROOT / 'runtime/freebsd/share/conf/item_proto.txt').open(encoding='latin1') as handle:
            self.items = {int(row['Vnum']): row for row in csv.DictReader(handle, delimiter='\t')
                          if row['Vnum'].isdigit()}
        with (ROOT / 'runtime/freebsd/share/conf/mob_proto.txt').open(encoding='latin1') as handle:
            self.mobs = {int(row['Vnum']): row for row in csv.DictReader(handle, delimiter='\t')}

    def test_all_rewards_exist_and_rows_are_contiguous(self):
        for filename in ('mob_drop_item.txt', 'special_item_group.txt'):
            names = set()
            for group in groups(filename):
                self.assertNotIn(group[1], names)
                names.add(group[1])
                if not group[1].startswith(('Phase3', 'MetinLv')):
                    continue
                entries = rows(group[2])
                self.assertEqual([row[0] for row in entries], list(range(1, len(entries) + 1)))
                for _, item, count, chance in entries:
                    self.assertIn(item, self.items, (group[1], item))
                    self.assertGreater(count, 0)
                    self.assertLessEqual(count, 200)
                    self.assertGreater(chance, 0)
                    if count > 1:
                        self.assertIn('ITEM_STACKABLE', self.items[item]['Flags'], (group[1], item))
                if filename == 'mob_drop_item.txt':
                    mob = int(re.search(r'\bMob\s+(\d+)', group[2])[1])
                    self.assertIn(mob, self.mobs)

    def test_every_boss_box_is_openable_with_one_weighted_reward(self):
        boxes = {}
        for group in groups('special_item_group.txt'):
            vnum = int(re.search(r'\bVnum\s+(\d+)', group[2])[1])
            self.assertNotIn(vnum, boxes)
            boxes[vnum] = group[2]
        drops = {int(re.search(r'\bMob\s+(\d+)', g[2])[1]): rows(g[2])
                 for g in groups('mob_drop_item.txt') if g[1].startswith('Phase3Boss_')}
        self.assertEqual(len(drops), 13)
        for boss in POLICY['bosses']:
            self.assertEqual(drops[boss['mob']], [(1, boss['chest'], 1, 400)])
            self.assertEqual(self.items[boss['chest']]['Type'], 'ITEM_GIFTBOX')
            body = boxes[boss['chest']]
            self.assertNotRegex(body, r'\bType\s+(pct|quest|special)')
            self.assertEqual(sum(row[3] for row in rows(body)), 100)
            self.assertEqual([list(row[1:]) for row in rows(body)], POLICY['chest_rewards'][boss['tier']])

    def test_soul_stones_start_at_40_and_increase_with_stone_level(self):
        last = 0
        for level, chance in sorted((int(k), v) for k, v in POLICY['soul_stone_pct'].items()):
            self.assertGreaterEqual(level, 40)
            self.assertGreaterEqual(chance, last)
            self.assertLessEqual(chance, 400)
            last = chance
        for group in groups('mob_drop_item.txt'):
            level = re.match(r'MetinLv(\d+)_', group[1])
            if not level:
                continue
            souls = [row[1:] for row in rows(group[2]) if row[1] == 50513]
            chance = POLICY['soul_stone_pct'].get(level[1])
            self.assertEqual(souls, [(50513, 1, chance)] if chance else [])

    def test_reaper_has_all_six_real_75_weapons_and_no_wrong_bow_id(self):
        expected = {180, 190, 1130, 2170, 3160, 5120}
        self.assertEqual(set(POLICY['reaper_75_weapons']), expected)
        rewards = POLICY['chest_rewards']['reaper']
        weapons = [row for row in rewards if row[0] in expected]
        self.assertEqual({row[0] for row in weapons}, expected)
        self.assertEqual(sum(row[2] for row in weapons), 30)
        for item, count, weight in weapons:
            self.assertEqual(self.items[item]['Type'], 'ITEM_WEAPON')
            self.assertEqual(self.items[item]['LimitValue0'], '75')
            self.assertEqual(self.items[item]['AddonType'], '-1')
            self.assertEqual((count, weight), (1, 5))
        self.assertNotIn(2150, [row[0] for row in rewards])
        for group in groups('mob_drop_item.txt'):
            if group[1].startswith('MetinLv'):
                self.assertFalse(expected.intersection(row[1] for row in rows(group[2])), group[1])

    def test_every_classic_chest_has_weapons_and_armour(self):
        for tier, rewards in POLICY['chest_rewards'].items():
            weapon_chance = sum(weight for item, count, weight in rewards
                                if self.items[item]['Type'] == 'ITEM_WEAPON')
            armour_chance = sum(weight for item, count, weight in rewards
                                if self.items[item]['Type'] == 'ITEM_ARMOR')
            self.assertEqual(weapon_chance, {'reaper':52, 'azrael':25}.get(tier,28), tier)
            self.assertEqual(armour_chance, {'reaper':12, 'azrael':49}.get(tier,12), tier)

    def test_reaper_also_has_the_verified_70_weapon_family(self):
        expected = {170,250,1120,3150,7150}
        self.assertEqual(set(POLICY['reaper_70_weapons']), expected)
        actual = [row for row in POLICY['chest_rewards']['reaper'] if row[0] in expected]
        self.assertEqual({row[0] for row in actual}, expected)
        self.assertEqual(sum(row[2] for row in actual), 15)
        for item, count, chance in actual:
            self.assertEqual(self.items[item]['LimitValue0'], '70')

    def test_all_previously_missing_bosses_have_real_drop_groups(self):
        expected = {591,993,1192,2092,2191,2291,2306,2307,2597,2598}
        by_mob = {int(re.search(r'\bMob\s+(\d+)', g[2])[1]): rows(g[2])
                  for g in groups('mob_drop_item.txt')}
        self.assertTrue(expected.issubset(by_mob))
        for boss in POLICY['direct_bosses']:
            self.assertEqual([list(row[1:]) for row in by_mob[boss['mob']]], boss['entries'])

    def test_late_forest_armour_is_plus_zero_66_and_stays_out_of_early_stones(self):
        armour = POLICY['red_forest_armour']
        for vnum in armour['vnums']:
            self.assertEqual(self.items[vnum]['SubType'], 'ARMOR_BODY')
            self.assertEqual(self.items[vnum]['LimitValue0'], '66')
            self.assertEqual(vnum % 10, 0)
        for group in groups('mob_drop_item.txt'):
            if not group[1].startswith('MetinLv'):
                continue
            actual = [row[1:] for row in rows(group[2]) if row[1] in armour['vnums']]
            if group[1].endswith('_8027'):
                self.assertEqual(actual, [(v, 1, 24) for v in armour['vnums']])
            else:
                self.assertEqual(actual, [])


if __name__ == '__main__':
    unittest.main()
