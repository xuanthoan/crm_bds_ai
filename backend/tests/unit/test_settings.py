"""Unit tests: typed configuration and fail-fast validation."""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from crm_bds_ai.bootstrap.settings import Profile, Settings


class TestSettingsDefaults:
    def test_local_profile_has_safe_explicit_defaults(self) -> None:
        settings = Settings(profile="local")
        assert settings.profile is Profile.LOCAL
        assert settings.database_url.startswith("postgresql+psycopg://")
        assert settings.broker_url.startswith("amqp://")
        assert settings.cache_url.startswith("redis://")
        assert settings.storage_endpoint.startswith("http://")
        assert settings.ai_enabled is False
        assert settings.ai_adapter == "mock"
        # Local defaults validate without error.
        settings.validate_for_profile()

    def test_ai_mock_is_isolated_from_providers(self) -> None:
        # No provider/model/base URL may be hard-coded in settings.
        raw = Settings().model_dump()
        joined = " ".join(str(v) for v in raw.values()).lower()
        for forbidden in ("openai", "anthropic", "gemini", "deepseek", "ollama"):
            assert forbidden not in joined


class TestProfileValidation:
    def test_production_profile_fails_fast_on_missing_config(self) -> None:
        settings = Settings(profile="production", database_url=None, broker_url=None)
        with pytest.raises(ValueError) as excinfo:
            settings.validate_for_profile()
        message = str(excinfo.value)
        assert "DATABASE_URL" in message
        assert "BROKER_URL" in message

    def test_production_profile_rejects_debug(self) -> None:
        settings = Settings(
            profile="production",
            database_url="postgresql+psycopg://u:p@db:5432/x",
            broker_url="amqp://guest:guest@broker:5672//",
            cache_url="redis://cache:6379/0",
            storage_endpoint="http://storage:9000",
            debug=True,
        )
        with pytest.raises(ValueError) as excinfo:
            settings.validate_for_profile()
        assert "debug" in str(excinfo.value)

    def test_invalid_log_level_rejected(self) -> None:
        with pytest.raises(ValidationError):
            Settings(log_level="LOUD")

    def test_blank_required_value_rejected(self) -> None:
        with pytest.raises(ValidationError):
            Settings(database_url="")

    def test_ci_profile_requires_explicit_values(self) -> None:
        settings = Settings(profile="ci", database_url=None)
        with pytest.raises(ValueError):
            settings.validate_for_profile()
