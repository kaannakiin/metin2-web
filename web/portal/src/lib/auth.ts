import { createServerFn } from "@tanstack/react-start";
import { getRequestHeader } from "@tanstack/react-start/server";
import { serverContext } from "../server/context";
import type { Limiter } from "../server/rate-limit";
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

function guard(limiter: Limiter): AuthResult | undefined {
  const { config } = serverContext();
  if (getRequestHeader("origin") !== config.SITE_ORIGIN)
    return { ok: false, error: "forbidden" };
  const verdict = limiter.take(clientIp() ?? "unknown");
  if (!verdict.allowed)
    return {
      ok: false,
      error: "rate_limited",
      retryAfterSec: verdict.retryAfterSec,
    };
  return undefined;
}

function clientIp(): string | undefined {
  return getRequestHeader(serverContext().config.CLIENT_IP_HEADER);
}

export const login = createServerFn({ method: "POST" })
  .validator(LoginBody)
  .handler(async ({ data }): Promise<AuthResult> => {
    const ctx = serverContext();
    const blocked = guard(ctx.loginLimiter);
    if (blocked) return blocked;
    const result = await ctx.accounts.check(data.login, data.password);
    if (result === "ok") return { ok: true };
    return {
      ok: false,
      error: result === "blocked" ? "blocked" : "wrong_credentials",
    };
  });

export const register = createServerFn({ method: "POST" })
  .validator(RegisterBody)
  .handler(async ({ data }): Promise<AuthResult> => {
    const ctx = serverContext();
    const blocked = guard(ctx.registerLimiter);
    if (blocked) return blocked;
    if (!(await ctx.verifyTurnstile(data.turnstileToken, clientIp())))
      return { ok: false, error: "captcha" };
    const result = await ctx.accounts.create(
      data.login,
      data.password,
      data.deleteCode,
    );
    return result === "created" ? { ok: true } : { ok: false, error: "taken" };
  });
