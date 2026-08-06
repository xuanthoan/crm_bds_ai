# ADR-007: JSON Schema and AsyncAPI Events

**Document ID:** `ADR-007`  
**Canonical path:** `docs/adr/adr-007-json-schema-and-asyncapi-events.md`  
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

Durable events dùng JSON Schema 2020-12 và AsyncAPI.

# Rationale

Versioned published language.

# Consequences

PII minimization và compatibility tests.

# Compliance

- Context Pack, code, tests và machine contracts phải tuân ADR này.
- Exception cần ADR mới hoặc waiver có owner/expiry.

# Supersedes

Không.
