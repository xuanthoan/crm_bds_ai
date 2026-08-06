# CRM_BDS_AI — DATA CLASSIFICATION

**Document ID:** `SEC-DAT-001`  
**Canonical path:** `docs/security/data-classification.md`  
**Product:** `crm_bds_ai`  
**Version:** `1.0.0`  
**Status:** `Ready for Review`  
**Owner:** `Data Governance Owner`  
**Reviewers:** `Security Owner, Legal Owner, Domain Owners`  
**Last reviewed:** `2026-08-05`  
**Classification:** `INTERNAL`


| Class | Meaning | Examples | Minimum controls |
|---|---|---|---|
| `PUBLIC` | Có thể công bố | Public product material | Integrity review |
| `INTERNAL` | Nội bộ doanh nghiệp | Non-sensitive configuration/docs | Authenticated access |
| `CONFIDENTIAL` | PII/business data | Phone, email, lead details | Scope + masking + audit where sensitive |
| `RESTRICTED` | Sensitive commercial/legal | Contract terms, commission | Purpose + role + scope + audit |
| `HIGHLY_RESTRICTED` | Critical identity/financial/security | ID documents, bank, secrets | Least privilege, re-auth, encryption, audit |

# Rules

- Mỗi aggregate/field/document/event phải có classification hoặc inherit rõ.
- Events giảm thiểu PII.
- Logs không chứa RESTRICTED/HIGHLY_RESTRICTED raw values.
- Classification cao nhất của components quyết định artifact/export class.
