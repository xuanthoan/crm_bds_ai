# CRM_BDS_AI — CAPABILITY 04: CUSTOMER 360, REQUIREMENTS AND FINANCIAL PROFILE

## Customer Relationship, Requirements, Financial Profile, Seller/Owner Declarations and Stakeholder Management

**Document ID:** `PROD-CAP-PAR-004`  
**Canonical path:** `docs/product/capabilities/cap-04-customer-360.md`  
**Product:** `crm_bds_ai`  
**Version:** `1.0.0`  
**Status:** `Accepted / Product Capability Baseline`  
**Document type:** `Product Capability Specification`  
**Primary capability code:** `CAP-PAR`  
**Primary owning Context:** `party`  
**Owner:** `Product Owner`  
**Co-owner:** `Party Domain Owner`  
**Reviewers:** `Architecture Owner`, `Security Owner`, `Lead Domain Owner`, `Product Domain Owner`, `Transaction Domain Owner`, `Contract Domain Owner`, `Activity Domain Owner`, `Marketing Domain Owner`, `Documents Domain Owner`, `QA Owner`  
**Effective date:** `2026-08-05`  
**Last reviewed:** `2026-08-05`  
**Classification:** `INTERNAL`

---

# 0. Phạm vi thẩm quyền và quan hệ tài liệu

Tài liệu này là nguồn canonical cho:

- Business outcomes của Customer 360 Capability.
- Party–Customer relationship semantics.
- Customer roles, lifecycle và enterprise-wide identity usage.
- Customer Requirements và structured criteria.
- Financial Profile, Financial Readiness và affordability snapshots.
- Seller/Owner declarations trước khi Product Context xác minh Asset/Ownership.
- Related parties, stakeholder maps, responsibilities, notes và Customer-context access outcomes.
- Consent, contact preferences và contact restrictions ở cấp Customer relationship.
- Product-level invariants, acceptance outcomes và anti-patterns của capability.

Tài liệu này không phải nguồn exact cho:

- Physical database schema hoặc DDL.
- Exact API paths, payloads hoặc error contracts.
- Exact Event names, payloads hoặc channels.
- Exact permission codes, scopes, masking hoặc Segregation of Duties rules.
- Exact lifecycle state machines.
- Exact UI routes, tabs hoặc component contracts.
- Exact SLA values, retention periods hoặc runtime topology.
- Exact implementation của Customer Identity Governance.

Nguồn exact tương ứng:

| Chủ đề | Nguồn canonical |
|---|---|
| Thuật ngữ | Domain Glossary |
| Product requirements | PRD |
| Context ownership | Source of Truth Matrix |
| Architecture boundaries | Architecture Overview, Context Map và Accepted ADRs |
| Party/Customer behavior chi tiết | Party Context Implementation Pack |
| Identity, Phone, merge và redirect | Customer Identity Governance Capability + Party Context Pack |
| Database | Alembic migrations và Party Context DB Specification |
| API | OpenAPI |
| Events | JSON Schema và AsyncAPI |
| Permissions/scopes/masking | Security registries và matrices |
| Documents | Documents Context contracts |
| Timeline/Interaction | Activity Context contracts |
| Công việc hiện tại | Current Sprint Detailed Execution Pack |

**Capability không đồng nghĩa Bounded Context.** Capability 04 và Customer Identity Governance Capability đều được thực hiện chủ yếu trong `party` Context. Việc tách thành hai capability nhằm phân tách product concerns, không tạo hai Customer masters hoặc hai identity authorities.

Các phần “candidate lifecycle vocabulary”, “candidate data model”, “candidate application operations”, “candidate permission vocabulary” và “candidate business facts” chỉ là đầu vào thiết kế. Chúng không được dùng thay Context Pack, migrations, OpenAPI, Event contracts hoặc security registries đã được chấp nhận.

---
# 1. Mục tiêu của capability

Customer 360 Capability xây dựng một hồ sơ Customer thống nhất trong enterprise operating boundary và cung cấp góc nhìn có kiểm soát về toàn bộ quan hệ thương mại của Customer với doanh nghiệp.

Capability phải giúp người dùng có thẩm quyền trả lời:

- Customer là cá nhân hay tổ chức và identity canonical nào đang được sử dụng.
- Customer có những contact points, roles và Legal Entity relationships nào.
- Customer đã phát sinh Lead, Requirement, Seller Objective, Deal, Contract hoặc activity nào theo phạm vi được phép.
- Customer đang có bao nhiêu nhu cầu active và mỗi nhu cầu thuộc context nào.
- Budget, Financial Profile, Financial Readiness và borrowing need áp dụng cho context nào.
- Customer khai báo sở hữu hoặc có liên quan đến tài sản nào và trạng thái xác minh ra sao.
- Ai là decision maker, payer, co-buyer, co-owner, representative, influencer hoặc end user trong từng Requirement/Deal/Contract context.
- Những sale, team hoặc đơn vị nào đang chịu trách nhiệm cho từng Requirement, seller-side objective hoặc transaction context.
- Consent, contact preferences và restrictions nào đang có hiệu lực.
- Vì sao một actor được phép xem Customer và section/field nào phải được full-view, masked hoặc concealed.
- Dữ liệu nào là source fact, dữ liệu nào chỉ là projection, snapshot hoặc declaration.

Capability phải hỗ trợ:

- Individual Customer và Organization Customer.
- Buyer, Seller, Owner, Land Owner, Investor, Tenant, Landlord, Payer, Representative và Referrer roles.
- Một Customer đồng thời có nhiều roles và nhiều Requirements.
- Nhiều Legal Entity relationships nhưng không tạo Customer duplicate chỉ vì khác Legal Entity.
- Structured Requirements, Seller Objectives và declared-asset claims.
- Context-scoped Financial Profiles.
- Related Party và Stakeholder maps.
- Customer 360 projection từ nhiều Context.
- Consent, privacy, masking và context-based access.
- Archive, restore và merge redirect behavior có lineage.

Nguyên tắc canonical:

> Customer là hồ sơ quan hệ thương mại dùng chung trong enterprise boundary; identity canonical thuộc `party` Context, còn activity, care protection, Asset/Ownership, Deal, Contract, Payment, Revenue, Commission, Documents và Audit vẫn thuộc owning Context tương ứng. Customer 360 chỉ tổng hợp theo quyền và không tạo nguồn chân lý cạnh tranh.

---
# 2. Vị trí của capability trong kiến trúc

Customer 360 Capability chủ yếu thuộc `party` Context và phối hợp với:

```text
Platform Configuration Capability
→ policy, calendar, numbering và configuration definitions

Identity, Access and Organization Capability
→ authenticated identity, organization và authorization context

Lead Management Capability
→ Lead facts, assignment/care-protection references và conversion requests

Customer Identity Governance Capability
→ Phone Identity, duplicate prevention, merge, redirect và identity resolution
  (cùng thuộc Party Context)

Customer 360 Capability
→ Party, Customer, roles, Requirements, Financial Profile,
  declarations, relationships và Customer 360 projection

Product Capability
→ Asset, Ownership, Selling Right, Listing, Availability và Commercial Lock

Matching Capability
→ matching execution, candidates, score và explanation

Deal and Transaction Capability
→ Deal, Transaction Case, Proposal, Hold và Booking

Contract and Cash Capability
→ Contract, Payment Schedule, Receivable, Payment, Receipt, Refund và Settlement

Revenue and Commission Capability
→ Revenue và Commission facts

Activity and Engagement Capability
→ Task, Appointment, Interaction và canonical Timeline facts

Marketing Capability
→ Campaign, Touchpoint, Audience, Journey và marketing eligibility

Documents Capability
→ File, Document, Dossier, verification và signature evidence

Audit Capability
→ immutable Audit facts
```

Luồng product-level điển hình:

```text
Lead
→ Customer identity resolution
→ Customer/Party link
→ Requirement hoặc Seller Objective
→ Financial Profile/Stakeholder Map
→ Matching hoặc Asset Verification
→ Deal/Transaction Case
→ Booking/Contract/Cash
→ Revenue/Commission
```

Customer 360 không được:

- Direct-write dữ liệu của Context khác.
- Sao chép source facts rồi trở thành competing source of truth.
- Dùng một `owner_sale_id` cố định để biểu diễn mọi responsibility.
- Dùng Project Access để mở rộng Customer scope.
- Dùng Customer Role làm permission.
- Trả toàn bộ hồ sơ rồi yêu cầu frontend tự ẩn.
- Suy luận rằng capability đánh số quyết định package, schema hoặc Bounded Context.

---
# 3. Ranh giới sở hữu dữ liệu

## 3.1. `party` Context sở hữu cho capability này

- Party.
- Customer relationship record.
- Customer lifecycle và Customer roles.
- Individual/Organization Party profiles.
- Customer emails, addresses và social-account relationships.
- Customer-level contact preferences, restrictions và consent facts theo accepted policy.
- Customer segments/tags khi là customer-domain classification.
- Customer Requirement và structured criteria.
- Requirement responsibilities và stakeholders.
- Financial Profile, income/capital/obligation declarations, borrowing need và readiness summary.
- Seller Profile, Seller Objective và declared-asset/ownership claims trước xác minh.
- Party relationships, Related Party stubs và Stakeholder Map.
- Customer notes và note-version lineage khi thuộc Customer domain.
- Customer Context và access-explanation projection.
- Customer 360 operational projection.
- Archive/restore eligibility và merge-redirect behavior.
- Logical references/snapshots cần thiết để liên kết facts từ Context khác.

## 3.2. Cùng `party` Context nhưng thuộc Customer Identity Governance concern

- Phone Identity.
- Phone normalization và verification.
- Duplicate prevention.
- Shared-phone exception.
- Identity Resolution Case.
- Customer merge.
- Redirect.
- Rebinding/reconciliation sau merge.

Capability 04 không tạo một identity subsystem riêng và không direct-write normalized phone ngoài accepted Party Context behavior.

## 3.3. Các Context khác sở hữu

- Lead, assignment, care protection, nurture và conversion process state: `lead`.
- User, workforce, organization và authorization: `iam`.
- Task, Appointment, Interaction và canonical Timeline facts: `activity`.
- Campaign, Touchpoint, marketing attribution model và marketing execution: `marketing`.
- Asset, verified Ownership, Selling Right, Listing, Availability và Commercial Lock: `product`.
- Matching runs/results: `matching`.
- Deal và Transaction Case: `transaction`.
- Contract, Payment, Receipt, Refund và Settlement: `contract`.
- Revenue và Commission: `revenue`.
- File, Document, Dossier và signature evidence: `documents`.
- Immutable Audit facts: `audit`.
- Provider/integration runtime: `integration`.
- Jobs/incidents/recovery runtime: `operations`.

## 3.4. Customer 360 là projection, không phải master của mọi dữ liệu

Customer 360 có thể lưu:

- Source reference.
- Approved summary.
- Read-model projection.
- Versioned snapshot khi lịch sử cần tái tạo.
- Freshness timestamp.
- Visibility metadata.

Customer 360 không được:

- Sao chép nguyên Contract, Payment, Receipt, Asset hoặc Deal.
- Sửa source data thông qua projection.
- Trở thành nguồn official cho financial hoặc legal facts.
- Mất source reference và provenance.
- Hiển thị stale data như current truth mà không có freshness.

## 3.5. Cross-context references

Các ID của Lead, Asset, Listing, Deal, Contract, Document hoặc Interaction là logical references.

Tài liệu này không mặc định:

- Cross-schema foreign key.
- Cross-context repository import.
- Shared transaction.
- Direct cross-context write.

Exact integration thuộc Context Map, API/Event contracts và Context Packs.

---
# 4. Khái niệm Party và Customer

## 4.1. Party

Party là một cá nhân hoặc tổ chức có thể tham gia nghiệp vụ.

Các loại:

```text
INDIVIDUAL
ORGANIZATION
```

Party có thể là:

* Customer.
* Employee.
* Chủ tài sản.
* Người mua.
* Người bán.
* Người đại diện.
* Đối tác.
* Chủ đầu tư.
* Cộng tác viên.

## 4.2. Customer

Customer là hồ sơ thể hiện Party có hoặc đã có quan hệ thương mại với công ty.

Không phải mọi Party đều là Customer.

Ví dụ:

* Một ngân hàng tích hợp có thể là Party nhưng chưa phải Customer.
* Một người đồng sở hữu được khai báo tạm thời có thể chưa có Customer chính thức.
* Một nhân viên có thể là Party và Workforce, nhưng chỉ trở thành Customer khi phát sinh quan hệ mua/bán.

## 4.3. Một Party chỉ có một Customer relationship chính trong Enterprise

Không tạo nhiều Customer cho cùng một Party chỉ vì:

* Khác dự án.
* Khác Legal Entity.
* Khác sale.
* Khác Lead.
* Khác vai trò Buyer/Seller.
* Khác chi nhánh.

Các quan hệ khác nhau được biểu diễn bằng:

* Customer Role.
* Requirement.
* Care Context.
* Deal.
* Listing Owner Relationship.
* Contract Party Role.

---

# 5. Customer dùng chung trong enterprise operating boundary nhưng không hiển thị không giới hạn

## 5.1. Customer Core là dữ liệu dùng chung

Các dữ liệu định danh lõi thuộc Enterprise:

* Customer ID.
* Party ID.
* Tên.
* Loại Customer.
* Phone Identity.
* Email.
* Address.
* Trạng thái.
* Consent.
* Customer role.

## 5.2. Không phải user nào cũng được xem toàn bộ Customer

Quyền truy cập được xác định từ:

* Lead active.
* Care protection.
* Requirement responsibility.
* Deal participation.
* Listing seller-side assignment.
* Contract participation.
* Task assignment.
* Project context.
* Share Grant.
* Team/department scope.
* Legal Entity context.
* Field permission.

## 5.3. Không sử dụng `owner_sale_id` làm quyền sở hữu Customer

Customer không có một sale sở hữu vĩnh viễn.

Có thể có:

* Sale phụ trách Requirement A.
* Sale phụ trách Project B.
* Sale phụ trách Seller Profile.
* Sale phụ trách Listing.
* Sale phụ trách Deal.
* Custodian tạm thời.

---

# 6. Mã Customer và danh tính hệ thống

## 6.1. Customer ID

Customer ID là khóa hệ thống không thay đổi.

## 6.2. Customer Code

Được cấp từ Numbering Engine Platform Configuration Capability.

Ví dụ:

```text
CUS-2026-000123
```

## 6.3. Customer Code không dùng để xác định trùng

Duplicate Customer cá nhân vẫn dựa trên Phone Identity theo Customer Identity Governance Capability.

## 6.4. Mã ngoài hệ thống

Có thể lưu:

* Customer ID từ approved external source.
* External CRM namespace ID khi integration được phê duyệt.
* ERP Customer Code.
* Chủ đầu tư Customer ID.
* Partner ID.
* Portal ID.

Mỗi external ID phải gắn:

* Nguồn.
* Namespace.
* Giá trị.
* Ngày hiệu lực.
* Trạng thái.
* Unique rule theo nguồn.

---

# 7. Loại Customer

## 7.1. Individual Customer

Customer cá nhân.

Có thể là:

* Người mua.
* Người bán.
* Chủ tài sản.
* Người thuê.
* Người cho thuê.
* Người thanh toán.
* Người đại diện.
* Người giới thiệu.

## 7.2. Organization Customer

Customer tổ chức.

Ví dụ:

* Doanh nghiệp mua bất động sản.
* Doanh nghiệp bán hoặc ký gửi tài sản.
* Quỹ đầu tư.
* Đơn vị thuê.
* Đơn vị mua đất.
* Đơn vị hợp tác.

## 7.3. Household hoặc nhóm gia đình

Không tạo một Customer giả đại diện cả gia đình.

Mô hình khuyến nghị:

```text
Customer chính
+ Related Parties
+ Transaction Participants
+ Household/Relationship Group
```

## 7.4. Group Purchase

Một nhóm mua chung được biểu diễn bằng:

* Nhiều Customer.
* Một Customer chính cho liên hệ nếu cần.
* Requirement chung hoặc các Requirement liên kết.
* Participant roles.
* Ownership ratio ở hợp đồng.

---

# 8. Candidate Customer lifecycle vocabulary

> Exact lifecycle, transitions và guards thuộc Party Context Implementation Pack. Danh sách dưới đây là product vocabulary đầu vào, không phải state machine canonical.


## 8.1. Trạng thái đề xuất

```text
NEW
PROFILE_INCOMPLETE
ACTIVE
IN_CARE
ACTIVE_REQUIREMENT
ACTIVE_SELLER
ACTIVE_DEAL
BOOKING
DEPOSIT
CONTRACTED
PURCHASED
SOLD_ASSET
AFTER_SALES
NURTURE
PAUSED
UNREACHABLE
NO_CURRENT_NEED
RESTRICTED_CONTACT
DISPUTED
MERGED
ARCHIVED
SOFT_DELETED
```

## 8.2. Customer Status không thay thế Lead/Deal Status

Ví dụ:

* Customer có thể `ACTIVE`.
* Một Lead của Customer đã `LOST`.
* Một Deal khác vẫn `NEGOTIATING`.
* Một Requirement khác đang `NURTURE`.

## 8.3. Trạng thái có thể được tính từ context

Một số trạng thái Customer 360 có thể là projection:

* Có active Requirement.
* Có active Deal.
* Có Contract.
* Có unpaid debt.

Không nên yêu cầu user cập nhật thủ công mọi trạng thái tổng hợp.

## 8.4. Trạng thái chính thức và trạng thái hiển thị

Có thể tách:

* `lifecycle_status`: trạng thái nghiệp vụ chính.
* `engagement_summary`: trạng thái tổng hợp hiển thị.

---

# 9. Candidate Customer Role vocabulary

> Exact role codes và semantics thuộc Domain Glossary, Party Context Pack và machine contracts. Customer Role không phải IAM role hoặc permission.


## 9.1. Các vai trò chuẩn

```text
BUYER
SELLER
PROPERTY_OWNER
LAND_OWNER
INVESTOR
TENANT
LANDLORD
PAYER
CO_PAYER
BORROWER
CO_BORROWER
GUARANTOR
CO_BUYER
CO_OWNER
END_USER
DECISION_MAKER
REPRESENTATIVE
AUTHORIZED_PERSON
REFERRER
BENEFICIARY
ORGANIZATION_CONTACT
```

## 9.2. Một Customer có nhiều role

Ví dụ:

* `SELLER`
* `PROPERTY_OWNER`
* `BUYER`
* `INVESTOR`

có thể cùng tồn tại.

## 9.3. Role có ngày hiệu lực

Mỗi role lưu:

* Ngày bắt đầu.
* Ngày kết thúc.
* Nguồn.
* Context.
* Trạng thái.
* Người xác minh.

## 9.4. Role không tự cấp quyền truy cập

Customer Role là dữ liệu nghiệp vụ, không phải permission.

---

# 10. Hồ sơ Customer cá nhân

## 10.1. Thông tin cơ bản

* Họ tên.
* Tên gọi.
* Ngày sinh nếu cần.
* Giới tính nếu Customer tự cung cấp và nghiệp vụ hợp lệ.
* Quốc tịch.
* Ngôn ngữ.
* Nghề nghiệp.
* Chức vụ.
* Nơi làm việc.
* Tình trạng hồ sơ.
* Nguồn xác minh.
* Ngày cập nhật.

## 10.2. Thông tin giấy tờ

Có thể lưu metadata:

* Loại giấy tờ.
* Số giấy tờ đã mã hóa/mask.
* Ngày cấp.
* Nơi cấp.
* Ngày hết hạn.
* Trạng thái xác minh.
* Link tài liệu.

Không hiển thị đầy đủ nếu không có permission.

## 10.3. Không thu thập quá mức

Chỉ thu thập thông tin phục vụ:

* Tư vấn.
* Giao dịch.
* Ký hợp đồng.
* Thanh toán.
* Compliance.

Không bắt buộc mọi trường ngay từ khi Customer mới được tạo.

---

# 11. Hồ sơ Customer tổ chức

## 11.1. Thông tin cơ bản

* Tên pháp lý.
* Tên thương mại.
* Loại tổ chức.
* Mã số thuế.
* Số đăng ký.
* Quốc gia.
* Địa chỉ đăng ký.
* Website.
* Ngành nghề.
* Quy mô.
* Trạng thái.
* Người đại diện.
* Người liên hệ chính.

## 11.2. Người liên hệ tổ chức

Một Organization Customer có nhiều contact person:

* Người ra quyết định.
* Người ký.
* Kế toán.
* Pháp chế.
* Người sử dụng.
* Người thanh toán.
* Trợ lý.

## 11.3. Duplicate tổ chức

Không sử dụng quy tắc phone-only của Customer cá nhân.

Registry tổ chức có thể kiểm tra:

* Mã số thuế.
* Số đăng ký.
* Legal name.
* Namespace external ID.

Chi tiết thuộc Customer Identity Governance concern và Party Context contracts.

---

# 12. Thông tin liên hệ

## 12.1. Phone Identity

Phone Identity, normalization, verification, duplicate enforcement và primary-phone governance thuộc Customer Identity Governance concern trong cùng `party` Context.

Customer 360 phải:

- Hiển thị phone theo permission và masking.
- Gửi command qua accepted Party application service khi thêm, sửa, xác minh hoặc đặt primary.
- Nhận identity-resolution outcome.
- Không ghi trực tiếp normalized phone hoặc bypass duplicate rules.
- Không lộ Customer ngoài scope khi phone đã tồn tại.

## 12.2. Email

Một Customer có thể có nhiều email theo purpose và context:

- Cá nhân.
- Công việc.
- Kế toán.
- Hợp đồng.
- Email phụ.

Thuộc tính có thể gồm:

- Raw value và normalized value.
- Type/purpose.
- Primary indicator.
- Verification state.
- Active/effective period.
- Consent/restriction reference.
- Source và provenance.

Exact fields thuộc Party Context DB Specification.

## 12.3. Social Account

Có thể quản lý các account references như Zalo, Facebook, Messenger, LinkedIn, Telegram hoặc kênh khác.

Mỗi account phải có:

- Platform/namespace.
- External identifier.
- Verification state.
- Primary/active state.
- Source và effective period.
- Privacy/consent policy.

## 12.4. Address

Một Party/Customer có thể có nhiều addresses theo purpose:

- Registered/residential.
- Current/contact.
- Billing.
- Organization address.
- Transaction-specific address.

Địa chỉ tài sản chính thức thuộc Product Context; Party chỉ giữ contact/address relationship hoặc declaration phù hợp.

---
# 13. Primary Contact

## 13.1. Một primary theo loại

Có thể có:

* Primary phone.
* Primary email.
* Primary address.
* Primary social channel.

## 13.2. Không xóa contact cũ

Contact cũ được:

* Inactivate.
* Đặt ngày hết hiệu lực.
* Ghi lý do.
* Giữ lịch sử.

## 13.3. Thay primary contact

Phải:

* Kiểm tra duplicate nếu là phone.
* Ghi before/after.
* Ghi người thay đổi.
* Có verification nếu policy yêu cầu.

---

# 14. Customer Segment

## 14.1. Segment có thể dựa trên

* Customer type.
* Nhu cầu.
* Giá trị giao dịch.
* Tần suất mua.
* Khu vực.
* Sản phẩm.
* Giai đoạn.
* Hồ sơ tài chính.
* Lịch sử giao dịch.
* Nguồn.

## 14.2. Segment hệ thống và segment thủ công

Tách:

* Segment do rule tính.
* Segment do user gán.
* Segment Marketing.
* Segment quản trị.

## 14.3. Segment không tự mở rộng quyền

Customer thuộc segment VIP không làm cho tất cả sale xem được Customer.

## 14.4. Không dùng dữ liệu nhạy cảm không liên quan

Không phân loại Customer bằng thuộc tính nhạy cảm không cần thiết cho nghiệp vụ.

---

# 15. Tag Customer

Tag dùng để hỗ trợ:

* Tìm kiếm.
* Phân nhóm.
* Campaign.
* Cảnh báo.
* Ghi nhớ nghiệp vụ.

Tag không được thay thế:

* Status.
* Role.
* Requirement.
* Consent.
* Risk flag.

Tag nhạy cảm cần permission.

---

# 16. Customer Requirement

## 16.1. Khái niệm

Requirement là một nhu cầu hoặc mục tiêu nghiệp vụ có cấu trúc của Customer.

Một Customer có thể có nhiều Requirement.

Ví dụ:

* Mua căn hộ để ở tại Hà Nội.
* Mua đất nền đầu tư.
* Bán căn hiện tại.
* Ký gửi biệt thự.
* Thuê văn phòng.
* Hợp tác phát triển đất.

## 16.2. Requirement Type

```text
BUY
INVEST
SELL
CONSIGN
RENT
LEASE_OUT
LAND_COOPERATION
PROJECT_COOPERATION
```

## 16.3. Một Requirement không phải Lead

Lead là tín hiệu đầu vào.

Requirement là nhu cầu đã được tổ chức hóa và xác minh ở mức nhất định.

## 16.4. Requirement không phải Deal

Requirement có thể tồn tại trước khi có sản phẩm hoặc cơ hội giao dịch cụ thể.

---

# 17. Candidate Requirement lifecycle vocabulary

> Exact states, transitions và guards thuộc Party Context Implementation Pack.


## 17.1. Trạng thái

```text
DRAFT
COLLECTING_INFORMATION
QUALIFYING
ACTIVE
MATCHING_READY
MATCHING
SHORTLISTED
DEAL_CREATED
NURTURE
PAUSED
FULFILLED
CANCELLED
EXPIRED
ARCHIVED
```

## 17.2. Requirement Active

Requirement active khi:

* Customer còn nhu cầu.
* Có người phụ trách.
* Không bị đóng.
* Consent và contact không chặn hoàn toàn.
* Có context rõ.

## 17.3. Fulfilled

Chỉ chuyển fulfilled khi:

* Giao dịch hoàn thành.
* Hoặc Customer xác nhận mục tiêu đã đạt.

Không tự fulfilled chỉ vì tạo Deal.

---

# 18. Tránh Requirement trùng

## 18.1. Duplicate active requirement

Hệ thống phải kiểm tra cùng:

* Customer.
* Requirement type.
* Project/khu vực.
* Property type.
* Mục tiêu.
* Thời gian.

## 18.2. Không tự merge Requirement

Có thể:

* Cảnh báo.
* Link.
* Yêu cầu user chọn.
* Tạo Requirement mới có lý do.

## 18.3. Trường hợp được phép nhiều Requirement gần nhau

Ví dụ:

* Mua để ở và đầu tư.
* Mua hai sản phẩm cho hai người sử dụng.
* Mua nhiều dự án.
* Seller objective khác nhau cho hai tài sản.

---

# 19. Thông tin nhu cầu mua

## 19.1. Mục đích

* Ở.
* Đầu tư tăng giá.
* Cho thuê.
* Nghỉ dưỡng.
* Kinh doanh.
* Cho người thân.
* Tích sản.
* Đổi tài sản.

## 19.2. Loại tài sản

* Căn hộ.
* Nhà phố.
* Biệt thự.
* Shophouse.
* Đất nền.
* Đất riêng lẻ.
* Văn phòng.
* Kho.
* Tài sản khác.

## 19.3. Vị trí

* Tỉnh/thành.
* Quận/huyện.
* Khu vực.
* Dự án.
* Bán kính.
* Gần tiện ích.
* Gần trường học.
* Gần nơi làm việc.

## 19.4. Ngân sách

* Ngân sách tối thiểu.
* Ngân sách mục tiêu.
* Ngân sách tối đa.
* Currency.
* Có thể mở rộng.
* Điều kiện mở rộng.
* Giá đã gồm thuế/phí hay chưa.

## 19.5. Thời gian mua

* Ngay.
* Trong một tháng.
* Trong ba tháng.
* Trong sáu tháng.
* Theo sự kiện.
* Chưa xác định.

## 19.6. Yêu cầu tài chính

* Vốn tự có.
* Khoản vay.
* Tỷ lệ vay.
* Khả năng thanh toán đợt đầu.
* Mức trả hàng tháng.
* Tài sản cần bán trước.
* Nguồn tiền khác.

---

# 20. Tiêu chí Requirement

## 20.1. Nhóm mức độ

Mỗi tiêu chí phải được phân loại:

```text
MANDATORY
PREFERRED
OPTIONAL
NOT_IMPORTANT
NOT_ACCEPTABLE
```

## 20.2. Ví dụ Mandatory

* Ngân sách tối đa.
* Khu vực.
* Tối thiểu hai phòng ngủ.
* Pháp lý cụ thể.
* Thời gian bàn giao.

## 20.3. Preferred

* Hướng.
* Tầng.
* View.
* Gần trường.
* Nội thất.

## 20.4. Not Acceptable

* Tầng thấp.
* Hướng cụ thể.
* Đang tranh chấp.
* Không có sổ.
* Khoảng cách vượt giới hạn.

## 20.5. Không lưu mọi tiêu chí trong một note

Tiêu chí phải có cấu trúc để Matching Engine sử dụng.

---

# 21. Candidate criterion vocabulary

> Exact criterion schema thuộc Party Context Pack và Matching contracts; Platform chỉ quản trị approved definitions khi được thiết kế như configuration.


Một criterion có thể là:

* Boolean.
* Number.
* Range.
* Enum.
* Multi-select.
* Text.
* Geography.
* Date.
* Duration.
* Formula condition.

Ví dụ:

```text
bedrooms >= 2
price <= 5_000_000_000
handover_date <= 2027-12-31
```

Cấu hình criterion schema thuộc Platform Configuration Capability hoặc Matching Capability.

---

# 22. Nhu cầu bán hoặc ký gửi

## 22.1. Seller Objective

Lưu:

* Tài sản đã xác định hay chưa.
* Loại tài sản.
* Vị trí.
* Giá kỳ vọng.
* Giá tối thiểu mong muốn.
* Lý do bán.
* Mức độ khẩn cấp.
* Thời gian cần bán.
* Độc quyền mong muốn.
* Phí chấp nhận.
* Có đồng sở hữu không.
* Có thế chấp không.
* Có tranh chấp không.
* Có người đại diện không.
* Sẵn sàng khảo sát không.
* Tài liệu hiện có.

## 22.2. Seller Objective không phải Listing

Seller Objective chỉ là nhu cầu của Customer.

Listing chỉ được tạo sau:

* Asset Verification.
* Ownership Verification.
* Quyền bán.
* Giá.
* Workflow approval.

## 22.3. Nhiều tài sản

Một Customer có thể có nhiều Seller Objective, mỗi tài sản một context riêng.

---

# 23. Owner Profile

## 23.1. Vai trò

Customer có thể là:

* Chủ sở hữu duy nhất.
* Đồng sở hữu.
* Người đại diện.
* Người được ủy quyền.
* Chủ đất.
* Người có quyền khai thác.
* Người cung cấp thông tin nhưng chưa xác minh.

## 23.2. Declared Ownership

Trước khi Product Capability xác minh tài sản, Customer 360 Capability có thể lưu khai báo:

* Loại tài sản.
* Địa chỉ.
* Mã tài sản nếu biết.
* Tỷ lệ sở hữu khai báo.
* Căn cứ khai báo.
* Đồng sở hữu.
* Tình trạng pháp lý sơ bộ.
* Tình trạng thế chấp.
* Mục đích.

## 23.3. Không coi khai báo là ownership chính thức

Phải phân biệt:

```text
DECLARED
DOCUMENT_RECEIVED
UNDER_VERIFICATION
VERIFIED
REJECTED
```

## 23.4. Chuyển sang Asset Verification

Khi đủ thông tin:

* Tạo Asset Verification Request ở Product Capability.
* Giữ link về Customer.
* Không xóa khai báo gốc.
* Nhận Asset ID sau xác minh.

---

# 24. Land Owner Profile

Thông tin có thể gồm:

* Vị trí đất.
* Diện tích.
* Số thửa/tờ bản đồ nếu có.
* Mục đích sử dụng.
* Tình trạng pháp lý.
* Quy hoạch sơ bộ.
* Đồng sở hữu.
* Mục tiêu hợp tác.
* Giá bán kỳ vọng.
* Tỷ lệ góp đất.
* Hình thức hợp tác mong muốn.
* Thời gian.
* Tài liệu.

Land Owner Profile không tự tạo Project hoặc Deal phát triển dự án.

---

# 25. Requirement Responsibility

## 25.1. Một Requirement có người phụ trách

Có thể gồm:

* Primary sale.
* Co-handler.
* Specialist.
* Manager.
* Financial consultant.
* Project consultant.

## 25.2. Nguồn trách nhiệm

* Lead conversion.
* Routing.
* Handover.
* Assignment.
* Share Grant.
* Deal creation.

## 25.3. Không thay đổi Customer core owner

Chỉ thay trách nhiệm của Requirement.

## 25.4. Lịch sử

Mọi thay đổi phải lưu:

* Người cũ.
* Người mới.
* Lý do.
* Ngày hiệu lực.
* Approval.
* Handover.

---

# 26. Requirement và Care Protection

Care Protection thuộc `lead` Context.

Customer 360 có thể hiển thị projection/reference gồm:

- Protection state.
- Protected actor.
- Care context.
- Effective/expiry time.
- Source and evidence reference.
- Dispute state.
- Freshness timestamp.

Requirement không được direct-create, extend hoặc end protection bằng cách sửa Party tables.

Khi Requirement được tạo từ Lead:

- Lead Context có thể gửi source/care-context facts.
- Party Context tạo Requirement trong local transaction.
- Lead và Party phối hợp qua accepted command/Event contracts.
- Attribution và source Lead reference phải được giữ.
- Protection stage chỉ thay đổi qua Lead policy và accepted integration.
- Retry phải idempotent và có reconciliation.

Không dùng distributed transaction hoặc cross-context business write.

---
# 27. Hồ sơ tài chính Customer

## 27.1. Mục tiêu

Hỗ trợ đánh giá:

* Khả năng mua.
* Nhu cầu vay.
* Khả năng thanh toán.
* Kế hoạch dòng tiền.
* Phù hợp sản phẩm.
* Rủi ro giao dịch.

Không thay thế:

* Thẩm định tín dụng của ngân hàng.
* Kết luận pháp lý.
* Tư vấn đầu tư được cấp phép.
* Báo cáo tài chính pháp định.

## 27.2. Customer có quyền từ chối cung cấp

Hồ sơ phải hỗ trợ trạng thái:

```text
NOT_REQUESTED
REQUESTED
PARTIALLY_PROVIDED
PROVIDED
CUSTOMER_DECLINED
UNAVAILABLE
UNDER_VERIFICATION
VERIFIED
EXPIRED
```

Không đánh dấu Customer không phù hợp chỉ vì từ chối cung cấp.

---

# 28. Phạm vi hồ sơ tài chính

Một Financial Profile có thể áp dụng cho:

* Toàn Customer.
* Một Requirement.
* Một Deal.
* Một giao dịch.
* Một thời kỳ.

Ví dụ Customer có khả năng tài chính khác nhau cho:

* Nhu cầu mua ở.
* Nhu cầu đầu tư.
* Giao dịch tổ chức.

## 28.1. Global Financial Profile

Dữ liệu tổng quan được Customer cho phép sử dụng chung.

## 28.2. Context Financial Profile

Dữ liệu chỉ phục vụ Requirement hoặc Deal cụ thể.

## 28.3. Không tự chia sẻ giữa các context

Nếu profile được đánh dấu restricted, sale ở Requirement khác không được xem.

---

# 29. Nội dung hồ sơ tài chính cá nhân

## 29.1. Thu nhập

* Loại thu nhập.
* Số tiền.
* Chu kỳ.
* Currency.
* Ổn định hay không.
* Nguồn.
* Ngày bắt đầu.
* Ngày kết thúc.
* Verification status.

## 29.2. Vốn tự có

* Tiền mặt.
* Tiền gửi.
* Khoản dự kiến nhận.
* Tài sản thanh khoản.
* Nguồn khác.

## 29.3. Nghĩa vụ tài chính

* Khoản vay.
* Trả góp.
* Nghĩa vụ định kỳ.
* Khoản nợ khác.
* Thời hạn.
* Monthly payment.

## 29.4. Tài sản khai báo

* Bất động sản.
* Phương tiện.
* Đầu tư.
* Tiền gửi.
* Tài sản khác.

## 29.5. Nhu cầu vay

* Số tiền cần vay.
* Tỷ lệ vay.
* Thời hạn.
* Mức trả hàng tháng mong muốn.
* Ngân hàng ưu tiên.
* Trạng thái pre-approval.

---

# 30. Hồ sơ tài chính tổ chức

Có thể gồm:

* Doanh thu.
* Lợi nhuận.
* Dòng tiền.
* Ngân sách đầu tư.
* Tài sản.
* Nợ.
* Nguồn vốn.
* Hạn mức tín dụng.
* Người phê duyệt ngân sách.
* Chu kỳ ra quyết định.
* Financial document metadata.

Dữ liệu chi tiết có thể được tích hợp từ hệ thống tài chính ngoài.

---

# 31. Verification tài chính

## 31.1. Mức xác minh

```text
SELF_DECLARED
DOCUMENT_RECEIVED
INTERNALLY_REVIEWED
BANK_PRE_APPROVED
EXTERNALLY_VERIFIED
REJECTED
EXPIRED
```

## 31.2. Người xác minh

Có thể là:

* Sale.
* Chuyên viên tài chính.
* Kế toán – Tài chính.
* Ngân hàng.
* Đối tác tín dụng.

## 31.3. Sale không được tự xác nhận mức cao

Sale có thể ghi `SELF_DECLARED` hoặc `DOCUMENT_RECEIVED`.

Các mức xác minh cao cần capability phù hợp.

## 31.4. Hết hiệu lực

Thông tin tài chính cần `as_of_date` và `expires_at` nếu policy yêu cầu.

---

# 32. Financial Readiness

## 32.1. Mục tiêu

Tạo summary phục vụ tư vấn:

* Ready.
* Ready with Financing.
* Need More Information.
* Need Asset Sale First.
* Budget Gap.
* Not Currently Ready.
* Customer Declined Assessment.

## 32.2. Không tự từ chối Customer

Financial Readiness chỉ:

* Cảnh báo.
* Hỗ trợ Matching.
* Đề xuất bước tiếp theo.

Không tự:

* Đóng Lead.
* Đóng Requirement.
* Từ chối Customer.
* Từ chối Booking.

## 32.3. Explanation

Phải giải thích:

* Dữ liệu đầu vào.
* Rule.
* Version.
* Khoảng thiếu hụt.
* Giả định.

---

# 33. Affordability Snapshot

Khi Matching hoặc Deal sử dụng dữ liệu tài chính, phải snapshot:

* Financial Profile ID.
* Version.
* As-of date.
* Ngân sách.
* Vốn tự có.
* Khoản vay.
* Mức trả hàng tháng.
* Assumption.
* Người xác nhận.

Không dùng dữ liệu Customer hiện tại để âm thầm thay đổi đánh giá lịch sử.

---

# 34. Bảo mật hồ sơ tài chính

## 34.1. Field-level permission

Sale có thể chỉ xem:

* Budget range.
* Readiness summary.
* Financing needed.

Không mặc định xem:

* Thu nhập chi tiết.
* Số dư.
* Khoản nợ.
* Tài liệu.
* Tài khoản ngân hàng.

## 34.2. Marketing

Không được xem hồ sơ tài chính chi tiết.

## 34.3. Accounting

Chỉ xem dữ liệu liên quan đến giao dịch đang xử lý.

## 34.4. Finance

Có thể xem trong phạm vi được giao.

## 34.5. Audit

Mọi lần xem hoặc export dữ liệu tài chính nhạy cảm cần được ghi log theo policy.

---

# 35. Người liên quan và Relationship Graph

## 35.1. Mục tiêu

Quản lý những người ảnh hưởng đến quyết định và giao dịch.

## 35.2. Loại quan hệ

* Vợ/chồng.
* Cha/mẹ.
* Con.
* Anh/chị/em.
* Người thân.
* Bạn.
* Đối tác.
* Đồng nghiệp.
* Trợ lý.
* Đại diện.
* Luật sư.
* Kế toán.
* Người giới thiệu.
* Người đồng mua.
* Người đồng sở hữu.
* Người thanh toán.
* Người đồng vay.
* Người bảo lãnh.
* Người sử dụng.
* Người ra quyết định.
* Người phản đối.
* Người tư vấn.

## 35.3. Quan hệ có hướng

Ví dụ:

```text
A IS_SPOUSE_OF B
A REPRESENTS B
A PAYS_FOR B
A REFERRED B
```

## 35.4. Quan hệ hai chiều

Một số relation cần tạo inverse:

```text
PARENT_OF ↔ CHILD_OF
REPRESENTS ↔ REPRESENTED_BY
```

## 35.5. Ngày hiệu lực

Quan hệ có thể thay đổi theo thời gian.

---

# 36. Related Person chưa phải Customer

## 36.1. Related Party Stub

Có thể lưu tối thiểu:

* Tên.
* Quan hệ.
* Vai trò.
* Phone/email theo quyền.
* Consent.
* Ghi chú.
* Nguồn.

## 36.2. Không bắt buộc tạo Customer ngay

Ví dụ chỉ biết:

* “Vợ là người quyết định.”
* “Anh trai sẽ đứng tên.”

## 36.3. Chuyển thành Customer

Khi người liên quan:

* Trực tiếp giao dịch.
* Cần được liên hệ.
* Đứng tên hợp đồng.
* Thanh toán.
* Đồng sở hữu.

thì chuyển qua quy trình identity check Customer Identity Governance Capability.

---

# 37. Vai trò người ảnh hưởng

## 37.1. Influence Role

```text
PRIMARY_DECISION_MAKER
CO_DECISION_MAKER
INFLUENCER
SUPPORTER
OPPONENT
ADVISOR
GATEKEEPER
PAYER
END_USER
LEGAL_SIGNER
```

## 37.2. Influence Level

* Very High.
* High.
* Medium.
* Low.
* Unknown.

## 37.3. Attitude

* Supportive.
* Neutral.
* Concerned.
* Opposed.
* Unknown.

## 37.4. Không dùng influence để thao túng trái consent

Thông tin này chỉ phục vụ phối hợp tư vấn và giao dịch hợp lệ.

---

# 38. Stakeholder Map theo Requirement/Deal

Relationship Graph là quan hệ chung.

Stakeholder Map xác định vai trò trong context cụ thể:

* Requirement.
* Deal.
* Listing.
* Contract.

Ví dụ:

* Vợ là payer trong Deal A.
* Nhưng không tham gia Requirement B.
* Luật sư chỉ tham gia Contract C.

---

# 39. Nhiều người mua và nhiều người bán

Customer 360 Capability phải chuẩn bị dữ liệu cho hợp đồng:

* Buyer.
* Co-buyer.
* Seller.
* Co-seller.
* Owner.
* Co-owner.
* Payer.
* Representative.
* Signer.
* Beneficiary.

Tỷ lệ sở hữu chính thức chỉ được xác nhận trong Transaction và Contract Context.

Customer 360 Capability lưu:

* Dự kiến.
* Khai báo.
* Role.
* Quan hệ.
* Verification.

---

# 40. Customer Context

## 40.1. Khái niệm

Customer Context là một phạm vi quan hệ nghiệp vụ.

Ví dụ:

* Customer + Buyer Requirement R1.
* Customer + Seller Objective S1.
* Customer + Project P1.
* Customer + Listing L1.
* Customer + Deal D1.
* Customer + Contract C1.

## 40.2. Mục tiêu

Dùng để:

* Tính quyền truy cập.
* Giới hạn timeline.
* Gắn note.
* Gắn stakeholder.
* Gắn financial profile.
* Gắn care protection.
* Gắn trách nhiệm.

## 40.3. Customer 360 là tổng hợp nhiều context

User chỉ được xem các context phù hợp với quyền.

---

# 41. Customer Access Relationship

## 41.1. Nguồn quyền truy cập

* Lead assignment.
* Care protection.
* Requirement responsibility.
* Deal participation.
* Seller-side responsibility.
* Listing access.
* Contract task.
* Finance assignment.
* Share Grant.
* Team/department scope.
* Director `all`.

## 41.2. Không tạo một bảng owner duy nhất

Có thể xây projection `customer_access_contexts` để tối ưu query, nhưng nguồn chân lý vẫn là các quan hệ nghiệp vụ.

## 41.3. Access explanation

Backend phải giải thích được:

> User được xem Customer vì đang là primary sale của Requirement R1.

---

# 42. Customer 360 Summary

## 42.1. Thông tin hiển thị

* Customer code.
* Tên.
* Type.
* Masked/full contacts theo quyền.
* Roles.
* Segment.
* Active Requirements.
* Active Deals.
* Active Listings/Owner links.
* Contracts.
* Outstanding tasks.
* Financial readiness.
* Care relationships.
* Consent.
* Risk/alert.
* Last meaningful interaction.
* Next action.

## 42.2. Không hiển thị mọi dữ liệu trong một màn hình

Sử dụng tab và permission-aware sections.

## 42.3. Summary phải tính theo thời gian thực hoặc projection được đồng bộ

Không dùng summary cũ không có timestamp.

---

# 43. Customer Timeline

## 43.1. Mục tiêu

Customer 360 cung cấp timeline view hợp nhất từ các facts mà actor được phép xem, ví dụ:

- Lead.
- Assignment/care protection.
- Interaction và Appointment.
- Requirement.
- Proposal và Deal.
- Asset verification, Listing và Booking.
- Contract, Payment và Receipt.
- Consent, handover và access changes.

## 43.2. Ownership

Canonical Interaction và Timeline facts thuộc `activity` Context hoặc owning Context của business fact.

Party Context có thể giữ:

- Source Context.
- Source resource reference.
- Approved summary.
- Customer/context link.
- Visibility metadata.
- Occurred-at timestamp.
- Projection freshness.

Timeline projection không thay source record.

## 43.3. Immutability và corrections

Business facts như Contract signed, Receipt issued, Customer merged hoặc Consent withdrawn không được sửa thông qua Timeline.

Khi source fact được corrected:

- Owning Context phát correction/replacement fact.
- Projection cập nhật idempotently.
- Lineage và original fact vẫn được giữ theo policy.

Customer notes có thể version/correct theo Party policy nhưng không được giả mạo source event.

---
# 44. Timeline Visibility

Các mức:

```text
PRIVATE
TEAM
DEPARTMENT
CUSTOMER_CONTEXT
DEAL_PARTICIPANTS
PROJECT
FINANCE
LEGAL
MANAGEMENT
COMPANY
```

## 44.1. Private

Chỉ tác giả xem, trừ audit/admin policy.

Không dùng Private để che giấu thông tin bắt buộc bàn giao.

## 44.2. Customer Context

Chỉ user có quyền trong context tương ứng.

## 44.3. Finance/Legal

Chỉ capability bundle phù hợp.

---

# 45. Ghi chú Customer

## 45.1. Loại note

* General.
* Sales.
* Requirement.
* Financial.
* Seller.
* Owner.
* Legal.
* Risk.
* Complaint.
* After-sales.
* Management.
* Private.

## 45.2. Note phải có context

Không nên tạo note không rõ áp dụng cho:

* Customer chung.
* Requirement.
* Deal.
* Asset.
* Contract.

## 45.3. Note quan trọng không sửa âm thầm

Các note:

* Pháp lý.
* Tài chính.
* Tranh chấp.
* Khiếu nại.
* Cam kết.

phải có version hoặc correction entry.

## 45.4. Không xóa note đã dùng trong quyết định

Có thể archive hoặc redact theo quyền đặc biệt.

---

# 46. Consent

## 46.1. Loại Consent

* Sales contact.
* Marketing contact.
* Data processing.
* Sharing with partner.
* Credit consultation.
* Document storage.
* Recording call.
* Electronic communication.
* Other.

## 46.2. Kênh

* Call.
* SMS.
* Zalo.
* Email.
* Push.
* Messenger.

## 46.3. Nội dung lưu

* Customer.
* Consent type.
* Purpose.
* Channel.
* Source.
* Evidence.
* Granted at.
* Expires at.
* Withdrawn at.
* Version của nội dung consent.

## 46.4. Consent theo mục đích

Customer đồng ý nhận tư vấn giao dịch không mặc định đồng ý Marketing dài hạn.

## 46.5. Ownership và consumption

`party` Context sở hữu Customer-level consent, contact preference và restriction facts theo accepted policy.

- `lead` và `activity` phải kiểm tra trước sales/outbound actions.
- `marketing` phải kiểm tra trước campaign enrollment và delivery.
- `integration` chỉ vận chuyển/provider-map consent facts theo contract.
- Context consumer không được tự tạo consent truth cạnh tranh hoặc bỏ qua withdrawal.

---

# 47. Contact Preference và Restriction

## 47.1. Preference

* Kênh ưu tiên.
* Giờ liên hệ.
* Ngôn ngữ.
* Người đại diện.
* Tần suất.
* Múi giờ.

## 47.2. Restriction

* Do not call.
* Do not email.
* Do not Zalo.
* No Marketing.
* Chỉ liên hệ qua người đại diện.
* Không liên hệ ngoài giờ.
* Không liên hệ đến ngày cụ thể.
* Restricted by legal request.

## 47.3. Thực thi

`lead`, `activity` và `marketing` Context phải kiểm tra consent/restriction trước khi tạo outbound action.

---

# 48. Customer Risk và Special Handling

## 48.1. Risk Flag

* Identity dispute.
* Shared phone.
* Legal dispute.
* Payment dispute.
* Complaint.
* Contact restriction.
* Fraud suspected.
* Sensitive customer.
* Management attention.
* Data quality issue.

## 48.2. Không dùng một cờ “blacklist” tùy tiện

Mỗi flag phải có:

* Loại.
* Lý do.
* Bằng chứng.
* Người tạo.
* Người duyệt nếu cần.
* Ngày hiệu lực.
* Ngày xem xét lại.
* Visibility.

## 48.3. Risk Flag không tự từ chối dịch vụ

Tùy workflow và authority.

---

# 49. Documents và evidence references

File, Document, Document Version, Verification, Dossier và signature evidence thuộc `documents` Context.

Party Context chỉ giữ logical references hoặc approved projection metadata cần cho Customer workflow, ví dụ:

- Document ID.
- Document type/purpose.
- Customer/Requirement/Financial Profile context.
- Verification summary.
- Effective/expiry state.
- Access-policy reference.
- Hash/evidence reference khi contract cho phép.

Party Context không được:

- Lưu binary trong Customer tables.
- Lưu permanent public URL cho restricted document.
- Ghi đè verified Document Version.
- Tự xác minh legal/financial evidence ngoài authority.
- Sao chép full document metadata rồi trở thành competing source.

---
# 50. Customer creation and linkage workflows

## 50.1. Từ Lead

Cross-context flow phải tuân local transactions và idempotency:

```text
Lead Context
→ request Customer identity resolution
→ Party Context resolves/creates canonical Party-Customer
→ durable result/Event
→ Lead Context links/finalizes conversion
```

Party Context phải:

1. Resolve identity theo accepted policy.
2. Trả masked/existing outcome khi Customer đã tồn tại.
3. Tạo Party/Customer tối thiểu khi đủ điều kiện.
4. Gắn Phone Identity/contact qua identity governance behavior.
5. Tạo Customer Role khi có căn cứ.
6. Lưu origin/source reference cần thiết.
7. Phát durable business fact.
8. Giữ idempotency và concurrency protection.

Lead Context phải:

- Giữ Lead source/attribution.
- Không direct-write Party tables.
- Không tạo Customer duplicate khi retry.
- Reconcile khi result/Event bị chậm hoặc xử lý thất bại.

## 50.2. Direct Create

Direct Create chỉ dành cho actor có permission và business reason.

Phải:

- Resolve identity trước create.
- Kiểm tra organization registry khi là Organization.
- Không bypass duplicate prevention.
- Ghi source/provenance.
- Dùng idempotency cho critical create.
- Audit sensitive identity changes theo policy.

## 50.3. Import

Import phải đi qua staging, validation, identity resolution và canonical Party commands.

Importer không được direct-insert Customer/Phone records.

Legacy migration không thuộc baseline Greenfield nếu chưa có approved migration scope.

## 50.4. Minimal Customer

Minimal Customer có thể chỉ chứa dữ liệu đủ để tạo quan hệ thương mại hợp lệ, ví dụ:

- Party type.
- Display/legal name khi có.
- Canonical contact/identity relationship hoặc pending identity state.
- Source/provenance.
- Lifecycle state phù hợp.
- Origin resource reference.

Exact required fields thuộc Party Context Pack.

---
# 51. Customer Profile Completion

## 51.1. Completeness Score

Có thể tính theo:

* Contact.
* Identity.
* Role.
* Requirement.
* Consent.
* Financial information.
* Stakeholder.
* Address.

## 51.2. Score chỉ hỗ trợ chất lượng dữ liệu

Không dùng để từ chối Customer.

## 51.3. Trường bắt buộc theo stage

Ví dụ:

* Lead stage: phone hoặc contact.
* Requirement: nhu cầu và thời gian.
* Booking: identity và participant.
* Contract: legal fields.

Không bắt buộc đầy đủ từ đầu.

---

# 52. Cập nhật Customer Core

## 52.1. Các thay đổi thông thường

* Tên hiển thị.
* Email.
* Address.
* Preference.
* Role.
* Tag.

## 52.2. Các thay đổi nhạy cảm

* Tên pháp lý.
* Giấy tờ.
* Phone Identity.
* Organization tax code.
* Primary contact.
* Customer type.

Có thể yêu cầu:

* Verification.
* Approval.
* Reason.
* Audit.

## 52.3. Phone thay đổi

Phải gọi Customer Identity Governance Capability.

Không cập nhật trực tiếp trường phone trong Customer.

---

# 53. Archive Customer

## 53.1. Điều kiện

Có thể archive khi:

* Không còn nhu cầu.
* Không có nghiệp vụ active.
* Hồ sơ cũ.
* Data cleanup.

## 53.2. Không archive khi

* Có Deal active.
* Có Booking.
* Có Contract active.
* Có công nợ.
* Có tranh chấp.
* Có Listing active.
* Có legal hold.

## 53.3. Archive không phải delete

Customer vẫn:

* Có thể tìm theo quyền.
* Có lịch sử.
* Có thể restore.

---

# 54. Soft Delete

Chỉ dùng cho:

* Hồ sơ tạo sai.
* Không có nghiệp vụ quan trọng.
* Có approval.

Không được soft delete Customer có:

* Contract.
* Payment.
* Commission.
* Ownership verified.
* Dispute.

Trường hợp trùng Customer phải dùng merge Customer Identity Governance Capability.

---

# 55. Restore Customer

Khi restore:

* Kiểm tra Phone Identity.
* Kiểm tra Customer đã merge.
* Kiểm tra duplicate.
* Kiểm tra active context.
* Ghi reason.
* Ghi audit.

Customer source đã merged không được restore thành hồ sơ độc lập thông thường.

---

# 56. Customer Merge và Redirect

Customer merge, redirect và rebinding thuộc Customer Identity Governance concern trong cùng `party` Context.

Customer 360 phải:

- Hiển thị source Customer là merged/redirected.
- Redirect authorized navigation tới canonical Customer.
- Chặn nghiệp vụ mới trên source record.
- Giữ source attribution và lineage.
- Rebuild/reconcile Customer 360 projections idempotently.
- Không tự cộng gộp Financial Profile, consent, risk hoặc legal facts khi chưa có merge policy.
- Phát durable facts để các Context khác rebind logical references.
- Không hard-delete source Customer.

Merged source không được restore thành independent Customer qua restore workflow thông thường.

---
# 57. Customer và nhiều Legal Entity

## 57.1. Customer identity được quản trị trong enterprise operating boundary

Không tạo Customer khác chỉ vì giao dịch với Legal Entity khác.

## 57.2. Legal Entity Relationship

Lưu:

* Legal Entity đã tiếp xúc.
* Legal Entity có Lead.
* Legal Entity có Requirement.
* Legal Entity có Deal.
* Legal Entity có Contract.

## 57.3. Quyền truy cập

User Legal Entity A không tự xem dữ liệu của Legal Entity B, trừ:

* Customer core tối thiểu được policy cho phép.
* Có context.
* Có Share Grant.
* Có quyền cross-entity.

---

# 58. Customer Responsibility Matrix

Customer 360 có thể hiển thị:

| Context              | Primary responsible | Unit    | Status      |
| -------------------- | ------------------- | ------- | ----------- |
| Buyer Requirement R1 | Sale A              | Team 1  | Active      |
| Seller Objective S1  | Sale B              | Team 2  | Active      |
| Deal D1              | Sale A              | Team 1  | Negotiating |
| Listing L1           | Sale B              | Team 2  | Active      |
| Contract C1          | Finance User C      | Finance | Collecting  |

Không dùng một owner duy nhất.

---

# 59. Temporary Access

Có thể cấp cho:

* Chuyên viên tài chính.
* Pháp chế.
* Quản lý.
* Sale hỗ trợ.
* Kế toán.

Thông qua Identity, Access and Organization Capability:

* Share Grant.
* Temporary Access.
* Delegation.

Phải có:

* Context.
* Trường được xem.
* Thời hạn.
* Reason.
* Approval.

---

# 60. Export Customer

## 60.1. Sale

Không được export Customer hàng loạt.

Có thể tạo tài liệu giới hạn:

* Proposal.
* Customer summary phục vụ giao dịch.
* Contact card của Customer mình phụ trách nếu policy cho phép.

## 60.2. Team Lead và Department Head

Không mặc định có bulk export.

## 60.3. Marketing

Chỉ export segment/aggregate được duyệt và phải tuân thủ consent.

## 60.4. Accounting – Finance

Có thể export dữ liệu phục vụ nghiệp vụ theo scope.

## 60.5. Director

Export có audit và Approval theo policy.

---

# 61. Customer Search

## 61.1. Tìm theo

* Phone.
* Customer code.
* Tên.
* Email.
* External ID.
* Organization tax code.
* Project.
* Requirement.
* Deal.
* Asset/Listing relation.

## 61.2. Search result phải theo quyền

Không trả toàn bộ Customer ngoài scope.

## 61.3. Phone lookup

Phải dùng Customer Identity Governance Capability và anti-enumeration policy.

## 61.4. Search ngoài scope

Có thể trả:

* Masked Customer.
* Exists.
* Request access.
* Link Lead.

Không trả full profile.

---

# 62. Customer 360 API Projection

Endpoint 360 phải hỗ trợ:

* Section-level permission.
* Field-level permission.
* Context filter.
* Legal Entity context.
* Pagination timeline.
* Lazy load.
* Audit sensitive section access.

Không trả toàn bộ hồ sơ tài chính nếu frontend chỉ mở tab Overview.

---

# 63. SLA của Customer 360 Capability

## 63.1. Các loại SLA

* Complete Customer profile.
* Identity verification.
* Requirement qualification.
* Financial document review.
* Seller profile verification.
* Related person confirmation.
* Consent issue resolution.
* Data quality correction.
* Access request.
* Customer dispute.

## 63.2. Cấu hình

Theo:

* Customer segment.
* Requirement type.
* Project.
* Deal stage.
* Legal Entity.
* Priority.
* Financial sensitivity.
* Seller urgency.

## 63.3. Quá SLA

Có thể:

* Nhắc người phụ trách.
* Escalate.
* Tạo Task.
* Đưa dashboard.
* Yêu cầu giải trình.

Không tự:

* Đóng Requirement.
* Xác minh tài chính.
* Tạo Listing.
* Mở rộng quyền truy cập.

---

# 64. Notification

## 64.1. Sale

* Customer Profile thiếu dữ liệu.
* Requirement sắp hết hiệu lực.
* Customer cập nhật nhu cầu.
* Consent thay đổi.
* Related person phản hồi.
* Financial Profile hết hạn.
* Customer được giao/bàn giao.
* Customer có Lead mới cùng context.

## 64.2. Team Lead

* Requirement không có người phụ trách.
* Customer có conflict.
* Financial Profile nhạy cảm bị truy cập bất thường.
* Seller Profile quá SLA.
* Requirement stale.

## 64.3. Finance

* Customer cung cấp tài liệu.
* Financial Profile chờ review.
* Nhu cầu vay.
* Profile hết hạn.

## 64.4. Legal

* Owner document chờ xác minh.
* Representative authority.
* Co-owner chưa xác nhận.
* Risk/legal note.

---

# 65. Cảnh báo và phát hiện bất thường

Hệ thống cần cảnh báo khi:

* Customer không có contact hợp lệ.
* Customer có nhiều primary email.
* Customer type thay đổi bất thường.
* Customer có Phone Identity conflict.
* Customer ngoài scope bị truy cập nhiều lần.
* User xem financial profile hàng loạt.
* Requirement active không có responsible user.
* Nhiều Requirement active trùng context.
* Requirement không có next action.
* Financial Profile không có as-of date.
* Financial Profile hết hạn vẫn được dùng.
* Sale xác minh tài chính vượt quyền.
* Customer đã opt-out vẫn bị liên hệ.
* Related person được liên hệ khi chưa có consent.
* Seller Profile tạo Asset Verification thiếu owner relation.
* Customer archived vẫn có Deal active.
* Customer merged vẫn nhận Lead mới.
* Note pháp lý bị sửa không qua version.
* Nhiều Customer cùng external ID.
* Organization Customer trùng tax code.
* User gắn tag nhạy cảm trái quyền.
* Customer 360 projection không đồng bộ.
* Access context còn hiệu lực sau offboarding.
* Customer bị export bất thường.
* Contact preference bị bỏ qua.
* Requirement budget mâu thuẫn Financial Profile nghiêm trọng.
* Customer có nhiều payer nhưng không xác định primary payer.
* Co-owner chưa xác minh gần thời điểm hợp đồng.

---

# 66. Data Quality Framework

## 66.1. Chỉ số

* Customer có primary contact.
* Customer có type.
* Customer có role.
* Customer có consent.
* Requirement completeness.
* Financial Profile freshness.
* Related person completeness.
* Seller Profile completeness.
* Organization profile completeness.
* Timeline synchronization.

## 66.2. Data Quality Rule

Ví dụ:

* Requirement BUY phải có budget range.
* Seller Objective phải có property location.
* Organization Customer phải có legal name.
* Contract-ready Customer phải có identity verification.

## 66.3. Không auto-fix dữ liệu nhạy cảm

Không tự sửa:

* Phone.
* Legal name.
* Identity document.
* Income.
* Ownership.
* Representative authority.

---

# 67. AI hỗ trợ Customer 360

Có thể hỗ trợ:

* Tóm tắt timeline.
* Gợi ý Requirement.
* Trích xuất tiêu chí từ note.
* Gợi ý stakeholder.
* Phát hiện thiếu dữ liệu.
* Gợi ý next action.
* So sánh nhu cầu và tài chính.

AI không được:

* Tự thay đổi Customer core.
* Tự xác minh tài chính.
* Tự xác nhận ownership.
* Tự từ chối Customer.
* Tự tạo risk flag nghiêm trọng không có review.
* Mở rộng quyền truy cập.

Mọi gợi ý cần có confidence và nguồn.

---

# 68. Candidate user experiences

> Đây là product interaction inventory. Exact routes, page hierarchy, components và layouts thuộc Navigation/IA, Design System, Frontend contracts và Sprint Pack.


## 68.1. Customer List

Bộ lọc:

* Type.
* Role.
* Status.
* Segment.
* Legal Entity relation.
* Requirement.
* Project.
* Responsible user.
* Financial readiness.
* Seller/Owner.
* Consent.
* Last interaction.
* Data quality.
* Risk.

## 68.2. Customer 360

Các tab:

1. Overview.
2. Identity & Contact.
3. Roles.
4. Leads.
5. Requirements.
6. Financial Profile.
7. Seller/Owner Profile.
8. Relationships & Influencers.
9. Assets & Listings.
10. Matching & Proposals.
11. Deals.
12. Bookings & Contracts.
13. Payments & Debt.
14. Notes.
15. Timeline.
16. Consent.
17. Access & Responsibilities.
18. Documents.
19. Audit.

## 68.3. Requirement Workspace

* Requirement type.
* Criteria.
* Budget.
* Geography.
* Financial link.
* Stakeholders.
* Responsibility.
* Matching readiness.
* History.

## 68.4. Financial Profile Workspace

* Summary.
* Income.
* Capital.
* Obligations.
* Assets.
* Loan need.
* Verification.
* Documents.
* Access log.

## 68.5. Seller/Owner Workspace

* Objective.
* Declared assets.
* Ownership claims.
* Co-owners.
* Legal summary.
* Verification.
* Asset Verification link.
* Listing Acquisition link.

## 68.6. Relationship Map

Hiển thị đồ thị:

* Customer.
* Related parties.
* Role.
* Influence.
* Attitude.
* Requirement/Deal context.

## 68.7. Customer Access Explanation

Hiển thị:

* User được xem vì lý do gì.
* Context nào.
* Trường nào bị mask.
* Quyền hết hạn khi nào.

---

# 69. Candidate dashboard outcomes cho Sale

* Customer active.
* Customer mới.
* Profile chưa hoàn thiện.
* Requirement active.
* Requirement thiếu dữ liệu.
* Customer cần follow-up.
* Financial Profile cần cập nhật.
* Seller Objective mới.
* Related person cần xác nhận.
* Consent sắp hết hạn.
* Requirement sắp hết protection.

---

# 70. Candidate dashboard outcomes cho Team Lead

* Customer theo team.
* Requirement theo stage.
* Customer không có responsible user.
* Requirement stale.
* Profile completeness.
* Financial readiness.
* Seller pipeline.
* Customer multi-context.
* Access conflicts.
* Consent risk.
* Handover Customer.

---

# 71. Candidate dashboard outcomes cho Director

* Tổng Customer.
* New vs returning.
* Buyer/Seller/Owner mix.
* Customer theo Legal Entity.
* Customer theo segment.
* Active Requirements.
* Seller inventory pipeline.
* Financial readiness distribution.
* Multi-project Customer.
* Customer lifetime activity.
* Customer conversion.
* Data quality.
* Consent compliance.
* Customer access risk.

---

# 72. Candidate reporting outcomes

> Exact metrics, grains, formulas, drill-down contracts và certification thuộc Analytics Metric Registry và Analytics Context contracts.


* Customer master.
* Customer type.
* Customer role.
* Customer lifecycle.
* New/returning Customer.
* Customer by source.
* Customer by Legal Entity.
* Customer by sale/team/department.
* Customer by project.
* Requirement type.
* Requirement stage.
* Requirement aging.
* Requirement completeness.
* Buyer budget.
* Seller objective.
* Owner profile.
* Declared asset.
* Financial readiness.
* Financial Profile freshness.
* Borrowing need.
* Stakeholder and influencer.
* Customer relationship.
* Consent.
* Contact restriction.
* Customer access relationship.
* Temporary access.
* Customer data quality.
* Archived Customer.
* Customer with active Deal.
* Customer with multiple roles.
* Customer multi-project.
* Customer without next action.
* Customer timeline activity.
* Customer export log.

Mọi báo cáo phải drill-down đúng scope.

---

# 73. Candidate data model — đầu vào thiết kế, không phải physical schema canonical

> **Classification:** `CONTEXT-SPECIFIC DESIGN INPUT / PENDING VALIDATION`  
> Exact tables, columns, constraints, indexes, schema ownership và migrations chỉ có hiệu lực khi được khóa trong Party Context DB Specification và Alembic. Cross-context IDs là logical references; tài liệu này không mặc định cross-schema foreign keys.


## 73.1. Party

### `parties`

* `id`
* `party_code`
* `party_type`
* `status`
* `created_at`
* `updated_at`

### `party_individual_profiles`

* `party_id`
* `full_name`
* `display_name`
* `date_of_birth`
* `gender_code`
* `nationality_code`
* `preferred_language`
* `occupation`
* `job_title`
* `employer_name`
* `verification_status`
* `updated_at`

### `party_organization_profiles`

* `party_id`
* `legal_name`
* `trade_name`
* `organization_type`
* `tax_code`
* `registration_number`
* `country_code`
* `registered_address_id`
* `website`
* `industry_code`
* `verification_status`
* `updated_at`

---

## 73.2. Customer

### `customers`

* `id`
* `customer_code`
* `enterprise_id`
* `party_id`
* `customer_type`
* `lifecycle_status`
* `engagement_summary`
* `profile_completeness_score`
* `primary_legal_entity_relationship_id`
* `first_lead_id`
* `first_source_snapshot_id`
* `created_from_type`
* `created_from_id`
* `status`
* `created_at`
* `updated_at`
* `archived_at`
* `merged_into_customer_id`
* `version`

### `customer_status_history`

* `id`
* `customer_id`
* `from_status`
* `to_status`
* `reason`
* `source_type`
* `source_id`
* `changed_by`
* `created_at`

### `customer_external_ids`

* `id`
* `customer_id`
* `namespace`
* `external_id`
* `source_system`
* `status`
* `effective_from`
* `effective_to`
* `created_at`

---

## 73.3. Customer Role

### `customer_roles`

* `id`
* `customer_id`
* `role_code`
* `context_type`
* `context_id`
* `verification_status`
* `effective_from`
* `effective_to`
* `source_type`
* `source_id`
* `status`
* `created_by`
* `created_at`

---

## 73.4. Email, Social và Address

### `customer_emails`

* `id`
* `customer_id`
* `raw_email`
* `normalized_email`
* `email_type`
* `is_primary`
* `verification_status`
* `consent_status`
* `status`
* `effective_from`
* `effective_to`
* `source_type`
* `source_id`
* `created_at`

### `customer_social_accounts`

* `id`
* `customer_id`
* `platform_code`
* `account_identifier`
* `profile_url`
* `is_primary`
* `verification_status`
* `status`
* `source_type`
* `source_id`
* `created_at`

### `customer_addresses`

* `id`
* `customer_id`
* `address_type`
* `country_code`
* `province_code`
* `district_code`
* `ward_code`
* `street`
* `address_line`
* `latitude`
* `longitude`
* `verification_status`
* `is_primary`
* `effective_from`
* `effective_to`
* `status`
* `created_at`

---

## 73.5. Legal Entity Relationship

### `customer_legal_entity_relationships`

* `id`
* `customer_id`
* `legal_entity_id`
* `relationship_type`
* `first_interaction_at`
* `last_interaction_at`
* `status`
* `created_at`

---

## 73.6. Segment và Tag

### `customer_segments`

* `id`
* `customer_id`
* `segment_code`
* `segment_source`
* `rule_version`
* `effective_from`
* `effective_to`
* `status`
* `created_at`

### `customer_tags`

* `id`
* `customer_id`
* `tag_code`
* `visibility_scope`
* `created_by`
* `created_at`
* `removed_at`

---

## 73.7. Requirement

### `customer_requirements`

* `id`
* `requirement_code`
* `customer_id`
* `legal_entity_id`
* `requirement_type`
* `purpose_code`
* `status`
* `priority`
* `currency`
* `budget_min`
* `budget_target`
* `budget_max`
* `budget_flexibility`
* `desired_start_at`
* `desired_completion_at`
* `timeline_code`
* `financial_profile_id`
* `primary_responsible_user_id`
* `source_lead_id`
* `care_context_id`
* `matching_readiness_status`
* `created_at`
* `updated_at`
* `completed_at`
* `version`

### `customer_requirement_history`

* `id`
* `requirement_id`
* `version`
* `snapshot_json`
* `change_reason`
* `changed_by`
* `created_at`

### `requirement_projects`

* `id`
* `requirement_id`
* `project_id`
* `preference_level`
* `status`
* `created_at`

### `requirement_property_types`

* `id`
* `requirement_id`
* `property_type_code`
* `preference_level`
* `created_at`

### `requirement_geographies`

* `id`
* `requirement_id`
* `geography_type`
* `geography_code`
* `radius_km`
* `preference_level`
* `created_at`

### `requirement_criteria`

* `id`
* `requirement_id`
* `criterion_code`
* `criterion_type`
* `operator_code`
* `value_json`
* `importance_level`
* `weight`
* `status`
* `created_at`

### `requirement_responsibilities`

* `id`
* `requirement_id`
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

---

## 73.8. Seller và Owner Profile

### `customer_seller_profiles`

* `id`
* `customer_id`
* `status`
* `seller_type`
* `default_urgency`
* `preferred_engagement_type`
* `general_notes`
* `created_at`
* `updated_at`

### `seller_objectives`

* `id`
* `seller_profile_id`
* `customer_id`
* `requirement_id`
* `declared_asset_id`
* `objective_type`
* `asking_price`
* `minimum_expected_price`
* `currency`
* `selling_reason_code`
* `urgency_level`
* `desired_sale_at`
* `exclusive_preference`
* `fee_expectation_json`
* `legal_summary`
* `mortgage_status`
* `co_owner_status`
* `survey_readiness`
* `status`
* `created_at`
* `updated_at`

### `customer_declared_assets`

* `id`
* `customer_id`
* `asset_type`
* `project_id`
* `address_text`
* `parcel_number`
* `map_sheet_number`
* `declared_area`
* `declared_ownership_percentage`
* `ownership_claim_type`
* `verification_status`
* `verified_asset_id`
* `source_type`
* `source_id`
* `created_at`
* `updated_at`

### `declared_asset_owners`

* `id`
* `declared_asset_id`
* `party_id`
* `customer_id`
* `relationship_type`
* `declared_percentage`
* `verification_status`
* `created_at`

---

## 73.9. Financial Profile

### `financial_profiles`

* `id`
* `customer_id`
* `profile_scope_type`
* `profile_scope_id`
* `profile_type`
* `status`
* `currency`
* `as_of_date`
* `valid_until`
* `verification_level`
* `readiness_status`
* `readiness_rule_version`
* `summary_json`
* `created_by`
* `reviewed_by`
* `verified_by`
* `created_at`
* `updated_at`
* `version`

### `financial_income_sources`

* `id`
* `financial_profile_id`
* `income_type`
* `amount`
* `currency`
* `frequency`
* `stability_level`
* `effective_from`
* `effective_to`
* `verification_status`
* `source_document_id`
* `created_at`

### `financial_capital_sources`

* `id`
* `financial_profile_id`
* `capital_type`
* `amount`
* `currency`
* `availability_date`
* `verification_status`
* `created_at`

### `financial_obligations`

* `id`
* `financial_profile_id`
* `obligation_type`
* `outstanding_amount`
* `monthly_payment`
* `currency`
* `maturity_date`
* `verification_status`
* `created_at`

### `financial_declared_assets`

* `id`
* `financial_profile_id`
* `asset_type`
* `estimated_value`
* `currency`
* `liquidity_level`
* `verification_status`
* `related_property_asset_id`
* `created_at`

### `financial_borrowing_needs`

* `id`
* `financial_profile_id`
* `requested_amount`
* `currency`
* `loan_term_months`
* `target_monthly_payment`
* `preferred_bank_party_id`
* `preapproval_status`
* `preapproval_amount`
* `valid_until`
* `created_at`

### `financial_profile_verification_events`

* `id`
* `financial_profile_id`
* `verification_type`
* `from_status`
* `to_status`
* `evidence_document_id`
* `verified_by`
* `reason`
* `created_at`

---

## 73.10. Relationship Graph

### `customer_relationships`

* `id`
* `source_party_id`
* `target_party_id`
* `relationship_code`
* `inverse_relationship_code`
* `context_type`
* `context_id`
* `verification_status`
* `effective_from`
* `effective_to`
* `source_type`
* `source_id`
* `status`
* `created_by`
* `created_at`

### `related_party_stubs`

* `id`
* `customer_id`
* `display_name`
* `relationship_code`
* `role_summary`
* `phone_raw`
* `email_raw`
* `consent_status`
* `converted_party_id`
* `converted_customer_id`
* `status`
* `created_at`

### `customer_stakeholders`

* `id`
* `customer_id`
* `party_id`
* `related_party_stub_id`
* `context_type`
* `context_id`
* `stakeholder_role`
* `influence_level`
* `attitude`
* `decision_authority_level`
* `financial_contribution_percentage`
* `contact_permission`
* `status`
* `created_at`
* `updated_at`

---

## 73.11. Note và Timeline

### `customer_notes`

* `id`
* `customer_id`
* `context_type`
* `context_id`
* `note_type`
* `content`
* `visibility_scope`
* `is_important`
* `is_locked`
* `version`
* `created_by`
* `created_at`
* `updated_at`
* `archived_at`

### `customer_note_versions`

* `id`
* `customer_note_id`
* `version`
* `content`
* `change_reason`
* `changed_by`
* `created_at`

### `customer_timeline_projection_items`

* `id`
* `customer_id`
* `event_type`
* `source_context`
* `source_resource_type`
* `source_resource_id`
* `context_type`
* `context_id`
* `summary`
* `visibility_scope`
* `actor_user_id`
* `occurred_at`
* `created_at`
* `event_version`

---

## 73.12. Consent và Contact Preference

### `customer_consents`

* `id`
* `customer_id`
* `consent_type`
* `purpose_code`
* `channel_code`
* `status`
* `consent_text_version`
* `source_type`
* `source_id`
* `evidence_url`
* `granted_at`
* `expires_at`
* `withdrawn_at`
* `created_at`

### `customer_contact_preferences`

* `id`
* `customer_id`
* `preferred_channel`
* `preferred_language`
* `timezone`
* `preferred_time_ranges_json`
* `frequency_policy`
* `representative_party_id`
* `effective_from`
* `effective_to`
* `status`
* `created_at`

### `customer_contact_restrictions`

* `id`
* `customer_id`
* `restriction_type`
* `channel_code`
* `reason`
* `source_type`
* `source_id`
* `effective_from`
* `effective_to`
* `status`
* `approved_by`
* `created_at`

---

## 73.13. Document References

### `customer_document_references`

* `id`
* `customer_id`
* `context_type`
* `context_id`
* `document_id`
* `document_type`
* `verification_summary`
* `access_policy_reference`
* `effective_from`
* `expires_at`
* `projection_freshness_at`
* `created_at`

---

## 73.14. Access Projection

### `customer_access_contexts`

* `id`
* `customer_id`
* `user_id`
* `source_type`
* `source_id`
* `context_type`
* `context_id`
* `access_level_code`
* `field_policy_id`
* `effective_from`
* `effective_to`
* `status`
* `last_recalculated_at`

Đây là projection tối ưu query, không phải nguồn chân lý độc lập.

---

# 74. Candidate application operations — không phải OpenAPI canonical

> Danh sách dưới đây là capability operation inventory. Exact paths, methods, payloads, errors, concurrency headers và authorization metadata thuộc OpenAPI.


## Customer

```text
GET    /customers
POST   /customers
GET    /customers/{id}
PATCH  /customers/{id}
GET    /customers/{id}/360
GET    /customers/{id}/summary
POST   /customers/{id}/archive
POST   /customers/{id}/restore
POST   /customers/{id}/soft-delete-request
GET    /customers/{id}/access-explanation
```

## Contact

```text
GET    /customers/{id}/phones
POST   /customers/{id}/phones
PATCH  /customer-phones/{id}
POST   /customer-phones/{id}/set-primary

GET    /customers/{id}/emails
POST   /customers/{id}/emails
PATCH  /customer-emails/{id}

GET    /customers/{id}/addresses
POST   /customers/{id}/addresses
PATCH  /customer-addresses/{id}

GET    /customers/{id}/social-accounts
POST   /customers/{id}/social-accounts
```

Phone endpoints phải proxy hoặc gọi service Customer Identity Governance Capability.

## Customer Role

```text
GET    /customers/{id}/roles
POST   /customers/{id}/roles
PATCH  /customer-roles/{id}
POST   /customer-roles/{id}/end
```

## Requirement

```text
GET    /customers/{id}/requirements
POST   /customers/{id}/requirements
GET    /requirements/{id}
PATCH  /requirements/{id}
POST   /requirements/{id}/activate
POST   /requirements/{id}/pause
POST   /requirements/{id}/complete
POST   /requirements/{id}/cancel
GET    /requirements/{id}/history

POST   /requirements/{id}/criteria
PATCH  /requirement-criteria/{id}
DELETE /requirement-criteria/{id}

POST   /requirements/{id}/responsibilities
POST   /requirement-responsibilities/{id}/end
```

## Financial Profile

```text
GET    /customers/{id}/financial-profiles
POST   /customers/{id}/financial-profiles
GET    /financial-profiles/{id}
PATCH  /financial-profiles/{id}
POST   /financial-profiles/{id}/submit-review
POST   /financial-profiles/{id}/verify
POST   /financial-profiles/{id}/expire
POST   /financial-profiles/{id}/calculate-readiness

POST   /financial-profiles/{id}/income-sources
POST   /financial-profiles/{id}/capital-sources
POST   /financial-profiles/{id}/obligations
POST   /financial-profiles/{id}/declared-assets
POST   /financial-profiles/{id}/borrowing-needs
```

## Seller/Owner

```text
GET    /customers/{id}/seller-profile
POST   /customers/{id}/seller-profile

GET    /customers/{id}/seller-objectives
POST   /customers/{id}/seller-objectives
PATCH  /seller-objectives/{id}
POST   /seller-objectives/{id}/asset-verification-request

GET    /customers/{id}/declared-assets
POST   /customers/{id}/declared-assets
PATCH  /declared-assets/{id}
POST   /declared-assets/{id}/submit-verification
```

## Relationship và Stakeholder

```text
GET    /customers/{id}/relationships
POST   /customers/{id}/relationships
PATCH  /customer-relationships/{id}
POST   /customer-relationships/{id}/end

GET    /customers/{id}/stakeholders
POST   /customers/{id}/stakeholders
PATCH  /customer-stakeholders/{id}

POST   /customers/{id}/related-party-stubs
POST   /related-party-stubs/{id}/convert-to-customer
```

## Notes và Timeline

```text
GET    /customers/{id}/notes
POST   /customers/{id}/notes
PATCH  /customer-notes/{id}
POST   /customer-notes/{id}/archive
GET    /customer-notes/{id}/versions

GET    /customers/{id}/timeline
GET    /customers/{id}/timeline/summary
```

## Consent

```text
GET    /customers/{id}/consents
POST   /customers/{id}/consents
POST   /customer-consents/{id}/withdraw

GET    /customers/{id}/contact-preferences
PUT    /customers/{id}/contact-preferences

GET    /customers/{id}/contact-restrictions
POST   /customers/{id}/contact-restrictions
POST   /customer-contact-restrictions/{id}/end
```

Backend phải tự enforce:

* Authenticated user.
* Legal Entity context.
* Customer access context.
* Permission.
* Scope.
* Field policy.
* Consent.
* Workflow.
* Approval.
* Requirement responsibility.
* Version.
* Idempotency.
* Phone Identity service.

---

# 75. Candidate permission vocabulary — không phải Permission Registry canonical

> Exact permission codes, scopes, role mappings, masking và SoD rules thuộc security registries/matrices. Các mã dưới đây chỉ là đầu vào đặt tên.


## Customer Core

```text
customer.view
customer.view_summary
customer.view_sensitive
customer.create
customer.update
customer.archive
customer.restore
customer.soft_delete_request
customer.view_audit
customer.export
```

## Identity và Contact

```text
customer.identity.view
customer.identity.view_full
customer.identity.update
customer.phone.view
customer.phone.view_full
customer.phone.add
customer.phone.correct
customer.phone.set_primary

customer.email.view
customer.email.manage
customer.address.view
customer.address.manage
customer.social.view
customer.social.manage
```

## Customer Role và Segment

```text
customer.role.view
customer.role.manage
customer.segment.view
customer.segment.manage
customer.tag.view
customer.tag.manage
customer.tag.manage_sensitive
```

## Requirement

```text
customer_requirement.view
customer_requirement.create
customer_requirement.update
customer_requirement.assign
customer_requirement.activate
customer_requirement.pause
customer_requirement.complete
customer_requirement.cancel
customer_requirement.view_history
```

## Financial Profile

```text
customer_financial.view_summary
customer_financial.view_detail
customer_financial.create
customer_financial.update
customer_financial.submit_review
customer_financial.review
customer_financial.verify
customer_financial.calculate_readiness
customer_financial.view_documents
customer_financial.export
```

## Seller/Owner

```text
customer_seller.view
customer_seller.create
customer_seller.update
customer_owner.view
customer_owner.create_claim
customer_owner.update_claim
customer_owner.submit_verification
customer_owner.view_legal_summary
```

## Relationship và Stakeholder

```text
customer_relationship.view
customer_relationship.create
customer_relationship.update
customer_relationship.end

customer_stakeholder.view
customer_stakeholder.manage
customer_related_party.convert
```

## Note và Timeline

```text
customer_note.view
customer_note.create
customer_note.update
customer_note.archive
customer_note.view_private
customer_note.view_finance
customer_note.view_legal

customer_timeline.view
customer_timeline.view_company
customer_timeline.view_sensitive
```

## Consent

```text
customer_consent.view
customer_consent.create
customer_consent.withdraw
customer_contact_preference.manage
customer_contact_restriction.view
customer_contact_restriction.manage
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

# 76. Phân quyền theo vai trò

## 76.1. Sale

Được:

* Xem Customer trong context của mình.
* Xem contact theo field policy.
* Tạo/update Requirement được giao.
* Cập nhật Seller Objective.
* Ghi note sales.
* Quản lý stakeholder trong context.
* Xem Financial Readiness summary.
* Gửi yêu cầu review tài chính.

Không mặc định được:

* Xem toàn bộ Financial Profile.
* Xem context khác.
* Export hàng loạt.
* Xem note Finance/Legal.
* Sửa Customer identity nhạy cảm không qua workflow.
* Merge Customer.

## 76.2. Team Lead

Được:

* Xem Customer team.
* Phân Requirement.
* Kiểm tra completeness.
* Theo dõi stakeholder.
* Xử lý conflict trong team.
* Xem Financial summary theo quyền.

## 76.3. Department Head

Được:

* Scope department.
* Xử lý tranh chấp context.
* Phê duyệt ngoại lệ.
* Xem pipeline Requirement.

## 76.4. Marketing

Được:

* Xem segment.
* Consent Marketing.
* Attribution.
* Aggregate Requirement.

Không mặc định xem:

* Full phone.
* Financial detail.
* Contract.
* Legal note.
* Seller legal documents.

## 76.5. Accounting – Finance

Được xem Customer liên quan giao dịch được giao.

Quyền tập trung:

* Identity cần cho chứng từ.
* Payer.
* Financial documents liên quan.
* Contact thanh toán.
* Công nợ.

Không mặc định xem toàn bộ sales notes.

## 76.6. Legal

Được:

* Legal identity.
* Owner/representative.
* Legal documents.
* Legal notes.
* Contract participant context.

## 76.7. Director

Được `all` theo scope đã cấp, với field permission và audit phù hợp.

---

# 77. Candidate business facts — không phải Event contract canonical

> Exact Event names, envelope, payload, versions và channels thuộc Event Registry, JSON Schema và AsyncAPI. Producer/consumer phải idempotent theo Event Standards.


Customer 360 Capability phát:

```text
party.created
customer.created
customer.updated
customer.role_added
customer.role_ended
customer.archived
customer.restored

customer.email_added
customer.address_added
customer.contact_preference_changed
customer.contact_restriction_added
customer.consent_granted
customer.consent_withdrawn

requirement.created
requirement.activated
requirement.updated
requirement.matching_ready
requirement.completed
requirement.cancelled
requirement.responsibility_changed

financial_profile.created
financial_profile.updated
financial_profile.submitted
financial_profile.verified
financial_profile.expired
financial_readiness_changed

seller_profile.created
seller_objective.created
seller_objective.updated
declared_asset.created
declared_asset.verification_requested

customer.relationship_added
customer.relationship_ended
customer.stakeholder_added
related_party.converted

customer.note_created
customer.note_updated
customer.risk_flag_added
```

Consumer phải idempotent.

---

# 78. Candidate configuration dependencies

> Các keys dưới đây là capability inventory. Exact Configuration Definitions, schemas, scopes, resolution strategies và versions thuộc Platform Context contracts.


```text
customer.default_workflow
customer.archive_workflow
customer.restore_workflow
customer_profile.completeness_policy

customer_role.dictionary
customer_segment.rule_set
customer_tag.policy

requirement.default_workflow
requirement.buyer_workflow
requirement.seller_workflow
requirement.duplicate_policy
requirement.matching_readiness_policy
requirement.sla_policy

financial_profile.workflow
financial_profile.verification_policy
financial_profile.expiration_policy
financial_readiness.rule_set
financial_profile.field_access_policy

seller_profile.workflow
owner_claim.verification_policy
related_party.conversion_policy

customer_note.visibility_policy
customer_note.versioning_policy
customer_timeline.visibility_policy

customer_consent.policy
customer_contact_restriction_policy
customer_data_retention_policy
customer_export_approval_policy
```

Tất cả phải có scope, version và ngày hiệu lực.

---

# 79. System invariant

Các quy tắc sau không được cấu hình tắt:

1. Customer ID dùng chung toàn Enterprise.
2. Không tạo Customer mới khi Phone Identity đã thuộc Customer hiện hữu trái rule.
3. Customer cá nhân duplicate được xác định theo Phone Identity Customer Identity Governance Capability.
4. Customer không có owner sale vĩnh viễn.
5. Backend phải enforce Customer access context.
6. Field nhạy cảm không được gửi ngoài quyền.
7. Customer Role không tự cấp permission.
8. Requirement và Deal là hai thực thể khác nhau.
9. Seller Objective không tự tạo Listing active.
10. Declared Ownership không được coi là verified ownership.
11. Financial Profile không được tự kết luận tín dụng ngân hàng.
12. Financial Readiness không được tự từ chối Customer.
13. Consent withdrawal phải được thực thi.
14. Customer merged source không nhận nghiệp vụ mới.
15. Customer có giao dịch tài chính không được xóa cứng.
16. Notes pháp lý/tài chính quan trọng không được sửa mất lịch sử.
17. Timeline event nguồn không được giả mạo.
18. Access ngoài Legal Entity context phải được kiểm tra.
19. Export không được suy ra từ quyền View.
20. Related Party chưa được identity check không được tự trở thành Customer chính thức.

---

# 80. Rule nghiệp vụ bắt buộc

1. Customer là hồ sơ dùng chung trong enterprise operating boundary.
2. Customer không thuộc sở hữu vĩnh viễn của sale.
3. Một Party chỉ có một Customer chính trong Enterprise.
4. Một Customer có thể có nhiều Lead.
5. Một Customer có thể có nhiều Requirement.
6. Một Customer có thể vừa Buyer vừa Seller.
7. Customer Role có thể đồng thời tồn tại.
8. Role phải có context và ngày hiệu lực khi cần.
9. Customer Status không thay Lead/Deal Status.
10. Customer 360 không sao chép nguồn dữ liệu Context khác.
11. Phone được quản lý qua Customer Identity Governance Capability.
12. Customer 360 Capability không tự ghi normalized phone.
13. Customer cá nhân duplicate không dùng email/tên/địa chỉ.
14. Organization Customer có duplicate registry riêng.
15. Contact cũ không được xóa khi thay đổi.
16. Chỉ có một primary contact active theo loại mặc định.
17. Customer ngoài scope phải được mask.
18. Search không được dùng để dò Customer trái phép.
19. Customer code không dùng xác định duplicate.
20. Requirement không phải Lead.
21. Requirement không phải Deal.
22. Requirement phải có type.
23. Requirement active phải có responsible context.
24. Không tự merge Requirement.
25. Duplicate active Requirement phải được cảnh báo.
26. Nhiều Requirement được phép nếu khác mục tiêu/context.
27. Criteria phải có cấu trúc.
28. Criteria phải có mức độ quan trọng.
29. Matching không dựa chỉ vào note tự do.
30. Budget phải có currency.
31. Budget range phải phân biệt min/target/max.
32. Seller Objective không phải Listing.
33. Seller Objective phải liên kết Customer.
34. Declared Asset không phải Property Asset verified.
35. Ownership claim phải có verification status.
36. Co-owner phải được quản lý riêng.
37. Land Owner Profile không tự tạo Project.
38. Financial Profile có thể theo Customer hoặc context.
39. Restricted Financial Profile không tự chia sẻ.
40. Customer có quyền từ chối cung cấp tài chính.
41. Từ chối tài chính không tự làm Customer unqualified.
42. Financial Profile phải có as-of date.
43. Financial Profile có thể hết hiệu lực.
44. Sale không tự xác minh mức tài chính cao.
45. Financial Readiness chỉ là hỗ trợ.
46. Affordability Snapshot phải lưu version.
47. Matching lịch sử không dùng dữ liệu tài chính mới âm thầm.
48. Related Person không bắt buộc là Customer.
49. Related Person chuyển Customer phải identity check.
50. Relationship phải có hướng.
51. Stakeholder role phải theo context.
52. Người ảnh hưởng không tự có quyền truy cập.
53. Người thanh toán và người sở hữu là hai vai trò khác nhau.
54. Ownership ratio dự kiến không phải tỷ lệ hợp đồng chính thức.
55. Customer Context phải xác định rõ.
56. User chỉ xem context được phép.
57. Customer 360 phải giải thích nguồn quyền.
58. Customer access projection không phải nguồn chân lý duy nhất.
59. Timeline phải giữ source reference.
60. Timeline visibility phải được backend enforce.
61. Private note không dùng để che dữ liệu bắt buộc bàn giao.
62. Financial/Legal note quan trọng phải có version.
63. Consent phải theo mục đích và kênh.
64. Sales consent không mặc định là Marketing consent.
65. Opt-out phải chặn outbound tương ứng.
66. Contact restriction có ngày hiệu lực.
67. Risk flag phải có reason.
68. Không dùng blacklist tùy tiện.
69. Risk flag không tự từ chối dịch vụ nếu chưa có workflow.
70. Customer create trực tiếp vẫn phải duplicate check.
71. Import vẫn phải duplicate check.
72. Customer tối thiểu có thể được tạo từ Lead hợp lệ.
73. Customer Profile không cần hoàn thiện toàn bộ ngay.
74. Trường bắt buộc thay đổi theo stage.
75. Customer archive không được có nghiệp vụ active trái rule.
76. Customer archive không phải delete.
77. Customer restore phải duplicate check.
78. Customer merged source không được restore thông thường.
79. Customer dùng chung Enterprise, không tạo lại theo Legal Entity.
80. Legal Entity A không tự xem context của B.
81. Temporary Access phải có thời hạn.
82. Project Access không tự mở Customer context.
83. Listing Access không tự mở Financial Profile.
84. View không đồng nghĩa Export.
85. Sale không được bulk export Customer.
86. Marketing không được xem tài chính chi tiết.
87. Accounting chỉ xem Customer giao dịch liên quan.
88. Backend phải enforce scope ở query layer.
89. Không tải toàn Customer rồi lọc frontend.
90. AI không tự sửa Customer core.
91. AI không tự xác minh ownership.
92. AI không tự xác minh tài chính.
93. AI gợi ý phải có confidence và source.
94. Customer đã converted từ Lead phải giữ attribution.
95. Requirement tạo từ Lead phải giữ source Lead.
96. Handover Customer chỉ chuyển responsibility context.
97. Handover không đổi Customer core.
98. Handover không tự chuyển commission.
99. User offboard không làm mất Customer history.
100. Audit Customer không được sửa.

---

# 81. Audit log

## 81.1. Thao tác bắt buộc

* Tạo Customer.
* Link Lead.
* Update Customer core.
* Add/end Customer Role.
* Add/update contact.
* Change primary contact.
* Create/update Requirement.
* Change responsibility.
* Update criteria.
* Create/update Financial Profile.
* View sensitive financial data theo policy.
* Verify Financial Profile.
* Create Seller Objective.
* Create ownership claim.
* Add relationship.
* Add stakeholder.
* Convert Related Party.
* Create/update note.
* Change consent.
* Add restriction.
* Archive/restore.
* Export.
* Access Customer ngoài context thông thường.

## 81.2. Nội dung

* Actor.
* Customer.
* Party.
* Legal Entity.
* Context.
* Permission.
* Field policy.
* Before.
* After.
* Reason.
* Approval.
* Source Lead.
* Requirement.
* IP.
* Device.
* Request ID.
* Correlation ID.
* Timestamp.
* Result.

---

# 82. Phạm vi MVP

## 82.1. Bắt buộc

* Individual Customer.
* Organization Customer cơ bản.
* Party và Customer.
* Customer code.
* Customer lifecycle status.
* Customer Role.
* Email.
* Address.
* Social account.
* Phone integration Customer Identity Governance Capability.
* Customer 360 Summary.
* Customer List.
* Buyer Requirement.
* Seller/Consignment Requirement.
* Budget.
* Geography.
* Project preference.
* Property type.
* Structured criteria.
* Requirement responsibility.
* Financial Profile cơ bản.
* Income.
* Capital.
* Obligation.
* Borrowing need.
* Financial Readiness summary.
* Seller Profile.
* Declared Asset.
* Ownership claim.
* Related Party Stub.
* Relationship.
* Stakeholder.
* Notes.
* Timeline.
* Consent.
* Contact Preference.
* Contact Restriction.
* Scope.
* Field masking.
* Archive/restore.
* Audit.
* Domain event.
* Lead conversion integration.

## 82.2. Giai đoạn nâng cao

* Organization hierarchy Customer.
* Advanced household graph.
* AI summary.
* AI criterion extraction.
* Advanced affordability.
* Bank pre-approval integration.
* Customer portal.
* Customer self-update.
* Document eKYC.
* Dynamic segmentation.
* Data clean room Marketing.
* Relationship graph visualization nâng cao.
* Customer lifetime value.
* Churn prediction.
* Customer identity federation.
* Advanced risk management.
* Multi-currency Financial Profile.
* Privacy request workflow.

---

# 83. Tiêu chí nghiệm thu

Capability được xem là đạt khi:

1. Tạo được Individual Customer.
2. Tạo được Organization Customer.
3. Customer có Party ID.
4. Customer có Customer Code.
5. Customer Code không đổi.
6. Customer dùng chung trong enterprise operating boundary.
7. Không tạo lại Customer theo Legal Entity.
8. Customer có nhiều Legal Entity relationship.
9. Customer có nhiều role.
10. Customer vừa Buyer vừa Seller được.
11. Role có ngày hiệu lực.
12. Role không tự mở permission.
13. Customer Status hoạt động.
14. Customer Status không thay Deal Status.
15. Tạo Customer từ Lead được.
16. Giữ source Lead.
17. Giữ attribution.
18. Direct Create vẫn duplicate check.
19. Import vẫn duplicate check.
20. Phone gọi đúng Customer Identity Governance Capability.
21. Không tự ghi normalized phone.
22. Email có nhiều bản ghi.
23. Chỉ một primary email active mặc định.
24. Address có nhiều loại.
25. Social account được lưu.
26. Contact cũ được inactivate thay vì xóa.
27. Customer ngoài scope được mask.
28. Search ngoài scope không lộ thông tin.
29. Tạo được Buyer Requirement.
30. Tạo được Seller Requirement.
31. Tạo được Investment Requirement.
32. Requirement có status.
33. Requirement có responsible user.
34. Requirement có source Lead.
35. Requirement có budget range.
36. Requirement có currency.
37. Requirement có geography.
38. Requirement có project preference.
39. Requirement có property type.
40. Requirement có structured criteria.
41. Criteria có importance level.
42. Criteria có Not Acceptable.
43. Duplicate Requirement được cảnh báo.
44. Không tự merge Requirement.
45. Một Customer có nhiều Requirement khác context.
46. Requirement history được lưu.
47. Requirement responsibility có lịch sử.
48. Handover Requirement không đổi Customer core.
49. Tạo được Financial Profile.
50. Financial Profile có scope.
51. Financial Profile có as-of date.
52. Financial Profile có status Customer Declined.
53. Customer Declined không tự unqualified.
54. Lưu được Income Source.
55. Lưu được Capital Source.
56. Lưu được Obligation.
57. Lưu được Borrowing Need.
58. Tính được Financial Readiness.
59. Readiness có explanation.
60. Readiness không tự đóng Requirement.
61. Sale chỉ xem Financial summary.
62. Finance xem detail theo quyền.
63. Marketing không xem Financial detail.
64. Financial Profile hết hạn được cảnh báo.
65. Snapshot tài chính được lưu khi dùng.
66. Tạo được Seller Profile.
67. Tạo được Seller Objective.
68. Seller Objective không tự tạo Listing.
69. Tạo được Declared Asset.
70. Declared Asset có verification status.
71. Declared Asset chuyển Asset Verification được.
72. Ownership claim không được coi là verified.
73. Lưu được co-owner.
74. Tạo được Land Owner Profile cơ bản.
75. Tạo được Related Party Stub.
76. Stub chưa phải Customer.
77. Stub convert Customer qua identity check.
78. Tạo được Relationship.
79. Relationship có hướng.
80. Relationship có context.
81. Tạo được Stakeholder.
82. Stakeholder có influence level.
83. Stakeholder có attitude.
84. Payer và Decision Maker tách được.
85. Customer 360 hiển thị Responsibility Matrix.
86. User chỉ thấy context được phép.
87. Access explanation hoạt động.
88. Timeline tổng hợp Lead.
89. Timeline tổng hợp Requirement.
90. Timeline hỗ trợ context filter.
91. Timeline visibility được enforce.
92. Tạo được note.
93. Note có visibility.
94. Note Legal/Finance có version.
95. Consent được lưu.
96. Consent theo channel.
97. Consent theo purpose.
98. Withdraw consent hoạt động.
99. Contact restriction chặn outbound.
100. Preferred contact time được lưu.
101. Archive Customer hoạt động.
102. Customer có Deal active không archive trái rule.
103. Restore Customer duplicate check.
104. Customer merged source redirect.
105. Sale chỉ xem `mine`.
106. Team Lead xem `team`.
107. Department Head xem `department`.
108. Director xem `all` theo quyền.
109. Backend enforce scope.
110. Backend enforce field masking.
111. Sửa URL không mở rộng quyền.
112. View không cho Export.
113. Sale không bulk export.
114. Marketing export phải theo consent.
115. Audit lưu before/after.
116. Audit lưu sensitive access theo policy.
117. Domain event được phát.
118. Event consumer idempotent.
119. Capability hoạt động với Customer mua.
120. Capability hoạt động với Customer bán/ký gửi.
121. Capability hoạt động với Customer chủ đất.
122. Capability hoạt động với Customer tổ chức.
123. Capability hỗ trợ nhiều người mua.
124. Capability hỗ trợ nhiều người bán.
125. Capability hỗ trợ nhiều người ảnh hưởng.
126. Capability không có owner sale vĩnh viễn.
127. Capability không làm mất lịch sử khi offboarding.
128. Capability cung cấp Requirement có cấu trúc cho Matching.
129. Capability cung cấp participant data cho Deal và Contract.
130. Capability cung cấp Customer 360 thống nhất trong enterprise operating boundary.

---

# 84. Anti-patterns và canonical requirements

Các nội dung dưới đây là anti-pattern bị cấm và canonical requirements hiện hành của dự án Greenfield.

## AP-PAR-001 — Đồng nhất Customer với Buyer

**Không được áp dụng**

Mô hình Customer chủ yếu như người mua sản phẩm.

**Canonical requirement**

Customer có thể đồng thời là Buyer, Seller, Owner, Land Owner, Payer, Representative, Investor hoặc Organization. Vai trò phải có context và effective period khi cần.

## AP-PAR-002 — Tạo Customer theo từng sale, project hoặc Legal Entity

**Không được áp dụng**

Tạo Customer mới khi khác sale, project, branch hoặc Legal Entity.

**Canonical requirement**

Một Party có một Customer relationship canonical trong enterprise operating boundary theo accepted identity policy. Các khác biệt được biểu diễn bằng roles, Requirements, responsibilities và transaction contexts.

## AP-PAR-003 — `owner_sale_id` là quyền sở hữu Customer

**Không được áp dụng**

Một sale sở hữu vĩnh viễn Customer và mọi dữ liệu liên quan.

**Canonical requirement**

Customer không có owner sale tuyệt đối. Access và responsibility được resolve từ Lead, care protection, Requirement, Deal, Listing, Contract, assignments, grants và organization context.

## AP-PAR-004 — Customer 360 là nguồn chân lý của mọi dữ liệu

**Không được áp dụng**

Sao chép Lead, Asset, Deal, Contract, Payment hoặc Receipt vào Customer tables và cho phép sửa từ màn hình 360.

**Canonical requirement**

Customer 360 là permission-aware projection có source references, provenance và freshness. Corrections phải thực hiện tại owning Context.

## AP-PAR-005 — Customer 360 và Identity Governance là hai Customer masters

**Không được áp dụng**

Capability 04 và Capability 05 tạo hai database/service độc lập cùng sở hữu Customer.

**Canonical requirement**

Cả hai capability thuộc `party` Context và dùng một canonical Party/Customer identity model. Tách capability chỉ để phân chia product concern.

## AP-PAR-006 — Phone được cập nhật trực tiếp trong Customer record

**Không được áp dụng**

Frontend hoặc Customer service ghi trực tiếp normalized phone và tự kết luận duplicate.

**Canonical requirement**

Phone Identity phải đi qua accepted identity-governance behavior, concurrency protection, masking và duplicate resolution trong Party Context.

## AP-PAR-007 — Declared Asset là verified Asset/Ownership

**Không được áp dụng**

Tài sản Customer khai báo được coi ngay là Property Asset hoặc Ownership chính thức.

**Canonical requirement**

Party Context chỉ sở hữu declaration/Seller Objective. Product Context sở hữu Asset, verified Ownership, Selling Right và Listing.

## AP-PAR-008 — Seller Objective tự tạo Listing active

**Không được áp dụng**

Khi Customer muốn bán, hệ thống tự tạo active Listing.

**Canonical requirement**

Listing chỉ được tạo/activate trong Product Context sau Asset/Ownership/Selling Right verification và required approval.

## AP-PAR-009 — Một Financial Profile áp dụng cho mọi context

**Không được áp dụng**

Dùng một hồ sơ tài chính hiện tại cho mọi Requirement, Deal và đánh giá lịch sử.

**Canonical requirement**

Financial Profile có scope, version, as-of date, validity và access policy. Historical decisions phải dùng approved snapshot/version.

## AP-PAR-010 — Financial Readiness là quyết định tín dụng

**Không được áp dụng**

Readiness hoặc score tự đóng Requirement, từ chối Customer hoặc quyết định Booking.

**Canonical requirement**

Financial Readiness chỉ hỗ trợ tư vấn và Matching, phải có explanation và không thay ngân hàng, legal authority hoặc human approval.

## AP-PAR-011 — Related Person tự trở thành Customer

**Không được áp dụng**

Mỗi người ảnh hưởng được tạo ngay thành Customer mà không identity resolution hoặc consent.

**Canonical requirement**

Related Party Stub có thể tồn tại tối thiểu. Khi tham gia giao dịch/liên hệ chính thức phải đi qua Party identity governance.

## AP-PAR-012 — Stakeholder Role cấp quyền truy cập

**Không được áp dụng**

Payer, Decision Maker, Owner hoặc Customer Role tự trở thành IAM permission.

**Canonical requirement**

Business role và authorization là hai concerns khác nhau. Backend resolve permission, scope, field policy và resource relationship độc lập.

## AP-PAR-013 — Project Access mở toàn bộ Customer

**Không được áp dụng**

User có Project Access được xem toàn Customer, Financial Profile, notes và các context khác.

**Canonical requirement**

Project Access chỉ là một input. Customer access phải giới hạn theo effective relationship, context và field policy.

## AP-PAR-014 — Aggregate access mặc định cấp detail/export access

**Không được áp dụng**

Xem Customer count hoặc summary đồng nghĩa xem detail, sensitive fields hoặc export.

**Canonical requirement**

Aggregate, summary, detail, sensitive-field và export access là các quyền riêng, được backend enforce.

## AP-PAR-015 — Timeline là nơi sửa business facts

**Không được áp dụng**

Sửa Timeline để sửa Contract, Receipt, Payment, Consent hoặc Customer merge history.

**Canonical requirement**

Timeline là projection. Business correction phải thực hiện tại owning Context và tạo correction/replacement fact có lineage.

## AP-PAR-016 — Direct cross-context write khi create/convert

**Không được áp dụng**

Lead direct-insert Party/Customer hoặc Party direct-create Deal/Asset/Document trong cùng transaction.

**Canonical requirement**

Mỗi Context dùng local transaction và phối hợp qua accepted application contracts/Events, idempotency và reconciliation. Không dùng distributed transaction.

## AP-PAR-017 — Candidate examples là exact contracts

**Không được áp dụng**

Dùng tables, endpoint paths, permission codes, states hoặc Event names trong Capability Specification để code trực tiếp.

**Canonical requirement**

Exact implementation phải được khóa trong Party Context Pack, Alembic, OpenAPI, JSON Schema/AsyncAPI và security registries.

## AP-PAR-018 — Mặc định có legacy migration

**Không được áp dụng**

Suy luận rằng có CRM tiền nhiệm, external legacy IDs hoặc compatibility layer bắt buộc.

**Canonical requirement**

`crm_bds_ai` là Greenfield. Migration chỉ được thực hiện khi có approved scope, mapping, reconciliation, security review và acceptance criteria riêng.

---

# 85. Kết luận

Customer 360 Capability là trung tâm quản trị Party–Customer relationship của `crm_bds_ai`.

Capability phải bảo đảm:

- Một canonical Party/Customer identity trong enterprise operating boundary.
- Customer có thể có nhiều roles, Requirements và business contexts.
- Customer không thuộc sở hữu vĩnh viễn của một sale.
- Requirement khác Lead và khác Deal.
- Seller Objective khác Listing.
- Declared Asset/Ownership khác verified Asset/Ownership.
- Financial Profile có scope, version, as-of date, validity và field-level protection.
- Financial Readiness chỉ hỗ trợ quyết định.
- Related parties và stakeholders được quản lý theo context.
- Customer 360 tổng hợp dữ liệu nhưng không thay source of truth.
- Access được backend resolve theo relationship, scope và field policy.
- Consent và restrictions được thực thi xuyên các capability liên quan.
- Merge giữ redirect, lineage và reconciliation.
- Cross-context workflows dùng local transactions, idempotency và durable integration.
- Mọi sensitive change và access có Audit theo policy.

> Customer 360 cung cấp góc nhìn thống nhất theo quyền; nó không phải một siêu aggregate, không phải một data warehouse và không được thay quyền sở hữu của các Bounded Context khác.
