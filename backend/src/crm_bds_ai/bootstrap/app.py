"""FastAPI application factory (composition root for the web shell)."""

from __future__ import annotations

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import Any

import structlog
from fastapi import FastAPI

from crm_bds_ai.bootstrap.container import create_container
from crm_bds_ai.bootstrap.settings import Settings, get_settings
from crm_bds_ai.infra.http.health import install_health_routes
from crm_bds_ai.infra.http.middleware import CorrelationIdMiddleware
from crm_bds_ai.infra.http.problem_details import install_error_handlers
from crm_bds_ai.infra.openapi import install_openapi_extensions

logger = structlog.get_logger(__name__)


def build_openapi_metadata(settings: Settings) -> dict[str, Any]:
    """Deterministic OpenAPI metadata for the application shell."""
    return {
        "title": settings.app_name,
        "version": settings.app_version,
        "description": (
            "CRM_BDS_AI backend shell (Sprint 1 Engineering Foundation). "
            "This contract intentionally contains no business endpoints."
        ),
    }


def create_app(settings: Settings | None = None) -> FastAPI:
    """Create the FastAPI application.

    A custom `container` is available on the app state for tests that need to
    substitute dependencies (e.g. an in-memory engine).
    """

    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncGenerator[None]:
        from crm_bds_ai.infra.logging import configure_logging

        cfg = settings or get_settings()
        configure_logging(cfg)
        container = create_container(cfg)
        app.state.container = container
        logger.info(
            "application_started",
            app=cfg.app_name,
            version=cfg.app_version,
            profile=cfg.profile.value,
        )
        yield
        try:
            container.engine.dispose()
        finally:
            logger.info("application_stopped", app=cfg.app_name)

    app = FastAPI(
        lifespan=lifespan,
        **build_openapi_metadata(settings or get_settings()),
    )

    # Middleware order: error boundary first is not possible in Starlette, but the
    # correlation middleware must wrap request handling to bind ids before logging.
    app.add_middleware(CorrelationIdMiddleware)

    install_error_handlers(app)
    install_health_routes(app, settings or get_settings())
    install_openapi_extensions(app)

    @app.get("/", tags=["meta"])
    async def root() -> dict[str, str]:
        return {
            "name": (settings or get_settings()).app_name,
            "version": (settings or get_settings()).app_version,
            "docs": "/docs",
            "openapi": "/openapi.json",
            "health": "/health/live",
        }

    return app
