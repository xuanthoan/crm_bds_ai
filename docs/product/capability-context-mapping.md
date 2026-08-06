# CRM_BDS_AI — CAPABILITY–CONTEXT MAPPING

**Document ID:** `PROD-CCM-001`  
**Canonical path:** `docs/product/capability-context-mapping.md`  
**Product:** `crm_bds_ai`  
**Version:** `1.0.0`  
**Status:** `Ready for Review / Foundation Baseline`  
**Owner:** `Architecture Owner`  
**Effective date:** `2026-08-05`  
**Last reviewed:** `2026-08-05`  
**Classification:** `INTERNAL`

---

# 1. Mapping

| Capability | Primary Context | Supporting Contexts |
|---:|---|---|
| 01 | `platform` | `iam`, `audit`, `operations` |
| 02 | `iam` | `party`, `platform`, `audit` |
| 03 | `lead` | `party`, `iam`, `marketing`, `activity` |
| 04 | `party` | `lead`, `activity`, `documents` |
| 05 | `party` | `integration`, `audit` |
| 06 | `product` | `party`, `documents`, `integration` |
| 07 | `matching` | `party`, `product`, `analytics` |
| 08 | `transaction` | `product`, `party`, `activity`, `documents` |
| 09 | `contract` | `transaction`, `product`, `documents`, `integration` |
| 10 | `revenue` | `contract`, `transaction`, `iam`, `integration` |
| 11 | `activity` | all owning business Contexts, `party`, `integration` |
| 12 | `marketing` | `lead`, `party`, `activity`, `integration`, `analytics` |
| 13 | `analytics` | all Contexts as read-only fact providers |
| 14 | composite | `documents`, `audit`, `integration`, `operations` |

# 2. Quy tắc

- Mapping không tạo shared ownership.
- Mỗi aggregate có đúng một owning Context.
- Supporting Context chỉ giao tiếp qua published contract.
- Capability 14 không tạo `runtime_support` Context.
