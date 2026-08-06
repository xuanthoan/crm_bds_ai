# ADR-006: REST and OpenAPI 3.1

**Document ID:** `ADR-006`  
**Canonical path:** `docs/adr/adr-006-rest-and-openapi-3-1.md`  
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

Synchronous public/internal APIs dùng REST với OpenAPI 3.1 canonical.

# Rationale

Typed contract và client generation.

# Consequences

Drift check trong CI.

# Compliance

- Context Pack, code, tests và machine contracts phải tuân ADR này.
- Exception cần ADR mới hoặc waiver có owner/expiry.

# Supersedes

Không.
