#!/usr/bin/env python3
"""Read-only encoding/key inventory. Exit nonzero on contract violations.

Missing keys in existing tables are a reported baseline, not newly translated
by this tool. No automatic detection, conversion, or file modification.
"""

import argparse
import importlib.util
import json
from pathlib import Path


KIT = Path(__file__).resolve().parents[1]


def load_codec():
    spec = importlib.util.spec_from_file_location("m2w_textcodec_audit", KIT / "compat/textcodec.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def audit(packs):
    codec = load_codec()
    result = {"tables": [], "errors": [], "missing_keys_against_tr": {}}
    keys = {}
    for language, encoding in codec.CONTRACT["locales"].items():
        for name in codec.CONTRACT["locale_tables"]:
            source = "locale/%s/%s" % (language, name)
            try:
                text = codec.decode_pack_text((packs / source).read_bytes(), source, 1254)
                rows = [codec.split_locale_row(line) for line in text.splitlines()]
                rows = [row for row in rows if len(row) >= 2 and row[0]]
                row_keys = [row[0] for row in rows]
                unique = set(row_keys)
                keys[language, name] = unique
                result["tables"].append({
                    "source": source, "encoding": encoding,
                    "rows": len(row_keys), "unique_keys": len(unique),
                    "duplicate_rows": len(row_keys) - len(unique),
                    "replacement_characters": text.count("\ufffd"),
                })
                if "\ufffd" in text:
                    result["errors"].append(source + ": contains U+FFFD")
            except (OSError, ValueError, UnicodeError) as error:
                result["errors"].append(str(error))

    for language in codec.CONTRACT["locales"]:
        result["missing_keys_against_tr"][language] = {
            name: len(keys.get(("tr", name), set()) - keys.get((language, name), set()))
            for name in codec.CONTRACT["locale_tables"]
        }

    labels = codec._read_json("text_labels.json")
    expected = set(codec.ui_labels("locale/en"))
    for language in codec.CONTRACT["locales"]:
        if set(labels.get(language, {})) != expected:
            result["errors"].append(language + ": missing/extra battle pass keys")
    result["label_languages"] = len(labels)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("packs", type=Path, help="unpacked root containing locale/<lang>/")
    args = parser.parse_args()
    result = audit(args.packs)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return bool(result["errors"])


if __name__ == "__main__":
    raise SystemExit(main())
