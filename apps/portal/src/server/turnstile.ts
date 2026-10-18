export type VerifyTurnstile = (
  token: string,
  ip: string | undefined,
) => Promise<boolean>;

const SITEVERIFY = "https://challenges.cloudflare.com/turnstile/v0/siteverify";

export function turnstileVerifier(
  secret: string,
  expectedHostname: string,
  fetchImpl: typeof fetch = fetch,
): VerifyTurnstile {
  return async (token, ip) => {
    const form = new URLSearchParams({ secret, response: token });
    if (ip) form.set("remoteip", ip);
    const response = await fetchImpl(SITEVERIFY, {
      method: "POST",
      body: form,
      signal: AbortSignal.timeout(5000),
    });
    if (!response.ok) return false;
    const result = (await response.json()) as {
      success?: boolean;
      hostname?: string;
    };
    return result.success === true && result.hostname === expectedHostname;
  };
}
