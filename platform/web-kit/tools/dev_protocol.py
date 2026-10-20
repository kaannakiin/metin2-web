"""Explicit protocol presets for private previews against an older live server."""
from pathlib import Path

PROFILES = {"source": 594, "live-yohara": 619}


def apply(stage, profile):
    if profile not in PROFILES:
        raise ValueError("Unknown development protocol: " + profile)
    if profile == "source":
        return
    header = Path(stage) / "UserInterface/Locale_inc.h"
    original = header.read_bytes()
    prefix = (b"// Private preview: match the deployed Yohara-enabled server protocol.\n"
              b"#ifndef ENABLE_YOHARA_SYSTEM\n#define ENABLE_YOHARA_SYSTEM\n#endif\n")
    header.write_bytes(prefix + original)
