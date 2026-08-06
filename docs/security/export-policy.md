# CRM_BDS_AI — DATA EXPORT POLICY

**Document ID:** `SEC-EXPORT-001`  
**Canonical path:** `docs/security/export-policy.md`  
**Product:** `crm_bds_ai`  
**Version:** `1.0.0`  
**Status:** `Ready for Review / Foundation Baseline`  
**Owner:** `Security Owner`  
**Effective date:** `2026-08-05`  
**Last reviewed:** `2026-08-05`  
**Classification:** `INTERNAL`

---

# 1. Rule

Export là permission riêng, không suy ra từ view/detail access.

# 2. Business baseline

- Sale, Team Lead và Sales Manager không export customer, project hoặc property datasets.
- Director và Accounting chỉ export khi có explicit permission, purpose, scope, masking và Audit.
- Export financial/identity/document data có thể cần approval và Segregation of Duties.

# 3. Controls

Backend scope resolution; field masking trước file generation; row/field count; watermark; expiry; encrypted storage; one-time/controlled download; recipient restrictions; Audit; retention/deletion.

# 4. Artifacts

Analytics/owning Context tạo export job intent; Documents sở hữu generated artifact; Integration sở hữu external delivery nếu có.
