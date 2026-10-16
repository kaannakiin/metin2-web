import { SITE } from "../site";

// client.html reads this key once, deletes it and keeps the credentials in memory
// only; the 60 s expiry stops a stale entry from logging in a later visit.
const HANDOFF_KEY = "m2w.autologin";

export function launchGame(login: string, password: string) {
  try {
    sessionStorage.setItem(HANDOFF_KEY, JSON.stringify({ login, password, expires: Date.now() + 60_000 }));
  } catch {
    // Storage blocked: the game still opens on its own login screen.
  }
  window.location.assign(SITE.gameUrl);
}
