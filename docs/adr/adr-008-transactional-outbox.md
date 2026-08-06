# ADR-008: Transactional Outbox

**Document ID:** `ADR-008`  
**Canonical path:** `docs/adr/adr-008-transactional-outbox.md`  
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

Domain/application transaction ghi Outbox cùng local state.

# Rationale

Không mất event sau commit.

# Consequences

Dispatcher retry, monitoring, idempotency.

# Compliance

- Context Pack, code, tests và machine contracts phải tuân ADR này.
- Exception cần ADR mới hoặc waiver có owner/expiry.

# Supersedes

Không.
