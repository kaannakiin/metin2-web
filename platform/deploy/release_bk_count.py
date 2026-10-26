#!/usr/bin/env python3
"""Publish only the BK counter module inside the current Emscripten package."""
import ast
import copy
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import time
from types import SimpleNamespace as NS


def digest(data):
    return hashlib.sha256(data).hexdigest()


def package(script, data):
    start = script.index('{"files":')
    metadata, length = json.JSONDecoder().raw_decode(script[start:])
    assert metadata['remote_package_size'] == len(data)
    return metadata, start, length


def check_module(old, new):
    before, after = ast.parse(old), ast.parse(new)
    old_class = next(n for n in before.body if isinstance(n, ast.ClassDef) and n.name == 'BKOku')
    new_class = next(n for n in after.body if isinstance(n, ast.ClassDef) and n.name == 'BKOku')
    helper = next(n for n in new_class.body if isinstance(n, ast.FunctionDef) and n.name == '__GetSelectedBookCount')
    refresh = next(n for n in new_class.body if isinstance(n, ast.FunctionDef) and n.name == 'yenile')
    old_refresh = next(n for n in old_class.body if isinstance(n, ast.FunctionDef) and n.name == 'yenile')
    fixture_class = ast.ClassDef(name='Window', bases=[], keywords=[], body=[copy.deepcopy(helper), copy.deepcopy(refresh)], decorator_list=[])
    new_class.body.remove(helper)
    assert len(refresh.body) == len(old_refresh.body) + 1
    assert ast.dump(ast.Module(body=refresh.body[2:], type_ignores=[])) == ast.dump(ast.Module(body=old_refresh.body[1:], type_ignores=[]))
    refresh.body = old_refresh.body
    assert ast.dump(before) == ast.dump(after), 'Unrelated Python behavior changed'
    items = {0: (50300, 1, 2), 1: (50300, 2, 7), 2: (71001, 1, 20), 3: (50300, 0, 4), 179: (50300, 1, 3)}
    grades = {1: 1, 2: 1, 3: 1}
    player = NS(INVENTORY_SLOT_COUNT=180,
        GetSkillGrade=lambda slot: grades.get(slot, 0),
        GetSkillIndex=lambda slot: slot if slot in grades else 0,
        GetItemIndex=lambda cell: items.get(cell, (0, 0, 0))[0],
        GetItemMetinSocket=lambda cell, socket: items.get(cell, (0, 0, 0))[1],
        GetItemCount=lambda cell: items.get(cell, (0, 0, 0))[2],
        GetItemCountByVnum=lambda vnum: sum(t[2] for t in items.values() if t[0] == vnum))
    scope = dict(player=player, SKILL_INDEX_DICT={}, net=NS(GetMainActorRace=lambda: 0, GetMainActorSkillGroup=lambda: 0), chr=NS(RaceToJob=lambda race: 0))
    exec(compile(ast.fix_missing_locations(ast.Module(body=[fixture_class], type_ignores=[])), '<bk-fixture>', 'exec'), scope)
    class Slot:
        value = None
        def SetItemSlot(self, slot, vnum, count): self.value = (vnum, count)
        def ClearSlot(self, slot): self.value = None
        def RefreshSlot(self): pass
    window = scope['Window']()
    for name in ('bkslot', 'kotuslot', 'munzevislot', 'skillslot'):
        setattr(window, name, Slot())
    def check(selected, expected):
        window.aktifslot = selected
        window.yenile()
        assert window.bkslot.value == expected, (selected, window.bkslot.value, expected)
    check(None, None)
    check(0, (50300, 5))
    check(1, (50300, 7))
    check(2, None)
    grades[1] = 2
    check(0, None)
    grades[1] = 1
    items.pop(0)
    check(0, (50300, 3))
    check(1, (50300, 7))
    items.pop(179)
    check(0, None)
    print('MODULE CHECK: only counter behavior changed; 8 inventory cases passed', flush=True)


def atomic_write(path, data):
    temporary = path.with_name(path.name + '.bk-release-tmp')
    try:
        temporary.write_bytes(data)
        temporary.chmod(path.stat().st_mode & 0o777)
        os.replace(temporary, path)
    finally:
        temporary.unlink(missing_ok=True)


def main():
    root = Path('/home/m2web')
    source, converted = map(Path, sys.argv[1:3])
    with (root / 'dev/client-build.lock').open('a') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        live = root / 'www'
        names = ('client.js', 'client.data', 'client.html')
        original = {name: (live / name).read_bytes() for name in names}
        wasm_hash = digest((live / 'client.wasm').read_bytes())
        script = original['client.js'].decode('utf-8')
        metadata, offset, length = package(script, original['client.data'])
        targets = [r for r in metadata['files'] if r['filename'] == '/uibkoku.py']
        assert len(targets) == 1
        target = targets[0]
        new_module = converted.read_bytes()
        check_module(original['client.data'][target['start']:target['end']].decode('utf-8'), new_module.decode('utf-8'))
        new_data = original['client.data'][:target['start']] + new_module + original['client.data'][target['end']:]
        delta = len(new_module) - (target['end'] - target['start'])
        updated = copy.deepcopy(metadata)
        for row in updated['files']:
            if row['filename'] == '/uibkoku.py':
                row['end'] += delta
            elif row['start'] >= target['end']:
                row['start'] += delta
                row['end'] += delta
            else:
                assert row['end'] <= target['start']
        updated['remote_package_size'] = len(new_data)
        replacement = json.dumps(updated)
        new_script = script[:offset] + replacement + script[offset + length:]
        parsed, new_offset, new_length = package(new_script, new_data)
        assert new_script[:new_offset] + new_script[new_offset + new_length:] == script[:offset] + script[offset + length:]
        changed = []
        for old_row, new_row in zip(metadata['files'], parsed['files']):
            assert old_row['filename'] == new_row['filename']
            a = original['client.data'][old_row['start']:old_row['end']]
            b = new_data[new_row['start']:new_row['end']]
            if a != b:
                changed.append(old_row['filename'])
        assert changed == ['/uibkoku.py'], changed
        page = original['client.html'].decode('utf-8')
        versions = set(re.findall(r'\?v=(\d+)', page))
        assert len(versions) == 1, versions
        version = str(max(int(time.time()), int(next(iter(versions))) + 1))
        new_page, stamps = re.subn(r'\?v=\d+', '?v=' + version, page)
        assert stamps >= 2
        assert not any(s in new_page for s in ('m2wDevVersions', 'localhost:1873', '127.0.0.1:1873'))
        candidate = {'client.js': new_script.encode('utf-8'), 'client.data': new_data, 'client.html': new_page.encode('utf-8')}
        backup = Path(tempfile.mkdtemp(prefix='bk-count-', dir=root / 'backups'))
        (backup / 'site').mkdir()
        (backup / 'candidate').mkdir()
        for name in names:
            shutil.copy2(live / name, backup / 'site' / name)
            (backup / 'candidate' / name).write_bytes(candidate[name])
        print('BACKUP:', backup, flush=True)
        print('PACKAGE SCOPE: %d files checked; only /uibkoku.py changed; engine JS outside file metadata unchanged' % len(metadata['files']), flush=True)
        subprocess.run(['docker', 'exec', 'm2web-build', 'node', '--check', '/work/' + str((backup / 'candidate/client.js').relative_to(root))], check=True)
        subprocess.run(['docker', 'exec', 'm2web-build', 'python3.13', '-c', "import ast; from pathlib import Path; ast.parse(Path('/work/bk-count/uibkoku.web.py').read_text()); print('CPYTHON 3.13: module syntax passed')"], check=True)
        watched = {name: digest((live / name).read_bytes()) for name in names}
        assert all(watched[name] == digest(original[name]) for name in names), 'Concurrent publish'
        assert digest((live / 'client.wasm').read_bytes()) == wasm_hash
        input_updates = ((root / 'dev/inputs/root/uibkoku.py', source.read_bytes()),
                         (root / 'kit/build/port/scripts/uibkoku.py', source.read_bytes()),
                         (root / 'kit/build/port/scripts3/uibkoku.py', new_module),
                         (root / 'kit/build/port/data/uibkoku.py', new_module))
        old_inputs = {}
        for path, content in input_updates:
            assert path.parent.is_dir(), path.parent
            old_inputs[path] = path.read_bytes() if path.exists() else None
            if path.exists():
                shutil.copy2(path, backup / (str(path.relative_to(root)).replace('/', '__')))
        try:
            for path, content in input_updates:
                if path.exists():
                    atomic_write(path, content)
                else:
                    path.write_bytes(content)
            for name in names:
                atomic_write(live / name, candidate[name])
            assert all((live / name).read_bytes() == candidate[name] for name in names)
            assert digest((live / 'client.wasm').read_bytes()) == wasm_hash
        except BaseException:
            for name in names:
                atomic_write(live / name, original[name])
            for path, old_content in old_inputs.items():
                if old_content is None:
                    path.unlink(missing_ok=True)
                else:
                    atomic_write(path, old_content)
            print('ROLLED BACK:', backup, flush=True)
            raise
        print('PUBLISHED:', version, 'WASM:', wasm_hash, flush=True)
        (backup / 'release.json').write_text(json.dumps({'version': version, 'wasm': wasm_hash, 'changed': changed, 'hashes': {name: digest(data) for name, data in candidate.items()}}, indent=2) + '\n')


if __name__ == '__main__':
    main()
