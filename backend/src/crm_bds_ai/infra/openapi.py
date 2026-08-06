"""Deterministic OpenAPI 3.1 generation extensions.

FastAPI only emits schemas referenced by declared endpoints. The Problem Details
error contract (ENG-API-001) must always be documented, so it is injected into
the generated document deterministically.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from fastapi import FastAPI

PROBLEM_DETAILS_SCHEMA: dict[str, Any] = {
    "type": "object",
    "required": ["type", "title", "status"],
    "properties": {
        "type": {"type": "string", "format": "uri-reference"},
        "title": {"type": "string"},
        "status": {"type": "integer", "minimum": 100, "maximum": 599},
        "detail": {"type": "string"},
        "instance": {"type": "string", "format": "uri-reference"},
        "error_code": {"type": "string"},
        "correlation_id": {"type": "string"},
        "field_errors": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "field": {"type": "string"},
                    "code": {"type": "string"},
                    "message": {"type": "string"},
                },
                "additionalProperties": False,
            },
        },
    },
    "additionalProperties": False,
}


def install_openapi_extensions(app: FastAPI) -> None:
    """Patch ``app.openapi`` to include the canonical Problem Details schema."""
    original_openapi: Callable[[], dict[str, Any]] = app.openapi

    def patched_openapi() -> dict[str, Any]:
        schema = original_openapi()
        components = schema.setdefault("components", {})
        schemas = components.setdefault("schemas", {})
        schemas.setdefault("ProblemDetails", PROBLEM_DETAILS_SCHEMA)
        return schema

    app.openapi = patched_openapi  # type: ignore[method-assign]
