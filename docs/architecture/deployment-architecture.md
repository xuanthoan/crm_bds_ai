# CRM_BDS_AI — DEPLOYMENT ARCHITECTURE

**Document ID:** `ARCH-DEPLOY-001`  
**Canonical path:** `docs/architecture/deployment-architecture.md`  
**Product:** `crm_bds_ai`  
**Version:** `1.0.0`  
**Status:** `Ready for Review / Foundation Baseline`  
**Owner:** `Operations Owner`  
**Effective date:** `2026-08-05`  
**Last reviewed:** `2026-08-05`  
**Classification:** `INTERNAL`

---

# 1. Baseline

Modular Monolith được deploy thành các runtime roles dùng cùng codebase/version:

- Web/API process.
- Worker process.
- Scheduler/beat process khi cần.
- Frontend web runtime.
- Migration job.
- Contract generation/validation job.

# 2. Dependencies

PostgreSQL, RabbitMQ, Valkey và S3-compatible Object Storage là external stateful dependencies. Cache không là business source of truth.

# 3. Environments

`local`, `test`, `staging`, `production` tách configuration, credentials, data và provider connections. Không dùng production secrets/data trong local/test.

# 4. Release

Build once, promote immutable artifact. Migration dùng expand–migrate–contract. Readiness chỉ PASS khi dependencies, migrations và required consumers ở trạng thái an toàn.

# 5. Chưa khóa

Cloud vendor, orchestration platform, region, replicas và sizing chỉ được khóa qua deployment decision/ADR sau capacity review.
