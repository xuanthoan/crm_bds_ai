import { render, screen } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";
import HealthStatus from "@/components/health-status";

describe("HealthStatus", () => {
  it("renders healthy state with all checks", () => {
    render(
      <HealthStatus
        liveness="ok"
        readiness="degraded"
        checks={[
          { name: "database", ok: true, message: "ok" },
          { name: "broker", ok: false, message: "unreachable" },
        ]}
        livenessLoading={false}
        readinessLoading={false}
        onRetry={() => {}}
      />,
    );

    expect(screen.getByText("Liveness")).toBeInTheDocument();
    expect(screen.getByText("ok")).toBeInTheDocument();
    expect(screen.getByText("degraded")).toBeInTheDocument();
    expect(screen.getByText("✓ database")).toBeInTheDocument();
    expect(screen.getByText("✗ broker")).toBeInTheDocument();
    expect(screen.getByText("unreachable")).toBeInTheDocument();
  });

  it("shows loading placeholders while pending", () => {
    render(
      <HealthStatus
        liveness={undefined}
        readiness={undefined}
        checks={[]}
        livenessLoading={true}
        readinessLoading={true}
        onRetry={() => {}}
      />,
    );
    expect(screen.getAllByText("checking…").length).toBe(2);
  });

  it("shows errors and a retry button on failure", () => {
    const retry = vi.fn();
    render(
      <HealthStatus
        liveness="ok"
        readiness={undefined}
        checks={[]}
        livenessLoading={false}
        readinessLoading={false}
        readinessError="Request failed with status 503"
        onRetry={retry}
      />,
    );
    expect(screen.getByText(/error: Request failed/)).toBeInTheDocument();
    screen.getByRole("button", { name: "Retry" }).click();
    expect(retry).toHaveBeenCalledOnce();
  });
});
