# CRM_BDS_AI — SECRETS MANAGEMENT

**Document ID:** `SEC-SECRETS-001`  
**Canonical path:** `docs/security/secrets-management.md`  
**Product:** `crm_bds_ai`  
**Version:** `1.0.0`  
**Status:** `Ready for Review / Foundation Baseline`  
**Owner:** `Security Owner`  
**Effective date:** `2026-08-05`  
**Last reviewed:** `2026-08-05`  
**Classification:** `INTERNAL`

---

# 1. Rules

- Không commit secret.
- Application config chỉ giữ secret reference khi có secret manager.
- Local dùng `.env.example` với placeholder; actual env ignored.
- Logs/errors/traces không lộ secret.
- CI dùng scoped ephemeral credentials.
- Rotation không yêu cầu code change khi có thể.

# 2. Classes

Database, broker, object storage, OIDC, signing, webhook, email/SMS/Zalo, bank/payment, ERP, encryption keys và service credentials.

# 3. Lifecycle

Provision → distribute least privilege → use → monitor → rotate → revoke → incident response → Audit.
