import assert from "node:assert/strict";
import { describe, it } from "node:test";
import type { Pool } from "mysql2/promise";
import { mysqlAccounts } from "../src/server/accounts.ts";
import { createLimiter } from "../src/server/rate-limit.ts";
import { turnstileVerifier } from "../src/server/turnstile.ts";
import { LoginBody, RegisterBody } from "../src/server/validation.ts";

describe("createLimiter", () => {
  it("allows up to the limit, then blocks until the window resets", () => {
    let t = 0;
    const limiter = createLimiter(2, 1000, () => t);
    assert.deepEqual(limiter.take("a"), { allowed: true });
    assert.deepEqual(limiter.take("a"), { allowed: true });
    assert.deepEqual(limiter.take("a"), { allowed: false, retryAfterSec: 1 });
    t = 1000;
    assert.deepEqual(limiter.take("a"), { allowed: true });
  });

  it("counts each key separately", () => {
    const limiter = createLimiter(1, 1000, () => 0);
    assert.equal(limiter.take("a").allowed, true);
    assert.equal(limiter.take("b").allowed, true);
    assert.equal(limiter.take("a").allowed, false);
  });

  it("check does not count, hit counts without checking", () => {
    const limiter = createLimiter(2, 1000, () => 0);
    assert.equal(limiter.check("a").allowed, true);
    assert.equal(limiter.check("a").allowed, true);
    limiter.hit("a");
    limiter.hit("a");
    assert.deepEqual(limiter.check("a"), { allowed: false, retryAfterSec: 1 });
  });

  it("evicts the oldest windows when full", () => {
    const limiter = createLimiter(1, 1000, () => 0, 2);
    limiter.hit("a");
    limiter.hit("b");
    limiter.hit("c");
    assert.equal(limiter.check("a").allowed, true);
    assert.equal(limiter.check("b").allowed, false);
    assert.equal(limiter.check("c").allowed, false);
  });
});

describe("validation", () => {
  const ok = {
    login: "numan42",
    password: "Abc!123",
    deleteCode: "1234567",
    turnstileToken: "t",
  };

  it("accepts a valid registration", () => {
    assert.equal(RegisterBody.safeParse(ok).success, true);
  });

  for (const [field, value] of [
    ["login", "abc"],
    ["login", "a".repeat(17)],
    ["login", "çağrı"],
    ["login", "user name"],
    ["login", "admin'--"],
    ["password", "12345"],
    ["password", "a".repeat(17)],
    ["password", "şifre123"],
    ["password", "has space"],
    ["deleteCode", "123456"],
    ["deleteCode", "12345678"],
    ["deleteCode", "12a4567"],
    ["turnstileToken", ""],
  ] as const) {
    it(`rejects ${field} = ${JSON.stringify(value)}`, () => {
      assert.equal(
        RegisterBody.safeParse({ ...ok, [field]: value }).success,
        false,
      );
    });
  }

  it("login body ignores registration-only fields", () => {
    assert.deepEqual(LoginBody.parse(ok), {
      login: "numan42",
      password: "Abc!123",
    });
  });
});

describe("turnstileVerifier", () => {
  function fakeFetch(body: unknown, status = 200) {
    const calls: URLSearchParams[] = [];
    const fn = (async (_url: string | URL | Request, init?: RequestInit) => {
      calls.push(init?.body as URLSearchParams);
      return new Response(JSON.stringify(body), { status });
    }) as typeof fetch;
    return { fn, calls };
  }

  it("passes the secret, token and client IP", async () => {
    const { fn, calls } = fakeFetch({
      success: true,
      hostname: "metin2.kaanakin.dev",
    });
    assert.equal(
      await turnstileVerifier(
        "s3cret",
        "metin2.kaanakin.dev",
        fn,
      )("tok", "1.2.3.4"),
      true,
    );
    assert.equal(calls[0]?.get("secret"), "s3cret");
    assert.equal(calls[0]?.get("response"), "tok");
    assert.equal(calls[0]?.get("remoteip"), "1.2.3.4");
  });

  it("rejects a token solved on another hostname", async () => {
    const { fn } = fakeFetch({ success: true, hostname: "evil.example" });
    assert.equal(
      await turnstileVerifier("s", "metin2.kaanakin.dev", fn)("tok", undefined),
      false,
    );
  });

  it("rejects a failed or errored verification", async () => {
    assert.equal(
      await turnstileVerifier(
        "s",
        "h",
        fakeFetch({ success: false, hostname: "h" }).fn,
      )("t", undefined),
      false,
    );
    assert.equal(
      await turnstileVerifier("s", "h", fakeFetch({}, 500).fn)("t", undefined),
      false,
    );
  });
});

describe("mysqlAccounts", () => {
  function fakePool(handler: (sql: string, params: unknown[]) => unknown) {
    const queries: { sql: string; params: unknown[] }[] = [];
    const pool = {
      async execute(sql: string, params: unknown[]) {
        queries.push({ sql, params });
        return [handler(sql, params), []];
      },
    } as unknown as Pool;
    return { pool, queries };
  }

  it("hashes the password with PASSWORD() and binds every value", async () => {
    const { pool, queries } = fakePool(() => ({}));
    assert.equal(
      await mysqlAccounts(pool).create("numan42", "Abc!123", "1234567"),
      "created",
    );
    assert.match(queries[0]!.sql, /VALUES \(\?, PASSWORD\(\?\), \?\)/);
    assert.deepEqual(queries[0]!.params, ["numan42", "Abc!123", "1234567"]);
  });

  it("reports a duplicate login as taken", async () => {
    const { pool } = fakePool(() => {
      throw Object.assign(new Error("dup"), { code: "ER_DUP_ENTRY" });
    });
    assert.equal(
      await mysqlAccounts(pool).create("numan42", "Abc!123", "1234567"),
      "taken",
    );
  });

  it("rethrows other database errors", async () => {
    const { pool } = fakePool(() => {
      throw Object.assign(new Error("gone"), {
        code: "PROTOCOL_CONNECTION_LOST",
      });
    });
    await assert.rejects(
      mysqlAccounts(pool).create("numan42", "Abc!123", "1234567"),
      /gone/,
    );
  });

  it("maps login results to ok, wrong and blocked", async () => {
    const rows: Record<string, unknown[]> = {
      good: [{ status: "OK" }],
      banned: [{ status: "BLOCK" }],
      nobody: [],
    };
    const { pool, queries } = fakePool(
      (_sql, params) => rows[params[0] as string],
    );
    const accounts = mysqlAccounts(pool);
    assert.equal(await accounts.check("good", "pw"), "ok");
    assert.equal(await accounts.check("banned", "pw"), "blocked");
    assert.equal(await accounts.check("nobody", "pw"), "wrong");
    assert.match(queries[0]!.sql, /password = PASSWORD\(\?\)/);
  });
});
