# CRM_BDS_AI — CUSTOMER VISIBILITY POLICY

**Document ID:** `SEC-CUST-VIS-001`  
**Canonical path:** `docs/security/customer-visibility-policy.md`  
**Product:** `crm_bds_ai`  
**Version:** `1.0.0`  
**Status:** `Ready for Review / Foundation Baseline`  
**Owner:** `Security Owner`  
**Effective date:** `2026-08-05`  
**Last reviewed:** `2026-08-05`  
**Classification:** `INTERNAL`

---

# 1. Baseline

Customer identity thuộc enterprise, nhưng visibility dựa trên effective responsibility, organization scope, purpose và field policy.

| Persona | Baseline scope |
|---|---|
| Sale | Lead/Customer do mình phụ trách hoặc được grant |
| Team Lead | Team effective scope |
| Sales Manager | Department effective scope |
| Director | Enterprise scope theo grant |
| Accounting | Financial-purpose scope; không mặc định mở toàn bộ care notes |
| System Administrator | Technical administration; không blanket business-data access |

# 2. Customer merge

Merge không mở rộng visibility. Access được tính lại theo canonical Customer và source-resource policies.

# 3. Field controls

Phone, identity, financial profile, bank, documents, commission và sensitive notes có permission/masking độc lập.
