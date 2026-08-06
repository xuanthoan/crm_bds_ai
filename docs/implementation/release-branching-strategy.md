# CRM_BDS_AI — RELEASE AND BRANCHING STRATEGY

**Document ID:** `IMPL-REL-001`  
**Canonical path:** `docs/implementation/release-branching-strategy.md`  
**Product:** `crm_bds_ai`  
**Version:** `1.0.0`  
**Status:** `Ready for Review / Foundation Baseline`  
**Owner:** `Engineering Owner`  
**Effective date:** `2026-08-05`  
**Last reviewed:** `2026-08-05`  
**Classification:** `INTERNAL`

---

# 1. Branching

Trunk-oriented hoặc short-lived feature branches. Exact policy được Engineering Owner chấp nhận trong Sprint 1. Không giữ long-lived environment branches như source truth.

# 2. Commits/PR

Small coherent commits, conventional subject, issue/task reference, generated artifacts included only when required. PR mô tả scope, risks, migrations, contracts, security và tests.

# 3. Release

Immutable versioned artifact; release record gắn commit, migration head, contracts, images, approvals, rollout và rollback conditions.

# 4. Hotfix

Hotfix vẫn phải có issue, regression test, contract/doc updates và post-release reconciliation.
