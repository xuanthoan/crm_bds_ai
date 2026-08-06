# CRM_BDS_AI — CAPABILITY 05: CUSTOMER IDENTITY GOVERNANCE

## Deduplication, Phone Identity, Shared Contact, Canonical Merge and Identity Resolution

**Document ID:** `PROD-CAP-PAR-005`  
**Canonical path:** `docs/product/capabilities/cap-05-customer-identity-governance.md`  
**Product:** `crm_bds_ai`  
**Version:** `1.0.0`  
**Status:** `Accepted / Product Capability Baseline`  
**Document type:** `Product Capability Specification`  
**Primary capability code:** `CAP-PAR`  
**Capability slice:** `customer-identity-governance`  
**Primary owning Context:** `party`  
**Owner:** `Product Owner`  
**Co-owner:** `Party Domain Owner`  
**Reviewers:** `Architecture Owner`, `Security Owner`, `IAM Owner`, `Lead Domain Owner`, `Activity Domain Owner`, `Product Domain Owner`, `Transaction Domain Owner`, `Contract Domain Owner`, `Revenue Domain Owner`, `Audit Owner`, `Integration Owner`, `Operations Owner`, `QA Owner`  
**Effective date:** `2026-08-05`  
**Last reviewed:** `2026-08-05`  
**Classification:** `INTERNAL`

---

# 0. Phạm vi thẩm quyền và quan hệ tài liệu

Tài liệu này là nguồn canonical cho:

- Business outcomes của Customer Identity Governance Capability.
- Product policy chống tạo trùng Customer cá nhân bằng Phone Identity.
- Phone normalization, Phone Identity và Customer–Phone relationship semantics.
- Shared Phone, Phone Ownership Change và Wrong Number correction semantics.
- Identity Check, masked-match và anti-enumeration outcomes.
- Duplicate Candidate, Identity Resolution Case, Customer Merge, redirect và split/repair governance.
- Organization identity-governance outcomes.
- Product-level invariants, acceptance outcomes và anti-patterns của capability.

Tài liệu này không phải nguồn exact cho:

- Physical database schema hoặc DDL.
- Exact API paths, payloads, result codes hoặc error contracts.
- Exact Event names, payloads, channels hoặc delivery topology.
- Exact permission codes, scopes, role mappings hoặc masking rules.
- Exact workflow/state-machine enumerations.
- Exact SLA values, rate limits, retention periods hoặc alert thresholds.
- Exact UI routes, screens hoặc dashboard contracts.
- Exact data-import/migration plan.

Nguồn exact tương ứng:

| Chủ đề | Nguồn canonical |
|---|---|
| Thuật ngữ | Domain Glossary |
| Product requirements | PRD |
| Context ownership | Source of Truth Matrix |
| Architecture boundaries | Architecture Overview, Context Map và Accepted ADRs |
| Party/Customer/Identity behavior chi tiết | Party Context Implementation Pack |
| Customer 360 behavior | Customer 360 Capability + Party Context Pack |
| Database | Alembic migrations và Party Context DB Specification |
| API | OpenAPI |
| Events | JSON Schema, AsyncAPI và Event Registry |
| Permissions/scopes/masking/SoD | Security registries và matrices |
| Audit facts | Audit Context contracts |
| Cross-context merge coordination | Process Manager specification và affected Context Packs |
| Runtime values | Environment configuration và approved policy registries |
| Công việc hiện tại | Current Sprint Detailed Execution Pack |

**Capability không đồng nghĩa Bounded Context.** Customer Identity Governance Capability và Customer 360 Capability đều được thực hiện chủ yếu trong `party` Context. Việc tách thành hai capability nhằm phân chia product concerns; không tạo hai Customer masters, hai Party roots hoặc hai identity authorities.

Các phần “candidate vocabulary”, “candidate data model”, “candidate application operations”, “candidate permission vocabulary”, “candidate business facts”, “candidate user experiences” và “candidate reports” chỉ là đầu vào thiết kế. Chúng không được dùng thay Context Pack, migrations, OpenAPI, Event contracts hoặc security registries đã được chấp nhận.

---

---

# 1. Mục tiêu của capability

Customer Identity Governance Capability bảo vệ tính thống nhất của Party/Customer identity trong accepted enterprise operating boundary.

Capability phải giúp hệ thống có thẩm quyền trả lời:

- Phone value sau chuẩn hóa đã tồn tại hay chưa.
- Phone Identity đang liên kết với Customer nào, ở trạng thái nào và trong effective period nào.
- Một Phone Identity có đang được dùng chung theo approved Shared Phone Exception hay không.
- Request hiện tại phải link Customer hiện hữu, tạo Customer mới, chọn Customer trong shared-phone set hay mở Identity Resolution Case.
- Lead mới là business opportunity mới của Customer hiện hữu hay technical duplicate của cùng inbound event.
- Actor được xem full match, masked match hay chỉ nhận opaque reference.
- Khi Customer thay số, số bị nhập sai hoặc số đổi người sử dụng, lịch sử phải được bảo toàn thế nào.
- Hai Customer có thực sự đại diện cùng một Party hay chỉ dùng chung contact point.
- Customer nào là canonical target trong merge và vì sao.
- Merge ảnh hưởng thế nào đến Lead, Requirement, Deal, Listing, Contract, Payment, Receipt, Revenue, Commission, consent và access contexts.
- Downstream Context nào đã hoàn thành rebind/reconciliation sau merge.
- Khi merge sai, có thể tạo controlled split/repair plan thế nào.
- Concurrent requests được ngăn tạo duplicate Phone Identity/Customer ra sao.
- Identity lookup được bảo vệ khỏi enumeration và data exfiltration như thế nào.
- Imported/historical data chỉ được scan và repair khi có approved scope riêng.
- Organization identity được quản trị bằng registry identifiers thay vì phone-only policy.

Capability áp dụng cho:

- Customer creation trực tiếp trong Party Context.
- Customer creation/linking từ Lead.
- Approved import/integration flows.
- Public form và provider webhook flows qua Integration/Marketing boundaries.
- Thêm, sửa, xác minh, inactivate hoặc thay primary phone.
- Customer archive/restore.
- Shared Phone review.
- Phone Ownership Change.
- Customer Merge, redirect, reconciliation và controlled split/repair.
- Individual và Organization Party/Customer.
- Buyer, Seller, Owner, Payer, Representative, Referrer và Related Party conversion.

Nguyên tắc canonical:

> Một Individual Customer có thể có nhiều Phone Identities. Một normalized phone mặc định chỉ có một active Customer relationship trong accepted enterprise boundary, trừ Shared Phone Exception đã được phê duyệt, còn hiệu lực và phù hợp với policy.

---

---

# 2. Vị trí của capability trong kiến trúc

Customer Identity Governance Capability là một capability slice của `party` Context.

Capability sử dụng:

- Platform Configuration Capability: policy definitions, Business Calendar, SLA, approval, notification và job definitions.
- IAM Context: authenticated actor, workforce/organization context, permission, scope, delegation và break-glass.
- Lead Context: Lead contact snapshot, source lineage, identity-resolution request và Customer-link result.
- Customer 360 Capability trong Party Context: Party, Customer, related-party conversion, roles và Customer-facing projections.
- Integration Context: provider authentication, transport payload, webhook delivery, idempotency và reconciliation.
- Audit Context: immutable Audit facts cho lookup, sensitive access, merge, repair và approvals.
- Operations Context: approved batch jobs, repair execution, monitoring và incident handling.

Capability cung cấp canonical identity outcomes cho:

- `lead`: Customer linking, masked match và redirect.
- `party`: Customer 360, contact management, related-party conversion và merge state.
- `product`: Owner/Seller/Representative references.
- `transaction`: Buyer/Seller/Payer references.
- `contract`: Contract party, payer và beneficiary references.
- `revenue`: participant/referrer/beneficiary references.
- `analytics`: Customer counts, returning-Customer semantics và identity-quality metrics.

Luồng tổng quát:

```text
Raw Contact
→ Normalize in Party Context
→ Resolve Phone Identity
→ Apply Identity Policy
→ Existing Customer / New Customer / Shared Phone Review / Resolution Case
→ Return masked or authorized result
→ Link business context
→ Preserve canonical Customer and redirect lineage
```

Cross-context rule:

- Mỗi Context chỉ cập nhật dữ liệu mình sở hữu.
- Party Context không direct-write Lead, Deal, Contract, Payment, Revenue hoặc Commission.
- Các Context khác không direct-write Phone Identity, Customer merge state hoặc redirect.
- Cross-context propagation dùng durable Events/application contracts, idempotency, Process Manager và reconciliation.
- Không dùng distributed transaction.

---

---

# 3. Ranh giới sở hữu dữ liệu

## 3.1. Party Context sở hữu trong capability này

- Phone Identity.
- Phone-normalization policy application và normalization result.
- Customer–Phone Identity relationship.
- Primary-phone governance.
- Phone verification state.
- Phone usage/effective-period state.
- Shared Phone Exception và participating Customer relationships.
- Phone Ownership Change request, decision và local execution.
- Wrong Number/Correction history.
- Identity Check decision record và masked-result metadata.
- Duplicate Candidate.
- Identity Resolution Case.
- Customer Merge request, plan, Party-owned execution state và redirect.
- Party/Customer merge lineage.
- Controlled split/identity-repair request.
- Organization identity records và duplicate candidates.
- Party identity claims.
- Identity-conflict state.
- Party-owned reconciliation state for canonical-customer propagation.

## 3.2. Party Context không sở hữu

- Lead source, attribution, care protection và Lead assignment: `lead`.
- Authentication, authorization, role/scope definitions và workforce: `iam`.
- Canonical Interaction/Task/Appointment records: `activity`.
- Asset, verified Ownership, Selling Right, Listing và Availability: `product`.
- Deal, Transaction Case, Hold và Booking: `transaction`.
- Contract, Payment, Receipt, Refund và Settlement: `contract`.
- Revenue Entitlement, Recognition, Commission và payout: `revenue`.
- File binary, Document versions và signature evidence: `documents`.
- Immutable Audit facts: `audit`.
- Provider connections, webhook/sync delivery và transport retries: `integration`.
- Batch runtime, queues, incidents, backup/restore và production repair execution: `operations`.
- Workflow/SLA/approval definitions: `platform`.

## 3.3. Một canonical Party/Customer identity authority

Customer 360 Capability và Customer Identity Governance Capability phải:

- Dùng cùng Party aggregate/identity root.
- Dùng cùng Customer relationship identity.
- Dùng cùng Phone Identity authority.
- Dùng cùng merge redirect và canonical-customer semantics.
- Không tạo service/database riêng cạnh tranh.
- Không đồng bộ hai Customer masters bằng eventual consistency.

## 3.4. Không direct-write qua Context boundaries

Các Context khác không được:

- Tự tạo normalized phone.
- Tự kết luận Customer duplicate.
- Tự tạo second Customer khi masked match tồn tại.
- Tự gắn cùng Phone Identity cho nhiều Customer.
- Tự chuyển phone từ Customer này sang Customer khác.
- Tự merge Customer.
- Tự bỏ qua duplicate check.
- Tự thay canonical Customer redirect.

Party Context không được:

- Direct-update Lead, Deal, Contract, Payment, Revenue hoặc Commission records khi merge.
- Giữ transaction mở chờ downstream Context.
- Sửa rendered Contract hoặc immutable Receipt evidence.
- Chuyển lịch sử tài chính chỉ vì Phone Ownership Change.

## 3.5. Audit và operational records

Party Context có thể giữ workflow/decision records cần thiết cho identity resolution.

Audit Context sở hữu immutable Audit facts về:

- Sensitive identity lookup.
- Shared-phone approval.
- Ownership change.
- Merge approval/execution.
- Split/repair.
- Bulk scan/import.
- Break-glass hoặc elevated access.

Operational job/incident evidence thuộc Operations Context.

---

---

# 4. Nguyên tắc xác định Customer cá nhân trùng

## 4.1. Quy tắc duy nhất

Hai Customer cá nhân được coi là duplicate candidate chính thức khi có ít nhất một Phone Identity chuẩn hóa trùng nhau.

```text
Customer A.phone_identity_id
=
Customer B.phone_identity_id
```

## 4.2. Các trường không được dùng để tự động kết luận duplicate

Không được tự kết luận Customer trùng chỉ vì giống:

* Họ tên.
* Email.
* Zalo.
* Facebook.
* Ngày sinh.
* CCCD.
* Địa chỉ.
* Nghề nghiệp.
* Nơi làm việc.
* Thiết bị.
* IP.
* Cookie.
* Ghi chú.
* Nguồn Lead.
* Người giới thiệu.

## 4.3. Các trường trên chỉ được dùng để

* Tìm kiếm.
* Hiển thị đối chiếu.
* Hỗ trợ xác định Customer khi shared phone.
* Hỗ trợ điều tra dữ liệu.
* Hỗ trợ xác minh merge sau khi đã có phone overlap.
* Cảnh báo dữ liệu có thể sai.

## 4.4. Không xây dựng duplicate score cá nhân dựa trên nhiều trường

Capability không được tự gán:

```text
Tên giống 80%
+ Email giống
+ Địa chỉ giống
= Customer trùng
```

nếu không có Phone Identity overlap.

## 4.5. Ngoại lệ sửa dữ liệu đặc biệt

Chỉ công cụ data repair đặc biệt mới được đề nghị merge hai Customer cá nhân không có phone overlap khi:

* Có bằng chứng lịch sử rõ ràng.
* Có proven import/data defect.
* Phone cũ đã bị mất khỏi dữ liệu.
* Có phê duyệt cấp Director.
* Có CRM Admin thực hiện.
* Có audit đầy đủ.

Đây không phải quy trình merge thông thường.

---

# 5. Khái niệm Phone Identity

## 5.1. Phone Identity là gì

Phone Identity là danh tính kỹ thuật đại diện cho một số điện thoại duy nhất sau chuẩn hóa.

Ví dụ các giá trị:

```text
0912 345 678
0912.345.678
0912-345-678
(0912) 345 678
84912345678
+84912345678
```

đều phải dẫn đến một Phone Identity:

```text
+84912345678
```

## 5.2. Một Phone Identity duy nhất trong Enterprise

Mỗi `normalized_phone` chỉ có một bản ghi trong `phone_identities`.

## 5.3. Customer không lưu normalized phone trực tiếp

Mô hình chuẩn:

```text
Customer
→ CustomerPhoneLink
→ PhoneIdentity
```

## 5.4. Shared phone không tạo Phone Identity thứ hai

Nhiều Customer dùng chung số vẫn liên kết đến cùng một Phone Identity.

---

# 6. Phone Identity semantics và candidate vocabulary

> Phone types, validation states và lifecycle states dưới đây là product-level vocabulary đầu vào. Exact enums và transitions thuộc Party Context Pack và machine-readable contracts.


Một Phone Identity gồm:

* Phone Identity ID.
* Normalized phone.
* Country calling code.
* National number.
* Phone type.
* Country code.
* Validation status.
* Carrier metadata nếu có.
* First seen at.
* Last seen at.
* Normalization version.
* Source count.
* Risk flags.
* Shared status.
* Active link count.
* Status.
* Created at.
* Updated at.

## 6.1. Phone type

* Mobile.
* Landline.
* Business hotline.
* Virtual number.
* VoIP.
* Unknown.
* Test number.
* Internal number.
* Invalid.

## 6.2. Validation status

```text
VALID
POSSIBLY_VALID
INVALID
UNSUPPORTED_COUNTRY
MISSING_COUNTRY_CONTEXT
TEST_NUMBER
BLOCKED_NUMBER
PENDING_REVIEW
```

## 6.3. Phone Identity status

```text
ACTIVE
RESTRICTED
BLOCKED
MERGED_ALIAS
INVALIDATED
ARCHIVED
```

---

# 7. Customer–Phone Identity relationship semantics

> Candidate link attributes/statuses không phải physical schema hoặc exact state machine.


## 7.1. Khái niệm

Customer Phone Link thể hiện quan hệ giữa Customer và Phone Identity.

## 7.2. Thuộc tính

* Customer.
* Phone Identity.
* Phone usage type.
* Is primary.
* Is Zalo.
* Active status.
* Verification status.
* Ownership status.
* Shared phone exception.
* Effective from.
* Effective to.
* Source.
* Source Lead.
* Created by.
* Approved by.
* Notes.
* Created at.

## 7.3. Phone usage type

* Personal.
* Work.
* Home.
* Assistant.
* Representative.
* Family.
* Business hotline.
* Emergency.
* Other.

## 7.4. Link status

```text
ACTIVE
INACTIVE
PENDING_VERIFICATION
PENDING_CONFLICT_REVIEW
OWNERSHIP_CHANGED
WRONG_NUMBER
REPLACED
REVOKED
ARCHIVED
```

---

# 8. Một Customer có nhiều số điện thoại

## 8.1. Không giới hạn số lượng

Customer có thể có:

* Số cá nhân.
* Số công việc.
* Số Zalo.
* Số phụ.
* Số người đại diện.
* Số cũ.
* Số không còn dùng.

## 8.2. Một primary phone active mặc định

Mỗi Customer cá nhân mặc định chỉ có một primary phone active.

## 8.3. Có thể không có primary tạm thời

Cho phép trong trường hợp:

* Đang giải quyết conflict.
* Customer không còn số hợp lệ.
* Đang chuyển ownership.
* Chờ xác minh.

## 8.4. Không xóa số cũ

Số cũ được chuyển:

* Inactive.
* Ownership changed.
* Wrong number.
* Replaced.

Lịch sử vẫn được giữ.

---

# 9. Chuẩn hóa số điện thoại

## 9.1. Quy trình chuẩn hóa

1. Nhận giá trị gốc.
2. Trim khoảng trắng.
3. Xóa ký tự trình bày.
4. Xác định dấu `+`.
5. Xác định country context.
6. Xác định country calling code.
7. Xử lý domestic trunk prefix.
8. Xử lý historical prefix nếu có approved normalization rule.
9. Kiểm tra độ dài.
10. Kiểm tra prefix hợp lệ.
11. Phân loại mobile/landline.
12. Sinh canonical normalized value.
13. Validate.
14. Lưu normalization version.
15. Sinh checksum hoặc hash tìm kiếm nếu cần.

## 9.2. Ký tự được loại bỏ

* Khoảng trắng.
* Dấu chấm.
* Dấu gạch ngang.
* Dấu ngoặc.
* Dấu phân cách.
* Ký tự định dạng không có ý nghĩa.

## 9.3. Không xóa số mở rộng tùy tiện

Nếu có extension:

```text
02812345678 ext 123
```

phải tách:

* Main Phone Identity.
* Extension metadata.

## 9.4. Số Việt Nam

Phải nhận diện tương đương giữa:

```text
09xxxxxxxx
84xxxxxxxxx
+84xxxxxxxxx
```

theo rule version hợp lệ.

## 9.5. Số nước ngoài

Phải có country context rõ ràng.

Không tự áp quy tắc Việt Nam cho số nước ngoài.

## 9.6. Không sửa dữ liệu gốc

Lưu cả:

* `raw_phone`.
* `normalized_phone`.

---

# 10. Phiên bản quy tắc chuẩn hóa

## 10.1. Vì sao cần version

Quốc gia có thể thay đổi:

* Prefix.
* Độ dài.
* Kế hoạch đánh số.
* Quy tắc landline.
* Quy tắc mobile.

## 10.2. Mỗi kết quả lưu version

Khi thay normalization rule:

* Số mới dùng version mới.
* Số cũ không bị sửa âm thầm.
* Có thể chạy re-normalization job có kiểm soát.

## 10.3. Re-normalization

Phải có:

* Dry run.
* Impact report.
* Duplicate conflicts mới.
* Approval.
* Batch limit.
* Rollback plan.
* Audit.

---

# 11. Phone-normalization policy inputs

> Exact country rules, library behavior và effective versions phải được validated và khóa trong approved configuration/contracts; danh sách dưới đây không phải universal implementation.


Có thể cấu hình theo quốc gia:

* Country code.
* Calling code.
* Trunk prefix.
* Valid lengths.
* Valid prefixes.
* Mobile ranges.
* Landline ranges.
* Test number list.
* Internal hotline list.
* Invalid pattern.
* Historical prefix conversion.
* International support.
* Default country context.

System invariant về uniqueness không được tắt.

---

# 12. Identity resolution khi tạo Customer trực tiếp

Quy trình business bắt buộc:

1. Actor cung cấp một hoặc nhiều raw phone values.
2. Backend normalize từng số bằng approved rule version.
3. Loại duplicate trong request.
4. Validate và classify.
5. Resolve Phone Identity trong accepted enterprise boundary.
6. Áp identity policy và effective shared-phone exceptions.
7. Trả authorized/masked outcome.
8. Chỉ cho phép create khi không có unresolved conflict.
9. Trong Party local transaction, tạo Party/Customer relationship và Phone Identity/links phù hợp.
10. Ghi Outbox Event và required audit request.
11. Commit.
12. Trả canonical Customer/result idempotently.

Không cho phép:

- Frontend tạo Customer trước rồi thêm phone sau để né duplicate check.
- Client tự gửi normalized phone làm authority.
- Tách Party creation và Phone Identity linking thành các thao tác có thể tạo orphan/duplicate mà không có reconciliation.

---

# 13. Identity resolution khi tạo hoặc xử lý Lead

Lead và Party là hai Context riêng.

Quy trình:

1. `lead` lưu Lead/source snapshot bằng local transaction và durable identity-resolution request.
2. `party` normalize contact point và resolve Phone Identity/Customer.
3. `party` trả một trong các outcomes: no match, existing Customer, shared-phone selection, imported-data conflict, invalid phone hoặc canonical redirect.
4. Khi cần tạo Customer tối thiểu, `party` thực hiện local transaction idempotently.
5. `lead` consume result và link canonical Customer trong local transaction.
6. Lead source, attribution và care-protection semantics vẫn thuộc `lead`.
7. Partial failure phải retry/reconcile.

Lead hợp lệ của Customer hiện hữu vẫn được tạo khi đó là business opportunity mới.

Không coi mọi Lead cùng Customer là technical duplicate.

Không được:

- `lead` direct-insert Party/Customer/Phone tables.
- `party` direct-update Lead tables.
- Dùng distributed transaction.

---

# 14. Kiểm tra khi thêm số điện thoại

Quy trình:

1. Xác định Customer hiện tại.
2. Normalize số mới.
3. Kiểm tra số đã có trên chính Customer.
4. Kiểm tra toàn Enterprise.
5. Phân loại:

   * Chưa tồn tại.
   * Đã có trên cùng Customer.
   * Đã có trên Customer khác.
   * Shared phone đã duyệt.
   * Phone inactive trên Customer cũ.
   * Phone thuộc merged Customer.
6. Thực hiện action phù hợp.

## 14.1. Số đã có trên cùng Customer

Không tạo link trùng.

Có thể:

* Update usage type.
* Update verification.
* Đặt primary theo quyền.

## 14.2. Số thuộc Customer khác

Mặc định chặn.

Tạo Resolution Case.

---

# 15. Kiểm tra khi sửa số điện thoại

## 15.1. Không overwrite normalized phone đã có lịch sử

Không thay:

```text
CustomerPhoneLink.phone_identity_id
```

từ số A sang số B như một edit đơn giản.

## 15.2. Quy trình đúng

* Đánh dấu link A là wrong/inactive/replaced.
* Tạo hoặc tìm Phone Identity B.
* Tạo link mới.
* Chuyển primary nếu phù hợp.
* Ghi quan hệ replacement.
* Audit.

## 15.3. Trường hợp lỗi nhập liệu chưa phát sinh nghiệp vụ

Có thể cho phép correction đơn giản nếu:

* Bản ghi mới tạo.
* Chưa có Lead/Deal/Contract.
* Có quyền.
* Không có conflict.
* Audit đầy đủ.

---

# 16. Kiểm tra khi thay primary phone

Phải kiểm tra:

* Link mới active.
* Phone Identity hợp lệ.
* Không có conflict chưa giải quyết.
* Customer có quyền sử dụng số.
* Shared exception nếu cần.
* Consent/contact preference.
* Một primary active sau transaction.

Thay primary không làm xóa primary cũ; primary cũ chỉ chuyển `is_primary=false`.

---

# 17. Kiểm tra khi restore Customer

Trước restore:

* Kiểm tra Customer đã merge hay chưa.
* Kiểm tra tất cả Phone Identity.
* Kiểm tra số đã chuyển ownership.
* Kiểm tra Customer mới đang dùng số.
* Kiểm tra shared phone.
* Kiểm tra active business records.
* Tạo Resolution Case nếu conflict.

Customer đã merge không được restore thông thường.

---

# 18. Kiểm tra khi import

## 18.1. Quy trình

1. Đọc từng dòng.
2. Lưu raw source.
3. Normalize phone.
4. Duplicate check trong file.
5. Duplicate check Phone Identity toàn Enterprise.
6. Technical duplicate check.
7. Phân loại.
8. Preview.
9. Approval nếu cần.
10. Import.
11. Reconciliation.
12. Error report.

## 18.2. Phân loại kết quả

* New Customer allowed.
* Existing Customer linked.
* New Lead for existing Customer.
* Duplicate row in file.
* Technical duplicate.
* Invalid phone.
* Shared phone review.
* Ownership change review.
* Imported-data identity conflict.
* Missing required data.
* Rejected by permission.

## 18.3. Không tạo tất cả rồi merge sau

Import phải kiểm tra trước khi insert Customer.

---

# 19. API/Integration behavior requirements

> Result codes dưới đây là candidate semantic outcomes. Exact codes, payloads và error contracts thuộc OpenAPI/Error Registry.


## 19.1. Backend tự normalize

Không tin client gửi:

```text
normalized_phone
```

## 19.2. Idempotency

Sử dụng:

* `external_id`.
* `source_event_id`.
* `idempotency_key`.
* `payload_hash`.

## 19.3. Result code chuẩn

```text
NEW_CUSTOMER_ALLOWED
EXISTING_CUSTOMER_LINKED
PHONE_INVALID
PHONE_ALREADY_LINKED_TO_SAME_CUSTOMER
OUT_OF_SCOPE_MATCH
SHARED_PHONE_REVIEW_REQUIRED
SHARED_PHONE_CUSTOMER_SELECTION_REQUIRED
PHONE_OWNERSHIP_REVIEW_REQUIRED
MERGED_CUSTOMER_REDIRECT
IMPORTED_IDENTITY_CONFLICT
TECHNICAL_DUPLICATE_IGNORED
IDENTITY_RESOLUTION_PENDING
```

## 19.4. Integration không được tự merge

Dù payload có cờ:

```text
merge=true
```

backend vẫn phải từ chối nếu không qua workflow.

---

# 20. Canonical Identity Check outcomes

> Exact transport representation thuộc OpenAPI; capability chỉ khóa business meaning và disclosure behavior.


## 20.1. Không tìm thấy

Cho phép:

* Tạo Customer.
* Tạo Phone Identity.
* Tạo link.

## 20.2. Tìm thấy trên cùng Customer

Không tạo link mới.

## 20.3. Tìm thấy trên Customer khác trong scope

Hiển thị thông tin phù hợp và action:

* Link Lead.
* Request collaboration.
* Request transfer.
* Open identity case.

## 20.4. Tìm thấy ngoài scope

Chỉ trả masked/minimal response.

## 20.5. Shared phone

Không tự chọn Customer.

Yêu cầu:

* Chọn Customer.
* Xác minh thêm.
* Hoặc đưa manual resolution.

## 20.6. Customer đã merge

Redirect về Customer chính.

## 20.7. Customer archived hoặc soft-deleted

Không tạo Customer mới.

Cho phép:

* Restore request.
* Ownership change request.
* Data review.

## 20.8. Phone inactive

Vẫn coi là Phone Identity đã tồn tại.

Không tự kết luận số đã thuộc người khác.

---

# 21. Masked Identity Result

> JSON bên dưới là illustrative example, không phải exact response contract.


## 21.1. Mục tiêu

Ngăn lộ dữ liệu Customer ngoài scope nhưng vẫn cho user biết số đã tồn tại.

## 21.2. Ví dụ response

```json
{
  "exists": true,
  "match_type": "OUT_OF_SCOPE_MATCH",
  "masked_customer_name": "Nguyễn V*** A",
  "masked_phone": "09******78",
  "customer_access_status": "OUT_OF_SCOPE",
  "available_actions": [
    "LINK_LEAD",
    "REQUEST_ACCESS",
    "OPEN_RESOLUTION_CASE"
  ]
}
```

## 21.3. Không trả trong payload

* Full Customer ID nếu không cần.
* Full name.
* Full phone.
* Sale name.
* Requirement.
* Deal.
* Contract.
* Financial Profile.
* Timeline.
* Other phones.

## 21.4. Opaque reference

Có thể sử dụng `match_reference_token` có thời hạn thay vì trả Customer ID thật.

---

# 22. Anti-enumeration

## 22.1. Rủi ro

User có thể nhập hàng loạt số để dò:

* Customer nào có trong hệ thống.
* Số của người nổi tiếng.
* Customer của sale khác.
* Danh sách Marketing.

## 22.2. Biện pháp

* Rate limit.
* Per-user quota.
* Per-session quota.
* Query pattern detection.
* Masked response.
* Opaque token.
* No full Customer ID.
* CAPTCHA cho public form nếu cần.
* Audit mọi lookup.
* Alert mass lookup.
* Chặn sequential number probing.
* Chỉ cho lookup trong workflow hợp lệ.
* Giới hạn bulk lookup.
* Re-authentication cho thao tác nhạy cảm.

## 22.3. Check không tạo Lead

Lookup nhiều nhưng không tạo Lead hoặc nghiệp vụ hợp lệ phải được cảnh báo.

---

# 23. Technical Duplicate và Business Identity Duplicate

## 23.1. Technical duplicate

Cùng một sự kiện bị gửi lại.

Ví dụ:

* Webhook retry.
* Import retry.
* Double-click.
* Network timeout.
* API retry.

Xác định bằng:

* External event ID.
* Idempotency key.
* Payload hash.
* Source.
* Time window.

## 23.2. Business identity duplicate

Hai Customer record đại diện cùng một người và có phone overlap.

## 23.3. New Lead for existing Customer

Không phải technical duplicate.

Lead vẫn được tạo vì có thể là:

* Nhu cầu mới.
* Dự án mới.
* Campaign mới.
* Seller-side context mới.

---

# 24. Shared Phone

## 24.1. Khái niệm

Shared phone là một Phone Identity được phép liên kết active với nhiều Customer.

## 24.2. Trường hợp hợp lệ

* Vợ/chồng dùng chung số.
* Người cao tuổi dùng số của con.
* Trẻ vị thành niên dùng số người giám hộ.
* Trợ lý dùng số liên hệ.
* Đại diện pháp lý.
* Chủ doanh nghiệp dùng hotline.
* Nhóm mua chung dùng một đầu mối.
* Một hộ gia đình dùng một số.
* Customer tổ chức dùng số tổng đài.

## 24.3. Trường hợp không hợp lệ

* Sale muốn né duplicate.
* Không xác minh được.
* Data import lỗi.
* Hai Customer ngẫu nhiên dùng cùng số.
* Customer đã đổi số nhưng chưa xử lý ownership.
* Dùng hotline nội bộ làm số Customer cá nhân.

---

# 25. Quy trình yêu cầu Shared Phone

1. User nhập số.
2. Hệ thống phát hiện conflict.
3. User chọn “Yêu cầu dùng chung”.
4. Nhập lý do.
5. Chọn loại quan hệ.
6. Chọn Customer hiện hữu và Customer đề xuất.
7. Đính kèm bằng chứng nếu cần.
8. Tạo Resolution Case.
9. CRM Admin kiểm tra dữ liệu.
10. Business Manager xác nhận quan hệ.
11. Finance/Legal tham gia nếu ảnh hưởng giao dịch.
12. Approver quyết định.
13. Tạo Shared Phone Exception.
14. Tạo Customer Phone Link mới.
15. Gắn exception ID.
16. Ghi audit.
17. Phát event.

---

# 26. Shared Phone Exception semantics

> Candidate statuses phải được khóa trong Party Context state machine trước implementation.


Gồm:

* Exception code.
* Phone Identity.
* Exception type.
* Relationship type.
* Customer list.
* Primary contact Customer nếu có.
* Reason.
* Evidence.
* Requester.
* Reviewer.
* Approver.
* Effective from.
* Effective to.
* Review date.
* Status.
* Restrictions.
* Notes.
* Audit.

## 26.1. Status

```text
DRAFT
PENDING_REVIEW
PENDING_APPROVAL
APPROVED
ACTIVE
SUSPENDED
EXPIRED
REVOKED
REJECTED
```

## 26.2. Có thể hết hạn

Shared phone exception nên có ngày review, đặc biệt với:

* Trợ lý.
* Đại diện.
* Số tạm thời.
* Số tổ chức.

---

# 27. Quyền phê duyệt Shared Phone

## 27.1. Sale

* Tạo request.
* Cung cấp bằng chứng.
* Không được tự duyệt.

## 27.2. Team Lead

* Xác nhận quan hệ trong team.
* Không mặc định duyệt exception cross-team.

## 27.3. Department Head

* Duyệt theo hạn mức/policy.
* Xử lý tranh chấp trong phòng.

## 27.4. CRM Admin

* Kiểm tra dữ liệu.
* Thực thi link.
* Không tự quyết định tranh chấp thương mại phức tạp.

## 27.5. Finance/Legal

Tham gia nếu:

* Đã có hợp đồng.
* Có payment.
* Có ownership.
* Có đại diện pháp lý.

## 27.6. Director

Duyệt:

* Cross-department.
* Cross-Legal Entity.
* Tranh chấp.
* Giao dịch giá trị lớn.
* Ngoại lệ đặc biệt.

---

# 28. Hành vi hệ thống khi Shared Phone active

## 28.1. Lookup

Trả:

```text
SHARED_PHONE_CUSTOMER_SELECTION_REQUIRED
```

## 28.2. Không tự link Lead

Hệ thống phải:

* Yêu cầu chọn Customer.
* Dùng thêm context.
* Hoặc đưa manual review.

## 28.3. Không tự merge

Shared phone là lý do ngăn auto-merge.

## 28.4. Hiển thị cảnh báo

Customer 360 hiển thị:

* Shared phone.
* Customer nào cùng dùng.
* Quan hệ theo quyền.
* Exception validity.

## 28.5. Routing Lead

Routing chỉ chạy sau khi Customer được xác định.

---

# 29. Thu hồi Shared Phone Exception

Có thể thu hồi khi:

* Không còn dùng chung.
* Quan hệ kết thúc.
* Dữ liệu sai.
* Customer có số riêng.
* Có tranh chấp.
* Exception bị lạm dụng.

Quy trình:

* Tạo revoke request.
* Xác định Customer giữ số.
* Xác định Customer ngừng link.
* Kiểm tra business impact.
* Approval.
* End Customer Phone Link.
* Audit.

---

# 30. Phone Ownership Change

## 30.1. Khái niệm

Số điện thoại có thể thực sự chuyển từ người này sang người khác.

Ví dụ:

* Nhà mạng tái cấp số.
* Nhân viên rời doanh nghiệp, hotline chuyển người.
* Customer đổi số, số cũ được người khác sử dụng.
* Số trợ lý chuyển cho người mới.

## 30.2. Không tự động chuyển ownership

Việc Customer mới cung cấp số đang thuộc Customer cũ không đủ để tự chuyển.

## 30.3. Phải phân biệt

* Shared phone.
* Wrong number.
* Old inactive number.
* Ownership change.
* Temporary representative.
* Data entry error.

---

# 31. Quy trình Phone Ownership Change

1. Phát hiện số thuộc Customer cũ.
2. Tạo Ownership Change Request.
3. Xác định Customer cũ.
4. Xác định Customer mới.
5. Kiểm tra lịch sử sử dụng.
6. Kiểm tra thời điểm Customer cũ ngừng sử dụng.
7. Kiểm tra Lead/Deal/Contract/Payment liên quan.
8. Thu thập bằng chứng.
9. CRM Admin review.
10. Business review.
11. Finance/Legal review nếu cần.
12. Approval.
13. Đóng link Customer cũ với status `OWNERSHIP_CHANGED`.
14. Tạo link Customer mới.
15. Ghi effective date.
16. Không chuyển lịch sử giao dịch.
17. Audit.
18. Phát event.

---

# 32. Lịch sử không được chuyển theo số điện thoại

Khi ownership thay đổi, các dữ liệu sau vẫn thuộc Customer cũ:

* Lead cũ.
* Call cũ.
* Requirement cũ.
* Deal cũ.
* Booking.
* Contract.
* Receipt.
* Commission.
* Timeline.
* Attribution.

Chỉ các sự kiện mới sau ngày hiệu lực mới thuộc Customer mới.

---

# 33. Số điện thoại sai

## 33.1. Wrong Number

Dùng khi số chưa bao giờ thuộc Customer hoặc bị nhập sai.

## 33.2. Quy trình

* Đánh dấu link sai.
* Ghi lý do.
* Không xóa Phone Identity.
* Tạo số mới nếu có.
* Kiểm tra Customer khác.
* Audit.

## 33.3. Không dùng Wrong Number thay cho Ownership Change

Nếu số từng thuộc Customer thật, phải dùng ownership change hoặc inactive.

---

# 34. Phone Verification

> Verification levels là candidate vocabulary; exact evidence requirements và expiry policies thuộc Context Pack/Security policy.


## 34.1. Mức xác minh

```text
UNVERIFIED
CALL_CONNECTED
MESSAGE_CONFIRMED
CUSTOMER_CONFIRMED
REPRESENTATIVE_CONFIRMED
MANAGER_CONFIRMED
DOCUMENT_CONFIRMED
FAILED
EXPIRED
```

## 34.2. Dù chưa xác minh vẫn phải duplicate check

Unverified phone không được bỏ qua uniqueness.

## 34.3. Verification không chứng minh ownership tuyệt đối

Một cuộc gọi kết nối chỉ chứng minh khả năng liên hệ tại thời điểm đó.

## 34.4. Verification có thể hết hạn

Đặc biệt với:

* Representative phone.
* Hotline.
* Shared phone.
* Temporary contact.

---

# 35. Customer Duplicate Candidate

> Candidate statuses là design input, không phải exact lifecycle contract.


## 35.1. Điều kiện tạo candidate

* Hai Customer active cùng Phone Identity mà không có shared exception.
* Imported/historical data conflict.
* Import phát hiện Customer đã tồn tại.
* Restore tạo conflict.
* Re-normalization tạo overlap.
* Manual data repair.

## 35.2. Candidate status

```text
NEW
UNDER_REVIEW
PENDING_INFORMATION
PENDING_BUSINESS_CONFIRMATION
PENDING_FINANCE_REVIEW
PENDING_LEGAL_REVIEW
APPROVED_FOR_MERGE
REJECTED_NOT_DUPLICATE
RESOLVED_SHARED_PHONE
RESOLVED_OWNERSHIP_CHANGE
MERGED
CANCELLED
```

## 35.3. Candidate không tự merge

Tạo candidate chỉ là bước cảnh báo và review.

---

# 36. Identity Resolution Case

> Case types và fields dưới đây là product inventory; exact workflow và schema thuộc Party Context Pack.


## 36.1. Loại case

* Customer Merge.
* Shared Phone.
* Phone Ownership Change.
* Wrong Phone Correction.
* Customer Identification.
* Restore Conflict.
* Imported Data Conflict.
* Organization Duplicate.
* Special Data Repair.
* Merge Split/Reversal.

## 36.2. Thông tin

* Case code.
* Case type.
* Phone Identity.
* Customer list.
* Lead list.
* Legal Entity.
* Priority.
* Risk level.
* Business impact.
* Finance impact.
* Legal impact.
* Owner.
* Reviewer.
* Approver.
* SLA.
* Status.
* Decision.
* Evidence.
* Created at.
* Resolved at.

---

# 37. Customer Merge

## 37.1. Khái niệm

Merge là quá trình xác lập một canonical Customer relationship khi hai hoặc nhiều Customer records đại diện cùng một Party.

## 37.2. Merge không phải delete

Customer nguồn:

* Không bị xóa.
* Chuyển status `MERGED`.
* Có redirect đến Customer đích.
* Giữ lịch sử.
* Không nhận nghiệp vụ mới.

## 37.3. Không auto-merge shared phone

Nếu shared phone đã được duyệt:

* Không đề xuất merge tự động.
* Phải hiển thị cảnh báo.

---

# 38. Điều kiện đề nghị merge

Thông thường phải có:

* Ít nhất một Phone Identity overlap.
* Không có shared exception giải thích overlap.
* Có bằng chứng hai hồ sơ là cùng một người.
* Không có ownership change.
* Không có tranh chấp chưa xử lý.
* Có quyền yêu cầu merge.

## 38.1. Bằng chứng hỗ trợ

* Cùng tên.
* Cùng email.
* Cùng ngày sinh.
* Cùng địa chỉ.
* Cùng giấy tờ.
* Cùng lịch sử Customer xác nhận.
* Cùng người liên quan.

Các bằng chứng này chỉ hỗ trợ sau khi có phone overlap.

---

# 39. Ai được yêu cầu và thực hiện merge

## 39.1. Sale

Có thể:

* Tạo merge request.
* Cung cấp bằng chứng.
* Không thực hiện merge.

## 39.2. Team Lead/Department Head

Có thể:

* Review business context.
* Xác nhận ownership/care impact.
* Đề nghị Customer chính.

## 39.3. CRM Admin/Data Steward

Có thể:

* Phân tích dữ liệu.
* Tạo merge plan.
* Thực thi merge đã duyệt.

## 39.4. Finance

Phải review nếu có:

* Receipt.
* Debt.
* Refund.
* Revenue.
* Commission.
* Settlement.

## 39.5. Legal

Review nếu có:

* Contract.
* Dispute.
* Ownership.
* Representative authority.
* Legal hold.

## 39.6. Director

Phê duyệt merge phức tạp, cross-department hoặc cross-Legal Entity.

---

# 40. Phân loại merge đơn giản và phức tạp

## 40.1. Merge đơn giản

Có thể khi Customer nguồn:

* Không có Deal.
* Không có Booking.
* Không có Contract.
* Không có Payment.
* Không có verified ownership.
* Không có dispute.
* Chỉ có Lead/Profile cơ bản.

Có thể CRM Admin thực hiện theo policy.

## 40.2. Merge phức tạp

Khi có:

* Nhiều Legal Entity.
* Active Requirement.
* Deal.
* Booking.
* Contract.
* Receipt.
* Debt.
* Commission.
* Asset ownership.
* Listing.
* Shared phone.
* Dispute.
* Consent conflict.

Phải có multi-step review.

---

# 41. Chọn Customer chính

## 41.1. Không mặc định chọn hồ sơ cũ nhất

Hồ sơ chính được chọn theo:

* Có hợp đồng pháp lý chính thức.
* Có payment.
* Có Customer ID được dùng rộng hơn.
* Dữ liệu identity đáng tin cậy hơn.
* Hồ sơ đầy đủ hơn.
* Dữ liệu đã xác minh.
* Nhiều hệ thống ngoài tham chiếu.
* Ít conflict hơn.
* Quyết định của Data Steward.

## 41.2. Không chọn theo sale mạnh hơn

Không được chọn Customer chính chỉ vì thuộc team hoặc sale có vị trí cao hơn.

## 41.3. Lưu lý do

Merge plan phải ghi:

* Target Customer.
* Source Customers.
* Lý do chọn target.
* Approver.

---

# 42. Merge Preview

Trước khi merge phải hiển thị:

* Customer core.
* Phones.
* Emails.
* Addresses.
* Roles.
* Leads.
* Attribution.
* Requirements.
* Financial Profiles.
* Seller Profiles.
* Declared Assets.
* Relationships.
* Stakeholders.
* Notes.
* Care protection.
* Deals.
* Listings.
* Bookings.
* Contracts.
* Payments.
* Revenue.
* Commission.
* Consent.
* Restrictions.
* Legal holds.
* Access contexts.

---

# 43. Conflict trong Merge Preview

Phải chỉ rõ:

* Hai primary phone.
* Hai primary email.
* Tên pháp lý khác nhau.
* Ngày sinh khác nhau.
* Consent khác nhau.
* Financial Profile conflict.
* Hai active Requirement trùng.
* Hai active Deal trùng.
* Hai care protection trùng context.
* Customer type khác nhau.
* Organization/Individual mismatch.
* Ownership claim conflict.
* Contract participant conflict.

Không cho thực thi nếu còn conflict bắt buộc chưa giải quyết.

---

# 44. Merge Plan

Merge plan xác định cho từng resource:

* Keep target.
* Move to target.
* Link to target.
* Merge values.
* Keep both.
* Archive source.
* Require manual resolution.
* Skip.
* Block.

## 44.1. Field-level merge

Ví dụ:

* Tên: chọn verified value.
* Email: giữ tất cả không trùng.
* Address: giữ lịch sử.
* Tag: hợp nhất.
* Consent: dùng quy tắc hạn chế cao hơn.
* Contact restriction: giữ tất cả active restriction.
* Note: chuyển giữ source.
* Financial Profile: không tự gộp số liệu.

---

# 45. Quy tắc merge theo resource

## 45.1. Lead

Chuyển Customer link sang target.

Giữ:

* Source.
* Attribution.
* Lead ID.
* Sale history.

## 45.2. Requirement

Chuyển sang target.

Nếu duplicate active Requirement:

* Manual resolution.
* Không tự merge.

## 45.3. Financial Profile

Giữ từng profile và context.

Không cộng thu nhập hoặc tài sản tự động.

## 45.4. Relationship

Hợp nhất relation không trùng.

Giữ source và verification.

## 45.5. Care Protection

Phải xử lý theo Lead Management Capability.

Không tự chọn sale.

## 45.6. Deal

Chuyển Customer reference nếu không tạo duplicate active Deal.

Nếu conflict, block merge hoặc yêu cầu Deal resolution.

## 45.7. Contract

Không sửa bên hợp đồng tùy tiện.

Có thể:

* Link Party alias.
* Giữ Customer snapshot.
* Dùng target cho truy xuất hiện tại.
* Không thay rendered contract.

## 45.8. Payment

Không chuyển tiền giữa giao dịch.

Chỉ cập nhật Customer canonical link khi được phép.

## 45.9. Commission

Không thay người hưởng hoặc attribution.

## 45.10. Consent

Áp dụng nguyên tắc hạn chế cao hơn.

Nếu một source đã opt-out:

* Target phải tôn trọng opt-out theo mục đích/kênh tương ứng.

---

# 46. Thực thi Customer Merge và cross-context reconciliation

Customer Merge là một cross-context business process. Không thực thi bằng một distributed transaction hoặc bằng cách Party Context trực tiếp sửa mọi bảng liên quan.

## 46.1. Party local commit

Party Context thực hiện local transaction để:

1. Lock Party/Customer và Phone Identity records thuộc Party Context.
2. Kiểm tra optimistic version/concurrency guards.
3. Kiểm tra Merge Plan đã được approved và chưa stale.
4. Re-evaluate blocking identity conflicts.
5. Ghi merge execution identity.
6. Hợp nhất Party-owned contacts, roles, consent và identity relationships theo plan.
7. Đánh source Customer `MERGED` theo exact state machine.
8. Tạo canonical redirect.
9. Ghi Party-owned merge item outcomes.
10. Ghi Outbox Event cho canonical-customer change.
11. Commit local transaction.

Sau commit:

- Source Customer không nhận Party-owned business changes mới.
- Reads phải resolve canonical redirect theo contract.
- Downstream rebind có thể đang pending và phải hiển thị trạng thái reconciliation.

## 46.2. Downstream Context handling

Mỗi affected Context:

- Consume canonical-customer change idempotently.
- Giữ local transaction riêng.
- Rebind references khi semantic contract cho phép.
- Giữ immutable snapshots và legal/financial evidence.
- Không thay attribution, Commission beneficiary hoặc payment meaning nếu merge không có authority đó.
- Publish completion/failure outcome.
- Hỗ trợ replay và reconciliation.

Ví dụ:

- `lead` cập nhật canonical Customer link nhưng giữ source/attribution/care history.
- `product` xử lý Owner/Seller aliases theo verified-ownership policy.
- `transaction` cập nhật participant canonical references nhưng giữ transaction snapshots.
- `contract` giữ rendered/signed Contract snapshots và Receipt evidence; chỉ cập nhật canonical lookup/reference khi được phép.
- `revenue` không tự thay participant entitlement, Commission allocation hoặc payout.
- `activity` giữ historical actor/customer context và cập nhật projections theo contract.

## 46.3. Process Manager

Merge Process Manager theo dõi:

- Required downstream Contexts.
- Delivery/processing state.
- Retry attempts.
- Blocking failures.
- Reconciliation findings.
- Completion criteria.
- Manual intervention.
- Final acceptance evidence.

Exact Process Manager states thuộc Process Manager specification.

## 46.4. Failure behavior

Khi Party local transaction chưa commit:

- Rollback local changes.
- Không publish canonical-change Event.

Khi Party local transaction đã commit nhưng downstream chưa hoàn tất:

- Không rollback bằng cách xóa redirect tùy tiện.
- Giữ merge state là committed/reconciling theo exact state machine.
- Retry idempotently.
- Mở reconciliation/manual repair khi cần.
- Không để source nhận nghiệp vụ mới.
- Không báo merge hoàn tất toàn hệ thống nếu required consumers chưa đạt acceptance.

## 46.5. Prohibitions

Không được:

- Giữ database transaction mở qua nhiều Context.
- Direct-write cross-schema tables.
- Dùng frontend để điều phối rebind.
- Sửa signed Contract, issued Receipt hoặc immutable financial facts.
- Báo success chỉ vì Party redirect đã được tạo.
- Bỏ qua downstream failures.

---

# 47. Merge Redirect

Mọi request đến Customer nguồn phải:

* Trả Customer target.
* Ghi source Customer ID.
* Giữ alias.
* Không tạo resource mới trên source.
* Có thể hiển thị banner “Hồ sơ đã được hợp nhất”.

API có thể trả:

```json
{
  "status": "MERGED",
  "source_customer_id": "...",
  "canonical_customer_id": "...",
  "redirect": true
}
```

---

# 48. External ID sau merge

## 48.1. Giữ tất cả external ID

Target Customer nhận alias/reference của source.

## 48.2. Không tạo unique conflict

Nếu cùng namespace có hai external ID:

* Giữ nhiều alias nếu hệ thống ngoài cho phép.
* Hoặc chọn primary và lưu external alias.

## 48.3. Đồng bộ hệ thống ngoài

Có thể cần outbound event:

```text
customer.canonical_changed
```

Không tự cập nhật hệ thống ngoài nếu integration chưa hỗ trợ.

---

# 49. Undo Merge và Split

## 49.1. Merge không nên có nút Undo đơn giản

Sau merge có thể đã phát sinh:

* Lead mới.
* Deal mới.
* Contract mới.
* Payment.
* Timeline.
* External sync.

## 49.2. Split Request

Dùng khi merge sai.

Phải:

* Xác định mốc merge.
* Xác định dữ liệu gốc.
* Xác định dữ liệu phát sinh sau merge.
* Xác định resource phải trả về Customer nào.
* Có multi-step approval.
* Có dry run.
* Có audit.

## 49.3. Baseline delivery

Baseline delivery có thể:

* Không hỗ trợ self-service split.
* Chỉ có công cụ admin đặc biệt.
* Yêu cầu Director approval.
* Bắt buộc backup và reconciliation.

---

# 50. Exceptional Identity Repair without Phone Overlap

Đây là quy trình ngoại lệ cho proven data defect khi hai Individual Customer records không còn Phone Identity overlap nhưng có bằng chứng mạnh rằng chúng cùng một Party.

Quy trình này không phải merge thông thường và không thuộc baseline execution nếu chưa có approved scope.

Yêu cầu:

- Dedicated repair workflow/tool.
- Problem statement và evidence.
- Data Steward ownership.
- Product/Domain approval.
- Security review.
- Finance/Legal review khi có ảnh hưởng.
- Dry run và impact report.
- Reconciliation plan.
- Critical Audit.
- Không chạy batch không kiểm soát.
- Không dùng fuzzy matching để auto-merge.
- Không suy luận rằng dữ liệu tiền nhiệm tồn tại nếu chưa có approved import/migration scope.

Các nguyên nhân hợp lệ có thể gồm:

- Proven import defect.
- Phone history bị mất do approved external-data defect.
- Canonical mapping sai đã được chứng minh.
- Historical source record không còn giữ contact identifier nhưng có legal evidence.

Exact repair actions thuộc approved Data Repair Plan và current Sprint/operations authority.

---

# 51. Customer Organization Identity Governance

## 51.1. Quy tắc khác Customer cá nhân

Organization Customer không dùng phone-only để kết luận duplicate.

## 51.2. Identity key có thể gồm

* Tax code.
* Registration number.
* Country.
* Legal registry ID.
* External organization ID.

## 51.3. Legal name chỉ hỗ trợ

Tên giống không đủ để tự merge.

## 51.4. Chi nhánh tổ chức

Phải phân biệt:

* Cùng pháp nhân, nhiều địa điểm.
* Công ty mẹ/con.
* Brand và legal entity.
* Văn phòng đại diện.

Không merge chỉ vì cùng hotline.

---

# 52. Organization Duplicate Workflow

1. Chuẩn hóa tax code/registration.
2. Tìm registry toàn Enterprise.
3. So sánh country/namespace.
4. Phân loại:

   * Same legal entity.
   * Branch.
   * Parent/subsidiary.
   * Separate organization.
   * Unknown.
5. Manual review khi conflict.
6. Merge Organization Customer nếu được duyệt.
7. Giữ contact person và transaction history.

---

# 53. Party và Customer Identity

## 53.1. Party là identity root

Customer là quan hệ thương mại của Party.

## 53.2. Merge Customer có thể kéo theo Party merge

Chỉ khi:

* Hai Customer là cùng Party.
* Không có Party role conflict.
* Không phải Employee và Customer khác biệt cần giữ.

## 53.3. Employee đồng thời là Customer

Không merge Workforce identity vào Customer record.

Chỉ liên kết cùng Party khi đã xác minh.

## 53.4. Related Party Stub conversion

Khi Stub chuyển thành Customer:

* Normalize phone.
* Identity check.
* Link Customer hiện hữu hoặc tạo mới.
* Không tạo Customer trùng.

---

# 54. Identity Verification

> Verification levels là candidate vocabulary và không thay approved duplicate policy.


## 54.1. Mục tiêu

Xác định mức độ tin cậy của Customer identity.

## 54.2. Verification level

```text
UNVERIFIED
CONTACT_VERIFIED
PROFILE_CONFIRMED
DOCUMENT_RECEIVED
DOCUMENT_VERIFIED
TRANSACTION_VERIFIED
LEGAL_VERIFIED
```

## 54.3. Verification không thay duplicate rule

CCCD giống nhau có thể hỗ trợ xác minh nhưng không tự merge Customer cá nhân nếu không có phone overlap, trừ data repair đặc biệt.

## 54.4. Verification source

* Sale.
* Customer self-service.
* Finance.
* Legal.
* Contract.
* eKYC.
* External provider.

---

# 55. Identity Claim

Identity Claim lưu một khẳng định có thể cần xác minh:

* Tên pháp lý.
* Ngày sinh.
* Giấy tờ.
* Phone ownership.
* Representative relation.
* Organization registration.

Mỗi claim có:

* Value.
* Source.
* Verification.
* Effective date.
* Confidence.
* Evidence.
* Status.

Không overwrite claim cũ đã dùng trong giao dịch.

---

# 56. Identity Conflict

> Conflict types/severity dưới đây là candidate vocabulary. Exact blocking effects phải được quyết định theo Context và policy.


## 56.1. Loại conflict

* Same phone, different Customer.
* Same Customer, conflicting legal names.
* Shared phone without exception.
* Organization tax code conflict.
* Phone ownership conflict.
* Merged Customer still active.
* Multiple primary phones.
* Duplicate Phone Identity.
* Verification mismatch.
* Individual/Organization mismatch.

## 56.2. Severity

* Info.
* Warning.
* High.
* Critical.

## 56.3. Critical conflict

Có thể chặn:

* Contract creation.
* Payment refund.
* Ownership verification.
* Commission payout.

Tùy policy và loại conflict.

---

# 57. Imported/Historical Data Identity Scan — conditional capability

## 57.1. Điều kiện kích hoạt

Capability này chỉ được kích hoạt khi có approved data-import/migration scope.

Dự án Greenfield không mặc định có:

- Hệ thống tiền nhiệm.
- Customer data cần migrate.
- Compatibility layer.
- Historical duplicate cleanup.

## 57.2. Mục tiêu khi được phê duyệt

- Normalize imported phone values bằng approved rule version.
- Resolve existing Phone Identities.
- Phát hiện duplicate candidates.
- Phân loại Shared Phone, Ownership Change, invalid contact và proven duplicate.
- Tạo review cases và reports.
- Không auto-merge.

## 57.3. Quy trình

1. Ingest vào staging.
2. Bảo toàn source lineage.
3. Normalize bằng versioned rules.
4. Group candidate overlaps.
5. Áp exclusion/exception rules.
6. Tạo candidate và risk classification.
7. Review.
8. Thực thi approved canonical commands.
9. Reconcile counts, references và failures.
10. Lưu evidence.

## 57.4. Mức ưu tiên

Ưu tiên cao hơn khi candidate liên quan:

- Contract.
- Payment/Receipt.
- Active Deal/Booking.
- Revenue/Commission.
- Verified Ownership.
- Nhiều Legal Entity relationships.
- Nhiều Customer cùng Phone Identity.

## 57.5. Không auto-merge

Scan chỉ tạo candidate, evidence và review queue. Mọi merge phải qua approved workflow.

---

# 58. Controlled Batch Identity Repair

## 58.1. Cho phép

* Re-normalize.
* Link orphan phone.
* Fix duplicate Phone Identity.
* Mark invalid numbers.
* Generate candidates.
* Apply approved merge plan.

## 58.2. Bắt buộc

* Dry run.
* Approval.
* Batch size.
* Checkpoint.
* Idempotency.
* Reconciliation.
* Audit.
* Error file.
* Rollback/compensation plan.

---

# 59. Concurrency và chống tạo trùng

> Exact locking/constraint strategy thuộc Party Context DB design; business invariant phải được database-backed và kiểm thử bằng concurrent transactions.


## 59.1. Rủi ro

Hai request cùng lúc:

* Tạo Customer từ website.
* Sale tạo thủ công.
* Webhook gửi.
* Import chạy.

có thể cùng không thấy số và cùng tạo Customer.

## 59.2. Biện pháp

* Database unique constraint trên normalized phone.
* Local transaction.
* Lock theo Phone Identity.
* Upsert.
* Idempotency.
* Retry.
* Conflict handling.

## 59.3. Mô hình đề xuất

```text
phone_identities.normalized_phone UNIQUE
```

Nhiều Customer link chỉ được phép khi có `shared_phone_exception_id`.

## 59.4. Không chỉ dựa vào application check

Kiểm tra:

```text
SELECT rồi INSERT
```

không đủ nếu không có constraint.

---

# 60. Candidate database constraints — phải được xác nhận trong Alembic

> Các constraint expressions dưới đây là illustrative design input. Exact syntax, indexes và active-link representation thuộc approved migrations.


## 60.1. Phone Identity unique

```text
UNIQUE(enterprise_id, normalized_phone)
```

## 60.2. Link cùng Customer unique

```text
UNIQUE(customer_id, phone_identity_id, active_link_key)
```

## 60.3. Primary phone

Một partial unique constraint hoặc invariant service bảo đảm một primary active.

## 60.4. Shared link

Nhiều active Customer link tới cùng Phone Identity chỉ hợp lệ khi:

* Có active Shared Phone Exception.
* Customer nằm trong exception.
* Effective date hợp lệ.

---

# 61. Identity Check Log

Mọi lookup chính thức phải lưu:

* User/integration.
* Raw phone.
* Normalized phone.
* Phone Identity.
* Legal Entity context.
* Workflow source.
* Result code.
* Matched Customer count.
* Masking level.
* Action sau lookup.
* IP.
* Device.
* Request ID.
* Correlation ID.
* Timestamp.

## 61.1. Privacy

Raw phone trong log có thể:

* Encrypt.
* Tokenize.
* Mask theo quyền.
* Retention riêng.

---

# 62. SLA requirement classes và illustrative baselines

> Bảng thời gian dưới đây chỉ là `ILLUSTRATIVE BASELINE / PENDING VALIDATION`. Exact targets thuộc approved SLA Policy, Business Calendar và SLO/NFR documents.


## 62.1. Các SLA

* Identity check: real-time.
* Customer identification review.
* Shared phone review.
* Ownership change.
* Wrong phone correction.
* Simple merge.
* Complex merge.
* Restore conflict.
* Imported/historical duplicate review.
* Split request.
* Critical identity conflict.

## 62.2. Giá trị khởi tạo tham khảo

| Nghiệp vụ                          |       SLA tham khảo |
| ---------------------------------- | ------------------: |
| Identity check                     |            Tức thời |
| Customer selection shared phone    |               2 giờ |
| Wrong phone correction             | Trong ngày làm việc |
| Shared phone review                |     1 ngày làm việc |
| Simple merge                       |     1 ngày làm việc |
| Complex merge                      |     2 ngày làm việc |
| Ownership change                   |   1–2 ngày làm việc |
| Critical contract/payment conflict |        Ưu tiên khẩn |

Exact values phải được quản trị bằng approved Platform SLA Policy và Business Calendar.

## 62.3. Quá SLA

Có thể:

* Nhắc reviewer.
* Escalate.
* Chuyển assignee.
* Đưa dashboard.
* Yêu cầu giải trình.

Không tự:

* Merge.
* Approve shared phone.
* Transfer ownership.
* Restore Customer.

---

# 63. Notification

## 63.1. Sale

* Phone đã tồn tại.
* Lead được link Customer cũ.
* Shared phone cần chọn Customer.
* Yêu cầu shared phone bị duyệt/từ chối.
* Merge hoàn tất.
* Customer redirect.
* Ownership change hoàn tất.

## 63.2. Team Lead

* Conflict trong team.
* Shared phone pending.
* Sale lookup bất thường.
* Duplicate Customer ảnh hưởng Lead active.

## 63.3. CRM Admin

* New duplicate candidate.
* Imported-data identity conflict.
* Merge execution failed.
* Duplicate Phone Identity.
* Normalization rule conflict.
* Ownership change pending.

## 63.4. Finance/Legal

* Merge có Contract/Payment.
* Ownership change ảnh hưởng giao dịch.
* Split request.
* Identity conflict Critical.

## 63.5. Director

* Cross-Legal Entity conflict.
* Complex merge.
* Special data repair.
* Mass identity anomaly.

---

# 64. Permission Model

## 64.1. Sale

Được:

* Check phone trong workflow.
* Nhận masked result.
* Link Lead với Customer được xác định.
* Tạo resolution request.
* Tạo shared phone request.
* Tạo merge request.
* Tạo wrong phone correction request.

Không được:

* Xem full Customer ngoài scope.
* Merge.
* Duyệt shared phone.
* Chuyển ownership.
* Bypass check.
* Bulk lookup.
* Xem full identity logs.

## 64.2. Team Lead

Được:

* Xem case team.
* Review bằng chứng.
* Xử lý conflict đơn giản trong team.
* Escalate.

## 64.3. Department Head

Được:

* Xem case department.
* Phê duyệt theo policy.
* Xử lý tranh chấp cross-team.

## 64.4. CRM Admin/Data Steward

Được:

* Quản lý Phone Identity.
* Review duplicate.
* Lập merge plan.
* Thực thi merge đã duyệt.
* Chạy imported/historical-data scan.
* Sửa dữ liệu kỹ thuật.

Không mặc định quyết định tranh chấp thương mại hoặc tài chính.

## 64.5. Finance/Legal

Chỉ tham gia case liên quan phạm vi nghiệp vụ.

## 64.6. Director

Có quyền phê duyệt case phức tạp theo scope.

---

# 65. Candidate permission vocabulary — không phải Permission Registry canonical

> Exact permission codes, scopes, role mappings, SoD và masking rules thuộc security registries/matrices.


```text
customer_identity.check
customer_identity.view_result
customer_identity.view_masked_match
customer_identity.view_full_match
customer_identity.view_audit
customer_identity.view_sensitive_log
customer_identity.configure

phone_identity.view
phone_identity.create
phone_identity.correct
phone_identity.validate
phone_identity.block
phone_identity.archive
phone_identity.re_normalize

customer_phone.view
customer_phone.view_full
customer_phone.add
customer_phone.set_primary
customer_phone.deactivate
customer_phone.mark_wrong
customer_phone.view_history

shared_phone.request
shared_phone.view
shared_phone.review
shared_phone.approve
shared_phone.activate
shared_phone.suspend
shared_phone.revoke

phone_ownership_change.request
phone_ownership_change.view
phone_ownership_change.review
phone_ownership_change.approve
phone_ownership_change.execute

customer_duplicate.view
customer_duplicate.create_case
customer_duplicate.assign_case
customer_duplicate.review
customer_duplicate.resolve

customer_merge.request
customer_merge.view
customer_merge.preview
customer_merge.create_plan
customer_merge.review
customer_merge.approve
customer_merge.execute
customer_merge.view_audit
customer_merge.split_request
customer_merge.split_approve
customer_merge.split_execute

identity_historical_scan.view
identity_historical_scan.run
identity_historical_scan.approve
identity_data_repair.execute

organization_identity.check
organization_identity.review
organization_identity.merge
```

Các quyền kết hợp với:

```text
mine
team
department
legal_entity
all
```

---

# 66. Candidate user experiences — không phải exact frontend contract

> Exact routes, navigation, components và layouts thuộc Navigation/IA, Design System và Sprint Pack.


## 66.1. Phone Identity Lookup

* Nhập phone.
* Quốc gia.
* Kết quả chuẩn hóa.
* Match status.
* Masked Customer.
* Available actions.
* Lookup audit indicator.

## 66.2. Phone Identity Detail

* Normalized phone.
* Raw variants.
* Customer links.
* Verification.
* Usage.
* Shared exceptions.
* Ownership changes.
* Lookup history.
* Risk flags.

## 66.3. Customer Phone Management

* Danh sách phone.
* Primary.
* Active/inactive.
* Verification.
* Zalo.
* Shared.
* Source.
* History.
* Add/correct/deactivate.

## 66.4. Identity Resolution Center

Queue:

* Shared Phone.
* Ownership Change.
* Wrong Number.
* Duplicate Customer.
* Restore Conflict.
* Imported Data Conflict.
* Organization Conflict.
* Critical Conflict.

## 66.5. Duplicate Customer Comparison

So sánh:

* Identity.
* Phones.
* Emails.
* Addresses.
* Leads.
* Roles.
* Requirements.
* Financial Profiles.
* Seller/Owner Profiles.
* Relationships.
* Deals.
* Listings.
* Contracts.
* Payments.
* Consent.
* Notes.
* Access contexts.

## 66.6. Merge Preview

* Target Customer.
* Source Customer.
* Conflict.
* Resource impact.
* Proposed action.
* Blockers.
* Approval.
* Dry run result.

## 66.7. Shared Phone Center

* Active exceptions.
* Sắp hết hạn.
* Customer links.
* Relationship.
* Review date.
* Revoke.

## 66.8. Ownership Change Center

* Old Customer.
* New Customer.
* Effective date.
* Evidence.
* Business impact.
* Approval.
* Execution status.

## 66.9. Imported/Historical Data Scan Dashboard

* Total phones.
* Invalid phones.
* Duplicate groups.
* Shared candidates.
* Merge candidates.
* Contract/payment risk.
* Resolution progress.

---

# 67. Candidate dashboards — không phải certified Analytics contract

> Exact Metrics, dimensions, drill-down và certification thuộc Analytics Metric/Dashboard Registries.


## 67.1. CRM Admin

* Identity checks.
* New Phone Identity.
* Duplicate candidates.
* Shared phone requests.
* Ownership change requests.
* Merge pending.
* Merge failed.
* Imported-data conflicts.
* Invalid phone rate.
* Duplicate Phone Identity anomaly.

## 67.2. Management

* Duplicate Customer rate.
* Merge rate.
* Customer reused from existing identity.
* New vs returning Customer.
* Shared phone rate.
* Conflict SLA.
* Cross-department disputes.
* Data quality by source.

## 67.3. Security

* Bulk lookup.
* Sequential number probing.
* Out-of-scope match rate.
* Lookup without Lead creation.
* Abnormal integration traffic.
* Mask bypass attempts.

---

# 68. Candidate reports — không phải certified Metric definitions

> Report names dưới đây là product inventory. Exact formulas, grains, dimensions và access policies thuộc Analytics contracts.


* Identity check volume.
* Identity check result.
* New Customer allowed.
* Existing Customer linked.
* Out-of-scope matches.
* Invalid phone.
* Phone by country.
* Phone verification.
* Customer with no active phone.
* Customer with multiple phones.
* Multiple primary phone anomaly.
* Shared phone.
* Shared phone expiry.
* Ownership change.
* Wrong phone correction.
* Duplicate candidate.
* Duplicate resolution.
* Simple/complex merge.
* Merge impact.
* Merge failure.
* Split request.
* Imported/historical duplicate.
* Duplicate by source.
* Duplicate by import job.
* Duplicate by integration.
* Lookup by user.
* Anti-enumeration alert.
* Organization duplicate.
* Data quality trend.

Mọi báo cáo phải drill-down đúng scope và field permission.

---

# 69. Candidate data model — không phải physical schema canonical

> **Classification:** `CONTEXT-SPECIFIC DESIGN INPUT / PENDING VALIDATION`  
> Exact tables, columns, constraints và indexes chỉ có hiệu lực khi được khóa trong Party Context DB Specification và Alembic migrations.


## 69.1. Phone Identity

### `phone_identities`

* `id`
* `enterprise_id`
* `normalized_phone`
* `country_code`
* `country_calling_code`
* `national_number`
* `phone_type`
* `validation_status`
* `normalization_version`
* `shared_status`
* `risk_flags_json`
* `first_seen_at`
* `last_seen_at`
* `status`
* `created_at`
* `updated_at`

Unique:

```text
enterprise_id + normalized_phone
```

---

## 69.2. Raw Phone Variant

### `phone_identity_raw_variants`

* `id`
* `phone_identity_id`
* `raw_phone`
* `source_type`
* `source_id`
* `country_context`
* `first_seen_at`
* `last_seen_at`
* `occurrence_count`
* `created_at`

---

## 69.3. Customer Phone Link

### `customer_phone_links`

* `id`
* `customer_id`
* `phone_identity_id`
* `phone_usage_type`
* `is_primary`
* `is_zalo`
* `verification_status`
* `ownership_status`
* `shared_phone_exception_id`
* `status`
* `effective_from`
* `effective_to`
* `source_type`
* `source_id`
* `source_lead_id`
* `created_by`
* `approved_by`
* `created_at`
* `updated_at`

---

## 69.4. Phone Verification

### `phone_verification_events`

* `id`
* `customer_phone_link_id`
* `verification_type`
* `from_status`
* `to_status`
* `channel`
* `evidence_reference`
* `verified_by`
* `verified_at`
* `expires_at`
* `created_at`

---

## 69.5. Phone Correction

### `phone_correction_events`

* `id`
* `customer_phone_link_id`
* `correction_type`
* `old_value_snapshot`
* `new_phone_identity_id`
* `reason`
* `requested_by`
* `approved_by`
* `created_at`

---

## 69.6. Identity Check Log

### `identity_check_logs`

* `id`
* `enterprise_id`
* `legal_entity_id`
* `requester_type`
* `requester_id`
* `workflow_source`
* `raw_phone_encrypted`
* `normalized_phone`
* `phone_identity_id`
* `result_code`
* `matched_customer_count`
* `masking_level`
* `action_taken`
* `request_id`
* `correlation_id`
* `ip_address`
* `user_agent`
* `created_at`

---

## 69.7. Duplicate Candidate

### `customer_duplicate_candidates`

* `id`
* `candidate_code`
* `phone_identity_id`
* `customer_a_id`
* `customer_b_id`
* `detection_source`
* `supporting_evidence_json`
* `risk_level`
* `status`
* `created_at`
* `reviewed_at`
* `resolved_at`

---

## 69.8. Resolution Case

### `identity_resolution_cases`

* `id`
* `case_code`
* `case_type`
* `enterprise_id`
* `legal_entity_id`
* `phone_identity_id`
* `priority`
* `risk_level`
* `business_impact_json`
* `finance_impact_json`
* `legal_impact_json`
* `assigned_user_id`
* `sla_policy_id`
* `due_at`
* `status`
* `decision_code`
* `decision_reason`
* `created_by`
* `approved_by`
* `created_at`
* `resolved_at`

### `identity_resolution_case_customers`

* `id`
* `case_id`
* `customer_id`
* `role_in_case`
* `snapshot_json`
* `created_at`

### `identity_resolution_case_evidence`

* `id`
* `case_id`
* `evidence_type`
* `source_resource_type`
* `source_resource_id`
* `document_url`
* `description`
* `created_by`
* `created_at`

---

## 69.9. Shared Phone

### `shared_phone_exceptions`

* `id`
* `exception_code`
* `phone_identity_id`
* `exception_type`
* `relationship_type`
* `reason`
* `restrictions_json`
* `effective_from`
* `effective_to`
* `review_at`
* `status`
* `requested_by`
* `reviewed_by`
* `approved_by`
* `created_at`
* `updated_at`

### `shared_phone_exception_customers`

* `id`
* `shared_phone_exception_id`
* `customer_id`
* `customer_role`
* `is_primary_contact`
* `status`
* `created_at`

---

## 69.10. Ownership Change

### `phone_ownership_change_requests`

* `id`
* `request_code`
* `phone_identity_id`
* `old_customer_id`
* `new_customer_id`
* `effective_at`
* `change_reason`
* `evidence_json`
* `business_impact_json`
* `status`
* `requested_by`
* `reviewed_by`
* `approved_by`
* `executed_by`
* `created_at`
* `executed_at`

### `phone_ownership_change_events`

* `id`
* `request_id`
* `old_customer_phone_link_id`
* `new_customer_phone_link_id`
* `effective_at`
* `created_at`

---

## 69.11. Merge Request

### `customer_merge_requests`

* `id`
* `merge_code`
* `target_customer_id`
* `merge_type`
* `risk_level`
* `reason`
* `phone_overlap_summary`
* `status`
* `requested_by`
* `business_reviewed_by`
* `finance_reviewed_by`
* `legal_reviewed_by`
* `approved_by`
* `created_at`
* `approved_at`

### `customer_merge_request_sources`

* `id`
* `merge_request_id`
* `source_customer_id`
* `snapshot_json`
* `created_at`

---

## 69.12. Merge Plan

### `customer_merge_plans`

* `id`
* `merge_request_id`
* `plan_version`
* `target_customer_id`
* `resource_summary_json`
* `conflict_summary_json`
* `blocking_issue_count`
* `status`
* `created_by`
* `reviewed_by`
* `approved_by`
* `created_at`

### `customer_merge_plan_items`

* `id`
* `merge_plan_id`
* `source_customer_id`
* `resource_type`
* `resource_id`
* `proposed_action`
* `target_resource_id`
* `conflict_type`
* `resolution_json`
* `status`
* `created_at`

---

## 69.13. Merge Event

### `customer_merge_events`

* `id`
* `merge_request_id`
* `merge_plan_id`
* `target_customer_id`
* `execution_id`
* `status`
* `started_at`
* `completed_at`
* `executed_by`
* `error_summary`
* `created_at`

### `customer_merge_item_logs`

* `id`
* `merge_event_id`
* `source_customer_id`
* `resource_type`
* `resource_id`
* `action`
* `before_snapshot`
* `after_snapshot`
* `status`
* `error_message`
* `created_at`

### `customer_merge_redirects`

* `id`
* `source_customer_id`
* `target_customer_id`
* `merge_event_id`
* `effective_from`
* `status`
* `created_at`

---

## 69.14. Split Request

### `customer_merge_split_requests`

* `id`
* `split_code`
* `merge_event_id`
* `reason`
* `proposed_split_plan_json`
* `risk_level`
* `status`
* `requested_by`
* `reviewed_by`
* `approved_by`
* `executed_by`
* `created_at`
* `executed_at`

---

## 69.15. Identity Claim

### `party_identity_claims`

* `id`
* `party_id`
* `claim_type`
* `claim_value_encrypted`
* `normalized_value`
* `source_type`
* `source_id`
* `verification_status`
* `confidence_level`
* `effective_from`
* `effective_to`
* `evidence_document_id`
* `created_at`

---

## 69.16. Organization Registry

### `organization_identity_records`

* `id`
* `party_id`
* `country_code`
* `tax_code`
* `registration_number`
* `registry_namespace`
* `registry_id`
* `legal_name_normalized`
* `verification_status`
* `status`
* `created_at`

### `organization_duplicate_candidates`

* `id`
* `organization_a_party_id`
* `organization_b_party_id`
* `match_type`
* `match_details_json`
* `status`
* `created_at`
* `resolved_at`

---

## 69.17. Normalization Rule

### `phone_normalization_rule_sets`

* `id`
* `rule_set_code`
* `country_code`
* `version`
* `configuration_json`
* `status`
* `effective_from`
* `effective_to`
* `created_by`
* `approved_by`
* `created_at`

### `phone_renormalization_jobs`

* `id`
* `rule_set_id`
* `from_version`
* `to_version`
* `status`
* `total_count`
* `conflict_count`
* `processed_count`
* `created_by`
* `approved_by`
* `created_at`
* `completed_at`

---

# 70. Candidate application operations — không phải OpenAPI canonical

> Exact paths, methods, payloads, errors và authorization metadata thuộc OpenAPI/Error Registry.


## Phone Identity Check

```text
POST   /customer-identities/check-phone
POST   /customer-identities/check-phones
GET    /customer-identities/check-results/{reference}
GET    /phone-identities/{id}
GET    /phone-identities/{id}/history
```

## Customer Phone

```text
GET    /customers/{id}/phones
POST   /customers/{id}/phones
POST   /customer-phone-links/{id}/set-primary
POST   /customer-phone-links/{id}/deactivate
POST   /customer-phone-links/{id}/mark-wrong
POST   /customer-phone-links/{id}/verify
GET    /customer-phone-links/{id}/history
```

## Resolution Case

```text
GET    /identity-resolution-cases
POST   /identity-resolution-cases
GET    /identity-resolution-cases/{id}
POST   /identity-resolution-cases/{id}/assign
POST   /identity-resolution-cases/{id}/request-information
POST   /identity-resolution-cases/{id}/resolve
POST   /identity-resolution-cases/{id}/cancel
```

## Shared Phone

```text
GET    /shared-phone-exceptions
POST   /shared-phone-exceptions
GET    /shared-phone-exceptions/{id}
POST   /shared-phone-exceptions/{id}/submit-review
POST   /shared-phone-exceptions/{id}/approve
POST   /shared-phone-exceptions/{id}/activate
POST   /shared-phone-exceptions/{id}/suspend
POST   /shared-phone-exceptions/{id}/revoke
```

## Ownership Change

```text
GET    /phone-ownership-change-requests
POST   /phone-ownership-change-requests
GET    /phone-ownership-change-requests/{id}
POST   /phone-ownership-change-requests/{id}/review
POST   /phone-ownership-change-requests/{id}/approve
POST   /phone-ownership-change-requests/{id}/execute
POST   /phone-ownership-change-requests/{id}/reject
```

## Duplicate Customer

```text
GET    /customer-duplicate-candidates
GET    /customer-duplicate-candidates/{id}
POST   /customer-duplicate-candidates/{id}/open-case
POST   /customer-duplicate-candidates/{id}/mark-not-duplicate
POST   /customer-duplicate-candidates/{id}/resolve-shared-phone
```

## Merge

```text
GET    /customer-merge-requests
POST   /customer-merge-requests
GET    /customer-merge-requests/{id}
POST   /customer-merge-requests/{id}/analyze
POST   /customer-merge-requests/{id}/create-plan
GET    /customer-merge-requests/{id}/preview
POST   /customer-merge-requests/{id}/submit-review
POST   /customer-merge-requests/{id}/approve
POST   /customer-merge-requests/{id}/execute
GET    /customer-merge-events/{id}
GET    /customer-merge-events/{id}/reconciliation
```

## Split

```text
POST   /customer-merge-events/{id}/split-requests
GET    /customer-merge-split-requests/{id}
POST   /customer-merge-split-requests/{id}/analyze
POST   /customer-merge-split-requests/{id}/approve
POST   /customer-merge-split-requests/{id}/execute
```

## Imported/Historical Data Scan

```text
POST   /identity-historical-scans
GET    /identity-historical-scans/{id}
POST   /identity-historical-scans/{id}/dry-run
POST   /identity-historical-scans/{id}/approve
POST   /identity-historical-scans/{id}/execute
GET    /identity-historical-scans/{id}/results
```

## Organization Identity

```text
POST   /organization-identities/check
GET    /organization-duplicate-candidates
POST   /organization-duplicate-candidates/{id}/resolve
```

Backend phải tự enforce:

* Authenticated user.
* Legal Entity context.
* Permission.
* Scope.
* Field masking.
* Rate limit.
* Workflow.
* Approval.
* Effective date.
* Idempotency.
* Database constraint.
* Customer merge redirect.

---

# 71. Candidate business facts — không phải Event contracts canonical

> Exact Event names, envelopes, payloads, compatibility và channels thuộc JSON Schema, AsyncAPI và Event Registry.


Party Context có thể publish các candidate business facts sau:

```text
phone_identity.created
phone_identity.validated
phone_identity.invalidated
phone_identity.renormalized

customer_phone.linked
customer_phone.primary_changed
customer_phone.deactivated
customer_phone.marked_wrong
customer_phone.verified

customer_identity.match_found
customer_identity.out_of_scope_match
customer_identity.conflict_detected

shared_phone.requested
shared_phone.approved
shared_phone.activated
shared_phone.suspended
shared_phone.revoked

phone_ownership_change.requested
phone_ownership_change.approved
phone_ownership_change.executed

customer_duplicate.detected
customer_duplicate.resolved

customer_merge.requested
customer_merge.plan_created
customer_merge.approved
customer_merge.started
customer_merge.completed
customer_merge.failed
customer.canonical_changed

customer_merge_split.requested
customer_merge_split.completed

organization_duplicate.detected
organization_identity.merged
```

Consumer phải idempotent.

---

# 72. Candidate Platform configuration dependencies

> Configuration keys dưới đây là naming input. Exact definitions, schemas, scopes, resolution strategies và values thuộc Platform Configuration contracts.


```text
identity.phone_normalization_rule_set
identity.default_country_context
identity.phone_validation_policy
identity.phone_verification_policy

identity.customer_check_policy
identity.masking_policy
identity.lookup_rate_limit_policy
identity.anti_enumeration_policy
identity.identity_log_retention_policy

identity.shared_phone_workflow
identity.shared_phone_approval_policy
identity.shared_phone_expiration_policy

identity.phone_ownership_change_workflow
identity.phone_ownership_change_approval_policy

identity.customer_merge_workflow
identity.simple_merge_policy
identity.complex_merge_policy
identity.merge_approval_policy
identity.merge_split_policy

identity.historical_import_scan_policy
identity.data_repair_approval_policy
identity.organization_duplicate_policy

identity.resolution_sla_policy
identity.notification_policy
```

Mỗi cấu hình phải có:

* Scope.
* Version.
* Effective date.
* Approval.
* Audit.

---

# 73. System Invariant

Các quy tắc sau không được cấu hình tắt:

1. Customer cá nhân duplicate chính thức dựa trên Phone Identity overlap.
2. Một normalized phone chỉ có một Phone Identity trong Enterprise.
3. Backend luôn tự normalize phone.
4. Client không được quyết định normalized phone.
5. Không tạo Customer mới khi phone đã thuộc Customer hiện hữu trái rule.
6. Nhiều active Customer links tới một Phone Identity phải có shared exception.
7. Shared phone không được auto-merge.
8. Phone ownership change không chuyển lịch sử giao dịch.
9. Customer merge không xóa source Customer.
10. Customer merged không nhận nghiệp vụ mới.
11. Merge phải có transaction và audit.
12. Merge không được thực hiện từ frontend bằng thao tác update thông thường.
13. Import không được bỏ qua duplicate check.
14. Integration không được tự merge.
15. Identity lookup phải có rate limit và audit.
16. Out-of-scope match không được trả full Customer.
17. Phone inactive vẫn được kiểm tra duplicate.
18. Số cũ không bị xóa khỏi lịch sử.
19. Merge Contract/Payment không được làm mất snapshot pháp lý.
20. Special merge không phone overlap phải dùng tool đặc biệt có Director approval.

---

# 74. Rule nghiệp vụ bắt buộc

1. Một Customer có thể có nhiều phone.
2. Một Customer mặc định có một primary phone active.
3. Một Phone Identity mặc định chỉ có một Customer active.
4. Shared phone cần exception.
5. Sale không tự duyệt shared phone.
6. Phone phải normalize trước khi so sánh.
7. Lưu raw và normalized phone.
8. Số Việt Nam `0`, `84` và `+84` phải normalize nhất quán.
9. Số nước ngoài cần country context.
10. Invalid phone không tạo Customer chính thức tự động.
11. Unverified phone vẫn phải duplicate check.
12. Số inactive vẫn phải duplicate check.
13. Customer create trực tiếp không được né duplicate.
14. Lead create phải gọi identity service.
15. Import phải check trong file và database.
16. API phải hỗ trợ idempotency.
17. Technical duplicate không tạo Lead/Customer lặp.
18. New Lead cho Customer cũ vẫn được ghi nhận.
19. Source Lead không bị mất khi link Customer.
20. Customer ngoài scope phải mask.
21. Backend không trả full data rồi frontend che.
22. Không trả Customer ID thật nếu không cần.
23. Lookup phải được audit.
24. Mass lookup phải bị cảnh báo.
25. Phone đã có trên cùng Customer không tạo link trùng.
26. Phone thuộc Customer khác phải chặn mặc định.
27. Add phone conflict phải tạo Resolution Case.
28. Không overwrite Phone Identity link khi sửa số.
29. Số cũ phải inactivate hoặc mark wrong.
30. Thay primary phải giữ lịch sử.
31. Shared phone không tự chọn Customer cho Lead.
32. Shared phone phải có manual selection hoặc resolution.
33. Shared exception phải có effective date.
34. Shared exception có thể bị revoke.
35. Ownership change phải có bằng chứng.
36. Ownership change phải có effective date.
37. Ownership change không chuyển Lead cũ.
38. Ownership change không chuyển Contract/Payment.
39. Wrong number khác Ownership change.
40. Duplicate Candidate không tự merge.
41. Merge thường phải có phone overlap.
42. Shared phone active ngăn merge thông thường.
43. Customer chính không mặc định là Customer cũ nhất.
44. Chọn target phải có reason.
45. Merge Preview phải hiển thị resource impact.
46. Merge có blocker không được execute.
47. Financial Profile không được tự cộng khi merge.
48. Duplicate Requirement không được tự merge.
49. Care protection phải được `lead` Context giải quyết.
50. Deal conflict phải được giải quyết trước hoặc trong plan.
51. Contract snapshot không được thay âm thầm.
52. Consent hạn chế hơn phải được giữ.
53. Opt-out không bị mất khi merge.
54. Notes giữ source Customer.
55. External IDs phải giữ alias.
56. Merge source phải redirect target.
57. Merge source không được restore thông thường.
58. Merge execution phải idempotent.
59. Merge failure phải có reconciliation.
60. Split không phải Undo đơn giản.
61. Split cần approval và dry run.
62. Imported/historical-data scan không auto-merge.
63. Re-normalization phải có dry run.
64. Duplicate Phone Identity là lỗi Critical.
65. Database phải có unique constraint.
66. Application check không thay database constraint.
67. Shared link phải tham chiếu exception.
68. Customer tổ chức không dùng phone-only.
69. Tax code conflict tổ chức phải review.
70. Hotline chung không đủ để merge organization.
71. Related Party conversion phải identity check.
72. Person/Employee/Customer không bị merge sai loại.
73. Identity Verification không thay duplicate rule.
74. CCCD không tự kích hoạt merge thông thường.
75. Identity conflict Critical có thể chặn nghiệp vụ nhạy cảm.
76. CRM Admin không mặc định quyết định tranh chấp kinh doanh.
77. Finance chỉ tham gia case có ảnh hưởng tài chính.
78. Legal chỉ tham gia case có ảnh hưởng pháp lý.
79. View không đồng nghĩa Export.
80. Sale không được bulk lookup hoặc export identity.
81. Query scope phải enforce ở backend.
82. Không tải toàn Customer rồi lọc frontend.
83. Every merge item phải có log.
84. Audit không được sửa.
85. Domain event phải có version.
86. Consumer phải idempotent.
87. Customer 360 phải dùng canonical Customer.
88. Dashboard phải drill-down đúng scope.
89. User offboard không làm mất identity history.
90. Handover không chuyển ownership phone.
91. Merge không tự thay commission attribution.
92. Merge không tự thay sale cũ.
93. Merge không tự thay Customer source.
94. Phone correction phải lưu reason.
95. Verification phải lưu actor.
96. Shared phone hết hạn phải được review.
97. Exception bị suspend phải chặn link mới.
98. Archived Customer vẫn được identity lookup.
99. Soft-deleted Customer vẫn được identity lookup.
100. Capability phải phục vụ thống nhất mọi Legal Entity trong Enterprise.

---

# 75. Cảnh báo và phát hiện bất thường

Hệ thống cần cảnh báo khi:

* Hai Phone Identity có cùng normalized phone.
* Một Phone Identity có nhiều active Customer links không có exception.
* Customer có nhiều primary phone.
* Customer không có phone active.
* Shared phone exception hết hạn.
* Shared phone có Customer ngoài danh sách approved.
* Ownership change lặp lại nhiều lần.
* Phone chuyển ownership ngay trước Contract/Payment.
* User lookup hàng loạt.
* User lookup tuần tự số.
* User có nhiều out-of-scope matches.
* Lookup không dẫn đến Lead hoặc case.
* Integration tạo duplicate tăng đột biến.
* Import duplicate rate cao.
* Re-normalization tạo conflict.
* Merged Customer nhận Lead mới.
* Merged Customer bị update.
* Merge có Payment chưa review.
* Merge có Contract chưa review.
* Merge execution thất bại.
* Merge item reconciliation lệch.
* Customer source bị restore sau merge.
* Split request không đủ bằng chứng.
* Organization tax code trùng.
* Individual Customer không được merge thiếu Phone Identity overlap bằng workflow thông thường.
* Sale tự tạo và tự duyệt shared phone.
* CRM Admin tự duyệt merge phức tạp.
* Identity log retention bị tắt.
* API cố gửi normalized phone khác với kết quả backend.
* Same idempotency key có payload khác.
* Phone marked wrong nhưng vẫn primary.
* Invalid phone được dùng tạo Contract.
* Shared phone Lead bị auto-link sai Customer.
* Customer archived có phone được tạo Customer mới.
* Search response lộ full Customer ngoài scope.

---

# 76. Audit Log

## 76.1. Thao tác bắt buộc

* Identity check.
* Normalize.
* Create Phone Identity.
* Link phone.
* Set primary.
* Deactivate phone.
* Mark wrong.
* Verify phone.
* Shared phone request/review/approval/revoke.
* Ownership change request/review/execute.
* Duplicate candidate creation.
* Resolution decision.
* Merge request.
* Merge preview.
* Merge approval.
* Merge execution.
* Merge failure.
* Merge redirect.
* Split request.
* Data repair.
* Imported/historical-data scan.
* Re-normalization.
* Organization identity merge.
* Sensitive identity lookup.
* Bulk lookup/export.

## 76.2. Nội dung

* Actor.
* Role.
* Legal Entity.
* Customer.
* Phone Identity.
* Raw phone masked/encrypted.
* Normalized phone.
* Result code.
* Before.
* After.
* Reason.
* Evidence.
* Workflow version.
* Approval.
* IP.
* Device.
* Request ID.
* Correlation ID.
* Idempotency key.
* Timestamp.
* Result.

---

# 77. Candidate baseline delivery scope

> Phần này mô tả product baseline/advanced outcomes. Nó không tự kích hoạt Sprint hoặc khóa implementation order; exact scope thuộc Roadmap và current Sprint Pack.


## 77.1. Product baseline outcomes

* Phone Identity.
* Vietnamese phone normalization.
* Basic international phone support.
* Raw phone storage.
* Unique normalized phone constraint.
* Customer Phone Link.
* Multiple phones per Customer.
* One primary phone.
* Phone active/inactive.
* Phone verification basic.
* Customer check toàn Enterprise.
* Direct create check.
* Lead integration.
* Import check.
* API idempotency.
* Masked result.
* Out-of-scope protection.
* Shared phone request/approval.
* Shared phone manual Customer selection.
* Wrong phone correction.
* Ownership change cơ bản.
* Duplicate Candidate.
* Resolution Case.
* Simple merge.
* Complex merge review.
* Merge Preview.
* Transactional merge.
* Merge redirect.
* Audit.
* Rate limit.
* Anti-enumeration basic.
* Imported/historical-data scan report.
* Organization tax code check cơ bản.
* Dashboard và alert cơ bản.

## 77.2. Advanced outcomes

* Multi-country normalization nâng cao.
* Carrier verification.
* OTP verification.
* eKYC.
* Advanced identity claims.
* Automated organization registry.
* Advanced merge simulation.
* Self-service split tool.
* Data lineage visualization.
* Identity graph.
* Fraud detection.
* Privacy-preserving lookup.
* Tokenized phone search.
* Cross-system identity federation.
* Automated anomaly scoring.
* Enterprise-wide historical re-normalization.
* Advanced shared household modeling.

---

# 78. Capability acceptance outcomes

> Các outcomes dưới đây phải được trace sang PRD requirements, Context use cases, contracts, tests và Acceptance Evidence trước khi được coi là Accepted.


Capability được xem là đáp ứng khi:

1. Tạo được Phone Identity.
2. Normalized phone unique toàn Enterprise.
3. Lưu được raw phone.
4. Lưu normalization version.
5. `0912 345 678` và `+84912345678` trả cùng Phone Identity.
6. Số nước ngoài dùng đúng country context.
7. Invalid phone được phân loại.
8. Invalid phone không tự tạo Customer.
9. Customer có nhiều phone.
10. Customer có một primary phone active.
11. Phone cũ được inactivate.
12. Phone cũ không bị xóa.
13. Phone unverified vẫn được duplicate check.
14. Phone inactive vẫn được duplicate check.
15. Tạo Customer trực tiếp chạy identity check.
16. Tạo Lead chạy identity check.
17. Import chạy identity check.
18. API backend tự normalize.
19. Client normalized value không được tin.
20. Không tìm thấy phone thì cho tạo Customer.
21. Tìm thấy cùng Customer không tạo link trùng.
22. Tìm thấy Customer khác thì chặn.
23. Out-of-scope match được mask.
24. Không lộ full Customer ID ngoài scope.
25. Existing Customer được link với Lead.
26. Lead source vẫn được giữ.
27. New Lead cho Customer cũ không bị coi technical duplicate.
28. External event lặp không tạo Lead trùng.
29. Import duplicate trong file được phát hiện.
30. Import không tạo Customer rồi merge sau.
31. Hai request đồng thời không tạo hai Phone Identity.
32. Database constraint ngăn race condition.
33. Same idempotency key trả cùng kết quả.
34. Same key payload khác báo conflict.
35. Tạo được Shared Phone Request.
36. Sale không tự duyệt shared phone.
37. Shared exception có nhiều Customer.
38. Shared link dùng cùng Phone Identity.
39. Shared phone lookup yêu cầu chọn Customer.
40. Shared phone không auto-link Lead.
41. Shared phone không auto-merge.
42. Shared exception có ngày hiệu lực.
43. Shared exception hết hạn được cảnh báo.
44. Shared exception revoke được.
45. Tạo được Ownership Change Request.
46. Ownership change cần approval.
47. Ownership change đóng link cũ.
48. Ownership change tạo link mới.
49. Ownership change giữ lịch sử Customer cũ.
50. Ownership change không chuyển Contract.
51. Ownership change không chuyển Payment.
52. Wrong phone được xử lý riêng.
53. Phone correction giữ audit.
54. Tạo được Duplicate Candidate.
55. Candidate không tự merge.
56. Tạo được Resolution Case.
57. Case có SLA.
58. Case có evidence.
59. Tạo được Merge Request.
60. Merge thông thường yêu cầu phone overlap.
61. Shared phone ngăn merge thông thường.
62. Merge Preview hiển thị Leads.
63. Merge Preview hiển thị Requirements.
64. Merge Preview hiển thị Deals.
65. Merge Preview hiển thị Contracts.
66. Merge Preview hiển thị Payments.
67. Merge Preview hiển thị Financial Profiles.
68. Merge Preview hiển thị Consent.
69. Chọn được target Customer.
70. Target selection có reason.
71. Merge blocker ngăn execute.
72. Simple merge thực hiện được.
73. Complex merge có Finance/Legal review.
74. Merge chạy trong transaction.
75. Merge source chuyển `MERGED`.
76. Merge source redirect target.
77. Merge source không nhận Lead mới.
78. Merge giữ source attribution.
79. Merge không tự cộng Financial Profile.
80. Merge không tự merge duplicate Requirement.
81. Merge giữ Contract snapshot.
82. Merge giữ Payment.
83. Merge không đổi Commission attribution.
84. Consent hạn chế hơn được giữ.
85. Opt-out không bị mất.
86. External ID source được giữ.
87. Merge item có audit log.
88. Merge lỗi có reconciliation.
89. Merge execution idempotent.
90. Split Request tạo được.
91. Split cần approval.
92. Split có dry run.
93. Imported/historical-data scan phát hiện duplicate groups.
94. Imported/historical-data scan không auto-merge.
95. Re-normalization có dry run.
96. Re-normalization phát hiện conflict.
97. Organization Customer check tax code được.
98. Organization cùng hotline không tự merge.
99. Related Party Stub conversion chạy identity check.
100. Identity lookup có rate limit.
101. Bulk lookup bị giới hạn.
102. Sequential probing bị cảnh báo.
103. Lookup có audit.
104. Sensitive log được bảo vệ.
105. Sale chỉ xem masked result ngoài scope.
106. Team Lead xem case team.
107. CRM Admin lập merge plan được.
108. CRM Admin không tự duyệt merge phức tạp trái policy.
109. Finance chỉ review case tài chính.
110. Legal chỉ review case pháp lý.
111. Director duyệt special data repair được.
112. View không cho export.
113. Sale không bulk export identity.
114. Backend enforce scope.
115. Sửa URL không mở rộng quyền.
116. Dashboard drill-down đúng scope.
117. Audit lưu before/after.
118. Audit không sửa được.
119. Domain event được phát.
120. Event consumer idempotent.
121. Customer 360 hiển thị canonical Customer.
122. Customer merged source có banner redirect.
123. Archived Customer vẫn được identity check.
124. Soft-deleted Customer vẫn được identity check.
125. Customer không bị tạo trùng qua Legal Entity khác.
126. Capability hỗ trợ Buyer Customer.
127. Capability hỗ trợ Seller/Owner Customer.
128. Capability hỗ trợ Customer tổ chức.
129. capability hỗ trợ dữ liệu được nhập hoặc dữ liệu lịch sử đã được phê duyệt.
130. Capability bảo đảm một danh tính Customer thống nhất toàn Enterprise.

---

# 79. Anti-patterns và canonical requirements

Các nội dung dưới đây là anti-pattern bị cấm và canonical requirements hiện hành của dự án Greenfield.

## AP-IDG-001 — Lưu normalized phone trực tiếp trên Customer

**Không được áp dụng**

Customer record chứa normalized phone như identity authority và các workflows tự cập nhật giá trị đó.

**Canonical requirement**

Phone phải được quản lý qua Phone Identity và Customer–Phone relationship trong Party Context, có normalization version, history và concurrency protection.

## AP-IDG-002 — Unique phone link không hỗ trợ Shared Phone

**Không được áp dụng**

Đặt uniqueness trực tiếp trên Customer phone field khiến một số không thể được dùng chung trong ngoại lệ hợp lệ.

**Canonical requirement**

Phone Identity vẫn unique; nhiều active Customer relationships chỉ hợp lệ khi có approved Shared Phone Exception còn hiệu lực.

## AP-IDG-003 — Tên, email hoặc giấy tờ tự động kết luận duplicate cá nhân

**Không được áp dụng**

Fuzzy score từ tên/email/địa chỉ/giấy tờ tự merge Individual Customer.

**Canonical requirement**

Theo accepted product policy, duplicate candidate chính thức của Individual Customer dựa trên Phone Identity overlap. Các thuộc tính khác chỉ hỗ trợ review, trừ controlled exceptional repair.

## AP-IDG-004 — Frontend hoặc integration quyết định normalized phone

**Không được áp dụng**

Client gửi `normalized_phone` và backend tin giá trị đó.

**Canonical requirement**

Backend phải normalize bằng approved rule version và không cho client mở rộng identity authority.

## AP-IDG-005 — Check rồi insert không có database guard

**Không được áp dụng**

Application `SELECT` rồi `INSERT` mà không có unique constraint/atomic mechanism.

**Canonical requirement**

Critical uniqueness phải có database-backed constraint/locking/upsert strategy và real concurrency tests.

## AP-IDG-006 — Customer mới được tạo để né masked match

**Không được áp dụng**

Actor không thấy full Customer nên tạo Customer khác.

**Canonical requirement**

Out-of-scope match phải chặn duplicate creation và trả masked/opaque outcome với approved next actions.

## AP-IDG-007 — Shared Phone tự chọn Customer

**Không được áp dụng**

Lead/integration tự link một Customer bất kỳ khi Phone Identity có nhiều approved Customer relationships.

**Canonical requirement**

Shared Phone yêu cầu context-aware selection hoặc Identity Resolution Case; không auto-link và không auto-merge.

## AP-IDG-008 — Phone Ownership Change chuyển lịch sử

**Không được áp dụng**

Khi số đổi người sử dụng, Lead/Contract/Payment/Timeline cũ chuyển sang Customer mới.

**Canonical requirement**

Ownership Change chỉ thay effective Phone relationship. Historical business records vẫn thuộc Customer cũ.

## AP-IDG-009 — Wrong Number thay cho Ownership Change

**Không được áp dụng**

Dùng correction đơn giản để xóa dấu vết số từng thuộc Customer thật.

**Canonical requirement**

Wrong Number, inactive/replaced phone, Shared Phone và Ownership Change là các semantics khác nhau, có workflow và evidence riêng.

## AP-IDG-010 — Merge là delete hoặc overwrite

**Không được áp dụng**

Xóa source Customer hoặc ghi đè target mà không giữ lineage.

**Canonical requirement**

Merge tạo canonical redirect, giữ source identity/history, không nhận nghiệp vụ mới trên source và có reconciliation.

## AP-IDG-011 — Merge xuyên Context trong một transaction

**Không được áp dụng**

Party Context lock và direct-update Lead, Deal, Contract, Payment, Revenue và Commission trong cùng database transaction.

**Canonical requirement**

Party commit local canonical merge; downstream Contexts consume durable Event idempotently; Process Manager theo dõi completion và reconciliation. Không dùng distributed transaction.

## AP-IDG-012 — Merge tự cộng/gộp financial data

**Không được áp dụng**

Cộng Financial Profiles, Payments, Revenue hoặc Commission chỉ vì Customer merge.

**Canonical requirement**

Financial/legal facts giữ source, context và immutable evidence. Mọi correction cần owning Context authority.

## AP-IDG-013 — Consent rộng hơn thắng khi merge

**Không được áp dụng**

Giữ consent thuận tiện hơn và bỏ opt-out/restriction.

**Canonical requirement**

Resolution phải tôn trọng policy hạn chế hơn theo purpose/channel cho đến khi có lawful correction.

## AP-IDG-014 — Organization duplicate dùng phone-only

**Không được áp dụng**

Merge Organization Customer chỉ vì cùng hotline.

**Canonical requirement**

Organization identity dùng tax/registration/registry identifiers theo country/namespace; legal name/hotline chỉ hỗ trợ review.

## AP-IDG-015 — Identity lookup là search API toàn công ty

**Không được áp dụng**

Cho phép bulk/sequential probing hoặc trả full Customer outside scope.

**Canonical requirement**

Lookup phải workflow-bound, rate-limited, audited, masked/opaque và có anomaly detection.

## AP-IDG-016 — Candidate examples là exact contracts

**Không được áp dụng**

Dùng tables, endpoint paths, result codes, permission codes, state lists hoặc Event names trong Capability Specification để code trực tiếp.

**Canonical requirement**

Exact implementation phải được khóa trong Party Context Pack, Alembic, OpenAPI, JSON Schema/AsyncAPI và security registries.

## AP-IDG-017 — Scan dữ liệu lịch sử tự auto-merge

**Không được áp dụng**

Batch scan tự hợp nhất Customer dựa trên Phone overlap hoặc fuzzy evidence.

**Canonical requirement**

Approved scan chỉ tạo candidates, evidence và review queue. Merge vẫn phải qua workflow và impact analysis.

## AP-IDG-018 — Mặc định có hệ thống tiền nhiệm hoặc migration

**Không được áp dụng**

Suy luận rằng có CRM cũ, dữ liệu cần migrate hoặc compatibility layer bắt buộc.

**Canonical requirement**

`crm_bds_ai` là Greenfield. Import/migration/repair chỉ tồn tại khi có approved scope, mapping, reconciliation, security review và acceptance criteria riêng.

---

# 80. Kết luận

Customer Identity Governance Capability bảo vệ canonical Party/Customer identity của `crm_bds_ai`.

Capability phải bảo đảm:

- Một normalized phone ánh xạ tới một Phone Identity trong accepted enterprise boundary.
- Một Customer có thể có nhiều Phone Identities nhưng mọi thay đổi đều có history và effective period.
- Duplicate creation bị ngăn ở direct create, Lead, import và integration flows.
- Shared Phone được hỗ trợ bằng approved exception mà không phá identity uniqueness.
- Shared Phone không dẫn đến auto-link hoặc auto-merge sai.
- Phone Ownership Change không chuyển lịch sử giao dịch.
- Identity lookup ngoài scope không làm lộ dữ liệu.
- Anti-enumeration, rate limiting, masking và Audit được áp dụng.
- Customer Merge giữ source, redirect, lineage và reconciliation.
- Cross-context merge không dùng distributed transaction hoặc direct writes.
- Contract, Payment, Receipt, Revenue và Commission không bị thay nghĩa khi merge.
- Organization identity có registry policy riêng.
- Customer 360 và các Context nghiệp vụ luôn resolve cùng canonical Customer.
- Imported/historical data repair không được mặc định và không auto-merge.
- Mọi sensitive decision có owner, approval, evidence và Audit.

> Customer Identity Governance là một capability slice trong `party` Context, không phải identity service độc lập cạnh tranh với Customer 360 và không phải công cụ fuzzy deduplication tự động.
