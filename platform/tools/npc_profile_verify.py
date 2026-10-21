#!/usr/bin/env python3
"""Read-only check of the live shop backend against the canonical stock."""
import subprocess
import npc_profile


def main():
    tabs = sorted(npc_profile.stock(), key=lambda tab: tab[1])
    ids = ','.join(str(tab[1]) for tab in tabs)
    attributes = ','.join('attrtype%d,attrvalue%d' % (i, i) for i in range(7))
    query = (
        "SELECT 'S',vnum,name,npc_vnum FROM shopex WHERE vnum IN (%s) ORDER BY vnum;"
        "SELECT 'I',shop_vnum,item_vnum,`count`,price,price_vnum,price_type+0,"
        "socket0,socket1,socket2,%s FROM shopex_item WHERE shop_vnum IN (%s) "
        "ORDER BY shop_vnum,item_vnum;"
        "SELECT 'CONFLICT',vnum,npc_vnum FROM shop WHERE npc_vnum IN (9001,9002,9003,9007,9008);"
    ) % (ids, attributes, ids)
    expected = [['S', shop, name, npc] for npc, shop, name, rows in tabs]
    expected += [['I', shop, vnum, count, price, 0, 1] + [0] * 17
                 for npc, shop, name, rows in tabs
                 for vnum, count, price in sorted(rows)]
    expected = '\n'.join('\t'.join(map(str, row)) for row in expected) + '\n'
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
