import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'platform/tools'))
import npc_profile


class MarketTests(unittest.TestCase):
    def test_market_matches_approved_prices_and_removals(self):
        tabs = npc_profile.stock()
        market = {vnum: (count, price) for npc, shop, name, rows in tabs
                  if shop == 301 for vnum, count, price in rows}
        self.assertEqual(len(market), 24)
        self.assertEqual(market[70024], (1, 1000000))
        for vnum in npc_profile.PERMANENT_SUPPORT_IDS:
            self.assertEqual(market[vnum], (1, 1000))
        self.assertTrue(set([27001, 27002, 27004, 27005, 27102, 27105, 22000, 22010]).isdisjoint(market))
        self.assertEqual(market[27003], (200, 80000))
        self.assertEqual(market[27006], (200, 240000))
        self.assertEqual(market[72725], (1, 100000))
        self.assertEqual(market[72729], (1, 100000))

    def test_other_shops_preserved(self):
        original = subprocess.check_output(
            ['git', 'show', 'HEAD:platform/tools/npc_profile.py'], cwd=ROOT, text=True)
        scope = {'__file__': str(ROOT / 'platform/tools/npc_profile.py'), '__name__': 'baseline'}
        exec(compile(original, 'baseline_npc_profile', 'exec'), scope)
        self.assertEqual([tab for tab in npc_profile.stock() if tab[1] != 301],
                         [tab for tab in scope['stock']() if tab[1] != 301])

    def test_real_resale_method_caps_sphere_for_both_gold_widths(self):
        compiler = shutil.which('c++')
        self.assertIsNotNone(compiler, 'C++ compiler required for resale validation')
        source = (ROOT / 'apps/server/game/src/item.cpp').read_text()
        start = source.index('#ifdef ENABLE_GOLD_LIMIT\nlong long CItem::GetShopBuyPrice()')
        end = source.index('#ifdef ENABLE_AUTO_SELL_SYSTEM', start)
        method = source[start:end]
        fixture = '''#include <algorithm>
#include <cassert>
struct Proto { long long dwShopBuyPrice; };
struct CItem {
    unsigned vnum; Proto proto;
    unsigned GetVnum() const { return vnum; }
    Proto* GetProto() { return &proto; }
#ifdef ENABLE_GOLD_LIMIT
    long long GetShopBuyPrice();
#else
    int GetShopBuyPrice();
#endif
};
''' + method + '''
int main() {
    CItem sphere{70024,{30000000}}, other{70025,{30000000}}, cheaper{70024,{10}};
    assert(sphere.GetShopBuyPrice()==500000);
    assert(other.GetShopBuyPrice()==30000000);
    assert(cheaper.GetShopBuyPrice()==10);
}
'''
        with tempfile.TemporaryDirectory() as temporary:
            cpp, binary = Path(temporary) / 'resale.cpp', Path(temporary) / 'resale'
            cpp.write_text(fixture)
            for flags in ([], ['-DENABLE_GOLD_LIMIT']):
                subprocess.run([compiler, '-std=c++20', *flags, str(cpp), '-o', str(binary)], check=True, capture_output=True)
                subprocess.run([str(binary)], check=True)


if __name__ == '__main__':
    unittest.main()
