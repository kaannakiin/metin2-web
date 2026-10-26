import importlib.util
from pathlib import Path
import shlex
import shutil
import subprocess
import sys
import tempfile
import types
import unittest
from unittest.mock import patch

from audit_text_encoding import audit, load_codec


KIT = Path(__file__).resolve().parents[1]
REPO = KIT.parents[1]
codec = load_codec()


def load_tool(name):
    workspace = types.ModuleType("workspace")
    workspace.CLIENT = ""
    workspace.GAME_FILES = ""
    workspace.FONT = ""
    workspace.PYTHON_2TO3 = sys.executable
    workspace.SOURCE_LIBRARIES = ""
    workspace.TREE = ""
    workspace.server_address = lambda: ""
    workspace.setting = lambda *args, default=None: default
    spec = importlib.util.spec_from_file_location("text_test_" + name, KIT / (name + ".py"))
    module = importlib.util.module_from_spec(spec)
    with patch.dict(sys.modules, workspace=workspace):
        spec.loader.exec_module(module)
    return module


class TextEncodingTests(unittest.TestCase):
    def test_utf8_script_is_independent_of_display_codepage(self):
        title = "Savaş Bileti Seçiniz"
        self.assertEqual(codec.decode_pack_text(title.encode(), "uiMiniMap.py", 1254), title)
        self.assertNotEqual(title.encode().decode("cp1254"), title)

    def test_all_language_tables_decode_by_file_contract(self):
        samples = {
            "tr": "İı Şş Ğğ Üü Öö Çç", "en": "English",
            "de": "äöüß", "pl": "ąęłńśźż", "cz": "čřěů",
            "hu": "őű", "pt": "ãõç", "ro": "ăâîșț",
            "fr": "éèêç", "es": "ñá¿¡", "it": "àèìòù",
        }
        self.assertEqual(set(samples), set(codec.CONTRACT["locales"]))
        for language, text in samples.items():
            with self.subTest(language=language):
                encoding = codec.CONTRACT["locales"][language]
                data = text.encode(encoding)
                for name in codec.CONTRACT["locale_tables"]:
                    path = "locale/%s/%s" % (language, name)
                    self.assertEqual(codec.decode_pack_text(data, path, 1254), text)

    def test_strict_failure_has_source_and_offset(self):
        with self.assertRaisesRegex(UnicodeError, r"uiBad.py.*offset 0"):
            codec.decode_pack_text(b"\xff", "uiBad.py", 1254)
        with self.assertRaisesRegex(UnicodeError, "locale/tr/locale_game.txt"):
            codec.decode_pack_text(b"\x81", "locale/tr/locale_game.txt", 1254)

    def test_no_double_decode_or_repair(self):
        text = "Savaş Bileti"
        self.assertIs(codec.decode_pack_text(text, "uiMiniMap.py", 1254), text)
        broken = "SavaÅŸ"
        self.assertEqual(codec.decode_pack_text(broken, "uiMiniMap.py", 1254), broken)

    def test_generated_python_cookie_matches_actual_bytes(self):
        rewrite = load_tool("tools/rewrite_scripts")
        content = '#!/usr/bin/python\r\n# coding: cp1254\r\ntext = "Ücretsiz"\r\n'
        normalized = rewrite.normalize_utf8_cookie(content)
        self.assertIn("# coding: utf-8\r\n", normalized)
        self.assertEqual(normalized.count("\r\n"), 3)
        namespace = {}
        exec(compile(normalized.encode("utf-8"), "generated.py", "exec"), namespace)
        self.assertEqual(namespace["text"], "Ücretsiz")

    def test_bom_newlines_last_row_and_format_fields(self):
        for ending in ("", "\n", "\r\n"):
            row = "KEY\tİı %s %d {} |cfffffffftext|r" + ending
            self.assertEqual(codec.split_locale_row(row), ["KEY", "İı %s %d {} |cfffffffftext|r"])
        self.assertEqual(codec.split_locale_row("\ufeffKEY\tText"), ["KEY", "Text"])
        self.assertEqual(codec.decode_pack_text(b"\xef\xbb\xbfKEY\tText", "locale/pl/locale_game.txt", 1254), "KEY\tText")

    def test_paths_are_case_and_separator_independent(self):
        self.assertEqual(codec.registered_encoding(r"D:\LOCALE\TR\locale_game.txt"), "cp1254")
        self.assertEqual(codec.registered_encoding("UIScript/Window.PY"), "utf-8-sig")
        with self.assertRaisesRegex(ValueError, "unregistered locale"):
            codec.registered_encoding("locale/xx/locale_game.txt")

    def test_unmigrated_legacy_and_binary_are_not_reinterpreted(self):
        self.assertEqual(codec.decode_pack_text(b"\xdc" + b"cretsiz", "locale/tr/description.txt", 1254), "Ücretsiz")
        raw = b"\x00\xff\x80"
        self.assertIs(codec.decode_pack_text(raw, "module.pyc", 1254), raw)

    def test_battlepass_labels_complete_and_fallback_explicit(self):
        labels = codec._read_json("text_labels.json")
        for language in codec.CONTRACT["locales"]:
            self.assertEqual(set(labels[language]), set(labels["en"]))
            self.assertEqual(codec.ui_labels("locale/" + language), labels[language])
        self.assertEqual(codec.ui_labels("locale/unknown"), labels["en"])
        self.assertEqual(codec.ui_labels("locale/tr")["BATTLEPASS_FREE"], "Ücretsiz")

    def test_repository_locale_contract(self):
        packs = REPO / "content/client/packs"
        if not packs.exists():
            self.skipTest("run the read-only audit against unpacked packs on the build host")
        result = audit(packs)
        self.assertEqual(result["errors"], [])
        self.assertEqual(len(result["tables"]), 22)

    def test_stage_patch_matches_real_pack_source(self):
        stage = load_tool("stage_port")
        source = REPO / "apps/client/source/UserInterface/PythonPackModule.cpp"
        if not source.exists():
            self.skipTest("real source is checked by patchcheck.py on the build host")
        content = source.read_bytes().decode("latin1").replace("\r\n", "\n")
        entries = [entry for entry in stage.PATCHES if entry[0] == "UserInterface/PythonPackModule.cpp"]
        self.assertEqual(len(entries), 2)
        for _, old, new, _ in entries:
            self.assertEqual(content.count(old), 1)
            content = content.replace(old, new)
        self.assertIn("M2W_DecodePackText(strFileName", content)
        self.assertNotIn('Py_BuildValue("s#"', content)

    def test_data_pack_installs_codec_and_contracts(self):
        module = load_tool("tools/build_client_data")
        with tempfile.TemporaryDirectory() as temp:
            module.TARGET = temp
            self.assertEqual(module.copy_text_codec(), 3)
            for name in ("textcodec.py", "text_encoding.json", "text_labels.json"):
                self.assertEqual((Path(temp) / name).read_bytes(), (KIT / "compat" / name).read_bytes())

    def test_build_checks_inputs_before_removing_previous_data(self):
        module = load_tool("tools/build_client_data")
        with tempfile.TemporaryDirectory() as temp:
            module.CLIENT = temp
            module.SCRIPTS = str(Path(temp) / "bad-input")
            module.TARGET = str(Path(temp) / "previous-data")
            previous = Path(module.TARGET)
            previous.mkdir()
            marker = previous / "keep"
            marker.write_bytes(b"previous build")
            with self.assertRaisesRegex(SystemExit, "Text encoding contract failed"):
                module.main()
            self.assertEqual(marker.read_bytes(), b"previous build")

    def test_real_script_patches_share_parser_and_localize_battlepass(self):
        from script_patches import PATCHES_SCRIPTS
        rewrite = load_tool("tools/rewrite_scripts")
        root = REPO / "content/client/packs/root"
        if not root.exists():
            self.skipTest("source pack is not installed on the build host")
        for name in ("localeInfo.py", "uiScriptLocale.py", "uiMiniMap.py"):
            content = "".join(rewrite._decode_line(line) for line in
                              (root / name.lower()).read_bytes().splitlines(keepends=True))
            content = content.replace("\r\n", "\n")
            for filename, old, new, _ in PATCHES_SCRIPTS:
                if filename.lower() == name.lower() and ("textcodec" in new or
                        "split_locale_row" in new or "ui_labels(" in new or
                        "uiScriptLocale.BATTLEPASS_" in new):
                    self.assertEqual(content.count(old), 1, (name, old))
                    content = content.replace(old, new)
            if name == "uiMiniMap.py":
                self.assertIn("SetText(uiScriptLocale.BATTLEPASS_SELECT_PASS)", content)
                self.assertNotIn('SetAcceptText("Ücretsiz")', content)
            else:
                self.assertNotIn('line[:-1].split("\\t")', content)

    def test_native_cpp_python_pack_boundary(self):
        compiler = shutil.which("clang++") or shutil.which("c++")
        config = shutil.which("python3-config")
        if not compiler or not config:
            self.skipTest("native pack boundary needs a C++ compiler and python3-config")
        flags = subprocess.check_output([config, "--includes", "--embed", "--ldflags"], text=True)
        with tempfile.TemporaryDirectory() as temp:
            target = Path(temp) / "test_pack_text"
            command = [compiler, "-std=c++17", "-DPY_SSIZE_T_CLEAN", "-I" + str(KIT / "compat"),
                       str(KIT / "tools/test_pack_text.cpp"), "-o", str(target)] + shlex.split(flags)
            subprocess.run(command, check=True, capture_output=True, text=True)
            result = subprocess.run([str(target), str(KIT / "compat")], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
