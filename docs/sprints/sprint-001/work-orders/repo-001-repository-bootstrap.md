# WORK ORDER REPO-001 — REPOSITORY BOOTSTRAP AND DETERMINISTIC DEVELOPMENT FOUNDATION

**Work Order ID:** `REPO-001`
**Sprint:** 1 (Engineering Foundation)
**Status:** `READY_FOR_EXECUTION`
**Owner:** Goose (Orchestrator) → Opencode (Executor) khi được giao
**Created:** `2026-08-06`
**Acceptance:** Goose (Acceptance Authority) + Sprint 0 Acceptance Report = PASS WITH CONDITIONS (đã được chủ dự án chấp nhận)

---

# 1. Objective

Tạo repository `crm_bds_ai` reproducible, chạy được local, có CI baseline,
health/readiness, migration/contract bootstrap và architecture guardrails —
**chưa có bất kỳ business feature nào**.

# 2. Context

Sprint 0 Readiness Report: `PASS WITH CONDITIONS` (docs/reviews/sprint-0-readiness-report.md).
Các điều kiện FIN-001/002 đã được xử lý hoặc gán vào Work Order này.

# 3. Dependencies

- Sprint 0 Acceptance Report = PASS (đã đạt)
- Toolchain Lock: `docs/engineering/technology-toolchain-lock.md`
- Bootstrap blueprints: `docs/implementation/repository-bootstrap-blueprint.md`,
  `bootstrap-acceptance-checklist.md`, `dev-command-contract.md`,
  `health-readiness-contract.md`, `project-structure.md`, `machine-contract-bootstrap.md`

# 4. Allowed files (sẽ tạo/sửa)

```text
README.md (quick start)
.gitignore, .editorconfig
backend/          (shell, config, health, logging, error boundary, OpenAPI, Alembic baseline, tests)
frontend/         (Next.js shell, typed env, design-system boundary, generated client boundary, tests)
contracts/openapi/, contracts/events/, contracts/asyncapi/  (baseline)
infrastructure/   (compose, docker, environments)
scripts/dev.py    (single command entry point)
tests/
docs/sprints/sprint-001/implementation-notes.md
docs/sprints/sprint-001/evidence/
```

# 5. Forbidden files

```text
- Bất kỳ business aggregate/table/endpoint/Event nào (Lead, Customer, Product, Deal, Contract, Revenue…)
- `contexts/<context>` business code
- AI provider SDK / model calls (chỉ Mock Adapter theo ADR-022)
- Legacy/v1/compatibility/future-feature folders
- Secrets, credentials thật, PII test data
- Sửa canonical docs (README, Product, Architecture, ADR, Security, Sprint packs) ngoài mục được chỉ định
```

# 6. Canonical references

```text
README.md
docs/product/product-overview.md, PRD.md, domain-glossary.md
docs/architecture/architecture-overview.md, context-map.md, source-of-truth-matrix.md
docs/engineering/technology-toolchain-lock.md, coding-standards.md, api-standards.md,
  database-standards.md, event-standards.md, testing-standards.md, security-standards.md,
  frontend-standards.md, observability-standards.md, documentation-governance.md,
  ai-agent-engineering-constitution.md
.skills/universal-ai-engineering-orchestration/SKILL.md
docs/implementation/repository-bootstrap-blueprint.md, bootstrap-acceptance-checklist.md,
  dev-command-contract.md, health-readiness-contract.md, project-structure.md,
  machine-contract-bootstrap.md, ci-quality-gates.md, local-development-contract.md
ADR-001, ADR-002, ADR-003, ADR-004, ADR-005, ADR-006, ADR-007, ADR-021, ADR-022
docs/sprints/sprint-001/sprint-001-execution-pack.md
```

# 7. Requirements

1. Repository top-level: `backend/ frontend/ contracts/ infrastructure/ scripts/ tests/ docs/ .agent/ .skills/`
2. Không tạo 16 Context packages rỗng.
3. Backend shell: bootstrap, typed config, env validation, health/liveness/readiness,
   structured logging, request/correlation ID, error boundary (Problem Details),
   OpenAPI 3.1 generation, graceful shutdown, test harness.
4. Frontend shell: Next.js bootstrap, typed env, generated API client boundary,
   error/loading/not-found states, accessibility baseline, build/type/test pass.
5. Worker/scheduler shell: bootstrap, typed config, logs/correlation, health, graceful shutdown,
   minimal technical smoke task (không business behavior).
6. Local infra: PostgreSQL, RabbitMQ, Valkey, S3-compatible storage, health checks,
   safe local credentials, startup/shutdown docs.
7. Alembic baseline: config, empty/baseline revision, upgrade/downgrade verification; KHÔNG tạo business schemas.
8. Contract bootstrap: valid OpenAPI 3.1, AsyncAPI baseline/placeholder có status rõ, JSON Schema validation, deterministic generation, drift check.
9. Quality entry point: `python scripts/dev.py check` orchestration (format, lint, type, unit, architecture, contract, frontend build, secret scan).
10. CI baseline từ clean checkout, dùng locked dependencies, không bỏ qua failed step.
11. Architecture guardrails: cấm domain→web/ORM dependency, cross-context import, presentation→DB direct, secrets committed.
12. AI abstraction foundation: AIUseCasePort, AIProviderAdapter interface, Provider/Model/Capability/UseCase registries (schemas), Mock Adapter, feature flag, canonical error types — KHÔNG tích hợp provider thật.
13. Environment config: `.env.example` (không secret thật), typed validation.

# 8. Anti-patterns (phải tránh)

- Không business CRUD sample.
- Không hard-code SLA/permission/metric formula.
- Không chỉnh canonical documents để khớp implementation sai.
- Không bỏ assertion làm test pass giả.
- Không disable security check.
- Không thêm dependency ngoài Toolchain Lock.

# 9. Implementation steps

1. Git init/verify state; kiểm tra không có code ngoài phạm vi.
2. Tạo top-level structure + governance files (.gitignore, .editorconfig).
3. Backend shell (config, factory, health, logging, error boundary, OpenAPI).
4. Alembic baseline + migration harness.
5. Worker/scheduler shell + smoke task.
6. Frontend shell + generated client boundary.
7. Infrastructure compose + health checks + safe credentials.
8. Contracts bootstrap (openapi/events/asyncapi + validation).
9. scripts/dev.py + quality orchestration.
10. CI pipeline.
11. AI abstraction foundation (ports, registries schemas, Mock Adapter).
12. Tests (unit, integration foundation, architecture, contract, health, migration).
13. Documentation runtime artifacts (implementation-notes, evidence).
14. Secret scan + full check + report.

# 10. Tests required

- Unit tests (backend shell, config, error boundary)
- Integration test foundation (DB connectivity, migration)
- Architecture tests (dependency/context boundaries, anti-pattern negative tests)
- Contract validation (OpenAPI/AsyncAPI/JSON Schema)
- Health/liveness/readiness tests (healthy/unhealthy/degraded, graceful shutdown)
- Migration test (upgrade/downgrade/re-upgrade)
- Frontend type/lint/test/build
- Secret scan
- AI Mock adapter conformance test (theo contracts/ai/provider-conformance)

# 11. Commands

```text
python scripts/dev.py setup
python scripts/dev.py up
python scripts/dev.py migrate
python scripts/dev.py check
python scripts/dev.py test
python scripts/dev.py openapi
python scripts/dev.py events
python scripts/dev.py architecture-check
python scripts/dev.py smoke
```

# 12. Acceptance criteria

- [ ] Clean checkout install từ lockfiles thành công.
- [ ] Runtime version pins committed.
- [ ] Local PostgreSQL/RabbitMQ/Valkey/Object Storage healthy.
- [ ] Backend/frontend/worker start/stop graceful.
- [ ] Liveness/readiness tests PASS.
- [ ] Alembic clean upgrade/downgrade/re-upgrade PASS.
- [ ] OpenAPI 3.1 + AsyncAPI/JSON Schema validation PASS.
- [ ] Backend lint/type/unit/architecture PASS.
- [ ] Frontend lint/type/test/build PASS.
- [ ] Secret/dependency/container scans PASS hoặc approved exceptions.
- [ ] CI từ clean checkout green.
- [ ] Không có business aggregate/table/endpoint/Event nào được tạo.
- [ ] AI abstraction không phụ thuộc provider thật; Mock Adapter conformance PASS.
- [ ] implementation-notes.md + evidence/ cập nhật đầy đủ.

# 13. Evidence required

- Commands executed + exit codes.
- Tests passed/failed (chính xác).
- Files created/modified.
- Migration status.
- Build status.
- Contract validation status.
- Secret scan results.
- Git diff summary + commit hash.

# 14. Rollback notes

- Mỗi thành phần tạo commit riêng, revert được độc lập.
- Không force-push/rewrite history.
- Backup trước khi xóa bất kỳ file nào ngoài phạm vi (nếu có).

# 15. Out-of-scope

- Mọi business Context (Lead, Party, Product, Transaction, Contract, Revenue, …)
- Authentication/authorization implementation thật
- AI provider production integration
- Sprint 2 reliability contracts
- Deployment production
