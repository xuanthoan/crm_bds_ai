# CRM_BDS_AI — DOCUMENTATION MAP AND AI AGENT ENTRY POINT

## Cổng vào chính thức của hệ thống tài liệu `crm_bds_ai`

**Document ID:** `DOC-ROOT-001`  
**Canonical path:** `README.md`  
**Product:** `crm_bds_ai`  
**Version:** `1.0.0`  
**Status:** `Ready for Review / Mandatory Entry Point`  
**Canonical:** `Yes`  
**Owner:** `Architecture Owner`  
**Co-owner:** `Technical Owner`  
**Reviewers:** `Product Owner`, `Domain Owners`, `Security Owner`, `Data Governance Owner`, `QA Owner`, `Operations Owner`  
**Effective date:** `2026-08-05`  
**Last reviewed:** `2026-08-05`  
**Review trigger:** Khi thay đổi cấu trúc tài liệu, Product Capability, Bounded Context, Source of Truth, ADR, Sprint, contract, toolchain hoặc release process  
**Supersedes:** `None — Greenfield baseline`  
**Superseded by:** Không  
**Classification:** `INTERNAL`

> Tài liệu này chỉ trở lại trạng thái `Accepted / Mandatory` sau khi Architecture Owner và Technical Owner hoàn tất review theo Change Control.

---

# 1. Mục đích

`README.md` là điểm bắt đầu bắt buộc đối với mọi AI Agent, developer, reviewer, tester và operator làm việc trong repository `crm_bds_ai`.

File này giúp người đọc xác định:

1. Phần mềm đang được xây dựng là gì.
2. Trạng thái thực tế của dự án và Sprint hiện tại.
3. Hệ thống có những Product Capabilities và Bounded Contexts nào.
4. Dữ liệu nào thuộc Context nào.
5. Tài liệu nào là nguồn canonical cho từng loại quyết định.
6. Khi hai tài liệu mâu thuẫn thì áp dụng tài liệu nào.
7. Trước khi code một Sprint phải đọc những gì.
8. Trước khi sửa API, Event, Database, Permission, Workflow hoặc Metric phải đọc những gì.
9. Project-local Skills được sử dụng như thế nào.
10. Sprint đã hoàn thành thật hay mới chỉ được mô tả.
11. Handoff, Project Status và Acceptance Report được sử dụng thế nào.
12. AI Agent phải cung cấp bằng chứng gì trước khi tuyên bố hoàn thành.

Nguyên tắc tối cao:

> Mọi công việc trong repository phải bắt đầu từ file này. Không được đọc ngẫu nhiên rồi chọn tài liệu thuận tiện nhất.

---

# 2. Trạng thái hiện tại của dự án

`crm_bds_ai` là dự án Greenfield. Application coding chưa bắt đầu.

| Phạm vi | Trạng thái |
|---|---|
| Sprint 0 | `READY FOR REVIEW` — Current Preparation Gate |
| Sprint 1 | `PLANNED / NOT ACTIVE` |
| Sprint 2 | `PLANNED / NOT ACTIVE` |
| Sprint 3 | `PLANNED / NOT ACTIVE` |
| Sprint 4–57 | `ROADMAP ONLY` |
| Application implementation | Chưa bắt đầu |
| Production release | Chưa có |
| Current Handoff | Chỉ tạo khi repository work bắt đầu |
| Project Status | Chỉ tạo khi repository work bắt đầu |

Không được diễn giải `Execution Pack` là bằng chứng Sprint đã hoàn thành.

Không được diễn giải tài liệu có trạng thái `Accepted` là bằng chứng code đã tồn tại.

Nguồn trạng thái:

```text
docs/sprints/sprint-000/sprint-000-preparation-pack.md
docs/sprints/sprint-001/sprint-001-execution-pack.md
docs/sprints/sprint-002/sprint-002-execution-pack.md
docs/sprints/sprint-003/sprint-003-execution-pack.md
docs/roadmap/sprint-roadmap.md
```

---

# 3. Tóm tắt sản phẩm

`crm_bds_ai` là nền tảng CRM bất động sản doanh nghiệp quản lý xuyên suốt:

```text
Marketing
→ Lead
→ Party / Customer
→ Requirement / Financial Profile
→ Project / Asset / Listing / Inventory
→ Matching / Shortlist
→ Deal
→ Transaction Case
→ Proposal / Negotiation
→ Hold Request
→ Product Commercial Lock
→ Active Hold
→ Booking
→ Deposit Commitment
→ Contract
→ Payment Plan / Receivable
→ Payment / Allocation / Receipt
→ Refund / Transaction Settlement
→ Revenue
→ Commission
→ Activity / SLA / Timeline
→ Analytics
→ Documents / Audit / Integration / Operations
```

Phân biệt bắt buộc:

```text
Hold business process
→ transaction Context

Commercial Lock
→ product Context
```

Hệ thống không phải là:

- Phần mềm danh bạ đơn giản.
- Một bảng Lead CRUD.
- Website đăng tin bất động sản.
- Dashboard riêng lẻ.
- Hệ thống kế toán tổng hợp hoặc General Ledger.
- Hệ thống payroll hoặc ngân hàng.
- Hệ thống quản lý xây dựng.
- Một collection nhiều màn hình không có ranh giới domain.
- Một microservice architecture bị chia nhỏ sớm.
- Một super-context sở hữu mọi dữ liệu.

Kiến trúc nền tảng:

```text
Greenfield
Modular Monolith First
Domain-Driven Design
16 Bounded Contexts
PostgreSQL Schema per Context
REST / OpenAPI 3.1
JSON Schema + AsyncAPI Events
Transactional Outbox
Consumer Inbox
Idempotency
Backend Authorization
Backend Scope Resolution
Field Masking
Append-only Audit
Read-only Analytics
Object Storage for Files
```

---

# 4. Product Capability và Bounded Context

Product Capability mô tả:

- Product outcome.
- Business meaning.
- Business rules.
- Capability boundary.
- Acceptance outcome.
- Anti-pattern.
- Canonical requirement.

Bounded Context mô tả:

- Domain language có thẩm quyền.
- Aggregate ownership.
- Data ownership.
- Transaction boundary.
- Published API và Events.
- Persistence boundary.
- Runtime behavior.

Quy tắc:

```text
Product Capability
≠ Bounded Context
≠ PostgreSQL schema
≠ Deployable service
```

Một Product Capability có thể sử dụng nhiều Context.

Một Context có thể tham gia nhiều Product Capabilities.

Capability Specification không phải nguồn exact cho DDL, OpenAPI, Event payload, permission code, production formula hoặc exact state machine.

---

# 5. 14 Product Capabilities

| Capability | Tên canonical | Phạm vi sản phẩm chính | Context chính |
|---:|---|---|---|
| 01 | Platform Configuration | Enterprise, Legal Entity, Business Calendar, configuration, workflow, approval, numbering, feature flags | `platform` |
| 02 | Identity, Access and Organization | Workforce, employment, organization, user, role, permission, scope, delegation | `iam` |
| 03 | Lead Management | Lead intake, routing, assignment, protection, qualification, conversion | `lead` |
| 04 | Customer 360 | Party, Customer relationship, Requirement, Financial Profile, Stakeholder, relationships | `party` |
| 05 | Customer Identity Governance | Phone Identity, duplicate prevention, shared contact, merge, redirect, identity resolution | `party` |
| 06 | Product, Asset, Listing and Inventory | Project, Asset, Ownership, Selling Right, Listing, Price, Inventory, Availability, Commercial Lock | `product` |
| 07 | Customer–Product Matching | Matching Profile, rules, run, score, explanation, shortlist, reverse matching | `matching` |
| 08 | Deal and Transaction | Deal, Transaction Case, Proposal, Negotiation, Hold, Booking, Deposit Commitment | `transaction` |
| 09 | Contract and Cash | Contract, Payment Plan, Receivable, Payment, Allocation, Receipt, Refund, Settlement | `contract` |
| 10 | Revenue and Commission | Revenue Arrangement, Entitlement, Recognition, Revenue Receivable, Commission, Payout, Clawback | `revenue` |
| 11 | Activity and Engagement | Task, Appointment, Call, Interaction, Timeline, SLA, Next Best Action | `activity` |
| 12 | Marketing | Campaign, Capture, Touchpoint, Audience, Journey, Attribution, Spend | `marketing` |
| 13 | Analytics | Dataset, Projection, Semantic Metric, Dashboard, Snapshot, Forecast | `analytics` |
| 14 | Runtime Support Overview | Composite overview cho Documents, Audit, Integration và Operations | Composite |

Canonical directory:

```text
docs/product/capabilities/
```

Canonical files:

```text
docs/product/capabilities/cap-01-platform-configuration.md
docs/product/capabilities/cap-02-identity-access-organization.md
docs/product/capabilities/cap-03-lead-management.md
docs/product/capabilities/cap-04-customer-360.md
docs/product/capabilities/cap-05-customer-identity-governance.md
docs/product/capabilities/cap-06-product-asset-listing-inventory.md
docs/product/capabilities/cap-07-matching.md
docs/product/capabilities/cap-08-deal-and-transaction.md
docs/product/capabilities/cap-09-contract-and-cash.md
docs/product/capabilities/cap-10-revenue-and-commission.md
docs/product/capabilities/cap-11-activity-and-engagement.md
docs/product/capabilities/cap-12-marketing.md
docs/product/capabilities/cap-13-analytics.md
docs/product/capabilities/cap-14-runtime-support-overview.md
```

## 5.1. Capability 04 và Capability 05

Capability 04 và Capability 05 đều chủ yếu thuộc `party`.

Không được tạo:

- Hai Customer masters.
- Hai Party identities.
- Một identity service cạnh tranh với `party`.
- Một duplicate Customer aggregate độc lập.

## 5.2. Capability 14

Capability 14 là:

```text
Composite Product Capability Overview
```

Participating Contexts:

```text
documents
audit
integration
operations
```

Không tạo:

```text
runtime_support schema
runtime_support repository
runtime_support super-context
runtime_support service sở hữu toàn bộ runtime data
```

---

# 6. 16 Bounded Contexts

```text
platform
iam
party
lead
product
matching
transaction
contract
revenue
activity
marketing
analytics
documents
audit
integration
operations
```

## 6.1. Bản đồ trách nhiệm canonical

| Context | Sở hữu chính | Không sở hữu |
|---|---|---|
| `platform` | Enterprise, Legal Entity, Business Calendar, configuration definitions, workflow, approval, numbering, feature flags | User account, Customer, Listing, Contract, runtime SLA instance |
| `iam` | Workforce Subject reference, Employment Assignment, User Account, Service Account, Organization Unit, Position, Role, Permission, Scope, Access Grant, Delegation | Canonical Person/Party identity, Customer Profile, Lead, Project business data |
| `party` | Party, Person/Organization identity, Customer relationship, Phone Identity, Contact Identity, Requirement, Financial Profile, Stakeholder, Consent, Contact Restriction, Merge, Redirect | Lead lifecycle, Listing, Booking, Payment |
| `lead` | Lead, intake, accepted source snapshot, routing, assignment, protection, qualification, conversion process | Canonical Customer identity, Campaign attribution model |
| `product` | Supply Partner Profile, Project, Asset, Ownership, Encumbrance, Selling Right, Listing, Price, Sales Policy, Inventory, Availability, Commercial Lock | Deal, Booking, Contract, Payment |
| `matching` | Matching Profile, Rule Set, Run, Eligibility Result, Score, Explanation, Shortlist, Reverse Matching | Requirement source, Listing source, Booking |
| `transaction` | Deal, Transaction Case, Proposal, Negotiation, Hold business process, Booking, Deposit Commitment, Co-sale Agreement | Product Availability, Commercial Lock aggregate, Contract cash truth |
| `contract` | Contract, Contract Version, signing requirements, legal state, Payment Plan, Receivable, Payment, Allocation, Receipt, Refund, Transaction Settlement | Product Availability, Revenue, Commission, binary signed document |
| `revenue` | Revenue Arrangement, Entitlement, operational Recognition, Revenue Receivable, Revenue Payment Application, Commission Entitlement, Vesting, Payable, Payout orchestration, Clawback | Buyer Payment, Receipt, Deal responsibility, bank execution |
| `activity` | Task, Appointment, Call Log, Interaction, Unified Timeline projection, SLA Instance, Next Best Action | Source business state, canonical consent, provider transport |
| `marketing` | Campaign, Flight, Marketing Capture, Touchpoint, Audience, Journey, Marketing Message Intent, Attribution, Operational Spend | Lead assignment, Customer identity, canonical Interaction, Commission |
| `analytics` | Dataset, Projection, Semantic Metric, KPI, Dashboard, Report definition, Snapshot, Forecast, Data Quality, Reconciliation | Operational source state; read-only đối với business truth |
| `documents` | File Object, Document, Document Version, Dossier, OCR/extraction artifact, Evidence, Signature Envelope, Signature Evidence, Retention, Legal Hold | Contract state, Booking state, provider transport |
| `audit` | Immutable Audit Fact, Audit Seal, Integrity Chain, Sensitive Access Audit | Business aggregate state, operational log |
| `integration` | Connection, provider credential reference, Mapping Version, Webhook, Sync, Cursor, delivery attempts, retry, DLQ, Replay, external reconciliation | Business aggregate ownership, operational source tables của Context khác |
| `operations` | Job runtime, Queue runtime, Operational Alert, Notification orchestration, Health, Incident, Maintenance, Backup, Restore, DR evidence, Data Repair orchestration, Release evidence, Support Session, Break-glass session runtime | Business truth, emergency access grant authority, provider delivery truth |

## 6.2. Person và Workforce

Canonical Person/Party identity thuộc `party`.

IAM chỉ tham chiếu Party identity để quản lý Workforce và User Account.

Không được tạo Person master cạnh tranh trong `iam`.

## 6.3. Signing boundary

```text
Contract signing requirements
Legal signing state
Contract effectiveness decision
→ contract

Signature Envelope
Signer execution evidence
Signed Document
Certificate
Signature Evidence
→ documents

Signature provider transport
Webhook
Retry
Provider callback
→ integration
```

## 6.4. Notification boundary

```text
Notification definition/template
→ platform

Consent/contact restriction
→ party

Marketing eligibility/journey
→ marketing

Notification orchestration
→ operations

Provider delivery
→ integration

Canonical Interaction
→ activity

Immutable evidence
→ audit
```

## 6.5. Break-glass boundary

```text
Emergency authorization grant
→ iam / security authority

Break-glass session orchestration
→ operations

Sensitive access evidence
→ audit
```

System Administrator không mặc định có blanket access tới Customer PII, bank data, Contract documents hoặc Commission.

---

# 7. Source of Truth tóm tắt

| Khái niệm | Context sở hữu |
|---|---|
| Enterprise, Legal Entity, Business Calendar | `platform` |
| Workforce, Employment Assignment, User, Org Unit, Role, Permission | `iam` |
| Party, Customer relationship, Phone Identity, Requirement, Consent | `party` |
| Lead, Assignment, Protection, Qualification | `lead` |
| Project, Asset, Ownership, Selling Right, Listing | `product` |
| Availability và Commercial Lock | `product` |
| Match Result, Explanation, Shortlist | `matching` |
| Deal, Transaction Case, Proposal, Hold, Booking | `transaction` |
| Contract, Payment Plan, Buyer Receivable, Payment, Allocation, Receipt | `contract` |
| Revenue, Revenue Receivable, Commission, Payout orchestration | `revenue` |
| Task, Appointment, Interaction, Timeline projection, SLA Instance | `activity` |
| Campaign, Capture, Touchpoint, Audience, Journey, Attribution | `marketing` |
| Dataset, Semantic Metric, Dashboard, Snapshot, Forecast | `analytics` |
| File, Document, Document Version, Dossier, Signature Evidence | `documents` |
| Immutable Audit Fact | `audit` |
| Provider connection, Mapping, Webhook, Sync, DLQ, Replay | `integration` |
| Job, Incident, Notification orchestration, Backup, Restore, Release evidence | `operations` |

Nguồn đầy đủ:

```text
docs/architecture/source-of-truth-matrix.md
```

Không suy ra ownership từ tên bảng, API route, vị trí UI, tên package, tên Event, Sprint Pack hoặc existing code bị drift.

---

# 8. Mandatory reading order cho AI Agent mới

AI Agent mới phải đọc theo thứ tự:

1. `README.md`
2. `docs/product/product-overview.md`
3. `docs/product/PRD.md`
4. `docs/product/domain-glossary.md`
5. `docs/architecture/architecture-overview.md`
6. `docs/architecture/context-map.md`
7. `docs/architecture/source-of-truth-matrix.md`
8. `docs/architecture/dependency-rules.md` nếu tồn tại
9. `docs/engineering/ai-agent-engineering-constitution.md`
10. `docs/engineering/technology-toolchain-lock.md`
11. `docs/engineering/documentation-governance.md`
12. Project-local Skills áp dụng trong `.skills/`
13. Tất cả ADR có trạng thái `Accepted` liên quan
14. `docs/project-status.md` nếu repository work đã bắt đầu
15. `docs/handoffs/current-handoff.md` nếu repository work đã bắt đầu
16. Current Sprint Preparation/Execution Pack
17. Relevant Product Capability Specifications
18. Relevant Context Implementation Packs
19. Machine-readable contracts liên quan
20. Existing code, migrations và tests liên quan

Không được đọc Sprint Pack trước Product Overview, PRD, Glossary và Source of Truth Matrix rồi tự suy diễn phần còn thiếu.

## 8.1. Project-local Skills

Skills nằm trong:

```text
.skills/
```

Agent phải:

1. Liệt kê các `SKILL.md` liên quan.
2. Đọc skill orchestration trước khi chia task.
3. Đọc specialist skill trước khi thực hiện công việc chuyên môn.
4. Ghi Skills đã đọc trong implementation notes.
5. Không để Skill thay thế project Constitution.

Authority:

```text
AI Agent Engineering Constitution
→ quy định các nguyên tắc không được vi phạm của crm_bds_ai

Project-local Skill
→ quy định workflow, cách phân tích, chia task,
  giao việc, kiểm tra và báo cáo
```

Khi Constitution và Skill mâu thuẫn, Constitution thắng.

## 8.2. Bằng chứng đã đọc

Trong `implementation-notes.md`, Agent phải ghi:

```markdown
## Documents Reviewed
- README.md
- docs/product/product-overview.md
- docs/product/PRD.md
- docs/product/domain-glossary.md
- docs/architecture/architecture-overview.md
- docs/architecture/context-map.md
- docs/architecture/source-of-truth-matrix.md
- docs/engineering/ai-agent-engineering-constitution.md
- docs/engineering/technology-toolchain-lock.md
- docs/engineering/documentation-governance.md

## Skills Reviewed
- .skills/<skill-name>/SKILL.md

## Context and Capability Documents Reviewed
- Relevant Capability Specifications:
- Relevant Context Implementation Packs:
- Relevant ADRs:
- Current Sprint Pack:
- Current Handoff:

## Machine Contracts Reviewed
- Alembic:
- OpenAPI:
- Event Schemas:
- AsyncAPI:
- Permission Registry:
```

Không chấp nhận câu chung chung: `Đã đọc tài liệu.`

---

# 9. Reading order theo nhiệm vụ

## 9.1. Sprint 0 readiness review

1. File này.
2. Product Overview.
3. PRD.
4. Domain Glossary.
5. Architecture Overview.
6. Context Map.
7. Source of Truth Matrix.
8. AI Agent Engineering Constitution.
9. Toolchain Lock.
10. Documentation Governance.
11. Project-local Skills.
12. Sprint 0 Preparation Pack.
13. Accepted ADRs.
14. Capability Specifications.
15. Documentation readiness evidence.

## 9.2. Khởi tạo repository

1. File này.
2. Product Overview.
3. PRD.
4. Domain Glossary.
5. Context Map.
6. Source of Truth Matrix.
7. Architecture Overview.
8. Accepted ADRs.
9. Engineering Constitution.
10. Toolchain Lock.
11. Documentation Governance.
12. Applicable Skills.
13. Sprint 1 Execution Pack.

## 9.3. Triển khai Sprint nghiệp vụ

1. File này.
2. Product Overview và PRD.
3. Domain Glossary.
4. Source of Truth Matrix.
5. Relevant Product Capability Specifications.
6. Relevant Context Implementation Packs.
7. Relevant ADRs.
8. Engineering Standards.
9. Current Sprint Execution Pack.
10. Previous relevant Acceptance Reports.
11. Existing migrations.
12. OpenAPI và Event contracts.
13. Permission/Scope/Masking registries.
14. Existing tests.
15. Current Handoff.
16. Applicable Skills.

## 9.4. Sửa bug

1. GitHub Issue hoặc bug report.
2. Current Handoff.
3. Owning Context.
4. Canonical contract.
5. Context invariants và state machine.
6. Existing regression tests.
7. Code.
8. Sanitized logs và evidence.

## 9.5. Thay API

1. API Standards.
2. Owning Context Pack.
3. OpenAPI.
4. Permission Registry.
5. Scope Resolution.
6. Field Masking Matrix.
7. Error Code Registry.
8. Generated clients/consumers.
9. Contract tests.
10. Current Sprint Pack.

## 9.6. Thay Event

1. Event Standards.
2. Owning Context Pack.
3. Event Registry.
4. JSON Schema.
5. AsyncAPI.
6. Producer.
7. Consumers.
8. Inbox/Outbox behavior.
9. Replay/compatibility tests.
10. Current Sprint Pack.

## 9.7. Thay Database

1. Database Standards.
2. Source of Truth Matrix.
3. Owning Context Pack.
4. Current Alembic graph.
5. Existing constraints/indexes.
6. Migration strategy.
7. Backfill hoặc data-transition plan khi được phê duyệt.
8. Concurrency/idempotency impact.
9. Integration tests.

## 9.8. Thay Permission

1. Security Architecture.
2. Permission Registry.
3. Role Baseline Matrix.
4. Scope Resolution.
5. Field Masking Matrix.
6. Segregation of Duties Matrix.
7. Endpoint/command metadata.
8. Security tests.

## 9.9. Thay Metric hoặc Dashboard

1. Analytics Capability Specification.
2. Analytics Context Pack.
3. Metric Registry.
4. Source Context contracts.
5. Dataset/Metric Version.
6. Scope/masking/export policy.
7. Snapshot/Restatement rules.
8. Metric validation và reconciliation tests.

## 9.10. Production incident

1. Incident record.
2. Relevant runbook.
3. Current release record.
4. Deployment topology.
5. Service health/observability.
6. Relevant contracts.
7. Current Handoff.
8. Code sau khi đã có evidence.

---

# 10. Canonical Source Matrix

| Chủ đề | Canonical source | Tài liệu giải thích |
|---|---|---|
| Product direction | `docs/product/product-overview.md` | PRD |
| Product requirements | `docs/product/PRD.md` | Capability Specifications |
| Business term | `docs/product/domain-glossary.md` | Context Pack |
| Capability scope | `docs/product/capabilities/` | PRD |
| Architecture baseline | `docs/architecture/architecture-overview.md` | Accepted ADRs |
| Context ownership | `docs/architecture/source-of-truth-matrix.md` | Context Map |
| Context relationships | `docs/architecture/context-map.md` | Accepted ADRs |
| Context behavior | Context Implementation Pack | Capability Specification |
| Architecture decision | Accepted ADR | Architecture Overview |
| Toolchain | Lockfiles + `infrastructure/toolchain.lock.toml` | Toolchain Lock |
| Python dependencies | `uv.lock` | `pyproject.toml` |
| JavaScript dependencies | `pnpm-lock.yaml` | `package.json` |
| Database thực thi | Alembic migrations | Context DB Specification |
| API thực thi | `contracts/openapi/openapi.json` | Context API section |
| Event thực thi | JSON Schema + AsyncAPI | Context Event section |
| Permission thực thi | Permission Registry + policy code | Security matrices |
| Field masking | Field Policy Registry + serializers | Field Masking Matrix |
| Workflow thực thi | Published Workflow Definition | Context Pack |
| Feature flag | Feature Flag Registry/Version | Platform docs |
| Metric | Metric Registry/Version | Analytics docs |
| Aggregate behavior | Domain code + unit tests | Context Pack |
| State machine | Domain code + state tests | Context Pack |
| Roadmap | `docs/roadmap/sprint-roadmap.md` | Product Overview |
| Current readiness gate | Sprint 0 Preparation Pack | Documentation readiness evidence |
| Sprint scope | Sprint Execution Pack | Roadmap |
| Sprint completion | Sprint Acceptance Report | Project Status |
| Current work | Current Handoff | Project Status |
| Known defect | GitHub Issue | Known Issues summary |
| Release state | Release Record | Release Report |
| Operational procedure | Runbook | Incident/Postmortem |
| Recovery objective | Operations/SLO/DR documents | Runbooks |
| Generated Report/Export artifact | Documents Context | Analytics job record |
| External provider transport | Integration Context | Provider contract |
| Immutable audit evidence | Audit Context | Audit policy |

---

# 11. Precedence khi có xung đột

1. Yêu cầu mới nhất được Product Owner chấp thuận và ghi nhận chính thức.
2. AI Agent Engineering Constitution.
3. Accepted ADR.
4. Source of Truth Matrix.
5. Domain Glossary.
6. Accepted Context Implementation Pack.
7. Published machine-readable contract.
8. Accepted Product Capability Specification.
9. Current Sprint Preparation/Execution Pack.
10. Engineering Standards.
11. Existing code và tests.
12. Runbooks.
13. Project Status.
14. Current Handoff.
15. Historical hoặc Superseded documents.
16. Suy đoán của AI Agent.

## 11.1. Quy tắc đặc biệt

- Alembic là schema thực thi.
- OpenAPI là API thực thi.
- JSON Schema + AsyncAPI là Event thực thi.
- Permission Registry và policy code là quyền thực thi.
- Metric Registry là định nghĩa Metric thực thi.
- Accepted ADR không được sửa meaning để phù hợp code.
- Capability Specification không thay exact machine contract.
- Code không tự động đúng khi mâu thuẫn canonical documentation.
- Drift giữa code và contract phải được sửa.
- Sprint Pack không được thay Source of Truth.
- Handoff không được thay business rule.
- Project-local Skill không được thay Constitution.

## 11.2. Conflict protocol

```markdown
## Documentation Conflict
- Subject:
- Source A:
- Source A status/version:
- Source B:
- Source B status/version:
- Applicable precedence:
- Safe implementation decision:
- Work blocked: Yes/No
- Follow-up owner:
```

Xung đột về security, financial truth, data ownership, customer identity, Commercial Lock, immutable Receipt hoặc data integrity phải block implementation.

---

# 12. Cấu trúc thư mục tài liệu

```text
docs/
├── README.md
├── project-status.md
├── product/
│   ├── product-overview.md
│   ├── PRD.md
│   ├── domain-glossary.md
│   └── capabilities/
├── architecture/
├── adr/
├── engineering/
├── security/
├── design/
├── contexts/
├── configuration/
├── deployment/
├── integration/
├── operations/
├── runbooks/
├── roadmap/
├── uat/
├── sprints/
├── handoffs/
├── reviews/
├── releases/
├── incidents/
└── historical/
```

Root `docs/` nên chỉ chứa entry points và directories cần thiết.

Chỉ tạo thư mục khi có tài liệu thực. Không tạo hàng trăm file rỗng để tạo cảm giác đầy đủ.

---

# 13. Product Capability Specification

Canonical location:

```text
docs/product/capabilities/
```

Capability Specification canonical cho:

- Product outcome.
- Business meaning.
- Scope và boundary.
- Business invariant.
- Acceptance outcome.
- Anti-pattern.
- Canonical requirement.
- Context collaboration intent.

Capability Specification không canonical exact cho DDL, Alembic constraints/indexes, OpenAPI paths/payloads, Event names/payloads, permission codes, scope codes, exact state machine, production formula, queue/retry topology, SLO/RPO/RTO hoặc provider-specific integration.

---

# 14. Context Implementation Pack

Canonical convention:

```text
docs/contexts/<context>/<context>-context-implementation-pack.md
```

Ví dụ:

```text
docs/contexts/platform/platform-context-implementation-pack.md
docs/contexts/iam/iam-context-implementation-pack.md
docs/contexts/party/party-context-implementation-pack.md
docs/contexts/lead/lead-context-implementation-pack.md
```

Một Context Implementation Pack nên bao phủ khi liên quan:

- Purpose và language.
- Aggregate ownership.
- Commands và queries.
- Invariants.
- Lifecycle/state machines.
- Transaction boundaries.
- Persistence model input.
- API operations.
- Events.
- Permission/scope/masking.
- Workflow/approval.
- Concurrency/idempotency.
- Background jobs.
- Projections.
- UI responsibilities.
- Error taxonomy.
- Acceptance tests.
- Operational concerns.

Khi Context đủ lớn, có thể tách thành các file chuyên biệt. Không bắt buộc tạo toàn bộ file con trước khi có nội dung thực. Không copy cùng một rule vào nhiều file.

---

# 15. ADR Governance

ADR nằm tại:

```text
docs/adr/
```

Mỗi ADR phải có ID duy nhất, Status, Date, Decision owner, Context, Decision, Alternatives, Consequences, Compliance và Supersedes/Superseded by.

Accepted ADR không được chỉnh meaning. Muốn thay quyết định phải tạo ADR mới và supersede ADR cũ.

---

# 16. Machine-readable contracts

## 16.1. OpenAPI

```text
contracts/openapi/openapi.json
```

- OpenAPI 3.1.
- Deterministic generation.
- Unique operation IDs.
- CI fail on drift.
- Frontend types generated từ file này.
- Authorization metadata phải được kiểm tra.
- Idempotency semantics phải được công bố khi cần.

## 16.2. Event contracts

```text
contracts/events/
contracts/asyncapi/asyncapi.yaml
```

- JSON Schema 2020-12.
- Version explicit.
- No secrets.
- PII minimized.
- Compatibility tests.
- Correlation và causation metadata.
- Producer/consumer ownership rõ.
- Replay và Inbox behavior rõ.

## 16.3. Database

```text
backend/migrations/
```

- Không sửa migration đã phát hành.
- Expand–migrate–contract.
- Upgrade/downgrade test.
- Constraints bảo vệ invariant khi có thể.
- Không direct-write schema Context khác.
- Không tạo cross-schema business foreign key nếu chưa có ADR chấp thuận.

## 16.4. Toolchain

```text
.python-version
.node-version
uv.lock
pnpm-lock.yaml
infrastructure/toolchain.lock.toml
infrastructure/docker/images.lock
```

Toolchain baseline phải được validate trong Sprint 0 trước khi code.


---

# 17. Cross-context rules

Mỗi Context:

- Chỉ ghi local business state.
- Không import repository hoặc ORM model của Context khác.
- Không direct-write schema Context khác.
- Không dùng distributed transaction xuyên Contexts.
- Giao tiếp qua published API, durable Event hoặc approved read contract.
- Dùng Transactional Outbox cho Event publication.
- Dùng Consumer Inbox hoặc equivalent idempotency guard cho consumption.
- Có retry, timeout, reconciliation và manual intervention khi process kéo dài.

Không sử dụng Dashboard, frontend hoặc cache làm final authority cho:

- Permission.
- Scope.
- Availability.
- Commercial Lock.
- Payment.
- Receipt.
- Revenue.
- Commission.
- Consent.

---

# 18. Cross-context Process Managers

Canonical location:

```text
docs/architecture/process-managers/
```

Tối thiểu khi được triển khai:

- Lead Conversion.
- Customer Merge.
- Listing Activation.
- Hold Activation.
- Booking Confirmation.
- Contract Effectiveness.
- Contract Cancellation.
- Revenue Entitlement.
- Commission Vesting.
- Signature Envelope.
- Marketing Lead Handoff.
- Payment/Receipt Reconciliation.
- Product Release after Cancellation.

Mỗi specification phải có:

- Trigger.
- Process owner.
- Participating Contexts.
- State.
- Steps.
- Commands.
- Events.
- Idempotency.
- Timeout.
- Retry.
- Compensation.
- Reconciliation.
- Manual intervention.
- Security.
- Metrics.
- Tests.

---

# 19. Sprint lifecycle

## 19.1. Trước Sprint

- Sprint Pack có trạng thái phù hợp.
- Dependency Sprints đã PASS hoặc được waiver chính thức.
- Context ownership rõ.
- Relevant Capability/Context docs đủ rõ.
- Relevant ADR Accepted.
- Definition of Ready pass.
- Không có blocking documentation conflict.
- Toolchain và environment prerequisites được xác nhận.

## 19.2. Trong Sprint

Cập nhật:

```text
docs/sprints/sprint-XXX/implementation-notes.md
```

Ghi:

- Documents reviewed.
- Skills reviewed.
- Assumptions.
- Decisions nhỏ.
- Deviations.
- Files changed.
- Migrations.
- API/Event changes.
- Permission changes.
- Risks.
- Test evidence.
- Follow-up.

## 19.3. Cuối Sprint

Phải có:

```text
docs/sprints/sprint-XXX/acceptance-report.md
```

Đồng thời cập nhật khi liên quan:

- Context docs.
- Machine contracts.
- Runbooks.
- Project Status.
- Current Handoff.
- Release records.
- Known issues.

Sprint không Done nếu Acceptance Report chưa PASS.

---

# 20. Sprint directory

```text
docs/sprints/sprint-XXX/
├── sprint-XXX-preparation-pack.md
├── sprint-XXX-execution-pack.md
├── implementation-notes.md
├── acceptance-report.md
└── evidence/
```

Chỉ sử dụng các file phù hợp với Sprint.

Evidence chỉ chứa dữ liệu đã sanitize.

Không tạo Acceptance Report PASS trước khi có implementation và bằng chứng thật.

---

# 21. Project Status

Canonical summary:

```text
docs/project-status.md
```

Chỉ tạo khi repository work bắt đầu.

Chỉ chứa:

- Current Sprint.
- Last accepted Sprint.
- Current branch/HEAD.
- CI status.
- Environments.
- Release state.
- Blockers.
- Links.

Không chứa:

- Business rules.
- Schema.
- API definitions.
- Permission definitions.
- Metric formulas.
- Source-of-Truth decisions.

---

# 22. Current Handoff

Canonical current file:

```text
docs/handoffs/current-handoff.md
```

Chỉ tạo khi repository work bắt đầu.

Chỉ có một current handoff.

Mẫu:

```markdown
# Current Handoff

## Timestamp
## Branch
## HEAD Commit
## Current Sprint
## Current Task
## Work Completed
## Files Changed
## Migrations
## API/Event Changes
## Permission Changes
## Tests Run
## Test Results
## Uncommitted Changes
## Blockers
## Next Exact Action
## Important Warnings
```

Handoff không phải nguồn chân lý kiến trúc hoặc nghiệp vụ.

---

# 23. AI Agent operating model

## 23.1. Goose

Goose đóng vai trò:

```text
Orchestrator
Tech Lead
Architecture/requirements analyst
Task decomposition authority
Acceptance authority
```

Goose phải:

- Đọc canonical docs và Skills.
- Xác định ownership.
- Phân tích và chia nhỏ công việc.
- Tạo task đủ nhỏ để restart hoặc retry.
- Giao việc cho Executor.
- Review evidence.
- Quyết định acceptance.

## 23.2. Opencode

Opencode đóng vai trò:

```text
Executor
Coding Agent
Implementation worker
```

Executor có thể báo:

```text
IMPLEMENTED
PARTIAL
BLOCKED
FAILED
```

Executor không tự quyết định Sprint accepted.

## 23.3. Acceptance authority

Goose quyết định:

```text
ACCEPTED
REWORK_REQUIRED
REJECTED
BLOCKED
```

Không được chấp nhận chỉ dựa trên câu `đã làm xong`.

---

# 24. AI Agent Task Intake Protocol

Trước khi code, Agent phải xác định:

1. Task thuộc Sprint nào.
2. Sprint có active không.
3. Primary owning Context nào.
4. Participating Contexts nào.
5. Product Capability nào liên quan.
6. Data thuộc Source of Truth nào.
7. Canonical documents nào áp dụng.
8. Applicable Skills nào.
9. Relevant ADR nào.
10. Có thay Database không.
11. Có thay API không.
12. Có Event không.
13. Có permission/scope/masking không.
14. Có workflow/state transition không.
15. Có idempotency/concurrency risk không.
16. Có audit requirement không.
17. Có UI không.
18. Có background job/integration không.
19. Có Documents/File không.
20. Có analytical Metric không.
21. Acceptance tests là gì.
22. Evidence phải thu thập là gì.

---

# 25. AI Agent Implementation Protocol

```text
READ
→ INSPECT
→ RESOLVE CONFLICTS
→ PLAN
→ DECOMPOSE
→ IMPLEMENT DOMAIN
→ IMPLEMENT PERSISTENCE
→ IMPLEMENT APPLICATION/API/EVENT
→ IMPLEMENT UI/JOBS
→ TEST
→ REVIEW
→ DOCUMENT
→ REPORT
→ ACCEPT OR REWORK
```

Không được:

- Code API trước khi hiểu invariant.
- Tạo table trước khi xác định owner.
- Tạo generic CRUD thay state machine.
- Đổi toolchain.
- Bỏ test failure.
- Sửa tests để che bug.
- Tuyên bố Done khi chưa chạy validation.
- Direct-write schema Context khác.
- Dùng frontend làm authority.
- Tự mở rộng scope.
- Tự tạo permission code.
- Tự tạo Event không registry.
- Tự sửa accepted ADR.
- Tự thay Product, Customer hoặc Financial source truth.

---

# 26. Required Completion Report

```markdown
# Completion Report

## Scope Completed
## Files Created
## Files Modified
## Domain Changes
## Database Migrations
## API Changes
## Event Changes
## Permission Changes
## UI Changes
## Background Jobs
## Integration Changes
## Documents/File Changes
## Analytics/Metric Changes
## Tests Executed
## Test Results
## Security/Quality Checks
## Known Limitations
## Documentation Updated
## Commit Hash
## Remaining Work
```

Không chỉ trả lời `Đã hoàn thành`.

---

# 27. Registries

## 27.1. Error codes

Documentation:

```text
docs/engineering/error-code-registry.md
```

Machine registry phải nằm tại accepted implementation location khi code bắt đầu.

## 27.2. Permissions

Documentation:

```text
docs/security/permission-registry.md
```

Machine source thuộc IAM/Security implementation.

Không tự tạo permission code trong router hoặc UI.

## 27.3. Scope

Canonical documentation:

```text
docs/security/scope-resolution.md
```

Backend resolve effective scope.

Frontend filter chỉ được thu hẹp.

## 27.4. Field masking

Canonical documentation:

```text
docs/security/field-masking-matrix.md
```

Masking phải áp dụng trước:

- Serialization.
- Cache.
- Export.
- Scheduled report.
- External BI publication.

## 27.5. Configuration

Canonical là versioned Platform configuration và stable seed codes.

Không hard-code configurable business values trong router hoặc UI.

## 27.6. Metrics

Canonical là Analytics Metric Registry và Metric Version.

Không tính official Metric ở frontend.

---

# 28. Security reading requirements

Trước khi code dữ liệu nhạy cảm, phải đọc:

```text
docs/architecture/security-architecture.md
docs/security/data-classification.md
docs/security/permission-registry.md
docs/security/role-baseline-matrix.md
docs/security/scope-resolution.md
docs/security/field-masking-matrix.md
docs/security/segregation-of-duties.md
docs/security/privacy-and-retention.md
docs/security/threat-model.md
```

Data classes:

```text
PUBLIC
INTERNAL
CONFIDENTIAL
RESTRICTED
HIGHLY_RESTRICTED
```

Không log:

- Password.
- Token.
- Provider secret.
- Identity number đầy đủ.
- Bank account đầy đủ.
- Raw signed document.
- Permanent signed URL.
- Raw restricted payload.
- Customer PII ngoài purpose.

---

# 29. Documents, Audit, Integration và Operations rules

## 29.1. Documents

- Binary files thuộc Documents Context và approved Object Storage.
- Business Context chỉ giữ Document references.
- Verified hoặc signed Document Version không được ghi đè.
- OCR là suggestion, không tự sửa business state.
- Signature completion không tự làm Contract effective.
- Legal Hold chặn destructive deletion.

## 29.2. Audit

- Audit append-only.
- Operational logs không thay Audit.
- Correction tạo Audit fact mới.
- Sensitive access, export, approval và break-glass phải có Audit evidence.

## 29.3. Integration

- Provider credentials không lưu plain text trong application database hoặc docs.
- Webhook phải verify signature và chống replay.
- Retry/replay phải idempotent.
- Provider payload không trở thành Domain Model canonical trực tiếp.
- Integration không tự quyết định business source of truth.

## 29.4. Operations

- Operations không có universal business repository.
- Data Repair cần dry run, approval, impact analysis và reconciliation.
- Backup success không chứng minh restore success.
- Restore test và DR drill phải đo RPO/RTO.
- Break-glass có scope, expiry, MFA, Audit và post-review.

---

# 30. UI/UX documentation

Canonical design documents:

```text
docs/design/
```

Tối thiểu khi áp dụng:

- `design-system.md`
- `design-tokens.md`
- `navigation-and-information-architecture.md`
- `dashboard-visualization-system.md`
- Responsive Layouts.
- Accessibility.
- Form Patterns.
- Table Patterns.
- Workflow Patterns.
- Loading/Empty/Error/Conflict States.

Feature UI không tự tạo design language riêng.

Frontend không được:

- Tự quyết định permission.
- Tự quyết định scope.
- Tự tính official Metric.
- Tự xác nhận Payment.
- Tự tạo Commercial Lock.
- Tự bỏ qua masking.
- Tự coi disabled button là security control.

---

# 31. Testing hierarchy

| Test type | Mục đích |
|---|---|
| Unit | Domain behavior cô lập |
| Integration | PostgreSQL, RabbitMQ, Valkey, Object Storage |
| Contract | OpenAPI, Event schemas, provider contracts |
| Architecture | Context boundaries và import rules |
| Security | Authorization, scope, masking, privilege escalation |
| Concurrency | Commercial Lock, allocation, idempotency |
| E2E | Hành trình người dùng |
| Performance | SLO/capacity |
| Failure injection | Recovery/retry |
| Reconciliation | Cross-context drift |
| Regression | Bug không tái diễn |
| Migration | Upgrade/downgrade/backfill |
| Analytics | Metric formula, lineage, snapshot và restatement |

Không dùng SQLite thay PostgreSQL trong integration tests.

Không mock away invariant quan trọng.

Không sửa expectation để hợp thức hóa bug.

---

# 32. Documentation statuses

```text
Draft
In Review
Ready for Review
Accepted
Published
Planned
Not Active
Roadmap Only
Superseded
Retired
Historical
```

Draft không điều khiển implementation nếu chưa có approval.

`Accepted document` không đồng nghĩa `implemented code`.

`Planned Sprint` không đồng nghĩa `active Sprint`.

---

# 33. File naming

Dùng lowercase và kebab-case.

Đúng:

```text
source-of-truth-matrix.md
database-standards.md
sprint-002-execution-pack.md
cap-08-deal-and-transaction.md
```

Sai:

```text
API_SPEC_FINAL.md
database_schema_latest.md
new_architecture_v2.md
copy_of_plan.md
module-8-v2.md
```

Không dùng trong canonical filename:

```text
final
latest
new
copy
v2
```

Version hợp lệ phải nằm trong metadata hoặc machine contract.


---

# 34. Generated files

Generated files phải ghi:

```text
DO NOT EDIT MANUALLY
```

Phải có:

- Command generate.
- Input source.
- Output path.
- Deterministic generation.
- CI drift check.

Không sửa generated OpenAPI, client hoặc schema trực tiếp nếu có source generator.

---

# 35. Documentation drift

Drift là release blocker khi liên quan:

- Authorization.
- Scope.
- Field masking.
- Financial invariant.
- Source of Truth.
- Customer identity.
- Commercial Lock.
- Immutable Receipt.
- API/Event contract.
- Database constraint.
- Metric definition.
- Migration/recovery.
- Production runbook.

Khi phát hiện:

1. Ghi issue.
2. Xác định canonical source.
3. Xác định code hoặc docs sai.
4. Sửa đúng source.
5. Thêm regression hoặc contract test.
6. Gán owner.
7. Ghi evidence.

---

# 36. Files không nên tạo cạnh tranh

Không tạo lại:

```text
PRD.md ở vị trí khác
PRODUCT_REQUIREMENTS.md
BUSINESS_RULES.md
API_SPEC.md
DATABASE_SCHEMA.md
PERMISSION_SYSTEM.md
WORKFLOWS.md
DEVELOPMENT_PLAN.md
IMPLEMENTATION_ORDER.md
MODULE_SPEC_V2.md
```

nếu nội dung đã có canonical location.

Có thể tạo index dẫn link.

Không copy toàn bộ nội dung canonical sang file khác.

---

# 37. Documentation validation

Các command mục tiêu:

```bash
uv run python scripts/dev.py docs-check
uv run python scripts/dev.py contracts
uv run python scripts/dev.py openapi
uv run python scripts/dev.py events
uv run python scripts/dev.py architecture-check
```

`docs-check` nên kiểm tra:

- Broken links.
- Missing metadata.
- Invalid status/version.
- Missing owner.
- Duplicate ADR/Sprint/Document IDs.
- Superseded file thiếu replacement.
- Forbidden filenames.
- Local absolute paths.
- Secret patterns.
- Markdown lint.
- Generated drift.
- Stale canonical paths.
- Capability/Context registry drift.
- Sprint status contradictions.
- Missing Change Log khi version tăng.

---

# 38. Documentation security

Không commit:

- Credentials.
- API keys.
- Private keys.
- Tokens.
- Production database URLs có credentials.
- Real customer PII.
- Bank details.
- Identity numbers.
- Signed URLs.
- Local absolute paths.
- Raw provider payload chứa dữ liệu nhạy cảm.

Dùng placeholder:

```text
<redacted>
example@example.invalid
0000000000
```

---

# 39. Minimum handoff package cho một Sprint

1. `README.md`.
2. Product Overview.
3. PRD.
4. Domain Glossary.
5. Architecture Overview.
6. Context Map.
7. Source of Truth Matrix.
8. Relevant ADRs.
9. Engineering Constitution.
10. Toolchain Lock.
11. Documentation Governance.
12. Applicable project-local Skills.
13. Relevant Engineering Standards.
14. Relevant Capability Specifications.
15. Relevant Context Implementation Packs.
16. Current Sprint Pack.
17. Previous relevant Acceptance Report.
18. Current Handoff.
19. Repository code, contracts và tests.

Không gửi toàn bộ tài liệu không liên quan khi Context window hạn chế.

---

# 40. Quick Start cho AI Agent

## Bước 1 — Xác định project state

Đọc:

```text
README.md
docs/sprints/sprint-000/sprint-000-preparation-pack.md
docs/roadmap/sprint-roadmap.md
```

Nếu repository work đã bắt đầu, đọc thêm:

```text
docs/project-status.md
docs/handoffs/current-handoff.md
```

## Bước 2 — Xác định Sprint

Chỉ làm Sprint có trạng thái active hoặc được Product/Architecture Owner cho phép.

## Bước 3 — Xác định Capability và Context

Đọc:

```text
docs/product/capabilities/
docs/contexts/<context>/<context>-context-implementation-pack.md
```

## Bước 4 — Đọc Skills

Đọc `SKILL.md` liên quan trong:

```text
.skills/
```

## Bước 5 — Xác định contracts

Kiểm tra:

```text
backend/migrations/
contracts/openapi/openapi.json
contracts/events/
contracts/asyncapi/asyncapi.yaml
docs/security/permission-registry.md
```

## Bước 6 — Inspect code/tests

Không giả định repository giống hoàn toàn Sprint Pack nếu implementation đã tồn tại.

## Bước 7 — Viết plan

Nêu:

- Context owner.
- Files.
- Migrations.
- API.
- Events.
- Permissions.
- UI.
- Jobs.
- Documents.
- Metrics.
- Tests.
- Risks.
- Evidence.

## Bước 8 — Implement và verify

Chạy quality gates thật.

## Bước 9 — Update docs và report

Không kết thúc khi docs chưa đồng bộ.

---

# 41. Definition of Ready cho task

Task chỉ Ready khi:

1. Sprint rõ và được phép thực hiện.
2. Primary Context owner rõ.
3. Participating Contexts rõ.
4. Source of Truth rõ.
5. Capability scope rõ.
6. In Scope/Out of Scope rõ.
7. Relevant ADR Accepted.
8. State machine/invariant đủ rõ.
9. API/Event/Database impact xác định.
10. Permission/scope/masking impact xác định.
11. Idempotency/concurrency impact xác định.
12. Audit/Documents/Integration impact xác định.
13. Test acceptance xác định.
14. Applicable Skills đã xác định.
15. Không có blocking documentation conflict.

---

# 42. Definition of Done cho task

Task chỉ Done khi:

1. Domain behavior đúng.
2. Migration đúng.
3. API/Event contracts cập nhật.
4. Authorization/scope/masking đúng.
5. Idempotency/concurrency đúng.
6. Audit requirements đúng.
7. Documents/Integration boundaries đúng.
8. Tests pass.
9. Architecture boundaries pass.
10. Security scans pass.
11. Documentation cập nhật.
12. Acceptance evidence thật.
13. Current Handoff cập nhật khi repository work đã bắt đầu.
14. Git state rõ.
15. Không còn TODO bắt buộc.
16. Không có hidden failure.
17. Agent báo cáo trung thực.
18. Goose hoặc Acceptance Authority đã review.
19. Acceptance Report PASS khi kết thúc Sprint.

---

# 43. Current Document Registry

## 43.1. Core documents

| Nhóm | Canonical file | Status |
|---|---|---|
| Documentation entry point | `README.md` | In Review |
| Product overview | `docs/product/product-overview.md` | Accepted |
| Product requirements | `docs/product/PRD.md` | Accepted |
| Terminology | `docs/product/domain-glossary.md` | Accepted khi tồn tại và được review |
| Architecture | `docs/architecture/architecture-overview.md` | Accepted |
| Context ownership | `docs/architecture/source-of-truth-matrix.md` | Accepted khi tồn tại và được review |
| Context relationships | `docs/architecture/context-map.md` | Accepted khi tồn tại và được review |
| Engineering behavior | `docs/engineering/ai-agent-engineering-constitution.md` | Accepted |
| Toolchain | `docs/engineering/technology-toolchain-lock.md` | Accepted baseline; Sprint 0 validation required |
| Documentation rules | `docs/engineering/documentation-governance.md` | Accepted |
| Roadmap | `docs/roadmap/sprint-roadmap.md` | Active Roadmap |
| Sprint 0 | `docs/sprints/sprint-000/sprint-000-preparation-pack.md` | Ready for Review |
| Sprint 1 | `docs/sprints/sprint-001/sprint-001-execution-pack.md` | Planned / Not Active |
| Sprint 2 | `docs/sprints/sprint-002/sprint-002-execution-pack.md` | Planned / Not Active |
| Sprint 3 | `docs/sprints/sprint-003/sprint-003-execution-pack.md` | Planned / Not Active |
| Project status | `docs/project-status.md` | Create when repository work starts |
| Current handoff | `docs/handoffs/current-handoff.md` | Create when repository work starts |

## 43.2. Product Capability Specifications

| Capability | Canonical file | Status |
|---:|---|---|
| 01 | `docs/product/capabilities/cap-01-platform-configuration.md` | Accepted Product Capability Baseline |
| 02 | `docs/product/capabilities/cap-02-identity-access-organization.md` | Accepted Product Capability Baseline |
| 03 | `docs/product/capabilities/cap-03-lead-management.md` | Accepted Product Capability Baseline |
| 04 | `docs/product/capabilities/cap-04-customer-360.md` | Accepted Product Capability Baseline |
| 05 | `docs/product/capabilities/cap-05-customer-identity-governance.md` | Accepted Product Capability Baseline |
| 06 | `docs/product/capabilities/cap-06-product-asset-listing-inventory.md` | Accepted Product Capability Baseline |
| 07 | `docs/product/capabilities/cap-07-matching.md` | Accepted Product Capability Baseline |
| 08 | `docs/product/capabilities/cap-08-deal-and-transaction.md` | Accepted Product Capability Baseline |
| 09 | `docs/product/capabilities/cap-09-contract-and-cash.md` | Accepted Product Capability Baseline |
| 10 | `docs/product/capabilities/cap-10-revenue-and-commission.md` | Accepted Product Capability Baseline |
| 11 | `docs/product/capabilities/cap-11-activity-and-engagement.md` | Accepted Product Capability Baseline |
| 12 | `docs/product/capabilities/cap-12-marketing.md` | Accepted Product Capability Baseline |
| 13 | `docs/product/capabilities/cap-13-analytics.md` | Accepted Product Capability Baseline |
| 14 | `docs/product/capabilities/cap-14-runtime-support-overview.md` | Accepted Composite Capability Baseline |

Bảng Registry phải được cập nhật khi tài liệu được tạo, đổi path, đổi version hoặc đổi status.

---

# 44. Documentation Readiness Registry

## 44.1. Global engineering

```text
docs/engineering/coding-standards.md
docs/engineering/database-standards.md
docs/engineering/api-standards.md
docs/engineering/event-standards.md
docs/engineering/testing-standards.md
docs/engineering/security-standards.md
docs/engineering/frontend-standards.md
docs/engineering/observability-standards.md
docs/engineering/error-code-registry.md
```

## 44.2. Architecture

```text
docs/architecture/non-functional-requirements.md
docs/architecture/security-architecture.md
docs/architecture/transaction-boundaries.md
docs/architecture/process-manager-standards.md
```

## 44.3. Security

```text
docs/security/permission-registry.md
docs/security/role-baseline-matrix.md
docs/security/scope-resolution.md
docs/security/field-masking-matrix.md
docs/security/segregation-of-duties.md
docs/security/threat-model.md
docs/security/data-classification.md
docs/security/privacy-and-retention.md
```

## 44.4. Design

```text
docs/design/design-system.md
docs/design/design-tokens.md
docs/design/navigation-and-information-architecture.md
docs/design/dashboard-visualization-system.md
```

## 44.5. Context Packs

Canonical target cho tất cả 16 Contexts:

```text
docs/contexts/<context>/<context>-context-implementation-pack.md
```

Registry trạng thái nên dùng:

```text
Accepted
Ready for Review
Planned
Not Yet Required
Blocked
Superseded
```

Thiếu tài liệu tương lai không block Sprint hiện tại nếu Sprint không phụ thuộc nó.

---

# 45. AI Agent prohibited behaviors

AI Agent không được:

1. Bắt đầu code mà chưa đọc file này.
2. Chọn tài liệu theo tên quen thuộc.
3. Dùng file Superseded.
4. Tạo duplicate canonical file.
5. Tự sửa ADR Accepted.
6. Tự đổi Source of Truth.
7. Tự thêm framework/dependency.
8. Tự tạo permission code không registry.
9. Tự tính official Metric ở frontend.
10. Publish broker trực tiếp từ Domain/Application nếu architecture không cho phép.
11. Direct-write schema Context khác.
12. Dùng Handoff làm business rule.
13. Dùng Project Status làm API/database spec.
14. Ghi secret/PII vào docs.
15. Báo test pass khi chưa chạy.
16. Báo Done khi Acceptance Report chưa đạt.
17. Tạo canonical filename chứa `final/latest/new/copy/v2`.
18. Xóa historical evidence.
19. Sửa test để hợp thức hóa bug.
20. Bỏ qua documentation drift.
21. Biến Capability 14 thành super-context.
22. Tạo Person master trong IAM cạnh tranh với Party.
23. Dùng Hold status thay Product Commercial Lock.
24. Đánh dấu Payment, Receipt hoặc Commission Paid từ frontend.
25. Dùng Analytics projection làm business source.
26. Dùng Marketing Attribution thay Sales Attribution hoặc Commission.
27. Dùng cached consent như quyền liên hệ vĩnh viễn.
28. Dùng Activity Task completion làm business transition.
29. Dùng Operations/Data Repair để bỏ qua owning Context invariants.
30. Tuyên bố Sprint active hoặc completed trái Registry.

---

# 46. AI Agent first response template

```markdown
## Understanding

- Product:
- Current Sprint:
- Sprint Status:
- Primary Capability:
- Primary Context:
- Participating Contexts:
- Source of Truth:
- Relevant ADRs:
- Applicable Skills:
- In Scope:
- Out of Scope:

## Documents Reviewed
- ...

## Repository Inspection
- Current branch:
- HEAD:
- Migration head:
- Relevant code:
- Relevant tests:
- Contract versions:

## Planned Changes
- Domain:
- Database:
- API:
- Events:
- Permissions:
- UI:
- Jobs:
- Integration:
- Documents:
- Analytics:
- Tests:
- Documentation:

## Risks / Conflicts
- ...
```

Agent không hỏi lại thông tin đã rõ trong canonical documents.

---

# 47. Change control

Mọi thay đổi file này phải:

1. Tăng version theo semantic documentation versioning.
2. Ghi Change Log.
3. Cập nhật Current Document Registry.
4. Review bởi Architecture Owner.
5. Review bởi Technical Owner.
6. Review bởi Product Owner khi thay product hoặc capability meaning.
7. Không làm mất history.
8. Không thay precedence âm thầm.
9. Kiểm tra broken links và stale paths.
10. Kiểm tra Sprint status contradictions.
11. Kiểm tra Capability/Context ownership drift.

---

# 48. Change Log

## Version 1.0.0 — 2026-08-05

- Phát hành bộ tài liệu Greenfield đầu tiên cho `crm_bds_ai`.
- Khóa 14 Product Capabilities và 16 Bounded Contexts.
- Khóa root `README.md` làm entry point canonical duy nhất.
- Khóa Source of Truth, Context Map, ADR, security registries và Context Pack baselines.
- Bổ sung Goose/Opencode prompts, open-decision register, implementation blueprints, contract templates và readiness gates.
- Không kế thừa code, schema, API hoặc compatibility layer từ hệ thống tiền nhiệm.

---

# 49. Kết luận

`README.md` là bản đồ bắt buộc để mọi AI Agent hiểu cùng một hệ thống và đưa ra cùng một quyết định đúng.

```text
One Entry Point
+ One Reading Order
+ One Canonical Source per Subject
+ One Context Owner per Data Concept
+ One Contract per Interface
+ One Current Sprint State
+ Capability and Context Separation
+ Traceable Decisions
+ Executable Evidence
```

> Không đọc ngẫu nhiên. Không suy diễn ownership. Không tạo nguồn chân lý thứ hai. Không biến Capability thành super-context. Không tuyên bố hoàn thành khi contract, test, tài liệu và bằng chứng chưa đồng bộ.


# AI architecture baseline

This repository includes a provider- and model-agnostic AI Copilot foundation under `docs/ai/` and `contracts/ai/`. AI is optional, uses capability-based routing, cannot own business truth, and must preserve all canonical business rules and anti-pattern prohibitions.

Mandatory AI reading before AI implementation:

1. `docs/product/canonical-business-rules.md`
2. `docs/product/business-rule-anti-patterns.md`
3. `docs/product/canonical-requirements-registry.md`
4. `docs/ai/README.md`
5. ADR-022 through ADR-025
6. `docs/implementation/ai-readiness-gate.md`
