"""AI adapter and use-case ports (ADR-022 canonical adapter contract).

The canonical adapter contract from `docs/ai/ai-provider-abstraction.md`:
every adapter implements ``generate``, ``embed`` where supported, ``rerank``
where supported, ``transcribe`` where supported, ``health``, ``capabilities``,
``usage_normalization`` and ``error_translation``.
"""

from __future__ import annotations

import abc
from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any, Protocol, runtime_checkable

from crm_bds_ai.infra.ai.errors import AIError


class Capability(StrEnum):
    """Canonical capability codes from `contracts/ai/capability-registry.yaml`."""

    CHAT = "CHAT"
    REASONING = "REASONING"
    STRUCTURED_OUTPUT = "STRUCTURED_OUTPUT"
    STREAMING = "STREAMING"
    TOOL_CALLING = "TOOL_CALLING"
    EMBEDDING = "EMBEDDING"
    RERANKING = "RERANKING"
    VISION = "VISION"
    DOCUMENT_UNDERSTANDING = "DOCUMENT_UNDERSTANDING"
    OCR = "OCR"
    SPEECH_TO_TEXT = "SPEECH_TO_TEXT"
    TEXT_TO_SPEECH = "TEXT_TO_SPEECH"
    MODERATION = "MODERATION"
    BATCH = "BATCH"


class SupportedOperation(StrEnum):
    """Operations declared in `contracts/ai/adapter-manifest.schema.json`."""

    GENERATE = "GENERATE"
    EMBED = "EMBED"
    RERANK = "RERANK"
    TRANSCRIBE = "TRANSCRIBE"
    SYNTHESIZE = "SYNTHESIZE"
    HEALTH = "HEALTH"


@dataclass(slots=True)
class UsageInfo:
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0
    extra: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class GenerationRequest:
    prompt: str
    use_case_code: str = ""
    system_prompt: str | None = None
    max_tokens: int | None = None
    temperature: float | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class GenerationResult:
    text: str
    output: dict[str, Any] = field(default_factory=dict)
    usage: UsageInfo = field(default_factory=UsageInfo)
    model_code: str = "unknown"
    provider_code: str = "unknown"
    latency_ms: float = 0.0


@dataclass(slots=True)
class EmbeddingRequest:
    text: str
    use_case_code: str = ""


@dataclass(slots=True)
class EmbeddingResult:
    vector: list[float]
    dimension: int
    model_code: str = "unknown"
    provider_code: str = "unknown"


@runtime_checkable
class AIProviderAdapter(Protocol):
    """Canonical AI provider adapter contract."""

    def adapter_manifest(self) -> dict[str, Any]: ...
    def capabilities(self) -> list[Capability]: ...
    def health(self) -> bool: ...
    def generate(self, request: GenerationRequest) -> GenerationResult: ...
    def embed(self, request: EmbeddingRequest) -> EmbeddingResult: ...
    def usage_normalization(self, usage: dict[str, Any]) -> UsageInfo: ...
    def error_translation(self, error: Exception) -> AIError: ...


class AIUseCasePort(abc.ABC):
    """Port implemented by every AI use case.

    Use cases are business-side objects; Sprint 1 only defines the contract and a
    technical conformance example. No business use case is implemented yet.
    """

    code: str
    owner_context: str
    required_capabilities: list[Capability]
    output_schema_ref: str
    approval_mode: str

    @abc.abstractmethod
    def execute(self, context: dict[str, Any]) -> dict[str, Any]:
        """Execute the use case and return an AI suggestion payload."""
