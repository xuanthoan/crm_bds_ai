# ADR-016: Contract Cash Separate from Revenue and Commission

**Document ID:** `ADR-016`  
**Canonical path:** `docs/adr/adr-016-contract-cash-separate-from-revenue-and-commission.md`  
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

Payment/Receipt/Settlement thuộc Contract; Revenue/Commission thuộc Revenue.

# Rationale

Không nhầm gross funds với revenue.

# Consequences

Revenue dùng accepted cash facts.

# Compliance

- Context Pack, code, tests và machine contracts phải tuân ADR này.
- Exception cần ADR mới hoặc waiver có owner/expiry.

# Supersedes

Không.
