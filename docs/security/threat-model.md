# CRM_BDS_AI — THREAT MODEL

**Document ID:** `SEC-THR-001`  
**Canonical path:** `docs/security/threat-model.md`  
**Product:** `crm_bds_ai`  
**Version:** `1.0.0`  
**Status:** `Ready for Review`  
**Owner:** `Security Owner`  
**Reviewers:** `Architecture Owner, Domain Owners, Operations Owner`  
**Last reviewed:** `2026-08-05`  
**Classification:** `INTERNAL`


# Assets

Customer PII, identity evidence, property inventory, Contract/Payment/Receipt, Revenue/Commission, credentials, audit evidence và availability.

# Trust boundaries

Browser, API, Context boundary, database schemas, broker, object storage, provider integrations, analytics/export và operations support.

# Threat register

| ID | Threat | Area | Primary controls |
|---|---|---|---|
| `T1` | Privilege escalation | API/UI | Backend permission+scope+resource tests |
| `T2` | Cross-tenant/legal-entity data leak | Queries/cache/export | Scope intersection, cache access hash |
| `T3` | Customer identity takeover/incorrect merge | Party merge | Phone identity, review, redirect, audit |
| `T4` | Double sell/lock race | Product | Atomic Commercial Lock invariant |
| `T5` | Payment/Receipt manipulation | Contract | SoD, immutable receipt, reconciliation |
| `T6` | Commission/payout fraud | Revenue | Snapshots, approval, external confirmation |
| `T7` | Webhook forgery/replay | Integration | Signature, timestamp, nonce/inbox |
| `T8` | File malware/data exfiltration | Documents | Scan, quarantine, short-lived access |
| `T9` | AI unsafe action | Activity/Marketing | Permission/consent/workflow gates, human approval |
| `T10` | Admin abuse | IAM/Operations | No blanket data access, break-glass, audit |
| `T11` | Data repair corruption | Operations | Dry run, approval, owner command, validation |
| `T12` | Analytics re-identification | Analytics | Minimum group size, masking, export controls |

# Review trigger

New provider, new sensitive field, new export, new AI action, new payment flow, new public endpoint hoặc architecture boundary change.
