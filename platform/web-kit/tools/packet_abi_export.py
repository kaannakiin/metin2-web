"""Export active client packet sizes, field offsets and GC header values.

Uses the same staged headers and Emscripten compiler as the engine. No native
host sizeof values, no guessed feature flags and no game connection are used.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import tempfile

import build_gamelib as build


def split_declarations(body):
    depth = 0
    start = 0
    for index, character in enumerate(body):
        if character == '{':
            depth += 1
        elif character == '}':
            depth -= 1
        elif character == ';' and depth == 0:
            yield body[start:index].strip()
            start = index + 1


def records(text):
    result = {}
    for match in re.finditer(r'typedef\s+struct\s*(\w+)?\s*\{', text):
        start = match.end()
        depth, end = 1, start
        while end < len(text) and depth:
            depth += (text[end] == '{') - (text[end] == '}')
            end += 1
        alias = re.match(r'\s*(\w+)\s*;', text[end:])
        if not alias or not re.fullmatch(r'TPacket(?:GC|CG)\w+|TPlayerSkill', alias[1]):
            continue
        fields, incomplete = [], []
        for declaration in split_declarations(text[start:end - 1]):
            if not declaration:
                continue
            if '{' in declaration or '(' in declaration or ':' in declaration:
                incomplete.append(declaration[:120])
                continue
            for part in declaration.split(','):
                field = re.search(r'\b(\w+)\s*(?:\[[^\]]*\]\s*)*$', part)
                if field:
                    fields.append(field[1])
                else:
                    incomplete.append(part[:120])
        result[alias[1]] = {'tag': match[1], 'fields': fields, 'unparsed_fields': incomplete}
    return result


def export():
    includes = ['-I' + build.COMPAT, '-I' + build.STAGE, '-I' + build.EXTERN,
                '-I' + str(Path(build.STAGE) / 'eterBase'), '-I' + build.PYTHON_INC]
    compiler = build.tool_name('em++')
    prefix = '#include "UserInterface/StdAfx.h"\n#include "UserInterface/Packet.h"\n#include <cstddef>\n'
    with tempfile.TemporaryDirectory(prefix='m2-packet-abi-') as temporary:
        source = Path(temporary) / 'layouts.cpp'
        source.write_text(prefix)
        preprocessed = subprocess.run([compiler, '-std=c++17', '-E', '-P', '-w', *includes, str(source)],
                                      capture_output=True, text=True, check=True).stdout
        types = records(preprocessed)
        headers = sorted(set(re.findall(r'\bHEADER_GC_\w+\b', preprocessed)))
        declarations, targets = [], []

        def measure(expression, target, add=0):
            index = len(targets)
            declarations.append('unsigned char m2w_audit_%d[(%s)+%d] = {};'
                                % (index, expression, add))
            targets.append((target, add))

        result = {'records': {}, 'headers': {}, 'compiler': subprocess.run(
            [compiler, '--version'], capture_output=True, text=True, check=True).stdout.splitlines()[0]}
        for name, record in types.items():
            target = {'tag': record['tag'], 'fields': {}, 'unparsed_fields': record['unparsed_fields']}
            result['records'][name] = target
            measure('sizeof(%s)' % name, (target, 'size'))
            for field in record['fields']:
                member = {}
                target['fields'][field] = member
                measure('offsetof(%s, %s)' % (name, field), (member, 'offset'), 1)
                measure('sizeof(((%s*)0)->%s)' % (name, field), (member, 'size'))
        for header in headers:
            measure(header, (result['headers'], header), 1)
        measure('sizeof(time_t)', (result, 'native_time_size'))
        measure('sizeof(void*)', (result, 'pointer_size'))
        source.write_text(prefix + 'extern "C" {\n' + '\n'.join(declarations) + '\n}\n')
        compiled = subprocess.run([compiler, '-std=c++17', '-S', '-emit-llvm', '-O0', '-w',
                                   *includes, str(source), '-o', '-'], capture_output=True, text=True)
        if compiled.returncode:
            raise SystemExit(compiled.stderr[-3500:])
        values = {int(index): int(size) for index, size in re.findall(
            r'@m2w_audit_(\d+)\s*=\s*[^\n]*?\[(\d+) x i8\]', compiled.stdout)}
        if len(values) != len(targets):
            raise SystemExit('Incomplete compiler layout export: %d/%d' % (len(values), len(targets)))
        for index, ((target, key), add) in enumerate(targets):
            target[key] = values[index] - add
    result['staged_packet_sha256'] = hashlib.sha256(
        (Path(build.STAGE) / 'UserInterface/Packet.h').read_bytes()).hexdigest()
    wasm = Path(build.STAGE).parent / 'client.wasm'
    if wasm.is_file():
        result['client_wasm_sha256'] = hashlib.sha256(wasm.read_bytes()).hexdigest()
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    output = Path(args.output)
    result = export()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2) + '\n')
    print('CLIENT ABI: %d records, %d GC headers; %s' %
          (len(result['records']), len(result['headers']), output))
