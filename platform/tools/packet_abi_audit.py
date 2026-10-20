#!/usr/bin/env python3
"""Compare an actual server ELF's DWARF against an Emscripten ABI export.

Checks common packet aliases' total sizes and ordered field offsets, plus GC
header numbers. Unmapped types and partially parsed fields remain explicit.
This is a wire-layout check; dynamic lengths, handler logic and gameplay still
need fixtures and scenario tests.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess


def number(value):
    token = re.search(r'\b(?:0x[0-9a-fA-F]+|\d+)\b', value or '')
    return int(token[0], 0) if token else None


def quoted(value):
    strings = re.findall(r'"([^"]*)"', value or '')
    return strings[-1] if strings else None


def parse_dwarf(text):
    records, aliases, headers = {}, {}, {}
    root = None
    child = None

    def finish():
        nonlocal root
        if not root:
            return
        name = quoted(root['attrs'].get('name'))
        if not name:
            return
        if root['tag'] == 'typedef':
            target = quoted(root['attrs'].get('type'))
            if target:
                aliases.setdefault(name, set()).add(target)
        elif root['tag'] == 'structure_type':
            size = number(root['attrs'].get('byte_size'))
            fields = [{'name': quoted(item.get('name')), 'offset': number(item.get('data_member_location'))}
                      for item in root['children'] if item.get('_tag') == 'member']
            fields = [item for item in fields if item['name'] and item['offset'] is not None]
            if size is not None:
                record = {'size': size, 'fields': fields}
                if record not in records.setdefault(name, []):
                    records[name].append(record)
        elif root['tag'] == 'enumeration_type' and name == 'PacketHeaderGC':
            for item in root['children']:
                key = quoted(item.get('name'))
                if key and key.startswith('HEADER_GC_'):
                    headers[key] = number(item.get('const_value'))

    for line in text.splitlines():
        tag = re.match(r'0x[0-9a-fA-F]+:(\s*)DW_TAG_(\w+)', line)
        if tag:
            indentation = len(tag[1])
            if not root or indentation <= root['indent']:
                finish()
                root = {'tag': tag[2], 'indent': indentation, 'attrs': {}, 'children': []}
                child = None
            else:
                child = {'_tag': tag[2]}
                root['children'].append(child)
            continue
        attribute = re.match(r'\s*DW_AT_(\w+)\s*\((.*)\)\s*$', line)
        if attribute and root:
            (child if child is not None else root['attrs'])[attribute[1]] = attribute[2]
    finish()
    return records, aliases, headers


def audit(client, records, aliases, headers):
    rows, unmapped, mismatches, partial, legacy = [], [], [], [], []
    # The fork retains old client declarations alongside the modern wire form.
    # These mappings are supported by numeric GC headers and the receive handlers.
    alternate = {'TPacketGCLoginSuccess4': 'TPacketGCLoginSuccess',
                 'TPacketGCItemSet2': 'TPacketGCItemSet',
                 'TPacketGCSkillLevelNew': 'TPacketGCSkillLevel',
                 'TPacketGCRefineInformationNew': 'TPacketGCRefineInformation',
                 'TPacketGCTargetCreateNew': 'TPacketGCTargetCreate'}
    header_aliases = {'HEADER_GC_ITEM_SET2': 'HEADER_GC_ITEM_SET',
                      'HEADER_GC_SKILL_LEVEL_NEW': 'HEADER_GC_SKILL_LEVEL',
                      'HEADER_GC_REFINE_INFORMATION_NEW': 'HEADER_GC_REFINE_INFORMATION',
                      'HEADER_GC_MAIN_CHARACTER2_EMPIRE': 'HEADER_GC_MAIN_CHARACTER',
                      'HEADER_GC_TARGET_CREATE_NEW': 'HEADER_GC_TARGET_CREATE'}
    old_types = {'TPacketGCItemSet': 'HEADER_GC_ITEM_SET2',
                 'TPacketGCSkillLevel': 'HEADER_GC_SKILL_LEVEL_NEW',
                 'TPacketGCRefineInformation': 'HEADER_GC_REFINE_INFORMATION_NEW',
                 'TPacketGCTargetCreate': 'HEADER_GC_TARGET_CREATE_NEW'}
    for old, modern in old_types.items():
        canonical = header_aliases[modern]
        if modern in client['headers'] and canonical in headers and client['headers'][modern] == headers[canonical]:
            legacy.append(old)
    for name, candidate in sorted(client['records'].items()):
        if name in legacy:
            continue
        server_alias = alternate.get(name, name)
        tags = aliases.get(server_alias, set())
        variants = []
        for tag in tags:
            variants.extend(record for record in records.get(tag, []) if record not in variants)
        if not variants:
            unmapped.append(name)
            continue
        differences = []
        if len(variants) != 1:
            differences.append('server binary contains inconsistent layouts for this type')
        server = variants[0]
        # SHOP_START reads owner VID separately from vecBuffer[0] and the
        # client item array at vecBuffer[4] (RecvShopPacket). It is not a 4B ABI bug.
        prefix = 4 if name == 'TPacketGCShopStart' else 0
        if candidate['size'] + prefix != server['size']:
            differences.append('size client=%d server=%d' % (candidate['size'], server['size']))
        fields = list(candidate['fields'].items())
        server_fields = server['fields'][1:] if prefix else server['fields']
        if candidate['unparsed_fields']:
            partial.append(name)
        elif len(fields) != len(server_fields):
            # e.g. the client groups refine data in TRefineTable while the
            # server writes flat members. Equal totals alone do not prove offsets.
            partial.append(name)
        else:
            for (client_name, field), server_field in zip(fields, server_fields):
                if field['offset'] + prefix != server_field['offset']:
                    differences.append('offset %s/%s client=%d server=%d' %
                                       (client_name, server_field['name'], field['offset'], server_field['offset']))
        row = {'type': name, 'server_alias': server_alias, 'client_size': candidate['size'],
               'server_size': server['size'], 'differences': differences,
               'field_comparison_partial': name in partial, 'separately_consumed_prefix': prefix}
        rows.append(row)
        if differences:
            mismatches.append(row)
    header_rows, unmapped_headers = [], []
    old_header_names = {canonical for modern, canonical in header_aliases.items()
                        if modern in client['headers']}
    for name, value in client['headers'].items():
        if name in old_header_names:
            continue
        canonical = header_aliases.get(name, name)
        if canonical in headers:
            header_rows.append({'name': name, 'server_name': canonical, 'client': value, 'server': headers[canonical]})
        else:
            unmapped_headers.append(name)
    header_mismatches = [row for row in header_rows if row['client'] != row['server']]
    return {'checked_records': len(rows), 'compatible_records': len(rows) - len(mismatches),
            'fully_compared_records': sum(not row['differences'] and not row['field_comparison_partial'] for row in rows),
            'checked_gc_headers': len(header_rows), 'legacy_client_declarations': legacy,
            'record_mismatches': mismatches, 'header_mismatches': header_mismatches,
            'unmapped_client_records': unmapped, 'unmapped_gc_headers': unmapped_headers,
            'partial_field_records': partial, 'records': rows,
            'validation_errors': ([] if rows else ['No shared packet records were compared']) +
                                 ([] if header_rows else ['No shared GC headers were compared']),
            'limits': ['No semantic-value, endianness or signedness comparison.',
                       'No dynamic-payload length or handler-consumption proof.',
                       'Unmapped and partial records are not a pass; gameplay scenarios remain required.']}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--server', required=True)
    parser.add_argument('--client', required=True)
    parser.add_argument('--output', required=True)
    parser.add_argument('--dwarfdump', default='/usr/bin/dwarfdump')
    parser.add_argument('--strict', action='store_true')
    args = parser.parse_args()
    binary = Path(args.server)
    if binary.read_bytes()[:6] != b'\x7fELF\x01\x01':
        raise SystemExit('Expected the deployed little-endian ELF32 server binary')
    result = subprocess.run([args.dwarfdump, '--regex',
        '--name=^(TPacket(GC|CG)|TPlayerSkill$|packet_|SPacket|SPlayerSkill$|PacketHeaderGC$)',
        '--show-children', str(binary)], capture_output=True, text=True, check=True)
    records, aliases, headers = parse_dwarf(result.stdout)
    if not records or not aliases or not headers:
        raise SystemExit('Incomplete server DWARF data; refusing a misleading empty audit')
    client = json.loads(Path(args.client).read_text())
    if client.get('pointer_size') != 4:
        raise SystemExit('Expected a wasm32 client ABI export')
    report = audit(client, records, aliases, headers)
    report['server_binary_sha256'] = hashlib.sha256(binary.read_bytes()).hexdigest()
    report['client_provenance'] = {key: value for key, value in client.items() if key not in ('records', 'headers')}
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2) + '\n')
    print('ABI AUDIT: records=%d compatible=%d mismatches=%d; GC headers=%d mismatches=%d; unmapped=%d partial=%d' %
          (report['checked_records'], report['compatible_records'], len(report['record_mismatches']),
           report['checked_gc_headers'], len(report['header_mismatches']),
           len(report['unmapped_client_records']), len(report['partial_field_records'])))
    print('Report:', output)
    if args.strict and (report['record_mismatches'] or report['header_mismatches'] or report['validation_errors']):
        raise SystemExit(1)


if __name__ == '__main__':
    main()
