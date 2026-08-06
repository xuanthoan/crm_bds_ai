# CRM_BDS_AI — DISASTER RECOVERY

**Document ID:** `OPS-DR-001`  
**Canonical path:** `docs/operations/disaster-recovery.md`  
**Product:** `crm_bds_ai`  
**Version:** `1.0.0`  
**Status:** `Ready for Review`  
**Owner:** `Operations Owner`  
**Reviewers:** `Security Owner, Database Owner, Documents Owner`  
**Last reviewed:** `2026-08-05`  
**Classification:** `INTERNAL`


# Scope

PostgreSQL, object storage, broker, cache, configuration, secrets references và deployment artifacts.

# Rules

- RPO/RTO được khóa theo environment/data class sau validation.
- Backup success không đủ; restore test định kỳ bắt buộc.
- DR drill có timeline, evidence, reconciliation và postmortem.
- Restore không được phá Event idempotency hoặc Audit integrity.
