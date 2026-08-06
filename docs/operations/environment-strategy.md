# CRM_BDS_AI — ENVIRONMENT STRATEGY

**Document ID:** `OPS-ENV-001`  
**Canonical path:** `docs/operations/environment-strategy.md`  
**Product:** `crm_bds_ai`  
**Version:** `1.0.0`  
**Status:** `Ready for Review / Foundation Baseline`  
**Owner:** `Operations Owner`  
**Effective date:** `2026-08-05`  
**Last reviewed:** `2026-08-05`  
**Classification:** `INTERNAL`

---

# 1. Environments

`local`, `test`, `ci`, `staging`, `production` có isolated data, credentials, provider connections và deployment history.

# 2. Promotion

Artifact build một lần và promote; configuration/secret khác nhau theo environment; migration compatibility checked trước rollout.

# 3. Data

Không copy raw production PII sang lower environments. Test fixtures synthetic hoặc sanitized theo approved process.

# 4. Access

Production access least privilege, time-bound khi phù hợp, MFA, Audit và break-glass only for emergency.
