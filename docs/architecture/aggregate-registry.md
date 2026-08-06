# CRM_BDS_AI — AGGREGATE REGISTRY

**Document ID:** `ARCH-AGG-001`  
**Canonical path:** `docs/architecture/aggregate-registry.md`  
**Product:** `crm_bds_ai`  
**Version:** `1.0.0`  
**Status:** `Ready for Review / Foundation Baseline`  
**Owner:** `Architecture Owner`  
**Effective date:** `2026-08-05`  
**Last reviewed:** `2026-08-05`  
**Classification:** `INTERNAL`

---

# 1. Mục đích

Registry cấp kiến trúc cho aggregate ownership. Exact fields và invariants thuộc Context Pack/domain code.

# 2. Registry

| Context | Candidate aggregates |
|---|---|
| `platform` | Enterprise, LegalEntity, BusinessCalendar, ConfigurationDefinition, WorkflowDefinition, ApprovalPolicy, NumberingScheme |
| `iam` | WorkforceSubject, EmploymentAssignment, UserAccount, ServiceAccount, OrganizationUnit, Position, Role, AccessGrant, Delegation |
| `party` | Party, CustomerRelationship, PhoneIdentity, Requirement, FinancialProfile, StakeholderRelation, Consent, MergeCase |
| `lead` | Lead, LeadIntake, LeadQueue, Assignment, CareProtection, Qualification, ConversionProcess |
| `product` | PartnerProfile, Project, Asset, OwnershipRecord, SellingRight, Listing, PriceBook, SalesPolicy, Availability, CommercialLock |
| `matching` | MatchingProfile, MatchingRuleSet, MatchingRun, MatchResult, Shortlist, ReverseMatchingRun |
| `transaction` | Deal, TransactionCase, Proposal, Negotiation, Hold, Booking, DepositCommitment, CoSaleAgreement |
| `contract` | Contract, ContractGroup, PaymentPlan, Receivable, PaymentTransaction, Allocation, Receipt, Refund, TransactionSettlement |
| `revenue` | RevenueArrangement, RevenueEntitlement, RevenueReceivable, CommissionPlan, CommissionEntitlement, PayoutBatch, ClawbackCase |
| `activity` | Task, Appointment, CallLog, Interaction, SLAInstance, NextBestActionRun |
| `marketing` | Campaign, MarketingCapture, Touchpoint, Audience, Journey, MessageIntent, AttributionRun, Experiment |
| `analytics` | DatasetDefinition, MetricDefinition, Dashboard, ReportDefinition, Snapshot, ForecastRun, DataQualityResult |
| `documents` | FileObject, Document, Dossier, SignatureEnvelope, EvidencePackage, LegalHold |
| `audit` | AuditStream, AuditSeal, IntegrityCheck |
| `integration` | Connection, MappingDefinition, WebhookDelivery, SyncRun, DeadLetterItem, ReconciliationCase |
| `operations` | JobRun, Alert, NotificationRun, Incident, BackupRun, RestoreRun, RepairRequest, ReleaseRecord, SupportSession |

# 3. Gate

Không tạo aggregate mới nếu chưa xác định owner, invariant, transaction boundary, identifiers, commands, Events, permissions và test strategy.
