import os, sys, tempfile, shutil
kit, src = os.path.abspath(sys.argv[1]), os.path.abspath(sys.argv[2])
SCAN_DIR = sys.argv[3] if len(sys.argv) > 3 else None
sys.path.insert(0, os.path.join(kit, 'tools'))
import stage_port as sp
stage = tempfile.mkdtemp(prefix='stagecheck_')
sp.TMP4 = src
entries = list(sp.PATCHES)
sp.PATCHES = []
sys.argv = ['stage_port.py', stage]
import contextlib, io
with contextlib.redirect_stdout(io.StringIO()):
    sp.main()
hits = 0
bad = []
for i, entry in enumerate(entries):
    sp.PATCHES = [entry]
    buf = io.StringIO()
    try:
        with contextlib.redirect_stdout(buf):
            sp.apply_patches(stage)
        hits += 1
    except SystemExit as e:
        bad.append((i, entry[0], str(e).split('\n')[0], str(e).split('occurrences:')[-1].split('\n')[0] if 'occurrences' in str(e) else ''))
    except OSError as e:
        bad.append((i, entry[0], 'NOFILE', str(e)))
print(f'patches={len(entries)} hit={hits} miss={len(bad)}')
for b in bad:
    print(*b, sep=' | ')
shutil.rmtree(stage)

if SCAN_DIR:
    import collections
    sp.PATCHES = entries
    sp.workspace.EXTERN_INCLUDE = os.path.join(os.path.dirname(src), 'extern', 'include')
    target = os.path.abspath(SCAN_DIR)
    sys.argv = ['stage_port.py', target]
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        sp.main()
    print(buf.getvalue().split('letter-case aliases:')[-1].strip(), '(aliases created by the pass)')
    sp._LISTINGS.clear()
    links = [os.path.join(r, n) for r, d, f in os.walk(target) for n in d + f if os.path.islink(os.path.join(r, n))]
    roots = [sp.workspace.COMPAT, target, sp.workspace.EXTERN_INCLUDE, os.path.join(target, 'eterBase')]
    total = 0
    failing = collections.Counter()
    where = {}
    for path in sp._include_sources(target):
        with open(path, encoding='utf-8', errors='ignore') as fh:
            text = fh.read()
        for bracket, name in sp.INCLUDE_RE.findall(text):
            total += 1
            name = name.replace('\\', '/')
            searched = ([os.path.dirname(path)] if bracket == '"' else []) + roots
            cands = [os.path.join(w, name) for w in searched]
            if any(sp._lookup(c, True) for c in cands):
                continue
            kind = 'CASE-ONLY' if any(sp._lookup(c, False) for c in cands) else 'not on the include path'
            failing[(kind, bracket, name)] += 1
            where.setdefault((kind, bracket, name), os.path.relpath(path, target))
    print(f'strict scan after aliases: includes={total} symlinks_in_stage={len(links)}')
    kinds = collections.Counter()
    for (kind, b, n), c in failing.items():
        kinds[kind] += c
    print('failing strict resolution:', dict(kinds))
    systemish = lambda b, n: b == '<' and (n.islower() or '/' in n and n.split('/')[0].islower()) 
    for (kind, b, n), c in sorted(failing.items()):
        if kind != 'CASE-ONLY' and os.environ.get('SHOW_ALL') is None and b == '<' and n[0].islower() and 'win' not in n: continue
        print(' ', kind, b + n, c, '<-', where[(kind, b, n)])
