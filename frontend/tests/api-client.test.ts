import { afterEach, describe, expect, it, vi } from "vitest";
import { ApiClientError, apiClient } from "@/lib/api-client";

describe("apiClient boundary", () => {
  afterEach(() => {
    vi.unstubAllGlobals();
  });

  it("maps a 503 Problem Details response into ApiClientError with error_code", async () => {
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue(
      new Response(
        JSON.stringify({
          type: "about:blank",
          title: "unhealthy",
          status: 503,
          detail: "database unreachable",
          instance: "/health/ready",
          error_code: "COMMON_DEPENDENCY_UNAVAILABLE",
        }),
        { status: 503, headers: { "Content-Type": "application/json", "X-Correlation-ID": "corr-1" } },
      ),
    ));

    await expect(apiClient.healthReady()).rejects.toMatchObject({
      name: "ApiClientError",
      status: 503,
      errorCode: "COMMON_DEPENDENCY_UNAVAILABLE",
      correlationId: "corr-1",
    });
  });

  it("propagates X-Request-ID and X-Correlation-ID headers", async () => {
    const fetchMock = vi.fn().mockResolvedValue(
      new Response(JSON.stringify({ status: "ok" }), {
        status: 200,
        headers: { "Content-Type": "application/json" },
      }),
    );
    vi.stubGlobal("fetch", fetchMock);

    await apiClient.healthLive();

    const [url, init] = fetchMock.mock.calls[0] as [string, RequestInit];
    expect(url).toContain("/health/live");
    const headers = init.headers as Record<string, string>;
    expect(headers["X-Request-ID"]).toBeTruthy();
    expect(headers["X-Correlation-ID"]).toBeTruthy();
  });
});
