"""Database engine factory and connectivity probe.

Only this module (and Alembic's env.py) builds SQLAlchemy engines. Consumers must
not construct engines themselves; this is enforced by architecture tests.
"""

from __future__ import annotations

from sqlalchemy import Engine, create_engine, text

from crm_bds_ai.bootstrap.settings import Settings


def create_db_engine(settings: Settings) -> Engine:
    """Create the application SQLAlchemy engine from typed settings."""
    url = settings.database_url
    if not url:
        raise ValueError("database_url is required to create the engine")
    connect_args: dict[str, object] = {}
    if url.startswith("postgresql"):
        connect_args = {"connect_timeout": 3}
    return create_engine(
        url,
        pool_pre_ping=True,
        pool_size=5,
        max_overflow=5,
        connect_args=connect_args,
    )


def check_database_connection(engine: Engine | None) -> bool:
    """Probe database connectivity with a short timeout.

    Returns False (never raises) when the database is unreachable, so readiness
    probes degrade gracefully instead of leaking connection errors.
    """
    if engine is None:
        return False
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return True
    except Exception:  # noqa: BLE001 - probe boundary must not raise
        return False
