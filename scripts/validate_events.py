#!/usr/bin/env python3
"""Validate machine contracts: JSON Schema (draft 2020-12), AsyncAPI 3.x baseline.

Invoked by `python scripts/dev.py events`.

Validation coverage:
- every `*.schema.json` under `contracts/events/` and `contracts/ai/` is a valid
  draft 2020-12 schema (meta-validation);
- sample documents validate against their schemas;
- the AsyncAPI 3.x baseline file is structurally valid;
- AI registries (capability + use-case) load against canonical capability codes.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import jsonschema
import yaml

ROOT = Path(__file__).resolve().parent.parent
EVENTS_DIR = ROOT / "contracts" / "events"
AI_DIR = ROOT / "contracts" / "ai"
ASYNCAPI_FILE = ROOT / "contracts" / "asyncapi" / "asyncapi.yaml"

DRAFT_2020_12 = "https://json-schema.org/draft/2020-12/schema"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_schema_files() -> list[str]:
    validated: list[str] = []
    for directory in (EVENTS_DIR, AI_DIR):
        if not directory.exists():
            continue
        for path in sorted(directory.rglob("*.schema.json")):
            schema = load_json(path)
            if schema.get("$schema") != DRAFT_2020_12:
                raise SystemExit(f"{path}: $schema must be draft 2020-12, got {schema.get('$schema')!r}")
            jsonschema.Draft202012Validator.check_schema(schema)
            validated.append(str(path))
    return validated


def validate_samples() -> list[str]:
    checked: list[str] = []
    envelope_schema = EVENTS_DIR / "event-envelope.schema.json"
    if envelope_schema.exists():
        schema = load_json(envelope_schema)
        sample = {
            "event_id": "123e4567-e89b-12d3-a456-426614174000",
            "event_type": "technical.smoke",
            "event_version": 1,
            "occurred_at": "2026-08-06T00:00:00Z",
            "producer": "crm-bds-ai-backend",
            "data_classification": "INTERNAL",
            "data": {"ok": True},
        }
        jsonschema.validate(instance=sample, schema=schema)
        checked.append(str(envelope_schema))
    problem_schema = EVENTS_DIR / "problem-details.schema.json"
    if problem_schema.exists():
        schema = load_json(problem_schema)
        sample = {
            "type": "about:blank",
            "title": "Validation failed",
            "status": 422,
            "detail": "bad payload",
            "instance": "/api/v1/x",
            "error_code": "COMMON_VALIDATION_FAILED",
            "correlation_id": "abc",
        }
        jsonschema.validate(instance=sample, schema=schema)
        checked.append(str(problem_schema))
    return checked


def validate_asyncapi() -> str:
    data = yaml.safe_load(ASYNCAPI_FILE.read_text(encoding="utf-8"))
    if data.get("asyncapi") not in ("3.0.0", "3.0"):
        raise SystemExit(f"{ASYNCAPI_FILE}: asyncapi version must be 3.0.0")
    if not data.get("info", {}).get("title"):
        raise SystemExit(f"{ASYNCAPI_FILE}: info.title required")
    if not data.get("info", {}).get("version"):
        raise SystemExit(f"{ASYNCAPI_FILE}: info.version required")
    for section in ("channels", "operations"):
        if section not in data:
            raise SystemExit(f"{ASYNCAPI_FILE}: missing required section '{section}'")
    return str(ASYNCAPI_FILE)


def validate_ai_registries() -> list[str]:
    """Validate AI YAML registries against canonical capability codes."""
    sys.path.insert(0, str(ROOT / "backend" / "src"))
    from crm_bds_ai.infra.ai.registries import (
        load_capability_registry,
        load_use_case_registry,
        validate_use_cases_against_capabilities,
    )

    registry = load_capability_registry(AI_DIR)
    use_cases = load_use_case_registry(AI_DIR)
    validate_use_cases_against_capabilities(use_cases, registry)
    return [str(AI_DIR / "capability-registry.yaml"), str(AI_DIR / "use-case-registry.yaml")]


def main() -> int:
    print("Validating JSON Schema files (draft 2020-12) ...")
    for path in validate_schema_files():
        print(f"  ok {path}")
    print("Validating sample documents ...")
    for path in validate_samples():
        print(f"  ok sample -> {path}")
    print("Validating AsyncAPI baseline ...")
    print(f"  ok {validate_asyncapi()}")
    print("Validating AI registries ...")
    for path in validate_ai_registries():
        print(f"  ok {path}")
    print("EVENTS: all contract validations passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
