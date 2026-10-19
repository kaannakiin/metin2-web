#!/usr/bin/env python3
"""Faz 2 QoL wiring asserts for mid-easy 1-99 PvP (offline)."""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PACK = ROOT / "content/client/packs/root"
CMD = ROOT / "apps/server/game/src/cmd_general.cpp"
LENGTH = ROOT / "apps/server/common/length.h"
CHAR_MGR = ROOT / "apps/server/game/src/char_manager.cpp"
OFFLINE = ROOT / "apps/server/game/src/offlineshop_manager.cpp"
LOCALE = ROOT / "apps/client/source/UserInterface/Locale_inc.h"
TELEPORT = PACK / "uiteleport.py"
BP = ROOT / "runtime/freebsd/share/locale/europe/battlepass_config.txt"
PET = ROOT / "apps/server/game/src/growth_pet.cpp"

# Combat / power vnums that must not appear as BP item rewards.
BP_DENYLIST = {
    39133,
    80013,
    39123,
    85001,
    149,  # example gear from old normal.txt if ever copied
}

errors: list[str] = []


def ok(msg: str) -> None:
    print(f"OK  {msg}")


def fail(msg: str) -> None:
    errors.append(msg)
    print(f"FAIL {msg}", file=sys.stderr)


def check_packs() -> None:
    for name in (
        "uiAutoHunt.py",
        "uiswitchbot.py",
        "uiofflineshop.py",
        "uibiologmanager.py",
        "uiteleport.py",
        "uibattlepass.py",
    ):
        if (PACK / name).is_file():
            ok(f"pack {name}")
        else:
            fail(f"missing pack {name}")


def check_cmds() -> None:
    text = CMD.read_text(encoding="latin-1", errors="replace")
    for sym in ("do_auto_hunt", "do_warp_on", "do_biyolog"):
        if re.search(rf"ACMD\s*\(\s*{sym}\s*\)", text):
            ok(f"ACMD({sym})")
        else:
            fail(f"ACMD({sym}) body missing in cmd_general.cpp")


def check_biolog_alias() -> None:
    text = LOCALE.read_text(encoding="latin-1", errors="replace")
    # Active defines with simple ifdef stack (same idea as flag_matrix)
    defined: set[str] = set()
    live = [True]

    def cur() -> bool:
        return all(live)

    for raw in text.splitlines():
        s = raw.strip()
        if s.startswith("//"):
            continue
        m_ifdef = re.match(r"#\s*ifdef\s+(\w+)", s)
        m_endif = re.match(r"#\s*endif\b", s)
        m_define = re.match(r"#\s*define\s+(\w+)", s)
        if m_ifdef:
            live.append(cur() and m_ifdef.group(1) in defined)
            continue
        if m_endif:
            if len(live) > 1:
                live.pop()
            continue
        if m_define and cur():
            defined.add(m_define.group(1))
    if "ENABLE_BIOLOGIST_SYSTEM" in defined and "ENABLE_BIOLOG_SYSTEM" in defined:
        ok("ENABLE_BIOLOG_SYSTEM alias active")
    else:
        fail("ENABLE_BIOLOG_SYSTEM alias missing under BIOLOGIST")


def check_multifarm() -> None:
    text = CHAR_MGR.read_text(encoding="latin-1", errors="replace")
    if re.search(r"farmPlayerCount\s*>=\s*2", text):
        ok("multi-farm limit >= 2")
    else:
        fail("multi-farm limit 2 not found")


def check_switchbot() -> None:
    text = LENGTH.read_text(encoding="latin-1", errors="replace")
    if re.search(r"SWITCHBOT_SLOT_COUNT\s*=\s*5", text):
        ok("SWITCHBOT_SLOT_COUNT == 5")
    else:
        fail("SWITCHBOT_SLOT_COUNT != 5")


def check_shop() -> None:
    text = OFFLINE.read_text(encoding="latin-1", errors="replace")
    if "2000000" in text and "20000000" in text:
        ok("offlineshop yang sinks 2M / 20M")
    else:
        fail("offlineshop yang sink constants missing")


def check_teleport() -> None:
    text = TELEPORT.read_text(encoding="latin-1", errors="replace")
    if re.search(r"'maxLevel':\s*1(?:10|20)", text):
        fail("uiteleport still has maxLevel 110/120")
    else:
        ok("uiteleport maxLevel capped (no 110/120)")
    for banned in ("MAP_CAPE", "MAP_DAWN", "MAP_BAY", "MAP_THUNDER", "MAP_MAGIC_FOREST", "MAP_ABANDONED_CASTLE"):
        if banned in text:
            fail(f"uiteleport still lists {banned}")
        else:
            ok(f"uiteleport no {banned}")
    if "MAP_A2" not in text or "MAP_DESERT" not in text:
        fail("uiteleport missing classic farm board (MAP_A2/DESERT)")
    else:
        ok("uiteleport classic farm board present")


def check_battlepass() -> None:
    if not BP.is_file():
        fail("battlepass_config.txt missing")
        return
    ok("battlepass_config.txt present")
    text = BP.read_text(encoding="utf-8", errors="replace")
    for tok in ("REWARDS_AND_NAME", "DO_MISSION", "FINAL_REWARD", "REWARDS_BONUS"):
        if tok not in text:
            fail(f"BP missing token {tok}")
        else:
            ok(f"BP has {tok}")
    # Collect item vnums from REWARDS_AND_NAME and FINAL_REWARD lines
    found: set[int] = set()
    for line in text.splitlines():
        s = line.strip()
        if not s or s.startswith("#"):
            continue
        parts = s.split()
        if not parts:
            continue
        if parts[0] in ("REWARDS_AND_NAME", "FINAL_REWARD"):
            nums = [int(x) for x in parts[1:] if x.isdigit()]
            # vnum/count pairs
            for i in range(0, min(len(nums), 6), 2):
                if nums[i] > 0:
                    found.add(nums[i])
        if parts[0] == "REWARDS_BONUS":
            nums = [int(x) for x in parts[1:] if x.isdigit()]
            if any(n != 0 for n in nums):
                fail("REWARDS_BONUS must be all zeros (no permanent BP combat affects)")
                return
    bad = found & BP_DENYLIST
    if bad:
        fail(f"BP denylist hit: {sorted(bad)}")
    else:
        ok(f"BP reward vnums clear of denylist ({len(found)} items)")


def check_pet_cap() -> None:
    text = PET.read_text(encoding="latin-1", errors="replace")
    if "no passive combat pet bonuses" in text or "Mid-easy 1-99 PvP (Faz 2)" in text:
        # ensure PASSIVE branch returns false
        if re.search(
            r"PET_SKILL_USE_TYPE_PASSIVE[\s\S]{0,200}?return false;",
            text,
        ):
            ok("growth pet passive combat disabled")
        else:
            fail("pet PASSIVE early-return not found")
    else:
        fail("pet mid-pvp passive cap comment/block missing")


def main() -> int:
    check_packs()
    check_cmds()
    check_biolog_alias()
    check_multifarm()
    check_switchbot()
    check_shop()
    check_teleport()
    check_battlepass()
    check_pet_cap()
    print(f"\n{len(errors)} fail")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
