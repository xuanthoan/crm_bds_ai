# CRM_BDS_AI — REPOSITORY BOOTSTRAP BLUEPRINT

**Document ID:** `IMPL-BOOT-001`  
**Canonical path:** `docs/implementation/repository-bootstrap-blueprint.md`  
**Product:** `crm_bds_ai`  
**Version:** `1.0.0`  
**Status:** `Ready for Review / Foundation Baseline`  
**Owner:** `Engineering Owner`  
**Effective date:** `2026-08-05`  
**Last reviewed:** `2026-08-05`  
**Classification:** `INTERNAL`

---

# 1. Goal

Tạo repository reproducible, chạy được local, có CI, health, migration/contract bootstrap và architecture guardrails nhưng chưa có business feature.

# 2. Top-level target

```text
crm_bds_ai/
├── README.md
├── .skills/
├── .agent/
├── backend/
├── frontend/
├── contracts/
├── infrastructure/
├── scripts/
├── tests/
└── docs/
```

# 3. Backend shell

- Typed configuration.
- Application factory/composition root.
- Liveness/readiness.
- Structured logging/correlation.
- Problem Details error boundary.
- OpenAPI generation.
- Worker/scheduler bootstrap.
- Test harness.

# 4. Frontend shell

- Next.js application bootstrap.
- Typed environment.
- Generated API client boundary.
- Design-system foundation.
- Error/loading/not-found/access-denied states.
- Unit/component/E2E foundation.

# 5. Infrastructure

Local Compose-equivalent stack: PostgreSQL, RabbitMQ, Valkey, S3-compatible storage, backend, worker, frontend. Health checks và safe local credentials bắt buộc.

# 6. Acceptance

Clean checkout install, local start, backend/frontend/worker health, migration bootstrap, OpenAPI/AsyncAPI validation, lint/type/test/build và secret scan phải PASS.
