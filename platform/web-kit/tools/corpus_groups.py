#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""corpus_groups.py - which corpus files belong together, for the prefetch.

The client reads a 4 MB chunk for every file it touches, synchronously, and
the picture stands still meanwhile. The page can fetch chunks in the
background - if it knows which ones are coming. Three kinds of groups:

  meta    small descriptor files (.msa, .msm, .mse, .txt ...): read by the
          thousand at login (every motion and effect is registered), tiny
          together, but alphabetically they sit between textures.
  motion  character motions (`ymir work/pc*/<job>/<dir>/*.gr2`, no hair):
          the client caches all races at login.
  map:X   everything map X loads: its directory, the texture set, the
          environment and the closure of the objects in its areas
          (property -> model -> textures). The client asks for the map of
          the character it is about to enter (webfs_web.cpp), so the
          prefetch follows the player instead of guessing a village.

`meta`, `motion` and the recorded `boot` list are placed first in the corpus
(build_corpus.py), so their chunks hold nothing else.
"""
import io
import os
import re
import sys

META_EXTENSIONS = {'.msa', '.msm', '.mss', '.mse', '.msf', '.msenv', '.mdatr',
                   '.prb', '.prt', '.prd', '.txt', '.xml', '.sub', '.cfg', '.inf'}
MOTION = re.compile(r'^ymir work/pc\d?/[^/]+/(?!hair/)[^/]+/.+\.gr2$')
REFERENCE = re.compile(rb'[A-Za-z0-9_ .:/\\-]{1,200}\.(?:dds|tga|jpg|png|gr2|mse|msf|msenv|spt|mde|txt|prt|prb|prd|wav|mp3|raw|atr|wtr)\b', re.I)
SCANNED = {'.txt', '.msenv', '.mse', '.msf', '.prb', '.prt', '.prd', '.msa', '.msm', '.mdatr'}


def corpus_name(path):
    """`D:\\Ymir Work\\a.dds` -> `ymir work/a.dds` (the client's CorpusName)."""
    p = path.strip().strip('"').replace('\\', '/').lower()
    if len(p) > 2 and p[1] == ':':
        p = p[3:]
    return p.lstrip('/')


def map_directories(names):
    """Top-level directories holding a map (`<dir>/setting.txt`)."""
    return sorted({n.split('/')[0] for n in names if n.count('/') == 1 and n.endswith('/setting.txt')})


def is_meta(name):
    """Descriptor outside a map directory and outside the language folders."""
    if name.startswith('locale/'):
        return False
    return os.path.splitext(name)[1] in META_EXTENSIONS


def is_motion(name):
    return bool(MOTION.match(name))


class Closure(object):
    """Follows file references through the corpus (`files`: name -> path on disk)."""

    def __init__(self, files, crc_index):
        self.files = files
        self.crc_index = crc_index
        self.by_basename = {}
        for n in files:
            self.by_basename.setdefault(n.rsplit('/', 1)[-1], []).append(n)
        self.cache = {}

    def resolve(self, raw, near):
        """The corpus name `raw` refers to from file `near`, or None."""
        name = corpus_name(raw)
        if not name:
            return None
        if name in self.files:
            return name
        joined = os.path.normpath(os.path.join(os.path.dirname(near), name)).replace(os.sep, '/')
        if joined in self.files:
            return joined
        if name.endswith('.msenv') and 'ymir work/environment/' + name in self.files:
            return 'ymir work/environment/' + name
        candidates = self.by_basename.get(name.rsplit('/', 1)[-1], [])
        return candidates[0] if len(candidates) == 1 else None

    def references(self, name):
        """Corpus names directly referenced by `name` (cached)."""
        if name in self.cache:
            return self.cache[name]
        found = set()
        extension = os.path.splitext(name)[1]
        path = self.files.get(name)
        if path and extension in SCANNED:
            data = io.open(path, 'rb').read()
            for m in REFERENCE.finditer(data):
                r = self.resolve(m.group(0).decode('latin-1'), name)
                if r and r != name:
                    found.add(r)
            if name.endswith('/areadata.txt'):
                found |= self.area_objects(data)
        elif path and extension == '.gr2':
            found |= self.model_textures(name, path)
        self.cache[name] = found
        return found

    def area_objects(self, data):
        """Property files of the objects placed in an `areadata.txt`."""
        found = set()
        lines = data.decode('latin-1').split('\n')
        for i, line in enumerate(lines):
            if line.startswith('Start Object') and i + 2 < len(lines):
                try:
                    crc = int(lines[i + 2].split()[0].split('#')[0])
                except (ValueError, IndexError):
                    continue
                p = self.crc_index.get(crc)
                if p and corpus_name(p) in self.files:
                    found.add(corpus_name(p))
        return found

    def model_textures(self, name, path):
        """Texture files a Granny model names (sections may be compressed)."""
        import gr2
        found = set()
        try:
            _file, image = gr2.open_file(path)
            textures = gr2.root_node(image)['Textures']
            for i in range(len(textures)):
                r = self.resolve(textures[i]['FromFileName'] or '', name)
                if r:
                    found.add(r)
        except Exception:
            pass
        return found

    def of_map(self, directory):
        """Every file the map in `directory` reaches."""
        todo = [n for n in self.files if n.startswith(directory + '/')]
        seen = set(todo)
        while todo:
            n = todo.pop()
            for r in self.references(n):
                if r not in seen:
                    seen.add(r)
                    todo.append(r)
        return seen


def read_crc_index(path):
    """CRC -> property file, from build_client_data.py's `property/crc_index.txt`."""
    index = {}
    if os.path.exists(path):
        for line in io.open(path, encoding='latin-1'):
            parts = line.rstrip('\n').split('\t')
            if len(parts) == 2:
                index[int(parts[0])] = parts[1]
    return index


def map_groups(file_list, crc_index_path):
    """{'map:<dir>': set of corpus names} for every map directory."""
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    files = dict(file_list)
    closure = Closure(files, read_crc_index(crc_index_path))
    return {'map:' + d: closure.of_map(d) for d in map_directories(files)}


if __name__ == '__main__':
    import workspace
    from build_corpus import collect_files
    entries = collect_files()
    sizes = {n: os.path.getsize(p) for n, p in entries}
    meta = [n for n, _ in entries if is_meta(n)]
    motion = [n for n, _ in entries if is_motion(n)]
    print('meta: %d files, %.1f MB' % (len(meta), sum(sizes[n] for n in meta) / 2**20))
    print('motion: %d files, %.1f MB' % (len(motion), sum(sizes[n] for n in motion) / 2**20))
    groups = map_groups(entries, os.path.join(workspace.PORT, 'data', 'property', 'crc_index.txt'))
    for g, names in sorted(groups.items(), key=lambda kv: -sum(sizes.get(n, 0) for n in kv[1])):
        print('%-40s %6d files %8.1f MB' % (g, len(names), sum(sizes.get(n, 0) for n in names) / 2**20))
