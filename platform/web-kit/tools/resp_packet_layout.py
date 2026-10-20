"""Measure RESP wire layouts with the actual staged Emscripten headers."""
from pathlib import Path
import re
import os
import shutil
import subprocess
import tempfile

import build_gamelib as build


def main():
    types = ('time_t', 'TPacketGCRespData', 'TPacketGCRespRefresh')
    with tempfile.TemporaryDirectory(prefix='m2-resp-layout-') as temporary:
        source = Path(temporary) / 'sizes.cpp'
        source.write_text('#include "UserInterface/StdAfx.h"\n'
                          '#include "UserInterface/Packet.h"\n' + ''.join(
                              'static_assert(sizeof(%s) == 0, "size %s");\n' % (name, name)
                              for name in types))
        result = subprocess.run([build.tool_name('em++'), '-std=c++17', '-c', '-w',
            '-I' + build.COMPAT, '-I' + build.STAGE, '-I' + build.EXTERN,
            '-I' + str(Path(build.STAGE) / 'eterBase'), '-I' + build.PYTHON_INC,
            str(source), '-o', str(Path(temporary) / 'sizes.o')],
            capture_output=True, text=True)
        sizes = re.findall(r"expression evaluates to '(\d+) == 0'", result.stderr)
        if len(sizes) != len(types):
            raise SystemExit(result.stderr[-2200:])
        for name, size in zip(types, sizes):
            print('%s=%s' % (name, size))
        if sizes[1:] != ['20', '20']:
            raise SystemExit('RESP wire layout differs from the running FreeBSD server')
        test = Path(__file__).with_name('test_resp_wire.cpp')
        executable = Path(temporary) / 'resp-test.js'
        command = [build.tool_name('em++'), '-std=c++17', '-O0', '-w',
            '-I' + build.COMPAT, '-I' + build.STAGE, '-I' + build.EXTERN,
            '-I' + str(Path(build.STAGE) / 'eterBase'), '-I' + build.PYTHON_INC,
            str(test), '-sENVIRONMENT=node', '-sEXIT_RUNTIME=1', '-o', str(executable)]
        compiled = subprocess.run(command, capture_output=True, text=True)
        if compiled.returncode:
            raise SystemExit(compiled.stderr[-2200:])
        node = os.environ.get('EMSDK_NODE') or shutil.which('node')
        if not node:
            raise SystemExit('Emscripten Node runtime unavailable for wire regression test')
        subprocess.run([node, str(executable)], check=True)


if __name__ == '__main__':
    main()
