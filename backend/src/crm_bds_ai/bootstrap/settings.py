"""Typed application configuration.

Configuration is loaded from environment variables (optionally a `.env` file in
the working directory). Local-only safe defaults exist ONLY for the `local`
profile. Production-like profiles fail fast when required values are missing.
"""

from __future__ import annotations

from enum import StrEnum
from functools import lru_cache

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Profile(StrEnum):
    LOCAL = "local"
    TEST = "test"
    CI = "ci"
    PRODUCTION = "production"


class Settings(BaseSettings):
    """Typed settings bound from the environment.

    `extra="ignore"` keeps unknown env vars harmless while every field stays typed.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

    profile: Profile = Profile.LOCAL
    app_name: str = "crm-bds-ai"
    app_version: str = "0.1.0"
    debug: bool = False
    log_level: str = Field(default="INFO", pattern="^(DEBUG|INFO|WARNING|ERROR|CRITICAL)$")

    # -- HTTP ---
    api_prefix: str = "/api/v1"
    # -- Infrastructure (env-specific; local defaults are DEV-ONLY safe credentials) --
    database_url: str | None = Field(
        default="postgresql+psycopg://crm_bds_ai:local_dev_password_only@localhost:5432/crm_bds_ai"
    )
    broker_url: str | None = Field(default="amqp://guest:guest@localhost:5672//")
    cache_url: str | None = Field(default="redis://localhost:6379/0")
    storage_endpoint: str | None = Field(default="http://localhost:9000")
    storage_access_key: str | None = Field(default="crm_bds_ai_local")
    storage_secret_key: str | None = Field(default="local_dev_password_only")

    # -- AI foundation (provider-agnostic; Mock Adapter only in Sprint 1) --
    ai_enabled: bool = False
    ai_adapter: str = Field(default="mock", pattern="^[a-z][a-z0-9_-]*$")
    ai_default_use_case: str = "CUSTOMER_TIMELINE_SUMMARY"

    # -- Paths (resolved relative to the repository root when unset) --
    contracts_dir: str | None = None

    @field_validator("database_url", "broker_url", "cache_url", "storage_endpoint", mode="before")
    @classmethod
    def _blank_means_missing(cls, value: object) -> object:
        if isinstance(value, str) and value.strip() == "":
            raise ValueError("value must not be empty")
        return value

    def validate_for_profile(self) -> None:
        """Fail fast on invalid configuration for the active profile.

        The `local` profile provides safe, explicit local-only defaults. Every other
        profile requires explicit values: production-like credentials must never be
        inferred from local defaults.
        """
        if self.profile is Profile.LOCAL:
            return
        missing: list[str] = []
        if not self.database_url:
            missing.append("DATABASE_URL")
        if not self.broker_url:
            missing.append("BROKER_URL")
        if not self.cache_url:
            missing.append("CACHE_URL")
        if not self.storage_endpoint:
            missing.append("STORAGE_ENDPOINT")
        if missing:
            raise ValueError(
                f"Profile '{self.profile.value}' requires explicit configuration; "
                f"missing: {', '.join(sorted(missing))}"
            )
        if self.profile is Profile.PRODUCTION and self.debug:
            raise ValueError("debug mode is not allowed for the production profile")


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Return the cached application settings (single read per process)."""
    return Settings()
