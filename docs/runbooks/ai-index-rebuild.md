# CRM_BDS_AI — AI VECTOR INDEX REBUILD RUNBOOK

**Document ID:** `RUN-AI-005`  
**Canonical path:** `docs/runbooks/ai-index-rebuild.md`  
**Product:** `crm_bds_ai`  
**Version:** `1.0.0`  
**Status:** `Accepted / Foundation Baseline`  
**Owner:** `Operations Owner`  
**Effective date:** `2026-08-05`  
**Last reviewed:** `2026-08-05`  
**Classification:** `INTERNAL`

---

Create new index version, validate source scope/version/classification, re-embed with fixed profile, run retrieval evaluation and cross-scope leakage tests, shadow/dual-read, switch feature flag, monitor and retain rollback window. Never mutate the active index in place.
