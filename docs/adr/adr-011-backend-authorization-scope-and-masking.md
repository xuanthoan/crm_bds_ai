# ADR-011: Backend Authorization Scope and Masking

**Document ID:** `ADR-011`  
**Canonical path:** `docs/adr/adr-011-backend-authorization-scope-and-masking.md`  
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

Security decisions nằm ở backend.

# Rationale

Frontend không trusted.

# Consequences

Permission ∩ scope ∩ resource ∩ field ∩ SoD.

# Compliance

- Context Pack, code, tests và machine contracts phải tuân ADR này.
- Exception cần ADR mới hoặc waiver có owner/expiry.

# Supersedes

Không.
