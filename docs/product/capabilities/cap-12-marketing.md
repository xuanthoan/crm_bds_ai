# CRM_BDS_AI — CAPABILITY 12: MARKETING

## Campaign, Lead Source Evidence, Audience, Journey Automation, Attribution and Conversion Measurement

**Document ID:** `PROD-CAP-MKT-001`
**Canonical path:** `docs/product/capabilities/cap-12-marketing.md`
**Product:** `crm_bds_ai`
**Version:** `1.0.0`  
**Status:** `Accepted / Product Capability Baseline`
**Document type:** `Product Capability Specification`
**Primary capability code:** `CAP-MKT`
**Primary owning Context:** `marketing`
**Owner:** `Product Owner`
**Co-owner:** `Marketing Domain Owner`
**Reviewers:** `Architecture Owner`, `Platform Domain Owner`, `IAM Domain Owner`, `Party Domain Owner`, `Lead Domain Owner`, `Product Domain Owner`, `Matching Domain Owner`, `Transaction Domain Owner`, `Contract Domain Owner`, `Revenue Domain Owner`, `Activity Domain Owner`, `Documents Owner`, `Integration Owner`, `Analytics Owner`, `Audit Owner`, `Security Owner`, `Database Owner`, `API Owner`, `Event Architecture Owner`, `AI Governance Owner`, `Operations Owner`, `QA Owner`
**Effective date:** `2026-08-05`  
**Last reviewed:** `2026-08-05`  
**Classification:** `INTERNAL`

---

# 0. Phạm vi thẩm quyền và quan hệ tài liệu

Tài liệu này là nguồn canonical cho:

- Product outcomes của Marketing Capability.
- Business meanings của Campaign, Flight, Channel Execution, Marketing Capture, Touchpoint, Audience, Journey, Marketing Message Intent, Conversion, Attribution, Operational Spend và Experiment.
- Marketing-specific eligibility, suppression, frequency policy, attribution và campaign measurement.
- Capability boundaries, invariants, acceptance outcomes và anti-patterns.
- Đầu vào phân tích cho Marketing Context Implementation Pack.

Tài liệu này không phải nguồn exact cho:

- Physical database schema hoặc DDL.
- Exact API paths, payloads, errors hoặc authorization metadata.
- Exact Event names, envelope hoặc payloads.
- Exact permission codes, scopes, masking hoặc role matrix.
- Exact state machines, source codes, channel codes, attribution formulas, lookback windows hoặc KPI formulas.
- Exact Lead, Customer, consent, Interaction, Contract hoặc Revenue behavior.
- Exact ad platform, website analytics, messaging, call-tracking, CMS, bank hoặc ERP integration.
- Exact File, Document, Creative binary hoặc export storage.
- Exact certified Funnel, CAC, ROAS, ROMI hoặc Revenue Metrics.
- Exact queue, retry, retention, batch hoặc deployment configuration.

Nguồn exact tương ứng:

| Chủ đề | Nguồn canonical |
|---|---|
| Thuật ngữ | Domain Glossary |
| Product requirements | PRD |
| Context ownership | Source of Truth Matrix |
| Architecture boundaries | Architecture Overview, Context Map và Accepted ADRs |
| Marketing behavior chi tiết | Marketing Context Implementation Pack |
| Database | Marketing Context DB Specification và Alembic historical imports |
| API | OpenAPI |
| Events | JSON Schema, AsyncAPI và Event Registry |
| Permissions/scopes/masking/SoD | Security registries và matrices |
| Lead/assignment/care protection/Lead Source Snapshot | Lead Context contracts |
| Customer/Party identity/consent/contact restriction | Party Context contracts |
| Project/Listing/Product facts | Product Context contracts |
| Deal/Booking/Sales attribution | Transaction Context contracts |
| Contract/Payment/Receipt/Cancellation | Contract Context contracts |
| Revenue/Commission | Revenue Context contracts |
| Interaction/Call/Appointment/Timeline/outbound activity | Activity Context contracts |
| File/Document/Creative artifact | Documents Context contracts |
| Provider/CMS/ad platform/messaging transport | Integration Context contracts |
| Certified Marketing/Funnel/ROI Metrics | Analytics Context và Metric Registry |
| Immutable Audit facts | Audit Context |
| Runtime jobs/incidents | Operations Context |
| Công việc hiện tại | Current Sprint Detailed Execution Pack |

**Capability không đồng nghĩa Bounded Context.** Capability này chủ yếu được thực hiện bởi `marketing` Context. Nó sở hữu campaign orchestration, marketing touchpoints, audience/journey state và attribution results, nhưng không được direct-write aggregates thuộc `lead`, `party`, `product`, `matching`, `transaction`, `contract`, `revenue`, `activity`, `documents`, `integration`, `analytics` hoặc `audit`.

Các phần candidate lifecycle, data model, operations, permissions, Events, screens, formulas và reports chỉ là design input. Chúng không được dùng thay machine-readable contracts hoặc Context Packs đã được chấp nhận.

---
# 1. Mục tiêu của capability

Marketing Capability quản lý vòng đời Marketing của `crm_bds_ai`, từ Campaign strategy, source/tracking, audience, content intent, capture, journey automation và attribution đến operational conversion/cost measurement.

Capability phải trả lời được:

- Campaign nào đang được chuẩn bị, phê duyệt, chạy, tạm dừng hoặc hoàn tất.
- Campaign thuộc Enterprise, Legal Entity, Project, Sales Launch, Brand hoặc Partner context nào.
- Channel, Flight, Placement, Creative và Landing Page nào đã được sử dụng.
- Marketing Capture hoặc Touchpoint nào tạo ra Lead intake request.
- Lead Source Snapshot nào đã được Lead Context chấp nhận tại thời điểm intake.
- Customer đã tồn tại hay là anonymous/unknown identity.
- Marketing influence nào xuất hiện trước Lead, Deal, Booking, Contract hoặc Revenue milestone.
- Marketing Attribution khác Sales Attribution và Commission entitlement như thế nào.
- Audience Version nào được đánh giá, ai đủ điều kiện, ai bị suppress và tại thời điểm nào.
- Consent, contact restriction, quiet hours, frequency cap và channel policy có cho phép outbound intent không.
- Journey Version nào đã enroll một entity và mỗi node đã thực thi ra sao.
- Marketing Message Intent nào đã được Activity/Integration chấp nhận, gửi, delivered, read, clicked, replied, bounced hoặc suppressed.
- Conversion Definition và Attribution Model Version nào đã được sử dụng.
- Contract cancellation hoặc Revenue reversal ảnh hưởng gross/net conversion và attributed value ra sao.
- Campaign Budget khác operational Spend và official accounting cost như thế nào.
- CPL, CPQL, CAC, ROAS và ROMI đang dùng denominator/numerator basis nào.
- Experiment/control/holdout có giữ integrity và consent không.
- Mọi calculation, audience membership và outbound decision có thể tái tạo từ versions, snapshots, facts và Audit evidence hay không.

Capability phải hỗ trợ:

- Brand, Project, Sales Launch, Lead Generation, Event, Referral, Partner, Nurture, Reactivation, Cross-sell và Acquisition Campaigns.
- Paid, organic, offline, event, call-center, website, email và messaging channels.
- Campaign hierarchy, Flight, Channel Execution, Placement và Creative Version.
- Source taxonomy, mapping, UTM, tracking URL, QR và call-tracking references.
- Form/Lead Ads/Event/Referral capture với validation, spam và deduplication.
- Anonymous Visitor và provisional identity-link evidence.
- Marketing Touchpoint và source confidence.
- Audience Definition/Version, evaluation, membership snapshot, suppression và activation intent.
- Journey/Automation Version, enrollment, node execution, retry, replay và safety limits.
- Marketing Message Intent liên kết Activity Interaction.
- First Touch, Lead Creation Touch, Last Touch và multi-touch attribution.
- Sourced và Influenced views.
- Contract/Revenue attribution adjustments.
- Operational Budget, Spend, Cost Allocation và vendor reconciliation.
- A/B Test, Control Group và Holdout.
- Multi-Legal Entity, Project Access, consent, masking, retention và Audit.
- Integration với ad platforms, website/CMS, analytics providers, forms, call tracking và messaging.

Nguyên tắc canonical:

> Marketing được ghi nhận Campaign, capture, Touchpoint, audience eligibility, journey và analytical influence; Marketing không sở hữu Customer identity, Lead assignment, sales responsibility, Contract/Revenue truth hoặc Interaction transport, và không được phát outbound khi chưa vượt qua Consent, Suppression, Frequency, Channel và Workflow gates.

---
# 2. Vị trí của capability trong kiến trúc

Marketing Context sử dụng:

- `platform`: configuration, Workflow/Approval, Business Calendar, templates, feature flags và policy definitions.
- `iam`: authenticated identity, Legal Entity, Project Access, effective scope, delegation và SoD decisions.
- `party`: canonical Party/Customer identity, roles, consent, preferences, contact restriction và redirect.
- `lead`: Lead intake result, official Lead, assignment, care protection, status, conversion và accepted Lead Source Snapshot.
- `product`: Partner, Project, Sales Launch, Listing, Product status và commercial references.
- `matching`: Match Result, Shortlist, Feedback và approved behavioral-signal references.
- `transaction`: Deal, Proposal, Hold, Booking, Sales Attribution và participant facts.
- `contract`: Contract, Payment/Receipt/Cancellation facts và contract-value components.
- `revenue`: Revenue Entitlement, Recognition, Collection, Reversal và Commission facts.
- `activity`: Interaction, Call, Appointment, Timeline, outbound eligibility/execution facts, quiet-hours/frequency evidence và Tasks.
- `documents`: Creative, Content, Landing Page, Form, export và evidence Document references.
- `integration`: ad platform, CMS, website analytics, Lead Ads, messaging, call-tracking, provider callbacks và ERP transport.
- `operations`: scheduled evaluation, journey execution, retry/DLQ và incident runtime.
- `audit`: immutable evidence của governed actions.
- `analytics`: certified Marketing/Funnel/ROI metrics và analytical snapshots.

Marketing Context cung cấp:

- Cho `lead`: versioned capture/source evidence và idempotent Lead intake request; Lead Context quyết định create/link, assignment và official source snapshot.
- Cho `party`: identity-resolution evidence và consent/restriction update requests; Party vẫn là authority.
- Cho `product`/`matching`: governed aggregate interest signals khi được phép.
- Cho `transaction`: Campaign influence và attribution references; không sửa Sales Attribution.
- Cho `activity`: outbound message/task intent và journey context; Activity tạo normalized Interaction/Task.
- Cho `analytics`: versioned campaign, audience, spend, conversion và attribution facts; Analytics định nghĩa certified Metrics.
- Cho provider systems qua `integration`: audience activation, campaign sync, message delivery và offline-conversion intents.

Luồng khái quát:

```text
Campaign Strategy
→ Campaign Version
→ Flight / Channel / Creative
→ Marketing Touchpoint or Capture
→ Lead intake through Lead Context
→ Party resolution through Party Context
→ Deal / Booking / Contract / Revenue facts
→ Conversion and Attribution
→ Certified analytics through Analytics Context
```

Luồng Customer đã tồn tại:

```text
Existing Customer
→ New Marketing Touchpoint
→ New interest/capture context
→ No automatic owner or sales-attribution change
→ New Marketing Influence only
```

Cross-context propagation sử dụng published APIs, durable Events, Transactional Outbox, idempotent consumers và reconciliation. Marketing không direct-write source aggregates và không dùng distributed transaction xuyên Contexts.

---
# 3. Ranh giới sở hữu dữ liệu

## 3.1. Marketing Context sở hữu

- Campaign, Campaign Version, Objective, hierarchy, scope, Flight, Channel Execution và Placement.
- Campaign Budget intent, Operational Spend representation, Cost Allocation và vendor reconciliation state.
- Creative/Content business metadata, Version, rights, approval và Document references.
- Landing Page/Form definitions, versions, Marketing Submission/Capture và processing state.
- Marketing Touchpoint, anonymous visitor identifiers và provisional identity-link evidence.
- Source taxonomy, mapping rule, UTM/tracking registry và normalization evidence.
- Audience, Definition, Version, evaluation run, membership snapshot, marketing suppression và activation intent/state.
- Journey/Automation, Version, enrollment, step execution, Marketing Message Intent và retry/replay domain state.
- Conversion Definition, operational Conversion, Attribution Model/Version, run, result, influence và adjustments.
- Marketing Experiment, Variant, Assignment và operational result.
- Marketing-originated business facts và Audit requests.

## 3.2. Marketing Context không sở hữu

- Official Lead, Lead assignment, care protection, qualification, status hoặc canonical Lead Source Snapshot: `lead`.
- Canonical Party/Customer identity, Requirement, consent, contact preference hoặc contact restriction: `party`.
- Project, Asset, Listing, Price, Sales Policy hoặc Availability: `product`.
- Match Result hoặc matching rules: `matching`.
- Deal, Booking, Sales Attribution, responsibility hoặc Co-sale Agreement: `transaction`.
- Contract, Payment, Receipt, Refund hoặc Cancellation source truth: `contract`.
- Revenue Entitlement, Recognition, Receivable, Collection, Commission hoặc Clawback: `revenue`.
- Canonical Interaction, Call, Appointment, Task, Timeline hoặc cross-channel contact history: `activity`.
- Binary File, Document, Creative/Content artifact hoặc export file: `documents`.
- Provider credentials, raw callbacks, ad platform/CMS/messaging/call-tracking transport hoặc retries: `integration`.
- Certified Marketing, Funnel, CAC, ROAS, ROMI hoặc Revenue Metrics: `analytics`.
- Immutable Audit facts: `audit`.
- General Ledger, statutory marketing accounting hoặc official vendor payable: ERP/accounting system.
- Job, queue infrastructure, retry/DLQ hoặc incident runtime: `operations`.

## 3.3. Lead intake và Lead Source Snapshot

Marketing sở hữu Marketing Capture, raw/normalized source evidence và proposed source payload.

Lead Context sở hữu:

- Official Lead creation/linking.
- Assignment và care protection.
- Canonical Lead Source Snapshot accepted at intake.
- Lead status và conversion.

Marketing không được tự tạo Lead/Customer records song song hoặc sửa official Lead Source Snapshot. Source correction phải đi qua governed Lead command và giữ original evidence.

## 3.4. Customer identity và anonymous linking

Marketing có thể giữ anonymous identifiers và provisional identity-link evidence.

Party Context quyết định canonical Party/Customer resolution, merge và redirect. Shared device, shared phone hoặc shared email không đủ để khẳng định identity.

## 3.5. Consent, suppression và frequency boundaries

Party Context sở hữu canonical consent và contact restriction.

Marketing sở hữu:

- Campaign/journey-specific eligibility.
- Marketing suppression rules/snapshots.
- Marketing-specific frequency policies/counters.
- Audience exclusion decisions.

Activity Context sở hữu normalized cross-channel contact facts và thực hiện final outbound eligibility checks theo Party policy.

Marketing eligibility snapshot không phải quyền liên hệ vĩnh viễn. Mọi outbound execution phải re-check current Party/Activity policy.

## 3.6. Marketing Message, Interaction và provider execution

Marketing sở hữu Marketing Message Intent và journey/campaign relationship.

Activity Context sở hữu canonical Interaction, Call, Task và Timeline records.

Integration Context sở hữu provider transport, credentials, callbacks, retries và external delivery truth.

Marketing status `QUEUED` hoặc `SCHEDULED` không đồng nghĩa message đã gửi. Delivery/read/click/reply projections chỉ cập nhật từ accepted Activity/Integration facts.

## 3.7. Content và Documents

Marketing sở hữu content meaning, version, personalization schema, rights, approval và rendering hash/snapshot.

Documents Context sở hữu binary images, videos, PDFs, brochures, exports và Document Versions.

Permanent Document reference không phải canonical artifact identity.

## 3.8. Attribution, Analytics và Revenue

Marketing sở hữu attribution models/runs/results ở cấp Campaign/Touchpoint.

Revenue Context sở hữu Revenue truth. Analytics Context sở hữu certified funnel, acquisition-cost, ROAS, ROMI và executive Metrics.

Attributed value không thay Contract Value, Revenue Entitlement hoặc Revenue Recognition.

---
# 4. Các lớp dữ liệu bắt buộc phải tách

## 4.1. Campaign

Chương trình Marketing có mục tiêu, thời gian, ngân sách và phạm vi xác định.

## 4.2. Campaign Execution

Lần triển khai cụ thể theo Channel, Flight, Audience và Creative.

## 4.3. Touchpoint

Một lần Customer hoặc anonymous identity tiếp xúc với nội dung, Campaign hoặc Channel.

## 4.4. Lead Source

Nguồn dẫn đến việc tạo Lead.

## 4.5. Marketing Attribution

Cách phân bổ ảnh hưởng Marketing cho conversion.

## 4.6. Sales Attribution

Quyền ghi nhận nguồn bán hàng, sale, co-sale và trách nhiệm thương mại.

Sales Attribution thuộc Lead/Transaction Contexts.

## 4.7. Audience

Tập hợp Party/Customer/Lead/anonymous identity đủ điều kiện Marketing tại một thời điểm.

## 4.8. Journey Automation

Quy trình tự động điều phối message, wait, branch, Task và audience membership.

## 4.9. Conversion

Một sự kiện mục tiêu được xác định rõ.

## 4.10. Revenue Attribution

Việc phân bổ Revenue cho Campaign theo mô hình báo cáo.

Không thay Revenue Entitlement pháp lý của Revenue and Commission Capability.

---

# 5. Nguyên tắc phân biệt Marketing Attribution và Sales Attribution

## 5.1. Marketing Attribution

Trả lời:

* Campaign nào tạo hoặc ảnh hưởng hành trình?
* Channel nào đóng góp?
* Touchpoint nào xảy ra trước conversion?
* Chi phí Marketing nào liên quan?

## 5.2. Sales Attribution

Trả lời:

* Lead được giao cho ai?
* Ai chăm sóc?
* Ai là primary sale?
* Ai là co-sale?
* Ai được hưởng commission?

## 5.3. Marketing không thay Sales Attribution

Một Customer xem quảng cáo mới sau khi đã được sale chăm sóc không làm:

* Mất care protection.
* Chuyển Customer cho sale khác.
* Đổi primary sale.
* Đổi co-sale.
* Đổi commission participant.
* Viết lại Lead source snapshot cũ.

## 5.4. Có thể đồng thời tồn tại

Ví dụ:

* Lead first source: Facebook Lead Ads.
* Lead assigned sale: Sale A.
* Campaign influence trước Booking: Email Nurture.
* Primary sale: Sale A.
* Co-sale: Sale B.
* Contract attribution: Facebook 60%, Email 40%.
* Commission: theo Co-sale Agreement, không theo tỷ lệ Marketing attribution.

---

# 6. Marketing Operating Model

Capability phải hỗ trợ các cấp:

```text
Enterprise Marketing Strategy
→ Brand / Business Line
→ Marketing Program
→ Campaign
→ Campaign Flight
→ Channel Execution
→ Placement / Ad Set
→ Ad / Creative
→ Touchpoint
```

Không bắt buộc mọi doanh nghiệp dùng đủ mọi cấp.

---

# 7. Campaign Hierarchy

Một Campaign có thể có:

* Parent Campaign.
* Child Campaign.
* Program.
* Project.
* Sales Launch.
* Legal Entity.
* Brand.
* Region.
* Business line.

Ví dụ:

```text
Program: Mở bán Project A
├── Campaign: Teaser
├── Campaign: Official Launch
├── Campaign: Site Visit
├── Campaign: Retargeting
└── Campaign: Customer Nurture
```

Campaign con phải kế thừa hoặc override cấu hình có kiểm soát.

---

# 8. Candidate Campaign Type vocabulary — pending validation

```text
BRAND_AWARENESS
PROJECT_AWARENESS
LEAD_GENERATION
SELLER_ACQUISITION
OWNER_ACQUISITION
BUYER_ACQUISITION
INVESTOR_ACQUISITION
PRODUCT_LAUNCH
SALES_LAUNCH
EVENT
OPEN_HOUSE
SITE_VISIT
WEBINAR
CONTENT
SEARCH
SOCIAL
DISPLAY
VIDEO
EMAIL_NURTURE
MESSAGING_NURTURE
RETARGETING
REACTIVATION
CROSS_SELL
UPSELL
REFERRAL
PARTNER_CO_MARKETING
CALL_CENTER
OFFLINE
PUBLIC_RELATIONS
OTHER
```

---

# 9. Candidate Campaign Objective vocabulary — pending validation

```text
REACH
AWARENESS
ENGAGEMENT
TRAFFIC
FORM_SUBMISSION
CALL
CHAT
LEAD_CREATED
QUALIFIED_LEAD
CUSTOMER_CREATED
REQUIREMENT_CREATED
APPOINTMENT_BOOKED
SITE_VISIT_COMPLETED
SHORTLIST_CREATED
PROPOSAL_SENT
DEAL_CREATED
HOLD_ACTIVATED
BOOKING_CREATED
DEPOSIT_CONFIRMED
CONTRACT_SIGNED
CONTRACT_EFFECTIVE
REVENUE_RECOGNIZED
REVENUE_COLLECTED
SELLER_MANDATE_SIGNED
LISTING_ACTIVATED
CUSTOM
```

Một Campaign có:

* Primary Objective.
* Secondary Objectives.
* Guardrail Metrics.

---

# 10. Candidate Campaign lifecycle — pending validation

```text
DRAFT
PLANNING
PENDING_CONTENT
PENDING_BUDGET
PENDING_REVIEW
PENDING_APPROVAL
APPROVED
SCHEDULED
ACTIVE
PAUSED
LIMITED
COMPLETED
CANCELLED
EXPIRED
ARCHIVED
REJECTED
```

## 10.1. ACTIVE

Chỉ được Active khi:

* Campaign Version approved.
* Budget hợp lệ nếu bắt buộc.
* Channel configured.
* Audience hợp lệ.
* Consent policy được resolve.
* Creative approved.
* Tracking configured.
* Start/end hợp lệ.
* User có quyền.

## 10.2. PAUSED

Không nhận thêm execution mới, nhưng:

* Delivery đang thực hiện có thể cần stop request.
* Existing Lead không bị xóa.
* Attribution lịch sử giữ nguyên.

---

# 11. Campaign Version

Mọi thay đổi quan trọng phải tạo version:

* Objective.
* Project.
* Audience.
* Budget.
* Channel.
* Tracking.
* Conversion goals.
* Attribution model.
* Consent purpose.
* Creative strategy.
* Start/end.
* Vendor.

Campaign Version đã Active không sửa trực tiếp.

Có thể thay bằng version mới với effective date.

---

# 12. Candidate Campaign Scope vocabulary — pending validation

Campaign có thể áp dụng theo:

```text
ENTERPRISE
LEGAL_ENTITY
BRANCH
REGION
PROJECT
SALES_LAUNCH
TRANSACTION_MODEL
PROPERTY_TYPE
CUSTOMER_SEGMENT
PARTNER
CHANNEL
```

Project Campaign không tự cấp Project Access cho người dùng.

---

# 13. Candidate Campaign commercial-context vocabulary — pending validation

Campaign phải xác định mục đích thương mại:

```text
BUY_SIDE_ACQUISITION
SELL_SIDE_ACQUISITION
OWNER_CONSIGNMENT
PRIMARY_PROJECT_SALE
SECONDARY_RESALE
COMPANY_ASSET_SALE
RENTAL
PARTNER_ACQUISITION
GENERAL_BRAND
```

Điều này giúp tránh dùng chung một source không rõ ý nghĩa.

---

# 14. Campaign Flight

Campaign Flight là một khoảng chạy cụ thể:

* Start/end.
* Timezone.
* Channel.
* Budget.
* Audience Version.
* Creative Version.
* Bid/optimization reference.
* Status.

Một Campaign có nhiều Flight:

* Teaser.
* Launch.
* Retargeting.
* Extension.

---

# 15. Candidate Campaign Channel vocabulary — pending validation

Các channel chuẩn:

```text
FACEBOOK_ADS
INSTAGRAM_ADS
GOOGLE_SEARCH_ADS
GOOGLE_DISPLAY
YOUTUBE
TIKTOK_ADS
LINKEDIN
ZALO_ADS
EMAIL
SMS
ZALO_MESSAGE
WHATSAPP
MESSENGER
WEB_PUSH
IN_APP
WEBSITE
SEO
ORGANIC_SOCIAL
CALL_CENTER
REFERRAL
PARTNER
EVENT
OUTDOOR
PRINT
RADIO
TELEVISION
DIRECT_MAIL
WALK_IN
BROKER_NETWORK
OTHER
```

Channel dictionary có thể mở rộng nhưng canonical group phải ổn định.

---

# 16. Source Taxonomy

Phải tách:

* `source`.
* `source_group`.
* `medium`.
* `channel`.
* `campaign`.
* `placement`.
* `ad_group/ad_set`.
* `ad`.
* `creative`.
* `keyword`.
* `landing_page`.
* `referrer`.
* `partner`.
* `offline_source`.

Ví dụ:

```text
source       = facebook
medium       = paid_social
campaign     = project_a_launch
ad_set       = investors_hanoi
ad           = video_01
creative     = creative_version_3
landing_page = project_a_lp_02
```

---

# 17. Candidate canonical Source Group vocabulary — pending validation

```text
PAID_SEARCH
PAID_SOCIAL
PAID_DISPLAY
PAID_VIDEO
ORGANIC_SEARCH
ORGANIC_SOCIAL
DIRECT
REFERRAL
PARTNER
EMAIL
MESSAGING
CALL_CENTER
EVENT
OFFLINE
BROKER_NETWORK
CUSTOMER_REFERRAL
EMPLOYEE_REFERRAL
UNKNOWN
OTHER
```

---

# 18. Source Normalization

Raw source từ provider phải được map sang canonical taxonomy.

Ví dụ:

* `fb`.
* `facebook`.
* `Facebook Ads`.
* `meta`.
* `instagram`.

có thể map về:

```text
source_group = PAID_SOCIAL
source = META
```

Mapping phải có:

* Rule.
* Priority.
* Effective dates.
* Version.
* Test.
* Audit.

---

# 19. UTM Management

Capability hỗ trợ:

* `utm_source`.
* `utm_medium`.
* `utm_campaign`.
* `utm_id`.
* `utm_content`.
* `utm_term`.
* Custom parameters.

## 19.1. UTM Registry

Cho phép:

* Tạo UTM chuẩn.
* Chống trùng.
* Validate naming.
* Sinh tracking URL.
* Sinh QR.
* Lock Campaign ID.

## 19.2. Raw và normalized value

Phải giữ cả:

* Raw received.
* Normalized value.
* Mapping rule.
* Confidence.

Không ghi đè raw data.

---

# 20. Candidate Tracking Code vocabulary — pending validation

Các loại:

```text
TRACKING_URL
QR_CODE
FORM_CODE
CALL_TRACKING_NUMBER
COUPON_CODE
EVENT_CODE
REFERRAL_CODE
PARTNER_CODE
OFFLINE_CODE
PIXEL_EVENT_REFERENCE
```

Tracking Code phải:

* Unique theo scope.
* Có effective dates.
* Có owner.
* Có Campaign/Flight.
* Có audit.

---

# 21. Offline Source

Offline Campaign có thể dùng:

* QR code.
* Unique hotline.
* Event code.
* Coupon.
* Staff source code.
* Booth code.
* Walk-in source.
* Manual source có approval.

Manual source correction phải có reason.

---

# 22. Lead Capture

Lead có thể được capture từ:

* Website form.
* Landing page.
* Lead Ads.
* Chat.
* Phone call.
* Missed call.
* Email inbound.
* Event registration.
* Event check-in.
* QR.
* Referral.
* Partner file.
* Offline staff entry.
* API.
* Import.
* Existing Customer re-engagement.

Marketing Capability tạo Marketing Submission hoặc Capture Event, sau đó gửi idempotent Lead intake command tới Lead Context.

---

# 23. Form Submission

Form Submission lưu:

* Form.
* Form Version.
* Campaign.
* Flight.
* Landing Page.
* Raw fields.
* Normalized fields.
* Consent fields.
* Tracking parameters.
* IP coarse metadata nếu policy.
* Device/session reference.
* Submission time.
* Spam score.
* Validation.
* Idempotency key.
* Processing status.
* Lead reference.
* Customer reference sau resolution.

Raw payload phải được bảo vệ và retention theo policy.

---

# 24. Form Definition

Form gồm:

* Form code.
* Purpose.
* Project.
* Fields.
* Required fields.
* Validation.
* Consent text.
* Privacy notice version.
* Hidden tracking fields.
* Routing rule.
* Thank-you action.
* Duplicate policy.
* Effective dates.
* Version.

Form active không sửa trực tiếp.

---

# 25. Form Field Mapping

Mapping có thể đến:

* Lead field.
* Customer identity input.
* Requirement field.
* Consent record.
* Campaign metadata.
* Custom attribute.

Form không được ghi trực tiếp vào sensitive Customer fields khi chưa qua validation.

---

# 26. Candidate Submission validation lifecycle — pending validation

Các signal:

* Bot score.
* Duplicate rapid submissions.
* Invalid phone.
* Disposable email.
* Impossible field combinations.
* Rate limit.
* Blacklisted source.
* Provider fraud signal.

Status:

```text
VALID
PENDING_VALIDATION
SPAM_SUSPECTED
SPAM_CONFIRMED
INVALID
DUPLICATE
TEST
IGNORED
```

Spam không được xóa raw audit trái retention policy.

---

# 27. Marketing Touchpoint

Touchpoint là một lần tiếp xúc có ý nghĩa giữa identity và Marketing.

Ví dụ:

* Ad impression.
* Ad click.
* Landing page visit.
* Form view.
* Form submit.
* Email delivered.
* Email click.
* Message reply.
* Event registration.
* Event attendance.
* Call.
* QR scan.
* Organic content engagement.

---

# 28. Candidate Touchpoint Event vocabulary — pending validation

```text
IMPRESSION
VIEW
CLICK
LANDING_PAGE_VISIT
FORM_VIEW
FORM_STARTED
FORM_SUBMITTED
CALL_INITIATED
CALL_CONNECTED
CHAT_STARTED
MESSAGE_SENT
MESSAGE_DELIVERED
MESSAGE_READ
MESSAGE_CLICKED
MESSAGE_REPLIED
EMAIL_OPENED
EMAIL_CLICKED
EVENT_REGISTERED
EVENT_ATTENDED
QR_SCANNED
CONTENT_DOWNLOADED
VIDEO_VIEWED
SOCIAL_ENGAGED
REFERRAL_SUBMITTED
LEAD_CREATED
CUSTOM
```

---

# 29. Touchpoint Quality

Mỗi Touchpoint có:

* Source confidence.
* Identity confidence.
* Bot/fraud score.
* Engagement quality.
* Duration nếu có.
* Human verified.
* Provider verified.
* Attribution eligibility.

Không phải mọi impression đều đủ chất lượng cho attribution.

---

# 30. Anonymous Visitor

Anonymous Visitor Profile có thể dựa trên:

* First-party cookie reference.
* Device/session identifier.
* Analytics client ID.
* Hashed provider ID.
* Anonymous chat ID.
* Call tracking session.

Không lưu fingerprint xâm phạm ngoài policy.

---

# 31. Anonymous-to-Known Resolution

Khi visitor cung cấp:

* Phone.
* Email.
* Login.
* Form.
* Chat identity.
* Call.

hệ thống có thể link anonymous history với Party/Lead/Customer.

Phải lưu:

* Resolution method.
* Confidence.
* Evidence.
* Resolved at.
* Resolver.
* Reversible status.

Không merge identity chắc chắn chỉ dựa trên thiết bị dùng chung.

---

# 32. Shared Device và Shared Contact

Không được tự nối toàn bộ Touchpoint khi:

* Thiết bị dùng chung.
* Shared phone.
* Family email.
* Office phone.
* Public computer.

Phải dùng identity confidence và shared identity rules từ Customer Identity Governance Capability.

---

# 33. Candidate Marketing Identity Link vocabulary — pending validation

Các loại:

```text
ANONYMOUS_TO_LEAD
ANONYMOUS_TO_PARTY
LEAD_TO_CUSTOMER
EMAIL_TO_PARTY
PHONE_TO_PARTY
PLATFORM_PROFILE_TO_PARTY
REFERRAL_CODE_TO_PARTY
CALL_SESSION_TO_LEAD
```

Link phải có:

* Confidence.
* Method.
* Effective time.
* Source.
* Review status.
* Merge redirect behavior.

---

# 34. Consent Architecture

Marketing phải sử dụng canonical consent/contact-restriction contracts từ Party Context và execution/contact facts từ Activity Context.

Consent cần phân biệt:

* Purpose.
* Channel.
* Legal Entity/Brand.
* Scope.
* Source.
* Collected at.
* Text/version.
* Effective dates.
* Withdrawn at.

---

# 35. Candidate Marketing Purpose vocabulary — pending validation

```text
GENERAL_MARKETING
PROJECT_INFORMATION
PRODUCT_RECOMMENDATION
EVENT_INVITATION
PROMOTION
CUSTOMER_REACTIVATION
SELLER_ACQUISITION
OWNER_CONSIGNMENT
PARTNER_MARKETING
SERVICE_UPDATE
TRANSACTIONAL_COMMUNICATION
RESEARCH
CUSTOM
```

Transactional Communication không được dùng để lách Marketing consent.

---

# 36. Consent Gate

Trước enrollment hoặc outbound action phải kiểm tra:

```text
Consent Purpose
∩ Channel Permission
∩ Brand/Legal Entity Scope
∩ Contact Restriction
∩ Quiet Hours
∩ Frequency Cap
∩ Suppression Policy
∩ Data Retention
```

Nếu không đạt:

* Không gửi.
* Ghi suppression reason.
* Không chuyển sang channel khác tùy ý.
* Có thể tạo Task review nếu phù hợp.

---

# 37. Candidate Marketing Suppression vocabulary — pending validation

Các loại suppression:

```text
GLOBAL_DO_NOT_CONTACT
CHANNEL_OPT_OUT
PURPOSE_OPT_OUT
LEGAL_HOLD
COMPLAINT_OPEN
FRAUD_OR_SPAM
EMPLOYEE_TEST
COMPETITOR
INVALID_CONTACT
HARD_BOUNCE
UNSUBSCRIBED
ACTIVE_TRANSACTION_EXCLUSION
RECENTLY_CONTACTED
FREQUENCY_LIMIT
CUSTOM
```

Suppression có:

* Scope.
* Reason.
* Source.
* Effective dates.
* Priority.
* Overridable hay không.
* Approver nếu override.

---

# 38. Hard Suppression và Soft Suppression

## 38.1. Hard Suppression

Không được override bằng Campaign user thông thường:

* Global do-not-contact.
* Legal restriction.
* Hard bounce.
* Invalid destination.
* Confirmed spam complaint.

## 38.2. Soft Suppression

Có thể được override theo policy:

* Recently contacted.
* Active Deal.
* Current Campaign overlap.
* Temporary frequency limit.
* Customer service case.

---

# 39. Frequency Cap

Frequency Cap có thể áp dụng theo:

* Customer.
* Party.
* Phone.
* Email.
* Device.
* Channel.
* Campaign.
* Brand.
* Enterprise.
* Rolling time window.

Ví dụ:

* Tối đa 2 cuộc gọi Marketing/ngày.
* Tối đa 3 SMS/tuần.
* Tối đa 5 Marketing messages/7 ngày.
* Không gửi hai Campaign cùng Project trong 24 giờ.

---

# 40. Contact Fatigue Score

Có thể tính từ:

* Số outbound.
* Số lần không phản hồi.
* Bounce.
* Unsubscribe.
* Complaint.
* Dismissal.
* No-show.
* Channel overlap.

Score chỉ hỗ trợ suppression/optimization, không được suy diễn thuộc tính nhạy cảm.

---

# 41. Audience

Audience là tập hợp đối tượng được xác định để phân tích hoặc kích hoạt Campaign.

Audience có thể gồm:

* Customer.
* Party.
* Lead.
* Anonymous Visitor.
* Partner.
* Owner.
* Seller.
* Buyer.
* Investor prospect.

---

# 42. Candidate Audience Type vocabulary — pending validation

```text
STATIC_LIST
DYNAMIC_SEGMENT
EVENT_BASED
LOOKALIKE_SEED
RETARGETING
SUPPRESSION
CONTROL_GROUP
EXPERIMENT_GROUP
PARTNER_PROVIDED
IMPORTED
CUSTOM
```

---

# 43. Audience Definition

Audience Definition có thể dùng:

* Demographic data được phép.
* Customer role.
* Requirement.
* Project interest.
* Listing interest.
* Budget range.
* Geographic preference.
* Interaction behavior.
* Lead stage.
* Deal stage.
* Contract status.
* Revenue segment.
* Last contact.
* Consent.
* Channel availability.
* Campaign history.
* Exclusion rules.

Không được dùng thuộc tính nhạy cảm trái policy.

---

# 44. Audience Rule Group

Hỗ trợ:

* AND.
* OR.
* NOT.
* Nested groups.
* Time-window condition.
* Event count.
* Aggregation.
* Exists/not exists.
* Threshold.

Ví dụ:

```text
Customer role = BUYER
AND Requirement status = ACTIVE
AND Project interest includes Project A
AND Last marketing contact > 7 days
AND Consent EMAIL = ACTIVE
NOT Contract status = EFFECTIVE for Project A
```

---

# 45. Audience Version

Mỗi thay đổi rule phải tạo version:

* Criteria.
* Exclusions.
* Consent purpose.
* Channel.
* Source fields.
* Evaluation time.
* Effective dates.
* Approval.

Audience Version đã được dùng cho Campaign Execution không sửa trực tiếp.

---

# 46. Audience Snapshot

Khi Campaign/Flight chạy phải snapshot membership:

* Audience Version.
* Evaluation timestamp.
* Member identity.
* Eligibility result.
* Consent result.
* Suppression result.
* Membership reason.
* Exclusion reason.
* Data snapshot reference.

Audience snapshot giúp tái tạo chính xác ai đã đủ điều kiện tại thời điểm kích hoạt.

---

# 47. Dynamic Audience

Dynamic Audience được đánh giá lại theo:

* Real-time event.
* Scheduled batch.
* Daily.
* Hourly.
* Before activation.
* Before every send.

Phải xác định:

* Entry policy.
* Exit policy.
* Re-entry policy.
* Cooldown.
* Snapshot policy.

---

# 48. Static Audience Import

Import phải kiểm tra:

* File format.
* Source.
* Consent evidence.
* Identity resolution.
* Duplicate.
* Shared phone.
* Invalid contact.
* Suppression.
* Legal Entity.
* Retention.

Không được coi danh sách mua ngoài là consent hợp lệ chỉ vì được import.

---

# 49. Audience Exclusion

Exclusion có thể gồm:

* Customer có Contract cùng Project.
* Customer đang có Booking.
* Customer đang Refund/Dispute.
* Customer đã mua.
* Customer vừa được sale liên hệ.
* Customer không có consent.
* Customer ngoài geographic scope.
* Customer là employee/test.
* Customer đang trong Control Group.

---

# 50. Audience Overlap

Hệ thống phải phân tích overlap giữa:

* Campaign.
* Audience.
* Project.
* Channel.
* Time window.

Cảnh báo khi cùng Customer sẽ nhận nhiều thông điệp gần nhau.

---

# 51. Audience Activation

Audience có thể được kích hoạt đến:

* Email provider.
* SMS provider.
* Zalo provider.
* Ad platform custom audience.
* Call center queue.
* Event invitation.
* Internal sales task.

Activation phải có:

* Audience snapshot.
* Destination.
* Hashing policy.
* Consent.
* Suppression.
* Sync status.
* Removal policy.
* Audit.

---

# 52. Ad Platform Custom Audience

Khi gửi dữ liệu sang ad platform:

* Chỉ gửi field được phép.
* Có hashing đúng policy.
* Không gửi raw sensitive data không cần thiết.
* Lưu platform audience ID.
* Lưu sync count.
* Lưu rejected records.
* Hỗ trợ removal khi consent withdrawn theo policy.

---

# 53. Marketing Journey

Journey là quy trình nhiều bước điều phối Customer/Lead qua thời gian.

Ví dụ:

```text
Lead Created
→ Wait 15 minutes
→ Gửi email giới thiệu
→ Nếu click
   → Tạo Task gọi trong 4 giờ
→ Nếu không click sau 2 ngày
   → Gửi message khác
→ Nếu Deal created
   → Exit Journey
```

---

# 54. Candidate Journey Type vocabulary — pending validation

```text
LEAD_NURTURE
PROJECT_NURTURE
EVENT_NURTURE
REACTIVATION
SELLER_ACQUISITION
OWNER_NURTURE
POST_SITE_VISIT
POST_PROPOSAL
BOOKING_REMINDER
CUSTOMER_EDUCATION
CROSS_SELL
REFERRAL
CUSTOM
```

Journey không được dùng thay workflow giao dịch của Transaction, Contract and Revenue Contexts.

---

# 55. Candidate Automation Trigger vocabulary — pending validation

Các trigger:

```text
SCHEDULE
AUDIENCE_ENTRY
FORM_SUBMITTED
LEAD_CREATED
LEAD_STATUS_CHANGED
CUSTOMER_CREATED
REQUIREMENT_CREATED
INTERACTION_RECEIVED
EMAIL_CLICKED
MESSAGE_REPLIED
APPOINTMENT_COMPLETED
SITE_VISIT_COMPLETED
MATCH_RESULT_CREATED
SHORTLIST_CREATED
PROPOSAL_SENT
PROPOSAL_VIEWED
DEAL_STAGE_CHANGED
HOLD_EXPIRING
BOOKING_CREATED
DEPOSIT_CONFIRMED
CONTRACT_SIGNED
CONTRACT_CANCELLED
RECEIVABLE_OVERDUE
REVENUE_RECOGNIZED
CUSTOM_EVENT
```

Trigger phải đến từ domain event có schema/version.

---

# 56. Candidate Automation Node vocabulary — pending validation

Các node chuẩn:

```text
START
WAIT
WAIT_UNTIL
CONDITION
BRANCH
SPLIT
RANDOM_SPLIT
CONTROL_GROUP
SEND_EMAIL
SEND_SMS
SEND_MESSAGE
CREATE_TASK
ASSIGN_QUEUE
ADD_TO_AUDIENCE
REMOVE_FROM_AUDIENCE
UPDATE_MARKETING_ATTRIBUTE
REQUEST_SOURCE_MODULE_ACTION
WEBHOOK
NOTIFY_INTERNAL
GOAL_CHECK
EXIT
```

Không cho custom code tùy ý trong production rule.

---

# 57. Request Source Capability Action

Automation muốn tạo:

* Lead.
* Requirement review.
* Matching Run.
* Proposal Task.
* Appointment.

phải gọi API capability nguồn.

Không ghi trực tiếp database của capability khác.

---

# 58. Wait Node

Wait có thể theo:

* Duration.
* Business duration.
* Fixed datetime.
* Customer timezone.
* Event.
* Condition.
* Until next allowed contact window.

Wait phải có:

* Timeout.
* Resume condition.
* Cancellation behavior.
* Version.

---

# 59. Branch Condition

Có thể dựa trên:

* Consent.
* Interaction.
* Message status.
* Lead stage.
* Deal stage.
* Project interest.
* Appointment outcome.
* Contract status.
* Audience membership.
* Custom safe expression.

Expression phải sandbox và validate.

---

# 60. Journey Enrollment

Enrollment phải lưu:

* Journey Version.
* Entity.
* Entry trigger.
* Audience snapshot.
* Consent snapshot.
* Suppression result.
* Entry time.
* Current node.
* Status.
* Re-entry count.

---

# 61. Candidate Journey Enrollment lifecycle — pending validation

```text
PENDING
ACTIVE
WAITING
PAUSED
GOAL_REACHED
EXITED
SUPPRESSED
CANCELLED
FAILED
EXPIRED
COMPLETED
```

---

# 62. Candidate Journey Re-entry policy vocabulary — pending validation

Policy:

```text
NEVER
AFTER_EXIT
AFTER_COOLDOWN
ON_NEW_CONTEXT
ON_NEW_PROJECT
LIMITED_COUNT
ALWAYS
```

Re-entry không được tạo message trùng trái Frequency Cap.

---

# 63. Journey Exit Criteria

Ví dụ:

* Lead converted.
* Deal created.
* Booking created.
* Contract signed.
* Consent withdrawn.
* Customer bought.
* Complaint opened.
* Campaign ended.
* Journey goal reached.
* Manual exit.

---

# 64. Journey Safety

Phải chặn:

* Infinite loop.
* Excessive node execution.
* Message burst.
* Re-entry storm.
* Cross-journey duplication.
* Webhook replay.
* Outbound after opt-out.
* Task explosion.
* Stale enrollment.

---

# 65. Automation Version

Journey/Automation active không sửa trực tiếp.

Version mới phải xác định:

* Enrollment mới dùng version nào.
* Enrollment cũ tiếp tục version cũ hay migrate.
* Migration approval.
* Impact simulation.

---

# 66. Automation Simulation

Trước activation phải có thể mô phỏng:

* Số audience.
* Số messages.
* Estimated suppression.
* Estimated Tasks.
* Estimated cost.
* Journey duration.
* Potential overlap.
* Risk.
* Sample path.

Simulation không gửi dữ liệu thật.

---

# 67. Automation Idempotency

Mỗi execution phải có khóa dựa trên:

* Journey.
* Version.
* Enrollment.
* Node.
* Trigger event.
* Execution attempt.

Webhook/event lặp không tạo:

* Message trùng.
* Task trùng.
* Audience enrollment trùng.
* Lead trùng.

---

# 68. Automation Retry

Retry policy gồm:

* Maximum attempts.
* Backoff.
* Retryable errors.
* Non-retryable errors.
* Dead-letter queue.
* Manual replay.
* Idempotency.

---

# 69. Marketing Message

Marketing Message là yêu cầu truyền thông do Campaign/Journey tạo.

Outbound intent được chuyển tới Activity Context; provider transport đi qua Integration Context.

Message phải có:

* Campaign.
* Journey.
* Audience member.
* Channel.
* Template Version.
* Sender.
* Purpose.
* Consent snapshot.
* Scheduled time.
* Frequency result.
* Status.
* Interaction reference.

---

# 70. Candidate Marketing Message lifecycle — pending validation

```text
DRAFT
PENDING_ELIGIBILITY
SUPPRESSED
QUEUED
SCHEDULED
SENT
DELIVERED
READ
CLICKED
REPLIED
BOUNCED
FAILED
CANCELLED
EXPIRED
COMPLAINT
UNSUBSCRIBED
```

---

# 71. Template và Content Asset

Content Asset có thể là:

* Email.
* SMS.
* Zalo template.
* Ad copy.
* Image.
* Video.
* Landing Page copy.
* Call script.
* Event invitation.
* Brochure.
* PDF.
* Social post.

Marketing lưu business metadata và Document references; Documents Context sở hữu binary artifacts.

---

# 72. Content Version

Mỗi version lưu:

* Headline.
* Body.
* CTA.
* Media references.
* Language.
* Project.
* Legal disclaimers.
* Personalization fields.
* Approval.
* Effective dates.
* Rights expiry.

Content đã sử dụng không sửa trực tiếp.

---

# 73. Content Approval

Có thể cần:

* Brand review.
* Project review.
* Legal review.
* Compliance review.
* Sales review.
* Director approval.

Approval dựa trên:

* Channel.
* Project.
* Claim type.
* Pricing statement.
* Financial promise.
* Legal status statement.
* Personalization.

---

# 74. Dynamic Personalization

Có thể dùng:

* Customer name.
* Project interest.
* Preferred location.
* Sale contact.
* Appointment time.
* Approved Listing information.

Không được dùng:

* Sensitive financial detail ngoài purpose.
* Unverified information.
* Floor Price.
* Internal commission.
* Private owner information.

---

# 75. Content Rendering Snapshot

Khi gửi phải lưu:

* Template Version.
* Personalization input.
* Rendered content hash.
* Language.
* CTA URL.
* Tracking parameters.
* Disclaimer version.

Không cần lưu toàn văn nếu policy dùng external reference, nhưng phải tái tạo được khi cần audit.

---

# 76. Landing Page

Landing Page metadata gồm:

* URL.
* Domain.
* Campaign.
* Project.
* Version.
* Form.
* Tracking.
* Consent notice.
* Status.
* Publish time.
* External CMS reference.

---

# 77. Landing Page Conversion

Có thể đo:

* Visit.
* Engaged visit.
* CTA click.
* Form started.
* Form submitted.
* Call initiated.
* Chat started.
* Event registration.

Conversion phải chống bot và duplicate.

---

# 78. Event Marketing

Event có thể là:

* Launch.
* Open house.
* Site visit.
* Webinar.
* Seminar.
* Investor event.
* Partner event.
* Owner acquisition event.

Event Campaign không thay Appointment cá nhân của Activity and Engagement Capability.

---

# 79. Event Registration

Lưu:

* Event.
* Participant.
* Registration source.
* Campaign.
* Consent.
* Ticket/code.
* Attendance.
* Check-in.
* Lead reference.
* Customer reference.
* Follow-up status.

---

# 80. Event Attendance

Attendance có thể tạo:

* Interaction.
* Timeline Event.
* Lead score signal.
* Follow-up Task.
* Journey branch.

Không tự tạo Deal chỉ vì tham dự.

---

# 81. Referral Campaign

Referral Campaign phải hỗ trợ:

* Referrer Party.
* Referral code.
* Referred contact.
* Consent/permission.
* Campaign.
* Qualified criteria.
* Reward eligibility reference.
* Duplicate control.

Referral reward tài chính thuộc Revenue and Commission Capability nếu là fee/commission.

---

# 82. Partner Co-Marketing

Phải xác định:

* Partner.
* Data ownership.
* Consent responsibility.
* Cost sharing.
* Lead routing.
* Attribution.
* Branding.
* Reporting.
* Data retention.
* Agreement reference.

Partner upload không được tự mở Customer data ngoài scope.

---

# 83. Call Tracking

Call Tracking Number có thể gắn:

* Campaign.
* Channel.
* Placement.
* Landing Page.
* Project.
* Flight.

Khi gọi vào:

* Activity and Engagement Capability tạo Call Log.
* Marketing Capability gắn source.
* Lead Management Capability tạo Lead nếu cần.
* Customer Identity Governance Capability resolve Phone Identity.

---

# 84. Lead Source Snapshot

Khi Lead Management Capability tạo Lead phải nhận snapshot:

* First known touch.
* Lead-creation touch.
* Source group.
* Source.
* Medium.
* Campaign.
* Flight.
* Placement.
* Ad.
* Creative.
* Keyword.
* Landing Page.
* Referral.
* Raw tracking.
* Normalization rule version.
* Capture time.
* Identity confidence.

Snapshot không sửa vì Campaign mới xuất hiện sau này.

---

# 85. Source Correction

Chỉ cho phép khi:

* Mapping sai.
* Tracking lỗi.
* Import lỗi.
* Duplicate provider data.
* Manual entry sai.

Correction phải:

* Giữ original source.
* Tạo correction.
* Reason.
* Evidence.
* Approval.
* Recalculate reports có version.
* Không tự thay sales attribution.

---

# 86. Candidate Touchpoint Attribution Eligibility vocabulary — pending validation

Mỗi Touchpoint có thể được đánh dấu:

```text
ELIGIBLE
INELIGIBLE
SUSPICIOUS
DUPLICATE
OUTSIDE_WINDOW
POST_CONVERSION
INTERNAL_TEST
SUPPRESSED
```

Chỉ eligible Touchpoint tham gia attribution.

---

# 87. Candidate Attribution Milestone vocabulary — pending validation

Các milestone chuẩn:

```text
LEAD_CREATED
LEAD_QUALIFIED
CUSTOMER_CREATED
REQUIREMENT_CREATED
APPOINTMENT_BOOKED
SITE_VISIT_COMPLETED
SHORTLIST_CREATED
DEAL_CREATED
PROPOSAL_SENT
HOLD_ACTIVATED
BOOKING_CREATED
DEPOSIT_CONFIRMED
CONTRACT_SIGNED
CONTRACT_EFFECTIVE
REVENUE_RECOGNIZED
REVENUE_COLLECTED
SELLER_MANDATE_SIGNED
LISTING_ACTIVATED
```

---

# 88. Candidate Attribution Model vocabulary — pending validation

```text
FIRST_TOUCH
LEAD_CREATION_TOUCH
LAST_TOUCH
LAST_NON_DIRECT_TOUCH
LINEAR
TIME_DECAY
POSITION_BASED
U_SHAPED
W_SHAPED
FULL_PATH
CUSTOM_RULE_BASED
DATA_DRIVEN_REFERENCE
CONTROLLED_MANUAL
```

---

# 89. First-Touch Attribution

Gán 100% credit cho Touchpoint eligible đầu tiên trong identity path.

Phải xác định:

* Lookback window.
* Identity confidence.
* Direct handling.
* Anonymous linking.

---

# 90. Lead-Creation Attribution

Gán credit cho Touchpoint làm phát sinh Lead Capture.

Đây thường là nguồn Lead chính được snapshot ở Lead Management Capability.

---

# 91. Last-Touch Attribution

Gán credit cho Touchpoint eligible cuối trước conversion.

Không mặc định ghi đè first source.

---

# 92. Last Non-Direct Attribution

Bỏ qua Direct nếu có Touchpoint Marketing hợp lệ trong lookback window.

Direct definition phải cấu hình rõ.

---

# 93. Linear Attribution

Chia đều credit cho tất cả Touchpoint eligible.

Cần chống:

* Nhiều impression vô nghĩa.
* Duplicate event.
* Message retries.
* Bot activity.

---

# 94. Time-Decay Attribution

Touchpoint gần conversion hơn nhận credit cao hơn.

Phải lưu:

* Half-life.
* Window.
* Formula.
* Model version.

---

# 95. Illustrative Position-Based Attribution — không phải production weights

Ví dụ:

* First touch: 40%.
* Lead creation: 20%.
* Last touch: 40%.

Hoặc U-shaped/W-shaped theo policy.

---

# 96. Custom Attribution

Custom rule có thể dựa trên:

* Channel.
* Campaign.
* Touchpoint quality.
* Conversion stage.
* Identity confidence.
* Project.
* Offline validation.

Formula phải:

* Deterministic.
* Versioned.
* Simulatable.
* Không chạy mã tùy ý.
* Tổng credit bằng 100% trong tolerance.

---

# 97. Attribution Window policy inputs — không phải production defaults

Cấu hình theo:

* Conversion type.
* Channel.
* Project.
* Campaign.
* Touchpoint type.

Ví dụ:

* Lead: 30 ngày.
* Booking: 90 ngày.
* Contract: 180 ngày.
* Revenue: kế thừa Contract attribution hoặc model riêng.

Không dùng một window duy nhất cho mọi milestone.

---

# 98. Direct Touchpoint

Direct có thể là:

* Gõ URL trực tiếp.
* Bookmark.
* Không có referrer.
* Unknown inbound.

Không được tự coi mọi unknown source là Direct nếu tracking bị lỗi.

---

# 99. Offline Attribution

Offline Touchpoint cần:

* Event check-in.
* Call tracking.
* QR.
* Referral code.
* Staff source code.
* Evidence.
* Confidence.

Manual “Campaign influenced” phải có authority và reason.

---

# 100. Campaign Sourced và Campaign Influenced

## 100.1. Marketing-Sourced

Campaign nhận source credit theo model đã chọn.

Ví dụ:

* First Touch.
* Lead Creation Touch.

## 100.2. Marketing-Influenced

Campaign có ít nhất một eligible Touchpoint trong attribution window trước conversion.

Influenced Revenue không được cộng dồn đơn giản giữa nhiều Campaign như doanh thu độc lập.

---

# 101. Deal Attribution

Khi Deal được tạo, Marketing Capability tạo snapshot:

* First touch.
* Lead source.
* Last eligible touch.
* Influencing Campaigns.
* Attribution Model.
* Credit allocation.
* Lookback window.
* Calculation time.

Deal attribution không đổi primary sale.

---

# 102. Contract Attribution

Khi Contract đạt milestone:

* Lấy identity path.
* Loại Touchpoint sau cut-off.
* Áp model/version.
* Snapshot Campaign credit.
* Lưu Contract Version.
* Lưu Contract value basis.

Contract amendment có thể yêu cầu recalculation delta nhưng không xóa snapshot cũ.

---

# 103. Revenue Attribution

Revenue Attribution có thể dựa trên:

* Contract attribution.
* Revenue Entitlement source.
* Revenue Recognition milestone.
* Revenue collected milestone.

Phải phân biệt:

```text
ATTRIBUTED_CONTRACT_VALUE
ATTRIBUTED_REVENUE_ENTITLEMENT
ATTRIBUTED_RECOGNIZED_REVENUE
ATTRIBUTED_COLLECTED_REVENUE
```

Gross Contract Value không được ghi nhãn là Revenue.

---

# 104. Revenue Reversal và Attribution

Khi Revenue bị reverse:

* Không xóa Attribution Result gốc.
* Tạo negative adjustment.
* Cập nhật net attributed revenue.
* Giữ historical gross.
* Gắn source event Revenue and Commission Capability.

---

# 105. Contract Cancellation và Attribution

Contract cancellation:

* Không xóa conversion lịch sử.
* Mark conversion reversed/cancelled.
* Tạo negative Contract/Revenue metric.
* Giữ Campaign influence.
* Tách gross conversion và net conversion.

---

# 106. Attribution Recalculation

Có thể cần khi:

* Identity merge.
* Source correction.
* Campaign mapping correction.
* Duplicate Touchpoint removal.
* Revenue adjustment.
* Model changed theo approved backfill.

Recalculation phải:

* Tạo run mới.
* Giữ result cũ.
* Nêu reason.
* So sánh delta.
* Có approval nếu ảnh hưởng báo cáo khóa.

---

# 107. Attribution Lock

Attribution Result có thể được khóa khi:

* Reporting period closed.
* Contract confirmed.
* Revenue period approved.
* Board reporting issued.

Late correction phải tạo adjustment period, không âm thầm viết lại.

---

# 108. Conversion Definition

Mỗi Conversion Definition có:

* Code.
* Source event.
* Qualifying conditions.
* Deduplication key.
* Value field.
* Currency.
* Reversal event.
* Attribution model.
* Window.
* Effective dates.
* Version.

---

# 109. Conversion Deduplication

Ví dụ:

* Một Lead chỉ tính một lần cho Campaign/milestone theo rule.
* Một Contract amendment không tạo Contract Conversion mới.
* Booking replacement có thể giữ conversion lineage.
* Webhook lặp không tạo conversion trùng.

---

# 110. Candidate Conversion lifecycle — pending validation

```text
PENDING_VALIDATION
VALID
REVERSED
CANCELLED
DUPLICATE
INVALID
ADJUSTED
DISPUTED
```

---

# 111. Candidate Marketing Funnel vocabulary — không phải certified funnel

Canonical funnel:

```text
REACH
ENGAGEMENT
VISIT
LEAD
VALID_LEAD
QUALIFIED_LEAD
CUSTOMER
REQUIREMENT
APPOINTMENT
SITE_VISIT
SHORTLIST
DEAL
PROPOSAL
HOLD
BOOKING
DEPOSIT
CONTRACT
REVENUE_RECOGNIZED
REVENUE_COLLECTED
```

Không bắt buộc mọi Campaign đi qua tất cả stage.

---

# 112. Lead Quality

Có thể đo:

* Valid contact.
* Duplicate rate.
* Spam rate.
* First response.
* Contactability.
* Qualification.
* Requirement completeness.
* Appointment.
* Deal.
* Booking.
* Contract.
* Revenue.

Không được chỉ đánh giá Campaign bằng số Lead.

---

# 113. Marketing Qualified Lead

MQL là Marketing classification/projection, không tự thay official Lead Status.

MQL có thể dựa trên:

* Form intent.
* Engagement.
* Project interest.
* Budget completeness.
* Behavior score.
* Event attendance.

Lead Context vẫn quyết định qualification, assignment và care protection.

---

# 114. Lead Scoring

Có thể gồm:

* Fit score.
* Intent score.
* Engagement score.
* Recency score.
* Data quality score.
* Negative score.

Không sử dụng thuộc tính nhạy cảm bị cấm hoặc không cần thiết.

Lead Score phải:

* Versioned.
* Explainable.
* Không tự tạo quyền chăm sóc.
* Không tự loại Customer khỏi dịch vụ quan trọng.

---

# 115. Behavioral Signal

Các signal:

* Landing page visits.
* Email clicks.
* Project content views.
* Site visit registration.
* Proposal view.
* Message reply.
* Event attendance.
* Repeated product interest.

Signal có expiry và decay.

---

# 116. Campaign Budget

Budget có thể theo:

* Campaign.
* Flight.
* Channel.
* Project.
* Legal Entity.
* Vendor.
* Period.
* Currency.

Budget không đồng nghĩa Spend thực tế.

---

# 117. Candidate Marketing Budget lifecycle — pending validation

```text
DRAFT
PENDING_APPROVAL
APPROVED
ACTIVE
PARTIALLY_COMMITTED
FULLY_COMMITTED
OVER_BUDGET
CLOSED
CANCELLED
```

---

# 118. Marketing Spend

Spend có thể từ:

* Ad platform.
* Vendor invoice reference.
* Agency fee.
* Creative production.
* Event cost.
* Software cost.
* Data cost.
* Call center cost.
* Sponsorship.
* Other.

Marketing Capability quản lý operational spend; hạch toán chính thức thuộc ERP.

---

# 119. Candidate Operational Spend lifecycle — pending validation

```text
ESTIMATED
PLANNED
COMMITTED
IMPORTED
VERIFIED
APPROVED
RECONCILED
DISPUTED
ADJUSTED
CANCELLED
```

---

# 120. Cost Allocation

Spend có thể phân bổ theo:

* Campaign.
* Channel.
* Flight.
* Creative.
* Project.
* Lead.
* Qualified Lead.
* Deal.
* Contract.

Chi phí chung có thể phân bổ theo rule:

* Impression.
* Click.
* Lead.
* Equal split.
* Revenue share.
* Manual approved.

---

# 121. Campaign Vendor và Agency

Lưu:

* Partner Party.
* Contract reference.
* Service scope.
* Cost model.
* Billing period.
* Campaign.
* Deliverable.
* KPI commitment.
* Data access.
* Status.
* Evaluation.

Không tự cấp Customer access cho agency.

---

# 122. Media Spend Integration

Import từ ad platform phải có:

* Platform account.
* Campaign ID.
* Ad Set ID.
* Ad ID.
* Date.
* Spend.
* Currency.
* Impressions.
* Clicks.
* Platform conversions.
* Payload hash.
* Import status.

Platform conversion không mặc định là CRM conversion.

---

# 123. Candidate KPI vocabulary — không phải Metric Registry canonical

Các KPI chuẩn:

```text
IMPRESSIONS
REACH
FREQUENCY
CLICKS
CTR
LANDING_PAGE_VISITS
FORM_STARTS
FORM_SUBMISSIONS
VALID_LEADS
QUALIFIED_LEADS
APPOINTMENTS
SITE_VISITS
DEALS
BOOKINGS
CONTRACTS
REVENUE
CPL
CPQL
CPA
CPD
CPB
CPCONTRACT
CAC
ROAS
ROMI
CONVERSION_RATE
DUPLICATE_RATE
SPAM_RATE
CONTACT_RATE
RESPONSE_RATE
UNSUBSCRIBE_RATE
COMPLAINT_RATE
```

---

# 124. Illustrative CPL and CPQL formulas — không phải certified Metric definitions

```text
CPL = Eligible Marketing Spend / Valid Leads
```

```text
CPQL = Eligible Marketing Spend / Qualified Leads
```

Phải xác định:

* Spend scope.
* Lead definition.
* Attribution model.
* Time period.
* Currency.
* Treatment of shared Campaign cost.

---

# 125. Illustrative acquisition-cost formulas — không phải certified Metric definitions

```text
CPD = Attributed Spend / Attributed Deals
```

```text
CPB = Attributed Spend / Attributed Bookings
```

```text
Cost per Contract = Attributed Spend / Valid Contracts
```

Contract cancelled có thể:

* Giữ gross metric.
* Loại khỏi net metric.

---

# 126. Customer Acquisition Cost

CAC phải định nghĩa rõ:

* Customer mới hoàn toàn.
* Customer mới theo Project.
* Customer tái kích hoạt.
* Contract Customer.
* Revenue Customer.

Không dùng một CAC duy nhất cho mọi báo cáo.

---

# 127. Illustrative ROAS expression — basis phải được chứng nhận

```text
ROAS
=
Attributed Commercial Value hoặc Revenue Metric
/
Paid Media Spend
```

Báo cáo phải ghi rõ numerator:

* Contract Value.
* Revenue Entitlement.
* Recognized Revenue.
* Collected Revenue.

Không ghi “ROAS” không có basis.

---

# 128. Illustrative ROMI expression — basis phải được chứng nhận

```text
ROMI
=
Attributed Revenue − Eligible Marketing Cost
/
Eligible Marketing Cost
```

Có thể dùng:

* Recognized Revenue.
* Collected Revenue.

Phải tách khỏi gross transaction value.

---

# 129. Pipeline Influence

Campaign có thể đo:

* Influenced Deal count.
* Influenced Deal value.
* Influenced Booking value.
* Influenced Contract value.
* Influenced Revenue.

Influenced metrics không được cộng dồn giữa Campaign như sourced metrics mà không cảnh báo double counting.

---

# 130. Funnel Cohort

Cohort có thể theo:

* Lead creation month.
* Campaign.
* First touch month.
* Project.
* Channel.
* Customer segment.
* Sale team.

Theo dõi conversion theo thời gian.

---

# 131. Time-to-Conversion

Đo:

* First Touch → Lead.
* Lead → Qualified.
* Lead → Appointment.
* Lead → Deal.
* Lead → Booking.
* Lead → Contract.
* Contract → Revenue.
* First Touch → Revenue.

Identity merge phải giữ lịch sử time path.

---

# 132. A/B Test

A/B Test có thể áp dụng:

* Creative.
* Subject.
* CTA.
* Landing Page.
* Form.
* Send time.
* Channel.
* Journey path.
* Offer presentation.

---

# 133. Candidate Experiment lifecycle — pending validation

```text
DRAFT
PENDING_REVIEW
APPROVED
SCHEDULED
RUNNING
PAUSED
COMPLETED
INCONCLUSIVE
CANCELLED
ARCHIVED
```

---

# 134. Experiment Assignment

Assignment phải:

* Deterministic nếu cần.
* Không đổi variant giữa phiên trái policy.
* Tôn trọng audience.
* Tôn trọng consent.
* Lưu assignment time.
* Chống contamination.

---

# 135. Control Group và Holdout

Control Group không nhận treatment nhưng:

* Vẫn phải đủ audience eligibility.
* Vẫn tuân thủ consent.
* Có thể không nhận message.
* Được dùng đo incremental lift.

Không đưa Customer vào control group nếu việc không gửi ảnh hưởng đến thông báo giao dịch bắt buộc.

---

# 136. Experiment Metric

Có thể gồm:

* Click.
* Form submission.
* Qualified Lead.
* Appointment.
* Booking.
* Contract.
* Revenue.

Phải định nghĩa:

* Primary metric.
* Guardrail.
* Attribution window.
* Sample.
* Stopping rule.

---

# 137. Experiment Integrity

Phải cảnh báo:

* Sample quá nhỏ.
* Variant imbalance.
* Audience leakage.
* Multiple exposure.
* Mid-test rule change.
* Tracking failure.
* Early stopping không đúng policy.

---

# 138. Marketing Calendar

Hiển thị:

* Campaign start/end.
* Flight.
* Content publication.
* Event.
* Email send.
* Audience activation.
* Experiment.
* Budget deadline.
* Reporting deadline.

Marketing Calendar không thay Google Calendar cá nhân của Activity and Engagement Capability.

---

# 139. Candidate Marketing user experience — không phải frontend contract canonical

Các khu vực:

1. Campaign Overview.
2. Objectives.
3. Projects và scope.
4. Flights.
5. Channels.
6. Audience.
7. Content.
8. Forms và Landing Pages.
9. Automation.
10. Touchpoints.
11. Leads.
12. Attribution.
13. Spend.
14. Conversions.
15. Experiments.
16. Timeline.
17. Audit.

---

# 140. Campaign List

Bộ lọc:

* Status.
* Type.
* Objective.
* Project.
* Legal Entity.
* Channel.
* Owner.
* Date.
* Budget.
* Spend.
* Lead volume.
* Contract count.
* Revenue.
* ROI.
* Agency.
* Audience.
* Experiment.

---

# 141. Campaign Detail

Hiển thị:

* Campaign code.
* Version.
* Objective.
* Owner.
* Project.
* Schedule.
* Audience.
* Consent purpose.
* Channels.
* Creative.
* Tracking.
* Budget.
* Spend.
* Funnel.
* Attribution.
* Revenue.
* Risks.
* Approval.
* Audit.

---

# 142. Audience Builder

Chức năng:

* Rule groups.
* Count estimate.
* Consent estimate.
* Suppression estimate.
* Overlap analysis.
* Sample preview có masking.
* Version compare.
* Save draft.
* Submit approval.
* Activate.
* Snapshot.

User không được xem full Customer details chỉ vì có quyền xây audience.

---

# 143. Journey Builder

Hiển thị:

* Trigger.
* Nodes.
* Conditions.
* Waits.
* Channels.
* Goals.
* Exit.
* Frequency gates.
* Error path.
* Simulation.
* Version.
* Activation status.

---

# 144. Attribution Workspace

Cho phép:

* Chọn conversion.
* Chọn model.
* Chọn window.
* Xem touch path.
* Xem credit.
* So sánh model.
* Xem correction.
* Xem identity confidence.
* Xem sourced/influenced.
* Export theo quyền.

---

# 145. Marketing Lead Inbox

Hiển thị Marketing submissions trước hoặc sau Lead processing:

* Raw source.
* Campaign.
* Form.
* Phone/email masked.
* Validation.
* Duplicate status.
* Lead link.
* Customer link.
* Routing status.
* Processing error.

Marketing Lead Inbox không thay Lead Queue Lead Management Capability.

---

# 146. Spend Workspace

* Budget.
* Planned.
* Committed.
* Imported spend.
* Verified spend.
* Vendor.
* Platform.
* Currency.
* Variance.
* Reconciliation.
* Cost allocation.

---

# 147. Dashboard cho Marketing Executive

* Campaign đang chạy.
* Spend hôm nay.
* Lead.
* Valid Lead.
* CPL.
* Qualified Lead.
* Conversion.
* Audience suppression.
* Delivery.
* Form issues.
* Tracking issues.
* Automation failures.

---

# 148. Dashboard cho Marketing Manager

* Budget versus Spend.
* Funnel theo Channel.
* Lead quality.
* Project performance.
* Audience overlap.
* Contact fatigue.
* Journey performance.
* Attribution.
* Contract và Revenue.
* Agency performance.
* Experiment results.

---

# 149. Dashboard cho Sales Manager

* Lead volume theo Campaign.
* Lead acceptance.
* First response.
* Contactability.
* Qualification.
* Appointment.
* Deal.
* Booking.
* Contract.
* Lead rejection reasons.
* Campaign-to-team performance.

Không cho Marketing dashboard thay đổi sale assignment.

---

# 150. Dashboard cho Director

* Marketing Spend.
* Valid Leads.
* Qualified Leads.
* Pipeline.
* Contract Value.
* Recognized Revenue.
* Collected Revenue.
* CAC.
* ROMI.
* ROAS basis.
* Project comparison.
* Channel comparison.
* Net conversion sau cancellation.
* Marketing-sourced Revenue.
* Marketing-influenced Revenue.
* Contact fatigue.
* Compliance and consent metrics.

---

# 151. Candidate analytical questions — không phải certified Metrics

> Exact grain, formulas, periods, attribution basis, snapshots, certification và access thuộc Analytics Context và Metric Registry.

## Campaign

* Campaign master.
* Campaign by status.
* Campaign by Project.
* Campaign by Legal Entity.
* Campaign by Channel.
* Campaign by Objective.
* Campaign budget.
* Campaign spend.
* Campaign variance.
* Campaign vendor.
* Campaign creative.
* Campaign flight.

## Lead Source

* Lead by source.
* Lead by source group.
* Lead by UTM.
* Lead by form.
* Lead by landing page.
* Lead by ad/ad set.
* Lead by event.
* Lead by referral.
* Lead by call tracking.
* Source correction.
* Unknown source.
* Duplicate Lead by Campaign.

## Audience

* Audience size.
* Eligible members.
* Suppressed members.
* Consent coverage.
* Overlap.
* Activation status.
* Membership changes.
* Frequency cap.
* Contact fatigue.

## Automation

* Enrollment.
* Active journeys.
* Goal reached.
* Exit reasons.
* Node performance.
* Message count.
* Task creation.
* Suppression.
* Failure.
* Retry.
* Average journey duration.

## Conversion

* Funnel.
* Lead quality.
* Qualified Lead.
* Appointment.
* Deal.
* Booking.
* Contract.
* Revenue.
* Conversion rate.
* Time-to-conversion.
* Gross versus net conversion.

## Attribution

* First Touch.
* Lead Creation Touch.
* Last Touch.
* Multi-touch.
* Sourced Campaign.
* Influenced Campaign.
* Contract attribution.
* Revenue attribution.
* Attribution adjustments.
* Model comparison.

## Cost và ROI

* CPL.
* CPQL.
* Cost per Appointment.
* Cost per Deal.
* Cost per Booking.
* Cost per Contract.
* CAC.
* ROAS.
* ROMI.
* Revenue per Lead.
* Revenue per Channel.
* Spend efficiency.
* Agency performance.

## Compliance

* Consent failures.
* Suppression.
* Opt-out.
* Hard bounce.
* Complaint.
* Frequency breach.
* Quiet-hour violation.
* Data retention.
* Audience export.
* Sensitive access.

Operational views phải drill-down đúng scope. Certified Metrics thuộc Analytics Context.

---

# 152. Candidate data model — không phải physical schema canonical

> Exact tables, columns, constraints, indexes và references chỉ có hiệu lực qua Marketing Context DB Specification và Alembic historical imports. Cross-context references không mặc định tạo cross-schema business foreign keys.

## 152.1. Campaign

### `marketing_campaigns`

* `id`
* `campaign_code`
* `enterprise_id`
* `legal_entity_id`
* `parent_campaign_id`
* `program_id`
* `name`
* `campaign_type`
* `primary_objective_code`
* `transaction_context`
* `project_id`
* `sales_launch_id`
* `owner_user_id`
* `currency`
* `planned_budget_amount`
* `status`
* `current_version`
* `planned_start_at`
* `planned_end_at`
* `actual_start_at`
* `actual_end_at`
* `created_by`
* `created_at`
* `updated_at`
* `version`

### `marketing_campaign_versions`

* `id`
* `campaign_id`
* `version`
* `strategy_snapshot_json`
* `scope_snapshot_json`
* `objective_snapshot_json`
* `channel_plan_json`
* `audience_strategy_json`
* `consent_purpose_code`
* `attribution_model_id`
* `conversion_goal_ids_json`
* `budget_snapshot_json`
* `effective_from`
* `effective_to`
* `status`
* `created_by`
* `reviewed_by`
* `approved_by`
* `created_at`

### `marketing_campaign_objectives`

* `id`
* `campaign_id`
* `campaign_version_id`
* `objective_code`
* `is_primary`
* `target_value`
* `target_unit`
* `target_date`
* `created_at`

### `marketing_campaign_projects`

* `id`
* `campaign_id`
* `project_id`
* `sales_launch_id`
* `relationship_type`
* `created_at`

---

## 152.2. Campaign Flight và Channel

### `marketing_campaign_flights`

* `id`
* `flight_code`
* `campaign_id`
* `campaign_version_id`
* `name`
* `start_at`
* `end_at`
* `timezone`
* `budget_amount`
* `currency`
* `audience_version_id`
* `status`
* `created_at`

### `marketing_channel_executions`

* `id`
* `execution_code`
* `campaign_id`
* `flight_id`
* `channel_code`
* `platform_account_id`
* `external_campaign_id`
* `external_ad_group_id`
* `placement_code`
* `budget_amount`
* `currency`
* `start_at`
* `end_at`
* `status`
* `created_at`

### `marketing_placements`

* `id`
* `channel_execution_id`
* `placement_code`
* `external_placement_id`
* `name`
* `status`
* `created_at`

---

## 152.3. Source Taxonomy

### `marketing_source_definitions`

* `id`
* `source_code`
* `source_group`
* `channel_code`
* `medium_code`
* `name`
* `status`
* `created_at`

### `marketing_source_mapping_rules`

* `id`
* `rule_code`
* `priority`
* `raw_pattern_json`
* `normalized_source_code`
* `normalized_medium_code`
* `normalized_channel_code`
* `effective_from`
* `effective_to`
* `status`
* `version`
* `created_by`
* `approved_by`
* `created_at`

### `marketing_tracking_codes`

* `id`
* `tracking_code`
* `tracking_type`
* `campaign_id`
* `flight_id`
* `channel_execution_id`
* `placement_id`
* `creative_version_id`
* `landing_page_id`
* `partner_party_id`
* `effective_from`
* `effective_to`
* `status`
* `created_at`

### `marketing_tracking_urls`

* `id`
* `tracking_code_id`
* `destination_url`
* `generated_tracking_url`
* `utm_snapshot_json`
* `short_url`
* `created_at`

---

## 152.4. Creative và Content

### `marketing_creatives`

* `id`
* `creative_code`
* `campaign_id`
* `creative_type`
* `name`
* `status`
* `current_version`
* `created_at`

### `marketing_creative_versions`

* `id`
* `creative_id`
* `version`
* `headline`
* `body_document_reference`
* `cta_code`
* `media_document_references_json`
* `language_code`
* `legal_disclaimer_version`
* `personalization_schema_json`
* `content_hash`
* `rights_valid_until`
* `status`
* `created_by`
* `brand_reviewed_by`
* `legal_reviewed_by`
* `approved_by`
* `created_at`

### `marketing_content_approvals`

* `id`
* `creative_version_id`
* `approval_type`
* `status`
* `reviewer_user_id`
* `comments`
* `resolved_at`
* `created_at`

---

## 152.5. Landing Page và Form

### `marketing_landing_pages`

* `id`
* `landing_page_code`
* `campaign_id`
* `project_id`
* `external_cms_provider`
* `external_page_id`
* `url`
* `status`
* `current_version`
* `published_at`
* `created_at`

### `marketing_landing_page_versions`

* `id`
* `landing_page_id`
* `version`
* `content_document_reference`
* `form_id`
* `tracking_configuration_json`
* `privacy_notice_version`
* `status`
* `created_at`

### `marketing_forms`

* `id`
* `form_code`
* `campaign_id`
* `project_id`
* `purpose_code`
* `status`
* `current_version`
* `created_at`

### `marketing_form_versions`

* `id`
* `form_id`
* `version`
* `field_schema_json`
* `validation_rules_json`
* `consent_fields_json`
* `hidden_tracking_fields_json`
* `routing_rule_json`
* `duplicate_policy_json`
* `privacy_notice_version`
* `effective_from`
* `effective_to`
* `status`
* `created_by`
* `reviewed_by`
* `approved_by`
* `created_at`

### `marketing_form_submissions`

* `id`
* `submission_code`
* `form_id`
* `form_version_id`
* `campaign_id`
* `flight_id`
* `landing_page_id`
* `anonymous_visitor_id`
* `raw_payload_reference`
* `normalized_payload_json`
* `tracking_snapshot_json`
* `consent_snapshot_json`
* `spam_score`
* `validation_status`
* `processing_status`
* `lead_id`
* `customer_id`
* `idempotency_key`
* `submitted_at`
* `processed_at`
* `created_at`

---

## 152.6. Anonymous Identity và Touchpoint

### `marketing_anonymous_visitors`

* `id`
* `anonymous_visitor_code`
* `first_seen_at`
* `last_seen_at`
* `first_source_snapshot_json`
* `identity_status`
* `resolved_party_id`
* `resolved_lead_id`
* `resolved_customer_id`
* `created_at`
* `updated_at`

### `marketing_anonymous_identifiers`

* `id`
* `anonymous_visitor_id`
* `identifier_type`
* `identifier_hash`
* `provider`
* `first_seen_at`
* `last_seen_at`
* `status`
* `created_at`

### `marketing_identity_links`

* `id`
* `link_type`
* `anonymous_visitor_id`
* `lead_id`
* `party_id`
* `customer_id`
* `phone_identity_id`
* `email_reference`
* `confidence_score`
* `resolution_method`
* `evidence_reference`
* `review_status`
* `resolved_at`
* `created_at`

### `marketing_touchpoints`

* `id`
* `touchpoint_code`
* `enterprise_id`
* `legal_entity_id`
* `campaign_id`
* `flight_id`
* `channel_execution_id`
* `placement_id`
* `creative_version_id`
* `landing_page_id`
* `tracking_code_id`
* `anonymous_visitor_id`
* `lead_id`
* `party_id`
* `customer_id`
* `touchpoint_type`
* `source_group`
* `source_code`
* `medium_code`
* `raw_tracking_json`
* `normalized_tracking_json`
* `identity_confidence`
* `source_confidence`
* `engagement_quality_score`
* `attribution_eligibility`
* `occurred_at`
* `recorded_at`
* `external_event_id`
* `payload_hash`
* `created_at`

---

## 152.7. Lead Source Snapshot

### `marketing_lead_source_snapshots`

* `id`
* `lead_id`
* `customer_id`
* `first_touchpoint_id`
* `lead_creation_touchpoint_id`
* `source_group`
* `source_code`
* `medium_code`
* `campaign_id`
* `flight_id`
* `channel_execution_id`
* `placement_id`
* `creative_version_id`
* `landing_page_id`
* `tracking_snapshot_json`
* `normalization_rule_version`
* `identity_confidence`
* `captured_at`
* `created_at`

### `marketing_source_corrections`

* `id`
* `lead_source_snapshot_id`
* `original_snapshot_json`
* `corrected_snapshot_json`
* `reason_code`
* `reason`
* `evidence_reference`
* `status`
* `requested_by`
* `approved_by`
* `created_at`
* `resolved_at`

---

## 152.8. Audience

### `marketing_audiences`

* `id`
* `audience_code`
* `enterprise_id`
* `legal_entity_id`
* `name`
* `audience_type`
* `purpose_code`
* `owner_user_id`
* `status`
* `current_version`
* `created_at`
* `updated_at`

### `marketing_audience_versions`

* `id`
* `audience_id`
* `version`
* `definition_json`
* `exclusion_rules_json`
* `consent_policy_json`
* `channel_code`
* `entry_policy_json`
* `exit_policy_json`
* `reentry_policy_json`
* `evaluation_schedule`
* `effective_from`
* `effective_to`
* `status`
* `created_by`
* `reviewed_by`
* `approved_by`
* `created_at`

### `marketing_audience_evaluation_runs`

* `id`
* `audience_version_id`
* `run_code`
* `evaluation_at`
* `data_snapshot_time`
* `candidate_count`
* `eligible_count`
* `suppressed_count`
* `excluded_count`
* `status`
* `started_at`
* `completed_at`
* `created_at`

### `marketing_audience_memberships`

* `id`
* `audience_evaluation_run_id`
* `audience_version_id`
* `member_type`
* `member_id`
* `party_id`
* `customer_id`
* `lead_id`
* `anonymous_visitor_id`
* `eligibility_status`
* `membership_reasons_json`
* `exclusion_reasons_json`
* `consent_snapshot_json`
* `suppression_snapshot_json`
* `effective_from`
* `effective_to`
* `created_at`

### `marketing_suppressions`

* `id`
* `suppression_code`
* `member_type`
* `member_id`
* `party_id`
* `customer_id`
* `contact_reference`
* `suppression_type`
* `scope_type`
* `scope_id`
* `reason`
* `source_type`
* `source_id`
* `is_hard`
* `effective_from`
* `effective_to`
* `status`
* `created_at`

### `marketing_frequency_counters`

* `id`
* `identity_type`
* `identity_id`
* `channel_code`
* `scope_type`
* `scope_id`
* `window_start`
* `window_end`
* `attempt_count`
* `sent_count`
* `delivered_count`
* `created_at`
* `updated_at`

---

## 152.9. Audience Activation

### `marketing_audience_activations`

* `id`
* `activation_code`
* `campaign_id`
* `flight_id`
* `audience_version_id`
* `audience_evaluation_run_id`
* `destination_type`
* `destination_provider`
* `external_audience_id`
* `eligible_count`
* `exported_count`
* `rejected_count`
* `removal_policy_json`
* `status`
* `activated_by`
* `activated_at`
* `created_at`

### `marketing_audience_activation_items`

* `id`
* `audience_activation_id`
* `audience_membership_id`
* `exported_identifier_hash`
* `provider_status`
* `rejection_reason`
* `created_at`

---

## 152.10. Journey và Automation

### `marketing_journeys`

* `id`
* `journey_code`
* `enterprise_id`
* `legal_entity_id`
* `campaign_id`
* `name`
* `journey_type`
* `owner_user_id`
* `status`
* `current_version`
* `created_at`
* `updated_at`

### `marketing_journey_versions`

* `id`
* `journey_id`
* `version`
* `trigger_definition_json`
* `node_graph_json`
* `entry_policy_json`
* `exit_policy_json`
* `reentry_policy_json`
* `goal_definition_json`
* `frequency_policy_json`
* `consent_policy_json`
* `error_policy_json`
* `effective_from`
* `effective_to`
* `status`
* `created_by`
* `reviewed_by`
* `approved_by`
* `created_at`

### `marketing_journey_enrollments`

* `id`
* `enrollment_code`
* `journey_id`
* `journey_version_id`
* `entity_type`
* `entity_id`
* `party_id`
* `customer_id`
* `lead_id`
* `entry_trigger_type`
* `entry_trigger_id`
* `audience_membership_id`
* `consent_snapshot_json`
* `suppression_snapshot_json`
* `current_node_id`
* `reentry_count`
* `status`
* `entered_at`
* `exited_at`
* `created_at`
* `updated_at`

### `marketing_journey_step_executions`

* `id`
* `journey_enrollment_id`
* `node_id`
* `node_type`
* `trigger_event_id`
* `input_snapshot_json`
* `output_snapshot_json`
* `idempotency_key`
* `attempt_number`
* `status`
* `scheduled_at`
* `started_at`
* `completed_at`
* `error_code`
* `created_at`

---

## 152.11. Marketing Message

### `marketing_messages`

* `id`
* `message_code`
* `campaign_id`
* `flight_id`
* `journey_id`
* `journey_enrollment_id`
* `audience_membership_id`
* `party_id`
* `customer_id`
* `lead_id`
* `channel_code`
* `creative_version_id`
* `purpose_code`
* `sender_reference`
* `recipient_reference`
* `consent_snapshot_json`
* `suppression_result_json`
* `frequency_result_json`
* `rendering_snapshot_json`
* `scheduled_at`
* `status`
* `interaction_id`
* `external_message_id`
* `created_at`
* `updated_at`

### `marketing_message_events`

* `id`
* `marketing_message_id`
* `event_type`
* `external_event_id`
* `occurred_at`
* `payload_reference`
* `created_at`

---

## 152.12. Conversion

### `marketing_conversion_definitions`

* `id`
* `conversion_code`
* `name`
* `source_event_type`
* `qualification_rules_json`
* `deduplication_rule_json`
* `value_rule_json`
* `reversal_event_type`
* `default_attribution_model_id`
* `default_window_policy_json`
* `effective_from`
* `effective_to`
* `status`
* `version`
* `created_at`

### `marketing_conversions`

* `id`
* `conversion_event_code`
* `conversion_definition_id`
* `source_event_type`
* `source_event_id`
* `lead_id`
* `customer_id`
* `deal_id`
* `booking_id`
* `contract_id`
* `revenue_entitlement_id`
* `conversion_value`
* `currency`
* `status`
* `occurred_at`
* `validated_at`
* `reversed_at`
* `deduplication_key`
* `created_at`

---

## 152.13. Attribution

### `marketing_attribution_models`

* `id`
* `model_code`
* `name`
* `model_type`
* `status`
* `current_version`
* `created_at`

### `marketing_attribution_model_versions`

* `id`
* `attribution_model_id`
* `version`
* `touchpoint_eligibility_rules_json`
* `weighting_rules_json`
* `window_rules_json`
* `direct_handling_policy_json`
* `identity_confidence_policy_json`
* `rounding_policy_json`
* `effective_from`
* `effective_to`
* `status`
* `created_by`
* `reviewed_by`
* `approved_by`
* `created_at`

### `marketing_attribution_runs`

* `id`
* `run_code`
* `conversion_id`
* `attribution_model_version_id`
* `identity_path_snapshot_json`
* `window_start`
* `window_end`
* `status`
* `reason_code`
* `calculated_at`
* `created_at`

### `marketing_attribution_results`

* `id`
* `attribution_run_id`
* `conversion_id`
* `touchpoint_id`
* `campaign_id`
* `flight_id`
* `channel_code`
* `source_code`
* `credit_percentage`
* `attributed_value`
* `currency`
* `is_sourced`
* `is_influenced`
* `status`
* `created_at`

### `marketing_attribution_adjustments`

* `id`
* `original_attribution_result_id`
* `new_attribution_run_id`
* `adjustment_type`
* `credit_delta`
* `value_delta`
* `reason`
* `source_type`
* `source_id`
* `approved_by`
* `created_at`

---

## 152.14. Budget và Spend

### `marketing_budgets`

* `id`
* `budget_code`
* `campaign_id`
* `flight_id`
* `legal_entity_id`
* `project_id`
* `channel_code`
* `vendor_party_id`
* `period_from`
* `period_to`
* `currency`
* `planned_amount`
* `approved_amount`
* `committed_amount`
* `spent_amount`
* `status`
* `created_by`
* `approved_by`
* `created_at`
* `updated_at`

### `marketing_spend_records`

* `id`
* `spend_code`
* `campaign_id`
* `flight_id`
* `channel_execution_id`
* `platform_account_id`
* `vendor_party_id`
* `spend_type`
* `spend_date`
* `currency`
* `estimated_amount`
* `actual_amount`
* `external_reference`
* `payload_hash`
* `status`
* `created_at`

### `marketing_cost_allocations`

* `id`
* `spend_record_id`
* `allocation_target_type`
* `allocation_target_id`
* `allocation_method`
* `allocated_amount`
* `currency`
* `rule_version`
* `created_at`

---

## 152.15. Experiment

### `marketing_experiments`

* `id`
* `experiment_code`
* `campaign_id`
* `name`
* `experiment_type`
* `primary_metric_code`
* `guardrail_metrics_json`
* `assignment_policy_json`
* `start_at`
* `end_at`
* `status`
* `current_version`
* `created_at`

### `marketing_experiment_variants`

* `id`
* `experiment_id`
* `variant_code`
* `name`
* `treatment_snapshot_json`
* `allocation_percentage`
* `is_control`
* `status`
* `created_at`

### `marketing_experiment_assignments`

* `id`
* `experiment_id`
* `variant_id`
* `entity_type`
* `entity_id`
* `party_id`
* `customer_id`
* `assignment_key`
* `assigned_at`
* `status`
* `created_at`

### `marketing_experiment_results`

* `id`
* `experiment_id`
* `variant_id`
* `metric_code`
* `sample_size`
* `conversion_count`
* `metric_value`
* `confidence_reference_json`
* `calculated_at`
* `created_at`

---

# 153. Candidate application operations — không phải OpenAPI canonical

> Exact paths, methods, payloads, errors, idempotency và authorization metadata thuộc OpenAPI.

## Campaign

```text
GET    /marketing/campaigns
POST   /marketing/campaigns
GET    /marketing/campaigns/{id}
PATCH  /marketing/campaigns/{id}
POST   /marketing/campaigns/{id}/versions
GET    /marketing/campaign-versions/{id}
POST   /marketing/campaign-versions/{id}/validate
POST   /marketing/campaign-versions/{id}/submit-review
POST   /marketing/campaign-versions/{id}/approve
POST   /marketing/campaign-versions/{id}/schedule
POST   /marketing/campaigns/{id}/activate
POST   /marketing/campaigns/{id}/pause
POST   /marketing/campaigns/{id}/complete
POST   /marketing/campaigns/{id}/cancel
GET    /marketing/campaigns/{id}/history
```

## Flight và Channel

```text
GET    /marketing/campaigns/{id}/flights
POST   /marketing/campaigns/{id}/flights
PATCH  /marketing/campaign-flights/{id}
POST   /marketing/campaign-flights/{id}/activate
POST   /marketing/campaign-flights/{id}/pause

GET    /marketing/channel-executions
POST   /marketing/campaign-flights/{id}/channel-executions
POST   /marketing/channel-executions/{id}/sync
POST   /marketing/channel-executions/{id}/reconcile
```

## Source và Tracking

```text
GET    /marketing/sources
POST   /marketing/source-mapping-rules
POST   /marketing/source-mapping-rules/{id}/test
POST   /marketing/source-mapping-rules/{id}/approve
POST   /marketing/source-mapping-rules/{id}/activate

POST   /marketing/tracking-codes
GET    /marketing/tracking-codes/{id}
POST   /marketing/tracking-urls
POST   /marketing/tracking-codes/{id}/disable
```

## Creative và Content

```text
GET    /marketing/creatives
POST   /marketing/creatives
GET    /marketing/creatives/{id}
POST   /marketing/creatives/{id}/versions
PATCH  /marketing/creative-versions/{id}
POST   /marketing/creative-versions/{id}/submit-review
POST   /marketing/creative-versions/{id}/approve
POST   /marketing/creative-versions/{id}/activate
```

## Form và Submission

```text
GET    /marketing/forms
POST   /marketing/forms
POST   /marketing/forms/{id}/versions
POST   /marketing/form-versions/{id}/validate
POST   /marketing/form-versions/{id}/approve
POST   /marketing/form-versions/{id}/activate

POST   /marketing/form-submissions
GET    /marketing/form-submissions
GET    /marketing/form-submissions/{id}
POST   /marketing/form-submissions/{id}/validate
POST   /marketing/form-submissions/{id}/process
POST   /marketing/form-submissions/{id}/mark-spam
POST   /marketing/form-submissions/{id}/reprocess
```

## Touchpoint và Identity

```text
GET    /marketing/touchpoints
POST   /marketing/touchpoints
GET    /marketing/touchpoints/{id}
POST   /marketing/touchpoints/{id}/validate
POST   /marketing/touchpoints/{id}/mark-duplicate
POST   /marketing/touchpoints/{id}/link-identity

GET    /marketing/anonymous-visitors/{id}
POST   /marketing/identity-links
POST   /marketing/identity-links/{id}/review
POST   /marketing/identity-links/{id}/reverse
```

## Lead Source

```text
GET    /marketing/leads/{id}/source-snapshot
POST   /marketing/form-submissions/{id}/create-or-link-lead
POST   /marketing/lead-source-snapshots/{id}/correction-requests
POST   /marketing/source-corrections/{id}/approve
POST   /marketing/source-corrections/{id}/execute
```

## Audience

```text
GET    /marketing/audiences
POST   /marketing/audiences
GET    /marketing/audiences/{id}
POST   /marketing/audiences/{id}/versions
PATCH  /marketing/audience-versions/{id}
POST   /marketing/audience-versions/{id}/estimate
POST   /marketing/audience-versions/{id}/preview
POST   /marketing/audience-versions/{id}/validate
POST   /marketing/audience-versions/{id}/submit-review
POST   /marketing/audience-versions/{id}/approve
POST   /marketing/audience-versions/{id}/activate
POST   /marketing/audience-versions/{id}/evaluate
GET    /marketing/audience-evaluation-runs/{id}
GET    /marketing/audience-evaluation-runs/{id}/members
```

## Suppression và Frequency

```text
GET    /marketing/suppressions
POST   /marketing/suppressions
POST   /marketing/suppressions/{id}/end
GET    /marketing/eligibility/check
GET    /marketing/frequency-counters
POST   /marketing/frequency-counters/recalculate
```

## Audience Activation

```text
POST   /marketing/audience-activations
GET    /marketing/audience-activations/{id}
POST   /marketing/audience-activations/{id}/execute
POST   /marketing/audience-activations/{id}/refresh
POST   /marketing/audience-activations/{id}/remove-members
POST   /marketing/audience-activations/{id}/reconcile
```

## Journey

```text
GET    /marketing/journeys
POST   /marketing/journeys
GET    /marketing/journeys/{id}
POST   /marketing/journeys/{id}/versions
PATCH  /marketing/journey-versions/{id}
POST   /marketing/journey-versions/{id}/validate
POST   /marketing/journey-versions/{id}/simulate
POST   /marketing/journey-versions/{id}/submit-review
POST   /marketing/journey-versions/{id}/approve
POST   /marketing/journey-versions/{id}/activate
POST   /marketing/journeys/{id}/pause
POST   /marketing/journeys/{id}/stop
```

## Enrollment và Execution

```text
GET    /marketing/journey-enrollments
GET    /marketing/journey-enrollments/{id}
POST   /marketing/journey-enrollments
POST   /marketing/journey-enrollments/{id}/pause
POST   /marketing/journey-enrollments/{id}/resume
POST   /marketing/journey-enrollments/{id}/exit
POST   /marketing/journey-enrollments/{id}/retry
GET    /marketing/journey-enrollments/{id}/executions
```

## Message

```text
GET    /marketing/messages
GET    /marketing/messages/{id}
POST   /marketing/messages/{id}/check-eligibility
POST   /marketing/messages/{id}/schedule
POST   /marketing/messages/{id}/send
POST   /marketing/messages/{id}/cancel
POST   /marketing/messages/{id}/retry
GET    /marketing/messages/{id}/events
```

## Conversion và Attribution

```text
GET    /marketing/conversion-definitions
POST   /marketing/conversion-definitions
POST   /marketing/conversion-definitions/{id}/versions
POST   /marketing/conversions
GET    /marketing/conversions
GET    /marketing/conversions/{id}
POST   /marketing/conversions/{id}/validate
POST   /marketing/conversions/{id}/reverse

GET    /marketing/attribution-models
POST   /marketing/attribution-models
POST   /marketing/attribution-models/{id}/versions
POST   /marketing/attribution-model-versions/{id}/simulate
POST   /marketing/attribution-model-versions/{id}/approve
POST   /marketing/conversions/{id}/attribution-runs
GET    /marketing/attribution-runs/{id}
POST   /marketing/attribution-runs/{id}/approve
POST   /marketing/conversions/{id}/recalculate-attribution
```

## Budget và Spend

```text
GET    /marketing/budgets
POST   /marketing/budgets
GET    /marketing/budgets/{id}
POST   /marketing/budgets/{id}/submit-review
POST   /marketing/budgets/{id}/approve
POST   /marketing/budgets/{id}/close

GET    /marketing/spend-records
POST   /marketing/spend-records
POST   /marketing/spend-records/import
POST   /marketing/spend-records/{id}/verify
POST   /marketing/spend-records/{id}/reconcile
POST   /marketing/spend-records/{id}/adjust
POST   /marketing/spend-records/{id}/allocate
```

## Experiment

```text
GET    /marketing/experiments
POST   /marketing/experiments
GET    /marketing/experiments/{id}
POST   /marketing/experiments/{id}/validate
POST   /marketing/experiments/{id}/approve
POST   /marketing/experiments/{id}/start
POST   /marketing/experiments/{id}/pause
POST   /marketing/experiments/{id}/complete
POST   /marketing/experiments/{id}/calculate-results
```

Backend phải tự enforce:

* Authenticated user.
* Legal Entity.
* Campaign scope.
* Project Access.
* Customer scope.
* Consent.
* Suppression.
* Quiet Hours.
* Frequency Cap.
* Field masking.
* Workflow.
* Approval.
* Audience Version.
* Campaign Version.
* Attribution Model Version.
* Idempotency.
* Optimistic locking.
* Retention.
* Audit.

---

# 154. Candidate permission vocabulary — không phải Permission Registry canonical

> Exact permissions, scopes, roles, SoD, concealment và masking thuộc security registries/matrices.

## Campaign

```text
marketing_campaign.view
marketing_campaign.create
marketing_campaign.update_draft
marketing_campaign.create_version
marketing_campaign.validate
marketing_campaign.review
marketing_campaign.approve
marketing_campaign.schedule
marketing_campaign.activate
marketing_campaign.pause
marketing_campaign.complete
marketing_campaign.cancel
marketing_campaign.view_audit
```

## Source và Tracking

```text
marketing_source.view
marketing_source.manage_mapping
marketing_source.test_mapping
marketing_source.approve_mapping
marketing_tracking.create
marketing_tracking.view
marketing_tracking.disable
marketing_source_correction.request
marketing_source_correction.approve
```

## Creative và Form

```text
marketing_creative.view
marketing_creative.create
marketing_creative.update_draft
marketing_creative.review
marketing_creative.legal_review
marketing_creative.approve

marketing_form.view
marketing_form.create
marketing_form.update_draft
marketing_form.review
marketing_form.approve
marketing_submission.view
marketing_submission.view_raw
marketing_submission.process
marketing_submission.mark_spam
marketing_submission.reprocess
```

## Audience

```text
marketing_audience.view
marketing_audience.create
marketing_audience.update_draft
marketing_audience.estimate
marketing_audience.preview_masked
marketing_audience.preview_full
marketing_audience.review
marketing_audience.approve
marketing_audience.activate
marketing_audience.export
marketing_suppression.view
marketing_suppression.manage
marketing_frequency.view
marketing_frequency.override
```

## Journey và Message

```text
marketing_journey.view
marketing_journey.create
marketing_journey.update_draft
marketing_journey.validate
marketing_journey.simulate
marketing_journey.review
marketing_journey.approve
marketing_journey.activate
marketing_journey.pause
marketing_journey.stop

marketing_message.view
marketing_message.schedule
marketing_message.send
marketing_message.cancel
marketing_message.retry
marketing_message.view_content
```

## Touchpoint và Attribution

```text
marketing_touchpoint.view
marketing_touchpoint.view_raw
marketing_touchpoint.create
marketing_touchpoint.validate
marketing_touchpoint.link_identity
marketing_touchpoint.mark_duplicate

marketing_attribution.view
marketing_attribution.view_path
marketing_attribution.calculate
marketing_attribution.recalculate
marketing_attribution.review
marketing_attribution.approve
marketing_attribution.adjust
marketing_attribution.export
```

## Budget và Spend

```text
marketing_budget.view
marketing_budget.create
marketing_budget.review
marketing_budget.approve
marketing_budget.close

marketing_spend.view
marketing_spend.view_sensitive
marketing_spend.create
marketing_spend.import
marketing_spend.verify
marketing_spend.reconcile
marketing_spend.adjust
marketing_spend.allocate
marketing_spend.export
```

## Experiment

```text
marketing_experiment.view
marketing_experiment.create
marketing_experiment.validate
marketing_experiment.review
marketing_experiment.approve
marketing_experiment.start
marketing_experiment.pause
marketing_experiment.complete
marketing_experiment.view_results
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

# 155. Candidate role baseline — không phải Role/Permission Registry canonical

## 155.1. Marketing Executive

Được:

* Tạo Campaign Draft.
* Tạo Creative Draft.
* Tạo Audience Draft.
* Tạo Journey Draft.
* Xem performance Campaign được giao.
* Xử lý Form Submission theo quyền.

Không được:

* Tự approve Campaign của mình nếu SoD áp dụng.
* Xem full Customer ngoài scope.
* Export Audience tùy ý.
* Override hard suppression.
* Sửa Lead assignment.
* Sửa sales attribution.

## 155.2. Marketing Manager

Được:

* Quản lý Campaign team.
* Review Audience.
* Review Automation.
* Phê duyệt trong authority.
* Xem spend và conversion.
* Xử lý source correction.

Không mặc định được xem Financial Profile chi tiết của Customer.

## 155.3. Sales Manager

Được:

* Xem Lead quality.
* Xem Campaign conversion tới pipeline.
* Xem rejection reason.
* Phối hợp routing.

Không được sửa Campaign attribution để thay commission.

## 155.4. Data/Marketing Operations

Được:

* Source mapping.
* Tracking.
* Form integration.
* Audience evaluation.
* Automation operation.
* Attribution calculation.
* Reconciliation.

## 155.5. Legal/Compliance

Được:

* Review consent text.
* Review content claims.
* Review privacy/suppression.
* Approve exception theo quyền.

## 155.6. Finance

Được:

* Budget.
* Spend.
* Cost reconciliation.
* ROI basis.
* Vendor cost.

Không mặc định xem message content hoặc Customer interaction chi tiết.

## 155.7. Director

Được:

* Approve Campaign lớn.
* Approve ngân sách.
* Xem all theo quyền.
* Export có audit.
* Approve attribution backfill hoặc major correction.

---

# 156. SLA policy inputs — không phải hardcoded SLA contract

Các SLA:

* Campaign review.
* Creative approval.
* Form processing.
* Lead handoff.
* Source normalization.
* Audience evaluation.
* Audience activation.
* Journey failure response.
* Message delivery failure review.
* Spend import.
* Spend reconciliation.
* Attribution calculation.
* Attribution correction.
* Partner data issue.
* Consent withdrawal propagation.

Giá trị tham khảo:

| Nghiệp vụ                         |       SLA tham khảo |
| --------------------------------- | ------------------: |
| Form Submission → Lead processing |         Dưới 5 phút |
| Lead source normalization         |  Gần thời gian thực |
| Consent withdrawal propagation    |       Ngay khi nhận |
| Audience evaluation trước send    | Trước mỗi execution |
| Critical journey failure          |             30 phút |
| Spend import                      |           Hằng ngày |
| Attribution sau Contract event    |          Trong ngày |
| Source correction review          |     1 ngày làm việc |
| Audience export approval          |          Trong ngày |
| Campaign content review           |   1–2 ngày làm việc |

SLA definitions lấy từ Platform Context và Business Calendar; Activity/owning Context quản lý runtime SLA instances theo Context Pack.

---

# 157. Notification

## Marketing Executive

* Campaign assigned.
* Creative rejected.
* Audience evaluation completed.
* Journey failure.
* Form integration error.
* Spend import error.
* Tracking issue.
* Campaign nearing budget.

## Marketing Manager

* Campaign pending approval.
* Audience suppression bất thường.
* Frequency risk.
* CPL tăng.
* Lead quality giảm.
* Attribution mismatch.
* Budget exceeded.
* Experiment integrity issue.

## Sales Manager

* Lead volume spike.
* Lead rejection tăng.
* First response SLA breach.
* Campaign quality issue.
* Duplicate Lead rate cao.

## Legal/Compliance

* Content claim pending.
* Consent text changed.
* Hard suppression override request.
* Complaint spike.
* Data export request.

## Finance/Director

* Over budget.
* High spend unverified.
* ROMI giảm mạnh.
* Revenue reversal ảnh hưởng Campaign.
* Vendor mismatch.

---

# 158. Candidate business facts — không phải Event contracts canonical

> Exact Event names, versions, payloads, channels và consumers thuộc JSON Schema, AsyncAPI và Event Registry.

Marketing Capability phát:

```text
marketing_campaign.created
marketing_campaign.version_created
marketing_campaign.approved
marketing_campaign.activated
marketing_campaign.paused
marketing_campaign.completed
marketing_campaign.cancelled

marketing_flight.created
marketing_flight.activated
marketing_channel_execution.synced

marketing_creative.version_created
marketing_creative.approved
marketing_creative.activated

marketing_form.submission_received
marketing_form.submission_validated
marketing_form.submission_rejected
marketing_form.submission_processed
marketing_form.submission_linked_to_lead

marketing_touchpoint.recorded
marketing_touchpoint.identity_linked
marketing_touchpoint.invalidated

marketing_lead_source.snapshot_created
marketing_lead_source.corrected

marketing_audience.version_created
marketing_audience.evaluated
marketing_audience.activated
marketing_audience.member_suppressed

marketing_journey.activated
marketing_journey.enrollment_created
marketing_journey.goal_reached
marketing_journey.enrollment_exited
marketing_journey.execution_failed

marketing_message.queued
marketing_message.suppressed
marketing_message.sent
marketing_message.delivered
marketing_message.clicked
marketing_message.replied
marketing_message.bounced
marketing_message.unsubscribed
marketing_message.complaint

marketing_conversion.created
marketing_conversion.validated
marketing_conversion.reversed

marketing_attribution.calculated
marketing_attribution.approved
marketing_attribution.adjusted

marketing_budget.approved
marketing_budget.exceeded
marketing_spend.imported
marketing_spend.verified
marketing_spend.reconciled

marketing_experiment.started
marketing_experiment.completed
marketing_experiment.result_calculated
```

Consumer phải idempotent.

---

# 159. Candidate Platform configuration references

```text
marketing.campaign_workflow
marketing.campaign_numbering_scheme
marketing.campaign_version_policy
marketing.campaign_approval_policy
marketing.campaign_scope_policy
marketing.objective_dictionary

marketing.channel_dictionary
marketing.source_taxonomy
marketing.source_mapping_policy
marketing.tracking_naming_policy
marketing.tracking_retention_policy

marketing.creative_workflow
marketing.content_approval_policy
marketing.personalization_policy
marketing.legal_claim_policy
marketing.content_rights_policy

marketing.form_workflow
marketing.form_validation_policy
marketing.form_spam_policy
marketing.form_duplicate_policy
marketing.form_lead_routing_policy

marketing.identity_resolution_policy
marketing.touchpoint_policy
marketing.touchpoint_eligibility_policy
marketing.anonymous_retention_policy

marketing.consent_gate_policy
marketing.suppression_policy
marketing.quiet_hours_policy
marketing.frequency_cap_policy
marketing.contact_fatigue_policy

marketing.audience_workflow
marketing.audience_evaluation_policy
marketing.audience_preview_policy
marketing.audience_activation_policy
marketing.audience_export_policy

marketing.journey_workflow
marketing.journey_reentry_policy
marketing.journey_safety_policy
marketing.journey_retry_policy
marketing.journey_failure_policy

marketing.message_delivery_policy
marketing.message_tracking_policy
marketing.unsubscribe_policy
marketing.complaint_policy

marketing.conversion_definition_policy
marketing.attribution_model_policy
marketing.attribution_window_policy
marketing.attribution_lock_policy
marketing.attribution_recalculation_policy

marketing.budget_workflow
marketing.spend_import_policy
marketing.spend_reconciliation_policy
marketing.cost_allocation_policy
marketing.roi_policy

marketing.experiment_policy
marketing.control_group_policy
marketing.metric_policy

marketing.sla_policy
marketing.notification_policy
marketing.field_access_policy
marketing.export_approval_policy
marketing.retention_policy
```

Mỗi configuration definition phải công bố schema, allowed scopes, resolution strategy, owner, version, effective period, approval và Audit requirements khi phù hợp.

---

# 160. System invariant

Các quy tắc sau không được cấu hình tắt:

1. Marketing không được thay Lead owner trực tiếp.
2. Marketing không được thay Customer care owner trực tiếp.
3. Marketing không được thay Deal primary sale trực tiếp.
4. Marketing Attribution không được dùng thay Commission Attribution.
5. Campaign touchpoint mới không được ghi đè Lead Source Snapshot cũ.
6. Customer merge không được làm mất Touchpoint.
7. Audience activation phải qua Consent Gate.
8. Audience activation phải qua Suppression Gate.
9. Outbound action phải qua Frequency Gate.
10. Hard suppression không được Campaign user thông thường override.
11. Journey không được ghi trực tiếp vào bảng capability nguồn.
12. Journey event lặp không được tạo message hoặc Task trùng.
13. Audience Version đã sử dụng không được sửa trực tiếp.
14. Campaign Version active không được sửa trực tiếp.
15. Attribution Model Version active không được sửa trực tiếp.
16. Attribution Result approved không được sửa trực tiếp.
17. Revenue Attribution không thay Revenue Entitlement.
18. Gross Contract Value không được ghi nhãn là Revenue nếu không nêu basis.
19. Contract cancellation không được xóa conversion lịch sử.
20. Source correction không được xóa source gốc.
21. Anonymous identity không được merge chắc chắn chỉ dựa trên shared device.
22. Imported audience không mặc định có consent.
23. Transactional message không được dùng để lách Marketing opt-out.
24. Provider conversion không mặc định là CRM conversion.
25. Ad platform spend không mặc định verified.
26. Timeline, Interaction và Lead source phải có traceability.
27. User không được tự approve Campaign/budget của mình trái SoD.
28. Backend phải enforce Customer và Project scope.
29. Sensitive Audience preview phải field-mask.
30. Audit Campaign, Audience, Automation, Attribution và Spend không được sửa.

---

# 161. Rule nghiệp vụ bắt buộc

1. Campaign phải có Campaign Type.
2. Campaign phải có Primary Objective.
3. Campaign phải có owner.
4. Campaign phải có Enterprise.
5. Project Campaign phải có Project.
6. Campaign active phải có approved version.
7. Campaign active phải có start/end hoặc always-on policy.
8. Campaign Version active không sửa trực tiếp.
9. Campaign pause không xóa Lead đã tạo.
10. Campaign cancellation giữ lịch sử.
11. Campaign hierarchy không được tạo cycle.
12. Flight phải nằm trong Campaign window hoặc có approved exception.
13. Channel Execution phải có channel.
14. External Campaign ID không được dùng làm internal ID duy nhất.
15. Source raw phải được giữ.
16. Source normalized phải có mapping rule.
17. Mapping rule phải có priority.
18. Mapping rule mới không tự viết lại source cũ.
19. UTM Campaign ID phải ổn định.
20. Tracking Code phải unique.
21. QR Code phải link Campaign/Flight.
22. Manual offline source phải có actor.
23. Source correction phải có reason.
24. Source correction không đổi Lead owner.
25. Form phải có version.
26. Active Form không sửa trực tiếp.
27. Form phải có purpose.
28. Form consent text phải version.
29. Form submission phải idempotent.
30. Invalid submission không tự tạo Lead.
31. Spam submission không được tính Valid Lead.
32. Lead creation phải qua Lead Management Capability.
33. Customer resolution phải qua Customer Identity Governance Capability.
34. Marketing không tạo Customer identity song song.
35. Touchpoint phải có occurred_at.
36. Touchpoint phải có source.
37. Touchpoint duplicate không tham gia attribution.
38. Bot Touchpoint không tham gia attribution trái policy.
39. Anonymous visitor phải có privacy-safe identifier.
40. Shared device không đủ để merge identity chắc chắn.
41. Identity link phải có confidence.
42. Reversed identity link không xóa Touchpoint.
43. Consent phải theo purpose.
44. Consent phải theo channel khi policy yêu cầu.
45. Consent withdrawal phải được áp dụng nhanh.
46. Hard opt-out phải chặn outbound.
47. Transactional communication phải tách Marketing.
48. Suppression phải có reason.
49. Hard suppression không override trái quyền.
50. Frequency Cap phải tính xuyên Campaign khi cấu hình.
51. Frequency Counter phải chống event lặp.
52. Contact fatigue không được dùng suy diễn nhạy cảm.
53. Audience phải có owner.
54. Audience phải có purpose.
55. Audience Definition phải version.
56. Audience used in execution không sửa trực tiếp.
57. Audience preview phải field-mask.
58. Audience membership phải snapshot khi activation.
59. Dynamic Audience phải có entry/exit policy.
60. Static import phải kiểm tra consent evidence.
61. Imported list không mặc định có consent.
62. Audience exclusion phải được áp dụng trước send.
63. Audience overlap phải được cảnh báo.
64. Audience export phải có quyền.
65. Ad platform activation chỉ gửi field được phép.
66. Consent withdrawal phải trigger removal khi policy yêu cầu.
67. Journey phải có version.
68. Journey active không sửa trực tiếp.
69. Journey phải có trigger.
70. Journey phải có exit criteria.
71. Journey phải có safety limit.
72. Journey không được tạo infinite loop.
73. Journey re-entry phải theo policy.
74. Journey outbound phải recheck consent tại execution time.
75. Journey outbound phải recheck frequency tại execution time.
76. Journey không tự đổi Lead owner.
77. Journey không tự đổi Deal stage.
78. Journey không tự tạo Booking.
79. Journey không tự xác nhận Contract.
80. Journey source action phải gọi API capability nguồn.
81. Wait Node phải có timeout hoặc exit.
82. Branch expression phải sandbox.
83. Custom code tùy ý bị cấm.
84. Automation retry phải idempotent.
85. Failed execution phải có error.
86. Dead-letter replay phải có quyền.
87. Message phải có purpose.
88. Message phải có consent snapshot.
89. Message phải có frequency result.
90. Message suppressed không được send.
91. Marketing Message phải link Interaction khi sent.
92. Delivery status phải đến từ nguồn hợp lệ.
93. Hard bounce phải tạo suppression.
94. Unsubscribe phải cập nhật restriction.
95. Complaint phải tạo hard suppression theo policy.
96. Content phải có version.
97. Approved content không sửa.
98. Personalization không được lộ field nhạy cảm.
99. Floor Price không được dùng trong Marketing content.
100. Owner contact không được lộ trái quyền.
101. Content rights hết hạn phải chặn sử dụng.
102. Landing Page phải link tracking.
103. Landing Page Form phải có version.
104. Event registration không tự tạo Deal.
105. Event attendance không tự tạo Deal.
106. Referral phải có referrer.
107. Referral không tự tạo reward.
108. Call tracking phải link Campaign.
109. Lead Source Snapshot phải bất biến.
110. New touchpoint không overwrite first source.
111. Attribution phải có model version.
112. Attribution phải có conversion.
113. Attribution phải có window.
114. Attribution Touchpoint phải eligible.
115. Tổng credit phải bằng 100% trong tolerance.
116. First Touch và Last Touch phải tách.
117. Lead Creation Touch phải tách First Touch.
118. Direct handling phải được cấu hình.
119. Unknown không tự coi Direct khi tracking lỗi.
120. Offline attribution cần evidence/confidence.
121. Manual influence cần reason.
122. Marketing-Sourced và Influenced phải tách.
123. Influenced Revenue không cộng dồn naïve.
124. Deal attribution không đổi primary sale.
125. Contract attribution không đổi Contract.
126. Revenue attribution không đổi Revenue Entitlement.
127. Revenue reversal phải tạo attribution adjustment.
128. Contract cancellation không xóa conversion.
129. Attribution recalculation phải tạo run mới.
130. Locked attribution không ghi đè.
131. Conversion Definition phải version.
132. Conversion phải chống duplicate.
133. Contract Amendment không tạo Contract Conversion mới trái rule.
134. Lead-quality operational views phải loại spam/duplicate theo accepted Lead facts.
135. MQL không tự đổi Lead Status.
136. Lead Score phải explainable.
137. Lead Score không tạo care ownership.
138. Behavioral signal phải có expiry.
139. Budget và Spend phải tách.
140. Spend imported không mặc định verified.
141. Spend adjustment không sửa raw import.
142. Cost allocation phải có method.
143. Cost allocation total không vượt Spend.
144. Vendor không tự có Customer access.
145. Platform conversion không mặc định CRM conversion.
146. CPL phải dùng Valid Lead definition.
147. ROAS phải nêu numerator.
148. ROMI phải nêu Revenue basis.
149. Contract Value không được gọi Revenue.
150. Cancelled Contract phải tách gross/net conversion.
151. Experiment phải có primary metric.
152. Experiment assignment phải ổn định.
153. Control Group không chặn transactional notice.
154. Experiment đang chạy không sửa treatment trực tiếp.
155. Early stopping phải theo policy.
156. Multi-Legal Entity phải xác định Campaign owner entity.
157. Project Access không mở Customer data.
158. Audience Access không mở Financial Profile.
159. View không đồng nghĩa Export.
160. Marketing user không bulk export Customer tùy ý.
161. Sensitive Audience access phải audit.
162. Same idempotency key cùng payload trả cùng kết quả.
163. Same key khác payload phải conflict.
164. Provider webhook lặp không tạo Touchpoint trùng.
165. Form webhook lặp không tạo Lead trùng.
166. Message callback lặp không tăng conversion nhiều lần.
167. Contract event lặp không tạo attribution trùng.
168. Revenue event lặp không tạo value trùng.
169. Automation phải lưu rule version.
170. Attribution phải tái tạo được.
171. Audience membership phải tái tạo được.
172. Campaign performance phải nêu data freshness.
173. External platform discrepancy phải được reconcile.
174. Customer merge phải giữ original identity path.
175. Customer merge không nhân đôi conversion.
176. Lead merge không nhân đôi Campaign credit.
177. Retention phải theo policy.
178. Legal Hold phải ngăn purge.
179. Marketing không thay thế ad platform.
180. Marketing không thay thế hệ thống kế toán.

---

# 162. Cảnh báo và phát hiện bất thường

Hệ thống cần cảnh báo khi:

* Campaign Active chưa approved.
* Campaign không có objective.
* Campaign vượt thời gian.
* Campaign vượt budget.
* Campaign chạy Creative hết quyền.
* Campaign không có tracking.
* Source unknown tăng bất thường.
* UTM naming sai.
* External Campaign ID trùng.
* Form submissions giảm đột ngột.
* Form spam tăng.
* Form webhook lặp.
* Lead duplicate rate cao.
* Lead source snapshot thiếu Campaign.
* Source correction hàng loạt.
* Touchpoint volume bất thường.
* Bot traffic tăng.
* Anonymous identity merge confidence thấp.
* Shared device bị link nhiều Customer.
* Consent missing nhưng message queued.
* Hard suppression bị override.
* Customer opt-out vẫn nhận message.
* Quiet-hour violation.
* Frequency Cap breach.
* Contact fatigue tăng.
* Audience size thay đổi bất thường.
* Audience chứa Customer không đủ consent.
* Audience overlap cao.
* Audience export lớn.
* Ad platform activation rejected nhiều.
* Journey loop.
* Journey enrollment tăng đột biến.
* Journey tạo quá nhiều Task.
* Journey message burst.
* Journey failure quá SLA.
* Retry tạo duplicate.
* Message hard bounce tăng.
* Complaint tăng.
* Unsubscribe tăng.
* Creative personalization lộ dữ liệu nhạy cảm.
* Floor Price xuất hiện trong content.
* Landing Page tracking lỗi.
* Event attendance vượt registration bất thường.
* Call tracking không map Campaign.
* Attribution credit không bằng 100%.
* Attribution path chứa Touchpoint sau conversion.
* Duplicate Touchpoint vẫn được credited.
* Revenue attribution vượt Revenue source.
* Influenced Revenue bị cộng trùng.
* Contract cancelled nhưng dashboard vẫn net conversion.
* Revenue reversed nhưng Campaign Revenue chưa điều chỉnh.
* Attribution recalculation thay đổi lớn.
* Locked reporting period bị backfill.
* Spend import trùng.
* Spend currency mismatch.
* Cost allocation vượt Spend.
* CPL giảm bất thường do spam Lead.
* ROAS dùng Contract Value nhưng nhãn Revenue.
* Experiment variant imbalance.
* Control group contamination.
* Tracking loss giữa variant.
* Marketing user xem Customer ngoài scope.
* Marketing export chứa phone đầy đủ.
* Same idempotency key khác payload.
* Provider webhook signature lỗi.
* Data freshness quá cũ nhưng dashboard không cảnh báo.

---

# 163. Audit requirements và evidence

> Audit Context sở hữu immutable Audit facts. Marketing chỉ phát sinh audit-worthy facts và references.

## 163.1. Thao tác bắt buộc

* Campaign create/version/review/approve/activate/pause.
* Flight và Channel Execution.
* Source mapping.
* Tracking code.
* Creative version.
* Content approval.
* Form version.
* Submission processing.
* Spam decision.
* Touchpoint create/invalidate.
* Identity linking.
* Lead source snapshot.
* Source correction.
* Audience create/version/evaluate.
* Audience preview.
* Audience export.
* Suppression.
* Frequency override.
* Audience activation.
* Journey create/version/simulate/activate.
* Journey enrollment.
* Automation execution/retry/replay.
* Message send/suppress/cancel.
* Conversion create/reverse.
* Attribution calculate/recalculate/approve.
* Budget.
* Spend.
* Cost allocation.
* Experiment.
* Sensitive view.
* Export.

## 163.2. Nội dung

* Actor.
* Role.
* Legal Entity.
* Campaign.
* Campaign Version.
* Project.
* Audience.
* Audience Version.
* Journey.
* Journey Version.
* Lead.
* Customer.
* Touchpoint.
* Conversion.
* Attribution Model Version.
* Spend.
* Before.
* After.
* Consent result.
* Suppression result.
* Frequency result.
* Reason.
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

# 164. Retention và Data Governance

Phải cấu hình retention theo:

* Anonymous Touchpoint.
* Known Customer Touchpoint.
* Form raw payload.
* Consent evidence.
* Message content.
* Attribution result.
* Spend data.
* Audience snapshot.
* Experiment data.
* Export file.

Các nguyên tắc:

* Chỉ giữ dữ liệu cần thiết.
* Raw form payload có retention ngắn hơn dữ liệu chuẩn hóa nếu phù hợp.
* Consent evidence phải giữ theo policy.
* Audience export phải có expiry.
* Revoked consent phải được propagation.
* Legal Hold ngăn purge.
* Purge không xóa dữ liệu giao dịch cần lưu hợp lệ.

---

# 165. Import và Export

## 165.1. Import

Hỗ trợ:

* Campaign.
* Spend.
* Form submission.
* Event registration.
* Partner Lead.
* Offline source.
* Platform metrics.
* Existing attribution historical import.

Import phải:

* Validate.
* Dedupe.
* Dry run.
* Mapping.
* Error report.
* Idempotency.
* Audit.

## 165.2. Export

Có thể export:

* Campaign report.
* Aggregated performance.
* Approved audience activation.
* Attribution report.
* Spend reconciliation.

Không mặc định export:

* Customer phone/email.
* Full audience member details.
* Consent evidence.
* Raw form payload.
* Sensitive interaction.

---

# 166. Integration

## 166.1. Ad Platforms

Có thể tích hợp:

* Campaign metadata.
* Spend.
* Impression/click.
* Lead Ads.
* Custom Audience.
* Offline conversion reference.

## 166.2. Analytics

Có thể nhận:

* Session.
* Page view.
* Event.
* Client ID.
* Conversion.

## 166.3. Website/CMS

* Landing Page.
* Form.
* Content.
* Tracking.
* Webhook.

## 166.4. Messaging

Qua Activity and Engagement Capability hoặc provider:

* Email.
* SMS.
* Zalo.
* Chat.

## 166.5. Call Tracking

* Dynamic number.
* Call session.
* Campaign mapping.
* Call outcome.

## 166.6. ERP/Finance

* Vendor reference.
* Budget.
* Spend verification.
* Invoice reference.

---

# 167. Integration Security

Mọi integration phải có:

* Secret management Platform Configuration Capability.
* Scoped credential.
* Webhook signature.
* Replay protection.
* IP/domain policy nếu áp dụng.
* Rate limit.
* Idempotency.
* Raw payload reference.
* Error monitoring.
* Credential rotation.
* Least privilege.

---

# 168. Phạm vi MVP

## 168.1. Bắt buộc

* Campaign.
* Campaign Version.
* Campaign Objective.
* Project/Legal Entity scope.
* Flight.
* Channel.
* Source Taxonomy.
* Source Mapping.
* UTM Registry.
* Tracking URL/QR.
* Creative Version.
* Content approval cơ bản.
* Landing Page metadata.
* Form.
* Form Version.
* Form Submission.
* Spam/Duplicate validation.
* Lead handoff Lead Management Capability.
* Lead Source Snapshot.
* Touchpoint.
* Anonymous Visitor cơ bản.
* Identity linking cơ bản.
* Consent Gate.
* Suppression.
* Frequency Cap.
* Audience.
* Audience Version.
* Audience evaluation.
* Audience snapshot.
* Audience activation cơ bản.
* Journey rule-based.
* Trigger/Wait/Condition/Message/Create Task/Exit.
* Journey enrollment.
* Idempotent execution.
* Marketing Message.
* Interaction link Activity and Engagement Capability.
* Conversion Definition.
* Lead/Deal/Booking/Contract/Revenue conversion.
* First Touch.
* Lead Creation Touch.
* Last Touch.
* Linear Attribution.
* Campaign sourced/influenced.
* Campaign budget.
* Spend import.
* Cost allocation cơ bản.
* CPL/CPQL/Cost per Contract.
* Revenue basis report.
* A/B Test cơ bản.
* Scope.
* Field masking.
* Approval.
* Audit.
* Dashboard.
* Domain events.

## 168.2. Giai đoạn nâng cao

* Real-time behavioral segmentation.
* Advanced multi-touch attribution.
* Data-driven attribution.
* Cross-device identity graph.
* Predictive Lead scoring.
* Predictive audience.
* Lookalike optimization.
* AI content assistance.
* Send-time optimization.
* Advanced experimentation.
* Incrementality measurement.
* Media mix modeling.
* Customer journey analytics.
* Marketing resource management.
* Agency portal.
* Full omnichannel orchestration.
* Advanced call center campaign.
* Dynamic web personalization.
* Customer preference center.
* Advanced consent jurisdiction rules.
* Clean room integration.
* Advanced partner co-marketing.
* Automated offline conversion uploads.
* Advanced spend forecasting.

---

# 169. Tiêu chí nghiệm thu

Capability được xem là đạt khi:

1. Tạo được Campaign.
2. Campaign có Campaign Code.
3. Campaign có Enterprise.
4. Campaign có Legal Entity.
5. Campaign có owner.
6. Campaign có type.
7. Campaign có objective.
8. Project Campaign có Project.
9. Campaign có planned dates.
10. Campaign có status.
11. Tạo được Campaign Version.
12. Version có objective.
13. Version có channel plan.
14. Version có audience strategy.
15. Version có consent purpose.
16. Version có attribution model.
17. Campaign Active cần approved version.
18. Active Version không sửa được.
19. Campaign pause hoạt động.
20. Campaign cancellation giữ lịch sử.
21. Campaign hierarchy hoạt động.
22. Hierarchy cycle bị chặn.
23. Tạo Flight được.
24. Flight có start/end.
25. Flight có timezone.
26. Flight có budget.
27. Tạo Channel Execution.
28. Channel Execution có external reference.
29. Tạo Source Definition.
30. Source Group được chuẩn hóa.
31. Tạo Source Mapping Rule.
32. Mapping Rule có priority.
33. Test Mapping hoạt động.
34. Raw source được giữ.
35. Normalized source được lưu.
36. Mapping mới không sửa source cũ.
37. Tạo UTM chuẩn.
38. Sinh Tracking URL.
39. Sinh QR Code.
40. Tracking Code unique.
41. Tracking Code link Campaign.
42. Tracking Code link Flight.
43. Offline source được hỗ trợ.
44. Manual source có actor.
45. Tạo Creative.
46. Tạo Creative Version.
47. Creative có headline/body/CTA.
48. Creative lưu media reference.
49. Creative có legal disclaimer version.
50. Content approval hoạt động.
51. Approved Creative không sửa được.
52. Creative hết quyền bị chặn.
53. Tạo Landing Page metadata.
54. Landing Page link Campaign.
55. Landing Page link Form.
56. Tạo Form.
57. Form có Purpose.
58. Tạo Form Version.
59. Form Version có field schema.
60. Form có validation.
61. Form có consent text version.
62. Active Form không sửa.
63. Nhận Form Submission.
64. Submission có idempotency key.
65. Submission lưu tracking.
66. Submission lưu consent snapshot.
67. Submission được validate.
68. Spam score được lưu.
69. Spam không tính Valid Lead.
70. Duplicate submission được phát hiện.
71. Submission tạo/link Lead qua Lead Management Capability.
72. Marketing Capability không tạo Customer riêng.
73. Lead Source Snapshot được tạo.
74. Snapshot có First Touch.
75. Snapshot có Lead Creation Touch.
76. Snapshot có Campaign.
77. Snapshot có raw tracking.
78. Snapshot có normalization version.
79. Snapshot không bị Campaign mới ghi đè.
80. Tạo Source Correction Request.
81. Correction giữ original snapshot.
82. Correction có approval.
83. Correction không đổi Lead owner.
84. Tạo Anonymous Visitor.
85. Anonymous Visitor có first source.
86. Tạo Touchpoint.
87. Touchpoint có occurred_at.
88. Touchpoint có source.
89. Touchpoint có Campaign.
90. Touchpoint có identity confidence.
91. Touchpoint có attribution eligibility.
92. Duplicate Touchpoint bị loại.
93. Provider event lặp không tạo Touchpoint trùng.
94. Anonymous-to-Lead link hoạt động.
95. Anonymous-to-Customer link hoạt động.
96. Link có confidence.
97. Shared device không tự merge chắc chắn.
98. Customer merge giữ Touchpoint.
99. Customer merge không nhân đôi Touchpoint.
100. Consent Gate hoạt động.
101. Consent theo purpose hoạt động.
102. Consent theo channel hoạt động.
103. Opt-out chặn outbound.
104. Do-not-contact chặn outbound.
105. Quiet Hours hoạt động.
106. Frequency Cap hoạt động.
107. Frequency tính xuyên Campaign theo policy.
108. Hard Suppression hoạt động.
109. Soft Suppression hoạt động.
110. Hard Suppression không override trái quyền.
111. Hard bounce tạo suppression.
112. Complaint tạo suppression.
113. Tạo Audience.
114. Audience có owner.
115. Audience có type.
116. Audience có purpose.
117. Tạo Audience Version.
118. Audience Version có rules.
119. Audience Version có exclusions.
120. Audience Version có consent policy.
121. Audience estimate hoạt động.
122. Audience preview được mask.
123. Full preview cần quyền.
124. Audience evaluation hoạt động.
125. Evaluation lưu candidate count.
126. Evaluation lưu eligible count.
127. Evaluation lưu suppressed count.
128. Membership có reasons.
129. Membership có consent snapshot.
130. Membership có suppression snapshot.
131. Audience Version used không sửa.
132. Dynamic entry/exit hoạt động.
133. Static import kiểm tra consent.
134. Imported list không mặc định consent.
135. Audience overlap được tính.
136. Overlap warning hoạt động.
137. Audience Activation được tạo.
138. Activation link snapshot.
139. Activation export đúng eligible members.
140. Rejected members được lưu.
141. Ad platform audience ID được lưu.
142. Consent withdrawal có removal flow.
143. Tạo Journey.
144. Tạo Journey Version.
145. Journey có trigger.
146. Journey có node graph.
147. Journey có goal.
148. Journey có exit.
149. Journey validate được.
150. Journey simulation được.
151. Simulation không gửi thật.
152. Journey approved mới Active.
153. Active Journey không sửa.
154. Enrollment được tạo.
155. Enrollment có Journey Version.
156. Enrollment có consent snapshot.
157. Enrollment có current node.
158. Trigger Lead Created hoạt động.
159. Trigger Form Submitted hoạt động.
160. Trigger Interaction Reply hoạt động.
161. Trigger Deal Stage hoạt động.
162. Wait Node hoạt động.
163. Condition Node hoạt động.
164. Branch Node hoạt động.
165. Send Message Node hoạt động.
166. Create Task Node gọi Activity and Engagement Capability.
167. Exit Node hoạt động.
168. Goal Reached hoạt động.
169. Re-entry policy hoạt động.
170. Journey chống infinite loop.
171. Journey chống Task explosion.
172. Journey execution idempotent.
173. Retry không gửi message trùng.
174. Failed execution vào queue xử lý.
175. Manual replay cần quyền.
176. Tạo Marketing Message.
177. Message có Campaign.
178. Message có purpose.
179. Message có consent snapshot.
180. Message có frequency result.
181. Suppressed Message không send.
182. Sent Message tạo Interaction reference.
183. Delivery event được ghi.
184. Click event được ghi.
185. Reply event được ghi.
186. Unsubscribe được ghi.
187. Template Version được snapshot.
188. Rendered content hash được lưu.
189. Personalization không lộ field nhạy cảm.
190. Tạo Event Campaign.
191. Event Registration được lưu.
192. Attendance được lưu.
193. Attendance tạo Timeline Event.
194. Attendance không tự tạo Deal.
195. Tạo Referral Campaign.
196. Referral có Referrer Party.
197. Referral không tự tạo reward.
198. Call Tracking Number link Campaign.
199. Inbound call link source.
200. Call có thể tạo Lead qua Lead Management Capability.
201. Tạo Conversion Definition.
202. Conversion Definition có source event.
203. Conversion Definition có dedupe rule.
204. Conversion Definition có reversal event.
205. Tạo Lead Conversion.
206. Tạo Deal Conversion.
207. Tạo Booking Conversion.
208. Tạo Contract Conversion.
209. Tạo Revenue Conversion.
210. Duplicate event không tạo conversion trùng.
211. Contract Amendment không tạo Contract conversion mới trái rule.
212. Contract cancellation reverse conversion.
213. Reversal không xóa conversion cũ.
214. Tạo Attribution Model.
215. Tạo Model Version.
216. Model có eligibility rules.
217. Model có window.
218. First Touch hoạt động.
219. Lead Creation Touch hoạt động.
220. Last Touch hoạt động.
221. Linear Model hoạt động.
222. Direct handling hoạt động.
223. Attribution loại duplicate Touchpoint.
224. Attribution loại Touchpoint sau conversion.
225. Attribution credit tổng bằng 100%.
226. Attribution lưu model version.
227. Attribution lưu identity path.
228. Attribution lưu conversion.
229. Attribution lưu Campaign credit.
230. Marketing-Sourced được tính.
231. Marketing-Influenced được tính.
232. Deal attribution không đổi primary sale.
233. Contract attribution không đổi Contract.
234. Revenue attribution không đổi Revenue Entitlement.
235. Recognized Revenue attribution được tính.
236. Collected Revenue attribution được tính.
237. Gross Contract Value được gắn nhãn riêng.
238. Revenue reversal tạo attribution adjustment.
239. Attribution recalculation tạo run mới.
240. Attribution result cũ được giữ.
241. Attribution lock hoạt động.
242. Late adjustment vào kỳ phù hợp.
243. Tạo Campaign Budget.
244. Budget có currency.
245. Budget approval hoạt động.
246. Planned, committed và spent được tách.
247. Import Spend được.
248. Spend có external reference.
249. Duplicate Spend được phát hiện.
250. Spend verified được.
251. Spend reconciliation hoạt động.
252. Cost Allocation hoạt động.
253. Allocation không vượt Spend.
254. CPL được tính từ Valid Lead.
255. CPQL được tính.
256. Cost per Deal được tính.
257. Cost per Booking được tính.
258. Cost per Contract được tính.
259. CAC có definition.
260. ROAS hiển thị numerator basis.
261. ROMI dùng Revenue basis rõ ràng.
262. Influenced Revenue cảnh báo double counting.
263. Tạo Experiment.
264. Experiment có primary metric.
265. Tạo Variants.
266. Control Variant được hỗ trợ.
267. Assignment deterministic hoạt động.
268. Variant allocation được kiểm tra.
269. Experiment start cần approval.
270. Treatment không sửa khi đang chạy.
271. Result được tính.
272. Variant imbalance được cảnh báo.
273. Control Group không chặn transactional notice.
274. Marketing Executive chỉ xem scope.
275. Marketing Manager xem team/project.
276. Sales Manager xem Lead quality nhưng không sửa attribution.
277. Finance xem spend nhưng không mặc định xem Customer detail.
278. Director xem all theo quyền.
279. Backend enforce Legal Entity.
280. Backend enforce Project Access.
281. Backend enforce Customer scope.
282. Audience Access không mở Customer 360 đầy đủ.
283. Field masking hoạt động.
284. Audience export cần permission.
285. View không đồng nghĩa Export.
286. Marketing không bulk export Customer trái quyền.
287. Sensitive access có audit.
288. Same idempotency key cùng payload trả cùng kết quả.
289. Same key khác payload báo conflict.
290. Form webhook lặp không tạo Lead trùng.
291. Message callback lặp không tạo event trùng.
292. Contract event lặp không tạo attribution trùng.
293. Revenue event lặp không cộng value trùng.
294. Domain events được phát.
295. Consumer idempotent.
296. Dashboard Campaign drill-down đúng scope.
297. Dashboard Lead Quality đúng scope.
298. Dashboard Attribution đúng scope.
299. Dashboard Revenue không nhầm Contract Value với Revenue.
300. Capability quản lý toàn bộ Marketing mà không làm sai Lead ownership, Customer ownership, Deal responsibility hoặc Commission attribution.

---

# 170. Quan hệ canonical với các Context liên quan

## 170.1. Platform Context

Marketing sử dụng configuration, Workflow/Approval, Business Calendar, templates, feature flags và policy definitions.

Platform sở hữu definitions; Marketing sở hữu Campaign/Audience/Journey runtime state.

## 170.2. IAM Context

Marketing sử dụng Legal Entity, Project Access, user scope, role, delegation và SoD.

Campaign hoặc Audience access không mở Customer scope.

## 170.3. Lead Context

Marketing cung cấp capture/source evidence và Lead intake request.

Lead Context quyết định official Lead, assignment, care protection, status và canonical Lead Source Snapshot.

## 170.4. Party Context

Marketing sử dụng canonical Customer/Party, roles, consent, preference, restrictions và redirect.

Marketing không tạo Customer identity cạnh tranh và không tự hợp nhất identity.

## 170.5. Product và Matching Contexts

Marketing sử dụng Project, Sales Launch, Listing interest, Match/Shortlist signals theo published contracts.

Marketing interest không Hold Listing, thay Availability hoặc tự tạo Deal.

## 170.6. Transaction Context

Marketing sử dụng Deal, Proposal, Booking và accepted Sales Attribution facts.

Marketing Attribution không thay primary sale, co-sale hoặc Commission basis.

## 170.7. Contract Context

Marketing sử dụng Contract, cancellation và payment-related conversion facts.

Marketing không sửa Contract, Receipt hoặc cancellation state.

## 170.8. Revenue Context

Marketing sử dụng Revenue Entitlement, Recognition, Collection và Reversal facts.

Revenue attribution chỉ phân tích Campaign influence; không thay Revenue ownership hoặc Commission.

## 170.9. Activity Context

Marketing gửi outbound/task intent và nhận Interaction, Call, Appointment, Timeline cùng delivery facts.

Marketing không tạo Interaction hoặc cross-channel contact history song song.

## 170.10. Documents, Integration, Analytics và Audit

- Documents sở hữu Creative/Content/export artifacts.
- Integration sở hữu ad platform, CMS, website analytics, messaging, call-tracking và ERP transport.
- Analytics sở hữu certified Marketing/Funnel/ROI Metrics.
- Audit sở hữu immutable Audit facts.

---

# 171. Anti-patterns và canonical requirements

## AP-MKT-001 — Nguồn Lead là một trường text có thể ghi đè

**Không được áp dụng**

Chỉ lưu một source string trên Lead và thay đổi khi có Campaign mới.

**Canonical requirement**

Giữ raw tracking, normalized source, Touchpoint evidence và versioned Lead-intake payload. Canonical Lead Source Snapshot thuộc Lead Context và bất biến sau acceptance, trừ governed correction.

## AP-MKT-002 — Campaign tạo Lead thì sở hữu Customer

**Không được áp dụng**

Campaign hoặc Marketing user tự tạo Customer, đổi owner hoặc mở Customer scope.

**Canonical requirement**

Lead intake đi qua Lead Context; identity/Customer resolution đi qua Party Context; ownership/care protection không thay vì Campaign influence.

## AP-MKT-003 — Marketing Attribution thay Sales Attribution hoặc Commission

**Không được áp dụng**

Dùng Campaign credit để đổi primary sale, co-sale hoặc Commission participant.

**Canonical requirement**

Marketing Attribution chỉ phân tích influence. Sales responsibility thuộc Transaction/Lead; Commission thuộc Revenue Context.

## AP-MKT-004 — Touchpoint mới ghi đè first source

**Không được áp dụng**

Last touch hoặc retargeting Campaign thay First Touch/Lead Creation Touch cũ.

**Canonical requirement**

First Touch, Lead Creation Touch, Last Touch, Sourced và Influenced là các dimensions/snapshots riêng.

## AP-MKT-005 — Audience là file số điện thoại

**Không được áp dụng**

Một static file không có purpose, version, consent, suppression hoặc evaluation evidence.

**Canonical requirement**

Audience phải có Definition/Version, evaluation run, eligibility/suppression results và membership snapshot.

## AP-MKT-006 — Imported audience mặc định có consent

**Không được áp dụng**

Danh sách mua hoặc partner upload được coi là được phép Marketing.

**Canonical requirement**

Mỗi activation phải có lawful basis/consent evidence, identity resolution, suppression và retention checks.

## AP-MKT-007 — Eligibility snapshot là quyền gửi vĩnh viễn

**Không được áp dụng**

Audience member đủ điều kiện lúc evaluation thì được gửi bất kể opt-out hoặc restriction mới.

**Canonical requirement**

Re-check Party consent/restriction, Marketing suppression/frequency và Activity outbound policy tại execution time.

## AP-MKT-008 — Journey ghi trực tiếp business state nguồn

**Không được áp dụng**

Automation tự đổi Lead owner, Deal stage, Booking, Contract hoặc Revenue bằng database write.

**Canonical requirement**

Journey gửi idempotent command tới owning Context; owning Context kiểm tra authorization, workflow và invariants.

## AP-MKT-009 — Marketing Message `QUEUED` đồng nghĩa đã gửi

**Không được áp dụng**

Intent hoặc queue state được tính là delivered Interaction.

**Canonical requirement**

Activity sở hữu normalized Interaction; Integration sở hữu transport. Marketing cập nhật projection từ accepted delivery facts.

## AP-MKT-010 — Marketing sở hữu consent và contact history

**Không được áp dụng**

Tạo consent truth hoặc Interaction store song song để tránh Party/Activity gates.

**Canonical requirement**

Party là consent authority; Activity là interaction/contact-history authority; Marketing giữ campaign eligibility và references.

## AP-MKT-011 — Shared device khẳng định Customer identity

**Không được áp dụng**

Merge anonymous history vào Customer chỉ vì cookie, device hoặc shared contact.

**Canonical requirement**

Identity link phải có confidence/evidence và Party resolution; ambiguous/shared identifiers không được auto-merge chắc chắn.

## AP-MKT-012 — Gross Contract Value được gọi là Revenue hoặc ROI

**Không được áp dụng**

Gọi Contract Value là Revenue hoặc dùng numerator không công bố cho ROAS/ROMI.

**Canonical requirement**

Tách Contract Value, Revenue Entitlement, Recognized Revenue và Collected Revenue; mọi KPI phải công bố basis, currency, period và attribution model.

## AP-MKT-013 — Influenced Revenue cộng dồn giữa Campaign

**Không được áp dụng**

Cộng toàn bộ influenced value của nhiều Campaign như doanh thu độc lập.

**Canonical requirement**

Influenced metrics phải cảnh báo non-additivity/double counting; sourced/allocated credit phải tuân model và tolerance.

## AP-MKT-014 — Attribution recalculation ghi đè kỳ đã khóa

**Không được áp dụng**

Backfill âm thầm thay approved result/reporting period.

**Canonical requirement**

Tạo run/adjustment mới, giữ result cũ, ghi reason/delta và áp approval/restatement policy.

## AP-MKT-015 — Marketing Context sở hữu provider runtime và binary content

**Không được áp dụng**

Lưu credentials, raw retries hoặc permanent media URL như source canonical.

**Canonical requirement**

Integration sở hữu transport/runtime; Documents sở hữu artifacts; Marketing giữ business metadata và governed references.

## AP-MKT-016 — Operational KPI tables là certified analytics

**Không được áp dụng**

Dùng Campaign/Attribution/Spend tables trực tiếp làm executive KPI không semantic governance.

**Canonical requirement**

Marketing phát governed facts; Analytics sở hữu Metric grain, formulas, snapshots, certification và access.

## AP-MKT-017 — Candidate examples là exact contracts

**Không được áp dụng**

Dùng table names, endpoints, statuses, Events, permissions, attribution windows hoặc KPI formulas trong tài liệu này để code trực tiếp.

**Canonical requirement**

Exact database, API, Event, lifecycle, permission, attribution, integration và Metric contracts phải được khóa trong nguồn canonical tương ứng.

## AP-MKT-018 — Mặc định tồn tại hệ thống tiền nhiệm

**Không được áp dụng**

Tự thiết kế old-source aliases, compatibility layer hoặc historical mappings khi chưa có approved scope.

**Canonical requirement**

`crm_bds_ai` là Greenfield. Historical import chỉ tồn tại khi có scope, source mapping, security review, reconciliation và acceptance criteria riêng.

---

# 172. Kết luận

Marketing Capability là lớp quản trị Campaign, marketing touchpoint, audience, journey và attribution của `crm_bds_ai`.

Capability phải bảo đảm:

- Campaign có scope, objective, version, budget intent và approval.
- Raw source được giữ; normalization có version và evidence.
- Lead intake đi qua Lead Context.
- Canonical Lead Source Snapshot không bị Campaign mới ghi đè.
- Customer identity và consent vẫn thuộc Party Context.
- Anonymous identity links có confidence và không merge chắc chắn từ shared device/contact.
- Audience có Definition, Version, evaluation run và membership snapshot.
- Mọi outbound execution re-check consent, restriction, suppression, frequency và workflow.
- Journey không direct-write owning Context aggregates.
- Marketing Message Intent khác Interaction và provider delivery.
- Activity sở hữu Interaction/Call/Task/Timeline; Integration sở hữu transport.
- Documents sở hữu Creative/Content/export artifacts.
- Attribution phân biệt First Touch, Lead Creation Touch, Last Touch, Sourced và Influenced.
- Marketing Attribution không thay Sales Attribution hoặc Commission.
- Contract cancellation và Revenue reversal tạo adjustment, không xóa lịch sử.
- Contract Value, Revenue Entitlement, Recognized Revenue và Collected Revenue được tách.
- CPL, CPQL, CAC, ROAS và ROMI có basis rõ ràng.
- Operational Spend không thay ERP/accounting truth.
- Certified Marketing/Funnel/ROI Metrics thuộc Analytics.
- Webhooks, submissions, touchpoints, conversions và automation đều idempotent.
- Immutable Audit facts thuộc Audit Context.
- Multi-Legal Entity, Project Access, Customer scope và masking được backend enforce.

> Marketing Context sở hữu campaign orchestration và analytical influence; nó không sở hữu Customer identity, Lead responsibility, Interaction truth, Contract/Revenue truth hoặc certified analytics.
