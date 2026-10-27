#!/usr/bin/env python3
"""Baseline secret scanner (stdlib only, deterministic).

Scans repository files for common secret material and prohibited committed files
(`.env`, private keys). Used by `python scripts/dev.py secret-scan` and by the
architecture guardrail tests. This is a baseline gate, not a substitute for a
full secret-management review (`docs/security/secrets-management.md`).
"""

from __future__ import annotations

import re
import sys
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Directories that are never scanned (generated/cache/local).
SKIP_DIRS = {".git", "node_modules", ".venv", ".next", ".pytest_cache", ".ruff_cache", "__pycache__", "dist", "out", "build", "coverage", "data", "logs"}
SKIP_SUFFIXES = {".pyc", ".png", ".jpg", ".jpeg", ".gif", ".ico", ".woff", ".woff2", ".ttf", ".zip", ".lock", ".min.js", ".min.css", ".map"}
# Lockfiles may legitimately contain checksums; skip them for the baseline scan.
SKIP_FILES = {"uv.lock", "pnpm-lock.yaml", "package-lock.json", "poetry.lock", "go.sum", "Cargo.lock"}

FORBIDDEN_FILENAMES = {".env", ".env.local", ".env.production", ".env.development"}
# Sanctioned placeholder-only env templates (e.g. frontend/.env.example) are allowed;
# they are content-scanned below, where known placeholder values are permitted.
ENV_TEMPLATE_SUFFIX = ".env.example"

PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    ("aws_access_key", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    ("aws_secret_key", re.compile(r"\baws_secret_access_key\s*=\s*['\"][0-9A-Za-z/+=]{40}['\"]", re.IGNORECASE)),
    ("private_key_block", re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----")),
    ("github_token", re.compile(r"\bgh[pousr]_[0-9A-Za-z]{30,}\b")),
    ("slack_token", re.compile(r"\bxox[baprs]-[0-9A-Za-z-]{20,}\b")),
    ("generic_password", re.compile(r"\b(password|passwd|pwd)\s*[:=]\s*['\"][^'\"]{6,}['\"]", re.IGNORECASE)),
    ("generic_api_key", re.compile(r"\b(api[_-]?key|apikey|client[_-]?secret|access[_-]?token)\s*[:=]\s*['\"][^'\"]{8,}['\"]", re.IGNORECASE)),
    ("jwt", re.compile(r"\beyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\b")),
    ("connection_string_secret", re.compile(r"\b(postgres|mysql|mongodb)(\+[a-z]+)?://[^:/\s]+:[^@/\s]+@", re.IGNORECASE)),
]


@dataclass(frozen=True, slots=True)
class Finding:
    path: Path
    line: int
    kind: str


# Explicit local-only placeholder values allowed by the local-development contract.
# Lines containing these values are templates, not leaked credentials.
KNOWN_LOCAL_PLACEHOLDERS = ("local_dev_password_only", "change-me-please")


def iter_files(root: Path) -> list[Path]:
    files: list[Path] = []
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        rel = path.relative_to(root)
        if any(part in SKIP_DIRS for part in rel.parts):
            continue
        if path.suffix.lower() in SKIP_SUFFIXES:
            continue
        if path.name in SKIP_FILES:
            continue
        files.append(path)
    return sorted(files)


def scan_repo(root: Path = ROOT) -> list[Finding]:
    findings: list[Finding] = []
    for path in iter_files(root):
        if path.name in FORBIDDEN_FILENAMES:
            findings.append(Finding(path=path, line=1, kind="forbidden_env_file"))
            continue
        try:
            lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
        except OSError:
            continue
        # Real env files are forbidden by filename above; *.env.example templates fall through to content scanning.
        for lineno, line in enumerate(lines, start=1):
            if any(placeholder in line for placeholder in KNOWN_LOCAL_PLACEHOLDERS):
                continue
            for kind, pattern in PATTERNS:
                if pattern.search(line):
                    findings.append(Finding(path=path, line=lineno, kind=kind))
                    break
    return findings


def main() -> int:
    findings = scan_repo(ROOT)
    if not findings:
        print("SECRET SCAN: no findings (baseline gate passed).")
        return 0
    print("SECRET SCAN: findings detected:")
    for finding in findings:
        print(f"  {finding.path} : {finding.line} [{finding.kind}]")
    print("Action required: remove the secret, rotate it if ever exposed, and add the file to .gitignore.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
