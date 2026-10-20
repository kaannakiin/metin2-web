#!/usr/bin/env python3
"""Render maintained ASCII mid-PvP quest profiles and level-independent access drops."""
import argparse
import json
from pathlib import Path
import re
import unicodedata

ROOT = Path(__file__).resolve().parents[2]
LOCALE = ROOT / 'runtime/freebsd/share/locale/europe'
ACCESS = {
    1093: [[30319, 2, 100]], 2091: [[30326, 1, 100]],
    2491: [[30179, 3, 100]], 2494: [[30179, 3, 100]],
    2492: [[30179, 3, 100], [30190, 1, 100]],
    2495: [[30179, 3, 100], [30190, 1, 100]],
    1191: [[30190, 1, 100]], 1192: [[30190, 1, 100]], 2493: [[30190, 1, 100]],
}
for mob, item in [(2001, 30057), (2002, 30056), (2003, 30025), (2004, 30058),
                  (2005, 30059), (2051, 30057), (2052, 30056), (2053, 30025),
                  (2054, 30058), (2055, 30059)]:
    ACCESS[mob] = [[item, 1, 25]]


def substitute(text, old, new, count=1):
    if text.count(old) != count:
        raise ValueError('Unexpected source pattern: ' + old[:90])
    return text.replace(old, new)


def entry(quest, npc, label, condition, level, ticket, count, destination, permission='', shared=False):
    map_id, x, y = destination
    allowed = 'pc.get_level() >= %d' % level
    if permission:
        allowed += ' and ' + permission
    allowed += ' and (pc.is_gm() or pc.getf("%s", "cooldown") <= get_global_time())' % quest
    when = '%d.chat."%s"' % (npc, label) if label else '%d.take' % npc
    if condition:
        when += ' with ' + condition
    cost = 'pc.count_item(%d) >= %d' % (ticket, count) if ticket else 'true'
    remove = 'pc.remove_item(%d, %d)' % (ticket, count) if ticket else '-- No ticket at this entry point.'
    member_cost = 'true' if shared else cost
    member_remove = '-- Shared entrance key is paid by the leader.' if shared else remove
    return '''        when %s begin
            say_title("Zindan girisi")
            say("Gerekli seviye: %d. Gunluk giris kotasi yok.")
            local choice = select("Yalniz", "Grupla", "Vazgec")
            if choice == 3 then return end
            if not (%s) or not (%s) then
                say("Seviye, hazirlik, anahtar veya bekleme kosulu eksik.")
                return
            end
            if choice == 1 then
                if party.is_party() then
                    say("Tek basina girmek icin once gruptan ayril.")
                    return
                end
                %s
                d.new_jump(%d, %d, %d)
            else
                if not party.is_party() or not party.is_leader() then
                    say("Grup lideri girisi baslatmali.")
                    return
                end
                local pids = {party.get_member_pids()}
                local origin = pc.get_map_index()
                local ready = party.get_near_count() == table.getn(pids)
                for i, pid in ipairs(pids) do
                    q.begin_other_pc_block(pid)
                    if pc.get_map_index() ~= origin or not (%s) or not (%s) then
                        ready = false
                    end
                    q.end_other_pc_block()
                end
                if not ready then
                    say("Tum uyeler yaninda olmali ve giris kosullarini tamamlamali.")
                    return
                end
                %s
                for i, pid in ipairs(pids) do
                    q.begin_other_pc_block(pid)
                    %s
                    q.end_other_pc_block()
                end
                d.new_jump_party(%d, %d, %d)
            end
            if d.select(d.get_map_index()) then
                d.setf("first_regen", 1)
                d.setf("DungeonBlock", 1)
            end
        end

''' % (when, level, allowed, cost, remove, map_id, x * 100, y * 100,
       allowed, member_cost, remove if shared else '-- Each member pays once below.',
       member_remove, map_id, x, y)


def profile(name):
    source = LOCALE / 'quest/quest_tr/_alldungeons' / (name + '.lua')
    text = source.read_bytes().decode('cp1254')
    text = unicodedata.normalize('NFKD', text.replace('\u0131', 'i')).encode('ascii', 'ignore').decode()
    text = text.replace('get_global_time()+60*60', 'get_global_time()+10*60')
    if name == 'deviltower_zone':
        text = substitute(text, '\t\t\tdeviltower_zone.clear_deviltower_flags()',
                          '\t\t\td.setqf2("midpvp_progression", "tower_done", 1)\n'
                          '\t\t\tdeviltower_zone.clear_deviltower_flags()')
    elif name == 'dragonlair':
        start = text.index('\t\twhen 30121.chat.')
        end = text.index('\t\twhen logout', start)
        text = text[:start] + entry(name, 30121, 'Ejderhanin Odasi', 'pc.get_map_index() == 73',
                                  75, 30179, 3, (208, 8436, 10669)) + text[end:]
    elif name == 'spider_dungeon':
        start = text.index('\t\twhen 20371.chat.')
        end = text.index('\t\twhen barones_1.server_timer', start)
        text = text[:start] + entry(name, 20371, "Barones'in Yuvasi", 'pc.get_map_index() == 217',
                                  50, 30324, 1, (217, 881, 6148),
                                  'pc.getf("midpvp_progression", "barones_ready") == 1') + text[end:]
        first = text.index('\t\t\t\t\td.spawn_mob(2095,')
        last = text.index('\t\t\t\t\td.setf("remain_egg", 9)', first)
        spawn = text[first:last] + '\t\t\t\t\td.setf("remain_egg", 9)\n'
        old = text[first:last + len('\t\t\t\t\td.setf("remain_egg", 9)\n')]
        text = substitute(text, old,
                          '                    d.spawn_name_mob(2094, 367, 588, "Orumcek Baronu")\n'
                          '                    d.setf("baron_dead", 0)\n'
                          '                    d.setf("barones_spawned", 0)\n')
        addition = '''        when 2094.kill with pc.get_map_index() >= 2170000 and pc.get_map_index() <= 2179990 begin
            if d.select(pc.get_map_index()) and d.getf("baron_dead") == 0 then
                d.setf("baron_dead", 1)
                game.drop_item_with_ownership(30327, 1)
                chat("Arachnida Flutu ile Baronesi cagir.")
            end
        end

        when 30327.use with pc.get_map_index() >= 2170000 and pc.get_map_index() <= 2179990 begin
            if d.select(pc.get_map_index()) and d.getf("baron_dead") == 1 and d.getf("barones_spawned") == 0 then
                if pc.count_item(30327) < 1 then return end
                d.setf("barones_spawned", 1)
                pc.remove_item(30327, 1)
SPAWN
                GetMissionInfo(2, 20*60)
            end
        end

'''.replace('SPAWN\n', spawn)
        text = text.replace('\t\twhen 2095.kill', addition + '\t\twhen 2095.kill', 1)
        text = text.replace('d.notice(index, 675', 'd.notice(pc.get_map_index(), 675')
        text = text.replace('d.notice(index, 676', 'd.notice(pc.get_map_index(), 676')
    elif name == 'devilcatacomb_zone':
        permission = 'pc.getf("midpvp_progression", "tower_done") == 1'
        start = text.index('\t\twhen 20367.chat.')
        end = text.index('\t\twhen kill with pc.get_map_index() == 216', start)
        text = text[:start] + entry(name, 20367, 'Seytanin Yeralti Mezari', '', 75, 0, 0,
                                  (216, 3622, 12077), permission) + text[end:]
        start = text.index('\t\twhen 30101.take')
        end = text.index('\t\twhen login', start)
        text = text[:start] + entry(name, 30101, '', 'pc.get_map_index() == 216 and item.get_vnum() == 30311',
                                  75, 30311, 1, (216, 3622, 12077), permission, shared=True) + text[end:]
        start = text.index('\t\twhen 30103.click')
        end = text.index('\t\twhen devilcatacomb_2.server_timer', start)
        text = text[:start] + '''        when 30103.click with pc.get_map_index() >= 2160000 and pc.get_map_index() <= 2169990 begin
            if not d.select(pc.get_map_index()) then return end
            if d.getf("level") ~= 2 or d.getf("tortoise_timer") ~= 1 or d.getf("head_paid") == 1 then return end
            local index = pc.get_map_index()
            local ready = true
            if party.is_party() then
                local pids = {party.get_member_pids()}
                for i, pid in ipairs(pids) do
                    q.begin_other_pc_block(pid)
                    if pc.get_map_index() == index and pc.count_item(30319) < 1 then ready = false end
                    q.end_other_pc_block()
                end
                if not ready then
                    say("Icerideki her uye icin bir Kuculen Kafa gerekli.")
                    return
                end
                d.setf("head_paid", 1)
                for i, pid in ipairs(pids) do
                    q.begin_other_pc_block(pid)
                    if pc.get_map_index() == index then pc.remove_item(30319, 1) end
                    q.end_other_pc_block()
                end
            else
                if pc.count_item(30319) < 1 then
                    say("Bir Kuculen Kafa gerekli.")
                    return
                end
                d.setf("head_paid", 1)
                pc.remove_item(30319, 1)
            end
            server_timer("devilcatacomb_2", 5, index)
            npc.purge()
        end

''' + text[end:]
        start = text.index('\t\twhen 30103.chat.')
        end = text.index('\t\twhen 2598.kill', start)
        text = text[:start] + '''        when 30103.chat."Odaya gir" with pc.get_map_index() >= 2160000 and pc.get_map_index() <= 2169990 and d.getf("level") == 6 begin
            if d.getf("head_paid") ~= 1 then return end
            pc.jump(314600, 1318900)
            pc.setf("devilcatacomb_zone", "catacombkey", 1)
        end

''' + text[end:]
        text = text.replace('local j = number(1, 80)', 'local j = number(1, 10)')
    else:
        raise ValueError(name)
    return '-- Active mid-easy profile. Baseline: quest_tr/_alldungeons/' + name + '.lua\n' + text


def drops():
    source = (LOCALE / 'mob_drop_item.txt').read_text()
    remaining = dict(ACCESS)
    bosses = 0

    def replace(match):
        nonlocal bosses
        name, body = match[1], match[2]
        if name.startswith('Phase3Access_'):
            return ''
        mob_match = re.search(r'\bMob\s+(\d+)', body)
        if not mob_match:
            return match[0]
        mob = int(mob_match[1])
        rows = [list(map(int, m)) for m in re.findall(r'^\s*\d+\s+(\d+)\s+(\d+)\s+(\d+)\s*$', body, re.M)]
        if name.startswith('Phase3Boss_'):
            bosses += 1
            rows = [[rows[0][0], 1, 100]] + remaining.pop(mob, [])
            kind = 'limit\n\tlevel_limit\t0'
        elif mob in ACCESS:
            rows = [row for row in rows if row[0] not in {e[0] for e in ACCESS[mob]}]
            kind = re.search(r'\bType\s+(\w+)', body)[1]
        else:
            return match[0]
        return 'Group\t%s\n{\n\tMob\t%d\n\tType\t%s\n%s\n}' % (
            name, mob, kind, '\n'.join('\t%d\t%d\t%d\t%d' % (i + 1, *row) for i, row in enumerate(rows)))

    output = re.sub(r'Group\s+(\S+)\s*\{([^{}]*)\}', replace, source)
    if bosses != 13:
        raise ValueError('Expected thirteen boss chest groups')
    for mob, rows in sorted(remaining.items()):
        output += '\nGroup\tPhase3Access_%d\n{\n\tMob\t%d\n\tType\tlimit\n\tlevel_limit\t0\n%s\n}\n' % (
            mob, mob, '\n'.join('\t%d\t%d\t%d\t%d' % (i + 1, *row) for i, row in enumerate(rows)))
    return re.sub(r'\n{3,}', '\n\n', output)


def policy():
    data = json.loads((ROOT / 'platform/gameplay/phase3_loot.json').read_text())
    data.update(version=4, boss_drop_type='limit', boss_chest_pct=100,
                access_drops={str(k): v for k, v in sorted(ACCESS.items())})
    for boss in data['direct_bosses']:
        if boss['mob'] == 1192:
            boss['entries'] = [row for row in boss['entries'] if row[0] != 30190]
    return json.dumps(data, indent=2) + '\n'


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('target', choices=['drops', 'policy', 'deviltower_zone', 'devilcatacomb_zone',
                                         'spider_dungeon', 'dragonlair'])
    args = parser.parse_args()
    print({'drops': drops, 'policy': policy}.get(args.target, lambda: profile(args.target))(), end='')
