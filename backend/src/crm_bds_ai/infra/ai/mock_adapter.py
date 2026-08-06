"""Mock AI provider adapter (Sprint 1 only — NO real provider integration).

Implements the canonical adapter contract from ADR-022 / `docs/ai/ai-provider-abstraction.md`
with fully deterministic behavior so tests and local development are reproducible.
No provider/model/base URL/API key is hard-coded anywhere.
"""

from __future__ import annotations

import hashlib
import json
import time
from typing import Any

from crm_bds_ai.infra.ai import errors as ai_errors
from crm_bds_ai.infra.ai.ports import (
    Capability,
    EmbeddingRequest,
    EmbeddingResult,
    GenerationRequest,
    GenerationResult,
    SupportedOperation,
    UsageInfo,
)

MOCK_EMBEDDING_DIMENSION = 384


def _stable_vector(text: str, dimension: int) -> list[float]:
    """Deterministic pseudo-vector derived from the input text."""
    digest = hashlib.sha256(text.encode("utf-8")).digest()
    return [((digest[i % len(digest)] / 255.0) - 0.5) * 2 for i in range(dimension)]


class MockAIProviderAdapter:
    """Deterministic in-process adapter used by the `local`/`test`/`ci` profiles."""

    ADAPTER_TYPE = "local_mock"
    VERSION = "1.0.0"

    def adapter_manifest(self) -> dict[str, Any]:
        return {
            "adapter_type": self.ADAPTER_TYPE,
            "implementation": "crm_bds_ai.infra.ai.mock_adapter.MockAIProviderAdapter",
            "version": self.VERSION,
            "supported_operations": [
                SupportedOperation.GENERATE.value,
                SupportedOperation.EMBED.value,
                SupportedOperation.HEALTH.value,
            ],
            "conformance_profile": "provider-conformance/conformance-cases.yaml",
        }

    def capabilities(self) -> list[Capability]:
        return [Capability.CHAT, Capability.STRUCTURED_OUTPUT, Capability.EMBEDDING]

    def health(self) -> bool:
        return True

    def generate(self, request: GenerationRequest) -> GenerationResult:
        self._validate_generation_request(request)
        started = time.monotonic()
        output = self._build_output(request)
        text = json.dumps(output, ensure_ascii=False, sort_keys=True)
        usage = UsageInfo(
            prompt_tokens=max(1, len(request.prompt) // 4),
            completion_tokens=len(text) // 4,
            total_tokens=max(1, len(request.prompt) // 4 + len(text) // 4),
        )
        return GenerationResult(
            text=text,
            output=output,
            usage=usage,
            model_code="mock-model-1",
            provider_code="mock",
            latency_ms=round((time.monotonic() - started) * 1000, 3),
        )

    def embed(self, request: EmbeddingRequest) -> EmbeddingResult:
        vector = _stable_vector(request.text, MOCK_EMBEDDING_DIMENSION)
        return EmbeddingResult(
            vector=vector,
            dimension=MOCK_EMBEDDING_DIMENSION,
            model_code="mock-model-1",
            provider_code="mock",
        )

    def rerank(self, *args: Any, **kwargs: Any) -> Any:
        raise ai_errors.AIValidationError(
            "rerank is not supported by the mock adapter",
            detail="operation not in supported_operations",
        )

    def transcribe(self, *args: Any, **kwargs: Any) -> Any:
        raise ai_errors.AIValidationError(
            "transcribe is not supported by the mock adapter",
            detail="operation not in supported_operations",
        )

    def usage_normalization(self, usage: dict[str, Any]) -> UsageInfo:
        return UsageInfo(
            prompt_tokens=int(usage.get("prompt_tokens", 0) or 0),
            completion_tokens=int(usage.get("completion_tokens", 0) or 0),
            total_tokens=int(usage.get("total_tokens", 0) or 0),
            extra={
                k: v
                for k, v in usage.items()
                if k not in ("prompt_tokens", "completion_tokens", "total_tokens")
            },
        )

    def error_translation(self, error: Exception) -> ai_errors.AIError:
        """Translate provider-specific failures into canonical AI errors."""
        if isinstance(error, ai_errors.AIError):
            return error
        if isinstance(error, TimeoutError):
            return ai_errors.AIProviderTimeoutError(str(error))
        if isinstance(error, (ConnectionError, OSError)):
            return ai_errors.AIProviderUnavailableError(str(error))
        return ai_errors.AIProviderUnavailableError(f"provider error: {type(error).__name__}")

    def _build_output(self, request: GenerationRequest) -> dict[str, Any]:
        """Deterministic canned structured output (technical, not business truth).

        For use cases with a canonical output schema, the mock produces payloads
        that satisfy the registered schema (validated by conformance tests).
        """
        use_case = request.use_case_code or "UNSPECIFIED"
        if use_case == "CUSTOMER_TIMELINE_SUMMARY":
            return {
                "summary": f"Mock summary for: {request.prompt[:120]}",
                "known_requirements": {"source": "mock"},
                "missing_information": ["preferred_contact_time"],
                "recommended_actions": [{"code": "FOLLOW_UP", "reason": "mock generated action"}],
                "evidence": [{"source_type": "mock", "source_id": "none"}],
                "confidence": 0.5,
            }
        return {
            "kind": "mock_generation",
            "use_case_code": use_case,
            "echo": request.prompt[:200],
            "generated_by": "mock",
        }

    def _validate_generation_request(self, request: GenerationRequest) -> None:
        if not request.prompt or not request.prompt.strip():
            raise ai_errors.AIValidationError("prompt must not be empty")
        if len(request.prompt) > 1_000_000:
            raise ai_errors.AIValidationError("prompt exceeds maximum length")
