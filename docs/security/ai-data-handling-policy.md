# CRM_BDS_AI — AI DATA HANDLING POLICY

**Document ID:** `SEC-AI-001`  
**Canonical path:** `docs/security/ai-data-handling-policy.md`  
**Product:** `crm_bds_ai`  
**Version:** `1.0.0`  
**Status:** `Accepted / Foundation Baseline`  
**Owner:** `Security Owner`  
**Effective date:** `2026-08-05`  
**Last reviewed:** `2026-08-05`  
**Classification:** `INTERNAL`

---

# 1. Data minimization

Only fields required by the use case are included. Restricted identifiers are masked/redacted unless an approved local/private route and purpose require them.

# 2. Classification routing

Provider profiles declare allowed classifications and deployment. Routing cannot downgrade classification or bypass Legal Entity policy.

# 3. Retention

Prompt/response content retention is use-case specific; default telemetry stores hashes/references. Provider-side retention and training use require approved terms.
