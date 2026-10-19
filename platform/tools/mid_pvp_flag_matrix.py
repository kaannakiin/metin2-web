#!/usr/bin/env python3
"""Assert mid-pvp feature flag matrix in service.h + Locale_inc.h.

Yohara/Conqueror must be OFF; core QoL flags must be ON.
Respects #if / #ifdef nesting so children under a disabled parent stay off.
ACCE/Aura/Dragon Soul may stay defined (power gated by content, not undef).
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SERVICE = ROOT / "apps/server/common/service.h"
LOCALE = ROOT / "apps/client/source/UserInterface/Locale_inc.h"

MUST_OFF = (
    "ENABLE_YOHARA_SYSTEM",
    "ENABLE_CONQUEROR_LEVEL",
    "ENABLE_CONQUEROR_LEVEL_UPDATE",
    "ENABLE_PASSIVE_SYSTEM",
    "ENABLE_NINETH_SKILL",
)

MUST_ON = (
    "__AUTO_HUNT__",
    "ENABLE_RENEWAL_SWITCHBOT",
    "ENABLE_RENEWAL_OFFLINESHOP",
    "ENABLE_BIOLOGIST_SYSTEM",
    "ENABLE_BATTLE_PASS",
    "ENABLE_MULTI_FARM_BLOCK",
)

OPTIONAL_ON = (
    "ENABLE_ACCE_COSTUME_SYSTEM",
    "ENABLE_AURA_COSTUME_SYSTEM",
    "ENABLE_DRAGON_SOUL_SYSTEM",
)


def active_defines(text: str) -> set[str]:
    """Active #define names with simple #ifdef/#ifndef/#if/#else/#endif stacking."""
    defined: set[str] = set()
    # stack of whether current branch is live
    live = [True]

    def currently_live() -> bool:
        return all(live)

    for raw in text.splitlines():
        s = raw.strip()
        if s.startswith("//"):
            continue

        m_ifdef = re.match(r"#\s*ifdef\s+([A-Za-z_][A-Za-z0-9_]*)\b", s)
        m_ifndef = re.match(r"#\s*ifndef\s+([A-Za-z_][A-Za-z0-9_]*)\b", s)
        m_if = re.match(r"#\s*if\b(.*)$", s)
        m_elif = re.match(r"#\s*elif\b", s)
        m_else = re.match(r"#\s*else\b", s)
        m_endif = re.match(r"#\s*endif\b", s)
        m_define = re.match(r"#\s*define\s+([A-Za-z_][A-Za-z0-9_]*)\b", s)

        if m_ifdef:
            name = m_ifdef.group(1)
            live.append(currently_live() and name in defined)
            continue
        if m_ifndef:
            name = m_ifndef.group(1)
            live.append(currently_live() and name not in defined)
            continue
        if m_if:
            # treat unknown #if as live only if parent live (conservative for #if 0)
            expr = m_if.group(1).strip()
            if expr == "0":
                live.append(False)
            else:
                live.append(currently_live())
            continue
        if m_elif:
            # flip: if sibling was taken, skip; simplistic — mark inactive
            if len(live) > 1:
                live[-1] = False
            continue
        if m_else:
            if len(live) > 1:
                parent = all(live[:-1])
                live[-1] = parent and not live[-1]
            continue
        if m_endif:
            if len(live) > 1:
                live.pop()
            continue
        if m_define and currently_live():
            defined.add(m_define.group(1))

    return defined


def check_file(path: Path) -> list[str]:
    errs: list[str] = []
    text = path.read_text(encoding="latin-1", errors="replace")
    active = active_defines(text)
    rel = path.relative_to(ROOT)

    for name in MUST_OFF:
        if name in active:
            errs.append(f"{rel}: {name} still active (must be off)")
        else:
            print(f"OK  {rel}: {name} off")

    for name in MUST_ON:
        if name not in active:
            errs.append(f"{rel}: {name} missing active #define")
        else:
            print(f"OK  {rel}: {name} on")

    for name in OPTIONAL_ON:
        if name in active:
            print(f"OK  {rel}: {name} on (content-gated power)")
        else:
            print(f"NOTE {rel}: {name} not defined")

    return errs


def main() -> int:
    errs: list[str] = []
    errs += check_file(SERVICE)
    errs += check_file(LOCALE)
    print(f"\n{len(errs)} fail")
    for e in errs:
        print(f"FAIL {e}", file=sys.stderr)
    return 1 if errs else 0


if __name__ == "__main__":
    sys.exit(main())
