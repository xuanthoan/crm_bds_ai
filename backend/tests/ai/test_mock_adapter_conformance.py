"""AI Mock adapter conformance tests.

Executes the conformance cases from
`contracts/ai/provider-conformance/conformance-cases.yaml` against the Mock
Adapter, validating it against `contracts/ai/adapter-manifest.schema.json`.
"""

from __future__ import annotations

import json
from pathlib import Path

import jsonschema
import pytest

from crm_bds_ai.infra.ai import errors as ai_errors
from crm_bds_ai.infra.ai.feature_flags import AIFeatureFlags
from crm_bds_ai.infra.ai.mock_adapter import MOCK_EMBEDDING_DIMENSION, MockAIProviderAdapter
from crm_bds_ai.infra.ai.ports import (
    EmbeddingRequest,
    GenerationRequest,
    SupportedOperation,
)
from crm_bds_ai.infra.ai.registries import (
    load_capability_registry,
    load_conformance_cases,
)

CONTRACTS_AI = Path(__file__).resolve().parents[3] / "contracts" / "ai"


@pytest.fixture()
def adapter() -> MockAIProviderAdapter:
    return MockAIProviderAdapter()


class TestConformanceHealthCheck:
    def test_health_returns_true(self, adapter: MockAIProviderAdapter) -> None:
        assert adapter.health() is True


class TestConformanceErrorNormalization:
    def test_timeout_error_translates_to_canonical(self, adapter: MockAIProviderAdapter) -> None:
        translated = adapter.error_translation(TimeoutError("slow provider"))
        assert isinstance(translated, ai_errors.AIProviderTimeoutError)
        assert translated.error_code == "AI_PROVIDER_TIMEOUT"

    def test_connection_error_translates_to_unavailable(
        self, adapter: MockAIProviderAdapter
    ) -> None:
        translated = adapter.error_translation(ConnectionError("refused"))
        assert isinstance(translated, ai_errors.AIProviderUnavailableError)

    def test_invalid_input_raises_canonical_error(self, adapter: MockAIProviderAdapter) -> None:
        with pytest.raises(ai_errors.AIValidationError):
            adapter.generate(GenerationRequest(prompt="  "))

    def test_unsupported_operation_raises_canonical_error(
        self, adapter: MockAIProviderAdapter
    ) -> None:
        with pytest.raises(ai_errors.AIValidationError):
            adapter.rerank(["a"], "query")
        with pytest.raises(ai_errors.AIValidationError):
            adapter.transcribe(b"audio")


class TestConformanceStructuredOutput:
    def test_generate_returns_parseable_structured_output(
        self, adapter: MockAIProviderAdapter
    ) -> None:
        result = adapter.generate(
            GenerationRequest(prompt="Summarize", use_case_code="CUSTOMER_TIMELINE_SUMMARY")
        )
        parsed = json.loads(result.text)
        assert parsed["summary"]  # schema-required field
        assert parsed["recommended_actions"][0]["code"] == "FOLLOW_UP"

    def test_output_matches_use_case_output_schema(self, adapter: MockAIProviderAdapter) -> None:
        schema = json.loads(
            (CONTRACTS_AI / "output-schemas" / "customer-summary.schema.json").read_text(
                encoding="utf-8"
            )
        )
        # The mock must produce output valid against the canonical use-case schema.
        result = adapter.generate(
            GenerationRequest(
                prompt="Customer 123 summary", use_case_code="CUSTOMER_TIMELINE_SUMMARY"
            )
        )
        jsonschema.validate(instance=result.output, schema=schema)


class TestConformanceEmbeddingDimensionStability:
    def test_embedding_is_deterministic_and_stable_dimension(
        self, adapter: MockAIProviderAdapter
    ) -> None:
        a = adapter.embed(EmbeddingRequest(text="crm_bds_ai"))
        b = adapter.embed(EmbeddingRequest(text="crm_bds_ai"))
        assert a.dimension == MOCK_EMBEDDING_DIMENSION
        assert a.vector == b.vector
        c = adapter.embed(EmbeddingRequest(text="different text"))
        assert a.vector != c.vector


class TestConformanceTimeoutAndCancellation:
    def test_generate_completes_within_bound(self, adapter: MockAIProviderAdapter) -> None:
        import time

        started = time.monotonic()
        adapter.generate(GenerationRequest(prompt="x" * 1000))
        assert time.monotonic() - started < 5.0


class TestAdapterManifest:
    def test_manifest_validates_against_schema(self, adapter: MockAIProviderAdapter) -> None:
        schema = json.loads(
            (CONTRACTS_AI / "adapter-manifest.schema.json").read_text(encoding="utf-8")
        )
        manifest = adapter.adapter_manifest()
        jsonschema.validate(instance=manifest, schema=schema)
        operations = set(manifest["supported_operations"])
        assert operations <= {op.value for op in SupportedOperation}

    def test_adapter_is_provider_agnostic(self, adapter: MockAIProviderAdapter) -> None:
        text_manifest = json.dumps(adapter.adapter_manifest(), sort_keys=True).lower()
        for forbidden in (
            "openai",
            "anthropic",
            "gemini",
            "deepseek",
            "ollama",
            "api key",
            "base_url",
        ):
            assert forbidden not in text_manifest


class TestConformanceAgainstRegistry:
    def test_capabilities_are_registered(self, adapter: MockAIProviderAdapter) -> None:
        registry = load_capability_registry(CONTRACTS_AI)
        for capability in adapter.capabilities():
            assert registry.contains(capability), f"unregistered capability: {capability}"

    def test_conformance_cases_cover_claimed_capabilities(
        self, adapter: MockAIProviderAdapter
    ) -> None:
        cases = load_conformance_cases(CONTRACTS_AI)
        codes = {case.code for case in cases}
        required = {case.code for case in cases if case.required}
        assert {"HEALTH_CHECK", "ERROR_NORMALIZATION", "TIMEOUT_AND_CANCELLATION"} <= required
        # Mock claims STRUCTURED_OUTPUT and EMBEDDING → their when-claimed cases must exist.
        when_claimed = {case.required_when_capability_claimed for case in cases}
        assert "STRUCTURED_OUTPUT" in when_claimed
        assert "EMBEDDING" in when_claimed
        assert codes == {
            "HEALTH_CHECK",
            "ERROR_NORMALIZATION",
            "STRUCTURED_OUTPUT_VALIDATION",
            "TOOL_CALL_SCHEMA_CONFORMANCE",
            "EMBEDDING_DIMENSION_STABILITY",
            "TIMEOUT_AND_CANCELLATION",
        }


class TestFeatureFlag:
    def test_disabled_flag_blocks_use_cases(self) -> None:
        flags = AIFeatureFlags(
            enabled=False, adapter="mock", default_use_case="CUSTOMER_TIMELINE_SUMMARY"
        )
        with pytest.raises(ai_errors.AIFeatureDisabledError):
            flags.require_enabled("CUSTOMER_TIMELINE_SUMMARY")

    def test_enabled_flag_allows_use_cases(self) -> None:
        flags = AIFeatureFlags(
            enabled=True, adapter="mock", default_use_case="CUSTOMER_TIMELINE_SUMMARY"
        )
        flags.require_enabled("CUSTOMER_TIMELINE_SUMMARY")  # no raise

    def test_default_settings_have_ai_disabled(self) -> None:
        from crm_bds_ai.bootstrap.settings import Settings

        flags = AIFeatureFlags.from_settings(Settings(profile="local"))
        assert flags.enabled is False
        assert flags.adapter == "mock"
