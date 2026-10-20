#!/usr/bin/env python3
"""Exercise the server's actual regen lexer/parser with the density map files."""
from pathlib import Path
import re
import shutil
import subprocess
import tempfile

import metin_density

ROOT = Path(__file__).resolve().parents[2]


def main():
    report = metin_density.check()
    source = (ROOT / 'apps/server/game/src/regen.cpp').read_bytes().decode('latin1')
    parser = source[source.index('enum ERegenModes'):source.index('bool is_regen_exception(')]
    header = (ROOT / 'apps/server/game/src/regen.h').read_text()
    structure = re.search(r'typedef struct regen\s*\{.*?\} REGEN;', header, re.S)
    types = re.search(r'enum\s*\{[^}]*REGEN_TYPE_MAX_NUM[^}]*\};', header, re.S)
    if not structure or not types or 'regen->id = m_regenId++;' not in parser:
        raise SystemExit('Regen source changed; update the parser fixture')
    preamble = r'''
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <set>
#define ENABLE_RESP_SYSTEM 1
using BYTE = unsigned char;
using DWORD = std::uint32_t;
struct regen;
using LPREGEN = regen*;
using LPEVENT = void*;
static std::size_t m_regenId = 0;
#define sys_err(...) std::fprintf(stderr, __VA_ARGS__)
template<class T> bool str_to_number(T& value, const char* text) {
    value = static_cast<T>(std::strtoll(text, nullptr, 10));
    return true;
}
'''
    main_source = r'''
int main(int argc, char** argv) {
    std::set<std::size_t> ids;
    unsigned count = 0;
    for (int file = 1; file < argc; ++file) {
        FILE* input = std::fopen(argv[file], "r");
        if (!input) return 2;
        REGEN row;
        while (read_line(input, &row)) {
            if (row.type == REGEN_TYPE_MOB && row.vnum >= 8001 && row.vnum <= 8027) {
                if (row.max_count != 1 || row.time == 0 || row.ex <= row.sx || row.ey <= row.sy) return 3;
                if (!ids.insert(row.id).second) return 4;
                count += row.max_count;
            }
        }
        std::fclose(input);
    }
    if (argc != 14 || count != 194 || ids.size() != 194) return 5;
    std::puts("SERVER REGEN PARSER: 13 maps, 194 Metins, 194 distinct RESP ids; timers and spawn areas valid PASS");
}
'''
    compiler = shutil.which('clang++') or shutil.which('c++')
    if not compiler:
        raise SystemExit('C++ compiler required')
    with tempfile.TemporaryDirectory(prefix='m2-regen-fixture-') as temporary:
        cpp = Path(temporary) / 'regen-fixture.cpp'
        executable = Path(temporary) / 'regen-fixture'
        cpp.write_text(preamble + '\n' + types[0] + '\n' + structure[0] + '\n' + parser + '\n' + main_source)
        subprocess.run([compiler, '-std=c++17', '-O0', '-w', str(cpp), '-o', str(executable)], check=True)
        subprocess.run([str(executable)] + [str(ROOT / 'runtime/freebsd/share/locale/europe' / row['path'])
                                          for row in report['maps']], check=True)


if __name__ == '__main__':
    main()
