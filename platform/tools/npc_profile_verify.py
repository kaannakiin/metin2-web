#!/usr/bin/env python3
"""Read-only check of the live shop backend against the canonical stock."""
import subprocess
import npc_profile


def main():
    tabs = sorted(npc_profile.stock(), key=lambda tab: tab[1])
    query = npc_profile.snapshot_sql()
    expected = npc_profile.snapshot()
    # Query has only fixed identifiers and numbers from the repository profile.
    remote = ('ssh -o BatchMode=yes -i /root/.ssh/metin2_vm root@192.168.122.10 '
              + '"mariadb -N -B player"')
    # Feed SQL explicitly through both SSH hops; the inner hop must read stdin.
    actual = subprocess.check_output(['ssh', '-o', 'BatchMode=yes', 'root@88.99.1.151', remote],
                                     input=query, text=True)
    if actual != expected:
        wanted, found = set(expected.splitlines()), set(actual.splitlines())
        raise SystemExit('Live SQL profile mismatch: %d missing, %d extra rows' %
                         (len(wanted - found), len(found - wanted)))
    print('Live renewed SQL profile matches: %d tabs, %d items, prices/counts/templates exact; no standard-shop conflicts.' %
          (len(tabs), sum(len(tab[3]) for tab in tabs)))


if __name__ == '__main__':
    main()
