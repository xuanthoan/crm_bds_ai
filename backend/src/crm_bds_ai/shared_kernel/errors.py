"""Canonical application error boundary (RFC 9457 Problem Details).

Error responses MUST follow the Problem Details shape required by
`docs/engineering/api-standards.md` (ENG-API-001) and the canonical error code
format `<CONTEXT>_<CATEGORY>_<SPECIFIC_REASON>` from
`docs/engineering/error-code-registry.md` (ENG-ERR-001).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class ProblemDetailsError(Exception):
    """Raised by application code to produce a stable Problem Details response."""

    error_code: str
    title: str
    status: int
    detail: str = ""
    type_uri: str = "about:blank"
    instance: str | None = None
    field_errors: list[dict[str, str]] = field(default_factory=list)
    extra: dict[str, Any] = field(default_factory=dict)

    def to_problem_details(self, correlation_id: str | None = None) -> dict[str, Any]:
        """Render the RFC 9457-compatible body.

        Required fields per API standards: type, title, status, detail, instance,
        error_code, correlation_id.
        """
        body: dict[str, Any] = {
            "type": self.type_uri,
            "title": self.title,
            "status": self.status,
            "detail": self.detail,
            "instance": self.instance,
            "error_code": self.error_code,
        }
        if correlation_id is not None:
            body["correlation_id"] = correlation_id
        if self.field_errors:
            body["field_errors"] = self.field_errors
        for key, value in self.extra.items():
            if key not in body:
                body[key] = value
        return body
