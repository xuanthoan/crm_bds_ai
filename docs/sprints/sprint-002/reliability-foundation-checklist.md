# CRM_BDS_AI — SPRINT 2 RELIABILITY FOUNDATION CHECKLIST

**Document ID:** `SPRINT-002-CHECK-001`  
**Canonical path:** `docs/sprints/sprint-002/reliability-foundation-checklist.md`  
**Product:** `crm_bds_ai`  
**Version:** `1.0.0`  
**Status:** `Planned / Not Active`  
**Owner:** `Engineering Owner`  
**Effective date:** `2026-08-05`  
**Last reviewed:** `2026-08-05`  
**Classification:** `INTERNAL`

---

- [ ] Context schema bootstrap and `infra` technical schema reviewed.
- [ ] Outbox atomic write/publish implemented.
- [ ] Inbox deduplication implemented.
- [ ] Idempotency key lifecycle implemented.
- [ ] Event dispatcher retry/DLQ/replay safe.
- [ ] Append-only Audit foundation implemented.
- [ ] Correlation/causation propagation verified.
- [ ] PostgreSQL/RabbitMQ integration and failure-injection tests pass.
- [ ] Reconciliation/health endpoints documented and secured.
