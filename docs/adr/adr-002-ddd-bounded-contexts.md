# ADR-002: DDD Bounded Contexts

**Document ID:** `ADR-002`  
**Canonical path:** `docs/adr/adr-002-ddd-bounded-contexts.md`  
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

Sử dụng 16 Bounded Contexts và language/ownership riêng.

# Rationale

Ngăn mô hình dữ liệu toàn cục và ambiguous ownership.

# Consequences

Context boundary phải được architecture tests enforce.

# Compliance

- Context Pack, code, tests và machine contracts phải tuân ADR này.
- Exception cần ADR mới hoặc waiver có owner/expiry.

# Supersedes

Không.
