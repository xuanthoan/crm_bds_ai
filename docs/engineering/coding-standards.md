# CRM_BDS_AI — CODING STANDARDS

## Quy chuẩn lập trình và kỷ luật triển khai bắt buộc cho repository `crm_bds_ai`

**Document ID:** `ENG-CODING-001`  
**Canonical path:** `docs/engineering/coding-standards.md`  
**Product:** `crm_bds_ai`  
**Version:** `1.0.0`  
**Status:** `Accepted / Mandatory`  
**Canonical authority:** `Coding principles, dependency boundaries, implementation discipline and review rules`  
**Owner:** `Technical Owner`  
**Reviewers:** `Architecture Owner`, `Security Owner`, `QA Owner`, `Frontend Owner`, `Database Owner`, `Context Owners`  
**Effective date:** `2026-08-05`  
**Last reviewed:** `2026-08-05`  
**Supersedes:** `None — Greenfield baseline`  
**Classification:** `INTERNAL`

---

# 1. Mục đích

Tài liệu này quy định cách viết và tổ chức code trong toàn bộ `crm_bds_ai` nhằm bảo đảm:

1. Domain intent được thể hiện rõ trong code.
2. Bounded Context và layer boundaries không bị phá vỡ.
3. Business invariants không bị thay bằng generic CRUD.
4. Authorization, transaction, idempotency, Audit và Event được triển khai nhất quán.
5. Code có strong typing, dễ đọc, dễ kiểm thử và dễ vận hành.
6. Frontend không trở thành nguồn chân lý nghiệp vụ.
7. Infrastructure details không xâm nhập Domain.
8. AI Agent có đủ quy tắc để thực hiện task mà không phải đoán coding style.
9. Code và tài liệu thay đổi cùng nhau.
10. Implementation thực tế vẫn có thể tiến hóa mà không bị khóa bởi dự đoán quá sớm.

---

# 2. Phạm vi thẩm quyền của tài liệu

## 2.1. Tài liệu này là nguồn chuẩn cho

- Dependency direction.
- Bounded Context boundaries.
- Layer responsibilities.
- Naming và code organization.
- Type-safety discipline.
- Error-handling discipline.
- Transaction, concurrency và idempotency coding patterns.
- Security implementation discipline.
- Audit và Event implementation discipline.
- Testability và review requirements.
- AI Agent implementation protocol.
- Coding anti-patterns bị cấm.

## 2.2. Tài liệu này không phải nguồn chuẩn cho exact implementation contracts

Tài liệu này **không định nghĩa chính xác**:

- Database tables, columns, constraints hoặc indexes.
- API endpoint inventory, exact request hoặc response payload.
- Event payload và routing key inventory.
- Permission codes và role assignments.
- Error-code inventory.
- Aggregate state machines cụ thể.
- Production timeout, pool size, retry count hoặc capacity.
- Sprint file list hoặc commit sequence.
- Exact UI layout của từng feature.

Các nguồn chuẩn tương ứng:

| Nội dung | Nguồn chân lý |
|---|---|
| Domain terms | Domain Glossary |
| Context ownership | Source of Truth Matrix |
| Architecture decisions | Accepted ADRs |
| Aggregate và invariants | Context Implementation Pack |
| Exact database schema | Alembic migrations + database contract docs |
| Exact API contract | OpenAPI 3.1 |
| Exact Event contract | JSON Schema + AsyncAPI |
| Exact permission codes | Permission Registry |
| Exact error codes | Error Code Registry |
| Sprint implementation scope | Current Sprint Detailed Execution Pack |
| Implementation completion | Acceptance Report |
| Current repository state | Code + tests + Project Status + Handoff |

## 2.3. Mọi ví dụ trong tài liệu

Ví dụ code, cấu trúc thư mục và tên class trong tài liệu này là:

```text
ILLUSTRATIVE EXAMPLE
```

trừ khi đoạn đó được gắn rõ là `MUST` hoặc `MUST NOT`.

---

# 3. Từ khóa quy chuẩn

Tài liệu sử dụng các từ khóa:

- **MUST**: Bắt buộc.
- **MUST NOT**: Bị cấm.
- **SHOULD**: Khuyến nghị mạnh; khác biệt cần có lý do.
- **SHOULD NOT**: Nên tránh; khác biệt cần có lý do.
- **MAY**: Được phép tùy use case.
- **RECOMMENDED BASELINE**: Điểm khởi đầu cần được kiểm chứng.
- **ILLUSTRATIVE EXAMPLE**: Ví dụ, không phải exact contract.
- **CONTEXT DECISION**: Phải được khóa trong Context Pack hoặc ADR.
- **ENVIRONMENT DECISION**: Phải được khóa trong deployment/operations configuration.

AI Agent không được chuyển `SHOULD`, `MAY` hoặc ví dụ thành luật tuyệt đối.

---

# 4. Thứ tự ưu tiên khi có xung đột

Áp dụng precedence trong `docs/engineering/documentation-governance.md`.

Nguyên tắc thực thi:

1. Machine-readable contracts quyết định exact executable shape.
2. Accepted ADR quyết định architecture exception.
3. Context Pack quyết định domain behavior của Context.
4. Sprint Pack quyết định phạm vi công việc hiện tại.
5. Coding Standards quyết định implementation discipline.
6. Code và tests phải phản ánh các nguồn trên.

Khi phát hiện xung đột:

- MUST dừng phần bị ảnh hưởng.
- MUST ghi conflict rõ.
- MUST xác định source có thẩm quyền.
- MUST cập nhật tài liệu hoặc contract cùng change.
- MUST NOT âm thầm chọn một phía.

---

# 5. Nguyên tắc tối cao

```text
Correctness
> Domain Integrity
> Security
> Data Integrity
> Auditability
> Reliability
> Maintainability
> Performance
> Developer Convenience
```

Code ngắn hơn không có giá trị nếu làm mất domain meaning, security boundary, transaction guarantee hoặc khả năng kiểm thử.

---

# 6. Kiến trúc nền tảng

`crm_bds_ai` là Modular Monolith gồm các Bounded Context:

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

Mỗi Context:

- MUST sở hữu domain model của mình.
- MUST sở hữu application use cases của mình.
- MUST sở hữu persistence implementation của mình.
- MUST NOT import repository hoặc ORM model của Context khác.
- MUST NOT direct-write schema của Context khác.
- MUST giao tiếp qua application port, internal API, domain/integration event hoặc approved process manager.

---

# 7. Ngôn ngữ và thuật ngữ

## 7.1. Identifiers

Code identifiers MUST dùng English:

- Module.
- Package.
- Class.
- Function.
- Variable.
- Database identifiers.
- API operation IDs.
- Event types.
- Permission codes.
- Error codes.

## 7.2. Documentation và UI

- Documentation chính MAY dùng tiếng Việt.
- UI ưu tiên tiếng Việt theo product scope.
- Stable codes vẫn dùng English.
- Domain terms MUST theo Domain Glossary.

## 7.3. Không tạo từ đồng nghĩa tùy ý

Ví dụ, khi Glossary định nghĩa `CommercialLock`, code MUST NOT dùng xen kẽ:

```text
InventoryLock
ReservationLock
StockLock
```

nếu không có distinction chính thức.

---

# 8. Repository organization

## 8.1. Nguyên tắc

Repository MUST làm rõ:

- Context ownership.
- Dependency direction.
- Contracts.
- Migrations.
- Shared technical foundations.
- Tests.

## 8.2. Reference layout

Đây là **ILLUSTRATIVE REFERENCE**, không phải yêu cầu tạo mọi thư mục từ đầu:

```text
backend/
├── contexts/
│   └── <context>/
│       ├── domain/
│       ├── application/
│       ├── infrastructure/
│       ├── presentation/
│       └── tests/
├── shared/
├── migrations/
├── scripts/
└── tests/

apps/web/
├── app/
├── features/
├── components/
├── lib/
└── tests/

contracts/
├── openapi/
├── events/
├── asyncapi/
└── schemas/
```

Rules:

- MUST NOT tạo thư mục rỗng chỉ để giống template.
- MAY thay đổi layout nếu có ADR hoặc repository convention đã accepted.
- MUST giữ Context ownership rõ dù layout thay đổi.

---

# 9. Dependency direction

Canonical direction:

```text
presentation → application → domain
infrastructure → application/domain ports
```

## 9.1. Domain MUST NOT phụ thuộc

- FastAPI.
- Pydantic transport schemas.
- SQLAlchemy.
- RabbitMQ hoặc Celery.
- Valkey.
- HTTP client.
- Object storage SDK.
- OpenTelemetry SDK.
- Next.js hoặc React.
- Environment variables.
- ORM models.

## 9.2. Application MUST NOT phụ thuộc

- HTTP router.
- Framework-specific request object.
- Concrete database session nếu port/UoW abstraction đã được định nghĩa.
- Frontend presentation types.

## 9.3. Infrastructure MAY phụ thuộc

- Frameworks.
- SDKs.
- ORM.
- Broker.
- Storage.
- Application ports.
- Domain types cần thiết.

## 9.4. Presentation MAY phụ thuộc

- Application use cases.
- Request/response mapping.
- Authentication context adapter.

Presentation MUST NOT chứa business invariant.

---

# 10. Shared code policy

`shared` chỉ dành cho capabilities thật sự dùng chung và không thuộc domain của một Context.

Shared technical capabilities MAY bao gồm:

- Clock.
- UUID provider.
- Error primitives.
- Unit of Work abstractions.
- Idempotency foundation.
- Outbox/Inbox foundation.
- Pagination primitives.
- Observability helpers.
- Authentication context types.

Shared MUST NOT trở thành nơi chứa:

```text
common business services
generic domain entities
all-purpose utils
shared repositories for multiple Contexts
```

Một abstraction chỉ được đưa vào shared khi có ít nhất một use case rõ và ownership rõ.

---

# 11. Module API và imports

- Mỗi module/feature SHOULD expose public API rõ.
- External modules SHOULD import qua public API, không import sâu vào internals.
- Circular imports MUST NOT được xử lý bằng import động tùy tiện.
- Relative imports SHOULD được dùng nhất quán theo repository convention.
- Star imports MUST NOT được dùng.
- Import side effects MUST NOT tạo connection, schedule job hoặc mutate global state.

---

# 12. Python coding baseline

Exact formatter, linter và type-checker versions theo Toolchain Lock và repository configuration.

Python code MUST:

- Có type annotations cho public functions và methods.
- Tránh implicit `Any`.
- Dùng `from __future__ import annotations` nếu repository convention yêu cầu.
- Dùng timezone-aware datetime.
- Dùng `Decimal` cho money.
- Dùng immutable value objects khi phù hợp.
- Dùng explicit exception types.
- Tránh mutable default arguments.

Python code MUST NOT:

```python
def f(items=[]): ...
```

hoặc:

```python
except Exception:
    pass
```

---

# 13. Functions và methods

Một function SHOULD:

- Có một responsibility chính.
- Có tên thể hiện intent.
- Có bounded parameters.
- Có return type rõ.
- Không mutate input bất ngờ.
- Không che side effect.

Không có giới hạn dòng tuyệt đối cho mọi function.

Review cần xem xét tách function khi:

- Có nhiều nhánh nghiệp vụ không liên quan.
- Khó đặt tên.
- Cần nhiều comments để hiểu flow.
- Khó test độc lập.
- Trộn validation, persistence, external calls và mapping.

---

# 14. Classes

Class SHOULD đại diện cho:

- Domain concept.
- Application use case.
- Infrastructure adapter.
- Presentation mapper/controller.

Class MUST NOT chỉ là namespace cho static helpers nếu module-level functions rõ hơn.

Tên bị tránh:

```text
Manager
Processor
Helper
Utils
CommonService
GenericService
```

trừ khi responsibility cụ thể được thể hiện đầy đủ, ví dụ `BookingConfirmationProcessManager`.

---

# 15. Naming

Tên phải mô tả business intent hoặc technical responsibility.

Tốt:

```text
ActivateListingHandler
IssueReceiptHandler
CommercialLockConflictError
CalculateBusinessDuration
ResolveCanonicalCustomer
```

Kém:

```text
ProcessData
HandleStuff
UpdateEntity
DoAction
GenericHandler
```

Booleans SHOULD dùng prefix:

```text
is_
has_
can_
should_
```

Collections SHOULD dùng plural nouns.

---

# 16. Comments và docstrings

Comments SHOULD giải thích:

- Tại sao.
- Constraint không hiển nhiên.
- Security hoặc concurrency reasoning.
- External provider quirk.
- Temporary compatibility rule.

Comments SHOULD NOT lặp lại code.

Public abstractions, non-obvious domain policies và adapters SHOULD có docstring.

Comments hoặc docstrings MUST NOT chứa secret hoặc production PII.

---

# 17. TODO và temporary code

TODO chỉ hợp lệ khi có:

```text
issue/reference
owner
reason
expiry hoặc target Sprint
```

Temporary code MUST NOT:

- Bypass security.
- Weaken invariant.
- Disable Audit.
- Disable idempotency.
- Introduce data corruption risk.

---

# 18. Domain model

Domain code MUST:

- Thể hiện ubiquitous language.
- Bảo vệ invariant.
- Quản lý state transition.
- Tạo Domain Events khi cần.
- Không phụ thuộc infrastructure.

Domain code SHOULD ưu tiên:

- Aggregate methods có intent.
- Value Objects.
- Typed enums.
- Explicit policies.
- Immutable records cho facts/history.

Domain MUST NOT là tập hợp dataclasses không behavior nếu invariant tồn tại.

---

# 19. Aggregate rules

Aggregate Root MUST:

- Là entry point cho mutation trong aggregate boundary.
- Bảo vệ invariant nội aggregate.
- Không expose mutable collections trực tiếp.
- Không cho caller set status tùy ý.
- Không biết repository hoặc HTTP.

Đúng:

```python
booking.confirm(...)
receipt.cancel_and_replace(...)
listing.activate(...)
```

Sai:

```python
booking.status = "CONFIRMED"
```

Exact states và transitions thuộc Context Pack.

---

# 20. Entities

Entity:

- Có identity.
- Equality semantics phải rõ.
- Mutation phải đi qua behavior có ý nghĩa.
- Không expose setters cho mọi field mặc định.

Entity con trong Aggregate MUST NOT được repository-save độc lập nếu aggregate boundary không cho phép.

---

# 21. Value Objects

Value Object SHOULD:

- Immutable.
- Validate khi tạo.
- So sánh theo value.
- Không có technical ID nếu không cần.
- Encode business semantics.

Examples:

```text
Money
CurrencyCode
EffectivePeriod
PhoneIdentity
TimezoneId
```

Examples không định nghĩa inventory bắt buộc cho mọi Context.

---

# 22. Domain Services và Policies

Dùng Domain Service/Policy khi behavior:

- Không thuộc tự nhiên một Entity.
- Cần nhiều domain inputs.
- Vẫn không cần infrastructure side effect.

Domain Service MUST NOT trở thành generic service chứa mọi logic.

---

# 23. Domain Events

Domain Event MUST:

- Là fact đã xảy ra.
- Immutable.
- Past tense.
- Framework-free.
- Không biết broker.

Exact Integration Event mapping thuộc Event Standards và machine-readable contracts.

---

# 24. Domain exceptions

Domain exception phải:

- Thể hiện invariant/business conflict.
- Có stable semantic identifier hoặc mapping path.
- Không chứa HTTP status.
- Không chứa SQL/provider details.

Example:

```python
class CommercialLockConflict(DomainError):
    pass
```

---

# 25. Application layer

Application layer chịu trách nhiệm:

- Orchestration.
- Authorization use-case boundary.
- Idempotency acquisition/completion.
- Unit of Work.
- Aggregate loading.
- Domain invocation.
- Audit fact creation.
- Outbox persistence.
- DTO result mapping.

Application layer MUST NOT chứa infrastructure-specific exception handling ngoài adapter error abstraction.

---

# 26. Commands

Command:

- Mô tả intent thay đổi state.
- Typed.
- Không chứa trusted actor/scope từ client body.
- Không chứa framework request object.
- Không generic `UpdateEntityCommand` nếu có business intent cụ thể.

Đúng:

```text
ConfirmBooking
ActivateListing
IssueReceipt
ApproveRefund
```

Sai:

```text
UpdateBookingStatus
PatchRecord
```

---

# 27. Command handlers

Handler SHOULD có flow rõ:

```text
resolve trusted context
→ authorize
→ acquire idempotency if required
→ load aggregate
→ execute domain behavior
→ persist aggregate and supporting facts
→ write Audit and Outbox
→ commit
→ return typed result
```

Handler MUST NOT:

- Gọi external network trong DB transaction nếu không có approved design.
- Publish broker trực tiếp.
- Update Context khác.
- Trust owner/scope từ request.

---

# 28. Queries

Query handlers:

- MUST enforce EffectiveScope trong query.
- SHOULD dùng projections cho list/read-heavy use cases.
- MUST NOT load tất cả rồi filter permission bằng Python.
- MUST NOT mutate business state.
- SHOULD select only needed fields.

Exact query shape và indexes thuộc Context/DB contracts.

---

# 29. DTOs

DTOs:

- Là typed data contracts giữa layers.
- Không phải Domain Entity.
- Không phải ORM model.
- Không chứa lazy-loading behavior.
- Không expose secret hoặc internal persistence fields.

Request, application và response DTOs MAY khác nhau khi semantics khác nhau.

---

# 30. Ports và adapters

Application/Domain port phải:

- Mô tả capability theo business/technical intent.
- Không expose framework internals không cần thiết.
- Có error contract rõ.
- Có fake/test implementation khi hữu ích.

Ví dụ:

```text
CustomerRepository
BusinessCalendarPort
NumberIssuerPort
ObjectStoragePort
SignatureProviderPort
```

Adapters implement ports và chứa provider/framework code.

---

# 31. Repository rules

Repository interface SHOULD theo aggregate/use-case needs, không generic CRUD.

Tốt:

```text
get_by_id
add
find_active_lock_for_listing
```

Kém:

```text
save_any
find_all
update_fields
```

Repository MUST NOT:

- Commit transaction độc lập nếu Unit of Work sở hữu commit.
- Return ORM objects ra Domain/Application nếu architecture tách mapping.
- Query/write schema Context khác.

---

# 32. Unit of Work

Unit of Work phải tạo transaction boundary rõ.

Một command transaction MAY bao gồm:

- Aggregate state.
- Child entities.
- Status/history facts.
- Audit record theo approved port.
- Outbox messages.
- Idempotency completion.

Một transaction SHOULD NOT bao gồm:

- External HTTP call.
- User think time.
- Large file processing.
- Sleep/backoff.
- Unbounded batch.

Exact transaction boundaries thuộc architecture/Context contracts.

---

# 33. Infrastructure layer

Infrastructure chứa:

- ORM mappings.
- Repository implementations.
- External clients.
- Broker adapters.
- Object storage adapters.
- Job runners.
- Telemetry exporters.

Infrastructure code MUST:

- Map provider errors thành typed adapter errors.
- Apply timeout/retry theo approved policy.
- Redact secrets.
- Be replaceable qua port.

---

# 34. ORM và persistence mapping

ORM model là persistence representation, không phải Domain model mặc định.

MUST:

- Đặt mapping trong owning Context infrastructure.
- Dùng explicit schema.
- Dùng explicit constraints qua migrations.
- Tránh hidden lazy loading trong business flow.
- Tránh cascade không được domain/database standards cho phép.

Exact DDL thuộc Alembic migrations.

---

# 35. Database session discipline

- Session lifecycle MUST được quản lý tại infrastructure/composition boundary.
- Session MUST NOT được truyền vào Domain.
- Repository MUST NOT tự tạo session tùy tiện.
- Commit/rollback ownership MUST rõ.
- Connection MUST NOT bị giữ trong external network call nếu không cần.

---

# 36. Presentation/API layer

Router/controller phải:

- Parse transport input.
- Resolve authentication context.
- Call application use case.
- Map result/error thành transport contract.
- Không chứa business invariant.
- Không query ORM trực tiếp trừ approved read-only composition adapter.

Exact paths, payloads và status codes thuộc OpenAPI/API Standards.

---

# 37. Validation layers

## Presentation validation

- Type.
- Required fields.
- Length/format.
- Basic cross-field structure.

## Domain/Application validation

- State transition.
- Eligibility.
- Ownership.
- Financial rule.
- Effective period.

## Database validation

- Unique.
- FK.
- Check.
- Exclusion.
- Concurrency guard.

Không duplicate một invariant ở nhiều nơi với semantics khác nhau.

---

# 38. Error handling

Error flow:

```text
Domain error
→ Application error or preserved semantic error
→ Presentation mapping
→ Stable Error Code / Problem Details
```

MUST NOT:

```python
except Exception:
    return {"success": False}
```

MUST NOT raise HTTP-specific exceptions trong Domain.

Unexpected errors:

- MUST preserve cause internally.
- MUST log safe context.
- MUST return generic safe response.
- MUST attach correlation ID.

Exact Error Code nằm trong Error Code Registry.

---

# 39. Idempotency

Critical commands MUST use shared idempotency foundation khi API/Context contract yêu cầu.

Idempotency implementation phải hỗ trợ:

- Operation scope.
- Canonical request hash.
- Same key/same request replay.
- Same key/different request conflict.
- In-progress state.
- Recovery from stale ownership.

Context MUST NOT tự phát minh idempotency table hoặc semantics riêng.

---

# 40. Optimistic concurrency

Mutable critical resources SHOULD dùng version token theo Database/API Standards.

Code phải:

- Accept expected version từ trusted transport header/contract.
- Compare atomically.
- Return semantic conflict.
- Không silently overwrite.

Exact column/header contract thuộc DB/OpenAPI.

---

# 41. Pessimistic concurrency

Row/advisory locks MAY dùng khi invariant cần.

Code MUST:

- Lock theo deterministic order.
- Giữ transaction ngắn.
- Có bounded timeout theo environment policy.
- Classify retryable conflicts.
- Có real concurrency tests.

Không dùng in-memory lock làm final protection trong multi-process production.

---

# 42. Time

MUST:

- Dùng timezone-aware datetime cho instant.
- Inject `Clock` hoặc equivalent tại domain/application code cần thời gian.
- Dùng UTC cho persistence/event instant.
- Dùng IANA timezone cho business-local calculations.

MUST NOT gọi `datetime.now()` rải rác trong domain logic.

Exact calendar semantics thuộc Platform Context.

---

# 43. Identifiers

Business technical IDs SHOULD dùng project-approved UUID strategy.

Current recommended strategy MAY là UUIDv7 theo Toolchain/Architecture decision.

Rules:

- ID generation phải centralized/injectable.
- Tests phải deterministic.
- Không expose database sequence như public identity nếu architecture cấm.
- Không tạo ID format mới theo từng Context.

Exact choice là Architecture/Toolchain decision, không bị khóa chỉ bởi ví dụ này.

---

# 44. Money và numeric precision

MUST:

- Dùng `Decimal` hoặc exact numeric representation.
- Gắn currency khi business semantics cần.
- Có rounding policy rõ.
- Không cộng/trừ khác currency tùy tiện.

MUST NOT dùng `float` cho tiền, tỷ lệ tài chính hoặc số liệu yêu cầu precision chính xác.

Exact database precision và API serialization thuộc DB/API contracts.

---

# 45. Enums và stable codes

Stable domain codes SHOULD:

- Uppercase.
- Typed.
- Không dùng display label làm stored value.
- Không đổi meaning âm thầm.

Exact allowed values thuộc Context/machine contract.

Code MUST handle unknown external enum versions an toàn theo compatibility policy.

---

# 46. Collections và mutability

- Domain SHOULD expose immutable/read-only collections.
- Caller MUST NOT mutate aggregate internals.
- Ordering MUST explicit khi business meaningful.
- Duplicate semantics MUST rõ.
- Mutable global collections MUST NOT chứa request/business state.

---

# 47. Configuration

Configuration MUST:

- Typed.
- Validated at startup hoặc use boundary.
- Environment-specific.
- Không chứa secret trong source.
- Có safe defaults chỉ khi thật sự an toàn.

MUST NOT dùng environment variable trực tiếp khắp business code.

Composition root/infrastructure config chịu trách nhiệm mapping settings.

---

# 48. Secrets

Secret value MUST NOT xuất hiện trong:

- Source code.
- Markdown.
- Test fixture committed.
- Frontend bundle.
- Logs.
- Error messages.
- Business database tables.

Code SHOULD nhận secret qua secret reference/provider.

---

# 49. Feature flags

Feature flag:

- Không thay authorization.
- Không thay domain invariant.
- Có owner và lifecycle.
- Có safe default.
- Có cleanup plan.

Không để permanent conditional complexity vì flag đã hết hạn.

---

# 50. Audit implementation

Audit facts MUST lấy từ trusted context:

- ActorContext.
- Application command.
- Domain result.
- Resource reference.
- Reason code nếu required.

MUST NOT lấy actor hoặc permission từ request body.

Operational logs MUST NOT thay Audit.

---

# 51. Event implementation

Producer flow:

```text
Domain fact
→ Application mapping
→ Outbox insert trong cùng transaction
→ Publisher sau commit
```

MUST NOT:

- Publish broker trực tiếp từ router/Domain.
- Publish trước DB commit.
- Serialize ORM object làm event payload.

Exact Event contracts thuộc JSON Schema/AsyncAPI.

---

# 52. Consumer implementation

Consumer MUST:

- Có stable consumer name.
- Dùng Inbox cho side effects.
- Idempotent.
- Ack sau commit.
- Classify retryable/permanent errors.
- Có ordering/gap policy khi relevant.
- Không write source Context schema.
- Có reconciliation path cho critical flow.

---

# 53. Process Managers

Dùng Process Manager khi flow:

- Multi-step.
- Cross-context.
- Có timeout.
- Có compensation.
- Có manual intervention.
- Có legal/financial criticality.

Process state MUST persist.

MUST NOT chỉ dựa vào in-memory chain hoặc worker callback sequence.

Exact process inventory thuộc Process Manager Standards và Context Packs.

---

# 54. Background jobs

Job MUST có:

- Stable name.
- Typed input/reference.
- Idempotency strategy.
- Timeout/retry classification.
- Progress/checkpoint nếu dài.
- Structured logs/metrics.
- Cancellation/recovery policy khi relevant.

Exact retry count, queue hoặc timeout là Context/Environment decision.

---

# 55. External clients

External client adapter MUST:

- Set bounded timeout.
- Validate TLS.
- Redact credentials.
- Map errors.
- Propagate correlation/tracing.
- Support idempotency/reconciliation cho irreversible actions.

Retry MUST chỉ áp dụng cho retry-safe operations.

---

# 56. Serialization

- Serialization MUST theo machine-readable contract.
- Decimal/time/UUID representation MUST nhất quán.
- Unknown fields MUST được xử lý theo compatibility policy.
- Unsafe object serialization MUST NOT được dùng.
- Pickle hoặc equivalent MUST NOT nhận untrusted input.

---

# 57. Logging

Code MUST dùng centralized structured logger.

MUST log:

- Operation.
- Result.
- Error code.
- Correlation ID.
- Duration khi phù hợp.

MUST NOT log:

- Token.
- Secret.
- Full request/response.
- Full PII.
- Financial evidence.
- Signed URL.

Exact fields/metrics thuộc Observability Standards.

---

# 58. Metrics và tracing

- Domain MUST NOT import telemetry SDK.
- Application MAY dùng shared observability abstraction.
- Metric labels MUST low-cardinality.
- Trace span names MUST không chứa resource IDs.
- Telemetry MUST NOT chứa PII hoặc secrets.

---

# 59. Security coding discipline

Every code change MUST consider:

- Authentication source.
- Permission.
- Scope.
- Resource relationship.
- Field masking.
- SoD/approval.
- Audit.
- Input validation.
- Output minimization.

MUST NOT trust client-provided role, scope, owner hoặc actor.

---

# 60. Authorization implementation

Authorization SHOULD được gọi qua shared policy/capability abstraction.

Router-only checks không đủ.

List/detail/export/search MUST áp dụng cùng access semantics.

Authorization failure MUST NOT tạo side effect.

Exact permissions thuộc Permission Registry.

---

# 61. Data minimization

Code chỉ nên load, serialize và publish dữ liệu cần thiết.

Không:

- Load full Customer khi chỉ cần ID.
- Publish full Aggregate trong Event.
- Return full financial profile cho list screen.
- Cache unmasked response không gắn access context.

---

# 62. File handling

File binary SHOULD nằm object storage theo architecture.

Code MUST:

- Validate upload intent.
- Sanitize filename.
- Verify size/MIME/hash theo File Security Standards.
- Không dùng client path làm server path.
- Không expose permanent public URL.

---

# 63. Import/export coding

Import MUST đi qua staging và canonical commands.

Export MUST:

- Reauthorize scope.
- Apply masking.
- Use async job khi lớn.
- Prevent spreadsheet formula injection theo Security Standards.
- Not expose storage keys.

---

# 64. Frontend coding scope

Frontend-specific implementation chi tiết thuộc `frontend-standards.md`.

Coding Standards chỉ khóa các nguyên tắc:

- Generated API types SHOULD là source cho transport types.
- Frontend MUST NOT quyết định authorization.
- Frontend MUST NOT tính official KPI hoặc financial truth.
- Critical mutation MUST handle idempotency/concurrency contract.
- UI MUST có loading, empty, error, permission và conflict states.
- Sensitive data MUST NOT được lưu trong browser storage.

---

# 65. TypeScript discipline

TypeScript code MUST:

- Chạy strict mode theo repository config.
- Tránh `any`.
- Dùng `unknown` và narrowing cho unknown data.
- Không duplicate generated API types.
- Không suppress type errors không có issue/justification.

Type assertion chỉ hợp lệ khi runtime invariant đã được chứng minh.

---

# 66. React/Next.js discipline

- Server/client boundary MUST rõ.
- `use client` chỉ dùng khi cần browser interaction.
- Components MUST không chứa backend security decisions.
- Effects MUST dùng để synchronize external systems, không để derive state tùy tiện.
- Server state SHOULD dùng approved query/fetch architecture.
- Critical optimistic updates SHOULD NOT được dùng nếu có corruption/conflict risk.

---

# 67. API client usage

Frontend SHOULD dùng generated/centralized API client.

MUST NOT:

- Raw fetch rải rác trong feature components nếu abstraction đã có.
- Handwrite duplicate DTOs.
- Ignore Problem Details.
- Silently overwrite stale resource.

---

# 68. Accessibility trong code

Interactive UI MUST:

- Dùng semantic elements.
- Keyboard accessible.
- Có accessible name.
- Có visible focus.
- Không truyền meaning chỉ bằng màu.

Exact design patterns thuộc Design System và Frontend Standards.

---

# 69. Testability

Code SHOULD được thiết kế để test bằng:

- Injected clock/ID providers.
- Ports/fakes.
- Explicit transaction boundaries.
- Pure domain behavior.
- Deterministic serialization.
- No hidden global state.

MUST NOT thêm test-only branch vào production domain logic nếu có cách thiết kế sạch hơn.

---

# 70. Testing obligations

Mỗi change MUST có tests tương ứng theo risk:

- Domain invariant → unit test.
- Repository/constraint → PostgreSQL integration test.
- API behavior → API/contract test.
- Event → schema/outbox/inbox tests.
- Authorization → security matrix test.
- Concurrency → real multi-session test.
- Critical UI journey → component/E2E test.

Exact test inventory thuộc Testing Standards và Sprint Acceptance Criteria.

---

# 71. Bug fixes

Bug fix MUST:

1. Reproduce bằng test ở layer phù hợp.
2. Fix root cause.
3. Giữ regression test.
4. Update contract/docs nếu behavior được làm rõ.

MUST NOT chỉ thay expected result để code sai trở thành pass.

---

# 72. Database migrations trong code review

Khi change có migration, review MUST kiểm tra:

- Owning Context/schema.
- Backward compatibility.
- Expand–migrate–contract strategy.
- Lock/data impact.
- Constraint/index purpose.
- Backfill/reconciliation.
- Rollback hoặc forward-fix plan.

Exact DDL không nằm trong Coding Standards.

---

# 73. API contract changes

Khi code thay API:

- OpenAPI MUST cập nhật trong cùng change.
- Generated client MUST sạch.
- Compatibility MUST được đánh giá.
- Error/permission metadata MUST cập nhật.
- Undocumented endpoint MUST NOT tồn tại.

---

# 74. Event contract changes

Khi code thay Event:

- JSON Schema MUST cập nhật.
- AsyncAPI/Event Registry MUST cập nhật.
- Compatibility MUST được đánh giá.
- Producer/consumer tests MUST cập nhật.
- Published schema MUST NOT bị sửa breaking in place.

---

# 75. Permission và error registry changes

Code MUST NOT dùng permission/error code chưa đăng ký.

Registry update SHOULD nằm cùng PR với code sử dụng.

CI SHOULD kiểm tra registry drift.

---

# 76. Performance discipline

Optimize sau khi có:

- Correctness.
- Measurement.
- Representative data.
- Query/profile evidence.

MUST NOT weaken scope, invariant hoặc Audit để tăng tốc.

Avoid:

- N+1.
- Load-all/filter-in-memory cho large data.
- Unbounded loops/requests.
- Repeated external calls.
- Excessive serialization.

Exact performance targets thuộc NFR/SLO.

---

# 77. Resource bounds

Every externally influenced operation SHOULD có bounded:

- Request size.
- Page size.
- Batch size.
- Timeout.
- Retry count.
- File size.
- Search complexity.

Exact values là Environment/Context decisions và phải được cấu hình, không hard-code rải rác.

---

# 78. Async code

Async MUST dùng khi dependency thực sự async/non-blocking.

MUST NOT:

- Gọi blocking I/O trong event loop không adapter.
- Tạo unbounded tasks.
- Fire-and-forget critical work trong request process.
- Swallow cancellation.

Long-running work SHOULD chuyển background job/process.

---

# 79. Retries

Retry policy MUST:

- Chỉ retry error được phân loại retryable.
- Có bounded attempts/time.
- Có backoff và jitter khi phù hợp.
- Tôn trọng idempotency.
- Có telemetry.

MUST NOT retry validation, permission hoặc permanent domain conflicts.

---

# 80. Caching

Cache:

- MUST NOT là source of truth.
- MUST NOT thay database constraint.
- MUST include access context khi response khác theo quyền.
- MUST have invalidation/TTL strategy.
- MUST fail safely.

Không cache unmasked sensitive response cho shared access.

---

# 81. Reconciliation

Derived state, integration state và long-running processes SHOULD có reconciliation khi correctness quan trọng.

Reconciliation MUST:

- Đọc source of truth.
- Detect discrepancy.
- Record finding.
- Repair derived state safely hoặc tạo canonical command.
- Audit/measure result.

MUST NOT silently mutate business truth.

---

# 82. Composition root và dependency injection

Concrete adapters SHOULD được wire tại composition root.

Business code MUST NOT tự instantiate:

- Database session.
- HTTP client.
- Broker client.
- Secret manager.
- Object storage client.

Dependency injection framework cụ thể là Toolchain/Architecture decision.

---

# 83. Global state

Mutable global state MUST NOT chứa:

- Current actor.
- Current Enterprise.
- Request scope.
- Transaction/session.
- Business cache không thread-safe.

Immutable configuration/registries MAY là module-level nếu lifecycle rõ.

---

# 84. Backward compatibility

Code thay đổi public/internal contracts MUST:

- Xác định consumers.
- Duy trì compatibility hoặc version.
- Có deprecation plan.
- Không đổi semantics âm thầm.

Internal private refactor MAY không cần compatibility nếu không vượt module public API.

---

# 85. Deprecation

Deprecated code cần:

- Replacement.
- Consumer inventory.
- Warning/documentation.
- Removal target.
- Tests trong migration window.

Không giữ dead compatibility layer vô thời hạn.

---

# 86. Dependency governance

Dependency mới cần:

- Use case rõ.
- Security/maintenance/license review.
- Toolchain Lock update nếu accepted.
- Bundle/runtime impact review.
- Không trùng capability hiện có.

MUST NOT thêm dependency chỉ để tránh viết vài dòng đơn giản.

---

# 87. Dead code

Dead code MUST được xóa khi không còn compatibility need.

MUST NOT giữ:

- Commented-out implementation.
- Old version trong cùng file.
- Unused feature flag branch.
- Duplicate helper.

Git là history.

---

# 88. Code review expectations

Reviewer phải xem:

## Ownership

- Đúng Context?
- Có cross-context coupling?

## Domain

- Intent rõ?
- Invariant đúng?
- Generic CRUD/status patch?

## Security

- Auth/scope/masking/SoD?
- PII/secret?

## Reliability

- Transaction?
- Idempotency?
- Concurrency?
- Event/Audit?

## Contracts

- OpenAPI/schema/registry/migration?

## Tests

- Đúng layer?
- Negative/boundary/concurrency?

## Maintainability

- Naming?
- Types?
- Complexity?
- Unrelated diff?

---

# 89. Pull request scope

PR SHOULD:

- Có một coherent goal.
- Có docs/contracts/tests đi cùng.
- Tránh unrelated refactor.
- Ghi migration/security/operational impact.
- Ghi commands/evidence đã chạy.

Large change MAY tách thành ordered PRs nếu compatibility được duy trì.

---

# 90. Formatting, linting và type checking

Repository configuration là executable truth cho:

- Formatter.
- Linter.
- Import sorting.
- Type checker.
- TypeScript compiler.

Code MUST pass configured gates.

Tài liệu này không khóa exact flags nếu config chưa accepted.

---

# 91. Architecture tests

CI SHOULD enforce:

- Domain không import framework.
- Không cross-context persistence imports.
- Presentation không direct-write DB.
- Router không publish broker trực tiếp.
- No business tables in public schema.
- Frontend không duplicate generated API types.

Architecture boundary violations MUST block merge trừ approved exception.

---

# 92. AI Agent reading order

Trước implementation, AI Agent MUST đọc:

1. `README.md`.
2. Relevant global standards.
3. Relevant ADRs.
4. Relevant Context Implementation Pack.
5. Current Sprint Detailed Execution Pack.
6. Existing code, migrations và tests.
7. Project Status và Current Handoff.

AI Agent SHOULD NOT đọc toàn bộ tài liệu không liên quan nếu làm tăng conflict/noise.

---

# 93. AI Agent task protocol

Trước khi code, AI Agent MUST:

1. Restate task scope.
2. Xác định owning Context.
3. Xác định source of truth.
4. Inspect current implementation.
5. Xác định impacted contracts.
6. Xác định security/concurrency/audit/event requirements.
7. Xác định tests.
8. Báo conflict/gap nếu có.

Trong khi code, AI Agent MUST:

- Giữ diff trong scope.
- Không invent requirement.
- Không bypass failing tests.
- Update docs/contracts cùng code.
- Không tạo fake evidence.

Sau code, AI Agent MUST:

- Chạy relevant gates.
- Ghi exact results.
- Ghi limitations/failures.
- Update handoff/status/acceptance artifacts theo workflow.

---

# 94. AI Agent prohibited behaviors

AI Agent MUST NOT:

1. Tạo generic CRUD thay stateful use case.
2. Tạo cross-context repository import.
3. Trust owner/scope từ request.
4. Publish broker trực tiếp từ router/Domain.
5. Dùng ORM model làm API/Domain contract.
6. Hard-code secret.
7. Log PII/token.
8. Dùng float cho money.
9. Dùng SQLite thay PostgreSQL integration test.
10. Sửa migration đã phát hành.
11. Xóa failing test để green.
12. Tự thêm dependency không approval.
13. Biến example trong Standards thành exact contract.
14. Báo test pass khi chưa chạy.
15. Báo Done khi còn conflict hoặc unknown critical.

---

# 95. Coding anti-patterns bị cấm

1. Giant `service.py` chứa toàn bộ Context.
2. `utils.py` làm nơi chứa business logic không owner.
3. Anemic model khi invariant cần behavior.
4. Generic `update_status`.
5. Direct cross-context database write.
6. Domain phụ thuộc framework.
7. Router chứa transaction/business workflow.
8. Catch-all exception rồi tiếp tục.
9. Hidden global request state.
10. Network call trong long DB transaction.
11. Direct broker publish trước commit.
12. Frontend tự quyết định quyền.
13. Full payload logging.
14. Hard-coded environment limits rải rác.
15. Copy/paste contract types.
16. Over-mocking khiến test không chứng minh behavior.
17. Silent fallback làm sai business truth.
18. In-memory lock làm final distributed guard.
19. Cache làm source of truth.
20. Temporary bypass không owner/expiry.

---

# 96. Definition of Ready cho coding task

Task chỉ Ready khi:

1. Owning Context rõ.
2. Business intent rõ.
3. Source of truth rõ.
4. Invariants/state impact rõ.
5. Security scope rõ.
6. Transaction/concurrency impact rõ.
7. Contracts impacted rõ.
8. Test plan rõ.
9. Migration/operational impact rõ khi relevant.
10. Không có unresolved blocking conflict.

---

# 97. Definition of Done cho code change

Change chỉ Done khi:

1. Đúng Context và layer.
2. Domain intent/invariant đúng.
3. Security enforce backend.
4. Transaction/idempotency/concurrency đúng khi relevant.
5. Audit/Event đúng khi required.
6. Contracts/registries/migrations cập nhật.
7. Formatter/lint/typecheck pass.
8. Relevant tests pass.
9. Security/concurrency/contract tests pass khi relevant.
10. Observability phù hợp.
11. Không secret/PII leakage.
12. Không unexplained TODO/skip.
13. Documentation cập nhật.
14. Evidence ghi trung thực.
15. Acceptance/Handoff cập nhật theo workflow.

---

# 98. Ngoại lệ

Ngoại lệ cần file:

```text
docs/engineering/coding-exceptions/EXC-CODING-XXX.md
```

Nội dung:

- Rule.
- Scope.
- Reason.
- Alternatives considered.
- Risk.
- Security/data impact.
- Mitigation.
- Owner.
- Expiry.
- Removal plan.
- Approval.

Không có ngoại lệ vô thời hạn không owner.

---

# 99. Checklist phân biệt Standards và implementation detail

Trước khi thêm một quy tắc vào file này, hỏi:

1. Quy tắc có áp dụng cho phần lớn repository không?
2. Quy tắc có bảo vệ architecture/security/correctness không?
3. Quy tắc có phụ thuộc một Context cụ thể không?
4. Quy tắc có phải exact contract máy đọc được không?
5. Giá trị số đã được benchmark/approved chưa?
6. Đây là MUST, baseline hay ví dụ?

Nếu là exact Context/API/DB/Event detail, MUST chuyển sang tài liệu hoặc contract có thẩm quyền tương ứng.

---

# 100. Hướng dẫn cập nhật tài liệu này

Thay đổi Coding Standards cần:

- Lý do rõ.
- Impact analysis.
- Review từ owner liên quan.
- Migration guidance nếu code hiện tại bị ảnh hưởng.
- Changelog.
- Không retroactively tuyên bố code cũ sai mà không có remediation plan.

---

# 101. Change Log

## Version 1.1.0 — 2026-07-26

- Làm rõ phạm vi thẩm quyền của Coding Standards.
- Phân biệt `MUST`, `SHOULD`, `MAY`, baseline và illustrative example.
- Tách semantic coding rules khỏi exact executable contracts.
- Hạ cấp các lựa chọn chưa được kiểm chứng thành Context/Environment decisions.
- Bổ sung authority matrix và conflict protocol.
- Bổ sung AI Agent rule không biến ví dụ thành exact specification.
- Giữ nguyên các boundary quan trọng về Context, Domain, security, transaction, Audit và Event.

## Version 1.0.0 — 2026-07-24

- Phiên bản baseline ban đầu.

---

# 102. Kết luận

Coding Standards của `crm_bds_ai` phải đủ chi tiết để ngăn implementation đi sai hướng, nhưng không được biến thành một bản dự đoán cứng nhắc về code tương lai.

Công thức đúng:

```text
Strict Architectural Boundaries
+ Explicit Domain Intent
+ Strong Types
+ Secure and Reliable Implementation
+ Machine-Readable Exact Contracts
+ Context-Specific Decisions Just in Time
+ Verified Code and Tests
```

Nguyên tắc cuối cùng:

> Khóa nguyên tắc và ranh giới từ sớm; khóa exact implementation tại đúng nguồn chân lý và đúng thời điểm triển khai.


# AI coding constraints

- Provider SDK imports are permitted only in provider adapters.
- Model/provider IDs, URLs and keys are configuration/secret references, never business constants.
- AI outputs use typed canonical DTOs and JSON Schema/Pydantic validation.
- Architecture tests must prevent direct provider/database dependencies from business Contexts.
- Open Decisions and business invariants cannot be encoded only in prompts.
