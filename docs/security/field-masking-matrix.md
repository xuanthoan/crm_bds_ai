# CRM_BDS_AI — FIELD MASKING MATRIX

**Document ID:** `SEC-MAS-001`  
**Canonical path:** `docs/security/field-masking-matrix.md`  
**Product:** `crm_bds_ai`  
**Version:** `1.0.0`  
**Status:** `Ready for Review`  
**Owner:** `Security Owner`  
**Reviewers:** `Data Governance Owner, Domain Owners, QA Owner`  
**Last reviewed:** `2026-08-05`  
**Classification:** `INTERNAL`


# 1. Rules

- Masking thực hiện backend trước serialization/cache/export.
- Masking không thay authorization; unauthorized field có thể omitted thay vì masked.
- List, detail, timeline, search, report, export và BI phải nhất quán.

# 2. Baseline

| Field group | Class | Baseline policy |
|---|---|---|
| Customer phone/email | `CONFIDENTIAL` | Sale mine: visible; team/manager: policy; marketing: masked; system admin: hidden |
| Identity number | `HIGHLY_RESTRICTED` | Only explicit legal/finance purpose; default masked |
| Financial Profile | `HIGHLY_RESTRICTED` | Authorized sale/manager limited; finance/legal by purpose |
| Bank account | `HIGHLY_RESTRICTED` | Finance execution only; masked elsewhere |
| Contract price/discount/floor price | `RESTRICTED` | Role + project + workflow; floor price highly restricted |
| Commission beneficiary/rate | `RESTRICTED` | Own beneficiary or authorized revenue/management |
| Signed document | `HIGHLY_RESTRICTED` | Short-lived Documents access + source-resource access |
| Audit sensitive payload | `RESTRICTED` | Auditor/security only, redacted |
| Provider secret | `HIGHLY_RESTRICTED` | Never returned; secret reference only |

# 3. Cache/export

Cache key chứa access-policy hash. Export re-authorize tại execution, áp watermark, expiry và Audit.

# 4. Testing

Role/scope matrix, list vs detail, nested DTO, search snippets, timeline, CSV/XLSX/PDF, scheduled report và external BI.
