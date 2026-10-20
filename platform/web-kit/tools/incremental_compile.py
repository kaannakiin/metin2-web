"""Content-based object cache; staging may recreate every source on each run."""

import hashlib
import json
import os
from pathlib import Path
import shlex
import shutil
import subprocess
import threading


class ObjectCache:
    def __init__(self, compiler, clean=False):
        self.clean = clean
        self.outputs = set()
        self.compiled = 0
        self.reused = 0
        self.failed = 0
        self._hashes = {}
        self._directories = {}
        self._lock = threading.Lock()
        resolved = shutil.which(compiler) or compiler
        self.compiler = str(Path(resolved).resolve())
        version = subprocess.run([compiler, '--version'], capture_output=True, text=True)
        if version.returncode:
            raise RuntimeError('Cannot identify compiler: ' + version.stderr)
        self.identity = [self.compiler, self.digest(self.compiler), version.stdout,
                         {k: v for k, v in os.environ.items()
                          if k.startswith(('EM', 'LLVM', 'BINARYEN', 'CCACHE'))
                          or k in ('PATH', 'CPATH', 'CPLUS_INCLUDE_PATH',
                                   'C_INCLUDE_PATH', 'SDKROOT')}]

    def digest(self, filename):
        # Thousands of dependency checks share headers. Resolving every symlink
        # component for every check costs more than stat+hashing on a warm build.
        p = Path(os.path.abspath(filename))
        st = p.stat()
        key = (st.st_dev, st.st_ino, st.st_size, st.st_mtime_ns, st.st_ctime_ns)
        with self._lock:
            value = self._hashes.get(key)
        if value is None:
            value = hashlib.sha256(p.read_bytes()).hexdigest()
            with self._lock:
                self._hashes[key] = value
        return value

    def inventory(self, directory):
        """New/removed headers can change include lookup without changing old deps."""
        directory = str(Path(directory).resolve())
        with self._lock:
            value = self._directories.get(directory)
        if value is None:
            names = []
            for root, dirs, files in os.walk(directory):
                dirs.sort()
                for name in sorted(dirs + files):
                    p = os.path.join(root, name)
                    names.append(os.path.relpath(p, directory) +
                                 ('->' + os.readlink(p) if os.path.islink(p) else ''))
            value = hashlib.sha256('\n'.join(names).encode()).hexdigest()
            with self._lock:
                self._directories[directory] = value
        return [directory, value]

    @staticmethod
    def dependencies(filename):
        text = Path(filename).read_text(encoding='utf-8')
        text = text.replace('\\\n', ' ')
        # -MT supplies one target; split there, not on a Windows drive colon.
        _, separator, prerequisites = text.partition(': ')
        if not separator:
            raise ValueError('Invalid compiler dependency file')
        return shlex.split(prerequisites)

    @staticmethod
    def discard(output):
        for suffix in ('', '.d', '.cache.json'):
            Path(str(output) + suffix).unlink(missing_ok=True)

    def run(self, command, **kwargs):
        """Same result shape as subprocess.run; failed compiles cannot leave old .o."""
        command = [str(x) for x in command]
        output = Path(command[command.index('-o') + 1]).resolve()
        # -c need not immediately precede the source (our commands have flags).
        sources = [x for x in command[1:] if x.endswith(('.cpp', '.cc', '.c', '.cxx'))]
        if len(sources) != 1:
            raise ValueError('Expected one source file: ' + repr(command))
        source = Path(sources[0]).resolve()
        with self._lock:
            self.outputs.add(str(output))
        includes = [str(source.parent)]
        for i, arg in enumerate(command):
            if arg == '-I':
                includes.append(command[i + 1])
            elif arg.startswith('-I'):
                includes.append(arg[2:])
        signature = hashlib.sha256(json.dumps(
            [command, os.getcwd(), self.identity,
             [self.inventory(p) for p in sorted(set(includes))]],
            sort_keys=True).encode()).hexdigest()
        stamp = Path(str(output) + '.cache.json')
        depfile = str(output) + '.d'
        if not self.clean:
            try:
                saved = json.loads(stamp.read_text(encoding='utf-8'))
                if (saved['command'] == signature and output.is_file()
                        and saved['object'] == self.digest(output)
                        and saved['dependencies']
                        and all(self.digest(p) == h for p, h in saved['dependencies'].items())):
                    with self._lock:
                        self.reused += 1
                    return subprocess.CompletedProcess(command, 0, '', '')
            except (OSError, ValueError, KeyError, TypeError):
                pass
        self.discard(output)
        output.parent.mkdir(parents=True, exist_ok=True)
        result = subprocess.run(command + ['-MD', '-MF', depfile, '-MT', str(output)], **kwargs)
        with self._lock:
            self.compiled += 1
        if result.returncode:
            self.discard(output)
            with self._lock:
                self.failed += 1
            detail = next((s.strip() for s in (result.stderr or '').splitlines()
                           if 'error:' in s), 'see compiler output')
            print('COMPILE FAILED: %s: %s' % (source.name, detail))
            return result
        try:
            deps = set(self.dependencies(depfile)) | {str(source)}
            saved = {'command': signature, 'object': self.digest(output),
                     'dependencies': {os.path.abspath(p): self.digest(p) for p in deps}}
            temporary = Path(str(stamp) + '.tmp')
            temporary.write_text(json.dumps(saved, sort_keys=True), encoding='utf-8')
            temporary.replace(stamp)
        except (OSError, ValueError):
            # A successful object is usable, but must be rebuilt without a valid stamp.
            stamp.unlink(missing_ok=True)
        return result

    def prune(self, directory):
        """Excluded/deleted source files must no longer supply linker symbols."""
        removed = 0
        for obj in Path(directory).rglob('*.o'):
            if str(obj.resolve()) not in self.outputs:
                self.discard(obj)
                removed += 1
        print('OBJECT CACHE: compiled %d | reused %d | failed %d | removed %d'
              % (self.compiled, self.reused, self.failed, removed))
        return sorted(p for p in self.outputs if Path(p).is_file())
