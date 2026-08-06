# ADR-015: Immutable Receipt and Signed Records

**Document ID:** `ADR-015`  
**Canonical path:** `docs/adr/adr-015-immutable-receipt-and-signed-records.md`  
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

Issued Receipt và signed Contract/Document versions không sửa tại chỗ.

# Rationale

Legal/financial traceability.

# Consequences

Correction bằng reversal/cancellation/replacement.

# Compliance

- Context Pack, code, tests và machine contracts phải tuân ADR này.
- Exception cần ADR mới hoặc waiver có owner/expiry.

# Supersedes

Không.
