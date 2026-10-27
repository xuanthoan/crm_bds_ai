"use client";

import { apiClient } from "@/lib/api-client";
import HealthStatus from "@/components/health-status";
import { useQuery } from "@tanstack/react-query";

export default function HealthPage() {
  const liveQuery = useQuery({
    queryKey: ["health", "live"],
    queryFn: () => apiClient.healthLive(),
  });
  const readyQuery = useQuery({
    queryKey: ["health", "ready"],
    queryFn: () => apiClient.healthReady(),
  });

  return (
    <main id="main-content" className="shell-page">
      <header className="shell-header">
        <p className="eyebrow">Technical shell</p>
        <h1>Backend health</h1>
      </header>

      <HealthStatus
        liveness={liveQuery.data?.status}
        readiness={readyQuery.data?.status}
        checks={readyQuery.data?.checks ?? []}
        livenessLoading={liveQuery.isPending}
        readinessLoading={readyQuery.isPending}
        livenessError={liveQuery.isError ? liveQuery.error.message : undefined}
        readinessError={readyQuery.isError ? readyQuery.error.message : undefined}
        onRetry={() => {
          liveQuery.refetch();
          readyQuery.refetch();
        }}
      />
    </main>
  );
}
