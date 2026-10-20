"""Execute the actual character layout with each supported feature combination."""
import ast
import itertools
import os
from pathlib import Path
import sys
import types
import textwrap
import unittest
from unittest.mock import patch


SCRIPT = (Path(os.environ["M2_CHARACTER_LAYOUT"]) if "M2_CHARACTER_LAYOUT" in os.environ
          else Path(__file__).resolve().parents[2] /
          "content/client/packs/root/uiscript/characterwindow.py")


class LocaleStub(types.ModuleType):
    def __getattr__(self, name):
        return name


class CharacterWindowTest(unittest.TestCase):
    def test_layout_feature_combinations(self):
        code = compile(SCRIPT.read_text(), str(SCRIPT), "exec")
        for conqueror, renewal, emotion, title, passive in itertools.product((False, True), repeat=5):
            with self.subTest(conqueror=conqueror, renewal=renewal, emotion=emotion,
                              title=title, passive=passive):
                app = types.ModuleType("app")
                app.ENABLE_CONQUEROR_LEVEL = conqueror
                app.ENABLE_RENEWAL_QUEST = renewal
                app.ENABLE_EXPRESSING_EMOTION = emotion
                app.ENABLE_TITLE_SYSTEM = title
                app.ENABLE_PASSIVE_SYSTEM = passive
                pyapi = types.ModuleType("pyapi")
                pyapi.GetModuleName = lambda name: name
                modules = {"app": app, "pyapi": pyapi,
                           "uiScriptLocale": LocaleStub("uiScriptLocale"),
                           "localeInfo": LocaleStub("localeInfo")}
                namespace = {"__USE_DYNAMIC_MODULE__": True,
                             "SCREEN_WIDTH": 1280, "SCREEN_HEIGHT": 720}
                with patch.dict(sys.modules, modules):
                    exec(code, namespace)
                board = namespace["window"]["children"][0]
                page = next(child for child in board["children"]
                            if child["name"] == "Character_Page")
                names = [child["name"] for child in page["children"]]
                self.assertEqual(names.count("Face_Button"), int(title))
                self.assertEqual(names.count("Write_Image"), int(title))
                def flatten(node):
                    yield node["name"]
                    for child in node.get("children", ()):
                        yield from flatten(child)
                all_names = list(flatten(namespace["window"]))
                for name in ("leader_board", "LeaderAttacker", "LeaderBerserker",
                             "LeaderTanker", "LeaderDefender", "LeaderBuffer", "LeaderSkillMaster"):
                    self.assertEqual(all_names.count(name), 1)
                if passive:
                    self.assertEqual(all_names.count("passive_expanded_btn"), 1)
                binding = Path(os.environ.get("M2_CHARACTER_BINDING", str(
                    Path(__file__).resolve().parent / "../../content/client/packs/root/uicharacter.py")))
                lines = binding.read_bytes().decode("latin1").splitlines()
                start = next(i for i, line in enumerate(lines) if line.startswith("\tdef __BindObject("))
                end = next(i for i in range(start + 1, len(lines))
                           if lines[i].strip() and lines[i].startswith("\t") and
                           not lines[i].startswith("\t\t"))
                method = ast.parse(textwrap.dedent("\n".join(lines[start:end]))).body[0]
                def required(nodes):
                    for node in nodes:
                        if isinstance(node, ast.If) and isinstance(node.test, ast.Attribute) and \
                                isinstance(node.test.value, ast.Name) and node.test.value.id == "app":
                            yield from required(node.body if getattr(app, node.test.attr, False) else node.orelse)
                        else:
                            if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and \
                                    node.func.attr == "GetChild" and node.args and \
                                    isinstance(node.args[0], ast.Constant):
                                yield node.args[0].value
                            yield from required(ast.iter_child_nodes(node))
                # The shipped controller requires the expanded emotion page.
                # Verify bindings for that deployed feature; both layouts still execute above.
                if emotion:
                    self.assertEqual(set(required(method.body)) - set(all_names), set())


if __name__ == "__main__":
    unittest.main()
