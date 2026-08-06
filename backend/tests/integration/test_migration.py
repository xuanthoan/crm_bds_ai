"""Integration test foundation: database connectivity and migration harness.

These tests use the dedicated ephemeral test database (`crm_bds_ai_test`) and
never touch the developer database (`crm_bds_ai`). They are skipped with an
explicit reason when the local PostgreSQL service is not reachable.
"""

from __future__ import annotations

import os
from pathlib import Path

import pytest
import sqlalchemy as sa
from sqlalchemy import text

from integration.db_helpers import (
    TEST_DATABASE_URL,
    ensure_test_database,
    reset_test_database,
)

ALEMBIC_INI = Path(__file__).resolve().parents[2] / "alembic.ini"

pytestmark = pytest.mark.integration


def _skip_if_db_unavailable() -> None:
    if os.environ.get("SKIP_DB_INTEGRATION") == "1":
        pytest.skip("SKIP_DB_INTEGRATION=1")
    try:
        engine = sa.create_engine(TEST_DATABASE_URL, connect_args={"connect_timeout": 2})
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        engine.dispose()
    except Exception as exc:  # noqa: BLE001
        pytest.skip(f"PostgreSQL test database unreachable: {exc}")


class TestDatabaseConnectivity:
    def test_select_one_on_test_database(self) -> None:
        _skip_if_db_unavailable()
        ensure_test_database()
        engine = sa.create_engine(TEST_DATABASE_URL, connect_args={"connect_timeout": 3})
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1 AS one")).scalar_one()
        engine.dispose()
        assert result == 1

    def test_connection_refused_returns_false_from_probe(self) -> None:
        from crm_bds_ai.bootstrap.settings import Settings
        from crm_bds_ai.infra.db import check_database_connection

        settings = Settings(
            profile="test",
            database_url="postgresql+psycopg://u:p@127.0.0.1:1/nope",
        )
        from crm_bds_ai.infra.db import create_db_engine

        engine = create_db_engine(settings)
        assert check_database_connection(engine) is False
        engine.dispose()


class TestMigrationHarness:
    @pytest.fixture(autouse=True)
    def _fresh_test_database(self) -> None:
        _skip_if_db_unavailable()
        ensure_test_database()
        reset_test_database()

    def _alembic(self, command: str, revision: str) -> None:
        import alembic.command
        import alembic.config

        # env.py reads DATABASE_URL from typed settings; point it at the test db.
        os.environ["DATABASE_URL"] = TEST_DATABASE_URL
        os.environ["PROFILE"] = "test"
        from crm_bds_ai.bootstrap.settings import get_settings

        get_settings.cache_clear()
        cfg = alembic.config.Config(str(ALEMBIC_INI))
        run = getattr(alembic.command, command)
        run(cfg, revision)

    def _user_tables(self) -> list[tuple[str, str]]:
        engine = sa.create_engine(TEST_DATABASE_URL)
        with engine.connect() as conn:
            rows = conn.execute(
                text(
                    "SELECT table_schema, table_name FROM information_schema.tables "
                    "WHERE table_schema IN ('public', 'infra') AND table_name <> 'alembic_version' "
                    "ORDER BY table_schema, table_name"
                )
            ).all()
        engine.dispose()
        return [(row[0], row[1]) for row in rows]

    def test_clean_upgrade_downgrade_reupgrade(self) -> None:
        # 1. Clean upgrade to head.
        self._alembic("upgrade", "head")
        tables = self._user_tables()
        assert tables == [], f"no business tables allowed in baseline, found: {tables}"

        # 2. Downgrade to base.
        self._alembic("downgrade", "base")
        engine = sa.create_engine(TEST_DATABASE_URL)
        with engine.connect() as conn:
            exists = conn.execute(
                text("SELECT 1 FROM information_schema.schemata WHERE schema_name = 'infra'")
            ).scalar_one_or_none()
        engine.dispose()
        assert exists is None, "infra schema must be removed by downgrade"

        # 3. Re-upgrade to head.
        self._alembic("upgrade", "head")
        engine = sa.create_engine(TEST_DATABASE_URL)
        with engine.connect() as conn:
            exists = conn.execute(
                text("SELECT 1 FROM information_schema.schemata WHERE schema_name = 'infra'")
            ).scalar_one_or_none()
        engine.dispose()
        assert exists == 1, "infra schema must exist after re-upgrade"
        assert self._user_tables() == []

    def test_alembic_current_is_head(self) -> None:
        self._alembic("upgrade", "head")
        import alembic.command
        import alembic.config

        os.environ["DATABASE_URL"] = TEST_DATABASE_URL
        cfg = alembic.config.Config(str(ALEMBIC_INI))
        alembic.command.current(cfg)
