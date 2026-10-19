#!/usr/bin/env python3
"""Static checks for mid-easy PvP economy / starter / death / CONFIG.

Validates GetMidPvp* formulas, death item-drop call site, MAX_LEVEL 99 in
CONFIG files, shop/refine SQL snippets, and welcome.lua starter vnums.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CONSTANTS = ROOT / "apps/server/game/src/constants.cpp"
CHAR_BATTLE = ROOT / "apps/server/game/src/char_battle.cpp"
CONFIG_DIR = ROOT / "runtime/freebsd/main"
WELCOME = (
    ROOT
    / "runtime/freebsd/share/locale/europe/quest/quest_tr/_npc_talk_mission/welcome.lua"
)
SHOP_SQL = ROOT / "content/server/sql/update_mid_pvp_shop_plus9.sql"
REFINE_SQL = ROOT / "content/server/sql/update_mid_pvp_refine.sql"
SAFE_MAPS_HDR = ROOT / "apps/server/game/src/pvp_safe_maps.h"

errors: list[str] = []
oks: list[str] = []


def ok(msg: str) -> None:
    oks.append(msg)
    print(f"OK  {msg}")


def fail(msg: str) -> None:
    errors.append(msg)
    print(f"FAIL {msg}", file=sys.stderr)


def check_mid_pvp_formulas(text: str) -> None:
    def extract_return(fn: str) -> int | None:
        m = re.search(
            rf"int\s+{fn}\s*\([^)]*\)\s*\{{(.*?)\n\}}",
            text,
            re.S,
        )
        if not m:
            return None
        body = m.group(1)
        # last plain return N; for simple functions
        rets = re.findall(r"return\s+(\d+)\s*;", body)
        return int(rets[-1]) if rets else None

    gold_rate = extract_return("GetMidPvpGoldAmountRate")
    gold_cap = extract_return("GetMidPvpGoldKillCap")
    if gold_rate == 50:
        ok("GetMidPvpGoldAmountRate == 50")
    else:
        fail(f"GetMidPvpGoldAmountRate expected 50 got {gold_rate}")
    if gold_cap == 400000:
        ok("GetMidPvpGoldKillCap == 400000")
    else:
        fail(f"GetMidPvpGoldKillCap expected 400000 got {gold_cap}")

    # Metin yang formula: 500 + stoneLevel * 150
    if "500 + stoneLevel * 150" in text or "500 + stoneLevel*150" in text:
        ok("GetMidPvpMetinYang formula 500+lv*150")
    else:
        fail("GetMidPvpMetinYang formula not found")

    # Unit checks mirroring formula
    for lv, expect in ((1, 650), (50, 8000), (90, 14000), (99, 15350)):
        got = 500 + lv * 150
        if got != expect:
            fail(f"metin yang unit {lv}: {got} != {expect}")
    ok("metin yang unit table")


def check_death_penalties(text: str) -> None:
    if re.search(r"int\s+iLoss\s*=\s*0\s*;", text):
        ok("DeathPenalty iLoss = 0 (no EXP loss)")
    else:
        fail("DeathPenalty mid-pvp iLoss=0 not found")
    # Call site must remain commented
    if re.search(r"^\s*//\s*ItemDropPenalty\s*\(", text, re.M):
        ok("ItemDropPenalty call site commented out")
    elif re.search(r"^\s*ItemDropPenalty\s*\(", text, re.M):
        fail("ItemDropPenalty is active — must stay commented for mid-pvp")
    else:
        fail("ItemDropPenalty call site not found near PC death")


def check_configs() -> None:
    configs = list(CONFIG_DIR.rglob("CONFIG")) + list(
        (CONFIG_DIR / "config").glob("*")
    )
    # channel configs under main/config are files without extension
    checked = 0
    bad: list[str] = []
    for path in sorted(set(configs)):
        if not path.is_file():
            continue
        raw = path.read_text(encoding="utf-8", errors="replace")
        if "CHANNEL:" not in raw and "HOSTNAME:" not in raw and "PORT:" not in raw:
            continue
        # auth has no max_level usually
        if "auth" in path.name.lower() or "/auth/" in str(path).replace("\\", "/"):
            continue
        m = re.search(r"(?i)^MAX_LEVEL:\s*(\d+)", raw, re.M)
        if not m:
            # also accept PLAYER_MAX_LEVEL
            m = re.search(r"(?i)^PLAYER_MAX_LEVEL:\s*(\d+)", raw, re.M)
        if not m:
            bad.append(f"{path.relative_to(ROOT)}: missing MAX_LEVEL")
            continue
        checked += 1
        if int(m.group(1)) != 99:
            bad.append(f"{path.relative_to(ROOT)}: MAX_LEVEL={m.group(1)} want 99")
    if bad:
        for b in bad:
            fail(b)
    elif checked == 0:
        fail("no game CONFIG files found with MAX_LEVEL")
    else:
        ok(f"MAX_LEVEL 99 in {checked} CONFIG files")


def check_welcome() -> None:
    text = WELCOME.read_text(encoding="latin-1", errors="replace")
    # +9 starter body/helm via make_item0
    need = [11209, 12209, 11409, 12349, 11609, 12489, 11809, 12629, 13009, 14009]
    for v in need:
        if str(v) not in text:
            fail(f"welcome.lua missing vnum {v}")
            return
    ok("welcome.lua starter armor/acc vnums present")
    if "make_item0" not in text:
        fail("welcome.lua has no make_item0 (+9 path)")
    else:
        ok("welcome.lua uses make_item0")


def check_shop_sql() -> None:
    text = SHOP_SQL.read_text(encoding="utf-8", errors="replace")
    for shop in (1, 2, 6, 7):
        if f"shop_vnum = {shop}" not in text and f"shop_vnum={shop}" not in text:
            fail(f"shop SQL missing shop_vnum {shop}")
            return
    # sample +9 early weapons from PVP_HEDEF
    for v in (49, 1019, 2039, 11229, 59, 1029):
        if str(v) not in text:
            fail(f"shop plus9 SQL missing sample vnum {v}")
            return
    ok("update_mid_pvp_shop_plus9.sql shops 1/2/6/7 + sample +9 vnums")


def check_refine_sql() -> None:
    text = REFINE_SQL.read_text(encoding="utf-8", errors="replace")
    # Classic chain ends: +8->+9 id multiples often prob=35
    if "prob=35" not in text and "prob = 35" not in text:
        fail("refine SQL missing prob=35 (+9 step)")
    else:
        ok("refine SQL has +9-ish probs (35)")
    if "prob=70" not in text:
        fail("refine SQL missing prob=70 (+7 step)")
    else:
        ok("refine SQL has +7-ish probs (70)")


def check_safe_maps_header() -> None:
    if not SAFE_MAPS_HDR.is_file():
        fail(f"missing {SAFE_MAPS_HDR.relative_to(ROOT)} (Faz 1 pvp maps)")
        return
    text = SAFE_MAPS_HDR.read_text(encoding="utf-8", errors="replace")
    if "IsMidPvpSafeMap" not in text:
        fail("IsMidPvpSafeMap not declared")
    else:
        ok("pvp_safe_maps.h present")


def main() -> int:
    constants = CONSTANTS.read_text(encoding="utf-8", errors="replace")
    battle = CHAR_BATTLE.read_text(encoding="utf-8", errors="replace")
    check_mid_pvp_formulas(constants)
    check_death_penalties(battle)
    check_configs()
    check_welcome()
    check_shop_sql()
    check_refine_sql()
    check_safe_maps_header()

    print(f"\n{len(oks)} ok, {len(errors)} fail")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
