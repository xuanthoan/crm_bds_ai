# CRM_BDS_AI backend shell

Backend application shell for the `crm_bds_ai` modular monolith (Sprint 1 Engineering Foundation).

**No business code lives here.** This package provides only the engineering foundation:
typed configuration, application factory, structured logging, request/correlation IDs,
Problem Details error boundary, health/liveness/readiness, Alembic baseline,
Celery worker shell and the AI provider abstraction foundation (Mock Adapter only).

## Layout

```text
backend/
  pyproject.toml        # dependency manifest (exact versions from Toolchain Lock + uv.lock)
  uv.lock               # fully resolved lockfile (deterministic install)
  migrations/           # Alembic baseline (no business schema)
  src/crm_bds_ai/
    bootstrap/          # settings, container, application factory
    shared_kernel/      # framework-free primitives (correlation ids, error types)
    infra/              # logging, http (middleware/health/problem details), db, worker, ai
  tests/                # unit / integration / health / contracts / migration / ai tests
```

Dependency versions are governed by `docs/engineering/technology-toolchain-lock.md`
(ENG-TOOLCHAIN-001) and committed lockfiles. Never add a dependency outside the lock.
