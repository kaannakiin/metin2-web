"""Print staged client login packet sizes without linking or changing the engine."""

from pathlib import Path
import os
import re
import subprocess
import tempfile

import build_gamelib as build


def main():
    with tempfile.TemporaryDirectory(prefix='m2-login-layout-') as temporary:
        source = Path(temporary) / 'sizes.cpp'
        source.write_text('#include "UserInterface/StdAfx.h"\n'
                          '#include "UserInterface/Packet.h"\n'
                          'static_assert(sizeof(TSimplePlayerInformation) == 0, "player size");\n'
                          'static_assert(sizeof(TPacketGCLoginSuccess4) == 0, "login size");\n')
        result = subprocess.run([build.tool_name('em++'), '-std=c++17', '-c', '-w',
            '-I' + build.COMPAT, '-I' + build.STAGE, '-I' + build.EXTERN,
            '-I' + str(Path(build.STAGE) / 'eterBase'), '-I' + build.PYTHON_INC,
            str(source), '-o', str(Path(temporary) / 'sizes.o')],
            capture_output=True, text=True)
        sizes = re.findall(r"expression evaluates to '(\d+) == 0'", result.stderr)
        if len(sizes) != 2:
            raise SystemExit(result.stderr[-2200:])
        print('client TSimplePlayerInformation=' + sizes[0])
        print('client TPacketGCLoginSuccess4=' + sizes[1])
        profile = os.environ.get('M2W_DEV_PROTOCOL')
        if profile:
            from dev_protocol import PROFILES
            expected = PROFILES[profile]
            if int(sizes[1]) != expected:
                raise SystemExit('Protocol preset %s expects %d bytes, got %s' % (profile, expected, sizes[1]))
            print('PROTOCOL: %s; login packet=%d bytes' % (profile, expected))


if __name__ == '__main__':
    main()
