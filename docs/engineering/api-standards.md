# CRM_BDS_AI — API STANDARDS

## Quy chuẩn API bắt buộc cho toàn bộ hệ thống `crm_bds_ai`

**Document ID:** `ENG-API-001`  
**Canonical path:** `docs/engineering/api-standards.md`  
**Product:** `crm_bds_ai`  
**Version:** `1.0.0`  
**Status:** `Accepted / Mandatory`  
**Canonical:** `Yes` đối với tiêu chuẩn thiết kế, triển khai và kiểm thử API  
**Owner:** `API Architecture Owner`  
**Reviewers:** `Architecture Owner`, `Technical Owner`, `Security Owner`, `Frontend Owner`, `Context Owners`, `QA Owner`, `Operations Owner`  
**Effective date:** `2026-08-05`  
**Last reviewed:** `2026-08-05`  
**Next review:** Khi API architecture, OpenAPI, authentication, authorization, versioning hoặc client-generation strategy thay đổi  
**Supersedes:** `None — Greenfield baseline`  
**Superseded by:** Không

---

# 1. Mục đích

Tài liệu này quy định cách thiết kế, đặt tên, triển khai, bảo vệ, version, document và kiểm thử mọi API trong `crm_bds_ai`.

Mục tiêu:

1. Bảo đảm mọi Context cung cấp API nhất quán.
2. Ngăn API trở thành generic CRUD làm mất domain intent.
3. Bảo đảm authorization, scope và field masking được enforce ở backend.
4. Bảo đảm commands idempotent và concurrency-safe.
5. Bảo đảm errors có stable codes.
6. Bảo đảm OpenAPI là contract máy đọc được.
7. Bảo đảm frontend client được generate nhất quán.
8. Bảo đảm internal/public/webhook APIs có boundary rõ.
9. Bảo đảm API có thể vận hành, monitor và deprecate an toàn.
10. Bảo đảm AI Agent không tự thiết kế endpoint theo thói quen cá nhân.

Tài liệu này phải được đọc cùng:

```text
docs/engineering/coding-standards.md
docs/engineering/database-standards.md
docs/engineering/event-standards.md
docs/engineering/security-standards.md
docs/engineering/testing-standards.md
docs/architecture/source-of-truth-matrix.md
Relevant Context Implementation Pack
Current Sprint Execution Pack
```

---

# 2. Nguyên tắc tối cao

```text
Domain Intent
> Security
> Correctness
> Idempotency
> Concurrency Safety
> Contract Stability
> Observability
> Client Convenience
```

API không được tối ưu cho frontend convenience nếu làm mất business meaning hoặc security boundary.

---

# 3. Phân loại API

Hệ thống có bốn lớp API:

```text
/api/v1
/internal/v1
/public/v1
/webhooks/v1
```

## 3.1. `/api/v1`

Dành cho authenticated first-party applications:

- Web admin.
- Internal staff UI.
- Approved first-party clients.

## 3.2. `/internal/v1`

Dành cho service-to-service hoặc Context-to-Context internal calls:

- Business Calendar calculation.
- Number issuance.
- Internal lookup.
- Configuration resolution.
- Reconciliation support.

Không expose public ingress mặc định.

## 3.3. `/public/v1`

Dành cho public/client-facing endpoints:

- Public form submission.
- Public catalog subset nếu sản phẩm hỗ trợ.
- Customer-facing workflow trong tương lai.

Public API cần rate limit, abuse prevention và privacy review riêng.

## 3.4. `/webhooks/v1`

Dành cho inbound provider callbacks:

- Signature provider.
- Payment provider.
- Marketing provider.
- Notification provider.
- OCR provider.

Phải có signature verification, replay protection và idempotency.

---

# 4. REST và domain intent

## 4.1. Resource-oriented URLs

Đúng:

```text
GET /api/v1/customers/{customer_id}
POST /api/v1/bookings/{booking_id}/confirm
POST /api/v1/contracts/{contract_id}/activate
```

Sai:

```text
POST /api/v1/doConfirmBooking
POST /api/v1/updateContractStatus
GET /api/v1/getCustomerById
```

## 4.2. Commands không phải CRUD

State transition phải dùng action endpoint:

```text
POST /bookings/{id}/submit
POST /bookings/{id}/approve
POST /bookings/{id}/confirm
POST /bookings/{id}/cancel
```

Không dùng:

```text
PATCH /bookings/{id}
{"status":"CONFIRMED"}
```

## 4.3. Resource plural và kebab-case

```text
customers
legal-entities
business-calendars
payment-allocations
```

---

# 5. Quy ước endpoint

## 5.1. Collection

```text
POST /resources
GET  /resources
```

## 5.2. Item

```text
GET   /resources/{resource_id}
PATCH /resources/{resource_id}
```

PATCH chỉ cho mutable profile fields, không cho business state.

## 5.3. Child resources

```text
POST /contracts/{contract_id}/versions
GET  /contracts/{contract_id}/versions
GET  /contract-versions/{version_id}
```

## 5.4. Actions

```text
POST /contracts/{contract_id}/activate
POST /receipts/{receipt_id}/cancel
POST /customer-merge-cases/{case_id}/execute
```

## 5.5. Preview và validation

```text
POST /numbering-scheme-versions/{id}/preview
POST /contract-cancellations/{id}/impact-preview
POST /business-calendar-versions/{id}/validate
```

Preview không tạo durable business state trừ khi contract mô tả rõ diagnostic record.

---

# 6. HTTP methods

## GET

- Read-only.
- Safe.
- Idempotent.
- Không thay state.
- Có thể ghi sensitive-access audit nếu policy yêu cầu.

## POST

- Create resource.
- Execute command.
- Start process/job.
- Có `Idempotency-Key` khi side effect critical.

## PATCH

- Partial update mutable profile fields.
- Không generic state update.
- Không dùng cho immutable version.

## PUT

Chỉ dùng khi replace complete sub-resource và idempotent semantics rõ.

Ví dụ:

```text
PUT /business-calendar-versions/{id}/weekly-pattern
```

## DELETE

Chỉ dùng khi actual deletion hợp lệ, chẳng hạn draft child hoặc temporary upload.

Không dùng DELETE để biểu diễn cancel/archive financial evidence.

---

# 7. HTTP status codes

| Status | Ý nghĩa chuẩn |
|---:|---|
| 200 | Query hoặc command synchronous thành công |
| 201 | Resource được tạo |
| 202 | Async process/job đã được chấp nhận |
| 204 | Thành công không có body |
| 400 | Malformed request hoặc query syntax invalid |
| 401 | Thiếu hoặc sai authentication |
| 403 | Thiếu capability và policy không conceal existence |
| 404 | Không tồn tại hoặc ngoài scope theo concealment policy |
| 409 | Business conflict hoặc idempotency conflict |
| 412 | `If-Match` mismatch |
| 415 | Unsupported media type |
| 422 | Field/domain input validation theo project standard |
| 429 | Rate limit |
| 500 | Unexpected internal error |
| 502 | Upstream invalid response |
| 503 | Dependency tạm unavailable |
| 504 | Upstream timeout |

Không trả HTTP 200 cho business failure.

---

# 8. Response envelope

## 8.1. Single resource

```json
{
  "data": {
    "id": "uuid",
    "status": "ACTIVE"
  },
  "meta": {
    "request_id": "uuid",
    "correlation_id": "uuid"
  }
}
```

## 8.2. Collection

```json
{
  "data": [],
  "meta": {
    "request_id": "uuid",
    "correlation_id": "uuid",
    "page": {
      "next_cursor": "opaque",
      "has_more": true,
      "page_size": 50
    }
  }
}
```

## 8.3. Async job

```json
{
  "data": {
    "job_id": "uuid",
    "status": "QUEUED",
    "status_url": "/api/v1/jobs/uuid"
  },
  "meta": {
    "request_id": "uuid",
    "correlation_id": "uuid"
  }
}
```

Không thêm `success: true`; HTTP status đã thể hiện kết quả.

---

# 9. Problem Details và stable errors

Errors phải theo RFC 9457-style Problem Details hoặc chuẩn tương thích đã khóa.

```json
{
  "type": "https://errors.example/invalid-state-transition",
  "title": "Invalid state transition",
  "status": 409,
  "detail": "The booking cannot be confirmed from its current state.",
  "instance": "/api/v1/bookings/uuid/confirm",
  "error_code": "BOOKING_INVALID_STATE_TRANSITION",
  "correlation_id": "uuid",
  "field_errors": []
}
```

Fields bắt buộc:

```text
type
title
status
detail
instance
error_code
correlation_id
```

Field errors:

```json
{
  "field_errors": [
    {
      "field": "base_currency",
      "code": "INVALID_CURRENCY",
      "message": "Currency code is invalid."
    }
  ]
}
```

Không expose:

- SQL.
- Stack trace.
- Constraint name thô.
- Internal hostname.
- Token.
- PII.
- Full upstream response.

Error code phải stable, uppercase snake case, có registry entry, HTTP status, retryability, audit và alert classification.

---

# 10. Request và response schemas

## 10.1. Request schema

- `additionalProperties: false` hoặc equivalent.
- Length/range/format rõ.
- Examples.
- Nullable semantics rõ.
- Không chấp nhận system fields.

Client không được gửi:

```text
created_at
created_by
updated_at
updated_by
row_version
audit metadata
authorized scope
calculated status
official metrics
```

trừ khi contract explicit.

## 10.2. Response schema

- Không reuse ORM.
- Không reuse request schema mù quáng.
- Không expose persistence-only fields.
- Có masking/omission semantics.
- Có version/ETag khi cần.
- Không expose secret/provider credential reference nếu không cần.

---

# 11. Identifiers và formats

- Resource ID dùng UUID canonical.
- Path parameter dùng semantic name như `customer_id`, `listing_id`.
- Business number không thay technical ID.
- Date: `YYYY-MM-DD`.
- Instant: RFC3339 UTC.
- Timezone: IANA ID.
- Money nên truyền amount dạng string cùng currency.
- Enum dùng stable uppercase codes.

Ví dụ money:

```json
{
  "amount": "1234567.8900",
  "currency": "VND"
}
```

---

# 12. API versioning và deprecation

## 12.1. Major version

```text
/api/v1
```

## 12.2. Non-breaking

- Thêm optional response field.
- Thêm optional request field với safe default.
- Thêm endpoint.

## 12.3. Breaking

- Remove/rename field.
- Change meaning.
- Change requiredness.
- Change enum semantics.
- Change auth/pagination behavior.

Breaking change cần major version hoặc compatibility strategy được phê duyệt.

Deprecated endpoint/field phải có:

- OpenAPI deprecated metadata.
- Sunset date.
- Replacement.
- Usage metrics.
- Removal release.

---

# 13. OpenAPI 3.1

Canonical contract:

```text
contracts/openapi/openapi.json
```

Requirements:

- OpenAPI 3.1 valid.
- Deterministic generation.
- Unique operation IDs.
- Stable component names.
- Examples validate.
- Error responses declared.
- Security schemes declared.
- Không endpoint undocumented.
- Generated file có `DO NOT EDIT MANUALLY`.

Operation IDs:

```text
createEnterprise
getEnterprise
listLegalEntities
activateListing
issueReceipt
```

Tags theo Context/resource, không dùng `General`, `Misc`, `CRUD`.

---

# 14. Authentication

## 14.1. User API

OIDC/JWT Bearer. Validate:

- Signature.
- Issuer.
- Audience.
- Expiry.
- Not-before.
- Key rotation.
- Token type.

## 14.2. Internal API

Service authentication qua mTLS, service token hoặc workload identity được phê duyệt.

Không reuse user token tùy tiện cho service-to-service.

## 14.3. Public API

- Rate limit.
- Abuse prevention.
- Consent.
- Minimal exposure.

## 14.4. Webhooks

Provider-specific verification.

---

# 15. Authorization, scope và masking

Mỗi endpoint phải khai báo:

- Permission code.
- Allowed scopes.
- Resource access rule.
- Field masking rule.
- SoD/approval requirement nếu có.

Authorization enforce ở backend trước data exposure và command execution.

List/detail query phải inject `EffectiveScope` vào SQL.

Không:

```python
rows = list_all()
rows = filter_allowed(rows)
```

Ngoài scope có thể trả 404 theo concealment policy.

Field masking phải do backend thực hiện:

- Omit.
- Mask.
- Redact.
- Aggregate.

Không trả full field rồi yêu cầu frontend che.

---

# 16. ETag và optimistic concurrency

Mutable resource response phải có:

```text
ETag: "7"
```

Update/transition yêu cầu:

```text
If-Match: "7"
```

Mismatch:

```text
412 Precondition Failed
```

Không dùng `updated_at` làm concurrency token.

---

# 17. Idempotency-Key

Critical POST commands phải hỗ trợ:

```text
Idempotency-Key
```

Áp dụng cho:

- Create critical resource.
- Booking confirm.
- Contract activate.
- Payment intake/allocation.
- Receipt issue.
- Refund execute.
- Number issue.
- Payout confirm.
- Webhook processing.

Semantics:

- Same key + same request → replay.
- Same key + different request → 409.
- In progress → conflict + `Retry-After` theo standard.
- Stale owner → controlled takeover.
- Scope gồm actor, operation và Enterprise.

Không lưu sensitive response tùy tiện.

---

# 18. Request ID và Correlation ID

Headers:

```text
X-Request-ID
X-Correlation-ID
```

Server phải:

- Validate hoặc generate.
- Return cho client.
- Propagate tới logs, events, jobs và provider calls.

Client-provided correlation ID không phải security input.

---

# 19. Pagination

Cursor pagination là chuẩn mặc định.

Query params:

```text
page_size
cursor
```

Response page metadata:

```json
{
  "next_cursor": "opaque",
  "has_more": true,
  "page_size": 50
}
```

Requirements:

- Default và max page size.
- Stable sort.
- ID tie-breaker.
- Cursor opaque.
- Filter/sort/scope hash.
- Không chứa sensitive plaintext.

Offset pagination chỉ cho small reference data hoặc endpoint được phê duyệt.

---

# 20. Filtering, sorting và search

## Filtering

Mỗi endpoint có allowlist.

Ví dụ:

```text
status
enterprise_id
legal_entity_id
created_from
created_to
effective_on
search
```

Không hỗ trợ arbitrary SQL-like filter language mặc định.

## Sorting

Allowed fields explicit, stable tie-breaker ID.

## Search

- Length limit.
- Normalization.
- Scope-aware.
- PII-safe.
- No wildcard injection.
- Relevance behavior documented.

---

# 21. PATCH và null semantics

PATCH chỉ dùng cho mutable profile fields.

Semantics:

- Omitted = unchanged.
- `null` = clear nếu allowed.
- Empty string không tự động null trừ normalization policy.

Reject immutable/system fields.

Không hỗ trợ arbitrary JSON Patch mặc định.

---

# 22. Resource creation và lifecycle actions

Create request không cho client set ID trừ import/integration contract đặc biệt.

Server phải:

- Generate UUIDv7.
- Set actor/timestamps.
- Set initial state.
- Audit.
- Outbox.
- Idempotency.

DELETE chỉ actual deletion. Business lifecycle dùng:

```text
/archive
/cancel
/retire
/revoke
/close
```

Không DELETE Contract, Receipt, Payment hoặc financial evidence.

---

# 23. Bulk, async process và jobs

Bulk operation lớn phải async:

```text
POST /api/v1/import-jobs
POST /api/v1/export-jobs
GET  /api/v1/jobs/{job_id}
```

Response `202`.

Phải có:

- Batch/job ID.
- Progress.
- Per-item result.
- Partial failure.
- Retry.
- Cancel policy.
- Audit.
- Idempotency.

Long-running business process:

```text
POST /resource/{id}/action
→ 202 + process_id
GET /processes/{process_id}
```

Không trả fake completed trước completion.

---

# 24. Export APIs

Export phải:

- Có permission riêng.
- Reauthorize scope.
- Apply masking.
- Async.
- Generate expiring file.
- Audit.
- Rate limit.
- Lưu filter snapshot.
- Lưu metric version nếu analytics.
- Không expose raw storage key.

---

# 25. File upload và download

Upload pattern:

```text
POST /api/v1/file-uploads/intents
PUT  <presigned URL>
POST /api/v1/file-uploads/{id}/complete
```

Requirements:

- Size.
- MIME.
- Hash.
- Scan.
- Quarantine.
- Classification.

Download:

- Reauthorize mỗi request.
- Short-lived signed URL.
- Audit sensitive download.
- No permanent public URL.
- Safe filename.

---

# 26. Internal APIs

Internal API không đồng nghĩa “không cần security”.

Phải có:

- Service identity.
- Permission/capability.
- Scope.
- Timeout.
- Idempotency khi side effect.
- Versioning.
- Audit nếu sensitive.
- OpenAPI riêng hoặc tagged.

Không expose public ingress mặc định.

---

# 27. Public APIs

Public APIs phải:

- Minimal data.
- Strict validation.
- Rate limiting.
- Abuse/spam protection.
- Consent.
- Privacy.
- No enumeration.
- No unrestricted search.
- Strong observability.

---

# 28. Webhook APIs

Inbound webhook flow:

1. Receive raw body.
2. Verify timestamp/signature.
3. Replay protection.
4. Deduplicate provider event ID.
5. Persist durable receipt/raw reference.
6. Return quickly.
7. Process async.
8. Reconcile.
9. Audit/metrics.

Không trust provider payload nếu chưa mapping/validation.

---

# 29. Rate limiting và request limits

Rate limit theo endpoint class:

- Public forms.
- Search.
- Export.
- Webhooks.
- File upload intents.
- Expensive analytics.

Rate key có thể gồm:

- IP.
- Actor.
- Service.
- Enterprise.
- Endpoint.

Không dựa chỉ vào IP.

Oversized request phải bị reject sớm.

---

# 30. Caching và conditional requests

Authenticated business data mặc định:

```text
Cache-Control: no-store
```

hoặc private short caching theo policy.

Public/reference data có thể dùng:

- ETag.
- Cache-Control.
- Last-Modified.
- `If-None-Match` / 304.

Không cache permission-sensitive unmasked response trong shared cache.

---

# 31. CORS, CSRF và headers

CORS:

- Approved origins only.
- No wildcard với credentials.
- Environment-specific.

Nếu dùng cookie auth, CSRF protection bắt buộc.

Security headers theo gateway/frontend standard.

Không expose server version không cần thiết.

---

# 32. PII trong API

API chỉ expose minimum necessary.

Tránh PII trong:

- URL.
- Query params.
- Error detail.
- Logs.
- Correlation metadata.
- Cursor.
- Public links.

Sensitive search có thể dùng body-based endpoint nếu URL logging risk và design đã được phê duyệt.

---

# 33. Audit, logging, metrics và tracing

## Audit

Commands, approvals, financial actions, exports/downloads và sensitive access phải audit theo policy.

## Logging

Log:

- Method.
- Route template.
- Status.
- Duration.
- Request/correlation ID.
- Actor reference.
- Enterprise/Legal Entity.
- Error code.

Không log full body, Authorization, cookies, PII, file content hoặc signed URL.

## Metrics

```text
requests_total
request_duration_seconds
request_errors_total
rate_limit_rejections_total
idempotency_replays_total
optimistic_conflicts_total
authorization_denials_total
```

Labels low-cardinality.

## Tracing

Trace API, application command, DB, Outbox, Consumer và provider calls; không attach raw bodies.

---

# 34. Timeout và retry guidance

- API timeout theo NFR/Operations.
- Provider timeout ngắn hơn request timeout.
- Long operations chuyển async.
- Không chờ vô hạn.

Retryable response có thể có:

```text
Retry-After
```

Client không retry non-idempotent POST nếu thiếu Idempotency-Key.

Không retry validation, permission hoặc business conflict.

---

# 35. Composition, dashboard và search APIs

Composition endpoint được phép khi:

- Có owner rõ.
- Chỉ là read model.
- Không tạo source of truth mới.
- Enforce permission.
- Không hidden cross-context write.

Dashboard API phải trả:

- Metric code/version.
- Value.
- Unit/currency.
- Filters.
- Freshness.
- Scope.
- Comparison period.
- Drill context.

Frontend không tự tính official KPI.

Search result phải được reauthorize và mask.

---

# 36. Health và diagnostics APIs

Public health:

```text
/health/live
/health/ready
```

Detailed diagnostics tách riêng và protected.

Không trả secret, credential, internal topology chi tiết ra public.

---

# 37. API documentation và examples

Mỗi endpoint phải document:

- Purpose.
- Permission.
- Scope.
- Request.
- Response.
- Errors.
- Idempotency.
- Concurrency.
- Audit.
- Events.
- Examples.

Examples phải validate, dùng fake data và không có PII thật.

---

# 38. Generated clients

Frontend/client generation từ OpenAPI.

Rules:

- Deterministic.
- Không manual edit.
- Không duplicate handwritten API types.
- Breaking diff detection.
- Client wrapper xử lý auth, correlation, Problem Details, ETag, Idempotency, timeout và telemetry.

---

# 39. API testing standards

## Contract tests

- OpenAPI valid.
- Operation IDs unique.
- Không endpoint undocumented.
- Schemas match implementation.
- Errors declared.
- Security declared.
- Examples validate.
- Generated client clean.
- No breaking change without approval.

## Command endpoint tests

1. Success.
2. No auth.
3. No permission.
4. Out-of-scope.
5. Validation error.
6. Invalid state.
7. Idempotency replay.
8. Idempotency conflict.
9. If-Match conflict.
10. Audit.
11. Outbox.
12. Transaction rollback.

## List endpoint tests

1. Scope.
2. Pagination.
3. Stable sorting.
4. Filters.
5. Masking.
6. Empty.
7. Cursor invalid/tampered.
8. Max page size.

---

# 40. Security testing

Phải test:

- BOLA/IDOR.
- Scope escalation.
- Mass assignment.
- Hidden field exposure.
- Enumeration.
- Rate limit.
- Webhook replay.
- Invalid signature.
- CORS.
- CSRF nếu applicable.
- Export/download reauthorization.
- Internal endpoint public access denial.

---

# 41. Load và failure-injection testing

Critical APIs:

- Lead intake.
- Customer duplicate check.
- Listing search.
- Commercial Lock.
- Number issuance.
- Payment allocation.
- Dashboard.
- Public form submission.
- Webhooks.

Measure:

- p50/p95/p99.
- Error rate.
- Lock wait.
- DB load.
- Queue lag.

Failure injection:

- DB unavailable.
- Lost response after commit.
- Audit/Outbox failure.
- Provider timeout.
- Worker delay.
- Cache unavailable.
- Idempotency conflict.
- Partial process failure.

---

# 42. API review checklist

## Domain

- Endpoint thể hiện business intent?
- Đúng Context?
- Đúng Aggregate action?
- Không generic status patch?

## Security

- Auth?
- Permission?
- Scope?
- Masking?
- SoD?
- Audit?

## Reliability

- Idempotency?
- If-Match?
- Transaction?
- Outbox?
- Async job?
- Retry?

## Contract

- OpenAPI?
- Stable operation ID?
- Errors?
- Examples?
- Versioning?

## Performance

- Pagination?
- Filter allowlist?
- Query scope?
- Size limits?
- Async nếu long-running?

---

# 43. Anti-patterns bị cấm

1. Generic CRUD endpoints cho stateful Aggregate.
2. `PATCH status`.
3. Authorization ở frontend.
4. Scope filter bằng Python sau query.
5. Return ORM trực tiếp.
6. Endpoint không OpenAPI.
7. `success: true` envelope.
8. HTTP 200 cho mọi lỗi.
9. Raw exception detail.
10. Thiếu Idempotency-Key cho critical command.
11. Thiếu If-Match cho mutable critical resource.
12. Offset pagination lớn.
13. Arbitrary filter language.
14. Unbounded list.
15. Internal endpoint public.
16. Webhook thiếu signature/replay protection.
17. Full PII trong response/log/error.
18. Frontend tính official KPI.
19. Async process trả fake completed.
20. Breaking change không version/deprecation.
21. Duplicate handwritten API types.
22. Tin owner/scope từ request body.
23. Cross-context write trong router.

---

# 44. AI Agent API protocol

Trước khi tạo endpoint, AI Agent phải:

1. Xác định owning Context.
2. Xác định command hay query.
3. Xác định Aggregate/state machine.
4. Xác định permission/scope/masking.
5. Xác định idempotency.
6. Xác định concurrency.
7. Xác định audit/event.
8. Xác định sync/async.
9. Thiết kế request/response/errors.
10. Update OpenAPI.
11. Implement tests.
12. Generate client.
13. Run contract/security tests.
14. Update docs.

---

# 45. AI Agent prohibited API behaviors

AI Agent không được:

1. Tạo endpoint chưa rõ domain owner.
2. Tạo `updateStatus`.
3. Bỏ permission metadata.
4. Tin `enterprise_id` hoặc `owner_id` từ body.
5. Trả ORM.
6. Trả raw provider response.
7. Tự tạo error code không registry.
8. Bỏ pagination.
9. Bỏ Idempotency-Key.
10. Bỏ If-Match.
11. Bỏ OpenAPI.
12. Handwrite duplicate TypeScript types.
13. Expose internal route public.
14. Log request body.
15. Báo Done khi contract tests fail.

---

# 46. Definition of Ready cho API change

API change chỉ Ready khi:

1. Use case rõ.
2. Context owner rõ.
3. Domain behavior rõ.
4. Permission/scope rõ.
5. Request/response rõ.
6. Errors rõ.
7. Idempotency/concurrency rõ.
8. Audit/event rõ.
9. Sync/async rõ.
10. Tests rõ.
11. Không có documentation conflict block.

---

# 47. Definition of Done cho API change

API change chỉ Done khi:

1. Endpoint implemented.
2. OpenAPI updated.
3. Operation ID stable.
4. Request/response schemas typed.
5. Permission/scope/masking enforced.
6. Idempotency implemented khi required.
7. If-Match implemented khi required.
8. Stable errors.
9. Audit/Outbox.
10. Pagination/filter/sort correct.
11. Integration tests pass.
12. Security tests pass.
13. Contract tests pass.
14. Generated client clean.
15. Docs/examples updated.
16. No PII/secret leakage.
17. Acceptance Report updated.

---

# 48. Exception process

Ngoại lệ cần file:

```text
docs/engineering/api-exceptions/EXC-API-XXX.md
```

Nội dung:

- Rule.
- Endpoint.
- Reason.
- Consumer impact.
- Security impact.
- Compatibility impact.
- Expiry.
- Mitigation.
- Owner.
- Approval.

Không có ngoại lệ vô thời hạn không owner.

---

# 49. Change Log

## Version 1.0.0 — 2026-07-24

- Thiết lập REST/API classes.
- Khóa path/method/status conventions.
- Khóa response envelope và Problem Details.
- Khóa OpenAPI 3.1 và operation IDs.
- Khóa auth, permission, scope và masking.
- Khóa ETag, If-Match và Idempotency-Key.
- Khóa cursor pagination, filters và sorting.
- Khóa public/internal/webhook/file/bulk APIs.
- Khóa observability, security và testing.
- Khóa AI Agent API protocol và anti-patterns.

---

# 50. Kết luận

API của `crm_bds_ai` không chỉ là transport layer.

Nó là contract bảo vệ:

```text
Domain Intent
+ Authorization
+ Concurrency
+ Idempotency
+ Auditability
+ Contract Stability
+ Client Interoperability
```

Nguyên tắc tối cao:

> Mỗi endpoint phải thể hiện một use case rõ, enforce quyền ở backend, có contract máy đọc được và không được làm mất domain meaning chỉ để thuận tiện cho frontend.
