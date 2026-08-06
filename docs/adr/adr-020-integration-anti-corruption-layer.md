# ADR-020: Integration Anti-Corruption Layer

**Document ID:** `ADR-020`  
**Canonical path:** `docs/adr/adr-020-integration-anti-corruption-layer.md`  
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

Provider models/transport nằm trong Integration Context.

# Rationale

Bảo vệ domain khỏi provider coupling.

# Consequences

Secret reference, mapping version, replay/reconciliation.

# Compliance

- Context Pack, code, tests và machine contracts phải tuân ADR này.
- Exception cần ADR mới hoặc waiver có owner/expiry.

# Supersedes

Không.
