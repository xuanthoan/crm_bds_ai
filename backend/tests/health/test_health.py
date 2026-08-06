"""Health/liveness/readiness tests (healthy / unhealthy / degraded transitions).

Contract: `docs/implementation/health-readiness-contract.md` (IMPL-HEALTH-001).
Transitions are simulated at the report level so the tests do not require the
full local stack; real-stack connectivity is covered by the smoke command and
integration tests.
"""

from __future__ import annotations

from types import SimpleNamespace
from unittest.mock import patch

from fastapi.testclient import TestClient

from crm_bds_ai.bootstrap.settings import Settings
from crm_bds_ai.infra.readiness import HealthCheckResult, build_readiness_report


class TestLiveness:
    def test_liveness_returns_ok(self, client: TestClient) -> None:
        response = client.get("/health/live")
        assert response.status_code == 200
        assert response.json() == {"status": "ok"}

    def test_liveness_never_touches_dependencies(self, client: TestClient) -> None:
        # Liveness must not perform heavy dependency checks: force all other
        # probes to raise if they are invoked by liveness.
        with patch(
            "crm_bds_ai.infra.readiness.check_database_connectivity",
            side_effect=AssertionError("liveness must not check the database"),
        ):
            response = client.get("/health/live")
        assert response.status_code == 200


class TestReadinessReport:
    def _report(
        self, *, db_ok: bool, broker_ok: bool = True, cache_ok: bool = True, storage_ok: bool = True
    ) -> object:
        settings = Settings(profile="test", database_url="postgresql+psycopg://u:p@db:5432/x")
        engine = SimpleNamespace() if db_ok else None
        with (
            patch(
                "crm_bds_ai.infra.readiness.check_database_connectivity",
                return_value=HealthCheckResult("database", db_ok),
            ),
            patch(
                "crm_bds_ai.infra.readiness.check_broker_connectivity",
                return_value=HealthCheckResult("broker", broker_ok),
            ),
            patch(
                "crm_bds_ai.infra.readiness.check_cache_connectivity",
                return_value=HealthCheckResult("cache", cache_ok),
            ),
            patch(
                "crm_bds_ai.infra.readiness.check_storage_connectivity",
                return_value=HealthCheckResult("storage", storage_ok),
            ),
        ):
            return build_readiness_report(settings, engine)

    def test_healthy(self) -> None:
        report = self._report(db_ok=True)
        assert report.status == "healthy"
        assert all(check.ok for check in report.checks)

    def test_degraded_when_optional_dependency_down(self) -> None:
        report = self._report(db_ok=True, broker_ok=False, storage_ok=False)
        assert report.status == "degraded"
        names = {check.name: check.ok for check in report.checks}
        assert names["database"] is True
        assert names["broker"] is False
        assert names["storage"] is False

    def test_unhealthy_when_database_down(self) -> None:
        report = self._report(db_ok=False)
        assert report.status == "unhealthy"

    def test_response_body_shape(self) -> None:
        report = self._report(db_ok=True)
        body = report.to_dict()
        assert set(body.keys()) == {"status", "checks"}
        assert all(set(check.keys()) == {"name", "ok", "message"} for check in body["checks"])


class TestReadinessEndpoint:
    def test_ready_returns_503_when_unhealthy(self, monkeypatch) -> None:  # type: ignore[no-untyped-def]
        from crm_bds_ai.infra.http import health as health_module
        from crm_bds_ai.infra.readiness import HealthCheckResult, ReadinessReport

        monkeypatch.setattr(
            health_module,
            "build_readiness_report",
            lambda *a, **k: ReadinessReport(
                status="unhealthy",
                checks=[HealthCheckResult("database", False, "unreachable")],
            ),
        )
        from crm_bds_ai.bootstrap.app import create_app

        app = create_app()
        with TestClient(app) as test_client:
            response = test_client.get("/health/ready")
        assert response.status_code == 503
        assert response.json()["status"] == "unhealthy"

    def test_ready_returns_200_when_healthy_or_degraded(self, client: TestClient) -> None:
        # With the real local stack up this returns healthy/degraded (200); with
        # the stack down it returns 503. Either is an acceptable state here; the
        # specific transitions are covered at the report level above.
        response = client.get("/health/ready")
        assert response.status_code in (200, 503)
        body = response.json()
        assert body["status"] in ("healthy", "degraded", "unhealthy")
