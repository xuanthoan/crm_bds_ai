"""Correlation and request identifier propagation (context-var based).

Per `docs/engineering/api-standards.md` (ENG-API-001) the server MUST accept or
generate `X-Request-ID` and `X-Correlation-ID`, return them to the client and
propagate them into logs, events, jobs and provider calls.
"""

from __future__ import annotations

import contextvars
import uuid

_request_id_var: contextvars.ContextVar[str | None] = contextvars.ContextVar(
    "request_id", default=None
)
_correlation_id_var: contextvars.ContextVar[str | None] = contextvars.ContextVar(
    "correlation_id", default=None
)


def new_id() -> str:
    """Generate a new opaque identifier (UUID4 hex)."""
    return uuid.uuid4().hex


def get_request_id() -> str | None:
    """Return the request id bound to the current async context, if any."""
    return _request_id_var.get()


def get_correlation_id() -> str | None:
    """Return the correlation id bound to the current async context, if any."""
    return _correlation_id_var.get()


def set_request_id(value: str | None) -> None:
    """Bind the request id for the current async context."""
    _request_id_var.set(value)


def set_correlation_id(value: str | None) -> None:
    """Bind the correlation id for the current async context."""
    _correlation_id_var.set(value)


def set_correlation_ids(request_id: str | None, correlation_id: str | None) -> None:
    """Bind both identifiers for the current async context."""
    set_request_id(request_id)
    set_correlation_id(correlation_id)
