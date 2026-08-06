"""Anti-pattern negative tests.

Each test creates a small technical fixture that *violates* an architecture rule
and asserts the analyzer detects it. The fixtures are ephemeral (`tmp_path`) and
never become part of the repository.
"""

from __future__ import annotations

from pathlib import Path

from analyzer import (
    check_cross_context_imports,
    check_frontend_handwritten_api_types,
    check_layer_dependencies,
    check_migrations_are_business_free,
    check_no_business_contexts,
)


def _write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


class TestSharedKernelFrameworkFree:
    def test_shared_kernel_importing_fastapi_is_detected(self, tmp_path: Path) -> None:
        _write(
            tmp_path / "backend" / "src" / "crm_bds_ai" / "shared_kernel" / "web.py",
            "from fastapi import FastAPI\n",
        )
        violations = check_layer_dependencies(tmp_path)
        assert any("shared_kernel" in str(v.path) and "fastapi" in v.message for v in violations)


class TestPresentationToDB:
    def test_presentation_importing_sqlalchemy_is_detected(self, tmp_path: Path) -> None:
        _write(
            tmp_path / "backend" / "src" / "crm_bds_ai" / "infra" / "http" / "handler.py",
            "import sqlalchemy  # direct DB access from presentation\n",
        )
        violations = check_layer_dependencies(tmp_path)
        assert any("presentation" in v.message and "sqlalchemy" in v.message for v in violations)


class TestDomainToWeb:
    def test_domain_importing_web_framework_is_detected(self, tmp_path: Path) -> None:
        _write(
            tmp_path / "backend" / "src" / "crm_bds_ai" / "contexts" / "party" / "domain" / "model.py",
            "from fastapi import Request  # domain must not depend on web\n",
        )
        violations = check_layer_dependencies(tmp_path)
        assert any("domain" in v.message and "fastapi" in v.message for v in violations)


class TestCrossContextImport:
    def test_cross_context_import_is_detected(self, tmp_path: Path) -> None:
        _write(
            tmp_path / "backend" / "src" / "crm_bds_ai" / "contexts" / "lead" / "application" / "svc.py",
            "from crm_bds_ai.contexts.party.domain.model import Party  # forbidden ADR-004\n",
        )
        violations = check_cross_context_imports(tmp_path)
        assert any("party" in v.message for v in violations)


class TestBusinessContextsNotCreated:
    def test_empty_context_package_is_detected(self, tmp_path: Path) -> None:
        _write(
            tmp_path / "backend" / "src" / "crm_bds_ai" / "contexts" / "lead" / "__init__.py",
            "",
        )
        violations = check_no_business_contexts(tmp_path)
        assert len(violations) == 1


class TestMigrationsBusinessFree:
    def test_business_table_in_migration_is_detected(self, tmp_path: Path) -> None:
        _write(
            tmp_path / "backend" / "migrations" / "versions" / "9999_bad.py",
            'def upgrade() -> None:\n    op.create_table("customers")\n',
        )
        violations = check_migrations_are_business_free(tmp_path)
        assert any("create table" in v.message.lower() for v in violations)


class TestFrontendHandwrittenTypes:
    def test_handwritten_type_colliding_with_generated_is_detected(self, tmp_path: Path) -> None:
        _write(
            tmp_path / "frontend" / "generated" / "api.d.ts",
            "export type ProblemDetails = { type: string };\n",
        )
        _write(
            tmp_path / "frontend" / "lib" / "custom.ts",
            "export type ProblemDetails = { other: string };  // collides\n",
        )
        violations = check_frontend_handwritten_api_types(tmp_path)
        assert any("ProblemDetails" in v.message for v in violations)

    def test_missing_generated_client_is_detected(self, tmp_path: Path) -> None:
        violations = check_frontend_handwritten_api_types(tmp_path)
        assert any("generated API client missing" in v.message for v in violations)
