# CRM_BDS_AI — OBSERVABILITY STANDARDS

## Quy chuẩn quan sát hệ thống bắt buộc cho toàn bộ `crm_bds_ai`

**Document ID:** `ENG-OBS-001`  
**Canonical path:** `docs/engineering/observability-standards.md`  
**Product:** `crm_bds_ai`  
**Version:** `1.0.0`  
**Status:** `Accepted / Mandatory`  
**Canonical scope:** Nguyên tắc, ranh giới, telemetry governance và operational-diagnostics discipline  
**Owner:** `Observability Architecture Owner`  
**Reviewers:** `Architecture Owner`, `Technical Owner`, `Operations Owner`, `Security Owner`, `Database Owner`, `Frontend Owner`, `QA Owner`, `Audit Owner`, `Context Owners`  
**Effective date:** `2026-08-05`  
**Last reviewed:** `2026-08-05`  
**Next review:** Khi topology, telemetry architecture, SLO, privacy policy, production traffic, alerting model hoặc major dependencies thay đổi  
**Supersedes:** `None — Greenfield baseline`  
**Classification:** `INTERNAL`

---

# 1. Mục đích

Tài liệu này quy định cách thiết kế, phát sinh, thu thập, truyền, lưu trữ, truy vấn, hiển thị, cảnh báo, kiểm thử và quản trị telemetry trong `crm_bds_ai`.

Mục tiêu:

1. Bảo đảm request, command, query, Event, job và process quan trọng có thể truy vết.
2. Bảo đảm lỗi có thể chẩn đoán mà không cần tái tạo production data.
3. Bảo đảm hệ thống đo được availability, latency, throughput, correctness, durability và freshness.
4. Bảo đảm SLI/SLO dựa trên telemetry đáng tin cậy.
5. Bảo đảm logs, metrics và traces không rò rỉ PII, secrets hoặc financial evidence.
6. Bảo đảm business anomalies được quan sát, không chỉ infrastructure failures.
7. Bảo đảm PostgreSQL, RabbitMQ, Valkey, Object Storage, jobs và frontend đều có signal phù hợp.
8. Bảo đảm cross-context flow có correlation và causation rõ.
9. Bảo đảm alerts có owner, severity, runbook và hành động cụ thể.
10. Bảo đảm AI Agent không tự thêm telemetry cardinality cao hoặc khóa cứng implementation chưa được kiểm chứng.

---

# 2. Phạm vi thẩm quyền của tài liệu

## 2.1. Tài liệu này là nguồn chuẩn cho

- Logging principles và structured-log discipline.
- Metrics semantics và cardinality discipline.
- Distributed tracing và context propagation.
- Correlation, causation và operation identity.
- SLI/SLO telemetry requirements.
- Dashboard và alert governance.
- Security/privacy requirements cho telemetry.
- Frontend, backend, database, broker, job và integration observability principles.
- Failure diagnostics và incident evidence requirements.
- Testing và release gates cho observability.
- Cost, retention và access-governance principles.
- AI Agent observability discipline.
- Các anti-pattern bị cấm.

## 2.2. Tài liệu này không phải nguồn chuẩn cho

- Exact metric inventory của toàn hệ thống.
- Exact metric names của feature chưa triển khai.
- Exact label set của từng metric.
- Exact log field inventory của từng Context.
- Exact dashboard layout.
- Exact alert threshold hoặc severity SLA.
- Exact trace sampling rate.
- Exact log/trace/metric retention.
- Exact telemetry vendor.
- Exact collector/exporter topology.
- Exact storage backend.
- Exact SLO target.
- Exact cardinality budget.
- Exact histogram buckets.
- Exact health-check dependency list.
- Exact synthetic-monitoring cadence.
- Exact business KPI definitions.
- Exact runbook inventory.
- Exact frontend telemetry event inventory.
- Exact incident-management integration.
- Exact infrastructure-agent configuration.
- Exact production capacity hoặc cost budget.

## 2.3. Nguồn chân lý thực thi

| Nội dung | Nguồn chân lý |
|---|---|
| Exact SLI/SLO targets | `service-level-objectives.md` |
| Exact performance/capacity assumptions | NFR + Capacity Model |
| Exact metric/log/trace inventory | Observability Catalog |
| Exact alerts | Alert Catalog + alert rules |
| Exact dashboards | Dashboard Catalog + dashboard definitions |
| Exact retention | Telemetry Retention + Privacy and Retention Policy |
| Exact telemetry platform/topology | Environment Topology + IaC |
| Exact Event fields/contracts | JSON Schema + AsyncAPI |
| Exact API operations | OpenAPI |
| Exact security classifications | Data Classification + security matrices |
| Exact Context signals | Context Implementation Pack |
| Exact feature scope | Sprint Detailed Execution Pack |
| Current implementation | Code + telemetry configuration + tests |
| Actual operational evidence | Telemetry backend + incident/release artifacts |
| Completion evidence | Sprint Acceptance Report |

Khi Markdown khác deployed telemetry configuration, machine-readable catalog hoặc accepted SLO, conflict phải được xử lý theo Documentation Governance.

---

# 3. Từ khóa quy chuẩn

- **MUST:** Bắt buộc.
- **MUST NOT:** Bị cấm.
- **SHOULD:** Khuyến nghị mạnh; lệch chuẩn cần lý do.
- **SHOULD NOT:** Không nên; lệch chuẩn cần lý do.
- **MAY:** Có thể dùng khi phù hợp.
- **BASELINE:** Điểm khởi đầu cần được kiểm chứng.
- **EXAMPLE:** Minh họa, không phải exact contract.
- **CONTEXT-SPECIFIC:** Quyết định thuộc Context Pack hoặc Observability Catalog.
- **ENVIRONMENT-SPECIFIC:** Quyết định thuộc topology/configuration.
- **SLO-SPECIFIC:** Quyết định thuộc Service Level Objectives.
- **RISK-BASED:** Quyết định dựa vào criticality, blast radius và data sensitivity.
- **PENDING VALIDATION:** Chưa được xem là production truth.

Mọi metric name, field, dashboard, threshold, sampling rate hoặc retention trong tài liệu này chỉ là ví dụ trừ khi nguồn chân lý tương ứng xác nhận.

---

# 4. Nguyên tắc tối cao

```text
Actionable Signal
> Correctness
> Security and Privacy
> Correlation
> Reliability
> Low Cardinality
> Cost Control
> Convenience
```

Telemetry không có giá trị nếu:

- Không dẫn đến hành động.
- Không có owner.
- Không có ngữ cảnh.
- Không thể tin cậy.
- Làm rò rỉ dữ liệu.
- Tạo chi phí không kiểm soát.
- Không giúp giảm thời gian phát hiện hoặc khôi phục.

---

# 5. Observability không đồng nghĩa monitoring

## 5.1. Monitoring

Monitoring trả lời các câu hỏi đã biết trước:

- Service có đang up không?
- Error rate có vượt threshold không?
- Queue backlog có tăng không?
- Backup có quá cũ không?

## 5.2. Observability

Observability giúp điều tra câu hỏi chưa dự đoán trước:

- Vì sao chỉ một nhóm scope bị lỗi?
- Vì sao một consumer chậm dù queue không đầy?
- Vì sao một business process kẹt ở bước cụ thể?
- Vì sao release mới chỉ ảnh hưởng một Context?

Hệ thống production-ready cần cả monitoring và observability.

---

# 6. Ba trụ cột telemetry

## 6.1. Logs

Dùng để trả lời:

- Điều gì đã xảy ra?
- Ở operation nào?
- Kết quả gì?
- Error code nào?
- Retry lần mấy?
- Correlation nào?

## 6.2. Metrics

Dùng để trả lời:

- Hệ thống đang khỏe không?
- Tỷ lệ lỗi bao nhiêu?
- Latency thay đổi thế nào?
- Backlog có tăng không?
- SLO có bị đốt nhanh không?
- Có anomaly không?

## 6.3. Traces

Dùng để trả lời:

- Request đi qua các thành phần nào?
- Chậm ở đâu?
- Dependency nào gây lỗi?
- Cross-context hop nào làm journey kẹt?
- Provider call hay database chiếm thời gian?

Ba trụ cột bổ sung cho nhau; không trụ cột nào thay hoàn toàn hai trụ cột còn lại.

---

# 7. Audit không phải observability log

Audit Context và operational telemetry có mục đích khác nhau.

## Audit

- Bằng chứng hành động.
- Append-only/protected.
- Actor.
- Resource.
- Reason.
- Outcome.
- Retention theo policy.
- Controlled access.

## Operational log

- Chẩn đoán kỹ thuật.
- Có thể sampled.
- Retention thường ngắn hơn.
- Không phải legal evidence.
- Có thể chứa implementation metadata an toàn.

MUST NOT:

- Ghi business approval chỉ bằng log.
- Dùng request log thay Audit.
- Dùng metric thay evidence.
- Dump full before/after object vào log.

---

# 8. Observability architecture

Logical flow:

```text
Application / Worker / Frontend / Infrastructure
→ Telemetry SDK / Structured Logger
→ Collector / Agent
→ Logs, Metrics, Traces Backends
→ Dashboards, Alerts, Reports, Incident Tools
```

Exact telemetry platform và topology thuộc Environment Topology/IaC.

Business Domain MUST NOT phụ thuộc vendor-specific telemetry SDK.

---

# 9. Open standards và abstraction

Telemetry implementation SHOULD tương thích approved open standards và project tooling, ví dụ:

- Structured JSON logs.
- Standard trace context propagation.
- OpenTelemetry-compatible instrumentation.
- Prometheus-style metrics semantics.

Exact vendor/exporter/backend không khóa trong Standards.

---

# 10. Telemetry ownership

Mỗi signal quan trọng MUST có:

```text
owner
purpose
source
unit/semantics
classification
retention
dashboard
alert policy
runbook
validation
```

Không tạo telemetry không owner hoặc “để sau này có thể dùng”.

---

# 11. Telemetry taxonomy

Telemetry được phân loại:

```text
Platform telemetry
Application telemetry
Domain anomaly telemetry
Security telemetry
Database telemetry
Messaging telemetry
Frontend telemetry
Integration telemetry
Job/process telemetry
Data-quality telemetry
SLO telemetry
```

Official business KPI không mặc định lấy từ operational telemetry.

---

# 12. Resource identity

Mọi telemetry SHOULD có resource/service attributes ổn định.

Conceptual attributes:

```text
service.name
service.namespace
service.version
deployment.environment
service.instance.id
region/zone when relevant
```

Exact attribute names thuộc telemetry conventions/catalog.

MUST NOT dùng hostname ngẫu nhiên làm business identity.

---

# 13. Environment identity

Mọi telemetry MUST xác định environment.

Conceptual environments:

```text
local
test
ci
staging
uat
production
```

Production và non-production MUST không bị trộn lẫn trong query/dashboard mà không có filter rõ.

---

# 14. Context identity

Application telemetry SHOULD xác định owning Bounded Context khi relevant.

Context label/field phải là low-cardinality stable code.

MUST NOT dùng arbitrary module path hoặc class name làm Context identity.

---

# 15. Operation identity

Telemetry SHOULD dùng stable operation name.

Examples:

```text
command.issue_receipt
query.list_customers
job.reconcile_payments
consumer.create_revenue_entitlement
```

Exact operation inventory thuộc Observability Catalog/Context Pack.

MUST NOT dùng raw URL, SQL text hoặc method signature làm metric label.

---

# 16. Correlation model

Canonical identifiers có thể gồm:

```text
request_id
correlation_id
causation_id
trace_id
span_id
event_id
job_id
process_id
resource_id
```

Không phải mọi signal cần mọi identifier.

---

# 17. Request ID

Request ID đại diện một inbound request.

MUST:

- Unique trong phạm vi đủ an toàn.
- Không chứa PII.
- Được trả cho client/support khi phù hợp.
- Được log/traced.
- Không dùng làm authorization input.

---

# 18. Correlation ID

Correlation ID liên kết một business journey qua:

- HTTP requests.
- Commands.
- Events.
- Jobs.
- Process Managers.
- Provider interactions.

Không generate correlation mới ở mỗi hop nếu vẫn cùng journey.

---

# 19. Causation ID

Causation ID xác định operation/message trực tiếp gây ra operation tiếp theo.

Giúp xây chain:

```text
request
→ command
→ Event
→ consumer command
→ next Event
```

---

# 20. Trace ID

Trace ID dành cho distributed tracing.

Trace ID không thay correlation ID.

Correlation có thể sống dài hơn một trace.

---

# 21. Event, Job và Process IDs

Event/job/process identifiers MAY xuất hiện trong logs/traces.

MUST NOT dùng làm metric labels do cardinality cao.

---

# 22. Correlation propagation

Correlation và trace context MUST được propagate qua các boundary khi relevant:

- HTTP.
- Application command/query.
- Outbox.
- Broker headers.
- Inbox.
- Background jobs.
- Process Manager.
- Provider calls.
- Reconciliation.
- Frontend error reports.

---

# 23. Correlation trust

Inbound correlation/request IDs là untrusted metadata.

MUST:

- Validate format/length.
- Regenerate khi invalid.
- Không dùng cho authorization.
- Không cho phép log injection.
- Không chứa PII.

---

# 24. Logging principles

Production logs MUST:

- Structured.
- Machine-readable.
- Timestamped.
- Correlated.
- Classified.
- Redacted.
- Bounded.
- Searchable.
- Actionable.

Human-readable logs MAY dùng local development, nhưng production truth phải structured.

---

# 25. Structured log format

Conceptual example:

```json
{
  "timestamp": "2026-07-26T03:00:00Z",
  "level": "INFO",
  "event_name": "application.command.completed",
  "message": "Command completed",
  "service": "crm-bds-next-api",
  "service_version": "release-id",
  "environment": "production",
  "context": "contract",
  "operation": "issue_receipt",
  "request_id": "uuid",
  "correlation_id": "uuid",
  "trace_id": "hex",
  "resource_type": "Receipt",
  "resource_id": "uuid",
  "result": "SUCCESS",
  "duration_ms": 83
}
```

Đây là example, không phải exact log schema.

---

# 26. Log schema governance

Shared log schema SHOULD được versioned/documented.

Breaking field changes cần:

- Consumer/dashboard inventory.
- Migration window.
- Query/alert updates.
- Changelog.
- Compatibility consideration.

Không rename field âm thầm.

---

# 27. Log levels

## TRACE

- Chẩn đoán rất sâu.
- Không production mặc định.
- Không chứa payload nhạy cảm.

## DEBUG

- Local/staging hoặc time-bound production debugging.
- Phải auto-expire/approval trong production.
- Không log full object.

## INFO

- Lifecycle/operation completion.
- Request completion.
- Job/process milestone.
- Controlled state transition summary.

## WARN

- Recoverable anomaly.
- Retry.
- Degraded dependency.
- Approaching threshold.
- Stale projection.

## ERROR

- Operation failure.
- Permanent consumer failure.
- Failed job.
- Unexpected dependency/database error.
- Integrity finding.

## CRITICAL

- Broad outage.
- Security compromise.
- Financial/data-integrity risk.
- Audit failure.
- Recovery capability loss.

Expected validation/conflict SHOULD NOT bị log như unexpected ERROR.

---

# 28. Stable log event names

Logs SHOULD có stable `event_name`.

Examples:

```text
http.request.completed
application.command.failed
event.outbox.publish_failed
event.consumer.permanent_failure
job.execution.completed
database.transaction.deadlocked
security.authorization.denied
```

Human-readable message có thể đổi; event name phải ổn định.

---

# 29. Required log fields

Common fields MAY gồm:

```text
timestamp
level
event_name
message
service
service_version
environment
context
operation
result
duration
request_id
correlation_id
trace_id
error_code
```

Conditional fields MAY gồm:

```text
actor_type
actor_key
enterprise_id
legal_entity_id
project_id
resource_type
resource_id
event_id
job_id
process_id
attempt
provider
```

Exact requiredness thuộc Log Schema Catalog.

---

# 30. Forbidden log content

MUST NOT log:

- Password.
- Access token.
- Refresh token.
- Authorization header.
- Cookie/session value.
- API secret.
- Private key.
- Database credential.
- Webhook secret.
- Permanent/signed URL.
- Full phone.
- Full email.
- Identity number.
- Bank account.
- Payment evidence.
- Contract/document content.
- Raw file.
- Full request/response body.
- Raw provider payload.
- SQL parameters chứa PII.
- Customer free text.
- Sensitive search term.

---

# 31. PII-safe references

MAY log khi policy cho phép:

- Opaque resource UUID.
- Actor key.
- Safe HMAC/reference.
- Count.
- Classification.
- Last digits nếu explicitly approved.

Plain hash của low-entropy PII không tự động anonymous.

---

# 32. Redaction

Redaction MUST centralized khi có thể.

Targets:

```text
authorization
cookie
password
token
secret
phone
email
identity_number
bank_account
signed_url
document_content
```

Nested object redaction phải được test.

Không phụ thuộc developer nhớ xóa thủ công ở từng call site.

---

# 33. Request logging

API request logs SHOULD ghi:

```text
method
route template
status code
duration
request/response size
request ID
correlation ID
operation
error code
safe scope metadata
```

MUST NOT log raw URL nếu query có thể chứa sensitive data.

---

# 34. Response logging

MUST NOT log response body mặc định.

MAY log:

- Status.
- Size.
- Result.
- Error code.
- ETag presence.
- Pagination count.
- Cache result.
- Partial/degraded state.

---

# 35. Command logging

State-changing command SHOULD log:

```text
command name
resource type
resource ID
expected version
result
error code
duration
idempotency outcome
Audit result
Outbox count
```

Không log full command payload.

---

# 36. Query logging

Query log MAY ghi:

```text
query name
scope type
page size
filter count
sort
result count
duration
cache result
```

Không log raw search term có PII.

---

# 37. Database logging

Application database telemetry SHOULD ghi:

- Operation/query name.
- Duration.
- Rows returned/affected.
- Retry.
- SQLSTATE category.
- Lock wait.
- Transaction outcome.

MUST NOT log raw SQL + bound parameters ở production mặc định.

---

# 38. Slow query diagnostics

Slow query diagnostics SHOULD có:

```text
query name/fingerprint
duration
rows
Context
route/job/consumer
correlation
plan reference when safely captured
```

Exact slow threshold thuộc SLO/NFR/configuration.

---

# 39. Event logging

Producer SHOULD log:

```text
event ID
event type/version
producer Context
aggregate/subject reference
Outbox status
publish attempt
result
```

Consumer SHOULD log:

```text
consumer name
event ID
event type/version
Inbox status
attempt
duration
result
error code
```

Không log full Event payload.

---

# 40. Job logging

Mỗi job execution SHOULD log:

```text
job name
job ID
queue
attempt
status
scheduled/started/completed times
duration
items total/processed/failed
checkpoint
error code
```

Không chỉ log “started” và “finished”.

---

# 41. Process Manager logging

Long-running process SHOULD log:

```text
process type
process ID
resource reference
current step
previous step
status
retry count
waiting reason
deadline
compensation state
```

---

# 42. Security logging

Security log event names MAY gồm:

```text
security.authentication.failed
security.authorization.denied
security.break_glass.activated
security.sensitive_export.requested
security.webhook.signature_invalid
security.file.quarantined
security.secret.rotation_failed
```

Exact event inventory thuộc Security/Audit catalogs.

---

# 43. Logging failures

Non-critical telemetry sink failure SHOULD NOT crash normal business request.

Tuy nhiên:

- Audit failure có policy riêng.
- Telemetry drop/export failure phải observable khi feasible.
- Buffer/backpressure phải bounded.
- Application không được tích lũy unbounded log memory.

---

# 44. Dynamic log levels

Dynamic log level MAY được hỗ trợ.

MUST:

- Scope theo service/Context.
- Time-bound.
- Approved.
- Audited.
- Auto-expire.
- Không bypass redaction.

Không bật DEBUG production vô thời hạn.

---

# 45. Metrics principles

Metrics MUST:

- Có clear semantics.
- Có unit.
- Có type đúng.
- Low-cardinality.
- Stable.
- Documented.
- Owned.
- Actionable.
- Không chứa PII.

---

# 46. Metric naming

Metric naming SHOULD theo stable project convention.

Conceptual example:

```text
crm_<subsystem>_<metric>_<unit>
```

Examples:

```text
crm_http_requests_total
crm_http_request_duration_seconds
crm_event_outbox_pending_messages
crm_job_execution_duration_seconds
```

Exact names thuộc Observability Catalog.

---

# 47. Metric types

## Counter

Chỉ tăng:

```text
requests_total
failures_total
retries_total
```

## Gauge

Giá trị hiện tại:

```text
queue_depth
active_sessions
outbox_pending
```

## Histogram

Distribution:

```text
request_duration_seconds
query_duration_seconds
payload_size_bytes
```

## Summary

MAY dùng khi tooling/aggregation requirements thật sự phù hợp.

Histogram thường được ưu tiên cho aggregation nhiều instance.

---

# 48. Metric units

MUST dùng consistent base units.

Examples:

- Seconds cho duration.
- Bytes cho size.
- Total suffix cho counters.
- Ratio cho 0–1 values.
- Count cho absolute items.

Không trộn milliseconds và seconds dưới cùng metric name.

---

# 49. Cardinality policy

MUST NOT dùng làm metric labels:

- Request ID.
- Correlation ID.
- Event ID.
- Job ID.
- Resource/customer/contract ID.
- Actor ID.
- Phone/email.
- Raw URL.
- Error message.
- Search term.
- SQL text.
- File name.
- Stack trace.

---

# 50. Allowed label classes

Potential low-cardinality labels:

```text
route template
HTTP method
status class
Context
operation
error code
consumer name
Event type/version
environment
result
provider
queue class
```

Exact labels vẫn cần cardinality review.

---

# 51. Cardinality budget

Mỗi metric mới SHOULD đánh giá:

```text
estimated series count
label dimensions
value counts
scrape frequency
retention
cost
```

Exact budget thuộc Observability Platform/Capacity Model.

High-cardinality metrics phải redesign hoặc dùng logs/traces.

---

# 52. Histogram buckets

Histogram buckets MUST phù hợp SLO và observed distribution.

Không dùng một bucket set cho mọi loại operation.

Exact buckets là SLO/environment-specific.

---

# 53. API metrics

API layer SHOULD có baseline signals:

```text
requests
duration
in-flight
request/response size
rate-limit rejection
authorization denial
idempotency replay/conflict
optimistic conflict
```

Exact metric names thuộc catalog.

---

# 54. Application-command metrics

Potential signals:

```text
command executions
command duration
command failures
idempotency conflicts
concurrency conflicts
```

Labels phải low-cardinality:

```text
Context
command name
result
error code
```

---

# 55. Query metrics

Potential signals:

```text
query executions
query duration
rows returned
cache hit/miss
pagination size
```

Không label filter value.

---

# 56. Database metrics

Required signal classes:

- Connections.
- Pool saturation/wait.
- Query duration.
- Transactions.
- Rollbacks.
- Deadlocks.
- Lock waits.
- Statement timeouts.
- Replication lag.
- WAL/storage.
- Autovacuum/bloat indicators.
- Backup age.

Exact exporter metrics thuộc infrastructure configuration.

---

# 57. Outbox metrics

Required signal classes:

- Pending count.
- Retry count.
- Dead count.
- Oldest age.
- Publish duration.
- Publish failures.
- Stale claims.
- Throughput.

---

# 58. Consumer/Inbox metrics

Required signal classes:

- Received.
- Processed.
- Duplicates.
- Failures.
- Retries.
- Permanent failures.
- Lag.
- Processing duration.
- Ordering gaps.
- Inbox stale processing.

---

# 59. RabbitMQ metrics

Monitor when relevant:

- Messages ready/unacknowledged.
- Publish/deliver/ack rates.
- Consumer count.
- Redeliveries.
- Connections/channels.
- Memory/disk alarms.
- Node/quorum health.
- Queue age/lag.

Exact topology/thresholds thuộc Operations.

---

# 60. Valkey metrics

Monitor when relevant:

- Memory.
- Evictions.
- Hit ratio.
- Connections.
- Command latency.
- Key count.
- Replication/persistence if used.
- Errors.

Cache hit ratio không tự động là incident nếu correctness không ảnh hưởng.

---

# 61. Object Storage metrics

Potential signals:

- Request error rate.
- Latency.
- Upload/download failures.
- Missing object findings.
- Replication lag.
- Scan backlog.
- Quarantine count.
- Storage growth.
- Signed-access failures.

---

# 62. Background-job metrics

Potential signals:

- Executions.
- Failures.
- Duration.
- Queue wait.
- Retries.
- Timeouts.
- Stale jobs.
- Items processed/failed.
- Missed schedules.

---

# 63. Process Manager metrics

Potential signals:

- Started.
- Completed.
- Failed.
- Waiting.
- Duration.
- Compensations.
- Manual intervention.
- Deadline missed.

---

# 64. Security metrics

Potential signals:

- Authentication failures.
- Authorization denials.
- Break-glass sessions.
- Webhook signature failures.
- Sensitive exports.
- File quarantines.
- Secret failures.
- Rate-limit rejection.
- Cross-scope attempts.

MUST NOT label actor/customer identity.

---

# 65. Frontend metrics

Frontend observability MAY đo:

- User-experience metrics.
- Route-transition duration.
- Frontend errors.
- API error rate.
- Session-expiry events.
- Build version.
- Critical interaction timing.

Exact browser metric set và thresholds thuộc Frontend/Observability Catalog.

---

# 66. Business anomaly metrics

Examples:

```text
customer duplicate candidates
commercial lock conflicts
booking confirmation failures
payment overallocation attempts
receipt issuance conflicts
reconciliation findings
audit write failures
document missing-object findings
```

Operational anomaly metrics không tự động là official KPI.

---

# 67. Data-quality metrics

Data-quality dimensions MAY gồm:

```text
completeness
validity
uniqueness
consistency
timeliness
referential integrity
```

Fix phải qua canonical repair/reconciliation process, không tự sửa chỉ vì metric tăng.

---

# 68. SLI definition

Mỗi SLI MUST có:

```text
name
purpose
numerator
denominator
data source
window
exclusions
owner
validation
```

Không dùng vague “uptime” không định nghĩa.

---

# 69. Availability SLI

Availability SLI phải xác định:

- Eligible operations/routes.
- Expected 4xx.
- Maintenance treatment.
- Dependency failures.
- Partial/degraded responses.
- Authentication/authorization outcomes.
- Synthetic versus server-side source.

Validation errors và legitimate authorization denial không mặc định là availability failure.

---

# 70. Latency SLI

Latency SLI MUST:

- Theo operation/route class.
- Có percentile.
- Có scope/payload assumptions.
- Phân biệt synchronous và async accepted work.
- Dùng source đáng tin cậy.
- Có exclusion rõ.

Exact targets thuộc SLO.

---

# 71. Correctness SLI

Critical correctness examples:

- No duplicate official number.
- No over-allocation.
- Required Outbox eventually published.
- Consumer permanent-failure rate bounded.
- Required Audit written.
- Document reference integrity.
- Projection correctness within tolerance.

Exact SLI inventory thuộc Context/SLO design.

---

# 72. Freshness SLI

Dùng cho:

- Analytics.
- Search.
- Timeline.
- Event consumers.
- Dashboards.
- External sync.

Conceptual definition:

```text
current time - latest successfully applied authoritative change
```

Exact source event/time semantics phải rõ.

---

# 73. Durability/recovery SLI

Potential signals:

- Backup age.
- WAL archive lag.
- Object replication lag.
- Restore verification success.
- Audit integrity check.
- Recovery drill success.

---

# 74. SLO governance

SLO MUST:

- Có owner.
- Có business rationale.
- Có reliable telemetry source.
- Có review.
- Có error-budget policy.
- Không dựa metric dễ bị thao túng.
- Không duplicate nhiều định nghĩa khác nhau.

Exact targets không thuộc Standards này.

---

# 75. Error budget

Error budget SHOULD:

- Gắn với SLO.
- Có consumption reporting.
- Ảnh hưởng release decision.
- Có policy khi burn cao.

Security hoặc integrity failures không được hợp thức hóa chỉ vì error budget còn.

---

# 76. Burn-rate alerting

Alerts MAY dùng multi-window burn-rate.

Exact windows/multipliers thuộc SLO/Alert Catalog.

Không alert dựa một datapoint nhiễu nếu không có reason.

---

# 77. Dashboard principles

Dashboard MUST:

- Có owner.
- Có purpose.
- Có audience.
- Có environment/time range.
- Có units.
- Có links tới runbook.
- Có deploy/incident annotations khi useful.
- Không mix unrelated signals.
- Không hiển thị PII.

---

# 78. Dashboard layers

Potential dashboard classes:

```text
Executive Service Health
API/Application Health
Database Health
Messaging/Events
Background Jobs
Object Storage/Documents
Security Operations
Frontend Experience
Context Health
SLO/Error Budget
Backup/Restore
Capacity/Cost
```

Exact catalog/layout thuộc Dashboard Catalog.

---

# 79. Executive health dashboard

Should summarize:

- Availability.
- Error rate.
- Latency.
- Active incidents.
- SLO burn.
- Critical backlog.
- Database health.
- Recent releases.

Không overload low-level panels.

---

# 80. Context health dashboard

Mỗi critical Context SHOULD có dashboard hoặc section thể hiện:

- Critical operations.
- Error rate.
- Latency.
- Domain anomaly.
- Event lag.
- Reconciliation.
- Dependencies.
- Recent releases.

Exact panels thuộc Context Observability Contract.

---

# 81. Dashboard query quality

Dashboard queries MUST:

- Be bounded.
- Be efficient.
- Use correct units.
- Avoid high-cardinality fan-out.
- Have stable semantics.
- Be tested/validated.
- Avoid hidden environment mixing.

---

# 82. Alert principles

Alert MUST:

- Actionable.
- Owned.
- Severity-classified.
- Have runbook.
- Have threshold/window.
- Have dedup/grouping.
- Avoid noise.
- Avoid PII.
- Have recovery/resolve behavior.
- Be tested.

---

# 83. Alert severities

Conceptual severities MAY include:

```text
CRITICAL / SEV-1
HIGH / SEV-2
MEDIUM / SEV-3
LOW / SEV-4
```

Exact mapping/SLA thuộc Incident Response/Alert Catalog.

---

# 84. Critical alert candidates

Potential critical conditions:

- Broad outage.
- Data-integrity risk.
- Security compromise.
- Financial corruption risk.
- Audit failure.
- Backup coverage lost.
- Critical Event permanently failing.
- Production secrets inaccessible.
- Cross-tenant leakage detected.

---

# 85. Alert payload

Alert SHOULD có:

```text
title
severity
environment
service/Context
condition
started_at
current value
threshold
dashboard link
runbook link
owner
safe example trace/correlation
```

Không include customer data.

---

# 86. Alert routing

Routing SHOULD dựa:

- Environment.
- Service/Context.
- Criticality.
- Security/financial classification.
- On-call team.
- Maintenance state.

Exact channels/escalations thuộc Operations.

---

# 87. Alert deduplication

Dedup key SHOULD dùng low-cardinality dimensions như:

```text
alert name
environment
service
Context
```

Không dùng resource ID làm generic alert dedup key.

---

# 88. Alert suppression

Suppression chỉ khi:

- Approved maintenance.
- Known incident.
- Controlled test.

Must have:

- Owner.
- Reason.
- Start/end.
- Auto-expiry.
- Audit/change reference.

Không mute vô thời hạn.

---

# 89. Alert testing

Critical alerts MUST được test:

- Trigger.
- Routing.
- Dedup.
- Runbook link.
- Recovery notification.
- No PII.
- Maintenance behavior.

---

# 90. Distributed tracing principles

Traces SHOULD phản ánh meaningful operations:

- HTTP request.
- Application command/query.
- Database operation.
- Outbox materialization/publish.
- Broker consume.
- Inbox processing.
- External provider call.
- Background job.
- Process step.

Không tạo span cho mỗi helper nhỏ.

---

# 91. Span naming

Span names MUST stable và low-cardinality.

Conceptual examples:

```text
HTTP GET /api/v1/customers/{customer_id}
command IssueReceipt
query ListListings
db product.listings.select
event publish contract.receipt.issued
consumer revenue.create_entitlement
job documents.run_ocr
```

MUST NOT include dynamic IDs trong span name.

---

# 92. Span attributes

Allowed classes MAY gồm:

```text
service
environment
Context
operation
resource type
HTTP route/method/status
database system/operation name
messaging system/destination/operation
error type/code
```

MUST NOT attach full payload hoặc sensitive fields.

---

# 93. Trace status

Span should be error khi operation thật sự fail.

Expected validation/authorization errors không nhất thiết được coi là internal system error; classification phải đúng.

---

# 94. Sampling

Sampling policy MUST:

- Preserve error/critical-flow visibility.
- Control cost.
- Respect privacy.
- Avoid bias that breaks diagnostics.
- Not affect SLI metrics.
- Be documented.

Exact sampling rates thuộc environment/configuration.

---

# 95. Tail-based sampling

Tail-based sampling MAY được dùng nếu platform hỗ trợ và operational complexity được chấp nhận.

Potential retained traces:

- Errors.
- High latency.
- Critical financial flows.
- Security anomalies.
- Rare operations.

---

# 96. Database tracing

Database spans SHOULD use:

- Normalized operation/query name.
- Database system.
- Duration.
- Rows where safe.
- Error category.

MUST NOT attach full SQL literals/parameters.

---

# 97. Messaging tracing

Trace context SHOULD propagate qua Event headers/envelope theo Event Standards.

Asynchronous relationship MAY dùng parent/child hoặc span links tùy semantics.

Exact propagation fields thuộc shared Event contract.

---

# 98. Provider tracing

External spans SHOULD capture safe metadata:

```text
provider
operation
timeout class
retry attempt
status class
safe provider request reference
```

MUST NOT log token, signed URL hoặc raw endpoint query secret.

---

# 99. Frontend tracing

Frontend MAY correlate:

- Page load.
- Route transition.
- User action.
- API call.
- Error.

MUST NOT capture keystrokes, form values hoặc sensitive DOM text.

---

# 100. Health endpoints

Conceptual minimum:

```text
/health/live
/health/ready
```

Exact paths thuộc OpenAPI/deployment.

## Liveness

Process/event loop có đang hoạt động.

## Readiness

Service có thể nhận traffic an toàn.

---

# 101. Health-check principles

Health checks MUST:

- Be bounded.
- Be cheap.
- Avoid cascading overload.
- Avoid leaking internal details.
- Have clear semantics.
- Not depend on every optional dependency.

---

# 102. Degraded state

System MAY distinguish:

```text
HEALTHY
DEGRADED
UNHEALTHY
```

Ví dụ projection lag có thể làm feature degraded nhưng API core vẫn ready.

Exact degradation policy thuộc Context/SLO design.

---

# 103. Dependency health

Dependency health SHOULD prefer:

- Passive metrics.
- Cached status.
- Lightweight checks.
- Circuit state.

Không gọi expensive external provider liên tục chỉ để health check.

---

# 104. Synthetic monitoring

Synthetic checks MAY cover:

- DNS/TLS.
- Frontend shell.
- API readiness.
- Authentication.
- Safe read.
- Safe draft write.
- Object access.
- Critical journey subset.

MUST NOT tạo legal/financial evidence thật.

---

# 105. Deployment annotations

Mỗi deployment SHOULD annotate observability system với:

```text
release version
commit
environment
migration revision
start/end
pipeline/operator reference
```

---

# 106. Incident annotations

Dashboards SHOULD annotate:

- Incident start.
- Mitigation.
- Recovery.
- Postmortem reference.

---

# 107. Error reporting

Unexpected exceptions SHOULD:

- Capture protected stack trace.
- Attach release/environment.
- Attach correlation/trace.
- Group by stable fingerprint.
- Redact sensitive data.
- Assign owner.

Expected business errors không nên làm crash tracker noisy.

---

# 108. Error fingerprinting

Fingerprint SHOULD dựa:

```text
exception type
normalized stack
operation
stable error code
```

Không dựa full dynamic message.

---

# 109. Frontend error capture

Capture MAY gồm:

- Unhandled errors.
- Promise rejections.
- Route error boundaries.
- Unexpected API errors.
- Build version.
- Browser metadata.

MUST NOT capture form values, tokens hoặc DOM content nhạy cảm.

---

# 110. Source maps

Production source maps MAY được upload riêng vào approved error platform.

Should:

- Match release.
- Be access-controlled.
- Not be publicly served nếu policy cấm.
- Not contain secrets/source artifacts beyond approved scope.

---

# 111. Business anomaly detection

Examples:

- Allocation vượt payment amount.
- Receipt không có eligible allocation.
- Active Commercial Lock overlap.
- Customer redirect cycle.
- Number counter thấp hơn issued maximum.
- Audit gap.
- Document metadata thiếu object.
- Required Outbox Event missing.
- Provider state ahead of local state.

Anomaly detection phải có owner và repair path.

---

# 112. Reconciliation telemetry

Mỗi reconciliation run SHOULD log:

```text
run ID
type
scope
started/completed
items scanned
findings
repaired
manual review
failed
duration
```

Run ID không dùng làm metric label.

---

# 113. Privacy telemetry

Monitor when relevant:

- Sensitive export.
- Sensitive reveal.
- Retention purge failures.
- Legal hold conflicts.
- Consent/suppression violations.
- Non-production access to production-derived data.
- Unauthorized file/download attempts.

---

# 114. Backup and restore telemetry

Required signal classes:

- Backup success/failure.
- Backup age.
- WAL lag.
- Object replication lag.
- Verification result.
- Restore drill result.
- Measured RPO/RTO.
- Key/access failure.

Exact metrics/thresholds thuộc backup runbook/SLO.

---

# 115. Retention principles

Telemetry retention MUST balance:

- Incident investigation.
- Security.
- Privacy.
- SLO reporting.
- Cost.
- Legal requirements.
- Data minimization.

Exact retention belongs Telemetry Retention/Privacy Policy.

---

# 116. Access control

Production telemetry MUST be access controlled.

Consider separate access for:

- General operations.
- Security.
- Finance-sensitive diagnostics.
- Audit.
- Executives.
- Support.

No public share links for restricted telemetry.

---

# 117. Telemetry encryption

Telemetry SHOULD be protected:

- In transit.
- At rest.
- In backups/exports.
- During cross-region transfer.

Exact key/provider controls belong Security Architecture.

---

# 118. Data residency

Telemetry platform selection MUST consider data residency and provider processing where applicable.

Exact regions belong Environment/Security Architecture.

---

# 119. Cost governance

Cost controls MAY include:

- Sampling.
- Retention tiers.
- Cardinality budgets.
- Log-level control.
- Aggregation.
- Dropping noisy fields.
- Archive tiers.
- Query/dashboard optimization.

MUST NOT giảm critical security/integrity visibility không review.

---

# 120. Telemetry volume review

New feature SHOULD estimate:

- Log rate.
- Metric series.
- Trace volume.
- Payload/attribute size.
- Retention.
- Expected cost.
- Peak behavior.

Exact budget thuộc Capacity Model.

---

# 121. Observability bootstrap

Ngay từ foundation Sprint SHOULD có:

- Structured logging.
- Request/correlation middleware.
- Basic HTTP metrics.
- Database instrumentation.
- Error reporting.
- Health endpoints.
- Service/version/environment attributes.
- Basic tracing.
- Redaction tests.

Không chờ production mới thêm.

---

# 122. Context observability contract

Mỗi Context Implementation Pack SHOULD định nghĩa:

```text
critical operations
failure modes
required logs
required metrics
trace boundaries
business anomalies
dashboards
alerts
runbooks
SLO impact
```

Exact signal names thuộc Observability Catalog.

---

# 123. Platform Context signals

Potential critical signals:

- Enterprise activation failures.
- Legal Entity activation failures.
- Calendar validation/publish failures.
- Number issuance latency/conflicts.
- Sequence integrity anomalies.
- Configuration resolution failures.

---

# 124. IAM Context signals

Potential signals:

- Authentication failures.
- Authorization denials.
- Scope resolution failures/latency.
- Role/permission changes.
- Delegation expiry.
- Break-glass.
- Access review overdue.

---

# 125. Party Context signals

Potential signals:

- Duplicate identity candidates.
- Identity conflicts.
- Merge failures.
- Merge reconciliation.
- PII access denials.
- Redirect failures.

---

# 126. Lead Context signals

Potential signals:

- Lead intake rate.
- Duplicate candidates.
- Assignment failures.
- SLA overdue.
- Conversion failures.
- Attribution gaps.

---

# 127. Product Context signals

Potential signals:

- Listing activation failures.
- Commercial Lock conflicts.
- Lock expiry lag.
- Availability inconsistencies.
- Mandate expiry.
- Price/version publish failures.

---

# 128. Matching Context signals

Potential signals:

- Matching duration.
- Candidate counts.
- Hard exclusion rate.
- Stale input.
- Explanation failures.
- Reverse-matching denials.

---

# 129. Transaction Context signals

Potential signals:

- Hold conflicts.
- Booking confirmation failures.
- Process waiting/failed.
- Commercial snapshot issues.
- State conflicts.

---

# 130. Contract Context signals

Potential signals:

- Contract generation failures.
- Signature-provider failures.
- Payment duplicates.
- Allocation conflicts.
- Receipt issuance failures.
- Refund failures.
- Financial reconciliation findings.

---

# 131. Revenue Context signals

Potential signals:

- Entitlement lag.
- Recognition failures.
- Collection mismatch.
- Commission vesting failures.
- Payout conflicts.
- Clawback anomalies.

---

# 132. Activity Context signals

Potential signals:

- Task overdue.
- Appointment conflicts.
- Timeline lag.
- Notification failures.
- SLA escalation backlog.

---

# 133. Marketing Context signals

Potential signals:

- Form rejection.
- Spam rate.
- Journey enrollment.
- Suppression violations.
- Campaign delivery failures.
- Attribution gaps.

---

# 134. Analytics Context signals

Potential signals:

- Dataset freshness.
- Metric computation failures.
- Snapshot/rebuild failures.
- Reconciliation mismatch.
- Dashboard query latency.
- Drill-down inconsistency.

---

# 135. Documents Context signals

Potential signals:

- Upload failures.
- Scan backlog.
- Quarantine.
- Missing objects.
- Hash mismatch.
- OCR failures.
- Dossier readiness gaps.
- Signature evidence missing.

---

# 136. Audit Context signals

Potential signals:

- Audit write failures.
- Seal/integrity failures.
- Unauthorized access.
- Retention job failures.
- Query latency.

Audit integrity failure SHOULD be treated as critical.

---

# 137. Integration Context signals

Potential signals:

- Webhook signature failures.
- Provider rate limits.
- Mapping failures.
- Cursor lag.
- Duplicate provider events.
- DLQ backlog.
- Reconciliation findings.

---

# 138. Operations Context signals

Potential signals:

- Job failures.
- Release health.
- Backup age.
- Restore drill.
- Capacity threshold.
- Incident response.
- Configuration drift.

---

# 139. Release observability gate

Before release, relevant changes SHOULD have:

- Structured logs.
- Metrics.
- Traces when useful.
- Correlation propagation.
- Redaction.
- Dashboard updates.
- Alert updates.
- Runbook links.
- Baseline comparison.
- Test evidence.

---

# 140. Post-release verification

After deployment, verify:

- Error rate.
- Latency.
- Database health.
- Queue lag.
- Job failures.
- Frontend errors.
- Security denials.
- Business anomalies.
- SLO burn.
- Telemetry pipeline health.

---

# 141. Rollback signals

Rollback MAY be considered when:

- Error-budget burn severe.
- Latency regression severe.
- Data-integrity anomaly.
- Audit failure.
- Critical consumer permanent failures.
- Security regression.
- Migration errors.

Exact thresholds belong Release Strategy/SLO.

---

# 142. Incident diagnostics questions

Observability SHOULD giúp trả lời:

```text
What is broken?
Who or what scope is affected?
When did it start?
What changed?
Is data integrity at risk?
Is security at risk?
Is the issue growing?
What is the next safe action?
Which runbook applies?
```

---

# 143. Incident timeline

Incident evidence SHOULD ghi:

- Alert time.
- Acknowledgement.
- Detection source.
- Diagnosis.
- Mitigation.
- Recovery.
- Verification.
- Deploy/config annotations.
- Follow-up.

---

# 144. Postmortem inputs

Postmortem MAY dùng:

- Logs.
- Metrics.
- Traces.
- Audit.
- Deploy annotations.
- Incident actions.
- Change records.
- Runbook outputs.

Telemetry gốc không được chỉnh sửa để phù hợp narrative.

---

# 145. Clock synchronization

All services/nodes MUST có time synchronization phù hợp.

Clock skew phá:

- Trace ordering.
- Audit.
- Event ordering.
- JWT/webhook verification.
- Incident timeline.
- SLO windows.

Clock skew SHOULD được monitored.

---

# 146. Telemetry integrity

Critical telemetry platform SHOULD có:

- Access control.
- Change audit.
- Retention enforcement.
- Configuration backup/export.
- Time synchronization.
- Tamper resistance where required.
- Collector health.
- Ingestion-loss monitoring.

---

# 147. Telemetry failure behavior

Application business operation SHOULD NOT fail chỉ vì optional telemetry exporter unavailable.

Exceptions:

- Required Audit is not optional telemetry.
- Security/integrity evidence may have fail-closed policy.
- Telemetry buffer must be bounded.
- Exporter failure must be observable when feasible.

---

# 148. Logging tests

Tests SHOULD verify:

- Structured schema.
- Required fields.
- Correct level/event name.
- Correlation.
- Error code.
- No secrets.
- No PII.
- No full payload.
- Valid serialization.

---

# 149. Redaction tests

Inject safe test values for:

```text
password
authorization header
phone
email
identity number
bank account
signed URL
```

Assert raw values không xuất hiện.

---

# 150. Metrics tests

Tests SHOULD verify:

- Metric registration.
- Correct type.
- Correct increment/update.
- Unit.
- Label allowlist.
- No high-cardinality values.
- Success/failure paths.

---

# 151. Cardinality tests

Static/runtime checks SHOULD phát hiện:

- UUID label.
- Raw path.
- Error-message label.
- Search-term label.
- Actor/customer label.
- SQL text label.
- File-name label.

---

# 152. Trace tests

Tests SHOULD verify:

- Trace propagation HTTP → application → DB.
- Correlation into Outbox/Event.
- Consumer spans.
- Provider spans.
- Error status.
- No sensitive attributes.
- Sampling configuration behavior where testable.

---

# 153. Alert tests

Critical alert tests SHOULD verify:

- Trigger.
- Routing.
- Severity.
- Runbook link.
- Recovery.
- Dedup.
- Maintenance suppression.
- No PII.

---

# 154. Dashboard tests

Dashboard validation SHOULD check:

- Query syntax.
- Units.
- Environment filters.
- Time range.
- Variable cardinality.
- Runbook links.
- Access classification.
- Panel semantics.

---

# 155. Failure-injection observability tests

Inject when relevant:

- Database unavailable.
- Broker unavailable.
- Provider timeout.
- Object missing.
- Audit failure.
- Outbox backlog.
- Consumer crash.
- Backup failure.
- Scope resolver failure.

Verify logs, metrics, traces, alerts và runbook routing.

---

# 156. Performance overhead tests

Measure observability overhead:

- CPU.
- Memory.
- Latency.
- Network.
- Storage.
- Cardinality.
- Collector backpressure.

Exact acceptable overhead thuộc NFR/Capacity Model.

---

# 157. Telemetry contract evolution

Metric names, structured-log fields và trace conventions là contracts.

Breaking changes need:

- Consumer/dashboard inventory.
- Migration period.
- Compatibility.
- Deprecation.
- Changelog.
- Tests.

---

# 158. Deprecation

Deprecated signal MUST have:

- Replacement.
- Consumer inventory.
- Sunset.
- Dashboard/alert migration.
- Owner.

Không remove metric/log field âm thầm.

---

# 159. Shared libraries

Application SHOULD dùng shared observability abstractions:

- Logger.
- Metrics registry/helpers.
- Trace helpers.
- Correlation middleware.
- Redaction.
- Error normalization.

Domain MUST NOT import telemetry vendor SDK.

---

# 160. Configuration

Typed configuration MAY include:

```text
log level
log format
metrics enabled
tracing enabled
sampling strategy
telemetry endpoint
service identity
environment
```

Exact environment variable names thuộc configuration catalog.

Secrets MUST NOT được log.

---

# 161. Local development

Local environment MAY dùng:

- Human-readable logs.
- Optional local collector.
- Reduced sampling.
- Simplified dashboards.

Nhưng redaction và correlation SHOULD vẫn active.

---

# 162. CI observability

CI SHOULD produce safe evidence:

- Test results.
- Durations.
- Flaky signals.
- Coverage.
- Build metrics.
- Migration results.
- Security scans.

CI logs MUST not contain secrets.

---

# 163. Staging observability

Staging SHOULD gần production về:

- Log schema.
- Metric names.
- Trace propagation.
- Dashboards.
- Alert tests.
- Synthetic traffic.

Retention/capacity có thể khác.

---

# 164. Production observability

Production requires:

- Durable telemetry backend.
- Access control.
- Alerting/on-call.
- Retention.
- Cost monitoring.
- Config backup/export.
- Incident integration.
- Ingestion-health monitoring.

---

# 165. Support diagnostics

Support-facing UI MAY expose safe references:

- Correlation ID.
- Request ID.
- Error code.
- Release version.
- Safe resource reference.

MUST NOT expose stack trace, topology hoặc secrets.

---

# 166. Observability documentation set

Recommended companion docs:

```text
docs/engineering/observability-standards.md
docs/operations/service-level-objectives.md
docs/operations/observability-catalog.md
docs/operations/dashboard-catalog.md
docs/operations/alert-catalog.md
docs/operations/telemetry-retention.md
Relevant runbooks
```

---

# 167. Observability Catalog entry

Each important signal SHOULD document:

```text
name
type
description
owner
fields/labels
unit
source
classification
dashboard
alert
retention
validation
```

---

# 168. Dashboard Catalog entry

Should include:

```text
dashboard name
purpose
audience
owner
data sources
panels
variables
access
runbooks
```

---

# 169. Alert Catalog entry

Should include:

```text
alert name
severity
condition
window
owner
route
runbook
auto-resolve
maintenance behavior
tests
```

---

# 170. Observability review checklist

## Logs

- Structured?
- Stable event name?
- Required safe context?
- Correct level?
- Redacted?
- Actionable?

## Metrics

- Clear semantics?
- Correct type/unit?
- Low cardinality?
- Owner?
- Dashboard/alert?
- Cost estimate?

## Traces

- Meaningful spans?
- Propagation?
- Safe attributes?
- Sampling?
- Cross-context links?

## Operations

- SLO impact?
- Runbook?
- Retention?
- Access?
- Failure behavior?

## Security

- Classification?
- PII/secrets?
- Export/access?
- Incident use?

---

# 171. Anti-patterns bị cấm

1. `print()` trong production.
2. Log full request/response.
3. Log token/secret.
4. Metric label là UUID/resource ID.
5. Metric label là raw URL.
6. Metric label là error message.
7. Alert không owner.
8. Alert không runbook.
9. Dashboard không environment filter.
10. ERROR cho expected validation.
11. Trace mỗi helper nhỏ.
12. Full sampling không cost/privacy review.
13. Audit thay bằng log.
14. Official KPI lấy từ operational metric chưa certified.
15. Dynamic log message làm metric label.
16. DEBUG production vô thời hạn.
17. Không deploy annotation.
18. Không correlation propagation.
19. Không consumer lag metric cho critical consumer.
20. Không backup-age signal.
21. Không redaction tests.
22. Duplicate metric names.
23. Silent telemetry exporter failure.
24. Alert threshold chưa test.
25. Dashboard chứa customer identifiers.
26. Log SQL parameters nhạy cảm.
27. Hard-code sampling/retention/threshold trong generic Standards.
28. Copy example metric/dashboard thành canonical implementation.
29. Tạo speculative telemetry cho Sprint xa không có use case.
30. Tuyên bố observable chỉ vì có logs.

---

# 172. AI Agent observability protocol

Before feature implementation, AI Agent MUST:

1. Xác định critical operations.
2. Xác định failure modes.
3. Xác định logs cần thiết.
4. Xác định metrics.
5. Xác định trace boundaries.
6. Xác định correlation/causation.
7. Xác định PII/secret risk.
8. Xác định SLI/SLO impact.
9. Xác định dashboards/alerts.
10. Xác định runbooks.
11. Viết tests.
12. Run redaction/cardinality tests.
13. Update Observability Catalog.
14. Record actual evidence.

---

# 173. AI Agent không được suy đoán exact observability implementation

Khi chưa có quyết định về:

- Metric name.
- Label set.
- Log field.
- Sampling rate.
- Retention.
- Threshold.
- Dashboard layout.
- Alert severity.
- Telemetry vendor.
- SLO target.
- Synthetic cadence.
- Cost budget.

AI Agent MUST:

1. Báo documentation gap.
2. Đề xuất options.
3. Nêu reliability, privacy, cardinality và cost trade-offs.
4. Không biến example thành canonical contract.
5. Không thêm high-cardinality telemetry để debug nhanh.
6. Chỉ triển khai exact values khi authority/evidence cho phép.
7. Cập nhật catalog/config/docs cùng code.

---

# 174. AI Agent prohibited behaviors

AI Agent MUST NOT:

1. Log payload để debug nhanh.
2. Log token/PII.
3. Dùng resource ID làm metric label.
4. Tạo alert không owner/runbook.
5. Tạo duplicate metric.
6. Import vendor SDK vào Domain.
7. Tự chọn vendor-specific API trong business code.
8. Bỏ correlation.
9. Tuyên bố observable khi chưa test.
10. Tạo fake dashboard/alert evidence.
11. Bỏ privacy/security review.
12. Dùng operational metric làm official business KPI.
13. Hard-code sampling/retention/threshold không source.
14. Bịa SLO result.
15. Bịa incident telemetry.
16. Sửa alert threshold chỉ để dashboard xanh.

---

# 175. Definition of Ready cho observability change

Observability change chỉ Ready khi:

1. Operation/failure mode rõ.
2. Signal purpose rõ.
3. Owner rõ.
4. Fields/labels rõ.
5. Cardinality đánh giá.
6. Classification rõ.
7. SLO impact rõ.
8. Dashboard/alert plan rõ.
9. Runbook rõ.
10. Test plan rõ.
11. Cost/retention impact rõ.
12. No unresolved telemetry source conflict.

---

# 176. Definition of Done cho observability change

Change chỉ Done khi relevant items hoàn thành:

1. Logs implemented.
2. Metrics implemented.
3. Traces implemented khi useful.
4. Correlation propagated.
5. Redaction pass.
6. Cardinality pass.
7. Dashboard updated.
8. Alert updated/tested.
9. Runbook linked.
10. SLI/SLO impact updated.
11. Access/retention reviewed.
12. Tests pass.
13. Catalog updated.
14. Acceptance evidence recorded.
15. No unexplained telemetry gap.

---

# 177. Numerical/configuration baselines

Các giá trị như:

```text
sampling rate
retention
alert threshold
burn-rate window
histogram buckets
scrape interval
dashboard refresh
synthetic cadence
cardinality budget
log-size limit
telemetry buffer size
```

MUST được phân loại:

- Recommended initial baseline.
- Context/SLI-specific requirement.
- Environment configuration.
- Verified production value.
- Capacity/cost budget.

Không coi con số trong example là universal mandatory truth.

---

# 178. Exception process

Ngoại lệ cần file:

```text
docs/engineering/observability-exceptions/EXC-OBS-XXX.md
```

Nội dung:

- Rule.
- Signal/component.
- Reason.
- Reliability impact.
- Security/privacy impact.
- Cardinality/cost impact.
- SLO impact.
- Mitigation.
- Owner.
- Expiry.
- Approval.

Không có ngoại lệ vô thời hạn không owner.

---

# 179. Conflict protocol

Khi phát hiện xung đột:

```text
Observability Standards
vs SLO/NFR
vs Observability Catalog
vs Context Pack
vs Code
vs Telemetry Configuration
vs Tests
```

Developer/AI MUST:

1. Dừng mở rộng thay đổi liên quan.
2. Xác định semantic hay execution conflict.
3. Áp dụng Documentation Governance.
4. Không âm thầm chọn source thuận tiện.
5. Tạo ADR/change note nếu telemetry architecture/SLO thay đổi.
6. Cập nhật catalog, configuration, code, tests và docs cùng PR.
7. Ghi resolution trong Acceptance Report.

---

# 180. Required companion artifacts

```text
docs/engineering/observability-standards.md
docs/architecture/non-functional-requirements.md
docs/operations/service-level-objectives.md
docs/operations/capacity-model.md
docs/operations/observability-catalog.md
docs/operations/dashboard-catalog.md
docs/operations/alert-catalog.md
docs/operations/telemetry-retention.md
docs/engineering/security-standards.md
docs/engineering/testing-standards.md
Relevant Context Implementation Pack
Relevant runbooks
Telemetry configuration and tests
```

---

# 181. Change Log

## Version 1.1.0 — 2026-07-26

- Làm rõ phạm vi thẩm quyền của Observability Standards.
- Phân biệt `MUST`, `SHOULD`, `BASELINE`, `EXAMPLE`, `CONTEXT-SPECIFIC`, `ENVIRONMENT-SPECIFIC`, `SLO-SPECIFIC` và `RISK-BASED`.
- Xác định SLO, NFR, Observability Catalog, Dashboard Catalog, Alert Catalog và Environment Topology là exact sources tương ứng.
- Loại bỏ cách hiểu rằng metric names, thresholds, retention, sampling rates hoặc dashboard layouts trong Standards là bắt buộc tuyệt đối.
- Làm rõ logging, metrics, tracing, correlation, anomaly detection, dashboards và alerts.
- Làm rõ privacy, cardinality, cost và telemetry-failure behavior.
- Bổ sung quy tắc chống AI suy đoán exact observability implementation.
- Bổ sung conflict protocol và cập nhật DoR/DoD.

## Version 1.0.0 — 2026-07-24

- Phiên bản baseline đầu tiên.

---

# 182. Kết luận

Observability Standards của `crm_bds_ai` phải khóa những điều không được phép sai:

```text
Structured and Safe Logs
+ Low-Cardinality Metrics
+ Correlated Traces
+ Reliable SLI/SLO Evidence
+ Actionable Alerts
+ Owned Dashboards
+ Tested Runbooks
+ Privacy and Cost Governance
```

Nhưng tài liệu không được đóng băng metric inventory, thresholds, sampling, retention, dashboards hoặc telemetry platform chưa được phân tích và kiểm chứng.

Nguyên tắc cuối cùng:

> Standards quy định telemetry phải được thiết kế và quản trị như thế nào; SLO, Catalogs và Environment Topology quy định exact operational contracts; code, telemetry configuration, tests và Acceptance Report chứng minh implementation thực tế.
