# CRM_BDS_AI — CI AND QUALITY GATES

**Document ID:** `IMPL-CI-001`  
**Canonical path:** `docs/implementation/ci-quality-gates.md`  
**Product:** `crm_bds_ai`  
**Version:** `1.0.0`  
**Status:** `Ready for Review / Foundation Baseline`  
**Owner:** `QA Owner`  
**Effective date:** `2026-08-05`  
**Last reviewed:** `2026-08-05`  
**Classification:** `INTERNAL`

---

# 1. Required jobs

- Documentation and link validation.
- Secret scan.
- Backend format/lint/type/unit.
- Backend architecture tests.
- PostgreSQL integration tests.
- Migration upgrade/downgrade/re-upgrade.
- OpenAPI/Event/AsyncAPI validation and drift.
- Frontend lint/type/unit/component/build.
- E2E smoke when environment available.
- Dependency/license/security scan.
- Container build and vulnerability scan.

# 2. Rules

- Clean checkout and locked install.
- Mandatory job không `allow_failure`.
- Cache không che missing lockfile.
- Artifacts gắn commit SHA.
- Flaky test phải được issue hóa, không retry vô hạn để tạo green.

# 3. Merge gate

PR chỉ merge khi mandatory checks PASS, review ownership satisfied và documentation/contracts synchronized.
