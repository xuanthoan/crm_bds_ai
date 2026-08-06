# CRM_BDS_AI — HEALTH AND READINESS CONTRACT

**Document ID:** `IMPL-HEALTH-001`  
**Canonical path:** `docs/implementation/health-readiness-contract.md`  
**Product:** `crm_bds_ai`  
**Version:** `1.0.0`  
**Status:** `Ready for Review / Foundation Baseline`  
**Owner:** `Operations Owner`  
**Effective date:** `2026-08-05`  
**Last reviewed:** `2026-08-05`  
**Classification:** `INTERNAL`

---

# 1. Liveness

Chứng minh process loop còn hoạt động; không kiểm tra dependency nặng; không chứa secret/detail nhạy cảm.

# 2. Readiness

Chứng minh runtime có thể nhận workload an toàn. Kiểm tra required configuration, database connectivity/migration compatibility, broker/storage khi bắt buộc và startup initialization.

# 3. Diagnostics

Internal diagnostics có auth, masking và rate limit. Không expose credentials, DSN, queue payload hoặc stack trace ra public.

# 4. Worker

Worker readiness phải thể hiện broker connection, consumer startup và critical configuration. Queue backlog thuộc metrics/alerts, không nhất thiết làm liveness fail.

# 5. Acceptance

Test healthy/unhealthy/degraded transitions, timeout và graceful shutdown.
