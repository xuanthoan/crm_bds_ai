# CRM_BDS_AI — CAPABILITY 07: CUSTOMER–PRODUCT MATCHING

## Recommendation, Shortlist, Comparison, Reverse Matching and Explainable Decision Support

**Document ID:** `PROD-CAP-MAT-001`
**Canonical path:** `docs/product/capabilities/cap-07-matching.md`
**Product:** `crm_bds_ai`
**Version:** `1.0.0`  
**Status:** `Accepted / Product Capability Baseline`
**Document type:** `Product Capability Specification`
**Primary capability code:** `CAP-MAT`
**Primary owning Context:** `matching`
**Owner:** `Product Owner`
**Co-owner:** `Matching Domain Owner`
**Reviewers:** `Architecture Owner`, `Party Domain Owner`, `Product Domain Owner`, `Transaction Domain Owner`, `Activity Domain Owner`, `Marketing Domain Owner`, `Analytics Domain Owner`, `Security Owner`, `Database Owner`, `API Owner`, `Event Architecture Owner`, `AI Governance Owner`, `Operations Owner`, `QA Owner`
**Effective date:** `2026-08-05`  
**Last reviewed:** `2026-08-05`  
**Classification:** `INTERNAL`

---

# 0. Phạm vi thẩm quyền và quan hệ tài liệu

Tài liệu này là nguồn canonical cho:

- Product outcomes của Customer–Product Matching Capability.
- Business meanings của Matching Profile, Criterion, Rule Set, Matching Run, Match Result, Explanation, Shortlist, Comparison, Matching Feedback và Reverse Matching.
- Capability boundaries, invariants, acceptance outcomes và anti-patterns.
- Đầu vào phân tích cho Matching Context Implementation Pack.

Tài liệu này không phải nguồn exact cho:

- Physical database schema hoặc DDL.
- Exact API paths, request/response payloads.
- Exact Event names, envelope hoặc payloads.
- Exact permission codes, scopes, masking hoặc role matrix.
- Exact state machines, score formulas, weights, thresholds hoặc result codes.
- Exact AI model, feature set, training pipeline hoặc model-deployment topology.
- Exact frontend routes, components hoặc certified Metrics.
- Exact performance thresholds, batch sizes, cache policy hoặc retention periods.

Nguồn exact tương ứng:

| Chủ đề | Nguồn canonical |
|---|---|
| Thuật ngữ | Domain Glossary |
| Product requirements | PRD |
| Context ownership | Source of Truth Matrix |
| Architecture boundaries | Architecture Overview, Context Map và Accepted ADRs |
| Matching behavior chi tiết | Matching Context Implementation Pack |
| Database | Matching Context DB Specification và Alembic migrations |
| API | OpenAPI |
| Events | JSON Schema, AsyncAPI và Event Registry |
| Permissions/scopes/masking | Security registries và matrices |
| Requirement/Financial Profile | Party Context contracts |
| Listing/Price/Policy/Availability | Product Context contracts |
| Deal/Proposal/Hold/Booking | Transaction Context contracts |
| Campaign/Audience/outbound | Marketing Context contracts |
| Certified supply–demand Metrics | Analytics Context và Metric Registry |
| Immutable Audit facts | Audit Context |
| Runtime jobs/incidents | Operations Context |
| Công việc hiện tại | Current Sprint Detailed Execution Pack |

**Capability không đồng nghĩa Bounded Context.** Capability này chủ yếu được thực hiện bởi `matching` Context. Nó đọc dữ liệu thông qua published contracts/projections được phép, tạo derived decision-support records, và không trở thành source of truth thay cho `party`, `product`, `transaction`, `marketing`, `activity`, `analytics` hoặc `audit`.

Các phần candidate lifecycle, score formula, data model, operations, permissions, Events, screens và reports chỉ là design input. Chúng không được dùng thay machine-readable contracts hoặc Context Packs đã được chấp nhận.

---
# 1. Mục tiêu của capability

Customer–Product Matching Capability cung cấp công cụ lọc, chấm điểm, giải thích, so sánh và lập shortlist cho nhu cầu bất động sản.

Capability phải trả lời được:

- Requirement nào đủ dữ liệu để Matching.
- Candidate Listings nào nằm trong effective access scope.
- Listing nào vượt Eligibility Gate và Hard Filters.
- Listing nào phù hợp nhất, theo Rule Version nào và vì sao.
- Listing nào bị loại, bởi criterion hoặc Product condition nào.
- Giá, Price Version, Sales Policy Version và Availability timestamp nào đã được sử dụng.
- Financial Fit và Cash-flow Fit được ước tính theo giả định nào.
- Stakeholder criteria nào đồng thuận hoặc mâu thuẫn.
- Dữ liệu nào thiếu, stale hoặc chưa được xác minh.
- Customer đã xem, từ chối hoặc ưu tiên Listing nào.
- Alternative nào có thể thay thế khi Listing thay đổi.
- Listing nào phù hợp với các active Requirements trong effective scope.
- Matching Run lịch sử có thể tái tạo từ versions/snapshots nào.

Capability phải hỗ trợ:

- Requirement-to-Listing Matching.
- Deal-context Matching khi Deal đã tồn tại.
- Quick, Standard và Advanced Matching.
- Multi-stakeholder scenarios.
- Shortlist, Comparison và Matching Feedback.
- Re-Matching và Alternative Recommendation.
- Reverse Matching trong effective Customer/Requirement scope.
- Batch Matching.
- Matching input cho Campaign/Audience nhưng không sở hữu Campaign hoặc outbound execution.
- Operational demand signals cho Analytics nhưng không sở hữu certified enterprise Metrics.
- AI assistance có guardrails và human confirmation.

Nguyên tắc canonical:

> Matching chỉ cung cấp decision support. Matching không tự tạo Deal, Proposal, Commercial Lock, Hold, Booking, Contract, Payment hoặc outbound contact; không mở rộng quyền dữ liệu; không thay Requirement/Financial Profile; và không trình bày ước tính như phê duyệt tín dụng hoặc xác suất mua.

---
# 2. Vị trí của capability trong kiến trúc

Matching nằm giữa demand-side facts và supply-side facts:

```text
Party Context
Customer
Requirement
Financial Profile
Stakeholder
        ↓ published contracts / authorized projections
Matching Context
Profile
Rules
Run
Results
Explanation
Shortlist
        ↓ selected references / snapshots
Transaction Context
Deal
Proposal
Negotiation
Hold
Booking
```

Nguồn cung:

```text
Product Context
Project
Asset
Listing
Selling Right
Price
Sales Policy
Availability
        ↓ published contracts / authorized projections
Matching Context
Eligibility
Hard Filter
Scoring
Explanation
```

Matching sử dụng:

- `platform`: configuration, rule governance, Workflow/Approval/SLA definitions và Business Calendar.
- `iam`: authenticated identity, effective access context và authorization decisions.
- `party`: canonical Customer, Requirement, Financial Profile, Stakeholder, consent/contact restrictions và Customer redirect.
- `lead`: permitted source/care-context references khi cần giải thích operational context.
- `activity`: canonical Interaction/Appointment/feedback-source references.
- `product`: Listing, Asset, Selling Right, Price, Sales Policy, Availability và freshness.
- `operations`: execution support cho batch/background jobs.
- `audit`: immutable evidence cho sensitive access và governed actions.

Matching cung cấp:

- Cho `transaction`: selected Listing references, Match Result, Shortlist và immutable commercial/source-version references; Transaction vẫn tạo Proposal, Deal, Hold và Booking.
- Cho `marketing`: aggregate/eligible audience input hoặc opaque audience token theo consent và access rules; Marketing vẫn sở hữu Campaign, Audience và outbound execution.
- Cho `analytics`: governed Matching facts và operational signals; Analytics vẫn sở hữu certified funnels, supply–demand projections và Metrics.
- Cho `product`: aggregate demand signals hoặc authorized operational feedback; Matching không sửa Listing, Price, Policy hoặc Availability.
- Cho `activity`: follow-up suggestions/references; Activity vẫn sở hữu Task, Appointment và Interaction.

Không Context nào được dùng Match Result để bypass Product Availability hoặc Transaction workflow.

---
# 3. Ranh giới sở hữu dữ liệu

## 3.1. Matching Context sở hữu

- Matching Profile và Matching Profile Version.
- Normalized Matching Criteria và stakeholder-specific matching inputs.
- Matching Rule Set, Rule Version, weight/threshold/penalty definitions trong phạm vi Matching.
- Matching Run và candidate-set evidence.
- Eligibility/Hard-filter evaluation results.
- Match Result, score components, confidence, explanation và staleness state.
- Sale ranking override được tách khỏi System Score.
- Product Shortlist và Shortlist Version.
- Product Comparison snapshot.
- Matching-specific Feedback classification và Requirement-update suggestion.
- Re-Matching trigger/process state và Alternative suggestions.
- Matching alerts.
- Reverse Matching Run/Result.
- Batch Matching process state ở mức domain; job execution runtime thuộc `operations`.
- Rule simulation results.
- Matching-originated business facts và Audit requests.

## 3.2. Matching Context không sở hữu

- Canonical Party, Customer, Customer Identity, Requirement, Financial Profile, Stakeholder, consent hoặc contact restriction: `party`.
- Lead, attribution hoặc care protection: `lead`.
- Canonical Interaction, Appointment, call/note hoặc site-visit facts: `activity`.
- Project, Asset, Listing, Selling Right, Price, Sales Policy, Availability hoặc Commercial Lock: `product`.
- Deal, Proposal, Negotiation, Hold, Booking hoặc Deposit Commitment: `transaction`.
- Contract, Payment, Receipt, Refund hoặc Settlement: `contract`.
- Revenue hoặc Commission: `revenue`.
- Campaign, Audience, Journey, outbound eligibility hoặc Attribution: `marketing`.
- Certified supply–demand snapshots, conversion Metrics hoặc executive dashboards: `analytics`.
- Immutable Audit facts: `audit`.
- Job, queue, retry/DLQ, incident hoặc deployment runtime: `operations`.

## 3.3. Derived records không thay dữ liệu nguồn

Matching Result, Shortlist, Feedback classification hoặc AI suggestion không được trực tiếp:

- Sửa Requirement hoặc Financial Profile.
- Sửa Customer/Stakeholder.
- Sửa Listing, Price, Policy hoặc Availability.
- Tạo hoặc sửa Commercial Lock.
- Tạo Deal, Proposal, Hold hoặc Booking.
- Tạo Campaign/Audience hoặc gửi outbound.
- Cấp quyền, Share Grant, assignment hoặc care protection.
- Chứng nhận financial/legal eligibility.

Khi user chấp nhận Requirement-update suggestion, Matching phải gửi command qua published Party application contract. Party Context quyết định validation, versioning và update.

## 3.4. Availability và transaction safety

Matching có thể giữ Product Availability snapshot cho explainability và historical reconstruction.

Trước khi Transaction thực hiện Proposal action có commercial consequence, Hold hoặc Booking:

1. Transaction phải gọi Product Context.
2. Product phải kiểm tra current Listing, Selling Right, Price/Policy và Availability.
3. Product tạo hoặc chuyển Commercial Lock bằng local atomic transaction nếu command hợp lệ.
4. Transaction tiếp tục dựa trên durable Product result.

Match Result hoặc Shortlist không phải reservation và không bảo đảm Listing còn hàng.

## 3.5. Analytics boundary

Matching có thể tạo operational aggregates hoặc emit governed facts.

Certified supply–demand analysis, funnel metrics, executive KPIs và historical analytical snapshots thuộc `analytics`. Matching không được trở thành analytical source of truth cạnh tranh hoặc tự chứng nhận Metric formulas.

---
# 4. Nguyên tắc thiết kế cốt lõi

## 4.1. Lọc cứng trước, chấm điểm sau

Quy trình bắt buộc:

```text
Candidate Pool
→ Access Filter
→ Eligibility Filter
→ Hard Filter
→ Soft Scoring
→ Ranking
→ Explanation
→ Result Group
```

Một Listing vi phạm điều kiện bắt buộc không được xếp hạng cao bằng điểm mềm.

## 4.2. Điểm phù hợp không phải xác suất mua

Điểm 90/100 chỉ có nghĩa:

* Listing phù hợp cao với tiêu chí đã biết.
* Không có nghĩa Customer chắc chắn mua.
* Không phải xác suất chốt.
* Không phải dự báo tín dụng.
* Không phải thẩm định đầu tư.

## 4.3. Matching phải giải thích được

Hệ thống phải trả lời:

* Vì sao Listing được đưa vào kết quả?
* Vì sao Listing bị loại?
* Điểm đến từ tiêu chí nào?
* Điểm bị trừ ở đâu?
* Dữ liệu nào đang thiếu?
* Giá và chính sách version nào được dùng?
* Availability được kiểm tra lúc nào?

## 4.4. Không dùng dữ liệu không được phép

Matching không được đọc hoặc sử dụng:

* Financial Profile ngoài context được phép.
* Customer ngoài scope.
* Listing ngoài Project/Listing Access.
* Trường tài chính bị giới hạn.
* Dữ liệu cá nhân nhạy cảm không liên quan.

## 4.5. Không tự động hóa giao dịch

Capability không được tự:

* Tạo Deal.
* Gửi Proposal.
* Tạo Hold.
* Tạo Booking.
* Thu tiền.
* Chuyển trạng thái Listing.
* Thay primary sale.
* Xác nhận khoản vay.

## 4.6. Dữ liệu lịch sử phải tái tạo được

Mỗi Matching Run phải lưu hoặc snapshot:

* Requirement version.
* Financial Profile version.
* Stakeholder version.
* Matching Rule version.
* Candidate inventory version.
* Listing version.
* Price version.
* Policy version.
* Availability timestamp.

---

# 5. Khái niệm Matching Profile

## 5.1. Matching Profile là gì

Matching Profile là biểu diễn chuẩn hóa các điều kiện dùng để ghép sản phẩm.

Matching Profile có thể được tạo từ:

* Requirement.
* Deal.
* Customer preference.
* Quick Match input.
* Campaign criteria.
* Reverse Matching filter.

## 5.2. Requirement vẫn là nguồn chân lý nghiệp vụ

Matching Profile không thay thế Requirement.

Matching Profile có nhiệm vụ:

* Chuẩn hóa tiêu chí.
* Resolve giá trị.
* Gán mức độ quan trọng.
* Gắn rule.
* Gắn stakeholder.
* Chuẩn bị cho Matching Engine.

## 5.3. Một Requirement có nhiều Matching Profile Version

Khi Requirement thay đổi:

* Không ghi đè Profile lịch sử.
* Tạo version mới.
* Matching Run cũ giữ version cũ.

---

# 6. Matching Target

## 6.1. Requirement-to-Listing

Mô hình chính:

```text
Customer Requirement
→ nhiều Listing phù hợp
```

## 6.2. Deal-to-Listing

Dùng khi Deal đã tồn tại nhưng chưa chọn sản phẩm.

## 6.3. Customer-to-Listing Quick Match

Dùng để tư vấn nhanh, nhưng phải chọn Requirement hoặc tạo Matching Profile tạm thời.

## 6.4. Listing-to-Customer Reverse Matching

Dùng tìm Customer phù hợp với một Listing.

## 6.5. Batch Matching

Chạy nhiều Requirement với nhiều Listing.

## 6.6. Campaign-oriented Matching

Tìm nhóm Customer phù hợp với:

* Sales Launch.
* Project.
* Nhóm Listing.
* Chính sách mới.
* Inventory vừa mở.

---

# 7. Candidate Matching modes — Context-specific, pending validation

> Exact mode codes, eligibility và behavior thuộc Matching Context Implementation Pack.


```text
QUICK_MATCH
STANDARD_MATCH
ADVANCED_MATCH
DEAL_MATCH
REVERSE_MATCH
BATCH_MATCH
CAMPAIGN_MATCH
RE_MATCH
SIMULATION
```

## 7.1. Quick Match

* Ít tiêu chí.
* Kết quả nhanh.
* Không thay Requirement chính thức.
* Hiển thị cảnh báo về độ thiếu dữ liệu.

## 7.2. Standard Match

* Dùng Requirement đã active.
* Có Hard Filter.
* Có Score.
* Có Explanation.
* Có Shortlist.

## 7.3. Advanced Match

* Stakeholder.
* Cash-flow.
* Legal criteria.
* Purpose-specific model.
* Nhiều scenario tài chính.
* Nhiều Project.

## 7.4. Simulation

Dùng để thử rule hoặc trọng số.

Không tạo shortlist nghiệp vụ chính thức trừ khi user xác nhận.

---

# 8. Đầu vào từ Customer 360 Capability

## 8.1. Customer

* Customer ID canonical.
* Customer type.
* Customer role.
* Legal Entity relationship.
* Segment theo quyền.
* Consent.
* Contact restriction.

## 8.2. Requirement

* Requirement type.
* Purpose.
* Status.
* Priority.
* Budget.
* Currency.
* Timeline.
* Geography.
* Project preference.
* Property type.
* Structured criteria.
* Responsible user.
* Matching readiness.
* Source Lead.
* Care context.

## 8.3. Financial Profile

* Profile scope.
* As-of date.
* Valid until.
* Verification level.
* Vốn tự có.
* Thu nhập.
* Nghĩa vụ.
* Nhu cầu vay.
* Monthly payment target.
* Financial readiness.

## 8.4. Stakeholder

* Decision maker.
* Payer.
* Co-buyer.
* End user.
* Influencer.
* Opponent.
* Preference.
* Influence level.
* Attitude.

## 8.5. Feedback lịch sử

* Sản phẩm đã xem.
* Sản phẩm đã từ chối.
* Lý do.
* Giá phản hồi.
* Khu vực phản hồi.
* Tầng/view/hướng phản hồi.
* Policy phản hồi.

---

# 9. Đầu vào từ Product, Asset, Listing and Inventory Capability

## 9.1. Project

* Project type.
* Developer.
* Location.
* Legal status.
* Development stage.
* Expected handover.
* Sales Launch.
* Transaction model.

## 9.2. Asset

* Asset type.
* Area.
* Bedrooms.
* Bathrooms.
* Floor.
* Direction.
* View.
* Physical status.
* Legal status.
* Land details.
* Handover standard.

## 9.3. Listing

* Listing type.
* Visibility.
* Status.
* Readiness.
* Effective dates.
* Seller.
* Internal Legal Entity.
* Mandate.
* Transaction model.

## 9.4. Giá

* Base price.
* Sales price.
* Asking price.
* Minimum acceptable price theo quyền.
* Price components.
* Tax.
* Fees.
* Price version.
* Currency.

## 9.5. Chính sách

* Discount.
* Payment schedule.
* Early-payment benefit.
* Loan support.
* Customer eligibility.
* Stacking rule.
* Policy version.
* Effective dates.

## 9.6. Availability

* Current result.
* Reason.
* Active lock.
* External status.
* Freshness.
* Checked at.

---

# 10. Matching Context

Mỗi Matching Run phải có context:

* Enterprise.
* Legal Entity.
* Customer.
* Requirement.
* Deal nếu có.
* Responsible user.
* Project scope.
* Listing scope.
* Sales Launch.
* Matching mode.
* Rule set.
* As-of timestamp.

Context quyết định:

* Listing nào được xét.
* Dữ liệu nào được đọc.
* Field nào được hiển thị.
* Rule nào được áp dụng.
* Ai được xem kết quả.

---

# 11. Candidate Matching Readiness vocabulary — pending validation

> Exact states và transition semantics thuộc Matching Context Pack và machine contracts.


## 11.1. Trạng thái

```text
NOT_READY
MISSING_REQUIRED_DATA
READY_BASIC
READY_STANDARD
READY_ADVANCED
STALE_DATA
BLOCKED_BY_PERMISSION
BLOCKED_BY_CONSENT
```

## 11.2. Điều kiện Ready Basic

Ví dụ:

* Requirement active.
* Có property type hoặc project/khu vực.
* Có budget tối đa hoặc khoảng giá.
* Có responsible user.

## 11.3. Ready Standard

Có thêm:

* Mục đích.
* Timeline.
* Criteria.
* Financial summary.
* Mandatory exclusions.

## 11.4. Ready Advanced

Có thêm:

* Cash-flow.
* Stakeholder.
* Legal preference.
* Detailed financial profile.
* Verification freshness.

## 11.5. Không cấm Quick Match vì thiếu dữ liệu

Có thể chạy nhưng phải:

* Giảm confidence.
* Hiển thị dữ liệu thiếu.
* Không gắn nhãn “phù hợp cao” quá mức nếu thiếu tiêu chí quan trọng.

---

# 12. Matching Criterion

Mỗi criterion gồm:

* Criterion code.
* Category.
* Data type.
* Operator.
* Value.
* Unit.
* Importance.
* Weight.
* Hard/Soft flag.
* Exclusion flag.
* Source.
* Confidence.
* Stakeholder.
* Effective date.

---

# 13. Nhóm Criterion

## 13.1. Product Identity

* Project.
* Asset type.
* Listing type.
* Transaction model.
* New/resale.
* Developer.

## 13.2. Geography

* Province.
* District.
* Ward.
* Project.
* Radius.
* Distance.
* Landmark.
* Work/school proximity.

## 13.3. Finance

* Budget.
* First payment.
* Own capital.
* Loan amount.
* Monthly payment.
* Price per m².
* Tax/fee ceiling.

## 13.4. Physical

* Area.
* Bedrooms.
* Bathrooms.
* Floor.
* Direction.
* View.
* Frontage.
* Road width.
* Land shape.
* Handover standard.

## 13.5. Legal

* Ownership form.
* Legal readiness.
* Certificate status.
* Transfer eligibility.
* Land use.
* Mortgage acceptance.
* Project eligibility.

## 13.6. Timing

* Launch date.
* Handover date.
* Contract date.
* Move-in date.
* Seller urgency.
* Availability.

## 13.7. Investment

* Rental potential.
* Liquidity expectation.
* Infrastructure.
* Developer reputation input.
* Expected holding period.
* Exit constraints.

Các chỉ số dự báo nâng cao phải ghi rõ là ước tính.

## 13.8. Policy

* Payment schedule.
* Loan support.
* Discount.
* Early-payment policy.
* Existing-customer policy.
* Bulk purchase.

---

# 14. Candidate criterion-importance vocabulary — pending validation

> Exact codes, precedence và veto semantics phải được khóa trong Matching contracts.


```text
MANDATORY
VERY_HIGH
HIGH
NORMAL
LOW
NICE_TO_HAVE
NOT_IMPORTANT
NOT_ACCEPTABLE
```

## 14.1. Mandatory

Vi phạm thì loại.

## 14.2. Not Acceptable

Listing có giá trị bị cấm sẽ bị loại.

## 14.3. Very High/High

Ảnh hưởng lớn đến điểm nhưng không nhất thiết loại.

## 14.4. Nice to Have

Chỉ cộng điểm nhỏ.

## 14.5. Not Important

Không dùng chấm điểm.

---

# 15. Hard Filter

## 15.1. Mục tiêu

Loại Listing không đủ điều kiện nghiệp vụ hoặc vi phạm yêu cầu bắt buộc.

## 15.2. Hard Filter nguồn cung

* Listing không active.
* Listing hết hạn.
* Mandate không hợp lệ.
* Listing không đủ readiness.
* Listing không có giá hợp lệ.
* Listing sold/contracted.
* Listing bị block.
* Availability unknown quá hạn cho phép.
* User không có Project/Listing Access.
* Listing ngoài Legal Entity context.
* External inventory cần xác nhận bắt buộc.

## 15.3. Hard Filter nhu cầu

* Sai property type bắt buộc.
* Sai project bắt buộc.
* Ngoài khu vực bắt buộc.
* Giá vượt budget tuyệt đối.
* Diện tích dưới mức tối thiểu bắt buộc.
* Phòng ngủ thiếu.
* Vi phạm tiêu chí Not Acceptable.
* Legal readiness không đạt.
* Handover quá muộn.
* Không phù hợp transaction model.

## 15.4. Hard Filter tài chính

Có thể gồm:

* First payment vượt vốn tự có tối đa.
* Khoản vay vượt mức Customer chấp nhận.
* Monthly payment vượt hard ceiling.
* Payment milestone xảy ra trước thời điểm có nguồn tiền.

Chỉ dùng khi Financial Profile đủ dữ liệu và user có quyền.

---

# 16. Kết quả Hard Filter

Mỗi Candidate phải có:

* Pass/Fail.
* Failed criterion.
* Source value.
* Listing value.
* Reason code.
* User-facing explanation.
* Internal explanation.
* Rule version.

## 16.1. Listing bị loại vẫn có thể hiển thị

Tùy permission và mode:

* Standard result chỉ hiển thị top exclusions.
* Advanced mode cho phép xem “Không phù hợp”.
* Không đưa Listing bị loại vào shortlist mặc định.

---

# 17. Candidate Pool

## 17.1. Candidate Pool có thể lấy từ

* Toàn inventory được cấp quyền.
* Một Project.
* Một Sales Launch.
* Một Inventory List.
* Một nhóm Listing.
* Một địa lý.
* Một Asset type.
* Private Listing được chia sẻ.

## 17.2. Candidate Pool không được mở rộng theo frontend

Backend phải tự intersect:

```text
Requested Scope
∩ User Project Access
∩ Listing Access
∩ Legal Entity Context
∩ Listing Visibility
∩ Inventory Availability
```

## 17.3. Candidate Pool Snapshot

Lưu:

* Query criteria.
* Candidate count.
* Inventory version.
* Listing IDs hoặc candidate set hash.
* Timestamp.
* Access context.

---

# 18. Eligibility Gate

Trước Hard Filter, Listing phải qua Eligibility Gate:

1. User được xem.
2. Customer context hợp lệ.
3. Listing được phép tư vấn.
4. Mandate cho phép Proposal/Marketing.
5. Sales Launch active hoặc được phép pre-launch.
6. Price/policy còn hiệu lực.
7. Không có legal/admin block.
8. Availability đủ mới.
9. Listing không bị merged/archived.
10. Customer không bị restriction đặc biệt với sản phẩm nếu có.

---

# 19. Soft Scoring principles

> Các trọng số bên dưới là illustrative baseline, không phải production score contract. Exact formulas/weights thuộc approved Rule Version.


Sau khi vượt Hard Filter, Listing được chấm điểm 0–100.

## 19.1. Nhóm điểm tham khảo

| Nhóm                     | Trọng số tham khảo |
| ------------------------ | -----------------: |
| Financial Fit            |                 30 |
| Property/Functional Fit  |                 25 |
| Geography Fit            |                 15 |
| Floor/View/Direction Fit |                 10 |
| Payment & Policy Fit     |                 10 |
| Timing/Handover Fit      |                  5 |
| Legal Fit                |                  5 |

Tổng trọng số phải bằng 100 hoặc được chuẩn hóa về 100.

## 19.2. Trọng số chỉ là cấu hình khởi tạo

Có thể khác theo:

* Purpose.
* Customer segment.
* Project.
* Asset type.
* Transaction model.
* Legal Entity.
* Buyer/Investor.
* Requirement type.

---

# 20. Illustrative scoring model — không phải exact production formula

> Công thức dưới đây biểu đạt invariant về normalization/range. Exact component formulas, precision và rounding thuộc versioned Matching Rule contracts.


Ví dụ tổng quát:

```text
Total Score
=
Σ(Component Score × Normalized Weight)
− Penalties
```

Trong đó:

```text
Component Score ∈ [0,100]
Normalized Weight ∈ [0,1]
```

Kết quả cuối:

```text
0 ≤ Total Score ≤ 100
```

## 20.1. Không cho điểm vượt 100

Bonus phải nằm trong cấu trúc trọng số hoặc bị giới hạn.

## 20.2. Decimal precision

Điểm nội bộ có thể lưu 4 chữ số thập phân.

Điểm hiển thị có thể làm tròn theo policy.

---

# 21. Financial Fit

## 21.1. Các thành phần

* Tổng giá.
* Giá sau chính sách.
* Thuế/phí.
* First payment.
* Vốn tự có.
* Khoản vay.
* Monthly payment.
* Payment milestones.
* Nguồn tiền dự kiến.
* Tài sản cần bán trước.
* Buffer tài chính.

## 21.2. Budget Range Fit

Ví dụ:

* Trong budget target: điểm tối đa.
* Trên target nhưng dưới max: giảm dần.
* Vượt absolute max: Hard Fail.
* Dưới min quá nhiều: có thể giảm nếu không đúng phân khúc kỳ vọng.

## 21.3. Financial Gap

Phải tính rõ:

```text
Financial Gap
=
Required Initial Capital
− Available Own Capital
```

## 21.4. Loan Need

```text
Estimated Loan Need
=
Estimated Purchase Obligation
− Own Capital Applied
```

Đây là ước tính, không phải phê duyệt vay.

## 21.5. Monthly Payment Fit

So sánh:

* Estimated monthly payment.
* Customer target monthly payment.
* Customer hard ceiling nếu có.

## 21.6. Financial Fit Explanation

Ví dụ:

> Giá sau chính sách là 4,8 tỷ đồng, cao hơn ngân sách mục tiêu 300 triệu nhưng vẫn thấp hơn mức tối đa 5 tỷ đồng. Customer cần khoảng 1,4 tỷ vốn ban đầu và khoản vay 2,8 tỷ theo giả định hiện tại.

---

# 22. Cash-Flow Fit

## 22.1. Mục tiêu

Đánh giá khả năng đáp ứng từng mốc thanh toán, không chỉ tổng giá.

## 22.2. Đầu vào

* Payment schedule.
* Policy.
* Booking amount.
* Deposit amount.
* Contract milestone.
* Construction milestones.
* Expected capital dates.
* Asset sale proceeds.
* Loan disbursement date.

## 22.3. Kết quả

* Fully aligned.
* Minor timing gap.
* Significant timing gap.
* Requires loan timing.
* Requires asset sale first.
* Insufficient data.

## 22.4. Không tự cam kết giải ngân

Luôn hiển thị:

* Giả định.
* Chưa phải xác nhận ngân hàng.
* Dữ liệu cần kiểm tra.

---

# 23. Purpose Fit

## 23.1. Mua để ở

Ưu tiên:

* Công năng.
* Khoảng cách.
* Hạ tầng.
* Phòng ngủ.
* Handover.
* Chi phí sử dụng.
* Người sử dụng.

## 23.2. Đầu tư

Ưu tiên có thể gồm:

* Giá.
* Khả năng thanh khoản.
* Tiến độ.
* Nguồn cung.
* Rental potential.
* Exit restrictions.
* Policy.
* Developer/project factors.

## 23.3. Cho thuê

* Nhu cầu khu vực.
* Loại khách thuê.
* Phí vận hành.
* Bàn giao.
* Nội thất.
* Rental estimate.

## 23.4. Kinh doanh

* Mặt tiền.
* Lưu lượng.
* Vị trí.
* Diện tích.
* Loại hình sử dụng.
* Legal use.

## 23.5. Cho người thân

Phải sử dụng tiêu chí của end user, không chỉ của payer.

---

# 24. Geography Fit

Có thể tính theo:

* Exact project.
* Exact district.
* Preferred area.
* Radius.
* Travel distance.
* Travel time.
* Landmark proximity.
* Work/school proximity.

## 24.1. Exact location của private Listing

Chỉ Matching Service nội bộ được dùng khi user có quyền.

Frontend có thể chỉ nhận khu vực gần đúng.

---

# 25. Property Fit

Các yếu tố:

* Asset type.
* Area.
* Bedrooms.
* Bathrooms.
* Floor.
* Direction.
* View.
* Frontage.
* Road width.
* Shape.
* Handover standard.
* Furnishing.
* Parking.
* Management fee.

## 25.1. Range score

Tiêu chí dạng range có thể:

* Điểm tối đa trong target range.
* Giảm dần trong acceptable range.
* Hard Fail ngoài absolute range.

---

# 26. Legal Fit

Đánh giá:

* Asset Legal Readiness.
* Project Legal Status.
* Ownership verification.
* Encumbrance.
* Transfer restriction.
* Land use purpose.
* Contract readiness.
* Customer legal preference.

## 26.1. Không che giấu rủi ro

Listing có `ELIGIBLE_WITH_CONDITIONS` phải hiển thị:

* Điều kiện.
* Người xác minh.
* Ngày xác minh.
* Tài liệu còn thiếu.

---

# 27. Timing Fit

So sánh:

* Desired purchase date.
* Desired move-in date.
* Listing availability.
* Launch date.
* Expected handover.
* Seller timeline.
* Contract timeline.
* Financial availability.

---

# 28. Policy Fit

Đánh giá:

* Customer có đủ điều kiện không.
* Discount có áp dụng không.
* Loan support phù hợp không.
* Payment schedule có phù hợp không.
* Chính sách có hết hạn trước quyết định dự kiến không.
* Chính sách có được cộng dồn không.

## 28.1. Không hiển thị Benefit chưa chắc chắn như giá chắc chắn

Phải phân biệt:

* Confirmed applicable.
* Conditionally applicable.
* Requires approval.
* Not applicable.
* Unknown.

---

# 29. Stakeholder Matching

## 29.1. Mục tiêu

Đánh giá sản phẩm theo yêu cầu của nhiều người tham gia.

## 29.2. Stakeholder có thể gồm

* Customer chính.
* Co-buyer.
* Payer.
* Decision maker.
* End user.
* Influencer.
* Opponent.
* Advisor.

## 29.3. Mỗi Stakeholder có thể có tiêu chí riêng

Ví dụ:

* Customer muốn gần trung tâm.
* Payer muốn ngân sách thấp.
* End user muốn ba phòng ngủ.
* Vợ/chồng không chấp nhận hướng Tây.

## 29.4. Stakeholder Weight

Trọng số có thể dựa trên:

* Decision authority.
* Financial contribution.
* Influence level.
* Role.

Không được dùng trọng số để che tiêu chí veto.

---

# 30. Stakeholder Conflict

## 30.1. Loại conflict

* Mandatory criteria mâu thuẫn.
* Budget mâu thuẫn.
* Geography mâu thuẫn.
* End-user requirement mâu thuẫn payer.
* Veto criterion mâu thuẫn.

## 30.2. Hành vi hệ thống

* Không tự quyết định bên nào thắng.
* Hiển thị conflict.
* Đề xuất câu hỏi làm rõ.
* Cho phép tạo scenario.
* Có thể chạy nhiều Matching Profile scenario.

## 30.3. Scenario

Ví dụ:

```text
Scenario A: ưu tiên vị trí
Scenario B: ưu tiên ngân sách
Scenario C: cân bằng hai bên
```

---

# 31. Penalty

Penalty có thể áp dụng cho:

* Giá vượt target.
* Dữ liệu Listing stale.
* Policy sắp hết hạn.
* Legal condition.
* Availability cần xác nhận.
* Requirement thiếu dữ liệu.
* Customer từng từ chối đặc điểm tương tự.
* Listing từng bị Customer loại.

## 31.1. Penalty không được biến Hard Fail thành Pass

## 31.2. Penalty phải giải thích được

---

# 32. Confidence

## 32.1. Match Score và Confidence tách biệt

Ví dụ:

* Match Score: 88.
* Confidence: 62%.

Điểm cao nhưng confidence thấp nếu:

* Requirement thiếu dữ liệu.
* Financial Profile hết hạn.
* Listing status stale.
* Policy eligibility chưa xác nhận.
* Stakeholder chưa rõ.

## 32.2. Confidence không phải xác suất mua

Chỉ phản ánh mức đầy đủ và độ tin cậy của dữ liệu Matching.

---

# 33. Freshness

## 33.1. Dữ liệu cần freshness

* Availability.
* External inventory.
* Price.
* Policy.
* Financial Profile.
* Requirement.
* Ownership/legal readiness.

## 33.2. Hiển thị

Mỗi kết quả cần cho biết:

* Availability checked at.
* Price effective at.
* Policy effective at.
* Requirement updated at.
* Financial Profile as-of date.

## 33.3. Stale Result

Kết quả có thể chuyển:

```text
CURRENT
PRICE_STALE
POLICY_STALE
AVAILABILITY_STALE
REQUIREMENT_STALE
FINANCIAL_STALE
MULTIPLE_STALE_FACTORS
```

---

# 34. Kết quả Matching

Mỗi Match Result gồm:

* Matching Run.
* Listing.
* Asset.
* Total score.
* Confidence.
* Rank.
* Result group.
* Hard-filter status.
* Financial fit.
* Purpose fit.
* Availability.
* Price.
* Policy.
* Main strengths.
* Main concerns.
* Data gaps.
* Generated at.

---

# 35. Candidate Match Result groups — pending validation

> Exact codes, thresholds và guards thuộc Matching Context Pack và Rule Version.


```text
IMMEDIATE_FIT
STRONG_FIT
CONDITIONAL_FIT
ALTERNATIVE
REQUIRES_CONFIRMATION
NOT_SUITABLE
EXCLUDED
NO_ACCESS
STALE_RESULT
```

## 35.1. Immediate Fit

* Vượt Hard Filter.
* Điểm cao.
* Availability phù hợp.
* Không có điều kiện nghiêm trọng.
* Giá/policy hiện hành.

## 35.2. Conditional Fit

Có thể cần:

* Vay cao hơn.
* Gia hạn timeline.
* Owner confirmation.
* Policy approval.
* External availability confirmation.

## 35.3. Alternative

Không phải lựa chọn đầu nhưng giải quyết được phần lớn nhu cầu.

## 35.4. Not Suitable

Không vượt ngưỡng mềm nhưng không vi phạm Hard Filter tuyệt đối.

## 35.5. Excluded

Vi phạm Hard Filter.

---

# 36. Illustrative result thresholds — không phải production values

> Các khoảng điểm dưới đây chỉ là baseline minh họa. Production thresholds phải versioned, simulated, approved và effective-dated.


Ví dụ cấu hình:

| Điểm     | Nhóm                 |
| -------- | -------------------- |
| 85–100   | Strong/Immediate Fit |
| 70–84,99 | Conditional Fit      |
| 55–69,99 | Alternative          |
| Dưới 55  | Not Suitable         |

Ngưỡng thực tế phải cấu hình theo Rule Set.

Immediate Fit còn phải kiểm tra:

* Availability.
* Confidence.
* Không có blocker.

---

# 37. Ranking

## 37.1. Thứ tự mặc định

1. Result group.
2. Total score.
3. Confidence.
4. Availability quality.
5. Price freshness.
6. Policy freshness.
7. Rule tie-breaker.

## 37.2. Không ưu tiên Listing chỉ vì phí hoặc hoa hồng cao

Matching Engine không được sử dụng:

* Commission của sale.
* Margin công ty.
* Phí môi giới.

làm tiêu chí phù hợp Customer, trừ khi hiển thị ở báo cáo nội bộ tách biệt và không ảnh hưởng Customer Fit Score.

## 37.3. Tie-breaker

Có thể dùng:

* Giá gần target.
* Availability mới hơn.
* Ít điều kiện hơn.
* Handover gần hơn.
* Data confidence cao hơn.

---

# 38. Explainability

## 38.1. Giải thích tổng quan

Ví dụ:

> Listing đạt 87/100 vì phù hợp ngân sách, đúng khu vực ưu tiên, đủ ba phòng ngủ và có lịch thanh toán phù hợp. Điểm bị giảm do bàn giao muộn hơn mong muốn bốn tháng và hướng không nằm trong nhóm ưu tiên.

## 38.2. Giải thích từng tiêu chí

* Criterion.
* Requirement value.
* Listing value.
* Score.
* Weight.
* Penalty.
* Source.
* Confidence.
* Result.

## 38.3. Giải thích Hard Fail

Ví dụ:

> Listing bị loại vì tổng giá 6,2 tỷ đồng vượt ngân sách tối đa bắt buộc 5,5 tỷ đồng.

## 38.4. Giải thích nội bộ và Customer-facing

Tách:

* Internal explanation.
* Customer-safe explanation.

Không hiển thị:

* Floor Price.
* Owner net.
* Internal risk note.
* Margin.
* Dữ liệu tài chính chi tiết.

---

# 39. Match History

Mỗi Requirement phải xem được:

* Các Matching Run.
* Ngày chạy.
* User.
* Rule version.
* Số candidate.
* Top result.
* Shortlist.
* Feedback.
* Kết quả đã stale.
* Sự thay đổi điểm giữa các lần.

Không ghi đè kết quả cũ.

---

# 40. Re-Matching

## 40.1. Trigger

* Requirement thay đổi.
* Budget thay đổi.
* Financial Profile cập nhật.
* Stakeholder thay đổi.
* Listing mới.
* Giá thay đổi.
* Policy thay đổi.
* Availability thay đổi.
* Listing ưu tiên bị giữ/bán.
* Customer feedback.
* Sales Launch mới.

## 40.2. Re-Matching tự động

Có thể chạy nền nhưng:

* Không tự thay shortlist chính thức.
* Không tự gửi Proposal.
* Không tự tạo Hold.
* Chỉ tạo result set hoặc alert.

## 40.3. So sánh Re-Match

Hiển thị:

* Listing mới xuất hiện.
* Listing bị loại.
* Listing tăng/giảm điểm.
* Lý do.
* Giá/policy thay đổi.

---

# 41. Shortlist

## 41.1. Khái niệm

Shortlist là danh sách sản phẩm được sale và Customer cân nhắc.

Shortlist không khóa sản phẩm.

## 41.2. Shortlist có thể gắn

* Customer.
* Requirement.
* Deal.
* Matching Run.
* Sale.
* Legal Entity.

## 41.3. Một Requirement có nhiều Shortlist Version

Ví dụ:

* Danh sách tư vấn lần 1.
* Danh sách sau khi Customer phản hồi.
* Danh sách chuẩn bị Proposal.

---

# 42. Shortlist Item

Mỗi item gồm:

* Listing.
* Match Result.
* System rank.
* Sale rank.
* Customer priority.
* Reason.
* Status.
* Feedback.
* Added by.
* Added at.
* Removed at.
* Price snapshot reference.
* Availability at add time.

---

# 43. Candidate Shortlist Item lifecycle — pending validation

> Exact lifecycle và Event-driven updates thuộc Matching Context Pack.


```text
CONSIDERING
PRIORITY_1
PRIORITY_2
BACKUP
NEEDS_CONFIRMATION
CUSTOMER_REJECTED
SALE_EXCLUDED
UNAVAILABLE
REPLACED
SELECTED_FOR_PROPOSAL
SELECTED_FOR_DEAL
HOLD_REQUESTED
BOOKED
ARCHIVED
```

## 43.1. Không tự chuyển Booked

Trạng thái phản chiếu `BOOKED` chỉ được cập nhật từ accepted Transaction business fact; Matching không sở hữu Booking.

---

# 44. Sale Override

## 44.1. Sale có thể

* Thay đổi thứ tự tư vấn.
* Thêm Listing vượt ngưỡng mềm.
* Loại Listing.
* Đưa Listing vào backup.
* Ghi lý do.

## 44.2. Sale không được

* Sửa System Score.
* Sửa Hard Filter.
* Sửa Availability.
* Sửa Price.
* Sửa Rule result.
* Biến Excluded thành Immediate Fit.

## 44.3. Lưu riêng

* System rank.
* Sale rank.
* Override type.
* Reason.
* Actor.
* Timestamp.

---

# 45. Product Comparison

## 45.1. Các trường so sánh

* Project.
* Listing type.
* Asset type.
* Giá.
* Giá/m².
* Tax/phí.
* Area.
* Bedrooms.
* Floor.
* Direction.
* View.
* Location.
* Payment schedule.
* Loan support.
* Policy.
* Initial capital.
* Estimated loan.
* Estimated monthly payment.
* Handover.
* Legal readiness.
* Availability.
* Match Score.
* Confidence.
* Strengths.
* Concerns.

## 45.2. Field permission

So sánh không hiển thị:

* Floor Price nếu user không có quyền.
* Owner contact.
* Internal margin.
* Financial Profile detail ngoài quyền.

## 45.3. Snapshot

Comparison có thể snapshot để:

* Tạo Proposal.
* Chia sẻ nội bộ.
* Lưu lịch sử tư vấn.

---

# 46. Tích hợp Proposal

Luồng:

```text
Run Matching
→ Chọn kết quả
→ Add Shortlist
→ Compare
→ Select for Proposal
→ Deal and Transaction Capability tạo Proposal
```

Customer–Product Matching Capability cung cấp:

* Listing.
* System score.
* Explanation.
* Price version.
* Policy version.
* Availability timestamp.
* Customer-safe summary.
* Financial estimate.

Deal and Transaction Capability chịu trách nhiệm:

* Proposal version.
* Approval.
* Nội dung gửi.
* Gửi Customer.
* Theo dõi phản hồi.

---

# 47. Matching Feedback

> Canonical Interaction/Appointment/source communication thuộc Activity Context. Matching chỉ giữ matching-specific classification và source reference.


## 47.1. Loại feedback

```text
LIKED
DISLIKED
TOO_EXPENSIVE
LOCATION_NOT_SUITABLE
AREA_TOO_SMALL
AREA_TOO_LARGE
WRONG_PROPERTY_TYPE
WRONG_FLOOR
WRONG_DIRECTION
WRONG_VIEW
PAYMENT_PLAN_NOT_SUITABLE
LEGAL_CONCERN
HANDOVER_TOO_LATE
POLICY_NOT_ATTRACTIVE
ALREADY_SEEN
NOT_INTERESTED_NOW
OTHER
```

## 47.2. Feedback source

* Customer.
* Stakeholder.
* Sale observation.
* Proposal response.
* Site visit.
* Appointment.

## 47.3. Không tự sửa Requirement

Hệ thống có thể đề xuất:

> Customer nhiều lần từ chối sản phẩm trên 5 tỷ đồng. Có cập nhật ngân sách tối đa không?

Sale phải xác nhận trước khi thay Requirement.

---

# 48. Học từ Feedback

## 48.1. MVP

Feedback dùng để:

* Re-rank trong Requirement.
* Gắn penalty.
* Đề xuất cập nhật tiêu chí.
* Giảm sản phẩm tương tự.

## 48.2. Giai đoạn nâng cao

Có thể dùng machine learning nhưng phải:

* Có model version.
* Có explainability.
* Có monitoring.
* Không học từ dữ liệu ngoài quyền.
* Không dùng dữ liệu nhạy cảm không phù hợp.
* Có khả năng tắt.
* Không phá Hard Filter.

---

# 49. Cảnh báo Listing ưu tiên

Hệ thống phải cảnh báo khi Listing trong shortlist:

* Bị Hold.
* Bị Booking.
* Bị bán.
* Bị rút.
* Hết hạn.
* Giá thay đổi.
* Policy thay đổi.
* Legal readiness thay đổi.
* External status stale.
* Mandate hết hạn.

Cảnh báo phải hiển thị:

* Listing.
* Thay đổi.
* Thời gian.
* Ảnh hưởng.
* Sản phẩm thay thế.

---

# 50. Alternative Recommendation

Khi Listing không còn khả dụng, hệ thống tìm Alternative dựa trên:

* Cùng project.
* Cùng Asset type.
* Khoảng giá gần.
* Area gần.
* Floor/view tương tự.
* Payment policy tương tự.
* Match Score gần.

Không tự thay Listing trong Proposal hoặc Deal.

---

# 51. Reverse Matching

## 51.1. Khái niệm

Reverse Matching tìm Requirement hoặc Customer phù hợp với một Listing.

```text
Listing
→ Matching Profiles
→ Customer/Requirement phù hợp
```

## 51.2. Trường hợp sử dụng

* Listing mới.
* Inventory vừa mở.
* Sản phẩm vừa được giải phóng.
* Chính sách mới.
* Listing ký gửi cần bán nhanh.
* Sales Launch.

## 51.3. Reverse Matching phải dùng Requirement

Không quét toàn Customer chỉ dựa trên phone hoặc segment.

Phải có:

* Requirement active.
* Matching readiness.
* Consent phù hợp.
* Access context.

---

# 52. Scope Reverse Matching

## 52.1. Sale

Chỉ Customer/Requirement `mine` hoặc được chia sẻ.

## 52.2. Team Lead

Scope `team`.

## 52.3. Department Head

Scope `department`.

## 52.4. Director hoặc user đặc biệt

Scope theo quyền `legal_entity/all`.

## 52.5. Inventory Manager

Không mặc định được xem Customer identity.

Có thể xem:

* Số lượng Requirement phù hợp.
* Aggregate demand.
* Masked result.

Muốn xem Customer cụ thể cần permission và context.

---

# 53. Reverse Matching Result

Gồm:

* Requirement.
* Customer masked/full theo quyền.
* Score.
* Confidence.
* Responsible sale.
* Main fit reasons.
* Main concerns.
* Last contact.
* Consent status.
* Existing shortlist/deal.
* Duplicate outreach warning.

## 53.1. Không tự gửi Customer cho sale khác

Reverse result không tự tạo:

* Customer Share Grant.
* Care protection.
* Assignment.
* Deal.
* Campaign contact.

---

# 54. Batch Matching

## 54.1. Mục tiêu

Chạy nhiều Requirement theo lịch hoặc theo sự kiện.

## 54.2. Yêu cầu kỹ thuật

* Background job.
* Batch size.
* Checkpoint.
* Idempotency.
* Retry.
* Priority.
* Access snapshot.
* Rule version.
* Result retention.
* Error handling.

## 54.3. Không gửi thông báo tràn lan

Cần:

* Notification threshold.
* Top-N.
* Dedup alert.
* Cooldown.
* User preference.

---

# 55. Campaign-oriented Matching

## 55.1. Mục tiêu

Xác định tập Customer có nhu cầu phù hợp với:

* Project mới.
* Sales Launch.
* Nhóm Listing.
* Policy.
* Price range.

## 55.2. Điều kiện

* Có campaign scope.
* Có approval nếu dùng dữ liệu Customer.
* Tuân thủ consent Marketing.
* Không mở rộng Customer access cho Marketing.
* Không tự gửi outbound.

## 55.3. Output

Có thể là:

* Aggregate count.
* Eligible Customer list theo quyền.
* Responsible sale list.
* Suggested campaign audience token.

---

# 56. Supply–Demand operational signals và Analytics boundary

> Matching có thể tạo operational signals/aggregates phục vụ phản hồi nhanh. Certified supply–demand snapshots và enterprise Metrics thuộc Analytics Context.


Capability tổng hợp:

* Nhu cầu theo khu vực.
* Nhu cầu theo ngân sách.
* Nhu cầu theo Asset type.
* Nhu cầu theo phòng ngủ.
* Nhu cầu theo timeline.
* Nhu cầu vay.
* Nhu cầu không có Listing phù hợp.
* Listing không có Requirement phù hợp.

## 56.1. Không lộ Customer identity

Báo cáo quản trị dùng dữ liệu aggregate.

## 56.2. Ứng dụng

* Nhập thêm nguồn cung.
* Điều chỉnh sản phẩm.
* Chọn dự án phân phối.
* Thiết kế sản phẩm tự phát triển.
* Điều chỉnh Price/Policy.
* Phân bổ Marketing.

---

# 57. Rule Set

## 57.1. Matching Rule Set gồm

* Rule code.
* Scope.
* Requirement type.
* Purpose.
* Asset type.
* Project.
* Hard filters.
* Weights.
* Thresholds.
* Penalties.
* Confidence rules.
* Tie-breakers.
* Explanation templates.
* Effective dates.
* Version.
* Status.

## 57.2. Rule Scope

* Enterprise.
* Legal Entity.
* Project.
* Sales Launch.
* Asset type.
* Customer segment.
* Purpose.
* Transaction model.

## 57.3. Specific rule precedence

Rule resolution phải sử dụng strategy được khai báo trong approved Matching/Platform contracts; không mặc định mọi trường hợp đều dùng most-specific-wins.

---

# 58. Rule Version

Rule active không sửa trực tiếp.

Quy trình:

1. Clone version.
2. Chỉnh sửa.
3. Validate.
4. Simulation.
5. Review.
6. Approval.
7. Activate.
8. Version cũ hết hiệu lực.

Matching Run cũ giữ rule version cũ.

---

# 59. Rule Simulation

## 59.1. Mục tiêu

Kiểm tra trước khi kích hoạt.

## 59.2. Simulation phải hiển thị

* Requirement mẫu.
* Candidate count.
* Pass Hard Filter.
* Score distribution.
* Top Listing thay đổi.
* Listing bị loại.
* Customer segment bị ảnh hưởng.
* Supply coverage.
* Runtime.
* Rule conflict.

## 59.3. Không ghi đè production result

Simulation có namespace riêng.

---

# 60. Trọng số và ngưỡng

## 60.1. Weight validation

* Tổng trọng số hợp lệ.
* Không có trọng số âm.
* Hard criterion không bị weight thay thế.
* Mandatory criterion không có score override.

## 60.2. Threshold validation

* Không chồng lấn.
* Bao phủ khoảng điểm.
* Immediate Fit cần điều kiện bổ sung.
* Confidence threshold rõ ràng.

---

# 61. AI hỗ trợ

AI có thể:

* Trích xuất tiêu chí từ cuộc gọi/note.
* Gợi ý criterion bị thiếu.
* Gợi ý câu hỏi qualification.
* Tóm tắt Match Result.
* Viết giải thích Customer-safe.
* Phân loại feedback.
* Gợi ý Alternative.
* Phát hiện stakeholder conflict.

AI không được:

* Tự thay Requirement chính thức.
* Tự sửa Financial Profile.
* Tự xác nhận legal readiness.
* Tự xác nhận khoản vay.
* Tự thay System Score không có model version.
* Tự mở rộng Candidate Pool ngoài quyền.
* Tự tạo Deal/Hold/Booking.
* Tự gửi Proposal.
* Dùng dữ liệu nhạy cảm không phù hợp.

---

# 62. Performance and implementation considerations — không phải topology lock

> Exact architecture, index/search technology, cache, worker topology và thresholds thuộc Architecture/Toolchain/Operations documents và Sprint Pack.


## 62.1. Mục tiêu

* Quick Match phản hồi nhanh.
* Standard Match xử lý hàng nghìn Listing.
* Batch Match chạy nền.
* Reverse Match dùng index phù hợp.

## 62.2. Kiến trúc đề xuất

* Candidate retrieval service.
* Rule evaluation engine.
* Scoring service.
* Explanation service.
* Snapshot store.
* Search/index layer.
* Background job worker.
* Cache có thời hạn.

## 62.3. Cache

Cache được dùng cho:

* Listing search.
* Static attributes.
* Rule version.

Không dùng cache làm nguồn chuẩn cho:

* Availability.
* Price active cuối cùng.
* Commercial Lock.
* Permission.

---

# 63. Availability khi hiển thị kết quả

Matching Run có thể dùng Availability snapshot.

Nhưng trước khi:

* Chọn Proposal.
* Tạo Deal.
* Request Hold.
* Booking.

Transaction Context phải gọi Product Context để kiểm tra current Availability và yêu cầu Commercial Lock phù hợp.

Không sử dụng Match Result hoặc Shortlist cũ để kết luận Listing vẫn còn hàng.

---

# 64. Multi-Legal Entity

## 64.1. Requirement có Legal Entity context

Matching chỉ dùng Listing:

* Thuộc Legal Entity được phép.
* Hoặc có mandate cross-entity hợp lệ.
* User có quyền.

## 64.2. Customer dùng chung Enterprise

Customer ID không thay đổi.

Nhưng Matching Result phải ghi:

* Legal Entity.
* Seller Legal Entity.
* Payment Receiver.
* Transaction model.

## 64.3. Không dùng quyền Entity A xem Listing Entity B

Trừ Project/Listing Access và policy hợp lệ.

---

# 65. Bảo mật Financial Explanation

## 65.1. Sale

Có thể xem:

* Budget fit.
* Initial capital estimate.
* Loan need summary.
* Monthly payment estimate.

Không mặc định xem:

* Thu nhập chi tiết.
* Nghĩa vụ chi tiết.
* Tài sản tài chính.
* Tài liệu.

## 65.2. Finance

Xem chi tiết khi có context và permission.

## 65.3. Customer-facing explanation

Không hiển thị dữ liệu nội bộ mà Customer không cần.

---

# 66. Consent và Contact Restriction

Matching có thể chạy nội bộ khi có mục đích nghiệp vụ hợp lệ.

Nhưng trước khi:

* Gửi Proposal.
* Tạo Campaign.
* Liên hệ Customer.

Capability liên quan phải kiểm tra:

* Consent.
* Contact restriction.
* Preferred channel.
* Legal basis.

Reverse Matching không đồng nghĩa được phép liên hệ.

---

# 67. SLA policy inputs

> Các giá trị dưới đây là recommended baselines để validation, không phải hardcoded SLO/SLA contract.


## 67.1. Các SLA

* Requirement readiness.
* Standard Matching.
* Advanced Matching.
* Reverse Matching.
* Batch Matching.
* Match review.
* Shortlist creation.
* Feedback update.
* Alternative suggestion.
* Stale result refresh.
* Rule review.
* Rule simulation.

## 67.2. Giá trị khởi tạo tham khảo

| Nghiệp vụ                           |                          SLA tham khảo |
| ----------------------------------- | -------------------------------------: |
| Quick Match                         |                               Vài giây |
| Standard Match                      | Dưới một phút với phạm vi thông thường |
| Alternative sau Listing unavailable |                          Trong 15 phút |
| Rule simulation                     |                Theo kích thước dữ liệu |
| Batch Matching                      |                          Theo lịch nền |
| Shortlist follow-up                 |                Trong một ngày làm việc |

Đây là mục tiêu cấu hình, không phải cam kết hardcode.

---

# 68. Notification

## 68.1. Sale

* Có Listing phù hợp mới.
* Top Listing thay đổi.
* Listing shortlist bị Hold/Booked/Sold.
* Giá thay đổi.
* Policy thay đổi.
* Match Result stale.
* Requirement thiếu dữ liệu.
* Customer feedback cần cập nhật.
* Alternative mới.

## 68.2. Team Lead

* Requirement không được Matching.
* Nhiều Customer không có sản phẩm phù hợp.
* Sale không follow-up shortlist.
* Override rank bất thường.
* Reverse Matching chưa được xử lý.

## 68.3. Inventory

* Nhu cầu cao nhưng thiếu nguồn cung.
* Listing có ít Customer phù hợp.
* Giá tạo khoảng trống lớn.
* Policy không phù hợp đa số nhu cầu.
* External status stale.

## 68.4. Director

* Supply–Demand Gap.
* Matching conversion thấp.
* Rule bias bất thường.
* Override rate cao.
* Project coverage thấp.

---

# 69. Candidate user experiences — không phải frontend contract canonical

> Exact routes, screens, components và responsive behavior thuộc Navigation/IA, Design System và Current Sprint Pack.


## 69.1. Requirement Matching Tab

Hiển thị:

* Matching readiness.
* Profile version.
* Last run.
* Top results.
* Shortlist.
* Alerts.
* Feedback.
* History.

## 69.2. Matching Workspace

Ba vùng:

### Criteria Panel

* Hard criteria.
* Soft criteria.
* Financial inputs.
* Stakeholder.
* Scenario.
* Missing data.

### Result Panel

* Listing cards/table.
* Score.
* Confidence.
* Result group.
* Price.
* Availability.
* Main reasons.
* Warnings.

### Shortlist Panel

* Selected items.
* Rank.
* Status.
* Comparison.
* Proposal action.

## 69.3. Match Result Detail

Các tab:

1. Overview.
2. Criteria Comparison.
3. Financial Fit.
4. Cash-Flow Fit.
5. Stakeholder Fit.
6. Legal Fit.
7. Price & Policy.
8. Availability.
9. Explanation.
10. History.
11. Audit.

## 69.4. Product Comparison

So sánh song song 2–10 Listing theo policy.

## 69.5. Shortlist Workspace

* Shortlist version.
* Item status.
* Sale ranking.
* Customer feedback.
* Proposal selection.
* Availability alerts.

## 69.6. Reverse Matching Workspace

* Listing.
* Matching scope.
* Requirement results.
* Responsible sale.
* Consent.
* Existing contact warning.
* Aggregate demand.

## 69.7. Rule Configuration Center

* Rule set.
* Version.
* Hard filters.
* Weights.
* Thresholds.
* Penalties.
* Simulation.
* Approval.
* Activation.

## 69.8. Supply–Demand Dashboard

* Demand heatmap.
* Budget gap.
* Product type gap.
* Geography gap.
* Unmatched Requirement.
* Unmatched Listing.
* Conversion.

---

# 70. Dashboard cho Sale

* Requirement chưa Match.
* Requirement cần bổ sung dữ liệu.
* Top new matches.
* Shortlist active.
* Listing shortlist sắp hết hạn.
* Listing unavailable.
* Alternative mới.
* Customer feedback chưa xử lý.
* Matching → Proposal conversion.
* Matching → Hold conversion.

---

# 71. Dashboard cho Team Lead

* Matching coverage của team.
* Requirement không có kết quả.
* Average Match Score.
* Shortlist aging.
* Sale override rate.
* Proposal conversion.
* Feedback completion.
* Unavailable top Listing.
* Reverse Match opportunities.
* Data completeness.

---

# 72. Dashboard cho Inventory Manager

* Listing có nhiều Requirement phù hợp.
* Listing ít hoặc không có Requirement phù hợp.
* Demand theo giá.
* Demand theo khu vực.
* Demand theo Asset type.
* Listing stale.
* Price gap.
* Policy gap.
* Availability impact.

Inventory Manager chỉ xem Customer identity khi có quyền.

---

# 73. Dashboard cho Director

* Matching coverage toàn công ty.
* Unmatched demand.
* Supply–Demand Gap.
* Conversion funnel.
* Project comparison.
* Legal Entity comparison.
* Average time Requirement → Shortlist.
* Average time Shortlist → Deal.
* Rule effectiveness.
* Override rate.
* Data quality.
* Project demand concentration.
* Budget distribution.

---

# 74. Candidate analytical questions — không phải certified Metrics

> Exact grain, formulas, dimensions, certification và access thuộc Analytics Context và Metric Registry.


* Matching Run.
* Matching by Requirement type.
* Matching by purpose.
* Matching by Project.
* Matching by Asset type.
* Matching by Legal Entity.
* Match Score distribution.
* Confidence distribution.
* Hard-filter failure reasons.
* Budget gap.
* Financial Fit.
* Cash-flow gap.
* Legal-fit failure.
* Location mismatch.
* Property criterion mismatch.
* Policy eligibility.
* Availability impact.
* Shortlist.
* Shortlist aging.
* Shortlist conversion.
* Customer rejection reason.
* Re-Matching.
* Listing alternative.
* Reverse Matching.
* Batch Matching.
* Campaign-oriented Matching.
* Rule version performance.
* Sale override.
* Matching → Proposal.
* Matching → Deal.
* Matching → Hold.
* Matching → Booking.
* Unmatched Requirement.
* Unmatched Listing.
* Supply–Demand Gap.
* Stale data.
* Financial Profile freshness.
* Inventory freshness.

Mọi báo cáo phải drill-down đúng scope.

---

# 75. Candidate data model — không phải physical schema canonical

> **Classification:** `CONTEXT-SPECIFIC DESIGN INPUT / PENDING VALIDATION`
> Exact tables, columns, constraints, indexes và cross-context references chỉ có hiệu lực khi được khóa trong Matching Context DB Specification và Alembic migrations. Cross-context references không mặc định tạo cross-schema business foreign keys.


## 75.1. Matching Profile

### `matching_profiles`

* `id`
* `profile_code`
* `customer_id`
* `requirement_id`
* `deal_id`
* `legal_entity_id`
* `profile_type`
* `status`
* `current_version`
* `created_by`
* `created_at`
* `updated_at`

### `matching_profile_versions`

* `id`
* `matching_profile_id`
* `version`
* `requirement_version`
* `financial_profile_id`
* `financial_profile_version`
* `stakeholder_snapshot_version`
* `profile_snapshot_json`
* `readiness_status`
* `data_completeness_score`
* `effective_from`
* `created_by`
* `created_at`

---

## 75.2. Criteria

### `matching_profile_criteria`

* `id`
* `matching_profile_version_id`
* `criterion_code`
* `criterion_category`
* `criterion_type`
* `operator_code`
* `value_json`
* `unit_code`
* `importance_level`
* `is_hard_filter`
* `is_exclusion`
* `weight_override`
* `source_type`
* `source_id`
* `confidence_level`
* `created_at`

### `matching_stakeholder_criteria`

* `id`
* `matching_profile_version_id`
* `stakeholder_id`
* `stakeholder_role`
* `criterion_code`
* `operator_code`
* `value_json`
* `importance_level`
* `stakeholder_weight`
* `is_veto`
* `created_at`

### `matching_profile_scenarios`

* `id`
* `matching_profile_version_id`
* `scenario_code`
* `name`
* `description`
* `criteria_overrides_json`
* `status`
* `created_by`
* `created_at`

---

## 75.3. Rule Set

### `matching_rule_sets`

* `id`
* `rule_set_code`
* `name`
* `scope_type`
* `scope_id`
* `requirement_type`
* `purpose_code`
* `asset_type`
* `status`
* `current_version`
* `created_at`

### `matching_rule_versions`

* `id`
* `matching_rule_set_id`
* `version`
* `hard_filter_rules_json`
* `score_formula_version`
* `confidence_rules_json`
* `tie_breaker_rules_json`
* `explanation_template_version`
* `effective_from`
* `effective_to`
* `status`
* `created_by`
* `reviewed_by`
* `approved_by`
* `created_at`

### `matching_rule_weights`

* `id`
* `matching_rule_version_id`
* `component_code`
* `weight`
* `minimum_component_score`
* `maximum_component_score`
* `created_at`

### `matching_score_thresholds`

* `id`
* `matching_rule_version_id`
* `result_group`
* `minimum_score`
* `maximum_score`
* `minimum_confidence`
* `additional_conditions_json`
* `created_at`

### `matching_penalty_rules`

* `id`
* `matching_rule_version_id`
* `penalty_code`
* `conditions_json`
* `penalty_value`
* `maximum_penalty`
* `created_at`

---

## 75.4. Matching Run

### `matching_runs`

* `id`
* `run_code`
* `matching_profile_id`
* `matching_profile_version_id`
* `customer_id`
* `requirement_id`
* `deal_id`
* `legal_entity_id`
* `scenario_id`
* `matching_mode`
* `matching_rule_version_id`
* `requested_scope_json`
* `effective_scope_json`
* `inventory_snapshot_reference`
* `candidate_set_hash`
* `candidate_count`
* `passed_hard_filter_count`
* `result_count`
* `status`
* `trigger_type`
* `trigger_resource_type`
* `trigger_resource_id`
* `requested_by`
* `started_at`
* `completed_at`
* `error_summary`
* `created_at`

### `matching_run_candidate_snapshots`

* `id`
* `matching_run_id`
* `listing_id`
* `listing_version`
* `asset_id`
* `price_list_version_id`
* `price_item_id`
* `sales_policy_version_ids_json`
* `availability_snapshot_id`
* `access_result`
* `candidate_status`
* `created_at`

---

## 75.5. Hard Filter Result

### `matching_hard_filter_results`

* `id`
* `matching_run_id`
* `listing_id`
* `passed`
* `failed_rule_count`
* `reason_codes_json`
* `created_at`

### `matching_hard_filter_details`

* `id`
* `hard_filter_result_id`
* `criterion_code`
* `rule_code`
* `requirement_value_json`
* `listing_value_json`
* `result`
* `reason_code`
* `internal_explanation`
* `customer_explanation`
* `created_at`

---

## 75.6. Match Result

### `matching_results`

* `id`
* `matching_run_id`
* `listing_id`
* `asset_id`
* `total_score`
* `confidence_score`
* `system_rank`
* `result_group`
* `hard_filter_passed`
* `financial_fit_status`
* `cashflow_fit_status`
* `availability_result`
* `price_amount`
* `currency`
* `main_strengths_json`
* `main_concerns_json`
* `data_gaps_json`
* `staleness_status`
* `created_at`

### `matching_result_components`

* `id`
* `matching_result_id`
* `component_code`
* `raw_score`
* `normalized_score`
* `weight`
* `weighted_score`
* `maximum_score`
* `explanation_json`
* `created_at`

### `matching_result_criterion_details`

* `id`
* `matching_result_id`
* `criterion_code`
* `requirement_value_json`
* `listing_value_json`
* `comparison_result`
* `score`
* `weight`
* `penalty`
* `source_reference_json`
* `confidence_level`
* `internal_explanation`
* `customer_explanation`
* `created_at`

### `matching_result_penalties`

* `id`
* `matching_result_id`
* `penalty_code`
* `penalty_value`
* `reason`
* `source_reference`
* `created_at`

### `matching_result_explanations`

* `id`
* `matching_result_id`
* `explanation_type`
* `audience_type`
* `language_code`
* `summary`
* `details_json`
* `generated_by`
* `template_version`
* `created_at`

---

## 75.7. Financial Fit

### `matching_financial_fit_snapshots`

* `id`
* `matching_result_id`
* `financial_profile_id`
* `financial_profile_version`
* `price_amount`
* `estimated_policy_benefit`
* `estimated_total_obligation`
* `required_initial_capital`
* `available_own_capital`
* `estimated_loan_need`
* `estimated_monthly_payment`
* `financial_gap`
* `fit_status`
* `assumptions_json`
* `calculation_version`
* `created_at`

### `matching_cashflow_milestones`

* `id`
* `financial_fit_snapshot_id`
* `milestone_code`
* `due_at`
* `required_amount`
* `available_amount`
* `gap_amount`
* `funding_source`
* `fit_status`
* `created_at`

---

## 75.8. Sale Override

### `matching_result_overrides`

* `id`
* `matching_result_id`
* `override_type`
* `system_rank`
* `sale_rank`
* `reason_code`
* `reason`
* `created_by`
* `approved_by`
* `created_at`
* `ended_at`

---

## 75.9. Shortlist

### `product_shortlists`

* `id`
* `shortlist_code`
* `customer_id`
* `requirement_id`
* `deal_id`
* `matching_run_id`
* `legal_entity_id`
* `version`
* `status`
* `created_by`
* `created_at`
* `updated_at`

### `product_shortlist_items`

* `id`
* `shortlist_id`
* `listing_id`
* `matching_result_id`
* `system_rank`
* `sale_rank`
* `customer_priority`
* `status`
* `reason`
* `price_snapshot_reference`
* `availability_snapshot_reference`
* `added_by`
* `added_at`
* `removed_at`

### `product_shortlist_versions`

* `id`
* `shortlist_id`
* `version`
* `snapshot_json`
* `change_reason`
* `created_by`
* `created_at`

---

## 75.10. Comparison

### `product_comparison_sessions`

* `id`
* `comparison_code`
* `customer_id`
* `requirement_id`
* `shortlist_id`
* `audience_type`
* `status`
* `created_by`
* `created_at`

### `product_comparison_items`

* `id`
* `comparison_session_id`
* `listing_id`
* `matching_result_id`
* `display_order`
* `comparison_snapshot_json`
* `created_at`

---

## 75.11. Feedback

### `product_match_feedback`

* `id`
* `customer_id`
* `requirement_id`
* `matching_result_id`
* `listing_id`
* `stakeholder_id`
* `feedback_type`
* `feedback_source`
* `feedback_value_json`
* `comment`
* `occurred_at`
* `recorded_by`
* `created_at`

### `matching_requirement_update_suggestions`

* `id`
* `requirement_id`
* `source_feedback_ids_json`
* `suggested_changes_json`
* `confidence_score`
* `status`
* `reviewed_by`
* `reviewed_at`
* `created_at`

---

## 75.12. Alert

### `matching_change_alerts`

* `id`
* `customer_id`
* `requirement_id`
* `shortlist_id`
* `listing_id`
* `alert_type`
* `severity`
* `old_snapshot_json`
* `new_snapshot_json`
* `alternative_run_id`
* `status`
* `assigned_user_id`
* `created_at`
* `acknowledged_at`
* `resolved_at`

---

## 75.13. Reverse Matching

### `reverse_matching_runs`

* `id`
* `run_code`
* `listing_id`
* `listing_version`
* `legal_entity_id`
* `matching_rule_version_id`
* `scope_type`
* `scope_id`
* `candidate_requirement_count`
* `result_count`
* `status`
* `requested_by`
* `started_at`
* `completed_at`
* `created_at`

### `reverse_matching_results`

* `id`
* `reverse_matching_run_id`
* `customer_id`
* `requirement_id`
* `responsible_user_id`
* `total_score`
* `confidence_score`
* `rank`
* `consent_status`
* `access_level`
* `main_fit_reasons_json`
* `main_concerns_json`
* `existing_contact_warning`
* `created_at`

---

## 75.14. Batch Matching

### `batch_matching_runs`

* `id`
* `batch_code`
* `batch_type`
* `scope_type`
* `scope_id`
* `trigger_type`
* `matching_rule_version_id`
* `requirement_count`
* `listing_count`
* `completed_requirement_count`
* `error_count`
* `checkpoint_json`
* `status`
* `created_by`
* `started_at`
* `completed_at`
* `created_at`

### `batch_matching_run_items`

* `id`
* `batch_matching_run_id`
* `requirement_id`
* `matching_run_id`
* `status`
* `error_message`
* `created_at`

---

## 75.15. Supply–Demand Aggregate

### `matching_supply_demand_operational_aggregates`

* `id`
* `snapshot_date`
* `legal_entity_id`
* `project_id`
* `geography_code`
* `asset_type`
* `budget_bucket`
* `requirement_count`
* `active_listing_count`
* `matched_requirement_count`
* `unmatched_requirement_count`
* `unmatched_listing_count`
* `average_match_score`
* `gap_index`
* `calculation_version`
* `created_at`

---

# 76. Candidate application operations — không phải OpenAPI canonical

> Các operations dưới đây là capability inventory. Exact paths, methods, payloads, errors, idempotency và authorization metadata thuộc OpenAPI.


## Matching Profile

```text
GET    /matching-profiles
POST   /matching-profiles
GET    /matching-profiles/{id}
PATCH  /matching-profiles/{id}
POST   /matching-profiles/{id}/versions
GET    /matching-profile-versions/{id}
POST   /matching-profile-versions/{id}/validate-readiness
POST   /matching-profile-versions/{id}/scenarios
```

## Requirement Matching

```text
POST   /requirements/{id}/matching-runs
GET    /requirements/{id}/matching-runs
GET    /matching-runs/{id}
GET    /matching-runs/{id}/results
GET    /matching-runs/{id}/excluded-results
POST   /matching-runs/{id}/cancel
POST   /matching-runs/{id}/rerun
```

## Match Result

```text
GET    /matching-results/{id}
GET    /matching-results/{id}/explanation
GET    /matching-results/{id}/financial-fit
GET    /matching-results/{id}/criterion-details
POST   /matching-results/{id}/sale-rank
POST   /matching-results/{id}/exclude
POST   /matching-results/{id}/restore
```

## Shortlist

```text
GET    /customers/{id}/shortlists
POST   /customers/{id}/shortlists
GET    /product-shortlists/{id}
PATCH  /product-shortlists/{id}
POST   /product-shortlists/{id}/items
PATCH  /product-shortlist-items/{id}
POST   /product-shortlist-items/{id}/remove
POST   /product-shortlists/{id}/create-version
GET    /product-shortlists/{id}/history
```

## Comparison

```text
POST   /product-comparisons
GET    /product-comparisons/{id}
POST   /product-comparisons/{id}/items
POST   /product-comparisons/{id}/snapshot
```

## Feedback

```text
POST   /matching-results/{id}/feedback
GET    /requirements/{id}/matching-feedback
GET    /requirements/{id}/update-suggestions
POST   /requirement-update-suggestions/{id}/accept-and-request-party-update
POST   /requirement-update-suggestions/{id}/reject
```

## Alternative

```text
POST   /product-shortlist-items/{id}/find-alternatives
GET    /matching-alerts
POST   /matching-alerts/{id}/acknowledge
POST   /matching-alerts/{id}/resolve
```

## Reverse Matching

```text
POST   /property-listings/{id}/reverse-matching-runs
GET    /property-listings/{id}/reverse-matching-runs
GET    /reverse-matching-runs/{id}
GET    /reverse-matching-runs/{id}/results
```

## Batch Matching

```text
POST   /batch-matching-runs
GET    /batch-matching-runs
GET    /batch-matching-runs/{id}
POST   /batch-matching-runs/{id}/cancel
POST   /batch-matching-runs/{id}/retry-errors
```

## Rule Set

```text
GET    /matching-rule-sets
POST   /matching-rule-sets
GET    /matching-rule-sets/{id}
POST   /matching-rule-sets/{id}/versions
GET    /matching-rule-versions/{id}
PATCH  /matching-rule-versions/{id}
POST   /matching-rule-versions/{id}/validate
POST   /matching-rule-versions/{id}/simulate
POST   /matching-rule-versions/{id}/submit-review
POST   /matching-rule-versions/{id}/approve
POST   /matching-rule-versions/{id}/activate
```

## Supply–Demand

```text
GET    /matching-analytics/supply-demand
GET    /matching-analytics/unmatched-requirements
GET    /matching-analytics/unmatched-listings
GET    /matching-analytics/conversion
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
* Consent.
* Rule version.
* Price/policy version.
* Availability freshness.
* Scope.
* Idempotency.

---

# 77. Candidate permission vocabulary — không phải Permission Registry canonical

> Exact permission codes, scopes, role mappings, concealment và field masking thuộc security registries/matrices.


## Matching Profile

```text
matching_profile.view
matching_profile.create
matching_profile.update
matching_profile.create_version
matching_profile.validate
matching_profile.manage_scenario
```

## Matching Run

```text
matching.run
matching.quick_run
matching.advanced_run
matching.rerun
matching.cancel
matching.view
matching.view_explanation
matching.view_excluded
matching.view_history
matching.view_audit
```

## Financial Explanation

```text
matching_financial.view_summary
matching_financial.view_detail
matching_financial.view_cashflow
matching_financial.view_assumptions
```

## Override

```text
matching_override.rank
matching_override.exclude
matching_override.restore
matching_override.view_history
```

## Shortlist

```text
matching_shortlist.view
matching_shortlist.create
matching_shortlist.update
matching_shortlist.add_item
matching_shortlist.remove_item
matching_shortlist.create_version
matching_shortlist.select_for_proposal
matching_shortlist.view_history
```

## Comparison

```text
matching_comparison.view
matching_comparison.create
matching_comparison.snapshot
matching_comparison.share_internal
```

## Feedback

```text
matching_feedback.view
matching_feedback.create
matching_feedback.apply_suggestion
matching_feedback.reject_suggestion
```

## Reverse Matching

```text
reverse_matching.run
reverse_matching.view
reverse_matching.view_customer_identity
reverse_matching.view_aggregate
reverse_matching.export
```

## Batch Matching

```text
batch_matching.view
batch_matching.create
batch_matching.cancel
batch_matching.retry
```

## Rule Configuration

```text
matching_rule.view
matching_rule.create
matching_rule.update_draft
matching_rule.validate
matching_rule.simulate
matching_rule.review
matching_rule.approve
matching_rule.activate
matching_rule.view_history
```

## Analytics

```text
matching_analytics.view
matching_analytics.view_supply_demand
matching_analytics.view_unmatched_customer
matching_analytics.view_unmatched_listing
matching_analytics.export
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

# 78. Candidate role baseline — không phải Role/Permission Registry canonical

> Role descriptions chỉ mô tả product intent. Backend authority phải được resolve từ IAM/Security canonical sources.


## 78.1. Sale

Được:

* Chạy Matching cho Requirement của mình.
* Xem Listing được cấp.
* Xem Match Explanation.
* Xem Financial summary.
* Tạo Shortlist.
* So sánh sản phẩm.
* Ghi feedback.
* Thay sale rank có lý do.
* Chọn Listing cho Proposal.

Không được:

* Chạy Reverse Matching toàn công ty.
* Xem Customer khác.
* Sửa System Score.
* Sửa Rule.
* Xem Financial Detail không được cấp.
* Xem Floor Price nếu không có quyền.
* Tạo Hold trong Customer–Product Matching Capability.

## 78.2. Team Lead

Được:

* Xem Matching team.
* Chạy Reverse Matching scope team.
* Review override.
* Theo dõi shortlist.
* Xem conversion.
* Xử lý Requirement không có kết quả.

## 78.3. Department Head

Được:

* Scope department.
* Reverse Matching department.
* Xem supply–demand.
* Review rule theo quyền.
* Phê duyệt ngoại lệ.

## 78.4. Inventory Manager

Được:

* Xem aggregate demand.
* Xem Listing fit statistics.
* Chạy Reverse Matching aggregate.
* Không mặc định xem Customer identity.

## 78.5. Finance

Được:

* Xem Financial Fit trong context được giao.
* Review assumptions.
* Không mặc định sửa Matching Rule.

## 78.6. Director

Được:

* Xem toàn bộ theo scope.
* Phê duyệt Rule.
* Xem supply–demand.
* Export có audit.

---

# 79. Candidate business facts — không phải Event contracts canonical

> Exact Event names, versions, payloads, channels và consumers thuộc JSON Schema, AsyncAPI và Event Registry.


Customer–Product Matching Capability phát:

```text
matching_profile.created
matching_profile.version_created
matching_profile.readiness_changed

matching.run_requested
matching.run_started
matching.run_completed
matching.run_failed
matching.run_cancelled

matching.result_created
matching.result_group_changed
matching.result_became_stale

matching.shortlist_created
matching.shortlist_item_added
matching.shortlist_item_removed
matching.shortlist_item_status_changed
matching.shortlist_version_created

matching.feedback_recorded
matching.requirement_update_suggested
matching.requirement_update_suggestion_accepted

matching.alert_created
matching.alternative_generated

reverse_matching.run_started
reverse_matching.run_completed

batch_matching.started
batch_matching.completed
batch_matching.failed

matching_rule.version_created
matching_rule.simulated
matching_rule.activated

matching.supply_demand_snapshot_created
```

Consumer phải idempotent.

---

# 80. Candidate Platform configuration references

> Exact configuration keys, schemas, scopes và resolution strategies thuộc Platform Context contracts.


```text
matching.default_rule_set
matching.rule_resolution_policy
matching.profile_readiness_policy
matching.hard_filter_policy
matching.score_weight_policy
matching.threshold_policy
matching.penalty_policy
matching.confidence_policy
matching.tie_breaker_policy

matching.financial_fit_policy
matching.cashflow_fit_policy
matching.stakeholder_policy
matching.legal_fit_policy
matching.purpose_fit_policy

matching.inventory_freshness_policy
matching.price_freshness_policy
matching.policy_freshness_policy
matching.financial_profile_freshness_policy

matching.shortlist_policy
matching.sale_override_policy
matching.feedback_policy
matching.rematching_policy
matching.alternative_policy

matching.reverse_matching_policy
matching.batch_policy
matching.campaign_matching_policy

matching.explanation_policy
matching.ai_assistance_policy
matching.notification_policy
matching.sla_policy
matching.result_retention_policy
matching.analytics_policy
```

Mọi configuration definition phải công bố schema, allowed scopes, resolution strategy, version, effective period, owner, approval và Audit requirements khi phù hợp.

---

# 81. System invariant

Các quy tắc sau không được cấu hình tắt:

1. Matching không tự tạo Hold.
2. Matching không tự tạo Booking.
3. Matching không tự gửi Proposal.
4. Matching không tự tạo Deal.
5. Hard Filter luôn chạy trước Soft Scoring.
6. Hard Fail không được Score override.
7. User không được sửa System Score.
8. Matching chỉ dùng Listing user được phép xem.
9. Matching không mở rộng Customer scope.
10. Reverse Matching không mở rộng Customer access.
11. Financial Profile ngoài quyền không được sử dụng hoặc hiển thị.
12. Match Result phải tham chiếu Rule version.
13. Match Result phải tham chiếu Listing/Price/Policy version.
14. Availability phải có timestamp.
15. Match Result cũ không được dùng thay Availability check khi Hold/Booking.
16. Sale Override phải lưu riêng.
17. Commission không được dùng trong Customer Fit Score.
18. Consent phải được kiểm tra trước outbound action.
19. Matching Result lịch sử không được ghi đè.
20. Rule active không sửa trực tiếp.
21. AI không tự thay dữ liệu nguồn.
22. Matching không xác nhận khả năng vay.
23. Backend luôn enforce scope.
24. Field nhạy cảm không được gửi ngoài quyền.
25. Matching Run phải tái tạo được từ snapshot/version.

---

# 82. Rule nghiệp vụ bắt buộc

1. Matching Profile không thay Requirement.
2. Một Requirement có thể có nhiều Matching Profile Version.
3. Matching Run phải dùng một Profile Version cụ thể.
4. Matching Run phải dùng một Rule Version cụ thể.
5. Candidate Pool phải giới hạn theo quyền.
6. Frontend không được mở rộng Candidate Pool.
7. Listing archived không được Match.
8. Listing sold không được Match như available.
9. Listing hết hạn không được Immediate Fit.
10. Mandate không hợp lệ phải loại.
11. Listing không có giá active phải loại.
12. Listing không có readiness phù hợp phải loại.
13. Availability stale phải cảnh báo hoặc loại theo policy.
14. Hard Filter chạy trước chấm điểm.
15. Mandatory criterion vi phạm phải loại.
16. Not Acceptable criterion vi phạm phải loại.
17. Score không được cứu Hard Fail.
18. Điểm phải nằm từ 0 đến 100.
19. Tổng trọng số phải hợp lệ.
20. Penalty phải giải thích được.
21. Confidence phải tách khỏi Match Score.
22. Confidence không phải xác suất mua.
23. Match Score không phải xác suất mua.
24. Score không được sử dụng commission.
25. Score không được sử dụng margin để ưu tiên Customer.
26. Financial Fit phải ghi assumptions.
27. Financial Fit không phải phê duyệt vay.
28. Customer từ chối Financial Profile vẫn có thể Matching cơ bản.
29. Financial Profile stale phải cảnh báo.
30. Cash-Flow Fit không chỉ dựa tổng giá.
31. Policy benefit chưa chắc chắn không tính như confirmed.
32. Stakeholder veto không được trung bình hóa mất.
33. Stakeholder conflict phải hiển thị.
34. Hệ thống không tự quyết định stakeholder nào thắng.
35. Scenario phải lưu riêng.
36. Result Group phải dựa score và điều kiện bổ sung.
37. Immediate Fit phải có Availability phù hợp.
38. Excluded Listing không vào shortlist mặc định.
39. Sale có thể thêm Alternative có reason.
40. Sale không sửa System Score.
41. Sale rank phải tách system rank.
42. Shortlist không khóa Listing.
43. Shortlist không đảm bảo còn hàng.
44. Shortlist phải lưu Price/Availability reference.
45. Proposal phải gọi lại Availability khi cần.
46. Deal and Transaction Capability phải kiểm tra Availability trước Hold.
47. Feedback không tự sửa Requirement.
48. Requirement update cần user xác nhận.
49. Feedback phải có source.
50. Re-Matching không ghi đè run cũ.
51. Re-Matching tự động không tự thay shortlist.
52. Alternative không tự thay Proposal.
53. Alert phải chống trùng.
54. Reverse Matching chỉ dùng Requirement active.
55. Reverse Matching không quét Customer không có context.
56. Inventory Manager không mặc định xem Customer identity.
57. Campaign-oriented Matching phải kiểm tra consent.
58. Campaign-oriented Matching không tự gửi outbound.
59. Batch Matching phải có checkpoint.
60. Batch Matching phải idempotent.
61. Rule active không sửa trực tiếp.
62. Rule mới không áp dụng hồi tố.
63. Rule Simulation không ghi production result.
64. Weight âm không hợp lệ.
65. Threshold chồng lấn không hợp lệ.
66. Hard criterion không phụ thuộc weight.
67. Explanation phải có nguồn dữ liệu.
68. Customer-facing explanation không lộ internal data.
69. Floor Price không được hiển thị ngoài quyền.
70. Owner contact không được hiển thị.
71. Financial detail phải field-mask.
72. Matching History phải giữ version.
73. Match Result stale phải được đánh dấu.
74. Price thay đổi phải tạo alert cho shortlist.
75. Policy thay đổi phải tạo alert khi ảnh hưởng.
76. Listing unavailable phải tạo Alternative suggestion theo policy.
77. Matching không tự xác nhận legal eligibility.
78. Legal conditional phải hiển thị điều kiện.
79. Private Listing chỉ được Match trong access scope.
80. Exact private location phải được bảo vệ.
81. Multi-Legal Entity phải kiểm tra context.
82. Customer dùng chung Enterprise không mở cross-entity data.
83. Project Access không mở Customer scope.
84. Listing Access không mở Financial Profile.
85. View không đồng nghĩa Export.
86. Sale không bulk export Reverse Matching Customer.
87. Marketing không xem Financial Profile.
88. AI suggestion phải có confidence.
89. AI không tự tạo Hold/Booking.
90. AI không sửa Score ngoài model version.
91. Cache không phải nguồn Availability cuối cùng.
92. Cache không phải nguồn permission.
93. Cache không phải nguồn price active cuối cùng khi giao dịch.
94. Matching Run thất bại phải có error audit.
95. Matching Result phải có timestamp.
96. Matching must use canonical Customer.
97. Merged Customer source không chạy Matching mới.
98. Requirement archived không chạy Standard Match.
99. Consent restriction không bị bỏ qua trong outbound.
100. Audit Matching không được sửa.
101. System rank phải tái tạo được.
102. Manual override phải có reason.
103. Override rate cao phải cảnh báo.
104. Rule bias bất thường phải được review.
105. Supply–Demand analytics phải aggregate theo quyền.
106. Unmatched demand không lộ Customer identity.
107. Reverse Matching result phải cảnh báo duplicate outreach.
108. Existing Deal/Proposal phải được hiển thị.
109. Customer đã từ chối Listing không được đề xuất lại không có cảnh báo.
110. Capability phải hỗ trợ mọi mô hình nguồn cung của Product, Asset, Listing and Inventory Capability.

---

# 83. Cảnh báo và phát hiện bất thường

Hệ thống cần cảnh báo khi:

* Requirement active nhưng chưa có Matching Profile.
* Requirement Matching Ready nhưng chưa chạy.
* Matching Profile thiếu budget.
* Matching Profile có Mandatory criteria mâu thuẫn.
* Stakeholder veto mâu thuẫn.
* Financial Profile hết hạn.
* Availability stale.
* Price version hết hiệu lực.
* Policy version hết hiệu lực.
* Rule version không active nhưng được dùng cho run mới.
* Candidate Pool bằng 0.
* Tất cả Listing bị Hard Fail.
* Score distribution bất thường.
* Một Listing luôn đứng đầu mọi Customer do rule lỗi.
* Sale override quá nhiều.
* Sale luôn loại top result.
* Sale cố thêm Excluded Listing.
* Immediate Fit nhưng Availability không hợp lệ.
* Listing shortlist bị sold.
* Listing shortlist giá tăng.
* Listing shortlist policy bị rút.
* Proposal dùng Match Result stale.
* Reverse Matching trả Customer ngoài scope.
* Inventory Manager xem Customer identity trái quyền.
* Batch job lỗi nhiều.
* Matching runtime tăng bất thường.
* Candidate count tăng đột biến.
* Rule activation làm giảm mạnh coverage.
* Financial Fit dùng profile hết hạn.
* Customer feedback không được xử lý.
* Requirement update suggestion tồn đọng.
* Campaign-oriented Matching không có consent.
* Matching Result không có explanation.
* Score component không cộng đúng total.
* Total score vượt 100.
* Hard Fail vẫn có Result Group phù hợp.
* Same Listing có nhiều result trùng trong một run.
* Merged Customer vẫn có Matching Run mới.
* Private Listing xuất hiện ngoài Project/Listing Access.
* Floor Price xuất hiện trong Customer-facing explanation.
* Commission/margin bị sử dụng trong Customer Fit Score.
* Reverse Matching tạo duplicate outreach.
* Alert lặp quá nhiều.
* Supply–Demand aggregate có Customer count quá nhỏ cần bảo vệ privacy.

---

# 84. Audit requirements và evidence

> Audit Context sở hữu immutable Audit facts. Matching Context phát sinh audit-worthy facts/references; operational logs không thay Audit.


## 84.1. Thao tác bắt buộc

* Tạo Matching Profile.
* Tạo Profile Version.
* Chỉnh criterion.
* Tạo scenario.
* Chạy Matching.
* Re-Matching.
* Xem Financial Explanation nhạy cảm.
* Xem excluded result.
* Thay sale rank.
* Exclude/restore Listing.
* Tạo Shortlist.
* Thêm/xóa item.
* Tạo Comparison.
* Ghi feedback.
* Chấp nhận Requirement suggestion.
* Chạy Reverse Matching.
* Chạy Batch Matching.
* Tạo/chỉnh/simulate/activate Rule.
* Export.
* Xem Customer identity từ Reverse Matching.

## 84.2. Nội dung

* Actor.
* Role.
* Legal Entity.
* Customer.
* Requirement.
* Deal.
* Listing.
* Matching Profile Version.
* Matching Rule Version.
* Price/Policy Version.
* Availability timestamp.
* Before.
* After.
* Reason.
* Approval.
* Scope.
* Field policy.
* IP.
* Device.
* Request ID.
* Correlation ID.
* Job ID.
* Timestamp.
* Result.

---

# 85. Phạm vi MVP

## 85.1. Bắt buộc

* Matching Profile từ Requirement.
* Profile Version.
* Matching readiness.
* Candidate Pool.
* Project/Listing Access filter.
* Listing eligibility.
* Hard Filter.
* Soft Scoring.
* Configurable weights.
* Configurable thresholds.
* Financial Fit cơ bản.
* Budget Fit.
* Initial capital estimate.
* Loan need estimate.
* Property Fit.
* Geography Fit.
* Timing Fit.
* Policy Fit cơ bản.
* Explanation.
* Confidence.
* Result Group.
* Ranking.
* Sale rank override.
* Shortlist.
* Shortlist version.
* Product Comparison.
* Feedback.
* Re-Matching.
* Match History.
* Listing unavailable alert.
* Price/policy alert.
* Alternative suggestion.
* Reverse Matching scope mine/team/department.
* Rule version.
* Rule simulation cơ bản.
* Batch Matching cơ bản.
* Supply–Demand aggregate cơ bản.
* Field masking.
* Audit.
* Dashboard.
* Domain event.

## 85.2. Giai đoạn nâng cao

* Advanced cash-flow Matching.
* Multi-stakeholder scenario.
* AI criterion extraction.
* AI explanation.
* AI feedback classification.
* Behavioral preference model.
* Machine-learning ranking.
* Dynamic weights.
* Rental yield model.
* ROI model.
* Exit-liquidity model.
* Geospatial travel-time Matching.
* Multi-unit purchase Matching.
* Package/bundle Matching.
* Campaign audience token.
* Real-time event-driven Re-Matching.
* Customer self-service preference update.
* Customer Portal shortlist.
* Explainable recommendation graph.
* Advanced supply planning.
* New project product-design analytics.

---

# 86. Tiêu chí nghiệm thu

Capability được xem là đạt khi:

1. Tạo được Matching Profile từ Requirement.
2. Matching Profile không thay Requirement.
3. Tạo được Profile Version.
4. Run cũ giữ Profile Version cũ.
5. Matching readiness hoạt động.
6. Thiếu dữ liệu được cảnh báo.
7. Quick Match chạy được với dữ liệu tối thiểu.
8. Quick Match có confidence thấp hơn khi thiếu dữ liệu.
9. Standard Match yêu cầu Requirement active.
10. Advanced Match hỗ trợ Financial Profile.
11. Candidate Pool giới hạn theo Project Access.
12. Candidate Pool giới hạn theo Listing Access.
13. Candidate Pool giới hạn theo Legal Entity.
14. Private Listing không xuất hiện ngoài quyền.
15. Listing archived không vào candidate.
16. Listing sold không vào available result.
17. Mandate invalid bị loại.
18. Listing hết hạn bị loại hoặc cảnh báo đúng policy.
19. Listing không có giá active bị loại.
20. Listing readiness không đạt bị loại.
21. Hard Filter chạy trước Score.
22. Mandatory criterion vi phạm bị loại.
23. Not Acceptable criterion vi phạm bị loại.
24. Score không override Hard Fail.
25. Hard-filter detail được lưu.
26. Hard Fail có explanation.
27. Soft Scoring hoạt động.
28. Điểm nằm từ 0 đến 100.
29. Tổng trọng số hợp lệ.
30. Score component cộng đúng total.
31. Financial Fit được tính.
32. Budget target và budget max tách biệt.
33. Vượt target nhưng dưới max bị giảm điểm.
34. Vượt absolute max bị Hard Fail.
35. Tính được initial capital.
36. Tính được estimated loan need.
37. Tính được financial gap.
38. Financial estimate có assumptions.
39. Financial estimate không được hiển thị như loan approval.
40. Financial Profile stale được cảnh báo.
41. Customer từ chối Financial Profile vẫn chạy basic Match.
42. Sale chỉ xem Financial summary.
43. Finance xem detail theo quyền.
44. Cash-flow milestone cơ bản hoạt động.
45. Payment schedule được so sánh.
46. Purpose Fit mua để ở hoạt động.
47. Purpose Fit đầu tư hoạt động.
48. Geography Fit hoạt động.
49. Property Type Fit hoạt động.
50. Area range Fit hoạt động.
51. Bedroom criteria hoạt động.
52. Direction/View Fit hoạt động.
53. Legal Fit hoạt động.
54. Legal condition được giải thích.
55. Timing Fit hoạt động.
56. Policy eligibility được kiểm tra.
57. Conditional policy không tính như confirmed.
58. Stakeholder criteria được lưu.
59. Stakeholder veto được hỗ trợ.
60. Stakeholder conflict được cảnh báo.
61. Hệ thống không tự chọn người thắng.
62. Tạo được scenario.
63. Scenario tạo kết quả riêng.
64. Penalty hoạt động.
65. Penalty có explanation.
66. Confidence score hoạt động.
67. Confidence tách Match Score.
68. Result Group hoạt động.
69. Immediate Fit cần Availability phù hợp.
70. Conditional Fit hiển thị điều kiện.
71. Alternative group hoạt động.
72. Excluded group hoạt động.
73. Ranking hoạt động.
74. Tie-breaker hoạt động.
75. Commission không ảnh hưởng Customer Fit Score.
76. Margin không ảnh hưởng Customer Fit Score.
77. Explanation tổng quan được tạo.
78. Explanation từng criterion được tạo.
79. Customer-facing explanation không lộ Floor Price.
80. Customer-facing explanation không lộ Owner contact.
81. Match Result lưu Listing Version.
82. Match Result lưu Price Version.
83. Match Result lưu Policy Version.
84. Match Result lưu Rule Version.
85. Match Result lưu Availability timestamp.
86. Run lịch sử xem được.
87. Run lịch sử không bị ghi đè.
88. Re-Matching tạo run mới.
89. Re-Matching so sánh kết quả cũ/mới.
90. Price change làm result stale.
91. Policy change làm result stale.
92. Availability change làm result stale.
93. Requirement change làm result stale.
94. Tạo được Shortlist.
95. Shortlist không khóa Listing.
96. Shortlist có nhiều item.
97. Shortlist có version.
98. Shortlist lưu system rank.
99. Shortlist lưu sale rank.
100. Sale rank không sửa system rank.
101. Sale override cần reason.
102. Sale không biến Hard Fail thành Immediate Fit.
103. Product Comparison hoạt động.
104. Comparison hiển thị giá.
105. Comparison hiển thị Financial Fit.
106. Comparison hiển thị legal readiness.
107. Comparison tuân thủ field permission.
108. Chọn được item cho Proposal.
109. Deal and Transaction Capability nhận snapshot phù hợp.
110. Proposal action không tự tạo Hold.
111. Ghi được Customer feedback.
112. Ghi được stakeholder feedback.
113. Feedback có source.
114. Feedback không tự sửa Requirement.
115. Requirement suggestion được tạo.
116. Sale chấp nhận hoặc từ chối suggestion được.
117. Listing Customer đã từ chối được cảnh báo khi đề xuất lại.
118. Listing shortlist bị Hold tạo alert.
119. Listing shortlist bị sold tạo alert.
120. Giá thay đổi tạo alert.
121. Policy thay đổi tạo alert.
122. Tìm được Alternative.
123. Alternative không tự thay shortlist.
124. Reverse Matching chạy được.
125. Sale Reverse Match chỉ scope mine.
126. Team Lead Reverse Match scope team.
127. Department Head scope department.
128. Inventory Manager chỉ xem aggregate mặc định.
129. Reverse result có responsible sale.
130. Reverse result có consent status.
131. Reverse result cảnh báo duplicate outreach.
132. Reverse Matching không tạo Customer access mới.
133. Batch Matching chạy nền.
134. Batch Matching có checkpoint.
135. Batch Matching idempotent.
136. Batch lỗi có retry.
137. Campaign-oriented Matching kiểm tra consent.
138. Campaign-oriented Matching không tự gửi outbound.
139. Rule Set được tạo.
140. Rule Version được tạo.
141. Active Rule không sửa trực tiếp.
142. Rule Simulation hoạt động.
143. Simulation không ghi production result.
144. Rule activation có approval.
145. Rule mới không sửa run cũ.
146. Weight âm bị từ chối.
147. Threshold chồng lấn bị từ chối.
148. Supply–Demand snapshot được tính.
149. Unmatched Requirement được báo cáo.
150. Unmatched Listing được báo cáo.
151. Supply–Demand report không lộ Customer identity trái quyền.
152. Matching conversion funnel hoạt động.
153. Sale chỉ xem Customer context của mình.
154. Team Lead xem scope team.
155. Department Head xem scope department.
156. Director xem scope được cấp.
157. Backend enforce scope.
158. Sửa URL không mở rộng quyền.
159. Field masking hoạt động.
160. Sale không bulk export Reverse Matching Customer.
161. Marketing không xem Financial Profile.
162. AI suggestion không tự sửa dữ liệu.
163. AI không tự tạo Hold.
164. AI không tự tạo Booking.
165. Cache không quyết định Availability cuối cùng.
166. Deal and Transaction Capability gọi lại Availability trước Hold.
167. Merged Customer không tạo run mới.
168. Archived Requirement không Standard Match.
169. Audit lưu actor và reason.
170. Audit lưu Rule Version.
171. Audit lưu Price/Policy Version.
172. Audit lưu sale override.
173. Domain event được phát.
174. Event consumer idempotent.
175. Capability hỗ trợ Project tự phát triển.
176. Capability hỗ trợ Project phân phối ngoài.
177. Capability hỗ trợ Company-owned Listing.
178. Capability hỗ trợ Listing ký gửi.
179. Capability hỗ trợ đất nền.
180. Capability hỗ trợ đất riêng lẻ.
181. Capability hỗ trợ nhiều Project.
182. Capability hỗ trợ một Project.
183. Capability hỗ trợ nhiều Stakeholder.
184. Capability hỗ trợ Customer không có Financial Profile đầy đủ.
185. Capability không tự thay quyết định của sale/Customer.
186. Capability không tự giữ hoặc bán sản phẩm.
187. Capability cung cấp Shortlist cho Deal and Transaction Capability.
188. Capability cung cấp snapshot có version.
189. Capability cung cấp phân tích cung–cầu.
190. Capability hoạt động như Matching Engine thống nhất toàn Enterprise.

---

# 87. Anti-patterns và canonical requirements

Phần này quy định các hành vi bị cấm và cách triển khai canonical cho dự án Greenfield.

## AP-MAT-001 — Ghép Customer trực tiếp với Unit

**Không được áp dụng**

Bỏ qua Requirement và coi một Project Unit là toàn bộ mô hình nguồn cung.

**Canonical requirement**

Matching chủ yếu ghép versioned Requirement/Matching Profile với canonical Listing thuộc mọi approved supply model.

## AP-MAT-002 — Một điểm tổng là đủ

**Không được áp dụng**

Chỉ lưu một score mà không có Hard Filter, confidence, explanation, source versions hoặc freshness.

**Canonical requirement**

Match Result phải giữ Eligibility/Hard-filter outcome, score components, confidence, explanation, source versions và staleness evidence.

## AP-MAT-003 — Soft Score cứu Hard Fail

**Không được áp dụng**

Listing vi phạm Mandatory hoặc Not-Acceptable criterion vẫn được xếp hạng cao nhờ các điểm mềm.

**Canonical requirement**

Eligibility và Hard Filters phải chạy trước scoring; Hard Fail không được score, rank hoặc manual override biến thành suitable result.

## AP-MAT-004 — Match Score là xác suất mua

**Không được áp dụng**

Diễn giải điểm phù hợp như xác suất chốt, phê duyệt tín dụng hoặc kết luận đầu tư.

**Canonical requirement**

Match Score chỉ biểu diễn mức phù hợp với criteria/rules đã biết. Confidence, data completeness, credit decision và conversion prediction là concepts riêng.

## AP-MAT-005 — Matching tự sửa Requirement

**Không được áp dụng**

Feedback hoặc AI trực tiếp thay budget, purpose, criteria hoặc Financial Profile.

**Canonical requirement**

Matching chỉ tạo versioned suggestion có evidence. Party Context thực hiện update sau human confirmation và domain validation.

## AP-MAT-006 — Matching tự tạo giao dịch

**Không được áp dụng**

Match Result hoặc Shortlist tự tạo Deal, Proposal, Hold, Booking, Contract hoặc Payment.

**Canonical requirement**

Transaction Context sở hữu transaction records. Matching chỉ cung cấp selected references, explanations và snapshots.

## AP-MAT-007 — Shortlist là reservation

**Không được áp dụng**

Hiển thị Shortlist như sản phẩm đã được giữ hoặc còn hàng chắc chắn.

**Canonical requirement**

Shortlist là decision-support record. Current Availability và Commercial Lock phải được Product Context xác nhận lại.

## AP-MAT-008 — Candidate Pool do frontend quyết định

**Không được áp dụng**

Frontend truyền Project/Listings/Customer IDs để mở rộng Candidate Pool hoặc Reverse Matching scope.

**Canonical requirement**

Backend phải intersect requested scope với effective IAM scope, Party responsibility, Product access, Listing visibility và Legal Entity context.

## AP-MAT-009 — Reverse Matching quét toàn Customer base

**Không được áp dụng**

Tìm Customer trực tiếp từ toàn CRM dựa trên segment, phone hoặc profile data.

**Canonical requirement**

Reverse Matching chỉ đánh giá active Requirements/Matching Profiles trong effective scope, consent/context phù hợp và không tự cấp Customer access.

## AP-MAT-010 — Commission hoặc margin ảnh hưởng Customer Fit Score

**Không được áp dụng**

Ưu tiên Listing vì commission của sale hoặc lợi nhuận công ty cao hơn.

**Canonical requirement**

Customer Fit Score chỉ sử dụng approved customer/product criteria. Commercial incentive analytics phải tách biệt, có quyền và không làm thay đổi fit ranking.

## AP-MAT-011 — Cache là nguồn availability hoặc permission cuối cùng

**Không được áp dụng**

Dùng cached Match Result, price, availability hoặc access decision cho action có commercial consequence.

**Canonical requirement**

Product/IAM authoritative checks phải được thực hiện tại trusted boundary; cache chỉ hỗ trợ retrieval và tính toán không quyết định cuối cùng.

## AP-MAT-012 — Matching sở hữu Campaign và outbound

**Không được áp dụng**

Campaign Matching tự tạo Audience, gửi email/message hoặc liên hệ Customer.

**Canonical requirement**

Matching chỉ cung cấp aggregate/candidate token theo policy. Marketing Context sở hữu Campaign, Audience, consent enforcement và outbound execution.

## AP-MAT-013 — Matching sở hữu certified analytics

**Không được áp dụng**

Dùng operational Matching tables làm nguồn KPI/funnel cuối cùng.

**Canonical requirement**

Matching emit governed facts; Analytics Context định nghĩa grain, formulas, snapshots, certification và access cho Metrics.

## AP-MAT-014 — AI thay System Score không có governance

**Không được áp dụng**

Model hoặc prompt thay đổi ranking mà không có model/rule version, evaluation, monitoring và explanation.

**Canonical requirement**

AI assistance phải versioned, bounded, explainable, monitored và không phá Hard Filters hoặc authority boundaries.

## AP-MAT-015 — Customer-facing explanation làm lộ dữ liệu nội bộ

**Không được áp dụng**

Đưa Floor Price, Owner PII, internal margin, sensitive financial detail hoặc restricted notes vào explanation.

**Canonical requirement**

Internal và Customer-safe explanations phải tách riêng, backend field-mask và Audit sensitive access.

## AP-MAT-016 — Candidate examples là exact contracts

**Không được áp dụng**

Dùng table names, endpoints, permission codes, status values, Event names hoặc score examples trong tài liệu này để code ngay.

**Canonical requirement**

Exact database, API, Event, permission, lifecycle và scoring contracts phải được khóa trong nguồn canonical tương ứng.

## AP-MAT-017 — Batch/AI jobs tự mở rộng access

**Không được áp dụng**

Background jobs chạy bằng scope hệ thống rộng hơn user/business purpose ban đầu.

**Canonical requirement**

Batch, Reverse và Campaign Matching phải lưu effective access snapshot/purpose, enforce current revocation rules khi cần và không phát dữ liệu vượt scope.

## AP-MAT-018 — Mặc định tồn tại hệ thống tiền nhiệm

**Không được áp dụng**

Tự thiết kế compatibility layer, old-score mappings hoặc migration aliases khi chưa có approved scope.

**Canonical requirement**

`crm_bds_ai` là Greenfield. Historical import hoặc migration chỉ tồn tại khi có scope, mapping, security review, reconciliation và acceptance criteria riêng.

---

# 88. Kết luận

Customer–Product Matching Capability cung cấp lớp decision support có cấu trúc, versioned và giải thích được cho `crm_bds_ai`.

Capability phải bảo đảm:

- Requirement và Financial Profile vẫn thuộc Party Context.
- Listing, Price, Policy, Availability và Commercial Lock vẫn thuộc Product Context.
- Deal, Proposal, Hold và Booking vẫn thuộc Transaction Context.
- Matching Profile không thay Requirement.
- Eligibility và Hard Filters chạy trước Soft Scoring.
- Mandatory criteria không bị score hoặc manual override ghi đè.
- Match Score khác Confidence, conversion probability và credit decision.
- Mọi kết quả giữ source versions, timestamp, assumptions và explanation.
- Stakeholder conflict được hiển thị thay vì tự quyết định.
- Sale rank tách khỏi System Score.
- Shortlist không khóa Listing.
- Reverse Matching không mở rộng Customer scope.
- Campaign input không tự tạo Campaign hoặc outbound action.
- Operational matching facts không thay certified Analytics Metrics.
- AI chỉ hỗ trợ trong guardrails có version, evaluation và human control.
- Product Availability phải được kiểm tra lại trước commercial action.
- Matching không direct-write Party, Product, Transaction, Marketing hoặc Analytics state.
- Immutable Audit facts thuộc Audit Context.

> Matching hỗ trợ quyết định; Matching không sở hữu Customer truth, Product availability hoặc transaction commitment.
