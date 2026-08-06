"""Helpers for the ephemeral test database (never touches developer data)."""

from __future__ import annotations

import os
from urllib.parse import urlparse

import sqlalchemy as sa
from sqlalchemy import text

TEST_DATABASE_URL = os.environ.get(
    "TEST_DATABASE_URL",
    "postgresql+psycopg://crm_bds_ai:local_dev_password_only@localhost:5432/crm_bds_ai_test",
)

ADMIN_DATABASE_URL = os.environ.get(
    "ADMIN_DATABASE_URL",
    "postgresql+psycopg://crm_bds_ai:local_dev_password_only@localhost:5432/crm_bds_ai",
)


def _admin_engine() -> sa.Engine:
    parsed = urlparse(TEST_DATABASE_URL)
    admin_url = (
        f"{parsed.scheme}://{parsed.username}:{parsed.password}@"
        f"{parsed.hostname}:{parsed.port}/crm_bds_ai"
    )
    return sa.create_engine(
        admin_url, isolation_level="AUTOCOMMIT", connect_args={"connect_timeout": 3}
    )


def ensure_test_database() -> None:
    """Create the ephemeral test database when it does not exist."""
    parsed = urlparse(TEST_DATABASE_URL)
    engine = _admin_engine()
    with engine.connect() as conn:
        exists = conn.execute(
            text("SELECT 1 FROM pg_database WHERE datname = :name"),
            {"name": parsed.path.lstrip("/")},
        ).scalar_one_or_none()
        if exists is None:
            conn.execute(text(f'CREATE DATABASE "{parsed.path.lstrip("/")}"'))
    engine.dispose()


def reset_test_database() -> None:
    """Drop and recreate the ephemeral test database (disposable test resource).

    The developer database `crm_bds_ai` is never touched.
    """
    parsed = urlparse(TEST_DATABASE_URL)
    db_name = parsed.path.lstrip("/")
    engine = _admin_engine()
    with engine.connect() as conn:
        conn.execute(text(f'DROP DATABASE IF EXISTS "{db_name}" WITH (FORCE)'))
        conn.execute(text(f'CREATE DATABASE "{db_name}"'))
    engine.dispose()
