# CRM_BDS_AI — PRODUCT REQUIREMENTS DOCUMENT

## Yêu cầu sản phẩm cho nền tảng CRM và điều hành kinh doanh bất động sản doanh nghiệp

**Document ID:** `PROD-PRD-001`
**Canonical path:** `docs/product/PRD.md`
**Product:** `crm_bds_ai`
**Version:** `1.0.0`  
**Status:** `Accepted / Product Requirements Baseline`
**Owner:** `Product Owner`
**Co-owners:** `Domain Owners`
**Reviewers:** `Architecture Owner`, `Engineering Owner`, `Security Owner`, `Finance Owner`, `Legal Owner`, `Operations Owner`, `QA Owner`
**Effective date:** `2026-08-05`  
**Last reviewed:** `2026-08-05`  
**Classification:** `INTERNAL`

---

# 1. Mục đích

Tài liệu này xác định các yêu cầu sản phẩm của `crm_bds_ai`.

PRD trả lời:

- Sản phẩm phải giải quyết vấn đề gì.
- Ai sử dụng sản phẩm.
- Người dùng phải đạt được kết quả gì.
- Các hành trình nghiệp vụ quan trọng.
- Các capability sản phẩm bắt buộc.
- Functional requirements cấp sản phẩm.
- Product acceptance outcomes.
- Product KPIs.
- Product risks, assumptions và open decisions.
- Cách truy vết requirement sang Context, Sprint và Acceptance Evidence.

PRD không định nghĩa:

- Exact kiến trúc.
- Exact database schema.
- Exact API path hoặc payload.
- Exact Event schema.
- Exact permission code hoặc scope list.
- Exact state machine.
- Exact UI route hoặc component.
- Exact framework/package.
- Exact SLO, retention hoặc infrastructure topology.
- Exact Sprint implementation.
- Quy trình điều phối Goose và Opencode.

Các nội dung exact thuộc tài liệu và machine-readable contract chuyên biệt.

---

# 2. Quan hệ với các tài liệu khác

| Câu hỏi | Nguồn canonical |
|---|---|
| Vì sao sản phẩm tồn tại, sản phẩm là gì và business truths nào phải đúng? | Product Overview |
| Sản phẩm phải cung cấp requirement nào? | PRD này |
| Thuật ngữ có nghĩa gì? | Domain Glossary |
| Context nào sở hữu dữ liệu? | Source of Truth Matrix |
| Hệ thống được chia thế nào? | Architecture Overview + Context Map |
| Mỗi Context vận hành chi tiết ra sao? | Context Implementation Pack |
| Exact database là gì? | Alembic migrations |
| Exact API là gì? | OpenAPI |
| Exact Event là gì? | JSON Schema + AsyncAPI |
| Exact permission/masking là gì? | Registries và matrices |
| Làm gì trong Sprint hiện tại? | Sprint Detailed Execution Pack |
| Đã hoàn thành chưa? | Sprint Acceptance Report |

PRD không thay thế bất kỳ nguồn exact nào kể trên.

---

# 3. Product statement

`crm_bds_ai` là một nền tảng CRM và điều hành kinh doanh bất động sản doanh nghiệp, quản lý xuyên suốt hành trình:

```text
Marketing
→ Lead
→ Customer
→ Requirement
→ Product
→ Matching
→ Transaction
→ Contract and Cash
→ Revenue and Commission
→ Activity
→ Analytics
→ Documents
→ Audit
→ Integration
→ Operations
```

Sản phẩm phải vận hành như một hệ thống nghiệp vụ có kiểm soát, không phải tập hợp màn hình CRUD rời rạc.

---

# 4. Problem statement

Các doanh nghiệp bất động sản thường gặp các vấn đề:

- Lead nằm rải rác ở nhiều nguồn.
- Customer bị tạo trùng.
- Sale không biết ai có quyền chăm sóc.
- Requirement không được chuẩn hóa.
- Asset, Listing và Inventory bị nhầm lẫn.
- Ownership và Selling Right không rõ.
- Availability không đáng tin cậy.
- Hai người cùng giữ hoặc bán một Listing.
- Deal, Booking, Contract và Payment không có lineage.
- Payment bị nhầm với Revenue.
- Revenue bị nhầm với Commission.
- Receipt đã phát hành bị sửa trực tiếp.
- Co-sale và Commission không có version.
- Dashboard tính KPI khác nhau.
- Export và dữ liệu nhạy cảm không được kiểm soát.
- Events, integrations và jobs thất bại nhưng không được reconciliation.
- Backup tồn tại nhưng khả năng restore không được chứng minh.

Sản phẩm phải giải quyết các vấn đề này bằng business ownership, lifecycle, permission, audit, idempotency, concurrency protection và reconciliation rõ ràng.

---

# 5. Product vision

Xây dựng một nền tảng:

- Đúng nghiệp vụ.
- An toàn với dữ liệu và tiền.
- Minh bạch và truy vết được.
- Hỗ trợ nhiều Legal Entity và mô hình kinh doanh.
- Có Customer identity thống nhất.
- Có Product availability đáng tin cậy.
- Có transaction lifecycle được kiểm soát.
- Có Contract, Payment, Revenue và Commission tách biệt.
- Có official metrics được quản trị.
- Có khả năng tích hợp, phục hồi và vận hành dài hạn.

Nguyên tắc sản phẩm:

```text
Canonical Customer Identity
One Source of Truth per Business Concept
Backend-Enforced Access
Product-Owned Availability
Controlled Transaction Lifecycles
Immutable Financial Evidence
Versioned Business Rules
Reliable Cross-context Propagation
Append-Only Audit
Certified Analytics
Operational Recoverability
```

---

# 6. Product goals

- **G-001:** Xây dựng Customer identity thống nhất và ngăn duplicate Customer.
- **G-002:** Chuẩn hóa Lead intake, routing, assignment, protection, qualification, conversion và SLA.
- **G-003:** Chuẩn hóa Project, Asset, Ownership, Selling Right, Listing, Price, Inventory và Availability.
- **G-004:** Ngăn double booking và double sale bằng Commercial Lock có concurrency protection.
- **G-005:** Tách rõ Deal, Transaction Case, Proposal, Negotiation, Hold, Booking và Contract.
- **G-006:** Tách rõ Receivable, Payment, Allocation, Receipt, Refund và Settlement.
- **G-007:** Tách rõ Revenue Entitlement, Recognition, Revenue Receivable và Collection.
- **G-008:** Tách rõ Commission Entitlement, Vesting, Payable, Payout và Clawback.
- **G-009:** Cung cấp Task, Appointment, Interaction, Timeline, SLA và Next Best Action.
- **G-010:** Cung cấp Campaign, Source, Touchpoint, Audience, Journey, Conversion, Attribution và Spend.
- **G-011:** Cung cấp certified Metrics, Dashboards, Drill-down, Snapshot và Forecast.
- **G-012:** Cung cấp Documents, Dossier, Verification, OCR, Signature và Evidence Package.
- **G-013:** Cung cấp Audit, Approval, SoD và sensitive-access evidence.
- **G-014:** Cung cấp integration lifecycle, mapping, idempotency, retries, replay và reconciliation.
- **G-015:** Cung cấp jobs, incidents, backup, restore, release evidence và recovery capability.

---

# 7. Product non-goals

Baseline không nhằm:

- Thay thế General Ledger.
- Thay thế hệ thống kế toán pháp định đầy đủ.
- Thay thế HR/Payroll.
- Quản lý thi công.
- Quản lý vận hành tòa nhà toàn diện.
- Là marketplace công khai quy mô lớn.
- Là core banking hoặc payment gateway.
- Là government land registry.
- Là arbitrary low-code platform.
- Là CDP toàn tập đoàn.
- Là contact-center platform chuyên dụng.
- Là event-sourcing platform toàn phần.
- Là microservices-first.
- Tự động quyết định tín dụng.
- Dùng AI làm final authority cho permission, financial calculation hoặc official KPI.
- Mặc định hỗ trợ backward compatibility với CRM cũ.
- Mặc định là SaaS multi-tenant cho nhiều doanh nghiệp độc lập.

---

# 8. Target organizations và business operating models

## 8.1. Target organizations

- Chủ đầu tư.
- Công ty phát triển dự án.
- Đại lý phân phối.
- Đơn vị môi giới.
- Công ty nhận ký gửi.
- Doanh nghiệp sở hữu và bán tài sản.
- Doanh nghiệp có nhiều Legal Entity.
- Doanh nghiệp có nhiều chi nhánh, phòng ban, đội sale và dự án.

## 8.2. Supported business operating models

### BOM-001 — Company as developer or seller

Expected outcomes:

- Quản lý Project, Asset và Listing.
- Kiểm soát giá và availability.
- Booking và Contract theo policy.
- Customer Payment được ghi đúng bản chất.
- Revenue và Internal Commission có căn cứ.

### BOM-002 — Distribution for external developer

Expected outcomes:

- Quản lý Distribution Mandate.
- Quản lý external inventory.
- Biết ai là seller và ai nhận tiền.
- Tách Customer Payment khỏi Distribution Revenue.
- Theo dõi Revenue Entitlement và Collection.

### BOM-003 — Brokerage or consignment

Expected outcomes:

- Xác minh Asset ownership.
- Quản lý Selling Right.
- Quản lý Seller-side và Buyer-side activity.
- Quản lý Settlement.
- Tính Brokerage Revenue và Internal Commission.

### BOM-004 — Company-owned assets

Expected outcomes:

- Quản lý ownership và source.
- Quản lý approval giá.
- Quản lý Listing, Transaction, cash và revenue.

### BOM-005 — Partner-owned assets

Expected outcomes:

- Quản lý effective Selling Right.
- Quản lý exclusivity, collection rights và commercial scope.
- Ngăn Listing hoạt động ngoài quyền được cấp.

---

# 9. Personas

- **PER-001 Executive / Director:** pipeline, Booking, Contract, Revenue, Collection, Commission, Forecast và risks.
- **PER-002 Platform Administrator:** Legal Entity, Calendar, Numbering, Configuration, Workflow và Approval.
- **PER-003 IAM Administrator:** User, workforce, organization, roles, permissions, delegations và access review.
- **PER-004 Marketing Manager:** Campaign, Source, Form, Audience, Journey, Spend và Attribution.
- **PER-005 Salesperson:** Lead, Customer, Requirement, Matching, Deal, Hold, Booking, Task và Commission.
- **PER-006 Sales Manager:** routing, reassign, care protection, pipeline, SLA, approvals và disputes.
- **PER-007 Inventory Administrator:** Project, Asset, Ownership, Listing, Price, Inventory, Availability và Lock.
- **PER-008 Transaction Coordinator:** Transaction Case, parties, Proposal, Hold, Booking và dossier readiness.
- **PER-009 Legal / Contract Officer:** Contract, versions, parties, signature, effectiveness và legal evidence.
- **PER-010 Finance / Cashier:** Receivable, Payment, Allocation, Receipt, Refund và Settlement.
- **PER-011 Revenue Operations:** Arrangement, Entitlement, Recognition, Revenue Receivable và Collection.
- **PER-012 Commission Administrator:** Plan, Entitlement, Vesting, Payable, Payout và Clawback.
- **PER-013 Operations / Support:** jobs, integrations, incidents, backup, restore và release evidence.
- **PER-014 Auditor:** Audit, approvals, financial evidence, exports, break-glass và data repair.

---

# 10. Product capability map

| Capability code | Capability |
|---|---|
| CAP-PLA | Platform Configuration |
| CAP-IAM | Identity, Access and Organization |
| CAP-PAR | Party, Customer and Requirement |
| CAP-LEA | Lead Management |
| CAP-PRO | Product, Asset, Listing and Inventory |
| CAP-MAT | Matching |
| CAP-TRA | Deal and Transaction |
| CAP-CON | Contract and Cash |
| CAP-REV | Revenue and Commission |
| CAP-ACT | Activity and Engagement |
| CAP-MAR | Marketing |
| CAP-ANA | Analytics |
| CAP-DOC | Documents and Dossier |
| CAP-AUD | Audit and Control |
| CAP-INT | Integration |
| CAP-OPE | Operations |

Capability grouping không quyết định package structure, Bounded Context hoặc database ownership.

---

# 11. Critical business journeys

## JRN-001 — Marketing to Lead

```text
Campaign → Tracking/Form → Submission → Validation → Touchpoint → Lead Intake → Source Snapshot
```

## JRN-002 — Lead to Customer

```text
Lead → Routing → Assignment → Qualification → Customer Resolution → Requirement → Conversion
```

## JRN-003 — Requirement to Matching

```text
Requirement → Financial Profile → Matching Run → Ranking → Explanation → Shortlist
```

## JRN-004 — Shortlist to Deal

```text
Shortlist → Deal → Transaction Case → Proposal → Negotiation
```

## JRN-005 — Deal to Booking

```text
Deal → Commercial Lock → Hold → Dossier Readiness → Booking → Confirmation
```

## JRN-006 — Booking to Contract

```text
Booking Confirmed → Contract Draft → Version → Approval → Signature → Effectiveness
```

## JRN-007 — Contract to Payment and Receipt

```text
Contract Effective → Payment Schedule → Receivable → Payment → Allocation → Receipt
```

## JRN-008 — Refund and Settlement

```text
Request → Impact → Approval → Execution → Reconciliation
```

## JRN-009 — Revenue

```text
Eligible Event → Arrangement → Entitlement → Recognition → Revenue Receivable → Collection → Reversal
```

## JRN-010 — Commission

```text
Eligible Event → Plan → Entitlement → Vesting → Payable → Payout → Clawback
```

## JRN-011 — Customer Merge

```text
Duplicate Candidate → Identity Case → Merge Plan → Approval → Redirect → Reconciliation
```

## JRN-012 — Contract Cancellation

```text
Cancellation → Product Release → Receivable Adjustment → Refund → Revenue Reversal → Clawback
```

## JRN-013 — Documents and Dossier

```text
Upload → Security Check → Version → Verification → Dossier → Signature/Evidence Package
```

## JRN-014 — Integration Recovery

```text
Interaction → Validation → Processing → Failure → Retry/DLQ → Replay → Reconciliation
```

## JRN-015 — Backup and Restore

```text
Backup → Verification → Restore Request → Isolated Restore → Validation → Evidence
```

---

# 12. Requirement format và priority

Mỗi requirement có:

- ID.
- Title.
- Business outcome.
- Primary actors.
- Priority.
- Owning capability.
- Acceptance outcomes.

Priority:

- **MUST:** Bắt buộc cho product baseline.
- **SHOULD:** Quan trọng nhưng có thể vào release sau.
- **MAY:** Tùy chọn hoặc mở rộng.

Requirement không định nghĩa exact implementation.

---

# 13. Functional requirements catalog

## 13.1. Platform Configuration

### FR-PLA-001 — Enterprise and operating boundary — MUST

Quản lý business boundary, identity, lifecycle và Audit.

### FR-PLA-002 — Legal Entity — MUST

Quản lý nhiều Legal Entity, lifecycle, timezone, currency và registration data.

### FR-PLA-003 — Business Calendar — MUST

Calendar có version, exceptions, effective periods và historical traceability.

### FR-PLA-004 — Numbering — MUST

Business numbers concurrency-safe, idempotent và không bị tái sử dụng trái policy.

### FR-PLA-005 — Configuration Registry — MUST

Configuration có type, version, scope, validation và effective period.

### FR-PLA-006 — Workflow Definition — MUST

Workflow có version, transition policy và không override Domain invariants.

### FR-PLA-007 — Approval Policy — MUST

Approval routing, authority limit và SoD được quản lý có Audit.

### FR-PLA-008 — Feature Configuration — SHOULD

Feature rollout có thể kiểm soát mà không bypass security hoặc integrity.

## 13.2. Identity, Access and Organization

### FR-IAM-001 — Organization structure — MUST

Branches, departments, teams và hierarchy có effective dates và không cycle.

### FR-IAM-002 — Workforce identity — MUST

User account, employee profile và employment assignments có lifecycle và history.

### FR-IAM-003 — Authentication — MUST

Chỉ identity hợp lệ, active được truy cập hệ thống.

### FR-IAM-004 — Authorization — MUST

Backend enforce capability, effective scope, resource relationship và field policy.

### FR-IAM-005 — Delegation and temporary grants — MUST

Delegation có owner, scope, effective period, expiry và Audit.

### FR-IAM-006 — Access review — SHOULD

Quyền truy cập được review định kỳ.

### FR-IAM-007 — Access explanation — SHOULD

Authorized staff có thể xem safe explanation của quyết định access.

### FR-IAM-008 — Break-glass authority — MUST

Emergency access có reauthentication, scope, expiry, approval và Audit.

## 13.3. Party, Customer and Requirement

### FR-PAR-001 — Party — MUST

Quản lý Individual/Organization Party và multiple business roles.

### FR-PAR-002 — Customer — MUST

Quản lý Customer lifecycle, roles và Customer 360 theo quyền.

### FR-PAR-003 — Phone identity — MUST

Normalize, verify, primary-state và shared-phone exception.

### FR-PAR-004 — Duplicate prevention — MUST

Không tạo duplicate Customer; concurrent create và masked candidate lookup được xử lý an toàn.

### FR-PAR-005 — Identity resolution — MUST

Ambiguous identity được review bằng case, evidence và approved resolution.

### FR-PAR-006 — Customer merge — MUST

Merge plan, canonical values, redirect, lineage và cross-context reconciliation.

### FR-PAR-007 — Requirement — MUST

Intent, criteria, budget, lifecycle, stakeholders và history.

### FR-PAR-008 — Financial Profile — MUST

Financial readiness có version, verification và restricted access.

### FR-PAR-009 — Customer relationships — SHOULD

Quản lý household, representative và related-party relationships.

## 13.4. Lead Management

### FR-LEA-001 — Lead intake — MUST

Manual/Marketing/Integration intake, source snapshot, validation và idempotency.

### FR-LEA-002 — Lead routing — MUST

Routing rules có version, capacity, explanation và safe failure.

### FR-LEA-003 — Assignment — MUST

Primary assignment, collaborators, accept/reject/reassign và history.

### FR-LEA-004 — Care protection — MUST

Request, approval, expiry, revocation và dispute.

### FR-LEA-005 — Qualification — MUST

Criteria, score, explanation và decision.

### FR-LEA-006 — Nurture, closure and reopen — MUST

Lead lifecycle có reason và history.

### FR-LEA-007 — Lead conversion — MUST

Customer resolution, optional Requirement, seller path và idempotent conversion.

## 13.5. Product, Asset, Listing and Inventory

### FR-PRO-001 — Partner and Project — MUST

Partner roles, Project hierarchy và access.

### FR-PRO-002 — Property Asset — MUST

Asset có physical/legal identity, verification và duplicate handling.

### FR-PRO-003 — Ownership — MUST

Multiple owners, shares, effective periods, verification và transfer history.

### FR-PRO-004 — Selling Right — MUST

Grantor, grantee, scope, effective period, exclusivity và collection rights.

### FR-PRO-005 — Listing — MUST

Listing liên kết Asset, parties, Selling Right, lifecycle và versions.

### FR-PRO-006 — Price and commercial policy — MUST

Price/components có version, approval, confidentiality và effective periods.

### FR-PRO-007 — Inventory — MUST

Inventory lists, versions, items và publishing.

### FR-PRO-008 — Availability — MUST

Product sở hữu availability và cung cấp trạng thái đáng tin cậy.

### FR-PRO-009 — Commercial Lock — MUST

Lock atomic, idempotent, concurrency-safe; conflicting Lock không coexist trái policy.

### FR-PRO-010 — External inventory mapping — SHOULD

External references có mapping version và reconciliation.

## 13.6. Matching

### FR-MAT-001 — Matching rule set — MUST

Hard/soft criteria có version, validation và approval.

### FR-MAT-002 — Matching run — MUST

Input snapshots, candidate pool, async state và authorized scope.

### FR-MAT-003 — Scoring and explanation — MUST

Scores, exclusion reasons và deterministic explanation.

### FR-MAT-004 — Staleness — MUST

Results được invalidate hoặc đánh dấu stale khi inputs thay đổi.

### FR-MAT-005 — Shortlist — MUST

Create, add/remove/reorder và stale marking.

### FR-MAT-006 — Customer feedback — SHOULD

Interested, neutral, rejected và needs-information feedback.

### FR-MAT-007 — Reverse matching — SHOULD

Listing-to-Requirement matching tôn trọng privacy và masking.

## 13.7. Deal and Transaction

### FR-TRA-001 — Deal — MUST

Buyer/seller side, pipeline, stage history, responsibility và closure.

### FR-TRA-002 — Transaction Case — MUST

Multi-party roles, Asset/Listing, company role, payment flow và readiness.

### FR-TRA-003 — Proposal — MUST

Versions, commercial snapshot, approval và lifecycle.

### FR-TRA-004 — Negotiation — MUST

Rounds, offers, counter-offers và append-only terms.

### FR-TRA-005 — Hold — MUST

Hold dùng Product Commercial Lock, có approval, extension, release và reconciliation.

### FR-TRA-006 — Booking — MUST

Multiple buyers, snapshot, dossier gate, confirm/cancel và idempotency.

### FR-TRA-007 — Deposit Commitment — SHOULD

Cam kết đặt cọc có lifecycle và không bị nhầm với Payment.

## 13.8. Contract and Cash

### FR-CON-001 — Contract — MUST

Contract có parties, numbering, lifecycle và source lineage.

### FR-CON-002 — Contract versions — MUST

Draft, review, approved/signed versions, diff và amendment lineage.

### FR-CON-003 — Signature — MUST

Envelope, signers, order, evidence, expiry và reconciliation.

### FR-CON-004 — Contract effectiveness — MUST

Signed và effective được phân biệt; activation có guards.

### FR-CON-005 — Payment Schedule — MUST

Milestones, versions, due dates, activation và adjustment.

### FR-CON-006 — Receivable — MUST

Due, partial, paid, overdue, waived và adjusted lifecycle.

### FR-CON-007 — Payment — MUST

Receive, identify, reverse/refund và provider idempotency.

### FR-CON-008 — Payment Allocation — MUST

Partial/reverse allocation và không over-allocation dưới concurrency.

### FR-CON-009 — Receipt — MUST

Issue idempotently, immutable, unique number và correction lineage.

### FR-CON-010 — Refund — MUST

Request, approval, execution, reconciliation và Audit.

### FR-CON-011 — Owner/Partner Settlement — MUST

Gross, deductions, payable, paid, outstanding và reconciliation.

### FR-CON-012 — Contract cancellation — MUST

Impact preview, approvals, compensation, retries và reconciliation.

## 13.9. Revenue and Commission

### FR-REV-001 — Revenue Arrangement — MUST

Versioned commercial revenue terms và components.

### FR-REV-002 — Revenue Entitlement — MUST

Basis, beneficiary, formula/policy version và source lineage.

### FR-REV-003 — Revenue Recognition — MUST

Milestones, append-only recognition, adjustment và reversal.

### FR-REV-004 — Revenue Receivable — MUST

Khoản đối tác phải trả công ty được tách khỏi Buyer Receivable.

### FR-REV-005 — Revenue Collection — MUST

Revenue payment intake, allocation và reconciliation.

### FR-REV-006 — Revenue adjustment/reversal — MUST

Correction giữ history và không silent update.

### FR-REV-007 — Commission Plan — MUST

Versioned basis, tiers, participants, splits và approval.

### FR-REV-008 — Commission Entitlement — MUST

Evaluate, confirm, adjust, cancel và source lineage.

### FR-REV-009 — Vesting — MUST

Milestones, holdback, waiver và partial vesting.

### FR-REV-010 — Payable and Payout — MUST

Payout không vượt payable, có approval và reconciliation.

### FR-REV-011 — Clawback — MUST

Calculate, approve, apply, dispute và negative balance.

## 13.10. Activity and Engagement

### FR-ACT-001 — Task — MUST

Create, assign, start, block, complete, cancel và resource linkage.

### FR-ACT-002 — Assignment and collaboration — MUST

Primary assignee và collaborators.

### FR-ACT-003 — Checklist and dependencies — SHOULD

Checklist, dependencies và readiness.

### FR-ACT-004 — Recurrence — SHOULD

Recurring generation idempotent.

### FR-ACT-005 — SLA — MUST

Business Calendar clock, pause/resume, breach và escalation.

### FR-ACT-006 — Appointment — MUST

Schedule, participants, confirmation, attendance và no-show.

### FR-ACT-007 — Call and Interaction — MUST

Channels, outcomes, threads và provider references.

### FR-ACT-008 — Timeline — MUST

Read-only event projection với source links và merge handling.

### FR-ACT-009 — Next Best Action — SHOULD

Rule-based recommendation có permission, consent và frequency gates.

## 13.11. Marketing

### FR-MAR-001 — Campaign — MUST

Campaign lifecycle, versions, flights, channels và budgets.

### FR-MAR-002 — Source and Tracking — MUST

Stable source codes, tracking lineage và references.

### FR-MAR-003 — Forms and Submissions — MUST

Versioned forms, validation, consent, spam control và Lead handoff.

### FR-MAR-004 — Touchpoints — MUST

Anonymous/known interactions và identity linkage.

### FR-MAR-005 — Audience — SHOULD

Versioned rules, evaluation runs và membership snapshots.

### FR-MAR-006 — Consent and Suppression — MUST

Suppression precedence, expiry và frequency controls.

### FR-MAR-007 — Journey — SHOULD

Versioned enrollment, waits, conditions, actions, retries và exit.

### FR-MAR-008 — Conversion — MUST

Definition, verification, reversal và lineage.

### FR-MAR-009 — Attribution — SHOULD

Versioned models; không quyết định Commission.

### FR-MAR-010 — Spend and Budget — MUST

Import, verify, adjust, reconcile và currency.

## 13.12. Analytics

### FR-ANA-001 — Dataset Registry — MUST

Grain, sources, schema, versions và activation.

### FR-ANA-002 — Projection Runtime — MUST

Offsets, replay, failures, freshness và reconciliation.

### FR-ANA-003 — Metric Registry — MUST

Versioned formula, grain, time, currency, scope và certification.

### FR-ANA-004 — Data Quality and Certification — MUST

Quality tests và certification blocking.

### FR-ANA-005 — Dashboards — MUST

Persona-aware dashboards, filters, sharing và freshness.

### FR-ANA-006 — Drill-down — MUST

Authorized rows và source-resource access.

### FR-ANA-007 — Export — MUST

Async, policy-driven, expiring và audited export.

### FR-ANA-008 — Snapshot — SHOULD

Generate, validate, approve, lock và restate.

### FR-ANA-009 — Targets and Scorecards — SHOULD

Targets theo scope, period và version.

### FR-ANA-010 — Forecast — SHOULD

Models, scenarios, overrides và accuracy.

## 13.13. Documents and Dossier

### FR-DOC-001 — File upload — MUST

Authentication, authorization, checksum, type, size và security checks.

### FR-DOC-002 — Document — MUST

Type, metadata, context links, lifecycle và archive.

### FR-DOC-003 — Document versions — MUST

Versions được giữ; verified version không bị ghi đè.

### FR-DOC-004 — Verification — MUST

Verifier, outcome, reason và evidence.

### FR-DOC-005 — Dossier — MUST

Checklist, completeness, exceptions, freeze và reopen.

### FR-DOC-006 — OCR and extraction — SHOULD

Results có review và không tự thành canonical truth.

### FR-DOC-007 — Document generation — MUST

Template version, rendering, retries và evidence.

### FR-DOC-008 — Signature evidence — MUST

Provider result, evidence và reconciliation.

### FR-DOC-009 — Evidence Package — MUST

Manifest, versions, hashes và restricted download.

### FR-DOC-010 — Legal hold — SHOULD

Retention purge bị chặn cho held items.

## 13.14. Audit and Control

### FR-AUD-001 — Audit facts — MUST

Append-only/protected actor, action, outcome, resource và correlation facts.

### FR-AUD-002 — Sensitive access audit — MUST

PII access, export, restricted download, break-glass và data repair.

### FR-AUD-003 — Audit integrity — MUST

Tampering/loss có thể phát hiện và alert.

### FR-AUD-004 — Audit query — MUST

Restricted, paginated, masked và auditable access.

## 13.15. Integration

### FR-INT-001 — Connections — MUST

Provider metadata, credential reference, lifecycle và health.

### FR-INT-002 — Mapping versions — MUST

Versioned transformations, validation và publishing.

### FR-INT-003 — Inbound webhooks — MUST

Authentication/signature, replay protection, dedupe và processing state.

### FR-INT-004 — Outbound webhooks — SHOULD

Subscriptions, delivery attempts, signatures, retries và DLQ.

### FR-INT-005 — Sync jobs — MUST

Cursors, item states, partial failures và reconciliation.

### FR-INT-006 — Data import — MUST

Staging, mapping, validation, dry run, canonical commands và reconciliation.

### FR-INT-007 — Source of Truth policy — MUST

CRM wins, external wins, merge hoặc manual resolution.

### FR-INT-008 — Replay — MUST

Scope, approval, idempotency, evidence và Audit.

## 13.16. Operations

### FR-OPE-001 — Jobs — MUST

Attempts, progress, retries, cancellation và results.

### FR-OPE-002 — Service health — MUST

Services, dependencies, readiness, liveness và degradation.

### FR-OPE-003 — Alerts — MUST

Rules, owner, severity, dedupe, assignment và runbook.

### FR-OPE-004 — Incidents — MUST

Declaration, timeline, mitigation, resolution, RCA và postmortem.

### FR-OPE-005 — Backup — MUST

Run, verify và evidence.

### FR-OPE-006 — Restore — MUST

Approval, isolation, execution, validation và evidence.

### FR-OPE-007 — Disaster recovery drill — MUST

Measured recovery capability và action tracking.

### FR-OPE-008 — Data repair — MUST

Request, dry run, approval, execution và evidence.

### FR-OPE-009 — Release — MUST

Artifacts, approvals, deployment, migration, smoke, rollback và hypercare.

### FR-OPE-010 — Maintenance — SHOULD

Maintenance windows, impact và communication.

---

# 14. Cross-cutting product requirements

- **CR-001 Backend-enforced access — MUST:** list, detail, export và actions chỉ hoạt động trong effective authorization.
- **CR-002 Data classification — MUST:** dữ liệu nhạy cảm có classification và handling policy.
- **CR-003 Auditability — MUST:** sensitive operations có Audit facts.
- **CR-004 Idempotency — MUST:** critical side effects chống duplicate request/delivery.
- **CR-005 Concurrency protection — MUST:** contentious operations bảo vệ invariants.
- **CR-006 History and correction — MUST:** approved/issued/recognized/paid records không silent-update trái policy.
- **CR-007 Event reliability — MUST:** required events không mất sau commit và duplicate không tạo side effects trùng.
- **CR-008 Reconciliation — MUST:** cross-context/external divergence có thể phát hiện và xử lý.
- **CR-009 Observability — MUST:** critical journeys có signal đủ để vận hành.
- **CR-010 Accessibility and responsive UX — MUST:** critical journeys dùng được trên thiết bị mục tiêu và accessibility baseline.
- **CR-011 Localization — MUST:** Vietnamese-first UI, English code identifiers, timezone/currency semantics rõ.
- **CR-012 Privacy and minimization — MUST:** chỉ thu thập, hiển thị, sao chép và export dữ liệu cần thiết.
- **CR-013 Operational recoverability — MUST:** critical state có backup/recovery/reconciliation capability.
- **CR-014 Explainability — SHOULD:** matching, routing và policy outcomes có safe explanation.

---

# 15. Product success criteria

- **SC-001:** Không tạo duplicate Customer trái identity policy.
- **SC-002:** Không có conflicting Commercial Locks trái invariant.
- **SC-003:** Không confirm Booking khi required Lock/readiness chưa hợp lệ.
- **SC-004:** Không có Payment Allocation vượt available balance.
- **SC-005:** Không có Receipt issued bị direct-edit hoặc number tái sử dụng trái policy.
- **SC-006:** Không ghi Customer Payment thành Revenue sai bản chất.
- **SC-007:** Không có Commission payout vượt payable; Clawback không xóa history.
- **SC-008:** Không có list/detail/export vượt effective authorization.
- **SC-009:** Không mất required business Event sau successful transaction.
- **SC-010:** Duplicate request/Event không tạo duplicate side effect.
- **SC-011:** Sensitive action có Audit và Audit không bị mutable bởi normal workflow.
- **SC-012:** Official KPI không được tính tùy ý ở frontend.
- **SC-013:** Integration failure có state, retry/replay và reconciliation.
- **SC-014:** Backup/restore capability được kiểm chứng bằng evidence.

---

# 16. Product acceptance journeys

Release candidate phải chứng minh các journeys phù hợp phạm vi release:

1. Campaign → Lead → Customer → Requirement.
2. Requirement → Matching → Shortlist.
3. Shortlist → Deal → Proposal.
4. Proposal → Commercial Lock → Hold → Booking.
5. Booking → Contract → Signature → Effective.
6. Contract → Receivable → Payment → Allocation → Receipt.
7. Cancellation → Product release → Refund → Revenue reversal → Commission clawback.
8. Revenue Entitlement → Recognition → Collection.
9. Commission Entitlement → Vesting → Payout.
10. Customer Merge → Redirect → Reconciliation.
11. Document → Dossier → Signature/Evidence Package.
12. Integration failure → Retry/DLQ → Replay → Reconciliation.
13. Backup → Restore → Verification.
14. Break-glass → Sensitive action → Audit → Expiry.
15. Dashboard → Drill-down → Authorized source resource.

Exact UAT cases thuộc UAT Plan.

---

# 17. Product KPIs

## 17.1. Adoption

- Active users.
- Usage by capability.
- Dashboard adoption.
- Matching adoption.
- Task completion adoption.

## 17.2. Sales

- Lead response time.
- Qualification rate.
- Conversion rate.
- Requirement completeness.
- Matching-to-Deal.
- Deal-to-Booking.
- Booking-to-Contract.
- Pipeline aging.
- SLA compliance.

## 17.3. Product and transaction

- Listing readiness.
- Availability accuracy.
- Lock conflict rate.
- Hold expiry rate.
- Booking cancellation rate.
- Dossier completeness.

## 17.4. Finance

- Receivable overdue.
- Payment identification time.
- Allocation accuracy.
- Unallocated funds.
- Receipt turnaround.
- Refund turnaround.
- Settlement reconciliation.

## 17.5. Revenue and Commission

- Entitlement creation time.
- Recognition accuracy.
- Collection aging.
- Commission calculation accuracy.
- Payout accuracy.
- Clawback recovery.

## 17.6. Data quality and operations

- Customer duplicate rate.
- Asset duplicate rate.
- Expired Selling Right exposure.
- Reconciliation findings.
- Availability.
- Event lag.
- Job failure rate.
- Integration failure rate.
- Backup verification.
- Restore drill success.
- Security findings.
- Regression rate.

Exact formulas, targets và SLO thuộc Metric Registry, NFR và SLO documents.

---

# 18. Product risks

- **RISK-001 Scope size:** giảm bằng phased delivery, vertical slices và just-in-time Sprint Packs.
- **RISK-002 Domain ambiguity:** giảm bằng Glossary, Context Packs và Domain review.
- **RISK-003 Financial correctness:** giảm bằng invariants, SoD, concurrency tests, reconciliation và Audit.
- **RISK-004 Customer identity:** giảm bằng central ownership, controlled merge và redirect.
- **RISK-005 Product availability:** giảm bằng Product-owned Lock và database-level guard.
- **RISK-006 Documentation drift:** giảm bằng Documentation Governance và machine-readable contracts.
- **RISK-007 External providers:** giảm bằng ACL, mapping versions, idempotency và reconciliation.
- **RISK-008 Recovery readiness:** giảm bằng backup verification và restore drills.

---

# 19. Product assumptions

- Dự án là Greenfield.
- Một installation trước hết phục vụ một doanh nghiệp hoặc nhóm doanh nghiệp nội bộ.
- Nhiều Legal Entity được hỗ trợ.
- Exact Enterprise/tenancy semantics sẽ được khóa trong Glossary/ADR.
- Vietnamese là ngôn ngữ UI đầu tiên.
- External providers có thể thất bại.
- Financial và legal operations cần Audit.
- File binary dùng Object Storage.
- Backend là final authorization boundary.
- Cross-context consistency có thể eventual.
- Production có staging/UAT và release gates.
- Legacy migration không thuộc baseline trừ khi được phê duyệt riêng.

---

# 20. Open product decisions

Cần formal approval cho:

- Exact Enterprise/tenancy boundary.
- Countries và currencies được hỗ trợ.
- Tax/e-invoice scope.
- Commission tax handling.
- Legal retention requirements.
- Customer portal scope.
- Mobile application scope.
- Rental capability scope.
- Property management scope.
- External BI scope.
- Search capability scope.
- E-signature provider scope.
- Payment/banking provider scope.
- OCR provider scope.
- Official numbering legal requirements.
- Data migration từ hệ thống cũ.
- Supported partner/public APIs.
- AI-assisted features và human-approval boundaries.

Open decision không được Agent tự giải quyết bằng code.

---

# 21. Requirement traceability

Mỗi requirement SHOULD được truy vết:

```text
PRD Requirement
→ Owning Capability
→ Owning Context
→ Context Use Case
→ ADRs
→ Machine-readable Contracts
→ Sprint Tasks
→ Tests
→ Acceptance Evidence
```

Recommended record:

```yaml
requirement_id: FR-PRO-009
owning_capability: CAP-PRO
owning_context: product
context_use_cases:
  - create_commercial_lock
  - release_commercial_lock
sprint_tasks:
  - SPRINT-XXX-TASK-YYY
contracts:
  - <OpenAPI operation>
  - <Event schema>
  - <Migration revision>
tests:
  - <test path>
acceptance_evidence:
  - <report path>
status: PLANNED|IN_PROGRESS|VERIFIED|ACCEPTED
```

---

# 22. Requirement change control

Một PRD change phải có:

- Owner.
- Reason.
- Impacted requirements.
- Product impact.
- Context impact.
- Security/privacy impact.
- Financial/legal impact.
- Roadmap impact.
- Acceptance impact.
- Version update.
- Change Log.

Không sửa meaning âm thầm.

---

# 23. Definition of Ready cho product requirement

Requirement đủ sẵn sàng để phân tích chi tiết khi:

- Business problem rõ.
- Desired outcome rõ.
- Primary actors rõ.
- Priority rõ.
- Owning capability rõ.
- Owning Context có thể xác định.
- Acceptance outcomes rõ.
- Major dependencies rõ.
- Security/privacy implications được nhận diện.
- Financial/legal implications được nhận diện.
- Không có blocking product conflict.

Requirement chưa Ready không được chuyển trực tiếp thành coding task.

---

# 24. Definition of Done cho product requirement

Requirement chỉ được coi Accepted khi:

- Product acceptance outcomes đạt.
- Relevant Context behavior hoàn chỉnh.
- Relevant contracts đồng bộ.
- Relevant tests pass.
- Security/privacy requirements pass.
- Financial/data integrity requirements pass.
- UX flow hoàn chỉnh khi relevant.
- Observability/operations sẵn sàng khi relevant.
- Documentation đồng bộ.
- Acceptance Evidence được ghi.
- Product Owner hoặc delegated authority chấp nhận.

`Implemented` không đồng nghĩa `Accepted`.

---

# 25. PRD use by AI Agents

AI Agents dùng PRD để:

- Hiểu product outcomes.
- Xác định requirement IDs.
- Xác định personas và journeys.
- Kiểm tra feature có phục vụ product goal không.
- Truy vết Context/Sprint task.
- Đối chiếu acceptance outcomes.

AI Agents không dùng PRD để:

- Tự tạo exact table.
- Tự tạo exact endpoint.
- Tự tạo Event payload.
- Tự tạo scope/permission.
- Tự chọn framework.
- Tự chọn SLO.
- Tự chia roadmap thành Sprint mới.
- Bỏ qua Context Pack hoặc machine contracts.

Goose và Opencode phải tuân AI Agent Engineering Constitution và Universal Orchestration Skill.

---

# 26. Required companion product artifacts

```text
README.md
docs/product/product-overview.md
docs/product/PRD.md
docs/product/domain-glossary.md
docs/architecture/architecture-overview.md
docs/architecture/context-map.md
docs/architecture/source-of-truth-matrix.md
docs/engineering/ai-agent-engineering-constitution.md
docs/engineering/technology-toolchain-lock.md
docs/engineering/documentation-governance.md
Applicable project-local Skills in .skills/
Relevant Accepted ADRs
Relevant Context Implementation Packs
Current Sprint Preparation/Execution Pack
UAT Plan
Product Acceptance Reports
```

---

# 27. Change Log

## Version 1.0.1 — 2026-08-05

- Đổi tên file triển khai Greenfield thành canonical filename `PRD.md`.
- Giữ canonical repository path là `docs/product/PRD.md`.
- Loại bỏ Product Charter khỏi dependency graph hiện hành.
- Hợp nhất câu hỏi về lý do tồn tại và định nghĩa sản phẩm vào `Product Overview`.
- Đồng bộ Domain Glossary về canonical location trong `docs/product/`.
- Bổ sung repository entry point `README.md`.
- Bổ sung AI Agent Engineering Constitution, Technology Toolchain Lock, Documentation Governance, project-local Skills, Accepted ADRs và Current Sprint Pack vào companion artifacts.
- Không thay đổi Product Goals, personas, journeys, functional requirements, acceptance outcomes, KPIs, risks, assumptions hoặc business rules.

## Version 1.0.0 — 2026-07-26

- Thiết lập PRD mới cho giai đoạn chuẩn bị Greenfield.
- Tách Product Requirements khỏi Architecture, Engineering Standards, runtime configuration và Agent orchestration.
- Giữ personas, business operating models, critical journeys, product goals, non-goals và success criteria.
- Tổ chức functional requirements theo stable capability codes.
- Loại bỏ module numbering làm architecture identity.
- Loại bỏ exact framework, API paths, Event envelope, scope list, runtime thresholds, retention values và Sprint numbering.
- Bổ sung requirement priority, acceptance outcomes, traceability, risks, assumptions và open decisions.
- Làm rõ `Implemented` không đồng nghĩa `Accepted`.

---

# 28. Final product requirement statement

`crm_bds_ai` phải được xây dựng như một nền tảng vận hành bất động sản doanh nghiệp với:

```text
Canonical Customer Identity
+ Trusted Product Availability
+ Controlled Transaction Lifecycles
+ Immutable Contract and Cash Evidence
+ Correct Revenue and Commission Separation
+ Reliable Events and Idempotency
+ Backend-Enforced Access
+ Append-Only Audit
+ Certified Analytics
+ Operational Recoverability
```

Mỗi requirement quan trọng phải có:

- Business outcome.
- Owner.
- Acceptance outcomes.
- Security implications.
- Data lineage.
- Failure behavior.
- Traceability.
- Evidence.

PRD trả lời:

> Sản phẩm phải cung cấp kết quả và capability nào.

PRD không trả lời:

> Exact implementation phải được viết bằng cách nào.


## AI extension canonical requirements

- AI Copilot is a cross-cutting product capability, not a replacement for the 14 Product Capabilities or 16 Bounded Contexts.
- The product must support pluggable local, on-premise, private-cloud, public-cloud and future AI runtimes through provider/model registries and adapters.
- No business module may depend on a named provider or model.
- AI output is suggestion/draft/extraction/forecast and cannot become business truth without canonical validation and approval.
- Core CRM must remain operational when AI is disabled or unavailable.
- Exact AI requirements are canonical in `docs/ai/ai-canonical-requirements.md` and `docs/product/canonical-business-rules.md`.
