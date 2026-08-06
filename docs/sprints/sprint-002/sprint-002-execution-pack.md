# CRM_BDS_AI — SPRINT 2 EXECUTION PACK

## Database Reliability and Event Delivery Foundation

**Document ID:** `SPRINT-002-EXECUTION-PACK`  
**Canonical path:** `docs/sprints/sprint-002/sprint-002-execution-pack.md`  
**Product:** `crm_bds_ai`  
**Version:** `1.0.0`  
**Status:** `Planned / Not Active`  
**Activation condition:** `Sprint 0 and Sprint 1 Acceptance Reports = PASS`  
**Sprint type:** `Cross-cutting Reliability Foundation`  
**Technical namespace:** `infra`  
**Owning business Contexts for Sprint scope:** `audit`, `operations`  
**Consumers:** all 16 Bounded Contexts  
**Owner:** `Engineering Reliability Owner`  
**Reviewers:** `Architecture Owner`, `Database Owner`, `Event Architecture Owner`, `Security Owner`, `Audit Owner`, `Operations Owner`, `QA Owner`  
**Effective date:** `2026-08-05`  
**Supersedes:** `None — Greenfield baseline`  
**Classification:** `INTERNAL`

---

# 1. Mục đích

Sprint 2 tạo nền tảng đảm bảo rằng business state, event delivery, command idempotency và audit evidence không bị xử lý theo các cơ chế khác nhau ở từng Context.

Nền tảng phải hỗ trợ:

```text
Command
→ authorization context
→ idempotency guard
→ Unit of Work
→ business/technical state + audit fact + Outbox
→ PostgreSQL commit
→ publisher
→ broker
→ consumer Inbox
→ idempotent handler
→ projection/side effect
```

Sprint 2 không tạo business aggregate của các Sprint sau.

---

# 2. Sprint Goal

> Thiết lập schema-per-context database foundation, Unit of Work, Transactional Outbox, Consumer Inbox, command idempotency, Event contract runtime, append-only Audit foundation và operational diagnostics với migrations, contracts và tests đủ để mọi Context sau sử dụng thống nhất.

---

# 3. Authority and mandatory reading

```text
README.md
docs/product/product-overview.md
docs/product/PRD.md
docs/product/domain-glossary.md
docs/architecture/architecture-overview.md
docs/architecture/context-map.md
docs/architecture/source-of-truth-matrix.md
docs/engineering/ai-agent-engineering-constitution.md
.skills/universal-ai-engineering-orchestration/SKILL.md
docs/engineering/documentation-governance.md
docs/engineering/technology-toolchain-lock.md
Relevant Accepted ADRs
Relevant Engineering Standards
Relevant Context Implementation Pack
Current Sprint Execution Pack
Current Project Status and Handoff, when they exist
Existing machine-readable contracts, migrations, code and tests, when they exist
```

Ngoài ra bắt buộc đọc:

```text
docs/engineering/database-standards.md
docs/engineering/event-standards.md
docs/engineering/api-standards.md
docs/engineering/testing-standards.md
docs/engineering/security-standards.md
docs/engineering/observability-standards.md
Relevant Audit and Operations Context documents, when accepted
Sprint 1 Acceptance Report
```

Quy tắc exact authority:

- Exact DDL: Alembic migrations.
- Exact API operations: OpenAPI.
- Exact Event envelope/payload: JSON Schema + AsyncAPI.
- Exact permission/error codes: registries.
- Exact queue/topology/runtime values: Toolchain Lock + environment configuration/IaC.
- Sprint Pack này quy định outcomes, boundaries và artifacts bắt buộc; không thay thế các nguồn exact trên.

---

# 4. Preconditions

Goose MUST xác minh:

1. Sprint 0 và Sprint 1 Acceptance Reports là `PASS`.
2. Repository clean hoặc worktree state được ghi rõ.
3. Toolchain services healthy theo repository check command.
4. Alembic baseline ở expected head.
5. OpenAPI/AsyncAPI/JSON Schema validation baseline pass.
6. Backend, worker và local infrastructure shells hoạt động.
7. No unapproved Toolchain change.
8. Database/Event/Audit decisions không có unresolved blocker.
9. Current Sprint pointer là Sprint 2.
10. Goose đã tạo design-review gate trước implementation.

Không hard-code version, queue name, timeout, retention hoặc retry count trong Sprint Pack; lấy từ canonical config được phê duyệt.

---

# 5. In Scope

## 5.1. PostgreSQL namespace foundation

Tạo chính xác các schemas canonical:

```text
infra
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

Quy tắc:

- `public` không chứa business table.
- Mỗi Context chỉ có quyền ghi theo ownership đã phê duyệt.
- Cross-schema business writes bị cấm, ngoại trừ controlled shared transaction ports có ADR/contract rõ.
- Role/grant names là environment-specific; privilege semantics là bắt buộc.
- Migration phải test least privilege và rollback behavior.

## 5.2. Transaction and Unit of Work foundation

Triển khai:

- Session/connection lifecycle.
- Transaction-scoped Unit of Work.
- Repository participation without autonomous commit.
- Commit/rollback semantics.
- Transaction context propagation.
- Safe retry boundary cho errors được phân loại retryable.
- After-commit behavior tách khỏi business transaction.

Không cho:

- Router tự commit.
- Repository tự commit.
- External provider call trong database transaction.
- Retry toàn bộ command mù quáng khi side effect không idempotent.

## 5.3. Transactional Outbox

Mandatory Sprint decision:

- Durable Outbox store nằm trong `infra` schema.
- Outbox insert cùng transaction với state/audit cần phát Event.
- Publisher claim an toàn với nhiều worker.
- Message chỉ được xem là published khi transport acceptance theo approved adapter đã được xác nhận.
- Retryable và permanent failure được phân biệt.
- Backlog, attempts và terminal failure observable.
- Replay/reconciliation phải có controlled path.

Exact table/columns/indexes/status values thuộc Alembic và Context database spec được tạo trong Sprint.

## 5.4. Consumer Inbox

Mandatory Sprint decision:

- Durable Inbox store nằm trong `infra` schema.
- Idempotency key tối thiểu theo logical consumer + Event identity.
- Duplicate delivery không tạo duplicate side effect.
- Handler transaction và Inbox completion có atomicity phù hợp use case.
- Payload identity conflict được phát hiện.
- Retry/permanent failure và reconciliation được phân loại.

Exact consumer naming và storage contract phải được ghi trong Event Registry/implementation docs.

## 5.5. Command idempotency

Triển khai shared capability cho commands được policy đánh dấu idempotent:

- Operation scope.
- Idempotency key.
- Canonical request fingerprint.
- Acquire/in-progress/replay/conflict behavior.
- Safe result reference hoặc minimized replay payload.
- Concurrent duplicate handling.
- Cleanup/retention hook.
- Audit/metrics without leaking sensitive payload.

Business-specific policy cho Booking, Payment, Receipt và các Context khác vẫn thuộc Context Pack tương ứng.

## 5.6. Event model and contracts

Triển khai:

- Phân biệt Domain Event và Integration Event.
- Approved common envelope contract.
- Serializer/deserializer boundary.
- Schema validation.
- Handler registry.
- Producer Outbox adapter.
- Consumer Inbox adapter.
- Correlation/causation propagation.
- Compatibility validation.
- Technical pipeline self-test Event.

Exact envelope fields, names và payload nằm trong JSON Schema/AsyncAPI. Sprint Pack không được trở thành payload truth.

## 5.7. Audit foundation

Triển khai:

- Controlled Audit Writer port.
- Append-only Audit storage.
- Actor/context/resource/correlation references phù hợp.
- Sensitive data minimization.
- Runtime privileges không cho update/delete Audit facts.
- Integrity verification foundation.
- Restricted read capability for diagnostics/testing.
- Failure policy rõ đối với critical audited commands.

Exact Audit Event inventory thuộc Audit Context Pack/registry. Sprint 2 chỉ xây foundation và technical evidence.

## 5.8. Operational diagnostics

Operations capability phải quan sát được:

- Outbox backlog/failure.
- Publisher health.
- Consumer failure/lag signal.
- Inbox duplicates/conflicts.
- Idempotency conflicts/stuck operations.
- Audit write/integrity status.
- Technical pipeline self-test result.

Exact metric names, labels, thresholds, dashboard layout và alerts thuộc Observability catalogs/SLO/configuration.

## 5.9. Internal diagnostics interfaces

Cung cấp internal, restricted operations cho:

- Health summary.
- Backlog/failure summary.
- Technical pipeline self-test.
- Approved reconciliation/retry command where safe.

Exact paths, methods, request/response và errors MUST được khai báo trong OpenAPI. Không expose public Outbox/Inbox CRUD.

## 5.10. Documentation and runbooks

Tạo hoặc cập nhật:

```text
docs/sprints/sprint-002/implementation-notes.md
docs/sprints/sprint-002/acceptance-report.md
docs/contexts/audit/ relevant foundation docs
docs/contexts/operations/ relevant foundation docs
contracts/events/ relevant JSON Schemas
contracts/asyncapi/asyncapi.yaml
contracts/openapi/ generated contract
runbooks for backlog, terminal failure and technical self-test
```

---

# 6. Mandatory Sprint decisions versus delegated details

| Subject | Classification | Source |
|---|---|---|
| All canonical schemas exist | Mandatory Sprint Decision | Alembic executes |
| Outbox same-transaction persistence | Mandatory Architecture/Sprint Decision | ADR + code/tests |
| Inbox idempotent consumer handling | Mandatory Architecture/Sprint Decision | Event contracts + code/tests |
| Command idempotency shared capability | Mandatory Sprint Decision | code + policy contracts |
| Audit append-only | Mandatory Architecture Decision | Audit Context + DB grants/tests |
| Exact tables/columns/indexes | Exact implementation | Alembic |
| Exact Event envelope/payload | Exact implementation | JSON Schema + AsyncAPI |
| Exact internal endpoints | Exact implementation | OpenAPI |
| Exact permissions/errors | Exact implementation | registries |
| Retry counts/delays/timeouts | Environment/runtime decision | config/SLO |
| Queue/exchange/routing topology | Environment/runtime decision | Toolchain/IaC/AsyncAPI bindings |
| Retention/archival periods | Policy decision | retention policy/config |
| Metrics/alerts | Observability decision | catalogs/SLO |

Goose MUST not fill delegated cells from examples without approval.

---

# 7. Out of Scope

Sprint 2 MUST NOT triển khai:

- Enterprise, Legal Entity hoặc Business Calendar.
- Organization, User, Role, Permission, Scope resolver hoặc OIDC.
- Party, Customer, Lead, Project, Asset, Listing, Deal, Booking, Contract, Payment, Revenue hoặc Commission.
- Business Events của future Contexts.
- Event sourcing.
- Separate CQRS database.
- Microservices.
- Distributed transaction.
- Business Saga/Process Manager.
- Public Outbox/Inbox APIs.
- User-facing Outbox/Audit administration UI.
- Production WORM archive, SIEM hoặc long-term legal retention implementation.
- A second broker/cache framework.
- Speculative partitioning.
- Provider calls inside transaction.
- Exact future idempotency policies.

---

# 8. Required implementation artifacts

Implementation MUST include exact artifacts equivalent to:

- Alembic revisions for schemas and reliability stores.
- Database roles/grants or environment-compatible privilege scripts.
- Unit of Work implementation.
- Outbox repository/publisher.
- Inbox guard/consumer integration.
- Idempotency service/integration.
- Event envelope/schema tooling.
- Audit Writer/storage foundation.
- Internal diagnostics.
- Tests.
- Runbooks.
- OpenAPI/AsyncAPI/JSON Schema updates.
- Implementation notes and Acceptance Report.

Exact file tree MUST be documented after design review; không ép mọi repository dùng file tree ví dụ từ tài liệu cũ.

---

# 9. Suggested micro-task graph

1. Design review and exact contract proposal.
2. Schema creation and privilege baseline.
3. Unit of Work and transaction tests.
4. Outbox persistence and rollback tests.
5. Publisher claim/publish/recovery tests.
6. Event envelope/schema/registry tooling.
7. Inbox and duplicate-delivery tests.
8. Command idempotency and concurrent duplicate tests.
9. Audit Writer, append-only grants and integrity tests.
10. Diagnostics and technical self-test.
11. Failure/restart/reconciliation tests.
12. Full contract/architecture/security verification.
13. Documentation and Acceptance Report.

Goose MAY parallelize only tasks with no shared migration/contract/file conflict.

---

# 10. Test matrix

## 10.1. Transaction atomicity

- State + Audit + Outbox commit together where required.
- Rollback removes all uncommitted effects.
- Repository cannot independently commit.
- Failure before commit does not publish.
- Failure after commit is recoverable by publisher.

## 10.2. Publisher concurrency and recovery

- Multiple workers do not publish the same claimed row concurrently beyond allowed at-least-once behavior.
- Process death after claim is recoverable.
- Broker rejection does not mark published.
- Duplicate publish is tolerated by consumers.
- Terminal failure becomes observable and reconcilable.

## 10.3. Inbox

- Same Event delivered repeatedly creates one logical effect.
- Different consumers may independently process same Event.
- Handler failure does not falsely mark success.
- Crash windows are exercised.
- Payload identity conflict is detected.

## 10.4. Idempotency

- Same key + same fingerprint returns/references same accepted result.
- Same key + different fingerprint conflicts.
- Concurrent same-key requests do not execute command twice.
- Stuck/in-progress recovery follows approved policy.
- Sensitive result is minimized and redacted.

## 10.5. Audit

- Runtime writer can append.
- Runtime writer cannot update/delete.
- Audit failure policy is tested.
- Sensitive fields are absent/redacted.
- Integrity verification detects tampering in test environment.

## 10.6. Database

- Clean upgrade.
- Downgrade/compensation verification according to Database Standards.
- Re-upgrade.
- Constraints/indexes tested on PostgreSQL, not SQLite.
- Privilege tests use representative runtime roles.

## 10.7. Contracts and architecture

- OpenAPI valid/deterministic.
- JSON Schemas valid.
- AsyncAPI valid and aligned.
- Compatibility check pass.
- No Domain dependency on transport/ORM.
- No business Context directly publishes broker or creates its own competing Outbox.

## 10.8. Operational failure

- Database unavailable.
- Broker unavailable.
- Consumer crash.
- Publisher restart.
- Backlog accumulation.
- Invalid schema/payload.
- Terminal failure/reconciliation path.

Exact test volumes and timing thresholds come from Testing Standards/NFR or Sprint test plan, not examples.

---

# 11. Security and privacy

- Least-privilege DB access.
- Internal diagnostics require approved service/user authorization.
- No raw secret, token, full PII, document content or unbounded request body in Outbox/Inbox/Idempotency/Audit by default.
- Replay and retry operations are privileged and audited.
- Payload validation occurs before handler execution.
- Error responses do not expose internal database/broker details.
- No arbitrary user-controlled routing/handler name.
- Test data is synthetic.

---

# 12. Observability

Signals MUST cover:

- Transaction outcome.
- Outbox pending/age/publish outcome.
- Consumer processing outcome and lag/freshness signal.
- Inbox duplicate/conflict.
- Idempotency acquire/replay/conflict/stuck.
- Audit append/integrity outcome.
- Technical self-test result.

Signals MUST avoid high-cardinality/PII labels. Exact catalog entries are created in the Observability Catalog.

---

# 13. Risks

| Risk | Required control |
|---|---|
| State committed but Event lost | Same-transaction Outbox + recovery test |
| Duplicate publish/consume | At-least-once design + Inbox/idempotent handler |
| Concurrent same command | Idempotency and database concurrency control |
| Audit mutation | Privileges + append-only tests |
| PII copied into infrastructure stores | Minimization + schema/review/tests |
| Publisher/consumer race | Claim/locking protocol + concurrency tests |
| Runtime values hard-coded | Config authority + no numeric assumptions in pack |
| Shared foundation becomes cross-context backdoor | Ports, ownership and architecture tests |

---

# 14. Definition of Ready

Sprint 2 Ready khi:

1. Sprint 1 PASS.
2. Reliability design review scheduled/approved.
3. Database/Event/Audit standards accepted.
4. Toolchain services available.
5. No blocking ADR conflict.
6. Exact contract work has owners.
7. Test environments support real PostgreSQL and broker.
8. Goose has task graph and allowed-file boundaries.

---

# 15. Definition of Done

Sprint 2 chỉ Done khi:

1. Canonical schemas exist via Alembic.
2. Unit of Work semantics verified.
3. Outbox atomicity and publisher recovery verified.
4. Inbox duplicate delivery verified.
5. Command idempotency concurrency verified.
6. Event schemas/AsyncAPI/OpenAPI are valid and aligned.
7. Audit append-only privilege and integrity foundation verified.
8. Diagnostics and technical pipeline self-test pass.
9. Architecture/security/contract tests pass.
10. Full repository quality gates and CI pass.
11. Runbooks and docs updated.
12. Acceptance Report contains exact commands/results.
13. No business entities/events outside scope.
14. Sprint 3 remains inactive until review.

---

# 16. Acceptance Report

`docs/sprints/sprint-002/acceptance-report.md` MUST include:

- Commit range/hash.
- Migrations and database revision.
- Schema/privilege evidence.
- UoW atomicity evidence.
- Outbox publisher and failure-recovery evidence.
- Inbox/idempotency concurrency evidence.
- Audit append-only/integrity evidence.
- OpenAPI/AsyncAPI/JSON Schema results.
- Architecture/security scans.
- Operational self-test.
- Deviations, exceptions and limitations.
- Final status/sign-off.

---

# 17. Chỉ thị cho Goose và Opencode

## Goose

- Require exact design proposal before migration/code.
- Reject copied exact file tree or numeric values without authority.
- Independently inspect migrations, contracts and tests.
- Run failure/concurrency tests, not only happy path.
- Do not accept “published once” as proof of idempotency.

## Opencode

- Implement only delegated micro-task.
- Do not create future business entities/events.
- Do not publish directly from Domain or transaction.
- Do not add a competing broker/client/foundation.
- Report all commands and unresolved failure windows.

---

# 18. Kết luận

```text
Atomic State and Outbox
+ Idempotent Commands
+ Inbox-Protected Consumers
+ Append-Only Audit
+ Tested Recovery
+ Machine-Readable Contracts
= RELIABILITY_FOUNDATION_READY
```
