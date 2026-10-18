import { createServerFn } from "@tanstack/react-start";
import { getRequestHeader } from "@tanstack/react-start/server";
import { serverContext } from "../server/context";
import type { Limiter, Verdict } from "../server/rate-limit";
import { LoginBody, RegisterBody } from "../server/validation";

export type AuthError =
  | "wrong_credentials"
  | "blocked"
  | "taken"
  | "captcha"
  | "rate_limited"
  | "forbidden";

export type AuthResult =
  { ok: true } | { ok: false; error: AuthError; retryAfterSec?: number };

const FORBIDDEN: AuthResult = { ok: false, error: "forbidden" };

function limited(verdict: Verdict): AuthResult | undefined {
  return verdict.allowed
    ? undefined
    : {
        ok: false,
        error: "rate_limited",
        retryAfterSec: verdict.retryAfterSec,
      };
}

// The IP header is only trustworthy because Traefik admits Cloudflare's ranges
// alone; without it the request did not come through Cloudflare.
function clientIp(): string | undefined {
  const ip = getRequestHeader(serverContext().config.CLIENT_IP_HEADER);
  return ip ?? (import.meta.env.DEV ? "local" : undefined);
}

function guard(limiter: Limiter): { ip: string } | AuthResult {
  if (getRequestHeader("origin") !== serverContext().config.SITE_ORIGIN)
    return FORBIDDEN;
  const ip = clientIp();
  if (!ip) return FORBIDDEN;
  return limited(limiter.take(ip)) ?? { ip };
}

export const login = createServerFn({ method: "POST" })
  .validator(LoginBody)
  .handler(async ({ data }): Promise<AuthResult> => {
    const ctx = serverContext();
    const passed = guard(ctx.loginLimiter);
    if (!("ip" in passed)) return passed;
    // Logins compare case-insensitively in MariaDB, so one lock covers every spelling.
    const account = data.login.toLowerCase();
    const locked = limited(ctx.loginFailureLimiter.check(account));
    if (locked) return locked;
    const result = await ctx.accounts.check(data.login, data.password);
    if (result === "ok") return { ok: true };
    if (result === "wrong") ctx.loginFailureLimiter.hit(account);
    return {
      ok: false,
      error: result === "blocked" ? "blocked" : "wrong_credentials",
    };
  });

export const register = createServerFn({ method: "POST" })
  .validator(RegisterBody)
  .handler(async ({ data }): Promise<AuthResult> => {
    const ctx = serverContext();
    const passed = guard(ctx.registerLimiter);
    if (!("ip" in passed)) return passed;
    if (!(await ctx.verifyTurnstile(data.turnstileToken, passed.ip)))
      return { ok: false, error: "captcha" };
    const result = await ctx.accounts.create(
      data.login,
      data.password,
      data.deleteCode,
    );
    return result === "created" ? { ok: true } : { ok: false, error: "taken" };
  });
