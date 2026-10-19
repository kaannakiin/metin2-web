#!/usr/bin/env python3
"""Offline 1-99 exp-time simulation for mid-easy PvP (PVP_HEDEF.md).

Parses exp_table_common + GetMidPvpMobExpRate from constants.cpp, estimates
same-level mob EXP from mob_proto.txt median, applies the server kill cap
(nextExp/10), and reports hours at KILLS_PER_HOUR.

Exit 0 if total active farm hours in [MIN_HOURS, MAX_HOURS]; else 1.
"""
from __future__ import annotations

import argparse
import re
import statistics
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CONSTANTS = ROOT / "apps/server/game/src/constants.cpp"
MOB_PROTO = ROOT / "runtime/freebsd/main/db/mob_proto.txt"

KILLS_PER_HOUR = 1500
MIN_HOURS = 8.0
MAX_HOURS = 12.0
# Travel/quest pad for 1-30 (PVP_HEDEF); pure farm sim understates early game.
EARLY_PAD_HOURS = 0.8


def get_mid_pvp_mob_exp_rate(level: int) -> int:
    """Mirror GetMidPvpMobExpRate (percent, 100 = 1x). Keep in sync with constants.cpp."""
    if level < 30:
        return 3500
    if level < 70:
        return 3800
    if level < 90:
        return 14000
    if level < 99:
        return 22000
    return 100


def parse_exp_table(text: str) -> list[int]:
    m = re.search(
        r"exp_table_common\[PLAYER_EXP_TABLE_MAX\s*\+\s*1\]\s*=\s*\{(.*?)\n\};",
        text,
        re.S,
    )
    if not m:
        raise SystemExit("exp_table_common not found in constants.cpp")
    body = m.group(1)
    # Stop before ENABLE_LEVEL_INT extension values for levels > 115-ish; we only need 0..99
    vals: list[int] = []
    for tok in re.finditer(r"(\d+)u?", body):
        vals.append(int(tok.group(1)))
        if len(vals) > 120:
            break
    if len(vals) < 100:
        raise SystemExit(f"exp_table too short: {len(vals)}")
    return vals


def parse_rate_from_source(text: str) -> None:
    """Sanity-check that C++ rates still match this script's mirror."""
    if "GetMidPvpMobExpRate" not in text:
        raise SystemExit("GetMidPvpMobExpRate missing from constants.cpp")
    for level, rate in ((10, 3500), (50, 3800), (80, 14000), (95, 22000)):
        if get_mid_pvp_mob_exp_rate(level) != rate:
            raise SystemExit(f"script rate mismatch at level {level}")
    for rate in (3500, 3800, 14000, 22000):
        if not re.search(rf"return\s+{rate}\s*;", text):
            raise SystemExit(f"expected return {rate} in GetMidPvpMobExpRate")


def median_mob_exp_by_level(path: Path) -> dict[int, int]:
    by_lv: dict[int, list[int]] = defaultdict(list)
    with path.open("r", encoding="latin-1", errors="replace") as f:
        header = f.readline().rstrip("\n").split("\t")
        try:
            i_lv = header.index("Level")
            i_exp = header.index("Exp")
            i_type = header.index("Type")
        except ValueError as e:
            raise SystemExit(f"mob_proto columns: {e}") from e
        for line in f:
            parts = line.rstrip("\n").split("\t")
            if len(parts) <= max(i_lv, i_exp, i_type):
                continue
            if parts[i_type] != "MONSTER":
                continue
            try:
                lv = int(parts[i_lv])
                exp = int(parts[i_exp])
            except ValueError:
                continue
            if 1 <= lv <= 99 and exp > 0:
                by_lv[lv].append(exp)
    out: dict[int, int] = {}
    for lv, exps in by_lv.items():
        out[lv] = int(statistics.median(exps))
    return out


def kills_for_level(need: int, base_mob_exp: int, rate_pct: int) -> int:
    """Kills to earn `need` EXP with same-level mob and mid-pvp rate + nextExp/10 cap."""
    if need <= 0:
        return 0
    scaled = max(1, base_mob_exp * rate_pct // 100)
    cap = max(1, need // 10)
    per = min(cap, scaled)
    # exact kill count (constant per-kill gain while leveling this step)
    return (need + per - 1) // per


def simulate(exp_table: list[int], mob_exp: dict[int, int], kills_per_hour: int) -> dict:
    bands = {
        "1-29": (1, 29, 0.0, 0),
        "30-69": (30, 69, 0.0, 0),
        "70-89": (70, 89, 0.0, 0),
        "90-98": (90, 98, 0.0, 0),
    }
    total_kills = 0
    for level in range(1, 99):
        need = exp_table[level]  # GetNextExp at level L uses exp_table[L]
        base = mob_exp.get(level)
        if base is None:
            # fallback: nearest lower
            for d in range(1, 20):
                if level - d in mob_exp:
                    base = mob_exp[level - d]
                    break
                if level + d in mob_exp:
                    base = mob_exp[level + d]
                    break
        if base is None:
            base = max(15, level * 40)
        rate = get_mid_pvp_mob_exp_rate(level)
        k = kills_for_level(need, base, rate)
        total_kills += k
        hours = k / kills_per_hour
        for name, (lo, hi, _, _) in list(bands.items()):
            if lo <= level <= hi:
                bands[name] = (lo, hi, bands[name][2] + hours, bands[name][3] + k)
                break
    farm_hours = total_kills / kills_per_hour
    # early pad
    bands["1-29"] = (
        bands["1-29"][0],
        bands["1-29"][1],
        bands["1-29"][2] + EARLY_PAD_HOURS,
        bands["1-29"][3],
    )
    total_hours = farm_hours + EARLY_PAD_HOURS
    return {
        "bands": bands,
        "farm_hours": farm_hours,
        "total_hours": total_hours,
        "total_kills": total_kills,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--kills-per-hour", type=int, default=KILLS_PER_HOUR)
    ap.add_argument("--min-hours", type=float, default=MIN_HOURS)
    ap.add_argument("--max-hours", type=float, default=MAX_HOURS)
    ap.add_argument("--no-assert", action="store_true", help="print only, never fail")
    args = ap.parse_args()

    text = CONSTANTS.read_text(encoding="utf-8", errors="replace")
    parse_rate_from_source(text)
    exp_table = parse_exp_table(text)
    mob_exp = median_mob_exp_by_level(MOB_PROTO)
    result = simulate(exp_table, mob_exp, args.kills_per_hour)

    print("mid_pvp_exp_sim")
    print(f"  kills/h={args.kills_per_hour}  early_pad={EARLY_PAD_HOURS}h")
    for name, (lo, hi, hours, kills) in result["bands"].items():
        print(f"  band {name:6}  levels {lo}-{hi}  kills={kills:8d}  hours={hours:6.2f}")
    print(f"  farm_hours={result['farm_hours']:.2f}")
    print(f"  total_hours={result['total_hours']:.2f}  (target {args.min_hours}-{args.max_hours})")

    ok = args.min_hours <= result["total_hours"] <= args.max_hours
    if args.no_assert:
        return 0
    if not ok:
        print(
            f"FAIL: total_hours {result['total_hours']:.2f} outside "
            f"[{args.min_hours}, {args.max_hours}] — tune GetMidPvpMobExpRate",
            file=sys.stderr,
        )
        return 1
    print("OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
