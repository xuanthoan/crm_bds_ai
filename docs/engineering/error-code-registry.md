# CRM_BDS_AI — ERROR CODE REGISTRY

**Document ID:** `ENG-ERR-001`  
**Canonical path:** `docs/engineering/error-code-registry.md`  
**Product:** `crm_bds_ai`  
**Version:** `1.0.0`  
**Status:** `Ready for Review`  
**Owner:** `API Owner`  
**Reviewers:** `Architecture Owner, Domain Owners, QA Owner`  
**Last reviewed:** `2026-08-05`  
**Classification:** `INTERNAL`


# 1. Format

```text
<CONTEXT>_<CATEGORY>_<SPECIFIC_REASON>
```

Categories: `VALIDATION`, `NOT_FOUND`, `CONFLICT`, `FORBIDDEN`, `STATE`, `DEPENDENCY`, `INTEGRATION`, `INTERNAL`.

# 2. Common codes

| Code | Meaning | HTTP guidance |
|---|---|---|
| `COMMON_VALIDATION_FAILED` | Payload/query không hợp lệ | 422 |
| `COMMON_UNAUTHENTICATED` | Chưa xác thực | 401 |
| `COMMON_FORBIDDEN` | Không có quyền | 403 |
| `COMMON_SCOPE_FORBIDDEN` | Resource ngoài effective scope | 403/404 theo concealment |
| `COMMON_NOT_FOUND` | Resource không tồn tại/không hiển thị | 404 |
| `COMMON_IDEMPOTENCY_CONFLICT` | Key cũ nhưng payload khác | 409 |
| `COMMON_VERSION_CONFLICT` | Optimistic concurrency conflict | 409 |
| `COMMON_RATE_LIMITED` | Vượt giới hạn | 429 |
| `COMMON_DEPENDENCY_UNAVAILABLE` | Dependency tạm thời lỗi | 503 |

# 3. Domain baseline

- `PARTY_PHONE_IDENTITY_CONFLICT`
- `PARTY_MERGE_REVIEW_REQUIRED`
- `LEAD_PROTECTION_CONFLICT`
- `PRODUCT_LISTING_NOT_AVAILABLE`
- `PRODUCT_COMMERCIAL_LOCK_CONFLICT`
- `MATCHING_PROFILE_STALE`
- `TRANSACTION_HOLD_NOT_ACTIVE`
- `TRANSACTION_BOOKING_STATE_INVALID`
- `CONTRACT_SIGNED_VERSION_IMMUTABLE`
- `CONTRACT_PAYMENT_OVER_ALLOCATION`
- `CONTRACT_RECEIPT_IMMUTABLE`
- `REVENUE_ARRANGEMENT_NOT_RESOLVED`
- `REVENUE_COMMISSION_NOT_PAYABLE`
- `ACTIVITY_CONSENT_REQUIRED`
- `MARKETING_AUDIENCE_SUPPRESSED`
- `ANALYTICS_DETAIL_ACCESS_FORBIDDEN`
- `DOCUMENTS_FILE_QUARANTINED`
- `INTEGRATION_WEBHOOK_REPLAYED`
- `OPERATIONS_REPAIR_APPROVAL_REQUIRED`

# 4. Rules

- Không lộ stack trace/SQL/provider secret.
- Error response có `code`, `message`, `correlation_id`, optional safe `details`.
- Code không đổi meaning; deprecate thay vì reuse.
- Machine registry phải sinh documentation hoặc CI kiểm tra drift.
