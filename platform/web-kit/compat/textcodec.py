"""Text-file boundary for the web client. Network bytes use a separate codec.

No encoding detection and no mojibake repair. Only registered file classes
become strict here; unregistered legacy text keeps its previous behaviour.
This module is also imported by the offline audit and regression tests.
"""

import json
import os


def _read_json(name):
    # These files are installed beside this module by build_client_data.py.
    # The game's pack importer executes modules without setting __file__.
    # In that case the package files are in the engine's working directory.
    directory = os.path.dirname(globals().get("__file__", ""))
    with open(os.path.join(directory, name), encoding="utf-8") as source:
        return json.load(source)


CONTRACT = _read_json("text_encoding.json")
if CONTRACT.get("version") != 1:
    raise ValueError("unsupported text encoding contract")


def _path(source):
    return str(source).replace("\\", "/").lower()


def registered_encoding(source):
    """Return an explicit file encoding, or None for unmigrated legacy text."""
    name = _path(source)
    if name.endswith(".py"):
        return CONTRACT["generated_python"]
    parts = name.split("/")
    if len(parts) >= 3 and parts[-3] == "locale" and parts[-1] in CONTRACT["locale_tables"]:
        language = parts[-2]
        if language not in CONTRACT["locales"]:
            raise ValueError("unregistered locale table: " + str(source))
        return CONTRACT["locales"][language]
    return None


def decode_text(data, encoding, source):
    """Decode known bytes once. Already decoded text is left unchanged."""
    if isinstance(data, str):
        return data
    if not isinstance(data, bytes):
        raise TypeError("text input must be bytes or str: " + str(source))
    try:
        return data.decode(encoding, errors="strict")
    except UnicodeDecodeError as error:
        # Do not put the file contents (possibly player text) in diagnostics.
        raise UnicodeError("%s [%s]: invalid bytes at offset %d" %
                           (source, encoding, error.start)) from error


def decode_pack_text(data, source, legacy_codepage):
    """pack.Get boundary: source encoding is independent of the display locale."""
    if _path(source).endswith(".pyc"):
        # marshal consumes bytes; the previous decoder corrupted bytecode.
        return data
    encoding = registered_encoding(source)
    if encoding is not None:
        return decode_text(data, encoding, source)
    if CONTRACT["unregistered_pack_text"] != "legacy-replace":
        raise ValueError("unregistered text source: " + str(source))
    # Deliberately limited migration. Descriptions and quest files need their
    # own inventory before changing their historical locale-codepage policy.
    if isinstance(data, str):
        return data
    return data.decode("cp%d" % legacy_codepage, errors="replace")


def split_locale_row(line):
    """Keep the last character even when the file has no final newline."""
    if not isinstance(line, str):
        raise TypeError("locale rows must be decoded text")
    return line.lstrip("\ufeff").rstrip("\r\n").split("\t")


_LABELS = None


def ui_labels(locale_path):
    global _LABELS
    if _LABELS is None:
        _LABELS = _read_json("text_labels.json")
    language = _path(locale_path).rstrip("/").split("/")[-1]
    # Explicit fallback for the new keys; existing locale dictionaries retain
    # their existing fallback policy until their missing-key audit is resolved.
    result = dict(_LABELS["en"])
    result.update(_LABELS.get(language, {}))
    return result
