#!/usr/bin/env python3
"""Builds classic Metin2 EterPack archives (.eix + .epk) from Tools/archiver/xml/*_create.xml.

The layout mirrors Source/Binary/source/EterPack/EterPack.{h,cpp}:
  .eix = 'EPKD' | version 2 | entry count | TEterPackIndex[count]   (little endian, #pragma pack(4))
  .epk = concatenated raw file data, no header (data_position is an absolute offset into it)
All entries use compressed_type 0 (raw), so the client reads them without any key or LZO.
"""

import argparse
import os
import re
import struct
import sys
import zlib

INDEX_FOURCC = b"EPKD"
INDEX_VERSION = 2
INDEX_HEADER = struct.Struct("<4sIl")
FILENAME_MAX_LEN = 160
COMPRESSED_TYPE_NONE = 0
MAX_PACK_SIZE = 0x7FFFFFFF

# id, filename[161] (+3 pad), filename_crc, real_data_size, data_size, data_crc, data_position, compressed_type (+3 pad)
INDEX_ENTRY = struct.Struct("<i161s3xIiiIib3x")
assert INDEX_ENTRY.size == 192

COPY_CHUNK = 1 << 20
SOURCE_ENCODINGS = ("cp1254", "utf-8", "latin-1")


def _build_crc_table():
    table = []
    for n in range(256):
        c = n
        for _ in range(8):
            c = (c >> 1) ^ 0xEDB88320 if c & 1 else c >> 1
        table.append(c)
    return table


CRC_TABLE = _build_crc_table()


def client_crc32(data):
    """GetCRC32() from EterBase/CRC32.cpp: crc = table[(crc ^ byte) & 0xff] ^ (crc >> 8), init/xorout 0xffffffff."""
    crc = 0xFFFFFFFF
    for byte in data:
        crc = CRC_TABLE[(crc ^ byte) & 0xFF] ^ (crc >> 8)
    return crc ^ 0xFFFFFFFF


def self_test():
    # Literal values copied from the CRCTable in CRC32.cpp (entries 1, 2, 128, 255).
    assert (CRC_TABLE[1], CRC_TABLE[2], CRC_TABLE[128], CRC_TABLE[255]) == (
        0x77073096, 0xEE0E612C, 0xEDB88320, 0x2D02EF8D)
    assert client_crc32(b"123456789") == 0xCBF43926
    assert client_crc32(b"") == 0
    sample = b"d:/ymir work/pc/warrior/x.dds"
    assert client_crc32(sample) == zlib.crc32(sample) & 0xFFFFFFFF


def normalize_name(raw_name):
    """inlineConvertPackFilename / CEterPackManager::ConvertFileName: '\\' -> '/', ASCII-only lowercase."""
    return raw_name.replace(b"\\", b"/").lower()


def name_crc(normalized_name):
    return client_crc32(normalized_name)


def unescape_xml_attribute(raw):
    for escaped, plain in ((b"&lt;", b"<"), (b"&gt;", b">"), (b"&quot;", b'"'), (b"&apos;", b"'"), (b"&amp;", b"&")):
        raw = raw.replace(escaped, plain)
    return raw


FILE_PATTERN = re.compile(rb'<File\s+ArchivedPath="([^"]*)"\s*>\s*<!\[CDATA\[(.*?)\]\]>', re.S)
ARCHIVE_PATH_PATTERN = re.compile(rb'<CreateEterPack\s[^>]*?ArchivePath="([^"]*)"')


def parse_xml(xml_path):
    with open(xml_path, "rb") as handle:
        content = handle.read()
    archive_match = ARCHIVE_PATH_PATTERN.search(content)
    if not archive_match:
        raise ValueError("%s: no <CreateEterPack ArchivePath=...>" % xml_path)
    pack_name = os.path.basename(archive_match.group(1).decode("latin-1").replace("\\", "/").rstrip("/"))
    files = [(unescape_xml_attribute(archived), source.strip())
             for archived, source in FILE_PATTERN.findall(content)]
    return pack_name, files


def resolve_source(base_dir, raw_source):
    # Archived names are raw cp1254 bytes, but on disk the same names are stored as decoded Unicode.
    for encoding in SOURCE_ENCODINGS:
        try:
            relative = raw_source.decode(encoding).replace("\\", "/")
        except UnicodeDecodeError:
            continue
        candidate = os.path.normpath(os.path.join(base_dir, relative))
        if os.path.isfile(candidate):
            return candidate
    return None


class PackPlan:
    def __init__(self, name):
        self.name = name
        self.entries = []
        self.missing = []
        self.empty = []
        self.duplicates = []
        self.rejected = []


def plan_pack(base_dir, pack_name, files):
    plan = PackPlan(pack_name)
    seen = set()
    for archived, raw_source in files:
        normalized = normalize_name(archived)
        source = resolve_source(base_dir, raw_source)
        if source is None:
            plan.missing.append(raw_source.decode("latin-1"))
            continue
        if len(normalized) > FILENAME_MAX_LEN:
            plan.rejected.append("name longer than %d bytes: %s" % (FILENAME_MAX_LEN, normalized.decode("latin-1")))
            continue
        if name_crc(normalized) == 0:
            plan.rejected.append("filename_crc is 0, the client treats that as a free slot: " + normalized.decode("latin-1"))
            continue
        size = os.path.getsize(source)
        if size == 0:
            # CMappedFile::Map treats size 0 as "map the whole file", so an empty entry would return the entire .epk.
            plan.empty.append(normalized.decode("latin-1"))
            continue
        if normalized in seen:
            plan.duplicates.append(normalized.decode("latin-1"))
            continue
        seen.add(normalized)
        plan.entries.append((normalized, source, size))
    return plan


def write_pack(plan, out_dir):
    """Returns (entry_count, epk_size); raises OverflowError when data_position would not fit a signed 32-bit long."""
    index_records = []
    position = 0
    epk_path = os.path.join(out_dir, plan.name + ".epk")
    with open(epk_path, "wb") as epk:
        for entry_id, (normalized, source, size) in enumerate(plan.entries):
            if position + size > MAX_PACK_SIZE:
                raise OverflowError("%s.epk would exceed 2 GiB (data_position is a 32-bit long)" % plan.name)
            data_crc = 0
            written = 0
            with open(source, "rb") as src:
                while True:
                    chunk = src.read(COPY_CHUNK)
                    if not chunk:
                        break
                    epk.write(chunk)
                    data_crc = zlib.crc32(chunk, data_crc)
                    written += len(chunk)
            if written != size:
                raise IOError("%s changed size while packing" % source)
            index_records.append(INDEX_ENTRY.pack(
                entry_id, normalized, name_crc(normalized), size, size,
                data_crc & 0xFFFFFFFF, position, COMPRESSED_TYPE_NONE))
            position += size
    with open(os.path.join(out_dir, plan.name + ".eix"), "wb") as eix:
        eix.write(INDEX_HEADER.pack(INDEX_FOURCC, INDEX_VERSION, len(index_records)))
        eix.write(b"".join(index_records))
    return len(index_records), position


def write_index_file(out_dir, pack_names):
    # PackInitialize() in UserInterface.cpp: line 0 is PACK|FILE, then (mount point, pack name) line pairs.
    # root is excluded because RegisterRootPack("pack/root") registers it unconditionally.
    lines = ["PACK"]
    for name in pack_names:
        if name != "root":
            lines.extend(["*", name])
    with open(os.path.join(out_dir, "Index"), "w", newline="") as handle:
        handle.write("\r\n".join(lines) + "\r\n")


class PackReader:
    """Reads a pack the way CEterPack::__BuildIndex / FindIndex / Get2 do."""

    def __init__(self, base_path):
        with open(base_path + ".eix", "rb") as handle:
            eix = handle.read()
        if len(eix) < INDEX_HEADER.size:
            raise ValueError("index header error")
        fourcc, version, count = INDEX_HEADER.unpack_from(eix, 0)
        if fourcc != INDEX_FOURCC:
            raise ValueError("index fourcc error")
        if version != INDEX_VERSION:
            raise ValueError("index version error")
        if len(eix) < INDEX_HEADER.size + INDEX_ENTRY.size * count:
            raise ValueError("index size error")
        self.epk_path = base_path + ".epk"
        self.epk_size = os.path.getsize(self.epk_path)
        self.entries = []
        self.by_crc = {}
        for i in range(count):
            fields = INDEX_ENTRY.unpack_from(eix, INDEX_HEADER.size + i * INDEX_ENTRY.size)
            entry = dict(zip(
                ("id", "filename", "crc", "real_size", "size", "data_crc", "position", "type"), fields))
            entry["filename"] = entry["filename"].split(b"\0", 1)[0]
            self.entries.append(entry)
            if entry["crc"] != 0:
                self.by_crc.setdefault(entry["crc"], []).append(entry)

    def find(self, name):
        normalized = normalize_name(name)
        for entry in self.by_crc.get(zlib.crc32(normalized) & 0xFFFFFFFF, []):
            if entry["filename"] == normalized:
                return entry
        return None

    def open_data(self, entry):
        """Mirrors out_file.Create(epk, &data, data_position, data_size) incl. CMappedFile::Map's size==0 quirk."""
        size = entry["size"] if entry["size"] != 0 else self.epk_size
        if entry["position"] + size > self.epk_size:
            raise ValueError("mapping past end of .epk")
        handle = open(self.epk_path, "rb")
        handle.seek(entry["position"])
        return handle, size


def files_equal(handle, size, source_path):
    with open(source_path, "rb") as src:
        remaining = size
        while remaining:
            want = min(COPY_CHUNK, remaining)
            left = handle.read(want)
            right = src.read(want)
            if left != right or len(left) != want:
                return False
            remaining -= want
        return src.read(1) == b""


def verify_pack(plan, out_dir):
    problems = []
    reader = PackReader(os.path.join(out_dir, plan.name))
    if len(reader.entries) != len(plan.entries):
        problems.append("index has %d entries, expected %d" % (len(reader.entries), len(plan.entries)))
    crc_collisions = sum(len(group) - 1 for group in reader.by_crc.values())
    for position, (normalized, source, size) in enumerate(plan.entries):
        label = normalized.decode("latin-1")
        entry = reader.find(normalized)
        if entry is None:
            problems.append("not found: " + label)
            continue
        if entry["id"] != position or entry["type"] != COMPRESSED_TYPE_NONE:
            problems.append("bad id/type: " + label)
        if entry["size"] != size or entry["real_size"] < entry["size"]:
            problems.append("bad size: " + label)
            continue
        try:
            handle, mapped_size = reader.open_data(entry)
        except ValueError as error:
            problems.append("%s: %s" % (error, label))
            continue
        with handle:
            if not files_equal(handle, mapped_size, source):
                problems.append("content mismatch: " + label)
                continue
            handle.seek(entry["position"])
            if zlib.crc32(handle.read(size)) & 0xFFFFFFFF != entry["data_crc"]:
                problems.append("data_crc mismatch: " + label)
    return len(plan.entries), crc_collisions, problems


def summarize_issues(label, items):
    if items:
        print("    %s: %d" % (label, len(items)))
        for item in items[:5]:
            print("      - " + item)
        if len(items) > 5:
            print("      ... %d more" % (len(items) - 5))


def main():
    parser = argparse.ArgumentParser(description="Build classic EterPack (.eix/.epk) archives from archiver XML lists.")
    parser.add_argument("--xml-dir", required=True, help="directory with *_create.xml (e.g. Tools/archiver/xml)")
    parser.add_argument("--out", required=True, help="output directory for <name>.eix / <name>.epk")
    parser.add_argument("--only", help="comma separated pack names to process")
    parser.add_argument("--base-dir", help="directory CDATA source paths are relative to (default: parent of --xml-dir)")
    parser.add_argument("--write-index", action="store_true", help="also write the pack/Index file PackInitialize() parses")
    parser.add_argument("--verify", action="store_true", help="re-read the produced packs and byte-compare with the sources")
    parser.add_argument("--verify-only", action="store_true", help="skip building, only verify existing output")
    args = parser.parse_args()

    self_test()

    xml_dir = os.path.abspath(args.xml_dir)
    base_dir = os.path.abspath(args.base_dir) if args.base_dir else os.path.dirname(xml_dir)
    out_dir = os.path.abspath(args.out)
    wanted = set(args.only.split(",")) if args.only else None

    xml_files = sorted(f for f in os.listdir(xml_dir) if f.endswith("_create.xml"))
    parsed = [parse_xml(os.path.join(xml_dir, f)) for f in xml_files]
    all_pack_names = sorted(name for name, _ in parsed)
    selected = [(name, files) for name, files in parsed if wanted is None or name in wanted]
    unknown = (wanted or set()) - set(all_pack_names)
    if unknown:
        print("unknown pack names: " + ", ".join(sorted(unknown)), file=sys.stderr)
        return 2

    os.makedirs(out_dir, exist_ok=True)
    failed = False

    for name, files in selected:
        plan = plan_pack(base_dir, name, files)
        print("[%s] %d listed, %d usable" % (name, len(files), len(plan.entries)))
        summarize_issues("missing source files", plan.missing)
        summarize_issues("empty files skipped", plan.empty)
        summarize_issues("duplicate names skipped", plan.duplicates)
        summarize_issues("rejected", plan.rejected)

        if not args.verify_only:
            try:
                count, size = write_pack(plan, out_dir)
            except OverflowError as error:
                print("    ERROR: %s" % error)
                failed = True
                continue
            print("    wrote %s.eix/.epk: %d entries, %.1f MiB" % (name, count, size / 1048576.0))

        if args.verify or args.verify_only:
            checked, collisions, problems = verify_pack(plan, out_dir)
            if problems:
                failed = True
                print("    VERIFY FAILED (%d problems)" % len(problems))
                for problem in problems[:10]:
                    print("      - " + problem)
            else:
                print("    VERIFY OK: %d/%d files found by CRC lookup and byte-identical (%d filename_crc collisions)"
                      % (checked, checked, collisions))

    if args.write_index:
        write_index_file(out_dir, all_pack_names)
        print("wrote %s" % os.path.join(out_dir, "Index"))

    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
