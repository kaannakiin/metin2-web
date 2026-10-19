#!/usr/bin/env python3
"""Assert mid-pvp SAFE map indices exist in locale map/index and in pvp_safe_maps.h."""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
INDEX = ROOT / "runtime/freebsd/share/locale/europe/map/index"
HDR = ROOT / "apps/server/game/src/pvp_safe_maps.h"


def parse_index(path: Path) -> dict[int, str]:
    out: dict[int, str] = {}
    for line in path.read_text(encoding="latin-1", errors="replace").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split()
        if len(parts) < 2:
            continue
        try:
            out[int(parts[0])] = parts[1]
        except ValueError:
            continue
    return out


def parse_safe_list(hdr: Path) -> list[int]:
    text = hdr.read_text(encoding="utf-8", errors="replace")
    m = re.search(
        r"kMidPvpSafeMapIndex\s*\[\s*\]\s*=\s*\{([^}]+)\}",
        text,
        re.S,
    )
    if not m:
        raise SystemExit("kMidPvpSafeMapIndex array not found in pvp_safe_maps.h")
    body = re.sub(r"//.*?$", "", m.group(1), flags=re.M)
    return [int(x) for x in re.findall(r"\d+", body)]


def main() -> int:
    if not HDR.is_file():
        print(f"FAIL missing {HDR}", file=sys.stderr)
        return 1
    index = parse_index(INDEX)
    safe = parse_safe_list(HDR)
    if not safe:
        print("FAIL empty safe list", file=sys.stderr)
        return 1
    errs = 0
    for idx in safe:
        if idx not in index:
            print(f"FAIL safe map {idx} not in map/index", file=sys.stderr)
            errs += 1
        else:
            print(f"OK  safe {idx} -> {index[idx]}")
    # Required villages / guild / ox / duel lobby
    required = {1, 21, 41, 6, 26, 46, 4, 24, 44, 112, 113, 81}
    missing = required - set(safe)
    if missing:
        print(f"FAIL required safe maps not listed: {sorted(missing)}", file=sys.stderr)
        errs += 1
    else:
        print("OK  required village/guild/ox/duel/wedding in safe set")
    return 1 if errs else 0


if __name__ == "__main__":
    sys.exit(main())
