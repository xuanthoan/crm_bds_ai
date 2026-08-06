"""Architecture boundary analyzer (import-based guardrails).

Pure filesystem + AST analysis — no runtime import of application code. Used by
the architecture guardrail tests, including anti-pattern negative fixtures.
"""

from __future__ import annotations

import ast
import re
from dataclasses import dataclass
from pathlib import Path

# Framework roots whose use inside restricted layers is forbidden.
WEB_FRAMEWORKS = ("fastapi", "uvicorn", "starlette")
ORM_FRAMEWORKS = ("sqlalchemy",)
BROKER_FRAMEWORKS = ("celery", "kombu")
FRAMEWORKS = (*WEB_FRAMEWORKS, *ORM_FRAMEWORKS, *BROKER_FRAMEWORKS)

# Business context names (ADR-002). No code may exist under contexts/ in Sprint 1.
BUSINESS_CONTEXTS = (
    "platform", "iam", "party", "lead", "product", "matching", "transaction",
    "contract", "revenue", "activity", "marketing", "analytics", "documents",
    "audit", "integration", "operations",
)


@dataclass(frozen=True, slots=True)
class Violation:
    path: Path
    message: str


def iter_python_files(root: Path) -> list[Path]:
    return sorted(
        path
        for path in root.rglob("*.py")
        if ".venv" not in path.parts and "node_modules" not in path.parts
    )


def _imports_of(source: str) -> list[str]:
    """Return the imported module names (dotted) from a python source file."""
    names: list[str] = []
    tree = ast.parse(source)
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            names.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            names.append(node.module)
    return names


def _module_root(module: str) -> str:
    return module.split(".")[0]


def check_layer_dependencies(root: Path) -> list[Violation]:
    """Enforce layer dependency rules on the backend source tree.

    - `shared_kernel` must never import web/ORM/broker frameworks.
    - presentation (`http`, `presentation`) must never import ORM/database drivers.
    - domain code (under `contexts/<ctx>/domain`) must never import frameworks.
    """
    violations: list[Violation] = []
    src = root / "backend" / "src"
    if not src.exists():
        return violations
    for path in iter_python_files(src):
        rel = path.relative_to(src).as_posix()
        try:
            roots = _imports_of(path.read_text(encoding="utf-8"))
        except (OSError, SyntaxError):
            continue
        for module in roots:
            framework = _module_root(module)
            if framework in FRAMEWORKS:
                if "shared_kernel" in rel:
                    violations.append(Violation(path, f"shared_kernel must not import {module}"))
                if "presentation" in rel or "/http/" in rel or rel.startswith("http"):
                    if framework in ORM_FRAMEWORKS or framework in BROKER_FRAMEWORKS:
                        violations.append(
                            Violation(path, f"presentation layer must not import {module}")
                        )
                if "/domain/" in rel and framework in FRAMEWORKS:
                    violations.append(Violation(path, f"domain must not import {module}"))
    return violations


def check_cross_context_imports(root: Path) -> list[Violation]:
    """Context modules must never import another context's module (ADR-004)."""
    violations: list[Violation] = []
    contexts_root = root / "backend" / "src" / "crm_bds_ai" / "contexts"
    if not contexts_root.exists():
        return violations  # Sprint 1: no contexts exist yet
    for path in iter_python_files(contexts_root):
        rel_parts = path.relative_to(contexts_root).parts
        own_context = rel_parts[0]
        try:
            roots = _imports_of(path.read_text(encoding="utf-8"))
        except (OSError, SyntaxError):
            continue
        for module in roots:
            for context in BUSINESS_CONTEXTS:
                if context == own_context:
                    continue
                if module == f"crm_bds_ai.contexts.{context}" or module.startswith(
                    f"crm_bds_ai.contexts.{context}."
                ):
                    violations.append(
                        Violation(path, f"cross-context import of {context} is forbidden (ADR-004)")
                    )
    return violations


def check_no_business_contexts(root: Path) -> list[Violation]:
    """Sprint 1 must not create any business context package."""
    contexts_root = root / "backend" / "src" / "crm_bds_ai" / "contexts"
    if contexts_root.exists():
        return [Violation(contexts_root, "business context packages must not exist in Sprint 1")]
    return []


def check_migrations_are_business_free(root: Path) -> list[Violation]:
    """Migrations must not create business tables in Sprint 1."""
    violations: list[Violation] = []
    migrations = root / "backend" / "migrations"
    if not migrations.exists():
        return violations
    for path in sorted(migrations.rglob("*.py")):
        if path.name in ("env.py", "script.py.mako"):
            continue
        try:
            text = path.read_text(encoding="utf-8").lower()
        except OSError:
            continue
        if "create table" in text or "op.create_table" in text or "sa.table(" in text:
            violations.append(Violation(path, "CREATE TABLE found in Sprint 1 baseline"))
    return violations


def check_frontend_handwritten_api_types(root: Path) -> list[Violation]:
    """Frontend must never redefine types owned by the generated API client.

    The generated client boundary is `frontend/generated/api.d.ts`. Feature/app
    code that redeclares the same top-level type names is a contract violation
    (`docs/engineering/api-standards.md` section 38).
    """
    generated = root / "frontend" / "generated" / "api.d.ts"
    if not generated.exists():
        return [Violation(generated, "generated API client missing; run openapi-typescript")]
    text = generated.read_text(encoding="utf-8")
    generated_names = set(re.findall(r"^\s*(?:export\s+)?(?:interface|type)\s+([A-Za-z_]\w*)", text, re.M))
    if not generated_names:
        return []
    violations: list[Violation] = []
    scan_dirs = [root / "frontend" / "app", root / "frontend" / "components", root / "frontend" / "lib"]
    for directory in scan_dirs:
        if not directory.exists():
            continue
        for path in sorted(directory.rglob("*.ts*")):
            if "generated" in path.parts:
                continue
            try:
                source = path.read_text(encoding="utf-8")
            except OSError:
                continue
            declared = set(
                re.findall(r"^\s*(?:export\s+)?(?:interface|type)\s+([A-Za-z_]\w*)", source, re.M)
            )
            for name in sorted(declared & generated_names):
                violations.append(
                    Violation(path, f"handwritten type '{name}' collides with generated API client")
                )
    return violations
