# CRM_BDS_AI — NON-FUNCTIONAL REQUIREMENTS

**Document ID:** `ARCH-NFR-001`  
**Canonical path:** `docs/architecture/non-functional-requirements.md`  
**Product:** `crm_bds_ai`  
**Version:** `1.0.0`  
**Status:** `Ready for Review`  
**Owner:** `Architecture Owner`  
**Reviewers:** `Product Owner, Security Owner, Operations Owner, QA Owner`  
**Last reviewed:** `2026-08-05`  
**Classification:** `INTERNAL`


# 1. Mục tiêu

Khóa quality attributes và cách xác định acceptance. Exact production SLO/capacity phải được validate và ghi trong Operations documents; không hard-code từ tài liệu này.

# 2. Security

- Deny by default.
- Backend authorization, scope resolution và field masking.
- MFA/re-auth cho high-risk actions.
- Secrets qua secret manager reference.
- Audit cho sensitive reads, exports, approvals và break-glass.

# 3. Data integrity

- PostgreSQL constraints bảo vệ invariants cục bộ.
- Decimal/fixed precision cho money.
- UTC storage + explicit business timezone.
- Idempotency cho external/cross-context commands.
- Receipt, signed Document Version và Audit Fact bất biến.

# 4. Availability và resilience

- Health/readiness/liveness riêng.
- Graceful degradation cho provider outage.
- Retry bounded + backoff + DLQ + replay.
- Reconciliation cho process kéo dài.
- Backup, restore test và DR drill có evidence.

# 5. Performance classes

| Class | Ví dụ | Validation |
|---|---|---|
| Interactive command | create/update/transition | p95/p99 theo SLO được khóa trước release |
| Interactive query | list/detail/search | query budget và pagination bắt buộc |
| Analytical query | dashboard/report | async/precompute khi vượt interactive budget |
| Batch | import/rebuild/reconciliation | checkpoint, resumable, bounded concurrency |

# 6. Scalability

- Scale vertical trước, horizontal khi evidence yêu cầu.
- Partition/index dựa trên query evidence.
- Không microservice split chỉ vì Context boundary.

# 7. Observability

- Structured logs, metrics, traces, correlation/causation IDs.
- Không log PII/secrets.
- SLI cho API, queue, outbox, inbox, provider, jobs và data freshness.

# 8. Privacy và retention

- Data minimization, purpose limitation, classification, masking.
- Retention policy theo data class và legal hold.
- Export có watermark, expiry và Audit.

# 9. Accessibility và UX

- Keyboard navigation, focus management, contrast, screen-reader semantics.
- Loading/empty/error/conflict states.
- Responsive enterprise layouts.

# 10. Maintainability

- Typed contracts, deterministic generation, architecture tests.
- No hidden framework magic cho business invariants.
- Documentation drift là blocker khi liên quan security/finance/ownership.

# 11. Acceptance

Mỗi Sprint phải map thay đổi tới NFR impact và cung cấp test/evidence tương ứng.
