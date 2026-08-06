# CRM_BDS_AI — RUNBOOK — QUEUE BACKLOG

**Document ID:** `RUN-QUEUE-001`  
**Canonical path:** `docs/runbooks/queue-backlog.md`  
**Product:** `crm_bds_ai`  
**Version:** `1.0.0`  
**Status:** `Ready for Review / Foundation Baseline`  
**Owner:** `Operations Owner`  
**Effective date:** `2026-08-05`  
**Last reviewed:** `2026-08-05`  
**Classification:** `INTERNAL`

---

# Detection

Queue depth/age, consumer health, retry rate, DLQ growth, database latency and provider failures.

# Response

Identify poison messages and systemic cause; do not blindly scale/replay. Pause affected routing if side-effect risk; fix consumer; test idempotency; drain in bounded batches; monitor and reconcile.

# Evidence

Affected queues, oldest age, event IDs, consumer version, retries, DLQ actions, business impact and final reconciliation.
