# CRM_BDS_AI — PROCESS MANAGER CATALOG

**Document ID:** `ARCH-PM-CAT-001`  
**Canonical path:** `docs/architecture/process-manager-catalog.md`  
**Product:** `crm_bds_ai`  
**Version:** `1.0.0`  
**Status:** `Ready for Review / Foundation Baseline`  
**Owner:** `Architecture Owner`  
**Effective date:** `2026-08-05`  
**Last reviewed:** `2026-08-05`  
**Classification:** `INTERNAL`

---

# 1. Catalog

| Process | Owner | Participants | Success outcome |
|---|---|---|---|
| Lead Conversion | `lead` | `party`, `activity` | Lead converted và Customer reference durable |
| Customer Merge | `party` | all reference consumers | Redirect published, downstream reconciled |
| Listing Activation | `product` | `documents`, `platform` | Listing active only after rights/policy evidence |
| Hold Activation | `transaction` | `product` | Hold ACTIVE only after Commercial Lock accepted |
| Booking Confirmation | `transaction` | `product`, `contract` | Booking confirmed with lock/payment conditions |
| Contract Effectiveness | `contract` | `documents`, `product`, `transaction` | Legal/evidence gates satisfied |
| Contract Cancellation | `contract` | `product`, `revenue`, `transaction` | cash, inventory and entitlement impacts reconciled |
| Revenue Entitlement | `revenue` | `contract` | versioned entitlement calculated |
| Commission Vesting | `revenue` | `contract`, `transaction`, `iam` | beneficiary and milestone snapshot locked |
| Signature Envelope | `documents` | `contract`, `integration` | signed evidence accepted; Contract decides effect |
| Marketing Lead Handoff | `marketing` | `lead`, `party` | capture accepted without duplicate source truth |
| Payment/Receipt Reconciliation | `contract` | `integration`, `audit` | external movement, allocation and receipt consistent |
| Product Release after Cancellation | `product` | `contract`, `transaction` | availability decided by Product rules |

# 2. Required design

Mỗi process phải công bố trigger, state, steps, commands, Events, idempotency, timeout, retry, compensation, reconciliation, manual intervention, security, metrics và tests.
