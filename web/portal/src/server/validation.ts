import { z } from "zod";

// The game client sends the password as cp1254 bytes and the server hashes it
// with PASSWORD(); anything beyond printable ASCII would hash differently here.
const login = z.string().regex(/^[A-Za-z0-9]{4,16}$/);
const password = z.string().regex(/^[\x21-\x7E]{6,16}$/);
const deleteCode = z.string().regex(/^\d{7}$/);

export const LoginBody = z.object({ login, password });

export const RegisterBody = z.object({
  login,
  password,
  deleteCode,
  turnstileToken: z.string().min(1).max(2048),
});

export type LoginBody = z.infer<typeof LoginBody>;
export type RegisterBody = z.infer<typeof RegisterBody>;
