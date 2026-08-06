"""Dependency composition boundary (composition root).

Only this module is allowed to wire infrastructure objects together. Business
modules (when they exist) receive dependencies through constructor injection and
never construct infra objects directly.
"""

from __future__ import annotations

from dataclasses import dataclass

from sqlalchemy.engine import Engine

from crm_bds_ai.bootstrap.settings import Settings
from crm_bds_ai.infra.db import create_db_engine


@dataclass(slots=True)
class Container:
    """Holds the resolved application dependencies."""

    settings: Settings
    engine: Engine


def create_container(settings: Settings | None = None) -> Container:
    """Compose the application dependency graph.

    Validates the profile configuration first so invalid environments fail fast.
    """
    resolved = settings or Settings()
    resolved.validate_for_profile()
    engine = create_db_engine(resolved)
    return Container(settings=resolved, engine=engine)
