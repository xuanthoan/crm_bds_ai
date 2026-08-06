# CRM_BDS_AI — CAPABILITY 11: ACTIVITY AND ENGAGEMENT

## Task, Appointment, Call, Interaction, Unified Timeline, SLA and Next Best Action Orchestration

**Document ID:** `PROD-CAP-ACT-001`
**Canonical path:** `docs/product/capabilities/cap-11-activity-and-engagement.md`
**Product:** `crm_bds_ai`
**Version:** `1.0.0`  
**Status:** `Accepted / Product Capability Baseline`
**Document type:** `Product Capability Specification`
**Primary capability code:** `CAP-ACT`
**Primary owning Context:** `activity`
**Owner:** `Product Owner`
**Co-owner:** `Activity Domain Owner`
**Reviewers:** `Architecture Owner`, `IAM Domain Owner`, `Party Domain Owner`, `Lead Domain Owner`, `Product Domain Owner`, `Matching Domain Owner`, `Transaction Domain Owner`, `Contract Domain Owner`, `Revenue Domain Owner`, `Marketing Domain Owner`, `Documents Owner`, `Integration Owner`, `Analytics Owner`, `Audit Owner`, `Security Owner`, `Database Owner`, `API Owner`, `Event Architecture Owner`, `AI Governance Owner`, `Operations Owner`, `QA Owner`
**Effective date:** `2026-08-05`  
**Last reviewed:** `2026-08-05`  
**Classification:** `INTERNAL`

---

# 0. Phạm vi thẩm quyền và quan hệ tài liệu

Tài liệu này là nguồn canonical cho:

- Product outcomes của Activity and Engagement Capability.
- Business meanings của Task, Appointment, Call Log, Interaction, Unified Timeline, SLA Instance và Next Best Action.
- Operational orchestration, assignment, recurrence, attendance, communication history, SLA clocks, escalation và recommendation feedback.
- Capability boundaries, invariants, acceptance outcomes và anti-patterns.
- Đầu vào phân tích cho Activity Context Implementation Pack.

Tài liệu này không phải nguồn exact cho:

- Physical database schema hoặc DDL.
- Exact API paths, payloads, errors hoặc authorization metadata.
- Exact Event names, envelope hoặc payloads.
- Exact permission codes, scopes, masking hoặc role matrix.
- Exact state machines, task/channel codes, SLA thresholds hoặc NBA scoring formulas.
- Exact Calendar, Email, Telephony hoặc Messaging provider implementation.
- Exact File, Document, recording, transcript hoặc attachment storage.
- Exact AI model, prompt, feature set hoặc deployment topology.
- Exact certified productivity, SLA, conversion hoặc NBA Metrics.
- Exact queue, retry, retention, job hoặc deployment configuration.

| Chủ đề | Nguồn canonical |
|---|---|
| Thuật ngữ | Domain Glossary |
| Product requirements | PRD |
| Context ownership | Source of Truth Matrix |
| Architecture boundaries | Architecture Overview, Context Map và Accepted ADRs |
| Activity behavior chi tiết | Activity Context Implementation Pack |
| Database | Activity Context DB Specification và Alembic historical imports |
| API | OpenAPI |
| Events | JSON Schema, AsyncAPI và Event Registry |
| Permissions/scopes/masking/SoD | Security registries và matrices |
| Consent/contact restriction/Party identity | Party Context contracts |
| Workforce/organization/delegation | IAM Context contracts |
| Business source state | Owning Context contracts |
| File/Document/recording/transcript/attachment | Documents Context contracts |
| Calendar/Email/Telephony/Messaging transport | Integration Context contracts |
| Certified activity/SLA/NBA Metrics | Analytics Context và Metric Registry |
| Immutable Audit facts | Audit Context |
| Runtime jobs/incidents | Operations Context |
| Công việc hiện tại | Current Sprint Detailed Execution Pack |

**Capability không đồng nghĩa Bounded Context.** Capability này chủ yếu được thực hiện bởi `activity` Context. Nó điều phối công việc và ghi nhận hoạt động qua published contracts và Events, nhưng không được direct-write aggregate thuộc Context khác.

Các phần candidate lifecycle, data model, operations, permissions, Events, screens, formulas và reports chỉ là design input. Chúng không được dùng thay machine-readable contracts hoặc Context Packs đã được chấp nhận.

---
# 1. Mục tiêu của capability

Activity and Engagement Capability là lớp điều phối công việc và tương tác dùng chung của `crm_bds_ai`.

Capability phải trả lời được:

- Người dùng cần thực hiện hành động nào tiếp theo.
- Task thuộc business context nào và ai chịu trách nhiệm.
- Due time được tính theo clock/calendar nào.
- Task có dependency, checklist, evidence hoặc approval nào.
- Appointment nào sắp diễn ra, có conflict hay thiếu confirmation không.
- Cuộc gọi hoặc Interaction nào thực sự đã xảy ra.
- Customer đã tương tác qua kênh nào và delivery/read evidence đáng tin cậy đến đâu.
- Consent, contact restriction, quiet hours và frequency cap có cho phép outbound action không.
- Timeline của Lead, Customer, Deal, Contract hoặc các resources khác gồm những facts nào.
- Timeline Event nào được phép hiển thị cho audience hiện tại.
- SLA Instance bắt đầu từ Event nào, dùng policy/calendar version nào và đã pause, breach hoặc escalate ra sao.
- Next Best Action nào phù hợp, vì sao và có đủ permission, consent, workflow conditions không.
- Recommendation đã được accept, dismiss, execute hay tạo kết quả gì.
- Handover hoặc delegation ảnh hưởng open work, appointments, SLA và inbox như thế nào.
- Toàn bộ hành động có thể tái tạo từ source references, versions, Events và Audit evidence hay không.

Capability phải hỗ trợ:

- Personal, team, queue, system, workflow, recurring và dependent Tasks.
- Checklist, completion requirements, evidence, reminders và reassignment.
- Appointment, site visit, online meeting, signing, payment và handover appointments.
- Participant, resource, confirmation, attendance, reschedule, cancellation và no-show.
- Inbound, outbound và missed Call Logs với disposition, outcome và follow-up.
- Interaction qua approved Email, SMS, Zalo, chat, social, portal và in-person channels.
- Recording/transcript metadata và governed Document references.
- Unified Timeline có visibility, masking, correction và rebuildability.
- SLA Instance, clock segments, pause, warning, breach, extension và escalation.
- Rule-based và AI-assisted Next Best Action.
- Permission, consent và workflow gates.
- Delegation, handover và Multi-Legal Entity context.
- Integration với Calendar, Email, Telephony và Messaging providers.
- Full idempotency, observability, traceability và Audit evidence.

Nguyên tắc canonical:

> Activity Context điều phối hành động và ghi nhận hoạt động thực tế, nhưng không tự thay đổi business state của owning Context, không giả lập Interaction từ Task, không liên hệ Customer khi chưa đủ consent và không coi recommendation hoặc automation intent là external execution truth.

---
# 2. Vị trí của capability trong kiến trúc

Activity Context sử dụng:

- `platform`: Task/SLA/Notification definitions, Business Calendar, workflow/approval references và configuration.
- `iam`: User, Workforce, organization hierarchy, delegation, acting role, handover, authorization và effective scope.
- `party`: canonical Party/Customer identity, consent, contact preference, contact restriction và redirect.
- `lead`: Lead assignment, care protection, status, source và conversion facts.
- `product`: Project, Asset, Listing, mandate/viewing rights, Availability và Product status.
- `matching`: Match Result, Shortlist, Feedback và stale facts.
- `transaction`: Deal, Proposal, Negotiation, Hold, Booking, Deposit Commitment và transaction next-action facts.
- `contract`: Contract, Receivable, Payment, Receipt, Refund, Settlement và legal/cash facts.
- `revenue`: Revenue, Commission, Payout và Clawback facts.
- `marketing`: Campaign/outbound purpose và campaign-contact context khi cần.
- `documents`: File, Document, recording, transcript và attachment references.
- `integration`: Calendar, Email, Telephony, Messaging và provider transport/runtime facts.
- `operations`: job, queue, retry/DLQ và incident runtime.
- `audit`: immutable evidence của sensitive actions.
- `analytics`: certified activity, SLA, conversion và NBA performance Metrics.

Activity Context cung cấp:

- Cho owning business Contexts: Task, Appointment và Interaction outcomes cùng accepted action requests; owning Context vẫn validate business transition.
- Cho Customer 360 và operational workspaces: permission-aware Timeline projection và activity summaries.
- Cho `marketing`: governed Interaction/contact facts; Marketing vẫn sở hữu Campaign, Audience và Attribution.
- Cho `analytics`: versioned activity/SLA/NBA facts; Analytics vẫn sở hữu certified Metrics.
- Cho `audit`: audit-worthy facts và references.
- Cho users/managers: My Work, Calendar, Inbox, SLA và NBA operational views.

```text
Owning Context fact
→ Task/Appointment/SLA/NBA orchestration
→ User or provider action
→ Call/Interaction/Outcome evidence
→ Owning Context command khi cần
→ Timeline projection
```

Cross-context actions dùng published APIs, durable Events, Transactional Outbox, idempotent consumers và reconciliation. Activity không direct-write source aggregates và không dùng distributed transaction xuyên Contexts.

---
# 3. Ranh giới sở hữu dữ liệu

## 3.1. Activity Context sở hữu

- Task, Task Type, Task Template, Assignment, Queue, Participant, Watcher, Checklist, Dependency, Recurrence, Reminder, Outcome và Completion Evidence references.
- Appointment, type, participants, resources, confirmation, reschedule, attendance, outcome và CRM calendar-sync state.
- Site Visit và Property Viewing operational records.
- Call Log, disposition, outcome, recording/transcript metadata và extraction suggestions.
- Interaction, participants, thread, business delivery/read projection, sensitivity và attachment references.
- Unified Timeline Event projection, relationships, visibility, summaries và corrections.
- SLA Instance, clock segments, pause, extension, escalation, breach và completion state.
- Next Best Action Run, Candidate, Recommendation, explanation, feedback và Activity-side execution state.
- Activity automation domain state và idempotency references.
- Activity-originated business facts và Audit requests.

## 3.2. Activity Context không sở hữu

- Lead, assignment, care protection hoặc conversion state: `lead`.
- Canonical Party/Customer identity, Requirement, consent hoặc contact restriction: `party`.
- Project, Asset, Listing, mandate, Availability hoặc Commercial Lock: `product`.
- Match Result hoặc Matching rules: `matching`.
- Deal, Proposal, Hold, Booking hoặc Deposit Commitment: `transaction`.
- Contract, Payment, Receipt, Refund hoặc Settlement: `contract`.
- Revenue, Commission, Payout hoặc Clawback: `revenue`.
- Campaign, Audience, Journey hoặc Attribution: `marketing`.
- Binary File, Document, Document Version, recording file, transcript artifact hoặc attachment file: `documents`.
- Provider transport, credentials, webhook attempts, retries hoặc raw payload runtime: `integration`.
- Certified productivity, SLA, conversion hoặc NBA Metrics: `analytics`.
- Immutable Audit facts: `audit`.
- Job, queue infrastructure, retry/DLQ hoặc incident runtime: `operations`.

## 3.3. Task và Outcome không thay business state nguồn

Task completion, Appointment outcome, Call disposition, Interaction classification hoặc NBA execution state không tự:

- Qualify hoặc convert Lead.
- Sửa Requirement hoặc consent.
- Hold hoặc Book Listing.
- Chuyển Deal stage.
- Xác nhận Payment hoặc Receipt.
- Làm Contract effective.
- Duyệt Revenue, Commission hoặc Payout.

Khi cần business transition, Activity gửi command tới owning Context. Owning Context thực hiện permission, workflow và invariant validation bằng local transaction.

## 3.4. Documents và content boundary

Activity giữ:

- `document_id` và `document_version_id`.
- Provider object reference khi cần.
- Recording/transcript availability metadata.
- Summary, confidence, model version và review state.
- Access-policy/retention references.

Documents Context sở hữu binary recordings, transcript artifacts, attachments, generated files và Legal Hold.

Permanent URL không phải canonical File/Document identity.

## 3.5. Integration boundary

Integration Context sở hữu:

- Provider connection và credentials.
- Calendar, Email, Telephony và Messaging transport.
- Webhook verification, replay protection và raw payload references.
- Delivery attempts, retries và provider reconciliation.
- External event, message và call IDs ở provider boundary.

Activity sở hữu normalized business records và accepted delivery, call và calendar projections.

## 3.6. Consent boundary

Party Context sở hữu canonical consent, contact preference và contact restriction.

Activity phải re-check authoritative Party policy trước outbound action. Cached consent result chỉ là evidence của lần kiểm tra trước, không phải quyền liên hệ vĩnh viễn.

## 3.7. Timeline, Analytics và Audit boundaries

Activity sở hữu Unified Timeline projection và operational activity facts.

Owning Contexts sở hữu source business facts. Analytics Context sở hữu certified activity, SLA, conversion và NBA Metrics. Audit Context sở hữu immutable Audit facts.

Timeline có thể rebuild từ source facts và không thay source of truth, certified Analytics hoặc Audit Log.

---
# 4. Các khái niệm cốt lõi

## 4.1. Activity

Khái niệm tổng quát đại diện cho một hoạt động.

Activity có thể là:

* Task.
* Appointment.
* Call.
* Interaction.
* System event.
* Workflow action.

Không bắt buộc tạo một bảng Activity duy nhất chứa toàn bộ chi tiết. Có thể dùng lớp tham chiếu chung và bảng chuyên biệt.

## 4.2. Task

Một đơn vị công việc cần được thực hiện bởi một hoặc nhiều người.

## 4.3. Appointment

Một cuộc hẹn có thời gian bắt đầu, kết thúc, người tham gia và địa điểm/kênh cụ thể.

## 4.4. Call

Một cuộc gọi thực tế hoặc một lần thử gọi.

## 4.5. Interaction

Một lần trao đổi hoặc tiếp xúc với Party, Customer, Lead, Partner hoặc hệ thống qua một kênh xác định.

## 4.6. Timeline Event

Một bản ghi lịch sử đã chuẩn hóa, dùng để hiển thị diễn biến của một thực thể.

## 4.7. SLA Instance

Một đồng hồ đo thời gian nghiệp vụ áp dụng cho một mục tiêu cụ thể.

## 4.8. Next Best Action

Một đề xuất có căn cứ về hành động tiếp theo nên được thực hiện.

Next Best Action không phải mệnh lệnh bắt buộc, trừ khi workflow nghiệp vụ đã tạo Task bắt buộc độc lập.

---

# 5. Nguyên tắc thiết kế cốt lõi

## 5.1. Tách kế hoạch và sự kiện thực tế

* Task “Gọi Customer” là kế hoạch.
* Call Log là cuộc gọi thực tế.
* Task hoàn thành có thể liên kết Call Log.
* Không được tự tạo Call Log chỉ vì Task được đánh dấu hoàn thành.

## 5.2. Tách lịch hẹn và tương tác

* Appointment là kế hoạch gặp.
* Attendance và Appointment Outcome ghi nhận việc diễn ra thực tế.
* Interaction ghi nhận nội dung trao đổi.
* No-show không được đánh dấu Completed như cuộc hẹn thành công.

## 5.3. Timeline là projection, không phải nguồn nghiệp vụ chính

Timeline tổng hợp các sự kiện từ nhiều capability.

Không sửa Contract, Receipt hoặc Deal bằng cách sửa Timeline Event.

## 5.4. SLA phải giải thích được

Mỗi SLA phải trả lời:

* Bắt đầu từ sự kiện nào?
* Dùng Business Calendar nào?
* Khoảng thời gian nào được tính?
* Khoảng nào bị pause?
* Vì sao breach?
* Ai chịu trách nhiệm?
* Escalation nào đã được thực hiện?

## 5.5. Next Best Action không được vượt quyền

Hệ thống không đề xuất user thực hiện hành động mà user không có capability hoặc scope phù hợp.

## 5.6. Không tự liên hệ khi chưa đủ điều kiện

Next Best Action có thể đề xuất liên hệ, nhưng trước khi gửi hoặc gọi phải kiểm tra:

* Consent.
* Contact restriction.
* Quiet hours.
* Preferred channel.
* User permission.
* Workflow state.
* Frequency cap.

## 5.7. Timeline lịch sử phải bất biến

Sửa lỗi phải dùng:

* Correction event.
* Redaction theo quy trình.
* Superseding event.
* Audit.

Không xóa hoặc viết lại lịch sử âm thầm.

---

# 6. Activity Context

Mọi Task, Appointment, Call hoặc Interaction phải có thể liên kết đến một hoặc nhiều context:

```text
LEAD
CUSTOMER
PARTY
REQUIREMENT
PARTNER
PROJECT
ASSET
LISTING
MATCHING_RUN
SHORTLIST
DEAL
TRANSACTION_CASE
PROPOSAL
NEGOTIATION
HOLD
BOOKING
DEPOSIT_COMMITMENT
CONTRACT
RECEIVABLE
PAYMENT_TRANSACTION
RECEIPT
REFUND
SETTLEMENT
REVENUE_ENTITLEMENT
REVENUE_RECONCILIATION
COMMISSION_ENTITLEMENT
PAYOUT_BATCH
CLAWBACK_CASE
OTHER
```

## 6.1. Primary Context

Mỗi Activity phải có một primary context.

Ví dụ:

* Task gọi Customer có primary context là Lead.
* Task bổ sung hồ sơ có primary context là Contract.
* Task xác minh tiền có primary context là Payment Transaction.

## 6.2. Secondary Context

Có thể liên kết thêm:

* Customer.
* Deal.
* Listing.
* Project.
* Contract.

## 6.3. Context không mở rộng quyền

User xem được Task không mặc định được xem toàn bộ dữ liệu của các context liên kết.

Backend phải áp dụng:

* Activity permission.
* Resource permission.
* Field masking.
* Context-specific summary.

---

# 7. Task Model

Một Task tối thiểu gồm:

* Task code.
* Tiêu đề.
* Mô tả.
* Task type.
* Primary context.
* Priority.
* Status.
* Assignee.
* Owner.
* Created by.
* Start time.
* Due time.
* SLA reference nếu có.
* Completion requirement.
* Outcome.
* Visibility.
* Audit.

---

# 8. Candidate Task Type vocabulary — pending validation

Các loại chuẩn:

```text
CALL_CUSTOMER
FOLLOW_UP
QUALIFY_LEAD
VERIFY_CUSTOMER_IDENTITY
UPDATE_REQUIREMENT
COLLECT_DOCUMENT
VERIFY_DOCUMENT
SCHEDULE_APPOINTMENT
SITE_VISIT_PREPARATION
SEND_PRODUCT_OPTIONS
CREATE_SHORTLIST
PREPARE_PROPOSAL
FOLLOW_UP_PROPOSAL
NEGOTIATION_FOLLOW_UP
CHECK_LISTING_AVAILABILITY
REQUEST_HOLD
FOLLOW_UP_HOLD
PREPARE_BOOKING
COLLECT_DEPOSIT
FOLLOW_UP_PAYMENT
PREPARE_CONTRACT
LEGAL_REVIEW
FINANCE_REVIEW
SIGNATURE_FOLLOW_UP
RECEIVABLE_COLLECTION
VERIFY_PAYMENT
ISSUE_RECEIPT
PROCESS_REFUND
PROCESS_SETTLEMENT
REVENUE_RECONCILIATION
COMMISSION_REVIEW
PAYOUT_REVIEW
CLAWBACK_REVIEW
CUSTOMER_SERVICE
COMPLAINT_RESOLUTION
DATA_QUALITY_REVIEW
APPROVAL_REQUEST
HANDOVER
OTHER
```

Task Type phải là dictionary/configuration, nhưng system-critical codes không được đổi ý nghĩa.

---

# 9. Candidate Task lifecycle — pending validation

```text
DRAFT
OPEN
READY
IN_PROGRESS
WAITING_CUSTOMER
WAITING_INTERNAL
WAITING_PARTNER
WAITING_APPROVAL
WAITING_SYSTEM
BLOCKED
DEFERRED
COMPLETED
COMPLETED_WITH_EXCEPTION
CANCELLED
FAILED
EXPIRED
ARCHIVED
```

## 9.1. OPEN

Task đã được tạo và có thể thực hiện.

## 9.2. READY

Các dependency bắt buộc đã hoàn thành.

## 9.3. WAITING

Task đang chờ một tác nhân bên ngoài hoặc điều kiện.

Trạng thái Waiting không tự pause SLA. Việc pause phụ thuộc SLA Policy.

## 9.4. COMPLETED_WITH_EXCEPTION

Task hoàn thành nhưng có sai lệch hoặc thiếu điều kiện được phép.

Phải có:

* Exception code.
* Lý do.
* Approval nếu cần.
* Follow-up task nếu cần.

---

# 10. Task Priority và Urgency

## 10.1. Priority

```text
CRITICAL
URGENT
HIGH
NORMAL
LOW
```

## 10.2. Urgency không đồng nghĩa Importance

Có thể tính riêng:

* Business impact.
* Time urgency.
* Customer risk.
* Financial risk.
* Legal risk.
* Inventory risk.

## 10.3. Priority Override

Manager có thể thay Priority với:

* Reason.
* Before/after.
* Audit.

System-generated Critical Task không được tự hạ thấp nếu user không có quyền.

---

# 11. Task Responsibility

Phải tách:

* Task owner.
* Primary assignee.
* Supporting assignee.
* Reviewer.
* Approver.
* Watcher.

## 11.1. Task Owner

Chịu trách nhiệm nghiệp vụ tổng thể.

## 11.2. Primary Assignee

Người trực tiếp thực hiện.

## 11.3. Supporting Assignee

Người phối hợp, không thay trách nhiệm chính.

## 11.4. Reviewer

Kiểm tra kết quả.

## 11.5. Approver

Duyệt khi Task là bước của Approval Workflow.

---

# 12. Task Assignment

Assignment có thể dựa trên:

* User cụ thể.
* Role.
* Position.
* Team.
* Department.
* Resource owner.
* Round-robin.
* Workload.
* Skill.
* Project assignment.
* Legal Entity.
* Delegation.
* Acting role.
* Queue.

## 12.1. Queue Assignment

Task có thể được đưa vào queue:

* Lead qualification queue.
* Legal review queue.
* Finance verification queue.
* Revenue reconciliation queue.

User claim Task phải có quyền.

## 12.2. Assignment Snapshot

Lưu:

* Assignee.
* Role.
* Team.
* Department.
* Legal Entity.
* Assignment rule version.
* Effective time.

---

# 13. Task Reassignment

Reassignment phải có:

* From assignee.
* To assignee.
* Reason.
* Effective time.
* Current progress.
* SLA impact.
* Handover note.
* Approval nếu cần.

Reassignment không được:

* Xóa lịch sử người cũ.
* Thay Lead attribution.
* Thay Deal commission participant.
* Reset SLA nếu policy không cho phép.

---

# 14. Task Watcher và Follower

Watcher nhận cập nhật nhưng không chịu trách nhiệm hoàn thành.

Watcher có thể gồm:

* Manager.
* Deal owner.
* Customer owner.
* Legal reviewer.
* Finance reviewer.
* Project manager.

Watcher không tự có quyền xem dữ liệu nhạy cảm trong Task.

---

# 15. Task Dependency

Các kiểu dependency:

```text
FINISH_TO_START
START_TO_START
FINISH_TO_FINISH
BLOCKING
INFORMATION_REQUIRED
APPROVAL_REQUIRED
EVENT_REQUIRED
```

## 15.1. Dependency Gate

Task chỉ chuyển `READY` khi các dependency bắt buộc đạt điều kiện.

## 15.2. Circular Dependency

Hệ thống phải phát hiện và chặn vòng lặp dependency.

## 15.3. Cross-capability Dependency

Ví dụ:

* Task “Phát hành Receipt” chờ Payment Allocation approved.
* Task “Gửi Contract ký” chờ Legal Review hoàn thành.
* Task “Tạo Payout Batch” chờ Payout Period locked.

---

# 16. Task Checklist

Task có thể có nhiều checklist item:

* Required/optional.
* Assignee.
* Due date.
* Evidence.
* Status.
* Completion timestamp.

Task không được Completed nếu checklist bắt buộc chưa hoàn thành, trừ exception workflow.

---

# 17. Task Completion Requirement

Có thể yêu cầu:

* Outcome code.
* Note.
* Call Log.
* Interaction.
* File evidence.
* Approval.
* Data field update tại capability nguồn.
* Customer response.
* Checklist.
* Next Task.

Ví dụ Task “Gọi Customer” có thể yêu cầu:

* Call Log.
* Call disposition.
* Next follow-up date.

---

# 18. Candidate Task Outcome vocabulary — pending validation

Các outcome chung:

```text
SUCCESS
PARTIAL_SUCCESS
NO_RESPONSE
CUSTOMER_DECLINED
RESCHEDULED
WAITING_INFORMATION
ESCALATED
NOT_APPLICABLE
FAILED
DUPLICATE
COMPLETED_BY_OTHER_PROCESS
OTHER
```

Task Type có thể định nghĩa outcome riêng.

---

# 19. Task Creation Source

Task có thể được tạo từ:

* User.
* Workflow transition.
* SLA warning.
* SLA breach.
* Domain event.
* Next Best Action acceptance.
* Template.
* Recurrence.
* Import.
* API.
* Integration.
* Manager assignment.
* Handover.
* Data quality rule.

Mỗi Task phải lưu source.

---

# 20. Task Template

Task Template gồm:

* Template code.
* Title template.
* Description template.
* Task type.
* Priority.
* Assignment rule.
* Due rule.
* Checklist.
* Completion requirements.
* Reminder policy.
* SLA policy.
* Visibility.
* Context requirements.
* Effective dates.
* Version.

Template active không được sửa trực tiếp.

---

# 21. Task Due Rule

Có thể dựa trên:

```text
FIXED_DATETIME
MINUTES_AFTER_EVENT
HOURS_AFTER_EVENT
BUSINESS_HOURS_AFTER_EVENT
CALENDAR_DAYS_AFTER_EVENT
BUSINESS_DAYS_AFTER_EVENT
BEFORE_MILESTONE
AT_MILESTONE
CUSTOM_FORMULA
```

Phải lưu:

* Source event.
* Rule version.
* Resolved due time.
* Calendar version.
* Timezone.

---

# 22. Task Recurrence

Hỗ trợ:

* Daily.
* Weekly.
* Monthly.
* Custom recurrence.
* Business day recurrence.
* Until date.
* Maximum occurrences.
* Skip holidays.
* Catch-up policy.

## 22.1. Recurring Task Instance

Mỗi lần chạy phải tạo instance riêng.

Không dùng một Task duy nhất thay đổi due date liên tục.

## 22.2. Recurrence khi instance cũ chưa hoàn thành

Policy:

* Vẫn tạo instance mới.
* Gộp.
* Chặn.
* Escalate.
* Skip.

---

# 23. Task Reminder

Có thể nhắc:

* Trước hạn.
* Đúng hạn.
* Sau hạn.
* Khi dependency hoàn thành.
* Khi priority thay đổi.
* Khi reassigned.

Kênh:

* In-app.
* Email.
* Push.
* SMS.
* Chat integration.

Reminder phải chống trùng.

---

# 24. Task Overdue

Task được coi Overdue khi:

* Due time đã qua.
* Chưa hoàn thành.
* Không bị pause theo rule.
* Không cancelled/expired.

Overdue không tự đổi Task thành Failed.

---

# 25. Task Completion

Khi hoàn thành:

* Validate checklist.
* Validate completion requirement.
* Lưu outcome.
* Lưu evidence.
* Stop SLA clock nếu policy.
* Phát event.
* Tạo follow-up task nếu rule.
* Không tự thay capability nguồn ngoài workflow.

---

# 26. Task Reopen

Chỉ được reopen khi:

* Kết quả sai.
* Bị capability nguồn từ chối.
* Evidence không hợp lệ.
* Event bị reversal.
* Manager yêu cầu.

Reopen phải:

* Có reason.
* Giữ completion lịch sử.
* Tạo SLA handling mới hoặc tiếp tục theo policy.
* Không xóa outcome cũ.

---

# 27. Task Cancellation

Cancellation reason:

* Duplicate.
* Source resource cancelled.
* No longer required.
* Completed elsewhere.
* Incorrectly created.
* Workflow replaced.
* Customer withdrew.
* Other.

Task cancellation không tự cancel resource nguồn.

---

# 28. Bulk Task Operations

Có thể hỗ trợ:

* Bulk assign.
* Bulk change due date.
* Bulk priority.
* Bulk close duplicate.
* Bulk archive.

Không cho bulk:

* Hoàn thành Task yêu cầu evidence riêng.
* Duyệt Task tài chính/pháp lý.
* Thay outcome Customer.
* Bỏ qua SLA exception.

Bulk action phải audit từng item.

---

# 29. Appointment Model

Appointment gồm:

* Appointment code.
* Type.
* Subject.
* Context.
* Organizer.
* Participants.
* Start/end.
* Timezone.
* Location/channel.
* Status.
* Confirmation.
* Reminder.
* Attendance.
* Outcome.
* Follow-up.
* External calendar references.

---

# 30. Candidate Appointment Type vocabulary — pending validation

```text
PHONE_APPOINTMENT
ONLINE_MEETING
OFFICE_MEETING
CUSTOMER_SITE_VISIT
PROJECT_SITE_VISIT
PROPERTY_VIEWING
OWNER_MEETING
NEGOTIATION_MEETING
BOOKING_APPOINTMENT
CONTRACT_SIGNING
PAYMENT_APPOINTMENT
NOTARY_APPOINTMENT
HANDOVER_APPOINTMENT
LEGAL_MEETING
FINANCE_REVIEW_MEETING
INTERNAL_MEETING
OTHER
```

---

# 31. Candidate Appointment lifecycle — pending validation

```text
DRAFT
PROPOSED
PENDING_CONFIRMATION
CONFIRMED
RESCHEDULE_REQUESTED
RESCHEDULED
IN_PROGRESS
COMPLETED
PARTIALLY_ATTENDED
CUSTOMER_NO_SHOW
INTERNAL_NO_SHOW
CANCELLED_BY_CUSTOMER
CANCELLED_BY_INTERNAL
CANCELLED_BY_PARTNER
FAILED
EXPIRED
```

---

# 32. Appointment Participants

Có thể gồm:

* User.
* Employee.
* Customer.
* Party.
* Partner.
* Owner.
* Developer representative.
* External attendee.

Mỗi participant có:

* Role.
* Required/optional.
* Invitation status.
* Confirmation.
* Attendance.
* Contact channel.
* Visibility.

---

# 33. Appointment Organizer và Owner

Organizer là người tạo hoặc quản lý lịch.

Appointment owner là người chịu trách nhiệm kết quả.

Hai người có thể khác nhau.

---

# 34. Appointment Scheduling

Khi tạo lịch phải kiểm tra:

* User availability.
* Required participant availability nếu có calendar access.
* Resource availability.
* Project opening hours.
* Customer preferred time.
* Timezone.
* Travel buffer.
* Existing appointments.
* Quiet hours.
* Business Calendar.

---

# 35. Scheduling Conflict

Các loại conflict:

```text
USER_TIME_CONFLICT
RESOURCE_CONFLICT
TRAVEL_TIME_CONFLICT
PROJECT_CLOSED
CUSTOMER_RESTRICTION
OUTSIDE_BUSINESS_HOURS
TIMEZONE_RISK
DUPLICATE_APPOINTMENT
```

Conflict có thể:

* Chặn.
* Cảnh báo.
* Cho override có reason.

---

# 36. Appointment Resource

Có thể đặt:

* Meeting room.
* Vehicle.
* Show unit.
* Project tour slot.
* Property access slot.
* Video meeting account.
* Interpreter.
* Project specialist.

Resource booking phải có:

* Availability.
* Capacity.
* Owner.
* Confirmation.
* Release policy.

---

# 37. Appointment Location

Có thể là:

* Office.
* Project.
* Property.
* Owner address.
* Notary office.
* Online meeting URL.
* External place.

Exact private property address phải field-mask theo Listing Access.

---

# 38. Appointment Confirmation

Hệ thống theo dõi:

* Internal confirmation.
* Customer confirmation.
* Partner confirmation.
* Resource confirmation.

Appointment `CONFIRMED` theo policy khi đủ required confirmation.

---

# 39. Appointment Invitation

Invitation lưu:

* Channel.
* Recipient.
* Message template.
* Sent at.
* Delivered at.
* Accepted/declined.
* External calendar event ID.
* Consent check.
* Timezone display.

---

# 40. Reschedule

Reschedule phải lưu:

* Old time.
* New time.
* Requester.
* Reason.
* Participant responses.
* Resource impact.
* SLA impact.
* Version.

Không ghi đè thời gian cũ mà không có history.

---

# 41. Appointment Cancellation

Cancellation phải xác định:

* Người hủy.
* Lý do.
* Thời gian.
* Có thông báo participant không.
* Resource release.
* Follow-up requirement.
* No-show hay cancel.

---

# 42. No-show

Phân biệt:

* Customer no-show.
* Internal no-show.
* Partner no-show.
* Unknown.

No-show phải có:

* Attendance evidence.
* Contact attempt.
* Follow-up task.
* Customer impact.
* SLA impact.

Không tự đánh dấu Customer no-show khi organizer không tham dự.

---

# 43. Candidate Appointment Attendance vocabulary — pending validation

Mỗi participant có:

```text
EXPECTED
CONFIRMED
ATTENDED
LATE
LEFT_EARLY
NO_SHOW
CANCELLED
UNKNOWN
```

---

# 44. Candidate Appointment Outcome vocabulary — pending validation

Ví dụ:

```text
CUSTOMER_INTERESTED
CUSTOMER_NEEDS_TIME
FOLLOW_UP_REQUIRED
PRODUCT_REJECTED
PRODUCT_SHORTLISTED
NEGOTIATION_STARTED
BOOKING_REQUESTED
DOCUMENTS_COLLECTED
CONTRACT_SIGNED
PAYMENT_COMMITTED
HANDOVER_COMPLETED
NO_DECISION
FAILED
OTHER
```

Outcome phải được capability nguồn xác nhận trước khi tạo transition nghiệp vụ.

---

# 45. Site Visit

Site Visit mở rộng Appointment với:

* Project/Listing.
* Visit purpose.
* Attending sale.
* Project specialist.
* Check-in/out.
* Customer count.
* Transport.
* Access authorization.
* Products viewed.
* Feedback.
* Photos/files metadata.
* Visit result.
* Follow-up.

---

# 46. Property Viewing

Đối với Listing ký gửi/private:

* Kiểm tra viewing right trong Mandate.
* Kiểm tra owner approval.
* Bảo vệ exact address.
* Không tiết lộ Owner contact.
* Lưu viewing confirmation.
* Lưu access instruction an toàn.
* Ghi nhận no-show hoặc cancellation.

---

# 47. External Calendar Integration

Hỗ trợ:

* Google Calendar.
* Microsoft Calendar.
* CalDAV hoặc provider khác.

Phải lưu:

* Provider.
* External event ID.
* Sync direction.
* Sync status.
* Last synced at.
* Conflict status.
* Payload version.

Không tự xóa Appointment CRM khi external event bị xóa nếu chưa qua sync policy.

---

# 48. Calendar Sync Conflict

Các trường hợp:

* CRM updated và external updated đồng thời.
* External cancelled.
* Participant changed.
* Time changed.
* Recurrence mismatch.

Resolution policy:

* CRM wins.
* External wins.
* Latest update wins.
* Manual review.
* Field-specific merge.

---

# 49. Call Model

Call Log gồm:

* Call code.
* Direction.
* Caller.
* Callee.
* Phone identity.
* Lead/Customer/Party.
* Context.
* Start/end.
* Duration.
* Provider.
* External call ID.
* Status.
* Disposition.
* Outcome.
* Recording.
* Transcript.
* Follow-up.
* Consent.
* Created by/source.

---

# 50. Candidate Call Direction vocabulary — pending validation

```text
OUTBOUND
INBOUND
INTERNAL
CONFERENCE
CALLBACK
```

---

# 51. Candidate Call lifecycle — pending validation

```text
INITIATED
RINGING
CONNECTED
COMPLETED
NO_ANSWER
BUSY
FAILED
CANCELLED
VOICEMAIL
MISSED
BLOCKED
UNKNOWN
```

---

# 52. Candidate Call Disposition vocabulary — pending validation

```text
CONNECTED_MEANINGFUL
CONNECTED_SHORT
NO_ANSWER
BUSY
WRONG_NUMBER
INVALID_NUMBER
CALL_BACK_REQUESTED
NOT_INTERESTED
INTERESTED
QUALIFIED
FOLLOW_UP_REQUIRED
APPOINTMENT_SCHEDULED
PROPOSAL_REQUESTED
COMPLAINT
DO_NOT_CONTACT_REQUEST
OTHER
```

Disposition code phải có dictionary theo scope nhưng mã cốt lõi ổn định.

---

# 53. Call Outcome

Call Outcome có thể cập nhật:

* Lead qualification suggestion.
* Requirement update suggestion.
* Appointment proposal.
* Follow-up Task.
* Contact restriction request.
* Customer feedback.

Không tự cập nhật dữ liệu nguồn nếu cần user xác nhận.

---

# 54. Click-to-Call

Luồng:

1. User chọn số được phép.
2. Backend kiểm tra Customer scope.
3. Kiểm tra contact restriction.
4. Kiểm tra quiet hours.
5. Mask/resolve số theo provider.
6. Tạo call initiation.
7. Provider thực hiện.
8. Nhận webhook.
9. Tạo Call Log.
10. Yêu cầu disposition.
11. Cập nhật Timeline.

---

# 55. Call Recording

Recording metadata gồm:

* Provider recording ID.
* URL/reference.
* Duration.
* File type.
* Retention.
* Access policy.
* Consent basis.
* Encryption.
* Available until.
* Deleted/redacted status.

Documents Context sở hữu recording artifact; Activity chỉ giữ metadata và governed Document reference.

---

# 56. Recording Consent

Trước recording phải xác định:

* Jurisdiction/policy.
* Customer consent.
* Employee notice.
* Provider capability.
* Recording purpose.
* Retention.

Không được bật recording ngầm ngoài policy.

---

# 57. Call Transcript

Transcript có thể từ:

* Telephony provider.
* Speech-to-text service.
* Manual note.

Phải lưu:

* Source.
* Language.
* Confidence.
* Speaker separation.
* Generated at.
* Model/version.
* Sensitive data flags.
* Review status.

Transcript AI không được coi là sự thật tuyệt đối.

---

# 58. Transcript Extraction

AI có thể đề xuất:

* Requirement criteria.
* Follow-up date.
* Customer objection.
* Budget.
* Product interest.
* Sentiment.
* Do-not-contact request.
* Complaint.
* Promise to pay.

Mọi cập nhật nghiệp vụ quan trọng phải được user xác nhận hoặc workflow tự động được phê duyệt.

---

# 59. Telephony Integration

Hỗ trợ:

* Cloud PBX.
* SIP provider.
* Call center.
* Mobile dialer integration.
* WebRTC.

Integration webhook handling phải:

* Có signature.
* Chống replay.
* Idempotent.
* Map provider status.
* Giữ raw payload reference.
* Không tin phone number từ frontend.

---

# 60. Interaction Model

Interaction là bản ghi một lần giao tiếp hoặc tiếp xúc.

Gồm:

* Interaction code.
* Channel.
* Direction.
* Type.
* Sender.
* Recipients.
* Context.
* Subject.
* Summary.
* Content reference.
* Occurred at.
* Delivery/read status.
* Consent.
* External ID.
* Thread.
* Attachments.
* Visibility.
* Source.

---

# 61. Candidate Interaction Channel vocabulary — pending validation

```text
PHONE
EMAIL
SMS
ZALO
WHATSAPP
MESSENGER
SOCIAL_MESSAGE
WEB_CHAT
IN_APP_CHAT
VIDEO_CALL
IN_PERSON
MEETING
SYSTEM
DOCUMENT
PORTAL
OTHER
```

Kênh được bật theo Integration và Feature Flag.

---

# 62. Candidate Interaction Direction vocabulary — pending validation

```text
INBOUND
OUTBOUND
INTERNAL
SYSTEM_GENERATED
BIDIRECTIONAL
```

---

# 63. Candidate Interaction Type vocabulary — pending validation

```text
GENERAL_COMMUNICATION
LEAD_INQUIRY
QUALIFICATION
FOLLOW_UP
PRODUCT_INTRODUCTION
PROPOSAL_DELIVERY
PROPOSAL_RESPONSE
APPOINTMENT_CONFIRMATION
NEGOTIATION
HOLD_CONFIRMATION
BOOKING_COMMUNICATION
PAYMENT_REMINDER
PAYMENT_CONFIRMATION
CONTRACT_COMMUNICATION
DOCUMENT_REQUEST
DOCUMENT_DELIVERY
RECEIPT_DELIVERY
REFUND_COMMUNICATION
SETTLEMENT_COMMUNICATION
REVENUE_RECONCILIATION
COMMISSION_COMMUNICATION
COMPLAINT
CONSENT_UPDATE
DO_NOT_CONTACT_REQUEST
SYSTEM_NOTIFICATION
OTHER
```

---

# 64. Interaction Participant

Có thể gồm:

* User.
* Customer.
* Party.
* Partner.
* Legal Entity.
* System.
* External address/number chưa xác định.

Mỗi participant có:

* Role.
* Address/phone reference.
* Identity confidence.
* Masked display.
* Sender/recipient.
* Delivery status.

---

# 65. Interaction Thread

Thread gom nhiều Interaction cùng cuộc hội thoại.

Ví dụ:

* Email thread.
* Zalo conversation.
* Proposal discussion.
* Revenue reconciliation conversation.

Thread có:

* External thread ID.
* Primary context.
* Participants.
* Subject.
* Last interaction.
* Status.
* Owner.
* Visibility.

---

# 66. Interaction Content

Nội dung có thể được lưu:

* Toàn văn.
* Snippet.
* Summary.
* External reference.
* Encrypted content.
* Metadata-only.

Policy phụ thuộc:

* Kênh.
* Consent.
* Data retention.
* Provider terms.
* Field sensitivity.

---

# 67. Interaction Attachment

Lưu metadata:

* Filename.
* MIME type.
* Size.
* URL.
* Hash.
* Provider.
* Malware scan status.
* Access policy.
* Retention.
* Related document type.

Không tự coi attachment là hồ sơ hợp lệ của Contract hoặc Customer trước khi capability nguồn xác minh.

---

# 68. Candidate Delivery and Read projections — pending validation

```text
DRAFT
QUEUED
SENT
DELIVERED
READ
FAILED
BOUNCED
REJECTED
EXPIRED
CANCELLED
UNKNOWN
```

Read status chỉ có giá trị khi provider cung cấp đáng tin cậy.

---

# 69. Communication Consent

Trước outbound Interaction phải kiểm tra:

* Consent purpose.
* Channel.
* Legal basis.
* Contact restriction.
* Do-not-contact.
* Preferred time.
* Quiet hours.
* Frequency cap.
* Sender identity.
* Template approval.

---

# 70. Do-not-contact Request

Khi Interaction ghi nhận yêu cầu không liên hệ:

* Tạo consent/restriction update request.
* Có thể áp dụng ngay theo policy an toàn.
* Chặn outbound tiếp theo.
* Thông báo responsible sale.
* Ghi Timeline.
* Audit.

Không chờ sale tự cập nhật nếu Customer yêu cầu rõ ràng và policy cho phép áp dụng ngay.

---

# 71. Quiet Hours

Quiet Hours có thể dựa trên:

* Customer timezone.
* Enterprise policy.
* Channel.
* Day of week.
* Holiday.
* Emergency exception.

System-generated payment/legal notice có thể có rule riêng nhưng vẫn phải tuân thủ policy.

---

# 72. Frequency Cap

Giới hạn:

* Số cuộc gọi/ngày.
* Số message/ngày.
* Số email/tuần.
* Số lần follow-up không phản hồi.
* Số campaign contact.

Frequency cap phải xem xét tương tác từ nhiều user để tránh Customer bị liên hệ quá mức.

---

# 73. Interaction Duplicate Detection

Dựa trên:

* External message ID.
* Provider event ID.
* Sender/recipient.
* Timestamp.
* Content hash.
* Thread.
* Channel.

Webhook lặp không được tạo Interaction trùng.

---

# 74. Internal Note và Customer Communication

Phải tách:

* Internal Note.
* Customer-visible message.
* Partner-visible message.
* System note.

Internal Note không được gửi ra ngoài.

---

# 75. Sensitive Interaction

Các Interaction có thể chứa:

* Identity.
* Financial details.
* Legal dispute.
* Bank information.
* Commission.
* Internal pricing.

Phải có:

* Sensitivity classification.
* Restricted visibility.
* Field masking.
* Access audit.
* Retention.

---

# 76. Unified Timeline

## 76.1. Mục tiêu

Timeline hiển thị chuỗi sự kiện theo thời gian của:

* Lead.
* Customer.
* Requirement.
* Listing.
* Deal.
* Transaction Case.
* Booking.
* Contract.
* Revenue.
* Commission.

## 76.2. Timeline không phải bảng note tự do

Timeline là projection từ:

* Domain Event.
* Task.
* Appointment.
* Call.
* Interaction.
* Status change.
* Approval.
* Document event.
* Payment event.
* System alert.

---

# 77. Candidate Timeline Event Type vocabulary — pending validation

Ví dụ:

```text
RESOURCE_CREATED
RESOURCE_UPDATED
STATUS_CHANGED
ASSIGNMENT_CHANGED
TASK_CREATED
TASK_COMPLETED
TASK_OVERDUE
APPOINTMENT_SCHEDULED
APPOINTMENT_COMPLETED
APPOINTMENT_NO_SHOW
CALL_COMPLETED
INTERACTION_RECEIVED
INTERACTION_SENT
DOCUMENT_UPLOADED
DOCUMENT_APPROVED
PROPOSAL_SENT
PROPOSAL_VIEWED
HOLD_ACTIVATED
BOOKING_CREATED
DEPOSIT_CONFIRMED
CONTRACT_SIGNED
PAYMENT_RECEIVED
RECEIPT_ISSUED
REFUND_PAID
SETTLEMENT_PAID
REVENUE_RECOGNIZED
COMMISSION_PAYABLE
PAYOUT_PAID
CLAWBACK_CREATED
SLA_WARNING
SLA_BREACHED
NEXT_BEST_ACTION_GENERATED
AUDIT_CORRECTION
OTHER
```

---

# 78. Timeline Event Structure

Mỗi event gồm:

* Event code.
* Event type.
* Occurred at.
* Recorded at.
* Actor.
* Source system.
* Source capability.
* Source resource.
* Primary context.
* Related contexts.
* Summary.
* Details reference.
* Sensitivity.
* Visibility.
* Correlation ID.
* Causation ID.
* Event schema version.

---

# 79. Occurred At và Recorded At

Phải tách:

* `occurred_at`: thời điểm sự kiện thực tế.
* `recorded_at`: thời điểm CRM ghi nhận.

Ví dụ cuộc gặp hôm qua được nhập hôm nay.

---

# 80. Timeline Immutability

Timeline Event đã ghi không sửa trực tiếp.

Khi cần correction:

* Tạo Correction Event.
* Link original event.
* Nêu reason.
* Mask/supersede phần hiển thị theo policy.
* Giữ audit.

---

# 81. Timeline Visibility

Có thể gồm:

```text
PRIVATE_TO_CREATOR
ASSIGNED_USERS
TEAM
DEPARTMENT
LEGAL_ENTITY
PROJECT
RESOURCE_SCOPE
SPECIFIC_ROLES
ALL_AUTHORIZED
```

Visibility không được rộng hơn quyền resource nguồn.

---

# 82. Timeline Field Masking

Ví dụ sale có thể thấy:

> Finance đã xác nhận thanh toán.

Nhưng không thấy:

* Bank account đầy đủ.
* Raw bank transaction.
* Internal settlement calculation.

Timeline Renderer phải tạo summary theo audience.

---

# 83. Timeline Merge khi Customer Merge

Khi Customer A merge vào Customer B:

* Timeline A được liên kết canonical Customer B.
* Giữ original Customer reference.
* Không nhân đôi event.
* Không thay event source.
* Search và display redirect về Customer B.
* Các event bị restricted vẫn giữ restriction.

---

# 84. Timeline Grouping

Có thể group theo:

* Ngày.
* Conversation.
* Workflow.
* Transaction Case.
* Contract.
* Channel.
* Event chain.

Không thay đổi thứ tự xảy ra thực tế.

---

# 85. Timeline Search và Filter

Cho phép lọc:

* Event type.
* Capability.
* Actor.
* Channel.
* Date.
* Deal/Contract.
* Sensitive/normal.
* Customer-facing/internal.
* SLA.
* Task.
* Appointment.

Search phải tuân thủ field masking.

---

# 86. Timeline Retention

Retention theo:

* Event type.
* Legal requirement.
* Contract status.
* Consent.
* Recording policy.
* Litigation/legal hold.
* Enterprise policy.

Legal Hold phải ngăn purge.

---

# 87. SLA Framework

## 87.1. SLA Definition

SLA Definition thuộc Platform Configuration Capability.

Activity and Engagement Capability sở hữu SLA Instance và vận hành đồng hồ.

## 87.2. SLA Target

SLA có thể áp dụng cho:

* Task completion.
* First response.
* Follow-up.
* Approval.
* Appointment scheduling.
* Call back.
* Hold confirmation.
* Contract review.
* Payment verification.
* Receipt issuance.
* Refund.
* Revenue reconciliation.
* Commission dispute.

---

# 88. SLA Instance

Mỗi instance gồm:

* SLA code.
* Policy version.
* Resource.
* Target type.
* Responsible user/team.
* Start event.
* Start time.
* Due time.
* Calendar.
* Pause duration.
* Warning threshold.
* Breach time.
* Status.
* Escalation.
* Completion event.

---

# 89. Candidate SLA lifecycle — pending validation

```text
PENDING_START
RUNNING
WARNING
AT_RISK
PAUSED
BREACHED
COMPLETED_WITHIN_SLA
COMPLETED_AFTER_SLA
CANCELLED
EXEMPTED
INVALIDATED
```

---

# 90. SLA Start

SLA bắt đầu từ một event rõ ràng:

* Lead assigned.
* Customer inbound interaction.
* Task ready.
* Proposal viewed.
* Hold requested.
* Booking approved.
* Payment received.
* Contract handoff received.
* Reconciliation created.

Không dùng `created_at` mặc định cho mọi SLA.

---

# 91. Candidate SLA Clock vocabulary — pending validation

Clock có thể tính:

```text
REAL_TIME_24_7
CALENDAR_HOURS
CALENDAR_DAYS
BUSINESS_HOURS
BUSINESS_DAYS
CUSTOM_CALENDAR
```

Phải lưu Business Calendar Version.

---

# 92. Candidate SLA Pause reasons — pending validation

Pause reason:

```text
WAITING_CUSTOMER
WAITING_PARTNER
WAITING_EXTERNAL_SYSTEM
WAITING_REQUIRED_DOCUMENT
WAITING_APPROVAL
LEGAL_HOLD
SYSTEM_OUTAGE
AUTHORIZED_EXCEPTION
OTHER
```

Không phải mọi trạng thái Waiting đều tự pause.

---

# 93. SLA Pause Approval

Pause có thể:

* Tự động theo rule.
* User request.
* Manager approval.
* System outage integration.

Lưu:

* Start.
* End.
* Reason.
* Evidence.
* Actor.
* Approval.
* Duration.

---

# 94. SLA Warning

Có thể cảnh báo tại:

* 50%.
* 75%.
* 90%.
* Thời gian cố định trước hạn.
* Dynamic threshold.

Cảnh báo phải chống trùng.

---

# 95. SLA Breach

Khi breach:

* Ghi breach event.
* Cập nhật health.
* Thông báo assignee.
* Escalate manager.
* Có thể tạo Critical Task.
* Không tự approve/reject/cancel nghiệp vụ.

---

# 96. Candidate SLA Escalation levels — pending validation

Các mức:

```text
LEVEL_1_ASSIGNEE
LEVEL_2_TEAM_LEAD
LEVEL_3_DEPARTMENT_HEAD
LEVEL_4_DIRECTOR
SPECIALIST_QUEUE
CONTROL_FUNCTION
```

Escalation route lấy từ organization snapshot và Platform Configuration Capability.

---

# 97. SLA Extension

Extension phải có:

* Requested duration.
* Reason.
* Impact.
* Requested by.
* Approver.
* New due time.
* Policy.
* Customer/partner responsibility nếu có.

Không chỉnh due time trực tiếp.

---

# 98. SLA Exemption và Waiver

Dùng khi:

* SLA không áp dụng.
* Dữ liệu historical import.
* System incident.
* Force majeure.
* Business-approved exception.

Waiver không xóa breach lịch sử nếu breach đã xảy ra.

---

# 99. SLA Invalidation

SLA có thể invalidated khi:

* Resource tạo trùng.
* Source event reversed.
* Workflow sai.
* Record cancelled trước khi SLA bắt đầu hợp lệ.

Phải lưu reason và approval.

---

# 100. SLA theo Lead Management Capability – Lead

Ví dụ:

* Thời gian nhận Lead.
* First contact.
* Số lần contact.
* Follow-up.
* Qualification.
* Lead recycling.
* Lead handover.

---

# 101. SLA theo Customer 360 Capability – Customer và Requirement

* Bổ sung Requirement.
* Xác minh Financial Profile.
* Cập nhật stakeholder.
* Phản hồi Customer request.
* Data quality correction.

---

# 102. SLA theo Product and Matching Capabilities – Listing và Matching

* Availability confirmation.
* Listing verification.
* Matching run.
* Shortlist preparation.
* Alternative recommendation.
* Feedback update.

---

# 103. SLA theo Deal and Transaction Capability – Deal

* Next action.
* Proposal preparation.
* Proposal follow-up.
* Negotiation response.
* Hold confirmation.
* Booking preparation.
* Deposit follow-up.

---

# 104. SLA theo Contract and Cash Capability – Contract và Finance

* Contract handoff.
* Legal review.
* Signature follow-up.
* Payment allocation.
* Receipt issuance.
* Refund.
* Settlement.
* Reconciliation.

---

# 105. SLA theo Revenue and Commission Capability – Revenue và Commission

* Revenue calculation.
* Partner statement review.
* Revenue mismatch resolution.
* Commission calculation.
* Commission dispute.
* Payout approval.
* Clawback review.

---

# 106. Next Best Action – Mục tiêu

Next Best Action giúp user chọn hành động tiếp theo có giá trị cao nhất và phù hợp nhất trong context hiện tại.

NBA phải trả lời:

* Nên làm gì?
* Với resource nào?
* Vì sao?
* Mức độ ưu tiên?
* Hạn thực hiện?
* Dữ liệu nào làm căn cứ?
* Điều kiện nào còn thiếu?
* Có rủi ro gì?
* User có quyền không?
* Customer có thể được liên hệ không?
* Hành động đã từng được đề xuất hoặc thực hiện chưa?
* Kết quả kỳ vọng là gì?

---

# 107. Candidate Next Best Action types — pending validation

```text
CALL_CUSTOMER
RESPOND_TO_INBOUND
SEND_FOLLOW_UP
SCHEDULE_APPOINTMENT
CONFIRM_APPOINTMENT
UPDATE_REQUIREMENT
REQUEST_FINANCIAL_INFORMATION
RUN_MATCHING
REVIEW_MATCH_RESULTS
CREATE_SHORTLIST
SEND_PRODUCT_OPTIONS
PREPARE_PROPOSAL
FOLLOW_UP_PROPOSAL
REQUEST_AVAILABILITY_CHECK
REQUEST_HOLD
FOLLOW_UP_HOLD
PREPARE_BOOKING
FOLLOW_UP_DEPOSIT
COLLECT_DOCUMENT
PREPARE_CONTRACT
FOLLOW_UP_SIGNATURE
SEND_PAYMENT_REMINDER
VERIFY_PAYMENT
ISSUE_RECEIPT
PROCESS_REFUND
PROCESS_SETTLEMENT
REVIEW_REVENUE_MISMATCH
REVIEW_COMMISSION
RESOLVE_DISPUTE
ESCALATE
HANDOVER
CLOSE_OR_NURTURE
DO_NOT_CONTACT
NO_ACTION
OTHER
```

---

# 108. Nguồn dữ liệu NBA

NBA có thể dùng:

* Lead status.
* Last interaction.
* Contact attempts.
* Customer consent.
* Requirement completeness.
* Financial readiness.
* Matching results.
* Listing Availability.
* Shortlist.
* Proposal status.
* Appointment status.
* Deal stage.
* Hold expiry.
* Booking status.
* Deposit due.
* Contract status.
* Receivable due.
* Payment status.
* Revenue mismatch.
* Commission dispute.
* Task backlog.
* SLA.
* User workload.
* Business Calendar.
* Customer behavior history.

---

# 109. NBA Candidate Generation

Quy trình:

```text
Resource Context
→ Permission Gate
→ Consent Gate
→ Workflow Gate
→ Candidate Rules
→ Duplicate Suppression
→ Feasibility Check
→ Priority Scoring
→ Explanation
→ Recommendation
```

---

# 110. NBA Permission Gate

Loại bỏ hành động nếu user không có:

* Capability.
* Scope.
* Resource access.
* Field access.
* Approval authority.
* Project access.
* Legal Entity context.

---

# 111. NBA Consent Gate

Loại bỏ hoặc chuyển hành động nếu:

* Customer yêu cầu không liên hệ.
* Channel không được phép.
* Quiet hours.
* Frequency cap.
* Consent hết hạn.
* Contact restriction.
* Legal hold.

Ví dụ thay vì `CALL_CUSTOMER`, hệ thống có thể đề xuất:

> Review contact restriction with authorized manager.

---

# 112. NBA Workflow Gate

Không đề xuất:

* Gửi Proposal khi Proposal chưa approved.
* Hold Listing khi user không có Listing access.
* Issue Receipt khi Payment chưa verified.
* Payout commission khi batch chưa approved.
* Mark Contract effective khi thiếu signature.

---

# 113. Illustrative NBA priority model — không phải production formula

Có thể tính:

```text
NBA Priority
=
Business Impact
+ Time Urgency
+ Customer Intent
+ SLA Risk
+ Financial Risk
+ Inventory Risk
+ Legal Risk
+ Expected Value
− Effort
− Contact Fatigue
− Data Uncertainty
```

Điểm phải có version và explainability.

---

# 114. NBA Result

Mỗi recommendation gồm:

* Action type.
* Target resource.
* Suggested owner.
* Priority.
* Confidence.
* Due recommendation.
* Reasons.
* Expected outcome.
* Required permissions.
* Preconditions.
* Blocking conditions.
* Suggested template.
* Expiry.
* Rule/model version.

---

# 115. NBA Confidence

Confidence phản ánh:

* Độ đầy đủ dữ liệu.
* Độ mới dữ liệu.
* Độ rõ của rule.
* Độ tin cậy AI.
* Sự nhất quán lịch sử.

Confidence không phải xác suất chốt giao dịch.

---

# 116. NBA Explanation

Ví dụ:

> Nên gọi Customer trong hôm nay vì Proposal đã được xem cách đây 18 giờ, Customer chưa phản hồi, Deal đang ở giai đoạn Customer Review và SLA follow-up còn 3 giờ làm việc.

Hoặc:

> Chưa nên liên hệ Customer. Customer đã yêu cầu không nhận cuộc gọi và chỉ đồng ý nhận email về hồ sơ hợp đồng.

---

# 117. NBA Expiry

Recommendation hết hiệu lực khi:

* Context thay đổi.
* Task được tạo.
* User thực hiện hành động.
* Customer phản hồi.
* SLA breach.
* Listing status thay đổi.
* Proposal hết hạn.
* Rule/model version thay đổi.
* Expiry time đến.

---

# 118. NBA Acceptance

User có thể:

* Accept.
* Accept and create Task.
* Accept and execute.
* Snooze.
* Dismiss.
* Reject with reason.
* Mark not relevant.

Execution vẫn phải gọi API capability nguồn.

---

# 119. NBA Execution

Ví dụ `PREPARE_PROPOSAL`:

* NBA tạo suggestion.
* User accept.
* Activity and Engagement Capability tạo Task hoặc điều hướng Deal and Transaction Capability.
* Deal and Transaction Capability kiểm tra Proposal rules.
* Deal and Transaction Capability tạo Proposal Draft.
* Timeline ghi event.

Activity and Engagement Capability không tự tạo Proposal bằng cách ghi trực tiếp database Deal and Transaction Capability.

---

# 120. NBA Feedback

Lưu:

* Accepted.
* Dismissed.
* Rejected.
* Executed.
* Completed.
* Outcome.
* Time to action.
* User reason.
* Business result.

Feedback dùng cải thiện rule/model nhưng không được làm mất audit.

---

# 121. NBA Duplicate Suppression

Không đề xuất lặp khi:

* Task tương ứng đang open.
* Recommendation tương tự còn active.
* Action vừa được thực hiện.
* Customer vừa phản hồi.
* User đã dismiss trong cooldown.
* Frequency cap.

---

# 122. NBA Rule-based Engine

MVP nên ưu tiên rule-based:

* Proposal viewed nhưng chưa phản hồi.
* Hold sắp hết hạn.
* Deposit sắp đến hạn.
* Receivable quá hạn.
* Contract thiếu chữ ký.
* Matching stale.
* Lead chưa first contact.
* Customer no-show.
* Revenue mismatch.
* Commission dispute.

Rule phải version, simulation và audit.

---

# 123. AI-assisted NBA

AI có thể:

* Tóm tắt context.
* Xếp hạng các candidate đã qua gate.
* Viết explanation.
* Dự đoán khả năng phản hồi.
* Đề xuất thời điểm liên hệ.
* Phân loại objection.
* Gợi ý câu hỏi tiếp theo.

AI không được:

* Vượt Permission Gate.
* Vượt Consent Gate.
* Tự gửi message.
* Tự gọi Customer.
* Tự xác nhận tiền.
* Tự duyệt Contract.
* Tự thay đổi Commission.
* Tạo nội dung gây hiểu nhầm pháp lý/tài chính.
* Tự suy luận thuộc tính nhạy cảm không được phép.

---

# 124. AI Summary

AI có thể tạo:

* Lead summary.
* Customer interaction summary.
* Deal activity summary.
* Contract activity summary.
* Revenue reconciliation summary.
* Commission dispute summary.

Summary phải:

* Có nguồn.
* Có generated time.
* Có model version.
* Có confidence.
* Phân biệt fact và inference.
* Không thay Timeline gốc.

---

# 125. Automation

Activity and Engagement Capability có thể tự động:

* Tạo Task từ event.
* Gửi reminder.
* Escalate SLA.
* Tạo NBA.
* Sync Calendar.
* Ghi Call webhook.
* Ghi message delivery.
* Tạo Timeline Event.

Không được tự động thực hiện giao dịch rủi ro cao nếu chưa có workflow/approval.

---

# 126. Automation Run

Mỗi lần automation lưu:

* Rule.
* Version.
* Trigger.
* Resource.
* Input snapshot.
* Action.
* Result.
* Error.
* Retry.
* Idempotency key.
* Started/completed time.

---

# 127. Automation Failure

Khi thất bại:

* Không tạo duplicate khi retry.
* Ghi error.
* Tạo alert nếu critical.
* Có dead-letter queue.
* Cho phép replay có quyền.
* Giữ correlation ID.

---

# 128. Delegation

## 128.1. Delegation tạm thời

Người được ủy quyền có thể:

* Xử lý Task.
* Tham gia Appointment.
* Follow-up Customer.
* Review queue.

Không mặc định được:

* Duyệt vượt thẩm quyền.
* Xem field nhạy cảm ngoài delegation scope.
* Nhận attribution/commission.

## 128.2. Delegation Snapshot

Task/Approval phải lưu delegation được dùng.

---

# 129. Handover

Khi user:

* Nghỉ phép.
* Chuyển team.
* Nghỉ việc.
* Thay vai trò.
* Bị khóa tài khoản.

Handover phải xử lý:

* Open Task.
* Overdue Task.
* Future Appointment.
* Customer communication.
* SLA.
* Queue ownership.
* Draft Interaction.
* Pending approval.
* NBA recommendations.

---

# 130. Handover Policy

Phân loại:

```text
TEMPORARY_COVERAGE
PERMANENT_TRANSFER
TEAM_TRANSFER
OFFBOARDING
EMERGENCY_REASSIGNMENT
```

Handover không tự:

* Đổi Customer identity.
* Đổi Lead attribution.
* Đổi Deal commission.
* Đổi Contract Party.
* Xóa Timeline.

---

# 131. Multi-Legal Entity

Mỗi Activity có thể gắn:

* Enterprise.
* Legal Entity context.
* Branch.
* Department.
* Team.
* Project.

## 131.1. Cross-entity Activity

Chỉ được tạo khi:

* User có cross-entity permission.
* Resource relationship hợp lệ.
* Visibility rõ.
* Data field policy phù hợp.

## 131.2. Customer dùng chung Enterprise

Customer Timeline có thể tổng hợp cross-entity, nhưng user chỉ thấy event thuộc scope và field access của mình.

---

# 132. Scope

Các scope chuẩn:

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

## 132.1. `mine`

Activity do user sở hữu hoặc được giao chính.

## 132.2. `assigned`

Activity user là assignee, reviewer hoặc participant hợp lệ.

## 132.3. `team/department`

Dựa trên membership effective date và hierarchy.

## 132.4. Timeline scope

Timeline phải intersect:

```text
User Capability
∩ Resource Access
∩ Event Visibility
∩ Field Permission
∩ Legal Entity Scope
```

---

# 133. Field Masking

Các field nhạy cảm:

* Phone đầy đủ.
* Email đầy đủ.
* Call recording.
* Transcript.
* Identity document.
* Bank information.
* Contract detail.
* Revenue amount.
* Commission amount.
* Internal note.
* Owner address.
* Exact private Listing address.

Masking phải thực hiện tại backend.

---

# 134. Segregation of Duties

Activity and Engagement Capability phải tôn trọng SoD của capability nguồn.

Ví dụ:

* Task “Review Receipt” không cho maker tự complete với outcome Approved nếu user không có approval capability.
* Appointment với Customer không cấp quyền sửa Contract.
* NBA không đề xuất tự duyệt Commission của chính mình.
* Delegated user không vượt approval limit.

---

# 135. Notification

## 135.1. Task

* Task assigned.
* Task reassigned.
* Task due soon.
* Task overdue.
* Dependency completed.
* Task blocked.
* Task reopened.
* Task escalation.

## 135.2. Appointment

* Invitation.
* Confirmation.
* Reminder.
* Reschedule.
* Cancellation.
* No-show.
* Resource conflict.

## 135.3. Interaction

* Inbound Customer message.
* Failed delivery.
* Do-not-contact request.
* Complaint.
* High-priority response.

## 135.4. SLA

* Warning.
* At risk.
* Breach.
* Escalation.
* Extension result.

## 135.5. NBA

* New critical recommendation.
* Recommendation expiring.
* Recommendation dismissed repeatedly.
* Recommendation outcome.

Notification phải chống trùng và tuân thủ quiet hours cho user.

---

# 136. Candidate user experience — My Work

Hiển thị:

* Task hôm nay.
* Overdue.
* Critical.
* Waiting.
* Upcoming appointments.
* Missed calls.
* Unread inbound interactions.
* SLA at risk.
* Next Best Actions.
* Recently completed.
* Delegated work.
* Queue work.

---

# 137. Task List

Bộ lọc:

* Status.
* Type.
* Priority.
* Assignee.
* Owner.
* Team.
* Context.
* Due date.
* SLA.
* Source.
* Customer.
* Project.
* Deal.
* Contract.
* Waiting reason.
* Recurring.
* Delegated.

---

# 138. Task Detail

Các tab:

1. Overview.
2. Context.
3. Checklist.
4. Dependencies.
5. Participants.
6. SLA.
7. Interactions.
8. Evidence.
9. History.
10. Audit.

---

# 139. Calendar Workspace

Chế độ:

* Day.
* Week.
* Month.
* Agenda.
* Team Calendar.
* Project visit calendar.
* Resource calendar.

Hiển thị:

* Appointment.
* Task deadline.
* Contract signing.
* Payment milestone.
* Hold expiry.
* SLA deadline.

Các item không phải Appointment phải hiển thị khác loại và không trở thành Calendar event ngoài nếu chưa có policy.

---

# 140. Appointment Workspace

Các tab:

* Details.
* Participants.
* Resources.
* Confirmation.
* Directions/location.
* Attendance.
* Outcome.
* Notes.
* Follow-up.
* Sync history.
* Audit.

---

# 141. Call Center Workspace

* Click-to-call.
* Incoming call queue.
* Missed calls.
* Call disposition.
* Recording.
* Transcript.
* Follow-up Task.
* Customer context.
* Consent warning.
* Call statistics.

---

# 142. Interaction Inbox

Có thể hợp nhất:

* Email.
* SMS.
* Zalo.
* Chat.
* Social.
* Portal message.

Chức năng:

* Assign.
* Claim.
* Reply.
* Link Customer.
* Link Lead.
* Merge thread.
* Mark spam.
* Escalate.
* Create Task.
* Update consent request.

---

# 143. Unified Timeline UI

Hiển thị:

* Event icon/type.
* Time.
* Actor.
* Context.
* Summary.
* Related resource.
* Visibility.
* Attachments.
* Correction.
* Audit indicator.

Có chế độ:

* All.
* Customer communication.
* Internal activity.
* Transaction.
* Finance.
* Legal.
* System.

---

# 144. SLA Control Center

* SLA definitions reference.
* Running instances.
* Warning.
* Breached.
* Paused.
* Extension requests.
* Escalations.
* Root cause.
* Team performance.
* Calendar impact.

---

# 145. Next Best Action Center

* Recommendations by user.
* Recommendations by Customer.
* Critical actions.
* Expiring recommendations.
* Accepted.
* Dismissed.
* Outcome.
* Explanation.
* Model/rule version.
* Bias/anomaly monitoring.

---

# 146. Dashboard cho Sale

* Task hôm nay.
* Overdue.
* First contact due.
* Upcoming appointments.
* Customer no-show.
* Unanswered inbound.
* Proposal follow-up.
* Hold expiry.
* Deposit reminder.
* Contract signature follow-up.
* NBA priority.
* SLA performance.
* Activity-to-conversion.

---

# 147. Dashboard cho Team Lead

* Team workload.
* Task distribution.
* Overdue by user.
* SLA breach.
* Lead response time.
* Appointment conversion.
* Call connect rate.
* Follow-up compliance.
* Interaction backlog.
* No-show rate.
* NBA execution rate.
* Handover backlog.
* Coaching opportunities.

---

# 148. Dashboard cho Department Head

* Department productivity.
* SLA by process.
* Workload imbalance.
* Queue aging.
* Cross-team dependency.
* Customer contact frequency.
* Deal inactivity.
* Contract review delays.
* Finance task delays.
* Escalation count.

---

# 149. Dashboard cho Director

* Enterprise activity volume.
* SLA compliance.
* First response.
* Sales cycle activity.
* Appointment-to-booking conversion.
* Call-to-appointment conversion.
* Proposal follow-up effectiveness.
* Task completion.
* Customer contact fatigue.
* Critical backlog.
* Process bottleneck.
* NBA business impact.
* Cross-Legal Entity workload.

---

# 150. Candidate analytical questions — không phải certified Metrics

> Exact grain, formulas, snapshots, certification và access thuộc Analytics Context và Metric Registry.

## Task

* Task master.
* Task by type.
* Task by status.
* Task by priority.
* Task aging.
* Task overdue.
* Task completion time.
* Task reassignment.
* Task workload.
* Task recurrence.
* Task dependency delay.
* Task outcome.
* Task by capability context.

## Appointment

* Appointment count.
* Confirmation rate.
* Attendance.
* No-show.
* Reschedule.
* Cancellation.
* Site visit.
* Appointment outcome.
* Appointment-to-shortlist.
* Appointment-to-booking.
* Resource utilization.

## Call

* Calls attempted.
* Connected calls.
* Call duration.
* No answer.
* Call disposition.
* Call outcome.
* Calls by user/team.
* First call response.
* Call-to-appointment.
* Recording coverage theo policy.
* Missing disposition.

## Interaction

* Interactions by channel.
* Inbound/outbound.
* Delivery failure.
* Response time.
* Thread aging.
* Do-not-contact.
* Complaint.
* Contact frequency.
* Unread backlog.

## Timeline

* Event volume.
* Activity gaps.
* Resource inactivity.
* Customer journey.
* Deal activity.
* Contract activity.

## SLA

* Compliance rate.
* Warning.
* Breach.
* Average resolution.
* Pause duration.
* Extension.
* Root cause.
* Escalation.
* SLA by capability.
* SLA by team/user.

## NBA

* Recommendations generated.
* Acceptance.
* Dismissal.
* Execution.
* Completion.
* Time to action.
* Outcome.
* Conversion impact.
* Rule/model performance.
* Recommendation duplication.
* Permission/consent rejection.

Operational views phải drill-down đúng scope. Certified Metrics thuộc Analytics Context.

---

# 151. Candidate data model — không phải physical schema canonical

> Exact tables, columns, constraints, indexes và references chỉ có hiệu lực qua Activity Context DB Specification và Alembic historical imports.

## 151.1. Activity Reference

### `activity_context_links`

* `id`
* `activity_type`
* `activity_id`
* `context_type`
* `context_id`
* `relationship_type`
* `is_primary`
* `created_at`

### `activity_participants`

* `id`
* `activity_type`
* `activity_id`
* `participant_type`
* `participant_id`
* `participant_role`
* `status`
* `created_at`

---

## 151.2. Task

### `tasks`

* `id`
* `task_code`
* `enterprise_id`
* `legal_entity_id`
* `task_type`
* `title`
* `description`
* `priority`
* `status`
* `health_status`
* `owner_user_id`
* `primary_assignee_user_id`
* `assignment_queue_id`
* `start_at`
* `due_at`
* `timezone`
* `completion_requirement_code`
* `outcome_code`
* `outcome_notes`
* `source_type`
* `source_id`
* `task_template_version_id`
* `recurrence_series_id`
* `sla_instance_id`
* `visibility_policy_id`
* `completed_at`
* `cancelled_at`
* `created_by`
* `created_at`
* `updated_at`
* `version`

### `task_assignments`

* `id`
* `task_id`
* `user_id`
* `assignment_role`
* `effective_from`
* `effective_to`
* `assignment_source`
* `assignment_rule_version`
* `status`
* `created_at`

### `task_status_history`

* `id`
* `task_id`
* `from_status`
* `to_status`
* `reason_code`
* `reason`
* `changed_by`
* `created_at`

### `task_checklist_items`

* `id`
* `task_id`
* `item_code`
* `title`
* `required`
* `assigned_user_id`
* `status`
* `due_at`
* `evidence_reference`
* `completed_by`
* `completed_at`
* `created_at`

### `task_dependencies`

* `id`
* `task_id`
* `depends_on_task_id`
* `dependency_type`
* `required_status`
* `status`
* `created_at`

### `task_watchers`

* `id`
* `task_id`
* `user_id`
* `watcher_role`
* `notification_policy`
* `created_at`

### `task_completion_evidence`

* `id`
* `task_id`
* `evidence_type`
* `source_type`
* `source_id`
* `document_id`
* `description`
* `created_by`
* `created_at`

### `task_reassignments`

* `id`
* `task_id`
* `from_user_id`
* `to_user_id`
* `reason_code`
* `reason`
* `sla_impact_json`
* `handover_note`
* `approved_by`
* `effective_at`
* `created_at`

---

## 151.3. Task Template và Recurrence

### `task_templates`

* `id`
* `template_code`
* `name`
* `task_type`
* `scope_type`
* `scope_id`
* `status`
* `current_version`
* `created_at`

### `task_template_versions`

* `id`
* `task_template_id`
* `version`
* `title_template`
* `description_template`
* `priority`
* `assignment_rule_json`
* `due_rule_json`
* `checklist_json`
* `completion_requirements_json`
* `reminder_policy_json`
* `sla_policy_id`
* `visibility_policy_json`
* `effective_from`
* `effective_to`
* `status`
* `created_by`
* `reviewed_by`
* `approved_by`
* `created_at`

### `task_recurrence_series`

* `id`
* `series_code`
* `task_template_version_id`
* `recurrence_rule`
* `timezone`
* `start_at`
* `end_at`
* `maximum_occurrences`
* `incomplete_instance_policy`
* `status`
* `created_by`
* `created_at`

### `task_reminders`

* `id`
* `task_id`
* `reminder_type`
* `scheduled_at`
* `channel`
* `recipient_user_id`
* `status`
* `sent_at`
* `deduplication_key`
* `created_at`

---

## 151.4. Appointment

### `appointments`

* `id`
* `appointment_code`
* `enterprise_id`
* `legal_entity_id`
* `appointment_type`
* `subject`
* `description`
* `organizer_user_id`
* `owner_user_id`
* `start_at`
* `end_at`
* `timezone`
* `location_type`
* `location_reference`
* `meeting_url`
* `status`
* `confirmation_status`
* `attendance_status`
* `outcome_code`
* `outcome_notes`
* `external_calendar_provider`
* `external_calendar_event_id`
* `sync_status`
* `visibility_policy_id`
* `created_by`
* `created_at`
* `updated_at`
* `version`

### `appointment_participants`

* `id`
* `appointment_id`
* `participant_type`
* `participant_id`
* `participant_role`
* `required`
* `invitation_status`
* `confirmation_status`
* `attendance_status`
* `contact_reference`
* `created_at`

### `appointment_resources`

* `id`
* `appointment_id`
* `resource_type`
* `resource_id`
* `required`
* `booking_status`
* `confirmed_at`
* `released_at`
* `created_at`

### `appointment_reschedules`

* `id`
* `appointment_id`
* `old_start_at`
* `old_end_at`
* `new_start_at`
* `new_end_at`
* `requested_by_type`
* `requested_by_id`
* `reason`
* `status`
* `created_at`

### `appointment_confirmations`

* `id`
* `appointment_id`
* `participant_type`
* `participant_id`
* `confirmation_type`
* `channel`
* `status`
* `confirmed_at`
* `created_at`

### `appointment_attendance_records`

* `id`
* `appointment_id`
* `participant_type`
* `participant_id`
* `attendance_status`
* `check_in_at`
* `check_out_at`
* `evidence_reference`
* `recorded_by`
* `created_at`

### `appointment_reminders`

* `id`
* `appointment_id`
* `participant_type`
* `participant_id`
* `channel`
* `scheduled_at`
* `status`
* `sent_at`
* `delivery_status`
* `created_at`

---

## 151.5. Site Visit

### `site_visits`

* `id`
* `appointment_id`
* `project_id`
* `listing_id`
* `visit_purpose`
* `access_authorization_reference`
* `transport_reference`
* `check_in_reference`
* `check_out_reference`
* `visit_result`
* `created_at`

### `site_visit_products`

* `id`
* `site_visit_id`
* `listing_id`
* `viewed`
* `customer_feedback_code`
* `notes`
* `created_at`

---

## 151.6. Call

### `call_logs`

* `id`
* `call_code`
* `enterprise_id`
* `legal_entity_id`
* `direction`
* `status`
* `caller_type`
* `caller_id`
* `callee_type`
* `callee_id`
* `phone_identity_id`
* `masked_phone`
* `started_at`
* `answered_at`
* `ended_at`
* `duration_seconds`
* `provider_code`
* `external_call_id`
* `disposition_code`
* `outcome_code`
* `consent_status`
* `recording_available`
* `transcript_available`
* `source_type`
* `created_by`
* `created_at`

### `call_recordings`

* `id`
* `call_log_id`
* `provider_recording_id`
* `recording_document_id`
* `duration_seconds`
* `encryption_reference`
* `consent_basis`
* `access_policy_id`
* `retention_until`
* `status`
* `created_at`

### `call_transcripts`

* `id`
* `call_log_id`
* `source_type`
* `language_code`
* `transcript_document_id`
* `summary`
* `confidence_score`
* `model_version`
* `sensitive_data_flags_json`
* `review_status`
* `reviewed_by`
* `created_at`

### `call_extraction_suggestions`

* `id`
* `call_transcript_id`
* `suggestion_type`
* `target_resource_type`
* `target_resource_id`
* `suggested_value_json`
* `confidence_score`
* `status`
* `reviewed_by`
* `reviewed_at`
* `created_at`

---

## 151.7. Interaction

### `interactions`

* `id`
* `interaction_code`
* `enterprise_id`
* `legal_entity_id`
* `channel`
* `direction`
* `interaction_type`
* `thread_id`
* `subject`
* `summary`
* `content_storage_type`
* `content_reference`
* `content_hash`
* `occurred_at`
* `recorded_at`
* `delivery_status`
* `read_status`
* `consent_check_result`
* `sensitivity_level`
* `visibility_policy_id`
* `external_provider`
* `external_message_id`
* `source_type`
* `created_by`
* `created_at`

### `interaction_participants`

* `id`
* `interaction_id`
* `participant_type`
* `participant_id`
* `participant_role`
* `address_reference`
* `masked_address`
* `identity_confidence`
* `delivery_status`
* `created_at`

### `interaction_threads`

* `id`
* `thread_code`
* `channel`
* `external_thread_id`
* `primary_context_type`
* `primary_context_id`
* `subject`
* `owner_user_id`
* `status`
* `last_interaction_at`
* `visibility_policy_id`
* `created_at`
* `updated_at`

### `interaction_attachments`

* `id`
* `interaction_id`
* `filename`
* `mime_type`
* `size_bytes`
* `document_version_id`
* `document_id`
* `file_hash`
* `malware_scan_status`
* `access_policy_id`
* `retention_until`
* `created_at`

### `interaction_delivery_events`

* `id`
* `interaction_id`
* `event_type`
* `provider_event_id`
* `occurred_at`
* `payload_reference`
* `created_at`

---

## 151.8. Timeline

### `timeline_events`

* `id`
* `timeline_event_code`
* `event_type`
* `event_schema_version`
* `source_context`
* `source_resource_type`
* `source_resource_id`
* `primary_context_type`
* `primary_context_id`
* `actor_type`
* `actor_id`
* `occurred_at`
* `recorded_at`
* `summary_template_code`
* `summary_data_json`
* `details_reference`
* `sensitivity_level`
* `visibility_policy_id`
* `correlation_id`
* `causation_id`
* `status`
* `created_at`

### `timeline_event_contexts`

* `id`
* `timeline_event_id`
* `context_type`
* `context_id`
* `relationship_type`
* `created_at`

### `timeline_event_corrections`

* `id`
* `original_timeline_event_id`
* `correction_timeline_event_id`
* `correction_type`
* `reason`
* `approved_by`
* `created_at`

---

## 151.9. SLA

### `sla_instances`

* `id`
* `sla_instance_code`
* `sla_definition_id`
* `sla_definition_version`
* `resource_type`
* `resource_id`
* `target_type`
* `responsible_user_id`
* `responsible_team_id`
* `start_event_type`
* `start_event_id`
* `started_at`
* `due_at`
* `business_calendar_id`
* `business_calendar_version`
* `warning_at`
* `breached_at`
* `completed_at`
* `total_pause_seconds`
* `status`
* `created_at`
* `updated_at`
* `version`

### `sla_clock_segments`

* `id`
* `sla_instance_id`
* `segment_type`
* `started_at`
* `ended_at`
* `duration_seconds`
* `reason_code`
* `source_type`
* `source_id`
* `created_at`

### `sla_pause_requests`

* `id`
* `sla_instance_id`
* `reason_code`
* `reason`
* `evidence_reference`
* `requested_by`
* `status`
* `approved_by`
* `started_at`
* `ended_at`
* `created_at`

### `sla_extension_requests`

* `id`
* `sla_instance_id`
* `requested_extension_seconds`
* `reason`
* `impact_json`
* `requested_by`
* `status`
* `approved_by`
* `new_due_at`
* `created_at`

### `sla_escalations`

* `id`
* `sla_instance_id`
* `escalation_level`
* `recipient_type`
* `recipient_id`
* `reason`
* `triggered_at`
* `acknowledged_at`
* `status`
* `created_at`

### `sla_breaches`

* `id`
* `sla_instance_id`
* `breach_type`
* `breach_duration_seconds`
* `responsibility_type`
* `root_cause_code`
* `resolution_reference`
* `created_at`

---

## 151.10. Next Best Action

### `next_best_action_runs`

* `id`
* `run_code`
* `enterprise_id`
* `legal_entity_id`
* `target_user_id`
* `target_resource_type`
* `target_resource_id`
* `trigger_type`
* `rule_set_version`
* `model_version`
* `input_snapshot_json`
* `candidate_count`
* `status`
* `started_at`
* `completed_at`
* `created_at`

### `next_best_action_candidates`

* `id`
* `next_best_action_run_id`
* `action_type`
* `target_resource_type`
* `target_resource_id`
* `suggested_owner_user_id`
* `business_impact_score`
* `urgency_score`
* `effort_score`
* `risk_score`
* `contact_fatigue_penalty`
* `priority_score`
* `confidence_score`
* `preconditions_json`
* `blocking_conditions_json`
* `status`
* `created_at`

### `next_best_actions`

* `id`
* `nba_code`
* `next_best_action_run_id`
* `candidate_id`
* `action_type`
* `target_user_id`
* `target_resource_type`
* `target_resource_id`
* `priority`
* `confidence_score`
* `recommended_due_at`
* `reason_summary`
* `explanation_json`
* `suggested_template_id`
* `expires_at`
* `status`
* `accepted_at`
* `dismissed_at`
* `executed_at`
* `completed_at`
* `created_at`

### `next_best_action_feedback`

* `id`
* `next_best_action_id`
* `feedback_type`
* `reason_code`
* `reason`
* `execution_reference_type`
* `execution_reference_id`
* `business_outcome_code`
* `submitted_by`
* `created_at`

---

## 151.11. Automation

### `activity_automation_runs`

* `id`
* `automation_run_code`
* `automation_rule_id`
* `automation_rule_version`
* `trigger_type`
* `trigger_id`
* `resource_type`
* `resource_id`
* `input_snapshot_json`
* `action_type`
* `action_result_json`
* `idempotency_key`
* `status`
* `retry_count`
* `error_code`
* `error_message`
* `started_at`
* `completed_at`
* `created_at`

---

# 152. Candidate application operations — không phải OpenAPI canonical

> Exact paths, methods, payloads, errors, idempotency và authorization metadata thuộc OpenAPI.

## Task

```text
GET    /tasks
POST   /tasks
GET    /tasks/{id}
PATCH  /tasks/{id}
POST   /tasks/{id}/transition
POST   /tasks/{id}/assign
POST   /tasks/{id}/reassign
POST   /tasks/{id}/claim
POST   /tasks/{id}/start
POST   /tasks/{id}/complete
POST   /tasks/{id}/complete-with-exception
POST   /tasks/{id}/reopen
POST   /tasks/{id}/cancel
POST   /tasks/{id}/defer
GET    /tasks/{id}/history
GET    /tasks/{id}/access-explanation
```

## Checklist và Dependency

```text
GET    /tasks/{id}/checklist
POST   /tasks/{id}/checklist-items
PATCH  /task-checklist-items/{id}
POST   /task-checklist-items/{id}/complete

GET    /tasks/{id}/dependencies
POST   /tasks/{id}/dependencies
DELETE /task-dependencies/{id}
POST   /tasks/{id}/validate-readiness
```

## Task Template và Recurrence

```text
GET    /task-templates
POST   /task-templates
GET    /task-templates/{id}
POST   /task-templates/{id}/versions
POST   /task-template-versions/{id}/validate
POST   /task-template-versions/{id}/approve
POST   /task-template-versions/{id}/activate

GET    /task-recurrence-series
POST   /task-recurrence-series
PATCH  /task-recurrence-series/{id}
POST   /task-recurrence-series/{id}/pause
POST   /task-recurrence-series/{id}/resume
POST   /task-recurrence-series/{id}/cancel
```

## Appointment

```text
GET    /appointments
POST   /appointments
GET    /appointments/{id}
PATCH  /appointments/{id}
POST   /appointments/{id}/propose
POST   /appointments/{id}/confirm
POST   /appointments/{id}/reschedule
POST   /appointments/{id}/cancel
POST   /appointments/{id}/start
POST   /appointments/{id}/complete
POST   /appointments/{id}/record-attendance
POST   /appointments/{id}/record-outcome
GET    /appointments/{id}/history
```

## Calendar và Resource

```text
GET    /calendar/availability
GET    /appointment-resources/availability
POST   /appointments/{id}/resources
POST   /appointments/{id}/send-invitations
POST   /appointments/{id}/sync-calendar
POST   /appointments/{id}/resolve-sync-conflict
```

## Call

```text
GET    /call-logs
POST   /calls/initiate
GET    /call-logs/{id}
POST   /call-logs/{id}/disposition
POST   /call-logs/{id}/outcome
POST   /call-logs/{id}/link-context
GET    /call-logs/{id}/recording
GET    /call-logs/{id}/transcript
POST   /call-transcripts/{id}/review
POST   /call-extraction-suggestions/{id}/accept
POST   /call-extraction-suggestions/{id}/reject
```

## Interaction

```text
GET    /interactions
POST   /interactions
GET    /interactions/{id}
POST   /interactions/{id}/send
POST   /interactions/{id}/retry
POST   /interactions/{id}/link-context
POST   /interactions/{id}/mark-read
POST   /interactions/{id}/create-task

GET    /interaction-threads
GET    /interaction-threads/{id}
POST   /interaction-threads/{id}/assign
POST   /interaction-threads/{id}/close
POST   /interaction-threads/{id}/merge
```

## Timeline

```text
GET    /timeline
GET    /resources/{type}/{id}/timeline
GET    /timeline-events/{id}
POST   /timeline-events/{id}/corrections
GET    /timeline-events/{id}/access-explanation
```

Timeline Event chủ yếu được tạo nội bộ từ domain event, không cho client tùy ý tạo mọi event type.

## SLA

```text
GET    /sla-instances
GET    /sla-instances/{id}
POST   /sla-instances/{id}/start
POST   /sla-instances/{id}/pause-requests
POST   /sla-pause-requests/{id}/approve
POST   /sla-instances/{id}/resume
POST   /sla-instances/{id}/extension-requests
POST   /sla-extension-requests/{id}/approve
POST   /sla-instances/{id}/complete
POST   /sla-instances/{id}/invalidate
GET    /sla-instances/{id}/clock
GET    /sla-instances/{id}/history
```

## Next Best Action

```text
GET    /next-best-actions
POST   /next-best-action-runs
GET    /next-best-actions/{id}
POST   /next-best-actions/{id}/accept
POST   /next-best-actions/{id}/accept-and-create-task
POST   /next-best-actions/{id}/execute
POST   /next-best-actions/{id}/snooze
POST   /next-best-actions/{id}/dismiss
POST   /next-best-actions/{id}/feedback
POST   /next-best-actions/{id}/refresh
GET    /next-best-actions/{id}/explanation
```

Backend phải tự enforce:

* Authenticated user.
* User status.
* Activity capability.
* Resource capability.
* Resource scope.
* Legal Entity.
* Project access.
* Customer context.
* Consent.
* Contact restriction.
* Quiet hours.
* Frequency cap.
* Field masking.
* Workflow.
* Approval.
* Business Calendar.
* SLA policy.
* Idempotency.
* Optimistic locking.
* Audit.

---

# 153. Candidate permission vocabulary — không phải Permission Registry canonical

> Exact permissions, scopes, role mappings, SoD và masking thuộc security registries/matrices.

## Task

```text
task.view
task.create
task.update
task.assign
task.reassign
task.claim
task.start
task.complete
task.complete_exception
task.reopen
task.cancel
task.defer
task.bulk_assign
task.bulk_update
task.view_audit
```

## Task Template

```text
task_template.view
task_template.create
task_template.update_draft
task_template.create_version
task_template.validate
task_template.review
task_template.approve
task_template.activate
```

## Appointment

```text
appointment.view
appointment.create
appointment.update
appointment.propose
appointment.confirm
appointment.reschedule
appointment.cancel
appointment.record_attendance
appointment.record_outcome
appointment.manage_resource
appointment.view_team_calendar
appointment.view_audit
```

## Call

```text
call.view
call.initiate
call.log_manual
call.record_disposition
call.record_outcome
call.view_recording
call.download_recording
call.view_transcript
call.review_transcript
call.apply_extraction
call.view_audit
```

## Interaction

```text
interaction.view
interaction.create
interaction.send
interaction.reply
interaction.retry
interaction.assign
interaction.link_context
interaction.view_content
interaction.view_sensitive
interaction.view_attachment
interaction.export
```

## Timeline

```text
timeline.view
timeline.view_internal
timeline.view_sensitive
timeline.view_finance
timeline.view_legal
timeline.create_correction
timeline.view_audit
```

## SLA

```text
sla.view
sla.view_team
sla.pause_request
sla.pause_approve
sla.extend_request
sla.extend_approve
sla.invalidate
sla.resolve_breach
sla.view_audit
```

## Next Best Action

```text
nba.view
nba.generate
nba.view_explanation
nba.accept
nba.execute
nba.snooze
nba.dismiss
nba.submit_feedback
nba.view_team
nba.manage_rules
nba.simulate_rules
nba.view_model_monitoring
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

# 154. Candidate role baseline — không phải Role/Permission Registry canonical

## 154.1. Sale

Được:

* Quản lý Task của mình.
* Xem lịch của mình.
* Tạo Appointment trong Customer scope.
* Gọi và ghi Interaction với Customer được phép.
* Xem Timeline Customer/Deal theo scope.
* Xem SLA liên quan.
* Nhận và xử lý NBA.

Không được:

* Xem recording của sale khác.
* Xem Timeline Finance nhạy cảm.
* Bulk export Interaction.
* Tự pause SLA không có reason.
* Gửi Customer trái consent.
* Xem Customer ngoài scope.

## 154.2. Team Lead

Được:

* Xem workload team.
* Reassign Task team.
* Xem Team Calendar.
* Review SLA.
* Approve extension theo authority.
* Xem NBA team.
* Coaching từ activity data.

Không mặc định được xem nội dung tài chính/pháp lý nhạy cảm.

## 154.3. Department Head

Được:

* Scope department.
* Xử lý escalation.
* Review bottleneck.
* Cross-team assignment theo quyền.

## 154.4. Legal

Được:

* Task và Appointment pháp lý.
* Contract Timeline theo quyền.
* Legal Interaction.
* Review sensitive legal evidence.

## 154.5. Accounting/Finance

Được:

* Payment/Receipt/Settlement Task.
* Finance Interaction.
* Finance SLA.
* Timeline tài chính theo permission.

Không tự xem Call Recording Customer nếu không có context.

## 154.6. Revenue/Commission Operations

Được:

* Reconciliation Task.
* Partner Interaction.
* Commission dispute Task.
* SLA liên quan.

## 154.7. Director

Được:

* Dashboard toàn scope.
* SLA escalation.
* Export có audit.
* Xem Timeline nhạy cảm khi có capability.

---

# 155. Candidate business facts — không phải Event contracts canonical

> Exact Event names, versions, payloads, channels và consumers thuộc JSON Schema, AsyncAPI và Event Registry.

Activity and Engagement Capability phát:

```text
task.created
task.assigned
task.reassigned
task.ready
task.started
task.blocked
task.waiting
task.completed
task.completed_with_exception
task.reopened
task.cancelled
task.overdue

appointment.created
appointment.proposed
appointment.confirmed
appointment.rescheduled
appointment.cancelled
appointment.started
appointment.completed
appointment.no_show
appointment.outcome_recorded

call.initiated
call.connected
call.completed
call.missed
call.disposition_recorded
call.transcript_available
call.extraction_suggested

interaction.created
interaction.queued
interaction.sent
interaction.delivered
interaction.read
interaction.failed
interaction.received
interaction.do_not_contact_requested
interaction.complaint_received

timeline.event_created
timeline.event_corrected

sla.started
sla.warning
sla.at_risk
sla.paused
sla.resumed
sla.breached
sla.escalated
sla.completed_within
sla.completed_after
sla.extended
sla.invalidated

nba.generated
nba.accepted
nba.task_created
nba.executed
nba.snoozed
nba.dismissed
nba.completed
nba.feedback_recorded

activity_automation.completed
activity_automation.failed
```

Consumer phải idempotent.

---

# 156. Candidate Platform configuration references

```text
task.type_dictionary
task.default_workflow
task.assignment_policy
task.queue_policy
task.priority_policy
task.due_rule_policy
task.dependency_policy
task.recurrence_policy
task.completion_policy
task.reopen_policy
task.bulk_action_policy
task.reminder_policy
task.template_resolution_policy

appointment.workflow
appointment.type_dictionary
appointment.scheduling_policy
appointment.conflict_policy
appointment.resource_policy
appointment.confirmation_policy
appointment.reminder_policy
appointment.no_show_policy
appointment.calendar_sync_policy

call.provider_policy
call.disposition_policy
call.recording_policy
call.transcript_policy
call.retention_policy
call.consent_policy

interaction.channel_policy
interaction.delivery_policy
interaction.thread_policy
interaction.content_storage_policy
interaction.attachment_policy
interaction.quiet_hours_policy
interaction.frequency_cap_policy
interaction.do_not_contact_policy

timeline.event_policy
timeline.visibility_policy
timeline.summary_template_policy
timeline.retention_policy
timeline.correction_policy

sla.definition_resolution_policy
sla.clock_policy
sla.pause_policy
sla.extension_policy
sla.warning_policy
sla.escalation_policy
sla.breach_policy
sla.waiver_policy

nba.rule_set
nba.priority_policy
nba.confidence_policy
nba.permission_gate_policy
nba.consent_gate_policy
nba.duplicate_suppression_policy
nba.expiry_policy
nba.feedback_policy
nba.ai_assistance_policy
nba.model_monitoring_policy

activity.notification_policy
activity.field_access_policy
activity.export_approval_policy
activity.retention_policy
```

Mỗi configuration definition phải công bố schema, allowed scopes, resolution strategy, owner, version, effective period, approval và Audit requirements khi phù hợp.

---

# 157. System invariant

Các quy tắc sau không được cấu hình tắt:

1. Task không đồng nghĩa Interaction thực tế.
2. Appointment không đồng nghĩa cuộc gặp đã diễn ra.
3. Task hoàn thành không tự thay capability nguồn.
4. Timeline Event không phải nguồn dữ liệu nghiệp vụ chính.
5. Timeline lịch sử không được sửa trực tiếp.
6. SLA phải có Definition Version.
7. SLA phải có Business Calendar Version khi dùng business time.
8. SLA breach không tự approve/reject/cancel nghiệp vụ.
9. NBA không được vượt permission.
10. NBA không được vượt consent.
11. NBA không được tự liên hệ Customer nếu chưa có automation được duyệt.
12. NBA không được tự xác nhận tiền.
13. NBA không được tự duyệt Contract, Revenue hoặc Commission.
14. Call Recording phải có consent/policy hợp lệ.
15. User không được xem recording ngoài scope.
16. Do-not-contact phải chặn outbound phù hợp.
17. Interaction webhook phải idempotent.
18. Task reassignment không tự thay attribution.
19. Handover không tự thay commission.
20. Customer merge không làm mất Timeline.
21. Event nhạy cảm phải field-mask.
22. Backend phải enforce resource scope.
23. External Calendar không được tự ghi đè CRM trái sync policy.
24. Call Transcript AI không được coi là fact đã xác minh.
25. Audit Activity, SLA và NBA không được sửa.

---

# 158. Rule nghiệp vụ bắt buộc

1. Mỗi Task phải có Task Type.
2. Mỗi Task phải có primary context hoặc business reason hợp lệ.
3. Mỗi Task phải có owner hoặc queue.
4. Task có thể chưa có assignee khi nằm trong queue.
5. Task Ready phải đủ dependency.
6. Circular dependency bị chặn.
7. Task Completed phải đủ completion requirement.
8. Task yêu cầu evidence không được hoàn thành thiếu evidence.
9. Completed With Exception phải có reason.
10. Reopen Task phải giữ lịch sử completion.
11. Task cancellation không hủy resource nguồn.
12. Task reassignment phải có history.
13. Reassignment không reset SLA trái policy.
14. User inactive không được là assignee mới.
15. Recurring Task tạo instance riêng.
16. Reminder phải chống trùng.
17. Bulk complete bị chặn với Task yêu cầu evidence.
18. Appointment phải có start/end.
19. Appointment end phải sau start.
20. Appointment timezone bắt buộc.
21. Appointment confirmed phải đủ required confirmation.
22. Reschedule phải giữ thời gian cũ.
23. Cancellation phải có actor/reason.
24. No-show phải tách cancellation.
25. Attendance phải theo participant.
26. Appointment Outcome không tự chuyển Deal.
27. Site Visit phải kiểm tra Project/Listing Access.
28. Private viewing phải kiểm tra Mandate.
29. Appointment Resource không được double-book trái policy.
30. External sync conflict phải được xử lý.
31. Call Log phải có direction.
32. Call duration không được âm.
33. Click-to-call phải kiểm tra consent.
34. Call Recording phải có policy.
35. Transcript phải lưu source/model.
36. Transcript suggestion không tự sửa Customer.
37. Call Disposition cần user/provider source.
38. Missed call phải có follow-up policy.
39. Interaction phải có channel.
40. Interaction phải có occurred_at.
41. Outbound Interaction phải kiểm tra consent.
42. Outbound Interaction phải kiểm tra quiet hours.
43. Outbound Interaction phải kiểm tra frequency cap.
44. Do-not-contact phải được xử lý ưu tiên.
45. Internal Note không được gửi Customer.
46. Interaction Attachment không tự thành verified document.
47. Duplicate provider event không tạo Interaction mới.
48. Delivery status chỉ cập nhật từ nguồn hợp lệ.
49. Timeline Event phải có source.
50. Timeline Event phải có occurred_at và recorded_at.
51. Timeline Event correction không xóa original.
52. Timeline visibility không vượt resource scope.
53. Customer merge không nhân đôi event.
54. Timeline sensitive summary phải mask.
55. SLA Instance phải tham chiếu policy version.
56. SLA start phải có event.
57. SLA due phải tái tính được.
58. Pause phải có reason.
59. Waiting status không mặc định pause.
60. Extension không sửa due trực tiếp.
61. SLA breach giữ lịch sử dù được waiver sau đó.
62. Escalation không tự đổi assignee nếu policy không quy định.
63. NBA phải qua Permission Gate.
64. NBA phải qua Consent Gate.
65. NBA phải qua Workflow Gate.
66. NBA không đề xuất hành động đã có Task active trùng.
67. NBA phải có explanation.
68. NBA confidence không phải xác suất chốt.
69. NBA phải có expiry.
70. NBA expired không được execute.
71. NBA accept không tự hoàn thành action.
72. NBA execution phải dùng API capability nguồn.
73. NBA dismissal phải lưu reason khi policy yêu cầu.
74. AI không tự gửi outbound.
75. AI không tự duyệt nghiệp vụ.
76. AI summary không thay Timeline.
77. Delegation phải có effective dates.
78. Delegation không mở field ngoài scope.
79. Handover phải xử lý Task open.
80. Handover phải xử lý Appointment tương lai.
81. Handover không đổi attribution.
82. Handover không đổi commission.
83. Multi-Legal Entity phải xác định context.
84. Customer shared Enterprise không mở toàn Timeline.
85. Project Access không mở Customer Interaction.
86. Task Access không mở Contract detail ngoài quyền.
87. View không đồng nghĩa Export.
88. Sale không bulk export Call/Interaction.
89. Recording download cần quyền riêng.
90. Sensitive access phải audit.
91. Same idempotency key cùng payload trả cùng kết quả.
92. Same key khác payload phải conflict.
93. Domain event lặp không tạo Task trùng.
94. Calendar webhook lặp không tạo Appointment trùng.
95. Telephony webhook lặp không tạo Call trùng.
96. NBA run lặp phải chống recommendation trùng.
97. Task completion event phải idempotent.
98. SLA completion event lặp không thay kết quả.
99. Timeline projection có thể rebuild từ source.
100. Capability không thay thế Email, Telephony hoặc Calendar provider source of truth.

---

# 159. Cảnh báo và phát hiện bất thường

Hệ thống cần cảnh báo khi:

* Task không có owner/queue.
* Task open không có due time khi type bắt buộc.
* Task completed thiếu outcome.
* Task completed thiếu evidence.
* Task overdue lâu.
* Task bị reassign quá nhiều.
* Task dependency vòng lặp.
* Recurring Task tạo quá nhiều instance.
* User inactive còn Task active.
* Appointment trùng giờ.
* Appointment không có Customer confirmation.
* Appointment resource double-book.
* Site Visit không có access approval.
* Customer no-show nhiều lần.
* Internal user no-show nhiều lần.
* Appointment Completed nhưng không có attendance.
* Call Completed thiếu disposition.
* Call recording không có consent.
* Recording được truy cập hàng loạt.
* Transcript chứa dữ liệu nhạy cảm nhưng không restricted.
* Outbound call trái do-not-contact.
* Message gửi ngoài quiet hours trái policy.
* Customer bị contact vượt frequency cap.
* Interaction delivery failed nhiều lần.
* Same provider message tạo nhiều Interaction.
* Timeline Event không có source.
* Timeline Event nhạy cảm hiển thị sai audience.
* SLA chạy nhưng resource đã cancelled.
* SLA pause quá lâu.
* SLA extension quá nhiều.
* SLA breach không escalation.
* SLA due tính sai Business Calendar.
* NBA đề xuất action ngoài quyền.
* NBA đề xuất gọi Customer bị restricted.
* NBA trùng Task active.
* NBA bị dismiss lặp lại.
* NBA model ưu tiên bất thường một nhóm user.
* NBA confidence cao nhưng dữ liệu stale.
* Handover bỏ sót Appointment.
* User offboard còn Interaction thread assigned.
* Customer merge tạo Timeline trùng.
* Queue backlog tăng bất thường.
* First response SLA giảm mạnh.
* Sale tạo Task rồi complete ngay hàng loạt.
* Bulk status change bất thường.
* Export Call/Interaction lớn.
* Same idempotency key khác payload.
* Integration webhook signature lỗi.
* Calendar sync loop.
* Automation retry vượt ngưỡng.

---

# 160. Audit requirements và evidence

> Audit Context sở hữu immutable Audit facts. Activity chỉ phát sinh audit-worthy facts và references.

## 160.1. Thao tác bắt buộc

* Task create/update/assign/reassign.
* Task start/complete/reopen/cancel.
* Checklist.
* Dependency.
* Bulk operations.
* Appointment create/reschedule/cancel.
* Invitation.
* Attendance.
* Outcome.
* Calendar sync.
* Call initiation.
* Disposition.
* Recording access.
* Transcript access/review.
* Interaction create/send/reply.
* Attachment access.
* Do-not-contact processing.
* Timeline correction.
* SLA start/pause/extend/breach/complete.
* NBA generation/accept/dismiss/execute.
* Rule/model change.
* Delegation.
* Handover.
* Sensitive view.
* Export.

## 160.2. Nội dung

* Actor.
* Role.
* Legal Entity.
* User/Employee.
* Customer/Party.
* Primary context.
* Task.
* Appointment.
* Call.
* Interaction.
* Timeline Event.
* SLA.
* NBA.
* Before.
* After.
* Reason.
* Consent result.
* Permission result.
* Rule/model version.
* Business Calendar version.
* Source event.
* Approval.
* IP.
* Device.
* Request ID.
* Correlation ID.
* Idempotency key.
* Timestamp.
* Result.

---

# 161. Phạm vi MVP

## 161.1. Bắt buộc

* Task.
* Task Type.
* Task Template.
* Assignment.
* Reassignment.
* Queue.
* Checklist.
* Dependency.
* Reminder.
* Recurring Task cơ bản.
* Task Outcome.
* Completion evidence.
* Appointment.
* Participant.
* Confirmation.
* Reschedule.
* Cancellation.
* Attendance.
* No-show.
* Site Visit.
* Calendar view.
* Google/Microsoft Calendar integration cơ bản.
* Call Log.
* Click-to-call integration.
* Call disposition.
* Recording metadata.
* Interaction.
* Email/SMS/Zalo hoặc các kênh được ưu tiên.
* Thread.
* Delivery status.
* Consent gate.
* Quiet hours.
* Frequency cap cơ bản.
* Unified Timeline.
* Timeline visibility.
* Timeline correction.
* SLA Instance.
* Business Calendar clock.
* Warning.
* Breach.
* Pause.
* Extension.
* Escalation.
* Rule-based Next Best Action.
* NBA explanation.
* NBA acceptance/dismissal.
* NBA tạo Task.
* Delegation.
* Handover.
* Scope.
* Field masking.
* Audit.
* Dashboard.
* Domain events.

## 161.2. Giai đoạn nâng cao

* Omnichannel Inbox đầy đủ.
* Telephony call center nâng cao.
* Voicebot.
* AI transcription realtime.
* Conversation intelligence.
* Sentiment.
* Objection detection.
* Automated coaching.
* Advanced route planning.
* Customer self-booking.
* Resource optimization.
* Predictive no-show.
* Dynamic SLA.
* AI Next Best Action ranking.
* Reinforcement learning có kiểm soát.
* Customer journey orchestration.
* Automated outbound campaign integration.
* WhatsApp/social integrations.
* Advanced workforce management.
* Quality assurance scoring.
* Call script adherence.
* Meeting intelligence.
* Smart calendar scheduling.
* Cross-channel frequency optimization.

---

# 162. Tiêu chí nghiệm thu

Capability được xem là đạt khi:

1. Tạo được Task thủ công.
2. Tạo được Task từ domain event.
3. Tạo được Task từ workflow.
4. Task có Task Code.
5. Task có Task Type.
6. Task có primary context.
7. Task có owner hoặc queue.
8. Task có priority.
9. Task có status.
10. Task có start/due time.
11. Task lưu timezone.
12. Task có source.
13. Task có history.
14. Task hỗ trợ primary assignee.
15. Task hỗ trợ supporting assignee.
16. Task hỗ trợ watcher.
17. Task hỗ trợ reviewer.
18. Task Assignment có effective dates.
19. User inactive không được assign mới.
20. Queue Task được claim.
21. Reassignment lưu from/to.
22. Reassignment có reason.
23. Reassignment không mất lịch sử.
24. Reassignment không reset SLA trái rule.
25. Tạo Checklist được.
26. Required checklist chặn completion.
27. Checklist có evidence.
28. Tạo dependency được.
29. Dependency gate hoạt động.
30. Circular dependency bị chặn.
31. Task Ready được xác định.
32. Task Blocked được ghi nhận.
33. Waiting Customer được hỗ trợ.
34. Waiting Partner được hỗ trợ.
35. Waiting Approval được hỗ trợ.
36. Task completion yêu cầu outcome.
37. Task yêu cầu Call Log được validate.
38. Task yêu cầu file evidence được validate.
39. Completed With Exception hoạt động.
40. Reopen Task giữ completion cũ.
41. Cancel Task không cancel resource nguồn.
42. Task Overdue được tính.
43. Reminder trước hạn hoạt động.
44. Reminder chống trùng.
45. Tạo Task Template.
46. Template có version.
47. Active Template không sửa trực tiếp.
48. Due Rule theo business hours hoạt động.
49. Due Rule lưu Calendar Version.
50. Recurring Task tạo instance riêng.
51. Recurrence stop date hoạt động.
52. Incomplete recurrence policy hoạt động.
53. Bulk assign hoạt động.
54. Bulk complete bị chặn với Task có evidence.
55. Tạo Appointment.
56. Appointment có Type.
57. Appointment có organizer.
58. Appointment có owner.
59. Appointment có start/end.
60. Appointment end sau start.
61. Appointment có timezone.
62. Appointment có location/channel.
63. Thêm Customer participant được.
64. Thêm internal participant được.
65. Thêm external participant được.
66. Required participant được hỗ trợ.
67. Invitation được gửi.
68. Delivery status được lưu.
69. Confirmation được ghi.
70. Appointment chỉ Confirmed khi đủ rule.
71. User conflict được phát hiện.
72. Resource conflict được phát hiện.
73. Travel conflict được cảnh báo.
74. Outside business hours được cảnh báo.
75. Override conflict cần reason.
76. Reschedule giữ old/new time.
77. Reschedule gửi update.
78. Cancellation có actor/reason.
79. Resource được release khi cancel.
80. Customer no-show được ghi.
81. Internal no-show được ghi.
82. Attendance theo participant.
83. Appointment Outcome được ghi.
84. Outcome không tự chuyển Deal.
85. Tạo Site Visit.
86. Site Visit link Project.
87. Site Visit link Listing.
88. Private viewing kiểm tra Mandate.
89. Exact address được mask.
90. Products viewed được ghi.
91. Customer feedback được ghi.
92. External Calendar event được tạo.
93. External Calendar ID được lưu.
94. Sync update hoạt động.
95. Sync conflict được phát hiện.
96. External delete không tự xóa CRM trái policy.
97. Tạo Call Log thủ công.
98. Click-to-call hoạt động.
99. Click-to-call kiểm tra Customer scope.
100. Click-to-call kiểm tra consent.
101. Call direction được lưu.
102. Call status được lưu.
103. Call duration được tính.
104. Missed call được ghi.
105. Disposition được ghi.
106. Call Outcome được ghi.
107. Follow-up Task được tạo.
108. Provider Call ID unique.
109. Recording metadata được lưu.
110. Recording cần consent.
111. Sale khác không xem recording trái scope.
112. Transcript metadata được lưu.
113. Transcript có model version.
114. Transcript có confidence.
115. Extraction suggestion được tạo.
116. Suggestion không tự sửa Requirement.
117. User accept/reject suggestion được.
118. Telephony webhook idempotent.
119. Tạo Interaction.
120. Interaction có channel.
121. Interaction có direction.
122. Interaction có type.
123. Interaction có sender/recipient.
124. Interaction có occurred_at.
125. Email inbound được ghi.
126. Email outbound được ghi.
127. SMS/Zalo hoặc kênh ưu tiên được ghi.
128. Interaction Thread hoạt động.
129. External Message ID chống trùng.
130. Delivery status được cập nhật.
131. Read status được cập nhật khi provider hỗ trợ.
132. Attachment metadata được lưu.
133. Malware status được lưu.
134. Attachment không tự thành verified document.
135. Internal Note không gửi ra ngoài.
136. Outbound kiểm tra consent.
137. Quiet Hours được enforce.
138. Frequency Cap được enforce.
139. Do-not-contact chặn outbound.
140. Do-not-contact request tạo Timeline.
141. Failed delivery tạo alert.
142. Tạo Timeline Event từ Task.
143. Tạo Timeline Event từ Appointment.
144. Tạo Timeline Event từ Call.
145. Tạo Timeline Event từ Interaction.
146. Tạo Timeline Event từ capability nguồn.
147. Timeline có occurred_at.
148. Timeline có recorded_at.
149. Timeline có actor.
150. Timeline có source.
151. Timeline có schema version.
152. Timeline visibility hoạt động.
153. Timeline field masking hoạt động.
154. Finance event được mask với sale.
155. Legal event được mask theo quyền.
156. Timeline correction tạo event mới.
157. Original Timeline không bị sửa.
158. Customer merge giữ Timeline.
159. Customer merge không nhân đôi event.
160. Timeline search hoạt động.
161. Timeline filter hoạt động.
162. Tạo SLA Instance.
163. SLA tham chiếu Definition Version.
164. SLA tham chiếu Business Calendar Version.
165. SLA start từ event đúng.
166. SLA due time tính đúng.
167. SLA warning hoạt động.
168. SLA at-risk hoạt động.
169. SLA breach hoạt động.
170. Breach không tự approve nghiệp vụ.
171. Pause Request được tạo.
172. Pause có reason.
173. Waiting không tự pause trái policy.
174. Resume SLA hoạt động.
175. Pause duration được tính.
176. Extension Request được tạo.
177. Extension cần approval.
178. New due time được lưu.
179. Extension không xóa due cũ.
180. Escalation route hoạt động.
181. Team Lead nhận escalation.
182. Department Head nhận escalation đúng rule.
183. SLA Completed Within được ghi.
184. SLA Completed After được ghi.
185. SLA invalidation có reason.
186. Tạo NBA Run.
187. NBA lấy đúng context.
188. NBA Permission Gate hoạt động.
189. NBA Consent Gate hoạt động.
190. NBA Workflow Gate hoạt động.
191. NBA loại action ngoài quyền.
192. NBA loại outbound bị restricted.
193. NBA suppress Task trùng.
194. NBA có priority.
195. NBA có confidence.
196. NBA có explanation.
197. NBA có expiry.
198. NBA expired không execute.
199. NBA Accept hoạt động.
200. NBA Accept and Create Task hoạt động.
201. NBA Dismiss hoạt động.
202. NBA Snooze hoạt động.
203. NBA Execution dùng API capability nguồn.
204. NBA không tự xác nhận Payment.
205. NBA không tự duyệt Contract.
206. NBA Feedback được lưu.
207. Rule-based NBA Proposal Follow-up hoạt động.
208. NBA Hold Expiry hoạt động.
209. NBA Deposit Due hoạt động.
210. NBA Receivable Overdue hoạt động.
211. AI summary có source/model version.
212. AI summary không thay Timeline.
213. Delegation được áp dụng cho Task.
214. Delegation có effective dates.
215. Delegation không mở field trái quyền.
216. Handover chuyển Open Task.
217. Handover chuyển Future Appointment.
218. Handover xử lý Interaction Thread.
219. Handover giữ SLA history.
220. Handover không đổi attribution.
221. Handover không đổi commission.
222. Sale chỉ xem `mine`.
223. Team Lead xem `team`.
224. Department Head xem `department`.
225. Director xem `all` theo quyền.
226. Backend enforce Legal Entity.
227. Backend enforce resource scope.
228. Backend enforce field masking.
229. Sửa URL không mở rộng quyền.
230. View không cho Export.
231. Sale không bulk export Interaction.
232. Recording download cần capability.
233. Sensitive access có audit.
234. Same idempotency key cùng payload trả cùng kết quả.
235. Same key khác payload báo conflict.
236. Domain event lặp không tạo Task trùng.
237. Calendar webhook lặp không tạo Appointment trùng.
238. Telephony webhook lặp không tạo Call trùng.
239. Message webhook lặp không tạo Interaction trùng.
240. Timeline projection rebuild được.
241. Dashboard My Work đúng scope.
242. Team workload đúng scope.
243. SLA dashboard drill-down đúng scope.
244. NBA dashboard đúng scope.
245. Capability hỗ trợ Lead.
246. Capability hỗ trợ Customer.
247. Capability hỗ trợ Listing.
248. Capability hỗ trợ Matching.
249. Capability hỗ trợ Deal.
250. Capability hỗ trợ Booking.
251. Capability hỗ trợ Contract.
252. Capability hỗ trợ Receivable/Receipt.
253. Capability hỗ trợ Revenue.
254. Capability hỗ trợ Commission.
255. Capability điều phối hoạt động toàn CRM mà không thay thế workflow nghiệp vụ của các capability nguồn.

---

# 163. Quan hệ canonical với các Context liên quan

## 163.1. Platform Context

Activity sử dụng Business Calendar, SLA, Notification và Workflow definitions cùng configuration references.

Platform sở hữu definitions; Activity sở hữu runtime Task, SLA, Appointment và Interaction instances.

## 163.2. IAM Context

Activity sử dụng User, Workforce, organization, delegation, acting role, handover và effective authorization.

Activity không tạo organization rule hoặc mở rộng delegation.

## 163.3. Lead Context

Task, Call hoặc Interaction có thể hỗ trợ Lead follow-up.

Task completion không thay Lead assignment, care protection, qualification hoặc conversion nếu Lead Context chưa chấp nhận command.

## 163.4. Party Context

Activity sử dụng canonical Customer/Party, consent, preference, restriction và redirect.

Customer merge không xóa Interaction hoặc Timeline; outbound action luôn kiểm tra Party policy hiện hành.

## 163.5. Product và Matching Contexts

Activity sử dụng Listing, Project, viewing rights, Availability, Match Result và Shortlist references.

Appointment hoặc Site Visit không tạo Commercial Lock. Activity không sửa Matching Result.

## 163.6. Transaction Context

Activity sử dụng Deal, Proposal, Hold, Booking và Deposit Commitment references.

Task hoặc Appointment outcome không tự chuyển Deal stage hay xác nhận Booking.

## 163.7. Contract Context

Activity sử dụng Contract, Receivable, Payment, Receipt, Refund và Settlement references.

Sale không xác nhận money movement bằng Task hoặc Call outcome.

## 163.8. Revenue Context

Activity hỗ trợ reconciliation, Commission dispute, payout review và Clawback work.

NBA hoặc Task không tự approve Revenue, Commission, Payout hoặc Clawback.

## 163.9. Documents, Integration, Analytics và Audit

- Documents sở hữu File, Document, recording, transcript và attachment artifacts.
- Integration sở hữu provider transport/runtime.
- Analytics sở hữu certified activity, SLA, conversion và NBA Metrics.
- Audit sở hữu immutable Audit facts.

---

# 164. Anti-patterns và canonical requirements

## AP-ACT-001 — Mọi hoạt động nằm trong một bảng note

**Không được áp dụng**

Dùng một note record cho Task, Appointment, Call, Interaction và Timeline.

**Canonical requirement**

Các concepts phải có models và lifecycles riêng; Timeline chỉ tổng hợp normalized facts và references.

## AP-ACT-002 — Task Completed đồng nghĩa business transition

**Không được áp dụng**

Hoàn thành Task tự chuyển Lead, Deal, Booking, Contract, Payment hoặc Commission.

**Canonical requirement**

Activity chỉ ghi outcome/evidence và gửi command; owning Context validate transition bằng authoritative rules.

## AP-ACT-003 — Task hoàn thành tự tạo Interaction

**Không được áp dụng**

Đánh dấu Task gọi Customer hoàn tất rồi tự sinh Call Log thành công.

**Canonical requirement**

Task là kế hoạch; Call hoặc Interaction thực tế cần provider/user evidence riêng và có thể liên kết completion.

## AP-ACT-004 — Appointment Completed đồng nghĩa cuộc gặp thành công

**Không được áp dụng**

Appointment tới hạn tự chuyển Completed hoặc ghi Customer attended.

**Canonical requirement**

Attendance, no-show, outcome và Interaction thực tế phải được ghi riêng với evidence phù hợp.

## AP-ACT-005 — Timeline là nguồn nghiệp vụ có thể sửa

**Không được áp dụng**

Sửa Timeline Event để đổi Contract, Receipt, Deal hoặc Customer history.

**Canonical requirement**

Timeline là rebuildable projection. Correction dùng superseding/correction Event; source business state chỉ thay qua owning Context.

## AP-ACT-006 — SLA chỉ là `due_at`

**Không được áp dụng**

Một deadline không có policy version, calendar, pause, warning, breach hoặc escalation.

**Canonical requirement**

SLA Instance phải giữ Definition Version, Business Calendar Version, clock segments, start/completion Events và governed exceptions.

## AP-ACT-007 — Waiting tự động pause mọi SLA

**Không được áp dụng**

Task chuyển Waiting là clock dừng ngay.

**Canonical requirement**

Pause chỉ xảy ra theo SLA Policy, reason, evidence và approval hoặc automation hợp lệ.

## AP-ACT-008 — NBA vượt permission, consent hoặc workflow

**Không được áp dụng**

Recommendation đề xuất hoặc gọi action mà user không có quyền hoặc Customer không được liên hệ.

**Canonical requirement**

Permission Gate, Consent Gate và Workflow Gate chạy trước ranking; execution vẫn qua owning Context/API.

## AP-ACT-009 — NBA hoặc AI tự thực hiện risky action

**Không được áp dụng**

AI tự gọi, gửi message, xác nhận tiền, duyệt Contract hoặc Commission.

**Canonical requirement**

AI chỉ hỗ trợ ranking, summary, extraction và explanation; risky execution cần approved automation hoặc human action cùng authoritative checks.

## AP-ACT-010 — Activity sở hữu consent

**Không được áp dụng**

Dùng consent snapshot cũ như quyền liên hệ vĩnh viễn hoặc tự sửa contact restriction.

**Canonical requirement**

Party Context là authority; Activity re-check trước outbound và gửi governed update request khi phát hiện do-not-contact.

## AP-ACT-011 — Activity sở hữu provider transport và files

**Không được áp dụng**

Lưu credentials, raw retries, recording URL hoặc attachment URL làm source canonical.

**Canonical requirement**

Integration sở hữu transport/runtime; Documents sở hữu File/Document artifacts; Activity giữ normalized records và governed references.

## AP-ACT-012 — Activity access mở sensitive source data

**Không được áp dụng**

Xem Task, Appointment hoặc Timeline rồi truy cập toàn bộ Customer, Contract, Finance hoặc recording.

**Canonical requirement**

Backend intersect Activity permission, source-resource access, visibility, Legal Entity scope và field masking.

## AP-ACT-013 — Handover thay attribution hoặc Commission

**Không được áp dụng**

Chuyển assignee/open work rồi tự đổi Lead source, Deal attribution hoặc Commission Participant.

**Canonical requirement**

Operational responsibility, attribution và financial entitlement là các dimensions riêng thuộc owning Contexts.

## AP-ACT-014 — External Calendar delete xóa Appointment CRM

**Không được áp dụng**

Provider event bị xóa thì CRM Appointment bị xóa hoặc cancel ngay không qua policy.

**Canonical requirement**

Integration ghi accepted sync fact; Activity áp sync-conflict policy, history và manual review khi cần.

## AP-ACT-015 — Transcript hoặc AI summary là verified fact

**Không được áp dụng**

Dùng AI extraction trực tiếp sửa Requirement, consent, payment promise hoặc legal/financial state.

**Canonical requirement**

AI output phải có source, model, confidence, phân biệt fact/inference và cần human hoặc workflow confirmation cho material updates.

## AP-ACT-016 — Operational tables là certified analytics

**Không được áp dụng**

Dùng Task, Call, SLA hoặc NBA tables trực tiếp làm enterprise KPI không semantic governance.

**Canonical requirement**

Activity phát governed facts; Analytics sở hữu Metric grain, formulas, snapshots, certification và access.

## AP-ACT-017 — Candidate examples là exact contracts

**Không được áp dụng**

Dùng table names, endpoints, statuses, Events, permissions hoặc score formula trong tài liệu này để code trực tiếp.

**Canonical requirement**

Exact database, API, Event, lifecycle, permission, SLA, AI và integration contracts phải được khóa trong nguồn canonical tương ứng.

## AP-ACT-018 — Mặc định tồn tại hệ thống tiền nhiệm

**Không được áp dụng**

Tự thiết kế old-task mappings, compatibility layer hoặc historical aliases khi chưa có approved scope.

**Canonical requirement**

`crm_bds_ai` là Greenfield. Historical import chỉ tồn tại khi có scope, source mapping, security review, reconciliation và acceptance criteria riêng.

---

# 165. Kết luận

Activity and Engagement Capability là lớp điều phối công việc và tương tác dùng chung của `crm_bds_ai`.

Capability phải bảo đảm:

- Task là kế hoạch công việc, không giả lập Interaction thực tế.
- Appointment tách khỏi attendance, no-show và outcome.
- Call và Interaction có source, consent, provider evidence và idempotency.
- Party Context vẫn là authority cho consent và contact restriction.
- Documents Context sở hữu recordings, transcripts và attachments.
- Integration Context sở hữu provider transport/runtime.
- Timeline là immutable, rebuildable projection và không phải business source.
- Timeline visibility không vượt source-resource access.
- SLA có policy/calendar version, clock segments, pause, warning, breach và escalation.
- NBA có permission, consent và workflow gates trước ranking.
- NBA và AI không tự thực hiện risky action.
- Task và Outcome không direct-write owning Context aggregates.
- Delegation và handover không thay attribution hoặc Commission.
- Cross-context orchestration dùng local transaction, Outbox, idempotency và reconciliation.
- Certified activity, SLA và NBA Metrics thuộc Analytics.
- Immutable Audit facts thuộc Audit Context.
- Provider systems vẫn giữ transport truth.
- My Work, Timeline, SLA và NBA cung cấp operational visibility đúng scope.

> Activity Context điều phối action và engagement; nó không sở hữu business outcome của Lead, Product, Transaction, Contract hoặc Revenue.
