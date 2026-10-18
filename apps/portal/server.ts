import { serve } from "@hono/node-server";
import { serveStatic } from "@hono/node-server/serve-static";
import { Hono } from "hono";

type StartEntry = { fetch(request: Request): Response | Promise<Response> };

const entryPath = "./dist/server/server.js";
const { default: start } = (await import(entryPath)) as { default: StartEntry };

const app = new Hono();

app.use("*", async (c, next) => {
  await next();
  c.header("X-Content-Type-Options", "nosniff");
  c.header("Content-Security-Policy", "frame-ancestors 'self'");
});

app.use(
  "/assets/*",
  serveStatic({
    root: "./dist/client",
    onFound: (_path, c) => {
      c.header("Cache-Control", "public, max-age=31536000, immutable");
    },
  }),
);

app.use("/favicon.svg", serveStatic({ root: "./dist/client" }));

app.all("*", (c) => start.fetch(c.req.raw));

const hostname = process.env.HOST ?? "127.0.0.1";
const port = Number(process.env.PORT ?? 3000);
serve({ fetch: app.fetch, hostname, port }, () =>
  console.log(`portal listening on ${hostname}:${port}`),
);
