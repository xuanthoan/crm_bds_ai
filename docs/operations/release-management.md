# CRM_BDS_AI — RELEASE MANAGEMENT

**Document ID:** `OPS-REL-001`  
**Canonical path:** `docs/operations/release-management.md`  
**Product:** `crm_bds_ai`  
**Version:** `1.0.0`  
**Status:** `Ready for Review / Foundation Baseline`  
**Owner:** `Operations Owner`  
**Effective date:** `2026-08-05`  
**Last reviewed:** `2026-08-05`  
**Classification:** `INTERNAL`

---

# 1. Release record

Commit SHA, artifacts/images, lockfiles, migration head, OpenAPI/Event versions, configuration versions, approvals, rollout plan, rollback plan và evidence.

# 2. Gates

CI green, security checks, migration rehearsal, backup/restore readiness, SLO capacity, UAT, data reconciliation and runbooks.

# 3. Rollout

Pre-deploy checks → expand migrations → deploy compatible app → verify health/metrics/contracts → migrate/backfill → contract later.

# 4. Hypercare

Defined owner, duration, dashboards, alert thresholds, rollback criteria and issue triage.
