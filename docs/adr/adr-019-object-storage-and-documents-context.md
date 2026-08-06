# ADR-019: Object Storage and Documents Context

**Document ID:** `ADR-019`  
**Canonical path:** `docs/adr/adr-019-object-storage-and-documents-context.md`  
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

Binary files trong object storage; Documents sở hữu metadata/version/evidence.

# Rationale

Không lưu binary/URL tùy tiện trong business tables.

# Consequences

Short-lived access, scan, retention, legal hold.

# Compliance

- Context Pack, code, tests và machine contracts phải tuân ADR này.
- Exception cần ADR mới hoặc waiver có owner/expiry.

# Supersedes

Không.
