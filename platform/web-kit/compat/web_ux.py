"""Browser login UX. Files carry readiness/username commands, never passwords."""
import json
import time
import app


def _read(path):
    try:
        with open(path, encoding="utf-8") as source:
            return json.load(source)
    except (OSError, ValueError):
        return {}


def _text(tr, en):
    return tr if app.GetLocalePath().replace("\\", "/").endswith("/tr") else en


def _request(action, **fields):
    request_id = str(time.monotonic_ns())
    fields.update(id=request_id, action=action)
    with open("/m2w_browser_request", "w", encoding="utf-8") as target:
        json.dump(fields, target)
    return request_id


def _accounts():
    values = _read("/m2w_browser_state").get("accounts", [])
    return [values[i] if i < len(values) and isinstance(values[i], str) else "" for i in range(4)]


def install(cls):
    """Only the generated web LoginWindow is adapted; source packs stay intact."""
    if getattr(cls, "_webux_installed", False):
        return
    cls._webux_installed = True
    original_open, original_close = cls.Open, cls.Close
    original_update, original_connect = cls.OnUpdate, cls.Connect

    def check_accounts(self):
        for slot, login in enumerate(_accounts()):
            buttons, label = self.accountData[slot]
            label.SetText(login or _text("Boş — kullanıcı adı", "Empty — username"))
            (buttons[1].Hide if login else buttons[1].Show)()
            (buttons[0].Show if login else buttons[0].Hide)()

    def open_window(self):
        self._webux_login = None
        self._webux_action = None
        original_open(self)
        for buttons, _label in self.accountData.values():
            for button, label in zip(buttons, [
                _text("Hatırlanan kullanıcı adını sil", "Forget username"),
                _text("Kullanıcı adını hatırla — şifre saklanmaz", "Remember username — password is not saved"),
                _text("Kullanıcı adını doldur; şifreni yaz", "Fill username, then enter your password"),
            ]):
                button.SetToolTipText(label)
        self.loginButton.SetToolTipText(_text("Giriş yap (Enter)", "Sign in (Enter)"))
        check_accounts(self)

    def close_window(self):
        self._webux_login = None
        self._webux_action = None
        original_close(self)

    def connect(self, login, password):
        # Keep credentials only in this window's memory while downloads finish.
        # No auth connection is opened until the startup working set is in RAM.
        if self._webux_login or self._webux_action:
            return
        try:
            request_id = _request("prepare_login")
        except OSError:
            self.PopupNotifyMessage(_text("Oyun verileri hazırlanamadı. Sayfayı yenile.", "Cannot prepare game data. Reload the page."))
            return
        self._webux_login = (request_id, login, password)
        self.loginButton.Disable()

    def update(self):
        response = _read("/m2w_browser_reply")
        pending = getattr(self, "_webux_login", None)
        if pending and response.get("id") == pending[0]:
            self._webux_login = None
            self.loginButton.Enable()
            if response.get("ok") is True:
                original_connect(self, pending[1], pending[2])
            else:
                self.PopupNotifyMessage(_text("İndirme tamamlanamadı. Yeniden giriş yapmayı dene.", "Download failed. Try signing in again."))
        action = getattr(self, "_webux_action", None)
        if action and response.get("id") == action[0]:
            self._webux_action = None
            check_accounts(self)
            if response.get("ok") is True:
                self.PopupNotifyMessage(action[1])
            else:
                self.PopupNotifyMessage(_text("Tarayıcı bu kullanıcı adını saklayamadı.", "Your browser could not save this username."))
        original_update(self)

    def account_action(self, slot, action):
        if getattr(self, "_webux_login", None) or getattr(self, "_webux_action", None):
            return
        login = self.idEditLine.GetText().strip()
        if action == "remember" and (not login or len(login) > 30 or not all(c.isascii() and (c.isalnum() or c == "_") for c in login)):
            self.PopupNotifyMessage(_text("Önce geçerli kullanıcı adını yaz.", "Enter a valid username first."))
            return
        try:
            request_id = _request(action, slot=slot, login=login if action == "remember" else "")
            message = _text("Kullanıcı adı hatırlandı. Şifre saklanmadı.", "Username remembered. Password was not saved.") if action == "remember" else _text("Kullanıcı adı silindi.", "Username forgotten.")
            self._webux_action = (request_id, message)
        except OSError:
            self.PopupNotifyMessage(_text("Kullanıcı adı saklanamadı.", "Could not save username."))

    def load_account(self, slot):
        login = _accounts()[slot]
        if login:
            self.idEditLine.SetText(login)
            self.pwdEditLine.SetText("")
            self.pwdEditLine.SetFocus()
        else:
            self.PopupNotifyMessage(_text("Bu alanda hatırlanan kullanıcı adı yok.", "No username saved in this slot."))

    cls.Open, cls.Close = open_window, close_window
    cls.OnUpdate, cls.Connect = update, connect
    cls.CheckAccount, cls.LoadAccount = check_accounts, load_account
    cls.SaveAccount = lambda self, slot: account_action(self, slot, "remember")
    cls.DeleteAccount = lambda self, slot: account_action(self, slot, "forget")
