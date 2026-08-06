"""Dependency probes for readiness (infrastructure-owned diagnostics).

Ownership rule: only this module touches SQLAlchemy, kombu, sockets or the
storage HTTP probe. The HTTP/presentation layer orchestrates these probes but
never imports framework drivers directly (enforced by architecture tests).
"""

from __future__ import annotations

import socket
from dataclasses import dataclass, field
from typing import Any
from urllib.parse import urlparse

import httpx
from kombu import Connection

from crm_bds_ai.bootstrap.settings import Settings
from crm_bds_ai.infra.db import check_database_connection

__all__ = [
    "HealthCheckResult",
    "ReadinessReport",
    "build_readiness_report",
    "check_broker_connectivity",
    "check_cache_connectivity",
    "check_storage_connectivity",
    "check_config_validity",
]


@dataclass(slots=True)
class HealthCheckResult:
    name: str
    ok: bool
    message: str = "ok"


@dataclass(slots=True)
class ReadinessReport:
    status: str  # healthy | degraded | unhealthy
    checks: list[HealthCheckResult] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "status": self.status,
            "checks": [{"name": c.name, "ok": c.ok, "message": c.message} for c in self.checks],
        }


def check_config_validity(settings: Settings) -> HealthCheckResult:
    try:
        settings.validate_for_profile()
        return HealthCheckResult("config", True)
    except ValueError as exc:
        return HealthCheckResult("config", False, str(exc))


def check_database_connectivity(engine: Any | None) -> HealthCheckResult:
    ok = check_database_connection(engine)
    return HealthCheckResult("database", ok, "ok" if ok else "unreachable")


def check_broker_connectivity(settings: Settings) -> HealthCheckResult:
    if not settings.broker_url:
        return HealthCheckResult("broker", False, "not configured")
    try:
        conn = Connection(
            settings.broker_url,
            connect_timeout=2,
            transport_options={"max_retries": 0},
        )
        conn.ensure_connection(max_retries=0, timeout=2)
        conn.release()
        return HealthCheckResult("broker", True)
    except Exception as exc:  # noqa: BLE001 - probe boundary
        return HealthCheckResult("broker", False, f"unreachable ({type(exc).__name__})")


def _tcp_probe(host: str, port: int, timeout: float) -> bool:
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except OSError:
        return False


def _url_host_port(url: str) -> tuple[str, int]:
    parsed = urlparse(url)
    host = parsed.hostname or "localhost"
    port = parsed.port or 6379
    return host, port


def check_cache_connectivity(settings: Settings) -> HealthCheckResult:
    if not settings.cache_url:
        return HealthCheckResult("cache", False, "not configured")
    host, port = _url_host_port(settings.cache_url)
    ok = _tcp_probe(host, port, timeout=2.0)
    return HealthCheckResult("cache", ok, "ok" if ok else "unreachable")


def check_storage_connectivity(settings: Settings) -> HealthCheckResult:
    if not settings.storage_endpoint:
        return HealthCheckResult("storage", False, "not configured")
    base = settings.storage_endpoint.rstrip("/")
    try:
        resp = httpx.get(f"{base}/minio/health/live", timeout=2.0)
        ok = resp.status_code == 200
        return HealthCheckResult("storage", ok, "ok" if ok else f"http {resp.status_code}")
    except Exception as exc:  # noqa: BLE001 - probe boundary
        return HealthCheckResult("storage", False, f"unreachable ({type(exc).__name__})")


def build_readiness_report(settings: Settings, engine: Any | None) -> ReadinessReport:
    """Run all readiness checks and aggregate healthy/degraded/unhealthy.

    `config` and `database` are critical; broker/cache/storage are degrading-only.
    """
    checks = [
        check_config_validity(settings),
        check_database_connectivity(engine),
        check_broker_connectivity(settings),
        check_cache_connectivity(settings),
        check_storage_connectivity(settings),
    ]
    critical = [c for c in checks if c.name in ("config", "database")]
    optional = [c for c in checks if c.name not in ("config", "database")]
    if not all(c.ok for c in critical):
        return ReadinessReport(status="unhealthy", checks=checks)
    if not all(c.ok for c in optional):
        return ReadinessReport(status="degraded", checks=checks)
    return ReadinessReport(status="healthy", checks=checks)
