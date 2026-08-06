# ADR-014: Product Owns Availability and Commercial Lock

**Document ID:** `ADR-014`  
**Canonical path:** `docs/adr/adr-014-product-owns-availability-and-commercial-lock.md`  
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

Product là authority cho availability/lock.

# Rationale

Ngăn double sell và UI status authority.

# Consequences

Transaction Hold chỉ orchestration/reference.

# Compliance

- Context Pack, code, tests và machine contracts phải tuân ADR này.
- Exception cần ADR mới hoặc waiver có owner/expiry.

# Supersedes

Không.
