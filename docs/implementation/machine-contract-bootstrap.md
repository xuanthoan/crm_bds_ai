# CRM_BDS_AI — MACHINE CONTRACT BOOTSTRAP

**Document ID:** `IMPL-CONTRACT-001`  
**Canonical path:** `docs/implementation/machine-contract-bootstrap.md`  
**Product:** `crm_bds_ai`  
**Version:** `1.0.0`  
**Status:** `Ready for Review / Foundation Baseline`  
**Owner:** `API Owner`  
**Effective date:** `2026-08-05`  
**Last reviewed:** `2026-08-05`  
**Classification:** `INTERNAL`

---

# 1. Sprint 1 baseline

Tạo valid empty/technical OpenAPI 3.1, AsyncAPI 3.x và JSON Schema 2020-12 validation pipeline. Không tạo speculative business endpoints/Events.

# 2. Exact authority

- OpenAPI generated/published file là API authority.
- JSON Schema + AsyncAPI là Event authority.
- Alembic là DB authority.
- Permission machine registry là permission authority.

# 3. Drift

Generation deterministic; CI regenerate và fail khi diff. Generated clients không sửa tay.

# 4. Templates

`contracts/templates/` chỉ là bootstrap example, status `TEMPLATE / NOT PUBLISHED`. Sprint 1 phải tạo canonical machine paths và remove template ambiguity.
