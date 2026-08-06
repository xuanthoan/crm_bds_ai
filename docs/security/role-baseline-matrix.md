# CRM_BDS_AI — ROLE BASELINE MATRIX

**Document ID:** `SEC-ROL-001`  
**Canonical path:** `docs/security/role-baseline-matrix.md`  
**Product:** `crm_bds_ai`  
**Version:** `1.0.0`  
**Status:** `Ready for Review`  
**Owner:** `Security Owner`  
**Reviewers:** `Product Owner, IAM Domain Owner, Domain Owners`  
**Last reviewed:** `2026-08-05`  
**Classification:** `INTERNAL`


# 1. Principle

Role là baseline bundle; final decision vẫn cần permission, scope, field policy, SoD và workflow.

# 2. Roles

| Role | Business intent | Grant source |
|---|---|---|
| `DIRECTOR` | Executive business oversight; broad authorized scope, sensitive data still masked by purpose. | See permission registry + scope policy |
| `SALES_MANAGER` | Department sales management. | See permission registry + scope policy |
| `TEAM_LEAD` | Team supervision and assignment. | See permission registry + scope policy |
| `SALE` | Own assigned leads/customers/deals; no customer/project export. | See permission registry + scope policy |
| `MARKETING_MANAGER` | Campaign/audience/attribution management. | See permission registry + scope policy |
| `MARKETING_USER` | Campaign operations with restricted customer fields. | See permission registry + scope policy |
| `CONTRACT_LEGAL` | Contract review, signing process and legal documents. | See permission registry + scope policy |
| `FINANCE_ACCOUNTING` | Payment, allocation, receipt, refund and settlement operations. | See permission registry + scope policy |
| `REVENUE_MANAGER` | Revenue/commission governance and payout approval. | See permission registry + scope policy |
| `HR_IAM_ADMIN` | Workforce, organization and account administration; no blanket CRM data. | See permission registry + scope policy |
| `SYSTEM_ADMIN` | Technical configuration/operations; no blanket business access. | See permission registry + scope policy |
| `AUDITOR` | Read-only approved audit/evidence access. | See permission registry + scope policy |
| `OPERATIONS_ENGINEER` | Runtime, incident, backup/restore; business data only through support scope. | See permission registry + scope policy |

# 3. High-level matrix

| Capability | Director | Sales Mgr | Team Lead | Sale | Marketing | Legal | Finance | Revenue | Admin/Ops |
|---|---|---|---|---|---|---|---|---|---|
| Lead/Customer | All authorized | Department | Team | Mine | Limited/masked | Case-linked | Financial purpose | No default | No default |
| Product | View/manage policy | View | View | View | View campaign scope | Contract-linked | View | View | Technical only |
| Transaction | View | Department | Team | Mine | Attribution only | Case-linked | Payment-linked | Revenue-linked | No default |
| Contract/Cash | View approved | Summary | Summary | Own masked | No default | Legal scope | Full finance scope | Revenue input | No default |
| Revenue/Commission | Executive | Team summary | Team summary | Own commission | No default | No default | Financial review | Full authorized | No default |
| Analytics | Executive aggregate/detail per policy | Department | Team | Mine | Marketing | Legal | Finance | Revenue | Operational only |

# 4. Export policy

Sale, Team Lead và Sales Manager không được export Customer/Project/Property datasets. Director và Finance/Accounting chỉ export khi có explicit permission, purpose, watermark và Audit.
