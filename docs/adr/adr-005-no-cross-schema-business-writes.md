# ADR-005: No Cross-schema Business Writes

**Document ID:** `ADR-005`  
**Canonical path:** `docs/adr/adr-005-no-cross-schema-business-writes.md`  
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

Một transaction chỉ ghi schema owner và local outbox.

# Rationale

Bảo vệ invariants/ownership.

# Consequences

Cross-context dùng command/event/process manager.

# Compliance

- Context Pack, code, tests và machine contracts phải tuân ADR này.
- Exception cần ADR mới hoặc waiver có owner/expiry.

# Supersedes

Không.
