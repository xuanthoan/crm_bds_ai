#!/usr/bin/env python3
"""CRM_BDS_AI repository command entry point (single entry point).

Contract: `docs/implementation/dev-command-contract.md` (IMPL-DEV-CMD-001).
All commands fail non-zero on error, print actionable messages and work on the
supported developer OS (Windows cmd / POSIX shells).

Usage:
    python scripts/dev.py <command> [args]
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BACKEND = ROOT / "backend"
FRONTEND = ROOT / "frontend"
COMPOSE_FILE = ROOT / "infrastructure" / "compose" / "compose.yaml"
ENV_EXAMPLE = ROOT / ".env.example"
ENV_FILE = ROOT / ".env"

TOOLS = {
    "git": ["--version"],
    "python": ["--version"],
    "uv": ["--version"],
    "node": ["--version"],
    "pnpm": ["--version"],
    "docker": ["--version"],
}


def _run(command: list[str], cwd: Path = ROOT) -> int:
    print(f"\n$ {' '.join(command)}", flush=True)
    result = subprocess.run(command, cwd=cwd, text=True)
    return result.returncode


def _require(*tools: str) -> int:
    missing = []
    for tool in tools:
        if shutil.which(tool) is None:
            missing.append(tool)
    if missing:
        print(f"ERROR: required tool(s) not found: {', '.join(missing)}")
        print("See docs/engineering/technology-toolchain-lock.md (ENG-TOOLCHAIN-001).")
        return 1
    return 0


def _uv_run(command: list[str], cwd: Path = ROOT) -> int:
    return _run(["uv", "run", "--project", str(BACKEND), *command], cwd=cwd)


# --------------------------------------------------------------------------- #
# commands
# --------------------------------------------------------------------------- #
def cmd_setup(_args: argparse.Namespace) -> int:
    if (rc := _require(*TOOLS)) != 0:
        return rc
    print("==> Locked backend install (uv sync)")
    if (rc := _run(["uv", "sync", "--project", str(BACKEND)])) != 0:
        return rc
    print("==> Locked frontend install (pnpm --frozen-lockfile)")
    if (rc := _run(["pnpm", "--dir", str(FRONTEND), "install", "--frozen-lockfile"])) != 0:
        return rc
    if not ENV_FILE.exists():
        if ENV_EXAMPLE.exists():
            shutil.copy2(ENV_EXAMPLE, ENV_FILE)
            print(f"NOTE: created {ENV_FILE} from {ENV_EXAMPLE.name} (local-only safe defaults).")
        else:
            print("WARNING: .env.example not found; environment file not created.")
    else:
        print("NOTE: .env already present; leaving it untouched.")
    print("SETUP: OK")
    return 0


def cmd_up(_args: argparse.Namespace) -> int:
    if (rc := _require("docker")) != 0:
        return rc
    return _run(
        [
            "docker", "compose",
            "-f", str(COMPOSE_FILE),
            "up", "-d", "--wait",
        ]
    )


def cmd_down(_args: argparse.Namespace) -> int:
    if (rc := _require("docker")) != 0:
        return rc
    return _run(["docker", "compose", "-f", str(COMPOSE_FILE), "down"])


def cmd_migrate(_args: argparse.Namespace) -> int:
    if (rc := _require("uv")) != 0:
        return rc
    print("==> Upgrade database to head (ephemeral/dev database)")
    return _uv_run(["alembic", "-c", "alembic.ini", "upgrade", "head"], cwd=BACKEND)


def cmd_worker(_args: argparse.Namespace) -> int:
    if (rc := _require("uv")) != 0:
        return rc
    print("==> Starting Celery worker (Ctrl+C to stop)")
    return _uv_run(
        ["celery", "-A", "crm_bds_ai.infra.worker.celery_app", "worker", "--loglevel=INFO"],
        cwd=BACKEND,
    )


def cmd_format(args: argparse.Namespace) -> int:
    if (rc := _require("uv")) != 0:
        return rc
    check_flag = ["--check"] if args.check else []
    return _uv_run(["ruff", "format", *check_flag, "src", "tests"], cwd=BACKEND)


def cmd_lint(_args: argparse.Namespace) -> int:
    if (rc := _require("uv")) != 0:
        return rc
    return _uv_run(["ruff", "check", "src", "tests"], cwd=BACKEND)


def cmd_typecheck(_args: argparse.Namespace) -> int:
    if (rc := _require("uv")) != 0:
        return rc
    return _uv_run(["pyright", "src"], cwd=BACKEND)


def cmd_test(args: argparse.Namespace) -> int:
    if (rc := _require("uv")) != 0:
        return rc
    selectors = {
        "unit": [str(BACKEND / "tests" / "unit"), str(BACKEND / "tests" / "health")],
        "integration": [str(BACKEND / "tests" / "integration")],
        "architecture": [str(ROOT / "tests" / "architecture")],
        "contracts": [str(BACKEND / "tests" / "contracts")],
        "ai": [str(BACKEND / "tests" / "ai")],
        "migration": [str(BACKEND / "tests" / "integration" / "test_migration.py")],
    }
    if args.selector == "all":
        paths = [str(BACKEND / "tests"), str(ROOT / "tests" / "architecture")]
    else:
        if args.selector not in selectors:
            print(f"ERROR: unknown test selector '{args.selector}'. Valid: {', '.join(['all', *selectors])}")
            return 1
        paths = selectors[args.selector]
    return _uv_run(["pytest", "-q", *paths])


def cmd_openapi(args: argparse.Namespace) -> int:
    if (rc := _require("uv")) != 0:
        return rc
    if args.check:
        return _uv_run(["python", str(ROOT / "scripts" / "generate_openapi.py"), "--check"])
    return _uv_run(["python", str(ROOT / "scripts" / "generate_openapi.py")])


def cmd_events(_args: argparse.Namespace) -> int:
    if (rc := _require("uv")) != 0:
        return rc
    return _uv_run(["python", str(ROOT / "scripts" / "validate_events.py")])


def cmd_secret_scan(_args: argparse.Namespace) -> int:
    return _run([sys.executable, str(ROOT / "scripts" / "secret_scan.py")])


def cmd_architecture_check(_args: argparse.Namespace) -> int:
    if (rc := _require("uv")) != 0:
        return rc
    return _uv_run(["pytest", "-q", str(ROOT / "tests" / "architecture")])


def cmd_docs_check(_args: argparse.Namespace) -> int:
    """Baseline documentation check: relative links resolve, no broken paths."""
    broken: list[str] = []
    files = [ROOT / "README.md", *sorted((ROOT / "docs").rglob("*.md"))]
    for file_path in files:
        text = file_path.read_text(encoding="utf-8", errors="replace")
        for match in __import__("re").finditer(r"\]\(([^)#]+)(?:#[^)]*)?\)", text):
            target = match.group(1).strip()
            if target.startswith(("http://", "https://", "mailto:")):
                continue
            resolved = (file_path.parent / target).resolve()
            if not resolved.exists():
                broken.append(f"{file_path.relative_to(ROOT)} -> {target}")
    if broken:
        print("DOCS CHECK: broken links detected:")
        for item in broken:
            print(f"  {item}")
        return 1
    print(f"DOCS CHECK: OK ({len(files)} files scanned, no broken relative links).")
    return 0


def cmd_check(_args: argparse.Namespace) -> int:
    """Full mandatory local quality gate orchestration."""
    steps: list[tuple[str, list[str]]] = [
        ("backend:format", ["format", "--check"]),
        ("backend:lint", ["lint"]),
        ("backend:typecheck", ["typecheck"]),
        ("backend:unit+health", ["test", "unit"]),
        ("backend:contracts", ["test", "contracts"]),
        ("backend:ai", ["test", "ai"]),
        ("architecture", ["architecture-check"]),
        ("contracts:openapi", ["openapi", "--check"]),
        ("contracts:events", ["events"]),
        ("frontend:lint", ["frontend", "lint"]),
        ("frontend:typecheck", ["frontend", "typecheck"]),
        ("frontend:test", ["frontend", "test"]),
        ("frontend:build", ["frontend", "build"]),
        ("secret-scan", ["secret-scan"]),
    ]
    failed: list[str] = []
    for name, argv in steps:
        print(f"\n===== CHECK [{name}] =====", flush=True)
        if cmd_dispatch(argv) != 0:
            failed.append(name)
    if failed:
        print(f"\nCHECK FAILED in: {', '.join(failed)}")
        print("Fix the failing steps above and re-run: python scripts/dev.py check")
        return 1
    print("\nCHECK: all mandatory quality gates passed.")
    return 0


def cmd_frontend(args: argparse.Namespace) -> int:
    if (rc := _require("pnpm")) != 0:
        return rc
    scripts = {
        "lint": "lint",
        "typecheck": "typecheck",
        "test": "test:run",
        "build": "build",
    }
    if args.step not in scripts:
        print(f"ERROR: unknown frontend step '{args.step}'. Valid: {', '.join(scripts)}")
        return 1
    return _run(["pnpm", "--dir", str(FRONTEND), "run", scripts[args.step]])


def cmd_smoke(_args: argparse.Namespace) -> int:
    """Local end-to-end health verification (no business behavior)."""
    print("==> smoke: verifying local stack endpoints")
    base = os.environ.get("API_BASE_URL", "http://localhost:8000")

    def get(path: str) -> tuple[int, dict]:
        try:
            with urllib.request.urlopen(f"{base}{path}", timeout=10) as response:
                return response.status, json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            try:
                return exc.code, json.loads(exc.read().decode("utf-8"))
            except Exception:  # noqa: BLE001
                return exc.code, {}
        except Exception as exc:  # noqa: BLE001
            return 0, {"error": str(exc)}

    status, body = get("/health/live")
    live_ok = status == 200
    print(f"  /health/live  -> {status} {body.get('status', body)}")
    status, body = get("/health/ready")
    ready_ok = status in (200, 503) and body.get("status") in ("healthy", "degraded", "unhealthy")
    print(f"  /health/ready -> {status} {body.get('status')} (checks: {len(body.get('checks', []))})")
    status, body = get("/openapi.json")
    openapi_ok = status == 200 and body.get("openapi") == "3.1.0"
    print(f"  /openapi.json -> {status} openapi={body.get('openapi')}")

    print("==> smoke: worker technical task executes")
    worker_rc = _uv_run(
        [
            "python", "-c",
            "from crm_bds_ai.infra.worker.tasks import diagnostics_smoke; "
            "r = diagnostics_smoke.run('smoke'); print('  worker smoke payload:', r)",
        ],
        cwd=BACKEND,
    )
    all_ok = live_ok and ready_ok and openapi_ok and worker_rc == 0
    if all_ok:
        print("SMOKE: PASS")
    else:
        print("SMOKE: FAIL (start local stack with `python scripts/dev.py up` first)")
    return 0 if all_ok else 1


# --------------------------------------------------------------------------- #
# dispatch
# --------------------------------------------------------------------------- #
COMMANDS = {
    "setup": cmd_setup,
    "up": cmd_up,
    "down": cmd_down,
    "migrate": cmd_migrate,
    "worker": cmd_worker,
    "format": cmd_format,
    "lint": cmd_lint,
    "typecheck": cmd_typecheck,
    "test": cmd_test,
    "openapi": cmd_openapi,
    "events": cmd_events,
    "secret-scan": cmd_secret_scan,
    "architecture-check": cmd_architecture_check,
    "docs-check": cmd_docs_check,
    "check": cmd_check,
    "frontend": cmd_frontend,
    "smoke": cmd_smoke,
}


def cmd_dispatch(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(prog="dev.py", description="crm_bds_ai repository command entry point")
    parser.add_argument("command", choices=sorted(COMMANDS))
    parser.add_argument("--check", action="store_true", help="check-only mode (openapi)")
    parser.add_argument("args", nargs="*", help="command-specific arguments")
    args = parser.parse_args(argv)
    handler = COMMANDS[args.command]

    if args.command == "format":
        return handler(argparse.Namespace(check=args.check))
    if args.command == "test":
        selector = args.args[0] if args.args else "all"
        return handler(argparse.Namespace(selector=selector))
    if args.command == "openapi":
        return handler(argparse.Namespace(check=args.check))
    if args.command == "frontend":
        step = args.args[0] if args.args else "lint"
        return handler(argparse.Namespace(step=step))
    return handler(args)


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: python scripts/dev.py <command> [args]")
        print(f"Commands: {', '.join(sorted(COMMANDS))}")
        return 2
    return cmd_dispatch(sys.argv[1:])


if __name__ == "__main__":
    raise SystemExit(main())
