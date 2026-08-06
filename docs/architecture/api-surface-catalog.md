# CRM_BDS_AI — API SURFACE CATALOG

**Document ID:** `ARCH-API-CAT-001`  
**Canonical path:** `docs/architecture/api-surface-catalog.md`  
**Product:** `crm_bds_ai`  
**Version:** `1.0.0`  
**Status:** `Ready for Review / Foundation Baseline`  
**Owner:** `Architecture Owner`  
**Effective date:** `2026-08-05`  
**Last reviewed:** `2026-08-05`  
**Classification:** `INTERNAL`

---

# 1. Phạm vi

Catalog này liệt kê capability-level operations, không phải OpenAPI exact.

# 2. Public application groups

| Context | Operation groups |
|---|---|
| `platform` | enterprise, legal entities, calendars, configurations, workflows, approvals, numbering |
| `iam` | session/me, workforce, organizations, roles, grants, delegation, access explanation |
| `party` | parties, customers, phones, requirements, financial profiles, consent, duplicate search, merge |
| `lead` | intake, queues, assignments, protection, qualification, conversion |
| `product` | projects, assets, ownership, selling rights, listings, prices, availability, locks |
| `matching` | profiles, runs, results, shortlist, feedback, reverse matching |
| `transaction` | deals, cases, proposals, negotiation, hold, booking, deposit commitment |
| `contract` | contracts, plans, receivables, payments, allocations, receipts, refunds, settlements |
| `revenue` | arrangements, entitlements, receivables, commission, payout, clawback |
| `activity` | tasks, appointments, calls, interactions, timeline, SLA, NBA |
| `marketing` | campaigns, captures, audiences, journeys, attribution, spend |
| `analytics` | semantic query, dashboards, reports, snapshots, forecasts, DQ |
| `documents` | upload intent, documents, dossiers, signature, evidence, legal hold |
| `audit` | governed audit search and integrity evidence |
| `integration` | connections, mappings, sync, webhooks, DLQ, reconciliation |
| `operations` | health, jobs, incidents, releases, backups, restore, repair, support |

# 3. Exact contract gate

Mỗi operation trước code phải có OpenAPI path/method, schemas, Problem Details, auth metadata, idempotency, concurrency precondition, audit classification và contract tests.
