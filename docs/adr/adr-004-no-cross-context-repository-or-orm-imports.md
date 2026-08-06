# ADR-004: No Cross-context Repository or ORM Imports

**Document ID:** `ADR-004`  
**Canonical path:** `docs/adr/adr-004-no-cross-context-repository-or-orm-imports.md`  
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

Context chỉ dùng published client/contracts của Context khác.

# Rationale

Ngăn hidden coupling.

# Consequences

CI import rules bắt buộc.

# Compliance

- Context Pack, code, tests và machine contracts phải tuân ADR này.
- Exception cần ADR mới hoặc waiver có owner/expiry.

# Supersedes

Không.
