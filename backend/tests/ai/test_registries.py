"""AI registry loading and JSON Schema (draft 2020-12) validation tests."""

from __future__ import annotations

from pathlib import Path

import pytest

from crm_bds_ai.infra.ai import errors as ai_errors
from crm_bds_ai.infra.ai.ports import Capability
from crm_bds_ai.infra.ai.registries import (
    load_capability_registry,
    load_conformance_cases,
    load_use_case_registry,
    validate_json_schema_files,
    validate_use_cases_against_capabilities,
)

CONTRACTS_AI = Path(__file__).resolve().parents[3] / "contracts" / "ai"


class TestRegistries:
    def test_capability_registry_loads_and_covers_known_codes(self) -> None:
        registry = load_capability_registry(CONTRACTS_AI)
        assert registry.version
        for capability in Capability:
            assert registry.contains(capability), f"missing canonical capability {capability}"

    def test_use_case_registry_loads_and_requires_known_capabilities(self) -> None:
        use_cases = load_use_case_registry(CONTRACTS_AI)
        assert len(use_cases) >= 3
        codes = {uc.code for uc in use_cases}
        assert {
            "CUSTOMER_TIMELINE_SUMMARY",
            "CALL_TASK_EXTRACTION",
            "SEMANTIC_LISTING_SEARCH",
        } <= codes
        validate_use_cases_against_capabilities(use_cases, load_capability_registry(CONTRACTS_AI))

    def test_all_json_schemas_are_draft_2020_12_and_valid(self) -> None:
        validated = validate_json_schema_files(CONTRACTS_AI)
        names = {Path(path).name for path in validated}
        assert "provider-registry.schema.json" in names
        assert "model-registry.schema.json" in names
        assert "adapter-manifest.schema.json" in names
        assert "routing-policy.schema.json" in names

    def test_invalid_schema_raises_configuration_error(self, tmp_path: Path) -> None:
        bad = tmp_path / "bad.schema.json"
        bad.write_text(
            '{"$schema": "https://json-schema.org/draft/2020-12/schema", "type": "not-a-type"}',
            encoding="utf-8",
        )
        with pytest.raises(ai_errors.AIConfigurationError):
            validate_json_schema_files(tmp_path)

    def test_conformance_cases_load(self) -> None:
        cases = load_conformance_cases(CONTRACTS_AI)
        assert len(cases) == 6
        assert [c.code for c in cases] == [
            "HEALTH_CHECK",
            "ERROR_NORMALIZATION",
            "STRUCTURED_OUTPUT_VALIDATION",
            "TOOL_CALL_SCHEMA_CONFORMANCE",
            "EMBEDDING_DIMENSION_STABILITY",
            "TIMEOUT_AND_CANCELLATION",
        ]
