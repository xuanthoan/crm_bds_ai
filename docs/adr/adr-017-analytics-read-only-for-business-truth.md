# ADR-017: Analytics Read-only for Business Truth

**Document ID:** `ADR-017`  
**Canonical path:** `docs/adr/adr-017-analytics-read-only-for-business-truth.md`  
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

Analytics sở hữu projection/metric/snapshot/forecast, không source aggregate.

# Rationale

Ngăn báo cáo trở thành master.

# Consequences

Correction qua owning Context.

# Compliance

- Context Pack, code, tests và machine contracts phải tuân ADR này.
- Exception cần ADR mới hoặc waiver có owner/expiry.

# Supersedes

Không.
