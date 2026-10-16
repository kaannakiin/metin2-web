import type { Pool, RowDataPacket } from "mysql2/promise";

export type CreateResult = "created" | "taken";
export type CheckResult = "ok" | "wrong" | "blocked";

export interface Accounts {
  create(login: string, password: string, deleteCode: string): Promise<CreateResult>;
  check(login: string, password: string): Promise<CheckResult>;
}

export function mysqlAccounts(pool: Pool): Accounts {
  return {
    async create(login, password, deleteCode) {
      try {
        await pool.execute(
          "INSERT INTO account (login, password, social_id) VALUES (?, PASSWORD(?), ?)",
          [login, password, deleteCode],
        );
        return "created";
      } catch (error) {
        if ((error as { code?: string }).code === "ER_DUP_ENTRY") return "taken";
        throw error;
      }
    },

    async check(login, password) {
      const [rows] = await pool.execute<RowDataPacket[]>(
        "SELECT status FROM account WHERE login = ? AND password = PASSWORD(?) LIMIT 1",
        [login, password],
      );
      const row = rows[0];
      if (!row) return "wrong";
      return row.status === "OK" ? "ok" : "blocked";
    },
  };
}
