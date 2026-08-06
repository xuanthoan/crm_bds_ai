# CRM_BDS_AI — SPRINT ROADMAP

## Sequencing, dependency gates and Just-in-Time execution-pack policy

**Document ID:** `ROADMAP-SPRINT-001`  
**Canonical path:** `docs/roadmap/sprint-roadmap.md`  
**Product:** `crm_bds_ai`  
**Version:** `1.0.0`  
**Status:** `Accepted / Planning Baseline`  
**Canonical scope:** Sprint sequence, high-level outcomes, ownership and readiness status  
**Owner:** `Product Owner`  
**Co-owner:** `Architecture Owner`  
**Reviewers:** `Engineering Owner`, `Domain Owners`, `Security Owner`, `QA Owner`, `Operations Owner`  
**Effective date:** `2026-08-05`  
**Supersedes:** `None — Greenfield baseline`  
**Classification:** `INTERNAL`

---

# 1. Mục đích

Roadmap này giữ định hướng triển khai từ Sprint 0 đến Sprint 57 mà không biến các Sprint tương lai thành exact implementation contracts được phê duyệt quá sớm.

Roadmap là nguồn chuẩn cho:

- Sprint number.
- High-level goal.
- Primary ownership.
- Broad dependency/readiness gate.
- Current planning status.

Roadmap không phải nguồn chuẩn cho:

- Exact aggregate/state machine.
- Exact table/column/index.
- Exact endpoint/payload.
- Exact Event name/payload.
- Exact permission/error.
- Exact UI route/layout/component.
- Exact job/queue/retry/timeout.
- Exact file plan/commit plan.
- Sprint completion.

Exact implementation chỉ được khóa trong JIT Context Pack, machine contracts và current Sprint Execution Pack.

---

# 2. Nguyên tắc không khóa sớm Sprint tương lai

Roadmap chỉ khóa sequence, high-level outcome, dependency gate và primary ownership. Sprint 4–57 không phải exact implementation contracts.

Lý do:

- Exact aggregate, schema, API, Event, permission và UI phải dựa trên Context Pack cùng machine contract mới nhất.
- Chỉ một Sprint được ACTIVE tại một thời điểm.
- Detailed Execution Pack phải được tạo Just-in-Time sau khi dependency Acceptance Reports PASS.
- Open decisions ảnh hưởng Sprint phải được đóng hoặc có waiver trước activation.
- Không sao chép giả định tương lai vào code chỉ vì chúng xuất hiện trong roadmap.

# 3. Status vocabulary

| Status | Meaning |
|---|---|
| `READY_FOR_REVIEW` | Gate hiện tại có thể được review, chưa PASS |
| `PLANNED_NOT_ACTIVE` | Có detailed pack nhưng chưa được kích hoạt |
| `ROADMAP_ONLY` | Chỉ có outcome/sequence; không được code từ roadmap |
| `ACTIVE` | Chỉ một Sprint có thể ở trạng thái này |
| `BLOCKED` | Không được triển khai cho tới khi blocker được giải quyết |
| `ACCEPTED` | Acceptance Report PASS và sign-off hoàn tất |
| `SUPERSEDED` | Không dùng triển khai |

Tại thời điểm phát hành file này:

```text
Sprint 0: READY_FOR_REVIEW
Sprint 1: PLANNED_NOT_ACTIVE
Sprint 2: PLANNED_NOT_ACTIVE
Sprint 3: PLANNED_NOT_ACTIVE
Sprint 4–57: ROADMAP_ONLY
Code implementation: NOT STARTED
```

---

# 4. Just-in-Time detailed-pack policy

A Sprint may receive an executable detailed pack only when:

1. Dependency Acceptance Reports pass.
2. Relevant Context Pack is accepted for the scope.
3. Product/Architecture open decisions that affect the Sprint are resolved.
4. Toolchain and standards required by the Sprint are ready.
5. Machine-contract owners are assigned.
6. Security/permission/masking implications are clear.
7. Test and operational evidence plan is clear.
8. The Sprint is the next active work, not speculative future design.

Detailed pack creation MUST include a conflict audit against current canonical sources. It must not copy the old master section unchanged.

---

# 5. Activation protocol

```text
Dependency PASS
→ Context readiness review
→ JIT Sprint Pack prepared/reviewed
→ Product/Technical activation approval
→ docs/sprints/README.md current pointer updated
→ exactly one Sprint becomes ACTIVE
→ Goose decomposes and delegates
→ Acceptance Report
→ next Sprint remains inactive until review
```

Roadmap order may change through approved change control; number/title alone does not create implementation authority.

---

# 6. Roadmap

## Phase 0 — Preparation and Engineering Foundation
| Sprint | Outcome | Primary ownership | Activation gate | Current status |
|---:|---|---|---|---|
| 000 | Documentation, Architecture and AI-Agent Readiness Gate | `Cross-cutting` | Current preparation gate | `READY_FOR_REVIEW` |
| 001 | Repository and Local Engineering Platform Foundation | `Engineering foundation` | Sprint 0 PASS | `PLANNED_NOT_ACTIVE` |
| 002 | Database, Outbox, Inbox, Idempotency, Event Dispatcher and Audit Foundation | `infra / audit / operations` | Sprint 0–1 PASS | `PLANNED_NOT_ACTIVE` |

## Phase 1 — Platform and IAM
| Sprint | Outcome | Primary ownership | Activation gate | Current status |
|---:|---|---|---|---|
| 003 | Enterprise, Legal Entity, Business Calendar and Numbering Foundation | `platform` | Sprint 0–2 PASS + Platform decisions | `PLANNED_NOT_ACTIVE` |
| 004 | Organization, Workforce, Position and Temporal Employment Assignment | `iam` | JIT pack + Sprint 3 PASS | `ROADMAP_ONLY` |
| 005 | OIDC Authentication, Permission Registry, Roles, Scope and Access Explanation | `iam` | JIT pack + Sprint 4 PASS | `ROADMAP_ONLY` |
| 006 | Configuration Registry, Workflow Engine, Approval Policy and Feature Flags | `platform / iam` | JIT pack + IAM prerequisites | `ROADMAP_ONLY` |

## Phase 2 — Party, Customer and Lead
| Sprint | Outcome | Primary ownership | Activation gate | Current status |
|---:|---|---|---|---|
| 007 | Party and Customer Foundation | `party` | JIT Party pack + Foundation PASS | `ROADMAP_ONLY` |
| 008 | Phone Identity, Shared Phone and Duplicate Prevention | `party` | JIT pack + Sprint 7 PASS | `ROADMAP_ONLY` |
| 009 | Customer Identity Resolution, Merge, Redirect and Reconciliation | `party / integration` | JIT pack + Sprint 8 PASS | `ROADMAP_ONLY` |
| 010 | Lead Intake, Raw Payload and Immutable Source Snapshot | `lead` | JIT Lead pack + Party capability | `ROADMAP_ONLY` |
| 011 | Lead Queue, Routing, Assignment, Collaboration and Care Protection | `lead / iam / activity` | JIT pack + Sprint 10 PASS | `ROADMAP_ONLY` |
| 012 | Lead Qualification, Scoring, Nurture, Closure and Conversion Saga | `lead / party` | JIT pack + Sprint 10–11 PASS | `ROADMAP_ONLY` |
| 013 | Customer Requirement, Criteria, Financial Profile and Customer 360 | `party` | JIT pack + Party/Lead prerequisites | `ROADMAP_ONLY` |

## Phase 3 — Product, Listing and Matching
| Sprint | Outcome | Primary ownership | Activation gate | Current status |
|---:|---|---|---|---|
| 014 | Partner, Project, Phase, Zone, Block, Floor and Project Access | `product` | JIT Product pack + Platform/IAM | `ROADMAP_ONLY` |
| 015 | Property Asset, Physical Identity, Ownership and Verification | `product / party` | JIT pack + Sprint 14 PASS | `ROADMAP_ONLY` |
| 016 | Property Listing, Mandate, Consignment and Listing Activation | `product` | JIT pack + Sprint 15 PASS | `ROADMAP_ONLY` |
| 017 | Price Versions, Inventory Lists, Availability and Commercial Lock | `product` | JIT pack + Sprint 16 PASS | `ROADMAP_ONLY` |
| 018 | Matching Rule Sets, Matching Runs, Scoring and Explanation | `matching` | JIT Matching pack + Product/Requirement | `ROADMAP_ONLY` |
| 019 | Shortlist, Customer Feedback, Product Comparison and Reverse Matching | `matching / party` | JIT pack + Sprint 18 PASS | `ROADMAP_ONLY` |

## Phase 4 — Deal and Transaction
| Sprint | Outcome | Primary ownership | Activation gate | Current status |
|---:|---|---|---|---|
| 020 | Deal Pipeline, Stage History, Responsibility and Health | `transaction` | JIT Transaction pack + upstream readiness | `ROADMAP_ONLY` |
| 021 | Transaction Case, Parties, Company Role, Payment Flow and Revenue Model | `transaction` | JIT pack + Sprint 20 PASS | `ROADMAP_ONLY` |
| 022 | Proposal Versions, Commercial Snapshot and Negotiation Rounds | `transaction` | JIT pack + Sprint 21 PASS | `ROADMAP_ONLY` |
| 023 | Hold Request, Commercial Lock Integration, Extension and Expiry | `transaction / product` | JIT pack + Product Lock + Sprint 22 | `ROADMAP_ONLY` |
| 024 | Booking, Multiple Buyers, Deposit Commitment and Dossier Gate | `transaction / documents` | JIT pack + Sprint 23 PASS | `ROADMAP_ONLY` |

## Phase 5 — Contract and Cash Operations
| Sprint | Outcome | Primary ownership | Activation gate | Current status |
|---:|---|---|---|---|
| 025 | Contract Foundation, Versions, Parties and Commercial Snapshot | `contract` | JIT Contract pack + Booking | `ROADMAP_ONLY` |
| 026 | Signature Envelope, Signing Evidence and Contract Effectiveness | `contract / documents / integration` | JIT pack + Sprint 25 PASS | `ROADMAP_ONLY` |
| 027 | Payment Schedule, Milestones, Buyer Receivables and Overdue | `contract / activity` | JIT pack + effective Contract | `ROADMAP_ONLY` |
| 028 | Payment Intake, Allocation, Unallocated Funds and Immutable Receipt | `contract` | JIT pack + Sprint 27 PASS | `ROADMAP_ONLY` |
| 029 | Refund, Owner Settlement and Contract Cancellation Compensation | `contract / transaction / revenue` | JIT pack + cash prerequisites | `ROADMAP_ONLY` |

## Phase 6 — Revenue and Commission
| Sprint | Outcome | Primary ownership | Activation gate | Current status |
|---:|---|---|---|---|
| 030 | Revenue Arrangement, Components and Entitlement | `revenue` | JIT Revenue pack + transaction/contract facts | `ROADMAP_ONLY` |
| 031 | Revenue Recognition, Revenue Receivable, Collection, Adjustment and Reversal | `revenue` | JIT pack + Sprint 30 PASS | `ROADMAP_ONLY` |
| 032 | Commission Plan, Participants, Entitlement, Vesting and Holdback | `revenue / iam` | JIT pack + revenue/organization | `ROADMAP_ONLY` |
| 033 | Commission Payable, Payout Batch, Payment, Advance, Negative Balance and Clawback | `revenue` | JIT pack + Sprint 32 PASS | `ROADMAP_ONLY` |

## Phase 7 — Activity and Engagement
| Sprint | Outcome | Primary ownership | Activation gate | Current status |
|---:|---|---|---|---|
| 034 | Task, Assignment, Checklist, Dependency, Recurrence and SLA Clock | `activity` | JIT Activity pack + Platform/IAM | `ROADMAP_ONLY` |
| 035 | Appointment, Participants, Attendance, Site Visit and Calendar Integration | `activity / integration` | JIT pack + Sprint 34 PASS | `ROADMAP_ONLY` |
| 036 | Call Logs, Omnichannel Interaction, Threads and Unified Timeline | `activity / integration` | JIT pack + Sprint 34–35 capability | `ROADMAP_ONLY` |
| 037 | Next Best Action Rule Engine, Gates, Explanation and Feedback | `activity / analytics` | JIT pack + trusted source facts | `ROADMAP_ONLY` |

## Phase 8 — Marketing
| Sprint | Outcome | Primary ownership | Activation gate | Current status |
|---:|---|---|---|---|
| 038 | Campaign, Source Taxonomy, UTM, Tracking URL and Channel Execution | `marketing` | JIT Marketing pack + Platform/Product | `ROADMAP_ONLY` |
| 039 | Forms, Submissions, Spam Control, Anonymous Visitor and Touchpoints | `marketing / lead` | JIT pack + Sprint 38 + Lead intake | `ROADMAP_ONLY` |
| 040 | Audience, Evaluation, Consent, Suppression and Frequency Caps | `marketing / party` | JIT pack + consent/privacy decisions | `ROADMAP_ONLY` |
| 041 | Journey Automation, Enrollment, Steps, Wait, Condition and Retry | `marketing / operations` | JIT pack + Sprint 40 PASS | `ROADMAP_ONLY` |
| 042 | Conversion Definitions, Attribution Models, Spend, Budget and ROI | `marketing / analytics` | JIT pack + source facts/metrics | `ROADMAP_ONLY` |

## Phase 9 — Analytics
| Sprint | Outcome | Primary ownership | Activation gate | Current status |
|---:|---|---|---|---|
| 043 | Analytics Projection Framework, Dataset Registry and Core Semantic Metrics | `analytics` | JIT Analytics pack + Event maturity | `ROADMAP_ONLY` |
| 044 | Financial, Commission and Marketing Semantic Metrics; Reconciliation and Certification | `analytics` | JIT pack + source Context maturity | `ROADMAP_ONLY` |
| 045 | Dashboard UI, Widgets, Filters, Scope-aware Cache, Drill-down and Export | `analytics / frontend` | JIT pack + certified metrics/design | `ROADMAP_ONLY` |
| 046 | Snapshots, Restatement, Targets, Scorecards and Forecast | `analytics` | JIT pack + Sprint 43–45 capability | `ROADMAP_ONLY` |

## Phase 10 — Documents, Audit, Integration and Operations
| Sprint | Outcome | Primary ownership | Activation gate | Current status |
|---:|---|---|---|---|
| 047 | File Object, Document, Version, Malware Scan and Secure Download | `documents` | JIT Documents pack + storage/security | `ROADMAP_ONLY` |
| 048 | Electronic Dossier, Checklist, OCR, Extraction, Generation and Evidence Package | `documents / integration` | JIT pack + Sprint 47 PASS | `ROADMAP_ONLY` |
| 049 | Append-only Audit, Alert, Notification, Delivery and Notification Center | `audit / operations / activity` | JIT pack + foundation and templates | `ROADMAP_ONLY` |
| 050 | Integration Hub: Connections, Mapping Versions, Webhooks, Sync, DLQ and Reconciliation | `integration` | JIT Integration pack + security/event maturity | `ROADMAP_ONLY` |
| 051 | Operations Center: Jobs, Queues, Health, Incidents, Maintenance, Backup, Restore and Break-glass | `operations` | JIT Operations pack + runbooks/SLO | `ROADMAP_ONLY` |

## Phase 11 — Hardening, UAT and Release
| Sprint | Outcome | Primary ownership | Activation gate | Current status |
|---:|---|---|---|---|
| 052 | Security Hardening, Full Authorization Matrix, Field Masking and SoD | `all / iam / security` | JIT hardening pack + feature completion | `ROADMAP_ONLY` |
| 053 | Performance, Partitioning, Caching, Concurrency and Capacity Hardening | `all / operations` | NFR/capacity evidence + JIT pack | `ROADMAP_ONLY` |
| 054 | Canonical Data Import Framework, Staging, Mapping, Validation and Reconciliation | `integration / all owners` | JIT import pack + source contracts | `ROADMAP_ONLY` |
| 055 | End-to-end UAT, Data Quality, Runbooks, Training and Operational Readiness | `all` | UAT plan + feature readiness | `ROADMAP_ONLY` |
| 056 | Production Release, Deployment Gates, Smoke Tests and Hypercare Activation | `operations / all` | Production readiness approval | `ROADMAP_ONLY` |
| 057 | Production Stabilization, Defect Closure, Reconciliation and Architecture Review | `all` | Release evidence + hypercare plan | `ROADMAP_ONLY` |

---

# 7. Cross-phase dependency principles

- Foundation decisions must precede dependent business Contexts.
- Party owns canonical Customer identity before Lead/Product/Transaction flows depend on it.
- Product owns Availability and Commercial Lock before Hold/Booking.
- Contract owns Buyer Receivable, Payment, Allocation and Receipt before Revenue consumes accepted facts.
- Revenue owns Revenue and Commission lifecycles; Analytics does not write operational truth.
- Documents/Audit/Integration/Operations foundations may be incrementally introduced earlier, but full capabilities remain in their planned phases.
- Security is continuous; Sprint 52 is hardening/completion, not the first time authorization is implemented.
- Testing/observability/documentation are continuous, not deferred to final phases.

---

# 8. Roadmap change control

A change requires:

- Change rationale.
- Affected requirements/Contexts.
- Dependency impact.
- Security/data/operations impact.
- Renumbering decision when necessary.
- Updates to detailed packs and docs registry.
- Owner approval.
- Changelog entry.

Do not silently reorder Sprint dependencies inside an implementation prompt.

---

# 9. AI Agent rules

Goose and Opencode MUST NOT:

- Code a `ROADMAP_ONLY` Sprint.
- Treat roadmap bullets as exact DDL/API/Event/UI contract.
- Read the entire old master by default.
- Activate multiple Sprints.
- Create future entities “to save time”.
- Copy exact tool versions into Sprint Packs.
- Mark a Sprint accepted without Acceptance Report.

Goose MAY use roadmap titles/outcomes to prepare discovery questions for the next JIT pack, but must distinguish discovery from approved implementation.

---

# 10. Completion truth

Roadmap status is planning truth only.

Sprint completion truth is:

```text
docs/sprints/sprint-XXX/acceptance-report.md
```

Exact implementation truth remains:

```text
Alembic
OpenAPI
JSON Schema + AsyncAPI
Permission/Error/Scope/Masking registries
Code + automated tests
```

---

# 11. Changelog

## Version 1.0.0 — 2026-07-26

- Replaced the active mega master with a lightweight planning roadmap.
- Preserved Sprint 0–57 sequence and outcomes.
- Changed future Sprints to `ROADMAP_ONLY`.
- Added JIT detailed-pack and single-active-Sprint rules.
- Removed repeated exact toolchain and speculative implementation contracts.

---

# 12. Kết luận

```text
Roadmap = sequence and intent
Context Pack = domain contract
Machine Contracts = exact executable shape
Current Sprint Pack = authorized work
Acceptance Report = completion evidence
```


# Cross-cutting AI delivery

AI readiness begins in Sprint 0; gateway abstractions and mock provider in foundation sprints; Copilot features are added incrementally after owning Context readiness. Predictive and agentic capabilities are deferred until data/evaluation/approval maturity. See `docs/ai/ai-roadmap.md`.
