# CRM_BDS_AI — TRANSACTION BOUNDARIES

**Document ID:** `ARCH-TXN-001`  
**Canonical path:** `docs/architecture/transaction-boundaries.md`  
**Product:** `crm_bds_ai`  
**Version:** `1.0.0`  
**Status:** `Ready for Review`  
**Owner:** `Architecture Owner`  
**Reviewers:** `Product Owner, Technical Owner, Security Owner, QA Owner`  
**Last reviewed:** `2026-08-05`  
**Classification:** `INTERNAL`


# 1. Local transaction rule

Một ACID transaction chỉ ghi business state trong một Context schema cùng Outbox records của Context đó.

# 2. Cấm

- Distributed transaction/2PC xuyên Context/provider.
- Cross-schema business write.
- Direct update từ Analytics, Integration hoặc Operations vào source aggregate.
- Gọi external provider trong DB transaction dài.

# 3. Cross-context process

```text
Local write + Outbox
→ publish command/event
→ downstream Inbox/idempotency
→ downstream local write
→ result event
→ Process Manager update
```

# 4. Idempotency

- Idempotency key gắn principal, operation và payload hash.
- Cùng key + payload khác phải conflict.
- Consumer Inbox lưu event/message identity và result.
- Replay không tạo side effect trùng.

# 5. Concurrency hotspots

- Product Commercial Lock: atomic conditional write/unique invariant.
- Payment Allocation: prevent over-allocation.
- Receipt numbering/issuance: serialized invariant theo scope.
- Customer merge: redirect và idempotent downstream remap.
- Payout: external confirmation reconciliation.

# 6. Immutable records

Issued Receipt, signed Contract Version, approved Allocation history, Payout history, Document Version và Audit Fact không sửa tại chỗ; dùng reversal/replacement/adjustment.

# 7. Timeouts và reconciliation

Mọi process manager phải có timeout, retry policy, reconciliation query và manual intervention path.

# 8. Testing

- Concurrent command tests với PostgreSQL.
- Outbox/Inbox failure injection.
- Duplicate/reordered Event tests.
- Partial process recovery.
- Provider timeout/retry tests.
