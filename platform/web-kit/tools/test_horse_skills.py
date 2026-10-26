#!/usr/bin/env python3
"""Exercise the real staged mounted-skill gate with the current support layout."""
import shutil
import re
import subprocess
import tempfile
import unittest
from pathlib import Path

from test_text_encoding import KIT, REPO, load_tool


class HorseSkillGateTest(unittest.TestCase):
    def test_real_gate_with_horse_summon_in_slot_109(self):
        settings = (REPO / "apps/client/source/UserInterface/PythonPlayerSettingsModule.h").read_text(encoding="latin-1")
        table = settings.split("supportSkillIndexes =", 1)[1].split(";", 1)[0]
        skills = [int(value) for value in re.findall(r"\d+", table)]
        self.assertEqual(skills[109 - 101], 131)
        stage = load_tool("stage_port")
        source = (REPO / "apps/client/source/UserInterface/PythonPlayerSkill.cpp").read_text(
            encoding="latin-1"
        ).replace("\r\n", "\n")
        patches = [p for p in stage.PATCHES if p[0].endswith("/PythonPlayerSkill.cpp")]
        self.assertEqual(len(patches), 1)
        _, old, new, *_ = patches[0]
        self.assertEqual(source.count(old), 1)
        fixed = source.replace(old, new)
        start = source.index("bool CPythonPlayer::__CanUseSkill()")
        end = source.index("bool CPythonPlayer::__UseSkill", start)
        original_gate = source[start:end]
        fixed_start = fixed.index("bool CPythonPlayer::__CanUseSkill()")
        fixed_end = fixed.index("bool CPythonPlayer::__UseSkill", fixed_start)
        fixed_gate = fixed[fixed_start:fixed_end]
        compiler = shutil.which("clang++") or shutil.which("c++")
        self.assertIsNotNone(compiler, "C++ compiler required for the actual gate regression")
        harness = r'''
#include <cassert>
struct CInstanceBase {
    bool mounted = true, allowed = true;
    bool IsMountingHorse() { return mounted; }
    bool IsMountingHoverBoard() { return false; }
    bool CanUseSkill() { return allowed; }
};
struct CPythonPlayer {
    CInstanceBase actor;
    bool present = true, observer = false;
    CInstanceBase* NEW_GetMainActorPtr() { return present ? &actor : nullptr; }
    bool IsObserverMode() { return observer; }
    int GetSkillGrade(int) { return 0; }
    int GetSkillLevel(int slot) { return slot == 109 ? 10 : 40; }
    bool __CanUseSkill();
};
GATE
int main() {
    CPythonPlayer p;
    assert(p.__CanUseSkill() == EXPECT_MOUNTED);
    p.actor.mounted = false;
    assert(p.__CanUseSkill());
    p.actor.allowed = false;
    assert(!p.__CanUseSkill());
    p.actor.allowed = true;
    p.observer = true;
    assert(!p.__CanUseSkill());
    p.observer = false;
    p.present = false;
    assert(!p.__CanUseSkill());
}
'''
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for label, gate, expected in [("old", original_gate, "false"), ("fixed", fixed_gate, "true")]:
                cpp, binary = root / (label + ".cpp"), root / label
                cpp.write_text(harness.replace("GATE", gate).replace("EXPECT_MOUNTED", expected))
                subprocess.run([compiler, "-std=c++17", str(cpp), "-o", str(binary)], check=True)
                subprocess.run([str(binary)], check=True)
        # Eligibility checks still live in the separate, unmodified per-skill gate.
        for check in ["IsHorseSkill()", "CanUseWeaponType", '"IN_SAFE"', '"NOT_ENOUGH_SP"']:
            self.assertEqual(source.count(check), fixed.count(check))


if __name__ == "__main__":
    unittest.main()
