# CRM_BDS_AI — SCOPE RESOLUTION

**Document ID:** `SEC-SCO-001`  
**Canonical path:** `docs/security/scope-resolution.md`  
**Product:** `crm_bds_ai`  
**Version:** `1.0.0`  
**Status:** `Ready for Review`  
**Owner:** `Security Owner`  
**Reviewers:** `IAM Domain Owner, API Owner, QA Owner`  
**Last reviewed:** `2026-08-05`  
**Classification:** `INTERNAL`


# 1. Scope vocabulary

```text
MINE
TEAM
DEPARTMENT
LEGAL_ENTITY
PROJECT
ALL_AUTHORIZED
RESOURCE_LINKED
```

`ALL_AUTHORIZED` không đồng nghĩa toàn hệ thống; nó là tập grants hiện hành của principal.

# 2. Resolution algorithm

1. Xác thực principal/session.
2. Resolve active Employment Assignment, roles, grants và delegation.
3. Resolve Legal Entity/Project/Org boundaries.
4. Intersect permission-specific allowed scope.
5. Intersect resource policy và workflow participation.
6. Intersect user filters; filters chỉ thu hẹp.
7. Apply concealment và field masking.

# 3. Client parameters

`scope`, `owner_id`, `team_id`, `department_id`, `legal_entity_id`, `project_id` từ client không được mở rộng quyền.

# 4. Historical/as-of

Analytics/reporting lịch sử dùng organization/assignment snapshot hoặc effective-time facts, không dùng current org để viết lại lịch sử.

# 5. Tests

Mine/team/department/all escalation, delegated scope expiry, inactive assignment, cross-entity access, URL/body tampering, export và cache isolation.
