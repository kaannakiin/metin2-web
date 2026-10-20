#!/usr/bin/env python3
"""Stage and build gameplay changes without changing the running game."""
import argparse
import datetime
import hashlib
import json
import re
from pathlib import Path
import subprocess
import tarfile
import tempfile

ROOT = Path(__file__).resolve().parents[2]
HOST = "root@88.99.1.151"
RUNTIME = "runtime/freebsd/share/locale/europe/"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--resume', help='Retry an unfinished candidate after a build/test repair')
    args = parser.parse_args()
    if args.resume and not re.fullmatch(r'\d{8}-\d{6}', args.resume):
        parser.error('resume must be YYYYMMDD-HHMMSS')
    release = args.resume or datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%d-%H%M%S")
    remote = "/home/m2web/gameplay-" + release
    paths = subprocess.check_output(
        ["git", "ls-files", "--cached", "--others", "--exclude-standard", "-z", "--", "apps/server"],
        cwd=ROOT).decode().split("\0")
    paths += [RUNTIME + "mob_drop_item.txt",
              RUNTIME + "quest/quest_tr/_npc_talk_mission/welcome.lua",
              "platform/tests/detector_fixture.cpp", "platform/tests/lua_fixture.cpp",
              "platform/tests/gameplay_fixture.lua", "platform/deploy/login_server_layout.cpp",
              "platform/deploy/gameplay_vm.sh"]
    paths = sorted({p for p in paths if p and (ROOT / p).is_file()
                    and not p.endswith((".o", ".a", ".d", ".core"))})
    with tempfile.TemporaryDirectory(prefix="m2-gameplay-") as temporary:
        archive = Path(temporary) / "source.tar.gz"
        with tarfile.open(archive, "w:gz") as out:
            for name in paths:
                out.add(ROOT / name, arcname=name, recursive=False)
        manifest = Path(temporary) / "manifest.json"
        manifest.write_text(json.dumps({
            "release": release, "protocol": "source", "expected_login_bytes": 594,
            "files": {p: hashlib.sha256((ROOT / p).read_bytes()).hexdigest() for p in paths},
            "archive_sha256": hashlib.sha256(archive.read_bytes()).hexdigest(),
        }, indent=2) + "\n")
        command = "test -d " + remote if args.resume else "mkdir -m 700 " + remote
        subprocess.run(["ssh", "-o", "BatchMode=yes", HOST, command], check=True)
        subprocess.run(["scp", "-q", str(archive), str(manifest),
                        str(ROOT / "platform/deploy/gameplay_host.sh"), HOST + ":" + remote + "/"], check=True)
    subprocess.run(["ssh", "-o", "BatchMode=yes", HOST,
                    "bash " + remote + "/gameplay_host.sh " + release], check=True)
    print("Candidate:", remote)
    print("Live binaries, quests and drops were not changed.")


if __name__ == "__main__":
    main()
