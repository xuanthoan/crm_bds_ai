"""Canonical AI error types (provider-agnostic).

Adapters translate provider-specific failures into these canonical types through
``error_translation`` so callers never depend on provider exception classes
(`docs/ai/ai-provider-abstraction.md`, ADR-024 failure isolation).
"""

from __future__ import annotations


class AIError(Exception):
    """Base class for all canonical AI errors."""

    error_code = "AI_ERROR"

    def __init__(self, message: str, *, detail: str | None = None) -> None:
        super().__init__(message)
        self.message = message
        self.detail = detail


class AIFeatureDisabledError(AIError):
    """The AI capability is disabled by a feature flag."""

    error_code = "AI_FEATURE_DISABLED"


class AIProviderUnavailableError(AIError):
    """The provider/adapter could not be reached or is not ready."""

    error_code = "AI_PROVIDER_UNAVAILABLE"


class AIProviderTimeoutError(AIError):
    """A provider call exceeded its timeout budget."""

    error_code = "AI_PROVIDER_TIMEOUT"


class AIConfigurationError(AIError):
    """Provider/model registry or feature configuration is invalid."""

    error_code = "AI_CONFIGURATION_INVALID"


class AIValidationError(AIError):
    """Adapter input/output failed validation (including unsupported operations)."""

    error_code = "AI_VALIDATION_FAILED"
