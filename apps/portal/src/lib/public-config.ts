import { createServerFn } from "@tanstack/react-start";
import { loadPublicConfig } from "../server/config";

export const getPublicConfig = createServerFn({ method: "GET" }).handler(
  () => ({
    turnstileSiteKey: loadPublicConfig().TURNSTILE_SITE_KEY,
  }),
);
