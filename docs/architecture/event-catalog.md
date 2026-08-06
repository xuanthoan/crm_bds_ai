# CRM_BDS_AI — EVENT CATALOG

**Document ID:** `ARCH-EVT-CAT-001`  
**Canonical path:** `docs/architecture/event-catalog.md`  
**Product:** `crm_bds_ai`  
**Version:** `1.0.0`  
**Status:** `Ready for Review / Foundation Baseline`  
**Owner:** `Architecture Owner`  
**Effective date:** `2026-08-05`  
**Last reviewed:** `2026-08-05`  
**Classification:** `INTERNAL`

---

# 1. Quy tắc

Catalog liệt kê business facts dự kiến. Exact Event name/version/payload chỉ có hiệu lực trong JSON Schema + AsyncAPI + Event Registry.

# 2. Candidate facts

| Context | Facts tiêu biểu |
|---|---|
| `platform` | EnterpriseCreated, LegalEntityActivated, ConfigurationPublished, WorkflowPublished, NumberIssued |
| `iam` | EmploymentStarted, EmploymentEnded, RoleGranted, RoleRevoked, DelegationActivated |
| `party` | PartyCreated, CustomerRelationshipActivated, PhoneVerified, ConsentChanged, CustomerMerged |
| `lead` | LeadIntakeAccepted, LeadAssigned, ProtectionActivated, LeadQualified, LeadConverted |
| `product` | ListingActivated, AvailabilityChanged, CommercialLockActivated, LockReleased |
| `matching` | MatchingRunCompleted, MatchResultPublished, ShortlistChanged, RequirementUpdateSuggested |
| `transaction` | DealStageChanged, ProposalSubmitted, HoldRequested, BookingConfirmed, BookingCancelled |
| `contract` | ContractSigned, ContractEffective, PaymentAllocated, ReceiptIssued, RefundCompleted, SettlementCompleted |
| `revenue` | RevenueEntitlementRecognized, CommissionVested, CommissionPayable, PayoutConfirmed, ClawbackOpened |
| `activity` | TaskCompleted, AppointmentOutcomeRecorded, InteractionRecorded, SLABreached, NBAFeedbackRecorded |
| `marketing` | CampaignActivated, CaptureAccepted, AudienceEvaluated, MessageIntentCreated, AttributionCalculated |
| `analytics` | SnapshotLocked, ForecastApproved, MetricCertified, DataQualityFailed |
| `documents` | DocumentVerified, SignatureCompleted, DossierFrozen, LegalHoldApplied |
| `audit` | AuditFactRecorded, IntegrityCheckFailed |
| `integration` | ConnectionActivated, SyncCompleted, DeliveryFailed, ReconciliationOpened |
| `operations` | IncidentDeclared, BackupVerified, RestoreVerified, ReleaseActivated |

# 3. Envelope

Mọi Event phải có event_id, event_type, event_version, occurred_at, producer, aggregate reference, correlation_id, causation_id, traceparent và data-classification metadata phù hợp.
