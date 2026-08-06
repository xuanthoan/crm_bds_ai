# Test zones

This repository keeps tests next to their ownership zone (backend/frontend) plus a
cross-cutting architecture zone at the root.

| Zone | Path | Runner | Requires |
|---|---|---|---|
| Backend unit + health | `backend/tests/unit/`, `backend/tests/health/` | pytest | backend venv |
| Backend contracts | `backend/tests/contracts/` | pytest | backend venv |
| Backend AI conformance | `backend/tests/ai/` | pytest | backend venv |
| Backend integration + migration | `backend/tests/integration/` | pytest | local PostgreSQL (docker compose) |
| Architecture guardrails | `tests/architecture/` | pytest | backend venv (fs scan only) |
| Frontend | `frontend/tests/` | vitest | pnpm |

Invocation:

```text
python scripts/dev.py test            # all backend + architecture tests
python scripts/dev.py test unit       # backend unit + health
python scripts/dev.py test integration
python scripts/dev.py test migration
python scripts/dev.py test architecture
python scripts/dev.py test contracts
python scripts/dev.py test ai
python scripts/dev.py frontend test   # vitest
```

Rules:

- Tests must never require wiping developer persistent data.
- Integration tests use the ephemeral `crm_bds_ai_test` database only.
- Architecture tests run a filesystem scan (no runtime imports) and include
  anti-pattern negative fixtures under `tmp_path`.
