"""Minimal technical smoke tasks.

These tasks contain NO business behavior. They exist only to prove that the
worker shell boots, connects to the broker and can execute a unit of work.
"""

from __future__ import annotations

import platform
import time
from typing import Any

from crm_bds_ai.infra.worker.celery_app import celery_app


@celery_app.task(name="diagnostics.smoke", bind=True)
def diagnostics_smoke(self: Any, message: str = "ping") -> dict[str, Any]:
    """Return a deterministic technical heartbeat payload."""
    return {
        "task": "diagnostics.smoke",
        # Direct (synchronous) execution has no broker request context; fall back.
        "request_id": self.request.id or "direct",
        "message": message,
        "echo": f"pong:{message}",
        "started_at": time.time(),
        "python": platform.python_version(),
    }
