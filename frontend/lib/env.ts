import { z } from "zod";

/**
 * Typed environment boundary.
 *
 * Every environment value used by the frontend is parsed once with Zod and
 * fails fast on invalid/missing values instead of silently misbehaving.
 * Local defaults come from `frontend/.env.example` (no real secrets).
 */
const envSchema = z.object({
  NEXT_PUBLIC_API_BASE_URL: z
    .string()
    .url()
    .default("http://localhost:8000"),
});

const parsed = envSchema.safeParse({
  NEXT_PUBLIC_API_BASE_URL: process.env.NEXT_PUBLIC_API_BASE_URL,
});

if (!parsed.success) {
  throw new Error(
    `Invalid frontend environment: ${parsed.error.issues
      .map((issue) => `${issue.path.join(".")}: ${issue.message}`)
      .join("; ")}`,
  );
}

export const env = parsed.data;
