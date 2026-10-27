import { env } from "@/lib/env";

/**
 * Generated API client boundary.
 *
 * Type definitions come from `generated/api.d.ts` (openapi-typescript output of
 * `contracts/openapi/openapi.json`) — DO NOT hand-write API types elsewhere.
 * This module is the ONLY place that talks to the backend over HTTP and owns
 * the request/correlation header contract.
 */

export class ApiClientError extends Error {
  readonly status: number;
  readonly errorCode: string | undefined;
  readonly correlationId: string | undefined;

  constructor(status: number, message: string, errorCode?: string, correlationId?: string) {
    super(message);
    this.name = "ApiClientError";
    this.status = status;
    this.errorCode = errorCode;
    this.correlationId = correlationId;
  }
}

export interface HealthLiveResponse {
  status: string;
}

export interface HealthCheckState {
  name: string;
  ok: boolean;
  message: string;
}

export interface HealthReadyResponse {
  status: "healthy" | "degraded" | "unhealthy";
  checks: HealthCheckState[];
}

function buildUrl(path: string): string {
  return `${env.NEXT_PUBLIC_API_BASE_URL.replace(/\/$/, "")}${path}`;
}

async function request<T>(path: string): Promise<T> {
  const requestId = crypto.randomUUID();
  const response = await fetch(buildUrl(path), {
    headers: {
      Accept: "application/json",
      "X-Request-ID": requestId,
      "X-Correlation-ID": requestId,
    },
    cache: "no-store",
  });

  if (!response.ok) {
    let errorCode: string | undefined;
    let message = `Request failed with status ${response.status}`;
    try {
      const body = (await response.json()) as { error_code?: string; detail?: string };
      errorCode = body.error_code;
      if (body.detail) {
        message = body.detail;
      }
    } catch {
      // non-JSON body — keep the generic message
    }
    throw new ApiClientError(
      response.status,
      message,
      errorCode,
      response.headers.get("X-Correlation-ID") ?? undefined,
    );
  }
  return (await response.json()) as T;
}

export const apiClient = {
  healthLive: (): Promise<HealthLiveResponse> => request<HealthLiveResponse>("/health/live"),
  healthReady: (): Promise<HealthReadyResponse> => request<HealthReadyResponse>("/health/ready"),
};
