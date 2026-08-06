# CRM_BDS_AI — RUNBOOK — RELEASE AND ROLLBACK

**Document ID:** `RUN-REL-001`  
**Canonical path:** `docs/runbooks/release-and-rollback.md`  
**Product:** `crm_bds_ai`  
**Version:** `1.0.0`  
**Status:** `Ready for Review / Foundation Baseline`  
**Owner:** `Operations Owner`  
**Effective date:** `2026-08-05`  
**Last reviewed:** `2026-08-05`  
**Classification:** `INTERNAL`

---

# Release

Verify approvals, immutable artifacts, migration plan, backup, provider readiness and dashboards. Execute rollout in ordered stages, record timestamps and evidence.

# Validation

Health, error/latency, consumer lag, database, critical smoke journeys, data reconciliation and security checks.

# Rollback

Trigger only on defined conditions. Roll back application only when schema compatibility permits. Never destructive-downgrade financial/legal data without explicit plan. Record incident and reconcile side effects.
