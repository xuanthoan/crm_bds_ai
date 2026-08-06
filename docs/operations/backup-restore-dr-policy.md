# CRM_BDS_AI — BACKUP, RESTORE AND DR POLICY

**Document ID:** `OPS-DR-POL-001`  
**Canonical path:** `docs/operations/backup-restore-dr-policy.md`  
**Product:** `crm_bds_ai`  
**Version:** `1.0.0`  
**Status:** `Ready for Review / Foundation Baseline`  
**Owner:** `Operations Owner`  
**Effective date:** `2026-08-05`  
**Last reviewed:** `2026-08-05`  
**Classification:** `INTERNAL`

---

# 1. Scope

PostgreSQL, Object Storage metadata/binaries, broker definitions when required, critical configuration, contracts, Audit integrity evidence and release metadata.

# 2. Principles

Backup success không chứng minh recoverability. Restore tests định kỳ, checksum/integrity, encrypted storage, access control, retention and off-site strategy.

# 3. Recovery

RPO/RTO chính thức thuộc accepted SLO/DR baseline. Restore run phải record source backup, target environment, duration, data checks, application checks and sign-off.
