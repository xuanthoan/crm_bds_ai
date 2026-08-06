# CRM_BDS_AI — TESTING STANDARDS

## Quy chuẩn kiểm thử bắt buộc cho toàn bộ hệ thống `crm_bds_ai`

**Document ID:** `ENG-TEST-001`  
**Canonical path:** `docs/engineering/testing-standards.md`  
**Product:** `crm_bds_ai`  
**Version:** `1.0.0`  
**Status:** `Accepted / Mandatory`  
**Canonical:** `Yes` đối với chiến lược, thiết kế, triển khai, vận hành và bằng chứng kiểm thử  
**Owner:** `QA Architecture Owner`  
**Reviewers:** `Architecture Owner`, `Technical Owner`, `Security Owner`, `Backend Owner`, `Frontend Owner`, `Database Owner`, `Operations Owner`, `Context Owners`  
**Effective date:** `2026-08-05`  
**Last reviewed:** `2026-08-05`  
**Next review:** Khi toolchain, CI, architecture, production topology, test strategy hoặc quality gates thay đổi  
**Supersedes:** `None — Greenfield baseline`  
**Superseded by:** Không

---

# 1. Mục đích

Tài liệu này quy định cách thiết kế, tổ chức, viết, chạy, đánh giá và duy trì mọi loại kiểm thử trong `crm_bds_ai`.

Mục tiêu:

1. Bảo đảm mọi business invariant đều có test.
2. Bảo đảm database constraints được kiểm thử bằng PostgreSQL thật.
3. Bảo đảm API, Event và Permission contracts không drift.
4. Bảo đảm concurrency-critical flows không tạo duplicate hoặc over-allocation.
5. Bảo đảm authorization, scope và masking không bị bypass.
6. Bảo đảm frontend phản ánh đúng loading, error, conflict và permission states.
7. Bảo đảm release không dựa trên cảm tính.
8. Bảo đảm bug có regression test.
9. Bảo đảm test suite ổn định, deterministic và có thể chạy trong CI.
10. Bảo đảm AI Agent không tự bỏ qua test hoặc sửa test chỉ để code pass.

Tài liệu này phải được đọc cùng:

```text
docs/engineering/coding-standards.md
docs/engineering/database-standards.md
docs/engineering/api-standards.md
docs/engineering/event-standards.md
docs/engineering/security-standards.md
docs/architecture/non-functional-requirements.md
docs/operations/service-level-objectives.md
Relevant Context Implementation Pack
Current Sprint Execution Pack
```

---

# 2. Nguyên tắc tối cao

```text
Correct Behavior
> Business Invariants
> Security
> Data Integrity
> Reliability
> Determinism
> Maintainability
> Coverage Percentage
```

Coverage cao không có giá trị nếu test không chứng minh behavior quan trọng.

---

# 3. Testing philosophy

## 3.1. Test behavior, không test implementation detail

Test phải tập trung vào:

- Input.
- State.
- Command.
- Output.
- Side effect.
- Invariant.
- Error.
- Event.
- Persistence.
- Authorization.

Không phụ thuộc quá sâu vào private method hoặc internal call order nếu không phải contract.

## 3.2. Test nhỏ nhất có thể nhưng đủ mạnh

- Domain invariant → Unit test.
- Database constraint → PostgreSQL integration test.
- API contract → API/contract test.
- Event delivery → Outbox/Inbox integration test.
- User journey → E2E.
- Concurrency → Multi-session concurrency test.
- Production failure → Failure-injection test.

## 3.3. Không mock thứ cần chứng minh

Không mock:

- PostgreSQL khi test repository/migration/constraint.
- RabbitMQ khi test broker delivery.
- Authorization policy khi test security.
- Business Calendar khi test SLA calculation nếu Calendar là subject.
- Domain Aggregate khi test application handler behavior.
- External provider contract test nếu cần chứng minh mapping thật.

## 3.4. Deterministic by default

Test phải kiểm soát:

- Clock.
- UUID.
- Random.
- Locale.
- Timezone.
- Environment variables.
- Database state.
- Queue state.
- External responses.

---

# 4. Test taxonomy

Các loại test bắt buộc:

```text
Unit
Application
Repository Integration
Database Constraint
Migration
API Integration
Contract
Architecture
Security
Concurrency
Event
Background Job
Frontend Unit
Frontend Component
Frontend Integration
E2E
Performance
Load
Failure Injection
Reconciliation
Backup/Restore
UAT
Regression
Smoke
Release Verification
```

---

# 5. Test pyramid

Baseline tỷ lệ định hướng:

```text
Unit / Domain Tests: nhiều nhất
Application / Component Tests: nhiều
Integration / Contract Tests: vừa phải
E2E / Performance / Failure Injection: ít hơn nhưng bắt buộc cho critical journeys
```

Không biến E2E thành nơi duy nhất kiểm tra business logic.

Không dùng unit tests để giả lập toàn bộ hệ thống rồi gọi đó là integration.

---

# 6. Test ownership

Mỗi test phải có owner theo Context hoặc platform capability.

Ví dụ:

```text
backend/contexts/product/tests/...
tests/integration/product/...
tests/security/product/...
```

Không đặt mọi test vào một thư mục `tests/common`.

Shared testing utilities chỉ chứa:

- Factories.
- Fixtures.
- Fakes.
- Assertion helpers.
- Environment helpers.

Không chứa business test cases của Context.

---

# 7. Test directory structure

Backend đề xuất:

```text
backend/contexts/<context>/tests/
├── unit/
├── application/
├── contract/
├── security/
└── concurrency/

tests/
├── integration/
│   ├── platform/
│   ├── iam/
│   ├── party/
│   └── ...
├── architecture/
├── migrations/
├── events/
├── performance/
├── failure_injection/
├── reconciliation/
├── smoke/
└── support/
```

Frontend:

```text
apps/web/
├── features/<feature>/__tests__/
├── components/__tests__/
├── tests/
│   ├── unit/
│   ├── component/
│   ├── integration/
│   └── e2e/
```

---

# 8. Test naming

## 8.1. Python

Format:

```text
test_<behavior>_when_<condition>_<expected_result>
```

Ví dụ:

```python
def test_confirm_booking_when_lock_expired_raises_conflict(): ...
def test_allocate_payment_when_amount_exceeds_receivable_is_rejected(): ...
```

## 8.2. TypeScript

Ví dụ:

```typescript
it("shows a conflict dialog when saving a stale legal entity", async () => {})
```

## 8.3. Không dùng tên mơ hồ

Sai:

```text
test_create
test_update
test_case_1
test_happy_path
test_error
```

Đúng:

```text
test_issue_receipt_when_allocation_is_complete_returns_issued_receipt
```

---

# 9. Arrange–Act–Assert

Mỗi test nên có cấu trúc rõ:

```text
Arrange
Act
Assert
```

Hoặc:

```text
Given
When
Then
```

Không lồng nhiều use cases trong một test.

Một test phải có một failure reason chính.

---

# 10. Unit tests — Domain

Unit tests phải chứng minh:

- Aggregate creation.
- State transitions.
- Guards.
- Value Object validation.
- Domain policies.
- Domain calculations.
- Domain Events.
- Immutability.
- Error conditions.

Unit test không:

- Kết nối database.
- Gọi HTTP.
- Gọi broker.
- Dùng sleep.
- Phụ thuộc current time.
- Dùng production config.

---

# 11. Domain Aggregate test matrix

Mỗi Aggregate stateful phải test:

1. Valid creation.
2. Invalid creation.
3. Every valid transition.
4. Every invalid transition.
5. Guard failure.
6. Timestamp changes.
7. Version/event changes.
8. Terminal state.
9. Immutable published/issued state.
10. No event when command fails.
11. Correct event payload.
12. Collection invariants.
13. Boundary values.

---

# 12. Value Object tests

Mỗi Value Object phải test:

- Valid input.
- Normalization.
- Invalid format.
- Boundary length.
- Equality.
- Hashability nếu dùng.
- Serialization.
- Immutability.

Ví dụ:

```text
CurrencyCode
PhoneIdentity
Money
EffectivePeriod
TimezoneId
EnterpriseCode
NumberingPattern
```

---

# 13. Property-based testing

Property-based tests nên dùng cho:

- Money arithmetic.
- Date/time ranges.
- Calendar windows.
- Numbering pattern parser.
- Pagination cursors.
- Matching scores.
- Allocation boundaries.
- Split percentages.
- Serialization roundtrip.

Properties phải có business meaning.

Ví dụ:

```text
Allocated total never exceeds payment total.
Business duration never becomes negative.
Rendered business number always contains exactly one sequence component.
```

---

# 14. Application handler tests

Application tests phải chứng minh:

- Authorization được gọi đúng.
- Aggregate load đúng.
- Command mapping đúng.
- Domain behavior được gọi.
- Unit of Work commit/rollback.
- Audit fact.
- Outbox event.
- Idempotency.
- Correct DTO.
- Infrastructure error mapping.

Có thể dùng fakes cho repositories/ports.

Không mock Aggregate behavior.

---

# 15. Fake vs Mock vs Stub

## Fake

In-memory implementation có behavior hữu ích.

Ví dụ:

```text
FakeClock
FakeUUIDProvider
FakeObjectStorage
FakeRepository
```

## Stub

Trả response cố định.

## Mock

Xác minh interaction.

Ưu tiên Fake/Stub hơn deep mocks.

Không mock chain phức tạp của SQLAlchemy Session.

---

# 16. Mocking policy

Bị cấm:

- Mock private methods để test public behavior.
- Mock ORM model internals.
- Mock every dependency khiến test chỉ verify call order.
- Mock database trong repository tests.
- Mock broker trong event integration tests.
- Mock authorization trong security tests.
- Mock entire frontend API client in E2E.

Mock hợp lệ cho:

- External provider in unit/application tests.
- Clock.
- UUID.
- Slow technical dependency.
- Error injection.

---

# 17. Test doubles naming

Tên rõ:

```text
FakeClock
StubSignatureProvider
FailingAuditWriter
RecordingEventPublisher
```

Không dùng:

```text
MockService
Dummy
FakeThing
```

---

# 18. Integration test definition

Integration test phải dùng ít nhất hai real components.

Ví dụ:

- SQLAlchemy + PostgreSQL.
- FastAPI + Application + PostgreSQL.
- Outbox Publisher + RabbitMQ.
- Consumer + Inbox + PostgreSQL.
- Object Storage Adapter + MinIO/S3-compatible test service.

Không gọi test là integration nếu chỉ dùng mocks.

---

# 19. PostgreSQL integration tests

Bắt buộc dùng:

```text
PostgreSQL thật
```

Khuyến nghị:

```text
Testcontainers
```

Không dùng SQLite.

Phải kiểm thử:

- Migrations.
- Constraints.
- Indexes.
- Locks.
- Isolation.
- SQLAlchemy mappings.
- Query plans cho hot paths.
- Grants.
- Schema boundaries.

---

# 20. Database constraint tests

Mỗi constraint critical phải có test trực tiếp:

- NOT NULL.
- UNIQUE.
- CHECK.
- FK.
- EXCLUSION.
- Immutable policy.
- Partial unique.
- NULLS NOT DISTINCT semantics.

Test phải chứng minh database reject invalid state ngay cả khi bypass application layer.

---

# 21. Migration tests

Mỗi Sprint database change phải test:

```text
fresh upgrade
previous head → new head
new head → previous head khi applicable
upgrade again
existing data backfill
constraint/index existence
grants
schema ownership
```

Không sửa migration đã phát hành để test pass.

---

# 22. Migration fixture strategy

Migrations có data change phải có fixture:

- Old schema.
- Representative legacy rows.
- Nulls.
- Duplicate candidates.
- Boundary dates.
- Financial rows.
- Large enough sample.

Không chỉ test empty database.

---

# 23. API integration tests

API tests phải chạy qua FastAPI routing layer với real application wiring và PostgreSQL test database.

Mỗi command endpoint test:

1. Success.
2. 401.
3. 403.
4. Out-of-scope.
5. Validation failure.
6. Business conflict.
7. Idempotency replay.
8. Idempotency conflict.
9. If-Match conflict.
10. Audit.
11. Outbox.
12. Rollback.
13. Response schema.
14. ETag/headers.

Mỗi query endpoint test:

1. Scope.
2. Masking.
3. Pagination.
4. Filters.
5. Sorting.
6. Empty state.
7. Invalid cursor.
8. Max page size.
9. Stable ordering.
10. No N+1 where relevant.

---

# 24. Contract tests

Contract tests bao gồm:

- OpenAPI validation.
- Operation ID uniqueness.
- Request schema.
- Response schema.
- Problem Details.
- JSON Schema.
- AsyncAPI.
- Generated client.
- Provider contracts.
- Backward compatibility.

Không merge API/Event change nếu contract diff chưa được đánh giá.

---

# 25. OpenAPI tests

Phải test:

- OpenAPI 3.1 valid.
- Every route documented.
- No orphan operation.
- Security metadata.
- Error responses.
- Idempotency/If-Match headers.
- Examples validate.
- Stable operation IDs.
- No duplicate schema names.
- Generated TypeScript client clean.

---

# 26. Event contract tests

Phải test:

- JSON Schema 2020-12 valid.
- Event examples validate.
- AsyncAPI references valid.
- Event Registry consistent.
- Schema URI/version match.
- No forbidden fields.
- Compatibility diff.
- Consumer supported versions.

---

# 27. Architecture tests

Architecture tests phải enforce:

- Domain không import framework.
- Application không import Presentation.
- Context A không import Context B persistence.
- Router không import SQLAlchemy Session trực tiếp.
- No direct broker publish.
- No direct Audit ORM import.
- No frontend imports backend internal code.
- No feature imports Design System internals.
- No Recharts outside approved Dashboard layer.
- No business table in `public`.
- No cross-context business write.

Architecture tests phải fail CI.

---

# 28. Security tests

Security tests không chỉ test login.

Phải test:

- Authentication.
- Permission.
- Scope.
- Resource relationship.
- Field masking.
- SoD.
- Approval limit.
- IDOR/BOLA.
- Over-posting.
- Mass assignment.
- Enumeration.
- Export/download reauthorization.
- Webhook signature/replay.
- Rate limiting.
- Break-glass.
- Sensitive audit.
- Internal API exposure.
- Log/response PII leakage.

---

# 29. Authorization matrix tests

Mỗi permission/resource cần test matrix:

```text
Role/Capability
× Scope
× Resource ownership/assignment
× Resource state
× Field classification
× Action
```

Không chỉ test “admin allowed / user denied”.

---

# 30. Field masking tests

Test phải chứng minh:

- Full field khi permitted.
- Masked field khi limited.
- Omitted field khi prohibited.
- Export follows same policy.
- Cache does not leak full version.
- Search does not leak.
- Error does not leak.
- Audit access follows policy.

---

# 31. Concurrency tests

Critical concurrency flows:

- Customer identity creation.
- Commercial Lock.
- Number issuance.
- Booking confirmation.
- Payment Allocation.
- Receipt issuance.
- Refund execution.
- Commission payout.
- Approval decision.
- Event Inbox duplicate handling.

Phải dùng:

- Real PostgreSQL sessions.
- Synchronization barrier.
- Real transaction overlap.
- Deterministic assertions.

Không dùng thread test chỉ chạy tuần tự do setup sai.

---

# 32. Concurrency test patterns

## Same resource, different commands

Ví dụ:

```text
Confirm Booking vs Cancel Booking
```

## Same resource, same command

Ví dụ:

```text
Two Receipt issue requests
```

## Unique creation race

Ví dụ:

```text
Two Customer identities same normalized phone
```

## Balance race

Ví dụ:

```text
Two allocations against same receivable
```

## First-row insert race

Ví dụ:

```text
Numbering sequence first bucket creation
```

---

# 33. Concurrency assertions

Test phải kiểm tra:

- Winner count.
- Loser error code.
- Final state.
- No duplicate rows.
- No lost update.
- No over-allocation.
- No duplicate event.
- No duplicate audit.
- No deadlock vượt policy.
- Correct retry count.

---

# 34. Event tests

Event test layers:

- Domain Event unit.
- Integration Event mapper.
- Outbox atomicity.
- Publisher confirm.
- Inbox deduplication.
- Retry.
- Ordering.
- DLQ.
- Replay.
- Reconciliation.

Mọi critical consumer phải có duplicate delivery test.

---

# 35. Background job tests

Mỗi job phải test:

- Happy path.
- Retryable failure.
- Permanent failure.
- Max attempts.
- Timeout.
- Idempotency.
- Duplicate scheduling.
- Cancellation.
- Progress.
- Metrics.
- Cleanup.
- Recovery after crash.

Không sleep thật.

---

# 36. Scheduler tests

Scheduled jobs phải test:

- Correct schedule registration.
- Missed schedule recovery.
- Timezone.
- DST.
- Duplicate scheduler instances.
- Singleton/advisory lock.
- Disabled state.
- Manual trigger.

---

# 37. Frontend unit tests

Frontend unit tests cho:

- Pure utilities.
- Formatters.
- Permission presentation helpers.
- State reducers.
- Zod schemas.
- Query key factories.
- Data transformation không phải official KPI.

Không test implementation detail của React.

---

# 38. Frontend component tests

Dùng DOM-oriented testing.

Test:

- Visible behavior.
- User interaction.
- Accessibility roles.
- Form validation.
- Loading.
- Empty.
- Error.
- Permission denied.
- Conflict.
- Read-only published state.
- Masked field rendering.

Không query bằng CSS class nếu semantic role có thể dùng.

---

# 39. Frontend integration tests

Phải kiểm tra:

- Component + API client mock server.
- Mutation.
- Cache invalidation.
- Problem Details mapping.
- ETag/If-Match.
- Idempotency key generation.
- Pagination.
- Filters.
- Permission UI.
- Error recovery.

Nên dùng network-level mock như MSW thay mock hook internals.

---

# 40. E2E testing

E2E phải chạy qua:

- Browser thật.
- Frontend build.
- API.
- PostgreSQL.
- Required services.
- Auth test configuration.
- Real routes.

Không mock toàn backend trong E2E chính.

---

# 41. E2E scope

E2E dành cho critical journeys:

1. Enterprise → Legal Entity activation.
2. Lead → Customer → Requirement.
3. Requirement → Matching → Shortlist.
4. Deal → Hold → Booking.
5. Booking → Contract → Signature → Effective.
6. Contract → Receivable → Payment → Allocation → Receipt.
7. Contract cancellation → Refund.
8. Revenue → Recognition → Collection.
9. Commission → Vesting → Payout.
10. Customer merge.
11. Document upload → Dossier → Verification.
12. Integration failure → DLQ → retry.
13. Backup → Restore verification.
14. Dashboard → Drill-down.

---

# 42. E2E design rules

- One journey per spec.
- Stable test data.
- Avoid brittle selectors.
- Use `data-testid` only khi semantic selector không đủ.
- No arbitrary sleeps.
- Wait on observable state.
- Capture screenshot/video/trace on failure.
- Clean test data.
- No production dependency.
- Parallel-safe where possible.

---

# 43. Smoke tests

Smoke tests phải nhanh và chạy sau deploy.

Minimum:

- Liveness.
- Readiness.
- Authentication.
- One read endpoint.
- One safe write.
- Database migration version.
- Outbox publisher.
- Critical worker.
- Object storage.
- Frontend shell.
- Dashboard minimal query.

Smoke test không thay full regression.

---

# 44. Regression tests

Mỗi bug fix phải có regression test:

- Fail trước fix.
- Pass sau fix.
- Nằm đúng layer.
- Có issue reference.
- Không chỉ snapshot UI nếu bug ở Domain/DB.

Không đóng bug nếu regression test chưa có, trừ incident emergency có follow-up bắt buộc.

---

# 45. Performance testing

Performance tests phải xác định:

- Scenario.
- Data volume.
- Concurrency.
- Warm/cold cache.
- Environment.
- p50/p95/p99.
- Throughput.
- Error rate.
- DB load.
- Queue lag.
- Lock waits.

Không chỉ đo average.

---

# 46. Performance targets

Targets lấy từ NFR/SLO.

Nếu chưa có final SLO, Sprint Pack phải có engineering baseline.

Critical examples:

- Commercial Lock.
- Numbering.
- Payment Allocation.
- Dashboard.
- Search.
- Lead intake.
- Event processing.
- Export.

---

# 47. Load testing

Load test phải có:

- Ramp-up.
- Steady state.
- Spike.
- Soak.
- Recovery.
- Backpressure.
- Error budget.

Không load test production không approval.

---

# 48. Soak testing

Soak test kiểm tra:

- Memory leak.
- Connection leak.
- Queue growth.
- File descriptor leak.
- Deadlock accumulation.
- Cache growth.
- Worker stability.
- Autovacuum pressure.

Duration theo release criticality.

---

# 49. Stress testing

Stress test tìm breaking point.

Phải ghi:

- Threshold.
- Failure mode.
- Recovery.
- Data integrity.
- Alert behavior.
- No silent corruption.

---

# 50. Failure-injection testing

Inject failures:

- PostgreSQL unavailable.
- PostgreSQL deadlock.
- Lock timeout.
- RabbitMQ unavailable.
- Publisher confirm lost.
- Consumer crash.
- Valkey unavailable.
- Object storage unavailable.
- Provider timeout.
- Provider duplicate callback.
- Network partition simulation.
- Disk/storage failure where possible.
- Audit writer failure.
- Outbox insert failure.

Expected behavior phải được xác định trước test.

---

# 51. Crash-window testing

Critical crash windows:

- After DB commit before HTTP response.
- After provider request before response.
- After consumer commit before ack.
- After Inbox insert before handler.
- After Outbox claim before publish.
- After file upload before complete.
- During migration/backfill.

Test phải chứng minh idempotent recovery.

---

# 52. Reconciliation tests

Mỗi critical process phải test discrepancy detection.

Ví dụ:

- Booking confirmed nhưng Contract chưa tạo.
- Payment allocated nhưng Receipt projection thiếu.
- Customer merged nhưng Lead chưa rebind.
- Revenue expected nhưng chưa có entitlement.
- Number issuance sequence mismatch.
- Outbox event missing.
- Document metadata không có object.

Test:

- Detect.
- Record finding.
- Retry/repair.
- Audit.
- No duplicate.

---

# 53. Backup tests

Backup test phải xác minh:

- Backup job runs.
- Artifact exists.
- Encryption/access.
- Metadata.
- Retention.
- Verification.
- Alert on failure.

Không coi exit code 0 là đủ.

---

# 54. Restore tests

Restore test phải xác minh:

- Fresh environment.
- Database restore.
- Object references.
- Migrations.
- Critical data counts.
- Constraints.
- Audit integrity.
- Critical journeys.
- RPO/RTO measurement.

Restore drill phải có report.

---

# 55. UAT

UAT không thay automated tests.

UAT tập trung:

- Business acceptance.
- Role workflow.
- Data meaning.
- Operational readiness.
- Reporting meaning.
- Usability.
- Compliance.

UAT scenarios phải versioned và repeatable.

---

# 56. Test data strategy

Test data phải:

- Fake.
- Deterministic.
- Non-production.
- Realistic enough.
- Classified.
- Minimal.
- Reusable qua factories.

Không dùng real customer data.

Không copy production dump vào developer environment nếu chưa anonymize và approve.

---

# 57. Factories

Factories phải:

- Tạo valid object mặc định.
- Cho override explicit.
- Không tạo hidden unrelated records.
- Có stable defaults.
- Theo Context.
- Support timestamps/versions.

Ví dụ:

```python
enterprise = EnterpriseFactory(active=True)
legal_entity = LegalEntityFactory(enterprise_id=enterprise.id)
```

---

# 58. Fixtures

Fixture scope phải nhỏ nhất hợp lý:

- function.
- class.
- module.
- session.

Không dùng session-scoped mutable business data gây coupling.

Fixtures không nên có nhiều side effects ẩn.

---

# 59. Golden data / snapshots

Snapshot testing chỉ dùng khi:

- Contract/serialization lớn.
- Generated OpenAPI.
- Event examples.
- UI stable output.

Không update snapshot mù.

Review snapshot diff như code.

Không dùng snapshot để thay semantic assertions.

---

# 60. Time control

Mọi test thời gian phải dùng:

- FixedClock.
- Frozen time utility được khóa.
- Explicit timezone.

Không phụ thuộc ngày hiện tại.

Phải test:

- End-of-day.
- Month/year boundary.
- Leap day.
- DST.
- Expiry exact boundary.
- Effective dates.

---

# 61. UUID/random control

- Deterministic UUID provider.
- Seeded random.
- No global random state.
- Tests không phụ thuộc UUID ordering trừ UUIDv7 behavior test.

---

# 62. Environment control

Test phải set explicit:

- Locale.
- Timezone.
- Feature flags.
- Settings.
- Service endpoints.
- Secrets dummy.
- Database isolation.

Không phụ thuộc developer machine.

---

# 63. Parallel testing

Parallel tests chỉ khi:

- Database isolation.
- Unique resource names.
- Queue isolation.
- Port isolation.
- File storage prefix.
- No global state.

Test không parallel-safe phải có marker và lý do.

Không disable parallel toàn suite vì một test yếu.

---

# 64. Flaky test policy

Flaky test là defect.

Không chấp nhận:

- Retry test vô hạn.
- Rerun để “green”.
- Quarantine không owner.
- Sleep tăng dần.

Flaky test phải:

1. Có issue.
2. Có owner.
3. Có reproduction.
4. Có expiry.
5. Được fix hoặc remove đúng lý do.
6. Không block critical coverage lâu dài.

---

# 65. Quarantine policy

Chỉ quarantine khi:

- Test flaky đã xác nhận.
- Không phải critical security/financial/concurrency test.
- Có issue/owner/deadline.
- CI vẫn báo quarantine status.

Không quarantine test chỉ vì code fail.

---

# 66. Coverage policy

Coverage dùng để phát hiện vùng chưa test, không phải mục tiêu duy nhất.

Baseline:

- Domain critical code: rất cao.
- Application handlers: cao.
- Shared reliability/security: rất cao.
- Presentation mapping: hợp lý.
- Generated code: exclude.
- Migrations: behavior tested, không cần line coverage.

Coverage threshold cụ thể trong CI config.

Không viết test vô nghĩa chỉ để tăng coverage.

---

# 67. Mutation testing

Nên áp dụng cho:

- Financial calculations.
- Authorization.
- State machines.
- Matching scoring.
- Numbering.
- Calendar.
- Allocation.

Mutation survivors trong critical code phải được review.

---

# 68. Test quality review

Test tốt phải:

- Fail đúng lý do.
- Có assertion mạnh.
- Không quá nhiều setup không liên quan.
- Không quá phụ thuộc implementation.
- Deterministic.
- Dễ đọc.
- Dễ chẩn đoán khi fail.
- Có business meaning.

---

# 69. Assertions

Ưu tiên assertions cụ thể:

```python
assert allocation.status is AllocationStatus.ACTIVE
assert allocation.amount == Decimal("100.00")
```

Không:

```python
assert result
assert response.status_code != 500
```

Error tests phải assert stable error code.

---

# 70. Exception tests

Test exception phải kiểm tra:

- Exception type.
- Error code.
- Safe context.
- No state mutation.
- No event.
- No commit.
- No PII leakage.

---

# 71. Database assertions

Sau command phải assert:

- Aggregate row.
- Child rows.
- History rows.
- Audit.
- Outbox.
- Idempotency.
- No unexpected rows.
- Transaction atomicity.

Không chỉ assert API response.

---

# 72. Event assertions

Phải assert:

- Event type.
- Version.
- Aggregate ID/version.
- Correlation/causation.
- Scope.
- Payload.
- Schema validity.
- PII absence.
- Outbox status.

---

# 73. Security assertions

Phải assert:

- Exact HTTP status.
- Stable error code.
- No resource existence leak.
- Masked/omitted fields.
- No side effect.
- Audit denial/sensitive access nếu policy.
- Same behavior across list/detail/export/search.

---

# 74. Frontend assertions

Ưu tiên:

- User-visible text.
- Role.
- Accessible name.
- State.
- Network call.
- Form error.
- Navigation.

Không assert internal component state.

---

# 75. CI test stages

Recommended pipeline:

```text
1. Static checks
2. Unit tests
3. Architecture tests
4. Database migration tests
5. Integration tests
6. Contract tests
7. Security tests
8. Concurrency tests
9. Frontend unit/component
10. Build
11. E2E
12. Performance smoke
13. Artifact/report generation
```

Critical tests phải block merge.

---

# 76. CI matrix

Matrix có thể gồm:

- Python version locked.
- Node version locked.
- PostgreSQL locked.
- RabbitMQ locked.
- Valkey locked.
- Browser set.
- OS baseline.

Không test trên versions ngoài Toolchain Lock trừ compatibility job explicit.

---

# 77. Test markers

Python markers đề xuất:

```text
unit
application
integration
contract
architecture
security
concurrency
performance
failure_injection
slow
smoke
```

Markers phải đăng ký trong config.

Không dùng marker để bỏ qua test mặc định mà không docs.

---

# 78. Test commands

Canonical commands qua:

```bash
uv run python scripts/dev.py test
uv run python scripts/dev.py test-unit
uv run python scripts/dev.py test-integration
uv run python scripts/dev.py test-contract
uv run python scripts/dev.py test-security
uv run python scripts/dev.py test-concurrency
uv run python scripts/dev.py test-architecture
uv run python scripts/dev.py test-migrations
pnpm test
pnpm test:e2e
```

Scripts phải trả non-zero khi fail.

---

# 79. Local developer test loop

Trước commit:

```text
format
lint
typecheck
relevant unit tests
relevant integration tests
contract tests nếu contract đổi
```

Trước PR:

```text
full changed-context suite
architecture
security nếu relevant
migration
frontend build
```

Trước Sprint acceptance:

```text
full CI
E2E
concurrency
failure injection
performance baseline
```

---

# 80. Test evidence

Acceptance Report phải ghi:

- Command.
- Environment.
- Commit.
- Timestamp.
- Result.
- Passed/failed/skipped.
- Duration.
- Known limitations.
- Artifacts.

Không ghi “tests should pass”.

---

# 81. Test report artifacts

Có thể lưu:

- JUnit XML.
- Coverage report.
- Playwright trace.
- Screenshots.
- Performance summary.
- Migration report.
- Security scan.
- Compatibility diff.
- Concurrency diagnostics.

Không commit oversized binary nếu CI artifact đủ.

---

# 82. Skipped tests

Skip chỉ khi:

- Platform not available.
- Approved environment condition.
- Known issue với owner.
- Feature explicitly disabled.

Mỗi skip phải có reason.

Không dùng skip để che failure.

---

# 83. Expected failures

`xfail` chỉ khi:

- Known defect.
- Issue.
- Strict mode.
- Expiry.

Unexpected pass phải fail hoặc alert.

---

# 84. Test cleanup

Cleanup phải:

- Idempotent.
- Không xóa unrelated data.
- Chạy khi test fail.
- Không che primary failure.
- Không dùng broad production-like delete.

Testcontainer teardown tự động.

---

# 85. External provider tests

Levels:

## Unit

Mock/stub provider.

## Contract

Provider sandbox/schema.

## Integration

Sandbox environment.

## E2E

Selected test account.

Không gọi production provider trong CI.

---

# 86. Webhook tests

Phải test:

- Valid signature.
- Invalid signature.
- Expired timestamp.
- Replay.
- Duplicate provider event.
- Out-of-order provider event.
- Unknown event type.
- Raw payload retention/reference.
- Async processing.
- Reconciliation.

---

# 87. File tests

Phải test:

- Upload intent.
- Size.
- MIME.
- Hash.
- Complete.
- Malware status.
- Quarantine.
- Signed URL.
- Unauthorized download.
- Expiry.
- Duplicate upload.
- Object missing.
- Cleanup.

Không dùng real malicious file; dùng safe standard test fixture.

---

# 88. Analytics tests

Phải test:

- Metric formula.
- Grain.
- Filter.
- Scope.
- Currency.
- Timezone.
- Freshness.
- Reconciliation.
- Drill-down.
- Snapshot.
- Restatement.
- Frontend không tự tính KPI.

Golden datasets phải versioned.

---

# 89. Matching tests

Phải test:

- Hard exclusions.
- Soft score.
- Weight sum.
- Missing data.
- Staleness.
- Explanation.
- Determinism.
- Tie-breaking.
- Scope/privacy.
- Reverse matching masking.

Không gọi score là probability nếu không phải model xác suất.

---

# 90. Financial tests

Phải test:

- Decimal precision.
- Rounding.
- Currency mismatch.
- Partial.
- Over-allocation.
- Duplicate intake.
- Reversal.
- Immutable evidence.
- Concurrent operations.
- Reconciliation.
- Audit.
- SoD.

Financial test vectors phải được Product/Finance review.

---

# 91. Customer identity tests

Phải test:

- Normalization.
- Duplicate.
- Shared phone exception.
- Verification.
- Concurrency.
- Merge.
- Redirect.
- Cross-context rebind.
- PII masking.
- Search privacy.

---

# 92. Commercial Lock tests

Phải test:

- Acquire.
- Conflict.
- Expire.
- Extend.
- Release.
- Convert.
- Concurrent requests.
- Database final guard.
- Reconciliation.
- Cache failure.
- Booking conversion.

---

# 93. Numbering tests

Phải test:

- Token grammar.
- Preview.
- Publish.
- Scope.
- Reset.
- 200 concurrent issuance.
- Idempotent replay.
- Same key/different payload.
- Lost response.
- No reuse.
- Gap accepted.
- Sequence integrity.

---

# 94. Business Calendar tests

Phải test:

- Weekly windows.
- Exceptions.
- Multiple windows.
- Boundary.
- Weekend.
- Holiday.
- Add duration.
- Calculate duration.
- DST.
- Version effective dates.
- Overlap.
- Publish immutability.
- Large range guard.

---

# 95. Permission tests

Permission Registry tests:

- Unique codes.
- Valid Context.
- Valid scopes.
- Field policies.
- SoD conflicts.
- Seed idempotency.
- Endpoint metadata consistency.
- No unregistered permission usage.

---

# 96. Error code tests

Error Registry tests:

- Unique codes.
- HTTP status.
- Retryability.
- Safe message.
- Context ownership.
- API documentation.
- No raw database/provider error leakage.

---

# 97. Observability tests

Test:

- Logs have correlation.
- No PII.
- Metrics increment.
- Low-cardinality labels.
- Trace propagation.
- Alert condition.
- Health degraded state.

Không cần assert exact log text nếu structured fields mới là contract.

---

# 98. Runbook verification tests

Critical runbooks phải được drill:

- Outbox backlog.
- DLQ.
- Backup/restore.
- Database failure.
- RabbitMQ failure.
- Data repair.
- Break-glass.
- Release rollback.

Runbook không được coi là hoàn chỉnh nếu chưa thử.

---

# 99. Test review checklist

## Behavior

- Test đúng requirement?
- Có edge cases?
- Có negative path?
- Có boundary?

## Architecture

- Đúng test layer?
- Có mock quá mức?
- Có dùng real dependency khi cần?

## Reliability

- Deterministic?
- Idempotent?
- Cleanup?
- Concurrency thật?

## Security

- Scope?
- Masking?
- No PII?
- No unauthorized side effects?

## Maintainability

- Tên rõ?
- Setup rõ?
- Assertions mạnh?
- Không brittle?

---

# 100. Test anti-patterns bị cấm

1. SQLite thay PostgreSQL.
2. Sleep để chờ async.
3. Test phụ thuộc order.
4. Shared mutable fixture.
5. Mock mọi thứ.
6. Chỉ test happy path.
7. Assert status != 500.
8. Update snapshot mù.
9. Skip không lý do.
10. Retry flaky test để green.
11. Quarantine critical test.
12. Dùng production data.
13. Test implementation private.
14. E2E cho toàn bộ business logic.
15. Không test constraints.
16. Không test concurrency.
17. Không test authorization matrix.
18. Không test duplicate event.
19. Sửa test để hợp thức hóa bug.
20. Báo pass khi chưa chạy.
21. Không ghi test command.
22. Dùng arbitrary sleep trong Playwright.
23. Dùng full backend mock trong core E2E.
24. Bỏ cleanup.
25. Test quá nhiều behavior trong một case.

---

# 101. AI Agent testing protocol

Trước khi code, AI Agent phải:

1. Đọc acceptance criteria.
2. Xác định test layers.
3. Liệt kê happy/negative/boundary/concurrency/security cases.
4. Viết hoặc cập nhật tests cùng code.
5. Chạy relevant tests.
6. Chạy regression.
7. Chạy contract/migration khi có thay đổi.
8. Review failures.
9. Không sửa tests mù.
10. Ghi test evidence.

---

# 102. AI Agent prohibited testing behaviors

AI Agent không được:

1. Bỏ test vì “không có thời gian”.
2. Chỉ viết happy path.
3. Mock database cho repository.
4. Dùng SQLite.
5. Sửa expected result để code sai pass.
6. Xóa failing test không lý do.
7. Skip/flaky retry không issue.
8. Báo test pass khi chưa chạy.
9. Bỏ concurrency/security test.
10. Dùng production PII.
11. Tạo fake evidence.
12. Tuyên bố Done khi CI đỏ.

---

# 103. Definition of Ready cho test plan

Test plan chỉ Ready khi:

1. Requirement rõ.
2. Invariants rõ.
3. State machine rõ.
4. Database impact rõ.
5. API/Event impact rõ.
6. Permission/scope rõ.
7. Concurrency risk rõ.
8. Failure modes rõ.
9. Acceptance criteria rõ.
10. Environment/data strategy rõ.

---

# 104. Definition of Done cho feature testing

Feature testing Done khi:

1. Unit tests.
2. Application tests.
3. Database integration.
4. API tests.
5. Contract tests.
6. Security tests.
7. Concurrency tests khi relevant.
8. Event tests khi relevant.
9. Frontend tests.
10. E2E critical path.
11. Failure injection khi critical.
12. Performance baseline khi hot path.
13. Regression tests.
14. CI green.
15. Evidence recorded.
16. No unexplained skips/flakes.

---

# 105. Definition of Done cho Sprint testing

Sprint testing Done khi:

1. All in-scope acceptance criteria mapped to tests.
2. Full changed-context suite pass.
3. Migrations pass.
4. Architecture pass.
5. Security pass.
6. Contract pass.
7. Concurrency pass.
8. Frontend build/test pass.
9. E2E pass.
10. Failure injection pass where required.
11. Performance baseline pass.
12. Test report complete.
13. Known limitations explicit.
14. Acceptance Report signed.

---

# 106. Release test gates

Production release phải block nếu:

- Critical/High test failure.
- Security regression.
- Migration failure.
- Contract breaking diff unapproved.
- Concurrency corruption.
- Backup/restore failure.
- UAT critical journey failure.
- Performance below hard SLO.
- Flaky critical test.
- Missing runbook drill.

---

# 107. Test exception process

Ngoại lệ cần file:

```text
docs/engineering/testing-exceptions/EXC-TEST-XXX.md
```

Nội dung:

- Rule.
- Test/scope.
- Reason.
- Risk.
- Coverage gap.
- Mitigation.
- Owner.
- Expiry.
- Replacement plan.
- Approval.

Không có ngoại lệ vô thời hạn không owner.

---

# 108. Required test documentation

Mỗi Context nên có:

```text
docs/contexts/<context>/acceptance-tests.md
```

Mỗi Sprint:

```text
docs/sprints/sprint-XXX/implementation-notes.md
docs/sprints/sprint-XXX/acceptance-report.md
```

Critical journeys:

```text
docs/uat/critical-business-journeys.md
```

---

# 109. Completion report template

```markdown
## Testing Summary

### Test Environment

### Test Commands

### Unit Tests

### Integration Tests

### Migration Tests

### Contract Tests

### Architecture Tests

### Security Tests

### Concurrency Tests

### Event Tests

### Frontend Tests

### E2E Tests

### Performance Tests

### Failure Injection

### Backup/Restore

### Skipped/Quarantined Tests

### Known Limitations

### Final Result
```

---

# 110. Change Log

## Version 1.0.0 — 2026-07-24

- Thiết lập test taxonomy và test pyramid.
- Khóa Unit, Integration, Contract và Architecture testing.
- Khóa PostgreSQL/Testcontainers.
- Khóa Security và Concurrency testing.
- Khóa Event, Job, Frontend và E2E testing.
- Khóa Performance, Load, Soak và Failure Injection.
- Khóa Reconciliation, Backup và Restore testing.
- Khóa fixtures, mocks, coverage và flaky-test policy.
- Khóa CI gates, evidence và acceptance.
- Khóa AI Agent Testing Protocol.

---

# 111. Kết luận

Testing trong `crm_bds_ai` không phải bước cuối cùng sau khi code.

Testing là một phần của thiết kế hệ thống:

```text
Business Requirements
→ Invariants
→ Contracts
→ Implementation
→ Automated Evidence
→ Operational Confidence
```

Nguyên tắc tối cao:

> Không một feature nào được coi là hoàn thành nếu chưa chứng minh bằng test rằng nó đúng ở điều kiện bình thường, điều kiện lỗi, điều kiện cạnh tranh và điều kiện bảo mật.


# AI testing requirements

AI changes require deterministic mock-adapter tests, adapter conformance tests, routing/security negative tests, schema/tool tests, evaluation regression, failure isolation, quota/circuit behavior and human-approval/Audit evidence. Live-provider tests are non-blocking unless explicitly approved for the environment.
