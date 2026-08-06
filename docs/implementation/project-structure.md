# CRM_BDS_AI — PROJECT STRUCTURE

**Document ID:** `IMPL-STRUCT-001`  
**Canonical path:** `docs/implementation/project-structure.md`  
**Product:** `crm_bds_ai`  
**Version:** `1.0.0`  
**Status:** `Ready for Review / Foundation Baseline`  
**Owner:** `Engineering Owner`  
**Effective date:** `2026-08-05`  
**Last reviewed:** `2026-08-05`  
**Classification:** `INTERNAL`

---

# 1. Backend direction

```text
backend/
├── pyproject.toml
├── uv.lock
├── migrations/
├── src/crm_bds_ai/
│   ├── bootstrap/
│   ├── shared_kernel/
│   ├── infra/
│   └── contexts/
└── tests/
```

Context code khi được kích hoạt:

```text
contexts/<context>/
├── domain/
├── application/
├── infrastructure/
└── presentation/
```

`shared_kernel` chỉ nhận primitive/value abstractions được Architecture review; không chứa Customer, Lead, Product hoặc financial business logic.

# 2. Frontend direction

```text
frontend/
├── app/
├── features/
├── components/
├── design-system/
├── generated/
├── lib/
└── tests/
```

Feature code không định nghĩa API types cạnh tranh với generated OpenAPI client.

# 3. Contracts

```text
contracts/openapi/
contracts/events/
contracts/asyncapi/
contracts/security/
```

# 4. Infrastructure

```text
infrastructure/compose/
infrastructure/docker/
infrastructure/environments/
infrastructure/observability/
```

Exact tree được khóa trong Sprint 1 implementation notes; không tạo 16 package rỗng để trang trí.
