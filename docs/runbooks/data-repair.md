# CRM_BDS_AI — DATA REPAIR RUNBOOK

**Document ID:** `RUN-REP-001`  
**Canonical path:** `docs/runbooks/data-repair.md`  
**Product:** `crm_bds_ai`  
**Version:** `1.0.0`  
**Status:** `Ready for Review`  
**Owner:** `Operations Owner`  
**Reviewers:** `Owning Domain Owner, Database Owner, Security Owner, Audit Owner`  
**Last reviewed:** `2026-08-05`  
**Classification:** `INTERNAL`


# Steps

1. Identify owning Context và invariant.
2. Capture evidence/read-only diagnosis.
3. Define repair command/script in owning Context.
4. Dry run và impact report.
5. Maker/checker/approval.
6. Execute with correlation ID and bounded scope.
7. Validate invariants, projections và external reconciliation.
8. Append Audit evidence và close.

Direct cross-schema repair hoặc deletion of immutable history bị cấm.
