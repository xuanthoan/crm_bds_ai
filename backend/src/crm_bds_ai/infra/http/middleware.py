"""Request / correlation identifier middleware.

Implements the `X-Request-ID` / `X-Correlation-ID` contract from
`docs/engineering/api-standards.md` section 18: the server validates or generates
the ids, returns them to the client and propagates them into logs.
"""

from __future__ import annotations

import time
from collections.abc import Awaitable, Callable

import structlog
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from crm_bds_ai.shared_kernel import correlation

REQUEST_ID_HEADER = "X-Request-ID"
CORRELATION_ID_HEADER = "X-Correlation-ID"

logger = structlog.get_logger(__name__)

# Paths whose access logs are downgraded to debug (noise reduction).
QUIET_PREFIXES = ("/health/",)


class CorrelationIdMiddleware(BaseHTTPMiddleware):
    """Assign or accept request/correlation ids and log a request summary."""

    async def dispatch(
        self, request: Request, call_next: Callable[..., Awaitable[Response]]
    ) -> Response:  # type: ignore[override]
        request_id = request.headers.get(REQUEST_ID_HEADER) or correlation.new_id()
        correlation_id = request.headers.get(CORRELATION_ID_HEADER) or request_id
        correlation.set_correlation_ids(request_id=request_id, correlation_id=correlation_id)

        started = time.monotonic()
        response = await call_next(request)
        duration_ms = round((time.monotonic() - started) * 1000, 2)

        response.headers[REQUEST_ID_HEADER] = request_id
        response.headers[CORRELATION_ID_HEADER] = correlation_id

        quiet = request.url.path.startswith(QUIET_PREFIXES)
        log = logger.debug if quiet else logger.info
        log(
            "http_request",
            method=request.method,
            path=request.url.path,
            status_code=response.status_code,
            duration_ms=duration_ms,
            request_id=request_id,
            correlation_id=correlation_id,
            health_noise=quiet,
        )
        return response
