# CRM_BDS_AI — PERMISSION REGISTRY

**Document ID:** `SEC-PER-001`  
**Canonical path:** `docs/security/permission-registry.md`  
**Product:** `crm_bds_ai`  
**Version:** `1.0.0`  
**Status:** `Ready for Review`  
**Owner:** `Security Owner`  
**Reviewers:** `IAM Domain Owner, Domain Owners, QA Owner`  
**Last reviewed:** `2026-08-05`  
**Classification:** `INTERNAL`


# 1. Rules

- Deny by default.
- Permission không bao hàm scope hoặc field access.
- View không bao hàm Export.
- Admin kỹ thuật không mặc định có business-data access.
- Exact machine registry phải dùng cùng stable codes.

# 2. Baseline codes

| Code | Namespace | Intent | Risk | Enforcement |
|---|---|---|---|---|
| `PLATFORM_VIEW` | platform | View | Standard | Backend command/query |
| `PLATFORM_CONFIGURE` | platform | Configure | Standard | Backend command/query |
| `PLATFORM_APPROVE_CONFIGURATION` | platform | Approve Configuration | High | Backend command/query |
| `PLATFORM_MANAGE_WORKFLOW` | platform | Manage Workflow | Standard | Backend command/query |
| `PLATFORM_MANAGE_CALENDAR` | platform | Manage Calendar | Standard | Backend command/query |
| `IAM_VIEW` | iam | View | Standard | Backend command/query |
| `IAM_MANAGE_USERS` | iam | Manage Users | Standard | Backend command/query |
| `IAM_MANAGE_ORG` | iam | Manage Org | Standard | Backend command/query |
| `IAM_MANAGE_ROLES` | iam | Manage Roles | Standard | Backend command/query |
| `IAM_GRANT_ACCESS` | iam | Grant Access | High | Backend command/query |
| `IAM_MANAGE_DELEGATION` | iam | Manage Delegation | Standard | Backend command/query |
| `IAM_BREAK_GLASS_APPROVE` | iam | Break Glass Approve | High | Backend command/query |
| `PARTY_VIEW` | party | View | Standard | Backend command/query |
| `PARTY_CREATE` | party | Create | Standard | Backend command/query |
| `PARTY_UPDATE` | party | Update | Standard | Backend command/query |
| `PARTY_VIEW_CONTACT` | party | View Contact | Standard | Backend command/query |
| `PARTY_VIEW_FINANCIAL` | party | View Financial | Standard | Backend command/query |
| `PARTY_MANAGE_CONSENT` | party | Manage Consent | Standard | Backend command/query |
| `PARTY_MERGE` | party | Merge | Standard | Backend command/query |
| `PARTY_EXPORT` | party | Export | High | Backend command/query |
| `LEAD_VIEW` | lead | View | Standard | Backend command/query |
| `LEAD_CREATE` | lead | Create | Standard | Backend command/query |
| `LEAD_ASSIGN` | lead | Assign | Standard | Backend command/query |
| `LEAD_TRANSFER` | lead | Transfer | Standard | Backend command/query |
| `LEAD_QUALIFY` | lead | Qualify | Standard | Backend command/query |
| `LEAD_CONVERT` | lead | Convert | Standard | Backend command/query |
| `LEAD_OVERRIDE_PROTECTION` | lead | Override Protection | Standard | Backend command/query |
| `LEAD_EXPORT` | lead | Export | High | Backend command/query |
| `PRODUCT_VIEW` | product | View | Standard | Backend command/query |
| `PRODUCT_MANAGE_PROJECT` | product | Manage Project | Standard | Backend command/query |
| `PRODUCT_MANAGE_ASSET` | product | Manage Asset | Standard | Backend command/query |
| `PRODUCT_MANAGE_LISTING` | product | Manage Listing | Standard | Backend command/query |
| `PRODUCT_MANAGE_PRICE` | product | Manage Price | Standard | Backend command/query |
| `PRODUCT_MANAGE_AVAILABILITY` | product | Manage Availability | Standard | Backend command/query |
| `PRODUCT_MANAGE_LOCK` | product | Manage Lock | High | Backend command/query |
| `PRODUCT_EXPORT` | product | Export | High | Backend command/query |
| `MATCHING_VIEW` | matching | View | Standard | Backend command/query |
| `MATCHING_RUN` | matching | Run | Standard | Backend command/query |
| `MATCHING_MANAGE_RULES` | matching | Manage Rules | Standard | Backend command/query |
| `MATCHING_MANAGE_SHORTLIST` | matching | Manage Shortlist | Standard | Backend command/query |
| `MATCHING_REVERSE_MATCH` | matching | Reverse Match | Standard | Backend command/query |
| `TRANSACTION_VIEW` | transaction | View | Standard | Backend command/query |
| `TRANSACTION_MANAGE_DEAL` | transaction | Manage Deal | Standard | Backend command/query |
| `TRANSACTION_MANAGE_PROPOSAL` | transaction | Manage Proposal | Standard | Backend command/query |
| `TRANSACTION_REQUEST_HOLD` | transaction | Request Hold | Standard | Backend command/query |
| `TRANSACTION_MANAGE_BOOKING` | transaction | Manage Booking | Standard | Backend command/query |
| `TRANSACTION_APPROVE_DISCOUNT` | transaction | Approve Discount | High | Backend command/query |
| `TRANSACTION_MANAGE_COSALE` | transaction | Manage Cosale | Standard | Backend command/query |
| `CONTRACT_VIEW` | contract | View | Standard | Backend command/query |
| `CONTRACT_CREATE` | contract | Create | Standard | Backend command/query |
| `CONTRACT_REVIEW` | contract | Review | Standard | Backend command/query |
| `CONTRACT_APPROVE` | contract | Approve | High | Backend command/query |
| `CONTRACT_SIGNING_MANAGE` | contract | Signing Manage | Standard | Backend command/query |
| `CONTRACT_PAYMENT_VERIFY` | contract | Payment Verify | Standard | Backend command/query |
| `CONTRACT_ALLOCATION_MANAGE` | contract | Allocation Manage | Standard | Backend command/query |
| `CONTRACT_RECEIPT_ISSUE` | contract | Receipt Issue | Standard | Backend command/query |
| `CONTRACT_RECEIPT_CANCEL` | contract | Receipt Cancel | High | Backend command/query |
| `CONTRACT_REFUND_APPROVE` | contract | Refund Approve | High | Backend command/query |
| `CONTRACT_SETTLEMENT_APPROVE` | contract | Settlement Approve | High | Backend command/query |
| `CONTRACT_EXPORT` | contract | Export | High | Backend command/query |
| `REVENUE_VIEW` | revenue | View | Standard | Backend command/query |
| `REVENUE_MANAGE_ARRANGEMENT` | revenue | Manage Arrangement | Standard | Backend command/query |
| `REVENUE_CALCULATE` | revenue | Calculate | Standard | Backend command/query |
| `REVENUE_RECOGNIZE` | revenue | Recognize | Standard | Backend command/query |
| `REVENUE_MANAGE_COMMISSION_PLAN` | revenue | Manage Commission Plan | Standard | Backend command/query |
| `REVENUE_APPROVE_COMMISSION` | revenue | Approve Commission | High | Backend command/query |
| `REVENUE_APPROVE_PAYOUT` | revenue | Approve Payout | High | Backend command/query |
| `REVENUE_CONFIRM_PAYOUT` | revenue | Confirm Payout | High | Backend command/query |
| `REVENUE_MANAGE_CLAWBACK` | revenue | Manage Clawback | Standard | Backend command/query |
| `REVENUE_EXPORT` | revenue | Export | High | Backend command/query |
| `ACTIVITY_VIEW` | activity | View | Standard | Backend command/query |
| `ACTIVITY_MANAGE_TASK` | activity | Manage Task | Standard | Backend command/query |
| `ACTIVITY_MANAGE_APPOINTMENT` | activity | Manage Appointment | Standard | Backend command/query |
| `ACTIVITY_LOG_INTERACTION` | activity | Log Interaction | Standard | Backend command/query |
| `ACTIVITY_VIEW_RECORDING` | activity | View Recording | Standard | Backend command/query |
| `ACTIVITY_MANAGE_SLA` | activity | Manage Sla | Standard | Backend command/query |
| `ACTIVITY_USE_NBA` | activity | Use Nba | Standard | Backend command/query |
| `MARKETING_VIEW` | marketing | View | Standard | Backend command/query |
| `MARKETING_MANAGE_CAMPAIGN` | marketing | Manage Campaign | Standard | Backend command/query |
| `MARKETING_MANAGE_AUDIENCE` | marketing | Manage Audience | Standard | Backend command/query |
| `MARKETING_ACTIVATE_AUDIENCE` | marketing | Activate Audience | Standard | Backend command/query |
| `MARKETING_MANAGE_JOURNEY` | marketing | Manage Journey | Standard | Backend command/query |
| `MARKETING_VIEW_ATTRIBUTION` | marketing | View Attribution | Standard | Backend command/query |
| `MARKETING_MANAGE_SPEND` | marketing | Manage Spend | Standard | Backend command/query |
| `MARKETING_EXPORT` | marketing | Export | High | Backend command/query |
| `ANALYTICS_VIEW_METRIC` | analytics | View Metric | Standard | Backend command/query |
| `ANALYTICS_VIEW_AGGREGATE` | analytics | View Aggregate | Standard | Backend command/query |
| `ANALYTICS_VIEW_BREAKDOWN` | analytics | View Breakdown | High | Backend command/query |
| `ANALYTICS_VIEW_DETAIL` | analytics | View Detail | Standard | Backend command/query |
| `ANALYTICS_VIEW_SOURCE` | analytics | View Source | Standard | Backend command/query |
| `ANALYTICS_VIEW_SENSITIVE` | analytics | View Sensitive | Standard | Backend command/query |
| `ANALYTICS_EXPORT` | analytics | Export | High | Backend command/query |
| `ANALYTICS_MANAGE_METRIC` | analytics | Manage Metric | Standard | Backend command/query |
| `ANALYTICS_PUBLISH_DASHBOARD` | analytics | Publish Dashboard | Standard | Backend command/query |
| `ANALYTICS_LOCK_SNAPSHOT` | analytics | Lock Snapshot | Standard | Backend command/query |
| `ANALYTICS_APPROVE_FORECAST` | analytics | Approve Forecast | High | Backend command/query |
| `DOCUMENTS_VIEW` | documents | View | Standard | Backend command/query |
| `DOCUMENTS_UPLOAD` | documents | Upload | Standard | Backend command/query |
| `DOCUMENTS_CLASSIFY` | documents | Classify | Standard | Backend command/query |
| `DOCUMENTS_VERIFY` | documents | Verify | Standard | Backend command/query |
| `DOCUMENTS_GENERATE` | documents | Generate | Standard | Backend command/query |
| `DOCUMENTS_SIGNATURE_MANAGE` | documents | Signature Manage | Standard | Backend command/query |
| `DOCUMENTS_DOSSIER_MANAGE` | documents | Dossier Manage | Standard | Backend command/query |
| `DOCUMENTS_LEGAL_HOLD_MANAGE` | documents | Legal Hold Manage | High | Backend command/query |
| `DOCUMENTS_EXPORT` | documents | Export | High | Backend command/query |
| `AUDIT_VIEW` | audit | View | Standard | Backend command/query |
| `AUDIT_VERIFY_INTEGRITY` | audit | Verify Integrity | Standard | Backend command/query |
| `AUDIT_EXPORT` | audit | Export | High | Backend command/query |
| `INTEGRATION_VIEW` | integration | View | Standard | Backend command/query |
| `INTEGRATION_MANAGE_CONNECTION` | integration | Manage Connection | Standard | Backend command/query |
| `INTEGRATION_MANAGE_MAPPING` | integration | Manage Mapping | Standard | Backend command/query |
| `INTEGRATION_REPLAY` | integration | Replay | Standard | Backend command/query |
| `INTEGRATION_DLQ_MANAGE` | integration | Dlq Manage | Standard | Backend command/query |
| `INTEGRATION_SYNC_RUN` | integration | Sync Run | Standard | Backend command/query |
| `OPERATIONS_VIEW` | operations | View | Standard | Backend command/query |
| `OPERATIONS_MANAGE_JOBS` | operations | Manage Jobs | Standard | Backend command/query |
| `OPERATIONS_MANAGE_ALERTS` | operations | Manage Alerts | Standard | Backend command/query |
| `OPERATIONS_MANAGE_INCIDENTS` | operations | Manage Incidents | Standard | Backend command/query |
| `OPERATIONS_BACKUP_RUN` | operations | Backup Run | Standard | Backend command/query |
| `OPERATIONS_RESTORE_RUN` | operations | Restore Run | High | Backend command/query |
| `OPERATIONS_DR_RUN` | operations | Dr Run | Standard | Backend command/query |
| `OPERATIONS_DATA_REPAIR_REQUEST` | operations | Data Repair Request | High | Backend command/query |
| `OPERATIONS_DATA_REPAIR_APPROVE` | operations | Data Repair Approve | High | Backend command/query |
| `OPERATIONS_RELEASE_MANAGE` | operations | Release Manage | Standard | Backend command/query |
| `OPERATIONS_SUPPORT_SESSION` | operations | Support Session | Standard | Backend command/query |

# 3. Decision inputs

```text
permission + effective scope + resource policy + field policy + SoD + workflow state
```

# 4. Change control

Code mới cần owner, purpose, risk, endpoints/commands, default role mapping, tests và migration impact.
