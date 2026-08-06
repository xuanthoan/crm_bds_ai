# CRM_BDS_AI — REPOSITORY BOOTSTRAP ACCEPTANCE CHECKLIST

**Document ID:** `IMPL-BOOT-ACC-001`  
**Canonical path:** `docs/implementation/bootstrap-acceptance-checklist.md`  
**Product:** `crm_bds_ai`  
**Version:** `1.0.0`  
**Status:** `Ready for Review / Foundation Baseline`  
**Owner:** `QA Owner`  
**Effective date:** `2026-08-05`  
**Last reviewed:** `2026-08-05`  
**Classification:** `INTERNAL`

---

# Acceptance checklist

- [ ] Sprint 0 PASS và Sprint 1 ACTIVE.
- [ ] Clean clone/install works from lockfiles.
- [ ] Runtime version pins committed.
- [ ] Local PostgreSQL/RabbitMQ/Valkey/Object Storage healthy.
- [ ] API, worker và frontend start/stop gracefully.
- [ ] Liveness/readiness tests pass.
- [ ] Alembic clean upgrade/downgrade/re-upgrade pass.
- [ ] OpenAPI 3.1 and AsyncAPI/JSON Schema validation pass.
- [ ] Backend lint/type/unit/architecture pass.
- [ ] Frontend lint/type/test/build pass.
- [ ] Secret/dependency/container scans pass or approved exceptions exist.
- [ ] CI from clean checkout green.
- [ ] No business aggregate/table/endpoint/Event implemented early.
- [ ] Project Status, Handoff, implementation notes and Acceptance Report updated.
