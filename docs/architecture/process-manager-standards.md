# CRM_BDS_AI — PROCESS MANAGER STANDARDS

**Document ID:** `ARCH-PM-001`  
**Canonical path:** `docs/architecture/process-manager-standards.md`  
**Product:** `crm_bds_ai`  
**Version:** `1.0.0`  
**Status:** `Ready for Review`  
**Owner:** `Architecture Owner`  
**Reviewers:** `Product Owner, Technical Owner, Security Owner, QA Owner`  
**Last reviewed:** `2026-08-05`  
**Classification:** `INTERNAL`


# 1. Khi nào dùng

Dùng Process Manager khi một business outcome cần nhiều local transactions hoặc Contexts và có trạng thái chờ, timeout, retry, compensation hoặc reconciliation.

# 2. Bắt buộc mô tả

- Process owner.
- Correlation ID và business key.
- Trigger.
- State machine.
- Commands gửi đi.
- Events/result nhận vào.
- Idempotency.
- Timeout.
- Retry/backoff.
- Compensation.
- Reconciliation.
- Manual intervention.
- Authorization/audit.
- Metrics/SLO.

# 3. Quy tắc

- Process Manager không sở hữu aggregate của participants.
- Không dùng distributed transaction.
- State transition phải monotonic hoặc có explicit correction.
- Duplicate/out-of-order events phải safe.
- Compensation là business action, không phải rollback giả.

# 4. Canonical processes

Lead Conversion, Customer Merge, Hold Activation, Booking Confirmation, Contract Effectiveness, Contract Cancellation, Revenue Entitlement, Commission Vesting, Signature Envelope, Marketing Lead Handoff, Payment/Receipt Reconciliation và Product Release.

# 5. Persistence

Process state, attempts, deadlines, last accepted event, expected next actions và reconciliation status nằm trong owning Context.

# 6. Acceptance tests

Happy path, duplicate trigger, duplicate result, out-of-order result, timeout, retry exhausted, compensation, manual repair và restart from checkpoint.
