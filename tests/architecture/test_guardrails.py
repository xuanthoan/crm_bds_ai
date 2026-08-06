"""Architecture guardrails (real repository scan)."""

from __future__ import annotations

from pathlib import Path

import pytest

from analyzer import (
    check_cross_context_imports,
    check_frontend_handwritten_api_types,
    check_layer_dependencies,
    check_migrations_are_business_free,
    check_no_business_contexts,
)

ROOT = Path(__file__).resolve().parents[2]


def _assert_no_violations(violations: list, label: str) -> None:
    if violations:
        details = "\n".join(f"  {v.path} : {v.message}" for v in violations)
        pytest.fail(f"{label} violations:\n{details}")


class TestBackendBoundaries:
    def test_shared_kernel_and_layers_obey_dependency_rules(self) -> None:
        _assert_no_violations(check_layer_dependencies(ROOT), "layer dependency")

    def test_no_cross_context_imports(self) -> None:
        _assert_no_violations(check_cross_context_imports(ROOT), "cross-context import")

    def test_no_business_context_packages_in_sprint1(self) -> None:
        _assert_no_violations(check_no_business_contexts(ROOT), "business context")

    def test_migrations_contain_no_business_tables(self) -> None:
        _assert_no_violations(check_migrations_are_business_free(ROOT), "migration business keyword")


class TestFrontendBoundary:
    def test_frontend_does_not_redefine_generated_api_types(self) -> None:
        _assert_no_violations(check_frontend_handwritten_api_types(ROOT), "handwritten API types")
