# CRM_BDS_AI — AI PROVIDER OR MODEL OUTAGE RUNBOOK

**Document ID:** `RUN-AI-001`  
**Canonical path:** `docs/runbooks/ai-provider-outage.md`  
**Product:** `crm_bds_ai`  
**Version:** `1.0.0`  
**Status:** `Accepted / Foundation Baseline`  
**Owner:** `Operations Owner`  
**Effective date:** `2026-08-05`  
**Last reviewed:** `2026-08-05`  
**Classification:** `INTERNAL`

---

Detect via health/error/latency alerts. Open circuit, stop new routes, preserve in-flight job state, evaluate policy-compliant alternatives, otherwise expose manual fallback. Never change classification boundary to recover availability. Record affected jobs and reprocess only idempotently.
