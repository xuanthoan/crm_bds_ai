"""Provider / model / capability / use-case registry loading and validation.

Registry files live in `contracts/ai/` (canonical machine contracts). This module
loads them deterministically and validates data against the canonical JSON
Schemas (draft 2020-12) and YAML registries.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import jsonschema
import yaml

from crm_bds_ai.infra.ai.errors import AIConfigurationError
from crm_bds_ai.infra.ai.ports import Capability

CONTRACTS_AI_REL = Path("contracts/ai")


@dataclass(slots=True)
class UseCaseDefinition:
    code: str
    owner_context: str
    required_capabilities: list[Capability]
    output_schema_ref: str
    approval_mode: str
    provider_or_model_locked: bool
    status: str


@dataclass(slots=True)
class CapabilityRegistry:
    version: str
    capabilities: list[Capability] = field(default_factory=list)

    def contains(self, capability: Capability) -> bool:
        return capability in self.capabilities


@dataclass(slots=True)
class ConformanceCase:
    code: str
    required: bool = False
    required_when_capability_claimed: str | None = None


def load_yaml(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle) or {}


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def load_capability_registry(contracts_dir: Path = CONTRACTS_AI_REL) -> CapabilityRegistry:
    data = load_yaml(contracts_dir / "capability-registry.yaml")
    try:
        capabilities = [Capability(code) for code in data.get("capabilities", [])]
    except ValueError as exc:
        raise AIConfigurationError(
            f"invalid capability code in capability-registry.yaml: {exc}"
        ) from exc
    return CapabilityRegistry(version=str(data.get("version", "")), capabilities=capabilities)


def load_use_case_registry(contracts_dir: Path = CONTRACTS_AI_REL) -> list[UseCaseDefinition]:
    data = load_yaml(contracts_dir / "use-case-registry.yaml")
    definitions: list[UseCaseDefinition] = []
    for item in data.get("use_cases", []):
        try:
            required = [Capability(code) for code in item.get("required_capabilities", [])]
        except ValueError as exc:
            raise AIConfigurationError(
                f"invalid capability in use-case {item.get('code')}: {exc}"
            ) from exc
        definitions.append(
            UseCaseDefinition(
                code=str(item["code"]),
                owner_context=str(item.get("owner_context", "")),
                required_capabilities=required,
                output_schema_ref=str(item.get("output_schema_ref", "")),
                approval_mode=str(item.get("approval_mode", "")),
                provider_or_model_locked=bool(item.get("provider_or_model_locked", False)),
                status=str(item.get("status", "")),
            )
        )
    return definitions


def load_conformance_cases(contracts_dir: Path = CONTRACTS_AI_REL) -> list[ConformanceCase]:
    data = load_yaml(contracts_dir / "provider-conformance" / "conformance-cases.yaml")
    cases: list[ConformanceCase] = []
    for item in data.get("cases", []):
        cases.append(
            ConformanceCase(
                code=str(item["code"]),
                required=bool(item.get("required", False)),
                required_when_capability_claimed=item.get("required_when_capability_claimed"),
            )
        )
    return cases


def validate_json_schema_files(contracts_dir: Path = CONTRACTS_AI_REL) -> list[str]:
    """Meta-validate every *.schema.json as draft 2020-12.

    Returns the list of validated files; raises ``AIConfigurationError`` on the
    first invalid file.
    """
    validated: list[str] = []
    for path in sorted(contracts_dir.glob("**/*.schema.json")):
        schema = load_json(path)
        declared = schema.get("$schema", "")
        if declared != "https://json-schema.org/draft/2020-12/schema":
            raise AIConfigurationError(
                f"{path.name}: $schema must be draft 2020-12, got '{declared}'"
            )
        try:
            jsonschema.Draft202012Validator.check_schema(schema)
        except jsonschema.SchemaError as exc:
            raise AIConfigurationError(f"{path.name}: invalid JSON Schema: {exc}") from exc
        validated.append(str(path))
    return validated


def validate_use_cases_against_capabilities(
    use_cases: list[UseCaseDefinition], registry: CapabilityRegistry
) -> None:
    """Every required capability in a use case must exist in the capability registry."""
    for use_case in use_cases:
        missing = [c.value for c in use_case.required_capabilities if not registry.contains(c)]
        if missing:
            raise AIConfigurationError(
                f"use case {use_case.code} requires unknown capabilities: {missing}"
            )
