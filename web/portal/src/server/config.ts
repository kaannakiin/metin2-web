import { z } from "zod";

const Env = z.object({
  SITE_ORIGIN: z.url(),
  DB_HOST: z.string().min(1),
  DB_PORT: z.coerce.number().int().positive().default(3306),
  DB_USER: z.string().min(1),
  DB_PASSWORD: z.string().min(1),
  DB_NAME: z.string().default("account"),
  TURNSTILE_SECRET: z.string().min(1),
  CLIENT_IP_HEADER: z.string().default("cf-connecting-ip"),
});

export type Config = z.infer<typeof Env>;

export function loadConfig(env: NodeJS.ProcessEnv = process.env): Config {
  return Env.parse(env);
}

const PublicEnv = z.object({ TURNSTILE_SITE_KEY: z.string().min(1) });

export function loadPublicConfig(env: NodeJS.ProcessEnv = process.env) {
  return PublicEnv.parse(env);
}
