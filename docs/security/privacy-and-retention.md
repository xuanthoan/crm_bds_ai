# CRM_BDS_AI — PRIVACY AND RETENTION

**Document ID:** `SEC-PRI-001`  
**Canonical path:** `docs/security/privacy-and-retention.md`  
**Product:** `crm_bds_ai`  
**Version:** `1.0.0`  
**Status:** `Ready for Review`  
**Owner:** `Data Governance Owner`  
**Reviewers:** `Security Owner, Legal Owner, Documents Owner, Operations Owner`  
**Last reviewed:** `2026-08-05`  
**Classification:** `INTERNAL`


# Principles

Purpose limitation, data minimization, accuracy, access control, retention limitation, accountability và Legal Hold.

# Data lifecycle

```text
collect → classify → use by purpose → restrict/mask → retain → archive/delete → evidence
```

# Retention rules

- Exact periods thuộc versioned Retention Policy theo jurisdiction/business need.
- Legal Hold chặn deletion.
- Deletion phải xử lý source, projections, caches, exports và provider copies theo contract.
- Audit giữ deletion evidence mà không giữ raw data không cần thiết.

# Data subject/Customer operations

Access, correction, restriction, consent withdrawal, export hoặc deletion request phải đi qua governed workflow, identity verification và legal exceptions.

# Historical analytics

Ưu tiên aggregation/anonymization; không giữ direct identifiers nếu không cần.
