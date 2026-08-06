# CRM_BDS_AI — RUNBOOK — LOCAL DEVELOPMENT

**Document ID:** `RUN-LOCAL-001`  
**Canonical path:** `docs/runbooks/local-development.md`  
**Product:** `crm_bds_ai`  
**Version:** `1.0.0`  
**Status:** `Ready for Review / Foundation Baseline`  
**Owner:** `Engineering Owner`  
**Effective date:** `2026-08-05`  
**Last reviewed:** `2026-08-05`  
**Classification:** `INTERNAL`

---

# Procedure

1. Validate supported runtime versions.
2. Install from lockfiles.
3. Create local env from example; never use production secrets.
4. Start stateful dependencies.
5. Run migrations.
6. Start API, worker and frontend.
7. Run readiness and smoke checks.
8. Run full `check` before commit.

# Troubleshooting

- Port conflict: identify process; do not change canonical ports silently.
- Migration mismatch: inspect head/current; do not delete volume before understanding.
- Broker/storage unavailable: use health logs and runbook; do not bypass readiness.
- Lock drift: regenerate only through approved dependency workflow.
