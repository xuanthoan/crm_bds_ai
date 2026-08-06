# CRM_BDS_AI — CAPABILITY 03: LEAD MANAGEMENT

## Lead intake, routing, assignment, care protection, qualification and conversion

**Document ID:** `PROD-CAP-LEA-001`  
**Canonical path:** `docs/product/capabilities/cap-03-lead-management.md`  
**Product:** `crm_bds_ai`  
**Version:** `1.0.0`  
**Status:** `Accepted / Product Capability Baseline`  
**Document type:** `Product Capability Specification`  
**Primary capability code:** `CAP-LEA`  
**Primary owning Context:** `lead`  
**Owner:** `Product Owner`  
**Co-owner:** `Lead Domain Owner`  
**Reviewers:** `Architecture Owner`, `Party Domain Owner`, `IAM Domain Owner`, `Marketing Domain Owner`, `Activity Domain Owner`, `Product Domain Owner`, `Transaction Domain Owner`, `Security Owner`, `QA Owner`  
**Effective date:** `2026-08-05`  
**Last reviewed:** `2026-08-05`  
**Classification:** `INTERNAL`

---

# 0. Phạm vi thẩm quyền và quan hệ tài liệu

Tài liệu này là nguồn canonical cho:

- Mục tiêu sản phẩm của Lead Management Capability.
- Business outcomes của intake, validation, routing, assignment, acceptance, qualification, nurture, care protection, dispute, handover và conversion.
- Lead-specific business rules, invariants, acceptance outcomes và anti-patterns.
- Đầu vào phân tích cho Lead Context Implementation Pack.

Tài liệu này không phải nguồn exact cho:

- Physical database schema hoặc DDL.
- Exact API paths, request/response payloads.
- Exact Event names, envelope hoặc payloads.
- Exact permission codes, scope vocabulary hoặc field-masking rules.
- Exact lifecycle enums, routing algorithms, scoring formulas, SLA durations, retry policies hoặc retention values.
- Exact cross-context orchestration implementation.
- Exact implementation của Party, Activity, Marketing, Product, Transaction hoặc Integration Context.

Nguồn exact tương ứng:

| Chủ đề | Nguồn canonical |
|---|---|
| Product requirements | PRD |
| Thuật ngữ | Domain Glossary |
| Context ownership | Source of Truth Matrix |
| Architecture boundaries | Architecture Overview, Context Map và Accepted ADRs |
| Lead behavior chi tiết | Lead Context Implementation Pack |
| Customer identity và Requirement | Party Context Implementation Pack |
| Interaction, Task, Timeline và operational SLA | Activity Context Implementation Pack |
| Campaign, Touchpoint và attribution model | Marketing Context Implementation Pack |
| Database | Alembic migrations và Context DB Specifications |
| API | OpenAPI |
| Events | JSON Schema và AsyncAPI |
| Permissions/scopes/masking | Security registries và matrices |
| Công việc hiện tại | Current Sprint Detailed Execution Pack |

**Capability không đồng nghĩa Bounded Context.** Capability này chủ yếu được thực hiện bởi `lead` Context nhưng phụ thuộc published contracts của `platform`, `iam`, `party`, `marketing`, `activity`, `product`, `transaction`, `integration`, `audit` và `operations`.

Các phần “candidate vocabulary”, “candidate data model”, “candidate application operations”, “candidate permission vocabulary” và “candidate business facts” chỉ là đầu vào thiết kế. Chúng không được dùng thay machine-readable contracts đã được chấp nhận.

---
# 1. Mục tiêu của capability

Lead Management Capability quản lý vòng đời của một Lead từ khi doanh nghiệp tiếp nhận một tín hiệu kinh doanh đến khi Lead được xác minh, chăm sóc, nuôi dưỡng, đóng hoặc chuyển giao sang capability/Context downstream.

Capability phải hỗ trợ Lead:

- Được tiếp nhận từ manual entry, approved import, Marketing hoặc Integration.
- Được validation và normalization mà không làm mất source evidence.
- Được resolve với Customer hiện hữu thông qua Party identity contracts.
- Được đưa vào queue và routing theo policy.
- Được assignment, accept/reject và reassignment có history.
- Được chăm sóc theo effective authorization và consent.
- Được bảo vệ quyền chăm sóc theo care context có thời hạn.
- Được qualification và prioritization có explanation.
- Được nurture và reactivation.
- Được chuyển sang Requirement, Deal, Asset Verification, Listing Acquisition hoặc Partner Opportunity thông qua cross-context contracts.
- Được handover khi leave, transfer hoặc offboarding.
- Được đóng với reason nhưng không bị xóa lịch sử.

Capability hỗ trợ nhiều business intents:

- Mua bất động sản.
- Bán tài sản.
- Ký gửi.
- Cho thuê.
- Thuê.
- Đầu tư.
- Hợp tác chủ đất.
- Hợp tác phát triển dự án.
- Hợp tác phân phối.
- Referral.
- After-sales opportunity.
- Partner opportunity.
- Customer hiện hữu quay lại.
- Intent chưa xác định.

Capability phải phân biệt:

1. Lead.
2. Party/Customer.
3. Người tạo Lead.
4. Người được assignment.
5. Người có temporary handling right.
6. Người có care protection.
7. Sale chính của Deal sau conversion.
8. Nguồn và attribution.
9. Người nhận handover.
10. Owning Context của đối tượng downstream.

Nguyên tắc canonical:

> Lead là một tín hiệu hoặc cơ hội tiếp cận kinh doanh. Lead không phải Customer và không tạo quyền sở hữu vĩnh viễn đối với Customer.

---
# 2. Vị trí của capability trong hệ thống

Lead Management Capability sử dụng các nền tảng và contracts sau:

```text
Platform Configuration Capability
→ workflow definitions, SLA policies, Business Calendar và configuration references

Identity, Access and Organization Capability
→ authenticated identity, workforce context, effective authorization, project access và delegation

Party, Customer and Requirement Capability
→ Customer identity resolution, Customer link, Requirement và shared-phone governance

Marketing Capability
→ Campaign, source, touchpoint, consent và attribution semantics

Activity and Engagement Capability
→ Task, Appointment, Interaction, Timeline và operational SLA instances

Lead Management Capability
→ Lead intake, routing, assignment, qualification, protection, nurture, dispute và conversion orchestration

Product / Transaction / Integration capabilities
→ target resources, external intake, downstream conversion và reconciliation
```

Lead Capability cung cấp đầu vào sạch và có lineage cho Customer 360, Matching, Deal, Asset/Listing acquisition và Analytics.

Delivery sequencing thuộc Sprint Roadmap và Sprint Packs. Tài liệu này không tự tuyên bố rằng toàn bộ capability phải được triển khai hoàn chỉnh trước mọi capability downstream; các vertical slices có thể được triển khai theo dependency đã được chấp nhận.

---
# 3. Ranh giới sở hữu dữ liệu

## 3.1. `lead` Context sở hữu

- Lead aggregate và Lead lifecycle.
- Lead intent/side classification trong phạm vi Lead.
- Lead intake snapshot đã được chấp nhận.
- Lead source snapshot và references cần cho lineage.
- Lead queue, queue entry và routing execution state.
- Lead routing-rule semantics và versions theo Lead Context Pack.
- Lead assignment, acceptance và reassignment history.
- Lead qualification assessment.
- Lead score result và explanation trong phạm vi Lead.
- Lead care-context reference, protection record và dispute.
- Lead nurture và reactivation state.
- Lead duplicate relationship/resolution trong phạm vi Lead.
- Lead conversion request, conversion process state và target links.
- Lead handover references.
- Lead-specific Audit requests và observability signals.

## 3.2. `lead` Context không sở hữu

- Canonical Party/Customer identity, Phone Identity, Customer merge và redirect: `party`.
- Requirement và Financial Profile: `party`.
- User, Workforce, Organization, roles, permissions, scopes, delegation và access grants: `iam`.
- Workflow, approval, SLA, calendar và configuration definitions: `platform`.
- Task, Appointment, Interaction, Timeline và operational SLA instances: `activity`.
- Campaign, Touchpoint, consent authority và attribution models: `marketing`.
- Asset, Ownership, Selling Right, Listing, Availability và Commercial Lock: `product`.
- Deal và Transaction Case: `transaction`.
- Contract/Payment/Receipt: `contract`.
- Revenue/Commission: `revenue`.
- Inbound delivery attempts, provider authentication, transport payload retention và integration reconciliation: `integration`.
- Immutable Audit facts: `audit`.
- Jobs, queues hạ tầng, incidents và operational recovery: `operations`.

## 3.3. Source payload và source lineage

- `integration` sở hữu transport delivery, signature verification, replay protection và provider-level raw envelope khi intake đến từ external system.
- `marketing` sở hữu Campaign/Touchpoint semantics và attribution models.
- `lead` sở hữu accepted intake snapshot, normalized Lead fields và immutable references cần để giải thích Lead đến từ đâu.
- Secret, credential và unneeded transport headers không được sao chép vào Lead records.

## 3.4. Customer identity resolution

Lead không tự tạo hoặc merge Customer bằng direct database write.

Lead phải sử dụng Party application contracts để:

- Resolve phone identity.
- Nhận masked duplicate outcome.
- Link canonical Customer.
- Yêu cầu tạo minimal Customer khi đủ điều kiện.
- Mở Identity Resolution Case khi kết quả ambiguous.
- Theo dõi redirect/rebind khi Customer được merge.

## 3.5. Activity và SLA

Lead có thể yêu cầu tạo Task/Interaction/SLA instance nhưng không sở hữu generic Activity runtime.

Lead giữ references hoặc projections cần thiết cho lifecycle decisions; `activity` vẫn là source of truth cho Interaction, Timeline và operational SLA facts.

## 3.6. Conversion ownership

Lead conversion không được direct-write target Context.

- Requirement creation thuộc `party`.
- Deal creation thuộc `transaction`.
- Asset/Listing verification/acquisition thuộc `product` hoặc Context được Context Map xác định.
- Partner profile/opportunity thuộc owning Context được chấp nhận.

Lead sở hữu conversion request/process state và target-resource link sau khi target Context xác nhận.

---
# 4. Khái niệm Lead

## 4.1. Lead là gì

Lead là một bản ghi phản ánh việc công ty nhận được tín hiệu kinh doanh từ một cá nhân, tổ chức hoặc nguồn dữ liệu.

Ví dụ:

* Một người điền form mua căn hộ.
* Một chủ nhà gọi điện muốn ký gửi.
* Một khách cũ hỏi mua thêm đất nền.
* Một chủ đất đề nghị hợp tác phát triển dự án.
* Một đối tác muốn nhận bảng hàng phân phối.
* Một số điện thoại được sale nhập từ sự kiện.
* Một Customer hiện hữu quay lại với nhu cầu mới.

## 4.2. Một Customer có thể có nhiều Lead

Ví dụ cùng một Customer:

* Lead mua căn hộ tại dự án A.
* Lead ký gửi căn cũ.
* Lead hỏi mua đất nền.
* Lead do chiến dịch khác ghi nhận sau sáu tháng.
* Lead giới thiệu người thân.

Không được coi nhiều Lead của cùng Customer là nhiều Customer.

## 4.3. Một Lead có thể có nhiều hướng chuyển đổi

Một Lead có thể tạo:

* Một Requirement mua ở.
* Một Requirement đầu tư.
* Một Seller-side opportunity.
* Một Asset Verification Request.
* Một Partner Opportunity.

Tuy nhiên phải tránh tạo trùng các đối tượng active cho cùng mục đích.

---

# 5. Lead-intent vocabulary và semantics

## 5.1. Candidate intent vocabulary

> Exact codes thuộc Lead Context Pack và machine-readable contracts.

Các mã chuẩn:

```text
BUY
SELL
CONSIGN
LEASE_OUT
RENT
INVEST
LAND_OWNER_COOPERATION
PROJECT_DEVELOPMENT_COOPERATION
PARTNER_DISTRIBUTION
REFERRAL
AFTER_SALES
UNKNOWN
```

## 5.2. Buyer Lead

Người có nhu cầu:

* Mua để ở.
* Mua đầu tư.
* Mua cho thuê.
* Mua cho người thân.
* Mua nhiều sản phẩm.
* Chuyển đổi tài sản.

## 5.3. Seller Lead

Người có tài sản cần:

* Bán.
* Chuyển nhượng.
* Thanh khoản.
* Định giá.
* Tìm người mua.

## 5.4. Consignment Lead

Người muốn:

* Ký gửi độc quyền.
* Ký gửi không độc quyền.
* Ủy quyền bán.
* Thuê công ty Marketing.
* Thuê công ty môi giới.

## 5.5. Land Owner Lead

Chủ đất có thể muốn:

* Bán đất.
* Hợp tác đầu tư.
* Góp đất.
* Phân chia sản phẩm.
* Tìm nhà phát triển.
* Tìm đơn vị phân phối.

## 5.6. Partner Lead

Đối tượng có thể là:

* Đại lý.
* Cộng tác viên.
* Chủ đầu tư.
* Đơn vị phân phối.
* Đối tác Marketing.
* Đơn vị tài chính.
* Đơn vị pháp lý.
* Đơn vị quản lý tài sản.

## 5.7. Unknown Lead

Lead chưa xác định rõ ý định.

Không được tự ép Lead vào `BUY` chỉ vì hệ thống hiện tại chủ yếu bán hàng.

---

# 6. Lead-side vocabulary và semantics

> Các codes dưới đây là candidate vocabulary; exact enums thuộc Lead Context Pack.

Mỗi Lead có thể được gắn `lead_side`:

```text
BUY_SIDE
SELL_SIDE
PARTNER_SIDE
LAND_OWNER_SIDE
UNDETERMINED
```

## 6.1. Buyer-side

Lead liên quan phía người mua hoặc người thuê.

## 6.2. Seller-side

Lead liên quan phía chủ tài sản, người bán hoặc người cho thuê.

## 6.3. Partner-side

Lead liên quan quan hệ B2B hoặc hợp tác.

## 6.4. Land-owner-side

Lead có tài sản đất hoặc quyền sử dụng đất cần hợp tác phát triển.

`lead_side` không thay thế `lead_intent`; hai trường phục vụ các chiều phân loại khác nhau.

---

# 7. Nguồn Lead

## 7.1. Nguồn Marketing

* Facebook Ads.
* Google Ads.
* TikTok Ads.
* Zalo Ads.
* Website.
* Landing page.
* SEO.
* Webinar.
* Livestream.
* Sự kiện.
* Hội thảo.
* Booth bán hàng.
* Call center.
* Hotline.

## 7.2. Nguồn nội bộ

* Sale tự khai thác.
* Customer cũ.
* Customer giới thiệu.
* Nhân viên giới thiệu.
* Team khác chuyển.
* Marketing chuyển.
* Quản lý phân bổ.
* Chăm sóc sau bán.

## 7.3. Nguồn đối tác

* Chủ đầu tư.
* Tổng đại lý.
* Đại lý liên kết.
* Cộng tác viên.
* Ngân hàng.
* Đối tác pháp lý.
* Đối tác Marketing.
* Môi giới tự do.

## 7.4. Nguồn kỹ thuật

* Import Excel/CSV.
* API.
* Webhook.
* Call tracking.
* Chatbot.
* Form bên thứ ba.
* Approved data migration/import khi có scope riêng.

---

# 8. Source, Channel và Attribution

## 8.1. Phân biệt Source và Channel

### Source

Nguồn cụ thể tạo Lead.

Ví dụ:

* Facebook Campaign A.
* Website Landing Page B.
* Customer Nguyễn Văn A giới thiệu.

### Channel

Nhóm kênh:

* Paid Social.
* Paid Search.
* Organic.
* Referral.
* Direct.
* Partner.
* Offline.
* Internal.

## 8.2. First-touch attribution

Lưu nguồn đầu tiên tạo quan hệ Lead.

## 8.3. Last-touch attribution

Lưu nguồn gần nhất trước sự kiện chuyển đổi.

## 8.4. Multi-touch attribution

Có thể lưu toàn bộ chuỗi:

* Campaign.
* Ad.
* Form.
* Cuộc gọi.
* Event.
* Referral.

## 8.5. Nguồn không thay đổi khi phân Lead

Việc chuyển sale không làm thay đổi:

* Nguồn Lead.
* Campaign.
* Người giới thiệu.
* UTM.
* Ngày tiếp nhận.
* Attribution.

## 8.6. Người nhập Lead không mặc định là nguồn

Ví dụ sale nhập Lead từ Facebook nhưng nguồn thực tế vẫn là Facebook.

## 8.7. Attribution snapshot

Khi Lead chuyển thành Requirement hoặc Deal, phải snapshot:

* First source.
* Last source.
* Campaign.
* Referrer.
* Import job.
* Original creator.
* Original received time.

---

# 9. Dữ liệu đầu vào của Lead

## 9.1. Trường tối thiểu

Một Lead có thể được tạo với:

* Một số điện thoại.
* Một email.
* Một tài khoản mạng xã hội.
* Một mã định danh ngoài.
* Một tên.
* Một nội dung yêu cầu.
* Một Organization Party.
* Một nguồn referral.

## 9.2. Trường khuyến nghị

* Họ tên.
* Số điện thoại.
* Quốc gia.
* Email.
* Ý định.
* Dự án quan tâm.
* Loại sản phẩm.
* Khu vực.
* Ngân sách sơ bộ.
* Nội dung.
* Nguồn.
* Campaign.
* Preferred channel.
* Preferred contact time.
* Consent.
* Legal Entity.
* Đơn vị nhận Lead.

## 9.3. Không bắt buộc phải có số điện thoại để tạo Lead tạm thời

Lead có thể chưa có số điện thoại khi:

* Đến từ inbox mạng xã hội.
* Đến từ email.
* Là Organization Lead.
* Là chủ đất qua đối tác.
* Đang chờ thu thập thông tin.

Tuy nhiên Lead chưa có định danh đủ mạnh không được tự động tạo Customer chính thức.

---

# 10. Source payload và accepted intake snapshot

## 10.1. Mục tiêu

Hệ thống phải bảo toàn bằng chứng về dữ liệu nguồn trước và sau normalization để:

- Chứng minh Lead đến từ đâu.
- Phát hiện duplicate delivery.
- Debug mapping.
- Reconcile với provider.
- Giữ source schema version.
- Hỗ trợ Audit và data-quality review.

## 10.2. Ownership split

- `integration` sở hữu provider delivery, signature/replay evidence, transport envelope và provider-level failure/retry state.
- `marketing` sở hữu Campaign/Touchpoint semantics khi nguồn là Marketing.
- `lead` sở hữu accepted intake snapshot, normalized Lead data và source references cần cho Lead lineage.

Lead Context không được sao chép toàn bộ transport payload nếu không có business need và retention policy.

## 10.3. Không ghi đè source evidence

Normalization không được ghi đè source snapshot đã được chấp nhận.

Correction phải tạo version/event hoặc mapping result mới có lineage.

## 10.4. Dữ liệu nhạy cảm

Source payload/snapshot phải:

- Có classification và field policy.
- Có retention-policy reference.
- Không hiển thị mặc định.
- Mask hoặc loại bỏ secret/token.
- Không lưu credential tích hợp.
- Không sao chép unneeded headers hoặc provider metadata.
- Có legal basis/business purpose phù hợp.

## 10.5. Schema và mapping version

Khi provider/source thay schema, phải giữ source schema version và mapping version để tái hiện kết quả normalization.

---
# 11. Chuẩn hóa Lead

Quy trình chuẩn hóa gồm:

1. Làm sạch tên.
2. Chuẩn hóa số điện thoại.
3. Xác định quốc gia.
4. Chuẩn hóa email.
5. Chuẩn hóa intent.
6. Chuẩn hóa project interest.
7. Chuẩn hóa source.
8. Gắn Legal Entity context.
9. Kiểm tra consent.
10. Kiểm tra spam.
11. Kiểm tra Customer hiện hữu.
12. Kiểm tra Lead trùng.
13. Xác định queue.
14. Chạy routing.

Không được làm mất dữ liệu gốc trong quá trình chuẩn hóa.

---

# 12. Chuẩn hóa số điện thoại

## 12.1. Dữ liệu lưu

* Số gốc.
* Số đã làm sạch.
* Mã quốc gia.
* Số chuẩn hóa E.164 hoặc chuẩn doanh nghiệp.
* Loại số.
* Trạng thái hợp lệ.
* Lý do không hợp lệ.
* Nguồn.
* Thời điểm chuẩn hóa.
* Version thuật toán chuẩn hóa.

## 12.2. Số không hợp lệ

Lead vẫn có thể được lưu với trạng thái:

* `PENDING_IDENTITY`.
* `INVALID_CONTACT`.
* `NEED_CONTACT_UPDATE`.

Không yêu cầu Party Context tạo canonical Customer chỉ từ contact point không hợp lệ.

## 12.3. Nhiều số điện thoại trong một Lead

Lead có thể chứa nhiều contact point.

Hệ thống phải kiểm tra tất cả số hợp lệ.

---

# 13. Liên kết Lead với Party/Customer

## 13.1. Identity-resolution contract

Khi Lead có contact point đủ điều kiện, `lead` Context gửi yêu cầu resolution tới `party` Context bằng published application contract.

Identity strategy phải tuân Party Context, Phone Identity governance và PRD. Lead không tự suy luận Customer bằng query trực tiếp vào Party tables.

## 13.2. Không tìm thấy Customer

Lead có thể yêu cầu Party Context tạo minimal Customer/Party record khi:

- Contact identity đủ điều kiện.
- Consent và business purpose phù hợp.
- Không có identity conflict.
- Caller có authority.
- Request idempotent.

Party Context trả canonical identifiers. Lead chỉ lưu reference.

## 13.3. Tìm thấy đúng một Customer

Lead liên kết canonical Customer hiện hữu.

Không tạo Customer mới.

## 13.4. Kết quả ambiguous hoặc shared-phone

Lead chuyển sang trạng thái cần identity resolution theo lifecycle vocabulary đã được chấp nhận.

Lead không tự chọn Customer tùy ý.

## 13.5. Lead chưa có identity đủ mạnh

Lead có thể được lưu tạm và chăm sóc qua kênh hiện có, nhưng:

- Không tự tạo canonical Customer.
- Không được coi là hoàn tất identity resolution.
- Có next action/SLA phù hợp.
- Dữ liệu nhạy cảm được hạn chế.

## 13.6. Organization Lead

Organization Lead phải dùng Party/Partner registry contracts, không dùng quy tắc duplicate cá nhân chỉ dựa trên phone.

---
# 14. Phản hồi khi phát hiện Customer ngoài scope

Sale tạo Lead có số điện thoại trùng Customer ngoài phạm vi không được nhận toàn bộ thông tin Customer.

Backend chỉ trả phản hồi tối thiểu, ví dụ:

* Đã tồn tại hồ sơ trong hệ thống.
* Lead đã được liên kết hoặc chuyển kiểm tra.
* Có quan hệ chăm sóc active.
* Yêu cầu đã được chuyển đến quản lý.

Không trả:

* Tên sale đang chăm sóc nếu policy không cho phép.
* Toàn bộ timeline.
* Deal.
* Số điện thoại khác.
* Hồ sơ tài chính.
* Ghi chú.

---

# 15. Lead trùng và Customer trùng

## 15.1. Lead trùng không đồng nghĩa Customer trùng

Hai Lead có thể cùng Customer nhưng khác:

* Dự án.
* Ý định.
* Nguồn.
* Thời điểm.
* Seller-side/Buyer-side.
* Nhu cầu.

## 15.2. Lead duplicate candidate

Có thể xác định dựa trên:

* Cùng Customer.
* Cùng intent.
* Cùng project.
* Cùng source event.
* Cùng khoảng thời gian.
* Cùng external lead ID.

## 15.3. Exact technical duplicate

Ví dụ webhook gửi lại cùng external lead ID.

Phải xử lý bằng idempotency, không tạo Lead mới.

## 15.4. Business duplicate

Hai Lead riêng biệt nhưng có cùng bối cảnh chăm sóc.

Có thể:

* Merge Lead.
* Link cùng care case.
* Đóng Lead mới là duplicate.
* Giữ cả hai nhưng một Lead chỉ là source event bổ sung.

## 15.5. Không xóa Lead duplicate

Giữ:

* Nguồn.
* Payload.
* Thời gian.
* Campaign.
* Người tạo.
* Quyết định xử lý.

---

# 16. Candidate lifecycle vocabulary

> **Classification:** `CONTEXT-SPECIFIC DESIGN INPUT / PENDING VALIDATION`  
> Các lifecycle groups và status codes dưới đây mô tả semantics mong muốn. Exact enums, transition graph, guards và terminal states chỉ có hiệu lực khi được khóa trong Lead Context Pack và machine-readable contracts.


## 16.1. Canonical status group

* Intake.
* Validation.
* Queue.
* Assignment.
* Contact.
* Qualification.
* Nurture.
* Conversion.
* Closure.

## 16.2. Trạng thái đề xuất

```text
RECEIVED
VALIDATING
PENDING_IDENTITY
PENDING_IDENTITY_RESOLUTION
PENDING_DUPLICATE_REVIEW
READY_FOR_ROUTING
QUEUED
ASSIGNED
PENDING_ACCEPTANCE
ACCEPTED
CONTACTING
CONNECTED
QUALIFYING
QUALIFIED
NURTURING
REACTIVATION_DUE
CONVERTING
CONVERTED
RECYCLED
UNQUALIFIED
UNREACHABLE
INVALID
SPAM
OPTED_OUT
DUPLICATE_CLOSED
LOST
CANCELLED
ARCHIVED
```

## 16.3. Pipeline theo Lead type

Buyer Lead, Seller Lead và Partner Lead có thể có workflow chi tiết khác nhau nhưng phải map về canonical group để báo cáo thống nhất.

## 16.4. Trạng thái không được đổi tùy ý

Mọi transition phải qua Lead application commands và Domain guards; Workflow Definition từ Platform chỉ là policy input.

---

# 17. Hàng đợi Lead

## 17.1. Mục tiêu

Lead Queue lưu các Lead chưa được giao hoặc chờ xử lý.

## 17.2. Loại queue

* General Buyer Queue.
* Seller Lead Queue.
* Consignment Queue.
* Land Owner Queue.
* Partner Queue.
* Project Queue.
* VIP Queue.
* Recycled Lead Queue.
* Unresolved Identity Queue.
* Duplicate Review Queue.
* Manual Review Queue.

## 17.3. Queue theo phạm vi

* Enterprise.
* Legal Entity.
* Branch.
* Department.
* Team.
* Project.
* Campaign.
* Transaction model.

## 17.4. Queue priority

Có thể dựa trên:

* Lead temperature.
* Campaign priority.
* Customer segment.
* Referral.
* Ngân sách.
* Seller urgency.
* Listing value.
* Project launch.
* Thời gian chờ.
* SLA risk.

## 17.5. Queue không phải quyền xem tự do

Sale không mặc định được duyệt toàn bộ queue.

Có thể:

* Chỉ routing engine đọc.
* Team Lead xem.
* Sale nhận từng Lead.
* Sale được phép claim theo policy.

---

# 18. Các phương thức phân bổ Lead

## 18.1. Manual assignment

Người có quyền chọn sale hoặc team.

## 18.2. Round-robin

Phân lần lượt cho các sale đủ điều kiện.

## 18.3. Weighted round-robin

Mỗi sale có trọng số khác nhau.

## 18.4. Least active workload

Chọn sale có tải thấp nhất.

## 18.5. Capacity-based

Phân theo capacity còn lại.

## 18.6. Percentage allocation

Ví dụ:

* Team A: 50%.
* Team B: 30%.
* Team C: 20%.

## 18.7. Skill-based

Theo:

* Loại sản phẩm.
* Khu vực.
* Ngôn ngữ.
* Ký gửi.
* Đất nền.
* Chủ đầu tư.
* Khách VIP.
* Tài chính/vay.

## 18.8. Project-based

Chỉ sale có Project Access hợp lệ.

## 18.9. Source-based

Ví dụ Lead từ đối tác A chỉ phân cho team chuyên trách.

## 18.10. Geographic routing

Theo:

* Quốc gia.
* Tỉnh/thành.
* Khu vực.
* Chi nhánh.
* Nơi ở Customer.
* Vị trí tài sản.

## 18.11. Shift-based

Chỉ phân cho user đang trong ca làm việc.

## 18.12. Referral routing

Ưu tiên sale hoặc người được chỉ định trong referral hợp lệ.

## 18.13. Existing relationship routing

Ưu tiên sale đang có quan hệ chăm sóc active hợp lệ với Customer trong cùng bối cảnh.

## 18.14. Self-created Lead

Có thể giao cho người tạo nếu:

* Người tạo có quyền.
* Không có quan hệ chăm sóc xung đột.
* Đủ Project Access.
* Không vi phạm routing policy.

Người tạo không mặc định được sở hữu Lead.

---

# 19. Routing Rule

## 19.1. Thông tin Rule

* Tên.
* Mã.
* Version.
* Effective scope enforcement theo Scope Resolution Specification.
* Lead intent.
* Lead side.
* Source.
* Campaign.
* Project.
* Property type.
* Geography.
* Customer segment.
* Priority.
* Eligibility filter.
* Distribution method.
* Candidate pool.
* Capacity rule.
* Tie-breaker.
* Acceptance SLA.
* Fallback.
* Effective date.
* Status.
* Người tạo.
* Người duyệt.

## 19.2. Eligibility filter

Sale chỉ được chọn khi:

* User active.
* Assignment active.
* Đúng Legal Entity.
* Đúng team/phòng.
* Có Project Access.
* Có skill cần thiết.
* Không nghỉ phép.
* Không offboarding.
* Không bị suspended.
* Trong ca làm việc nếu rule yêu cầu.
* Chưa vượt capacity.
* Không vi phạm SoD.
* Đã hoàn tất đào tạo nếu cần.
* Không bị hạn chế nhận Lead.

## 19.3. Tie-breaker

* Ít Lead hơn.
* Lâu nhất chưa nhận Lead.
* Conversion rate.
* Response SLA.
* Random có seed.
* Priority rank.

Không nên dùng conversion rate đơn lẻ làm yếu tố duy nhất vì có thể làm Lead luôn tập trung vào một nhóm sale.

---

# 20. Phiên bản và mô phỏng Routing Rule

## 20.1. Rule có phiên bản

Rule active không sửa trực tiếp.

## 20.2. Mô phỏng

Trước khi kích hoạt cần xem:

* Lead mẫu được phân cho ai.
* Bao nhiêu sale đủ điều kiện.
* Sale nào bị loại và lý do.
* Tỷ lệ phân bổ dự kiến.
* Capacity.
* Xung đột Project Access.
* Lead không có người nhận.
* Rule chồng lấn.

## 20.3. Không áp dụng hồi tố

Rule mới không tự phân lại Lead đã giao.

Muốn phân lại phải chạy workflow reassignment được phê duyệt.

---

# 21. Routing Run

Mỗi lần hệ thống phân Lead phải lưu:

* Lead.
* Rule set.
* Version.
* Candidate list.
* Người đủ điều kiện.
* Người bị loại.
* Lý do loại.
* Scoring.
* Sale được chọn.
* Fallback.
* Thời gian.
* Kết quả.
* Correlation ID.

Điều này cho phép trả lời:

> Vì sao Lead này được giao cho Sale A mà không phải Sale B?

---

# 22. Capacity và workload

## 22.1. Capacity có thể tính theo

* Số Lead mới chưa liên hệ.
* Số Lead active.
* Số Deal active.
* Tổng giá trị pipeline.
* Số Task quá hạn.
* Số Lead nóng.
* Ca làm việc.
* Hạn mức cá nhân.

## 22.2. Capacity theo Lead type

Một sale có thể nhận tối đa:

* 20 Buyer Lead active.
* 5 Seller Lead.
* 2 Land Owner Lead.

## 22.3. Không sử dụng một capacity cố định toàn công ty

Capacity phải cấu hình theo:

* Role.
* Team.
* Skill.
* Lead intent.
* Project.
* Giai đoạn.
* Thời kỳ mở bán.

---

# 23. Assignment

## 23.1. Một primary assignee

Một Lead có tối đa một primary assignee active tại một thời điểm.

## 23.2. Collaborator

Có thể thêm:

* Co-handler.
* Specialist.
* Manager.
* Project consultant.
* Legal support.

Collaborator không tự có quyền bảo vệ chính.

## 23.3. Assignment source

* Routing engine.
* Manual.
* Claim.
* Reassignment.
* Handover.
* Delegation.
* Existing relationship.

## 23.4. Lịch sử Assignment

Không ghi đè.

Mỗi lần thay đổi phải lưu:

* Người cũ.
* Người mới.
* Lý do.
* Người thao tác.
* Rule.
* Approval.
* Thời gian.
* Care protection impact.

---

# 24. Lead acceptance

## 24.1. Trạng thái sau phân bổ

Lead chuyển sang:

```text
PENDING_ACCEPTANCE
```

## 24.2. Sale có thể

* Accept.
* Reject có lý do.
* Request reassignment.
* Báo duplicate.
* Báo không đủ Project Access.
* Báo xung đột chăm sóc.
* Báo dữ liệu không hợp lệ.

## 24.3. Acceptance SLA

Ví dụ cấu hình khởi tạo:

* Lead nóng: 5–10 phút.
* Lead thông thường: 15 phút.
* Seller Lead: 30 phút.
* Partner Lead: theo giờ làm việc.

Đây chỉ là giá trị tham khảo; effective duration phải được resolve từ versioned SLA Policy và Business Calendar.

## 24.4. Quá thời gian nhận

Có thể:

* Nhắc sale.
* Thông báo Team Lead.
* Thu hồi assignment.
* Chuyển người khác.
* Giảm capacity.
* Ghi SLA breach.

Không tự coi sale đã accept.

## 24.5. Reject reason

* Không đúng chuyên môn.
* Không có quyền dự án.
* Đang nghỉ.
* Capacity đầy.
* Lead trùng.
* Đang có tranh chấp.
* Dữ liệu không hợp lệ.
* Xung đột lợi ích.
* Lý do khác.

Reject bất hợp lý lặp lại phải được cảnh báo.

---

# 25. Quyền xử lý tạm thời sau Assignment

Assignment có thể tạo một `temporary handling right`.

Quyền này cho phép sale:

* Xem Lead.
* Xem phần Customer tối thiểu liên quan.
* Gọi/liên hệ.
* Ghi activity.
* Qualification.

Quyền tạm thời:

* Không phải quyền bảo vệ đầy đủ.
* Có thời hạn.
* Có thể bị thu hồi nếu không accept hoặc không hoạt động.
* Không cho phép xem toàn bộ Customer ngoài scope.

---

# 26. Tương tác với Lead

## 26.1. Loại activity

* Call attempt.
* Connected call.
* Inbound call.
* SMS.
* Zalo.
* Email.
* Chat.
* Meeting.
* Appointment.
* Site visit.
* Property viewing.
* Internal note.
* Qualification update.
* Document request.
* Seller property visit.
* Negotiation.

## 26.2. Activity source

* Manual.
* Call center.
* Email integration.
* Zalo integration.
* Calendar.
* Website.
* Customer portal.
* External webhook.

## 26.3. Activity phải có timestamp thực tế

Phân biệt:

* `occurred_at`.
* `created_at`.
* `synced_at`.

Không dùng thời gian nhập bản ghi thay cho thời gian tương tác.

---

# 27. Tương tác có ý nghĩa

## 27.1. Được xem là meaningful interaction

* Cuộc gọi kết nối và có trao đổi thực tế.
* Customer phản hồi tin nhắn.
* Customer trả lời email.
* Cuộc gặp.
* Lịch hẹn được Customer xác nhận.
* Site visit.
* Property viewing.
* Customer cung cấp thêm nhu cầu.
* Chủ tài sản cung cấp hồ sơ.
* Có đàm phán thực tế.
* Có xác nhận bước tiếp theo.

## 27.2. Không mặc định có ý nghĩa

* Gọi không nghe.
* Nhắn một chiều không phản hồi.
* Email tự động.
* Internal note.
* Tạo Task.
* Cập nhật trạng thái không có bằng chứng.
* Gọi quá ngắn không có nội dung.
* Activity do sale tự nhập để giữ Lead nhưng không có dấu hiệu Customer tham gia.

## 27.3. Rule xác nhận

Một số interaction có thể cần:

* Call integration xác nhận connected.
* Message inbound.
* Appointment confirmed.
* Manager review.
* Evidence link.

---

# 28. Bảo vệ quyền chăm sóc

## 28.1. Mục tiêu

Bảo vệ công sức chăm sóc hợp lệ nhưng không tạo quyền sở hữu Customer vĩnh viễn.

## 28.2. Đối tượng bảo vệ

Protection không chỉ gắn vào Customer.

Nên xác định theo một `care context`, có thể gồm:

* Customer.
* Lead intent.
* Deal side.
* Requirement.
* Project.
* Property type.
* Asset hoặc Listing.
* Seller relationship.
* Partner opportunity.

## 28.3. Ví dụ

Customer A:

* Sale X chăm sóc mua dự án P1.
* Sale Y chăm sóc mua dự án P2.
* Sale Z phụ trách ký gửi căn cũ.

Ba quan hệ có thể cùng tồn tại nếu không xung đột context.

## 28.4. Một context chỉ có một primary protection

Ví dụ:

```text
Customer A
+ BUY
+ Project P1
+ Requirement R1
```

chỉ nên có một primary care protection active.

---

# 29. Thời điểm bắt đầu bảo vệ

## 29.1. Assignment không mặc định tạo bảo vệ dài hạn

Assignment chỉ tạo quyền xử lý tạm thời.

## 29.2. Bảo vệ chính thức có thể bắt đầu khi

* Có meaningful interaction.
* Customer xác nhận sale phụ trách.
* Có lịch hẹn được xác nhận.
* Có site visit.
* Requirement được qualification.
* Có Proposal được Customer phản hồi.
* Chủ tài sản cung cấp hồ sơ.
* Hợp đồng ký gửi đang được đàm phán.

## 29.3. Chính sách khác theo Lead type

### Buyer Lead

Có thể bắt đầu từ connected interaction.

### Seller Lead

Có thể bắt đầu từ buổi khảo sát tài sản hoặc khi chủ tài sản cung cấp hồ sơ.

### Partner Lead

Có thể bắt đầu từ cuộc họp chính thức hoặc proposal hợp tác.

---

# 30. Thời hạn bảo vệ

Các giá trị khởi tạo tham khảo:

| Sự kiện                          | Thời hạn tham khảo |
| -------------------------------- | -----------------: |
| Assignment mới chưa có tương tác |              2 giờ |
| Meaningful interaction           |            30 ngày |
| Requirement đã qualification     |            45 ngày |
| Lịch hẹn/site visit              |            60 ngày |
| Đàm phán active                  |            90 ngày |
| Booking/đặt cọc trở lên          | Theo vòng đời Deal |

Các giá trị:

* Chỉ là mặc định ban đầu.
* Không hardcode.
* Có thể khác theo Legal Entity, project, Lead type và stage.
* Phải có version.

---

# 31. Gia hạn bảo vệ

## 31.1. Tự động gia hạn khi

Có interaction đủ điều kiện theo policy.

## 31.2. Không gia hạn khi

* Chỉ gọi không kết nối.
* Chỉ nhắn một chiều.
* Chỉ tạo Task.
* Chỉ sửa ghi chú.
* Activity bị nghi ngờ.
* Customer đã opt-out.

## 31.3. Gia hạn thủ công

Cần:

* Lý do.
* Bằng chứng.
* Thời gian đề nghị.
* Manager approval nếu vượt policy.
* Audit.

---

# 32. Hết quyền bảo vệ

Protection có thể hết khi:

* Hết thời hạn.
* Không có tương tác có ý nghĩa.
* Customer yêu cầu đổi sale.
* Sale từ chối tiếp tục.
* Sale nghỉ việc.
* Sale mất Project Access.
* Deal đóng mất.
* Lead chuyển nurture.
* Manager thu hồi có approval.
* Tranh chấp có quyết định.
* Customer opt-out.

## 32.1. Hết protection không xóa lịch sử

Giữ:

* Người từng chăm sóc.
* Thời gian.
* Activity.
* Lý do kết thúc.
* Nguồn.
* Attribution.

---

# 33. Protection và Customer Scope

Protection chỉ tạo quyền xem trong phạm vi care context.

Ví dụ sale được bảo vệ cho Customer ở Project A không tự được xem:

* Deal Project B.
* Hồ sơ tài chính không liên quan.
* Listing của Customer.
* Contract ngoài context.
* Timeline toàn công ty.

Quyền chi tiết phụ thuộc effective authorization từ `iam`, Customer relationship từ `party` và Lead care context.

---

# 34. Cùng Customer, cùng dự án

## 34.1. Một Requirement active

Mặc định một Customer chỉ có một primary care protection cho cùng:

* Project.
* Intent.
* Requirement/need.

## 34.2. Lead mới cùng context

Hệ thống có thể:

* Liên kết vào care case hiện hữu.
* Thông báo sale đang phụ trách.
* Ghi source event mới.
* Không tạo assignment cạnh tranh.
* Hoặc mở conflict review nếu nguồn có quy tắc đặc biệt.

## 34.3. Referral đặc biệt

Không tự thay người chăm sóc chỉ vì xuất hiện referral mới.

Referral attribution và quyền chăm sóc là hai khái niệm khác nhau.

---

# 35. Cùng Customer, khác dự án

Có thể cho phép nhiều sale nếu:

* Project khác.
* Requirement khác.
* Không có policy cross-project exclusivity.
* Customer đồng ý.
* Các sale chỉ thấy context của mình.

Có thể cấu hình:

* Một sale phụ trách toàn Customer.
* Một sale theo project.
* Một sale theo department.
* Hybrid theo Customer segment.

---

# 36. Buyer-side và Seller-side đồng thời

Một Customer có thể:

* Bán căn cũ với Sale A.
* Mua căn mới với Sale B.

Seller-side protection và Buyer-side protection là hai context độc lập.

Không được coi đây là xung đột mặc định.

---

# 37. Tranh chấp quyền chăm sóc

## 37.1. Nguyên nhân

* Hai sale cùng liên hệ.
* Lead nhập trùng.
* Customer cũ quay lại.
* Referral.
* Chuyển team.
* Project khác nhưng policy chưa rõ.
* Seller-side/Buyer-side bị nhầm.
* Sale nghỉ phép.
* Activity bị nghi ngờ.
* Customer yêu cầu đổi sale.

## 37.2. Hồ sơ tranh chấp

* Customer.
* Các Lead.
* Care context.
* Các sale.
* Assignment history.
* Interaction evidence.
* Protection record.
* Source.
* Timeline.
* Claim.
* Người xử lý.
* SLA.
* Quyết định.

## 37.3. Tạm thời khi tranh chấp

Có thể:

* Giữ sale hiện tại.
* Chỉ cho một người tiếp tục liên hệ.
* Tạm dừng outbound contact.
* Giao manager làm custodian.
* Không làm lộ dữ liệu ngoài scope.

## 37.4. Cấp xử lý

* Cùng team: Team Lead.
* Khác team cùng phòng: Department Head.
* Khác phòng: Giám đốc kinh doanh.
* Khác Legal Entity: người có authority liên pháp nhân.
* Tranh chấp giá trị lớn: Director.

## 37.5. Kết quả

* Giữ người đang chăm sóc.
* Chuyển sale.
* Chia co-sale khi Deal hình thành.
* Tách context.
* Đưa Lead về queue.
* Đóng claim không hợp lệ.

---

# 38. Reassignment

## 38.1. Nguyên nhân

* Không accept.
* Không liên hệ đúng SLA.
* Capacity.
* Sale nghỉ.
* Chuyển team.
* Mất Project Access.
* Customer yêu cầu.
* Manager quyết định.
* Tranh chấp.
* Sale tự đề nghị.
* Lead cần chuyên môn khác.

## 38.2. Không sửa assignment cũ

Tạo Assignment mới và đóng Assignment cũ.

## 38.3. Bảo vệ khi Reassignment

Cần xác định:

* Protection cũ chấm dứt.
* Protection được chuyển.
* Bắt đầu protection mới.
* Có giai đoạn chuyển tiếp.
* Sale cũ có collaborator access không.
* Co-sale có được tạo không.

## 38.4. Customer timeline

Phải ghi rõ:

* Ai giao.
* Ai nhận.
* Lý do.
* Thời gian.
* Manager.
* Context.

---

# 39. Leave, Transfer và Offboarding

## 39.1. Nghỉ ngắn hạn

Có thể dùng delegation:

* Không chuyển ownership.
* Không đổi attribution.
* Substitute chăm sóc tạm thời.
* Protection gốc có thể giữ theo policy.

## 39.2. Nghỉ dài hạn

Có thể tạo Handover Case:

* Lead nóng bàn giao trước.
* Appointment sắp tới bàn giao ngay.
* Seller Lead đang đàm phán ưu tiên cao.
* Lead nurture có thể chờ.

## 39.3. Chuyển team

Không tự chuyển tất cả Lead.

Phải đánh giá:

* Lead mới.
* Lead active.
* Project Access.
* Customer context.
* Deal đã hình thành.
* Protection.
* Commission.

## 39.4. Offboarding

* Ngừng nhận Lead mới.
* Thu hồi queue eligibility.
* Chuyển Lead active.
* Team Lead làm custodian mặc định.
* Department Head phân phối lại.
* Giữ attribution và activity cũ.
* Không chuyển hoa hồng đã hình thành tự động.

---

# 40. Qualification

## 40.1. Mục tiêu

Xác định Lead có đủ thông tin và mức độ phù hợp để chuyển sang đối tượng nghiệp vụ tiếp theo.

## 40.2. Buyer Lead qualification

* Có nhu cầu thật.
* Loại sản phẩm.
* Khu vực/dự án.
* Ngân sách sơ bộ.
* Thời gian mua.
* Mục đích.
* Nhu cầu vay.
* Người quyết định.
* Khả năng liên hệ.
* Next action.

## 40.3. Seller Lead qualification

* Có tài sản cụ thể.
* Quan hệ với tài sản.
* Vị trí.
* Loại tài sản.
* Giá mong muốn.
* Lý do bán.
* Thời gian bán.
* Tình trạng pháp lý sơ bộ.
* Đồng sở hữu.
* Sẵn sàng ký gửi.
* Khả năng khảo sát.

## 40.4. Land Owner Lead qualification

* Vị trí đất.
* Diện tích.
* Tình trạng pháp lý.
* Quy hoạch sơ bộ.
* Mục tiêu hợp tác.
* Giá trị kỳ vọng.
* Các đồng sở hữu.
* Thời gian.
* Tài liệu.

## 40.5. Partner Lead qualification

* Loại tổ chức.
* Năng lực.
* Khu vực.
* Sản phẩm.
* Nhu cầu hợp tác.
* Người quyết định.
* Tính hợp lệ.
* Xung đột đối tác hiện hữu.

---

# 41. Qualification status

* Not Started.
* In Progress.
* Need More Information.
* Qualified.
* Qualified with Conditions.
* Nurture.
* Unqualified.
* Invalid.
* Disqualified by Policy.
* Pending Manager Review.

## 41.1. Unqualified không đồng nghĩa bị xóa

Lead vẫn giữ để:

* Báo cáo.
* Nurture.
* Phân tích nguồn.
* Tái kích hoạt.

---

# 42. Lead Score

## 42.1. Mục tiêu

Hỗ trợ ưu tiên, không thay thế quyết định nghiệp vụ.

## 42.2. Nhóm điểm

* Profile fit.
* Intent strength.
* Engagement.
* Timeline.
* Budget fit.
* Project fit.
* Seller urgency.
* Asset quality.
* Source quality.
* Data completeness.
* Risk.

## 42.3. Score version

Mỗi score phải lưu:

* Model.
* Version.
* Input.
* Kết quả.
* Thời gian.
* Explanation.

## 42.4. Không tự động từ chối vì điểm thấp

Lead Score không được:

* Tự đóng Lead.
* Tự từ chối Customer.
* Tự tước quyền chăm sóc.
* Tự quyết định khả năng vay.
* Tự phân biệt dựa trên dữ liệu nhạy cảm không liên quan.

## 42.5. Manual priority

Manager có thể điều chỉnh priority nhưng không sửa score gốc.

Lưu:

* System score.
* Manual priority.
* Reason.
* Approver.

---

# 43. Lead Temperature

Có thể phân loại:

* Hot.
* Warm.
* Cold.
* Nurture.
* Dormant.

Temperature có thể dựa trên score nhưng phải tách riêng để business sử dụng.

Thay đổi temperature phải có:

* Nguồn.
* Rule.
* User.
* Thời gian.
* Lý do.

---

# 44. Nuôi dưỡng Lead

## 44.1. Lead vào Nurture khi

* Chưa đến thời điểm mua.
* Chưa đủ tài chính.
* Chưa sẵn sàng bán.
* Chờ hoàn thiện pháp lý.
* Chờ dự án phù hợp.
* Chưa liên hệ được nhưng dữ liệu hợp lệ.
* Customer yêu cầu liên hệ lại.

## 44.2. Nurture plan

* Ngày liên hệ lại.
* Kênh.
* Nội dung.
* Campaign.
* Người phụ trách.
* Điều kiện tái kích hoạt.
* Consent.

## 44.3. Nurture không kéo dài protection vô hạn

Có thể:

* Giảm mức protection.
* Chuyển sang pool nurture.
* Giữ attribution.
* Cho sale cũ ưu tiên tái nhận theo policy.

---

# 45. Tái kích hoạt Lead

## 45.1. Trigger

* Customer phản hồi.
* Có sản phẩm phù hợp.
* Customer mở email/click.
* Đến ngày follow-up.
* Lead mới cùng Customer.
* Dự án mới.
* Seller cập nhật giá.
* Tài sản hoàn thiện pháp lý.

## 45.2. Routing khi tái kích hoạt

Có thể ưu tiên:

1. Sale đang có protection active.
2. Sale cũ nếu policy cho phép.
3. Team cũ.
4. Routing engine mới.

## 45.3. Không tự khôi phục protection cũ đã hết

Phải tạo protection record mới nếu đủ điều kiện.

---

# 46. Chuyển đổi Buyer Lead

Luồng tiêu chuẩn:

```text
Buyer Lead
→ Customer
→ Requirement
→ Matching Profile
→ Buyer Deal
```

## 46.1. Chuyển thành Requirement

Yêu cầu tối thiểu:

* Customer xác định.
* Intent mua.
* Nhu cầu sơ bộ.
* Người phụ trách.
* Không có Requirement active trùng context.

## 46.2. Chuyển thành Deal

Có thể khi:

* Nhu cầu đủ rõ.
* Có project/listing cụ thể.
* Có cơ hội giao dịch thực tế.
* Có sale chính.
* Không có Deal active trùng.

## 46.3. Một Lead có thể tạo nhiều Requirement

Ví dụ:

* Mua để ở.
* Mua đầu tư.

Phải có lý do và context riêng.

## 46.4. Không tạo duplicate active Deal

Không cho phép nhiều Deal active cho cùng:

* Customer.
* Project hoặc Listing.
* Requirement.
* Transaction side.

trừ khi có approval.

---

# 47. Chuyển đổi Seller/Consignment Lead

Luồng:

```text
Seller Lead
→ Customer/Owner Profile
→ Asset Verification Request
→ Listing Acquisition Deal
→ Consignment Agreement
→ Listing
```

## 47.1. Asset Verification Request

Có thể tạo khi:

* Có tài sản xác định.
* Có thông tin chủ sở hữu.
* Có vị trí.
* Có nhu cầu bán/ký gửi.

## 47.2. Listing Acquisition Deal

Quản lý:

* Xác minh chủ tài sản.
* Định giá.
* Đàm phán phí.
* Độc quyền.
* Thời hạn.
* Hồ sơ pháp lý.
* Quyền bán.

## 47.3. Không tự tạo Listing active từ Lead

Listing chỉ active sau:

* Xác minh đủ.
* Có quyền bán.
* Có giá.
* Có workflow approval.

---

# 48. Chuyển đổi Land Owner Lead

Có thể chuyển thành:

* Land Owner Profile.
* Asset/Parcel Verification.
* Cooperation Opportunity.
* Project Development Deal.
* Partner relationship.

Không ép chuyển thành Listing bán nếu mục tiêu là hợp tác phát triển.

---

# 49. Chuyển đổi Partner Lead

Có thể chuyển thành:

* Organization Party.
* Partner Profile.
* Distribution Opportunity.
* Referral Agreement.
* Service Agreement.
* Project Partnership Opportunity.

Việc tạo Organization Party phải kiểm tra registry đối tác, không dùng quy tắc duplicate Customer cá nhân.

---

# 50. Conversion phải nhất quán, idempotent và recoverable

Lead conversion thường đi qua nhiều Bounded Context nên không được mô phỏng bằng distributed transaction hoặc direct cross-context database write.

Canonical workflow:

1. `lead` kiểm tra version, authorization, Lead state và conversion preconditions.
2. `lead` tạo conversion request/process state trong local transaction.
3. Cùng transaction, `lead` ghi durable Outbox fact/command request theo Event Standards.
4. Owning target Context kiểm tra target-specific duplicates và invariants.
5. Target Context tạo hoặc liên kết target resource trong local transaction.
6. Target Context phát durable result.
7. `lead` xử lý result idempotently, lưu target link và hoàn tất conversion state.
8. Failure, timeout hoặc partial progress phải có retry, reconciliation và operator visibility.

Hệ thống không được để:

- Lead được đánh dấu converted nhưng target resource không tồn tại.
- Target resource được tạo nhưng Lead không thể reconcile.
- Requirement/Deal bị tạo trùng do retry.
- Attribution/source lineage bị mất.
- Conversion được thực hiện hai lần.
- Target Context bị bypass bởi direct write.

Không dùng distributed transaction. Exact Process Manager, commands, Events và compensation thuộc Lead/target Context Packs, Event contracts và Process Manager Standards.

---
# 51. Idempotency chuyển đổi

Mỗi conversion request phải có:

* Idempotency key.
* Lead ID.
* Target type.
* Payload hash.
* User.
* Result resource.

Gửi lại cùng request phải trả cùng kết quả.

Cùng key nhưng payload khác phải báo conflict.

---

# 52. Reopen Lead

Lead đã đóng có thể mở lại khi:

* Customer quay lại.
* Dữ liệu mới.
* Sai trạng thái.
* Có approval.
* Có campaign tái kích hoạt.

Khuyến nghị:

* Không sửa trạng thái lịch sử trực tiếp.
* Tạo reactivation event.
* Có thể tạo Lead mới liên kết Lead cũ nếu đây là cơ hội mới thực sự.

---

# 53. Consent và quyền liên hệ

## 53.1. Dữ liệu cần quản lý

* Consent source.
* Consent type.
* Kênh được phép.
* Mục đích.
* Thời gian.
* Bằng chứng.
* Hết hạn.
* Withdrawal.

## 53.2. Contact restriction

* Do not call.
* Do not SMS.
* Do not Zalo.
* Do not email.
* Chỉ liên hệ giờ nhất định.
* Chỉ qua sale cụ thể.
* Không Marketing.
* Không liên hệ.

## 53.3. Opt-out

Khi Customer opt-out:

* Dừng các kênh tương ứng.
* Hủy Task tự động không phù hợp.
* Không routing lại cho outbound sales trái consent.
* Giữ bản ghi phục vụ compliance.

---

# 54. Preferred Contact

Có thể lưu:

* Kênh ưu tiên.
* Khung giờ.
* Ngôn ngữ.
* Ngày tránh liên hệ.
* Người đại diện.
* Múi giờ.

Routing và Task phải sử dụng thông tin này.

---

# 55. SLA Lead

## 55.1. Các loại SLA

* Intake validation.
* Identity resolution.
* Duplicate review.
* Queue waiting.
* Assignment.
* Acceptance.
* First contact.
* Qualification.
* Next action.
* Reassignment.
* Conflict resolution.
* Conversion.
* Handover.

## 55.2. Cấu hình mặc định tham khảo

| SLA                         |    Mặc định tham khảo |
| --------------------------- | --------------------: |
| Validate Lead               |                5 phút |
| Routing tự động             |              1–5 phút |
| Sale accept                 |               15 phút |
| First contact Lead nóng     |            15–30 phút |
| First contact Lead thường   |           Trong 2 giờ |
| Seller Lead initial contact |           Trong 2 giờ |
| Qualification sơ bộ         | Trong 1 ngày làm việc |
| Duplicate review            |  Trong 4 giờ làm việc |

Các SLA values phải được resolve từ versioned Platform SLA Policy; exact values không được hardcode trong capability document.

## 55.3. Phạm vi SLA

* Enterprise.
* Legal Entity.
* Campaign.
* Lead intent.
* Source.
* Priority.
* Project.
* Team.
* Customer segment.
* Working shift.

## 55.4. Business Calendar

Deadline sử dụng Business Calendar từ Platform; effective workforce/calendar context được resolve qua IAM.

## 55.5. Quá SLA

Có thể:

* Nhắc sale.
* Nhắc Team Lead.
* Giảm capacity.
* Tái phân bổ.
* Escalate.
* Ghi breach.
* Yêu cầu giải trình.

Không tự:

* Đóng Lead.
* Đánh Lead không hợp lệ.
* Chuyển đổi.
* Tạo Customer mới ngoài quy tắc.

---

# 56. Notification

## 56.1. Sale

* Có Lead mới.
* Sắp hết thời gian accept.
* First contact sắp quá hạn.
* Customer phản hồi.
* Protection sắp hết.
* Lead được tái kích hoạt.
* Lead bị chuyển.
* Tranh chấp được mở.
* Handover yêu cầu xác nhận.

## 56.2. Team Lead

* Lead không được accept.
* Lead nóng quá SLA.
* Queue không có sale đủ điều kiện.
* Sale reject bất thường.
* Protection conflict.
* Lead chưa qualification.
* Handover quá hạn.

## 56.3. Marketing

* Lead source lỗi.
* Payload thiếu.
* Campaign có duplicate cao.
* Lead invalid cao.
* Conversion thay đổi.

Marketing chỉ xem dữ liệu theo quyền.

## 56.4. CRM Admin

* Routing rule lỗi.
* Không resolve được queue.
* Webhook duplicate.
* Integration delay.
* Routing job thất bại.

---

# 57. Spam, fraud và Lead không hợp lệ

## 57.1. Dấu hiệu

* Số điện thoại rác.
* Payload tự động.
* Một IP gửi quá nhiều.
* Nội dung không liên quan.
* Trùng external ID.
* Test Lead.
* Bot.
* Referral giả.
* User nội bộ tạo Lead hàng loạt bất thường.

## 57.2. Không auto-delete

Đưa vào:

* Spam Review.
* Invalid.
* Technical Duplicate.

## 57.3. Blocklist

Có thể dùng:

* Phone hash.
* Email.
* IP.
* External source.
* Pattern.

Blocklist là dữ liệu nhạy cảm, cần quyền và audit.

---

# 58. Data Quality

## 58.1. Các chỉ số

* Lead có số điện thoại hợp lệ.
* Lead xác định intent.
* Lead có source.
* Lead có Customer link.
* Lead có next action.
* Lead có meaningful interaction.
* Lead có qualification.
* Lead bị duplicate.
* Lead quá SLA.

## 58.2. Không tự sửa dữ liệu quan trọng

AI hoặc rule có thể gợi ý:

* Intent.
* Dự án.
* Khu vực.
* Ngân sách.

Nhưng thay đổi dữ liệu chính thức cần user xác nhận nếu độ tin cậy chưa đủ.

---

# 59. Import Lead

## 59.1. Nguồn

* Excel.
* CSV.
* Migration.
* Danh sách sự kiện.
* Danh sách đối tác.
* Marketing platform.

## 59.2. Quy trình

1. Upload.
2. Mapping.
3. Validate.
4. Normalize phone.
5. Party identity resolution.
6. Lead duplicate check.
7. Preview.
8. Xác định queue.
9. Approval nếu cần.
10. Import.
11. Routing.
12. Báo cáo lỗi.

## 59.3. Người import không mặc định sở hữu Lead

Ownership/routing theo policy.

## 59.4. Import lớn

Phải dùng job:

* Batch.
* Checkpoint.
* Idempotency.
* Error file.
* Không tạo duplicate Customer qua Party identity contracts.
* Không bỏ qua permission.

---

# 60. Webhook và API tiếp nhận Lead

## 60.1. Inbound endpoint

Có thể tiếp nhận:

* Website.
* Landing page.
* Facebook Lead Ads.
* Google.
* Zalo.
* Call center.
* Partner API.

## 60.2. Security và reliability outcomes

* Signature.
* Source authentication.
* Rate limit.
* Replay protection.
* External event ID.
* Idempotency.
* Schema version.
* Payload size limit.
* Failure isolation và recovery path theo Integration/Event Standards.

## 60.3. Không routing trước khi validate tối thiểu

Phải kiểm tra:

* Source.
* Payload.
* Contact point.
* Spam.
* Legal Entity.
* Consent cơ bản.

---

# 61. Quyền truy cập

## 61.1. Sale

Được:

* Xem Lead `mine`.
* Accept/reject.
* Liên hệ.
* Ghi activity.
* Qualification.
* Convert theo quyền.
* Xem Customer context cần thiết.
* Đề nghị reassignment.
* Mở dispute.

Không được:

* Xem toàn queue.
* Xem Lead sale khác.
* Export hàng loạt.
* Tự chuyển protection.
* Tự duyệt tranh chấp.
* Xem Customer toàn công ty.

## 61.2. Team Lead

Được:

* Xem Lead team.
* Phân/tái phân.
* Quản lý queue team.
* Xử lý conflict trong team.
* Theo dõi SLA.
* Handover.

## 61.3. Department Head

Được:

* Scope department.
* Quản lý routing theo quyền.
* Xử lý tranh chấp giữa team.
* Phê duyệt ngoại lệ.
* Theo dõi conversion.

## 61.4. Marketing

Được:

* Xem attribution và campaign result.
* Xem dữ liệu aggregate.
* Xem Lead cần thiết theo permission.

Không mặc định xem:

* Customer 360 đầy đủ.
* Financial profile.
* Contract.
* Commission.

## 61.5. Director

Được xem toàn bộ theo Legal Entity/Enterprise và phê duyệt chính sách quan trọng.

---

# 62. Field-level permission

Các trường cần kiểm soát:

* Full phone.
* Email.
* Raw payload.
* Referral identity.
* Customer ID ngoài scope.
* Lead source cost.
* Marketing attribution chi tiết.
* Notes nhạy cảm.
* Dispute evidence.
* Spam/fraud indicators.

Backend phải mask hoặc không trả trường.

---

# 63. Candidate permission vocabulary — không phải Permission Registry canonical

> Exact permission codes, scopes và role mappings thuộc Permission Registry và Scope Resolution Specification.

```text
lead.view
lead.view_sensitive
lead.view_raw_payload
lead.create
lead.update
lead.archive
lead.restore
lead.import
lead.export
lead.view_audit

lead_queue.view
lead_queue.manage
lead_queue.claim

lead_assignment.view
lead_assignment.assign
lead_assignment.accept
lead_assignment.reject
lead_assignment.reassign
lead_assignment.override

lead_routing_rule.view
lead_routing_rule.create
lead_routing_rule.update
lead_routing_rule.simulate
lead_routing_rule.review
lead_routing_rule.approve
lead_routing_rule.activate

lead_qualification.view
lead_qualification.update
lead_qualification.approve

lead_protection.view
lead_protection.create
lead_protection.extend
lead_protection.end
lead_protection.override
lead_protection.view_evidence

lead_dispute.create
lead_dispute.view
lead_dispute.resolve
lead_dispute.override

lead_score.view
lead_score.calculate
lead_score.override_priority
lead_score.configure

lead_conversion.customer
lead_conversion.requirement
lead_conversion.deal
lead_conversion.asset_verification
lead_conversion.listing_acquisition
lead_conversion.partner_opportunity

lead_nurture.view
lead_nurture.assign
lead_nurture.reactivate
```

Candidate scope vocabulary tham khảo — exact vocabulary thuộc Scope Resolution Specification:

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

# 64. Các màn hình chính

## 64.1. Lead Inbox

* Lead mới.
* Chờ accept.
* Sắp quá SLA.
* Lead nóng.
* Customer phản hồi.
* Lead tái kích hoạt.

## 64.2. Lead List

Bộ lọc:

* Status.
* Intent.
* Side.
* Source.
* Campaign.
* Project.
* Assignee.
* Team.
* Customer.
* Temperature.
* SLA.
* Protection.
* Legal Entity.
* Created date.

## 64.3. Lead Detail

Các tab:

1. Overview.
2. Identity.
3. Customer Link.
4. Intent.
5. Source & Attribution.
6. Assignment.
7. Care Protection.
8. Activities.
9. Qualification.
10. Score.
11. SLA.
12. Conversion.
13. Duplicate.
14. Dispute.
15. Raw Payload.
16. Audit.

## 64.4. Lead Queue Center

* Queue.
* Waiting time.
* Priority.
* Eligible pool.
* Unassigned.
* No candidate.
* Claim.
* Manual assign.

## 64.5. Routing Rule Center

* Rule.
* Version.
* Condition.
* Candidate pool.
* Distribution.
* Simulation.
* Result.
* Approval.

## 64.6. Protection Center

* Active protection.
* Sắp hết hạn.
* Context.
* Người phụ trách.
* Evidence.
* Extension.
* Conflict.

## 64.7. Duplicate Review Center

* Lead candidate.
* Customer candidate.
* Shared phone.
* Source.
* Decision.
* Masked data.

## 64.8. Lead Dispute Center

* Claim.
* Parties.
* Evidence.
* SLA.
* Custodian.
* Decision.

## 64.9. Conversion Workspace

Cho phép chọn:

* Requirement.
* Deal.
* Asset Verification.
* Listing Acquisition.
* Partner Opportunity.

Hiển thị duplicate warning trước khi tạo.

---

# 65. Dashboard cho Sale

* Lead mới.
* Chờ accept.
* First contact quá hạn.
* Lead nóng.
* Lead chưa qualification.
* Protection sắp hết.
* Lead cần follow-up.
* Nurture đến hạn.
* Conversion trong tháng.
* Lead bị chuyển.
* Tranh chấp đang mở.

---

# 66. Dashboard cho Team Lead

* Lead theo source.
* Queue.
* Lead chưa phân.
* Acceptance rate.
* First response time.
* SLA breach.
* Conversion.
* Capacity từng sale.
* Reject rate.
* Reassignment.
* Protection conflict.
* Lead stale.
* Seller Lead chưa khảo sát.

---

# 67. Dashboard cho Department Head và Director

* Tổng Lead.
* Buyer/Seller/Partner split.
* Lead theo Legal Entity.
* Lead theo nguồn.
* Cost per Lead khi có dữ liệu Marketing.
* Qualification rate.
* Conversion rate.
* Time to first contact.
* Time to conversion.
* Lead aging.
* Lost reason.
* Seller Listing acquisition rate.
* Project demand.
* Team performance.
* Routing fairness.
* Lead protection dispute.
* Cross-project Customer activity.

---

# 68. Báo cáo

* Lead intake.
* Lead by source.
* Lead by campaign.
* Lead by intent.
* Lead by side.
* Lead by Legal Entity.
* Lead by project.
* Lead by sale/team/phòng.
* Queue aging.
* Assignment time.
* Acceptance time.
* First response time.
* Qualification time.
* Conversion time.
* SLA breach.
* Lead rejection.
* Reassignment.
* Duplicate Lead.
* Customer existing/new.
* Shared-phone resolution.
* Protection duration.
* Protection expiration.
* Protection dispute.
* Nurture.
* Reactivation.
* Buyer Lead conversion.
* Seller Lead conversion.
* Asset verification conversion.
* Listing acquisition conversion.
* Partner conversion.
* Lost reasons.
* Invalid/spam.
* Routing distribution.
* Routing fairness.
* Sale capacity.
* Source quality.

Mọi báo cáo phải drill-down đúng scope.

---

# 69. Candidate data model — không phải physical schema canonical

> **Classification:** `CONTEXT-SPECIFIC DESIGN INPUT / PENDING VALIDATION`  
> Exact tables, columns, constraints và indexes chỉ có hiệu lực khi được khóa trong Lead Context DB Specification và Alembic migrations.

## 69.1. Lead

### `leads`

* `id`
* `lead_code`
* `enterprise_id`
* `legal_entity_id`
* `lead_type`
* `lead_intent`
* `lead_side`
* `status`
* `canonical_status_group`
* `priority`
* `temperature`
* `customer_id`
* `organization_party_id`
* `primary_project_id`
* `primary_property_type_id`
* `preferred_contact_channel`
* `preferred_contact_time`
* `received_at`
* `qualified_at`
* `converted_at`
* `closed_at`
* `created_by`
* `created_at`
* `updated_at`
* `version`

## 69.2. Lead contact

### `lead_contact_points`

* `id`
* `lead_id`
* `contact_type`
* `raw_value`
* `normalized_value`
* `country_code`
* `validation_status`
* `validation_reason`
* `is_primary`
* `source`
* `normalization_version`
* `created_at`

## 69.3. Intake snapshot và Integration reference

### `lead_intake_snapshots`

* `id`
* `lead_id`
* `integration_delivery_ref`
* `source_system`
* `external_event_id`
* `source_schema_version`
* `mapping_version`
* `accepted_snapshot_json`
* `payload_hash`
* `retention_policy_ref`
* `received_at`
* `created_at`

> Full provider envelope và delivery-attempt records thuộc `integration`. `accepted_snapshot_json` chỉ chứa dữ liệu cần thiết cho Lead business lineage theo classification/retention policy.
## 69.4. Source và attribution

### `lead_source_events`

* `id`
* `lead_id`
* `source_type`
* `source_id`
* `channel_code`
* `campaign_id`
* `ad_id`
* `adset_id`
* `landing_page`
* `utm_source`
* `utm_medium`
* `utm_campaign`
* `utm_content`
* `referrer_party_id`
* `external_lead_id`
* `touch_type`
* `occurred_at`
* `created_at`

### `lead_attribution_snapshots`

* `id`
* `lead_id`
* `snapshot_type`
* `first_touch_source_event_id`
* `last_touch_source_event_id`
* `attribution_model`
* `snapshot_json`
* `created_at`

## 69.5. Lead intent history

### `lead_intent_history`

* `id`
* `lead_id`
* `from_intent`
* `to_intent`
* `reason`
* `changed_by`
* `created_at`

## 69.6. Queue

### `lead_queues`

* `id`
* `queue_code`
* `name`
* `legal_entity_id`
* `scope_type`
* `scope_id`
* `lead_intent`
* `priority_policy`
* `status`
* `created_at`

### `lead_queue_entries`

* `id`
* `lead_id`
* `queue_id`
* `priority`
* `entered_at`
* `available_at`
* `status`
* `removed_at`
* `removal_reason`

## 69.7. Routing Rule

### `lead_routing_rule_sets`

* `id`
* `rule_set_code`
* `name`
* `scope_type`
* `scope_id`
* `version`
* `status`
* `effective_from`
* `effective_to`
* `created_by`
* `reviewed_by`
* `approved_by`
* `created_at`

### `lead_routing_rules`

* `id`
* `rule_set_id`
* `priority`
* `conditions_json`
* `eligibility_json`
* `distribution_method`
* `candidate_pool_json`
* `capacity_policy_json`
* `tie_breaker_json`
* `acceptance_sla_policy_id`
* `fallback_action`
* `status`

### `lead_routing_runs`

* `id`
* `lead_id`
* `rule_set_id`
* `rule_version`
* `trigger_type`
* `status`
* `selected_user_id`
* `selected_team_id`
* `result_json`
* `started_at`
* `completed_at`

### `lead_routing_candidates`

* `id`
* `routing_run_id`
* `candidate_user_id`
* `eligibility_status`
* `exclusion_reasons_json`
* `workload_snapshot`
* `score`
* `rank`

## 69.8. Assignment

### `lead_assignments`

* `id`
* `lead_id`
* `assignee_user_id`
* `assignee_assignment_id`
* `assignment_type`
* `source_type`
* `source_resource_id`
* `is_primary`
* `status`
* `assigned_at`
* `acceptance_due_at`
* `accepted_at`
* `ended_at`
* `end_reason`
* `assigned_by`
* `created_at`

### `lead_assignment_events`

* `id`
* `lead_assignment_id`
* `event_type`
* `actor_user_id`
* `reason_code`
* `reason`
* `created_at`

## 69.9. Interaction references và meaningful-evaluation state

> Canonical Interaction records thuộc `activity`; Lead chỉ lưu reference, evaluation state hoặc approved snapshot cần cho Lead decisions.

### `lead_interaction_references`

* `id`
* `lead_id`
* `activity_interaction_id`
* `interaction_type_snapshot`
* `outcome_snapshot`
* `occurred_at_snapshot`
* `activity_version`
* `created_at`

### `lead_meaningful_interaction_evaluations`

* `id`
* `lead_id`
* `activity_interaction_id`
* `policy_id`
* `policy_version`
* `evaluation_status`
* `evidence_resource_type`
* `evidence_resource_id`
* `evaluated_by`
* `evaluated_at`
* `created_at`
## 69.10. Protection

### `lead_care_contexts`

* `id`
* `customer_id`
* `lead_intent`
* `lead_side`
* `project_id`
* `requirement_id`
* `asset_id`
* `listing_id`
* `context_key`
* `status`
* `created_at`

### `lead_protection_records`

* `id`
* `lead_id`
* `care_context_id`
* `protected_user_id`
* `protected_assignment_id`
* `protection_type`
* `source_event_type`
* `source_event_id`
* `started_at`
* `expires_at`
* `status`
* `ended_at`
* `end_reason`
* `created_at`

### `lead_protection_events`

* `id`
* `protection_record_id`
* `event_type`
* `old_expires_at`
* `new_expires_at`
* `reason`
* `evidence_resource_type`
* `evidence_resource_id`
* `requested_by`
* `approved_by`
* `created_at`

## 69.11. Duplicate

### `lead_duplicate_candidates`

* `id`
* `lead_id`
* `candidate_lead_id`
* `customer_id`
* `match_type`
* `match_score`
* `match_details_json`
* `status`
* `reviewed_by`
* `reviewed_at`

### `lead_duplicate_resolutions`

* `id`
* `lead_id`
* `resolution_type`
* `target_lead_id`
* `target_customer_id`
* `reason`
* `resolved_by`
* `approved_by`
* `created_at`

## 69.12. Qualification

### `lead_qualification_assessments`

* `id`
* `lead_id`
* `assessment_type`
* `version`
* `status`
* `answers_json`
* `completeness_score`
* `qualification_result`
* `next_action`
* `assessed_by`
* `assessed_at`

## 69.13. Score

### `lead_scoring_models`

* `id`
* `model_code`
* `name`
* `lead_type`
* `scope_type`
* `scope_id`
* `version`
* `configuration_json`
* `status`
* `effective_from`
* `effective_to`

### `lead_scores`

* `id`
* `lead_id`
* `scoring_model_id`
* `model_version`
* `total_score`
* `component_scores_json`
* `explanation_json`
* `calculated_at`

## 69.14. Nurture

### `lead_nurture_records`

* `id`
* `lead_id`
* `nurture_reason`
* `assigned_user_id`
* `campaign_id`
* `next_contact_at`
* `contact_channel`
* `reactivation_conditions_json`
* `status`
* `started_at`
* `ended_at`

### `lead_reactivation_events`

* `id`
* `lead_id`
* `trigger_type`
* `trigger_resource_type`
* `trigger_resource_id`
* `routing_run_id`
* `reactivated_at`
* `created_at`

## 69.15. Conversion

### `lead_conversion_events`

* `id`
* `lead_id`
* `conversion_type`
* `target_resource_type`
* `target_resource_id`
* `customer_id`
* `attribution_snapshot_id`
* `idempotency_key`
* `payload_hash`
* `converted_by`
* `converted_at`

### `lead_resource_links`

* `id`
* `lead_id`
* `resource_type`
* `resource_id`
* `relationship_type`
* `created_at`

## 69.16. Dispute

### `lead_care_disputes`

* `id`
* `dispute_code`
* `customer_id`
* `care_context_id`
* `primary_lead_id`
* `dispute_type`
* `status`
* `custodian_user_id`
* `assigned_reviewer_id`
* `due_at`
* `resolution`
* `created_by`
* `created_at`
* `resolved_at`

### `lead_care_dispute_claims`

* `id`
* `dispute_id`
* `claimant_user_id`
* `claimed_protection_record_id`
* `claim_reason`
* `evidence_json`
* `created_at`

## 69.17. Consent

### `lead_contact_consents`

* `id`
* `lead_id`
* `customer_id`
* `consent_type`
* `channel`
* `purpose`
* `status`
* `source`
* `evidence_url`
* `granted_at`
* `withdrawn_at`
* `expires_at`

---

# 70. Candidate application operations — không phải OpenAPI canonical

> Các operation dưới đây là capability inventory. Exact paths, methods, payloads, errors và authorization metadata thuộc OpenAPI.

## Lead intake

```text
GET    /leads
POST   /leads
GET    /leads/{id}
PATCH  /leads/{id}
POST   /leads/{id}/validate
POST   /leads/{id}/archive
POST   /leads/{id}/restore
```

## Identity

```text
GET    /leads/{id}/identity-check
POST   /leads/{id}/identity-check
POST   /leads/{id}/link-customer
POST   /leads/{id}/request-minimal-customer
POST   /leads/{id}/identity-resolution-request
```

## Queue và routing

```text
GET    /lead-queues
GET    /lead-queues/{id}/entries
POST   /leads/{id}/enqueue
POST   /leads/{id}/route
GET    /lead-routing-runs/{id}
GET    /lead-routing-runs/{id}/candidates

GET    /lead-routing-rule-sets
POST   /lead-routing-rule-sets
PATCH  /lead-routing-rule-sets/{id}
POST   /lead-routing-rule-sets/{id}/simulate
POST   /lead-routing-rule-sets/{id}/approve
POST   /lead-routing-rule-sets/{id}/activate
```

## Assignment

```text
GET    /leads/{id}/assignments
POST   /leads/{id}/assign
POST   /lead-assignments/{id}/accept
POST   /lead-assignments/{id}/reject
POST   /lead-assignments/{id}/reassign
POST   /lead-assignments/{id}/end
```

## Activity

```text
GET    /leads/{id}/activities
POST   /leads/{id}/activities
POST   /lead-activities/{id}/confirm-meaningful
POST   /lead-activities/{id}/reject-meaningful
```

## Protection

```text
GET    /leads/{id}/protection
POST   /leads/{id}/protection/start
POST   /lead-protection-records/{id}/extend-request
POST   /lead-protection-records/{id}/extend
POST   /lead-protection-records/{id}/end
GET    /customers/{id}/care-contexts
```

## Duplicate

```text
GET    /leads/{id}/duplicate-candidates
POST   /leads/{id}/duplicate-review
POST   /lead-duplicate-candidates/{id}/resolve
```

## Qualification

```text
GET    /leads/{id}/qualification
POST   /leads/{id}/qualification
PATCH  /lead-qualification-assessments/{id}
POST   /lead-qualification-assessments/{id}/complete
```

## Score

```text
GET    /leads/{id}/score
POST   /leads/{id}/score/recalculate
POST   /leads/{id}/priority-override
```

## Nurture

```text
POST   /leads/{id}/nurture
PATCH  /lead-nurture-records/{id}
POST   /lead-nurture-records/{id}/reactivate
POST   /lead-nurture-records/{id}/complete
```

## Conversion

```text
POST   /leads/{id}/convert/customer
POST   /leads/{id}/convert/requirement
POST   /leads/{id}/convert/deal
POST   /leads/{id}/convert/asset-verification
POST   /leads/{id}/convert/listing-acquisition
POST   /leads/{id}/convert/partner-opportunity
GET    /leads/{id}/conversions
```

## Dispute

```text
GET    /lead-care-disputes
POST   /lead-care-disputes
GET    /lead-care-disputes/{id}
POST   /lead-care-disputes/{id}/claims
POST   /lead-care-disputes/{id}/resolve
```

Backend phải tự enforce:

* User identity.
* Legal Entity context.
* Permission.
* Effective scope enforcement theo Scope Resolution Specification.
* Field policy.
* Project Access.
* Queue access.
* Assignment.
* Protection.
* Consent.
* Workflow.
* SLA.
* Idempotency.
* Version check.

---

# 71. Candidate business facts — không phải Event contract canonical

> Exact Event names, envelopes, payloads, routing và compatibility thuộc Event Registry, JSON Schema và AsyncAPI.

Lead Context có thể công bố các candidate business facts sau:

```text
lead.received
lead.validated
lead.identity_pending
lead.customer_linked
lead.duplicate_detected

lead.queued
lead.routing_started
lead.routed
lead.routing_failed

lead.assigned
lead.accepted
lead.rejected
lead.reassigned

lead.interaction_reference_recorded
lead.protection_eligibility_confirmed
lead.protection_started
lead.protection_extended
lead.protection_expired
lead.protection_ended

lead.qualified
lead.unqualified
lead.nurtured
lead.reactivated

lead.converted_to_requirement
lead.converted_to_deal
lead.converted_to_asset_verification
lead.converted_to_listing_acquisition
lead.converted_to_partner_opportunity

lead.dispute_opened
lead.dispute_resolved
lead.opted_out
lead.closed
```

Consumers phải xử lý idempotently theo Event Standards.

---

# 72. Candidate configuration definitions

> Các keys dưới đây là design input. Exact Configuration Definitions, schemas, scopes, defaults và versions thuộc Platform Context contracts.

```text
lead.default_workflow
lead.buyer_workflow
lead.seller_workflow
lead.partner_workflow

lead.identity_validation_policy
lead.duplicate_review_policy
lead.customer_link_policy

lead.routing_rule_set
lead.routing_fallback_policy
lead.capacity_policy
lead.acceptance_sla_policy
lead.first_contact_sla_policy
lead.qualification_sla_policy

lead.protection_start_policy
lead.protection_duration_policy
lead.protection_extension_policy
lead.protection_conflict_policy

lead.nurture_policy
lead.reactivation_policy
lead.conversion_policy

lead.notification_policy
lead.raw_payload_retention_policy
lead.spam_detection_policy
lead.import_approval_policy
```

Tất cả phải có scope và version.

---

# 73. System invariant

Các quy tắc sau không được cấu hình tắt:

1. Customer cá nhân không được tạo trùng theo số điện thoại đã chuẩn hóa.
2. External event trùng không được tạo Lead kỹ thuật trùng.
3. Một Lead chỉ có một primary assignment active.
4. Một care context chỉ có một primary protection active.
5. Backend phải enforce scope.
6. Project Access không mở Customer scope.
7. Field nhạy cảm không được gửi ngoài quyền.
8. Assignment history không được ghi đè.
9. Attribution gốc không bị thay bởi reassignment.
10. Conversion phải idempotent.
11. Conversion không được tạo duplicate active Deal trái rule.
12. Lead Score không được tự động từ chối Lead.
13. Opt-out phải được thực thi.
14. Protection không tạo quyền sở hữu Customer vĩnh viễn.
15. Lead không bị xóa chỉ vì duplicate hoặc invalid.
16. Routing Rule active không sửa trực tiếp.
17. SLA không được frontend tự quyết định.
18. User inactive không được nhận Lead.
19. Sale không có Project Access không được nhận Lead bắt buộc Project đó.
20. Handover không tự chuyển quyền hoa hồng.

---

# 74. Rule nghiệp vụ bắt buộc

1. Lead và Customer là hai thực thể khác nhau.
2. Một Customer có thể có nhiều Lead.
3. Một Lead có thể có nhiều source event.
4. Source gốc không thay đổi khi chuyển sale.
5. Người nhập Lead không mặc định sở hữu Lead.
6. Lead không có identity đủ mạnh được lưu tạm nhưng không yêu cầu tạo canonical Customer.
7. Lead có số hợp lệ phải kiểm tra Customer toàn công ty.
8. Tìm thấy một Customer thì liên kết, không tạo mới.
9. Tìm thấy nhiều Customer thì chuyển manual resolution.
10. Response duplicate ngoài scope phải được mask.
11. Customer duplicate determination phải tuân Party Phone Identity policy; baseline chỉ dùng phone identity làm tiêu chí xác định trùng.
12. Email, tên và địa chỉ không dùng kết luận trùng Customer.
13. Lead duplicate và Customer duplicate là hai khái niệm khác nhau.
14. Technical duplicate phải xử lý idempotency.
15. Business duplicate phải giữ lịch sử nguồn.
16. Một Lead chỉ có một primary assignee active.
17. Collaborator không tự có primary protection.
18. User inactive không đủ điều kiện routing.
19. User nghỉ phép không nhận Lead nếu leave policy cấm.
20. User không có Project Access không nhận Lead project đó.
21. Routing phải lưu rule version.
22. Routing phải giải thích candidate exclusion.
23. Routing Rule mới không phân lại Lead cũ.
24. Manual assignment vẫn phải kiểm tra eligibility.
25. Lead assignment có acceptance SLA.
26. Quá acceptance SLA không tự coi accepted.
27. Reject phải có lý do.
28. Reject không xóa Lead.
29. Reassignment không ghi đè assignment cũ.
30. Assignment chỉ tạo temporary handling right mặc định.
31. Protection chính thức cần sự kiện đủ điều kiện.
32. Gọi không nghe không mặc định là meaningful.
33. Tin nhắn một chiều không mặc định là meaningful.
34. Internal note không gia hạn protection.
35. Một care context chỉ có một primary protection.
36. Customer có thể có protection khác nhau theo project/intent.
37. Buyer-side và Seller-side có thể do sale khác nhau.
38. Protection hết hạn không xóa activity.
39. Extension thủ công phải có reason.
40. Tranh chấp phải có evidence.
41. Chỉ tạm giữ context đang tranh chấp.
42. Customer yêu cầu đổi sale phải qua workflow.
43. Chuyển team không tự chuyển Lead.
44. Offboarding phải tạo handover.
45. Custodian không tự hưởng commission.
46. Qualification phải theo Lead type.
47. Buyer qualification và Seller qualification không dùng chung hoàn toàn.
48. Lead Score chỉ hỗ trợ ưu tiên.
49. Score model phải có version.
50. Manual priority không sửa system score.
51. Nurture không giữ protection vô hạn.
52. Reactivation phải tạo event mới.
53. Reactivation không tự khôi phục protection đã hết.
54. Conversion phải kiểm tra Customer link.
55. Conversion phải kiểm tra duplicate target.
56. Conversion phải lưu attribution snapshot.
57. Lead có thể chuyển thành Requirement mà chưa tạo Deal.
58. Lead Seller không tự tạo Listing active.
59. Land Owner Lead không bị ép thành Listing.
60. Partner Lead dùng Party registry.
61. Opt-out phải chặn outbound theo kênh.
62. Raw payload phải có retention.
63. Raw payload không được chứa credential.
64. Import không bỏ qua duplicate check.
65. Importer không mặc định là assignee.
66. Webhook phải có replay protection.
67. Domain event phải có version.
68. SLA phải sử dụng Business Calendar.
69. Quá SLA không tự đóng Lead.
70. Dashboard phải drill-down đúng scope.
71. View không đồng nghĩa Export.
72. Sale không được export Lead hàng loạt.
73. Backend không tin `scope` frontend.
74. Query scope phải enforce ở database/query layer.
75. Audit Lead không được sửa.
76. Lead đã converted vẫn giữ lịch sử.
77. Closed Lead có thể được reactivated theo workflow.
78. Source/campaign không bị mất khi merge Lead.
79. Hệ thống phải phân biệt Lead invalid và Customer không phù hợp.
80. Không dùng thuộc tính nhạy cảm không liên quan để routing hoặc scoring.

---

# 75. Cảnh báo và phát hiện bất thường

Hệ thống cần cảnh báo khi:

* Lead mới không được route.
* Không có sale đủ điều kiện.
* Sale được route nhưng không có Project Access.
* Sale đang nghỉ vẫn nhận Lead.
* Một sale nhận quá nhiều Lead.
* Routing distribution lệch bất thường.
* Sale reject Lead liên tục.
* Sale accept nhưng không liên hệ.
* First contact quá SLA.
* Activity đáng ngờ dùng để gia hạn protection.
* Nhiều call attempt ngắn bất thường.
* Protection được gia hạn thủ công liên tục.
* Hai protection active cùng context.
* Lead cùng phone được tạo hàng loạt.
* Webhook lặp.
* Source có invalid rate cao.
* Import có duplicate rate cao.
* Customer ngoài scope bị truy vấn nhiều lần.
* Lead đã opt-out vẫn bị liên hệ.
* Lead converted hai lần.
* Deal trùng được tạo từ Lead.
* Seller Lead tạo Listing khi chưa xác minh.
* Lead nằm queue quá lâu.
* User offboard vẫn còn assignment Lead.
* Handover quá SLA.
* Lead score thay đổi bất thường sau model mới.
* Routing Rule mới không có candidate trong mô phỏng.
* Raw payload chứa dữ liệu nghi là secret.
* Sale truy cập Lead ngoài scope.
* Export Lead bất thường.

---

# 76. Audit log

## 76.1. Thao tác bắt buộc

* Tạo Lead.
* Nhận webhook.
* Normalize.
* Party identity resolution.
* Link Customer.
* Yêu cầu Party Context tạo minimal Customer.
* Duplicate resolution.
* Enqueue.
* Routing.
* Manual assignment.
* Accept/reject.
* Reassignment.
* Activity.
* Meaningful confirmation.
* Protection start/extend/end.
* Qualification.
* Score.
* Priority override.
* Nurture.
* Reactivation.
* Conversion.
* Opt-out.
* Dispute.
* Archive/restore.
* Import/export.

## 76.2. Nội dung Audit

* Actor.
* Lead.
* Customer.
* Legal Entity.
* Assignment.
* Rule version.
* Workflow version.
* SLA policy version.
* Protection context.
* Before/after.
* Reason.
* Approval.
* IP.
* Device.
* Request ID.
* Correlation ID.
* Idempotency key.
* Timestamp.
* Result.

---

# 77. Product baseline và deferred capabilities

> Delivery scope cuối cùng thuộc Roadmap và Current Sprint Packs; danh sách dưới đây không tự kích hoạt implementation.

## 77.1. Bắt buộc

* Buyer Lead.
* Seller/Consignment Lead.
* Unknown Lead.
* Intake thủ công.
* Import.
* Webhook cơ bản.
* Raw payload.
* Phone normalization.
* Party identity resolution trong enterprise boundary.
* Customer link/minimal Customer request qua Party contracts.
* Lead duplicate.
* Queue.
* Manual routing.
* Round-robin.
* Capacity cơ bản.
* Project Access eligibility.
* Assignment.
* Acceptance.
* First-contact SLA.
* Activity.
* Meaningful interaction.
* Care protection.
* Protection expiration.
* Qualification.
* Lead Score cơ bản.
* Nurture.
* Reactivation.
* Convert Requirement.
* Convert Buyer Deal.
* Convert Asset Verification.
* Convert Listing Acquisition Deal.
* Effective scope enforcement theo Scope Resolution Specification.
* Field masking.
* Handover.
* Audit.
* Dashboard cơ bản.

## 77.2. Giai đoạn nâng cao

* Weighted routing.
* AI intent extraction.
* AI spam detection.
* AI lead summary.
* Predictive score.
* Dynamic capacity.
* Multi-touch attribution.
* Call center integration.
* Zalo/Facebook inbox.
* Auto activity confirmation.
* Advanced protection evidence.
* Partner Lead.
* Land Owner pipeline.
* Automated nurture campaign.
* Reverse routing by product availability.
* Cross-Legal Entity routing.
* Lead marketplace nội bộ có kiểm soát.
* Advanced routing fairness.
* Attribution modeling.

---

# 78. Product acceptance outcomes

Capability baseline được xem là đáp ứng khi:

1. Tạo được Buyer Lead.
2. Tạo được Seller Lead.
3. Tạo được Consignment Lead.
4. Tạo được Unknown Lead.
5. Lead có thể chưa có phone.
6. Lead chưa có identity đủ mạnh không yêu cầu tạo canonical Customer.
7. Phone được chuẩn hóa.
8. Số hợp lệ được kiểm tra toàn công ty.
9. Không tìm thấy Customer thì có thể yêu cầu Party Context tạo minimal Customer theo policy.
10. Tìm thấy một Customer thì liên kết.
11. Tìm thấy nhiều Customer thì manual resolution.
12. Không lộ Customer ngoài scope.
13. Lead lưu được raw payload.
14. Raw payload có source schema version.
15. Webhook trùng không tạo Lead trùng.
16. Import không tạo duplicate Customer qua Party identity contracts.
17. Source được lưu.
18. Campaign được lưu.
19. First-touch được lưu.
20. Reassignment không đổi source.
21. Tạo được queue.
22. Lead vào đúng queue.
23. Tạo được routing rule.
24. Routing rule có version.
25. Routing loại user inactive.
26. Routing loại user nghỉ phép.
27. Routing loại user không có Project Access.
28. Round-robin hoạt động.
29. Capacity hoạt động.
30. Routing lưu candidate.
31. Routing giải thích lý do chọn sale.
32. Một Lead chỉ có một primary assignment.
33. Sale accept được.
34. Sale reject có reason.
35. Quá acceptance SLA có escalation.
36. Reassignment giữ lịch sử.
37. Sale ghi được activity.
38. Call connected có thể được xác định meaningful.
39. Call không nghe không mặc định meaningful.
40. Tin nhắn một chiều không tự gia hạn protection.
41. Assignment tạo temporary handling right.
42. Meaningful interaction tạo protection theo policy.
43. Protection có ngày hết hạn.
44. Protection được gia hạn bằng sự kiện hợp lệ.
45. Protection thủ công cần reason.
46. Một context không có hai primary protection.
47. Cùng Customer khác project có thể có sale khác.
48. Buyer-side và Seller-side có thể tách.
49. Protection hết hạn vẫn giữ lịch sử.
50. Mở được dispute.
51. Dispute có evidence.
52. Resolve dispute cập nhật protection đúng.
53. Buyer Lead qualification hoạt động.
54. Seller Lead qualification hoạt động.
55. Lead Score hoạt động.
56. Score lưu model version.
57. Score thấp không tự đóng Lead.
58. Manual priority lưu riêng.
59. Lead vào Nurture được.
60. Nurture có next contact.
61. Lead được reactivate.
62. Reactivation không tự khôi phục protection cũ.
63. Convert được sang Requirement.
64. Convert được sang Buyer Deal.
65. Convert được sang Asset Verification.
66. Convert được sang Listing Acquisition Deal.
67. Conversion lưu attribution.
68. Conversion có idempotency.
69. Conversion lặp không tạo resource trùng.
70. Không tạo duplicate active Deal.
71. Seller Lead không tạo Listing active trực tiếp.
72. Consent được lưu.
73. Opt-out chặn contact.
74. SLA dùng Business Calendar.
75. SLA khác nhau theo Lead type.
76. Quá SLA không tự đóng Lead.
77. Sale chỉ xem `mine`.
78. Team Lead xem `team`.
79. Department Head xem `department`.
80. Director xem `all` theo quyền.
81. Backend enforce scope.
82. Sửa URL không mở rộng quyền.
83. Project Access không mở Customer scope.
84. Field masking hoạt động.
85. Sale không export hàng loạt.
86. Team Lead không export hàng loạt.
87. Marketing không xem hồ sơ tài chính.
88. Leave ngừng routing Lead mới.
89. Offboarding tạo handover.
90. Team Lead làm custodian theo policy.
91. Handover không đổi attribution.
92. Handover không tự chuyển commission.
93. Dashboard drill-down đúng scope.
94. Audit lưu routing rule version.
95. Audit lưu protection event.
96. Audit lưu conversion.
97. Alert khi không có routing candidate.
98. Alert khi protection xung đột.
99. Alert khi converted hai lần.
100. Capability hỗ trợ cả Lead mua và Lead bán.
101. Capability hỗ trợ doanh nghiệp tự làm chủ đầu tư.
102. Capability hỗ trợ phân phối dự án ngoài.
103. Capability hỗ trợ ký gửi tài sản Customer.
104. Capability hỗ trợ đất nền.
105. Capability không giả định mọi Lead là Buyer Lead.
106. Capability không giả định người nhập Lead là owner.
107. Capability không tạo quyền sở hữu Customer vĩnh viễn.
108. Capability giữ lịch sử Lead đã đóng.
109. Capability hoạt động với một hoặc nhiều Legal Entity.
110. Capability cung cấp dữ liệu sạch cho Customer 360, Matching và Deal.

---

# 79. Anti-patterns và canonical requirements

Phần này thay thế mọi cách diễn đạt mang tính “đặc tả cũ/phiên bản mới”. Các nội dung dưới đây là quy tắc hiện hành của dự án Greenfield.

## AP-LEA-001 — Đồng nhất Lead với Customer

**Không được áp dụng**

Mỗi Lead được coi là một Customer mới.

**Canonical requirement**

Lead và Customer là hai concepts khác nhau. Một Customer có thể có nhiều Lead; identity resolution và Customer creation thuộc Party Context.

## AP-LEA-002 — Mọi Lead đều là Buyer Lead

**Không được áp dụng**

Ép mọi Lead vào nhu cầu mua sản phẩm.

**Canonical requirement**

Lead có thể đại diện buyer, seller, consignment, renter, land owner, partner, referral hoặc intent chưa xác định.

## AP-LEA-003 — Conversion chỉ tạo Deal mua

**Không được áp dụng**

Mọi Lead qualified đều được chuyển trực tiếp thành Buyer Deal.

**Canonical requirement**

Lead có thể tạo Requirement, Deal, Asset Verification, Listing Acquisition hoặc Partner Opportunity theo intent và owning Context.

## AP-LEA-004 — Protection gắn vĩnh viễn vào Customer

**Không được áp dụng**

Sale có meaningful interaction thì sở hữu toàn bộ Customer vô thời hạn.

**Canonical requirement**

Protection có care context, effective period, evidence và lifecycle; không mở rộng quyền ngoài context và không tạo Customer ownership.

## AP-LEA-005 — Assignment tự tạo protection dài hạn

**Không được áp dụng**

Routing/assignment ngay lập tức tạo quyền bảo vệ đầy đủ.

**Canonical requirement**

Assignment chỉ tạo temporary handling right theo policy. Protection chính thức cần qualifying evidence hoặc approved event.

## AP-LEA-006 — Activity tự khai báo luôn meaningful

**Không được áp dụng**

Call attempt, one-way message, Task hoặc internal note tự gia hạn protection.

**Canonical requirement**

Meaningful interaction phải đáp ứng policy và evidence; generic Interaction facts thuộc Activity Context.

## AP-LEA-007 — Lead direct-query hoặc direct-write Customer tables

**Không được áp dụng**

Lead Context tự query Phone Identity tables, tạo Customer hoặc merge Customer bằng repository/SQL của Party Context.

**Canonical requirement**

Lead sử dụng published Party contracts; Party là source of truth cho identity, duplicate resolution, merge và redirect.

## AP-LEA-008 — Conversion dùng một cross-context transaction

**Không được áp dụng**

Lead, Requirement và Deal được tạo trong một shared transaction bằng cross-schema writes.

**Canonical requirement**

Conversion dùng local transactions, durable messaging/process management, idempotency và reconciliation.

## AP-LEA-009 — Source thay đổi khi reassignment

**Không được áp dụng**

Chuyển sale làm thay Campaign, referral, original creator hoặc first-touch source.

**Canonical requirement**

Assignment/care ownership và attribution/source lineage là các concepts độc lập.

## AP-LEA-010 — Importer hoặc creator mặc định sở hữu Lead

**Không được áp dụng**

Người nhập/import Lead tự động trở thành assignee hoặc được protection.

**Canonical requirement**

Routing, assignment và protection phải tuân eligibility, scope, policy và conflict checks.

## AP-LEA-011 — Frontend quyết định scope hoặc assignment eligibility

**Không được áp dụng**

Frontend truyền `scope=all`, `owner_id`, `sale_id`, `team_id` hoặc project để mở rộng access/routing.

**Canonical requirement**

Backend resolve effective authorization, workforce context, project access, queue eligibility và resource relationship.

## AP-LEA-012 — Project Access mở Customer scope

**Không được áp dụng**

Sale được bán Project A thì được xem mọi Customer quan tâm Project A.

**Canonical requirement**

Project Access chỉ cho phép product/project actions; Customer access vẫn phụ thuộc IAM/Party/Lead care relationships và masking.

## AP-LEA-013 — Score tự động loại bỏ con người

**Không được áp dụng**

Lead score thấp tự đóng Lead, tước protection hoặc quyết định khả năng tài chính.

**Canonical requirement**

Scoring hỗ trợ prioritization, có version/explanation và không thay human-authorized business decision.

## AP-LEA-014 — Nurture giữ protection vô hạn

**Không được áp dụng**

Đưa Lead vào nurture để sale giữ Customer mãi mãi.

**Canonical requirement**

Nurture có lifecycle, next action và protection behavior riêng; protection phải hết hạn hoặc giảm theo policy.

## AP-LEA-015 — Candidate examples là exact contracts

**Không được áp dụng**

Dùng status codes, table names, endpoint paths, permission codes, Event names hoặc SLA numbers trong tài liệu này để code như contract cuối cùng.

**Canonical requirement**

Exact implementation thuộc Context Packs, Alembic, OpenAPI, JSON Schema/AsyncAPI, security registries và environment configuration.

## AP-LEA-016 — Mặc định có legacy migration

**Không được áp dụng**

Suy luận rằng có hệ thống tiền nhiệm, data migration hoặc compatibility layer phải duy trì.

**Canonical requirement**

`crm_bds_ai` là Greenfield. Migration/import từ hệ thống bên ngoài chỉ được thực hiện khi có approved scope, mapping, reconciliation và acceptance criteria.

---
# 80. Kết luận

Lead Management Capability là cửa ngõ tiếp nhận và điều phối tín hiệu kinh doanh của `crm_bds_ai`.

Capability phải bảo đảm:

- Lead được tiếp nhận mà không mất source lineage.
- Lead và Customer không bị đồng nhất.
- Customer identity được resolve qua Party Context.
- Creator/importer không tự động trở thành owner hoặc protected assignee.
- Routing và assignment tôn trọng effective authorization, workforce state, project access, capacity và policy.
- Assignment, acceptance, reassignment và handover có history.
- Care protection bảo vệ công sức hợp lệ nhưng không tạo quyền sở hữu Customer vĩnh viễn.
- Buyer, seller, consignment, land-owner và partner intents được mô hình hóa phù hợp.
- Qualification và scoring hỗ trợ quyết định nhưng không tự động loại bỏ con người.
- Conversion dùng cross-context contracts, idempotency và reconciliation.
- Leave, transfer và offboarding không làm mất Lead, attribution hoặc history.
- Consent, masking, export restrictions và backend authorization được enforce.
- Activity, Marketing, Party, Product và Transaction ownership được tôn trọng.
- Candidate examples không bị dùng thay exact contracts.

> Lead Management Capability cung cấp dữ liệu đầu vào sạch, có nguồn gốc, có trách nhiệm và có context cho Customer 360, Matching, Product acquisition, Deal và toàn bộ hành trình giao dịch tiếp theo.
