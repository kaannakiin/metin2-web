import importlib.util
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location('audit', Path(__file__).parents[1] / 'tools/packet_abi_audit.py')
audit = importlib.util.module_from_spec(spec)
spec.loader.exec_module(audit)


class PacketAuditTests(unittest.TestCase):
    def compare(self, size=20, offsets=(0,4,8,12,16), server_size=20, server_offsets=(0,4,8,12,16)):
        name = 'TPacketGCRespRefresh'
        client = {'headers': {'HEADER_GC_RESP': 49}, 'records': {name: {
            'size': size, 'unparsed_fields': [],
            'fields': {str(i): {'offset': offset, 'size': 4} for i, offset in enumerate(offsets)}}}}
        records = {'SResp': [{'size': server_size, 'fields': [
            {'name': str(i), 'offset': offset} for i, offset in enumerate(server_offsets)]}]}
        return audit.audit(client, records, {name: {'SResp'}}, {'HEADER_GC_RESP': 49})

    def test_resp_native_time64_is_rejected(self):
        result = self.compare(size=24, offsets=(0,4,8,16,20))
        self.assertEqual(len(result['record_mismatches']), 1)
        self.assertEqual(result['fully_compared_records'], 0)

    def test_wire32_passes(self):
        result = self.compare()
        self.assertEqual(result['record_mismatches'], [])
        self.assertEqual(result['fully_compared_records'], 1)

    def test_equal_size_wrong_offsets_fail(self):
        self.assertTrue(self.compare(offsets=(0,4,12,8,16))['record_mismatches'])

    def test_grouped_fields_are_partial(self):
        result = self.compare(offsets=(0,4))
        self.assertEqual(result['compatible_records'], 1)
        self.assertEqual(result['fully_compared_records'], 0)
        self.assertEqual(result['partial_field_records'], ['TPacketGCRespRefresh'])

    def test_empty_export_cannot_pass(self):
        result = audit.audit({'records': {}, 'headers': {}}, {}, {}, {})
        self.assertEqual(len(result['validation_errors']), 2)

    def test_unknown_type_is_not_compared(self):
        result = audit.audit({'records': {'Unknown': {}}, 'headers': {}}, {}, {}, {})
        self.assertEqual(result['unmapped_client_records'], ['Unknown'])
        self.assertEqual(result['fully_compared_records'], 0)

    def test_header_alias_and_mismatch(self):
        result = audit.audit({'records': {}, 'headers': {
            'HEADER_GC_ITEM_SET': 21, 'HEADER_GC_ITEM_SET2': 32}}, {}, {}, {'HEADER_GC_ITEM_SET': 33})
        self.assertEqual(result['checked_gc_headers'], 1)
        self.assertEqual(len(result['header_mismatches']), 1)

    def test_canonical_header_without_modern_alias_still_checked(self):
        result = audit.audit({'records': {}, 'headers': {'HEADER_GC_ITEM_SET': 21}}, {}, {}, {'HEADER_GC_ITEM_SET': 22})
        self.assertEqual(len(result['header_mismatches']), 1)

    def test_dwarf_types_members_and_enum(self):
        text = '''0x0001: DW_TAG_typedef
  DW_AT_name ("TPacketGCRespRefresh")
  DW_AT_type (0x0002 "SResp")
0x0002: DW_TAG_structure_type
  DW_AT_name ("SResp")
  DW_AT_byte_size (0x14)
0x0003:   DW_TAG_member
  DW_AT_name ("id")
  DW_AT_data_member_location (0x00)
0x0004:   DW_TAG_member
  DW_AT_name ("nextRespTime")
  DW_AT_data_member_location (0x08)
0x0005: DW_TAG_enumeration_type
  DW_AT_name ("PacketHeaderGC")
0x0006:   DW_TAG_enumerator
  DW_AT_name ("HEADER_GC_RESP")
  DW_AT_const_value (49)
'''
        records, aliases, headers = audit.parse_dwarf(text)
        self.assertEqual(records['SResp'][0]['size'], 20)
        self.assertEqual(records['SResp'][0]['fields'][1]['offset'], 8)
        self.assertEqual(aliases['TPacketGCRespRefresh'], {'SResp'})
        self.assertEqual(headers['HEADER_GC_RESP'], 49)


if __name__ == '__main__':
    unittest.main()
