# CRM_BDS_AI — LOCAL DEVELOPMENT CONTRACT

**Document ID:** `IMPL-LOCAL-001`  
**Canonical path:** `docs/implementation/local-development-contract.md`  
**Product:** `crm_bds_ai`  
**Version:** `1.0.0`  
**Status:** `Ready for Review / Foundation Baseline`  
**Owner:** `Engineering Owner`  
**Effective date:** `2026-08-05`  
**Last reviewed:** `2026-08-05`  
**Classification:** `INTERNAL`

---

# 1. Supported flow

```text
clone → install locked tools → copy safe env example → start dependencies → migrate → start API/worker/frontend → run check
```

# 2. Requirements

- Clean setup không dùng production secret.
- Persistent local developer volumes tách ephemeral test resources.
- Test không xóa shared developer data.
- Startup fails fast khi required config thiếu/sai.
- README ghi exact commands sau Sprint 1.

# 3. Profiles

`local`, `test`, `ci`. Production-like credentials không được commit. Provider calls mặc định disabled/mock tại local trừ approved sandbox.

# 4. Verification

Liveness, readiness, OpenAPI endpoint, worker diagnostic, frontend build, migration head và end-to-end smoke route.
