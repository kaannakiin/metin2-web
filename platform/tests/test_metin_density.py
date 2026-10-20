import importlib.util
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location('density', ROOT / 'platform/tools/metin_density.py')
density = importlib.util.module_from_spec(spec)
spec.loader.exec_module(density)


class MetinDensityTests(unittest.TestCase):
    def setUp(self):
        self.policy = json.loads((ROOT / 'platform/gameplay/metin_density.json').read_text())
        self.spec = self.policy['maps'][0]
        self.data = (ROOT / 'runtime/freebsd/share/locale/europe' / self.spec['path']).read_bytes()

    def test_actual_13_maps_double_capacity_without_changing_other_rows(self):
        result = density.check()
        self.assertEqual(len(result['maps']), 13)
        self.assertEqual((result['before'], result['after']), (97,194))
        self.assertEqual(sum(row['added_records'] for row in result['maps']), 97)

    def test_shared_regen_counter_is_rejected(self):
        old, new = self.data.split(density.MARKER.encode())
        lines = new.splitlines(keepends=True)
        row = lines[1].decode().split()
        row[9] = '2'
        lines[1] = ('\t'.join(row) + '\n').encode()
        with self.assertRaises(ValueError):
            density.validate(self.spec, old + density.MARKER.encode() + b''.join(lines))

    def test_changed_original_timer_is_rejected(self):
        old, new = self.data.split(density.MARKER.encode())
        with self.assertRaises(ValueError):
            density.validate(self.spec, old.replace(b'2000s', b'1000s', 1) + density.MARKER.encode() + new)

    def test_ore_cannot_be_duplicated_as_a_metin(self):
        old, new = self.data.split(density.MARKER.encode())
        ore = next(line for line in old.splitlines() if line.startswith(b'r\t'))
        lines = new.splitlines(keepends=True)
        lines[1] = ore + b'\n'
        with self.assertRaises(ValueError):
            density.validate(self.spec, old + density.MARKER.encode() + b''.join(lines))

    def test_missing_one_area_even_with_same_total_is_rejected(self):
        old, new = self.data.split(density.MARKER.encode())
        lines = new.splitlines(keepends=True)
        lines[2] = lines[1]
        with self.assertRaises(ValueError):
            density.validate(self.spec, old + density.MARKER.encode() + b''.join(lines))


if __name__ == '__main__':
    unittest.main()
