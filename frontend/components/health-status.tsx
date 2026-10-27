import type { HealthCheckState } from "@/lib/api-client";

interface HealthStatusProps {
  liveness?: string;
  readiness?: string;
  checks: HealthCheckState[];
  livenessLoading: boolean;
  readinessLoading: boolean;
  livenessError?: string;
  readinessError?: string;
  onRetry: () => void;
}

const statusClass = (status?: string): string => {
  if (status === "ok" || status === "healthy") return "status-ok";
  if (status === "degraded") return "status-degraded";
  if (status === "unhealthy") return "status-unhealthy";
  return "";
};

export default function HealthStatus({
  liveness,
  readiness,
  checks,
  livenessLoading,
  readinessLoading,
  livenessError,
  readinessError,
  onRetry,
}: HealthStatusProps) {
  return (
    <section aria-label="Backend health status">
      <dl className="status-list">
        <div>
          <dt>Liveness</dt>
          <dd>
            {livenessLoading ? "checking…" : livenessError ? (
              <span className="status-unhealthy">error: {livenessError}</span>
            ) : (
              <span className={statusClass(liveness)}>{liveness ?? "unknown"}</span>
            )}
          </dd>
        </div>
        <div>
          <dt>Readiness</dt>
          <dd>
            {readinessLoading ? "checking…" : readinessError ? (
              <span className="status-unhealthy">error: {readinessError}</span>
            ) : (
              <span className={statusClass(readiness)}>{readiness ?? "unknown"}</span>
            )}
          </dd>
        </div>
      </dl>

      {checks.length > 0 && (
        <ul className="status-list" aria-label="Readiness checks">
          {checks.map((check) => (
            <li key={check.name}>
              <span className={check.ok ? "status-ok" : "status-unhealthy"}>
                {check.ok ? "✓" : "✗"} {check.name}
              </span>
              {!check.ok && <span className="shell-muted"> — {check.message}</span>}
            </li>
          ))}
        </ul>
      )}

      {(livenessError || readinessError) && (
        <button type="button" onClick={onRetry}>
          Retry
        </button>
      )}
    </section>
  );
}
