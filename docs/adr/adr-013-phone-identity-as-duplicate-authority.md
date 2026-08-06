# ADR-013: Phone Identity as Duplicate Authority

**Document ID:** `ADR-013`  
**Canonical path:** `docs/adr/adr-013-phone-identity-as-duplicate-authority.md`  
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

Duplicate Customer được xác định theo normalized phone identity; shared phone có governance.

# Rationale

Rule business đã chốt.

# Consequences

Không auto-merge theo tên/email/social/address.

# Compliance

- Context Pack, code, tests và machine contracts phải tuân ADR này.
- Exception cần ADR mới hoặc waiver có owner/expiry.

# Supersedes

Không.
