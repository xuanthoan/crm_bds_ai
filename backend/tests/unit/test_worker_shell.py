"""Worker shell tests: technical smoke task executes without a broker.

The smoke task contains no business behavior; this test proves the worker shell
can execute a unit of work deterministically.
"""

from __future__ import annotations

from crm_bds_ai.infra.worker.celery_app import celery_app
from crm_bds_ai.infra.worker.tasks import diagnostics_smoke


class TestWorkerShell:
    def test_celery_app_configured_without_business_schedule(self) -> None:
        assert celery_app.main == "crm_bds_ai"
        assert celery_app.conf.beat_schedule == {}
        assert "diagnostics.smoke" in celery_app.tasks

    def test_smoke_task_runs_locally_and_returns_payload(self) -> None:
        result = diagnostics_smoke.run("ping")
        assert result["task"] == "diagnostics.smoke"
        assert result["echo"] == "pong:ping"
        assert result["request_id"]
        assert result["python"]

    def test_smoke_task_has_technical_only_namespace(self) -> None:
        assert diagnostics_smoke.name == "diagnostics.smoke"
        assert not diagnostics_smoke.name.startswith(
            ("lead", "party", "product", "contract", "revenue")
        )
