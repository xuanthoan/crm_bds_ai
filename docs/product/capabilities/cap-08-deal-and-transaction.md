# CRM_BDS_AI — CAPABILITY 08: DEAL AND TRANSACTION

## Deal Pipeline, Transaction Case, Proposal, Negotiation, Hold, Booking and Deposit Commitment

**Document ID:** `PROD-CAP-TRA-001`
**Canonical path:** `docs/product/capabilities/cap-08-deal-and-transaction.md`
**Product:** `crm_bds_ai`
**Version:** `1.0.0`  
**Status:** `Accepted / Product Capability Baseline`
**Document type:** `Product Capability Specification`
**Primary capability code:** `CAP-TRA`
**Primary owning Context:** `transaction`
**Owner:** `Product Owner`
**Co-owner:** `Transaction Domain Owner`
**Reviewers:** `Architecture Owner`, `Party Domain Owner`, `Product Domain Owner`, `Contract Domain Owner`, `Revenue Domain Owner`, `Activity Domain Owner`, `Documents Owner`, `Integration Owner`, `Analytics Owner`, `Security Owner`, `Database Owner`, `API Owner`, `Event Architecture Owner`, `Operations Owner`, `QA Owner`
**Effective date:** `2026-08-05`  
**Last reviewed:** `2026-08-05`  
**Classification:** `INTERNAL`

---

# 0. Phạm vi thẩm quyền và quan hệ tài liệu

Tài liệu này là nguồn canonical cho:

- Product outcomes của Deal and Transaction Capability.
- Business meanings của Deal, Transaction Case, Proposal, Negotiation, Hold, Booking và Deposit Commitment.
- Transaction-side responsibility, co-sale agreement, commercial approvals, stage gates và contract handoff.
- Capability boundaries, invariants, acceptance outcomes và anti-patterns.
- Đầu vào phân tích cho Transaction Context Implementation Pack.

Tài liệu này không phải nguồn exact cho:

- Physical database schema hoặc DDL.
- Exact API paths, request/response payloads.
- Exact Event names, envelope hoặc payloads.
- Exact permission codes, scopes, masking hoặc role matrix.
- Exact state machines, stage codes, probability formulas hoặc forecast formulas.
- Exact Commercial Lock implementation.
- Exact Payment, Receipt, Refund, Settlement hoặc Revenue calculations.
- Exact document/file storage, provider-delivery runtime hoặc certified Metrics.
- Exact retry, timeout, retention, queue hoặc deployment configuration.

Nguồn exact tương ứng:

| Chủ đề | Nguồn canonical |
|---|---|
| Thuật ngữ | Domain Glossary |
| Product requirements | PRD |
| Context ownership | Source of Truth Matrix |
| Architecture boundaries | Architecture Overview, Context Map và Accepted ADRs |
| Transaction behavior chi tiết | Transaction Context Implementation Pack |
| Database | Transaction Context DB Specification và Alembic migrations |
| API | OpenAPI |
| Events | JSON Schema, AsyncAPI và Event Registry |
| Permissions/scopes/masking | Security registries và matrices |
| Customer/Requirement/Financial Profile | Party Context contracts |
| Listing/Price/Policy/Availability/Lock | Product Context contracts |
| Payment/Receipt/Refund/Settlement | Contract Context contracts |
| Revenue/Commission | Revenue Context contracts |
| Task/Appointment/Interaction | Activity Context contracts |
| Document/File/Signature | Documents Context contracts |
| Provider delivery/external confirmation | Integration Context contracts |
| Certified pipeline/forecast Metrics | Analytics Context và Metric Registry |
| Immutable Audit facts | Audit Context |
| Runtime jobs/incidents | Operations Context |
| Công việc hiện tại | Current Sprint Detailed Execution Pack |

**Capability không đồng nghĩa Bounded Context.** Capability này chủ yếu được thực hiện bởi `transaction` Context. Nó điều phối giao dịch tiền hợp đồng bằng published contracts và Events, nhưng không được direct-write state thuộc `party`, `product`, `contract`, `revenue`, `activity`, `documents`, `integration`, `analytics` hoặc `audit`.

Các phần candidate lifecycle, data model, operations, permissions, Events, screens và reports chỉ là design input. Chúng không được dùng thay machine-readable contracts hoặc Context Packs đã được chấp nhận.

---
# 1. Mục tiêu của capability

Deal and Transaction Capability quản lý quá trình chuyển một nhu cầu và một Listing phù hợp thành giao dịch tiền hợp đồng có kiểm soát.

Capability bắt đầu khi có một hoặc nhiều điều kiện:

- Customer có Requirement đủ điều kiện.
- Sale xác định cơ hội thương mại.
- Customer quan tâm Listing hoặc Shortlist.
- Cần phát hành Proposal.
- Bắt đầu Negotiation hoặc commercial approval.
- Customer yêu cầu Hold.
- Chuẩn bị Booking.
- Phát sinh Deposit Commitment.

Capability kết thúc hoặc bàn giao khi:

- Transaction Case đủ điều kiện handoff sang Contract Context.
- Deal đóng Lost/Cancelled hoặc được đưa về Nurture.
- Hold/Booking hết hiệu lực hoặc bị hủy theo workflow.
- Product Lock được giải phóng/chuyển đổi bởi Product Context.
- Deposit Commitment được xác nhận, điều chỉnh, hoàn trả hoặc xử lý tài chính thông qua Contract Context.
- Customer chuyển sang Listing khác bằng governed change process.

Capability phải trả lời được:

- Customer có những Deal nào và mỗi Deal thuộc context nào.
- Deal, Transaction Case, Hold, Booking và Contract khác nhau như thế nào.
- Listing nào được cân nhắc hoặc selected.
- Proposal/Offer version nào đã được gửi và phản hồi.
- Commercial terms, Price Version và Policy Version nào được sử dụng.
- Approval nào được yêu cầu, đã hết hạn hay đã hoàn tất.
- Product Availability và Commercial Lock hiện hành là gì.
- Booking gồm Buyer/Payer/Representative nào.
- Deposit Commitment là bao nhiêu, đến hạn khi nào và ai là receiver.
- Contract Context đã xác nhận khoản tiền/Receipt/Allocation nào.
- Booking đã đủ điều kiện contract handoff chưa.
- Primary sale, co-sale và responsibilities thay đổi thế nào.
- Toàn bộ quyết định có thể tái tạo từ versions, snapshots, approvals và Events hay không.

Capability phải hỗ trợ:

- Nhiều Transaction Models.
- Một Customer có nhiều Deal.
- Một Deal cân nhắc nhiều Listings.
- Một Deal có nhiều Transaction Cases lịch sử.
- Multi-unit Deal theo approved design.
- Proposal nhiều phiên bản.
- Negotiation nhiều vòng.
- Discount/policy exception và external confirmation.
- Soft Hold, Hard Hold và Booking transition.
- Booking nhiều Buyer/Payer.
- Deposit Commitment, expected-payment request và payment-status projection.
- Product/party change requests.
- Cancellation, reactivation và contract handoff.
- Co-sale, responsibility handover và delegation.
- Maker–checker–approver.
- Multi-Legal Entity.
- Full versioning, traceability và Audit evidence.

Nguyên tắc canonical:

> Deal là cơ hội thương mại; Transaction Case điều phối một giao dịch cụ thể; Hold là business request/process; Product Context sở hữu Availability và Commercial Lock; Booking là cam kết tiền hợp đồng; Deposit Commitment là nghĩa vụ dự kiến; còn Payment, Receipt, Refund, Settlement và Contract thuộc Contract Context.
# 2. Vị trí của capability trong kiến trúc

Transaction Context sử dụng:

- `platform`: Workflow/Approval/SLA definitions, Business Calendar, Numbering và configuration.
- `iam`: authenticated identity, effective access context, delegation và authorization decisions.
- `lead`: attribution/source/care-context references.
- `party`: canonical Customer, Requirement, Financial Profile, Stakeholder, consent và redirect.
- `product`: Project, Asset, Listing, Selling Right, Price, Sales Policy, Availability và Commercial Lock commands/results.
- `matching`: Match Result, Shortlist, Comparison và versioned explanation references.
- `activity`: Task, Appointment, Interaction và operational next-action references.
- `documents`: Proposal/Booking/contract-handoff Document references.
- `integration`: provider delivery, external approval/hold/booking confirmation và transport evidence.
- `contract`: Payment/Receipt/Allocation/Refund/Settlement facts và Contract handoff result.
- `revenue`: downstream commercial facts; Transaction không tính official Revenue/Commission.
- `analytics`: certified pipeline/forecast/conversion projections.
- `audit`: immutable evidence của governed actions.

Transaction Context cung cấp:

- Cho `product`: idempotent commands yêu cầu Availability/Commercial Lock và accepted transaction facts.
- Cho `contract`: Contract handoff package, Booking/Party/Product/Commercial snapshots và Deposit Commitment references.
- Cho `revenue`: approved co-sale/commercial basis references; Revenue Context quyết định entitlement/calculation.
- Cho `matching`: selected/rejected Listing feedback và conversion facts.
- Cho `marketing`: governed conversion facts; Marketing vẫn sở hữu attribution model và campaign semantics.
- Cho `activity`: next-action và operational follow-up references.

Luồng khái quát:

```text
Lead/Customer/Requirement
→ Matching/Shortlist
→ Deal
→ Proposal/Negotiation
→ Transaction Case
→ Hold business process
→ Product Commercial Lock
→ Booking
→ Deposit Commitment
→ Contract-side payment confirmation
→ Contract handoff
```

Không dùng distributed transaction hoặc cross-schema business writes để đồng bộ Transaction với Product, Contract hay Revenue. Mỗi Context commit local transaction, phát durable Outbox Event hoặc trả idempotent command result, rồi dùng Process Manager/reconciliation khi workflow kéo dài.
# 3. Ranh giới sở hữu dữ liệu

## 3.1. Transaction Context sở hữu

- Deal, pipeline, stage/status/health và transaction-side forecast inputs.
- Deal responsibility, participants, handover và co-sale agreement phục vụ giao dịch.
- Deal–Requirement và Deal–Listing references.
- Transaction Case, parties, Product/commercial snapshots, checklist và risks.
- Proposal, Proposal Version, Proposal Item và business delivery/response references.
- Negotiation Thread, Offer/Counteroffer và commercial term proposals.
- Discount/policy-exception/external-commercial-approval requests.
- Hold business record, extension/cancellation requests và Product Lock reference.
- Booking, Booking Version, parties, commercial/product snapshots và change/cancellation requests.
- Deposit Commitment, version, payment instruction intent và expected-payment request.
- Payment/Receipt/Allocation status projection hoặc references nhận từ Contract Context.
- Contract handoff package/process state.
- Transaction-originated business facts và Audit requests.

## 3.2. Transaction Context không sở hữu

- Canonical Party, Customer, Requirement, Financial Profile, Stakeholder, consent hoặc identity verification truth: `party`.
- Listing, Price, Sales Policy, Availability, Commercial Lock hoặc sold state: `product`.
- Match Score, Matching Rule hoặc Shortlist engine: `matching`.
- Task, Appointment, Interaction hoặc canonical Timeline facts: `activity`.
- Contract, Payment Schedule, Receivable, Payment, Allocation, Receipt, Refund hoặc Settlement: `contract`.
- Revenue, Commission entitlement, payout hoặc clawback: `revenue`.
- Campaign, Audience hoặc Attribution model: `marketing`.
- Binary File, Document, Document Version hoặc signature evidence: `documents`.
- Provider transport, external credentials, retries hoặc delivery attempts: `integration`.
- Certified pipeline/forecast/conversion Metrics: `analytics`.
- Immutable Audit facts: `audit`.
- Job, queue, retry/DLQ hoặc incident runtime: `operations`.

## 3.3. Hold và Commercial Lock

Transaction sở hữu Hold business process:

- Business purpose.
- Customer/Deal/Case context.
- Approval state.
- Requested duration.
- Extension/release intent.
- Conflict/result references.

Product sở hữu:

- Authoritative Availability.
- Commercial Lock aggregate.
- Lock concurrency invariant.
- Lock expiry/priority/conversion.
- Product availability recalculation.

Hold chỉ được `ACTIVE` khi Transaction nhận durable Product Lock result phù hợp. Product Lock không được tạo bằng direct database write từ Transaction.

## 3.4. Deposit Commitment và tiền thực nhận

Transaction có thể tạo:

- Deposit Commitment.
- Payment instruction intent.
- Expected-payment request.
- Refund/forfeiture/transfer business request.

Contract Context sở hữu:

- Receivable/payment expectation canonical khi accepted.
- Payment transaction.
- Allocation.
- Receipt.
- Receipt correction/reversal.
- Refund payment.
- Settlement.

Transaction chỉ cập nhật payment-status projection từ authenticated, versioned và idempotently-consumed Contract facts. Không được cho user hoặc frontend tự đặt `PAID/CONFIRMED`.

## 3.5. Proposal delivery và Documents

Transaction sở hữu Proposal business content/version và delivery intent.

`documents` sở hữu generated Document/File/Version.

`integration` sở hữu channel transport, external-message delivery attempts và provider responses.

Transaction chỉ giữ Document references, delivery business status và external evidence references cần thiết.

## 3.6. Co-sale và Commission

Transaction sở hữu co-sale participation/agreement dự kiến và versioned commercial evidence.

Revenue Context sở hữu:

- Commission rules.
- Entitlement.
- Calculation.
- Approval/payment state.
- Adjustment/clawback.

Thay responsibility hoặc handover không tự thay attribution hay Commission entitlement.
# 4. Ba lớp nghiệp vụ chính

## 4.1. Deal

Deal là cơ hội thương mại.

Deal trả lời:

* Customer đang cân nhắc giao dịch gì?
* Giá trị dự kiến là bao nhiêu?
* Giai đoạn bán hàng là gì?
* Ai phụ trách?
* Xác suất và forecast?
* Listing nào đang cân nhắc?
* Việc gì cần làm tiếp?

Deal có thể tồn tại trước khi chọn Listing cụ thể.

## 4.2. Transaction Case

Transaction Case là hồ sơ điều phối một giao dịch cụ thể.

Case trả lời:

* Customer nào đang giao dịch với Listing nào?
* Bên bán và bên mua là ai?
* Mô hình giao dịch nào?
* Giá và chính sách version nào?
* Các phê duyệt nào cần hoàn tất?
* Hold, Booking, đặt cọc và Contract handoff ra sao?

Transaction Case thường được tạo khi:

* Có Listing cụ thể.
* Có Proposal chính thức.
* Bắt đầu đàm phán nghiêm túc.
* Có yêu cầu Hold.
* Chuẩn bị Booking.

## 4.3. Booking

Booking là cam kết mua/đăng ký sản phẩm có kiểm soát.

Booking:

* Không phải hợp đồng mua bán.
* Không tự chứng minh tiền đã thu.
* Không tự chứng minh giao dịch đã hoàn tất.
* Phải gắn với Listing và Transaction Case.
* Có thể có nghĩa vụ đặt cọc.
* Có thể hết hạn hoặc bị hủy.

---

# 5. Mối quan hệ giữa Deal và Transaction Case

## 5.1. Một Deal có thể chưa có Transaction Case

Ví dụ:

* Customer muốn mua căn hộ nhưng chưa chọn sản phẩm.
* Sale đang tư vấn nhiều dự án.
* Deal mới ở giai đoạn discovery.

## 5.2. Một Deal có thể có nhiều Transaction Case lịch sử

Ví dụ:

* Case 1 cho Listing A bị hủy.
* Customer chuyển sang Listing B.
* Case 2 được tạo.

## 5.3. Mặc định một Deal chỉ có một Transaction Case active chính

Nhiều Case active đồng thời chỉ được phép khi:

* Customer thực sự mua nhiều sản phẩm.
* Deal được thiết kế là multi-unit deal.
* Có approval.
* Mỗi Case có Listing riêng.

## 5.4. Một Transaction Case có thể liên kết nhiều Deal

Trong giao dịch phức tạp có thể có:

* Buyer Deal.
* Seller Deal.
* Referral Deal.
* Partner Deal.

MVP có thể sử dụng một primary Deal và các Deal liên quan.

---

# 6. Candidate Transaction Model vocabulary — Context-specific, pending validation

> Exact model codes, required parties, payment flows và guards thuộc Transaction Context Pack.


Capability phải hỗ trợ các mô hình:

```text
SELF_DEVELOPED_PRIMARY
INTERNAL_PROJECT_ENTITY_SALE
THIRD_PARTY_DEVELOPER_DISTRIBUTION
COMPANY_OWNED_RESALE
CUSTOMER_OWNED_RESALE
PARTNER_OWNED_RESALE
LAND_PLOT_PRIMARY
STANDALONE_LAND_RESALE
BROKERAGE_ONLY
INTRODUCTION_ONLY
```

Transaction Model quyết định:

* Bên bán.
* Bên sở hữu.
* Bên ký hợp đồng.
* Bên nhận tiền.
* Bên phê duyệt giá.
* Bên xác nhận Hold.
* Bên phát hành Booking.
* Revenue model.
* Contract workflow.
* Deposit flow.

---

# 7. Candidate Deal Type vocabulary — pending validation

> Exact codes và lifecycle applicability thuộc Transaction machine contracts.


```text
BUYER_PURCHASE
INVESTMENT_PURCHASE
MULTI_UNIT_PURCHASE
RESALE_PURCHASE
LAND_PURCHASE
LEASE
PARTNER_TRANSACTION
OTHER
```

Deal and Transaction Capability tập trung chủ yếu vào giao dịch mua/bán.

Seller acquisition Deal để lấy quyền bán đã được xử lý trong Lead, Party và Product capabilities.

Tuy nhiên Transaction Case phải liên kết được với Seller Objective, Mandate và Listing Acquisition Deal gốc.

---

# 8. Deal Side

```text
BUY_SIDE
SELL_SIDE
DUAL_SIDE
PARTNER_SIDE
```

## 8.1. Buy-side Deal

Công ty đại diện hoặc tư vấn phía người mua.

## 8.2. Sell-side Deal

Công ty đại diện phía chủ tài sản hoặc người bán.

## 8.3. Dual-side

Công ty tham gia cả hai phía, nếu policy và pháp luật cho phép.

Phải:

* Công khai xung đột lợi ích.
* Có consent cần thiết.
* Tách trách nhiệm.
* Áp dụng field access phù hợp.

---

# 9. Nguồn tạo Deal

Deal có thể được tạo từ:

* Lead conversion.
* Requirement.
* Match Result.
* Shortlist.
* Proposal request.
* Listing inquiry.
* Appointment/site visit.
* Customer cũ.
* Referral.
* Approved historical import, khi có phạm vi riêng.
* API.
* Manual create có quyền.

Mỗi Deal phải giữ:

* Source Lead.
* First-touch attribution.
* Last-touch attribution.
* Requirement.
* Matching Run.
* Shortlist.
* Người tạo.
* Ngày tạo.
* Legal Entity.

---

# 10. Điều kiện tạo Deal

Điều kiện tối thiểu:

* Customer canonical hợp lệ.
* Customer không merged source.
* Có Requirement hoặc reason rõ ràng.
* Deal type.
* Deal side.
* Legal Entity.
* Primary responsible user.
* Không có duplicate active Deal trái rule.
* User có quyền.
* Customer context hợp lệ.

Deal chưa có Listing vẫn được tạo.

---

# 11. Kiểm tra Deal trùng

## 11.1. Duplicate Deal Candidate

Có thể dựa trên:

* Customer.
* Requirement.
* Deal side.
* Project.
* Listing.
* Transaction model.
* Active status.
* Time window.

## 11.2. Không tự chặn mọi Deal cùng Customer

Customer có thể:

* Mua nhiều sản phẩm.
* Có nhiều Requirement.
* Có Buyer Deal và Seller Deal.
* Giao dịch ở nhiều Project.

## 11.3. Duplicate active Deal nghiêm trọng

Ví dụ:

* Cùng Customer.
* Cùng Requirement.
* Cùng Listing.
* Cùng Buy-side.
* Cùng thời điểm.

Hệ thống phải cảnh báo hoặc chặn theo policy.

---

# 12. Candidate Deal Pipeline vocabulary — pending validation

> Exact stages, transitions, guards và terminal semantics thuộc Transaction Context Implementation Pack.


## 12.1. Canonical Pipeline Group

```text
DISCOVERY
QUALIFICATION
PRODUCT_SELECTION
PROPOSAL
NEGOTIATION
RESERVATION
BOOKING
DEPOSIT
CONTRACT_PREPARATION
WON
LOST
ON_HOLD
```

## 12.2. Stage đề xuất

```text
NEW
DISCOVERY
REQUIREMENT_CONFIRMED
MATCHING
SHORTLISTED
PROPOSAL_PREPARATION
PROPOSAL_SENT
CUSTOMER_REVIEW
NEGOTIATING
COMMERCIAL_APPROVAL_PENDING
LISTING_SELECTED
HOLD_REQUESTED
HOLD_ACTIVE
BOOKING_PREPARATION
BOOKING_PENDING_APPROVAL
BOOKED
DEPOSIT_PENDING
DEPOSIT_PARTIALLY_PAID
DEPOSIT_CONFIRMED
CONTRACT_PREPARATION
CONTRACT_READY
CLOSED_WON
CLOSED_LOST
NURTURE
PAUSED
CANCELLED
```

## 12.3. Stage không đồng nghĩa Status

Có thể tách:

* `pipeline_stage`.
* `deal_status`.
* `health_status`.
* `forecast_category`.

---

# 13. Candidate Deal status dimensions — pending validation

> Pipeline stage, lifecycle status, health và forecast là các dimensions riêng; exact codes thuộc machine contracts.


```text
ACTIVE
PAUSED
BLOCKED
AT_RISK
WON
LOST
CANCELLED
ARCHIVED
MERGED
```

## 13.1. Health Status

```text
HEALTHY
NEEDS_ATTENTION
STALE
SLA_BREACHED
COMMERCIAL_RISK
LEGAL_RISK
FINANCIAL_RISK
INVENTORY_RISK
```

---

# 14. Stage Gate

Không được đổi stage chỉ bằng cập nhật tự do.

Ví dụ:

## 14.1. SHORTLISTED

Yêu cầu:

* Có Shortlist active.
* Có ít nhất một Listing hợp lệ.
* Customer context hợp lệ.

## 14.2. PROPOSAL_SENT

Yêu cầu:

* Proposal approved nếu policy yêu cầu.
* Có delivery record.
* Giá/policy snapshot.
* Listing access hợp lệ.

## 14.3. NEGOTIATING

Yêu cầu:

* Customer có phản hồi.
* Hoặc Offer được tạo.
* Có Listing cụ thể.

## 14.4. HOLD_ACTIVE

Yêu cầu:

* Commercial Lock active từ Product, Asset, Listing and Inventory Capability.

## 14.5. BOOKED

Yêu cầu:

* Booking approved.
* Booking Lock active.
* Buyer parties xác định.
* Booking terms snapshot.

## 14.6. DEPOSIT_CONFIRMED

Yêu cầu:

* Contract and Cash Capability xác nhận tiền/phiếu thu hợp lệ.
* Deposit Commitment đủ điều kiện.

## 14.7. CONTRACT_READY

Yêu cầu:

* Parties đủ.
* Product snapshot đủ.
* Commercial terms final.
* Deposit status phù hợp.
* Legal checklist phù hợp.

---

# 15. Deal Probability policy inputs

> Probability là operational forecast input, không phải certified prediction. Exact formula/model thuộc approved policy/model version.


Probability có thể lấy từ:

* Stage default.
* Rule.
* Deal health.
* Customer engagement.
* Inventory status.
* Financial readiness.
* Approval status.

## 15.1. Probability không được sửa tùy ý

Có thể cho phép manager override với:

* Reason.
* Before/after.
* Audit.

## 15.2. Probability không được dùng để tự đóng Deal

---

# 16. Candidate Forecast Category vocabulary — pending validation

> Certified forecast semantics và formulas thuộc Analytics Metric Registry; Transaction chỉ giữ operational inputs/category references.


```text
PIPELINE
BEST_CASE
COMMIT
CLOSED
OMITTED
```

Forecast Category có thể dựa trên:

* Stage.
* Expected close date.
* Hold/Booking.
* Deposit.
* Customer confirmation.
* Manager review.

---

# 17. Deal Value

Có thể gồm:

* Estimated gross transaction value.
* Expected selling price.
* Selected Listing price.
* Expected fee/revenue.
* Expected quantity.
* Currency.

Deal Value không phải Revenue chính thức.

Revenue Context tính official Revenue từ accepted Contract/Collection facts.

---

# 18. Expected Close Date

Phải lưu:

* Customer target date.
* Sale forecast date.
* System predicted date nếu có.
* Confidence.
* Last updated.
* Reason.

Quá expected close date phải cảnh báo.

---

# 19. Deal Responsibility

Một Deal có thể có:

* Primary sale.
* Co-sale.
* Team Lead.
* Transaction coordinator.
* Project specialist.
* Financial consultant.
* Legal reviewer.
* Referral participant.
* Partner manager.

Mỗi trách nhiệm có:

* Role.
* User/Party.
* Effective dates.
* Scope.
* Source.
* Status.

---

# 20. Primary Sale

Một Deal chỉ có một primary sale active mặc định.

Thay primary sale phải:

* Qua reassignment/handover workflow.
* Giữ người cũ trong lịch sử.
* Không thay attribution.
* Không tự thay co-sale agreement.
* Không tự thay commission entitlement.

---

# 21. Co-sale

## 21.1. Khái niệm

Co-sale là nhiều sale cùng tham gia một Deal theo thỏa thuận có cấu trúc.

## 21.2. Co-sale không được suy ra chỉ từ Activity

Việc user:

* Gọi Customer.
* Tạo Task.
* Tham gia cuộc họp.
* Hỗ trợ giấy tờ.

không tự tạo quyền co-sale hoặc hoa hồng.

## 21.3. Co-sale Agreement

Phải xác định:

* Primary sale.
* Co-sale participants.
* Vai trò.
* Tỷ lệ hoặc phương pháp phân bổ dự kiến.
* Effective date.
* Điều kiện.
* Lý do.
* Approver.
* Version.
* Status.

## 21.4. Deal and Transaction Capability quản lý thỏa thuận nghiệp vụ

Revenue Context sử dụng approved versioned commercial references và tự quyết định Commission entitlement/calculation.

---

# 22. Co-sale Role

```text
LEAD_OWNER
CUSTOMER_RELATIONSHIP_OWNER
PRODUCT_SPECIALIST
CLOSING_SUPPORT
SELLER_SIDE_AGENT
BUYER_SIDE_AGENT
REFERRAL_AGENT
TRANSACTION_COORDINATOR
OTHER
```

## 22.1. Không ép tổng tỷ lệ hoa hồng trong Deal and Transaction Capability

Deal and Transaction Capability có thể lưu:

* Tỷ lệ dự kiến.
* Rule phân bổ.
* Agreement.

Revenue Context chịu trách nhiệm kiểm tra financial rules và tính Commission.

---

# 23. Co-sale Version và khóa

Khi Deal đạt một milestone cấu hình:

* Hold approved.
* Booking.
* Deposit.
* Contract preparation.

Co-sale agreement có thể được khóa.

Sau khi khóa:

* Không sửa trực tiếp.
* Thay đổi phải tạo adjustment request.
* Có approval.
* Revenue and Commission Capability nhận version mới hoặc delta.

---

# 24. Deal Participant

Deal Participant có thể là:

* Customer chính.
* Co-buyer.
* Payer.
* Co-payer.
* Decision maker.
* End user.
* Representative.
* Guarantor.
* Advisor.
* Referrer.
* Seller.
* Co-seller.
* Owner.
* Co-owner.

Mỗi participant phải liên kết:

* Party.
* Customer nếu có.
* Role.
* Verification.
* Contact permission.
* Effective dates.
* Context.

---

# 25. Stakeholder kế thừa từ Customer 360 Capability

Khi tạo Deal:

* Có thể copy/link Stakeholder Map.
* Không sửa Relationship Graph gốc.
* Tạo Deal Participant riêng.
* Lưu snapshot vai trò tại thời điểm tạo.

Nếu stakeholder thay đổi:

* Cập nhật Deal Participant.
* Không làm mất lịch sử cũ.

---

# 26. Deal Product Candidate

Một Deal có thể cân nhắc nhiều Listing.

Mỗi candidate có:

* Listing.
* Match Result.
* Shortlist Item.
* System rank.
* Sale rank.
* Customer feedback.
* Status.
* Price snapshot reference.
* Availability status.
* Added at.
* Removed at.

---

# 27. Candidate Deal Product status vocabulary — pending validation

> Exact status codes và transitions thuộc Transaction Context Pack.


```text
CONSIDERING
PRIORITY
BACKUP
PROPOSAL_INCLUDED
CUSTOMER_REJECTED
UNAVAILABLE
REPLACED
SELECTED
HOLD_REQUESTED
BOOKED
ARCHIVED
```

Một Deal chỉ có một selected Listing active mặc định, trừ multi-unit Deal.

---

# 28. Chọn Listing chính

Điều kiện:

* Listing còn trong access scope.
* Không archived/withdrawn.
* Mandate phù hợp.
* Có giá/policy hợp lệ.
* Availability được kiểm tra.
* Customer đã thể hiện quan tâm.
* User có quyền.

Việc chọn Listing:

* Không tạo Hold.
* Không đảm bảo còn hàng.
* Không khóa sản phẩm.

---

# 29. Multi-unit Deal

Dùng khi Customer mua nhiều sản phẩm.

Phải có:

* Quantity.
* Nhiều Transaction Case hoặc Case Items.
* Giá từng Listing.
* Policy mua nhiều.
* Buyer allocation.
* Deposit allocation.
* Contract strategy.

MVP có thể hỗ trợ bằng một Deal và nhiều Transaction Case.

---

# 30. Deal Activity và Next Action

Deal phải có:

* Last meaningful interaction.
* Next action.
* Next action due date.
* Responsible user.
* Blocker.
* Customer commitment.
* Manager note.

Active Deal không có next action phải bị cảnh báo.

---

# 31. Deal Aging

Theo dõi:

* Thời gian ở mỗi stage.
* Thời gian không có Activity.
* Thời gian từ Shortlist đến Proposal.
* Proposal đến Negotiation.
* Negotiation đến Hold.
* Hold đến Booking.
* Booking đến Deposit.
* Deposit đến Contract.

---

# 32. Deal Lost

> Lost-reason codes dưới đây là candidate vocabulary; exact registry thuộc Transaction contracts.


## 32.1. Lost Reason

```text
NO_RESPONSE
BUDGET_MISMATCH
FINANCING_FAILED
PRODUCT_NOT_AVAILABLE
PRICE_REJECTED
POLICY_REJECTED
LEGAL_CONCERN
LOCATION_REJECTED
CUSTOMER_POSTPONED
CUSTOMER_BOUGHT_ELSEWHERE
OWNER_REJECTED
DEVELOPER_REJECTED
COMPETITOR_WON
DUPLICATE_DEAL
INVALID_CUSTOMER
CONSENT_WITHDRAWN
OTHER
```

## 32.2. Lost phải có reason

Có thể yêu cầu:

* Competitor.
* Selected alternative.
* Lost notes.
* Effective date.
* Manager review với Deal giá trị lớn.

## 32.3. Closed Lost không xóa dữ liệu

Giữ:

* Proposal.
* Negotiation.
* Hold.
* Booking.
* Source.
* Attribution.
* Activities.
* Feedback.

---

# 33. Deal Won

Deal chỉ `CLOSED_WON` khi milestone cấu hình đạt.

Khuyến nghị:

* Contract đã ký và hợp lệ tại Contract and Cash Capability.
* Hoặc milestone giao dịch khác được cấu hình.

Không nên đóng Won chỉ vì:

* Customer nói đồng ý.
* Hold active.
* Booking created.
* Deposit instruction issued.

---

# 34. Reopen Deal

Có thể khi:

* Customer quay lại.
* Booking bị hủy nhưng Customer chọn Listing khác.
* Deal đóng nhầm.
* Có inventory mới.

Phải:

* Tạo reactivation event.
* Kiểm tra Duplicate Deal.
* Kiểm tra Requirement.
* Tạo stage mới.
* Không sửa lịch sử đóng cũ.

---

# 35. Transaction Case

## 35.1. Mục tiêu

Transaction Case gom các dữ liệu cần thiết cho một giao dịch sản phẩm cụ thể:

* Deal.
* Customer.
* Listing.
* Buyer parties.
* Seller parties.
* Commercial terms.
* Price/policy snapshot.
* Proposal.
* Negotiation.
* Hold.
* Booking.
* Deposit.
* Checklist.
* Approval.
* Contract handoff.

## 35.2. Transaction Case không thay Contract

Case là hồ sơ điều phối trước hợp đồng.

---

# 36. Điều kiện tạo Transaction Case

Có thể tạo khi:

* Listing đã được chọn.
* Proposal có Listing cụ thể.
* Negotiation bắt đầu.
* Customer yêu cầu Hold.
* Sale chuẩn bị Booking.

Bắt buộc có:

* Primary Deal.
* Customer.
* Listing.
* Transaction Model.
* Internal Legal Entity.
* Primary sale.
* Buyer-side context.
* Seller/Mandate context.

---

# 37. Transaction Case Code

Cấp qua Numbering Engine.

Ví dụ:

```text
TXC-2026-000123
```

Case Code không thay Booking Code hoặc Contract Code.

---

# 38. Candidate Transaction Case lifecycle — pending validation

> Exact states, transitions và stage gates thuộc Transaction Context Pack.


```text
DRAFT
PRODUCT_SELECTED
COMMERCIAL_REVIEW
PROPOSAL_ACTIVE
NEGOTIATING
HOLD_PENDING
HOLD_ACTIVE
BOOKING_PREPARATION
BOOKED
DEPOSIT_PENDING
DEPOSIT_CONFIRMED
CONTRACT_PREPARATION
CONTRACT_HANDED_OFF
COMPLETED
PAUSED
CANCELLED
FAILED
```

---

# 39. Transaction Case Party

Các vai trò:

```text
PRIMARY_BUYER
CO_BUYER
PAYER
CO_PAYER
BORROWER
GUARANTOR
AUTHORIZED_REPRESENTATIVE
SELLER
CO_SELLER
OWNER
CO_OWNER
LEGAL_SELLER
PAYMENT_RECEIVER
REVENUE_BENEFICIARY
INTERNAL_LEGAL_ENTITY
DEVELOPER
DISTRIBUTOR
BROKER
REFERRER
```

Mỗi Party phải có:

* Party ID.
* Customer ID nếu có.
* Role.
* Verification.
* Identity snapshot.
* Effective dates.
* Signing expectation.
* Payment obligation expectation.

---

# 40. Xác minh Party trước Booking

Tùy policy, Booking có thể yêu cầu:

* Customer canonical.
* Tên đầy đủ.
* Phone verified.
* Identity information tối thiểu.
* Representative authority.
* Co-buyer confirmation.
* Payer identification.

Không bắt buộc đầy đủ hồ sơ hợp đồng quá sớm nếu policy cho phép.

---

# 41. Transaction Case Product Snapshot

Phải snapshot:

* Project.
* Asset.
* Listing.
* Listing version.
* Mandate.
* Seller.
* Owner.
* Transaction model.
* Internal Legal Entity.
* Payment Receiver.
* Price version.
* Policy version.
* Availability timestamp.
* Legal readiness.
* Physical status.

Snapshot không được sửa âm thầm sau đó.

---

# 42. Transaction Case Checklist

Có thể gồm:

* Customer identity.
* Buyer parties.
* Seller parties.
* Ownership.
* Mandate.
* Listing readiness.
* Price.
* Policy.
* Financial readiness.
* Consent.
* Co-sale.
* Approval.
* Hold.
* Deposit.
* Contract documents.

Checklist có:

* Item.
* Required stage.
* Status.
* Assignee.
* Due date.
* Evidence.
* Waiver.
* Approver.

---

# 43. Proposal

## 43.1. Khái niệm

Proposal là tài liệu hoặc thông điệp thương mại chính thức gửi Customer.

Proposal có thể gồm:

* Một Listing.
* Nhiều Listing.
* Giá.
* Chính sách.
* Ước tính tài chính.
* Lịch thanh toán.
* Điều kiện.
* Hiệu lực.
* Tài liệu đính kèm.

## 43.2. Proposal không phải Offer ràng buộc mặc định

Phải xác định:

* Informational.
* Indicative.
* Negotiable.
* Formal offer.
* Subject to approval.

---

# 44. Candidate Proposal Type vocabulary — pending validation

> Exact codes và legal/commercial semantics thuộc Transaction contracts.


```text
PRODUCT_INTRODUCTION
PRODUCT_COMPARISON
PRICE_PROPOSAL
COMMERCIAL_OFFER
NEGOTIATED_OFFER
BOOKING_INVITATION
REVISED_PROPOSAL
```

---

# 45. Proposal Version

Mọi thay đổi quan trọng phải tạo phiên bản:

* Listing.
* Giá.
* Discount.
* Policy.
* Payment schedule.
* Buyer party.
* Expiry.
* Terms.
* Conditions.

Không sửa Proposal đã gửi.

---

# 46. Candidate Proposal lifecycle — pending validation

> Exact states, transitions và delivery semantics thuộc Transaction Context Pack.


```text
DRAFT
PENDING_REVIEW
PENDING_APPROVAL
APPROVED
READY_TO_SEND
SENT
DELIVERED
VIEWED
CUSTOMER_REVIEWING
ACCEPTED
PARTIALLY_ACCEPTED
REJECTED
EXPIRED
WITHDRAWN
SUPERSEDED
CANCELLED
```

---

# 47. Proposal Item

Mỗi item gồm:

* Listing.
* Match Result.
* Quantity.
* Price snapshot.
* Policy snapshot.
* Tax/fee summary.
* Availability at creation.
* Customer-safe explanation.
* Display order.
* Alternative status.

---

# 48. Proposal Commercial Snapshot

Phải lưu:

* Base price.
* Asking price.
* Discount.
* Policy benefits.
* Estimated total.
* Currency.
* Tax inclusion.
* Fees.
* Payment schedule.
* Assumptions.
* Valid until.
* Approval references.

Không chỉ lưu tổng giá cuối.

---

# 49. Proposal Approval

Có thể yêu cầu khi:

* Giá dưới mức sale được phép.
* Có discount.
* Có policy exception.
* Có floor price impact.
* Có owner/developer confirmation.
* Có điều khoản đặc biệt.
* Có private Listing.
* Có tài liệu nhạy cảm.

---

# 50. Proposal delivery intent, evidence and Integration boundary

> Transaction owns delivery intent/business status; Integration owns channel transport, provider attempts and responses; Documents owns generated files.


Lưu:

* Channel.
* Recipient.
* Sent by.
* Sent at.
* Delivered at.
* Viewed at.
* Failed at.
* External message ID.
* Document reference.
* Proposal version.
* Consent check.
* Contact restriction check.

---

# 51. Proposal Response

Có thể ghi:

* Accepted.
* Rejected.
* Interested.
* Request changes.
* Request negotiation.
* Request hold.
* No response.
* Expired.

Phải lưu:

* Customer/Stakeholder.
* Channel.
* Evidence.
* Occurred at.
* Recorded by.
* Notes.

---

# 52. Proposal hết hạn

Khi hết `valid_until`:

* Không được dùng như giá có hiệu lực.
* Không tự hủy Deal.
* Customer cần Proposal mới hoặc extension.
* Availability phải kiểm tra lại.
* Price/policy phải resolve lại.

---

# 53. Đàm phán

## 53.1. Negotiation Thread

Mỗi Listing hoặc Transaction Case có một hoặc nhiều negotiation thread.

Thread quản lý:

* Buyer offer.
* Seller response.
* Counteroffer.
* Discount.
* Payment schedule.
* Furniture.
* Fees.
* Handover.
* Conditions.

## 53.2. Không sửa Offer cũ

Mỗi vòng tạo Offer Version mới.

---

# 54. Candidate Offer Type vocabulary — pending validation

> Exact offer types và legal effect thuộc Transaction contracts.


```text
BUYER_OFFER
SELLER_OFFER
COUNTER_OFFER
INTERNAL_RECOMMENDATION
FINAL_OFFER
OWNER_CONFIRMATION
DEVELOPER_CONFIRMATION
```

---

# 55. Candidate Offer lifecycle — pending validation

> Exact states and transition guards thuộc Transaction Context Pack.


```text
DRAFT
SUBMITTED
PENDING_INTERNAL_REVIEW
PENDING_OWNER_REVIEW
PENDING_DEVELOPER_REVIEW
APPROVED
COUNTERED
ACCEPTED
REJECTED
EXPIRED
WITHDRAWN
SUPERSEDED
```

---

# 56. Điều khoản đàm phán

Có thể gồm:

* Giá.
* Deposit.
* Booking fee.
* Payment schedule.
* Handover date.
* Furniture.
* Tax/fee allocation.
* Loan condition.
* Document condition.
* Owner repair obligation.
* Due diligence condition.
* Contract signing deadline.
* Refund condition.
* Penalty condition.

Mỗi term phải có:

* Type.
* Proposed value.
* Accepted value.
* Status.
* Party proposing.
* Approval.
* Version.

---

# 57. Discount Request

## 57.1. Loại

* Price discount.
* Fee waiver.
* Gift.
* Additional incentive.
* Payment schedule exception.
* Early payment benefit.
* Special Customer policy.
* Owner net adjustment.

## 57.2. Nội dung

* Requested amount/rate.
* Current price.
* Proposed price.
* Floor price impact.
* Margin/revenue impact theo quyền.
* Customer reason.
* Competitor information.
* Expiry.
* Approver chain.
* Status.

---

# 58. Authority Matrix

Thẩm quyền có thể dựa trên:

* Discount percentage.
* Discount amount.
* Giá dưới floor.
* Transaction value.
* Project.
* Listing type.
* Legal Entity.
* Owner mandate.
* Policy exception.
* Revenue impact.

Ví dụ:

* Sale: trong biên độ cho phép.
* Team Lead: mức 1.
* Department Head: mức 2.
* Director: ngoại lệ cao.
* Owner/developer: điều khoản cần xác nhận ngoài.

---

# 59. Không làm lộ Floor Price

Sale chỉ được biết:

* Có nằm trong quyền hay không.
* Cần cấp duyệt nào.
* Khoảng có thể đề nghị nếu policy cho phép.

Không mặc định trả số Floor Price.

---

# 60. Owner/Developer Confirmation

Trong mô hình bên ngoài, một đề nghị có thể cần:

* Owner confirmation.
* Developer confirmation.
* Master agent confirmation.
* Inventory portal confirmation.

Lưu:

* Request.
* Terms.
* Sent at.
* External reference.
* Response.
* Effective until.
* Evidence.
* Approver.

---

# 61. Offer Acceptance

Customer hoặc seller acceptance không tự:

* Tạo Booking.
* Nhận tiền.
* Chuyển Listing sold.
* Tạo Contract.

Acceptance chỉ tạo điều kiện cho bước tiếp theo.

---

# 62. Hold

## 62.1. Khái niệm

Hold là yêu cầu giữ quyền ưu tiên đối với Listing trong thời gian giới hạn.

Hold business record thuộc Deal and Transaction Capability.

Commercial Lock kỹ thuật thuộc Product, Asset, Listing and Inventory Capability.

## 62.2. Hold không phải Booking

Hold:

* Có thể chưa đủ thông tin Buyer.
* Có thể chưa có deposit.
* Có thời hạn ngắn.
* Có thể bị từ chối bởi nguồn ngoài.

---

# 63. Candidate Hold Type vocabulary — pending validation

> Hold Type là Transaction business vocabulary; Product Lock taxonomy thuộc Product Context contracts.


```text
SOFT_HOLD
HARD_HOLD
EXTERNAL_HOLD
MANAGER_HOLD
CUSTOMER_PRIORITY_HOLD
```

Deal and Transaction Capability map Hold Type sang Commercial Lock Type của Product, Asset, Listing and Inventory Capability.

---

# 64. Điều kiện yêu cầu Hold

Có thể yêu cầu:

* Deal active.
* Transaction Case.
* Customer.
* Listing.
* Primary sale.
* Availability vừa được kiểm tra.
* Listing cho phép Hold.
* User có Project/Listing Access.
* Mandate có Hold Right.
* Giá/policy xác định.
* Customer commitment tối thiểu.
* Không có conflict.

---

# 65. Hold Request Flow

1. Sale chọn Listing.
2. Deal and Transaction Capability kiểm tra quyền.
3. Gọi Product, Asset, Listing and Inventory Capability Availability.
4. Transaction commit Hold Request local và Outbox fact.
5. Chạy approval nếu cần.
6. Gửi idempotent Product Lock command qua published contract.
7. Product tạo Commercial Lock bằng local atomic transaction.
8. Nếu nguồn ngoài, Integration thực hiện external confirmation.
9. Transaction nhận durable result và cập nhật Hold bằng local transaction.
10. Cập nhật Deal/Case.
11. Thông báo.
12. Ghi audit.

---

# 66. Candidate Hold lifecycle — pending validation

> Exact statuses/transitions phải phản ánh durable Product Lock results.


```text
DRAFT
REQUESTED
PENDING_APPROVAL
PENDING_LOCK
PENDING_EXTERNAL_CONFIRMATION
ACTIVE
EXTENSION_PENDING
CONVERTED_TO_BOOKING
REJECTED
CONFLICTED
EXPIRED
RELEASED
CANCELLED
FAILED
```

---

# 67. Hold Expiry

Hold phải có:

* Start.
* Expiry.
* Business Calendar policy nếu áp dụng.
* Reminder.
* Extension count.
* Maximum duration.

Khi hết hạn:

* Product Context expire/release Lock theo Product policy và phát durable fact.
* Deal and Transaction Capability nhận event.
* Hold chuyển `EXPIRED`.
* Deal không tự đóng.
* Alternative có thể được đề xuất.

---

# 68. Hold Extension

Yêu cầu:

* Hold còn active.
* Chưa có competing higher-priority transaction trái policy.
* Customer có tiến triển.
* Chưa vượt số lần.
* Reason.
* Approval.
* External confirmation nếu cần.

Không được gia hạn vô hạn bằng cách tạo Hold mới liên tục.

---

# 69. Hold Conflict

Khi hai request cùng Listing:

* Product Context quyết định Lock bằng authoritative concurrency rules.
* Request thất bại nhận conflict.
* Deal and Transaction Capability lưu conflict.
* Có thể đưa Customer vào waitlist.
* Không tự preempt Hold hiện hữu.

---

# 70. Hold Release

Có thể do:

* Customer từ chối.
* Chọn Listing khác.
* Hết hạn.
* Sale request.
* Manager quyết định.
* Owner/developer từ chối.
* Booking thất bại.
* Legal issue.
* Data conflict.

Release cần:

* Reason.
* Actor.
* Approval nếu lock mạnh.
* Event.
* Audit.

---

# 71. Waitlist

Deal có thể tham gia waitlist khi Listing bị giữ.

Waitlist:

* Không tạo lock.
* Không bảo đảm ưu tiên tuyệt đối.
* Có priority.
* Có expiry.
* Có consent nhận thông báo.
* Không được hiển thị như Hold.

---

# 72. Booking

## 72.1. Khái niệm

Booking là hồ sơ ghi nhận Customer cam kết chọn mua Listing theo điều khoản cụ thể.

Booking phải gắn:

* Transaction Case.
* Deal.
* Listing.
* Customer.
* Buyer parties.
* Giá/policy snapshot.
* Booking Lock.
* Booking validity.
* Deposit terms.

## 72.2. Booking không phải Contract

Booking không thay:

* Hợp đồng đặt cọc pháp lý nếu doanh nghiệp sử dụng.
* Hợp đồng mua bán.
* Chuyển nhượng.
* Phiếu thu.

---

# 73. Điều kiện tạo Booking

1. Transaction Case hợp lệ.
2. Listing selected.
3. Availability phù hợp.
4. Hold active hoặc Booking Lock có thể được tạo trực tiếp.
5. Customer canonical.
6. Buyer parties tối thiểu.
7. Seller/payment flow xác định.
8. Price/policy snapshot.
9. Proposal/Offer accepted nếu policy yêu cầu.
10. Approval hoàn tất.
11. Co-sale agreement ở trạng thái phù hợp.
12. Không có legal blocker.
13. Booking terms xác định.

---

# 74. Booking Code

Cấp qua Numbering Engine.

Ví dụ:

```text
BKG-2026-000456
```

Booking Code unique trong phạm vi cấu hình.

---

# 75. Candidate Booking lifecycle — pending validation

> Exact states, transitions và Contract-handoff guards thuộc Transaction Context Pack.


```text
DRAFT
PENDING_INFORMATION
PENDING_APPROVAL
PENDING_LOCK
PENDING_EXTERNAL_CONFIRMATION
ACTIVE
DEPOSIT_PENDING
DEPOSIT_PARTIALLY_PAID
DEPOSIT_CONFIRMED
CONTRACT_PREPARATION
CONVERTED_TO_CONTRACT
EXPIRED
CANCEL_REQUESTED
CANCELLED
REJECTED
FAILED
```

---

# 76. Booking Version

Mọi thay đổi quan trọng tạo version:

* Buyer parties.
* Listing.
* Giá.
* Policy.
* Deposit amount.
* Payment deadline.
* Booking expiry.
* Seller/payment receiver.
* Commercial terms.

Booking đã deposit confirmed không được sửa trực tiếp.

---

# 77. Booking Parties

Một Booking có thể có:

* Primary buyer.
* Co-buyer.
* Payer.
* Co-payer.
* Representative.
* Borrower.
* Guarantor.

Phải phân biệt:

* Tỷ lệ sở hữu dự kiến.
* Tỷ lệ nghĩa vụ thanh toán dự kiến.
* Tỷ lệ đóng góp dự kiến.

Các tỷ lệ này chưa phải tỷ lệ hợp đồng chính thức.

---

# 78. Buyer Party Validation

Trước Booking active có thể yêu cầu:

* Party tồn tại.
* Customer canonical.
* Không merged source.
* Contact hợp lệ.
* Identity minimum.
* Consent.
* Representative authority nếu có.
* Không có conflict Critical.

---

# 79. Booking Product Snapshot

Phải lưu:

* Asset.
* Listing.
* Listing version.
* Project.
* Unit/plot.
* Transaction model.
* Seller.
* Owner snapshot.
* Mandate.
* Legal Entity.
* Payment Receiver.
* Availability.
* Booking Lock.
* External inventory reference.

---

# 80. Booking Commercial Snapshot

Phải lưu:

* Agreed price.
* Currency.
* Base price.
* Discount.
* Policy benefits.
* Tax/fee components.
* Deposit amount.
* Deposit deadline.
* Payment schedule reference.
* Special terms.
* Approval.
* Price version.
* Policy version.
* Offer version.

---

# 81. Booking Lock

Khi Booking active:

* Commercial Lock phải chuyển thành `BOOKING_LOCK`.
* Lock source phải là Booking.
* Lock không hết hạn trước Booking.
* Booking cancellation phải giải phóng hoặc chuyển lock theo policy.

Không được chỉ đổi Listing status mà không có lock.

---

# 82. Booking Validity

Booking phải có:

* Effective from.
* Expires at.
* Deposit deadline.
* Contract deadline nếu có.
* Grace period.
* Extension policy.

Booking có thể hết hạn khi:

* Không nộp deposit.
* Không hoàn tất hồ sơ.
* Owner/developer từ chối.
* Customer không ký.
* External inventory hết hiệu lực.

---

# 83. Gia hạn Booking

Yêu cầu:

* Booking chưa expired/cancelled.
* Listing Lock còn hợp lệ.
* Deposit status.
* Customer reason.
* Seller/owner approval nếu cần.
* Manager approval.
* New expiry.
* Version mới.

---

# 84. Booking Cancellation

## 84.1. Nguyên nhân

* Customer yêu cầu.
* Không thanh toán.
* Thông tin không hợp lệ.
* Owner/developer từ chối.
* Product unavailable.
* Legal issue.
* Duplicate Booking.
* Chuyển Listing.
* Contract không thể ký.
* Khác.

## 84.2. Cancellation workflow

1. Tạo request.
2. Kiểm tra deposit/receipt.
3. Kiểm tra refund/forfeit policy.
4. Finance review nếu có tiền.
5. Legal review nếu cần.
6. Approval.
7. Cập nhật Booking.
8. Xử lý Commercial Lock.
9. Tạo adjustment/financial instruction cho Contract and Cash Capability.
10. Ghi audit.

Deal and Transaction Capability không tự hoàn tiền.

---

# 85. Booking Rejection

Booking có thể bị từ chối trước khi active:

* Không đủ thông tin.
* Listing unavailable.
* Giá không được duyệt.
* Customer không hợp lệ.
* Owner/developer từ chối.
* Mandate không cho phép.
* Project policy không phù hợp.

Rejection không đồng nghĩa Customer mất Deal.

---

# 86. Chuyển sản phẩm

## 86.1. Trường hợp

* Listing cũ không còn.
* Customer đổi lựa chọn.
* Giá/policy thay đổi.
* Owner rút bán.
* Upgrade/downgrade.

## 86.2. Không sửa Listing ID trực tiếp trên Booking đã active

Phải:

* Tạo Product Change Request.
* Kiểm tra Listing mới.
* Tạo lock mới.
* Xử lý lock cũ.
* Tính chênh lệch.
* Xử lý deposit allocation.
* Approval.
* Tạo Booking version mới hoặc Booking replacement.

---

# 87. Thay đổi người mua

Không được sửa Buyer tùy ý sau Booking.

Phải phân biệt:

* Sửa lỗi dữ liệu.
* Thêm co-buyer.
* Xóa co-buyer.
* Chuyển quyền Booking.
* Thay payer.
* Thay representative.

Mỗi loại có workflow, verification và approval riêng.

---

# 88. Chuyển Booking

Booking transfer có thể cần:

* Chính sách cho phép.
* Customer cũ.
* Customer mới.
* Identity check.
* Owner/developer approval.
* Finance review.
* Tax/fee review.
* Contract impact.
* Deposit transfer instruction.

Không chuyển lịch sử tiền bằng cách sửa Customer ID.

---

# 89. Đặt cọc

## 89.1. Deposit Commitment

Deposit Commitment là nghĩa vụ hoặc cam kết đặt cọc gắn với Booking/Transaction Case.

Gồm:

* Amount.
* Currency.
* Due date.
* Payer.
* Payment Receiver.
* Purpose.
* Refundability.
* Forfeiture rule.
* Applicable agreement.
* Status.
* Version.

## 89.2. Deposit Commitment không phải Receipt

Trạng thái “đã nhận” chỉ được cập nhật từ Contract and Cash Capability.

---

# 90. Candidate Deposit Commitment types — pending validation

> Tên gọi và legal nature phải được phê duyệt theo Transaction Model và Contract policy.


```text
RESERVATION_FEE
BOOKING_FEE
REFUNDABLE_DEPOSIT
NON_REFUNDABLE_DEPOSIT
PURCHASE_DEPOSIT
OWNER_HOLD_DEPOSIT
OTHER
```

Tên pháp lý và bản chất phải cấu hình theo Transaction Model.

---

# 91. Candidate Deposit Commitment/payment projection lifecycle — pending validation

> Payment facts thuộc Contract Context. Transaction statuses chỉ là governed commitment/projection states.


```text
DRAFT
PENDING_APPROVAL
ISSUED
PAYMENT_PENDING
PARTIALLY_PAID
PAID_PENDING_RECONCILIATION
CONFIRMED
OVERDUE
WAIVED
CANCELLED
REFUND_PENDING
REFUNDED
FORFEITED
TRANSFERRED
DISPUTED
```

---

# 92. Deposit Instruction

Có thể gồm:

* Payment amount.
* Bank account.
* Payment method.
* Transfer content.
* Payment reference.
* QR/reference code.
* Due date.
* Payer.
* Receiver.
* Instructions.
* Validity.
* Security warning.

Tài khoản nhận tiền phải lấy từ cấu hình/đối tác hợp lệ, không cho sale tự nhập tùy ý.

---

# 93. Payment Receiver

Phải xác định rõ:

* Internal Legal Entity.
* Developer.
* Owner.
* Partner.
* Escrow account.
* Authorized collector.

Mandate phải cho phép nhận tiền nếu công ty thu.

---

# 94. Expected Payment

Transaction Context có thể gửi idempotent expected-payment request tới Contract Context:

* Booking.
* Deposit Commitment.
* Amount.
* Due date.
* Payer.
* Receiver.
* Reference.
* Allocation purpose.

Contract Context quyết định có chấp nhận và tạo Receivable/Payment Expectation canonical hay không.

---

# 95. Thanh toán một phần

Nếu Contract and Cash Capability báo nhận một phần:

* Deposit chuyển `PARTIALLY_PAID`.
* Booking có thể vẫn `DEPOSIT_PENDING`.
* Lock xử lý theo policy.
* SLA tiếp tục.
* Không tự coi Booking đủ điều kiện Contract.

---

# 96. Deposit Confirmation

Chỉ khi Contract and Cash Capability phát event:

```text
deposit.payment_confirmed
```

hoặc tương đương với:

* Receipt approved.
* Allocation đúng.
* Amount đủ.
* Currency đúng.
* Receiver đúng.
* Không bị reversed.

Deal and Transaction Capability mới chuyển:

* Deposit `CONFIRMED`.
* Booking `DEPOSIT_CONFIRMED`.

---

# 97. Receipt Link

Deal and Transaction Capability lưu reference:

* Receipt ID.
* Payment transaction ID.
* Allocation ID.
* Confirmed amount.
* Confirmed at.
* Finance user.
* Reversal status.

Không sao chép toàn bộ receipt.

---

# 98. Deposit Overdue

Khi quá due date:

* Deposit `OVERDUE`.
* Thông báo sale/manager.
* Booking at risk.
* Có thể hết hạn theo grace period.
* Không tự hủy nếu workflow cần review.
* Không tự giải phóng lock trước quyết định hợp lệ.

---

# 99. Refund và Forfeiture

Transaction Context quản lý transaction-side request/decision intent:

* Refund requested.
* Refund approved.
* Forfeit approved.
* Amount.
* Reason.
* Policy.
* Approver.

Contract Context quyết định và thực hiện financial execution:

* Refund payment.
* Receipt reversal/correction.
* Financial settlement.

---

# 100. Deposit Transfer

Khi đổi Listing hoặc Booking:

* Không sửa receipt.
* Tạo Deposit Transfer Request.
* Xác định source Booking.
* Target Booking.
* Amount.
* Approval.
* Finance allocation adjustment.
* Audit.

---

# 101. Transaction Model – Công ty tự phát triển

Luồng:

```text
Customer
→ Deal
→ Listing của Project nội bộ
→ Proposal
→ Hold
→ Booking
→ Deposit vào Legal Entity nội bộ
→ Contract với Seller Legal Entity
```

Công ty kiểm soát:

* Giá.
* Policy.
* Availability.
* Booking.
* Deposit.
* Contract.

---

# 102. Transaction Model – Phân phối chủ đầu tư ngoài

Luồng:

```text
Customer
→ Deal
→ Listing chủ đầu tư ngoài
→ Internal Proposal
→ External Hold Confirmation
→ Booking
→ Deposit theo Payment Flow
→ Developer Confirmation
→ Contract handoff
```

Cần quản lý:

* External inventory.
* External booking code.
* External confirmation.
* Developer price/policy.
* Bên nhận tiền.
* Thời hạn xác nhận.
* Reconciliation.

---

# 103. Transaction Model – Tài sản công ty sở hữu

Cần xác định:

* Owner Legal Entity.
* Seller Legal Entity.
* Payment Receiver.
* Internal approval.
* Giá tối thiểu.
* Tax/fee.
* Contract type.

---

# 104. Transaction Model – Customer ký gửi

Luồng:

```text
Owner Customer
→ Verified Asset
→ Consignment Mandate
→ Listing
→ Buyer Deal
→ Proposal/Negotiation
→ Owner Confirmation
→ Hold
→ Booking/Deposit
→ Contract
```

Đặc thù:

* Owner net price.
* Brokerage fee.
* Owner approval.
* Co-owner confirmation.
* Deposit receiver.
* Refund/forfeiture authority.
* Seller identity.

---

# 105. Đất nền và đất riêng lẻ

Phải hỗ trợ:

* Plot/parcel identity.
* Multiple owners.
* Legal conditions.
* Infrastructure condition.
* Handover boundary.
* Area adjustment.
* Price per m² và total price.
* Payment schedule.
* Deposit based on estimated/final area.
* Conditions before Contract.

---

# 106. Legal Readiness trước Booking

Tùy Transaction Model, Booking có thể yêu cầu:

* Listing legal readiness.
* Ownership verified.
* Mandate active.
* Co-owner approval.
* Seller identity.
* Transfer eligibility.
* Project sales eligibility.
* No critical encumbrance.
* Required disclosures.

Waiver phải có:

* Reason.
* Authority.
* Effective scope.
* Risk acknowledgement.

---

# 107. Financial Readiness

Deal and Transaction Capability có thể dùng Financial Readiness từ Customer 360 Capability để:

* Cảnh báo.
* Xác định deposit khả thi.
* Đề xuất payment schedule.
* Yêu cầu Finance consultation.

Không tự từ chối Booking chỉ vì readiness thấp, trừ business rule được phê duyệt và hợp lệ.

---

# 108. Consent và Communication

Trước khi gửi:

* Proposal.
* Booking instruction.
* Deposit instruction.
* Reminder.

Phải kiểm tra:

* Contact preference.
* Consent.
* Restriction.
* Authorized recipient.
* Secure channel.

---

# 109. Handover

## 109.1. Nghỉ phép

Có thể delegation:

* Substitute xử lý Task.
* Primary sale giữ attribution.
* Deal responsibility tạm thời.
* Hold/Booking không bị mất.

## 109.2. Chuyển team/nghỉ việc

Phải tạo Handover Case:

* Active Deal.
* Proposal.
* Negotiation.
* Hold.
* Booking.
* Deposit.
* Customer communication.
* External contacts.
* Pending approval.

## 109.3. Không tự thay co-sale/commission

Handover chỉ thay trách nhiệm vận hành, không thay quyền lợi lịch sử.

---

# 110. SLA policy inputs

> Các giá trị dưới đây là recommended baselines để validation, không phải hardcoded SLO/SLA contract.


## 110.1. SLA Deal

* Deal acceptance.
* Requirement confirmation.
* Shortlist review.
* Proposal preparation.
* Proposal follow-up.
* Negotiation response.
* Discount approval.
* Hold confirmation.
* Booking preparation.
* Deposit payment.
* Contract handoff.

## 110.2. Giá trị tham khảo

| Nghiệp vụ                      |                 SLA tham khảo |
| ------------------------------ | ----------------------------: |
| Tạo Proposal từ Shortlist      |           Trong ngày làm việc |
| Phản hồi Customer sau Proposal |               1 ngày làm việc |
| Discount approval nội bộ       |                       1–4 giờ |
| External Hold confirmation     |                     5–30 phút |
| Booking approval               |                   Trong 2 giờ |
| Gửi deposit instruction        |              Ngay sau Booking |
| Deposit follow-up              |                 Theo deadline |
| Contract handoff               | Trong 1 ngày sau đủ điều kiện |

Các SLA definitions lấy từ Platform Configuration và Business Calendar; Activity/owning Context quản lý operational SLA instances theo Context Pack.

---

# 111. Notification

## 111.1. Sale

* Deal mới.
* Deal stale.
* Proposal được duyệt.
* Customer xem Proposal.
* Customer phản hồi.
* Discount được duyệt/từ chối.
* Hold active/sắp hết hạn.
* Hold conflict.
* Booking cần bổ sung.
* Deposit đến hạn/quá hạn.
* Listing thay đổi.
* Booking bị hủy.
* Contract handoff ready.

## 111.2. Team Lead

* Deal không next action.
* Deal quá stage SLA.
* Override bất thường.
* Discount vượt hạn mức.
* Hold kéo dài.
* Booking không deposit.
* Co-sale chưa thống nhất.
* Deal giá trị lớn at risk.

## 111.3. Inventory

* Hold request.
* External confirmation.
* Lock conflict.
* Booking conversion.
* Listing change.
* Product release.

## 111.4. Finance

* Deposit expected.
* Payment received chưa allocate.
* Partial payment.
* Refund request.
* Deposit transfer.
* Deposit dispute.

## 111.5. Legal

* Buyer identity issue.
* Owner/co-owner issue.
* Mandate condition.
* Contract handoff.
* Booking cancellation có legal impact.

---

# 112. Candidate user experiences — không phải frontend contract canonical

> Exact routes, screens, components và responsive behavior thuộc Navigation/IA, Design System và Current Sprint Pack.


## 112.1. Deal List

Bộ lọc:

* Stage.
* Status.
* Health.
* Forecast.
* Expected close.
* Customer.
* Requirement.
* Listing.
* Project.
* Sale.
* Co-sale.
* Legal Entity.
* Hold.
* Booking.
* Deposit.
* Source.
* Lost reason.

## 112.2. Deal Workspace

Các tab:

1. Overview.
2. Customer & Stakeholders.
3. Requirement.
4. Matching & Shortlist.
5. Products.
6. Proposal.
7. Negotiation.
8. Transaction Cases.
9. Hold.
10. Booking.
11. Deposit.
12. Tasks & Activities.
13. Co-sale.
14. Approvals.
15. Documents.
16. Timeline.
17. Audit.

## 112.3. Transaction Case Workspace

* Parties.
* Product snapshot.
* Commercial terms.
* Checklist.
* Proposal.
* Offers.
* Hold.
* Booking.
* Deposit.
* Contract handoff.
* Risks.
* Audit.

## 112.4. Proposal Builder

* Chọn Listing.
* Chọn Match Result.
* Price/policy.
* Comparison.
* Customer-safe explanation.
* Expiry.
* Approval.
* Preview.
* Send.

## 112.5. Negotiation Board

* Offer timeline.
* Term comparison.
* Approvals.
* Owner/developer responses.
* Final agreed terms.

## 112.6. Hold Monitor

* Listing.
* Customer.
* Deal.
* Lock.
* Expiry.
* External status.
* Extension.
* Conflict.
* Waitlist.

## 112.7. Booking Workspace

* Buyer parties.
* Listing.
* Terms.
* Booking Lock.
* Deposit.
* Approvals.
* External references.
* Cancellation/change.
* Contract readiness.

## 112.8. Deposit Monitor

* Commitment.
* Due date.
* Expected amount.
* Received amount.
* Receipt.
* Allocation.
* Overdue.
* Refund/transfer.
* Finance status.

---

# 113. Dashboard cho Sale

* Deal mới.
* Deal cần next action.
* Proposal chờ gửi.
* Proposal chờ phản hồi.
* Negotiation active.
* Hold sắp hết hạn.
* Booking chờ thông tin.
* Deposit đến hạn.
* Deposit quá hạn.
* Contract handoff ready.
* Deal at risk.
* Expected close trong tháng.

---

# 114. Dashboard cho Team Lead

* Pipeline team.
* Stage conversion.
* Deal aging.
* Deal without next action.
* Proposal conversion.
* Discount requests.
* Hold conversion.
* Hold conflict.
* Booking conversion.
* Deposit conversion.
* Co-sale disputes.
* Forecast.
* Lost reason.

---

# 115. Dashboard cho Inventory Manager

* Hold by Listing.
* Booking by Project.
* Lock aging.
* Booking cancellation.
* Product transfer.
* External confirmation SLA.
* Hold-to-booking conversion.
* Inventory released.

Không mặc định xem Customer Financial Profile.

---

# 116. Dashboard cho Finance

* Deposit expected.
* Due today.
* Partial payments.
* Unallocated payments.
* Receipt pending.
* Refund requests.
* Deposit transfers.
* Booking without confirmed payment.

---

# 117. Dashboard cho Director

* Pipeline value.
* Forecast.
* Deal by Legal Entity.
* Deal by Transaction Model.
* Proposal conversion.
* Negotiation conversion.
* Discount impact.
* Hold conversion.
* Booking value.
* Deposit value.
* Cancellation rate.
* Lost reason.
* Project performance.
* Sale/team performance.
* Co-sale activity.
* Average sales cycle.

---

# 118. Candidate analytical questions — không phải certified Metrics

> Exact grain, formulas, snapshots, forecast semantics, certification và access thuộc Analytics Context và Metric Registry.


* Deal pipeline.
* Deal stage aging.
* Deal source.
* Deal by Customer segment.
* Deal by Requirement.
* Deal by Project.
* Deal by Listing.
* Deal by Transaction Model.
* Deal by Legal Entity.
* Deal by sale/team/department.
* Deal value.
* Expected close.
* Forecast.
* Proposal.
* Proposal response.
* Proposal expiry.
* Negotiation rounds.
* Discount request.
* Discount approval.
* Owner/developer confirmation.
* Hold.
* Hold expiry.
* Hold extension.
* Hold conflict.
* Waitlist.
* Booking.
* Booking conversion.
* Booking cancellation.
* Booking product change.
* Deposit commitment.
* Deposit due.
* Deposit partial.
* Deposit confirmed.
* Deposit overdue.
* Refund.
* Deposit transfer.
* Contract handoff.
* Co-sale.
* Lost reason.
* Reopened Deal.
* Sales cycle duration.
* Matching-to-Deal conversion.
* Deal-to-Proposal conversion.
* Proposal-to-Hold.
* Hold-to-Booking.
* Booking-to-Deposit.
* Deposit-to-Contract.

Mọi báo cáo phải drill-down đúng scope.

---

# 119. Candidate data model — không phải physical schema canonical

> **Classification:** `CONTEXT-SPECIFIC DESIGN INPUT / PENDING VALIDATION`
> Exact tables, columns, constraints, indexes và references chỉ có hiệu lực khi được khóa trong Transaction Context DB Specification và Alembic migrations. Cross-context references không mặc định tạo cross-schema business foreign keys.


## 119.1. Deal

### `deals`

* `id`
* `deal_code`
* `enterprise_id`
* `legal_entity_id`
* `customer_id`
* `requirement_id`
* `source_lead_id`
* `deal_type`
* `deal_side`
* `transaction_model`
* `pipeline_stage`
* `canonical_stage_group`
* `status`
* `health_status`
* `forecast_category`
* `probability`
* `currency`
* `estimated_value`
* `expected_close_date`
* `primary_responsible_user_id`
* `primary_team_id`
* `current_transaction_case_id`
* `selected_listing_id`
* `lost_reason_code`
* `won_at`
* `lost_at`
* `created_by`
* `created_at`
* `updated_at`
* `version`

### `deal_stage_history`

* `id`
* `deal_id`
* `from_stage`
* `to_stage`
* `reason`
* `workflow_transition_id`
* `changed_by`
* `changed_at`

### `deal_status_history`

* `id`
* `deal_id`
* `from_status`
* `to_status`
* `reason`
* `changed_by`
* `created_at`

### `deal_attribution_snapshots`

* `id`
* `deal_id`
* `source_lead_id`
* `first_touch_snapshot_json`
* `last_touch_snapshot_json`
* `created_at`

---

## 119.2. Deal Responsibility

### `deal_responsibilities`

* `id`
* `deal_id`
* `user_id`
* `assignment_id`
* `responsibility_role`
* `is_primary`
* `effective_from`
* `effective_to`
* `source_type`
* `source_id`
* `status`
* `created_at`

### `deal_handover_events`

* `id`
* `deal_id`
* `from_user_id`
* `to_user_id`
* `handover_type`
* `reason`
* `effective_at`
* `approval_id`
* `created_at`

---

## 119.3. Co-sale

### `deal_cosale_agreements`

* `id`
* `deal_id`
* `agreement_code`
* `version`
* `allocation_method`
* `status`
* `effective_from`
* `locked_at`
* `created_by`
* `reviewed_by`
* `approved_by`
* `created_at`

### `deal_cosale_participants`

* `id`
* `cosale_agreement_id`
* `user_id`
* `party_id`
* `participant_role`
* `proposed_share_percentage`
* `proposed_share_amount`
* `conditions_json`
* `effective_from`
* `effective_to`
* `status`
* `created_at`

---

## 119.4. Deal Participant

### `deal_participants`

* `id`
* `deal_id`
* `party_id`
* `customer_id`
* `participant_role`
* `verification_status`
* `contact_permission`
* `ownership_percentage_expected`
* `payment_obligation_percentage_expected`
* `financial_contribution_percentage_expected`
* `effective_from`
* `effective_to`
* `status`
* `created_at`

---

## 119.5. Deal Product

### `deal_product_candidates`

* `id`
* `deal_id`
* `listing_id`
* `asset_id`
* `matching_result_id`
* `shortlist_item_id`
* `system_rank`
* `sale_rank`
* `candidate_status`
* `price_snapshot_reference`
* `availability_snapshot_reference`
* `added_by`
* `added_at`
* `removed_at`

---

## 119.6. Transaction Case

### `transaction_cases`

* `id`
* `transaction_case_code`
* `enterprise_id`
* `legal_entity_id`
* `primary_deal_id`
* `customer_id`
* `listing_id`
* `asset_id`
* `transaction_model`
* `status`
* `current_proposal_id`
* `current_negotiation_thread_id`
* `current_hold_id`
* `current_booking_id`
* `commercial_terms_status`
* `legal_readiness_status`
* `financial_readiness_status`
* `contract_handoff_status`
* `created_by`
* `created_at`
* `updated_at`
* `version`

### `transaction_case_deals`

* `id`
* `transaction_case_id`
* `deal_id`
* `relationship_type`
* `is_primary`
* `created_at`

### `transaction_case_parties`

* `id`
* `transaction_case_id`
* `party_id`
* `customer_id`
* `party_role`
* `identity_snapshot_json`
* `verification_status`
* `signing_expectation`
* `payment_expectation`
* `status`
* `created_at`

### `transaction_case_product_snapshots`

* `id`
* `transaction_case_id`
* `listing_id`
* `listing_version`
* `asset_id`
* `project_id`
* `mandate_id`
* `mandate_version`
* `seller_party_id`
* `owner_snapshot_json`
* `internal_legal_entity_id`
* `payment_receiver_party_id`
* `price_list_version_id`
* `price_item_id`
* `sales_policy_version_ids_json`
* `availability_snapshot_id`
* `legal_readiness_snapshot`
* `snapshot_at`
* `created_at`

### `transaction_case_checklist_items`

* `id`
* `transaction_case_id`
* `checklist_code`
* `required_stage`
* `status`
* `assigned_user_id`
* `due_at`
* `evidence_reference`
* `waiver_status`
* `waiver_reason`
* `approved_by`
* `created_at`
* `completed_at`

---

## 119.7. Proposal

### `proposals`

* `id`
* `proposal_code`
* `deal_id`
* `transaction_case_id`
* `customer_id`
* `proposal_type`
* `current_version`
* `status`
* `valid_until`
* `created_by`
* `created_at`
* `updated_at`

### `proposal_versions`

* `id`
* `proposal_id`
* `version`
* `currency`
* `commercial_snapshot_json`
* `payment_schedule_snapshot_json`
* `conditions_json`
* `customer_safe_summary`
* `internal_notes`
* `valid_from`
* `valid_until`
* `status`
* `created_by`
* `reviewed_by`
* `approved_by`
* `created_at`

### `proposal_items`

* `id`
* `proposal_version_id`
* `listing_id`
* `asset_id`
* `matching_result_id`
* `quantity`
* `price_snapshot_json`
* `policy_snapshot_json`
* `availability_snapshot_id`
* `customer_explanation`
* `display_order`
* `created_at`

### `proposal_deliveries`

* `id`
* `proposal_version_id`
* `recipient_party_id`
* `channel`
* `recipient_address_masked`
* `external_message_id`
* `document_id`
* `consent_check_result`
* `sent_by`
* `sent_at`
* `delivered_at`
* `viewed_at`
* `failed_at`
* `status`
* `created_at`

### `proposal_responses`

* `id`
* `proposal_version_id`
* `party_id`
* `response_type`
* `response_details_json`
* `evidence_reference`
* `occurred_at`
* `recorded_by`
* `created_at`

---

## 119.8. Negotiation

### `negotiation_threads`

* `id`
* `transaction_case_id`
* `deal_id`
* `listing_id`
* `status`
* `started_at`
* `closed_at`
* `created_by`
* `created_at`

### `negotiation_offers`

* `id`
* `negotiation_thread_id`
* `offer_code`
* `offer_type`
* `version`
* `proposing_party_id`
* `currency`
* `proposed_price`
* `commercial_terms_json`
* `valid_until`
* `status`
* `previous_offer_id`
* `created_by`
* `submitted_at`
* `accepted_at`
* `rejected_at`
* `created_at`

### `negotiation_term_items`

* `id`
* `negotiation_offer_id`
* `term_type`
* `proposed_value_json`
* `accepted_value_json`
* `status`
* `requires_approval`
* `approval_id`
* `created_at`

### `discount_requests`

* `id`
* `transaction_case_id`
* `deal_id`
* `listing_id`
* `negotiation_offer_id`
* `discount_type`
* `current_price`
* `requested_price`
* `requested_discount_amount`
* `requested_discount_percentage`
* `floor_impact_status`
* `revenue_impact_snapshot`
* `reason`
* `valid_until`
* `status`
* `requested_by`
* `reviewed_by`
* `approved_by`
* `created_at`
* `resolved_at`

### `external_commercial_approvals`

* `id`
* `transaction_case_id`
* `approval_type`
* `external_party_id`
* `request_snapshot_json`
* `external_reference`
* `status`
* `requested_at`
* `responded_at`
* `response_snapshot_json`
* `evidence_reference`
* `created_at`

---

## 119.9. Hold

### `deal_holds`

* `id`
* `hold_code`
* `deal_id`
* `transaction_case_id`
* `customer_id`
* `listing_id`
* `hold_type`
* `commercial_lock_id`
* `status`
* `requested_at`
* `approved_at`
* `started_at`
* `expires_at`
* `extension_count`
* `external_confirmation_status`
* `reason`
* `requested_by`
* `approved_by`
* `released_by`
* `released_at`
* `release_reason`
* `created_at`
* `version`

### `deal_hold_extension_requests`

* `id`
* `hold_id`
* `requested_expires_at`
* `reason`
* `customer_progress_snapshot`
* `status`
* `requested_by`
* `reviewed_by`
* `approved_by`
* `created_at`
* `resolved_at`

### `deal_hold_conflicts`

* `id`
* `listing_id`
* `requesting_deal_id`
* `existing_hold_id`
* `conflict_type`
* `result`
* `created_at`

### `deal_waitlist_entries`

* `id`
* `deal_id`
* `customer_id`
* `listing_id`
* `priority`
* `status`
* `expires_at`
* `created_at`
* `notified_at`

---

## 119.10. Booking

### `bookings`

* `id`
* `booking_code`
* `enterprise_id`
* `legal_entity_id`
* `deal_id`
* `transaction_case_id`
* `customer_id`
* `listing_id`
* `asset_id`
* `transaction_model`
* `current_version`
* `status`
* `commercial_lock_id`
* `external_booking_code`
* `effective_from`
* `expires_at`
* `deposit_due_at`
* `contract_due_at`
* `created_by`
* `approved_by`
* `created_at`
* `updated_at`
* `version`

### `booking_versions`

* `id`
* `booking_id`
* `version`
* `buyer_snapshot_json`
* `product_snapshot_json`
* `commercial_snapshot_json`
* `deposit_terms_snapshot_json`
* `special_conditions_json`
* `effective_from`
* `effective_to`
* `change_reason`
* `created_by`
* `reviewed_by`
* `approved_by`
* `created_at`

### `booking_parties`

* `id`
* `booking_id`
* `party_id`
* `customer_id`
* `booking_party_role`
* `ownership_percentage_expected`
* `payment_obligation_percentage_expected`
* `contribution_percentage_expected`
* `verification_status`
* `status`
* `created_at`

### `booking_status_history`

* `id`
* `booking_id`
* `from_status`
* `to_status`
* `reason`
* `source_type`
* `source_id`
* `changed_by`
* `created_at`

### `booking_cancellation_requests`

* `id`
* `booking_id`
* `reason_code`
* `reason`
* `deposit_impact_status`
* `refund_policy_snapshot`
* `lock_action`
* `status`
* `requested_by`
* `finance_reviewed_by`
* `legal_reviewed_by`
* `approved_by`
* `created_at`
* `resolved_at`

### `booking_change_requests`

* `id`
* `booking_id`
* `change_type`
* `old_snapshot_json`
* `new_snapshot_json`
* `price_difference`
* `deposit_impact_json`
* `status`
* `requested_by`
* `reviewed_by`
* `approved_by`
* `created_at`
* `resolved_at`

---

## 119.11. Deposit

### `deposit_commitments`

* `id`
* `deposit_code`
* `booking_id`
* `transaction_case_id`
* `deal_id`
* `deposit_type`
* `currency`
* `required_amount`
* `confirmed_amount`
* `payer_party_id`
* `payment_receiver_party_id`
* `due_at`
* `refundability_type`
* `forfeiture_policy_snapshot`
* `status`
* `current_version`
* `created_by`
* `approved_by`
* `created_at`
* `updated_at`

### `deposit_commitment_versions`

* `id`
* `deposit_commitment_id`
* `version`
* `terms_snapshot_json`
* `effective_from`
* `change_reason`
* `created_by`
* `approved_by`
* `created_at`

### `deposit_payment_instructions`

* `id`
* `deposit_commitment_id`
* `payment_method`
* `receiver_account_reference`
* `payment_reference_code`
* `transfer_content`
* `instruction_document_id`
* `issued_at`
* `valid_until`
* `status`
* `created_by`
* `created_at`

### `deposit_expected_payments`

* `id`
* `deposit_commitment_id`
* `external_receivable_id`
* `expected_amount`
* `due_at`
* `payer_party_id`
* `receiver_party_id`
* `allocation_purpose`
* `status`
* `created_at`

### `deposit_receipt_links`

* `id`
* `deposit_commitment_id`
* `receipt_id`
* `payment_transaction_id`
* `payment_allocation_id`
* `confirmed_amount`
* `confirmed_at`
* `reversal_status`
* `created_at`

### `deposit_transfer_requests`

* `id`
* `source_deposit_commitment_id`
* `target_booking_id`
* `target_deposit_commitment_id`
* `requested_amount`
* `approved_amount`
* `reason`
* `status`
* `requested_by`
* `finance_reviewed_by`
* `approved_by`
* `created_at`
* `resolved_at`

---

# 120. Candidate application operations — không phải OpenAPI canonical

> Các operations dưới đây là capability inventory. Exact paths, methods, payloads, errors, idempotency và authorization metadata thuộc OpenAPI.


## Deal

```text
GET    /deals
POST   /deals
GET    /deals/{id}
PATCH  /deals/{id}
POST   /deals/{id}/transition
POST   /deals/{id}/pause
POST   /deals/{id}/close-lost
POST   /deals/{id}/reopen
POST   /deals/{id}/archive
GET    /deals/{id}/history
GET    /deals/{id}/access-explanation
```

## Responsibility và Co-sale

```text
GET    /deals/{id}/responsibilities
POST   /deals/{id}/responsibilities
POST   /deal-responsibilities/{id}/end
POST   /deals/{id}/handover

GET    /deals/{id}/cosale-agreements
POST   /deals/{id}/cosale-agreements
PATCH  /deal-cosale-agreements/{id}
POST   /deal-cosale-agreements/{id}/submit-review
POST   /deal-cosale-agreements/{id}/approve
POST   /deal-cosale-agreements/{id}/lock
```

## Participant và Product

```text
GET    /deals/{id}/participants
POST   /deals/{id}/participants
PATCH  /deal-participants/{id}
POST   /deal-participants/{id}/end

GET    /deals/{id}/product-candidates
POST   /deals/{id}/product-candidates
POST   /deal-product-candidates/{id}/select
POST   /deal-product-candidates/{id}/reject
POST   /deal-product-candidates/{id}/remove
```

## Transaction Case

```text
GET    /transaction-cases
POST   /transaction-cases
GET    /transaction-cases/{id}
PATCH  /transaction-cases/{id}
POST   /transaction-cases/{id}/transition
POST   /transaction-cases/{id}/refresh-product-snapshot
POST   /transaction-cases/{id}/validate-readiness
POST   /transaction-cases/{id}/cancel
GET    /transaction-cases/{id}/checklist
POST   /transaction-case-checklist-items/{id}/complete
POST   /transaction-case-checklist-items/{id}/waive
```

## Proposal

```text
GET    /deals/{id}/proposals
POST   /deals/{id}/proposals
GET    /proposals/{id}
POST   /proposals/{id}/versions
GET    /proposal-versions/{id}
POST   /proposal-versions/{id}/validate
POST   /proposal-versions/{id}/submit-review
POST   /proposal-versions/{id}/approve
POST   /proposal-versions/{id}/send
POST   /proposal-versions/{id}/withdraw
POST   /proposal-versions/{id}/responses
```

## Negotiation

```text
GET    /transaction-cases/{id}/negotiations
POST   /transaction-cases/{id}/negotiations
GET    /negotiation-threads/{id}
POST   /negotiation-threads/{id}/offers
GET    /negotiation-offers/{id}
POST   /negotiation-offers/{id}/submit
POST   /negotiation-offers/{id}/accept
POST   /negotiation-offers/{id}/reject
POST   /negotiation-offers/{id}/counter

POST   /transaction-cases/{id}/discount-requests
GET    /discount-requests/{id}
POST   /discount-requests/{id}/review
POST   /discount-requests/{id}/approve
POST   /discount-requests/{id}/reject
```

## Hold

```text
GET    /deals/{id}/holds
POST   /deals/{id}/holds
GET    /deal-holds/{id}
POST   /deal-holds/{id}/submit
POST   /deal-holds/{id}/approve
POST   /deal-holds/{id}/activate-lock
POST   /deal-holds/{id}/extension-requests
POST   /deal-hold-extension-requests/{id}/approve
POST   /deal-holds/{id}/release
POST   /deal-holds/{id}/cancel
POST   /deal-holds/{id}/convert-to-booking
```

## Booking

```text
GET    /bookings
POST   /bookings
GET    /bookings/{id}
PATCH  /bookings/{id}
POST   /bookings/{id}/validate
POST   /bookings/{id}/submit-review
POST   /bookings/{id}/approve
POST   /bookings/{id}/activate
POST   /bookings/{id}/extend
POST   /bookings/{id}/change-requests
POST   /bookings/{id}/cancellation-requests
POST   /booking-cancellation-requests/{id}/approve
POST   /bookings/{id}/handoff-to-contract
GET    /bookings/{id}/history
```

## Deposit

```text
GET    /bookings/{id}/deposit-commitments
POST   /bookings/{id}/deposit-commitments
GET    /deposit-commitments/{id}
POST   /deposit-commitments/{id}/approve
POST   /deposit-commitments/{id}/issue-instruction
POST   /deposit-commitments/{id}/create-expected-payment
POST   /deposit-commitments/{id}/cancel
POST   /deposit-commitments/{id}/refund-requests
POST   /deposit-commitments/{id}/transfer-requests
GET    /deposit-commitments/{id}/receipt-links
```

Backend phải tự enforce:

* Authenticated user.
* Customer context.
* Requirement responsibility.
* Legal Entity.
* Project Access.
* Listing Access.
* Permission.
* Field masking.
* Listing Availability.
* Commercial Lock.
* Mandate.
* Price/Policy version.
* Workflow.
* Approval.
* Consent.
* Idempotency.
* Optimistic version.
* Stage gate.

---

# 121. Candidate permission vocabulary — không phải Permission Registry canonical

> Exact permission codes, scopes, role mappings, concealment, SoD và field masking thuộc security registries/matrices.


## Deal

```text
deal.view
deal.create
deal.update
deal.transition
deal.pause
deal.close_lost
deal.reopen
deal.archive
deal.view_forecast
deal.override_probability
deal.view_audit
deal.export
```

## Responsibility và Co-sale

```text
deal_responsibility.view
deal_responsibility.assign
deal_responsibility.reassign
deal_responsibility.handover

deal_cosale.view
deal_cosale.create
deal_cosale.update
deal_cosale.review
deal_cosale.approve
deal_cosale.lock
deal_cosale.adjust_request
```

## Participant

```text
deal_participant.view
deal_participant.add
deal_participant.update
deal_participant.remove
deal_participant.verify
```

## Transaction Case

```text
transaction_case.view
transaction_case.create
transaction_case.update
transaction_case.transition
transaction_case.validate
transaction_case.cancel
transaction_case.complete_checklist
transaction_case.waive_checklist
transaction_case.view_sensitive
```

## Proposal

```text
proposal.view
proposal.create
proposal.create_version
proposal.update_draft
proposal.review
proposal.approve
proposal.send
proposal.withdraw
proposal.record_response
proposal.view_internal_terms
```

## Negotiation

```text
negotiation.view
negotiation.create
negotiation.offer_create
negotiation.offer_submit
negotiation.offer_accept
negotiation.offer_reject
negotiation.offer_counter

discount_request.create
discount_request.view
discount_request.review
discount_request.approve
discount_request.reject
discount_request.view_floor_impact
```

## Hold

```text
deal_hold.view
deal_hold.request_soft
deal_hold.request_hard
deal_hold.review
deal_hold.approve
deal_hold.activate
deal_hold.extend_request
deal_hold.extend
deal_hold.release
deal_hold.override
deal_hold.view_conflict
```

## Booking

```text
booking.view
booking.create
booking.update_draft
booking.add_party
booking.change_party
booking.validate
booking.review
booking.approve
booking.activate
booking.extend
booking.change_product_request
booking.transfer_request
booking.cancel_request
booking.cancel_approve
booking.handoff_contract
booking.view_audit
```

## Deposit

```text
deposit_commitment.view
deposit_commitment.create
deposit_commitment.update_draft
deposit_commitment.review
deposit_commitment.approve
deposit_instruction.issue
deposit_expected_payment.create
deposit_receipt_link.view
deposit_refund.request
deposit_refund.review
deposit_refund.approve
deposit_transfer.request
deposit_transfer.review
deposit_transfer.approve
```

Các quyền kết hợp với:

```text
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

# 122. Candidate role baseline — không phải Role/Permission Registry canonical

> Role descriptions chỉ mô tả product intent. Backend authority phải được resolve từ IAM/Security canonical sources.


## 122.1. Sale

Được:

* Quản lý Deal của mình.
* Tạo Proposal.
* Tạo Offer.
* Yêu cầu discount.
* Yêu cầu Hold.
* Chuẩn bị Booking.
* Tạo Deposit Commitment theo policy.
* Ghi phản hồi Customer.

Không được:

* Tự duyệt discount vượt quyền.
* Tự thay Floor Price.
* Tự kích hoạt Hold nếu cần approval.
* Tự xác nhận tiền.
* Tự hoàn tiền.
* Tự sửa Booking đã deposit.
* Tự đổi Customer trên Booking.

## 122.2. Team Lead

Được:

* Xem Deal team.
* Review Deal health.
* Duyệt mức thương mại theo authority.
* Review Hold.
* Review Booking.
* Xử lý handover/co-sale trong team.

## 122.3. Department Head

Được:

* Scope department.
* Duyệt ngoại lệ cao hơn.
* Xử lý cross-team.
* Xem forecast.
* Review cancellation.

## 122.4. Inventory Manager

Được:

* Xác nhận availability.
* Quản lý lock.
* External hold.
* Booking inventory status.

Không mặc định được xem Financial Profile chi tiết.

## 122.5. Finance

Được:

* Xem Deposit Commitment.
* Tạo/đối chiếu expected payment.
* Xác nhận receipt từ Contract and Cash Capability.
* Review refund/transfer.

Không được tự thay Deal hoặc Listing.

## 122.6. Legal

Được:

* Review parties.
* Seller/owner.
* Special terms.
* Cancellation.
* Contract handoff.

## 122.7. Director

Được:

* Approve ngoại lệ.
* View `all` theo scope.
* Export có audit.
* Duyệt Deal/Booking giá trị lớn.

---

# 123. Candidate business facts — không phải Event contracts canonical

> Exact Event names, versions, payloads, channels và consumers thuộc JSON Schema, AsyncAPI và Event Registry.


Deal and Transaction Capability phát:

```text
deal.created
deal.updated
deal.stage_changed
deal.responsibility_changed
deal.paused
deal.closed_lost
deal.reopened
deal.closed_won

deal.cosale_agreement_created
deal.cosale_agreement_approved
deal.cosale_agreement_locked

transaction_case.created
transaction_case.product_selected
transaction_case.status_changed
transaction_case.cancelled
transaction_case.contract_ready

proposal.created
proposal.version_created
proposal.approved
proposal.sent
proposal.delivered
proposal.viewed
proposal.accepted
proposal.rejected
proposal.expired
proposal.withdrawn

negotiation.started
negotiation.offer_submitted
negotiation.offer_countered
negotiation.offer_accepted
negotiation.offer_rejected
discount.requested
discount.approved
discount.rejected

deal_hold.requested
deal_hold.approved
deal_hold.activated
deal_hold.extended
deal_hold.conflicted
deal_hold.expired
deal_hold.released
deal_hold.converted_to_booking

booking.created
booking.approved
booking.activated
booking.extended
booking.product_change_requested
booking.party_change_requested
booking.cancel_requested
booking.cancelled
booking.deposit_pending
booking.deposit_confirmed
booking.contract_handoff_ready
booking.converted_to_contract

deposit_commitment.created
deposit_instruction.issued
deposit.payment_expected
deposit.partially_paid
deposit.payment_confirmed
deposit.overdue
deposit.refund_requested
deposit.transfer_requested
deposit.cancelled
```

Consumer phải idempotent.

---

# 124. Candidate Platform configuration references

> Exact configuration keys, schemas, scopes và resolution strategies thuộc Platform Context contracts.


```text
deal.default_workflow
deal.pipeline_definition
deal.stage_gate_policy
deal.duplicate_policy
deal.probability_policy
deal.forecast_policy
deal.aging_policy
deal.lost_reason_policy
deal.reopen_policy

deal.responsibility_policy
deal.handover_policy
deal.cosale_workflow
deal.cosale_lock_policy

transaction_case.workflow
transaction_case.checklist_policy
transaction_case.party_validation_policy
transaction_case.readiness_policy

proposal.workflow
proposal.versioning_policy
proposal.approval_policy
proposal.expiration_policy
proposal.delivery_policy

negotiation.workflow
negotiation.offer_policy
negotiation.discount_authority_policy
negotiation.external_approval_policy

deal_hold.workflow
deal_hold.duration_policy
deal_hold.extension_policy
deal_hold.approval_policy
deal_hold.conflict_policy
deal_hold.waitlist_policy

booking.workflow
booking.party_policy
booking.versioning_policy
booking.expiration_policy
booking.extension_policy
booking.cancellation_policy
booking.change_product_policy
booking.transfer_policy

deposit.workflow
deposit.amount_policy
deposit.payment_instruction_policy
deposit.receiver_policy
deposit.refund_policy
deposit.forfeiture_policy
deposit.transfer_policy
deposit.overdue_policy

deal.notification_policy
deal.sla_policy
deal.export_approval_policy
```

Mỗi configuration definition phải công bố schema, allowed scopes, resolution strategy, owner, version, effective period, approval và Audit requirements khi phù hợp.

---

# 125. System invariant

Các quy tắc sau không được cấu hình tắt:

1. Deal và Transaction Case là hai thực thể khác nhau.
2. Booking và Contract là hai thực thể khác nhau.
3. Deposit Commitment và Receipt là hai thực thể khác nhau.
4. Deal and Transaction Capability không tự xác nhận tiền thực nhận.
5. Hold business record phải tham chiếu Commercial Lock Product, Asset, Listing and Inventory Capability.
6. Booking active phải có Booking Lock hợp lệ.
7. Một Listing không được có hai Booking Lock active trái rule.
8. Booking phải snapshot Listing, Price và Policy version.
9. Proposal đã gửi không được sửa trực tiếp.
10. Offer đã submit không được sửa trực tiếp.
11. Floor Price không được lộ ngoài quyền.
12. Sale không được tự duyệt yêu cầu của chính mình trái SoD.
13. Customer merged source không được tạo Deal/Booking mới.
14. Booking cancellation có tiền phải qua Finance review.
15. Deposit confirmed phải đến từ Contract and Cash Capability.
16. Contract handoff phải có checklist tối thiểu.
17. Handover không tự thay attribution hoặc commission.
18. Co-sale agreement đã khóa không được sửa trực tiếp.
19. Backend phải kiểm tra Availability trước Hold/Booking.
20. Frontend không được tự kết luận Listing available.
21. Stage transition phải qua Workflow Engine.
22. Booking product không được thay bằng edit trực tiếp sau activation.
23. Buyer party không được thay bằng edit trực tiếp sau activation.
24. Deposit receipt không được giả lập từ trạng thái frontend.
25. Audit giao dịch không được sửa.

---

# 126. Rule nghiệp vụ bắt buộc

1. Deal là cơ hội thương mại.
2. Transaction Case là hồ sơ điều phối giao dịch cụ thể.
3. Booking không phải Contract.
4. Deposit Commitment không phải tiền thực nhận.
5. Một Customer có thể có nhiều Deal.
6. Một Requirement có thể có nhiều Deal nếu context khác.
7. Duplicate active Deal phải được cảnh báo.
8. Deal có thể chưa có Listing.
9. Transaction Case phải có Listing.
10. Một Deal mặc định có một Transaction Case active chính.
11. Multi-unit Deal phải được cấu hình rõ.
12. Deal phải có primary sale.
13. Primary sale không phải owner Customer vĩnh viễn.
14. Reassignment giữ lịch sử.
15. Reassignment không đổi attribution.
16. Reassignment không tự đổi commission.
17. Co-sale không được suy ra từ Activity.
18. Co-sale phải có agreement.
19. Co-sale agreement phải có version.
20. Co-sale agreement có thể bị khóa.
21. Participant role phải tách buyer, payer và owner.
22. Payer không mặc định là buyer.
23. Co-buyer không mặc định là payer.
24. Ownership percentage expected chưa phải hợp đồng.
25. Deal Product Candidate không khóa Listing.
26. Selected Listing không khóa Listing.
27. Shortlist không khóa Listing.
28. Stage transition phải qua gate.
29. Deal không có next action phải cảnh báo.
30. Probability không tự đóng Deal.
31. Deal Won không được dựa chỉ trên Hold hoặc Booking.
32. Closed Lost phải có reason.
33. Closed Lost giữ lịch sử.
34. Reopen Deal tạo event mới.
35. Transaction Case phải snapshot product.
36. Snapshot phải có Listing Version.
37. Snapshot phải có Price Version.
38. Snapshot phải có Policy Version.
39. Snapshot phải có Availability timestamp.
40. Transaction Case không thay Contract.
41. Proposal đã gửi không được sửa.
42. Proposal thay đổi phải tạo version.
43. Proposal phải có valid until.
44. Proposal hết hạn không còn là giá hiện hành.
45. Proposal không tự tạo Hold.
46. Proposal delivery phải kiểm tra consent.
47. Proposal Customer-facing không lộ Floor Price.
48. Proposal không lộ Owner contact trái quyền.
49. Proposal response phải có source.
50. Negotiation phải lưu từng vòng.
51. Offer đã submit không sửa trực tiếp.
52. Counteroffer tạo record mới.
53. Offer acceptance không tự tạo Booking.
54. Discount vượt quyền phải approval.
55. Sale không tự duyệt discount của mình trái SoD.
56. Floor Price không được gửi frontend ngoài quyền.
57. Owner/developer approval phải có evidence.
58. Approval hết hạn không được sử dụng.
59. Hold phải có Deal, Customer và Listing.
60. Hold phải kiểm tra Availability.
61. Hold phải kiểm tra Mandate Hold Right.
62. Hold phải kiểm tra Project/Listing Access.
63. Hold phải map tới Commercial Lock.
64. Hold active không được giả lập nếu Lock failed.
65. Hold phải có expiry.
66. Hold không được gia hạn vô hạn.
67. Extension phải có reason.
68. Extension có thể cần owner/developer approval.
69. Hai Hold cùng Listing chỉ một lock độc quyền thành công.
70. Hold conflict không tự preempt.
71. Waitlist không khóa sản phẩm.
72. Waitlist không hiển thị như Hold.
73. Hold hết hạn không tự đóng Deal.
74. Hold release phải có reason.
75. Booking phải gắn Transaction Case.
76. Booking phải gắn Listing.
77. Booking phải có Buyer tối thiểu.
78. Booking phải có Seller/Payment Receiver context.
79. Booking phải có Price/Policy snapshot.
80. Booking active phải có Booking Lock.
81. Booking Code phải unique.
82. Booking phải có expiry.
83. Booking hết hạn không tự xóa.
84. Booking gia hạn phải có version.
85. Booking cancellation không tự hoàn tiền.
86. Booking cancellation có deposit phải Finance review.
87. Booking cancellation không tự chuyển Listing available trước khi xử lý lock.
88. Product change không sửa Listing ID trực tiếp.
89. Product change phải tạo lock mới.
90. Product change phải xử lý lock cũ.
91. Product change phải tính chênh lệch.
92. Buyer change không sửa Customer ID trực tiếp.
93. Buyer change phải identity check.
94. Booking transfer phải workflow.
95. Booking transfer không chuyển receipt bằng update.
96. Deposit Commitment phải có payer.
97. Deposit Commitment phải có receiver.
98. Deposit Commitment phải có amount/currency.
99. Deposit Instruction dùng tài khoản được cấu hình.
100. Sale không tự nhập tài khoản nhận tiền tùy ý.
101. Expected Payment phải gửi Contract and Cash Capability.
102. Partial payment không tự coi confirmed.
103. Deposit confirmed phải có receipt/allocation hợp lệ.
104. Receipt reversal phải cập nhật deposit status.
105. Deposit overdue không tự hủy Booking nếu policy cần review.
106. Refund decision và refund payment là hai bước khác nhau.
107. Deal and Transaction Capability quyết định nghiệp vụ refund.
108. Contract and Cash Capability thực hiện tài chính refund.
109. Deposit transfer phải có source và target.
110. Deposit transfer không sửa receipt.
111. Company-developed transaction phải xác định Seller Legal Entity.
112. Third-party transaction phải xác định external confirmation.
113. Consignment transaction phải xác định owner approval.
114. Owner, Seller và Payment Receiver có thể khác nhau.
115. Land transaction phải snapshot parcel/plot.
116. Legal blocker Critical có thể chặn Booking.
117. Waiver phải có authority.
118. Financial Readiness chỉ hỗ trợ cảnh báo.
119. Matching Score không tự quyết định Booking.
120. Customer consent phải kiểm tra trước gửi thông tin.
121. Deal scope phải backend enforce.
122. Project Access không mở Customer scope.
123. Listing Access không mở Financial Profile.
124. View không đồng nghĩa Export.
125. Sale không bulk export Deal.
126. Team Lead không mặc định bulk export.
127. Floor Price access phải audit theo policy.
128. Deposit information phải field-mask.
129. User inactive không được tạo Hold/Booking.
130. User offboard phải handover active Deal.
131. Handover không làm mất pending approval.
132. Handover không làm mất external reference.
133. Domain event phải có version.
134. Consumer phải idempotent.
135. Same idempotency key cùng payload trả cùng kết quả.
136. Same key khác payload phải conflict.
137. Booking Lock không được hết hạn trước Booking trái rule.
138. Deposit confirmed Booking mới đủ điều kiện stage tương ứng.
139. Contract handoff không tự tạo Contract nếu Contract and Cash Capability từ chối.
140. Audit không được sửa.

---

# 127. Cảnh báo và phát hiện bất thường

Hệ thống cần cảnh báo khi:

* Customer có Deal trùng cùng Listing.
* Deal active không next action.
* Deal ở stage quá lâu.
* Expected close date quá hạn.
* Probability cao nhưng không có Proposal/Hold.
* Closed Won chưa có Contract milestone.
* Co-sale chưa được phê duyệt gần Booking.
* Co-sale bị sửa sau khóa.
* Proposal dùng Price Version hết hiệu lực.
* Proposal dùng Availability stale.
* Proposal gửi ngoài consent.
* Proposal hết hạn vẫn được dùng tạo Hold.
* Offer thấp hơn Floor Price.
* Sale tạo nhiều discount request bất thường.
* Người yêu cầu tự duyệt.
* Owner/developer approval hết hạn.
* Hold active nhưng Commercial Lock không active.
* Commercial Lock active nhưng Hold không tồn tại.
* Hold sắp hết hạn.
* Hold gia hạn quá nhiều.
* Một sale giữ quá nhiều Listing.
* Hold không có Customer activity.
* Hai Booking cùng Listing.
* Booking active nhưng không có Booking Lock.
* Booking Lock hết hạn trước Booking.
* Booking thiếu primary buyer.
* Booking có merged Customer.
* Booking thiếu Price Version.
* Booking thiếu Payment Receiver.
* Booking deposit overdue.
* Deposit confirmed không có Receipt.
* Receipt reversed nhưng Booking vẫn confirmed.
* Deposit amount khác confirmed amount.
* Payer khác Receipt payer không được giải thích.
* Refund approved nhưng chưa thực hiện quá SLA.
* Deposit transfer không có target Booking.
* Booking cancelled nhưng Lock chưa release.
* Listing sold nhưng Booking khác vẫn active.
* External developer status mâu thuẫn Booking.
* Product change chưa giải phóng Listing cũ.
* Buyer change không identity check.
* Contract handoff thiếu checklist.
* User offboard còn active Hold/Booking.
* Floor Price bị truy cập hàng loạt.
* Export Deal bất thường.
* Proposal Customer-facing chứa internal margin.
* Transaction Case snapshot không đủ version.
* Same idempotency key khác payload.
* Event Deposit đến trước Booking bất thường.
* Deal stage không khớp Booking/Deposit status.

---

# 128. Audit requirements và evidence

> Audit Context sở hữu immutable Audit facts. Transaction Context phát sinh audit-worthy facts/references; operational logs không thay Audit.


## 128.1. Thao tác bắt buộc

* Tạo/update Deal.
* Stage transition.
* Probability override.
* Close Lost/Reopen.
* Assignment/Handover.
* Co-sale create/update/approve/lock.
* Participant add/change.
* Select Listing.
* Create Transaction Case.
* Product snapshot.
* Checklist waiver.
* Proposal create/version/approve/send/withdraw.
* Proposal response.
* Offer create/submit/counter/accept/reject.
* Discount request/review/approve.
* External approval.
* Hold request/approve/activate/extend/release.
* Hold conflict.
* Booking create/version/approve/activate/extend.
* Booking party/product change.
* Booking cancellation.
* Deposit create/approve/instruction.
* Expected payment.
* Receipt confirmation event.
* Refund/transfer request.
* Contract handoff.
* Sensitive price access.
* Export.

## 128.2. Nội dung

* Actor.
* Role.
* Legal Entity.
* Customer.
* Deal.
* Transaction Case.
* Listing.
* Booking.
* Deposit.
* Price/Policy Version.
* Commercial Lock.
* Before.
* After.
* Reason.
* Approval.
* Workflow version.
* IP.
* Device.
* Request ID.
* Correlation ID.
* Idempotency key.
* Timestamp.
* Result.

---

# 129. Phạm vi MVP

## 129.1. Bắt buộc

* Deal.
* Deal pipeline.
* Stage history.
* Deal status/health.
* Probability/forecast cơ bản.
* Deal responsibility.
* Deal participant.
* Co-sale agreement cơ bản.
* Deal Product Candidates.
* Selected Listing.
* Transaction Case.
* Product snapshot.
* Party snapshot.
* Checklist.
* Proposal.
* Proposal version.
* Proposal delivery.
* Proposal response.
* Negotiation thread.
* Offer/counteroffer.
* Discount request.
* Owner/developer confirmation.
* Soft Hold.
* Hard Hold.
* Commercial Lock integration.
* Hold expiry.
* Hold extension.
* Hold conflict.
* Waitlist.
* Booking.
* Booking version.
* Multiple buyers.
* Booking Lock.
* Booking expiry.
* Booking cancellation.
* Product change request.
* Deposit Commitment.
* Deposit Instruction.
* Expected Payment.
* Partial/confirmed status from Contract and Cash Capability.
* Refund request.
* Contract handoff.
* Scope.
* Field masking.
* Audit.
* Dashboard.
* Alerts.
* Domain events.

## 129.2. Giai đoạn nâng cao

* Multi-unit Deal nâng cao.
* Digital Proposal portal.
* Electronic acceptance.
* Advanced negotiation matrix.
* Automated approval routing.
* Real-time developer booking API.
* Customer self-service Booking.
* Digital deposit agreement.
* Escrow integration.
* Advanced deal scoring.
* AI Deal summary.
* AI next-best action.
* AI negotiation assistant.
* Advanced forecast.
* Dynamic discount recommendation.
* Competitive offer tracking.
* Complex Booking transfer.
* Multi-currency deposit.
* Package/product bundle.
* Auction/bidding.
* Legal e-sign integration.

---

# 130. Tiêu chí nghiệm thu

Capability được xem là đạt khi:

1. Tạo được Deal từ Requirement.
2. Tạo được Deal từ Match Result.
3. Tạo được Deal từ Shortlist.
4. Deal giữ source Lead.
5. Deal giữ attribution.
6. Deal có Legal Entity.
7. Deal có primary sale.
8. Deal có pipeline stage.
9. Deal có status.
10. Deal có health status.
11. Deal có forecast category.
12. Deal có probability.
13. Deal có expected close date.
14. Deal có value estimate.
15. Duplicate Deal được cảnh báo.
16. Customer có nhiều Deal khác context.
17. Deal chưa có Listing vẫn tồn tại.
18. Stage transition qua Workflow.
19. Stage gate chặn transition thiếu điều kiện.
20. Stage history được lưu.
21. Deal không next action được cảnh báo.
22. Deal aging được tính.
23. Close Lost bắt buộc reason.
24. Closed Lost giữ dữ liệu.
25. Reopen tạo event mới.
26. Closed Won không chỉ dựa Booking.
27. Deal responsibility có lịch sử.
28. Reassignment không đổi attribution.
29. Handover hoạt động.
30. Co-sale Agreement được tạo.
31. Co-sale có participants.
32. Co-sale có version.
33. Co-sale cần approval.
34. Co-sale được khóa.
35. Activity không tự tạo co-sale.
36. Tạo được Deal Participant.
37. Buyer và Payer tách biệt.
38. Co-buyer được hỗ trợ.
39. Expected ownership/payment ratio được lưu.
40. Tạo được Product Candidate.
41. Link được Match Result.
42. Chọn được selected Listing.
43. Chọn Listing không tạo Hold.
44. Tạo được Transaction Case.
45. Case có Deal.
46. Case có Customer.
47. Case có Listing.
48. Case có Transaction Model.
49. Case có parties.
50. Case có product snapshot.
51. Snapshot lưu Listing Version.
52. Snapshot lưu Price Version.
53. Snapshot lưu Policy Version.
54. Snapshot lưu Availability.
55. Case có checklist.
56. Checklist có assignee/due date.
57. Checklist waiver có approval.
58. Tạo được Proposal.
59. Proposal có version.
60. Proposal có nhiều Listing.
61. Proposal lưu price snapshot.
62. Proposal lưu policy snapshot.
63. Proposal có valid until.
64. Proposal approval hoạt động.
65. Proposal được gửi.
66. Delivery status được lưu.
67. Consent được kiểm tra.
68. Proposal đã gửi không sửa trực tiếp.
69. Proposal mới tạo version.
70. Proposal response được ghi.
71. Proposal hết hạn được cảnh báo.
72. Tạo được Negotiation Thread.
73. Tạo được Buyer Offer.
74. Tạo được Counteroffer.
75. Offer đã submit không sửa.
76. Offer có valid until.
77. Offer acceptance không tự Booking.
78. Tạo được Discount Request.
79. Authority Matrix hoạt động.
80. Sale không tự duyệt vượt quyền.
81. Floor Price không lộ ngoài quyền.
82. Owner confirmation được lưu.
83. Developer confirmation được lưu.
84. External approval có evidence.
85. Tạo được Soft Hold.
86. Tạo được Hard Hold.
87. Hold kiểm tra Availability.
88. Hold kiểm tra Mandate.
89. Hold kiểm tra Project Access.
90. Hold gọi Product, Asset, Listing and Inventory Capability tạo Lock.
91. Lock thành công thì Hold active.
92. Lock thất bại thì Hold không active.
93. Hold có expiry.
94. Hold sắp hết hạn có notification.
95. Hold hết hạn nhận event.
96. Hold extension có reason.
97. Extension có approval.
98. Không gia hạn quá policy.
99. Hai request đồng thời chỉ một Hold active.
100. Hold conflict được lưu.
101. Waitlist không tạo lock.
102. Waitlist có priority.
103. Release Hold hoạt động.
104. Release có reason.
105. Tạo được Booking từ Hold.
106. Tạo được Booking trực tiếp khi policy cho phép.
107. Booking có Booking Code.
108. Booking có Customer.
109. Booking có Listing.
110. Booking có Transaction Case.
111. Booking có Transaction Model.
112. Booking có version.
113. Booking có Buyer parties.
114. Booking hỗ trợ nhiều buyer.
115. Booking hỗ trợ Payer riêng.
116. Booking lưu expected ownership ratio.
117. Booking lưu product snapshot.
118. Booking lưu commercial snapshot.
119. Booking lưu Price Version.
120. Booking lưu Policy Version.
121. Booking active cần Booking Lock.
122. Booking có expiry.
123. Booking có deposit due date.
124. Booking approval hoạt động.
125. Booking external confirmation hoạt động.
126. Booking extension tạo version.
127. Booking hết hạn được xử lý.
128. Booking cancellation request được tạo.
129. Booking có deposit cần Finance review khi cancel.
130. Cancellation không tự hoàn tiền.
131. Cancellation xử lý Lock đúng.
132. Product Change Request được tạo.
133. Product change kiểm tra Listing mới.
134. Product change tạo Lock mới.
135. Product change xử lý Lock cũ.
136. Product change tính chênh lệch.
137. Buyer Change Request được tạo.
138. Buyer mới identity check.
139. Booking transfer có workflow.
140. Booking transfer không sửa Customer ID trực tiếp.
141. Tạo được Deposit Commitment.
142. Deposit có type.
143. Deposit có amount/currency.
144. Deposit có payer.
145. Deposit có receiver.
146. Deposit có due date.
147. Deposit có refundability.
148. Deposit Instruction được tạo.
149. Account receiver lấy từ cấu hình.
150. Sale không tự nhập tài khoản trái quyền.
151. Expected Payment được gửi Contract and Cash Capability.
152. Partial payment cập nhật đúng.
153. Partial không thành Confirmed.
154. Receipt approved cập nhật Deposit Confirmed.
155. Deposit Confirmed có Receipt Link.
156. Receipt reversal cập nhật lại trạng thái.
157. Deposit Overdue được cảnh báo.
158. Booking không tự hủy trước workflow.
159. Refund Request được tạo.
160. Refund approval tách refund payment.
161. Deposit Transfer Request được tạo.
162. Transfer có source/target.
163. Transfer không sửa receipt.
164. Công ty tự phát triển được hỗ trợ.
165. Phân phối chủ đầu tư ngoài được hỗ trợ.
166. Tài sản công ty sở hữu được hỗ trợ.
167. Customer ký gửi được hỗ trợ.
168. Đất nền dự án được hỗ trợ.
169. Đất riêng lẻ được hỗ trợ.
170. Owner, Seller và Receiver tách biệt.
171. Co-owner được hỗ trợ.
172. Legal blocker chặn Booking theo rule.
173. Financial Readiness chỉ cảnh báo.
174. Handover không mất Hold.
175. Handover không mất Booking.
176. Handover không đổi attribution.
177. Handover không tự đổi commission.
178. Sale chỉ xem `mine`.
179. Team Lead xem `team`.
180. Department Head xem `department`.
181. Director xem `all` theo quyền.
182. Backend enforce scope.
183. Sửa URL không mở rộng quyền.
184. Project Access không mở Customer context.
185. Listing Access không mở Financial detail.
186. Field masking hoạt động.
187. Sale không bulk export Deal.
188. Sensitive price access có audit.
189. Deal dashboard drill-down đúng scope.
190. Finance dashboard chỉ hiển thị dữ liệu được phép.
191. Audit lưu before/after.
192. Audit lưu approval.
193. Audit lưu Price/Policy Version.
194. Audit lưu Commercial Lock.
195. Idempotency hoạt động.
196. Same key khác payload báo conflict.
197. Domain events được phát.
198. Event consumer idempotent.
199. Contract handoff gửi đủ snapshot cho Contract and Cash Capability.
200. Capability chuyển cơ hội tư vấn thành giao dịch có kiểm soát mà không tự thay thế Contract hoặc Finance.

---

# 131. Quan hệ canonical với các Context liên quan

## 131.1. Lead Context

Transaction giữ source/attribution references đã được công bố.

Transaction không tạo Lead ownership, care protection hoặc assignment mới bằng cách cập nhật Deal.

## 131.2. Party Context

Transaction sử dụng canonical Customer, Requirement, Financial Profile, Stakeholder và consent qua published contracts.

Transaction không ghi đè Requirement, Financial Profile hoặc Party Identity. Customer redirect phải được xử lý theo Party contract.

## 131.3. Product Context

Transaction bắt buộc sử dụng Product contracts cho:

- Listing và Selling Right.
- Listing/Price/Policy versions.
- Availability.
- Commercial Lock.
- Product-side sold/unavailable facts.

Transaction không lưu Availability như source of truth và không direct-write Product status.

## 131.4. Matching Context

Transaction tiếp nhận Match Result, Shortlist, Comparison và explanation references.

Transaction không sửa System Score hoặc Matching Rule.

## 131.5. Contract Context

Transaction gửi versioned handoff package và Deposit Commitment references.

Contract Context quyết định Contract creation, Receivable, Payment, Receipt, Allocation, Refund và Settlement. Transaction không giả lập các facts này.

## 131.6. Revenue Context

Transaction cung cấp commercial/co-sale snapshots cần thiết.

Revenue Context quyết định official Revenue và Commission. Deal Value hoặc proposed co-sale share không phải financial entitlement.

---

# 132. Anti-patterns và canonical requirements

## AP-TRA-001 — Gộp Deal, Booking và Contract vào một record

**Không được áp dụng**

Một record duy nhất vừa thể hiện opportunity, product transaction, reservation, contract và payment.

**Canonical requirement**

Deal, Transaction Case, Hold, Booking, Deposit Commitment và Contract là các aggregates/concepts riêng, có lifecycle và ownership riêng.

## AP-TRA-002 — Booking đồng nghĩa Sold hoặc Contract

**Không được áp dụng**

Khi Booking active thì tự đánh dấu Listing sold hoặc Deal won.

**Canonical requirement**

Booking là pre-contract commitment. Product sold state và Deal Won phải dựa trên accepted Product/Contract milestones theo policy.

## AP-TRA-003 — Đánh dấu đã cọc thủ công

**Không được áp dụng**

Sale/frontend chỉnh trạng thái Deposit thành `CONFIRMED`.

**Canonical requirement**

Deposit/payment projection chỉ được cập nhật từ authenticated Contract facts về Payment, Receipt và Allocation, với idempotency và reversal handling.

## AP-TRA-004 — Hold chỉ là một status field

**Không được áp dụng**

Transaction đổi stage thành Hold mà không có Product Commercial Lock.

**Canonical requirement**

Hold business record phải tham chiếu durable Product Lock result; Product Context bảo vệ concurrency và Availability.

## AP-TRA-005 — Distributed transaction xuyên Product/Contract

**Không được áp dụng**

Giữ một database transaction xuyên Hold, Commercial Lock, Booking, Receivable và Receipt.

**Canonical requirement**

Mỗi Context dùng local transaction, Transactional Outbox, idempotent commands/consumers, Process Manager và reconciliation.

## AP-TRA-006 — Proposal/Offer đã gửi vẫn sửa tại chỗ

**Không được áp dụng**

Ghi đè giá, terms hoặc expiry của Proposal/Offer đã phát hành.

**Canonical requirement**

Mọi thay đổi material tạo version/record mới; bản cũ giữ nguyên để tái tạo lịch sử.

## AP-TRA-007 — Sale nhập giá/tài khoản tùy ý

**Không được áp dụng**

Sale tự nhập Floor Price, receiver account hoặc commercial terms ngoài authority.

**Canonical requirement**

Giá/policy dùng approved Product versions; receiver/payment instructions dùng verified Contract/Platform/Partner references; exceptions đi qua Authority Matrix và SoD.

## AP-TRA-008 — Selected Listing hoặc Shortlist tự khóa sản phẩm

**Không được áp dụng**

Chọn Listing, tạo Proposal hoặc thêm Shortlist làm mất Availability.

**Canonical requirement**

Chỉ Product Commercial Lock hợp lệ mới thay đổi Product availability.

## AP-TRA-009 — Booking change bằng sửa trực tiếp IDs

**Không được áp dụng**

Sửa `listing_id`, `customer_id`, Buyer hoặc Payer trực tiếp trên Booking active.

**Canonical requirement**

Product/party changes dùng governed request, identity checks, lock transition, financial-impact review, versioning và Audit.

## AP-TRA-010 — Cancellation tự refund hoặc giải phóng mọi state

**Không được áp dụng**

Hủy Booking tự hoàn tiền, sửa Receipt hoặc giải phóng Product Lock trước khi decision/process hoàn tất.

**Canonical requirement**

Cancellation orchestration phải phân tách business decision, Product Lock action và Contract-side Refund/Settlement execution.

## AP-TRA-011 — Co-sale suy ra từ Activity

**Không được áp dụng**

User gọi điện, tham dự cuộc họp hoặc tạo Task thì tự có Commission share.

**Canonical requirement**

Co-sale phải có versioned agreement, role, conditions và approval. Revenue Context quyết định entitlement.

## AP-TRA-012 — Handover thay attribution/Commission

**Không được áp dụng**

Đổi primary responsible user tự chuyển source attribution hoặc quyền lợi tài chính.

**Canonical requirement**

Operational responsibility, attribution và financial entitlement là các dimensions riêng; mỗi thay đổi đi qua owning Context.

## AP-TRA-013 — Frontend tự đổi stage hoặc scope

**Không được áp dụng**

Frontend gửi stage/status/scope rộng hơn để bypass guards.

**Canonical requirement**

Backend resolve effective scope, thực thi command và stage gates tại trusted boundary.

## AP-TRA-014 — Proposal delivery sở hữu provider transport

**Không được áp dụng**

Transaction lưu credentials, raw provider retries hoặc coi external message ID là delivery truth duy nhất.

**Canonical requirement**

Integration sở hữu transport runtime. Transaction giữ delivery intent/result references và business status.

## AP-TRA-015 — Document URL là Proposal evidence canonical

**Không được áp dụng**

Lưu permanent URL như nguồn Proposal/Booking document cuối cùng.

**Canonical requirement**

Documents Context sở hữu File/Document/Version; Transaction giữ `document_id` và approved evidence references.

## AP-TRA-016 — Deal pipeline tables là certified analytics

**Không được áp dụng**

Dùng operational Deal records làm nguồn KPI/forecast cuối cùng mà không có semantic definition và snapshot.

**Canonical requirement**

Transaction phát governed facts; Analytics Context sở hữu certified pipeline, forecast, conversion và historical Metrics.

## AP-TRA-017 — Candidate examples là exact contracts

**Không được áp dụng**

Dùng table names, endpoints, statuses, Events hoặc permissions trong tài liệu này để code trực tiếp.

**Canonical requirement**

Exact database, API, Event, lifecycle, permission và error contracts phải được khóa trong nguồn canonical tương ứng.

## AP-TRA-018 — Mặc định tồn tại hệ thống tiền nhiệm

**Không được áp dụng**

Tự thiết kế old-stage aliases, compatibility layer hoặc migration mapping khi chưa có approved scope.

**Canonical requirement**

`crm_bds_ai` là Greenfield. Historical import hoặc migration chỉ tồn tại khi có scope, mapping, security review, reconciliation và acceptance criteria riêng.

---

# 133. Kết luận

Deal and Transaction Capability điều phối cơ hội bán hàng và giao dịch tiền hợp đồng của `crm_bds_ai`.

Capability phải bảo đảm:

- Deal khác Transaction Case.
- Hold business process khác Product Commercial Lock.
- Booking khác Contract.
- Deposit Commitment khác Payment/Receipt.
- Customer/Requirement truth vẫn thuộc Party Context.
- Availability/Commercial Lock vẫn thuộc Product Context.
- Payment/Receipt/Refund/Settlement vẫn thuộc Contract Context.
- Revenue/Commission vẫn thuộc Revenue Context.
- Proposal và Offer có immutable version history.
- Commercial exceptions đi qua Authority Matrix và SoD.
- Booking luôn có parties, Product/commercial snapshots và Product Lock phù hợp.
- Deposit status không thể được xác nhận thủ công.
- Product/Buyer changes và cancellation có governed workflows.
- Co-sale có version; Activity không tự tạo entitlement.
- Handover không tự thay attribution hoặc Commission.
- Cross-context orchestration dùng local transactions, Outbox, idempotency và reconciliation.
- Contract handoff có đầy đủ snapshots, approvals, evidence và traceability.
- Certified pipeline/forecast Metrics thuộc Analytics.
- Immutable Audit facts thuộc Audit Context.

> Transaction Context điều phối cam kết tiền hợp đồng; nó không sở hữu Product availability, tiền thực nhận, Contract hoặc Revenue.
