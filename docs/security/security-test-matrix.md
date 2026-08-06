# CRM_BDS_AI — SECURITY TEST MATRIX

**Document ID:** `SEC-TEST-001`  
**Canonical path:** `docs/security/security-test-matrix.md`  
**Product:** `crm_bds_ai`  
**Version:** `1.0.0`  
**Status:** `Ready for Review / Foundation Baseline`  
**Owner:** `Security Owner`  
**Effective date:** `2026-08-05`  
**Last reviewed:** `2026-08-05`  
**Classification:** `INTERNAL`

---

# 1. Test groups

- Authentication/session/OIDC failures.
- Permission allow/deny and access explanation.
- Scope escalation via query/path/body IDs.
- Cross-Legal-Entity/Project access.
- Field masking before serialization/cache/export.
- IDOR/BOLA.
- Maker-checker and SoD.
- Delegation expiry and acting role.
- Customer merge visibility.
- Export/download expiry.
- Webhook signature/replay.
- File upload malware/type/size.
- Secret/log redaction.
- Break-glass scope/expiry/Audit.

# 2. Evidence

Mỗi sensitive endpoint/command có positive, negative, boundary và regression cases. Security tests chạy backend-side; disabled UI không là control.
