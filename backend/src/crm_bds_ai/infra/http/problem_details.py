"""Standard error boundary: RFC 9457 Problem Details for every failure.

Errors MUST use the Problem Details shape required by API standards. Unhandled
exceptions are logged with full details server-side but the response never leaks
stack traces, SQL, internal hostnames, tokens or PII.
"""

from __future__ import annotations

import structlog
from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from crm_bds_ai.shared_kernel import correlation
from crm_bds_ai.shared_kernel.errors import ProblemDetailsError

logger = structlog.get_logger(__name__)

DEFAULT_ERROR_TYPE = "about:blank"


def _problem_response(
    status_code: int,
    title: str,
    detail: str,
    error_code: str,
    instance: str | None,
    request: Request,
    field_errors: list[dict[str, str]] | None = None,
    extra: dict[str, object] | None = None,
) -> JSONResponse:
    body: dict[str, object] = {
        "type": DEFAULT_ERROR_TYPE,
        "title": title,
        "status": status_code,
        "detail": detail,
        "instance": instance or request.url.path,
        "error_code": error_code,
        "correlation_id": correlation.get_correlation_id(),
    }
    if field_errors:
        body["field_errors"] = field_errors
    if extra:
        body.update(extra)
    return JSONResponse(status_code=status_code, content=body)


def install_error_handlers(app: FastAPI) -> None:
    """Register the canonical error handlers on the application."""

    @app.exception_handler(ProblemDetailsError)
    async def problem_details_handler(request: Request, exc: ProblemDetailsError) -> JSONResponse:
        return _problem_response(
            status_code=exc.status,
            title=exc.title,
            detail=exc.detail,
            error_code=exc.error_code,
            instance=exc.instance,
            request=request,
            field_errors=exc.field_errors,
            extra=exc.extra,
        )

    @app.exception_handler(RequestValidationError)
    async def validation_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
        field_errors: list[dict[str, str]] = []
        for error in exc.errors():
            field_errors.append(
                {
                    "field": ".".join(str(part) for part in error.get("loc", ())),
                    "code": error.get("type", "INVALID_VALUE"),
                    "message": error.get("msg", "Invalid value"),
                }
            )
        return _problem_response(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            title="Validation failed",
            detail="One or more fields failed validation.",
            error_code="COMMON_VALIDATION_FAILED",
            instance=None,
            request=request,
            field_errors=field_errors,
        )

    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request: Request, exc: StarletteHTTPException) -> JSONResponse:
        error_code = "COMMON_INTERNAL_ERROR"
        if exc.status_code == 404:
            error_code = "COMMON_NOT_FOUND"
        elif exc.status_code == 405:
            error_code = "COMMON_METHOD_NOT_ALLOWED"
        return _problem_response(
            status_code=exc.status_code,
            title=str(exc.detail),
            detail=str(exc.detail),
            error_code=error_code,
            instance=None,
            request=request,
        )

    @app.exception_handler(Exception)
    async def unhandled_handler(request: Request, exc: Exception) -> JSONResponse:
        # Full details stay in the logs; the response is intentionally generic.
        logger.exception(
            "unhandled_error",
            path=request.url.path,
            error_type=type(exc).__name__,
        )
        return _problem_response(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            title="Internal server error",
            detail="An unexpected error occurred.",
            error_code="COMMON_INTERNAL_ERROR",
            instance=None,
            request=request,
        )
