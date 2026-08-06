# CRM_BDS_AI — ARCHITECTURE OVERVIEW

## Kiến trúc tổng thể, Bounded Context, ownership và ranh giới kỹ thuật

**Document ID:** `ARCH-OVERVIEW-001`  
**Canonical path:** `docs/architecture/architecture-overview.md`  
**Product:** `crm_bds_ai`  
**Version:** `1.0.0`  
**Status:** `Accepted / Architecture Baseline`  
**Owner:** `Architecture Owner`  
**Reviewers:** `Product Owner`, `Domain Owners`, `Security Owner`, `Database Owner`, `API Owner`, `Event Architecture Owner`, `Operations Owner`, `Frontend Owner`, `QA Owner`  
**Effective date:** `2026-08-05`  
**Last reviewed:** `2026-08-05`  
**Supersedes:** `None — Greenfield baseline`  
**Classification:** `INTERNAL`

---

# 1. Mục đích tài liệu

Tài liệu này xác định:

- Hướng kiến trúc tổng thể của `crm_bds_ai`.
- Các architectural drivers.
- Bounded Context và trách nhiệm cấp cao.
- Dependency direction.
- Data ownership.
- Cross-context communication.
- Transaction boundaries.
- Security boundary.
- High-level API/Event/Data architecture.
- Operational và quality boundaries.
- Những quyết định không được thay đổi tùy tiện.

Tài liệu này không định nghĩa:

- Exact database DDL.
- Exact table inventory.
- Exact column type.
- Exact API path hoặc payload.
- Exact response envelope.
- Exact Event inventory hoặc payload.
- Exact permission code.
- Exact queue/exchange topology.
- Exact retry/timeout/retention.
- Exact repository tree.
- Exact framework version.
- Exact Sprint scope.
- Exact deployment topology.

Exact implementation phải được lấy từ các nguồn canonical tương ứng.

---

# 2. Nguồn chân lý kỹ thuật

| Nội dung | Nguồn chân lý |
|---|---|
| Product direction | Product Charter + Product Overview |
| Terms | Domain Glossary |
| Architecture decision | Accepted ADR |
| Context relationship | Context Map |
| Data ownership | Source of Truth Matrix |
| Context invariants | Context Implementation Pack |
| Exact database | Alembic migrations |
| Database principles | Database Standards |
| Exact API | OpenAPI |
| API principles | API Standards |
| Exact Event | JSON Schema + AsyncAPI |
| Event principles | Event Standards |
| Exact permission | Permission Registry |
| Exact scope/masking | Scope Resolution + Field Masking Matrix |
| Tool versions | Technology Toolchain Lock |
| NFR/SLO | NFR + Service Level Objectives |
| Sprint work | Sprint Detailed Execution Pack |
| Completion evidence | Sprint Acceptance Report |

Architecture Overview là nguồn chuẩn cho shape và boundaries, không phải exact contract.

---

# 3. Tuyên bố kiến trúc

`crm_bds_ai` là sản phẩm Greenfield.

Kiến trúc baseline:

```text
Greenfield
Modular Monolith First
Domain-Driven Design
Bounded Context rõ
PostgreSQL schema per Context
REST/OpenAPI cho synchronous business APIs
Domain/Integration Events cho asynchronous propagation
Transactional Outbox
Consumer Inbox
Idempotency
Backend-enforced authorization
Object Storage cho file binary
Read-only Analytics
Append-only Audit
```

Không xây microservices trước khi:

- Context boundaries ổn định.
- Operational capability đủ.
- Data ownership rõ.
- Contract maturity đủ.
- Có business hoặc scale reason rõ.

---

# 4. Architectural drivers

Kiến trúc phải hỗ trợ:

- Enterprise-global Customer identity theo definition đã được chấp nhận.
- Nhiều Legal Entity.
- Party và Customer tách biệt.
- Asset và Listing tách biệt.
- Ownership có effective period.
- Selling Right có lifecycle.
- Product sở hữu Availability.
- Commercial Lock chống double booking.
- Transaction Case quản lý giao dịch đa phía.
- Contract tách khỏi Revenue.
- Payment tách khỏi Revenue Collection.
- Revenue tách khỏi Commission.
- Receipt immutable sau issuance theo policy.
- Customer merge giữ lineage.
- Audit append-only.
- Analytics read-only.
- Integration idempotent và có reconciliation.
- Scope và field masking enforce tại backend.
- Eventual consistency được biểu hiện rõ cho người dùng.

---

# 5. Architectural goals

## 5.1. Correctness

Ưu tiên transaction correctness và business invariants hơn convenience.

## 5.2. Clear ownership

Mỗi loại dữ liệu có một Context owner.

## 5.3. Controlled coupling

Context giao tiếp qua:

- Application Port.
- Public application API.
- Integration Event.
- Process Manager.
- Approved read model.

Không truy cập trực tiếp repository/ORM của Context khác.

## 5.4. Evolvability

Kiến trúc cho phép:

- Thay đổi workflow.
- Thêm transaction model.
- Thêm integration.
- Tách service sau này nếu cần.
- Nâng cấp UI độc lập.
- Mở rộng reporting.

## 5.5. Auditability

Critical operations có lineage, Audit và reconciliation.

## 5.6. Operability

Hệ thống có health, logs, metrics, tracing, alerts, runbooks, backup và restore.

---

# 6. Architectural non-goals

Baseline không nhằm:

- Microservices-first.
- Event sourcing cho mọi Aggregate.
- Distributed transaction.
- Shared database model không ownership.
- Generic CRUD cho sensitive state transitions.
- Frontend-driven authorization.
- SaaS multi-tenant độc lập nếu chưa có ADR.
- Legacy compatibility mặc định.
- Low-code runtime thay thế Domain Model.
- Redis hoặc broker làm business source of truth.
- Analytics write ngược operational Context.
- Central “god module” sở hữu mọi logic.

---

# 7. System shape

Logical architecture:

```text
Web Application / PWA
        ↓
Backend Edge / API Layer
        ↓
crm_bds_ai Modular Monolith
        ├── Platform
        ├── IAM
        ├── Party
        ├── Lead
        ├── Product
        ├── Matching
        ├── Transaction
        ├── Contract
        ├── Revenue
        ├── Activity
        ├── Marketing
        ├── Analytics
        ├── Documents
        ├── Audit
        ├── Integration
        └── Operations
        ↓
PostgreSQL
Event Broker
Valkey-compatible Cache
Object Storage
Workers
Scheduler
External Providers
```

Exact topology và products thuộc Toolchain Lock và Environment Topology.

---

# 8. Architectural style

## 8.1. Modular Monolith

Một deployable backend có nhiều Context modules.

Mỗi Context có:

- Domain.
- Application.
- Infrastructure.
- Presentation/API.
- Tests.
- Migration ownership.
- Event ownership.

## 8.2. DDD layering

Baseline dependency direction:

```text
Presentation
→ Application
→ Domain

Infrastructure
→ implements Application/Domain ports
```

Domain không phụ thuộc:

- Web framework.
- ORM.
- Broker SDK.
- HTTP client.
- Cache SDK.
- Object Storage SDK.
- Provider SDK.

## 8.3. Shared Kernel

Shared Kernel chỉ chứa primitives ổn định và thật sự dùng chung.

Không đưa:

- Customer.
- Listing.
- Deal.
- Contract.
- Revenue.
- Commission.

vào Shared Kernel.

Exact shared types thuộc ADR và Coding Standards.

---

# 9. Bounded Contexts

## 9.1. Platform

Sở hữu:

- Enterprise configuration.
- Legal Entity configuration.
- Business Calendar.
- Numbering policies.
- Configuration versions.
- Workflow/approval definitions.
- Templates và feature configuration.

Không sở hữu:

- User identity.
- Customer.
- Transaction.
- Financial evidence.

## 9.2. IAM

Sở hữu:

- Users.
- Accounts.
- Workforce identity.
- Organization assignments.
- Roles và permissions.
- Access grants.
- Delegation.
- Break-glass authority.
- Scope resolution inputs.

Không sở hữu:

- Customer.
- Lead.
- Product availability.
- Financial approval state của Context khác.

## 9.3. Party

Sở hữu:

- Party.
- Customer.
- Customer roles.
- Customer identity.
- Phone identity.
- Requirement.
- Financial Profile.
- Customer relationships.
- Merge và redirect.

Không sở hữu:

- Lead assignment.
- Listing.
- Deal.
- Contract.
- Revenue.

## 9.4. Lead

Sở hữu:

- Lead.
- Source snapshot.
- Lead assignment.
- Routing.
- Qualification.
- Care protection.
- Lead conversion state.
- Lead closure.

Không sở hữu:

- Canonical Customer identity.
- Requirement after creation.
- Deal.
- Listing.

## 9.5. Product

Sở hữu:

- Partner/project product structures.
- Property Asset.
- Ownership records.
- Selling rights.
- Listing.
- Price/policy versions.
- Inventory.
- Availability.
- Commercial Lock.

Không sở hữu:

- Buyer Deal.
- Booking business process.
- Contract.
- Revenue.

## 9.6. Matching

Sở hữu:

- Matching rules.
- Matching runs.
- Candidate scores.
- Exclusion reasons.
- Shortlists.
- Reverse matching.
- Feedback.

Không sở hữu:

- Requirement source.
- Listing availability source.
- Deal.
- Booking.

## 9.7. Transaction

Sở hữu:

- Deal.
- Deal participants.
- Transaction Case.
- Proposal.
- Negotiation.
- Hold.
- Booking.
- Deposit Commitment.
- Transaction cancellation orchestration.

Không sở hữu:

- Product availability truth.
- Contract.
- Payment.
- Revenue.

## 9.8. Contract

Sở hữu:

- Contract.
- Contract versions.
- Contract parties.
- Payment Schedule.
- Receivable.
- Payment Transaction.
- Payment Allocation.
- Receipt.
- Refund.
- Owner Settlement.
- Contract adjustments/cancellation.

Không sở hữu:

- Revenue entitlement.
- Commission.
- Product Listing.

## 9.9. Revenue

Sở hữu:

- Revenue Arrangement.
- Revenue Entitlement.
- Recognition.
- Revenue Receivable/Collection.
- Revenue adjustments/reversals.
- Commission Plan.
- Commission Entitlement.
- Vesting.
- Payable.
- Payout.
- Clawback.

Không sở hữu:

- Contract.
- Payment source records.
- Receipt.
- Booking.

## 9.10. Activity

Sở hữu:

- Task.
- Appointment.
- Call.
- Interaction.
- Timeline projection.
- SLA instance.
- Escalation.
- Next Best Action.

Không sở hữu operational source state của Context khác.

## 9.11. Marketing

Sở hữu:

- Campaign.
- Channel execution.
- Source taxonomy.
- Tracking.
- Form/submission.
- Audience.
- Suppression.
- Journey.
- Conversion.
- Attribution.
- Spend.

Không sở hữu Customer identity hoặc Lead business state.

## 9.12. Analytics

Sở hữu:

- Projection datasets.
- Metric definitions.
- Metric versions.
- Certified KPIs.
- Dashboard definitions.
- Snapshots.
- Forecasts.
- Data-quality results.

Không được write operational Context state.

## 9.13. Documents

Sở hữu:

- File object metadata.
- Document.
- Document version.
- Verification.
- OCR/extraction.
- Signature evidence.
- Dossier.
- Secure share.
- Legal hold.

Không sở hữu business state của Contract hoặc Product.

## 9.14. Audit

Sở hữu:

- Audit facts.
- Audit archives.
- Integrity checks.

Không cho phép normal business users sửa Audit.

## 9.15. Integration

Sở hữu:

- Connection.
- Mapping version.
- Sync runtime.
- Webhook receipt/delivery.
- Cursor.
- DLQ.
- Replay.
- Integration reconciliation.

Không direct-write operational schemas.

## 9.16. Operations

Sở hữu:

- Job execution metadata.
- Queue operations.
- Service health.
- Incident.
- Maintenance.
- Backup.
- Restore.
- DR drill.
- Data repair request.
- Release/deployment metadata.
- Operational break-glass sessions.

Không sở hữu business data của Context khác.

---

# 10. Stable Context identifiers

Context được định danh bằng stable code:

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

Không dùng module number làm identity kỹ thuật.

Module numbering có thể xuất hiện trong roadmap hoặc tài liệu lịch sử, nhưng không được dùng làm source of truth cho ownership.

---

# 11. Context Map

High-level business flow:

```text
Platform
   ↓
IAM
   ↓
Lead → Party
         ↓
      Product
         ↓
      Matching
         ↓
     Transaction
         ↓
      Contract
         ↓
      Revenue
```

Cross-cutting/support Contexts:

```text
Activity
← consumes relevant business events

Documents
← links to resources through IDs and access policy

Audit
← records sensitive command facts

Marketing
← consumes Lead, Customer, Interaction and conversion facts

Analytics
← consumes Events and builds read-only projections

Integration
← connects external providers through ACL and contracts

Operations
← observes and operates jobs, services, incidents and recovery
```

Exact relationships thuộc Context Map và individual Context Packs.

---

# 12. Dependency rules

## 12.1. Allowed

Context A có thể dùng:

- Application Port.
- Public application service.
- Internal API.
- Integration Event.
- Read model.
- Anti-Corruption Layer.

## 12.2. Forbidden

Context A không được:

- Import repository của Context B.
- Import ORM model của Context B.
- Direct-write schema B.
- Reuse Aggregate B làm internal model.
- Bypass B bằng raw SQL.
- Dựa frontend để đồng bộ business state.
- Dùng broker queue name làm business contract.

## 12.3. Shared reads

Shared reads chỉ qua:

- Owner API.
- Approved read model.
- Projection.
- Snapshot.
- Materialized view có owner rõ.
- Database view có ADR và read-only contract.

---

# 13. Source of Truth summary

| Data | Owning Context |
|---|---|
| Enterprise configuration | Platform |
| User, organization và access | IAM |
| Party, Customer và Requirement | Party |
| Lead và assignment | Lead |
| Asset, Listing, Availability | Product |
| Matching Result | Matching |
| Deal, Transaction Case, Hold, Booking | Transaction |
| Contract, Receivable, Payment, Receipt | Contract |
| Revenue và Commission | Revenue |
| Task, Appointment, Timeline, SLA | Activity |
| Campaign, Audience, Attribution | Marketing |
| Metric, Dashboard, Forecast | Analytics |
| Document và Dossier | Documents |
| Audit fact | Audit |
| Integration runtime | Integration |
| Job, Incident, Backup, Restore | Operations |

Exact matrix thuộc Source of Truth Matrix.

---

# 14. Database architecture

## 14.1. PostgreSQL

Baseline dùng PostgreSQL với schema per Context.

Conceptual schemas:

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
infra
```

## 14.2. Ownership

- Mỗi Context ghi schema của mình.
- Migration có owner.
- Runtime user có least privilege.
- Migration user có DDL authority.
- Analytics không write operational schemas.
- Audit append-only.
- Integration không direct-write business schemas.

## 14.3. Cross-schema foreign keys

Cross-schema FK nghiệp vụ không mặc định.

Có thể dùng hạn chế cho stable platform references nếu ADR cho phép.

Cross-context integrity được bảo vệ bằng:

- Application validation.
- Snapshot.
- Event.
- Process Manager.
- Reconciliation.

## 14.4. Exact DDL

Exact tables, columns, indexes, constraints và types chỉ được định nghĩa bởi:

- Alembic migrations.
- Context DB Specs.
- Database Standards.

Không lấy DDL example trong Architecture Overview làm canonical implementation.

---

# 15. Transaction boundaries

## 15.1. Intra-context

Một business command trong một Context dùng local ACID transaction.

Business state, Audit reference và required Outbox records phải commit theo transaction boundary đã được thiết kế.

## 15.2. Cross-context

Không dùng distributed transaction.

Dùng:

- Event.
- Process Manager.
- Saga.
- Retry.
- Compensation.
- Reconciliation.

## 15.3. Eventual consistency

UI/API phải biểu hiện rõ các state như:

```text
PENDING
PROCESSING
PENDING_CONFIRMATION
SYNCHRONIZATION_REQUIRED
RECONCILIATION_REQUIRED
FAILED
ACTION_REQUIRED
```

Exact state codes thuộc Context Pack.

Không báo final success khi downstream required step chưa hoàn tất.

---

# 16. Process Manager

Process Manager được dùng khi workflow:

- Nhiều bước.
- Nhiều Context.
- Có waiting state.
- Có timeout.
- Có compensation.
- Có manual intervention.
- Có financial/legal impact.
- Cần progress tracking.

Potential processes:

- Lead conversion.
- Hold and Booking.
- Contract activation.
- Contract cancellation.
- Customer merge.
- Refund.
- Revenue reversal.
- Commission clawback.
- Document signing.
- External synchronization.

Exact state machine thuộc Process Manager spec và Context Packs.

---

# 17. Event architecture

## 17.1. Principles

Domain Event là fact đã xảy ra trong Context.

Integration Event là versioned contract cho consumer ngoài producer Context.

Producer phải:

- Sở hữu business meaning.
- Dùng Transactional Outbox.
- Publish contract versioned.
- Minimize payload.
- Không chứa secret.
- Hạn chế PII.

Consumer phải:

- Idempotent.
- Dùng Inbox hoặc equivalent.
- Handle duplicate.
- Handle unsupported version.
- Có retry/DLQ/reconciliation phù hợp.

## 17.2. Exact contract

Exact Event names, payload, envelope, version và channels thuộc:

- Event Registry.
- JSON Schema.
- AsyncAPI.
- Event Standards.

Architecture Overview không khóa exact Event inventory.

---

# 18. API architecture

## 18.1. API styles

- REST là baseline cho synchronous business API.
- OpenAPI 3.1 là exact execution contract.
- Sensitive state transition dùng explicit command endpoint.
- Generic PATCH không được dùng để bypass Domain transition.
- Query API dùng bounded pagination/filter/sort.
- Public/internal/webhook APIs có security boundary riêng.

## 18.2. Exact contract

Exact paths, methods, headers, request/response schema, pagination và error payload thuộc:

- OpenAPI.
- API Standards.
- Error Registry.
- Security specifications.

Architecture Overview không khóa exact base path hoặc response envelope.

---

# 19. Security architecture

Backend là security boundary.

Authorization có thể kết hợp:

```text
Authenticated identity
∩ Capability
∩ Effective scope
∩ Enterprise/Legal Entity/Project access
∩ Resource relationship
∩ Resource state
∩ Field policy
∩ Effective period
∩ SoD
∩ Approval limits
```

Nguyên tắc:

- Deny by default.
- Least privilege.
- Scope enforce tại backend query.
- Field masking trước serialization.
- Frontend không grant permission.
- Client-supplied scope/owner không phải authority.
- Sensitive actions có thể yêu cầu reauthentication.
- Break-glass phải controlled và audited.

Exact permissions thuộc Registry/Matrix.

---

# 20. Customer Identity architecture

Customer identity thuộc Party Context.

Architectural invariants:

- Identity boundary theo Enterprise definition đã accepted.
- Duplicate strategy dùng normalized phone overlap theo ADR.
- Shared phone có controlled exception.
- Merge không hard-delete nguồn.
- Redirect được propagate.
- Consumer Context phải handle merge/rebind.
- Search và duplicate check tôn trọng masking/scope.

Exact data model thuộc Party Context Pack và migrations.

---

# 21. Commercial Lock architecture

Product Context là source duy nhất cho Listing availability và Commercial Lock.

Transaction Context không tự quyết định availability.

Required properties:

- Atomic.
- Idempotent.
- Concurrency-safe.
- Version-aware.
- Database-backed final guard.
- Observable.
- Reconciliation-capable.

Exact lock table, index, exclusion constraint hoặc command flow thuộc Product Context Pack, ADR và migrations.

---

# 22. Contract, Payment, Revenue và Commission separation

Architectural boundaries:

```text
Transaction
→ Deal, Hold, Booking

Contract
→ Contract, Receivable, Payment, Receipt, Refund, Settlement

Revenue
→ Revenue entitlement, recognition, collection, Commission, Payout, Clawback
```

Rules:

- Contract không direct-write Revenue tables.
- Revenue không update Payment hoặc Receipt.
- Payment không mặc định là Revenue.
- Receipt không phải Revenue proof duy nhất.
- Commission không đồng nhất với Revenue.
- Analytics không tự recompute official financial truth từ raw operational data.

---

# 23. Documents architecture

Tách:

```text
File Object
→ Document
→ Document Version
→ Dossier
→ Evidence Package
```

Object Storage lưu binary.

Database lưu metadata, storage key, classification, hash, version, verification và access policy.

Business Context chỉ giữ reference.

Exact object-storage implementation thuộc Toolchain/Environment.

---

# 24. Audit architecture

Audit là append-only/protected.

Business command quan trọng phải tạo Audit evidence theo policy.

Audit khác operational log.

Audit phải có:

- Actor/service.
- Resource.
- Action.
- Reason.
- Outcome.
- Correlation.
- Timestamp.
- Integrity protection phù hợp.

Exact Audit schema thuộc Audit Context Pack và migrations.

---

# 25. Analytics architecture

Analytics:

- Read-only đối với operational data.
- Xây projections từ Events/snapshots.
- Quản lý metric definitions/version.
- Có lineage.
- Có freshness.
- Có reconciliation.
- Không write operational Context.

Official KPI đến từ certified metrics.

---

# 26. Integration architecture

Mọi integration phải có:

- Connection.
- Credential reference.
- Mapping version.
- Source-of-truth policy.
- Authentication/signature.
- Idempotency.
- Retry.
- Rate limit.
- Circuit breaker.
- DLQ.
- Replay.
- Reconciliation.
- Health monitoring.

Integration dùng Anti-Corruption Layer.

Raw provider payload không trở thành canonical domain model.

---

# 27. Background processing

Background processing dùng cho:

- Event publishing/consuming.
- Long-running jobs.
- Scheduled work.
- Imports/exports.
- Reconciliation.
- Documents/OCR.
- Notifications.
- External sync.
- Analytics projections.

Business workers phải gọi Application services hoặc approved commands, không direct-write database.

Exact worker framework, queue topology và retry values thuộc Toolchain Lock và Operations configuration.

---

# 28. Cache architecture

Cache:

- Không là source of truth.
- Không mở rộng quyền.
- Không lưu unmasked response across scopes.
- Có invalidation/freshness policy.
- Failure không làm authorization fail-open.
- Không dùng làm final availability guard.

Exact cache technology và TTL thuộc Toolchain/Context configuration.

---

# 29. Frontend architecture

Frontend:

- Dùng generated API client.
- Không là business authority.
- Không là security boundary.
- Hiển thị loading, empty, error, conflict, permission và eventual-consistency states.
- Dùng Design System.
- Tôn trọng accessibility.
- Không tính official KPI hoặc financial truth.
- Không persist restricted data không cần thiết.

Exact framework, routes, components và cache values thuộc Toolchain, Frontend Standards và Design System.

---

# 30. Observability architecture

Mọi critical flow cần:

- Structured logs.
- Metrics.
- Traces khi hữu ích.
- Correlation.
- Business anomaly signals.
- Alerts.
- Runbooks.

Không log secrets hoặc full sensitive payload.

Exact metric inventory, thresholds, sampling và retention thuộc Observability Catalog, SLO và Environment configuration.

---

# 31. Testing architecture

Test layers gồm khi relevant:

- Domain/unit.
- Application.
- PostgreSQL integration.
- Migration.
- API contract.
- Event contract.
- Architecture.
- Security.
- Concurrency.
- Frontend component/integration.
- E2E.
- Performance/failure injection.

Critical database behavior phải dùng PostgreSQL thật.

Exact commands, thresholds và test inventory thuộc Testing Standards, Sprint Pack và CI configuration.

---

# 32. Deployment architecture

Architecture phải hỗ trợ:

- Local development.
- CI.
- Staging/UAT.
- Production.
- Workers.
- Scheduler.
- Database migrations.
- Object Storage.
- Broker.
- Telemetry.
- Backup/restore.
- Rollback.

Exact topology thuộc Environment Topology/IaC.

Architecture Overview không khóa Docker, Kubernetes hoặc cloud provider.

---

# 33. Greenfield policy

`crm_bds_ai` có:

- Repository mới.
- Database mới.
- Migration history mới.
- API/Event contract mới.
- Authorization model mới.
- Frontend mới.
- Worker/scheduler mới.
- CI/CD mới.

Không mặc định:

- Legacy table compatibility.
- API alias cũ.
- Status mapping cũ.
- Database migration từ hệ thống cũ.
- Import code/domain model cũ.

Legacy migration hoặc integration chỉ được triển khai khi có approved scope và specification.

---

# 34. Repository organization principles

Repository phải:

- Thể hiện ownership.
- Tách contexts.
- Tách contracts.
- Tách frontend/backend/infrastructure phù hợp.
- Có architecture tests.
- Có generated artifacts rõ.
- Không tạo circular dependencies.
- Không dùng `shared` làm nơi chứa business logic không owner.

Exact folder tree thuộc Coding Standards và accepted repository state.

---

# 35. Architecture decision governance

Mọi thay đổi architectural baseline cần:

- Problem statement.
- Options.
- Trade-offs.
- Decision.
- Consequences.
- Migration impact.
- Security impact.
- Operational impact.
- ADR.

Không thay đổi bằng code-only PR.

---

# 36. Non-negotiable decisions

Các quyết định sau không được thay tùy tiện:

1. Greenfield product.
2. Modular Monolith first.
3. Bounded Context ownership.
4. PostgreSQL schema per Context.
5. No cross-context repository/ORM import.
6. No direct cross-context business writes.
7. Product owns Availability.
8. Product owns Commercial Lock.
9. Party owns Customer identity.
10. Asset khác Listing.
11. Ownership khác Selling Right.
12. Transaction Case là hồ sơ giao dịch đa phía.
13. Booking cần valid Commercial Lock.
14. Contract tách khỏi Revenue.
15. Payment không mặc định là Revenue.
16. Receipt immutable theo policy.
17. Revenue tách Commission.
18. Customer merge giữ lineage.
19. Analytics read-only.
20. Audit append-only.
21. Backend-enforced authorization.
22. Important side-effect commands idempotent.
23. Cross-context consistency dùng Event/Process Manager/Reconciliation.
24. Không dùng distributed transaction.
25. Không dùng generic PATCH để thay sensitive state.
26. Không microservices-first.
27. File binary nằm Object Storage.
28. Exact contracts machine-readable.

---

# 37. Readiness for implementation

Architecture chỉ được xem là sẵn sàng cho một Context khi:

- Context owner rõ.
- Business invariants rõ.
- Data ownership rõ.
- State machine rõ.
- Commands/queries rõ.
- Security rõ.
- Cross-context dependencies rõ.
- API/Event impact rõ.
- Database boundaries rõ.
- Acceptance criteria rõ.
- Test strategy rõ.
- Không có blocking conflict.

---

# 38. Architecture quality gates

Một architectural change không được accepted nếu:

- Tạo source of truth cạnh tranh.
- Direct-write Context khác.
- Không có ADR khi cần.
- Thiếu security analysis.
- Thiếu migration strategy.
- Thiếu contract changes.
- Không có architecture tests.
- Làm mất history/audit.
- Dùng cache/broker làm source of truth.
- Tạo distributed transaction.
- Tự lock implementation chưa được kiểm chứng.
- Phá Greenfield boundary bằng legacy coupling ngoài scope.

---

# 39. Relationship với các tài liệu khác

## Product Overview

Trả lời:

```text
Xây sản phẩm gì và business truths nào phải đúng.
```

## Architecture Overview

Trả lời:

```text
Hệ thống được chia và bảo vệ ở cấp cao như thế nào.
```

## Context Packs

Trả lời:

```text
Mỗi Context có Aggregate, invariant, command, query và state machine nào.
```

## Machine-readable Contracts

Trả lời:

```text
Exact implementation contract là gì.
```

## Sprint Pack

Trả lời:

```text
Làm gì trong Sprint hiện tại.
```

---

# 40. Conflict protocol

Khi Architecture Overview xung đột với:

- Product Overview.
- ADR.
- Context Map.
- Source of Truth Matrix.
- Context Pack.
- OpenAPI.
- Migrations.
- Event schema.
- Permission Registry.
- Code/tests.

Phải:

1. Dừng phần bị ảnh hưởng.
2. Xác định semantic, architecture hay execution conflict.
3. Áp dụng Documentation Governance.
4. Không tự chọn nguồn thuận tiện.
5. Tạo ADR/change note nếu architecture thay đổi.
6. Cập nhật contracts, code, tests và docs cùng thay đổi.
7. Ghi resolution trong Acceptance Report.

---

# 41. Change Log

## Version 1.1.0 — 2026-07-26

- Tách Architecture Overview khỏi Product Overview.
- Loại bỏ exact DDL, API, Event, queue, runtime thresholds và Sprint plan khỏi tài liệu kiến trúc.
- Dùng stable Context identifiers thay module numbering.
- Làm rõ Greenfield không mặc định compatibility với hệ thống cũ.
- Giữ 16 Bounded Context và ownership.
- Làm rõ Context dependency, transaction boundary và cross-context consistency.
- Chuyển exact implementation về machine-readable contracts và Context Packs.
- Bổ sung source-of-truth table, non-goals, quality gates và conflict protocol.

## Version 1.0

- Xác định Greenfield.
- Modular Monolith first.
- Bounded Context map.
- PostgreSQL schema per Context.
- REST/OpenAPI.
- Domain Events.
- Transactional Outbox.
- Backend authorization.
- Roadmap nền tảng.

---

# 42. Kết luận

Kiến trúc chính thức của `crm_bds_ai` là:

```text
Greenfield
+ Modular Monolith First
+ Domain-Driven Design
+ 16 Bounded Contexts
+ PostgreSQL Schema per Context
+ REST/OpenAPI
+ Domain and Integration Events
+ Transactional Outbox
+ Consumer Inbox
+ Backend-enforced Authorization
+ Object Storage
+ Append-only Audit
+ Read-only Analytics
+ Reconciliation-driven Cross-context Consistency
```

Tài liệu này trả lời:

> Hệ thống được chia thành những phần nào, mỗi phần sở hữu gì và các phần được phép tương tác như thế nào.

Tài liệu này không trả lời:

> Exact table, endpoint, Event payload, permission hoặc Sprint task là gì.


# Provider- and model-agnostic AI addendum

All AI requests cross the canonical AI Gateway. Provider/model adapters live behind Integration/Operations boundaries; Platform manages registries/policies, IAM applies scope/masking, Audit records evidence and owning Contexts execute accepted commands. See ADR-022 through ADR-025 and `docs/ai/`.
