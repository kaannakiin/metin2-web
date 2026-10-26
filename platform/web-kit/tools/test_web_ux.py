"""Login methods run against the same file bridge as the browser release."""
import importlib.util
import sys
import types
import unittest
from pathlib import Path
from unittest.mock import patch


class Field:
    def __init__(self, value=""):
        self.value = value
        self.enabled = True
    def GetText(self): return self.value
    def SetText(self, value): self.value = value
    def SetFocus(self): self.focused = True
    def Enable(self): self.enabled = True
    def Disable(self): self.enabled = False
    def Show(self): pass
    def Hide(self): pass
    def SetToolTipText(self, value): self.tooltip = value


class Base:
    def Open(self): pass
    def Close(self): pass
    def OnUpdate(self): pass
    def Connect(self, login, password): self.connections.append((login, password))
    def PopupNotifyMessage(self, message): self.messages.append(message)


class WebUXTests(unittest.TestCase):
    def setUp(self):
        app = types.SimpleNamespace(GetLocalePath=lambda: "locale/tr")
        spec = importlib.util.spec_from_file_location("web_ux_test_module", Path(__file__).parent.parent / "compat/web_ux.py")
        self.module = importlib.util.module_from_spec(spec)
        with patch.dict(sys.modules, app=app):
            spec.loader.exec_module(self.module)
        cls = type("Window", (Base,), {})
        self.module.install(cls)
        self.window = cls()
        self.window._webux_login = self.window._webux_action = None
        self.window.loginButton = Field()
        self.window.idEditLine = Field("test_user")
        self.window.pwdEditLine = Field("secret")
        self.window.connections, self.window.messages = [], []
        self.window.accountData = {i: ([Field(), Field(), Field()], Field()) for i in range(4)}
        self.request = patch.object(self.module, "_request", return_value="request-1").start()
        self.read = patch.object(self.module, "_read", return_value={}).start()
        self.addCleanup(patch.stopall)

    def test_auth_waits_for_matching_success_and_close_discards_credentials(self):
        self.window.Connect("test_user", "secret")
        self.assertEqual(self.window.connections, [])
        self.request.assert_called_once_with("prepare_login")
        self.read.return_value = {"id": "wrong-request", "ok": True}
        self.window.OnUpdate()
        self.assertEqual(self.window.connections, [])
        self.read.return_value = {"id": "request-1", "ok": True}
        self.window.OnUpdate()
        self.assertEqual(self.window.connections, [("test_user", "secret")])
        self.window.Connect("test_user", "another-secret")
        self.window.Close()
        self.assertIsNone(self.window._webux_login)

    def test_failed_preparation_does_not_authenticate(self):
        self.window.Connect("test_user", "secret")
        self.read.return_value = {"id": "request-1", "ok": False}
        self.window.OnUpdate()
        self.assertEqual(self.window.connections, [])
        self.assertIsNone(self.window._webux_login)
        self.assertTrue(self.window.loginButton.enabled)

    def test_remember_waits_for_browser_confirmation_and_never_sends_password(self):
        self.window.SaveAccount(0)
        self.request.assert_called_once_with("remember", slot=0, login="test_user")
        self.assertEqual(self.window.messages, [])
        self.read.return_value = {"id": "request-1", "ok": False}
        self.window.OnUpdate()
        self.assertNotIn("hatırlandı", self.window.messages[-1])

    def test_loading_username_clears_a_different_accounts_password(self):
        self.read.return_value = {"accounts": ["other_user", "", "", ""]}
        self.window.LoadAccount(0)
        self.assertEqual(self.window.idEditLine.value, "other_user")
        self.assertEqual(self.window.pwdEditLine.value, "")


if __name__ == "__main__":
    unittest.main()
