export type Verdict =
  { allowed: true } | { allowed: false; retryAfterSec: number };

export interface Limiter {
  take(key: string): Verdict;
  check(key: string): Verdict;
  hit(key: string): void;
}

export function createLimiter(
  limit: number,
  windowMs: number,
  now: () => number = Date.now,
  maxKeys = 10_000,
): Limiter {
  const windows = new Map<string, { count: number; resetAt: number }>();

  function window(key: string, t: number) {
    let w = windows.get(key);
    if (!w || w.resetAt <= t) {
      if (windows.size >= maxKeys) evict(t);
      w = { count: 0, resetAt: t + windowMs };
      windows.delete(key);
      windows.set(key, w);
    }
    return w;
  }

  function evict(t: number) {
    for (const [key, w] of windows) if (w.resetAt <= t) windows.delete(key);
    // Map iterates in insertion order, so this drops the oldest windows first.
    for (const key of windows.keys()) {
      if (windows.size < maxKeys) break;
      windows.delete(key);
    }
  }

  function verdict(w: { count: number; resetAt: number }, t: number): Verdict {
    return w.count >= limit
      ? { allowed: false, retryAfterSec: Math.ceil((w.resetAt - t) / 1000) }
      : { allowed: true };
  }

  return {
    take(key) {
      const t = now();
      const w = window(key, t);
      const v = verdict(w, t);
      if (v.allowed) w.count++;
      return v;
    },
    check(key) {
      const t = now();
      const w = windows.get(key);
      return w && w.resetAt > t ? verdict(w, t) : { allowed: true };
    },
    hit(key) {
      window(key, now()).count++;
    },
  };
}
