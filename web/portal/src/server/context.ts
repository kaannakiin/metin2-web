import { createPool } from "mysql2/promise";
import { type Accounts, mysqlAccounts } from "./accounts";
import { type Config, loadConfig } from "./config";
import { type Limiter, createLimiter } from "./rate-limit";
import { type VerifyTurnstile, turnstileVerifier } from "./turnstile";

export interface ServerContext {
  config: Config;
  accounts: Accounts;
  verifyTurnstile: VerifyTurnstile;
  loginLimiter: Limiter;
  loginFailureLimiter: Limiter;
  registerLimiter: Limiter;
}

let context: ServerContext | undefined;

export function serverContext(): ServerContext {
  if (context) return context;
  const config = loadConfig();
  const pool = createPool({
    host: config.DB_HOST,
    port: config.DB_PORT,
    user: config.DB_USER,
    password: config.DB_PASSWORD,
    database: config.DB_NAME,
    charset: "utf8mb4",
    connectionLimit: 4,
  });
  context = {
    config,
    accounts: mysqlAccounts(pool),
    verifyTurnstile: turnstileVerifier(
      config.TURNSTILE_SECRET,
      new URL(config.SITE_ORIGIN).hostname,
    ),
    loginLimiter: createLimiter(10, 10 * 60_000),
    loginFailureLimiter: createLimiter(5, 15 * 60_000),
    registerLimiter: createLimiter(5, 60 * 60_000),
  };
  return context;
}
