# CRM_BDS_AI — INFRASTRUCTURE BASELINE

**Document ID:** `INFRA-README-001`  
**Canonical path:** `infrastructure/README.md`  
**Product:** `crm_bds_ai`  
**Version:** `1.0.0`  
**Status:** `Template / Sprint 0 Validation Required`  
**Owner:** `Operations Owner`  
**Effective date:** `2026-08-05`  
**Last reviewed:** `2026-08-05`  
**Classification:** `INTERNAL`

---

# Scope

Thư mục này sẽ chứa local Compose, image locks, environment templates, Dockerfiles và observability configuration sau Sprint 1.

# Rules

- Không dùng `latest`.
- Không commit production secret.
- Stateful services có health checks và declared volumes.
- Test resources tách developer persistent data.
- Exact images/digests phải khớp Toolchain Lock.
