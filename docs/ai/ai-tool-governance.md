# CRM_BDS_AI — AI TOOL GOVERNANCE

**Document ID:** `AI-TOL-001`  
**Canonical path:** `docs/ai/ai-tool-governance.md`  
**Product:** `crm_bds_ai`  
**Version:** `1.0.0`  
**Status:** `Accepted / Foundation Baseline`  
**Owner:** `AI Architecture Owner`  
**Effective date:** `2026-08-05`  
**Last reviewed:** `2026-08-05`  
**Classification:** `INTERNAL`

---

# 1. Tool modes

`READ_ONLY`, `DRAFT_ONLY`, `APPROVAL_REQUIRED_COMMAND`; no unrestricted SQL, repository, shell or permission-granting tools.

# 2. Tool Guard

Every call must validate principal, permission, effective scope, input schema, purpose, rate/loop limit, idempotency and Context business preconditions.

# 3. High-impact prohibited defaults

No default tools for merge customer, force release lock, confirm payment, issue receipt, approve commission, execute payout/refund, grant permission, delete evidence or production data repair.
