# CRM_BDS_AI — PRODUCT CONTEXT IMPLEMENTATION PACK

**Document ID:** `CTX-PRO-001`  
**Canonical path:** `docs/contexts/product/product-context-implementation-pack.md`  
**Product:** `crm_bds_ai`  
**Version:** `1.0.0`  
**Status:** `Ready for Review`  
**Owner:** `Product Context Owner`  
**Reviewers:** `Architecture Owner, Product Owner, Security Owner, API Owner, Database Owner, Event Owner, QA Owner`  
**Last reviewed:** `2026-08-05`  
**Classification:** `INTERNAL`


# 0. Authority

Tài liệu này khóa baseline triển khai của `product`. Exact physical schema thuộc Alembic; exact API thuộc OpenAPI; exact Events thuộc JSON Schema/AsyncAPI; exact permissions thuộc Security Registry.

# 1. Purpose

Projects, assets, listings, commercial policy, availability và Commercial Lock.

# 2. Ownership

## 2.1. Aggregates/records owned

- `SupplyPartnerProfile`
- `Project`
- `Asset`
- `Ownership`
- `Encumbrance`
- `SellingRight`
- `Listing`
- `PriceVersion`
- `SalesPolicyVersion`
- `Inventory`
- `Availability`
- `CommercialLock`

## 2.2. Boundary

- Chỉ ghi schema `product` và local Outbox.
- Không import repository/ORM model Context khác.
- Cross-context reference bằng ID/snapshot có lineage.
- External/provider data đi qua Integration ACL.

# 3. Candidate commands

- `CreateProject`
- `RegisterAsset`
- `GrantSellingRight`
- `ActivateListing`
- `PublishPrice`
- `ChangeAvailability`
- `AcquireCommercialLock`
- `ExtendCommercialLock`
- `ReleaseCommercialLock`
- `ConvertLock`

# 4. Candidate queries

- `SearchListings`
- `GetListing`
- `GetAvailability`
- `GetCommercialLock`
- `GetPricePolicy`

# 5. Canonical invariants

- Listing cần valid selling right.
- Commercial Lock atomic.
- Một conflicting active lock bị cấm.
- Availability do Product quyết định.

# 6. Candidate published business facts

- `ListingActivated`
- `PricePublished`
- `AvailabilityChanged`
- `CommercialLockAcquired`
- `CommercialLockReleased`
- `CommercialLockExpired`

# 7. Candidate consumed facts

- `HoldLockRequested`
- `ContractInventoryImpactRequested`

# 8. Application and transaction rules

- Mỗi command có explicit authorization metadata, idempotency policy và transaction boundary.
- Local state + Outbox commit atomically.
- Consumer dùng Inbox/idempotency guard.
- Long-running cross-context process dùng Process Manager và reconciliation.
- Không gọi provider trong DB transaction dài.

# 9. Persistence input

- Schema: `product`.
- Technical Outbox/Inbox có thể dùng `infra` theo ADR nhưng ownership/correlation rõ.
- Money dùng fixed precision; time lưu UTC + business timezone metadata.
- Immutable/versioned records không update tại chỗ.
- Exact tables/indexes/constraints chỉ được tạo qua accepted DB specification và Alembic.

# 10. API/Event input

- Operations ở mục 3–4 là capability inventory, không phải exact route.
- Errors dùng Error Code Registry.
- Events có version, occurred_at, correlation_id, causation_id và minimized PII.

# 11. Security

- Deny by default.
- Backend permission + scope + resource + field + SoD + workflow.
- Sensitive reads/exports/approvals có Audit.
- Frontend không làm authority.

# 12. Concurrency and idempotency

- Optimistic version hoặc atomic constraint tùy invariant.
- Same idempotency key + different payload = conflict.
- Duplicate/out-of-order events phải safe.

# 13. Test baseline

- Domain invariant unit tests.
- PostgreSQL integration tests.
- API/Event contract tests.
- Authorization/scope/masking tests.
- Idempotency/concurrency tests.
- Process timeout/retry/reconciliation tests khi áp dụng.
- Architecture import/schema-boundary tests.

# 14. Definition of Ready

- Capability/Glossary/Source of Truth/ADRs reviewed.
- States/commands/events đủ rõ cho Sprint.
- Permissions và acceptance tests identified.
- Không có blocking conflict.

# 15. Definition of Done

- Code, migrations, machine contracts, tests, docs và evidence đồng bộ.
- Goose review và Acceptance Report PASS cho Sprint.
