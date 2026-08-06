# CRM_BDS_AI — EVENT STANDARDS

## Quy chuẩn Event, Outbox, Inbox, AsyncAPI và xử lý bất đồng bộ bắt buộc cho toàn bộ hệ thống `crm_bds_ai`

**Document ID:** `ENG-EVENT-001`  
**Canonical path:** `docs/engineering/event-standards.md`  
**Product:** `crm_bds_ai`  
**Version:** `1.0.0`  
**Status:** `Accepted / Mandatory`  
**Canonical:** `Yes` đối với tiêu chuẩn Domain Event, Integration Event, Outbox, Inbox, consumer, replay và event contracts  
**Owner:** `Event Architecture Owner`  
**Reviewers:** `Architecture Owner`, `Technical Owner`, `Security Owner`, `Context Owners`, `QA Owner`, `Operations Owner`, `Integration Owner`, `Analytics Owner`  
**Effective date:** `2026-08-05`  
**Last reviewed:** `2026-08-05`  
**Next review:** Khi event architecture, broker, AsyncAPI, retry, replay, schema compatibility hoặc operational policy thay đổi  
**Supersedes:** `None — Greenfield baseline`  
**Superseded by:** Không

---

# 1. Mục đích

Tài liệu này quy định cách tạo, đặt tên, version, serialize, persist, publish, consume, retry, replay, monitor, bảo vệ và kiểm thử mọi Event trong `crm_bds_ai`.

Mục tiêu:

1. Bảo đảm Event phản ánh đúng business fact đã xảy ra.
2. Phân biệt rõ Domain Event và Integration Event.
3. Ngăn business transaction publish trực tiếp lên broker.
4. Bảo đảm business state và Outbox commit trong cùng transaction.
5. Bảo đảm consumer xử lý at-least-once an toàn.
6. Bảo đảm duplicate delivery không tạo side effect trùng.
7. Bảo đảm schema versioning có compatibility rõ.
8. Bảo đảm event không rò rỉ PII, secret hoặc internal implementation detail.
9. Bảo đảm replay và reconciliation có kiểm soát.
10. Bảo đảm mọi AI Agent triển khai event theo cùng một chuẩn.

Tài liệu này phải được đọc cùng:

```text
docs/engineering/coding-standards.md
docs/engineering/database-standards.md
docs/engineering/api-standards.md
docs/engineering/testing-standards.md
docs/engineering/security-standards.md
docs/architecture/context-map.md
docs/architecture/source-of-truth-matrix.md
docs/architecture/transaction-boundaries.md
Relevant Context Implementation Pack
Current Sprint Execution Pack
```

---

# 2. Nguyên tắc tối cao

```text
Business Truth
> Transactional Reliability
> Idempotency
> Compatibility
> Security
> Observability
> Throughput
> Convenience
```

Không được đánh đổi business correctness hoặc khả năng replay chỉ để publish nhanh hơn.

---

# 3. Event taxonomy

## 3.1. Domain Event

Domain Event:

- Được tạo bên trong Aggregate hoặc Domain Service.
- Phản ánh business fact trong cùng Bounded Context.
- Có thể chưa phải contract công khai cho Context khác.
- Không biết broker.
- Không biết Celery.
- Không biết RabbitMQ.
- Không biết SQLAlchemy.
- Không tự persist.

Ví dụ:

```text
BookingConfirmed
CommercialLockActivated
PaymentAllocated
ReceiptIssued
CustomerMerged
```

## 3.2. Integration Event

Integration Event:

- Là contract versioned được publish ra ngoài Context.
- Được materialize từ Domain Event hoặc Application result.
- Có JSON Schema.
- Có AsyncAPI registration.
- Tối giản payload.
- Không chứa internal object graph.
- Có compatibility policy.

Ví dụ:

```text
transaction.booking.confirmed.v1
product.commercial_lock.activated.v1
contract.payment.allocated.v1
contract.receipt.issued.v1
party.customer.merged.v1
```

## 3.3. Technical Event

Technical Event:

- Phản ánh trạng thái hạ tầng hoặc vận hành.
- Không thay business truth.
- Có owner rõ.

Ví dụ:

```text
operations.job.failed.v1
integration.webhook.signature_invalid.v1
audit.integrity_check.failed.v1
```

## 3.4. Command message

Command message là yêu cầu làm việc trong async flow.

Ví dụ:

```text
crm.events.consume
crm.events.consume_handler
crm.documents.run_ocr
crm.integration.retry_delivery
```

Command message không được đặt tên ở past tense như Event.

## 3.5. Notification message

Notification message dùng để gửi email/in-app/SMS, không phải business event.

Không dùng notification delivery làm source of truth.

---

# 4. Event naming

## 4.1. Integration Event type

Format:

```text
<context>.<aggregate_or_subject>.<past_tense_fact>
```

Version nằm riêng trong envelope hoặc suffix registry, không nhét tùy tiện vào event name trong code.

Canonical examples:

```text
platform.enterprise.activated
party.customer.merged
lead.lead.converted
product.listing.activated
transaction.booking.confirmed
contract.receipt.issued
revenue.commission_entitlement.vested
activity.task.completed
marketing.form_submission.accepted
analytics.snapshot.locked
documents.document.verified
audit.integrity_check.failed
integration.sync.completed
operations.release.completed
```

## 4.2. Past tense

Event phải mô tả fact đã xảy ra.

Đúng:

```text
booking.confirmed
payment.allocated
receipt.issued
```

Sai:

```text
confirm_booking
allocate_payment
issue_receipt
booking.confirm
payment.allocate
```

## 4.3. Stable vocabulary

Event name phải dùng Domain Glossary.

Không rename event chỉ vì wording đẹp hơn nếu đã publish.

## 4.4. Không dùng generic names

Bị cấm:

```text
entity.updated
data.changed
record.created
process.completed
status.changed
```

trừ khi subject rất rõ và use case thực sự generic đã được ADR phê duyệt.

---

# 5. Event versioning

## 5.1. Version field

Mỗi Integration Event phải có:

```text
event_version: integer
```

## 5.2. Version 1

Event đầu tiên:

```text
event_version = 1
```

## 5.3. Non-breaking change

Có thể giữ version nếu:

- Thêm optional field.
- Thêm field có safe default.
- Thêm metadata không bắt consumer cũ thay đổi.
- Mở rộng enum chỉ khi consumer contract chấp nhận unknown values.

## 5.4. Breaking change

Phải tăng version khi:

- Xóa field.
- Rename field.
- Đổi type.
- Đổi meaning.
- Đổi requiredness.
- Đổi enum semantics.
- Đổi unit/currency/date semantics.
- Đổi aggregation/grain.
- Đổi source of truth.
- Đổi ordering guarantees.

## 5.5. Compatibility window

Version cũ phải được hỗ trợ trong khoảng thời gian migration được phê duyệt.

Không xóa schema cũ ngay khi tạo version mới.

## 5.6. Version trong tên file

```text
contracts/events/transaction/booking-confirmed/v1.json
contracts/events/transaction/booking-confirmed/v2.json
```

---

# 6. Event envelope

Canonical envelope:

```json
{
  "event_id": "uuid",
  "event_type": "transaction.booking.confirmed",
  "event_version": 1,
  "occurred_at": "2026-07-24T10:00:00Z",
  "recorded_at": "2026-07-24T10:00:00Z",

  "producer": {
    "context": "transaction",
    "service": "crm-bds-next",
    "instance": "optional"
  },

  "aggregate": {
    "type": "Booking",
    "id": "uuid",
    "version": 7
  },

  "scope": {
    "enterprise_id": "uuid",
    "legal_entity_id": "uuid",
    "project_id": "uuid"
  },

  "correlation_id": "uuid",
  "causation_id": "uuid",
  "trace_id": "string",

  "actor": {
    "actor_type": "USER",
    "actor_key": "uuid"
  },

  "data": {},

  "metadata": {
    "schema_uri": "urn:crm-bds-next:event:transaction:booking-confirmed:1",
    "content_type": "application/json"
  }
}
```

---

# 7. Envelope field rules

## 7.1. `event_id`

- UUIDv7.
- Unique toàn hệ thống.
- Không reuse.
- Consumer Inbox deduplicate theo event ID.

## 7.2. `event_type`

- Stable.
- Lowercase dot notation.
- Không chứa version nếu version field riêng.

## 7.3. `event_version`

- Integer >= 1.
- Match JSON Schema.

## 7.4. `occurred_at`

Thời điểm business fact xảy ra.

## 7.5. `recorded_at`

Thời điểm event được ghi Outbox.

Thông thường gần `occurred_at`, nhưng không bắt buộc giống.

## 7.6. Producer

Producer Context là owner của fact.

Không giả mạo producer khác.

## 7.7. Aggregate

Có khi Event gắn Aggregate.

Nếu Event là projection/technical event không có Aggregate, contract phải nói rõ.

## 7.8. Scope

Chỉ chứa IDs cần thiết cho routing/security.

Không chứa scope do client tự khai báo không được xác thực.

## 7.9. Correlation

`correlation_id` liên kết toàn bộ business flow.

## 7.10. Causation

`causation_id` trỏ tới command/event trực tiếp gây ra event.

## 7.11. Trace

Trace ID hỗ trợ observability, không phải business identity.

## 7.12. Actor

Actor lấy từ trusted ActorContext.

Không lấy từ request body.

## 7.13. Data

Data là payload domain-specific.

## 7.14. Metadata

Chỉ technical metadata allowlist.

Không nhét arbitrary map không kiểm soát.

---

# 8. Event payload principles

Payload phải:

- Tối giản.
- Có đủ dữ liệu để consumer xử lý use case contract.
- Không replicate toàn Aggregate.
- Không chứa ORM model.
- Không chứa request body.
- Không chứa secret.
- Không chứa file binary.
- Không chứa raw provider payload trừ event technical có reference.
- Không chứa full PII nếu không bắt buộc.

---

# 9. Event data ownership

Event chỉ publish data thuộc producer hoặc snapshot producer có quyền công bố.

Ví dụ:

`transaction.booking.confirmed` có thể chứa:

- Booking ID.
- Transaction Case ID.
- Listing ID reference.
- Buyer Party IDs.
- Commercial snapshot ID.
- Confirmed at.

Không nên chứa:

- Full Customer profile.
- Full Listing details.
- Full Contract template.
- Payment bank details.

Consumer cần dữ liệu đầy đủ thì:

- Query internal API.
- Dùng own projection.
- Consume owner events khác.

---

# 10. Snapshot vs reference

## 10.1. Reference

Dùng ID reference khi consumer có thể query source.

## 10.2. Snapshot

Dùng snapshot khi meaning tại thời điểm event phải được bảo toàn.

Ví dụ:

- Price version ID.
- Contract version ID.
- Commission plan version ID.
- Attribution model version ID.

## 10.3. Không snapshot tùy tiện

Snapshot lớn:

- Tăng broker/storage.
- Tăng PII exposure.
- Tăng compatibility burden.

Chỉ snapshot fields cần audit/reproducibility.

---

# 11. Data types trong Event

## 11.1. UUID

String canonical UUID.

## 11.2. Datetime

RFC3339 UTC.

## 11.3. Date

`YYYY-MM-DD`.

## 11.4. Decimal

String để tránh precision loss:

```json
"amount": "123456.7800"
```

## 11.5. Currency

ISO 4217 uppercase.

## 11.6. Enum

Stable uppercase codes.

## 11.7. Boolean

Chỉ cho binary facts rõ.

## 11.8. Null

Null semantics phải explicit.

Không dùng null để biểu diễn unknown và not-applicable cùng lúc nếu consumer cần phân biệt.

---

# 12. JSON Schema

Canonical:

```text
JSON Schema 2020-12
```

## 12.1. Requirements

Mỗi Integration Event phải có schema.

Schema phải:

- Có `$id`.
- Có title.
- Có version.
- Có required fields.
- Có `additionalProperties: false` ở các object critical.
- Có examples.
- Có descriptions.
- Có formats.
- Có enum codes.
- Có max lengths khi phù hợp.

## 12.2. File structure

```text
contracts/events/<context>/<event-name>/v1.json
```

## 12.3. Shared envelope schema

```text
contracts/events/_shared/event-envelope-v1.json
```

Context schema compose qua `$ref`.

## 12.4. Không sửa schema published

Schema version đã publish không được sửa breaking.

Sửa typo/description không đổi validation có thể patch với review.

---

# 13. AsyncAPI

Canonical:

```text
contracts/asyncapi/asyncapi.yaml
```

Phải mô tả:

- Channels.
- Messages.
- Producers.
- Consumers.
- Bindings.
- Security.
- Examples.
- Version references.
- Delivery semantics.
- Retry/DLQ conventions.

AsyncAPI không thay event schema source; nó tham chiếu JSON Schema.

---

# 14. Event registry

Phải có Event Registry machine-readable hoặc code registry.

Mỗi entry:

- Event type.
- Version.
- Producer Context.
- Aggregate.
- Schema URI.
- Classification.
- Retention.
- Expected consumers.
- Replay allowed.
- Ordering key.
- Compatibility status.
- Deprecated/sunset.

Không publish event không có registry.

---

# 15. Domain Event coding rules

Domain Event:

- Immutable.
- Framework-free.
- Past tense.
- Contains business fact.
- No serialization concern.
- No broker concern.
- No PII beyond domain need.

Ví dụ:

```python
@dataclass(frozen=True, slots=True)
class BookingConfirmed:
    booking_id: UUID
    transaction_case_id: UUID
    listing_id: UUID
    confirmed_at: datetime
```

---

# 16. Integration Event materialization

Application layer hoặc dedicated mapper chuyển Domain Event thành Integration Event.

Không serialize Domain Event trực tiếp nếu integration contract khác internal domain shape.

Ví dụ:

```python
class BookingConfirmedEventMapper:
    def to_integration_event(
        self,
        domain_event: BookingConfirmed,
        context: EventContext,
    ) -> IntegrationEvent:
        ...
```

Mapper phải test.

---

# 17. Transactional Outbox

## 17.1. Nguyên tắc

Business state và Outbox row phải commit trong cùng database transaction.

## 17.2. Bị cấm

- Publish broker trước commit.
- Publish broker trực tiếp từ router.
- Publish broker trực tiếp từ Domain.
- Commit business state rồi insert Outbox ở transaction khác.
- Best-effort in-memory queue.

## 17.3. Outbox source

Một shared Outbox foundation trong schema `infra`.

Không tạo Outbox riêng mỗi Context.

---

# 18. Outbox fields

Outbox row phải có tối thiểu:

```text
id
event_id
event_type
event_version
producer_context
aggregate_type
aggregate_id
aggregate_version
enterprise_id
legal_entity_id
correlation_id
causation_id
trace_id
actor_type
actor_key
payload_json
payload_sha256
status
available_at
attempt_count
claimed_at
claimed_by
published_at
last_error_code
last_error_message
created_at
```

Error message phải sanitized và bounded.

---

# 19. Outbox states

```text
PENDING
PUBLISHING
RETRY
PUBLISHED
DEAD
```

## PENDING

Chờ publish.

## PUBLISHING

Đã claim bởi worker.

## RETRY

Publish tạm thời thất bại.

## PUBLISHED

Broker xác nhận publish theo configured guarantee.

## DEAD

Vượt retry policy hoặc permanent failure.

Không delete dead row tự động trước investigation/retention.

---

# 20. Outbox claiming

Claim algorithm phải dùng PostgreSQL concurrency-safe pattern:

```sql
SELECT ...
FROM infra.outbox_messages
WHERE status IN ('PENDING', 'RETRY')
  AND available_at <= now()
ORDER BY created_at, id
FOR UPDATE SKIP LOCKED
LIMIT :batch_size
```

Sau đó mark claim trong cùng transaction ngắn.

Không giữ DB transaction trong lúc chờ broker publish nếu design không yêu cầu.

---

# 21. Outbox publish confirmation

Publisher chỉ mark `PUBLISHED` khi nhận broker confirmation theo RabbitMQ publisher confirm hoặc equivalent.

Không coi network write thành công nếu chưa có confirm.

---

# 22. Outbox retry

Retryable:

- Broker unavailable.
- Network timeout.
- Temporary channel error.
- Publisher confirm timeout.

Permanent/dead candidate:

- Schema serialization impossible.
- Unsupported event registry.
- Payload hash mismatch.
- Event type invalid.
- Message exceeds limit.

Retry có:

- Exponential backoff.
- Jitter.
- Max attempts.
- Available-at scheduling.
- Metrics.
- Alert threshold.

---

# 23. Stale Outbox claims

Job recovery phải:

- Detect PUBLISHING quá timeout.
- Move về RETRY.
- Increment recovery count.
- Audit technical action.
- Avoid duplicate dangerous behavior bằng idempotent consumer.

Duplicate publish có thể xảy ra và phải được chấp nhận theo at-least-once.

---

# 24. Delivery semantics

Canonical guarantee:

```text
At least once
```

Không tuyên bố:

```text
Exactly once
```

Exactly-once end-to-end không được claim nếu không chứng minh toàn chain.

---

# 25. Broker routing

RabbitMQ routing design phải có:

- Stable exchange.
- Routing key.
- Queue ownership.
- DLQ.
- Retry mechanism.
- Durable queues/messages.
- Publisher confirms.
- Consumer acknowledgements.

Example routing key:

```text
event.transaction.booking.confirmed.v1
```

Routing key có thể chứa version để broker routing rõ, dù `event_type` trong payload không chứa version.

---

# 26. Exchange and queue naming

Recommended:

```text
crm.events
crm.events.retry
crm.events.dead
```

Consumer queue:

```text
crm.<consumer_context>.<consumer_name>.v1
```

Ví dụ:

```text
crm.contract.booking_confirmed.v1
crm.analytics.booking_confirmed_projection.v1
```

Tên queue phải stable và owner rõ.

---

# 27. Consumer Inbox

Mỗi consumer side effect phải dùng Inbox.

Unique:

```text
consumer_name + event_id
```

Inbox row phải có:

```text
id
consumer_name
event_id
event_type
event_version
payload_sha256
handler_version
status
attempt_count
received_at
processing_started_at
processed_at
next_retry_at
last_error_code
last_error_message
correlation_id
```

---

# 28. Inbox states

```text
RECEIVED
PROCESSING
PROCESSED
FAILED_RETRYABLE
FAILED_PERMANENT
```

## RECEIVED

Đã persist message receipt.

## PROCESSING

Handler đang xử lý.

## PROCESSED

Side effect commit thành công.

## FAILED_RETRYABLE

Có thể retry.

## FAILED_PERMANENT

Cần DLQ/manual resolution.

---

# 29. Consumer transaction

Preferred pattern:

1. Receive message.
2. Start DB transaction.
3. Insert/find Inbox row.
4. If processed, ack duplicate.
5. Mark processing.
6. Execute handler side effect.
7. Persist own Context state.
8. Write Audit/Outbox nếu cần.
9. Mark Inbox processed.
10. Commit.
11. Ack broker.

Không ack trước commit.

---

# 30. Duplicate delivery

Nếu Inbox thấy event đã `PROCESSED`:

- Không chạy handler lại.
- Ack message.
- Increment duplicate metric.
- Không tạo second Outbox side effect.

Same event ID nhưng payload hash khác:

- Security/integrity conflict.
- Mark permanent failure.
- Alert.
- Không tự chọn một payload.

---

# 31. Consumer naming

`consumer_name` stable:

```text
<consumer_context>.<business_purpose>
```

Ví dụ:

```text
contract.create_contract_from_booking
analytics.project_booking_fact
activity.create_followup_after_site_visit
```

Không dùng tên class implementation có thể đổi:

```text
BookingHandlerV2
Consumer1
```

---

# 32. Handler version

Handler version dùng để:

- Track logic deployment.
- Replay planning.
- Diagnostics.
- Migration.

Không dùng handler version thay event version.

---

# 33. Consumer compatibility

Consumer phải khai báo supported versions.

Ví dụ:

```text
transaction.booking.confirmed v1, v2
```

Nếu nhận unsupported version:

- Không silently process.
- Mark permanent/unsupported.
- DLQ.
- Alert.
- Compatibility incident.

---

# 34. Ordering

## 34.1. Không mặc định global ordering

Hệ thống không đảm bảo thứ tự toàn cục.

## 34.2. Aggregate ordering

Có thể dùng:

```text
aggregate_id + aggregate_version
```

Consumer phải detect:

- Duplicate.
- Next version.
- Gap.
- Older version.

## 34.3. Out-of-order handling

Policy theo consumer:

- Buffer.
- Retry.
- Query source.
- Rebuild projection.
- Accept commutative event.
- Mark reconciliation required.

Không giả định broker luôn giữ đúng order khi multiple workers/queues/retries.

---

# 35. Aggregate version

Integration Event nên chứa aggregate version khi event thuộc Aggregate.

Consumer projection có thể lưu last applied version.

Nếu nhận version <= last:

- Duplicate/stale.
- Ignore safely hoặc verify event ID.

Nếu nhận version > last + 1:

- Gap.
- Retry/reconcile/query source.

---

# 36. Concurrency trong consumer

Consumer update own aggregate/projection phải có:

- Row lock hoặc optimistic lock.
- Inbox idempotency.
- Stable ordering policy.
- Retry classification.

Không dựa vào single worker assumption.

---

# 37. Retry classification

## Retryable

- Temporary DB unavailable.
- Deadlock/serialization.
- Provider timeout.
- Dependency 503.
- Missing previous event có khả năng đến sau.
- Lock timeout.

## Permanent

- Unsupported event version.
- Invalid schema.
- Missing required business reference không thể recover.
- Permission/configuration invariant permanent.
- Payload hash mismatch.
- Domain conflict không thể retry tự động.

Không retry mọi exception.

---

# 38. Consumer backoff

Retry policy:

- Exponential.
- Jitter.
- Max attempts.
- Max elapsed time.
- Next retry timestamp.
- Queue-specific.

Critical financial consumer có policy riêng.

---

# 39. Dead Letter Queue

DLQ message phải preserve:

- Original payload.
- Headers.
- Event ID.
- Consumer name.
- Attempt count.
- Error classification.
- First/last failure time.
- Correlation ID.

DLQ không được chứa thêm secret.

---

# 40. DLQ operations

Operators có thể:

- Inspect sanitized metadata.
- Retry.
- Resolve.
- Ignore với approval.
- Mark permanent.
- Open incident.
- Trigger reconciliation.

Mọi action auditable.

Không delete DLQ item để “dọn sạch” mà không resolution record.

---

# 41. Replay

## 41.1. Replay use cases

- Rebuild analytics projection.
- Rebuild timeline.
- Recover consumer bug.
- Backfill new projection.
- Reconcile stale derived state.

## 41.2. Replay không dùng cho

- Re-execute irreversible external payment.
- Re-send notification không kiểm soát.
- Re-issue receipt.
- Re-run payout confirmation.
- Re-use number issuance.

## 41.3. Replay modes

```text
DRY_RUN
PROJECTION_REBUILD
SAFE_SIDE_EFFECT
MANUAL_REVIEW
```

## 41.4. Replay authorization

- Restricted permission.
- Approval for sensitive contexts.
- Scope.
- Audit.
- Rate limit.
- Maintenance window.

---

# 42. Replay source

Replay source có thể là:

- Retained Outbox/Event Archive.
- Audit-approved event store.
- Source Context query.
- Snapshot + delta.

Không assume RabbitMQ là long-term event store.

---

# 43. Replay idempotency

Replay phải dùng same event ID hoặc explicit replay identity policy.

Consumer Inbox cần mode hỗ trợ:

- Reprocess same event intentionally.
- Separate replay run ID.
- Avoid irreversible side effects.

Không bypass Inbox bằng cách xóa processed rows tùy tiện.

---

# 44. Event retention

Retention theo event class.

Examples:

- Financial/legal events: long retention.
- Technical delivery events: shorter.
- Outbox published rows: baseline 30+ days.
- Inbox: baseline 90+ days.
- Event archive: policy-defined.
- DLQ: until resolved + retention.

Final policy nằm Data Retention Matrix.

---

# 45. Event archive

Nếu cần replay dài hạn, phải có Event Archive hoặc durable analytics/archive store.

Archive phải:

- Immutable.
- Integrity checked.
- Partitioned/retained.
- Access controlled.
- Searchable by event ID/type/time/aggregate.
- Not source of operational truth.

---

# 46. Event security classification

Mỗi Event Registry entry có classification:

```text
PUBLIC
INTERNAL
CONFIDENTIAL
RESTRICTED
HIGHLY_RESTRICTED
```

Broker queues/access tương ứng.

Không publish HIGHLY_RESTRICTED payload nếu consumer có thể query owner thay thế.

---

# 47. PII rules

Mặc định event không chứa:

- Full phone.
- Full email.
- Identity number.
- Bank account.
- Raw document.
- Full address.
- Financial evidence.
- Secret.
- Token.
- Signed URL.

Nếu bắt buộc:

- Có threat/privacy review.
- Có consumer allowlist.
- Encryption/access controls.
- Retention.
- Masking.
- Audit.

---

# 48. Actor data

Actor payload chỉ cần:

```text
actor_type
actor_key
```

Không nhúng full user profile.

System/service actor có stable key.

Actor may be:

```text
USER
SERVICE
SYSTEM
PROVIDER
BREAK_GLASS
```

---

# 49. Correlation and causation

## Correlation ID

Một business journey dùng cùng correlation ID.

Ví dụ:

```text
Booking Confirmed
→ Contract Created
→ Contract Activated
→ Revenue Entitlement Created
```

## Causation ID

Mỗi event/message chỉ trực tiếp bị gây bởi một command/event ID.

Không tạo new correlation ID ở mỗi hop nếu cùng journey.

---

# 50. Trace propagation

Broker headers phải propagate tracing theo OpenTelemetry standard.

Trace metadata không thay correlation ID.

Không persist sensitive baggage.

---

# 51. Event headers

Broker headers allowlist:

```text
event_id
event_type
event_version
correlation_id
causation_id
traceparent
producer_context
content_type
schema_uri
```

Không duplicate full payload fields vào headers.

---

# 52. Message size

Event phải nhỏ.

Baseline target:

```text
< 256 KB
```

Hard maximum theo broker/infrastructure policy.

Large payload:

- Store object/document separately.
- Event contains reference + hash.
- Reauthorize access.

Không nhúng file/base64.

---

# 53. Compression

Không compress individual small events mặc định.

Large technical messages chỉ compress khi:

- Supported.
- Measured.
- Security reviewed.
- Schema/content encoding explicit.

---

# 54. Event serialization

Canonical JSON:

- UTF-8.
- Deterministic field semantics.
- No NaN/Infinity.
- Decimal as string.
- Datetime UTC.
- Stable enum.
- Canonical hash for integrity/idempotency.

Không dùng Python pickle.

---

# 55. Schema validation

Validate:

- Before Outbox insert hoặc materialization.
- Before publish.
- On consumer ingress for external/untrusted messages.
- In contract tests.

Internal trusted events vẫn phải validate in tests/CI.

---

# 56. Schema compatibility checks

CI phải detect:

- Removed required field.
- Type change.
- Requiredness change.
- Enum narrowing.
- Format change.
- AdditionalProperties change.
- Semantic version mismatch.

Breaking diff phải fail nếu không có approved new version.

---

# 57. Event producer responsibilities

Producer phải:

1. Own business fact.
2. Emit after invariant passes.
3. Write Outbox transactionally.
4. Provide valid schema.
5. Document semantics.
6. Maintain compatibility.
7. Monitor publish health.
8. Support consumer questions.
9. Provide reconciliation API/path.
10. Deprecate responsibly.

---

# 58. Event consumer responsibilities

Consumer phải:

1. Declare purpose.
2. Register consumer.
3. Support versions.
4. Use Inbox.
5. Be idempotent.
6. Classify retry.
7. Handle ordering.
8. Monitor lag/failures.
9. Provide reconciliation.
10. Avoid source-of-truth takeover.

---

# 59. Producer does not know consumers

Producer không viết payload tùy consumer riêng nếu fact chung.

Nếu consumer-specific command cần thiết, dùng explicit command contract/port.

Không tạo event:

```text
booking.confirmed_for_contract_context
```

Nếu fact là `booking.confirmed`.

---

# 60. Choreography vs Process Manager

## Choreography

Phù hợp khi:

- Loose coupling.
- Independent reactions.
- No complex rollback.
- No central state.

## Process Manager

Bắt buộc khi:

- Multi-step.
- Timeouts.
- Compensation.
- Financial/legal critical.
- Need progress/state.
- Manual intervention.

Không dùng event choreography mù cho Contract Cancellation, Customer Merge hoặc Booking Confirmation complex flows nếu cần orchestration state.

---

# 61. Saga state

Process Manager state phải persist.

Fields:

```text
process_id
process_type
resource_id
status
current_step
started_at
updated_at
completed_at
correlation_id
failure_code
retry_count
```

Không lưu saga state chỉ trong Celery chain.

---

# 62. External events

Provider webhook không tự động trở thành Integration Event.

Flow:

```text
Provider Webhook
→ Verify
→ Persist raw receipt/reference
→ Map through Anti-Corruption Layer
→ Validate
→ Execute canonical command
→ Publish owned business event
```

Không publish raw provider payload cho toàn hệ thống.

---

# 63. External outbound events

Outbound webhook/subscription:

- Derived from owned Integration Event.
- Mapping version.
- Subscriber contract.
- Signature.
- Retry.
- DLQ.
- Delivery log.
- Secret reference.
- PII policy.

External delivery failure không rollback business transaction.

---

# 64. Analytics event consumption

Analytics:

- Consumer of operational events.
- Own projection.
- Store event ID/version.
- Support replay.
- Track freshness.
- Reconcile to source.
- Never write operational state.

---

# 65. Timeline event consumption

Activity Timeline projection:

- Read-only.
- Source event reference.
- Masking at query.
- Merge redirect support.
- Replay.
- Not source of truth.

Không copy full sensitive payload.

---

# 66. Notification consumption

Notification consumer:

- Reauthorize recipient/resource if needed.
- Apply preferences/suppression.
- Use template version.
- Avoid duplicate sends.
- Track delivery.
- Event itself không guarantee notification success.

---

# 67. Audit event relationship

Business Integration Event không thay Audit Event.

Audit captures:

- Actor.
- Command/action.
- Outcome.
- Resource.
- Reason.

Integration Event captures:

- Business fact for consumers.

Cả hai có thể cùng transaction nhưng là contract khác.

---

# 68. Event observability metrics

Required metrics:

```text
crm_event_outbox_pending_total
crm_event_outbox_retry_total
crm_event_outbox_dead_total
crm_event_outbox_publish_duration_seconds
crm_event_outbox_oldest_age_seconds
crm_event_consumer_received_total
crm_event_consumer_processed_total
crm_event_consumer_duplicate_total
crm_event_consumer_retry_total
crm_event_consumer_permanent_failure_total
crm_event_consumer_lag_seconds
crm_event_dlq_total
crm_event_replay_total
crm_event_schema_validation_failure_total
crm_event_ordering_gap_total
```

Labels low-cardinality:

- event_type.
- event_version.
- producer_context.
- consumer_name.
- result.
- error_code.

Không label event ID/aggregate ID.

---

# 69. Event logs

Structured fields:

```text
event_id
event_type
event_version
producer_context
consumer_name
aggregate_type
aggregate_id_hash_or_safe_reference
correlation_id
causation_id
attempt
result
error_code
duration_ms
```

Không log full payload mặc định.

---

# 70. Event tracing

Spans:

- Outbox insert.
- Outbox claim.
- Broker publish.
- Broker receive.
- Inbox acquire.
- Handler execute.
- Ack.
- Retry/DLQ.

Trace không chứa PII payload.

---

# 71. Alert thresholds

Alerts tối thiểu:

- Outbox oldest age vượt threshold.
- Dead Outbox > 0 critical events.
- Consumer lag vượt threshold.
- Permanent failure.
- Unsupported version.
- Payload hash mismatch.
- DLQ growth.
- Replay unexpected side effect.
- Audit/event transaction mismatch.
- Queue unavailable.

Threshold cụ thể trong Operations/SLO docs.

---

# 72. Health checks

Readiness có thể kiểm tra:

- Database.
- Broker.
- Outbox publisher health.
- Critical consumer registration.

Không mark entire API unhealthy chỉ vì non-critical consumer lag, nhưng phải degraded.

---

# 73. Outbox cleanup

Cleanup chỉ `PUBLISHED` đủ retention.

Phải:

- Chunked.
- Indexed.
- Observable.
- Respect legal/event archive policy.
- Không xóa DEAD chưa resolved.
- Không lock large table lâu.

---

# 74. Inbox cleanup

Cleanup processed rows theo retention và replay policy.

Nếu consumer replay cần lâu hơn, archive summary trước cleanup.

Không xóa permanent failures chưa resolved.

---

# 75. Event reconciliation

Mỗi critical consumer phải có reconciliation strategy.

Examples:

- Booking confirmed nhưng Contract chưa tạo.
- Payment allocated nhưng Receipt projection thiếu.
- Customer merged nhưng Lead reference chưa rebind.
- Commission entitlement expected nhưng chưa có.

Reconciliation:

- Query source.
- Detect gap.
- Create finding.
- Retry/repair safely.
- Audit.
- Metrics.

---

# 76. Event consistency model

Cross-context consistency là eventual consistency.

API/UI phải phản ánh:

- Pending.
- Processing.
- Synchronized.
- Failed.
- Reconciliation required.

Không giả vờ atomic cross-context transaction.

---

# 77. UI implications

UI không được assume event side effect hoàn tất ngay.

Nếu command bắt đầu async process:

- Return process state.
- Poll/subscription.
- Show pending.
- Show partial failure.
- Offer retry/escalation when allowed.

---

# 78. Event-driven cache invalidation

Consumers có thể invalidate cache theo versioned event.

Cache invalidation:

- Idempotent.
- Safe on duplicate.
- Not business side effect.
- Fallback TTL.

Không dựa chỉ vào cache invalidation để correctness.

---

# 79. Event-driven read models

Projection updater:

- Inbox.
- Event version.
- Last applied aggregate version.
- Replay.
- Rebuild.
- Idempotent upsert.
- Freshness.

Projection table owner là consumer Context.

---

# 80. Event schema documentation

Mỗi event docs phải có:

- Business meaning.
- Trigger.
- Producer.
- Event timing.
- Payload.
- Version.
- Consumers.
- Ordering.
- Idempotency.
- Classification.
- Replay.
- Deprecation.
- Examples.

---

# 81. Example — Booking Confirmed

```json
{
  "event_id": "018f0000-0000-7000-8000-000000000001",
  "event_type": "transaction.booking.confirmed",
  "event_version": 1,
  "occurred_at": "2026-07-24T10:00:00Z",
  "recorded_at": "2026-07-24T10:00:00Z",
  "producer": {
    "context": "transaction",
    "service": "crm-bds-next"
  },
  "aggregate": {
    "type": "Booking",
    "id": "018f0000-0000-7000-8000-000000000002",
    "version": 7
  },
  "scope": {
    "enterprise_id": "018f0000-0000-7000-8000-000000000003",
    "legal_entity_id": "018f0000-0000-7000-8000-000000000004",
    "project_id": "018f0000-0000-7000-8000-000000000005"
  },
  "correlation_id": "018f0000-0000-7000-8000-000000000006",
  "causation_id": "018f0000-0000-7000-8000-000000000007",
  "trace_id": "00000000000000000000000000000001",
  "actor": {
    "actor_type": "USER",
    "actor_key": "018f0000-0000-7000-8000-000000000008"
  },
  "data": {
    "booking_id": "018f0000-0000-7000-8000-000000000002",
    "transaction_case_id": "018f0000-0000-7000-8000-000000000009",
    "listing_id": "018f0000-0000-7000-8000-000000000010",
    "commercial_snapshot_id": "018f0000-0000-7000-8000-000000000011",
    "confirmed_at": "2026-07-24T10:00:00Z"
  },
  "metadata": {
    "schema_uri": "urn:crm-bds-next:event:transaction:booking-confirmed:1",
    "content_type": "application/json"
  }
}
```

---

# 82. Example — Payment Allocated

Payload phải phân biệt:

- Payment.
- Receivable.
- Allocation.
- Amount.
- Currency.
- Reversal lineage.

Không nhúng bank account hoặc payment evidence.

---

# 83. Example — Customer Merged

Payload tối thiểu:

```text
merge_case_id
surviving_customer_id
merged_customer_ids
executed_at
```

Consumers dùng redirect/resolution API nếu cần chi tiết.

Không nhúng full Customer profiles.

---

# 84. Testing hierarchy

## Unit tests

- Domain Event creation.
- Event mapper.
- Envelope builder.
- Canonical serialization.
- Payload hash.
- Retry classification.
- Ordering policy.
- Replay policy.

## Integration tests

- Business state + Outbox atomic.
- Outbox claim.
- Publisher confirm.
- Inbox transaction.
- Duplicate.
- Retry.
- DLQ.
- Stale claim recovery.

## Contract tests

- JSON Schema.
- AsyncAPI.
- Event Registry.
- Examples.
- Compatibility.

## Concurrency tests

- Multiple publishers.
- Duplicate delivery.
- Same aggregate out-of-order.
- Consumer lock.
- First Inbox insert race.

## Security tests

- PII absence.
- Secret absence.
- Queue access.
- Unsupported producer.
- Payload hash mismatch.
- Replay permission.

## Failure injection

- Broker down.
- DB down.
- Publish confirm lost.
- Consumer crash before commit.
- Consumer crash after commit before ack.
- DLQ unavailable.
- Schema registry mismatch.

---

# 85. Domain Event unit tests

Mỗi Aggregate transition phải test:

- Correct event type.
- Correct data.
- Correct occurred_at.
- Correct aggregate version handling.
- No event on failed transition.
- Exactly one event for one fact unless spec says otherwise.
- No PII leakage.

---

# 86. Outbox atomicity tests

Scenario:

1. Aggregate changes.
2. Audit insert.
3. Outbox insert.
4. Force failure.
5. Rollback.

Expected:

- No aggregate change.
- No Audit.
- No Outbox.

Success:

- All three committed.

---

# 87. Outbox concurrency tests

- 10 publisher workers.
- 1,000 pending rows.
- `SKIP LOCKED`.
- No row claimed concurrently.
- All eventually published.
- Duplicate publish acceptable only under injected confirm ambiguity.
- No lost row.

---

# 88. Publisher confirm failure tests

Cases:

- Publish rejected.
- Confirm timeout.
- Connection close.
- Channel error.
- Broker unavailable.

Expected:

- Retry/Dead policy.
- No false `PUBLISHED`.
- Metrics/logs.

---

# 89. Inbox duplicate tests

- Same event twice sequential.
- Same event concurrent.
- Same event after consumer restart.
- Same event from replay.
- Same event ID different hash.

Expected:

- One side effect.
- Duplicate ack.
- Hash mismatch alert.

---

# 90. Crash-window tests

## Crash after side effect commit before ack

Broker redelivers.

Inbox sees processed.

No duplicate side effect.

## Crash before commit

Broker redelivers.

Handler retries safely.

## Crash after Inbox insert before processing

Stale processing recovery.

---

# 91. Ordering tests

- Version 1 then 2.
- Version 2 before 1.
- Duplicate 1.
- Missing 2 then 3.
- Replay old event after latest.

Consumer policy must be explicit and tested.

---

# 92. Compatibility tests

For every schema change:

- Old consumer sample validates new event if non-breaking.
- New consumer validates old event where promised.
- Breaking diff requires new version.
- Examples validate.
- Registry version matches schema.

---

# 93. Replay tests

- Projection rebuild.
- Duplicate replay.
- Dry run.
- Forbidden irreversible consumer.
- Replay with scope.
- Replay rate limit.
- Replay audit.

---

# 94. Performance tests

Measure:

- Outbox insert overhead.
- Claim throughput.
- Publish throughput.
- Consumer throughput.
- Lag.
- Inbox contention.
- Payload size.
- Replay throughput.
- Cleanup performance.

Critical targets thuộc NFR/SLO.

---

# 95. Architecture tests

Fail nếu:

- Domain imports broker/Celery.
- Router publishes directly.
- Business handler calls RabbitMQ.
- Context creates private Outbox table.
- Consumer lacks Inbox.
- Event lacks schema.
- Event type lacks registry.
- Consumer writes producer schema.
- Analytics writes operational schema.
- Notification event used as business truth.
- Raw provider webhook published directly.

---

# 96. Event test file plan

```text
tests/unit/events/
├── test_event_envelope.py
├── test_event_serialization.py
├── test_event_hashing.py
├── test_event_registry.py
└── test_retry_classification.py

tests/integration/events/
├── test_outbox_atomicity.py
├── test_outbox_claiming.py
├── test_outbox_publisher_confirm.py
├── test_inbox_processing.py
├── test_inbox_duplicates.py
├── test_stale_claim_recovery.py
└── test_dlq_flow.py

tests/contract/events/
├── test_json_schemas.py
├── test_asyncapi.py
├── test_event_examples.py
└── test_event_compatibility.py

tests/concurrency/events/
├── test_multi_publisher_claiming.py
├── test_concurrent_duplicate_delivery.py
└── test_ordering_gap_handling.py

tests/security/events/
├── test_event_payload_classification.py
├── test_no_secret_or_pii.py
├── test_replay_authorization.py
└── test_payload_hash_conflict.py
```

---

# 97. CI requirements

CI jobs:

- Event schema validation.
- AsyncAPI validation.
- Registry consistency.
- Example validation.
- Compatibility diff.
- Unit tests.
- PostgreSQL Outbox/Inbox integration.
- RabbitMQ integration.
- Concurrency.
- Security.
- Architecture tests.

No event contract can merge with failed compatibility check.

---

# 98. Broker local/test environment

Tests phải dùng real RabbitMQ container cho integration.

Không chỉ mock broker.

Unit tests có fake publisher.

Integration tests verify:

- Durable exchange.
- Queue binding.
- Confirm.
- Ack.
- Redelivery.
- DLQ.

---

# 99. RabbitMQ operational rules

- Durable exchanges/queues.
- Persistent messages.
- Publisher confirms.
- Manual consumer ack.
- Prefetch tuned.
- DLQ configured.
- Queue TTL only when explicitly designed.
- Quorum/classic queue choice documented.
- No auto-delete for critical queues.
- No exclusive queue for business consumers.

---

# 100. Prefetch

Prefetch theo handler cost.

Không đặt quá cao gây unfairness/memory.

Financial/slow consumers dùng lower prefetch.

Measure before tuning.

---

# 101. Consumer scaling

Horizontal scaling allowed when:

- Inbox.
- Ordering policy.
- Locking.
- Idempotency.
- Partitioning key.

Không scale consumer mù nếu aggregate ordering cần single partition.

---

# 102. Event partition/routing key

Routing/partition key có thể là:

- Aggregate ID.
- Enterprise ID.
- Legal Entity ID.
- Project ID.

Chọn theo ordering/load requirements.

Phải document per event/consumer.

---

# 103. Backpressure

Khi consumer lag:

- Queue retains.
- Autoscale if safe.
- Rate limit producer only if business-safe.
- Alert.
- Degrade non-critical consumers.
- Preserve critical financial flows.

Không drop event.

---

# 104. Poison messages

Poison message:

- Repeated permanent failure.
- Move DLQ.
- Preserve evidence.
- Alert.
- Stop infinite retry.

Không block entire queue indefinitely nếu one message fails; retry topology phải tránh head-of-line blocking.

---

# 105. Event-driven external side effects

External side effect consumer phải có provider idempotency key.

Examples:

- Email send.
- Signature request.
- Outbound webhook.
- Payment initiation.

Inbox alone không đủ nếu provider request có uncertain outcome.

---

# 106. Provider uncertainty

Nếu timeout sau request:

- Do not assume failed.
- Query provider/reconcile.
- Use provider idempotency.
- Persist request reference.
- Avoid duplicate financial action.

---

# 107. Financial event rules

Financial events:

- Minimal payload.
- Decimal as string.
- Currency explicit.
- Immutable source reference.
- Long retention.
- Strict consumer allowlist.
- No full bank evidence.
- Strong replay restrictions.
- Reconciliation mandatory.

---

# 108. Receipt event rules

`contract.receipt.issued`:

- Receipt ID.
- Receipt number.
- Contract/Payment references.
- Issued at.
- Total amount/currency if required.
- Replacement lineage if applicable.

No direct edit event.

Correction:

```text
receipt.cancelled
receipt.replacement_issued
```

---

# 109. Commission event rules

Events distinguish:

```text
commission_entitlement.created
commission_entitlement.vested
commission_payable.created
commission_payout.confirmed
commission_clawback.applied
```

Không publish generic `commission.updated`.

---

# 110. Customer identity event rules

Events:

```text
party.customer.created
party.customer.phone_verified
party.customer.merged
party.customer.canonical_redirect_created
```

PII minimized.

Merge event must be replay-safe.

---

# 111. Commercial Lock event rules

Events:

```text
product.commercial_lock.requested
product.commercial_lock.activated
product.commercial_lock.extended
product.commercial_lock.released
product.commercial_lock.expired
product.commercial_lock.converted
```

Event includes lock/listing IDs, timing, status fact.

No private pricing unless required.

---

# 112. State change event policy

Không phải mọi field update cần public Integration Event.

Publish khi:

- Other Context depends.
- Audit/business milestone.
- Projection needs update.
- Integration needs signal.

Không publish event noise cho every profile typo fix nếu không có consumer/business meaning.

---

# 113. Event granularity

Too coarse:

```text
customer.updated
```

Too fine:

```text
customer_first_name_character_changed
```

Correct granularity theo meaningful fact:

```text
customer.contact_identity_verified
customer.primary_phone_changed
customer.merged
```

---

# 114. Batch events

Không gom nhiều unrelated business facts vào một giant event.

Batch event hợp lệ cho technical/import projection nếu:

- Items bounded.
- Each item has identity/result.
- Retry semantics clear.
- Payload size safe.

Critical business events thường one fact per message.

---

# 115. Event evolution guidelines

Khi cần thêm field:

1. Xác định consumer need.
2. Kiểm tra classification.
3. Thêm optional.
4. Update schema/examples.
5. Compatibility test.
6. Update AsyncAPI/registry.
7. Notify consumers.
8. Deploy producer after consumer tolerance nếu needed.

---

# 116. Event deprecation

Deprecation requires:

- New replacement event/version.
- Consumer inventory.
- Usage metrics.
- Migration deadline.
- Sunset.
- Archive compatibility.
- Documentation.

Không ngừng publish event khi consumer chưa migrate.

---

# 117. Consumer inventory

Registry phải biết expected consumers.

Không để hidden consumer không owner.

Consumer registration:

- Name.
- Context.
- Owner.
- Queue.
- Supported versions.
- Criticality.
- Retry/DLQ.
- Replay allowed.
- SLO.

---

# 118. Criticality classes

```text
CRITICAL_FINANCIAL
CRITICAL_BUSINESS
OPERATIONAL
ANALYTICAL
BEST_EFFORT
```

Criticality ảnh hưởng:

- Alert.
- Retention.
- Retry.
- Replay.
- Queue.
- SLO.
- On-call.

---

# 119. Best-effort policy

Best-effort chỉ cho non-critical side effects như optional analytics telemetry.

Không dùng best-effort cho:

- Contract.
- Payment.
- Receipt.
- Revenue.
- Commission.
- Customer merge.
- Commercial Lock.

---

# 120. Security review checklist

- Payload classification?
- PII minimized?
- Secret absent?
- Consumer allowlist?
- Broker ACL?
- Replay access?
- Retention?
- Logs?
- DLQ access?
- External exposure?
- Integrity hash?

---

# 121. Event design review checklist

## Meaning

- Fact đã xảy ra?
- Producer owner đúng?
- Past tense?
- Granularity đúng?

## Contract

- Schema?
- Version?
- Examples?
- AsyncAPI?
- Registry?

## Data

- Minimal?
- Snapshot/reference?
- Money/time types?
- PII?

## Reliability

- Outbox?
- Inbox?
- Idempotency?
- Retry?
- Ordering?
- Reconciliation?

## Operations

- Metrics?
- DLQ?
- Replay?
- Retention?
- Owner?

---

# 122. Anti-patterns bị cấm

1. Direct broker publish trong request transaction.
2. Domain imports Celery/RabbitMQ.
3. Event không schema.
4. Event generic `entity.updated`.
5. Event chứa full Aggregate.
6. Event chứa secret/PII không review.
7. Consumer không Inbox.
8. Ack trước commit.
9. Retry mọi exception.
10. Infinite retry.
11. Delete DLQ không resolution.
12. Assume global ordering.
13. Use broker as long-term event store.
14. Replay irreversible side effects.
15. Raw provider webhook broadcast.
16. Notification event làm business truth.
17. Cross-context write trong consumer.
18. Event schema breaking edit in place.
19. No consumer owner.
20. No reconciliation for critical flow.
21. Store binary/base64 in event.
22. Claim exactly-once without proof.
23. Mark Outbox published without confirm.
24. Log full payload.
25. Reuse event ID.

---

# 123. AI Agent event protocol

Trước khi tạo Event, AI Agent phải:

1. Xác định business fact.
2. Xác định producer owner.
3. Xác định Domain Event hay Integration Event.
4. Xác định consumers.
5. Xác định payload tối thiểu.
6. Xác định classification.
7. Xác định version.
8. Tạo JSON Schema.
9. Update AsyncAPI.
10. Update Event Registry.
11. Implement Outbox.
12. Implement consumer Inbox.
13. Xác định retry/ordering/replay.
14. Implement tests.
15. Add metrics/logs.
16. Update docs.

---

# 124. AI Agent prohibited event behaviors

AI Agent không được:

1. Tạo event vì “có thể cần sau”.
2. Publish trực tiếp từ router.
3. Bỏ Outbox.
4. Bỏ Inbox.
5. Nhúng ORM/request object.
6. Tự thêm PII.
7. Tự rename event published.
8. Tự sửa schema v1 breaking.
9. Tự coi duplicate là impossible.
10. Tự assume ordering.
11. Tự replay financial side effect.
12. Tự delete DLQ.
13. Bỏ AsyncAPI/Registry.
14. Báo Done khi contract tests fail.
15. Dùng event để bypass Context ownership.

---

# 125. Definition of Ready cho Event

Event chỉ Ready khi:

1. Business fact rõ.
2. Producer owner rõ.
3. Consumer need rõ.
4. Event name/version rõ.
5. Payload/classification rõ.
6. Ordering/idempotency rõ.
7. Retry/DLQ rõ.
8. Replay/retention rõ.
9. Schema/AsyncAPI draft rõ.
10. Reconciliation rõ.
11. No ownership conflict.

---

# 126. Definition of Done cho Event producer

Producer Done khi:

1. Domain/Application event mapping.
2. Outbox transaction.
3. Schema valid.
4. AsyncAPI updated.
5. Registry updated.
6. Examples valid.
7. Publish metrics/logs.
8. Atomicity tests.
9. Compatibility tests.
10. Security review.
11. Docs updated.

---

# 127. Definition of Done cho Consumer

Consumer Done khi:

1. Registered consumer name.
2. Queue/binding.
3. Supported versions.
4. Inbox.
5. Idempotent handler.
6. Retry classification.
7. Ordering policy.
8. DLQ.
9. Reconciliation.
10. Metrics/logs.
11. Duplicate/concurrency/failure tests.
12. Replay policy.
13. Runbook.
14. Docs updated.

---

# 128. Runbooks bắt buộc

```text
docs/runbooks/outbox-backlog.md
docs/runbooks/event-consumer-failure.md
docs/runbooks/event-dlq.md
docs/runbooks/event-replay.md
docs/runbooks/event-schema-compatibility.md
docs/runbooks/rabbitmq-failure.md
```

---

# 129. Completion report

Event-related task phải báo:

```markdown
## Event Changes

- Domain Events:
- Integration Events:
- Event versions:
- Schema files:
- AsyncAPI changes:
- Registry changes:
- Producers:
- Consumers:
- Queues:
- Inbox:
- Retry/DLQ:
- Ordering:
- Replay:
- Security classification:
- Tests:
- Metrics:
- Runbooks:
```

---

# 130. Exception process

Ngoại lệ cần file:

```text
docs/engineering/event-exceptions/EXC-EVENT-XXX.md
```

Nội dung:

- Rule.
- Event/consumer.
- Reason.
- Reliability impact.
- Compatibility impact.
- Security impact.
- Replay impact.
- Mitigation.
- Owner.
- Expiry.
- Approval.

Không có ngoại lệ vô thời hạn không owner.

---

# 131. Change Log

## Version 1.0.0 — 2026-07-24

- Thiết lập Event taxonomy.
- Khóa Event naming và versioning.
- Khóa canonical Event Envelope.
- Khóa JSON Schema và AsyncAPI.
- Khóa Transactional Outbox.
- Khóa Consumer Inbox.
- Khóa at-least-once semantics.
- Khóa retry, DLQ, ordering và replay.
- Khóa security/PII/event classification.
- Khóa observability, reconciliation và testing.
- Khóa AI Agent event protocol và anti-patterns.

---

# 132. Kết luận

Event architecture của `crm_bds_ai` phải bảo đảm:

```text
Business Fact
+ Transactional Outbox
+ At-Least-Once Delivery
+ Idempotent Consumer
+ Versioned Contract
+ Controlled Replay
+ Observable Failure
+ Reconciliation
```

Nguyên tắc tối cao:

> Event chỉ có giá trị khi fact đúng, contract ổn định, delivery đáng tin cậy và consumer có thể xử lý duplicate, retry, out-of-order và replay một cách an toàn.
