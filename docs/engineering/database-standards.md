# CRM_BDS_AI — DATABASE STANDARDS

## Quy chuẩn cơ sở dữ liệu bắt buộc cho toàn bộ hệ thống `crm_bds_ai`

**Document ID:** `ENG-DB-001`  
**Canonical path:** `docs/engineering/database-standards.md`  
**Product:** `crm_bds_ai`  
**Version:** `1.0.0`  
**Status:** `Accepted / Mandatory`  
**Canonical:** `Yes` đối với tiêu chuẩn thiết kế và triển khai cơ sở dữ liệu  
**Owner:** `Database Architecture Owner`  
**Reviewers:** `Architecture Owner`, `Technical Owner`, `Security Owner`, `Context Owners`, `QA Owner`, `Operations Owner`  
**Effective date:** `2026-08-05`  
**Last reviewed:** `2026-08-05`  
**Next review:** Khi PostgreSQL, Alembic, migration strategy, data governance hoặc architecture boundaries thay đổi  
**Supersedes:** `None — Greenfield baseline`  
**Superseded by:** Không

---

# 1. Mục đích

Tài liệu này quy định cách thiết kế, tạo, thay đổi, truy vấn, kiểm thử, vận hành và bảo vệ dữ liệu trong `crm_bds_ai`.

Mục tiêu:

1. Bảo đảm mỗi Bounded Context có ownership rõ.
2. Bảo đảm schema vật lý phản ánh đúng domain boundaries.
3. Ngăn cross-context write trực tiếp.
4. Bảo đảm invariant quan trọng được bảo vệ ở nhiều lớp.
5. Bảo đảm migration an toàn.
6. Bảo đảm transaction và concurrency rõ ràng.
7. Bảo đảm dữ liệu tài chính, audit và evidence không bị sửa sai.
8. Bảo đảm query có hiệu năng và scope đúng.
9. Bảo đảm dữ liệu temporal, monetary và identity được mô hình nhất quán.
10. Bảo đảm mọi AI Agent và developer cùng dùng một chuẩn.

Tài liệu này phải được đọc cùng:

```text
docs/engineering/coding-standards.md
docs/engineering/api-standards.md
docs/engineering/event-standards.md
docs/engineering/testing-standards.md
docs/architecture/source-of-truth-matrix.md
docs/architecture/context-map.md
docs/architecture/transaction-boundaries.md
Relevant Context Implementation Pack
Current Sprint Execution Pack
```

---

# 2. Nguyên tắc tối cao

```text
Domain Ownership
> Data Integrity
> Security
> Auditability
> Correct Concurrency
> Recoverability
> Query Performance
> Convenience
```

Không được hy sinh constraint, transaction hoặc source of truth chỉ để schema đơn giản hơn.

---

# 3. Database platform

## 3.1. Hệ quản trị

Primary operational database:

```text
PostgreSQL 18.x
```

Version thực tế theo Technology Toolchain Lock.

## 3.2. Không hỗ trợ thay thế

Không dùng:

- SQLite cho integration tests.
- MySQL compatibility mode.
- MongoDB thay PostgreSQL cho operational truth.
- Valkey làm source of truth.
- Spreadsheet làm business database.
- External search index làm source of truth.
- Analytics warehouse làm operational truth.

## 3.3. Extensions

Chỉ sử dụng extension được phê duyệt, ví dụ:

```text
btree_gist
pgcrypto khi thực sự cần
uuid-ossp chỉ khi có lý do, không mặc định
pg_trgm nếu search design được phê duyệt
```

Mỗi extension phải:

- Có migration.
- Có operational support.
- Có security review.
- Có fallback/compatibility consideration.
- Không được thêm tùy tiện.

---

# 4. Một database, schema theo Context

## 4.1. Schemas chuẩn

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

## 4.2. Schema ownership

Mỗi Context chỉ sở hữu schema cùng tên.

Ví dụ:

```text
product → schema product
contract → schema contract
revenue → schema revenue
```

## 4.3. Schema `public`

- Không chứa business tables.
- Không chứa business functions.
- Không chứa enum domain.
- Không chứa migration-owned objects trừ extension/system need.
- `CREATE` trên schema `public` phải bị revoke khỏi PUBLIC.

## 4.4. Không cross-context business write

Bị cấm:

```sql
UPDATE contract.contracts
SET ...
FROM transaction.bookings ...
```

từ code thuộc Context `transaction`.

Bị cấm:

- Repository Context A update table Context B.
- Trigger Context A ghi table Context B.
- Stored procedure shared ghi nhiều schema nghiệp vụ.
- Background job direct-write cross-context.

Hợp lệ:

- Application port.
- Internal API.
- Event consumer.
- Process Manager.
- Controlled AuditWriter port.
- Read-only projection được ADR phê duyệt.

---

# 5. Database roles

## 5.1. Roles đề xuất

```text
crm_schema_owner
crm_migrator_role
crm_runtime_role
crm_worker_role
crm_audit_writer_role
crm_audit_reader_role
crm_operations_reader_role
crm_analytics_reader_role
```

## 5.2. Login principals

Local/test có thể dùng:

```text
crm_migrator
crm_app
crm_worker
crm_audit_writer
crm_readonly
```

Production credentials đến từ secret management.

## 5.3. Ownership

- `crm_schema_owner` sở hữu schemas/tables.
- `crm_migrator` chạy migration bằng role phù hợp.
- Runtime app không sở hữu object.
- Runtime app không được DDL.
- Read-only roles không write.
- Audit writer chỉ INSERT tối thiểu.
- Analytics reader không write operational schemas.

## 5.4. Default privileges

Migration phải set default privileges.

Không để table mới vô tình public-readable hoặc public-writable.

---

# 6. Naming conventions

## 6.1. Schema

```text
lowercase_snake_case
```

## 6.2. Table

Plural noun hoặc collective semantic rõ:

```text
customers
commercial_locks
payment_allocations
audit_events
```

Không dùng:

```text
tbl_customer
t_customer
data
items
records
misc
```

## 6.3. Column

```text
snake_case
```

## 6.4. Primary key

```text
id
```

## 6.5. Foreign key

```text
<resource>_id
```

Ví dụ:

```text
enterprise_id
legal_entity_id
customer_id
listing_id
```

## 6.6. Timestamps

```text
created_at
updated_at
activated_at
published_at
issued_at
cancelled_at
```

## 6.7. Actor fields

```text
created_by
updated_by
approved_by
issued_by
```

Hoặc actor key nếu actor không chỉ user UUID:

```text
issued_by_actor_key
```

## 6.8. Constraints

```text
pk_<table>
fk_<table>_<column>_<ref_table>
uq_<table>_<columns>
ck_<table>_<rule>
ex_<table>_<rule>
```

## 6.9. Indexes

```text
ix_<table>_<columns_or_purpose>
```

Partial index:

```text
ix_outbox_claim
```

## 6.10. Migration revision names

```text
s003_0001_create_enterprise_and_legal_entity
```

Không dùng:

```text
update_db
fix_schema
final_migration
new_tables
```

---

# 7. Primary keys

## 7.1. UUIDv7

Primary keys cho business records phải dùng UUIDv7.

Lợi ích:

- Globally unique.
- Không phụ thuộc sequence public.
- Tốt hơn UUIDv4 cho index locality.
- Hỗ trợ distributed creation.

## 7.2. Không dùng integer ID làm business identity

Integer có thể dùng cho:

- Ordinal.
- Version number.
- Sequence counter.
- Small reference table nội bộ khi được phê duyệt.

Không expose integer surrogate như public resource identity.

## 7.3. UUID generation

- Generate tại application/shared provider.
- Test dùng deterministic provider.
- Không gọi random UUID trực tiếp rải rác.
- Database default có thể hỗ trợ fallback nếu ADR cho phép.
- Canonical format lowercase.

---

# 8. Common metadata columns

Bảng mutable thông thường nên có:

```sql
id uuid PRIMARY KEY,
created_at timestamptz NOT NULL,
created_by uuid NULL,
updated_at timestamptz NOT NULL,
updated_by uuid NULL,
row_version bigint NOT NULL DEFAULT 1
```

Không bắt buộc mọi bảng có mọi field.

Append-only table thường chỉ cần:

```text
created_at
recorded_at
actor reference
```

Không thêm `updated_at` giả vào immutable table.

---

# 9. Timestamps

## 9.1. Storage

Instant phải lưu:

```text
timestamptz
```

## 9.2. Timezone

PostgreSQL session timezone phải nhất quán, mặc định UTC.

## 9.3. Local recurring time

Business recurring local time có thể dùng:

```text
time
```

kèm:

```text
timezone
```

trên version/calendar.

## 9.4. Date

Dùng `date` cho:

- Business date.
- Effective date.
- Birth date nếu domain cho phép.
- Holiday date.
- Reporting date.

Không dùng `timestamp` khi meaning chỉ là date.

## 9.5. Không dùng naive timestamp

Không dùng:

```text
timestamp without time zone
```

cho instant.

Chỉ dùng khi local wall-clock semantics thực sự cần và timezone được lưu riêng, có tài liệu rõ.

---

# 10. Effective periods

## 10.1. Standard columns

```text
effective_from
effective_to
```

## 10.2. Boundary

Mặc định:

```text
[effective_from, effective_to]
```

cho date nếu domain dùng inclusive end.

Hoặc dùng range `[start, end)` cho timestamp.

Phải ghi rõ trong Context Pack.

## 10.3. Validation

```sql
CHECK (effective_to IS NULL OR effective_to >= effective_from)
```

## 10.4. No overlap

Dùng exclusion constraint khi cần:

```sql
EXCLUDE USING gist (
    scope_key WITH =,
    daterange(effective_from, COALESCE(effective_to + 1, 'infinity'::date), '[)') WITH &&
)
WHERE (status = 'PUBLISHED')
```

Không chỉ kiểm tra overlap bằng application.

---

# 11. Versioned records

Áp dụng cho:

- Calendar Version.
- Numbering Version.
- Configuration Version.
- Workflow Version.
- Approval Policy Version.
- Listing Price Version.
- Proposal Version.
- Contract Version.
- Metric Version.
- Template Version.

## 11.1. Fields

```text
version_number
status
effective_from
effective_to
published_at
published_by
```

## 11.2. Rules

- Version number unique trong parent.
- Published immutable.
- Không sửa historical version.
- Tạo version mới để thay đổi.
- Effective overlap bị chặn.
- Historical version không hard-delete.
- Resource reference phải ghi exact version ID khi cần auditability.

---

# 12. Status columns

Status lưu stable code.

Ví dụ:

```text
DRAFT
ACTIVE
SUSPENDED
ARCHIVED
```

Không lưu display text tiếng Việt.

Không dùng `is_active` khi lifecycle có nhiều state.

Không generic update status.

Database check constraint phải enumerate allowed values khi ổn định.

---

# 13. Enum strategy

Ưu tiên:

```text
varchar + CHECK constraint
```

thay vì PostgreSQL enum khi cần migration linh hoạt.

PostgreSQL enum chỉ dùng nếu ADR cho phép.

Lý do tránh enum native mặc định:

- Khó rollback.
- Khó đổi thứ tự/lifecycle.
- Khó reuse across contexts.
- Dễ coupling migration.

---

# 14. String standards

## 14.1. `varchar(n)` khi có business limit

Ví dụ:

```text
code varchar(50)
name varchar(200)
description varchar(1000)
```

## 14.2. `text`

Dùng khi không có business max cụ thể nhưng cần giới hạn application/API.

## 14.3. Normalization

Code:

- Uppercase.
- Trim.
- Stable.
- Regex check.

Names:

- Preserve user-visible case.
- Search có normalized expression/index khi cần.

## 14.4. Không lưu comma-separated values

Bị cấm:

```text
project_ids = 'a,b,c'
```

Dùng relation table.

---

# 15. Numeric types

## 15.1. Money

```text
numeric(20,4)
```

hoặc type được Financial Architecture phê duyệt.

Không dùng:

```text
float
double precision
real
```

cho money.

## 15.2. Percentage/rate

Dùng numeric precision rõ:

```text
numeric(12,8)
```

tùy domain.

Ghi rõ:

- 0.15 nghĩa 15%.
- hay 15 nghĩa 15%.

Không để ambiguity.

## 15.3. Counters

Dùng:

```text
bigint
```

nếu có thể tăng lớn.

## 15.4. Quantity

Chọn integer hoặc numeric theo domain.

---

# 16. Currency

## 16.1. Column

```text
currency char(3)
```

## 16.2. Validation

ISO 4217 active code.

Có thể validate application/reference registry.

Database check regex:

```sql
CHECK (currency ~ '^[A-Z]{3}$')
```

không đủ để chứng minh valid ISO code, nhưng là structural guard.

## 16.3. Multi-currency

Amount luôn gắn currency khi domain có khả năng nhiều currency.

Không suy currency từ Legal Entity nếu record có historical financial meaning; nên snapshot currency trên record.

---

# 17. JSONB policy

## 17.1. JSONB được phép

- Typed configuration payload.
- External raw payload reference/snapshot.
- Event payload.
- Safe audit metadata.
- Schema-defined provider metadata.
- Flexible criteria snapshot có JSON Schema.

## 17.2. JSONB bị cấm làm default relational model

Không nhét vào JSONB:

- Customer core fields.
- Contract parties.
- Payment allocations.
- Listing prices.
- Ownership shares.
- Commission lines.
- Workflow states nếu cần relational queries/invariants.

## 17.3. JSONB requirements

- Có schema/version.
- Có size limit.
- Có classification.
- Có canonical hash nếu audit/idempotency.
- Có indexes khi query thực tế cần.
- Không arbitrary unbounded.

---

# 18. Arrays

PostgreSQL array chỉ dùng khi:

- Danh sách nhỏ.
- Không cần entity attributes.
- Không cần FK.
- Không cần update từng item phức tạp.
- Không cần query relationship thường xuyên.

Ví dụ có thể dùng:

```text
changed_fields text[]
```

Không dùng array cho:

- Party IDs.
- Project IDs.
- Permission assignments.
- Allocations.
- Owners.

---

# 19. Foreign keys

## 19.1. Within Context

Foreign keys trong cùng Context phải được dùng khi phù hợp.

## 19.2. Cross-context FK

Mặc định không tạo cross-context FK.

Lý do:

- Coupling deployment.
- Ownership boundaries.
- Delete/update coupling.
- Khó tách Context.

Có thể lưu UUID reference và validate qua application/internal service.

Cross-context FK chỉ khi có ADR.

## 19.3. Delete behavior

Mặc định:

```text
RESTRICT / NO ACTION
```

Không cascade delete financial/audit/history.

Cascade chỉ cho pure child entities trong cùng Aggregate khi hard-delete aggregate draft là hợp lệ.

## 19.4. Deferrable

Chỉ dùng deferrable constraints khi có use case và test rõ.

---

# 20. Unique constraints

Mọi business uniqueness phải có database protection khi có thể.

Ví dụ:

```text
Enterprise code
Legal Entity code per Enterprise
Customer canonical phone identity
Active Commercial Lock
Receipt number
Issued business number
Idempotency key scope
Consumer inbox key
```

Application pre-check chỉ cải thiện UX, không thay unique constraint.

---

# 21. NULL semantics trong unique

PostgreSQL coi NULL khác nhau trong unique.

Nếu business cần NULL bằng nhau, dùng:

- `NULLS NOT DISTINCT`.
- Expression index với `COALESCE`.
- Partial indexes rõ.

Phải có integration test.

Ví dụ sequence per Enterprise khi `legal_entity_id IS NULL`.

---

# 22. Check constraints

Check constraint dùng cho:

- Allowed status.
- Non-negative amount.
- Date ranges.
- Percentage bounds.
- Required timestamp theo status.
- Mutually exclusive fields.
- Structural code format.

Không đưa business logic phức tạp phụ thuộc external tables vào CHECK.

---

# 23. Exclusion constraints

Dùng cho:

- Effective version overlap.
- Active lock overlap.
- Ownership period overlap nếu domain yêu cầu.
- Appointment/resource overlap khi database guard phù hợp.

Exclusion constraints phải có integration/concurrency tests.

---

# 24. Index principles

## 24.1. Mỗi index phải có mục đích

Mỗi index trong migration phải ghi lý do trong code comment/implementation notes nếu không hiển nhiên.

## 24.2. Index common patterns

- Foreign key columns.
- Scope columns.
- Status + time.
- Cursor sorting columns.
- Effective date queries.
- Idempotency key.
- Correlation ID.
- Backlog claim.
- Search normalized fields.

## 24.3. Partial indexes

Dùng cho hot subsets:

```sql
WHERE status IN ('PENDING', 'RETRY')
```

## 24.4. Composite order

Index column order theo query predicate/sort thực tế.

## 24.5. Không index mọi column

Index tăng:

- Write cost.
- Storage.
- Vacuum cost.
- Migration time.

## 24.6. Covering index

Dùng `INCLUDE` khi benchmark chứng minh lợi ích.

## 24.7. Expression index

Ví dụ:

```sql
CREATE INDEX ... ON party.customers (lower(display_name));
```

phải khớp query.

---

# 25. Cursor pagination

Query list phải có stable order.

Ví dụ:

```text
ORDER BY created_at DESC, id DESC
```

Index:

```text
(created_at DESC, id DESC)
```

Cursor phải chứa:

- Sort values.
- ID tie-breaker.
- Filter hash.
- Scope hash khi cần.

Không dùng OFFSET lớn cho operational tables.

---

# 26. Search

## 26.1. Baseline

PostgreSQL search được dùng trước.

## 26.2. Trigram/full-text

Chỉ thêm khi:

- Query requirement rõ.
- Index cost được đánh giá.
- Scope filtering vẫn enforce.
- Search không lộ PII.

## 26.3. External search

Chỉ sau ADR.

External index:

- Derived.
- Scope-aware.
- Rebuildable.
- Không source of truth.

---

# 27. Soft delete

Không có global soft-delete pattern.

Mỗi Aggregate chọn:

- Archive.
- Retire.
- Cancel.
- Revoke.
- Anonymize.
- Purge.
- Hard delete.

Không tự động thêm:

```text
deleted_at
is_deleted
```

vào mọi table.

---

# 28. Hard delete

Hard delete chỉ hợp lệ cho:

- Draft/test/temp data.
- Expired technical artifacts theo retention.
- Derived cache/projection.
- Uploaded temporary object chưa committed.

Không hard-delete:

- Receipt.
- Payment.
- Allocation history.
- Contract version approved.
- Revenue recognition.
- Commission payout.
- Audit event.
- Issued business number.
- Merge redirect.

---

# 29. Immutability

Immutable records:

- Published versions.
- Issued receipts.
- Issued business numbers.
- Recognition events.
- Payout payment confirmations.
- Audit events.
- Snapshots.
- Historical status entries.

Correction:

- New version.
- Reversal.
- Adjustment.
- Cancel-and-replace.
- Restatement.

Không update original evidence.

---

# 30. Audit columns vs Audit Context

`created_at`, `updated_at`, `created_by`, `updated_by` không thay Audit Event.

Audit Context lưu:

- Action.
- Outcome.
- Actor.
- Resource.
- Reason.
- Changed fields.
- Correlation.
- Classification.

Database standards yêu cầu cả metadata row-level và Audit khi use case cần.

---

# 31. Row version / optimistic concurrency

Mutable aggregates phải có:

```text
row_version bigint NOT NULL DEFAULT 1
```

Update pattern:

```sql
UPDATE ...
SET ..., row_version = row_version + 1
WHERE id = :id
  AND row_version = :expected_version
```

Nếu 0 rows:

```text
412 / version conflict
```

Không dùng updated_at làm concurrency token.

---

# 32. Pessimistic locking

Dùng:

```sql
SELECT ... FOR UPDATE
```

cho:

- Numbering sequence.
- Payment allocation.
- Commission payable/payout.
- Critical balance updates.
- Lock acquisition khi unique/exclusion chưa đủ.

Phải:

- Giữ transaction ngắn.
- Lock deterministic order.
- Có timeout.
- Có deadlock retry policy.
- Có concurrency tests.

---

# 33. Advisory locks

Chỉ dùng khi:

- Lock key logic không map tự nhiên vào row.
- Publish effective version.
- Singleton maintenance.
- Reconciliation batch.

Advisory lock không thay database constraint.

Lock key phải deterministic và documented.

---

# 34. Transaction isolation

Baseline:

```text
READ COMMITTED
```

Không tăng toàn hệ thống lên Serializable.

Use cases cần mạnh hơn phải:

- Có ADR/design.
- Có retry-safe semantics.
- Có performance test.

---

# 35. Transaction boundaries

Một command transaction nên bao gồm:

- Aggregate state.
- Child entities.
- Status history.
- Required Audit.
- Outbox.
- Idempotency completion.

Không bao gồm:

- External HTTP call.
- Email.
- Webhook.
- Signature provider.
- Long-running OCR.
- Bulk processing.

---

# 36. Long transactions

Bị cấm:

- User think time trong transaction.
- Network call trong transaction.
- Large file processing.
- Full-table scan.
- Sleep/retry loop.
- Batch hàng triệu rows trong một transaction.

Batch phải chia chunk và checkpoint.

---

# 37. Deadlock prevention

- Lock rows theo stable order.
- Không lock cross-context tables.
- Transaction ngắn.
- Index đúng.
- Tránh update rows không cần.
- Retry chỉ retry-safe.
- Log SQLSTATE sanitized.
- Metrics deadlock/retry.

---

# 38. Statement and lock timeout

Baseline request transaction:

```text
statement_timeout = 15s
lock_timeout = 3s
idle_in_transaction_session_timeout = 30s
```

Jobs/batch có config riêng.

Không disable timeout toàn session tùy tiện.

---

# 39. Outbox tables

Outbox phải:

- Durable.
- Unique event ID.
- Status.
- Available at.
- Attempt count.
- Claimed by/at.
- Published at.
- Payload hash.
- Correlation/causation.
- Partial index claim.
- Stale claim recovery.

Không tạo Outbox riêng mỗi Context.

---

# 40. Inbox tables

Inbox unique:

```text
consumer_name + event_id
```

Phải có:

- Payload hash.
- Status.
- Attempt.
- Retry time.
- Processed timestamp.
- Error.
- Handler version.

Không mark processed trước side effect commit.

---

# 41. Idempotency tables

Scope unique:

```text
enterprise_id
actor_key
operation_code
idempotency_key
```

Phải lưu:

- Request hash.
- Status.
- Owner token.
- Heartbeat.
- Expiry.
- Replay strategy.
- Resource reference.

Không lưu token/PII inline.

---

# 42. Audit schema

Audit tables:

- Append-only.
- Runtime không UPDATE/DELETE.
- Writer role riêng.
- Seal/integrity support.
- Retention class.
- Data classification.

Không tạo trigger tự động dump toàn row trước/sau vào audit.

Audit facts phải semantic.

---

# 43. Money and financial evidence

Financial tables phải có:

- Currency.
- Amount numeric.
- Source reference.
- Status.
- Effective/occurred time.
- Audit.
- Reversal/adjustment lineage.
- Unique provider/idempotency reference.

Không update amount đã posted/issued nếu domain yêu cầu immutable.

---

# 44. Allocation tables

Payment allocation cần:

```text
payment_id
receivable_id
allocated_amount
currency
status
allocated_at
reversed_at
```

Database phải chặn:

- Negative amount.
- Duplicate active allocation nếu không hợp lệ.
- Over-allocation qua transaction locks/application invariant.
- Currency mismatch.

Over-allocation khó enforce bằng CHECK cross-row; phải có row locking và integration/concurrency tests.

---

# 45. Receipt tables

Receipt:

- Unique number.
- Issuance timestamp.
- Immutable lines.
- Cancel/replacement lineage.
- No update after issue.
- Sensitive access.
- Long retention.

Không cascade delete Receipt.

---

# 46. Customer identity

Canonical phone identity cần:

- Normalized E.164 hoặc project-approved canonical format.
- Enterprise scope.
- Verification state.
- Unique constraint.
- Shared phone exception design.
- Merge redirect.

Không lưu phone normalized chỉ ở application memory.

---

# 47. Commercial Lock

Commercial Lock cần database final guard.

Có thể dùng:

- Unique partial index.
- Exclusion constraint theo listing/time/status.
- Row lock.

Active conflict semantics phải explicit.

Không dùng cache lock làm final guard.

---

# 48. Temporal assignments

Org/role/ownership/access assignments cần:

```text
effective_from
effective_to
status
```

As-of queries phải index.

Overlap policy phải explicit:

- Allowed.
- Not allowed.
- Allowed by role/type only.

Không lưu chỉ current assignment nếu history quan trọng.

---

# 49. Snapshot strategy

Snapshot dùng khi cần preserve meaning tại thời điểm giao dịch.

Ví dụ:

- Commercial terms.
- Customer contact display.
- Price version.
- Commission plan version.
- Attribution version.

Snapshot phải có:

- Source ID.
- Source version.
- Captured at.
- Schema version.
- Safe payload.

Snapshot không thay source record.

---

# 50. Denormalization

Denormalization chỉ khi:

- Query need rõ.
- Derived field có owner.
- Rebuild/reconcile được.
- Không tạo second truth không kiểm soát.

Mỗi denormalized field phải ghi:

- Source.
- Update mechanism.
- Staleness policy.
- Reconciliation.

---

# 51. Analytics schema

Analytics Context:

- Read-only đối với source.
- Projection tables.
- Dataset/metric versions.
- Freshness.
- Reconciliation.

Không direct-update operational tables.

Không dùng analytics projection cho operational decision critical nếu staleness không phù hợp.

---

# 52. Document metadata

Object binary ở object storage.

Database lưu:

- Object key.
- Bucket reference.
- Hash.
- MIME.
- Size.
- Scan status.
- Version.
- Classification.
- Retention.
- Context links.

Không lưu large binary trong PostgreSQL trừ ADR đặc biệt.

---

# 53. Secrets

Không lưu secret value trong business tables.

Chỉ lưu:

```text
secret_reference
provider_credential_reference
```

Secret manager chịu trách nhiệm value.

Không log DB URLs/passwords.

---

# 54. Encryption

TLS in transit.

Encryption at rest dựa infrastructure/platform.

Field-level encryption chỉ khi:

- Threat model yêu cầu.
- Key management rõ.
- Search/masking impact rõ.
- Rotation/restore rõ.

Không tự viết crypto.

---

# 55. Data classification metadata

Sensitive tables/columns phải được ghi trong Context docs và security matrix.

Có thể dùng metadata registry ngoài database.

Không dựa chỉ vào column name để phân loại.

---

# 56. Row-level security

PostgreSQL RLS không phải baseline mặc định nếu architecture dùng application authorization.

Chỉ dùng RLS khi ADR phê duyệt.

Nếu dùng:

- Policy rõ.
- Test rõ.
- Không giả định RLS thay application permission.
- Migration/operations support.
- Connection role semantics rõ.

---

# 57. Triggers

## 57.1. Triggers bị hạn chế

Không dùng trigger để:

- Thực thi business workflow.
- Publish event.
- Ghi cross-context table.
- Gửi network.
- Tính permission.
- Tạo hidden mutation.

## 57.2. Trigger có thể hợp lệ

- Update technical `updated_at` nếu standard phê duyệt.
- Enforce immutable rows.
- Maintain local technical invariant khó enforce khác.
- Audit seal technical support nếu documented.

Mọi trigger phải:

- Có migration.
- Có test.
- Có docs.
- Có performance review.

---

# 58. Stored procedures/functions

Không dùng stored procedure làm default application layer.

Có thể dùng cho:

- Controlled technical maintenance.
- Complex query hot path.
- Bulk migration.
- Integrity verification.
- Advisory lock helper.

Không dùng để che business logic khỏi Domain.

---

# 59. Views and materialized views

Views:

- Read-only.
- Query convenience.
- Security review.
- Stable owner.

Materialized views:

- Derived.
- Refresh strategy.
- Freshness metric.
- Rebuildable.
- Không source of truth.

Cross-context view cần ADR.

---

# 60. Partitioning

Partitioning không phải mặc định.

Candidate:

- Audit events.
- Timeline events.
- Large integration payload logs.
- Analytics facts.
- Notifications.
- Job attempts.

Partitioning chỉ khi:

- Volume estimate.
- Query pattern.
- Retention.
- Maintenance.
- Migration.
- Test.

Không partition sớm không có evidence.

---

# 61. Retention and purge

Mỗi data class cần retention policy.

Purge job phải:

- Chỉ terminal/eligible rows.
- Chunked.
- Audited khi required.
- Metrics.
- Dry run.
- No lock storm.
- Respect legal hold.

Không dùng `DELETE FROM table` không filter trong production.

---

# 62. Legal hold

Rows liên quan legal hold không được purge/anonymize.

Legal hold reference và release phải auditable.

---

# 63. Anonymization

Anonymization:

- Irreversible khi required.
- Preserve referential integrity.
- Preserve financial/legal history.
- Remove direct identifiers.
- Audit.
- Test.

Không replace tất cả bằng NULL nếu phá invariant.

---

# 64. Import staging

Import tables ở Integration Context:

- Raw row.
- Mapping result.
- Validation result.
- Error.
- Canonical resource reference.
- Status.

Import không insert trực tiếp business tables.

---

# 65. Database migration framework

Canonical:

```text
Alembic
```

Migrations nằm:

```text
backend/migrations/
```

Organize theo Context nếu project structure hỗ trợ, nhưng revision graph phải quản lý được.

---

# 66. Migration principles

## 66.1. Immutable migration history

Migration đã phát hành không được sửa.

## 66.2. Expand–migrate–contract

1. Expand schema.
2. Deploy compatible code.
3. Backfill.
4. Switch reads/writes.
5. Validate.
6. Contract old schema ở release sau.

## 66.3. No destructive same deploy

Không:

- Drop column used.
- Rename breaking trực tiếp.
- Change type destructive.
- Add NOT NULL không backfill.
- Rewrite huge table trong request release.

## 66.4. Idempotent seed

Stable seed phải upsert an toàn hoặc fail rõ.

---

# 67. Adding NOT NULL

Safe process:

1. Add nullable column.
2. Deploy dual-compatible code.
3. Backfill chunked.
4. Validate no null.
5. Add CHECK NOT VALID.
6. Validate constraint.
7. Set NOT NULL.
8. Remove temporary logic later.

---

# 68. Adding unique constraint

Safe process:

1. Detect duplicates.
2. Resolve.
3. Create unique index concurrently nếu production/size cần.
4. Attach constraint.
5. Add application handling.
6. Test concurrency.

---

# 69. Index creation

Large production table:

```text
CREATE INDEX CONCURRENTLY
```

nếu migration framework/deployment cho phép.

Alembic transaction handling phải explicit.

Không dùng concurrently trên test nếu khác semantics mà không test production path.

---

# 70. Type changes

Không change type trực tiếp nếu rewrite lớn.

Dùng:

- New column.
- Dual write.
- Backfill.
- Validate.
- Swap.
- Remove later.

---

# 71. Column rename

Treat as breaking.

Dùng:

- Add new column.
- Dual write/read fallback.
- Backfill.
- Switch.
- Remove old later.

---

# 72. Table rename

Phải đánh giá:

- ORM.
- Queries.
- Views.
- Jobs.
- BI.
- Permissions/grants.
- Backups.
- Runbooks.

Không rename chỉ vì style nếu production risk không đáng.

---

# 73. Backfill jobs

Backfill phải:

- Chunked.
- Checkpointed.
- Idempotent.
- Observable.
- Pause/resume.
- Rate limited.
- Reconciliation.
- Không giữ transaction lớn.
- Có dry run nếu critical.

---

# 74. Migration rollback

Downgrade test trên DB test.

Production rollback không mặc định chạy Alembic downgrade cho data-bearing destructive changes.

Có thể cần:

- Forward fix.
- Compensation migration.
- Feature rollback.
- Dual compatibility.

Runbook phải rõ.

---

# 75. Migration ownership

Mỗi migration phải ghi:

- Sprint.
- Context.
- Owner.
- Purpose.
- Safety notes.
- Data impact.
- Lock impact.
- Rollback strategy.

---

# 76. Migration CI

CI phải chạy:

```text
fresh upgrade
downgrade to previous sprint head
upgrade again
schema inspection
constraint/index checks
grants tests
```

Ngoài ra:

- No multiple unintended heads.
- Naming conventions.
- No public business tables.
- No direct cross-context FK nếu không approved.

---

# 77. Seed data standards

Seed categories:

- Stable permission codes.
- Stable error/reason codes.
- Reference data.
- Development fixtures.
- Test fixtures.

Không seed production business data trong migration chung.

Không hard-code tax/customer/project thật.

---

# 78. Reference data

Reference data phải có:

- Stable code.
- Display label.
- Status.
- Effective dates nếu cần.
- Versioning nếu business-controlled.
- Localization support khi cần.

Không dùng free-text thay stable code cho reason/status.

---

# 79. Query standards

## 79.1. Scope in SQL

Authorization scope phải nằm trong query predicate.

Không:

```python
rows = repository.list_all()
return [r for r in rows if allowed(r)]
```

## 79.2. Select only needed columns

List/projection không load full aggregate/document/blob.

## 79.3. Avoid N+1

Use joins/eager load/query projection.

## 79.4. Explain analyze

Hot query phải có `EXPLAIN (ANALYZE, BUFFERS)` trong performance evidence.

Không commit production PII trong query plan artifact.

---

# 80. Query repositories

Read-heavy query có thể dùng:

- SQLAlchemy Core.
- Typed projection.
- Database view.
- Raw SQL khi justified.

Không bắt buộc reconstruct Aggregate cho every list query.

Command side phải load Aggregate khi invariant cần.

---

# 81. Counting and pagination

Full `COUNT(*)` có thể đắt.

API phải xác định:

- Exact total required?
- Approximate?
- Has next page?

Không tính total mặc định cho mọi list nếu không cần.

---

# 82. Batch queries

Use:

- `IN` với bounded size.
- Temp/staging table cho large set.
- Chunking.
- Server-side iteration khi phù hợp.

Không xây SQL với hàng chục nghìn OR thủ công.

---

# 83. Connection pooling

- Pool size theo capacity.
- Timeout.
- Recycle/pre-ping khi cần.
- Separate worker/app pools nếu settings.
- Không giữ connection khi external call.
- Metrics pool.

Không set pool quá lớn làm PostgreSQL overload.

---

# 84. Read replicas

Không baseline cho operational correctness.

Nếu dùng:

- Staleness policy.
- Read-after-write routing.
- Critical queries primary.
- Analytics/reporting preference.
- Failover.
- Metrics.

---

# 85. High availability

Production design phải có:

- Backups.
- PITR.
- Replication/managed HA.
- Failover procedure.
- Restore drills.
- Monitoring.

Database standards không tự giả định provider.

---

# 86. Backup requirements

Backup phải bao gồm:

- PostgreSQL.
- Alembic version.
- Roles/grants definitions.
- Object storage references.
- Configuration metadata.

Backup success chỉ khi verify.

---

# 87. Restore requirements

Restore test phải verify:

- Schema.
- Data counts.
- Constraints.
- Critical journeys.
- Outbox/inbox states.
- Audit integrity.
- Application compatibility.
- Object references.

---

# 88. Data repair

Data repair không chạy ad-hoc SQL trực tiếp production nếu có thể tránh.

Phải có:

- Repair request.
- Dry run.
- Scope.
- Approval.
- Backup/checkpoint.
- Script version.
- Audit.
- Verification.
- Rollback/compensation.

---

# 89. Manual SQL access

Production manual write:

- Restricted.
- Break-glass.
- Approved.
- Logged.
- Time-bound.
- No shared credentials.
- Evidence.

Read queries cũng phải tuân PII policy.

---

# 90. Database observability

Metrics:

```text
connections
pool wait
query latency
slow queries
deadlocks
lock waits
transactions
rollbacks
replication lag
WAL
autovacuum
table/index bloat
cache hit
disk
backup status
```

Domain anomaly metrics riêng.

---

# 91. Slow query policy

Slow query threshold theo environment.

Slow query phải được:

- Correlated.
- Sanitized.
- Analyzed.
- Assigned owner.
- Fixed/tested.
- Không log full sensitive parameters.

---

# 92. Autovacuum and maintenance

Không disable autovacuum.

Large/high-churn tables có tuning riêng khi evidence.

Monitor:

- Dead tuples.
- Freeze age.
- Bloat.
- Vacuum duration.
- Analyze freshness.

---

# 93. Statistics

Hot skewed columns có thể cần extended statistics.

Chỉ thêm khi explain evidence.

Analyze sau major backfill/migration.

---

# 94. Database security

- TLS.
- Least privilege.
- Secret rotation.
- No public DDL.
- No shared superuser.
- Restricted extensions.
- Search path safe.
- Parameterized queries.
- No dynamic SQL from user.
- Audit access.

---

# 95. Search path

Set explicit safe search path.

Không dựa vào implicit `public`.

Migration và runtime phải qualify schema khi cần.

---

# 96. SQL injection prevention

- SQLAlchemy bound parameters.
- Filter/sort allowlist.
- No string concatenation.
- Raw SQL bind parameters.
- Identifier selection from allowlist only.

---

# 97. Sensitive data in indexes

Index có thể duplicate sensitive values.

Đánh giá:

- Need.
- Access.
- Encryption.
- Logging/explain.
- Backup.

Không index full PII nếu không cần.

---

# 98. Hashing identifiers

Hash chỉ dùng:

- Dedup helper.
- Audit/log privacy.
- Integrity.

Hash không thay encryption.

Use salt/HMAC khi threat model cần.

---

# 99. Testing standards — database

## Unit

- Mapping.
- Value object conversion.
- Query predicate builders.
- Migration helper logic.

## Integration

Phải dùng PostgreSQL thật/Testcontainers.

Test:

- DDL.
- Constraint.
- FK.
- Index existence.
- Query result.
- Transaction.
- Locks.
- Grants.

## Concurrency

- Multi-session.
- Real transactions.
- Barrier synchronization.
- Timeouts.
- Reproducible.

## Migration

- Upgrade/downgrade/upgrade.
- Existing data fixtures.
- Backfill.
- Lock behavior khi có thể.

## Security

- Role grants.
- Schema isolation.
- Audit append-only.
- Read-only denial.

---

# 100. Required database test cases

Mỗi table/aggregate critical phải có:

1. Insert valid.
2. Null violation.
3. Check violation.
4. Unique violation.
5. FK violation.
6. Optimistic conflict.
7. Transaction rollback.
8. Scope query.
9. Index/query plan nếu hot.
10. Retention/archive behavior.
11. Migration behavior.
12. Concurrency behavior khi relevant.

---

# 101. Test isolation

- Mỗi test transaction hoặc clean database.
- Không phụ thuộc order.
- Deterministic IDs/time.
- Không use production data.
- Không sleep tùy ý.
- Concurrency test cleanup.
- Separate schema/database per worker nếu parallel.

---

# 102. Factories

Factories phải tạo valid objects mặc định.

Invalid state chỉ khi test explicit.

Không hard-code fragile defaults.

Factories theo Context.

---

# 103. Performance tests

Critical database paths:

- Commercial Lock.
- Number issuance.
- Payment allocation.
- Receipt issuance.
- Customer duplicate detection.
- Lead list.
- Timeline list.
- Dashboard projection.
- Outbox claim.
- Inbox retry.
- Import batch.

Performance evidence phải lưu:

- Data scale.
- Query plan.
- p95/p99.
- Locks.
- Rows.
- Hardware/environment.

---

# 104. Database anti-patterns bị cấm

1. One giant schema.
2. Public business tables.
3. Cross-context repository writes.
4. Generic EAV settings cho mọi thứ.
5. JSONB cho toàn bộ domain.
6. No constraints because application validates.
7. Float money.
8. Naive timestamps.
9. Global soft delete.
10. Cascade delete financial data.
11. Offset pagination lớn.
12. Load all/filter Python.
13. N+1.
14. Redis counter as truth.
15. Modify migration history.
16. Destructive same-release migration.
17. Ad-hoc production SQL repair.
18. Trigger business workflow.
19. Stored procedure thay Domain.
20. No concurrency tests.
21. Index every column.
22. No index on FK/hot query.
23. Logging raw SQL params chứa PII.
24. Long transaction around network call.
25. Update immutable evidence.

---

# 105. Database design review checklist

## Ownership

- Table thuộc Context nào?
- Có second truth không?
- Có cross-context coupling không?

## Model

- Aggregate boundary?
- Entity/value meaning?
- Nullable rõ?
- Status rõ?
- Effective periods?

## Integrity

- PK?
- FK?
- Unique?
- Check?
- Exclusion?
- Immutability?

## Concurrency

- Optimistic?
- Row lock?
- Idempotency?
- Retry?
- Database final guard?

## Performance

- Query patterns?
- Indexes?
- Pagination?
- Volume?
- Partitioning need?

## Security

- Classification?
- Grants?
- PII?
- Retention?
- Audit?

## Migration

- Expand/contract?
- Backfill?
- Lock?
- Rollback?
- Tests?

---

# 106. AI Agent database protocol

Trước khi tạo/sửa database, AI Agent phải:

1. Đọc Source of Truth Matrix.
2. Xác định owning Context.
3. Đọc Context database specification.
4. Inspect existing migrations/models/tests.
5. Xác định invariant.
6. Xác định transaction/concurrency.
7. Xác định retention/classification.
8. Thiết kế DDL.
9. Thiết kế migration safety.
10. Thiết kế tests.
11. Review query/index.
12. Update docs.
13. Run migration checks.
14. Báo evidence.

---

# 107. AI Agent prohibited database behaviors

AI Agent không được:

1. Tạo table ngoài owning schema.
2. Thêm cross-context FK không ADR.
3. Tạo nullable field tùy tiện.
4. Dùng text cho mọi thứ.
5. Dùng float money.
6. Bỏ constraint để dễ seed.
7. Sửa migration cũ.
8. Drop column ngay.
9. Tạo index không purpose.
10. Tạo trigger hidden business logic.
11. Direct-write audit.
12. Dùng ORM model làm Domain.
13. Dùng SQLite test.
14. Báo migration pass khi chưa chạy.
15. Dùng raw SQL không bind.
16. Tạo soft-delete global.
17. Reuse issued number.
18. Xóa financial history.
19. Bỏ concurrency test.
20. Tạo public table.

---

# 108. Definition of Ready cho database change

Database change chỉ Ready khi:

1. Ownership rõ.
2. Domain meaning rõ.
3. DDL draft rõ.
4. Constraints rõ.
5. Index/query rõ.
6. Migration path rõ.
7. Backfill rõ.
8. Concurrency rõ.
9. Security/retention rõ.
10. Tests rõ.
11. No blocking architecture conflict.

---

# 109. Definition of Done cho database change

Database change chỉ Done khi:

1. Migration created.
2. Upgrade pass.
3. Downgrade test pass khi applicable.
4. Upgrade again pass.
5. Constraints verified.
6. Indexes verified.
7. Grants verified.
8. ORM mapping pass.
9. Integration tests pass.
10. Concurrency tests pass khi relevant.
11. Query scope pass.
12. Performance evidence khi hot path.
13. Documentation updated.
14. No migration drift.
15. No unintended Alembic heads.
16. No public schema objects.
17. No secret/PII leakage.
18. Acceptance Report updated.

---

# 110. Exception process

Ngoại lệ cần file:

```text
docs/engineering/database-exceptions/EXC-DB-XXX.md
```

Nội dung:

- Rule.
- Reason.
- Scope.
- Data impact.
- Security impact.
- Performance impact.
- Migration plan.
- Risk.
- Mitigation.
- Owner.
- Expiry.
- Approval.

Không có ngoại lệ vô thời hạn không owner.

---

# 111. Change Log

## Version 1.0.0 — 2026-07-24

- Thiết lập PostgreSQL standards.
- Khóa schema-per-context.
- Khóa role/grant strategy.
- Khóa naming, keys, timestamps, money và JSONB.
- Khóa FK, constraints, indexes và pagination.
- Khóa transactions, concurrency, locks và isolation.
- Khóa Outbox/Inbox/Idempotency/Audit.
- Khóa immutability, retention và data repair.
- Khóa Alembic migration strategy.
- Khóa database testing và performance.
- Khóa AI Agent database protocol.

---

# 112. Kết luận

Database của `crm_bds_ai` không chỉ là nơi lưu dữ liệu.

Nó là lớp bảo vệ cuối cùng cho:

```text
Domain Ownership
+ Business Invariants
+ Financial Integrity
+ Concurrency Safety
+ Historical Evidence
+ Security Boundaries
+ Reliable Recovery
```

Nguyên tắc tối cao:

> Nếu một invariant quan trọng có thể được bảo vệ bằng database constraint hoặc transaction đúng, không được chỉ tin vào code phía trên.
