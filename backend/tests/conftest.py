"""Shared test fixtures for the backend test suite."""

from __future__ import annotations

import os
from collections.abc import Iterator

import pytest
from fastapi.testclient import TestClient

from crm_bds_ai.bootstrap.app import create_app
from crm_bds_ai.bootstrap.settings import Settings

# Tests never touch the developer database. When a dedicated test database URL is
# not provided, integration tests are skipped instead of failing silently.
TEST_DATABASE_URL = os.environ.get(
    "TEST_DATABASE_URL",
    "postgresql+psycopg://crm_bds_ai:local_dev_password_only@localhost:5432/crm_bds_ai_test",
)


@pytest.fixture()
def settings() -> Settings:
    return Settings(
        profile="test",
        database_url=TEST_DATABASE_URL,
        broker_url="amqp://guest:guest@localhost:5672//",
        cache_url="redis://localhost:6379/0",
        storage_endpoint="http://localhost:9000",
        ai_enabled=True,
        ai_adapter="mock",
    )


@pytest.fixture()
def client(settings: Settings) -> Iterator[TestClient]:
    """TestClient with an isolated app instance (lifespan executes per client)."""
    app = create_app(settings=settings)
    with TestClient(app) as test_client:
        yield test_client
