"""Liveness / readiness HTTP endpoints.

Contract: `docs/implementation/health-readiness-contract.md` (IMPL-HEALTH-001).

- `/health/live` proves the process loop is alive; it never touches dependencies.
- `/health/ready` delegates to the infrastructure-owned probes
  (`crm_bds_ai.infra.readiness`) — this presentation module imports no framework
  drivers directly (architecture-enforced).

Responses never expose credentials, DSNs, queue payloads or stack traces.
"""

from __future__ import annotations

from typing import Any

import structlog
from fastapi import APIRouter, Request, Response, status
from starlette.concurrency import run_in_threadpool

from crm_bds_ai.bootstrap.settings import Settings
from crm_bds_ai.infra.readiness import build_readiness_report

logger = structlog.get_logger(__name__)

router = APIRouter(prefix="/health", tags=["health"])


def install_health_routes(app: Any, default_settings: Settings | None = None) -> None:
    """Register health endpoints.

    Dependencies are read from ``app.state.container`` (created by the lifespan)
    so tests can substitute the container freely.
    """

    @app.get("/health/live")
    async def liveness(request: Request) -> dict[str, str]:
        return {"status": "ok"}

    @app.get("/health/ready")
    async def readiness(request: Request) -> Response:
        from fastapi.responses import JSONResponse

        container = getattr(request.app.state, "container", None)
        cfg = getattr(container, "settings", None) or default_settings or Settings()
        engine = getattr(container, "engine", None)
        report = await run_in_threadpool(build_readiness_report, cfg, engine)
        http_status = (
            status.HTTP_200_OK
            if report.status in ("healthy", "degraded")
            else status.HTTP_503_SERVICE_UNAVAILABLE
        )
        return JSONResponse(status_code=http_status, content=report.to_dict())
