# ADR-001: Modular Monolith First

**Document ID:** `ADR-001`  
**Canonical path:** `docs/adr/adr-001-modular-monolith-first.md`  
**Product:** `crm_bds_ai`  
**Version:** `1.0.0`  
**Status:** `Accepted`  
**Owner:** `Architecture Owner`  
**Reviewers:** `Product Owner, Technical Owner, Domain Owners`  
**Last reviewed:** `2026-08-05`  
**Classification:** `INTERNAL`


# Context

Greenfield `crm_bds_ai` cần một quyết định nền tảng nhất quán cho mọi Sprint và AI Agent.

# Decision

Triển khai một deployable modular monolith trước; không tách microservice khi chưa có evidence.

# Rationale

Giảm distributed complexity, giữ Context boundaries bằng code/tests.

# Consequences

Tách service cần ADR mới và operational readiness.

# Compliance

- Context Pack, code, tests và machine contracts phải tuân ADR này.
- Exception cần ADR mới hoặc waiver có owner/expiry.

# Supersedes

Không.
