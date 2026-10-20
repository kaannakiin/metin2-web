#!/usr/bin/env python3
"""Build the current server tree separately; never install or restart services."""
import datetime
import pathlib
import subprocess
import tarfile
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[2]
HOST = "root@88.99.1.151"


def main():
    build_id = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%d-%H%M%S")
    remote = "/home/m2web/login-fix-" + build_id
    paths = subprocess.check_output(
        ["git", "ls-files", "--cached", "--others", "--exclude-standard", "-z", "--", "apps/server"], cwd=ROOT
    ).decode().split("\0")
    with tempfile.TemporaryDirectory(prefix="m2-login-fix-") as tmp:
        archive = pathlib.Path(tmp) / "source.tar.gz"
        with tarfile.open(archive, "w:gz") as out:
            for name in paths:
                if name and (ROOT / name).is_file() and not name.endswith((".o", ".a", ".d", ".core")):
                    out.add(ROOT / name, arcname=name, recursive=False)
        subprocess.run(["ssh", "-o", "BatchMode=yes", HOST, "mkdir -m 700 " + remote], check=True)
        subprocess.run(["scp", "-q", str(archive), str(ROOT / "platform/deploy/login_fix_vm.sh"),
                        str(ROOT / "platform/deploy/login_fix_host.sh"), HOST + ":" + remote + "/"], check=True)
    subprocess.run(["ssh", "-o", "BatchMode=yes", HOST,
                    "bash " + remote + "/login_fix_host.sh " + build_id], check=True)
    print("Prepared host directory:", remote)
    print("VM build directory: /usr/metin2-login-fix-" + build_id)


if __name__ == "__main__":
    main()
