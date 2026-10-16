export interface Limiter {
  take(key: string): { allowed: true } | { allowed: false; retryAfterSec: number };
}

export function createLimiter(limit: number, windowMs: number, now: () => number = Date.now): Limiter {
  const windows = new Map<string, { count: number; resetAt: number }>();

  function prune(t: number) {
    for (const [key, w] of windows) if (w.resetAt <= t) windows.delete(key);
  }

  return {
    take(key) {
      const t = now();
      if (windows.size > 10_000) prune(t);
      let w = windows.get(key);
      if (!w || w.resetAt <= t) {
        w = { count: 0, resetAt: t + windowMs };
        windows.set(key, w);
      }
      if (w.count >= limit) return { allowed: false, retryAfterSec: Math.ceil((w.resetAt - t) / 1000) };
      w.count++;
      return { allowed: true };
    },
  };
}
