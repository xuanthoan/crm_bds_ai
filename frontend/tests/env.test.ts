import { describe, expect, it, vi } from "vitest";

describe("typed environment boundary", () => {
  it("defaults the API base URL when not configured", async () => {
    const previous = process.env.NEXT_PUBLIC_API_BASE_URL;
    delete process.env.NEXT_PUBLIC_API_BASE_URL;
    vi.resetModules();
    const { env } = await import("@/lib/env");
    expect(env.NEXT_PUBLIC_API_BASE_URL).toBe("http://localhost:8000");
    if (previous !== undefined) {
      process.env.NEXT_PUBLIC_API_BASE_URL = previous;
    }
  });

  it("accepts a valid configured URL", async () => {
    const previous = process.env.NEXT_PUBLIC_API_BASE_URL;
    process.env.NEXT_PUBLIC_API_BASE_URL = "http://localhost:9999";
    vi.resetModules();
    const { env } = await import("@/lib/env");
    expect(env.NEXT_PUBLIC_API_BASE_URL).toBe("http://localhost:9999");
    if (previous !== undefined) {
      process.env.NEXT_PUBLIC_API_BASE_URL = previous;
    }
  });
});
