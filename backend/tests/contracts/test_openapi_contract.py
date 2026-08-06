"""Contract validation tests: OpenAPI 3.1 baseline and deterministic generation."""

from __future__ import annotations

import json
import sys
from pathlib import Path

from openapi_spec_validator import validate as validate_openapi

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "scripts"))

from generate_openapi import build_spec_dict  # noqa: E402

CONTRACTS_OPENAPI = ROOT / "contracts" / "openapi" / "openapi.json"


def _generated_spec_dict() -> dict:
    return build_spec_dict()


class TestOpenAPIContract:
    def test_openapi_version_is_3_1(self) -> None:
        spec = _generated_spec_dict()
        assert spec["openapi"] == "3.1.0"

    def test_spec_is_valid(self) -> None:
        validate_openapi(_generated_spec_dict())

    def test_only_technical_paths(self) -> None:
        spec = _generated_spec_dict()
        assert set(spec["paths"].keys()) == {"/", "/health/live", "/health/ready"}

    def test_operation_ids_unique(self) -> None:
        spec = _generated_spec_dict()
        operation_ids = [
            (path, method, op.get("operationId"))
            for path, methods in spec["paths"].items()
            for method, op in methods.items()
            if isinstance(op, dict) and "operationId" in op
        ]
        ids = [op_id for _, _, op_id in operation_ids]
        assert len(ids) == len(set(ids)), f"duplicate operation ids: {ids}"

    def test_problem_details_schema_declared(self) -> None:
        spec = _generated_spec_dict()
        schemas = spec.get("components", {}).get("schemas", {})
        assert "ProblemDetails" in schemas

    def test_committed_contract_matches_generation(self) -> None:
        """Deterministic drift check: committed openapi.json == regenerated spec."""
        assert CONTRACTS_OPENAPI.exists(), f"missing committed contract: {CONTRACTS_OPENAPI}"
        committed = json.loads(CONTRACTS_OPENAPI.read_text(encoding="utf-8"))
        generated = _generated_spec_dict()
        assert committed == generated, (
            "contract drift detected: regenerate via `python scripts/dev.py openapi`"
        )

    def test_committed_contract_has_no_manual_edit_header(self) -> None:
        content = CONTRACTS_OPENAPI.read_text(encoding="utf-8")
        assert "DO NOT EDIT MANUALLY" in content
