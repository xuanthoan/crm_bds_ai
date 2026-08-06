"""Celery application shell.

Broker is resolved from typed settings (`BROKER_URL`). No result backend is
configured yet; queue names, routing keys, retry counts and timeouts are
environment configuration and belong to Sprint 2 reliability contracts — Sprint 1
must not invent them.
"""

from __future__ import annotations

from celery import Celery

from crm_bds_ai.bootstrap.settings import get_settings

_settings = get_settings()

celery_app = Celery(
    "crm_bds_ai",
    broker=_settings.broker_url,
    include=["crm_bds_ai.infra.worker.tasks"],
)

celery_app.conf.update(
    timezone="UTC",
    enable_utc=True,
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    task_track_started=True,
    task_acks_late=False,
    broker_connection_retry_on_startup=True,
    # Explicitly empty: no business schedules are defined in Sprint 1.
    beat_schedule={},
)
