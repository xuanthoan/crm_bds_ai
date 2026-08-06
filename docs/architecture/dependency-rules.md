# CRM_BDS_AI — DEPENDENCY RULES

**Document ID:** `ARCH-DEP-001`  
**Canonical path:** `docs/architecture/dependency-rules.md`  
**Product:** `crm_bds_ai`  
**Version:** `1.0.0`  
**Status:** `Ready for Review`  
**Owner:** `Architecture Owner`  
**Reviewers:** `Product Owner, Technical Owner, Security Owner, QA Owner`  
**Last reviewed:** `2026-08-05`  
**Classification:** `INTERNAL`


# 1. Mục tiêu

Ngăn Modular Monolith trở thành distributed monolith trong cùng process.

# 2. Layer direction

```text
presentation → application → domain
infrastructure → application/domain ports
```

- Domain không phụ thuộc FastAPI, SQLAlchemy, broker, filesystem hoặc provider SDK.
- Application điều phối use case và transaction port.
- Infrastructure triển khai repositories, outbox, provider adapters.
- Presentation chỉ map protocol ↔ application contract.

# 3. Context direction

- Không import `other_context.infrastructure` hoặc ORM model.
- Không gọi repository Context khác.
- Không join trực tiếp schema khác trong command path.
- Read model xuyên Context chỉ qua approved analytical/read contract.
- Shared package chỉ chứa technical primitives; không chứa business aggregate.

# 4. Package baseline

```text
backend/src/crm_bds_ai/contexts/<context>/
├── domain/
├── application/
├── infrastructure/
└── presentation/
```

# 5. Allowed dependencies

| From | To | Allowed |
|---|---|---|
| presentation | application DTO/ports | Yes |
| application | own domain | Yes |
| infrastructure | own application/domain ports | Yes |
| context A application | context B published client | Yes |
| context A | context B ORM/repository | No |
| domain | framework/provider | No |
| analytics projection | approved source event/read contract | Yes |

# 6. Enforcement

CI architecture tests phải kiểm tra import graph, schema ownership, route ownership và forbidden packages.

# 7. Exceptions

Chỉ Accepted ADR mới cho phép exception, phải có expiry, owner và removal plan.
