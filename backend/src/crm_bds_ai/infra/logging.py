"""Structured logging foundation (structlog).

Logs are structured JSON in non-local profiles and human-readable in the local
profile. Request/correlation ids are merged from the shared kernel context vars.
Health-check access is logged at DEBUG to avoid excessive noise
(`docs/implementation/health-readiness-contract.md` IMPL-HEALTH-001).
"""

from __future__ import annotations

import logging
import sys
from typing import Any

import structlog

from crm_bds_ai.bootstrap.settings import Profile, Settings
from crm_bds_ai.shared_kernel import correlation


def _add_correlation_ids(
    _logger: Any, _method_name: str, event_dict: dict[str, Any]
) -> dict[str, Any]:
    """Attach request/correlation ids from the current async context."""
    request_id = correlation.get_request_id()
    if request_id is not None:
        event_dict["request_id"] = request_id
    correlation_id = correlation.get_correlation_id()
    if correlation_id is not None:
        event_dict["correlation_id"] = correlation_id
    return event_dict


def _reject_noise(_logger: Any, _method_name: str, event_dict: dict[str, Any]) -> dict[str, Any]:
    """Drop debug-level health access logs (noise reduction)."""
    event_dict.pop("health_noise", None)
    return event_dict


def configure_logging(settings: Settings) -> None:
    """Configure standard logging and structlog for the process."""
    level = getattr(logging, settings.log_level.upper(), logging.INFO)
    logging.basicConfig(level=level, format="%(message)s", stream=sys.stdout)

    shared_processors: list[Any] = [
        structlog.contextvars.merge_contextvars,
        _add_correlation_ids,
        structlog.processors.add_log_level,
        structlog.processors.TimeStamper(fmt="iso", utc=True),
        _reject_noise,
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
    ]

    if settings.profile is Profile.LOCAL:
        renderer: Any = structlog.dev.ConsoleRenderer()
    else:
        renderer = structlog.processors.JSONRenderer(ensure_ascii=False, sort_keys=True)

    structlog.configure(
        processors=[*shared_processors, renderer],
        wrapper_class=structlog.make_filtering_bound_logger(level),
        logger_factory=structlog.PrintLoggerFactory(),
        cache_logger_on_first_use=True,
    )
    # Keep uvicorn/access logs structured too.
    logging.getLogger("uvicorn").handlers = []
