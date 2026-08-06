# CRM_BDS_AI — CAPABILITY 14: RUNTIME SUPPORT OVERVIEW

## Composite Capability Overview for Documents, Audit, Integration and Operations

**Document ID:** `PROD-CAP-RUN-001`
**Canonical path:** `docs/product/capabilities/cap-14-runtime-support-overview.md`
**Product:** `crm_bds_ai`
**Version:** `1.0.0`  
**Status:** `Accepted / Product Capability Baseline`
**Document type:** `Composite Product Capability Overview`
**Capability classification:** `Composite / Cross-context`
**Primary participating Contexts:** `documents`, `audit`, `integration`, `operations`
**Related authority Contexts:** `platform`, `iam`, `party`, `activity`, `marketing`, owning business Contexts
**Owner:** `Product Owner`
**Co-owners:** `Documents Domain Owner`, `Audit Domain Owner`, `Integration Domain Owner`, `Operations Domain Owner`
**Reviewers:** `Architecture Owner`, `Platform Domain Owner`, `IAM Domain Owner`, `Security Owner`, `Database Owner`, `API Owner`, `Event Architecture Owner`, `Data Governance Owner`, `Compliance Owner`, `SRE/Operations Owner`, `QA Owner`
**Effective date:** `2026-08-05`  
**Last reviewed:** `2026-08-05`  
**Classification:** `INTERNAL`

---

# 0. Phạm vi thẩm quyền và quan hệ tài liệu

Tài liệu này là nguồn canonical cho:

- Product outcomes của Runtime Support Composite Capability.
- Quan hệ product-level giữa Documents, Audit, Integration và Operations.
- Business meanings của File, Document, Document Version, Dossier, Audit Evidence, Operational Alert, Notification Runtime, Connector Runtime, Job, Incident, Backup/Restore Evidence và Break-glass Session.
- Cross-context invariants về evidence, idempotency, least privilege, source-of-truth preservation, recoverability và operational safety.
- Capability boundaries, acceptance outcomes và anti-patterns.
- Đầu vào phân rã thành bốn Context Implementation Packs độc lập.

Tài liệu này không phải nguồn exact cho:

- Một Bounded Context hoặc một schema duy nhất mang tên Runtime Support.
- Physical database schema hoặc DDL.
- Exact API paths, payloads, errors hoặc authorization metadata.
- Exact Event names, envelopes, channels hoặc payloads.
- Exact permission codes, scopes, masking hoặc role matrix.
- Exact lifecycle states, document dictionaries, provider mappings, retry parameters, RPO/RTO hoặc operational SLOs.
- Exact storage, vault, queue, scheduler, observability, backup, deployment hoặc disaster-recovery topology.
- Exact signature, OCR, notification, messaging, BI, bank, ERP hoặc provider implementation.
- Exact sprint scope hoặc implementation order.

Nguồn exact tương ứng:

| Chủ đề | Nguồn canonical |
|---|---|
| Thuật ngữ | Domain Glossary |
| Product requirements | PRD |
| Context ownership | Source of Truth Matrix |
| Architecture boundaries | Architecture Overview, Context Map và Accepted ADRs |
| Document/File/Dossier behavior | Documents Context Implementation Pack |
| Immutable Audit behavior | Audit Context Implementation Pack |
| Connector/Webhook/Provider runtime | Integration Context Implementation Pack |
| Job/Queue/Incident/Recovery runtime | Operations Context Implementation Pack |
| Configuration definitions | Platform Context contracts |
| Identity/authorization/emergency grants | IAM Context và Security registries |
| Consent/contact restriction | Party Context contracts |
| Interaction/Timeline | Activity Context contracts |
| Marketing eligibility/journey | Marketing Context contracts |
| Database | Context-specific DB Specifications và Alembic migrations |
| API | Context-specific OpenAPI |
| Events | JSON Schema, AsyncAPI và Event Registry |
| Permissions/scopes/masking/SoD | Security registries và matrices |
| Operational SLO/RPO/RTO | Operations and Recovery documents |
| Công việc hiện tại | Current Sprint Detailed Execution Pack |

**Đây là Composite Capability Overview, không phải một Bounded Context.** Không được tạo một `runtime_support` super-context, một schema tổng hợp hoặc một repository trung tâm sở hữu toàn bộ Documents, Audit, Integration và Operations.

Mỗi participating Context có aggregate, persistence, API, Events và invariants riêng. Phối hợp xuyên Context sử dụng published contracts, durable Events, Transactional Outbox, idempotent consumers, Process Managers và reconciliation; không dùng cross-schema business writes hoặc distributed transaction.

Các phần candidate lifecycle, data model, operations, permissions, Events, screens, dictionaries và thresholds chỉ là design input. Chúng không được dùng thay machine-readable contracts hoặc Context Packs đã được chấp nhận.

---
# 1. Mục tiêu của capability

Runtime Support Composite Capability hoàn thiện các năng lực evidence, integration và operations xuyên suốt `crm_bds_ai` mà không tạo một nguồn chân lý nghiệp vụ cạnh tranh.

Capability phải trả lời được:

- File nào là binary object, Document nào mang business meaning và Dossier nào đại diện bộ hồ sơ có cấu trúc.
- Document Version nào là current, effective, verified, signed hoặc archived.
- File có integrity hash, malware/DLP result, retention và Legal Hold nào.
- Dossier còn thiếu evidence gì và milestone nào bị chặn.
- OCR hoặc AI extraction nào là suggestion, confidence bao nhiêu và đã được human review chưa.
- Electronic Signature Envelope, signer và provider evidence đang ở trạng thái nào.
- Audit fact nào chứng minh business change, sensitive access, approval, export, admin action hoặc break-glass action.
- Audit integrity có được kiểm tra và có dấu hiệu tampering hay không.
- Alert nào phản ánh vấn đề cần xử lý, Notification nào chỉ là delivery intent và Interaction nào chứng minh giao tiếp thực tế.
- Consent, contact restriction, marketing eligibility và quiet-hours gates đã được kiểm tra bởi Context có thẩm quyền chưa.
- Connector, Connection, Mapping Version, Sync, Webhook, DLQ và Reconciliation đang ở trạng thái nào.
- Hệ thống nào là source of truth cho từng resource/field.
- Retry hoặc replay có idempotent và không tạo Lead, Payment, Receipt, Interaction, Document hoặc Payout trùng hay không.
- Job, queue, service, dependency, incident và maintenance state đang thế nào.
- Backup gần nhất đã verify chưa, Restore Drill gần nhất có đạt RPO/RTO không.
- Data Repair hoặc approved data transfer có source-of-truth reference, dry run, approval, validation và reconciliation không.
- Release/deployment nào đang chạy và effective feature configuration nào được Platform công bố.
- Support hoặc break-glass session có authority, scope, expiry, MFA và post-review không.
- System Administrator có đang bị giới hạn khỏi dữ liệu nghiệp vụ nhạy cảm hay không.

Capability phải hỗ trợ:

- Secure File, Document, Version, metadata, classification, review, verification, retention, Legal Hold và secure sharing.
- Electronic Dossier, checklist, completeness, exception, freeze và Evidence Package.
- OCR/extraction suggestions, document generation và electronic-signature evidence.
- Append-only Audit, sensitive-access evidence, integrity verification và archive.
- Operational Alert aggregation, acknowledgement, assignment, escalation, incident linkage và resolution.
- Notification orchestration, preference/eligibility snapshots, secure action links và delivery status.
- Connector, Connection, Mapping/Transformation Version, Webhook, Sync, retry, DLQ, replay và reconciliation.
- Job/queue runtime, health, incidents, maintenance, backup, restore, DR drill, data repair và deployment evidence.
- Multi-Legal Entity, backend authorization, data minimization, idempotency, observability và traceability.

Nguyên tắc canonical:

> Runtime-support Contexts cung cấp evidence, transport và operational control; chúng không sở hữu business outcome của Context nguồn, không dùng technical administration để vượt authorization và không coi delivery intent, provider callback, OCR output, retry hoặc backup metadata là business truth khi chưa có authoritative validation.

---
# 2. Vị trí của capability trong kiến trúc

Runtime Support Composite Capability bao gồm bốn participating Contexts:

```text
documents
→ File, Document, Version, Dossier, OCR/Generation/Signature evidence,
  Retention, Legal Hold and Evidence Package

audit
→ Immutable Audit facts, integrity, archive and access evidence

integration
→ Connectors, provider transport, webhooks, mappings, sync,
  provider delivery, DLQ and external reconciliation

operations
→ Jobs, queues, operational alerts/notifications orchestration,
  health, incidents, maintenance, backup/restore/DR,
  repair orchestration, deployment evidence and support sessions
```

Nó sử dụng:

- `platform`: policy, template, workflow, approval, retention, schedule, notification, connector-profile, feature-flag và SLO/SLA definitions.
- `iam`: User, Service Account, role, scope, delegation, emergency-access authority và authorization decisions.
- Owning business Contexts: source resources, commands, Events, dossier gates, notification intents và correction decisions.
- `party`: canonical Party identity, consent, contact preference và restriction.
- `activity`: canonical Interaction, Task và Timeline.
- `marketing`: Campaign/Journey eligibility và marketing-purpose controls.
- `analytics`: analytical alerts, report/export intents và operational projections.
- External providers: storage, OCR, signature, messaging, bank, ERP, payroll, BI và infrastructure services.

Luồng document/evidence:

```text
Owning Context resource
→ Documents API
→ File scan/classification/versioning
→ Review/verification/signature
→ Dossier evaluation/freeze
→ owning Context gate decision
```

Luồng notification:

```text
Owning Context intent
→ current authorization/consent/purpose checks
→ Operations notification orchestration
→ Integration channel delivery
→ Activity Interaction when communication occurs
→ Audit evidence
```

Luồng integration:

```text
External provider
→ Integration gateway
→ signature/replay/idempotency validation
→ canonical mapping
→ command to owning Context
→ accepted result
→ reconciliation
```

Luồng operations:

```text
Telemetry or runtime failure
→ operational alert
→ incident/maintenance/recovery workflow
→ owning service action
→ validation
→ Audit evidence
```

Không Context nào trong composite capability được direct-write aggregate của Context khác.

---
# 3. Control Plane, Authorization Plane và Runtime Planes

## 3.1. Platform Context là Control Plane

Platform sở hữu definitions và versioned policies:

- Workflow và Approval definitions.
- Template definitions.
- Retention, deletion và Legal Hold policies.
- Notification policies và template definitions.
- Connector profile definitions và secret references.
- Job schedule definitions.
- Feature Flag definitions và effective configuration.
- SLA/SLO policy definitions.
- Numbering, localization và Business Calendar definitions.

Runtime Contexts lưu exact definition/version reference hoặc immutable execution snapshot đã sử dụng; không tạo configuration registry cạnh tranh.

## 3.2. IAM Context là Authorization Plane

IAM/Security sở hữu:

- User và Service Account identity.
- Roles, permissions, scopes và field authorities.
- Delegation và time-bound grants.
- Break-glass authorization decision.
- Authentication, re-authentication và MFA facts.
- Effective organization/Legal Entity/Project access.

Operations có thể điều phối break-glass request/session, nhưng emergency grant và access decision vẫn thuộc IAM/Security authority.

## 3.3. Participating Runtime Contexts

- `documents`: document/evidence runtime.
- `audit`: immutable Audit runtime.
- `integration`: external transport and reconciliation runtime.
- `operations`: jobs, alerts, notifications orchestration, incidents and recovery runtime.

Mỗi runtime execution phải tham chiếu versioned policy/configuration khi policy có ảnh hưởng đến kết quả.

## 3.4. Không tạo super-context

Không được:

- Tạo schema `runtime_support` gom tất cả tables.
- Cho Operations repository truy cập trực tiếp Document/Audit/Integration aggregates.
- Cho Documents sở hữu provider credentials hoặc job infrastructure.
- Cho Integration sửa source business state trực tiếp.
- Cho Audit trở thành technical-log database.
- Sao chép IAM permissions hoặc Platform configuration thành nguồn authority mới.

---
# 4. Ranh giới sở hữu dữ liệu

## 4.1. Documents Context sở hữu

- File Object, Document Record, Document Version và Document relationships.
- Metadata, classification, sensitivity, access grants, review và verification.
- Malware/DLP result references, integrity hashes, redaction, watermark và secure share.
- OCR/extraction runs, suggestions, confidence và review state.
- Document Generation Run, rendering snapshot và generated artifact.
- Signature Envelope business record, signer snapshot và Signature Evidence.
- Electronic Dossier, checklist, exception, evaluation, freeze và Evidence Package.
- Document retention state, archive state, deletion process, Legal Hold và destruction evidence.

Documents không sở hữu Customer, Asset, Deal, Contract, Payment, Revenue hoặc Commission state. Dossier gate result là evidence/input; owning Context quyết định business transition.

## 4.2. Audit Context sở hữu

- Immutable Business, Access, Security, Administrative, Integration và Operations Audit facts.
- Hash-chain/Merkle/WORM integrity metadata.
- Audit archives, integrity checks và retention state.
- Correlation/causation lineage và audit-query policies.

Audit append-only; correction tạo fact mới liên kết fact cũ. Technical logs không thay Audit.

## 4.3. Integration Context sở hữu

- Connector runtime, Connection instance và provider endpoint references.
- Mapping/Transformation Versions và validation/dry-run results.
- Webhook intake/delivery, signature/replay checks và provider payload references.
- Sync runs, cursors, external IDs, delivery attempts, retries, DLQ và replay state.
- Provider-side messaging/signature/storage/bank/ERP/BI transport.
- External reconciliation cases và connection health.

Integration không quyết định business source of truth. Nó map/transport và gửi command tới owning Context.

## 4.4. Operations Context sở hữu

- Background Job, Job Attempt, Queue/DLQ operational state và replay orchestration.
- Cross-system operational Alert aggregation và Incident linkage.
- Notification orchestration instance, recipients, scheduling, digest và business delivery projection.
- Service/dependency health, operational incidents, maintenance và RCA.
- Backup/Restore/DR evidence và recovery drill results.
- Data Repair/approved transfer orchestration, release/deployment evidence và operational telemetry.
- Support Session và break-glass request/session orchestration.
- Operational dashboards and runtime control records.

Operations không sở hữu domain-specific Alert aggregate khi owning Context đã sở hữu nó, không sở hữu provider transport, không sở hữu IAM emergency grant và không sửa business records trực tiếp.

## 4.5. Related ownership boundaries

- `platform`: definitions, templates, policies, schedules, feature flags và secret references.
- `iam`: principal, Service Account, permission/scope, delegation và emergency grant.
- `party`: Party identity, consent, preferences và contact restrictions.
- `activity`: Task, Interaction và Timeline.
- `marketing`: marketing journey, audience eligibility, suppression và attribution.
- Owning business Contexts: Lead, Product, Deal, Contract, Payment, Revenue, Commission và other business truth.
- `analytics`: certified Metrics, analytical Alerts/Anomalies và governed export/report definitions.
- External systems: bank transaction, payroll, General Ledger và provider-side execution truth.

## 4.6. Notification boundary

Operations sở hữu notification orchestration; Integration sở hữu provider transport; Activity sở hữu canonical Interaction; Party sở hữu consent/restrictions; Marketing sở hữu marketing eligibility; Platform sở hữu notification definitions/templates.

`QUEUED`, `SCHEDULED` hoặc `SENT` không mặc định chứng minh Customer đã nhận hoặc tương tác.

## 4.7. Data Repair boundary

Operations điều phối request, dry run, approval, execution evidence và reconciliation.

Mọi business correction phải được thực hiện bởi approved command/script thuộc owning Context hoặc database migration governed by that Context. Operations không có universal business-write repository.

---
# 5. Nguyên tắc thiết kế cốt lõi

1. File, Document và Dossier là ba lớp khác nhau.
2. Document Version đã xác nhận không được ghi đè.
3. Audit phải append-only.
4. Alert không đồng nghĩa Notification.
5. Notification orchestration không đồng nghĩa Customer Interaction.
6. Integration không được tự quyết định source of truth.
7. Retry phải idempotent.
8. Support access không được vượt permission nghiệp vụ.
9. Data Repair phải có workflow và audit.
10. Backup chưa được restore test không được coi là bảo đảm phục hồi.
11. Mọi runtime execution phải tham chiếu Configuration Version.
12. Mọi file và payload nhạy cảm phải được bảo vệ ở backend và storage layer.

---

# 6. File Object

File Object là binary hoặc external file reference.

Một File Object tối thiểu gồm:

* File code.
* Storage provider.
* Storage key.
* Original filename.
* MIME type.
* Extension.
* Size.
* Hash.
* Encryption reference.
* Upload source.
* Malware scan status.
* DLP classification.
* Created at.
* Retention reference.
* Legal Hold status.

File Object không tự mang đầy đủ ý nghĩa nghiệp vụ.

---

# 7. Document Record

Document Record là bản ghi nghiệp vụ đại diện cho một tài liệu.

Ví dụ:

* CCCD.
* Hộ chiếu.
* Giấy chứng nhận quyền sử dụng đất.
* Hợp đồng.
* Phiếu đặt chỗ.
* Phiếu thu.
* Biên bản đối soát.
* Revenue Statement.
* Commission Statement.
* Chứng từ chuyển tiền.

Một Document Record có thể có nhiều Document Version.

---

# 8. Candidate Document Type vocabulary — pending Documents Context validation

Các nhóm chuẩn:

```text
IDENTITY_DOCUMENT
ADDRESS_DOCUMENT
CUSTOMER_PROFILE_DOCUMENT
FINANCIAL_CAPACITY_DOCUMENT
OWNERSHIP_DOCUMENT
PROPERTY_LEGAL_DOCUMENT
LISTING_DOCUMENT
MANDATE_DOCUMENT
DISTRIBUTION_AGREEMENT
PROPOSAL_DOCUMENT
BOOKING_DOCUMENT
DEPOSIT_DOCUMENT
CONTRACT_DOCUMENT
CONTRACT_APPENDIX
PAYMENT_DOCUMENT
RECEIPT_DOCUMENT
REFUND_DOCUMENT
SETTLEMENT_DOCUMENT
REVENUE_DOCUMENT
COMMISSION_DOCUMENT
TAX_REFERENCE_DOCUMENT
SIGNATURE_EVIDENCE
APPROVAL_EVIDENCE
MARKETING_CONTENT
SYSTEM_EXPORT
AUDIT_EVIDENCE
OTHER
```

Document Type là dictionary có mã cốt lõi ổn định.

---

# 9. Candidate Document lifecycle — pending Documents Context validation

```text
DRAFT
UPLOADING
UPLOADED
SCANNING
SCAN_FAILED
PENDING_CLASSIFICATION
PENDING_REVIEW
PENDING_VERIFICATION
VERIFIED
REJECTED
SUPERSEDED
EXPIRED
REVOKED
ARCHIVED
PENDING_DELETION
DELETED
QUARANTINED
LEGAL_HOLD
```

---

# 10. Document Version

Mỗi Version phải lưu:

* Document ID.
* Version number.
* File Object.
* Source.
* Author/uploader.
* Effective date.
* Expiry date.
* Status.
* Content hash.
* Metadata snapshot.
* Classification snapshot.
* Verification.
* Superseded version.
* Created at.

Không ghi đè file cũ khi người dùng “tải bản mới”.

---

# 11. Phiên bản hiệu lực

Một Document có thể có:

* Latest Version.
* Current Effective Version.
* Last Verified Version.
* Signed Version.
* Archived Version.

Các khái niệm này không mặc định giống nhau.

---

# 12. Candidate Document Source vocabulary — pending validation

```text
USER_UPLOAD
SYSTEM_GENERATED
EXTERNAL_PROVIDER
EMAIL_ATTACHMENT
MESSAGE_ATTACHMENT
SCANNER
MOBILE_CAPTURE
API
IMPORT
SIGNATURE_PROVIDER
STORAGE_LINK
APPROVED_IMPORT
```

---

# 13. Document Metadata

Metadata có thể gồm:

* Document number.
* Issuing authority.
* Issued date.
* Expiry date.
* Party name.
* Asset reference.
* Contract reference.
* Project.
* Currency.
* Amount.
* Language.
* Country.
* Verification source.
* Custom metadata.

Metadata nhạy cảm phải được field-mask.

---

# 14. Document Classification

Phân loại theo:

* Document Type.
* Business domain.
* Sensitivity.
* Personal data class.
* Financial data.
* Legal data.
* Confidentiality.
* Retention class.
* Export class.

Classification có thể:

* User selected.
* Rule-based.
* OCR-assisted.
* AI-assisted.
* Reviewer confirmed.

---

# 15. Candidate Sensitivity vocabulary — pending Data Classification alignment

```text
PUBLIC
INTERNAL
CONFIDENTIAL
HIGHLY_CONFIDENTIAL
RESTRICTED_PERSONAL
RESTRICTED_FINANCIAL
RESTRICTED_LEGAL
RESTRICTED_SECURITY
```

Sensitivity phải ảnh hưởng:

* View.
* Download.
* Share.
* Export.
* Watermark.
* Retention.
* Audit.
* Storage policy.

---

# 16. Candidate Document relationship vocabulary — pending validation

Document có thể liên kết:

```text
PARTY
LEAD
CUSTOMER
REQUIREMENT
PARTNER
PROJECT
ASSET
OWNERSHIP_RECORD
LISTING
MANDATE
DEAL
TRANSACTION_CASE
PROPOSAL
HOLD
BOOKING
CONTRACT
RECEIVABLE
PAYMENT
RECEIPT
REFUND
SETTLEMENT
REVENUE_ENTITLEMENT
COMMISSION_ENTITLEMENT
PAYOUT_BATCH
CAMPAIGN
AUDIT_CASE
INCIDENT
OTHER
```

Mỗi Document có một primary context và nhiều secondary contexts.

---

# 17. Context không mở rộng quyền

User có quyền xem Document metadata không mặc định có quyền xem toàn bộ:

* Customer.
* Contract.
* Revenue.
* Commission.
* Call Transcript.

Quyền thực tế:

```text
Document Capability
∩ Context Resource Access
∩ Sensitivity Policy
∩ Field Permission
∩ Legal Entity Scope
```

---

# 18. Storage Architecture

Hỗ trợ:

* Object Storage nội bộ.
* S3-compatible storage.
* Cloud storage.
* External DMS.
* Secure external URL.
* Provider-specific file reference.

Capability lưu metadata và reference; binary có thể ở hệ thống ngoài.

---

# 19. Storage Policy

Phải xác định:

* Provider.
* Region.
* Encryption.
* Bucket/container.
* Object naming.
* Versioning.
* Access class.
* Retention lock.
* Backup.
* Replication.
* Maximum file size.
* Allowed MIME types.

---

# 20. File Upload

Luồng:

1. Request upload.
2. Backend kiểm tra quyền.
3. Sinh signed upload URL hoặc stream.
4. Upload file.
5. Xác nhận size/hash.
6. Malware scan.
7. DLP/classification.
8. Tạo File Object.
9. Tạo Document Version.
10. Ghi Audit.
11. Phát event.

File chưa scan xong không được đưa vào workflow nhạy cảm.

---

# 21. Multipart Upload

File lớn phải hỗ trợ:

* Multipart session.
* Chunk hash.
* Resume.
* Expiry.
* Abort.
* Final checksum.
* Maximum concurrency.

---

# 22. Candidate Malware Scan lifecycle — pending security-provider validation

Status:

```text
PENDING
SCANNING
CLEAN
SUSPICIOUS
INFECTED
SCAN_FAILED
UNSUPPORTED
```

File `INFECTED` phải:

* Quarantine.
* Chặn view/download.
* Alert Security/Admin.
* Không gắn vào hồ sơ chính thức.
* Giữ evidence theo retention.

---

# 23. Content Hash

Mỗi File Object phải có:

* SHA-256 hoặc algorithm approved.
* Hash algorithm version.
* Hash time.
* Verification status.

Hash dùng:

* Integrity.
* Duplicate detection.
* Evidence.
* Signature package.
* Audit.

---

# 24. Duplicate File Detection

Phân biệt:

* Binary duplicate.
* Same file name.
* Similar scanned document.
* Same business document khác phiên bản.

Binary duplicate không tự có nghĩa là Document duplicate.

---

# 25. External Document

Khi chỉ lưu URL ngoài:

* Provider.
* External file ID.
* URL.
* Permission.
* Last verified.
* Hash nếu lấy được.
* Availability.
* Expiry.
* Sync status.

URL ngoài không được coi luôn tồn tại; phải có health verification.

---

# 26. Document Review

Review có thể kiểm tra:

* Đúng loại.
* Đúng Party.
* Đúng Asset.
* Đúng Contract.
* Đủ trang.
* Đọc được.
* Không hết hạn.
* Không bị sửa.
* Metadata đúng.
* Có chữ ký.
* Có con dấu nếu cần.
* Có approval.

---

# 27. Candidate Verification lifecycle — pending validation

```text
NOT_REQUIRED
PENDING
IN_REVIEW
VERIFIED
VERIFIED_WITH_EXCEPTION
REJECTED
EXPIRED
REVOKED
```

Verified phải có:

* Verifier.
* Method.
* Evidence.
* Time.
* Policy Version.

---

# 28. Candidate Verification methods — pending validation

```text
MANUAL_REVIEW
SOURCE_SYSTEM_CHECK
QR_VERIFICATION
SIGNATURE_CERTIFICATE
GOVERNMENT_REFERENCE
PARTNER_CONFIRMATION
OCR_MATCH
HASH_MATCH
OTHER
```

OCR match đơn thuần không mặc định đủ để xác minh pháp lý.

---

# 29. OCR

OCR hỗ trợ:

* Image.
* PDF.
* Multi-page document.
* Vietnamese và ngôn ngữ được cấu hình.
* Orientation detection.
* Page segmentation.
* Confidence.
* Key-value extraction.
* Table extraction.

---

# 30. OCR Result

Phải lưu:

* Provider/model.
* Model Version.
* Language.
* Raw text reference.
* Structured extraction.
* Confidence từng field.
* Page.
* Bounding box nếu cần.
* Generated at.
* Review status.

---

# 31. OCR Human Review

Trường quan trọng phải được kiểm tra trước khi cập nhật nghiệp vụ:

* Identity number.
* Contract number.
* Amount.
* Bank account.
* Asset identifier.
* Ownership share.
* Dates.
* Party name.

---

# 32. OCR không tự sửa owning Context

OCR có thể tạo:

* Extraction Suggestion.
* Data Validation Task.
* Document Metadata Suggestion.

Không tự sửa Customer, Contract, Payment hoặc Revenue nếu chưa qua API và workflow owning Context.

---

# 33. Document Generation

Tạo tài liệu từ:

* Template Version Platform Configuration Capability.
* Business resource.
* Data snapshot.
* Language.
* Format.
* Branding.
* Legal Entity.
* Numbering.

---

# 34. Generation Snapshot

Phải lưu:

* Template Version.
* Data fields.
* Resource Version.
* User.
* Generated time.
* Locale.
* Currency.
* Numbering.
* Render engine.
* Output hash.

---

# 35. Merge Field

Merge Field phải:

* Có schema.
* Có data source.
* Có required flag.
* Có formatting.
* Có field access check.
* Có missing behavior.

Không cho template truy cập field ngoài allowlist.

---

# 36. Document Format

Hỗ trợ:

* PDF.
* DOCX.
* XLSX.
* Image.
* Text.
* Provider-native format.

Tài liệu ký hoặc khóa nên có immutable PDF representation khi policy yêu cầu.

---

# 37. Electronic Signature

Capability hỗ trợ integration với nhà cung cấp ký điện tử.

Luồng:

```text
Document Version
→ Signature Envelope
→ Signer Authentication
→ Signature Actions
→ Provider Completion
→ Signed Document
→ Certificate/Evidence
→ Verification
→ Dossier Update
```

---

# 38. Signature Envelope

Envelope gồm:

* Provider.
* External envelope ID.
* Document Version.
* Signers.
* Signing order.
* Authentication method.
* Expiry.
* Reminder policy.
* Status.
* Callback status.
* Evidence.

---

# 39. Candidate Signature Envelope lifecycle — pending validation

```text
DRAFT
PENDING_APPROVAL
CREATED
SENT
DELIVERED
VIEWED
PARTIALLY_SIGNED
COMPLETED
DECLINED
EXPIRED
VOIDED
CANCELLED
FAILED
DISPUTED
```

---

# 40. Signer

Signer có:

* Party.
* User hoặc external signer.
* Role.
* Email.
* Phone reference.
* Authentication method.
* Signing order.
* Status.
* Signed at.
* Decline reason.
* Provider evidence.

Không lấy email/số điện thoại trực tiếp từ frontend khi đã có Party Identity chuẩn.

---

# 41. Signature Authentication

Có thể dùng:

* Email link.
* OTP.
* SMS OTP.
* Identity provider.
* Digital certificate.
* Provider verification.
* In-person witness.
* Custom approved method.

---

# 42. Signature Evidence

Lưu:

* Signed file.
* Completion certificate.
* Audit trail.
* Timestamp.
* IP/provider metadata theo policy.
* Authentication evidence.
* Hash.
* Provider signature.
* Certificate chain reference.

---

# 43. Signature Webhook

Webhook phải:

* Verify signature.
* Chống replay.
* Idempotent.
* Kiểm tra envelope mapping.
* Giữ raw payload.
* Không tự chuyển Contract Effective nếu Contract and Cash Capability chưa validate.

---

# 44. Signature Void và Replacement

Khi void:

* Giữ envelope cũ.
* Ghi reason.
* Không xóa signed evidence cũ.
* Tạo envelope mới nếu cần.
* Owning Context quyết định hiệu lực nghiệp vụ.

---

# 45. Redaction

Có thể che:

* Identity number.
* Phone.
* Email.
* Bank account.
* Signature.
* Address.
* Commission.
* Price nội bộ.

Redaction có thể:

* View-time dynamic.
* Export-time.
* Permanent derived copy.

Original phải được giữ theo policy và restricted.

---

# 46. Watermark

Watermark có thể chứa:

* User.
* Time.
* Purpose.
* Confidentiality.
* Document code.
* Download ID.
* “Bản tham khảo”.
* “Không có giá trị ký kết”.

Watermark không thay đổi original file; tạo derived representation.

---

# 47. Secure Sharing

Chia sẻ ngoài hệ thống phải có:

* Recipient.
* Purpose.
* Document Version.
* Expiry.
* Password/OTP nếu cần.
* Download/view limit.
* Watermark.
* Access logging.
* Revocation.
* Approval.

Không gửi public URL vĩnh viễn.

---

# 48. Candidate Secure Share lifecycle — pending validation

```text
DRAFT
PENDING_APPROVAL
ACTIVE
EXPIRED
REVOKED
DOWNLOAD_LIMIT_REACHED
FAILED
```

---

# 49. Document Expiry

Document có thể hết hạn theo:

* Explicit expiry date.
* Policy duration.
* Agreement termination.
* Contract cancellation.
* New version replacement.
* Provider revocation.

Expiry không đồng nghĩa xóa.

---

# 50. Retention

Retention phải dựa trên:

* Document Type.
* Legal Entity.
* Country.
* Business process.
* Contract status.
* Legal Hold.
* Sensitivity.
* Source.

---

# 51. Candidate Retention lifecycle — pending validation

```text
ACTIVE
RETENTION_PENDING
ELIGIBLE_FOR_ARCHIVE
ARCHIVED
ELIGIBLE_FOR_DELETION
DELETION_BLOCKED
DELETED
```

---

# 52. Legal Hold

Legal Hold có thể áp dụng cho:

* Document.
* Dossier.
* Customer.
* Contract.
* Transaction Case.
* Incident.
* Audit range.

Legal Hold chặn:

* Deletion.
* Purge.
* Automatic expiry cleanup.
* Destructive migration.

---

# 53. Candidate Legal Hold lifecycle — pending validation

```text
DRAFT
ACTIVE
RELEASE_PENDING
RELEASED
CANCELLED
```

Legal Hold phải có:

* Reason.
* Scope.
* Authority.
* Start.
* Review date.
* Release approval.

---

# 54. Archive

Archive phải:

* Giữ hash.
* Giữ metadata.
* Giữ access policy.
* Giữ Audit.
* Có thể chuyển storage class.
* Có retrieval SLA.
* Không làm mất legal evidence.

---

# 55. Deletion

Deletion phải:

* Có policy.
* Có eligibility check.
* Kiểm tra Legal Hold.
* Có approval nếu cần.
* Ghi deletion certificate/evidence.
* Xóa secure share.
* Xử lý backup theo policy.
* Giữ tombstone metadata tối thiểu khi cần.

---

# 56. Electronic Dossier

Dossier là tập hợp có cấu trúc của:

* Documents.
* Checklist.
* Reviews.
* Approvals.
* Required evidence.
* Completeness status.
* Snapshot.

Dossier không chỉ là folder.

---

# 57. Candidate Dossier Type vocabulary — pending validation

```text
CUSTOMER_DOSSIER
SELLER_DOSSIER
OWNER_DOSSIER
PARTNER_DOSSIER
PROJECT_DOSSIER
ASSET_LEGAL_DOSSIER
LISTING_DOSSIER
DEAL_DOSSIER
BOOKING_DOSSIER
CONTRACT_DOSSIER
PAYMENT_DOSSIER
REFUND_DOSSIER
SETTLEMENT_DOSSIER
REVENUE_DOSSIER
COMMISSION_DOSSIER
MARKETING_CAMPAIGN_DOSSIER
AUDIT_EVIDENCE_DOSSIER
INCIDENT_DOSSIER
OTHER
```

---

# 58. Candidate Dossier lifecycle — pending validation

```text
DRAFT
OPEN
COLLECTING
PENDING_REVIEW
INCOMPLETE
COMPLETE
COMPLETE_WITH_EXCEPTION
FROZEN
CLOSED
ARCHIVED
LEGAL_HOLD
CANCELLED
```

---

# 59. Dossier Checklist

Checklist item có:

* Required Document Type.
* Required metadata.
* Party role.
* Minimum version.
* Verification level.
* Expiry policy.
* Reviewer.
* Required before milestone.
* Exception rule.

---

# 60. Dossier Completeness

Phải tách:

* Document present.
* Document current.
* Document verified.
* Document approved.
* Document not expired.
* Document matches context.

Completeness không chỉ dựa trên số file.

---

# 61. Candidate Completeness vocabulary — pending validation

```text
NOT_EVALUATED
INCOMPLETE
PARTIALLY_COMPLETE
COMPLETE
COMPLETE_WITH_EXCEPTION
BLOCKED
```

---

# 62. Dossier Gate

Owning Context có thể yêu cầu:

* Booking chỉ submit khi Dossier đạt mức A.
* Contract chỉ ký khi Dossier đạt mức B.
* Receipt chỉ phát hành khi Payment Dossier đủ.
* Payout chỉ approve khi Commission Dossier đủ.

Gate do owning Context enforce qua Dossier API.

---

# 63. Dossier Exception

Exception phải có:

* Missing item.
* Reason.
* Temporary/permanent.
* Risk.
* Approver.
* Expiry.
* Compensating control.
* Follow-up Task.

---

# 64. Dossier Freeze

Freeze tạo snapshot bất biến của:

* Dossier items.
* Document Versions.
* Verification.
* Checklist.
* Completeness.
* Approval.
* Hash.

Dùng tại:

* Booking approval.
* Contract signing.
* Contract effective.
* Payment confirmation.
* Revenue statement approval.
* Payout approval.

---

# 65. Evidence Package

Evidence Package có thể gồm:

* Dossier Snapshot.
* Audit events.
* Signed documents.
* Approvals.
* Payment references.
* Timeline references.
* Hash manifest.
* Export certificate.

Dùng cho:

* Kiểm toán.
* Tranh chấp.
* Legal.
* Partner reconciliation.
* Internal investigation.

---

# 66. Customer Merge và Dossier

Khi Customer merge:

* Dossier được link canonical Customer.
* Giữ original Customer references.
* Không nhân đôi file.
* Không thay Document history.
* Conflict checklist được đánh dấu.
* Access được recalculated.

---

# 67. Contract Amendment và Dossier

Amendment phải:

* Link Contract Version.
* Xác định tài liệu thay thế.
* Giữ signed version cũ.
* Tạo checklist mới nếu cần.
* Không ghi đè Dossier Snapshot tại thời điểm ký cũ.

---

# 68. Multi-Legal Entity Dossier

Dossier phải xác định:

* Owning Legal Entity.
* Participating Legal Entities.
* Shared documents.
* Restricted documents.
* Cross-entity access grant.

Không mặc định chia sẻ toàn bộ tài liệu trong Enterprise.

---

# 69. Audit Architecture

Audit phải bao phủ:

* Business changes.
* Access.
* Approval.
* Security.
* Administration.
* Integration.
* Export.
* Document.
* System operation.

---

# 70. Candidate Audit Event categories — pending Audit Context validation

```text
BUSINESS_CHANGE
STATUS_TRANSITION
ASSIGNMENT_CHANGE
APPROVAL
DATA_ACCESS
SENSITIVE_DATA_ACCESS
DOCUMENT_ACCESS
DOCUMENT_DOWNLOAD
DOCUMENT_SHARE
EXPORT
AUTHENTICATION
AUTHORIZATION
SECURITY
ADMINISTRATION
CONFIGURATION
INTEGRATION
JOB_EXECUTION
DATA_REPAIR
APPROVED_IMPORT
BACKUP_RESTORE
BREAK_GLASS
INCIDENT
OTHER
```

---

# 71. Audit Event Structure

Mỗi Audit Event gồm:

* Event ID.
* Category.
* Action.
* Actor type.
* Actor ID.
* Acting role.
* Delegation.
* Legal Entity.
* Resource type.
* Resource ID.
* Parent resource.
* Before.
* After.
* Changed fields.
* Reason.
* Approval.
* Request ID.
* Correlation ID.
* Causation ID.
* Session.
* IP.
* Device.
* Source system.
* Occurred at.
* Recorded at.
* Hash.
* Previous hash reference nếu dùng chain.

---

# 72. Candidate Audit Actor vocabulary — pending IAM/Audit validation

Actor có thể là:

```text
USER
SERVICE_ACCOUNT
SYSTEM
INTEGRATION
SCHEDULED_JOB
SUPPORT_USER
BREAK_GLASS_USER
EXTERNAL_PROVIDER
ANONYMOUS_EXTERNAL
```

---

# 73. Business Audit và Technical Log

Phải tách:

## Business Audit

* Ai đổi trạng thái.
* Ai sửa amount.
* Ai approve.
* Ai reassign.
* Ai export.

## Technical Log

* Stack trace.
* Runtime error.
* Query performance.
* Service logs.

Technical log có retention và quyền khác Business Audit.

---

# 74. Data Access Audit

Bắt buộc với:

* Customer PII.
* Phone.
* Identity document.
* Financial Profile.
* Bank data.
* Floor Price.
* Contract sensitive term.
* Revenue Arrangement.
* Commission.
* Call Recording.
* Transcript.
* Document restricted.

---

# 75. Audit Immutability

Audit không được:

* Update.
* Delete.
* Reorder.
* Replace.

Correction phải tạo Audit Event mới liên kết event cũ.

---

# 76. Tamper Evidence

Có thể dùng:

* Hash từng event.
* Hash chain.
* Batch Merkle root.
* WORM storage.
* Signed archive.
* External timestamping.

Mức áp dụng theo policy và mức độ rủi ro.

---

# 77. Audit Partitioning

Có thể partition theo:

* Month.
* Legal Entity.
* Domain.
* Severity.
* Retention class.

Partition không được làm mất query lineage.

---

# 78. Audit Search

Có thể tìm theo:

* User.
* Resource.
* Action.
* Date.
* Legal Entity.
* Request ID.
* Correlation ID.
* IP.
* Sensitive access.
* Export.
* Break-glass.
* Integration.

---

# 79. Audit Visibility

Không phải user xem resource đều xem được toàn Audit.

Quyền tách:

* View business history.
* View approval history.
* View access history.
* View security audit.
* View admin audit.
* Export audit.

---

# 80. Audit Retention

Audit retention có thể lâu hơn dữ liệu nghiệp vụ.

Audit deletion nếu được phép phải:

* Theo policy.
* Ngoài Legal Hold.
* Có approval.
* Có destruction evidence.
* Không làm mất nghĩa vụ kiểm toán.

---

# 81. Audit Privacy

Audit có thể chứa dữ liệu nhạy cảm.

Phải:

* Hạn chế before/after full payload.
* Mask field.
* Lưu hash/reference khi đủ.
* Không ghi password, token, secret.
* Không ghi full payment credential.

---

# 82. Alert và Notification là hai lớp khác nhau

## Alert

Biểu thị vấn đề, rủi ro hoặc tình trạng cần xử lý.

## Notification

Là thông điệp được gửi đến một hoặc nhiều người.

Một Alert có thể tạo nhiều Notification.

Một Notification có thể không liên quan Alert.

---

# 83. Alert Source

Alert có thể từ:

* Business rule.
* SLA.
* Data Quality.
* Security.
* Integration.
* Job.
* System Health.
* Budget.
* Contract.
* Payment.
* Revenue.
* Commission.
* Marketing.
* Analytics.

---

# 84. Candidate Operational Alert severity — pending Operations policy

```text
INFO
LOW
MEDIUM
HIGH
CRITICAL
```

Severity phải dựa trên policy có version.

---

# 85. Candidate Operational Alert lifecycle — pending validation

```text
NEW
OPEN
ACKNOWLEDGED
ASSIGNED
INVESTIGATING
WAITING_EXTERNAL
MITIGATED
RESOLVED
FALSE_POSITIVE
SUPPRESSED
CLOSED
```

---

# 86. Alert Fingerprint

Fingerprint dùng gộp Alert dựa trên:

* Rule.
* Resource.
* Scope.
* Error code.
* Time window.
* Dimension.

Không tạo Alert mới mỗi lần poll nếu vấn đề chưa được giải quyết.

---

# 87. Alert Aggregation

Có thể gộp:

* Nhiều Payment allocation failure.
* Nhiều webhook failure cùng provider.
* Nhiều stale projection.
* Nhiều Lead source mapping lỗi.
* Nhiều Customer bị gửi message trái rule.

---

# 88. Alert Suppression

Suppression dùng khi:

* Maintenance Window.
* Known issue.
* Test environment.
* Temporary approved exception.
* Duplicate incident.

Suppression không xóa event gốc.

---

# 89. Alert Escalation

Escalation có thể theo:

* Severity.
* Time open.
* Legal Entity.
* Service owner.
* Business owner.
* On-call.
* Department hierarchy.

---

# 90. Alert Assignment

Alert có:

* Owner.
* Assigned user/team.
* Due time.
* SLA.
* Related Incident.
* Related Task.
* Resolution.

---

# 91. Alert Resolution

Phải có:

* Resolution code.
* Root cause hoặc known cause.
* Action taken.
* Evidence.
* Resolved by.
* Resolved at.
* Validation.

Không cho close Critical Alert chỉ bằng note rỗng.

---

# 92. Candidate Notification Type vocabulary — pending validation

```text
INFORMATIONAL
ACTION_REQUIRED
APPROVAL_REQUIRED
REMINDER
SLA_WARNING
SLA_BREACH
SECURITY
SYSTEM
DOCUMENT
SIGNATURE
INTEGRATION
INCIDENT
REPORT_READY
EXPORT_READY
TRANSACTIONAL_CUSTOMER
MARKETING_REFERENCE
OTHER
```

---

# 93. Candidate Notification Channel vocabulary — pending Integration availability

```text
IN_APP
EMAIL
SMS
PUSH
ZALO
WHATSAPP
CHAT
WEBHOOK
VOICE_REFERENCE
OTHER
```

Channel phải được bật theo Platform Configuration Capability và integration availability.

---

# 94. Notification Recipient

Recipient có thể được resolve từ:

* User.
* Role.
* Team.
* Department.
* Manager.
* Resource owner.
* Assignee.
* Approver.
* Customer.
* Partner.
* External address.

Recipient resolution phải snapshot tại lúc gửi.

---

# 95. Notification Template

Notification dùng Template Version Platform Configuration Capability.

Runtime lưu:

* Template Version.
* Rendering input.
* Rendered hash.
* Locale.
* Channel.
* Recipient.
* Sensitivity.
* Action link.

---

# 96. Notification Localization

Hỗ trợ:

* Language.
* Timezone.
* Number.
* Currency.
* Date format.
* Legal Entity branding.
* Channel length restrictions.

---

# 97. Notification Preference

User preference có thể gồm:

* Channel enabled.
* Digest.
* Quiet hours.
* Severity threshold.
* Category.
* Immediate/daily/weekly.

Critical security notification có thể bỏ qua một số preference theo policy.

---

# 98. Customer Notification

Customer-facing Notification orchestration phải:

* Kiểm tra consent/purpose phù hợp.
* Phân biệt transactional và marketing.
* Kiểm tra contact restriction.
* Kiểm tra Quiet Hours nếu áp dụng.
* Yêu cầu Activity Context ghi canonical Interaction khi communication được accepted/executed.
* Không lưu nội dung song song gây phân mảnh.

---

# 99. Transactional và Marketing

## Transactional

* Contract signature.
* Payment reminder.
* Receipt.
* Appointment.
* Service update.

## Marketing

* Promotion.
* Campaign.
* Project invitation.
* Nurture.

Marketing intent phải đi qua Marketing Context eligibility/journey; Operations điều phối và Integration vận hành delivery khi request hợp lệ.

---

# 100. Candidate Notification lifecycle — pending validation

```text
DRAFT
PENDING_RENDER
PENDING_ELIGIBILITY
SUPPRESSED
QUEUED
SCHEDULED
SENDING
SENT
DELIVERED
READ
ACTIONED
FAILED
BOUNCED
EXPIRED
CANCELLED
```

---

# 101. Delivery Attempt

Mỗi attempt lưu:

* Provider.
* Credential reference.
* External ID.
* Attempt number.
* Request hash.
* Sent at.
* Response.
* Error.
* Retryability.
* Delivery status.

---

# 102. Notification Retry

Retry phải:

* Dựa trên error class.
* Có backoff.
* Có maximum attempts.
* Idempotency.
* Không gửi duplicate.
* Dừng khi notification expired hoặc recipient bị suppress.

---

# 103. Notification Digest

Có thể gộp:

* Task reminder.
* Daily summary.
* Weekly KPI.
* Alert digest.
* Approval digest.

Critical Alert không được trì hoãn vào digest nếu policy yêu cầu real-time.

---

# 104. Secure Action Link

Action link phải:

* Short-lived.
* User-bound hoặc recipient-bound.
* Scope-bound.
* Single-use nếu cần.
* Không chứa secret trong URL.
* Re-authentication cho hành động nhạy cảm.
* Audit click/action.

---

# 105. Notification Content Security

Không đưa vào subject/push preview:

* Full identity number.
* Bank account.
* Full Commission.
* Password.
* Secret.
* Sensitive document URL.

---

# 106. Integration Hub – Vai trò

Integration Hub quản lý runtime kết nối giữa CRM và:

* Email.
* Calendar.
* Telephony.
* Messaging.
* Ad platform.
* Analytics.
* Storage.
* Signature provider.
* Payment gateway.
* Bank.
* ERP.
* Payroll.
* Identity provider.
* Document provider.
* BI.
* Partner system.
* Custom API.

---

# 107. Candidate Connector Type vocabulary — pending Integration Context validation

```text
EMAIL
CALENDAR
TELEPHONY
MESSAGING
AD_PLATFORM
ANALYTICS
FILE_STORAGE
E_SIGNATURE
PAYMENT
BANK
ERP
PAYROLL
IDENTITY_PROVIDER
CRM
BI
WEBHOOK
CUSTOM_API
DATABASE_REFERENCE
OTHER
```

---

# 108. Integration Connection

Connection Instance gồm:

* Connector Type.
* Provider.
* Environment.
* Legal Entity.
* Account.
* Credential reference Platform Configuration Capability.
* Service account Identity, Access and Organization Capability.
* Endpoint.
* Scope.
* Status.
* Health.
* Rate limits.
* Data ownership rules.
* Effective dates.

---

# 109. Candidate Connection lifecycle — pending validation

```text
DRAFT
PENDING_CREDENTIAL
PENDING_TEST
ACTIVE
DEGRADED
SUSPENDED
AUTHENTICATION_FAILED
RATE_LIMITED
DISCONNECTED
EXPIRED
DECOMMISSIONED
```

---

# 110. Credential Boundary

Integration Context không lưu plain secret.

Chỉ lưu:

* Secret reference.
* Credential version.
* Last rotated.
* Expiry.
* Health.

Secret material thuộc approved vault; Platform sở hữu secret reference definitions, Integration chỉ dùng reference/version.

---

# 111. Candidate Integration Direction vocabulary — pending validation

```text
INBOUND
OUTBOUND
BIDIRECTIONAL
EVENT_ONLY
QUERY_ON_DEMAND
BATCH_IMPORT
BATCH_EXPORT
```

---

# 112. Candidate Integration Mode vocabulary — pending validation

```text
REAL_TIME_WEBHOOK
NEAR_REAL_TIME
SCHEDULED_SYNC
MANUAL_SYNC
ON_DEMAND
FILE_EXCHANGE
API_REQUEST_RESPONSE
EVENT_STREAM
```

---

# 113. Canonical Integration Schema

Dữ liệu ngoài phải map vào canonical schema trước khi gọi owning Context.

Ví dụ:

* External Lead → Canonical Lead Intake.
* External Payment → Canonical Payment Candidate.
* External Email → Canonical Interaction.
* External Campaign → Marketing Channel Execution.

---

# 114. Field Mapping

Mapping gồm:

* Source field.
* Target field.
* Data type.
* Required.
* Default.
* Transformation.
* Lookup.
* Code mapping.
* Null policy.
* Validation.
* Sensitivity.

---

# 115. Mapping Version

Mapping active không sửa trực tiếp.

Version mới phải có:

* Effective date.
* Compatibility.
* Sample test.
* Dry run.
* Impact.
* Approval.

---

# 116. Transformation

Hỗ trợ an toàn:

* Trim.
* Normalize.
* Date parse.
* Number parse.
* Currency conversion reference.
* Code mapping.
* Concatenate.
* Split.
* Conditional.
* Lookup.
* Hashing.
* Masking.

Không chạy arbitrary code production.

---

# 117. Integration Validation

Kiểm tra:

* Schema.
* Required fields.
* Data type.
* Referential integrity.
* Business preconditions.
* Duplicates.
* Idempotency.
* Permission.
* Source signature.
* Data ownership.

---

# 118. Sync Job

Sync Job gồm:

* Connection.
* Direction.
* Resource.
* Mapping Version.
* Cursor.
* Time window.
* Status.
* Counts.
* Errors.
* Reconciliation.

---

# 119. Candidate Sync lifecycle — pending validation

```text
QUEUED
RUNNING
PARTIALLY_COMPLETED
COMPLETED
COMPLETED_WITH_WARNINGS
FAILED
CANCELLED
RETRYING
RECONCILIATION_REQUIRED
```

---

# 120. Sync Cursor

Cursor có thể là:

* Timestamp.
* Sequence.
* Page token.
* Change token.
* Event offset.
* Provider cursor.

Cursor chỉ cập nhật sau khi dữ liệu được xử lý thành công theo policy.

---

# 121. Inbound Webhook

Gateway phải:

* Xác định provider.
* Verify signature.
* Chống replay.
* Rate limit.
* Lưu raw payload reference.
* Tạo idempotency key.
* Route.
* Trả acknowledgment.
* Xử lý async.
* Ghi Audit.

---

# 122. Outbound Webhook

Subscription gồm:

* Subscriber.
* Event types.
* Endpoint.
* Secret reference.
* Filter.
* Payload schema version.
* Retry.
* Rate limit.
* Effective dates.

---

# 123. Candidate Webhook Delivery lifecycle — pending validation

```text
PENDING
DELIVERING
DELIVERED
FAILED_RETRYABLE
FAILED_FINAL
DISABLED
EXPIRED
```

---

# 124. Webhook Signature

Hỗ trợ:

* HMAC.
* Asymmetric signature.
* Provider-specific signature.
* Timestamp.
* Nonce.
* Replay window.

---

# 125. Idempotency

Mỗi integration action phải có idempotency key dựa trên:

* Provider.
* External event ID.
* Resource.
* Operation.
* Payload hash.

Cùng key và cùng payload trả cùng kết quả.

Cùng key nhưng payload khác phải conflict.

---

# 126. Integration Retry

Retry policy:

* Maximum attempts.
* Exponential backoff.
* Retryable status.
* Provider rate limit.
* Timeout.
* Circuit breaker.
* DLQ.

---

# 127. Dead-letter Queue

DLQ item phải có:

* Original payload reference.
* Error.
* Attempts.
* Mapping Version.
* Connection.
* Resource.
* Created at.
* Replay status.
* Assigned owner.

---

# 128. Replay

Replay phải:

* Có permission.
* Có reason.
* Giữ original idempotency lineage.
* Có dry run nếu cần.
* Không tạo duplicate.
* Ghi Audit.

---

# 129. Rate Limiting

Áp dụng theo:

* Connection.
* Provider.
* Endpoint.
* User.
* Legal Entity.
* Operation.

Phải hỗ trợ provider quota và internal safety limit.

---

# 130. Circuit Breaker

Khi provider lỗi liên tục:

* Mở circuit.
* Dừng request mới.
* Alert.
* Chờ cooldown.
* Health probe.
* Half-open.
* Resume có kiểm soát.

---

# 131. Integration Reconciliation

Đối soát:

* Record count.
* External IDs.
* Status.
* Amount.
* Hash.
* Updated time.
* Missing records.
* Duplicate records.
* Divergent records.

---

# 132. Candidate Integration Reconciliation vocabulary — pending validation

```text
MATCHED
MISSING_INTERNAL
MISSING_EXTERNAL
VALUE_MISMATCH
STATUS_MISMATCH
DUPLICATE
STALE_EXTERNAL
STALE_INTERNAL
UNRESOLVED_IDENTITY
REQUIRES_REVIEW
```

---

# 133. Candidate Conflict Resolution strategies — source-of-truth policy required

Với bidirectional sync:

```text
CRM_WINS
EXTERNAL_WINS
LATEST_VALID_UPDATE
FIELD_LEVEL_MERGE
MANUAL_REVIEW
SOURCE_OF_TRUTH_POLICY
```

Không dùng `latest update wins` mặc định cho dữ liệu tài chính hoặc pháp lý.

---

# 134. Source of Truth Registry

Mỗi integration resource phải xác định:

* Source of truth.
* Authoritative fields.
* Read-only fields.
* Sync direction.
* Conflict policy.
* Correction path.

---

# 135. Data Minimization

Chỉ truyền:

* Field cần thiết.
* Đúng purpose.
* Đúng provider.
* Đúng Legal Entity.
* Đúng retention.

Không gửi toàn Customer 360 khi provider chỉ cần email.

---

# 136. Integration Sandbox

Trước production phải có:

* Test Connection.
* Sample payload.
* Mapping test.
* Authentication test.
* Permission test.
* Error simulation.
* Rate-limit simulation.
* Idempotency test.
* Reconciliation test.

---

# 137. Integration Go-live

Yêu cầu:

* Approved Mapping Version.
* Credential active.
* Service account active.
* Monitoring.
* Alert route.
* Rollback plan.
* Data ownership.
* Retention.
* Security review.
* Business owner approval.

---

# 138. Integration Decommission

Phải:

* Ngừng schedule.
* Disable webhooks.
* Revoke credential.
* Export reconciliation.
* Xử lý pending queue.
* Retain Audit.
* Xác định data retention.
* Cập nhật dependent workflows.

---

# 139. Background Job Runtime

Capability quản lý runtime của:

* Scheduled Job.
* Domain event consumer.
* Batch process.
* Report generation.
* Document generation.
* OCR.
* Signature sync.
* Notification send.
* Data import.
* Export.
* Projection refresh.
* Retention purge.
* Backup.
* Reconciliation.

---

# 140. Candidate Job lifecycle — pending Operations Context validation

```text
CREATED
QUEUED
SCHEDULED
RUNNING
PAUSED
RETRYING
PARTIALLY_COMPLETED
COMPLETED
COMPLETED_WITH_WARNINGS
FAILED
CANCELLED
EXPIRED
DEAD_LETTERED
```

---

# 141. Job Instance

Lưu:

* Job definition/version.
* Trigger.
* Scope.
* Parameters.
* Requested by.
* Started/completed.
* Progress.
* Counts.
* Errors.
* Retry.
* Idempotency.
* Correlation.

---

# 142. Queue

Queue có:

* Queue code.
* Purpose.
* Priority.
* Concurrency.
* Consumer group.
* Retry policy.
* Retention.
* DLQ.
* Health.

---

# 143. Candidate Queue Priority vocabulary — pending validation

```text
CRITICAL
HIGH
NORMAL
LOW
BULK
MAINTENANCE
```

Không để bulk import chặn Payment hoặc Contract event quan trọng.

---

# 144. Batch Processing

Batch lớn phải hỗ trợ:

* Chunking.
* Resume.
* Progress.
* Partial failure.
* Checkpoint.
* Rate limit.
* Cancellation.
* Result report.

---

# 145. Job Retry

Retry không được:

* Tạo Lead trùng.
* Phát hành Receipt trùng.
* Gửi notification trùng.
* Tạo payout trùng.
* Tạo document trùng.

---

# 146. Job Cancellation

Cancellation phải phân biệt:

* Requested.
* Graceful stopping.
* Force stopped.
* Cannot cancel.
* Completed before cancel.

Cancellation không tự rollback nghiệp vụ đã commit.

---

# 147. Maintenance Window

Maintenance Window gồm:

* Environment.
* Services.
* Start/end.
* Expected impact.
* Read-only mode.
* Notification.
* Suppression rules.
* Rollback.
* Status.

---

# 148. Candidate Maintenance lifecycle — pending validation

```text
PLANNED
APPROVED
ANNOUNCED
ACTIVE
EXTENDED
COMPLETED
CANCELLED
FAILED
```

---

# 149. Operational Incident

Incident là sự cố có ảnh hưởng rộng hơn một Alert đơn lẻ.

Ví dụ:

* Payment integration outage.
* Storage outage.
* Data leak suspicion.
* Database degradation.
* Notification provider failure.
* Analytics stale toàn hệ thống.

---

# 150. Candidate Incident Severity vocabulary — pending Operations policy

```text
SEV1_CRITICAL
SEV2_HIGH
SEV3_MEDIUM
SEV4_LOW
```

Severity dựa trên:

* User impact.
* Financial impact.
* Data integrity.
* Security.
* Duration.
* Legal impact.
* Scope.

---

# 151. Candidate Incident lifecycle — pending validation

```text
DECLARED
TRIAGING
INVESTIGATING
MITIGATING
MONITORING
RESOLVED
POSTMORTEM_PENDING
CLOSED
```

---

# 152. Incident Record

Gồm:

* Incident code.
* Severity.
* Title.
* Services.
* Legal Entities.
* Started/detected.
* Declared by.
* Commander.
* Impact.
* Timeline.
* Alerts.
* Tasks.
* Communications.
* Mitigation.
* Resolution.
* Root cause.
* Follow-up actions.

---

# 153. Incident Timeline

Mọi sự kiện:

* Detection.
* Escalation.
* Decision.
* Deployment.
* Rollback.
* Recovery.
* Communication.

Timeline không sửa trực tiếp.

---

# 154. Incident Communication

Có thể thông báo:

* Internal users.
* Management.
* Support.
* Customers nếu cần.
* Partners.
* Regulators theo process ngoài.

Nội dung phải approved theo severity/policy.

---

# 155. Root Cause Analysis

RCA gồm:

* What happened.
* Impact.
* Detection gap.
* Root cause.
* Contributing factors.
* Timeline.
* Recovery.
* Preventive actions.
* Owners.
* Due dates.

Không dùng RCA để thay audit kỹ thuật.

---

# 156. System Health

Health theo:

* Service.
* Database.
* Queue.
* Storage.
* Integration.
* Job.
* API.
* Cache.
* Search.
* Notification.
* Signature.
* Backup.

---

# 157. Candidate Health Status vocabulary — pending observability contract

```text
HEALTHY
DEGRADED
UNHEALTHY
UNAVAILABLE
MAINTENANCE
UNKNOWN
```

---

# 158. Dependency Health

Service Health phải biết:

* Upstream.
* Downstream.
* Criticality.
* Current status.
* Last successful call.
* Error rate.
* Latency.

---

# 159. Observability

Theo dõi:

* Request volume.
* Error rate.
* Latency.
* Queue lag.
* Job duration.
* Webhook failures.
* Notification delivery.
* Storage errors.
* Database health.
* Integration quota.
* Backup status.
* Audit ingestion.

---

# 160. Log và Trace

Phải hỗ trợ:

* Structured logs.
* Correlation ID.
* Request ID.
* Trace ID.
* Service.
* Environment.
* Severity.
* PII masking.
* Retention.

Không ghi secret hoặc full sensitive payload vào log.

---

# 161. Data Repair

Data Repair là thay đổi dữ liệu có kiểm soát khi:

* Approved data transfer hoặc schema transition lỗi.
* Projection sai.
* Mapping sai.
* Orphan link.
* Duplicate system record.
* Corrupted metadata.

---

# 162. Data Repair Workflow

1. Phát hiện.
2. Tạo Repair Request.
3. Xác định source of truth.
4. Dry run.
5. Impact analysis.
6. Review.
7. Approval.
8. Execute.
9. Validate.
10. Reconcile.
11. Close.
12. Audit.

---

# 163. Data Repair không dùng SQL tùy tiện

Production repair nên dùng:

* Versioned script.
* Approved command.
* Scoped records.
* Dry run.
* Checksum.
* Rollback/compensation plan.
* Audit.

---

# 164. Approved Data Transfer or Schema Transition Run

Approved data transfer hoặc schema transition gồm:

* Source.
* Target.
* Mapping Version.
* Scope.
* Batch.
* Validation.
* Error report.
* Reconciliation.
* Cutover.
* Rollback.

---

# 165. Backup

Backup theo:

* Database.
* Object storage metadata.
* Documents.
* Config.
* Audit.
* Snapshot.
* Secrets reference metadata.

Secret actual backup theo vault policy riêng.

---

# 166. Backup Status

```text
SCHEDULED
RUNNING
COMPLETED
COMPLETED_WITH_WARNINGS
FAILED
EXPIRED
DELETED
```

---

# 167. Backup Evidence

Lưu:

* Backup ID.
* Type.
* Scope.
* Start/end.
* Size.
* Encryption.
* Storage.
* Checksum.
* Retention.
* Verification.
* Restore-tested status.

---

# 168. Restore

Restore phải có:

* Backup reference.
* Target environment.
* Scope.
* Point in time.
* Requested by.
* Approval.
* Started/completed.
* Validation.
* Data loss estimate.
* Result.

---

# 169. Restore Drill

Phải thực hiện định kỳ:

* Restore vào môi trường cô lập.
* Validate database.
* Validate documents.
* Validate audit.
* Validate integrations disabled.
* Measure RTO.
* Record gaps.

---

# 170. Disaster Recovery

DR Plan gồm:

* Critical services.
* Dependencies.
* Alternate infrastructure.
* Failover.
* Data replication.
* Communication.
* RPO.
* RTO.
* Return-to-primary.

---

# 171. RPO và RTO

Mỗi service class phải có:

* Recovery Point Objective.
* Recovery Time Objective.
* Actual achieved.
* Last test.
* Gap.
* Remediation.

---

# 172. Candidate Environment vocabulary — pending deployment standards

Các môi trường:

```text
DEVELOPMENT
TEST
STAGING
UAT
PRODUCTION
DISASTER_RECOVERY
```

Không dùng production credential/data thật trong non-production trái policy.

---

# 173. Test Data

Test data phải:

* Synthetic hoặc masked.
* Không chứa secret.
* Không chứa full Customer PII trái policy.
* Có expiry.
* Có nguồn.

---

# 174. Release Metadata

Release gồm:

* Version.
* Commit/build reference.
* Components.
* Environment.
* Release notes.
* Database schema transitions.
* Feature Flags.
* Approvals.
* Deployment status.
* Rollback status.

---

# 175. Candidate Deployment lifecycle — pending release standards

```text
PLANNED
PENDING_APPROVAL
DEPLOYING
VERIFYING
COMPLETED
FAILED
ROLLED_BACK
PARTIALLY_ROLLED_BACK
CANCELLED
```

---

# 176. Feature Flag operational observation

Platform Context sở hữu Feature Flag definition và effective configuration.

Operations có thể theo dõi operational rollout telemetry:

* Environment state.
* Effective audience.
* Activation time.
* Evaluation errors.
* Rollout percentage.
* Rollback.
* Runtime audit.

---

# 177. Support Access

Support user có thể cần:

* Xem lỗi.
* Xem metadata.
* Replay Job.
* Kiểm tra Integration.
* Hỗ trợ user.

Không mặc định được xem:

* Full Customer PII.
* Bank data.
* Commission.
* Document restricted.

---

# 178. Break-glass Access

Chỉ dùng khi:

* Incident nghiêm trọng.
* Không có phương án thông thường.
* Có authority.
* Có thời hạn.
* Có re-authentication/MFA.
* Có reason.
* Có session recording/logging phù hợp.
* Có post-review.

---

# 179. Candidate Break-glass session lifecycle — pending IAM/Security validation

```text
REQUESTED
APPROVED
ACTIVE
EXPIRED
REVOKED
COMPLETED
UNDER_REVIEW
```

---

# 180. Break-glass không thay business authorization invariants

IAM/Security có thể cấp emergency grant tạm thời; Operations điều phối session, nhưng:

* Không thay resource owner.
* Không thay approval authority.
* Không thay commission.
* Không xóa audit.
* Mọi access bị ghi chi tiết.

---

# 181. Candidate user experience — Document Center

Các khu vực:

1. Documents.
2. Recent uploads.
3. Pending scan.
4. Pending verification.
5. Expiring.
6. Rejected.
7. Quarantined.
8. Legal Hold.
9. Archive.
10. Secure shares.
11. Audit.

---

# 182. Candidate user experience — Document Detail

Các tab:

* Overview.
* Versions.
* Contexts.
* Metadata.
* Verification.
* OCR.
* Signature.
* Access.
* Sharing.
* Retention.
* History.
* Audit.

---

# 183. Candidate user experience — Dossier Center

Bộ lọc:

* Dossier Type.
* Status.
* Completeness.
* Legal Entity.
* Project.
* Customer.
* Contract.
* Missing documents.
* Expiring documents.
* Reviewer.
* Legal Hold.

---

# 184. Candidate user experience — Dossier Detail

Các tab:

1. Summary.
2. Checklist.
3. Documents.
4. Missing items.
5. Reviews.
6. Exceptions.
7. Snapshot.
8. Evidence Package.
9. History.
10. Audit.

---

# 185. Candidate user experience — Audit Explorer

Chức năng:

* Search.
* Filter.
* Correlation view.
* Resource history.
* User activity.
* Sensitive access.
* Export activity.
* Break-glass.
* Integration.
* Hash verification.

---

# 186. Candidate user experience — Alert Center

Hiển thị:

* New.
* Critical.
* Assigned to me.
* Unacknowledged.
* Overdue.
* Suppressed.
* Related incidents.
* Resolved.
* False positive.

---

# 187. Candidate user experience — Notification Center

Hiển thị:

* Unread.
* Action required.
* Approvals.
* Document.
* Signature.
* System.
* Alerts.
* Reports.
* Delivery failures.

---

# 188. Candidate user experience — Integration Hub

Các khu vực:

1. Connections.
2. Connectors.
3. Mapping.
4. Sync Jobs.
5. Webhooks.
6. DLQ.
7. Reconciliation.
8. Credentials health.
9. Provider quota.
10. Audit.

---

# 189. Candidate user experience — System Operations Center

Hiển thị:

* Service Health.
* Queue Health.
* Job Health.
* Integration Health.
* Storage.
* Backup.
* Incidents.
* Maintenance.
* Deployments.
* Data Repair.
* DR status.

---

# 190. Candidate operational dashboard — System Administrator

* Active incidents.
* Failed jobs.
* Queue lag.
* Integration failures.
* Notification failures.
* Storage usage.
* Backup status.
* Restore test.
* Audit ingestion.
* Credential expiry.
* Maintenance schedule.

---

# 191. Candidate operational dashboard — Compliance/Audit

* Sensitive data access.
* Document downloads.
* Secure shares.
* Exports.
* Break-glass sessions.
* Legal Holds.
* Audit integrity.
* Retention exceptions.
* Failed access attempts.
* Admin operations.

---

# 192. Candidate operational dashboard — Business Operations

* Incomplete Dossiers.
* Expiring documents.
* Signature pending.
* Integration backlog.
* Business alerts.
* Notification failure.
* SLA.
* Evidence package readiness.

---

# 193. Candidate operational reports — not certified Analytics or statutory reports

> Certified Metrics thuộc Analytics Context; statutory reports thuộc external systems. Các mục dưới đây chỉ là operational questions/views.

## Document

* Document master.
* Version history.
* Document by type.
* Expiring documents.
* Rejected documents.
* Verification status.
* OCR status.
* Signature status.
* Downloads.
* Shares.
* Legal Hold.
* Retention.

## Dossier

* Dossier completeness.
* Missing checklist.
* Exception.
* Frozen snapshots.
* Evidence packages.
* Dossier cycle time.

## Audit

* Business changes.
* Sensitive access.
* Document access.
* Export.
* Break-glass.
* Admin actions.
* Integration.
* Data repair.
* Audit integrity.

## Alert và Notification

* Alerts by severity.
* Alert aging.
* Resolution time.
* False positives.
* Notification delivery.
* Bounce/failure.
* Notification latency.
* Provider performance.

## Integration

* Connection health.
* Sync runs.
* Webhook delivery.
* DLQ.
* Replay.
* Mapping errors.
* Reconciliation differences.
* Provider quota.

## Operations

* Job success.
* Queue lag.
* Incident.
* MTTA.
* MTTR.
* Backup.
* Restore.
* RPO/RTO.
* Deployment.
* Maintenance.

---

# 194. Candidate data model — not canonical physical schemas

> **Classification:** `MULTI-CONTEXT DESIGN INPUT / PENDING DECOMPOSITION`
> Các tables dưới đây phải được tách vào `documents`, `audit`, `integration` hoặc `operations`; không tạo schema tổng hợp. Exact columns, constraints, indexes, partitions và cross-context references chỉ có hiệu lực qua Context-specific DB Specifications và Alembic migrations.

## 194.1. File và Document

### `file_objects`

* `id`
* `file_code`
* `storage_provider`
* `storage_container`
* `storage_key`
* `external_file_id`
* `original_filename`
* `mime_type`
* `file_extension`
* `size_bytes`
* `hash_algorithm`
* `content_hash`
* `encryption_reference`
* `upload_source`
* `malware_scan_status`
* `dlp_classification`
* `retention_policy_id`
* `legal_hold_status`
* `created_by`
* `created_at`

### `documents`

* `id`
* `document_code`
* `enterprise_id`
* `legal_entity_id`
* `document_type`
* `title`
* `primary_context_type`
* `primary_context_id`
* `sensitivity_level`
* `status`
* `current_version`
* `effective_version_id`
* `retention_policy_id`
* `created_by`
* `created_at`
* `updated_at`

### `document_versions`

* `id`
* `document_id`
* `version_number`
* `file_object_id`
* `source_type`
* `source_reference`
* `metadata_snapshot_json`
* `classification_snapshot_json`
* `effective_from`
* `effective_to`
* `expiry_at`
* `verification_status`
* `status`
* `supersedes_version_id`
* `created_by`
* `created_at`

### `document_context_links`

* `id`
* `document_id`
* `context_type`
* `context_id`
* `relationship_type`
* `is_primary`
* `created_at`

### `document_metadata_values`

* `id`
* `document_version_id`
* `metadata_key`
* `value_type`
* `value_text`
* `value_number`
* `value_date`
* `value_json`
* `sensitivity_level`
* `source_type`
* `confidence_score`
* `created_at`

---

## 194.2. Scan, OCR và Verification

### `file_scan_runs`

* `id`
* `file_object_id`
* `scan_provider`
* `scan_engine_version`
* `status`
* `result_json`
* `started_at`
* `completed_at`
* `created_at`

### `document_ocr_runs`

* `id`
* `document_version_id`
* `provider`
* `model_version`
* `language_code`
* `status`
* `raw_text_reference`
* `average_confidence`
* `started_at`
* `completed_at`
* `created_at`

### `document_extraction_results`

* `id`
* `ocr_run_id`
* `field_code`
* `extracted_value_json`
* `confidence_score`
* `page_number`
* `bounding_box_json`
* `review_status`
* `reviewed_value_json`
* `reviewed_by`
* `reviewed_at`
* `created_at`

### `document_verifications`

* `id`
* `document_version_id`
* `verification_method`
* `verification_policy_version`
* `status`
* `evidence_reference`
* `verified_by`
* `verified_at`
* `expiry_at`
* `notes`
* `created_at`

---

## 194.3. Document Access và Sharing

### `document_access_grants`

* `id`
* `document_id`
* `principal_type`
* `principal_id`
* `access_level`
* `purpose`
* `effective_from`
* `effective_to`
* `granted_by`
* `created_at`

### `document_secure_shares`

* `id`
* `share_code`
* `document_version_id`
* `recipient_type`
* `recipient_reference`
* `purpose`
* `access_policy_json`
* `watermark_policy_json`
* `expires_at`
* `view_limit`
* `download_limit`
* `view_count`
* `download_count`
* `status`
* `approved_by`
* `created_by`
* `created_at`

### `document_access_events`

* `id`
* `document_id`
* `document_version_id`
* `actor_type`
* `actor_id`
* `action_type`
* `purpose`
* `ip_address`
* `device_reference`
* `request_id`
* `occurred_at`
* `created_at`

### `document_redactions`

* `id`
* `document_version_id`
* `redaction_type`
* `redaction_definition_json`
* `derived_file_object_id`
* `reason`
* `created_by`
* `approved_by`
* `created_at`

---

## 194.4. Document Generation và Signature

### `document_generation_runs`

* `id`
* `generation_code`
* `template_version_id`
* `resource_type`
* `resource_id`
* `resource_version_reference`
* `input_snapshot_json`
* `locale`
* `render_engine_version`
* `output_file_object_id`
* `output_hash`
* `status`
* `requested_by`
* `started_at`
* `completed_at`
* `created_at`

### `signature_envelopes`

* `id`
* `envelope_code`
* `document_version_id`
* `provider_code`
* `external_envelope_id`
* `signature_policy_version`
* `signing_order_type`
* `expires_at`
* `status`
* `created_by`
* `sent_at`
* `completed_at`
* `created_at`

### `signature_envelope_signers`

* `id`
* `signature_envelope_id`
* `signer_party_id`
* `signer_user_id`
* `signer_role`
* `signing_order`
* `email_reference`
* `phone_identity_id`
* `authentication_method`
* `status`
* `viewed_at`
* `signed_at`
* `decline_reason`
* `created_at`

### `signature_evidence`

* `id`
* `signature_envelope_id`
* `signed_file_object_id`
* `certificate_file_object_id`
* `audit_file_object_id`
* `content_hash`
* `provider_signature_reference`
* `verification_status`
* `created_at`

---

## 194.5. Retention và Legal Hold

### `document_retention_records`

* `id`
* `document_id`
* `retention_policy_id`
* `retention_start_at`
* `retention_end_at`
* `archive_eligible_at`
* `deletion_eligible_at`
* `status`
* `last_evaluated_at`
* `created_at`

### `legal_holds`

* `id`
* `legal_hold_code`
* `enterprise_id`
* `legal_entity_id`
* `name`
* `reason`
* `scope_type`
* `scope_id`
* `start_at`
* `review_at`
* `status`
* `created_by`
* `approved_by`
* `released_by`
* `released_at`
* `created_at`

### `legal_hold_items`

* `id`
* `legal_hold_id`
* `resource_type`
* `resource_id`
* `document_id`
* `added_at`
* `released_at`
* `status`
* `created_at`

### `document_deletion_runs`

* `id`
* `deletion_run_code`
* `policy_version`
* `candidate_count`
* `deleted_count`
* `blocked_count`
* `status`
* `requested_by`
* `approved_by`
* `started_at`
* `completed_at`
* `created_at`

---

## 194.6. Dossier

### `electronic_dossiers`

* `id`
* `dossier_code`
* `enterprise_id`
* `legal_entity_id`
* `dossier_type`
* `primary_context_type`
* `primary_context_id`
* `owner_user_id`
* `status`
* `completeness_status`
* `current_snapshot_number`
* `created_at`
* `updated_at`

### `dossier_checklist_items`

* `id`
* `dossier_id`
* `item_code`
* `required_document_type`
* `party_role`
* `verification_level`
* `required_before_milestone`
* `required`
* `status`
* `matched_document_version_id`
* `exception_id`
* `created_at`

### `dossier_exceptions`

* `id`
* `dossier_id`
* `checklist_item_id`
* `exception_type`
* `reason`
* `risk_level`
* `compensating_control`
* `expires_at`
* `status`
* `requested_by`
* `approved_by`
* `created_at`

### `dossier_evaluations`

* `id`
* `dossier_id`
* `policy_version`
* `result_status`
* `required_count`
* `satisfied_count`
* `missing_count`
* `expired_count`
* `rejected_count`
* `details_json`
* `evaluated_at`
* `created_at`

### `dossier_snapshots`

* `id`
* `dossier_id`
* `snapshot_number`
* `snapshot_type`
* `resource_version_reference`
* `checklist_snapshot_json`
* `document_versions_json`
* `verification_snapshot_json`
* `completeness_status`
* `hash_manifest`
* `status`
* `created_by`
* `approved_by`
* `frozen_at`
* `created_at`

### `evidence_packages`

* `id`
* `evidence_package_code`
* `dossier_snapshot_id`
* `purpose`
* `included_resources_json`
* `audit_range_json`
* `manifest_file_object_id`
* `package_file_object_id`
* `package_hash`
* `status`
* `created_by`
* `approved_by`
* `created_at`

---

## 194.7. Audit

### `audit_events`

* `id`
* `audit_event_code`
* `category`
* `action_code`
* `actor_type`
* `actor_id`
* `acting_role_id`
* `delegation_reference`
* `enterprise_id`
* `legal_entity_id`
* `resource_type`
* `resource_id`
* `parent_resource_type`
* `parent_resource_id`
* `before_reference`
* `after_reference`
* `changed_fields_json`
* `reason`
* `approval_reference`
* `request_id`
* `correlation_id`
* `causation_id`
* `session_id`
* `ip_address`
* `device_reference`
* `source_system`
* `occurred_at`
* `recorded_at`
* `event_hash`
* `previous_event_hash`
* `created_at`

### `audit_archives`

* `id`
* `archive_code`
* `period_from`
* `period_to`
* `partition_reference`
* `event_count`
* `root_hash`
* `signature_reference`
* `storage_reference`
* `status`
* `created_at`

### `audit_integrity_checks`

* `id`
* `audit_archive_id`
* `check_type`
* `expected_hash`
* `actual_hash`
* `status`
* `checked_at`
* `created_at`

---

## 194.8. Alert

### `alerts`

* `id`
* `alert_code`
* `alert_rule_version`
* `alert_type`
* `severity`
* `source_context`
* `source_type`
* `source_id`
* `resource_type`
* `resource_id`
* `fingerprint`
* `title`
* `description`
* `occurrence_count`
* `first_occurred_at`
* `last_occurred_at`
* `status`
* `assigned_user_id`
* `assigned_team_id`
* `sla_instance_id`
* `incident_id`
* `acknowledged_by`
* `acknowledged_at`
* `resolved_by`
* `resolved_at`
* `created_at`

### `alert_occurrences`

* `id`
* `alert_id`
* `source_event_id`
* `payload_reference`
* `occurred_at`
* `created_at`

### `alert_suppressions`

* `id`
* `suppression_code`
* `scope_type`
* `scope_id`
* `fingerprint_pattern`
* `reason`
* `effective_from`
* `effective_to`
* `approved_by`
* `status`
* `created_at`

### `alert_resolutions`

* `id`
* `alert_id`
* `resolution_code`
* `root_cause_code`
* `action_taken`
* `evidence_reference`
* `validated_by`
* `created_at`

---

## 194.9. Notification

### `notifications`

* `id`
* `notification_code`
* `notification_type`
* `source_context`
* `source_type`
* `source_id`
* `template_version_id`
* `locale`
* `rendering_input_json`
* `rendered_content_hash`
* `sensitivity_level`
* `priority`
* `scheduled_at`
* `expires_at`
* `status`
* `created_at`

### `notification_recipients`

* `id`
* `notification_id`
* `recipient_type`
* `recipient_id`
* `recipient_address_reference`
* `channel_code`
* `preference_snapshot_json`
* `eligibility_result_json`
* `status`
* `created_at`

### `notification_delivery_attempts`

* `id`
* `notification_recipient_id`
* `provider_code`
* `credential_version_reference`
* `attempt_number`
* `idempotency_key`
* `external_message_id`
* `request_hash`
* `response_reference`
* `error_code`
* `retryable`
* `status`
* `started_at`
* `completed_at`
* `created_at`

### `notification_read_events`

* `id`
* `notification_recipient_id`
* `event_type`
* `occurred_at`
* `source`
* `created_at`

### `notification_digests`

* `id`
* `digest_code`
* `recipient_user_id`
* `digest_type`
* `period_from`
* `period_to`
* `notification_ids_json`
* `status`
* `scheduled_at`
* `sent_at`
* `created_at`

---

## 194.10. Integration Hub

### `integration_connections`

* `id`
* `connection_code`
* `enterprise_id`
* `legal_entity_id`
* `connector_type`
* `provider_code`
* `environment_code`
* `account_reference`
* `endpoint_reference`
* `credential_reference`
* `credential_version`
* `service_account_id`
* `direction`
* `integration_mode`
* `scope_json`
* `rate_limit_policy_json`
* `source_of_truth_policy_json`
* `status`
* `last_health_check_at`
* `created_at`
* `updated_at`

### `integration_mapping_versions`

* `id`
* `connection_id`
* `mapping_code`
* `version`
* `source_schema_json`
* `target_schema_json`
* `field_mappings_json`
* `transformation_rules_json`
* `validation_rules_json`
* `effective_from`
* `effective_to`
* `status`
* `created_by`
* `reviewed_by`
* `approved_by`
* `created_at`

### `integration_sync_jobs`

* `id`
* `sync_job_code`
* `connection_id`
* `mapping_version_id`
* `direction`
* `resource_type`
* `cursor_start`
* `cursor_end`
* `window_from`
* `window_to`
* `input_count`
* `success_count`
* `warning_count`
* `failure_count`
* `status`
* `started_at`
* `completed_at`
* `created_at`

### `integration_sync_items`

* `id`
* `sync_job_id`
* `external_resource_id`
* `internal_resource_type`
* `internal_resource_id`
* `operation_type`
* `payload_hash`
* `idempotency_key`
* `status`
* `error_code`
* `created_at`

### `integration_cursors`

* `id`
* `connection_id`
* `resource_type`
* `cursor_type`
* `cursor_value`
* `last_success_at`
* `updated_at`

### `integration_webhook_events`

* `id`
* `webhook_event_code`
* `connection_id`
* `external_event_id`
* `event_type`
* `signature_status`
* `replay_status`
* `payload_reference`
* `payload_hash`
* `idempotency_key`
* `received_at`
* `processed_at`
* `status`
* `created_at`

### `integration_webhook_subscriptions`

* `id`
* `subscription_code`
* `subscriber_party_id`
* `endpoint_url`
* `credential_reference`
* `event_types_json`
* `filter_json`
* `payload_schema_version`
* `retry_policy_json`
* `rate_limit_policy_json`
* `effective_from`
* `effective_to`
* `status`
* `created_at`

### `integration_webhook_deliveries`

* `id`
* `subscription_id`
* `source_event_id`
* `delivery_number`
* `idempotency_key`
* `request_hash`
* `response_status`
* `error_code`
* `status`
* `next_retry_at`
* `delivered_at`
* `created_at`

### `integration_dead_letter_items`

* `id`
* `dlq_code`
* `connection_id`
* `source_type`
* `source_id`
* `mapping_version_id`
* `payload_reference`
* `error_code`
* `error_message`
* `attempt_count`
* `status`
* `assigned_user_id`
* `created_at`
* `resolved_at`

### `integration_reconciliation_cases`

* `id`
* `case_code`
* `connection_id`
* `resource_type`
* `internal_resource_id`
* `external_resource_id`
* `result_type`
* `internal_snapshot_json`
* `external_snapshot_json`
* `difference_json`
* `status`
* `assigned_user_id`
* `created_at`
* `resolved_at`

---

## 194.11. Jobs và Queue

### `system_jobs`

* `id`
* `job_code`
* `job_type`
* `job_definition_version`
* `trigger_type`
* `trigger_reference`
* `enterprise_id`
* `legal_entity_id`
* `scope_json`
* `parameters_json`
* `priority`
* `idempotency_key`
* `status`
* `requested_by`
* `scheduled_at`
* `started_at`
* `completed_at`
* `progress_percentage`
* `result_reference`
* `created_at`

### `system_job_attempts`

* `id`
* `job_id`
* `attempt_number`
* `worker_reference`
* `started_at`
* `completed_at`
* `status`
* `error_code`
* `error_message`
* `retryable`
* `created_at`

### `system_queues`

* `id`
* `queue_code`
* `name`
* `purpose`
* `priority_class`
* `maximum_concurrency`
* `retry_policy_json`
* `dead_letter_queue_id`
* `status`
* `created_at`

### `system_queue_items`

* `id`
* `queue_id`
* `job_id`
* `priority`
* `available_at`
* `locked_by`
* `locked_at`
* `attempt_count`
* `status`
* `created_at`

### `system_replay_requests`

* `id`
* `replay_code`
* `source_type`
* `source_id`
* `reason`
* `dry_run`
* `status`
* `requested_by`
* `reviewed_by`
* `approved_by`
* `executed_at`
* `created_at`

---

## 194.12. Incident và Health

### `operational_services`

* `id`
* `service_code`
* `name`
* `service_type`
* `criticality`
* `owner_team_id`
* `support_team_id`
* `rpo_seconds`
* `rto_seconds`
* `status`
* `created_at`

### `service_health_checks`

* `id`
* `service_id`
* `health_status`
* `latency_ms`
* `error_rate`
* `details_json`
* `checked_at`
* `created_at`

### `service_dependencies`

* `id`
* `service_id`
* `depends_on_service_id`
* `dependency_type`
* `critical`
* `created_at`

### `operational_incidents`

* `id`
* `incident_code`
* `severity`
* `title`
* `description`
* `affected_services_json`
* `affected_scopes_json`
* `commander_user_id`
* `status`
* `detected_at`
* `declared_at`
* `mitigated_at`
* `resolved_at`
* `closed_at`
* `created_at`

### `incident_timeline_events`

* `id`
* `incident_id`
* `event_type`
* `summary`
* `details_reference`
* `actor_id`
* `occurred_at`
* `created_at`

### `incident_root_cause_analyses`

* `id`
* `incident_id`
* `root_cause`
* `contributing_factors_json`
* `detection_gaps_json`
* `corrective_actions_json`
* `status`
* `created_by`
* `reviewed_by`
* `approved_by`
* `created_at`

### `maintenance_windows`

* `id`
* `maintenance_code`
* `environment_code`
* `affected_services_json`
* `planned_start_at`
* `planned_end_at`
* `actual_start_at`
* `actual_end_at`
* `impact_description`
* `read_only_mode`
* `suppression_policy_json`
* `rollback_plan_reference`
* `status`
* `created_by`
* `approved_by`
* `created_at`

---

## 194.13. Backup, Restore và DR

### `backup_runs`

* `id`
* `backup_code`
* `backup_type`
* `scope_json`
* `storage_reference`
* `encryption_reference`
* `checksum`
* `size_bytes`
* `retention_until`
* `verification_status`
* `restore_tested`
* `status`
* `started_at`
* `completed_at`
* `created_at`

### `restore_runs`

* `id`
* `restore_code`
* `backup_run_id`
* `target_environment`
* `point_in_time`
* `scope_json`
* `validation_result_json`
* `estimated_data_loss_seconds`
* `status`
* `requested_by`
* `approved_by`
* `started_at`
* `completed_at`
* `created_at`

### `disaster_recovery_drills`

* `id`
* `drill_code`
* `scenario_type`
* `services_json`
* `planned_rpo_seconds`
* `planned_rto_seconds`
* `achieved_rpo_seconds`
* `achieved_rto_seconds`
* `findings_json`
* `status`
* `conducted_at`
* `approved_by`
* `created_at`

---

## 194.14. Data Repair, Migration và Release

### `data_repair_requests`

* `id`
* `repair_code`
* `resource_type`
* `scope_json`
* `issue_description`
* `source_of_truth_reference`
* `repair_script_version`
* `dry_run_result_json`
* `impact_analysis_json`
* `rollback_plan_json`
* `status`
* `requested_by`
* `reviewed_by`
* `approved_by`
* `executed_by`
* `executed_at`
* `created_at`

### `approved_transfer_runs`

* `id`
* `transfer_code`
* `source_system`
* `target_system`
* `mapping_version_id`
* `scope_json`
* `input_count`
* `success_count`
* `failure_count`
* `reconciliation_result_json`
* `rollback_reference`
* `status`
* `started_at`
* `completed_at`
* `created_at`

### `system_releases`

* `id`
* `release_code`
* `version`
* `build_reference`
* `commit_reference`
* `release_notes_reference`
* `components_json`
* `schema_transition_references_json`
* `feature_flag_snapshot_json`
* `status`
* `created_at`

### `system_deployments`

* `id`
* `deployment_code`
* `release_id`
* `environment_code`
* `status`
* `started_at`
* `completed_at`
* `rollback_status`
* `deployed_by`
* `approved_by`
* `created_at`

---

## 194.15. Break-glass và Support

### `break_glass_requests`

* `id`
* `request_code`
* `user_id`
* `requested_capabilities_json`
* `requested_scope_json`
* `reason`
* `incident_id`
* `effective_from`
* `effective_to`
* `status`
* `requested_by`
* `approved_by`
* `created_at`

### `break_glass_sessions`

* `id`
* `break_glass_request_id`
* `session_id`
* `activated_at`
* `expired_at`
* `revoked_at`
* `actions_count`
* `review_status`
* `reviewed_by`
* `created_at`

### `support_sessions`

* `id`
* `support_session_code`
* `support_user_id`
* `customer_user_id`
* `purpose`
* `scope_json`
* `consent_reference`
* `effective_from`
* `effective_to`
* `status`
* `created_at`

---

# 195. Candidate application operations — not canonical OpenAPI

> Operations dưới đây là capability inventory. Exact paths, methods, payloads, errors, idempotency và authorization metadata thuộc OpenAPI của từng Context.

## Document

```text
GET    /documents
POST   /documents
GET    /documents/{id}
PATCH  /documents/{id}
POST   /documents/{id}/versions
GET    /document-versions/{id}
POST   /document-versions/{id}/submit-review
POST   /document-versions/{id}/verify
POST   /document-versions/{id}/reject
POST   /document-versions/{id}/supersede
POST   /document-versions/{id}/archive
GET    /documents/{id}/history
GET    /documents/{id}/access-explanation
```

## File Upload và Download

```text
POST   /files/upload-sessions
POST   /files/upload-sessions/{id}/complete
POST   /files/upload-sessions/{id}/abort
GET    /file-objects/{id}/scan-status
POST   /document-versions/{id}/download-tokens
POST   /document-versions/{id}/view-tokens
```

## OCR và Verification

```text
POST   /document-versions/{id}/ocr-runs
GET    /document-ocr-runs/{id}
GET    /document-ocr-runs/{id}/results
POST   /document-extraction-results/{id}/accept
POST   /document-extraction-results/{id}/correct
POST   /document-extraction-results/{id}/reject
POST   /document-versions/{id}/verification-requests
```

## Document Generation

```text
POST   /document-generation-runs
GET    /document-generation-runs/{id}
POST   /document-generation-runs/{id}/retry
POST   /document-generation-runs/{id}/cancel
```

## Signature

```text
POST   /signature-envelopes
GET    /signature-envelopes/{id}
POST   /signature-envelopes/{id}/send
POST   /signature-envelopes/{id}/remind
POST   /signature-envelopes/{id}/void
POST   /signature-envelopes/{id}/refresh-status
GET    /signature-envelopes/{id}/evidence
```

## Sharing và Retention

```text
POST   /document-versions/{id}/secure-shares
GET    /document-secure-shares/{id}
POST   /document-secure-shares/{id}/revoke
POST   /documents/{id}/legal-holds
POST   /legal-holds/{id}/release-requests
POST   /documents/{id}/archive
POST   /documents/{id}/deletion-requests
```

## Dossier

```text
GET    /dossiers
POST   /dossiers
GET    /dossiers/{id}
POST   /dossiers/{id}/evaluate
POST   /dossiers/{id}/checklist-items
POST   /dossier-checklist-items/{id}/link-document
POST   /dossiers/{id}/exceptions
POST   /dossier-exceptions/{id}/approve
POST   /dossiers/{id}/freeze
POST   /dossiers/{id}/evidence-packages
GET    /dossiers/{id}/history
```

## Audit

```text
GET    /audit/events
GET    /audit/events/{id}
GET    /audit/resources/{type}/{id}
GET    /audit/correlations/{correlation_id}
POST   /audit/integrity-checks
GET    /audit/integrity-checks/{id}
POST   /audit/exports
```

Audit Event creation chủ yếu nội bộ; không cho client tùy ý ghi Audit.

## Alert

```text
GET    /alerts
GET    /alerts/{id}
POST   /alerts/{id}/acknowledge
POST   /alerts/{id}/assign
POST   /alerts/{id}/suppress
POST   /alerts/{id}/create-incident
POST   /alerts/{id}/resolve
POST   /alerts/{id}/mark-false-positive
```

## Notification

```text
GET    /notifications
GET    /notifications/{id}
POST   /notifications
POST   /notifications/{id}/schedule
POST   /notifications/{id}/cancel
POST   /notifications/{id}/retry
POST   /notifications/{id}/mark-read
POST   /notifications/{id}/action
GET    /notifications/preferences
PATCH  /notifications/preferences
```

## Integration

```text
GET    /integration/connections
POST   /integration/connections
GET    /integration/connections/{id}
PATCH  /integration/connections/{id}
POST   /integration/connections/{id}/test
POST   /integration/connections/{id}/activate
POST   /integration/connections/{id}/suspend
POST   /integration/connections/{id}/decommission
POST   /integration/connections/{id}/rotate-credential-reference
```

## Mapping và Sync

```text
POST   /integration/connections/{id}/mapping-versions
POST   /integration/mapping-versions/{id}/validate
POST   /integration/mapping-versions/{id}/dry-run
POST   /integration/mapping-versions/{id}/approve
POST   /integration/mapping-versions/{id}/activate

GET    /integration/sync-jobs
POST   /integration/sync-jobs
GET    /integration/sync-jobs/{id}
POST   /integration/sync-jobs/{id}/cancel
POST   /integration/sync-jobs/{id}/retry
POST   /integration/sync-jobs/{id}/reconcile
```

## Webhook và DLQ

```text
POST   /integration/webhooks/{connection_code}
GET    /integration/webhook-events
GET    /integration/webhook-deliveries
GET    /integration/dead-letter-items
POST   /integration/dead-letter-items/{id}/assign
POST   /integration/dead-letter-items/{id}/replay
POST   /integration/dead-letter-items/{id}/resolve
```

## Jobs và Queue

```text
GET    /system/jobs
POST   /system/jobs
GET    /system/jobs/{id}
POST   /system/jobs/{id}/cancel
POST   /system/jobs/{id}/retry
POST   /system/jobs/{id}/replay
GET    /system/queues
GET    /system/queues/{id}/items
POST   /system/queues/{id}/pause
POST   /system/queues/{id}/resume
```

## Incident và Maintenance

```text
GET    /operations/incidents
POST   /operations/incidents
GET    /operations/incidents/{id}
POST   /operations/incidents/{id}/declare
POST   /operations/incidents/{id}/update-status
POST   /operations/incidents/{id}/add-timeline-event
POST   /operations/incidents/{id}/resolve
POST   /operations/incidents/{id}/root-cause-analysis

GET    /operations/maintenance-windows
POST   /operations/maintenance-windows
POST   /operations/maintenance-windows/{id}/approve
POST   /operations/maintenance-windows/{id}/start
POST   /operations/maintenance-windows/{id}/complete
```

## Backup, Restore và DR

```text
GET    /operations/backups
POST   /operations/backups
GET    /operations/backups/{id}
POST   /operations/backups/{id}/verify
POST   /operations/restores
GET    /operations/restores/{id}
POST   /operations/dr-drills
GET    /operations/dr-drills/{id}
```

## Data Repair và Release

```text
GET    /operations/data-repair-requests
POST   /operations/data-repair-requests
POST   /operations/data-repair-requests/{id}/dry-run
POST   /operations/data-repair-requests/{id}/submit-review
POST   /operations/data-repair-requests/{id}/approve
POST   /operations/data-repair-requests/{id}/execute
POST   /operations/data-repair-requests/{id}/validate

GET    /operations/releases
POST   /operations/releases
GET    /operations/deployments
POST   /operations/deployments
POST   /operations/deployments/{id}/rollback
```

## Break-glass

```text
POST   /operations/break-glass-requests
GET    /operations/break-glass-requests
POST   /operations/break-glass-requests/{id}/approve
POST   /operations/break-glass-requests/{id}/activate
POST   /operations/break-glass-sessions/{id}/revoke
POST   /operations/break-glass-sessions/{id}/review
```

---

# 196. Candidate permission vocabulary — not canonical Permission Registry

> Exact permission codes, scopes, role mappings, SoD, concealment và field masking thuộc Security registries/matrices.

## Document

```text
document.view
document.view_metadata
document.view_sensitive
document.create
document.upload
document.create_version
document.update_metadata
document.review
document.verify
document.reject
document.supersede
document.archive
document.download
document.download_original
document.download_redacted
document.share
document.revoke_share
document.view_audit
```

## OCR, Generation và Signature

```text
document_ocr.run
document_ocr.view_result
document_ocr.review
document_ocr.apply_suggestion

document_generation.run
document_generation.retry
document_generation.cancel

signature_envelope.view
signature_envelope.create
signature_envelope.send
signature_envelope.remind
signature_envelope.void
signature_evidence.view
```

## Dossier và Retention

```text
dossier.view
dossier.create
dossier.update
dossier.evaluate
dossier.link_document
dossier.create_exception
dossier.approve_exception
dossier.freeze
dossier.create_evidence_package

legal_hold.view
legal_hold.create
legal_hold.approve
legal_hold.release
document_retention.view
document_retention.archive
document_retention.delete_request
document_retention.delete_approve
```

## Audit

```text
audit.view_business
audit.view_access
audit.view_sensitive_access
audit.view_security
audit.view_admin
audit.view_integration
audit.view_break_glass
audit.verify_integrity
audit.export
```

## Alert và Notification

```text
alert.view
alert.acknowledge
alert.assign
alert.suppress
alert.resolve
alert.mark_false_positive
alert.create_incident

notification.view
notification.create
notification.schedule
notification.cancel
notification.retry
notification.manage_preferences
notification.view_delivery
notification.view_content
```

## Integration

```text
integration_connection.view
integration_connection.create
integration_connection.update_draft
integration_connection.test
integration_connection.activate
integration_connection.suspend
integration_connection.decommission

integration_mapping.view
integration_mapping.create_version
integration_mapping.validate
integration_mapping.dry_run
integration_mapping.review
integration_mapping.approve
integration_mapping.activate

integration_sync.view
integration_sync.run
integration_sync.cancel
integration_sync.retry
integration_sync.reconcile

integration_webhook.view
integration_webhook.manage_subscription
integration_webhook.replay
integration_dlq.view
integration_dlq.assign
integration_dlq.replay
integration_dlq.resolve
```

## System Operations

```text
system_job.view
system_job.create
system_job.cancel
system_job.retry
system_job.replay
system_queue.view
system_queue.pause
system_queue.resume

operations_health.view
operations_incident.view
operations_incident.create
operations_incident.command
operations_incident.resolve
operations_incident.approve_rca

operations_maintenance.view
operations_maintenance.create
operations_maintenance.approve
operations_maintenance.execute

operations_backup.view
operations_backup.run
operations_backup.verify
operations_restore.request
operations_restore.approve
operations_restore.execute
operations_drill.run

operations_data_repair.view
operations_data_repair.request
operations_data_repair.dry_run
operations_data_repair.review
operations_data_repair.approve
operations_data_repair.execute

operations_release.view
operations_release.create
operations_deployment.execute
operations_deployment.rollback
```

## Break-glass

```text
break_glass.request
break_glass.approve
break_glass.activate
break_glass.revoke
break_glass.review
support_session.create
support_session.view
support_session.terminate
```

Các quyền kết hợp với:

```text
self
mine
assigned
team
department
branch
legal_entity
project
shared
all
```

---

# 197. Candidate role baseline — not canonical Role/Permission Registry

> Role descriptions chỉ thể hiện product intent. Backend authority phải resolve từ IAM/Security canonical sources.

## 197.1. Sale

Được:

* Tải tài liệu cho Customer/Deal thuộc scope.
* Xem tài liệu được phép.
* Xem Dossier completeness.
* Tạo Secure Share nếu policy cho phép.
* Nhận Notification.
* Xem business alerts liên quan.

Không được:

* Xem Audit bảo mật.
* Xem Document restricted ngoài scope.
* Replay integration.
* Download hàng loạt.
* Xóa tài liệu đã Verified.

## 197.2. Team Lead

Được:

* Xem Dossier Team.
* Review missing document.
* Xem Alert Team.
* Xem Audit nghiệp vụ Team theo quyền.
* Approve một số exception.

## 197.3. Legal

Được:

* Xem Legal Dossier.
* Verify legal documents.
* Legal Hold.
* Signature evidence.
* Contract document audit.

## 197.4. Accounting/Finance

Được:

* Payment/Receipt/Settlement documents.
* Revenue/Commission evidence theo quyền.
* Finance alerts.
* Relevant integration reconciliation.

## 197.5. Marketing

Được:

* Marketing content.
* Campaign Dossier.
* Ad platform integration summary.
* Notification delivery aggregate.

Không mặc định xem Customer identity documents.

## 197.6. Compliance/Audit

Được:

* Audit Explorer.
* Sensitive access audit.
* Export audit.
* Legal Hold.
* Evidence Package.
* Break-glass review.

## 197.7. System Administrator

Được:

* Integration runtime.
* Job.
* Queue.
* Health.
* Backup.
* Deployment.
* Incident.

Không mặc định xem nội dung nghiệp vụ nhạy cảm.

## 197.8. Security Administrator

Được:

* Security alert.
* Break-glass.
* Authentication audit.
* Malware/DLP.
* Incident security.

## 197.9. Director

Được:

* Operational overview.
* Critical Incident.
* Major Alert.
* Legal Hold summary.
* Export approval.
* Break-glass approval theo authority.

---

# 198. Candidate business facts — not canonical Event contracts

> Exact Event names, versions, payloads, channels và consumers thuộc JSON Schema, AsyncAPI và Event Registry của owning Context.

Runtime Support Composite Capability phát:

```text
file.uploaded
file.scan_completed
file.quarantined
document.created
document.version_created
document.verified
document.rejected
document.superseded
document.expiring
document.expired
document.archived
document.deleted
document.secure_share_created
document.secure_share_revoked

document_ocr.completed
document_extraction.reviewed
document_generation.completed
document_generation.failed

signature_envelope.created
signature_envelope.sent
signature_envelope.partially_signed
signature_envelope.completed
signature_envelope.declined
signature_envelope.expired
signature_envelope.voided

dossier.created
dossier.evaluated
dossier.incomplete
dossier.complete
dossier.exception_created
dossier.frozen
evidence_package.created

legal_hold.created
legal_hold.activated
legal_hold.released

audit.integrity_check_failed

alert.created
alert.acknowledged
alert.assigned
alert.escalated
alert.resolved
alert.false_positive
alert.incident_created

notification.queued
notification.sent
notification.delivered
notification.read
notification.failed
notification.bounced
notification.expired

integration.connection_activated
integration.connection_degraded
integration.connection_failed
integration.mapping_activated
integration.sync_started
integration.sync_completed
integration.sync_failed
integration.webhook_received
integration.webhook_failed
integration.webhook_delivered
integration.dlq_item_created
integration.dlq_item_replayed
integration.reconciliation_created
integration.reconciliation_resolved

system_job.queued
system_job.started
system_job.completed
system_job.failed
system_job.dead_lettered
system_queue.degraded

operations.incident_declared
operations.incident_mitigated
operations.incident_resolved
operations.maintenance_started
operations.maintenance_completed
operations.backup_completed
operations.backup_failed
operations.restore_completed
operations.restore_failed
operations.dr_drill_completed
operations.data_repair_executed
operations.deployment_completed
operations.deployment_failed
operations.deployment_rolled_back

break_glass.requested
break_glass.approved
break_glass.activated
break_glass.revoked
break_glass.expired
break_glass.review_completed
```

Consumer phải idempotent.

---

# 199. Candidate Platform configuration references

```text
document.type_dictionary
document.storage_policy
document.upload_policy
document.allowed_file_policy
document.malware_scan_policy
document.dlp_policy
document.classification_policy
document.verification_policy
document.ocr_policy
document.generation_policy
document.redaction_policy
document.watermark_policy
document.share_policy
document.retention_policy
document.archive_policy
document.deletion_policy

dossier.type_policy
dossier.checklist_policy
dossier.completeness_policy
dossier.exception_policy
dossier.freeze_policy
dossier.evidence_package_policy

signature.provider_policy
signature.authentication_policy
signature.reminder_policy
signature.expiry_policy
signature.evidence_policy

audit.event_policy
audit.retention_policy
audit.integrity_policy
audit.access_policy
audit.archive_policy

alert.rule_policy
alert.severity_policy
alert.deduplication_policy
alert.suppression_policy
alert.escalation_policy
alert.resolution_policy

notification.template_policy
notification.channel_policy
notification.preference_policy
notification.quiet_hours_policy
notification.retry_policy
notification.digest_policy
notification.security_policy

integration.connector_policy
integration.connection_policy
integration.mapping_policy
integration.transformation_policy
integration.validation_policy
integration.sync_policy
integration.webhook_policy
integration.retry_policy
integration.dlq_policy
integration.reconciliation_policy
integration.source_of_truth_policy

system.job_policy
system.queue_policy
system.retry_policy
system.replay_policy
system.maintenance_policy
system.incident_policy
system.health_policy
system.observability_policy
system.data_repair_policy
system.approved_transfer_policy
system.backup_policy
system.restore_policy
system.dr_policy
system.release_policy
system.deployment_policy
system.support_policy
system.break_glass_policy

runtime_support.sla_policy
runtime_support.notification_policy
runtime_support.field_access_policy
runtime_support.export_policy
runtime_support.retention_policy
```

Mỗi configuration definition phải công bố schema, allowed scopes, resolution strategy, owner, version, effective period, approval và Audit requirements khi phù hợp.

---

# 200. System invariant

Các quy tắc sau không được cấu hình tắt:

1. File Object không đồng nghĩa Document.
2. Document không đồng nghĩa Dossier.
3. Document Version Verified không được ghi đè.
4. Signed Document không được thay file âm thầm.
5. File chưa scan sạch không được dùng cho workflow nhạy cảm.
6. Malware file phải quarantine.
7. Content hash bắt buộc với file chính thức.
8. Document access không mở rộng context access.
9. Document download phải backend authorize.
10. Secure Share phải có expiry.
11. OCR không tự sửa nghiệp vụ nguồn.
12. Signature webhook không tự chuyển trạng thái Contract trái Contract and Cash Capability.
13. Dossier completeness không chỉ dựa trên file present.
14. Dossier Frozen không được sửa.
15. Legal Hold chặn deletion.
16. Audit phải append-only.
17. Audit không ghi secret.
18. Audit correction tạo event mới.
19. Alert không đồng nghĩa Notification.
20. Notification orchestration không đồng nghĩa Interaction.
21. Customer communication phải tạo canonical Interaction qua Activity Context khi accepted/executed.
22. Marketing outbound intent phải qua Marketing Context.
23. Transactional Notification không được dùng để lách opt-out Marketing.
24. Integration không lưu plain secret.
25. Integration phải có source-of-truth policy.
26. Mapping active không sửa trực tiếp.
27. Webhook phải verify signature khi provider hỗ trợ.
28. Webhook phải idempotent.
29. Retry không được tạo record trùng.
30. DLQ replay phải audit.
31. Bidirectional conflict không tự dùng latest update cho dữ liệu tài chính/pháp lý.
32. Background Job phải có idempotency khi có side effect.
33. Data Repair không được bypass approval.
34. Production repair không dùng SQL tùy ý không kiểm soát.
35. Backup phải có integrity verification.
36. Restore phải có validation.
37. Break-glass phải có thời hạn.
38. Break-glass không xóa Audit.
39. System Admin không tự có quyền xem nghiệp vụ nhạy cảm.
40. Runtime Support Composite Capability không thay source of truth của owning Contexts.

---

# 201. Rule nghiệp vụ bắt buộc

1. File phải có storage reference.
2. File phải có MIME type.
3. File phải có size.
4. File chính thức phải có hash.
5. File upload phải kiểm tra quyền.
6. File upload session phải hết hạn.
7. Upload complete phải xác nhận checksum.
8. Scan status phải được lưu.
9. Infected file bị chặn.
10. Scan failed không được tự coi clean.
11. Document phải có type.
12. Document phải có primary context.
13. Document phải có Legal Entity khi nghiệp vụ yêu cầu.
14. Document Version phải có File Object.
15. Version number phải tăng tuần tự.
16. Version cũ không bị xóa khi upload bản mới.
17. Verified Version không sửa metadata trọng yếu trực tiếp.
18. Metadata correction phải có history.
19. Document expiry phải tạo alert khi cấu hình.
20. Document rejection phải có reason.
21. Supersede phải link Version cũ.
22. External URL phải được health check.
23. Download original cần quyền riêng.
24. Download phải audit.
25. Secure Share phải có recipient.
26. Secure Share phải có purpose.
27. Secure Share phải có expiry.
28. Share revoked không truy cập tiếp.
29. Watermark phải tạo derived copy.
30. Redaction không ghi đè original.
31. OCR phải lưu model version.
32. OCR phải lưu confidence.
33. OCR field quan trọng cần review.
34. OCR suggestion không tự update Customer.
35. Generated Document phải lưu Template Version.
36. Generated Document phải lưu resource snapshot.
37. Generated Document phải có output hash.
38. Template không được đọc field ngoài allowlist.
39. Signature Envelope phải có Document Version.
40. Signature Envelope phải có provider.
41. Signer phải có identity reference.
42. Signature callback phải idempotent.
43. Completed Envelope phải có evidence.
44. Void Envelope không xóa evidence.
45. Contract Effective vẫn do Contract and Cash Capability quyết định.
46. Retention phải tham chiếu Policy Version.
47. Legal Hold chặn archive deletion nếu policy.
48. Legal Hold release cần approval.
49. Deletion phải có eligibility check.
50. Deletion phải giữ audit/tombstone theo policy.
51. Dossier phải có type.
52. Dossier phải có primary context.
53. Checklist item phải có requirement.
54. Presence không đồng nghĩa Verified.
55. Expired document không thỏa checklist trái policy.
56. Dossier exception phải có risk.
57. Exception phải có expiry khi tạm thời.
58. Dossier Freeze phải snapshot Versions.
59. Frozen snapshot không sửa.
60. Evidence Package phải có manifest/hash.
61. Customer merge không nhân đôi file.
62. Contract amendment không ghi đè Dossier cũ.
63. Audit Event phải có actor hoặc system actor.
64. Audit Event phải có occurred_at.
65. Audit Event phải có resource/action.
66. Audit không update.
67. Audit không delete trái retention.
68. Sensitive access phải audit.
69. Export phải audit.
70. Break-glass phải audit từng action.
71. Alert phải có severity.
72. Alert phải có fingerprint.
73. Alert occurrence lặp phải aggregate.
74. Alert resolve phải có action.
75. Critical Alert close cần validation theo policy.
76. Suppression không xóa occurrence.
77. Maintenance suppression phải có window.
78. Notification phải có type.
79. Notification phải có recipient.
80. Notification phải có channel.
81. Notification phải tham chiếu Template Version.
82. Notification sensitive không hiển thị full data trong preview.
83. Notification retry phải idempotent.
84. Notification expired không retry.
85. Customer message phải link Interaction.
86. Marketing outbound phải qua consent gate Marketing Capability.
87. Notification action link phải short-lived.
88. Connection phải có Connector Type.
89. Connection phải có Credential Reference.
90. Connection active phải test thành công.
91. Service Account phải active.
92. Mapping phải có version.
93. Active Mapping không sửa.
94. Transformation phải sandbox.
95. Source raw payload phải có retention.
96. Webhook signature fail không xử lý business action.
97. Replay window phải được kiểm tra.
98. External event ID phải dedupe.
99. Cursor chỉ advance sau success theo policy.
100. Partial Sync phải ghi failed items.
101. Sync retry không tạo duplicate.
102. Rate limit phải được tôn trọng.
103. Circuit breaker phải alert.
104. DLQ item phải có payload reference.
105. DLQ replay phải có reason.
106. Reconciliation phải có snapshots.
107. Accepted mismatch cần authority.
108. Source of truth phải được công bố.
109. Data minimization phải được áp dụng.
110. Sandbox test không dùng production data trái policy.
111. Go-live cần monitoring.
112. Decommission phải revoke credentials.
113. Job phải có definition/version.
114. Job side effect phải idempotent.
115. Job attempt phải lưu error.
116. Job cancellation không rollback committed work âm thầm.
117. Queue phải có DLQ khi critical.
118. Queue lag phải có threshold.
119. Critical Job không bị bulk queue block.
120. Maintenance phải có impact.
121. Incident phải có commander với SEV1/SEV2.
122. Incident Timeline không sửa.
123. RCA phải có actions.
124. Health status phải có last check.
125. Log không chứa secret.
126. Data Repair phải có source of truth.
127. Data Repair phải dry run.
128. Data Repair phải impact analysis.
129. Data Repair execute cần approval.
130. Approved transfer/transition phải reconcile.
131. Backup phải có checksum.
132. Backup success không đồng nghĩa restore-tested.
133. Restore phải dùng target environment rõ.
134. DR drill phải đo RPO/RTO.
135. Production và Test phải tách credential.
136. Test data phải masked/synthetic.
137. Release phải có build reference.
138. Deployment failure phải ghi rollback status.
139. Feature Flag runtime phải audit.
140. Support session phải có purpose.
141. Support session phải có expiry.
142. Break-glass cần MFA/re-auth.
143. Break-glass phải tự expire.
144. Break-glass review bắt buộc.
145. User inactive không dùng Integration credential cá nhân.
146. View không đồng nghĩa Download.
147. Download không đồng nghĩa Share.
148. Share không đồng nghĩa Export.
149. Field masking phải backend.
150. Capability không thay nguồn chân lý nghiệp vụ.

---

# 202. Cảnh báo và phát hiện bất thường

Hệ thống cần cảnh báo khi:

* File scan chưa chạy.
* Malware scan failed.
* File infected.
* File hash thay đổi.
* Document Verified bị thay file.
* Document sắp hết hạn.
* Dossier thiếu tài liệu trước milestone.
* Dossier exception sắp hết hạn.
* Secure Share không có expiry.
* Secure Share download bất thường.
* Download nhiều tài liệu nhạy cảm.
* Recording/document restricted bị truy cập hàng loạt.
* Legal Hold item bị đưa vào deletion.
* Retention job xóa quá nhiều record.
* OCR confidence thấp nhưng được apply tự động.
* Signature Envelope sắp hết hạn.
* Signature provider callback bất thường.
* Completed Envelope thiếu evidence.
* Audit hash chain lỗi.
* Audit ingestion bị chậm.
* Sensitive access ngoài giờ.
* Break-glass được dùng không có Incident.
* Alert Critical không được acknowledge.
* Alert bị suppress quá lâu.
* Notification failure tăng.
* Customer transactional message không tạo Interaction.
* Marketing message được gửi không có consent snapshot.
* Provider bounce tăng.
* Credential sắp hết hạn.
* Connection Authentication Failed.
* Sync Job thất bại liên tục.
* Cursor không tiến.
* Webhook signature lỗi.
* Webhook replay.
* DLQ tăng.
* Mapping error tăng.
* Reconciliation mismatch.
* External/CRM amount mismatch.
* Rate limit gần cạn.
* Circuit breaker mở.
* Queue lag.
* Job chạy quá lâu.
* Job retry storm.
* Backup failed.
* Backup không restore test lâu.
* RPO/RTO drill fail.
* Storage gần đầy.
* Service error rate tăng.
* Incident SEV1 chưa có commander.
* Maintenance kéo dài.
* Data Repair không có dry run.
* Deployment không có approval.
* Production credential dùng ở Test.
* Support session vượt thời hạn.
* Same idempotency key khác payload.
* Data export/download bất thường.
* Audit hoặc evidence package không tái tạo được.

---

# 203. Audit Log

Runtime Support Composite Capability phải audit đặc biệt:

* Upload.
* Download.
* View restricted document.
* Secure share.
* Redaction.
* Watermark.
* Verification.
* OCR apply.
* Signature.
* Legal Hold.
* Deletion.
* Evidence Package.
* Alert suppression.
* Notification retry.
* Connection change.
* Mapping activation.
* Webhook replay.
* DLQ replay.
* Job retry.
* Queue pause.
* Incident action.
* Data Repair.
* Migration.
* Backup/Restore.
* Deployment.
* Break-glass.
* Support session.
* Export.

Audit phải lưu:

* Actor.
* Role.
* Scope.
* Resource.
* Before/after hoặc references.
* Reason.
* Approval.
* Request/correlation.
* IP/device.
* Configuration Version.
* Timestamp.
* Result.

---

# 204. Candidate delivery scope — product baseline, not a Sprint commitment

## 204.1. Document và Dossier

* File Object.
* Object storage integration.
* Upload.
* Malware scan.
* Hash.
* Document.
* Document Version.
* Metadata.
* Context links.
* Classification.
* Verification.
* Expiry.
* Secure download.
* Watermark cơ bản.
* Secure Share.
* OCR cơ bản.
* Document Generation.
* Signature integration.
* Retention.
* Legal Hold.
* Dossier.
* Checklist.
* Completeness.
* Exception.
* Freeze.
* Evidence Package cơ bản.

## 204.2. Audit

* Business Audit.
* Data Access Audit.
* Export Audit.
* Admin Audit.
* Integration Audit.
* Append-only storage.
* Search.
* Correlation.
* Hash integrity cơ bản.
* Retention.

## 204.3. Alert và Notification

* Alert.
* Severity.
* Deduplication.
* Assignment.
* Acknowledgement.
* Escalation.
* Resolution.
* In-app Notification.
* Email.
* SMS/Chat integration ưu tiên.
* Delivery status.
* Retry.
* Digest cơ bản.
* Action link.
* Interaction link.

## 204.4. Integration Hub

* Connection.
* Credential reference.
* Mapping Version.
* Validation.
* Dry run.
* Webhook gateway.
* Signature verification.
* Idempotency.
* Sync Job.
* Cursor.
* Retry.
* DLQ.
* Replay.
* Reconciliation.
* Health.

## 204.5. Operations

* Background Job.
* Queue.
* Retry.
* DLQ.
* Job monitoring.
* Service Health.
* Incident.
* Maintenance.
* Backup metadata.
* Restore metadata.
* DR drill.
* Data Repair workflow.
* Release/Deployment metadata.
* Break-glass.
* Operational Dashboard.

## 204.6. Giai đoạn nâng cao

* Full enterprise DMS.
* Advanced DLP.
* AI document classification.
* Advanced contract extraction.
* Digital certificate verification nâng cao.
* WORM archive.
* External timestamp authority.
* Full SIEM integration.
* SOAR automation.
* Multi-region active-active.
* Automated failover.
* Chaos testing.
* Advanced observability.
* OpenTelemetry full tracing.
* API marketplace.
* Partner integration portal.
* Low-code integration builder.
* Secure data clean room.
* Automated compliance evidence.
* Immutable ledger anchoring.
* Advanced records management.

---

# 205. Capability acceptance catalog — not a single Sprint Definition of Done

Capability được xem là đạt khi:

1. Tạo được File Object.
2. File có storage provider.
3. File có storage key.
4. File có filename.
5. File có MIME type.
6. File có size.
7. File có hash.
8. Upload session hoạt động.
9. Multipart upload hoạt động.
10. Upload resume hoạt động.
11. Upload complete xác nhận checksum.
12. Malware scan được chạy.
13. File clean được đánh dấu.
14. File infected bị quarantine.
15. File scan failed không được dùng.
16. Tạo Document.
17. Document có code.
18. Document có type.
19. Document có primary context.
20. Document có sensitivity.
21. Tạo Document Version.
22. Version number tăng.
23. Version có File Object.
24. Version có source.
25. Version có metadata snapshot.
26. Version cũ được giữ.
27. Version mới supersede đúng.
28. Verified Version không sửa trực tiếp.
29. Document link Customer được.
30. Document link Asset được.
31. Document link Listing được.
32. Document link Deal được.
33. Document link Contract được.
34. Document link Payment được.
35. Context link không mở rộng quyền.
36. Metadata field masking hoạt động.
37. Document classification hoạt động.
38. Sensitivity policy hoạt động.
39. Binary duplicate được phát hiện.
40. Duplicate không tự merge Document.
41. External Document URL được lưu.
42. External URL health check hoạt động.
43. Tạo Document Review.
44. Review có outcome.
45. Verification có method.
46. Verification có policy version.
47. Verification có verifier.
48. Rejection có reason.
49. Expiry được tính.
50. Expiry alert được tạo.
51. Tạo OCR Run.
52. OCR lưu provider.
53. OCR lưu model version.
54. OCR lưu raw text reference.
55. OCR lưu confidence.
56. OCR extraction theo field.
57. OCR review hoạt động.
58. OCR correction giữ original.
59. OCR không tự sửa Customer.
60. Tạo Document Generation Run.
61. Generation lưu Template Version.
62. Generation lưu input snapshot.
63. Generation tạo output hash.
64. Generated document tạo Document Version.
65. Missing required merge field bị chặn.
66. Template truy cập field ngoài allowlist bị chặn.
67. Tạo Signature Envelope.
68. Envelope link Document Version.
69. Envelope có provider.
70. Thêm signer được.
71. Signing order được hỗ trợ.
72. Authentication method được lưu.
73. Send Envelope hoạt động.
74. Reminder hoạt động.
75. Partial Signed được ghi.
76. Completed được ghi.
77. Declined được ghi.
78. Expired được ghi.
79. Void được ghi.
80. Webhook signature được verify.
81. Webhook lặp không tạo status trùng.
82. Signed file được lưu.
83. Certificate được lưu.
84. Audit evidence được lưu.
85. Contract không tự Effective chỉ vì envelope complete.
86. Tạo Redacted Copy.
87. Original không bị thay.
88. Watermark được tạo.
89. Download original cần quyền.
90. Download redacted hoạt động.
91. Download có audit.
92. Tạo Secure Share.
93. Share có recipient.
94. Share có purpose.
95. Share có expiry.
96. Share có view/download limit.
97. Share có watermark.
98. Share revoke hoạt động.
99. Expired share không truy cập.
100. Tạo Retention Record.
101. Retention tham chiếu policy.
102. Archive eligibility được tính.
103. Deletion eligibility được tính.
104. Tạo Legal Hold.
105. Legal Hold có scope.
106. Legal Hold có reason.
107. Legal Hold cần approval.
108. Legal Hold chặn deletion.
109. Release Legal Hold cần approval.
110. Archive hoạt động.
111. Deletion Request hoạt động.
112. Deletion giữ tombstone/audit.
113. Tạo Dossier.
114. Dossier có type.
115. Dossier có primary context.
116. Dossier có owner.
117. Tạo Checklist Item.
118. Checklist yêu cầu Document Type.
119. Link Document Version vào checklist.
120. Presence được kiểm tra.
121. Verification được kiểm tra.
122. Expiry được kiểm tra.
123. Completeness evaluation hoạt động.
124. Incomplete được xác định.
125. Complete được xác định.
126. Complete With Exception hoạt động.
127. Tạo Dossier Exception.
128. Exception có risk.
129. Exception có compensating control.
130. Exception có expiry.
131. Exception approval hoạt động.
132. Dossier Gate API hoạt động.
133. Freeze Dossier hoạt động.
134. Frozen snapshot có document versions.
135. Frozen snapshot có checklist.
136. Frozen snapshot có hash.
137. Frozen snapshot không sửa.
138. Tạo Evidence Package.
139. Package có manifest.
140. Package có hash.
141. Customer merge giữ Documents.
142. Customer merge không duplicate file.
143. Contract amendment giữ Dossier cũ.
144. Multi-Legal Entity access hoạt động.
145. Tạo Business Audit Event.
146. Tạo Data Access Audit.
147. Tạo Export Audit.
148. Tạo Admin Audit.
149. Audit có actor.
150. Audit có action.
151. Audit có resource.
152. Audit có occurred_at.
153. Audit có request ID.
154. Audit có correlation ID.
155. Audit lưu changed fields.
156. Audit không update.
157. Audit không delete.
158. Audit correction tạo event mới.
159. Audit không lưu secret.
160. Sensitive access được audit.
161. Hash chain/integrity check hoạt động.
162. Audit Search theo user.
163. Audit Search theo resource.
164. Audit Search theo correlation.
165. Audit Export cần quyền.
166. Tạo Alert.
167. Alert có severity.
168. Alert có fingerprint.
169. Occurrence lặp được aggregate.
170. Alert acknowledgement hoạt động.
171. Alert assignment hoạt động.
172. Alert escalation hoạt động.
173. Alert suppression hoạt động.
174. Suppression không xóa occurrence.
175. Alert resolution có action.
176. Critical Alert cần validation.
177. Alert tạo Incident được.
178. Tạo Notification.
179. Notification có type.
180. Notification có template version.
181. Notification có recipient.
182. Notification có channel.
183. In-app Notification hoạt động.
184. Email Notification hoạt động.
185. SMS/Chat channel ưu tiên hoạt động.
186. Notification render theo locale.
187. Notification preference hoạt động.
188. Quiet Hours hoạt động.
189. Critical override theo policy hoạt động.
190. Delivery Attempt được lưu.
191. Provider external ID được lưu.
192. Retry hoạt động.
193. Retry không gửi trùng.
194. Expired Notification không retry.
195. Notification read được ghi.
196. Secure Action Link hết hạn.
197. Customer Notification tạo Interaction.
198. Marketing Notification yêu cầu Marketing Capability eligibility.
199. Sensitive preview được mask.
200. Tạo Integration Connection.
201. Connection có Connector Type.
202. Connection có provider.
203. Connection có Credential Reference.
204. Connection có Service Account.
205. Test Connection hoạt động.
206. Connection Active cần test thành công.
207. Connection degraded được phát hiện.
208. Credential expiry được cảnh báo.
209. Tạo Mapping Version.
210. Mapping có source schema.
211. Mapping có target schema.
212. Mapping có field rules.
213. Mapping validation hoạt động.
214. Mapping dry run hoạt động.
215. Active Mapping không sửa.
216. Transformation an toàn hoạt động.
217. Arbitrary code bị chặn.
218. Tạo Sync Job.
219. Sync có Mapping Version.
220. Sync có cursor.
221. Sync lưu counts.
222. Partial completion được ghi.
223. Sync retry hoạt động.
224. Sync retry không tạo duplicate.
225. Cursor chỉ advance đúng policy.
226. Inbound Webhook được nhận.
227. Webhook signature được kiểm tra.
228. Webhook replay bị chặn.
229. Raw payload reference được lưu.
230. External Event ID được dedupe.
231. Webhook xử lý async.
232. Outbound Subscription được tạo.
233. Outbound Delivery retry hoạt động.
234. Failed delivery vào DLQ.
235. Tạo DLQ Item.
236. DLQ có error.
237. DLQ assignment hoạt động.
238. Replay cần quyền.
239. Replay có reason.
240. Replay không tạo duplicate.
241. Rate limit hoạt động.
242. Circuit breaker hoạt động.
243. Circuit breaker tạo Alert.
244. Reconciliation Case được tạo.
245. Missing internal được phát hiện.
246. Missing external được phát hiện.
247. Value mismatch được phát hiện.
248. Status mismatch được phát hiện.
249. Conflict resolution theo source-of-truth.
250. Data minimization được áp dụng.
251. Integration Sandbox test hoạt động.
252. Go-live checklist hoạt động.
253. Decommission revoke credential reference.
254. Tạo System Job.
255. Job có definition version.
256. Job có idempotency key.
257. Job được queue.
258. Job started được ghi.
259. Job progress được ghi.
260. Job completed được ghi.
261. Job failed được ghi.
262. Job retry hoạt động.
263. Job cancellation hoạt động.
264. Partial committed work không bị rollback âm thầm.
265. Queue priority hoạt động.
266. Critical queue không bị bulk block.
267. Queue lag alert hoạt động.
268. Dead-lettered Job được ghi.
269. Batch chunking hoạt động.
270. Batch resume hoạt động.
271. Tạo Maintenance Window.
272. Maintenance có affected services.
273. Maintenance có impact.
274. Maintenance approval hoạt động.
275. Maintenance start/end được ghi.
276. Alert suppression theo maintenance hoạt động.
277. Tạo Incident.
278. Incident có severity.
279. SEV1/SEV2 có commander.
280. Incident Timeline hoạt động.
281. Incident status transition hoạt động.
282. Incident communication được ghi.
283. Incident resolution hoạt động.
284. RCA được tạo.
285. RCA có corrective actions.
286. Service Health được ghi.
287. Dependency Health được ghi.
288. Health degradation tạo Alert.
289. Structured logs có correlation.
290. Logs không chứa secret.
291. Tạo Data Repair Request.
292. Repair có source of truth.
293. Repair có dry run.
294. Repair có impact analysis.
295. Repair có rollback plan.
296. Repair cần approval.
297. Repair execute được audit.
298. Repair validation hoạt động.
299. Tạo Approved Data Transfer or Schema Transition Run.
300. Approved transfer mapping được lưu.
301. Approved transfer error report được tạo.
302. Approved transfer reconciliation hoạt động.
303. Tạo Backup Run.
304. Backup có checksum.
305. Backup có encryption reference.
306. Backup verification hoạt động.
307. Backup status được theo dõi.
308. Tạo Restore Run.
309. Restore cần approval.
310. Restore có validation.
311. Restore không bật integration ngoài trái policy.
312. Tạo DR Drill.
313. DR Drill đo RPO.
314. DR Drill đo RTO.
315. Gap được ghi.
316. Environment separation hoạt động.
317. Production credential không dùng Test.
318. Test data được mask.
319. Tạo Release.
320. Release có build/commit reference.
321. Tạo Deployment.
322. Deployment có environment.
323. Deployment failure được ghi.
324. Rollback được ghi.
325. Feature Flag runtime được audit.
326. Tạo Support Session.
327. Support Session có purpose.
328. Support Session có expiry.
329. Support không mặc định xem PII.
330. Tạo Break-glass Request.
331. Break-glass có reason.
332. Break-glass có capabilities.
333. Break-glass có scope.
334. Break-glass cần approval.
335. Break-glass cần MFA/re-auth.
336. Break-glass tự hết hạn.
337. Break-glass actions được audit.
338. Break-glass review hoạt động.
339. Sale chỉ xem Documents trong scope.
340. Team Lead xem Team.
341. Legal xem Legal Dossier.
342. Finance xem Finance evidence.
343. System Admin không tự xem Customer PII.
344. Security xem Security Audit.
345. Director xem summary theo quyền.
346. Backend enforce Legal Entity.
347. Backend enforce resource scope.
348. Backend enforce sensitivity.
349. Sửa URL không mở rộng quyền.
350. View không đồng nghĩa Download.
351. Download không đồng nghĩa Share.
352. Share không đồng nghĩa Export.
353. Same idempotency key cùng payload trả cùng kết quả.
354. Same key khác payload báo conflict.
355. Domain events được phát.
356. Consumers idempotent.
357. Document Dashboard đúng scope.
358. Dossier Dashboard đúng scope.
359. Audit Dashboard đúng scope.
360. Alert Dashboard đúng scope.
361. Integration Dashboard đúng scope.
362. Operations Dashboard đúng scope.
363. Capability sử dụng Configuration Version Platform Configuration Capability.
364. Capability sử dụng Authorization Identity, Access and Organization Capability.
365. Capability không sửa Lead Lead Management Capability.
366. Capability không sửa Customer Party Context.
367. Capability không sửa Listing Product, Asset, Listing and Inventory Capability.
368. Capability không sửa Matching Customer–Product Matching Capability.
369. Capability không sửa Deal Deal and Transaction Capability.
370. Capability không sửa Contract/Payment Contract and Cash Capability.
371. Capability không sửa Revenue/Commission Revenue and Commission Capability.
372. Capability không tạo Interaction song song Activity and Engagement Capability.
373. Capability không tạo Marketing Journey song song Marketing Capability.
374. Capability cung cấp operational data cho Analytics Capability.
375. Capability hoàn thiện dịch vụ hỗ trợ toàn hệ thống mà không tạo nguồn chân lý nghiệp vụ thứ hai.

---

# 206. Quan hệ canonical với các Context liên quan

## 206.1. Platform Context

Platform cung cấp policies, templates, workflows, approvals, retention, schedules, feature flags, connector-profile definitions và secret references.

Runtime Contexts thực thi bằng exact definition/version reference; không tạo control plane cạnh tranh.

## 206.2. IAM Context

IAM/Security cung cấp User, Service Account, roles, scopes, field authorities, delegation và emergency grants.

Operations điều phối support/break-glass session nhưng không tạo identity hoặc permission system riêng.

## 206.3. Lead và Party Contexts

Documents lưu evidence theo governed references; Integration có thể chuyển Lead-intake/identity-resolution commands; Operations gửi notification intents.

Không Context runtime nào sửa identity, care protection, Customer ownership, consent hoặc contact restrictions trực tiếp.

## 206.4. Product và Matching Contexts

Documents quản lý Project/Asset/Listing dossiers và evidence.

Runtime support không đổi Availability, Commercial Lock hoặc Match Result.

## 206.5. Transaction Context

Documents quản lý Proposal/Booking/Deal evidence và Dossier.

Dossier/Signature result không tự chuyển Deal, Hold hoặc Booking state.

## 206.6. Contract Context

Documents quản lý Contract, Payment, Receipt, Refund và Settlement evidence.

Signature completion, OCR result hoặc Dossier completeness không tự làm Contract effective hoặc xác nhận money movement.

## 206.7. Revenue Context

Documents quản lý Revenue/Commission statements và payout evidence.

Runtime support không tạo Revenue Entitlement, Commission Payable, Payout hoặc Clawback.

## 206.8. Activity Context

Activity sở hữu canonical Task, Interaction và Timeline.

Customer communication từ notification/provider runtime phải được phản ánh qua Activity contract; Runtime Support không tạo Interaction source cạnh tranh.

## 206.9. Marketing Context

Marketing sở hữu Campaign/Journey eligibility, audience, suppression và marketing purpose.

Runtime delivery không được lách consent, suppression hoặc frequency policies.

## 206.10. Analytics Context

Analytics sở hữu certified Metrics, analytical Alert/Anomaly, Report/Export definitions và policies.

Documents lưu generated artifacts; Integration thực hiện BI delivery; Operations vận hành jobs. Runtime telemetry được cung cấp cho Analytics qua governed facts.

---

# 207. Anti-patterns và canonical requirements

## AP-RUN-001 — Composite capability trở thành một super-context

**Không được áp dụng**

Gom Documents, Audit, Integration và Operations vào một schema, repository hoặc service layer sở hữu mọi runtime data.

**Canonical requirement**

Bốn Context có aggregate, persistence, API và Events riêng; tài liệu này chỉ là product-level composite overview.

## AP-DOC-001 — File, Document và Dossier là cùng một khái niệm

**Không được áp dụng**

Gắn binary trực tiếp vào resource hoặc dùng folder như hồ sơ hoàn chỉnh.

**Canonical requirement**

File Object, Document Record, Document Version, Context Link và Dossier/Checklist/Snapshot phải tách biệt.

## AP-DOC-002 — Ghi đè verified hoặc signed document

**Không được áp dụng**

Thay file cùng tên hoặc sửa metadata trọng yếu trên Version đã verified/signed.

**Canonical requirement**

Tạo Version mới, giữ original Version/evidence/hash và liên kết supersession/amendment.

## AP-DOC-003 — OCR hoặc signature callback tự sửa business state

**Không được áp dụng**

OCR cập nhật Customer/Payment hoặc provider completion tự làm Contract effective.

**Canonical requirement**

OCR tạo suggestion; callback tạo accepted evidence; owning Context quyết định transition qua API/workflow.

## AP-DOC-004 — Document link mở rộng quyền resource

**Không được áp dụng**

Có quyền xem Document thì tự xem toàn Customer, Contract, Revenue hoặc Call Transcript.

**Canonical requirement**

Backend intersect Document permission, source-resource access, sensitivity, field authority và Legal Entity scope.

## AP-AUD-001 — Audit là technical log có thể update/delete

**Không được áp dụng**

Lưu Audit chung với application logs hoặc sửa/xóa event để “sửa lịch sử”.

**Canonical requirement**

Audit Context giữ append-only facts, correlation và integrity evidence; correction tạo event mới.

## AP-OPS-001 — Alert, Notification và Interaction là một bảng

**Không được áp dụng**

Một record vừa là vấn đề cần xử lý, vừa là delivery, vừa là Customer communication fact.

**Canonical requirement**

Operational Alert, Notification orchestration, provider delivery và Activity Interaction có ownership/lifecycles riêng.

## AP-OPS-002 — Notification runtime bypass consent hoặc marketing policy

**Không được áp dụng**

Operations/Integration gửi Customer message chỉ vì có address hoặc queue item.

**Canonical requirement**

Re-check Party consent/restriction, Marketing purpose/eligibility và Activity outbound rules trước execution.

## AP-INT-001 — Integration tự quyết định source of truth

**Không được áp dụng**

Provider payload hoặc “latest update wins” ghi đè dữ liệu tài chính, pháp lý hoặc identity.

**Canonical requirement**

Source-of-Truth Registry công bố authoritative fields và correction path; owning Context validate every business command.

## AP-INT-002 — Retry/replay không giữ idempotency lineage

**Không được áp dụng**

Retry tạo Lead, Receipt, Interaction, Document, Notification hoặc Payout trùng.

**Canonical requirement**

Side-effect operation phải có stable idempotency key, payload-hash conflict detection, durable result và reconciliation.

## AP-INT-003 — Runtime lưu plain secrets hoặc sensitive payloads trong logs

**Không được áp dụng**

Credentials, tokens, full bank data hoặc document payload được lưu trong application DB/logs.

**Canonical requirement**

Dùng vault references, least privilege, encryption, data minimization, masking và bounded retention.

## AP-OPS-003 — System Administrator có blanket business access

**Không được áp dụng**

Quyền vận hành tự mở Customer PII, bank data, Commission hoặc restricted Documents.

**Canonical requirement**

Technical role và business-data authority tách biệt; sensitive access cần explicit grant, purpose, expiry và Audit.

## AP-OPS-004 — Data Repair bằng SQL tùy tiện

**Không được áp dụng**

Support/Admin sửa production trực tiếp không request, dry run, approval hoặc reconciliation.

**Canonical requirement**

Repair dùng versioned scoped command/script thuộc owning Context, impact analysis, approval, validation, compensation và Audit.

## AP-OPS-005 — Backup thành công đồng nghĩa có thể phục hồi

**Không được áp dụng**

Chỉ kiểm tra backup job status rồi tuyên bố đạt recoverability.

**Canonical requirement**

Backup cần checksum/integrity verification, isolated restore tests, RPO/RTO measurement và remediation tracking.

## AP-OPS-006 — Break-glass là superuser không giới hạn

**Không được áp dụng**

Emergency access không scope, không expiry, không MFA hoặc không post-review.

**Canonical requirement**

IAM/Security cấp time-bound emergency grant; Operations điều phối session; mọi action được Audit và review.

## AP-RUN-002 — Runtime Context sao chép Platform/IAM authority

**Không được áp dụng**

Tạo policy, template, permission hoặc secret registry cạnh tranh trong runtime services.

**Canonical requirement**

Runtime records tham chiếu exact Platform/IAM version/decision; authority vẫn ở owning Context.

## AP-RUN-003 — Cross-context direct write hoặc distributed transaction

**Không được áp dụng**

Operations/Integration/Documents repository sửa aggregate Context khác hoặc khóa transaction xuyên Contexts.

**Canonical requirement**

Dùng local transaction, Outbox, published API/Event, idempotent Process Manager và reconciliation.

## AP-RUN-004 — Candidate examples là exact contracts

**Không được áp dụng**

Dùng table names, endpoints, statuses, Events, permissions, retries hoặc RPO/RTO examples trong tài liệu này để code trực tiếp.

**Canonical requirement**

Exact artifacts phải được khóa trong Context-specific DB/API/Event/Security/Operations sources.

## AP-RUN-005 — Mặc định tồn tại hệ thống tiền nhiệm

**Không được áp dụng**

Tự thiết kế compatibility layer, old-document mappings hoặc data-transfer pipeline khi chưa có approved scope.

**Canonical requirement**

`crm_bds_ai` là Greenfield. Historical import hoặc schema/data transition chỉ tồn tại khi có scope, mapping, security review, rollback/reconciliation và acceptance criteria riêng.

---

# 208. Kết luận

Runtime Support Composite Capability hoàn thiện evidence, audit, integration và operations cho `crm_bds_ai` mà không tạo một super-context hoặc nguồn chân lý cạnh tranh.

Capability phải bảo đảm:

- `documents`, `audit`, `integration` và `operations` vẫn là bốn Bounded Contexts độc lập.
- File Object, Document, Version và Dossier được tách.
- Verified/signed evidence không bị ghi đè.
- OCR/AI extraction chỉ tạo suggestion cho đến khi authoritative workflow chấp nhận.
- Dossier gate cung cấp evidence; owning Context quyết định business transition.
- Audit append-only, có correlation, sensitive-access evidence và integrity verification.
- Alert, Notification, provider delivery và Interaction được tách.
- Party/Marketing/Activity gates được tôn trọng cho Customer communication.
- Integration có Mapping Version, idempotency, source-of-truth policy, DLQ và reconciliation.
- Integration không sửa business source trực tiếp.
- Jobs, queues và replay không tạo side effect trùng.
- Operations không sở hữu domain business aggregates.
- Data Repair dùng versioned governed commands/scripts, không dùng universal direct SQL.
- Backup được chứng minh bằng verify, restore test và DR drill.
- Break-glass authority thuộc IAM/Security; Operations chỉ điều phối session.
- System Administrator không mặc định xem dữ liệu nghiệp vụ nhạy cảm.
- Platform configuration và IAM authorization không bị sao chép.
- Documents, Integration, Operations và Audit phối hợp qua published contracts, Outbox, idempotency và reconciliation.
- Candidate database/API/Event/permission/UI artifacts không được coi là exact contracts.
- Historical import không được mặc định trong Greenfield scope.

> Runtime support cung cấp evidence, transport và operational resilience; business truth vẫn thuộc owning Contexts.
