"""AI feature flags (ADR-024: AI must be kill-switchable and failure-isolated).

The default for every profile except an explicitly approved sandbox is *disabled*.
No provider call may happen while the flag is off (`AIFeatureDisabledError`).
"""

from __future__ import annotations

from dataclasses import dataclass

from crm_bds_ai.bootstrap.settings import Settings
from crm_bds_ai.infra.ai.errors import AIFeatureDisabledError


@dataclass(frozen=True, slots=True)
class AIFeatureFlags:
    enabled: bool
    adapter: str
    default_use_case: str

    @classmethod
    def from_settings(cls, settings: Settings) -> AIFeatureFlags:
        return cls(
            enabled=settings.ai_enabled,
            adapter=settings.ai_adapter,
            default_use_case=settings.ai_default_use_case,
        )

    def require_enabled(self, use_case_code: str | None = None) -> None:
        """Fail fast when AI is disabled (provider calls must never bypass this)."""
        if not self.enabled:
            subject = f" for use case {use_case_code}" if use_case_code else ""
            raise AIFeatureDisabledError(f"AI is disabled by feature flag{subject}")
