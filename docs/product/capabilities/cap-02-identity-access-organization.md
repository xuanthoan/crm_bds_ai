# CRM_BDS_AI — CAPABILITY 02: IDENTITY, ACCESS AND ORGANIZATION

## Quản lý tổ chức, Workforce Identity, User Accounts, Authorization và Handover

**Document ID:** `PROD-CAP-IAM-001`  
**Canonical path:** `docs/product/capabilities/cap-02-identity-access-organization.md`  
**Product:** `crm_bds_ai`  
**Version:** `1.0.0`  
**Status:** `Accepted / Product Capability Baseline`  
**Document type:** `Product Capability Specification`  
**Primary capability code:** `CAP-IAM`  
**Primary owning Context:** `iam`  
**Owner:** `Product Owner`  
**Co-owner:** `IAM Domain Owner`  
**Reviewers:** `Architecture Owner`, `Security Owner`, `Platform Domain Owner`, `Party Domain Owner`, `Database Owner`, `API Owner`, `QA Owner`, `Operations Owner`  
**Effective date:** `2026-08-05`  
**Last reviewed:** `2026-08-05`  
**Classification:** `INTERNAL`

---

# 0. Phạm vi thẩm quyền và quan hệ tài liệu

Tài liệu này là nguồn canonical cho:

- Product outcomes của Identity, Access and Organization Capability.
- Khái niệm Workforce, User Account, Service Account, Employment Assignment và Organizational Unit.
- Authorization outcomes theo capability, effective scope, resource relationship và field policy.
- Delegation, temporary access, access review, onboarding, transfer, leave, offboarding và handover.
- Business rules, system invariants, anti-patterns và acceptance outcomes của capability.
- Đầu vào phân tích cho IAM Context Implementation Pack.

Tài liệu này không phải nguồn exact cho:

- Physical database schema hoặc DDL.
- Exact API paths, payloads hoặc error contracts.
- Exact Event names, envelopes hoặc payloads.
- Exact permission codes, role bundles, scope vocabulary hoặc field-masking rules.
- Exact authentication/session/MFA configuration.
- Exact approval limits, SLA values hoặc organizational hierarchy.
- Exact Sprint implementation.

Nguồn exact tương ứng:

| Chủ đề | Nguồn canonical |
|---|---|
| Thuật ngữ | Domain Glossary |
| Product requirements | PRD |
| Context ownership | Source of Truth Matrix |
| Architecture boundaries | Architecture Overview, Context Map và Accepted ADRs |
| IAM behavior chi tiết | IAM Context Implementation Pack |
| Canonical Party/Person identity | Party Context Implementation Pack |
| Database | Alembic migrations và Context DB Specification |
| API | OpenAPI |
| Events | JSON Schema, AsyncAPI và Event Registry |
| Permissions | Permission Registry |
| Scopes | Scope Resolution Specification |
| Field access/masking | Field Masking Matrix |
| SoD | Segregation of Duties Matrix |
| Authentication/session/MFA | Security Architecture và environment configuration |
| Current work | Current Sprint Detailed Execution Pack |

**Capability không đồng nghĩa Bounded Context.** Capability này chủ yếu được thực hiện bởi `iam` Context và phối hợp với `platform`, `party`, `lead`, `product`, `transaction`, `contract`, `revenue`, `activity`, `audit`, `integration` và `operations`.

Các phần “candidate data model”, “candidate application operations”, “candidate permission vocabulary”, “candidate scope vocabulary” và “candidate business facts” trong tài liệu này chỉ là đầu vào thiết kế. Chúng không được dùng thay machine-readable contracts hoặc registries đã được chấp nhận.

---

# 1. Mục tiêu của capability

Identity, Access and Organization Capability quản lý cơ cấu tổ chức, workforce identity, user/service accounts, authorization, access governance và trách nhiệm vận hành trong `crm_bds_ai`.

Capability phải trả lời được:

- Chủ thể đang đăng nhập là ai?
- Chủ thể là human user, external user hay service account?
- Workforce relationship và active assignments nào đang có hiệu lực?
- Chủ thể đang hoạt động trong Legal Entity và organizational context nào?
- Chủ thể có capability/permission nào?
- Effective scope của permission là gì?
- Resource relationship nào cho phép hoặc từ chối truy cập?
- Field nào được ẩn, che, đọc hoặc cập nhật?
- Project/Listing access nào đang có hiệu lực?
- Approval authority, hạn mức và SoD áp dụng thế nào?
- Delegation, temporary access hoặc emergency access nào đang có hiệu lực?
- Khi transfer, leave hoặc offboarding, trách nhiệm và access phải thay đổi thế nào?
- Business resources nào cần handover và owning Context nào phải thực hiện reassignment?
- Nguồn gốc của từng quyền hiệu lực là gì?
- Session, device hoặc access behavior nào cần cảnh báo?

Capability hỗ trợ:

- Một doanh nghiệp hoặc nhóm doanh nghiệp nội bộ có nhiều Legal Entity.
- Một Workforce có thể có nhiều Employment Assignment theo thời gian.
- Assignment chính, kiêm nhiệm, tạm thời, dự án và cross-entity.
- Organizational hierarchy và matrix organization có effective dates.
- Position, Job Function và manager relationships.
- Role/permission/scope/field policy có version và effective period.
- Project Access, Listing Access và Share Grant.
- Delegation, temporary access, just-in-time access và emergency access.
- Approval Authority và SoD.
- Onboarding, probation, transfer, leave, offboarding và handover.
- Session/device control, MFA/re-authentication policy references và security-risk response.
- Export access tách biệt với view access.
- Audit và permission explanation.

Capability không sở hữu:

- Canonical Party, Customer hoặc Customer Identity: `party`.
- Lead: `lead`.
- Asset, Listing, Availability hoặc Commercial Lock: `product`.
- Deal, Hold hoặc Booking: `transaction`.
- Contract, Payment, Receipt, Refund hoặc Settlement: `contract`.
- Revenue hoặc Commission: `revenue`.
- Task, Appointment hoặc Interaction: `activity`.
- Immutable Audit facts: `audit`.
- Integration runtime: `integration`.
- Jobs, incidents hoặc recovery runtime: `operations`.

IAM cung cấp authenticated identity, effective authorization, workforce/organization context và governance decisions để owning Context thực hiện nghiệp vụ an toàn.

---

# 2. Quan hệ với Platform Configuration Capability

IAM phụ thuộc vào các definitions và policy references thuộc `platform`, nhưng không sao chép source of truth của Platform.

## 2.1. Enterprise và Legal Entity

Platform Context sở hữu Enterprise Profile và Legal Entity Profile.

IAM sở hữu:

- Workforce relationship với Legal Entity.
- Employment Assignment.
- Organizational Unit, Position và manager relationships.
- User/service-account context.
- Role/permission assignments.
- Access governance.
- Delegation và approval authority.
- Transfer, leave, offboarding và handover coordination.

IAM chỉ lưu reference/snapshot cần thiết; không tạo Legal Entity master cạnh tranh.

## 2.2. Business Calendar

IAM tham chiếu Business Calendar definition/version từ Platform cho:

- Working schedule.
- Leave coverage.
- Delegation period.
- Handover SLA.
- Escalation.
- Effective-date calculation.

Candidate inheritance order có thể gồm:

```text
User override
→ Employment Assignment
→ Team
→ Department
→ Branch
→ Legal Entity
→ Enterprise default
```

Exact allowed levels và resolution strategy thuộc Configuration Definition và Platform Context Pack.

## 2.3. Approval Policy

Access grant, critical permission, delegation, transfer, offboarding hoặc emergency access có thể cần Approval Policy từ Platform.

Approval runtime phải giữ:

- Policy/version.
- Requester và beneficiary.
- Resource/action.
- Authority snapshot.
- Reason.
- Effective period.
- Decision evidence.

Exact approval runtime ownership thuộc Context Map và Platform/IAM Context Packs.

## 2.4. Workflow Definition

IAM sử dụng versioned Workflow Definitions cho:

- Onboarding.
- Role/access grant.
- Transfer.
- Leave.
- Delegation.
- Handover.
- Offboarding.
- Access review.
- Security suspension và recovery.

IAM vẫn sở hữu Domain command, aggregate transition và invariants; generic workflow không direct-write IAM state.

## 2.5. Notification Policy

Platform cung cấp notification policy/template definitions. Runtime delivery thuộc designated runtime owner.

IAM phát sinh notification intents cho:

- Invitation/activation.
- Role/access changes.
- Delegation start/expiry.
- Leave/handover.
- Account lock.
- Security anomaly.
- Access review.
- Offboarding.

## 2.6. Numbering Scheme

IAM có thể tham chiếu Numbering Scheme cho employee, request, delegation, handover hoặc offboarding codes.

Exact format là Context/Legal-specific decision, không phải universal rule.

## 2.7. Feature Configuration

Feature configuration có thể điều khiển rollout của optional capabilities như:

- Multiple Employment Assignments.
- Project/Listing-level access.
- Just-in-time access.
- Device trust.
- Automated access review.
- Advanced ABAC.
- Emergency access.

Feature configuration không được tắt backend authorization, Audit, expiry enforcement, SoD critical controls hoặc session revocation.

---

# 3. Nguyên tắc thiết kế cốt lõi

## 3.1. Party/Person identity, Workforce và User Account là các khái niệm khác nhau

### Canonical Party/Person identity

Canonical identity của cá nhân hoặc tổ chức thuộc `party` Context theo Source of Truth Matrix.

IAM không được tạo một Person master cạnh tranh. IAM có thể lưu:

- `party_id` hoặc approved identity reference.
- Authentication subject reference.
- Minimal display/contact snapshot khi policy cho phép.
- Workforce-specific attributes không thuộc Party.

### Workforce Profile

Workforce Profile mô tả quan hệ làm việc giữa một human Party và doanh nghiệp.

Một Workforce có thể:

- Chưa có User Account.
- Có nhiều Employment Assignment.
- Nghỉ việc nhưng vẫn cần historical reference.
- Vẫn là participant/beneficiary của historical Commission theo Revenue policy.
- Có external HR reference.

### User Account

User Account là security principal dùng để authentication và authorization.

Một human Party có thể:

- Có Workforce Profile nhưng chưa có tài khoản.
- Có một hoặc nhiều linked external identities theo approved authentication model.
- Bị deactivated mà Workforce/history vẫn tồn tại.
- Đồng thời là Customer, nhưng Customer role thuộc Party Context.

Service Account không phải human Party và phải có owner chịu trách nhiệm.

---

## 3.2. Chức danh không đồng nghĩa với quyền

Ví dụ:

* “Trưởng phòng kinh doanh” là chức danh.
* `deal.view` với scope `department` là quyền.
* `discount.approve` đến hạn mức 100 triệu là approval authority.
* `export.customer` là quyền riêng.

Không hardcode:

```text
Nếu chức danh = Trưởng phòng thì được xem toàn phòng
```

Thay vào đó:

* Chức danh được dùng cho tổ chức và báo cáo.
* Role bundle cấp quyền.
* Scope policy giới hạn dữ liệu.
* Approval policy xác định quyền duyệt.

---

## 3.3. Role chỉ là tập hợp quyền

Role không phải nguồn chân lý cuối cùng và không được kiểm tra bằng role name trong business code.

Quyền hiệu lực của user được tính từ:

* Role assignment.
* Direct permission grant được kiểm soát.
* Scope assignment.
* Project/Listing access.
* Delegation.
* Temporary access.
* Deny rule.
* Field masking.
* Legal Entity.
* Ngày hiệu lực.
* Trạng thái user.
* Feature flag.
* Approval state.

---

## 3.4. Deny ưu tiên hơn Allow

Khi có xung đột:

```text
Explicit Deny > Temporary Restriction > Allow
```

Ví dụ:

* Role cho phép xem Contract.
* Nhưng user bị hạn chế xem dữ liệu tài chính.
* Backend phải loại bỏ trường tài chính.

Không sử dụng deny tùy tiện gây khó quản trị; deny chỉ dùng cho ngoại lệ rõ ràng.

---

## 3.5. Quyền luôn gồm hành động và phạm vi

Ví dụ:

```text
deal.view + mine
deal.view + team
deal.view + department
deal.view + all
```

`deal.view` không có scope không được mặc định thành `all`.

---

## 3.6. Scope không được lấy từ frontend

Frontend có thể yêu cầu:

```text
scope=mine
```

Nhưng backend phải:

1. Đọc authenticated user.
2. Resolve quyền hiệu lực.
3. Resolve đơn vị hiệu lực.
4. Resolve project/Listing access.
5. Áp điều kiện SQL.
6. Chỉ trả dữ liệu hợp lệ.

Không tin:

* `owner_id`.
* `sale_id`.
* `team_id`.
* `department_id`.
* `scope`.
* `legal_entity_id`.

do frontend gửi để mở rộng phạm vi.

---

## 3.7. Quyền xem không đồng nghĩa quyền xuất

Các quyền phải tách:

```text
customer.view
customer.export

listing.view
listing.export

deal.view
deal.export

contract.view
contract.export
```

Sale, Team Lead và Trưởng phòng mặc định không được export dữ liệu hàng loạt.

---

## 3.8. Resource permission không tự cấp quyền trường nhạy cảm

Ví dụ người có `customer.view` chưa chắc được xem:

* Số điện thoại đầy đủ.
* CCCD.
* Tài khoản ngân hàng.
* Hồ sơ tài chính.
* Ghi chú pháp lý.
* Giá sàn.
* Hoa hồng.

Phải có field policy riêng.

---

## 3.9. Quyền có ngày hiệu lực và hết hiệu lực

Mọi assignment quan trọng cần:

* `effective_from`.
* `effective_to`.
* Trạng thái.
* Nguồn cấp.
* Người cấp.
* Approval.
* Lý do.

Không cấp quyền vĩnh viễn khi nhu cầu chỉ là tạm thời.

---

## 3.10. Mọi quyền nhạy cảm phải truy xuất được nguồn gốc

Backend phải có thể giải thích:

> User A được phép duyệt hoàn tiền vì Role Finance Approver thuộc Legal Entity B, có hiệu lực từ ngày X và hạn mức Y.

---

# 4. Các đối tượng danh tính

## 4.1. Workforce subject và Party reference

IAM phải liên kết Workforce với canonical Party/Person identity thay vì sao chép một Person master độc lập.

Thông tin IAM có thể giữ ở mức cần thiết:

- Workforce subject ID.
- Party/person reference.
- Display-name snapshot khi cần vận hành.
- Preferred locale/timezone.
- Authentication identity references.
- Security/contact attributes được Security Architecture cho phép.
- Trạng thái liên kết.

PII canonical như personal identity, Customer contact hoặc legal identity phải tuân ownership, classification và masking của Party Context.

Một nhân viên có thể đồng thời là Customer; hai vai trò dùng chung canonical Party identity nhưng có lifecycle, access và business relationships riêng.

---

## 4.2. Workforce Profile

Thông tin:

* Workforce ID.
* Canonical Party/person reference.
* Mã nhân viên chung.
* Ngày gia nhập Enterprise.
* Trạng thái nhân sự.
* Loại lao động.
* Người quản lý hồ sơ.
* Ngày nghỉ dự kiến.
* Ngày nghỉ thực tế.
* Lý do kết thúc.
* Có đủ điều kiện nhận hoa hồng sau nghỉ hay không theo policy.
* Link hồ sơ nhân sự.

Loại workforce:

* Nhân viên chính thức.
* Thử việc.
* Hợp đồng.
* Cộng tác viên nội bộ.
* Quản lý.
* Chuyên gia.
* Nhân sự thuê ngoài.
* Nhân sự thuê ngoài có human identity phù hợp.

Non-human identities phải dùng Service Account, không dùng Workforce Profile.

---

## 4.3. User Account

Thông tin:

* User ID.
* Username.
* Email đăng nhập.
* Phone login nếu hỗ trợ.
* Identity provider.
* MFA status.
* Account status.
* Last login.
* Password status.
* Failed attempts.
* Locked until.
* Default Legal Entity.
* Default assignment.
* Locale.
* Timezone.
* Security risk status.
* Created at.
* Deactivated at.

---

## 4.4. Service Account

Service Account dùng cho:

* Integration.
* Job.
* API.
* Automation.
* ETL.
* System connector.

Service Account phải:

* Có owner chịu trách nhiệm.
* Có scope tối thiểu.
* Không dùng chung tùy tiện.
* Có secret rotation.
* Có ngày hết hạn nếu có thể.
* Không được đăng nhập giao diện như user thông thường.
* Có audit riêng.

---

## 4.5. External User

Có thể mở rộng cho:

* Cộng tác viên.
* Đại lý đối tác.
* Chủ tài sản.
* Chủ đầu tư.
* Customer Portal.

External User không mặc định thuộc cơ cấu tổ chức nội bộ.

Quyền phải giới hạn theo:

* Party.
* Transaction.
* Listing.
* Contract.
* Portal scope.

MVP có thể chưa triển khai đầy đủ External User nhưng mô hình dữ liệu không được ngăn cản mở rộng.

---

# 5. Trạng thái tài khoản

## 5.1. Trạng thái chuẩn

* Pending Invitation.
* Invited.
* Pending Activation.
* Active.
* Temporarily Suspended.
* Security Locked.
* Leave Restricted.
* Offboarding.
* Deactivated.
* Archived.
* Compromised.
* Service Disabled.

## 5.2. Active

User được đăng nhập và thực hiện quyền hiệu lực.

## 5.3. Temporarily Suspended

Dùng khi:

* Điều tra.
* Nghỉ tạm thời.
* Vi phạm quy trình.
* Chờ xác minh.

Không làm mất assignment hoặc lịch sử.

## 5.4. Security Locked

Do:

* Đăng nhập sai.
* Phát hiện rủi ro.
* Thiết bị bất thường.
* Admin khóa khẩn cấp.

## 5.5. Leave Restricted

User đang nghỉ nhưng có thể:

* Đăng nhập đọc giới hạn.
* Không nhận Lead mới.
* Không duyệt.
* Không thực hiện nghiệp vụ tài chính.

Policy phải cấu hình được.

## 5.6. Deactivated

User không đăng nhập được.

Dữ liệu lịch sử vẫn giữ.

---

# 6. Employment Assignment

## 6.1. Khái niệm

Employment Assignment mô tả một người đang làm việc ở đâu và với tư cách nào trong một khoảng thời gian.

Một Workforce Profile có thể có:

* Một assignment chính.
* Nhiều assignment kiêm nhiệm.
* Assignment tạm thời.
* Assignment theo dự án.
* Assignment theo Legal Entity.

## 6.2. Thông tin assignment

* Workforce.
* Legal Entity.
* Branch.
* Department.
* Team.
* Position.
* Manager.
* Assignment type.
* Employment type.
* Start date.
* End date.
* Is primary.
* Business Calendar.
* Cost center nếu có.
* Working location.
* Working schedule.
* Status.
* Approval.
* Reason.

## 6.3. Assignment type

* Primary.
* Secondary.
* Concurrent.
* Temporary.
* Acting.
* Project-based.
* Cross-entity.
* Delegated duty.

## 6.4. Một assignment chính tại một thời điểm

Mặc định mỗi Workforce có một assignment chính trong một Legal Entity.

Có thể có nhiều assignment chính nếu làm việc đồng thời cho nhiều Legal Entity, nhưng phải có:

* Legal Entity cụ thể.
* Phạm vi rõ ràng.
* Approval.
* Calendar.
* Manager.

## 6.5. Không sửa lịch sử assignment

Khi chuyển team:

* Kết thúc assignment cũ.
* Tạo assignment mới.
* Không ghi đè team cũ.

---

# 7. Cấu trúc tổ chức

## 7.1. Cấp tổ chức

Mô hình mặc định:

```text
Enterprise
└── Legal Entity
    └── Branch
        └── Department
            └── Team
                └── Position/Assignment
```

Không bắt buộc doanh nghiệp phải dùng đủ mọi cấp.

Ví dụ doanh nghiệp nhỏ:

```text
Enterprise
└── Legal Entity
    └── Department
        └── Team
```

---

## 7.2. Organizational Unit

Nên dùng một mô hình đơn vị chung:

* Branch.
* Division.
* Department.
* Center.
* Team.
* Project Office.
* Sales Office.
* Functional Group.

Mỗi đơn vị có:

* Mã.
* Tên.
* Loại.
* Legal Entity.
* Parent.
* Manager.
* Business Calendar.
* Địa điểm.
* Ngày hiệu lực.
* Trạng thái.
* Cost center.
* Metadata.

---

## 7.3. Branch

Chi nhánh có thể có:

* Địa chỉ.
* Mã.
* Người đứng đầu.
* Legal Entity.
* Business Calendar.
* Giờ làm việc.
* Vùng hoạt động.
* Dự án phụ trách.
* Kênh bán.

Branch không tự động là một pháp nhân.

---

## 7.4. Department

Ví dụ:

* Kinh doanh.
* Marketing.
* Kế toán.
* Tài chính.
* Pháp chế.
* Quản lý kho.
* Phát triển dự án.
* Chăm sóc khách hàng.
* Công nghệ.
* Nhân sự.
* Kiểm soát nội bộ.

---

## 7.5. Team

Team có thể là:

* Team sale dự án.
* Team seller-side.
* Team buyer-side.
* Team telesales.
* Team ký gửi.
* Team đất nền.
* Team chăm sóc sau bán.
* Team collection.

Team có thể thay đổi dự án phụ trách theo thời gian.

---

## 7.6. Matrix organization

Một user có thể:

* Thuộc Team A về mặt tổ chức.
* Tham gia Project Sales Group B.
* Được cấp quyền bán Project C.
* Nhận delegation từ Manager D.

IAM phải hỗ trợ cấu trúc ma trận nhưng không làm mất assignment chính.

---

# 8. Position và Job Function

## 8.1. Position

Position là vị trí trong sơ đồ tổ chức.

Ví dụ:

* Giám đốc.
* Trưởng phòng.
* Team Lead.
* Chuyên viên kinh doanh.
* Chuyên viên pháp chế.
* Kế toán viên.

Position có thể đang:

* Có người đảm nhiệm.
* Đang trống.
* Có người acting.
* Có nhiều slot.

## 8.2. Job Function

Job Function mô tả nhóm nghiệp vụ:

* Sales.
* Accounting.
* Finance.
* Legal.
* Marketing.
* Inventory.
* Project Development.
* Customer Service.
* Administration.

Job Function có thể dùng để đề xuất Role Bundle nhưng không tự động cấp mọi quyền.

## 8.3. Acting Position

Khi người quản lý vắng mặt:

* User có thể được bổ nhiệm acting.
* Có ngày bắt đầu/kết thúc.
* Có phạm vi.
* Có approval.
* Có thể kèm delegation.

Acting không tự động chuyển toàn bộ dữ liệu sở hữu.

---

# 9. Quan hệ quản lý

## 9.1. Direct Manager

Mỗi assignment có thể có direct manager.

## 9.2. Functional Manager

Có thể khác direct manager.

Ví dụ:

* Sale thuộc Team Lead A.
* Nhưng nghiệp vụ dự án chịu quản lý của Project Sales Manager B.

## 9.3. Approval Manager

Approval Engine có thể chọn người duyệt dựa trên:

* Direct manager.
* Functional manager.
* Unit head.
* Legal Entity director.
* Capability group.

## 9.4. Lịch sử manager

Thay manager phải có lịch sử.

Không ghi đè manager cũ.

---

# 10. Role Model

## 10.1. System Role

Role kỹ thuật có phạm vi toàn hệ thống:

* Super Admin.
* CRM Admin.
* Security Admin.
* Integration Admin.
* Auditor.

Các role này phải cấp rất hạn chế.

## 10.2. Business Role

Ví dụ:

* Sale.
* Team Lead.
* Department Head.
* Project Sales.
* Listing Acquisition.
* Inventory Manager.
* Accountant.
* Finance Officer.
* Legal Reviewer.
* Commission Specialist.
* Director.

## 10.3. Role Bundle

Role Bundle là tập hợp permission được quản lý có version và effective lifecycle.

Ví dụ candidate bundle `SALE_STANDARD_BASELINE` có thể gồm:

* Lead mine.
* Customer mine.
* Deal mine.
* Listing permitted projects.
* Proposal create.
* Booking request.
* Task mine.

## 10.4. Composite Role

Có thể kết hợp:

* Sale.
* Project Specialist.
* Temporary Approver.

Nhưng hệ thống phải hiển thị quyền tổng hợp và xung đột.

## 10.5. Role Template theo mô hình doanh nghiệp

Có thể có template:

* Doanh nghiệp nhỏ.
* Chủ đầu tư.
* Phân phối.
* Ký gửi.
* Multi-model.

Template chỉ là điểm khởi tạo, không phải hardcode.

---

# 11. Permission semantic model

> Exact permissions thuộc Permission Registry. Tài liệu này chỉ quy định product semantics và governance outcomes.


## 11.1. Cấu trúc mã quyền

Khuyến nghị:

```text
context.resource.action
```

Ví dụ:

```text
customer.profile.view
customer.phone.view_full
listing.inventory.update
deal.stage.change
contract.receipt.approve
commission.payout.execute
```

Có thể rút gọn với resource.action nếu namespace đã rõ, nhưng cần thống nhất toàn hệ thống.

---

## 11.2. Các nhóm action

* View.
* View sensitive.
* Create.
* Update.
* Delete draft.
* Archive.
* Restore.
* Assign.
* Transfer.
* Approve.
* Reject.
* Cancel.
* Execute.
* Export.
* Import.
* Merge.
* Override.
* View audit.
* Configure.

## 11.3. Permission Definition

Mỗi permission cần:

* Code.
* Name.
* Owning Context hoặc capability.
* Resource.
* Action.
* Risk level.
* Allowed scopes.
* Field policy group.
* Requires MFA.
* Requires re-authentication.
* Requires approval to grant.
* Incompatible permissions.
* Status.

## 11.4. Permission Risk Level

* Low.
* Medium.
* High.
* Critical.

Ví dụ Critical:

* `payment_receipt.cancel`
* `refund.execute`
* `commission_payout.execute`
* `user.security_admin`
* `export.all_customers`

---

# 12. Candidate scope vocabulary và semantic requirements

> Exact scope codes, composition, precedence và resolution semantics thuộc `docs/security/scope-resolution.md`. Các scope dưới đây là product vocabulary cần được canonical hóa, không phải registry tự thực thi.


## 12.1. Scope chuẩn

* `self`
* `mine`
* `assigned`
* `team`
* `department`
* `branch`
* `legal_entity`
* `project`
* `shared`
* `all`

## 12.2. `self`

Chỉ dữ liệu của chính user.

Ví dụ:

* Hồ sơ cá nhân.
* Bảng kê hoa hồng cá nhân.

## 12.3. `mine`

Dữ liệu mà user có quan hệ nghiệp vụ trực tiếp:

* Sale chính.
* Co-sale.
* Owner.
* Assignee.
* Creator trong trường hợp policy cho phép.
* Người được bàn giao.

Không chỉ dựa vào một trường `owner_id`.

## 12.4. `assigned`

Dữ liệu được giao cụ thể cho user.

## 12.5. `team`

Dữ liệu thuộc thành viên team hiệu lực.

## 12.6. `department`

Dữ liệu thuộc toàn phòng.

## 12.7. `branch`

Dữ liệu thuộc chi nhánh.

## 12.8. `legal_entity`

Dữ liệu thuộc pháp nhân.

## 12.9. `project`

Dữ liệu trong danh sách dự án được cấp quyền.

## 12.10. `shared`

Dữ liệu được chia sẻ qua Share Grant hợp lệ.

## 12.11. `all`

Toàn Enterprise hoặc phạm vi hệ thống theo permission.

`all` là quyền nhạy cảm, phải cấp có kiểm soát.

---

# 13. Scope resolution

## 13.1. Thành phần resolution

Backend resolve dựa trên:

* User.
* Active assignments.
* Legal Entity context.
* Role assignments.
* Permission grants.
* Scope assignments.
* Project access.
* Delegation.
* Share grants.
* Explicit deny.
* Effective dates.
* Resource relationship.

## 13.2. Legal Entity context

Khi user làm việc nhiều pháp nhân, giao diện phải cho chọn context hoặc tự xác định từ resource.

Không cho user sử dụng quyền của Legal Entity A để thao tác dữ liệu Legal Entity B.

## 13.3. SQL enforcement

Ví dụ Deal `mine` có thể bao gồm:

```text
primary_sale_user_id = current_user
OR active_co_sale_user_id = current_user
OR valid_delegation_assignee_id = current_user
OR explicit_assignment_user_id = current_user
```

Điều kiện phải ở SQL hoặc query layer, không tải toàn bộ rồi lọc Python.

---

# 14. Attribute-Based Access Control

Ngoài Role/Scope, hệ thống cần hỗ trợ điều kiện thuộc tính cho các trường hợp nâng cao.

Ví dụ:

* Chỉ được duyệt giao dịch dưới hạn mức.
* Chỉ được xem Listing trong Project được cấp.
* Chỉ được sửa hợp đồng Draft.
* Chỉ được xem Customer có quan hệ active.
* Chỉ được duyệt khi không phải người tạo.
* Chỉ được export trong giờ làm việc và mạng công ty.
* Chỉ được xem giá sàn của dự án được chỉ định.

ABAC không thay thế RBAC; nó bổ sung điều kiện.

---

# 15. Field-level access và masking semantics

> Exact fields, access modes và masking rules thuộc Field Masking Matrix.


## 15.1. Nhóm trường nhạy cảm

### Customer identity

* Số điện thoại.
* Email.
* CCCD.
* Địa chỉ.
* Ngày sinh.

### Financial

* Thu nhập.
* Tài sản.
* Nghĩa vụ nợ.
* Tài khoản ngân hàng.
* Công nợ.
* Hoàn tiền.

### Commercial

* Giá sàn.
* Biên lợi nhuận.
* Discount funding.
* Revenue.
* Company margin.

### Commission

* Hoa hồng công ty.
* Thu nhập người khác.
* Clawback.
* Tỷ lệ quản lý.

### Legal

* Ghi chú pháp lý.
* Tranh chấp.
* Tài liệu hạn chế.

## 15.2. Các chế độ field access

* Hidden.
* Masked.
* Read.
* Update.
* Approve.
* Full.

## 15.3. Masking

Ví dụ:

```text
090****789
ng***@email.com
0012********
****6789
```

## 15.4. Backend enforcement

Backend không được trả full value rồi yêu cầu frontend che.

---

# 16. Project Access

## 16.1. Mục tiêu

Không phải mọi sale đều được bán mọi dự án.

Project Access xác định:

* User/team/phòng được xem dự án nào.
* Được xem bảng hàng hay không.
* Được xem giá nào.
* Được tạo Proposal không.
* Được tạo Hold/Booking không.
* Được xem khách hàng dự án không.
* Kênh bán.
* Đợt mở bán.
* Thời hạn.

## 16.2. Project Access level

* View project.
* View inventory summary.
* View unit details.
* View sales price.
* View floor price.
* Create proposal.
* Create hold request.
* Create booking.
* Approve exception.
* Manage inventory.

## 16.3. Cấp quyền theo

* User.
* Team.
* Department.
* Branch.
* Role.
* Distribution mandate.
* Sales launch.

## 16.4. Quyền dự án không mở rộng Customer scope

Sale có quyền bán Project A không đồng nghĩa được xem tất cả Customer quan tâm Project A.

---

# 17. Listing Access

Listing Access áp dụng cho:

* Tài sản ký gửi.
* Tài sản đối tác.
* Listing riêng tư.
* Listing độc quyền.
* Listing có hồ sơ nhạy cảm.

Có thể giới hạn:

* Team phụ trách Listing.
* Sale seller-side.
* Sale buyer-side.
* Người được chủ tài sản cho phép.
* Thời gian.
* Mức thông tin.

Listing Access không được làm lộ toàn bộ hồ sơ chủ tài sản nếu user chỉ cần xem thông tin sản phẩm.

---

# 18. Share Grant

## 18.1. Mục tiêu

Cho phép chia sẻ có kiểm soát một resource cụ thể.

Ví dụ:

* Chia sẻ một Deal cho chuyên viên pháp lý.
* Chia sẻ một Listing cho sale hỗ trợ.
* Chia sẻ một Customer cho co-sale.
* Chia sẻ hợp đồng cho Kế toán.

## 18.2. Thông tin

* Resource.
* Người nhận.
* Quyền.
* Trường được xem.
* Lý do.
* Effective from/to.
* Người cấp.
* Approval.
* Có được chia sẻ tiếp không.
* Trạng thái.

## 18.3. Không tạo quyền vĩnh viễn ngoài scope

Share Grant nên có thời hạn và tự hết hiệu lực.

---

# 19. Direct Permission Grant

Direct grant chỉ dùng cho ngoại lệ.

Ví dụ:

* Điều tra viên cần xem audit.
* Nhân sự dự án tạm thời cần quyền Booking.
* Kế toán thay thế trong một tuần.

Mọi direct grant cần:

* Lý do.
* Thời hạn.
* Approval.
* Người chịu trách nhiệm.
* Access review.

Không sử dụng direct grant thay cho thiết kế role đúng.

---

# 20. Temporary và Just-in-Time Access

## 20.1. Temporary Access

Quyền có thời hạn xác định.

## 20.2. Just-in-Time Access

User yêu cầu quyền khi cần:

1. Chọn nghiệp vụ.
2. Nhập lý do.
3. Chọn thời hạn.
4. Approval.
5. Cấp tự động.
6. Thu hồi tự động.
7. Audit.

## 20.3. Emergency Access

Dùng trong sự cố nghiêm trọng.

Yêu cầu:

* Break-glass reason.
* MFA.
* Re-authentication.
* Thời hạn rất ngắn.
* Thông báo Giám đốc/Security.
* Audit chi tiết.
* Review sau sử dụng.

---

# 21. Segregation of Duties

> Exact incompatible-permission pairs và exception rules thuộc Segregation of Duties Matrix.


## 21.1. Mục tiêu

Ngăn một người kiểm soát toàn bộ nghiệp vụ nhạy cảm.

Ví dụ không nên đồng thời có:

* Tạo phiếu thu và hủy phiếu thu không cần duyệt.
* Tạo refund và thực hiện refund.
* Thay tài khoản nhận hoa hồng và chi hoa hồng.
* Tạo policy hoa hồng và tự phê duyệt.
* Tạo user admin và tự cấp quyền.
* Tạo Listing và tự duyệt pháp lý trong trường hợp nhạy cảm.

## 21.2. SoD Rule

Mỗi rule gồm:

* Permission A.
* Permission B.
* Conflict type.
* Scope.
* Có cho phép ngoại lệ không.
* Approval policy.
* Thời hạn ngoại lệ.
* Risk level.

## 21.3. Conflict detection

Phải kiểm tra khi:

* Cấp role.
* Cấp direct permission.
* Tạo delegation.
* Thay assignment.
* Tạo temporary access.

---

# 22. Delegation

## 22.1. Khái niệm

Delegation là việc một user ủy quyền một phần trách nhiệm hoặc quyền duyệt cho user khác trong thời gian xác định.

Delegation không chuyển quyền sở hữu dữ liệu vĩnh viễn.

## 22.2. Loại delegation

* Approval delegation.
* Work delegation.
* Task delegation.
* Customer care delegation.
* Deal delegation.
* Financial review delegation.
* Acting manager delegation.

## 22.3. Phạm vi

* Một permission.
* Một nhóm permission.
* Một resource.
* Một project.
* Một team.
* Một approval policy.
* Một khoảng hạn mức.

## 22.4. Điều kiện

* Người ủy quyền có quyền gốc.
* Không vượt phạm vi quyền gốc.
* Không vượt hạn mức.
* Không vi phạm SoD.
* Người nhận đủ điều kiện.
* Có ngày bắt đầu/kết thúc.
* Có approval nếu cần.

## 22.5. Không được ủy quyền tiếp mặc định

Sub-delegation mặc định bị cấm.

Chỉ cho phép khi policy ghi rõ.

## 22.6. Delegation kết thúc

Khi hết hạn:

* Quyền delegation tự thu hồi.
* Approval pending được xử lý theo policy.
* Task chưa hoàn thành có thể trả lại hoặc bàn giao.
* Gửi thông báo.
* Ghi audit.

---

# 23. Approval Authority

## 23.1. Khái niệm

Approval Authority xác định user được duyệt nghiệp vụ nào và hạn mức bao nhiêu.

Ví dụ:

* Giảm giá tối đa 100 triệu.
* Hoàn tiền tối đa 50 triệu.
* Duyệt Listing ký gửi giá tối thiểu.
* Duyệt export tối đa 5.000 dòng.
* Duyệt hoa hồng tối đa 500 triệu.

## 23.2. Authority source

* Role.
* Position.
* Direct appointment.
* Project assignment.
* Delegation.
* Acting assignment.

## 23.3. Snapshot

Approval Request phải snapshot authority tại thời điểm quyết định.

Thay đổi authority sau đó không làm thay đổi quyết định cũ.

---

# 24. Access Request

## 24.1. Người dùng yêu cầu quyền

User có thể yêu cầu:

* Role.
* Project access.
* Listing access.
* Sensitive field access.
* Export.
* Temporary access.
* Delegation.

## 24.2. Quy trình

1. Chọn quyền.
2. Chọn scope.
3. Nhập lý do.
4. Chọn thời hạn.
5. Hệ thống kiểm tra SoD.
6. Xác định approver.
7. Approval.
8. Cấp quyền.
9. Thông báo.
10. Access review khi đến hạn.

## 24.3. Không cấp quyền trước khi duyệt

Trừ quyền low-risk được policy tự động phê duyệt.

---

# 25. Access Review và Recertification

## 25.1. Mục tiêu

Định kỳ kiểm tra quyền còn cần thiết hay không.

## 25.2. Chu kỳ

* Hàng tháng.
* Hàng quý.
* Sáu tháng.
* Hàng năm.
* Khi chuyển đơn vị.
* Khi thay manager.
* Khi nghỉ dài ngày.
* Khi phát hiện rủi ro.

## 25.3. Người review

* Direct Manager.
* Unit Head.
* Legal Entity Admin.
* Security.
* Data Owner.
* Project Owner.

## 25.4. Quyết định

* Giữ.
* Thu hồi.
* Giảm scope.
* Gia hạn.
* Yêu cầu giải trình.
* Chuyển sang role khác.

## 25.5. Quyền Critical

Phải review thường xuyên hơn.

---

# 26. Onboarding

## 26.1. Điều kiện đầu vào

* Canonical Party/person reference.
* Workforce Profile.
* Legal Entity.
* Assignment.
* Manager.
* Position.
* Start date.
* Email đăng nhập.
* Role template.
* Project access nếu có.
* Calendar.
* Thiết bị nếu quản lý.

## 26.2. Quy trình onboarding

1. Resolve hoặc tạo canonical Party/Person qua Party Context.
2. Tạo Workforce Profile trong IAM.
3. Tạo Employment Assignment.
4. Cấp mã nhân viên.
5. Xác định Legal Entity.
6. Xác định đơn vị.
7. Xác định manager.
8. Chọn Position.
9. Chọn Role Bundle.
10. Kiểm tra SoD.
11. Approval.
12. Tạo User Account.
13. Gửi invitation.
14. Yêu cầu đổi mật khẩu/MFA.
15. Cấp Project Access.
16. Tạo Task đào tạo.
17. Xác nhận hoàn thành.
18. Kích hoạt đầy đủ.

## 26.3. Quyền tối thiểu trước đào tạo

Có thể giới hạn:

* Chỉ xem tài liệu.
* Không export.
* Không Booking.
* Không duyệt.
* Không xem dữ liệu nhạy cảm.

## 26.4. Onboarding theo mô hình nghiệp vụ

### Sale dự án tự phát triển

Cần:

* Project access.
* Inventory access.
* Booking request.
* Price policy.

### Sale phân phối

Cần:

* Distribution project.
* Sales launch.
* External inventory workflow.

### Sale ký gửi

Cần:

* Seller Lead.
* Listing acquisition.
* Owner profile.
* Consignment workflow.

---

# 27. Probation và nâng quyền sau thử việc

User thử việc có thể:

* Giới hạn Lead.
* Không xem full phone ngoài Lead được giao.
* Không tạo Booking giá trị lớn.
* Không export.
* Không được duyệt.

Khi đạt điều kiện:

* Manager đề nghị.
* Review.
* Approval.
* Chuyển Role Bundle.
* Ghi lịch sử.

---

# 28. Chuyển đơn vị

## 28.1. Các trường hợp

* Chuyển Team.
* Chuyển Department.
* Chuyển Branch.
* Chuyển Legal Entity.
* Kiêm nhiệm.
* Bổ nhiệm quản lý.
* Điều chuyển dự án.

## 28.2. Quy trình

1. Tạo Transfer Request.
2. Xác định assignment cũ.
3. Xác định assignment mới.
4. Ngày hiệu lực.
5. Manager cũ.
6. Manager mới.
7. Kiểm tra role.
8. Kiểm tra project access.
9. Kiểm tra Customer/Deal/Listing đang phụ trách.
10. Tạo Handover Plan.
11. Approval.
12. Kết thúc assignment cũ.
13. Tạo assignment mới.
14. Cập nhật role.
15. Thu hồi quyền không còn phù hợp.
16. Cấp quyền mới.
17. Thực hiện bàn giao.
18. Audit.

## 28.3. Không tự chuyển dữ liệu theo assignment

Dữ liệu phải theo Handover Plan.

Ví dụ:

* Customer có thể giữ sale cũ trong giai đoạn chuyển tiếp.
* Listing có thể chuyển cho team mới.
* Deal active cần quyết định riêng.
* Commission đã hình thành không tự chuyển.

---

# 29. Nghỉ phép và vắng mặt

## 29.1. Loại vắng mặt

* Nghỉ phép.
* Nghỉ ốm.
* Nghỉ thai sản.
* Công tác.
* Đào tạo.
* Tạm đình chỉ.
* Nghỉ không lương.
* Vắng mặt khác.

## 29.2. Leave Profile

* User.
* Assignment.
* Start/end.
* Full day/partial.
* Business Calendar.
* Status.
* Substitute user.
* Delegation.
* Lead distribution behavior.
* Handover requirement.

## 29.3. Tác động

Có thể cấu hình:

* Không phân Lead mới.
* Tạm dừng giao Task mới.
* Chuyển approval.
* Giữ quyền xem.
* Chặn thao tác tài chính.
* Chuyển Customer chăm sóc tạm thời.
* Chuyển Task đến substitute.

## 29.4. Không tự chuyển Customer vĩnh viễn

Leave delegation chỉ tạo quyền tạm thời.

Khi user quay lại:

* Quyền tạm thời kết thúc.
* Task được trả lại theo policy.
* Lịch sử chăm sóc được giữ.

---

# 30. Offboarding

## 30.1. Trigger

* Nghỉ việc.
* Chấm dứt hợp đồng.
* Kết thúc cộng tác.
* Chuyển ra ngoài hệ thống.
* Vi phạm nghiêm trọng.
* Tài khoản không còn cần thiết.

## 30.2. Offboarding case

Thông tin:

* Workforce.
* User.
* Last working date.
* Account disable time.
* Reason.
* Manager.
* Handover custodian.
* Assets to hand over.
* Outstanding approvals.
* Project access.
* Commission balance.
* Security actions.
* Checklist.
* Status.

## 30.3. Quy trình

1. Tạo Offboarding Case.
2. Xác định ngày cuối.
3. Xác định mức độ khẩn cấp.
4. Chặn cấp Lead mới.
5. Thu hồi temporary access.
6. Thu hồi delegation đã cấp.
7. Chuyển approval pending.
8. Lập Handover Plan.
9. Xác định custodian.
10. Bàn giao Lead.
11. Bàn giao Customer relationship.
12. Bàn giao Listing.
13. Bàn giao Deal.
14. Bàn giao Booking/Contract Task.
15. Kiểm tra commission.
16. Kiểm tra tài khoản/thiết bị.
17. Disable user.
18. Thu hồi session/token.
19. Archive assignment.
20. Hoàn tất audit.

## 30.4. Trường hợp khẩn cấp

Nếu có rủi ro:

* Disable ngay.
* Revoke token.
* Khóa API key.
* Chuyển dữ liệu cho custodian.
* Thực hiện handover sau bằng manager/admin.

## 30.5. Không xóa user

User đã phát sinh dữ liệu không được xóa cứng.

---

# 31. Custodian và quyền giữ tạm

## 31.1. Custodian mặc định

Khi sale nghỉ việc:

* Team Lead là custodian tạm thời.
* Department Head có quyền phân phối lại.
* Có thể cấu hình custodian khác.

## 31.2. Custodian không tự trở thành owner vĩnh viễn

Custodian có trách nhiệm:

* Bảo quản dữ liệu.
* Theo dõi SLA.
* Chuyển giao.
* Không mặc định hưởng hoa hồng.
* Không mặc định được tính là người tạo quan hệ Customer.

## 31.3. Custodian scope

Chỉ áp dụng resource được liệt kê trong Handover Plan.

---

# 32. Handover Framework

## 32.1. Đối tượng bàn giao

* Lead.
* Customer care relationship.
* Requirement.
* Asset owner relationship.
* Listing.
* Deal.
* Transaction Case.
* Proposal.
* Hold.
* Booking.
* Contract Task.
* Receivable follow-up.
* Commission dispute.
* Approval request.
* Task.
* Appointment.
* External document link.
* Integration responsibility.

## 32.2. Handover Case

Thông tin:

* Mã.
* Handover type.
* Người giao.
* Người nhận.
* Custodian.
* Legal Entity.
* Đơn vị cũ/mới.
* Ngày bắt đầu.
* Deadline.
* SLA policy.
* Trạng thái.
* Approval.
* Checklist.
* Tổng resource.
* Đã hoàn thành.
* Quá hạn.

## 32.3. Handover type

* Transfer.
* Leave.
* Offboarding.
* Project reassignment.
* Team restructuring.
* Emergency.
* Temporary coverage.
* Manager change.

## 32.4. Handover Item

Mỗi item gồm:

* Resource type.
* Resource ID.
* Priority.
* Current status.
* Next action.
* Deadline.
* Sensitive flag.
* Acceptance status.
* Reason.
* Notes.
* Attachments link.
* Old assignee.
* New assignee.
* Custodian.

## 32.5. Trạng thái item

* Pending Preparation.
* Ready.
* Sent.
* Accepted.
* Rejected.
* Need Clarification.
* Completed.
* Exempted.
* Overdue.

## 32.6. Người nhận phải xác nhận

Người nhận có thể:

* Accept.
* Reject có lý do.
* Yêu cầu bổ sung.
* Escalate.

Không tự động coi item đã hoàn thành chỉ vì deadline qua.

---

# 33. SLA bàn giao

## 33.1. Recommended initialization baseline — PENDING VALIDATION

| Loại dữ liệu                  | SLA mặc định        |
| ----------------------------- | ------------------- |
| Lead mới chưa chăm sóc        | Trong 2 giờ         |
| Lịch hẹn trong 24 giờ         | Ngay lập tức        |
| Deal đang hoạt động           | Trong 24 giờ        |
| Hold/Booking/đặt cọc          | Trong ngày làm việc |
| Contract/Payment Task         | Trong ngày làm việc |
| Listing có người mua quan tâm | Trong 24 giờ        |
| Task sắp đến hạn              | Trước deadline      |
| Dữ liệu khác                  | Trong 3 ngày        |

Các giá trị trên chỉ là recommended initialization baseline. Chúng không phải universal code constants hoặc accepted SLO cho đến khi được Platform Configuration và Product Owner phê duyệt.

## 33.2. Cấu hình theo phạm vi

Có thể theo:

* Legal Entity.
* Branch.
* Department.
* Team.
* Project.
* Transaction model.
* Resource type.
* Priority.
* Deal stage.
* Có tiền hay chưa.
* Handover type.

## 33.3. Thứ tự ưu tiên

Cấu hình cụ thể hơn thắng theo Configuration Definition của Platform Context.

## 33.4. Cảnh báo

* 50%.
* 80%.
* Sắp đến hạn.
* Đến hạn.
* Quá hạn.
* Quá hạn nghiêm trọng.

## 33.5. Escalation

```text
Người giao/người nhận
→ Team Lead
→ Department Head
→ Legal Entity Director
→ Director
```

Có thể cấu hình khác.

## 33.6. Pause/extension

Chỉ được khi:

* Có lý do.
* Có người yêu cầu.
* Có người duyệt.
* Có ngày mới.
* Có audit.

## 33.7. Quy tắc bắt buộc

> SLA bàn giao là cấu hình nghiệp vụ động, không phải giá trị cố định trong mã nguồn.

---

# 34. Reassignment sau bàn giao

## 34.1. Lead

Yêu cầu Lead Context cập nhật assignment qua published command/workflow.

## 34.2. Customer

Không thay owner core.

Chỉ cập nhật care relationship hoặc access relationship.

## 34.3. Listing

Cập nhật seller-side assignment hoặc listing team.

## 34.4. Deal

Thay primary sale bằng workflow Deal.

## 34.5. Booking/Contract

Không thay dữ liệu lịch sử sale cũ.

Tạo assignment mới cho trách nhiệm tiếp theo.

## 34.6. Commission

Không tự chuyển quyền hưởng đã hình thành.

---

# 35. Thay đổi manager và tái cấu trúc tổ chức

Khi đổi manager hoặc gộp/tách đơn vị:

* Không ghi đè lịch sử.
* Tạo structure version mới.
* Xác định ngày hiệu lực.
* Re-resolve approval chain.
* Kiểm tra approval pending.
* Kiểm tra delegation.
* Kiểm tra scope team/department.
* Chạy impact preview.
* Tạo handover nếu cần.

Workflow pending có thể:

* Giữ approver cũ.
* Chuyển approver mới.
* Re-resolve theo policy.

Phải cấu hình rõ.

---

# 36. Organizational Structure Versioning

## 36.1. Lý do

Cơ cấu tổ chức thay đổi theo thời gian.

Báo cáo lịch sử cần biết:

* Sale thuộc team nào khi giao dịch phát sinh.
* Manager là ai.
* Phòng nào ghi nhận doanh số.
* Hoa hồng quản lý dùng cơ cấu nào.

## 36.2. Snapshot

Các owning business Context quan trọng cần lưu organization snapshot tại mốc:

* Deal created.
* Contract signed.
* Revenue recognized.
* Commission recognized.

## 36.3. Không tính lại lịch sử tự động

Thay cơ cấu hiện tại không thay đổi snapshot cũ.

---

# 37. Business Calendar Assignment

## 37.1. Cơ chế kế thừa

```text
User override
→ Employment Assignment
→ Team
→ Department
→ Branch
→ Legal Entity
→ Enterprise
```

## 37.2. Ca làm việc

Có thể gán:

* Ca hành chính.
* Ca telesales.
* Ca cuối tuần.
* Ca trực dự án.
* Ca sự kiện mở bán.

## 37.3. Calendar thay đổi

Assignment phải lưu calendar version hiệu lực.

SLA đã bắt đầu không bị tính lại âm thầm.

---

# 38. Authentication product requirements

> Exact identity providers, protocols, token/session parameters và MFA controls thuộc Security Architecture và Toolchain/Environment configuration.


## 38.1. Phương thức đăng nhập

* Email/password.
* SSO.
* OAuth/OIDC.
* Google Workspace.
* Microsoft Entra ID.
* Phone OTP nếu cấu hình.
* Passkey trong giai đoạn nâng cao.

## 38.2. MFA

Có thể yêu cầu theo:

* System Admin.
* Finance.
* Accounting.
* Legal.
* Director.
* Export permission.
* Payout.
* Refund.
* Secret management.

## 38.3. Re-authentication

Bắt buộc cho thao tác nhạy cảm:

* Thay tài khoản ngân hàng.
* Cấp quyền Critical.
* Export dữ liệu lớn.
* Execute refund.
* Execute payout.
* Emergency access.

---

# 39. Session và device product requirements

> Exact session schema, lifetime, device fingerprinting và risk thresholds thuộc Security Architecture và environment policy.


## 39.1. Session

Lưu:

* User.
* Device.
* IP.
* Location coarse.
* Created.
* Last active.
* Expiration.
* Revoked.
* Risk score.

## 39.2. Device trust

Thiết bị có thể:

* New.
* Pending verification.
* Trusted.
* Restricted.
* Blocked.

## 39.3. Session revocation

Cho phép:

* User tự logout các thiết bị.
* Admin revoke.
* Revoke toàn bộ khi offboarding.
* Revoke khi đổi mật khẩu.
* Revoke khi security incident.

---

# 40. Security-risk outcomes

> Exact detection rules, thresholds và incident routing thuộc Threat Model, Alert Catalog và security operations configuration.


## 40.1. Rủi ro

* Đăng nhập từ vị trí bất thường.
* Nhiều lần sai mật khẩu.
* Tải dữ liệu lớn.
* Xem nhiều Customer ngoài hành vi.
* Thay đổi quyền liên tục.
* Sử dụng emergency access.
* Đăng nhập ngoài giờ và thực hiện tài chính.
* Dùng tài khoản nhiều thiết bị bất thường.

## 40.2. Phản ứng

* Cảnh báo.
* Yêu cầu MFA.
* Re-authentication.
* Hạn chế session.
* Khóa tạm.
* Yêu cầu Security review.

---

# 41. Export Permission

## 41.1. Mặc định

* Sale: không export hàng loạt.
* Team Lead: không export hàng loạt.
* Department Head: không export hàng loạt.

## 41.2. Kế toán – Tài chính

Có thể export dữ liệu tài chính trong scope.

## 41.3. Giám đốc

Có thể export theo quyền và approval.

## 41.4. Export grant

Có thể giới hạn:

* Owning Context hoặc capability.
* Resource.
* Fields.
* Maximum rows.
* Format.
* Legal Entity.
* Project.
* Time.
* Purpose.
* Watermark.
* Approval.

## 41.5. Không dùng UI ẩn nút làm bảo mật

Backend phải từ chối export API nếu không có quyền.

---

# 42. Data Ownership và Data Stewardship

## 42.1. Không đồng nhất owner nghiệp vụ và người sở hữu dữ liệu

Customer core thuộc công ty.

Sale chỉ có care relationship.

Listing thuộc quyền quản lý theo mandate.

Deal có primary sale.

Contract thuộc Legal Entity/Transaction.

## 42.2. Data Steward

Mỗi owning Context có thể xác định Data Steward:

* Customer Data Steward.
* Inventory Steward.
* Contract Steward.
* Finance Steward.
* Commission Steward.

Data Steward chịu trách nhiệm chất lượng dữ liệu, không mặc định được thao tác tài chính.

---

# 43. Các màn hình chính

## 43.1. Organization Explorer

Hiển thị cây:

* Enterprise.
* Legal Entity.
* Branch.
* Department.
* Team.
* Position.
* User.

Có bộ lọc theo ngày hiệu lực.

## 43.2. Legal Entity Workforce

* Danh sách nhân sự.
* Assignment.
* Trạng thái.
* Role.
* Manager.
* Calendar.
* Project access.

## 43.3. User Directory

* User.
* Workforce.
* Legal Entity.
* Đơn vị.
* Chức danh.
* Account status.
* Last login.
* Risk status.
* MFA.
* Role.

## 43.4. User 360 Administration

Các tab:

1. Profile.
2. Employment.
3. Assignments.
4. Roles.
5. Permissions.
6. Scope.
7. Project Access.
8. Listing Access.
9. Delegation.
10. Approval Authority.
11. Calendar.
12. Leave.
13. Handover.
14. Sessions.
15. Devices.
16. Access History.
17. Audit.

## 43.5. Role Center

* Role definitions.
* Role version.
* Permissions.
* Allowed scope.
* Risk.
* Assigned users.
* Conflicts.
* Simulation.

## 43.6. Permission Catalog

* Permission code.
* Owning Context hoặc capability.
* Risk.
* Allowed scope.
* Sensitive fields.
* MFA requirement.
* Grant policy.

## 43.7. Access Matrix

So sánh:

* User.
* Role.
* Resource.
* Action.
* Scope.
* Legal Entity.
* Project.
* Effective date.
* Source.

## 43.8. Access Request Center

* Yêu cầu mới.
* Chờ duyệt.
* Đã cấp.
* Sắp hết hạn.
* Bị từ chối.
* Thu hồi.

## 43.9. Delegation Center

* Người giao.
* Người nhận.
* Phạm vi.
* Thời gian.
* Trạng thái.
* Approval.
* Quyền được sử dụng.

## 43.10. Handover Center

* Case.
* Người giao/nhận.
* Resource.
* SLA.
* Progress.
* Overdue.
* Escalation.
* Acceptance.

## 43.11. Access Review Center

* Campaign.
* Reviewer.
* User.
* Role.
* Permission.
* Decision.
* Deadline.
* Progress.

## 43.12. Security Sessions

* Active sessions.
* Devices.
* Risk.
* IP.
* Last activity.
* Revoke.

---

# 44. Dashboard theo vai trò

## 44.1. CRM Admin

* User active.
* User chưa kích hoạt.
* Role sắp hết hạn.
* Direct grant.
* Quyền Critical.
* Access request.
* Handover quá hạn.
* Offboarding chưa xong.
* SoD conflict.
* User không có manager.
* Assignment hết hạn.

## 44.2. Manager

* Nhân sự team.
* Nghỉ phép.
* Delegation.
* Access request chờ duyệt.
* Handover.
* User thiếu đào tạo.
* Project access.
* Access review.

## 44.3. Security Admin

* Login risk.
* Account locked.
* Emergency access.
* Permission escalation.
* Export bất thường.
* Session lạ.
* Service account sắp hết hạn.

## 44.4. Giám đốc

* Headcount theo pháp nhân.
* Cơ cấu tổ chức.
* Quyền Critical.
* Export access.
* Handover risk.
* Offboarding.
* SoD conflict.
* User đa pháp nhân.
* Access review compliance.

---

# 45. Báo cáo

* Headcount theo Legal Entity.
* Headcount theo Branch/Department/Team.
* User active/inactive.
* Employment Assignment.
* Role assignment.
* Permission assignment.
* Direct permission.
* Temporary access.
* Delegation.
* Project access.
* Listing access.
* Quyền Critical.
* SoD conflict.
* Access review.
* User không hoạt động.
* Login risk.
* Onboarding duration.
* Offboarding duration.
* Handover SLA.
* Handover overdue.
* Leave coverage.
* Role usage.
* Permission không được sử dụng.
* Service account.
* Export authorization.
* Multi-entity assignment.

Mọi báo cáo phải tuân effective scope, field policy và certified analytical access rules.

---

# 46. Candidate data model — không phải physical schema canonical

> **Classification:** `CONTEXT-SPECIFIC DESIGN INPUT / PENDING VALIDATION`  
> Exact tables, columns, constraints, indexes và cross-schema references chỉ có hiệu lực khi được khóa trong IAM Context DB Specification và Alembic migrations.


## 46.1. Workforce subject và Party reference

Canonical Person/Party record thuộc `party` Context.

IAM candidate model chỉ được lưu reference hoặc workforce-specific subject data, ví dụ:

### `workforce_subjects` — candidate only

- `id`
- `party_id`
- `display_name_snapshot`
- `preferred_locale`
- `preferred_timezone`
- `status`
- `created_at`
- `updated_at`

> Exact table/fields phải được khóa trong IAM Context DB Specification và Alembic. Không tạo `persons` table trong IAM để cạnh tranh với Party source of truth.

---

## 46.2. Workforce

### `workforce_profiles`

* `id`
* `workforce_subject_id`
* `enterprise_id`
* `employee_code`
* `workforce_type`
* `employment_status`
* `enterprise_joined_at`
* `planned_exit_at`
* `actual_exit_at`
* `exit_reason_code`
* `commission_eligibility_status`
* `created_at`
* `updated_at`

---

## 46.3. User Account

### `users`

* `id`
* `workforce_subject_id`
* `workforce_profile_id`
* `username`
* `login_email`
* `identity_provider`
* `account_type`
* `account_status`
* `default_legal_entity_id`
* `default_assignment_id`
* `locale`
* `timezone`
* `mfa_status`
* `security_risk_status`
* `last_login_at`
* `activated_at`
* `deactivated_at`
* `created_at`
* `updated_at`

### `user_account_status_history`

* `id`
* `user_id`
* `from_status`
* `to_status`
* `reason`
* `changed_by`
* `approval_request_id`
* `created_at`

---

## 46.4. Service Account

### `service_accounts`

* `id`
* `service_code`
* `display_name`
* `owner_user_id`
* `legal_entity_id`
* `purpose`
* `status`
* `secret_reference`
* `effective_from`
* `effective_to`
* `last_used_at`
* `created_at`

---

## 46.5. Organizational Unit

### `organizational_units`

* `id`
* `enterprise_id`
* `legal_entity_id`
* `unit_code`
* `name`
* `unit_type`
* `parent_unit_id`
* `manager_position_id`
* `business_calendar_id`
* `cost_center_code`
* `location`
* `status`
* `effective_from`
* `effective_to`
* `created_at`
* `updated_at`

### `organizational_unit_history`

* `id`
* `organizational_unit_id`
* `version`
* `parent_unit_id`
* `manager_position_id`
* `name`
* `status`
* `effective_from`
* `effective_to`
* `change_reason`
* `created_at`

---

## 46.6. Position

### `positions`

* `id`
* `position_code`
* `name`
* `organizational_unit_id`
* `job_function_code`
* `position_level`
* `reports_to_position_id`
* `headcount_limit`
* `status`
* `effective_from`
* `effective_to`
* `created_at`

### `position_assignments`

* `id`
* `position_id`
* `employment_assignment_id`
* `assignment_type`
* `is_primary`
* `effective_from`
* `effective_to`
* `status`
* `created_at`

---

## 46.7. Employment Assignment

### `employment_assignments`

* `id`
* `workforce_profile_id`
* `legal_entity_id`
* `branch_unit_id`
* `department_unit_id`
* `team_unit_id`
* `position_id`
* `manager_assignment_id`
* `assignment_type`
* `employment_type`
* `is_primary`
* `business_calendar_id`
* `working_location`
* `cost_center_code`
* `status`
* `effective_from`
* `effective_to`
* `created_by`
* `approved_by`
* `created_at`

---

## 46.8. Role

### `roles`

* `id`
* `role_code`
* `name`
* `role_type`
* `capability_group`
* `risk_level`
* `version`
* `status`
* `effective_from`
* `effective_to`
* `created_by`
* `reviewed_by`
* `approved_by`
* `created_at`

### `role_permissions`

* `id`
* `role_id`
* `permission_id`
* `allowed_scope_types`
* `default_scope_type`
* `field_policy_id`
* `conditions_json`
* `created_at`

### `role_assignments`

* `id`
* `user_id`
* `employment_assignment_id`
* `role_id`
* `role_version`
* `scope_type`
* `scope_id`
* `source_type`
* `source_resource_id`
* `effective_from`
* `effective_to`
* `status`
* `requested_by`
* `approved_by`
* `created_at`

---

## 46.9. Permission

### `permissions`

* `id`
* `permission_code`
* `name`
* `context_code`
* `resource_code`
* `action_code`
* `risk_level`
* `allowed_scope_types`
* `requires_mfa`
* `requires_reauthentication`
* `grant_requires_approval`
* `status`
* `created_at`

### `direct_permission_grants`

* `id`
* `user_id`
* `permission_id`
* `effect`
* `scope_type`
* `scope_id`
* `field_policy_id`
* `conditions_json`
* `effective_from`
* `effective_to`
* `reason`
* `status`
* `requested_by`
* `approved_by`
* `created_at`

---

## 46.10. Field Policy

### `field_access_policies`

* `id`
* `policy_code`
* `name`
* `resource_type`
* `version`
* `status`
* `created_at`

### `field_access_policy_items`

* `id`
* `field_access_policy_id`
* `field_code`
* `access_mode`
* `masking_rule`
* `conditions_json`

---

## 46.11. Scope Assignment

### `user_scope_assignments`

* `id`
* `user_id`
* `permission_id`
* `scope_type`
* `scope_id`
* `effective_from`
* `effective_to`
* `source_type`
* `status`
* `created_at`

---

## 46.12. Project Access

### `project_access_grants`

* `id`
* `grantee_type`
* `grantee_id`
* `project_id`
* `sales_launch_id`
* `access_level_code`
* `allowed_actions_json`
* `field_policy_id`
* `effective_from`
* `effective_to`
* `status`
* `requested_by`
* `approved_by`
* `created_at`

### `project_access_levels`

* `id`
* `access_level_code`
* `name`
* `permissions_json`
* `status`

---

## 46.13. Listing Access

### `listing_access_grants`

* `id`
* `listing_id`
* `grantee_type`
* `grantee_id`
* `access_level_code`
* `field_policy_id`
* `effective_from`
* `effective_to`
* `reason`
* `status`
* `created_by`
* `approved_by`
* `created_at`

---

## 46.14. Share Grant

### `resource_share_grants`

* `id`
* `resource_type`
* `resource_id`
* `grantee_user_id`
* `permission_codes_json`
* `field_policy_id`
* `can_reshare`
* `effective_from`
* `effective_to`
* `reason`
* `status`
* `granted_by`
* `approved_by`
* `created_at`

---

## 46.15. Segregation of Duties

### `segregation_of_duties_rules`

* `id`
* `rule_code`
* `name`
* `permission_a_id`
* `permission_b_id`
* `conflict_type`
* `scope_type`
* `scope_id`
* `exception_allowed`
* `approval_policy_id`
* `status`
* `created_at`

### `segregation_of_duties_conflicts`

* `id`
* `user_id`
* `rule_id`
* `source_a`
* `source_b`
* `status`
* `detected_at`
* `resolved_at`
* `resolution`

---

## 46.16. Delegation

### `delegations`

* `id`
* `delegation_code`
* `delegator_user_id`
* `delegate_user_id`
* `delegation_type`
* `scope_type`
* `scope_id`
* `permission_codes_json`
* `resource_type`
* `resource_id`
* `maximum_approval_amount`
* `effective_from`
* `effective_to`
* `allow_subdelegation`
* `reason`
* `status`
* `approval_request_id`
* `created_at`

### `delegation_usage_logs`

* `id`
* `delegation_id`
* `actor_user_id`
* `resource_type`
* `resource_id`
* `action_code`
* `occurred_at`

---

## 46.17. Approval Authority

### `approval_authorities`

* `id`
* `user_id`
* `employment_assignment_id`
* `action_code`
* `resource_type`
* `scope_type`
* `scope_id`
* `currency`
* `minimum_amount`
* `maximum_amount`
* `source_type`
* `source_resource_id`
* `effective_from`
* `effective_to`
* `status`
* `approved_by`
* `created_at`

---

## 46.18. Access Request

### `access_requests`

* `id`
* `request_code`
* `requester_user_id`
* `beneficiary_user_id`
* `request_type`
* `requested_role_id`
* `requested_permission_id`
* `scope_type`
* `scope_id`
* `effective_from`
* `effective_to`
* `reason`
* `risk_level`
* `sod_check_result`
* `approval_request_id`
* `status`
* `created_at`
* `resolved_at`

---

## 46.19. Access Review

### `access_review_campaigns`

* `id`
* `campaign_code`
* `name`
* `scope_type`
* `scope_id`
* `review_type`
* `started_at`
* `due_at`
* `status`
* `created_by`
* `created_at`

### `access_review_items`

* `id`
* `campaign_id`
* `reviewer_user_id`
* `subject_user_id`
* `access_type`
* `access_resource_id`
* `decision`
* `comment`
* `status`
* `reviewed_at`

---

## 46.20. Leave

### `workforce_leave_records`

* `id`
* `workforce_profile_id`
* `employment_assignment_id`
* `leave_type`
* `start_at`
* `end_at`
* `business_calendar_id`
* `substitute_user_id`
* `delegation_id`
* `lead_distribution_policy`
* `account_restriction_policy`
* `status`
* `approved_by`
* `created_at`

---

## 46.21. Transfer

### `workforce_transfer_requests`

* `id`
* `workforce_profile_id`
* `from_assignment_id`
* `target_legal_entity_id`
* `target_unit_id`
* `target_position_id`
* `target_manager_assignment_id`
* `effective_at`
* `reason`
* `handover_case_id`
* `approval_request_id`
* `status`
* `created_at`
* `resolved_at`

---

## 46.22. Offboarding

### `offboarding_cases`

* `id`
* `case_code`
* `workforce_profile_id`
* `user_id`
* `last_working_at`
* `disable_account_at`
* `reason_code`
* `reason`
* `manager_user_id`
* `custodian_user_id`
* `handover_case_id`
* `commission_review_status`
* `security_review_status`
* `status`
* `created_by`
* `approved_by`
* `created_at`
* `completed_at`

### `offboarding_checklist_items`

* `id`
* `offboarding_case_id`
* `item_code`
* `assigned_to`
* `status`
* `due_at`
* `completed_at`
* `evidence_url`

---

## 46.23. Handover

### `handover_cases`

* `id`
* `handover_code`
* `handover_type`
* `legal_entity_id`
* `from_user_id`
* `to_user_id`
* `custodian_user_id`
* `from_assignment_id`
* `to_assignment_id`
* `sla_policy_id`
* `sla_policy_version`
* `started_at`
* `due_at`
* `status`
* `approval_request_id`
* `created_at`
* `completed_at`

### `handover_items`

* `id`
* `handover_case_id`
* `resource_type`
* `resource_id`
* `priority`
* `current_status_snapshot`
* `next_action`
* `next_action_due_at`
* `sensitive_flag`
* `from_assignee_user_id`
* `to_assignee_user_id`
* `acceptance_status`
* `rejection_reason`
* `status`
* `accepted_at`
* `completed_at`
* `created_at`

### `handover_item_events`

* `id`
* `handover_item_id`
* `event_type`
* `actor_user_id`
* `comment`
* `created_at`

---

## 46.24. Sessions và Devices

### `user_sessions`

* `id`
* `user_id`
* `session_token_hash`
* `device_id`
* `ip_address`
* `user_agent`
* `risk_score`
* `created_at`
* `last_active_at`
* `expires_at`
* `revoked_at`
* `revoked_by`

### `user_devices`

* `id`
* `user_id`
* `device_fingerprint`
* `device_name`
* `platform`
* `trust_status`
* `first_seen_at`
* `last_seen_at`
* `verified_at`
* `blocked_at`

---

# 47. Candidate application operations — không phải OpenAPI canonical

> Các operation dưới đây mô tả capability inventory. Exact paths, methods, payloads, Problem Details, concurrency và authorization metadata thuộc OpenAPI.


## Workforce subject, Workforce và User

Canonical Party/Person creation và update thuộc Party API. IAM chỉ resolve/reference Party identity.

```text
GET    /workforce-subjects
GET    /workforce-subjects/{id}

GET    /workforce
POST   /workforce
GET    /workforce/{id}
PATCH  /workforce/{id}

GET    /users
POST   /users
GET    /users/{id}
PATCH  /users/{id}
POST   /users/{id}/invite
POST   /users/{id}/activate
POST   /users/{id}/suspend
POST   /users/{id}/deactivate
POST   /users/{id}/unlock
POST   /users/{id}/revoke-sessions
```

## Organizational Units

```text
GET    /organizational-units
POST   /organizational-units
GET    /organizational-units/{id}
PATCH  /organizational-units/{id}
POST   /organizational-units/{id}/create-version
POST   /organizational-units/{id}/activate
POST   /organizational-units/{id}/deactivate
GET    /organization/tree
```

## Assignment và Position

```text
GET    /employment-assignments
POST   /employment-assignments
GET    /employment-assignments/{id}
PATCH  /employment-assignments/{id}
POST   /employment-assignments/{id}/end

GET    /positions
POST   /positions
PATCH  /positions/{id}
POST   /positions/{id}/assign
POST   /position-assignments/{id}/end
```

## Role và Permission

```text
GET    /roles
POST   /roles
GET    /roles/{id}
PATCH  /roles/{id}
POST   /roles/{id}/create-version
POST   /roles/{id}/simulate
POST   /roles/{id}/approve
POST   /roles/{id}/activate

GET    /permissions
GET    /users/{id}/effective-permissions
GET    /users/{id}/permission-explanation
POST   /users/{id}/role-assignments
POST   /role-assignments/{id}/revoke
POST   /users/{id}/direct-permission-grants
POST   /direct-permission-grants/{id}/revoke
```

## Project và Listing Access

```text
GET    /users/{id}/project-access
POST   /project-access-grants
PATCH  /project-access-grants/{id}
POST   /project-access-grants/{id}/revoke

GET    /users/{id}/listing-access
POST   /listing-access-grants
POST   /listing-access-grants/{id}/revoke
```

## Share Grant

```text
POST   /resource-shares
GET    /resource-shares
POST   /resource-shares/{id}/revoke
```

## Delegation

```text
GET    /delegations
POST   /delegations
GET    /delegations/{id}
POST   /delegations/{id}/submit-review
POST   /delegations/{id}/approve
POST   /delegations/{id}/activate
POST   /delegations/{id}/revoke
GET    /delegations/{id}/usage
```

## Access Request

```text
GET    /access-requests
POST   /access-requests
GET    /access-requests/{id}
POST   /access-requests/{id}/cancel
POST   /access-requests/{id}/approve
POST   /access-requests/{id}/reject
```

## Access Review

```text
GET    /access-review-campaigns
POST   /access-review-campaigns
GET    /access-review-campaigns/{id}
POST   /access-review-campaigns/{id}/start
GET    /access-review-items
POST   /access-review-items/{id}/retain
POST   /access-review-items/{id}/revoke
POST   /access-review-items/{id}/reduce-scope
```

## Leave và Transfer

```text
GET    /workforce-leaves
POST   /workforce-leaves
GET    /workforce-leaves/{id}
POST   /workforce-leaves/{id}/approve
POST   /workforce-leaves/{id}/start
POST   /workforce-leaves/{id}/complete

POST   /workforce-transfer-requests
GET    /workforce-transfer-requests/{id}
POST   /workforce-transfer-requests/{id}/approve
POST   /workforce-transfer-requests/{id}/execute
```

## Offboarding

```text
GET    /offboarding-cases
POST   /offboarding-cases
GET    /offboarding-cases/{id}
POST   /offboarding-cases/{id}/approve
POST   /offboarding-cases/{id}/start
POST   /offboarding-cases/{id}/disable-account
POST   /offboarding-cases/{id}/complete
```

## Handover

```text
GET    /handover-cases
POST   /handover-cases
GET    /handover-cases/{id}
POST   /handover-cases/{id}/generate-items
POST   /handover-cases/{id}/start
POST   /handover-cases/{id}/complete

GET    /handover-cases/{id}/items
POST   /handover-items/{id}/send
POST   /handover-items/{id}/accept
POST   /handover-items/{id}/reject
POST   /handover-items/{id}/request-clarification
POST   /handover-items/{id}/complete
```

## Security

```text
GET    /users/{id}/sessions
POST   /user-sessions/{id}/revoke
GET    /users/{id}/devices
POST   /user-devices/{id}/trust
POST   /user-devices/{id}/block
GET    /security/access-events
```

Backend phải tự kiểm tra:

* Người gọi API.
* Legal Entity context.
* Role.
* Permission.
* Scope.
* Field policy.
* SoD.
* Approval.
* Effective date.
* User status.
* Project/Listing access.
* Delegation.
* MFA/re-authentication.

---

# 48. Candidate permission vocabulary — không phải Permission Registry canonical

> Các mã dưới đây là naming input. Exact permission codes, risk, allowed scopes, grant policies và incompatibilities thuộc Permission Registry và SoD Matrix.


## Workforce subject và Workforce

Party/Person permissions thuộc Party Permission Registry. IAM candidate permissions chỉ quản lý workforce reference và employment data.

```text
organization.workforce_subject.view_reference

organization.workforce.view
organization.workforce.create
organization.workforce.update
organization.workforce.terminate
organization.workforce.view_compensation_related
```

## User Account

```text
organization.user.view
organization.user.create
organization.user.update
organization.user.invite
organization.user.activate
organization.user.suspend
organization.user.deactivate
organization.user.unlock
organization.user.revoke_sessions
organization.user.view_security
organization.user.view_audit
```

## Organizational Unit

```text
organization.unit.view
organization.unit.create
organization.unit.update
organization.unit.restructure
organization.unit.activate
organization.unit.deactivate
```

## Position và Assignment

```text
organization.position.view
organization.position.create
organization.position.update
organization.position.assign

organization.assignment.view
organization.assignment.create
organization.assignment.update
organization.assignment.end
organization.assignment.transfer
```

## Role và Permission

```text
access.role.view
access.role.create
access.role.update_draft
access.role.simulate
access.role.review
access.role.approve
access.role.activate
access.role.assign
access.role.revoke

access.permission.view_catalog
access.permission.view_effective
access.permission.explain
access.permission.grant_direct
access.permission.revoke_direct
access.permission.grant_critical
```

## Scope và Field Policy

```text
access.scope.view
access.scope.assign
access.scope.revoke

access.field_policy.view
access.field_policy.create
access.field_policy.update
access.field_policy.assign
```

## Project/Listing Access

```text
access.project.view
access.project.grant
access.project.update
access.project.revoke

access.listing.view
access.listing.grant
access.listing.update
access.listing.revoke
```

## Delegation

```text
access.delegation.view
access.delegation.create
access.delegation.review
access.delegation.approve
access.delegation.activate
access.delegation.revoke
access.delegation.view_usage
```

## Access Request/Review

```text
access.request.create
access.request.view
access.request.review
access.request.approve
access.request.reject
access.request.cancel

access.review.view
access.review.create_campaign
access.review.perform
access.review.enforce
```

## Leave/Transfer/Offboarding

```text
workforce.leave.view
workforce.leave.create
workforce.leave.approve
workforce.leave.manage_coverage

workforce.transfer.view
workforce.transfer.create
workforce.transfer.review
workforce.transfer.approve
workforce.transfer.execute

workforce.offboarding.view
workforce.offboarding.create
workforce.offboarding.review
workforce.offboarding.approve
workforce.offboarding.execute
workforce.offboarding.emergency_disable
```

## Handover

```text
organization.handover.view
organization.handover.create
organization.handover.prepare
organization.handover.send
organization.handover.accept
organization.handover.reject
organization.handover.complete
organization.handover.override
organization.handover.view_audit

organization.handover_sla.view
organization.handover_sla.configure
organization.handover_sla.approve
organization.handover_sla.pause
organization.handover_sla.extend
```

## Security

```text
security.session.view
security.session.revoke
security.device.view
security.device.trust
security.device.block
security.risk.view
security.account.lock
security.emergency_access.grant
```

---

# 49. Candidate Role Bundles — không phải role baseline canonical

> Các bundles dưới đây là product examples. Exact role definitions, permissions, scopes và versioning thuộc Role Baseline Matrix và IAM configuration.


## 49.1. Sale

* Lead mine.
* Customer mine.
* Requirement mine.
* Listing theo project access.
* Matching.
* Deal mine.
* Proposal.
* Hold/Booking request.
* Task mine.
* Hoa hồng self.

Không có:

* Export hàng loạt.
* Phiếu thu.
* Xác nhận tiền.
* Duyệt giảm giá ngoài hạn mức.
* Revenue toàn công ty.
* Hoa hồng người khác.

## 49.2. Team Lead

* Dữ liệu team.
* Phân Lead.
* Handover team.
* Access request low-risk.
* Theo dõi SLA.
* Xác nhận co-sale theo policy.

Không mặc định có export.

## 49.3. Department Head

* Scope department.
* Approval trong hạn mức.
* Điều chuyển trong phòng.
* Theo dõi doanh số và SLA.

Không mặc định được thao tác tài chính.

## 49.4. Accounting

* Receipt.
* Allocation.
* Receivable.
* Reconciliation.
* Financial export theo scope.

## 49.5. Finance

* Refund.
* Transfer.
* Cash flow.
* Revenue funding.
* Payout review.

## 49.6. Legal

* Contract review.
* Party verification.
* Listing legal review.
* Termination legal review.

## 49.7. Inventory Manager

* Project inventory.
* Listing status.
* Hold/Booking inventory validation.
* Anti-double-sale.

## 49.8. Director

* `all` theo phạm vi Enterprise hoặc Legal Entity.
* Approval cấp cao.
* Export được audit.
* Revenue/commission tổng hợp.

---

# 50. Rule nghiệp vụ bắt buộc

1. Canonical Party/Person identity, Workforce và User Account là các concepts khác nhau.
2. User đã phát sinh dữ liệu không được xóa cứng.
3. Một Workforce có thể có nhiều assignment.
4. Assignment phải có ngày hiệu lực.
5. Assignment cũ không được ghi đè khi chuyển đơn vị.
6. Legal Entity master phải tham chiếu Platform Context.
7. Business Calendar phải tham chiếu Platform Context và version hiệu lực.
8. Chức danh không tự động cấp quyền.
9. Role là tập hợp permission, không phải logic hardcode.
10. Permission phải có action.
11. Permission truy cập dữ liệu phải có scope.
12. Không có scope không được mặc định thành `all`.
13. Backend phải resolve scope.
14. Frontend không được mở rộng scope.
15. `mine` phải dựa trên quan hệ nghiệp vụ hợp lệ.
16. `team` phải dựa trên assignment hiệu lực.
17. `department` phải dựa trên cấu trúc hiệu lực.
18. User nhiều pháp nhân phải có Legal Entity context.
19. Quyền pháp nhân A không áp dụng cho pháp nhân B.
20. Deny rõ ràng ưu tiên hơn Allow.
21. Field permission phải được backend enforce.
22. View không đồng nghĩa Export.
23. Sale, Team Lead và Department Head không mặc định được export.
24. Project Access không mở rộng Customer scope.
25. Listing Access không làm lộ toàn bộ Owner Profile.
26. Direct permission chỉ dùng cho ngoại lệ.
27. Direct permission phải có thời hạn khi có thể.
28. Quyền Critical phải có approval.
29. Temporary access phải tự hết hạn.
30. Emergency access phải có MFA và audit.
31. Delegation không vượt quyền gốc.
32. Delegation không mặc định cho phép sub-delegation.
33. Delegation phải có ngày kết thúc.
34. Approval authority phải có hạn mức khi liên quan tiền.
35. Người tạo không tự duyệt nếu policy cấm.
36. SoD conflict phải được kiểm tra trước khi cấp quyền.
37. Role active không sửa trực tiếp; phải tạo version.
38. Role mới không tự thay role lịch sử.
39. Access Review phải hỗ trợ thu hồi.
40. Onboarding chưa hoàn tất có thể bị giới hạn quyền.
41. User thử việc không mặc định có full access.
42. Leave không tự chuyển Customer vĩnh viễn.
43. Offboarding phải revoke session.
44. Offboarding phải ngừng phân Lead mới.
45. Team Lead là custodian mặc định nếu policy quy định.
46. Custodian không tự hưởng hoa hồng.
47. Handover phải theo từng resource.
48. Người nhận phải xác nhận handover.
49. Quá SLA không tự hoàn tất handover.
50. Handover SLA phải tham chiếu approved Platform policy.
51. Chuyển team không tự chuyển Deal.
52. Thay primary sale phải qua workflow của Transaction Context.
53. Customer core không có owner vĩnh viễn.
54. Commission đã hình thành không tự chuyển theo handover.
55. Thay manager phải giữ lịch sử.
56. Cơ cấu tổ chức phải có ngày hiệu lực.
57. Snapshot tổ chức phải được sử dụng cho giao dịch lịch sử.
58. Business Calendar thay đổi không tự sửa SLA cũ.
59. Service Account phải có owner.
60. Service Account không dùng như user giao diện.
61. MFA phải áp dụng cho quyền Critical theo policy.
62. Session phải có thể revoke.
63. Thiết bị lạ có thể bị yêu cầu xác minh.
64. Export API phải kiểm tra permission.
65. UI ẩn nút không được coi là authorization.
66. Account suspended không được thực hiện nghiệp vụ mới.
67. Account deactivated không được đăng nhập.
68. Dữ liệu lịch sử của user deactivated phải giữ.
69. Mọi cấp/thu hồi quyền phải có audit.
70. Mọi delegation usage phải có audit.
71. Mọi emergency access phải được review.
72. Permission explanation phải truy xuất được nguồn cấp.
73. Các phép kiểm tra scope phải thực hiện ở query layer.
74. Không tải dữ liệu toàn công ty rồi lọc tại frontend.
75. User không được tự nâng quyền.
76. CRM Admin không mặc định được duyệt tài chính.
77. Super Admin không mặc định được thay đổi tiền.
78. Access grant hết hạn phải tự thu hồi.
79. Approval pending phải được xử lý khi approver offboard.
80. Capability phải hỗ trợ một hoặc nhiều Legal Entity theo accepted enterprise boundary.

---

# 51. Cảnh báo và phát hiện bất thường

Hệ thống cần cảnh báo khi:

* User không có assignment active.
* User có nhiều assignment chính cùng Legal Entity.
* User có quyền `all` không có approval.
* User có direct grant Critical.
* Role có permission xung đột.
* User vi phạm SoD.
* Delegation vượt quyền gốc.
* Delegation sắp hết hạn nhưng còn approval pending.
* Quyền hết hạn nhưng vẫn được sử dụng.
* User offboard còn session active.
* User offboard còn API token.
* User nghỉ phép vẫn nhận Lead.
* Handover quá hạn.
* Deal active chưa có người nhận.
* Listing active không có sale phụ trách.
* User đổi team nhưng project access cũ chưa thu hồi.
* User nhiều Legal Entity sử dụng sai context.
* Thiết bị mới đăng nhập.
* Đăng nhập từ vị trí bất thường.
* User xem số lượng lớn Customer.
* User thử export không có quyền.
* User thay đổi tài khoản ngân hàng gần kỳ chi.
* Service Account không có owner.
* Service Account không sử dụng lâu.
* User Critical chưa bật MFA.
* Access Review quá hạn.
* Role không còn người quản lý.
* Organizational Unit không có manager.
* Approval policy resolve vào user inactive.
* Handover item bị từ chối nhiều lần.
* Emergency access được dùng ngoài sự cố.

---

# 52. Audit log

## 52.1. Thao tác bắt buộc

* Liên kết canonical Party/Person với Workforce.
* Tạo Workforce.
* Tạo User.
* Invite/activate.
* Suspend/deactivate.
* Unlock.
* Revoke session.
* Tạo đơn vị.
* Tái cấu trúc.
* Tạo assignment.
* Chuyển assignment.
* Tạo role.
* Thay role.
* Cấp role.
* Thu hồi role.
* Cấp direct permission.
* Cấp project/listing access.
* Share resource.
* Tạo delegation.
* Sử dụng delegation.
* Access request.
* Access review.
* Leave.
* Transfer.
* Offboarding.
* Handover.
* Emergency access.
* Export grant.
* Security lock.

## 52.2. Nội dung

* Actor.
* Subject user.
* Legal Entity.
* Assignment.
* Role.
* Permission.
* Scope.
* Resource.
* Before.
* After.
* Reason.
* Approval.
* IP.
* Device.
* Request ID.
* Correlation ID.
* Effective date.
* Expiration.
* Result.
* Timestamp.

Audit không được sửa bởi user thông thường.

---

# 53. Product baseline và deferred capability

> Phần này phân loại product baseline, không phải Sprint scope. Chỉ Current Sprint Detailed Execution Pack được phép kích hoạt implementation.


## 53.1. Bắt buộc

* Person.
* Workforce.
* User Account.
* Một hoặc nhiều Legal Entity.
* Organizational Unit.
* Position.
* Employment Assignment.
* Manager relationship.
* Role.
* Permission.
* Scope `mine/team/department/legal_entity/all`.
* Role Assignment.
* Direct Grant có kiểm soát.
* Field masking cơ bản.
* Project Access.
* Delegation cơ bản.
* Approval Authority.
* Onboarding.
* Transfer.
* Leave.
* Offboarding.
* Handover.
* Business Calendar assignment.
* Approval Engine integration.
* Notification.
* Session revocation.
* MFA flag.
* Audit.
* Export restriction.
* Permission explanation.
* SQL scope enforcement.

## 53.2. Giai đoạn nâng cao

* Listing-level access.
* Full ABAC.
* Just-in-time access.
* Emergency access.
* Automated access review.
* SoD simulation nâng cao.
* Device trust.
* Risk-based authentication.
* SSO đa nhà cung cấp.
* Passkey.
* External User.
* Partner Portal.
* Position budgeting.
* Org chart visual versioning.
* Automated deprovisioning.
* SCIM.
* HRIS integration.
* Privileged access management.

---

# 54. Capability acceptance outcomes

> Đây là product acceptance inventory. Exact automated/manual test cases và evidence thuộc Testing Standards, UAT Plan và Sprint Acceptance Reports.


Capability acceptance baseline được xem là đáp ứng khi:

1. Liên kết được canonical Party/Person identity với IAM Workforce.
2. Tạo được Workforce Profile.
3. Tạo được User Account.
4. Một canonical Party/Person có thể tồn tại mà chưa có Workforce hoặc User Account.
5. User bị deactivated vẫn giữ lịch sử.
6. Tạo được nhiều Legal Entity assignment.
7. Một user có thể làm việc cho nhiều Legal Entity.
8. Quyền Legal Entity A không dùng được ở B.
9. Tạo được Branch/Department/Team.
10. Cấu trúc đơn vị có parent.
11. Cấu trúc có ngày hiệu lực.
12. Thay parent không xóa lịch sử.
13. Tạo được Position.
14. Gán user vào Position.
15. Tạo được Employment Assignment.
16. Assignment có manager.
17. Assignment có Business Calendar.
18. Assignment cũ được kết thúc thay vì ghi đè.
19. Tạo được Role.
20. Role có version.
21. Role active không sửa trực tiếp.
22. Tạo được Permission Catalog.
23. Permission có risk level.
24. Permission có allowed scope.
25. Gán role cho user.
26. Role assignment có ngày hiệu lực.
27. Role hết hạn tự ngừng.
28. Resolve được effective permission.
29. Giải thích được nguồn quyền.
30. `mine` hoạt động đúng.
31. `team` hoạt động đúng.
32. `department` hoạt động đúng.
33. `legal_entity` hoạt động đúng.
34. `all` chỉ có khi được cấp.
35. Frontend gửi `all` không mở rộng quyền.
36. Thay URL không mở rộng quyền.
37. Query scope được enforce ở backend.
38. Field masking hoạt động.
39. User không có quyền không nhận full phone.
40. View không cho export.
41. Sale không export hàng loạt.
42. Team Lead không export hàng loạt.
43. Department Head không export hàng loạt.
44. Project Access giới hạn đúng dự án.
45. Project Access không mở Customer ngoài scope.
46. Tạo được Share Grant có thời hạn.
47. Share Grant hết hạn tự thu hồi.
48. Tạo được Direct Grant.
49. Direct Grant Critical cần approval.
50. SoD conflict được phát hiện.
51. Không cấp role xung đột nếu policy chặn.
52. Tạo được Delegation.
53. Delegation không vượt quyền gốc.
54. Delegation có ngày kết thúc.
55. Delegation usage được audit.
56. Tạo được Approval Authority.
57. Hạn mức duyệt được kiểm tra.
58. User không tự duyệt khi policy cấm.
59. Tạo được Access Request.
60. Access Request chạy qua Approval Engine.
61. Quyền chỉ cấp sau approval.
62. Tạo được Access Review.
63. Reviewer có thể thu hồi quyền.
64. Onboarding tạo đủ assignment và role.
65. User mới có thể bị giới hạn trước đào tạo.
66. Tạo được Leave Record.
67. User nghỉ không nhận Lead mới theo policy.
68. Leave delegation tự kết thúc.
69. Chuyển team tạo assignment mới.
70. Chuyển team tạo Handover Case.
71. Deal không tự đổi sale chỉ vì chuyển team.
72. Offboarding disable user.
73. Offboarding revoke session.
74. Offboarding thu hồi delegation.
75. Offboarding tạo handover.
76. Team Lead làm custodian theo policy.
77. Custodian không tự hưởng commission.
78. Handover có nhiều item.
79. Người nhận accept/reject được.
80. Handover có SLA.
81. SLA lấy từ approved Platform policy/version.
82. SLA có cảnh báo.
83. Quá SLA không tự complete.
84. Handover resource được owning Context cập nhật qua approved command/workflow.
85. Business Calendar resolve đúng.
86. Calendar user override hoạt động.
87. Calendar thay đổi không sửa SLA cũ.
88. MFA flag áp dụng cho permission Critical.
89. Session được liệt kê.
90. Admin revoke session được.
91. Thiết bị có trust status.
92. User suspended không thao tác được.
93. Service Account có owner.
94. Service Account không đăng nhập UI.
95. Mọi cấp quyền có audit.
96. Mọi thu hồi quyền có audit.
97. Mọi thay assignment có audit.
98. Emergency access có audit.
99. Dashboard drill-down đúng scope.
100. Báo cáo không lộ dữ liệu ngoài quyền.
101. Capability hoạt động với doanh nghiệp một Legal Entity.
102. Capability hoạt động với nhiều Legal Entity.
103. Role bundle có thể dùng cho doanh nghiệp nhỏ.
104. Doanh nghiệp lớn có thể tách quyền mà không sửa code.
105. User nghỉ việc vẫn có thể được xử lý hoa hồng lịch sử.
106. Thay manager không làm mất approval history.
107. Approval pending có thể được re-route theo policy.
108. Không có permission nào được hardcode theo chức danh.
109. Không có scope nào được frontend tự quyết định.
110. Capability cung cấp identity và authorization ổn định cho các owning Context còn lại.

---

# 55. Anti-patterns và canonical requirements

Phần này trình bày trực tiếp các hành vi bị cấm và quy tắc canonical của dự án Greenfield.

## AP-IAM-001 — Một user chỉ có một công ty hoặc một team

**Không được áp dụng**

Giả định một User luôn thuộc duy nhất một Legal Entity, team hoặc project role.

**Canonical requirement**

Workforce có thể có nhiều effective Employment Assignments. Mỗi authorization decision phải xác định Legal Entity context, active assignment và resource relationship phù hợp.

## AP-IAM-002 — Chức danh tự cấp quyền

**Không được áp dụng**

Hardcode quyền theo Position hoặc title, ví dụ “Trưởng phòng mặc định xem toàn phòng”.

**Canonical requirement**

Position mô tả tổ chức. Effective access đến từ Permission Registry, role/grant, scope resolution, field policy, SoD, effective dates và resource relationships.

## AP-IAM-003 — Scope list hardcode trong code

**Không được áp dụng**

Mỗi Context tự tạo một danh sách scope hoặc tự diễn giải `mine`, `team`, `department`, `all`.

**Canonical requirement**

Exact vocabulary và semantics thuộc Scope Resolution Specification. Mọi Context phải dùng shared resolver contract nhưng enforce quan hệ nghiệp vụ của chính mình.

## AP-IAM-004 — Frontend quyết định scope

**Không được áp dụng**

Tin `owner_id`, `team_id`, `legal_entity_id`, `scope=all` hoặc URL parameter từ frontend để mở rộng quyền.

**Canonical requirement**

Backend resolve effective scope từ authenticated principal, active assignments, permission grants và resource relationships; filters phải được enforce tại query/data-access boundary.

## AP-IAM-005 — View access đồng nghĩa Export access

**Không được áp dụng**

Người xem được records mặc định được export hàng loạt hoặc tải full sensitive fields.

**Canonical requirement**

View, field reveal, breakdown, detail và export là các capabilities độc lập; export phải enforce scope, masking, approval, purpose và Audit theo policy.

## AP-IAM-006 — Role là nguồn chân lý cuối cùng

**Không được áp dụng**

Chỉ kiểm tra role name hoặc generic `is_admin`.

**Canonical requirement**

Role chỉ là versioned permission bundle. Effective authorization còn phụ thuộc scope, deny, field policy, Legal Entity, project/listing access, delegation, SoD, resource state và effective dates.

## AP-IAM-007 — Mutable active role/grant

**Không được áp dụng**

Sửa trực tiếp active Role Bundle, Permission Grant hoặc Approval Authority.

**Canonical requirement**

Critical definitions và grants phải có version/effective period, review/approval khi phù hợp và historical lineage.

## AP-IAM-008 — Direct grant là cơ chế bình thường

**Không được áp dụng**

Dùng direct permission grants để bù cho role design không đầy đủ.

**Canonical requirement**

Direct grant chỉ dành cho ngoại lệ có reason, owner, approval, expiry, review và automatic revocation.

## AP-IAM-009 — Delegation chuyển toàn bộ quyền

**Không được áp dụng**

Delegation vô thời hạn, vượt quyền gốc hoặc tự cho phép sub-delegation.

**Canonical requirement**

Delegation phải giới hạn action, scope, resource, authority limit và effective period; không vượt quyền gốc và phải kiểm tra SoD.

## AP-IAM-010 — Transfer/leave/offboarding tự chuyển business ownership

**Không được áp dụng**

Khi Workforce chuyển team, nghỉ phép hoặc nghỉ việc, IAM direct-update Lead, Customer, Listing, Deal, Booking, Contract hoặc Commission.

**Canonical requirement**

IAM tạo approved Handover Plan và phát business facts. Owning Context thực hiện reassignment/coverage theo workflow và giữ historical attribution.

## AP-IAM-011 — Project access mở Customer scope

**Không được áp dụng**

Quyền bán Project hoặc xem Listing mặc định cho phép xem mọi Customer liên quan.

**Canonical requirement**

Project/Listing access và Customer access là các policy dimensions riêng; kết quả phải là intersection của effective grants và resource relationships.

## AP-IAM-012 — Xóa User/Workforce để offboard

**Không được áp dụng**

Hard-delete User, Workforce hoặc assignments đã tham gia business records.

**Canonical requirement**

Offboarding phải deactivate account, revoke sessions/grants, end assignments và giữ immutable historical references.

## AP-IAM-013 — Super Admin bypass business controls

**Không được áp dụng**

Super Admin hoặc CRM Admin mặc định được duyệt tài chính, thay đổi tiền hoặc xem mọi PII.

**Canonical requirement**

Administrative access và business authority tách biệt. Sensitive actions vẫn cần permission, scope, SoD, approval, re-authentication và Audit.

## AP-IAM-014 — IAM tạo Person/Customer master cạnh tranh

**Không được áp dụng**

Tạo Person master trong IAM độc lập với Party Context hoặc dùng Workforce record thay Customer.

**Canonical requirement**

Party Context sở hữu canonical human/organization identity. IAM sở hữu Workforce, account và access relationships qua stable reference.

## AP-IAM-015 — Candidate examples là exact contracts

**Không được áp dụng**

Code trực tiếp từ candidate tables, endpoint lists, Event names, permission codes hoặc role examples trong Capability Specification.

**Canonical requirement**

Exact implementation chỉ có hiệu lực khi được khóa trong Context Packs, Alembic, OpenAPI, Event schemas và security registries.

## AP-IAM-016 — Legacy migration mặc định

**Không được áp dụng**

Suy luận rằng có hệ thống tiền nhiệm, user/role schema cũ hoặc compatibility layer phải duy trì.

**Canonical requirement**

`crm_bds_ai` là Greenfield. Legacy migration chỉ được thực hiện khi có approved scope, mapping, reconciliation, security review và acceptance criteria riêng.

---

# 56. Platform configuration references sử dụng bởi IAM

Danh sách dưới đây là candidate configuration vocabulary, không phải Config Registry canonical.

IAM Context Pack phải xác định chính xác các configuration definitions cần thiết, có thể bao gồm:

```text
organization.default_business_calendar
organization.employee_numbering_scheme
organization.default_onboarding_workflow
organization.default_transfer_workflow
organization.default_leave_workflow
organization.default_offboarding_workflow
organization.default_handover_workflow

organization.handover_sla_policy
organization.handover_custodian_policy
organization.leave_access_policy
organization.offboarding_disable_policy

access.role_grant_approval_policy
access.critical_permission_approval_policy
access.delegation_approval_policy
access.project_access_approval_policy
access.export_grant_approval_policy
access.access_review_frequency

security.mfa_required_roles
security.mfa_required_permissions
security.session_policy
security.device_trust_policy
security.emergency_access_policy
```

Mỗi accepted Configuration Definition phải có:

- Owner.
- Schema.
- Allowed scopes.
- Resolution strategy.
- Version/effective period.
- Approval requirements.
- Data classification.
- Consumers.
- Tests và Audit behavior.

---

# 57. Candidate business facts và Event traceability

Các business facts dưới đây là candidate inventory để phân tích, không phải canonical Event names hoặc payloads:

```text
Workforce created or ended
User invited, activated, suspended, locked or deactivated
Organizational Unit changed
Employment Assignment started, ended or transferred
Role/access grant activated, expired or revoked
Project/Listing access changed
Delegation activated, expired or revoked
Leave coverage started or completed
Handover started, item accepted/rejected or completed
Offboarding started, account disabled or completed
```

Exact Event contract phải xác định trong Event Registry, JSON Schema và AsyncAPI:

- Event owner.
- Stable name.
- Version.
- Aggregate/resource identity.
- Occurred-at semantics.
- Correlation/causation.
- Minimal payload.
- Data classification.
- Producer transaction.
- Consumers.
- Idempotency and ordering expectations.
- Replay/reconciliation behavior.

Consumer phải idempotent theo Event Standards.

---

# 58. System invariant

Các system invariants sau không được cấu hình tắt:

1. Backend authorization luôn hoạt động.
2. User deactivated không được đăng nhập.
3. Permission không có scope không mặc định thành `all`.
4. User không thể tự cấp quyền cho chính mình nếu không có authority hợp lệ.
5. Delegation không vượt quyền gốc.
6. Audit facts về access không được sửa bởi normal IAM workflows.
7. Session phải revoke được.
8. Scope phải enforce ở query layer.
9. Field nhạy cảm không được gửi ngoài quyền.
10. Offboarding không xóa lịch sử user.
11. Số liệu giao dịch không tự chuyển chỉ vì user chuyển đơn vị.
12. Expired grant không còn hiệu lực.
13. Legal Entity context phải được kiểm tra.
14. SoD Critical không được bỏ qua không có approval.
15. Service Account không được dùng như người dùng thông thường.

---

# 59. Kết luận

Identity, Access and Organization Capability cung cấp identity, workforce, organization và authorization control plane cho `crm_bds_ai`.

Capability phải bảo đảm:

- Canonical Party/Person identity không bị sao chép thành source of truth cạnh tranh.
- Workforce, Employment Assignment và User Account là các concepts riêng.
- Nhiều Legal Entity được hỗ trợ mà không trộn authority.
- Organizational structure có version/effective history.
- Position không bị hardcode thành permission.
- Authorization dựa trên permission, effective scope, field policy, resource relationship, SoD và effective dates.
- Project/Listing access không mở rộng Customer scope.
- Delegation và temporary access có giới hạn, expiry và lineage.
- Approval Authority có basis và limits.
- Onboarding, transfer, leave, offboarding và handover có workflow được kiểm soát.
- IAM không direct-write business aggregates của Context khác.
- User deactivation không làm mất historical attribution, Commission rights hoặc Audit evidence.
- Export, sessions, service accounts và Critical access được quản trị riêng.
- Backend là final authorization boundary.
- Exact contracts được quản lý bởi machine-readable sources và security registries.

> IAM phải được ổn định trước khi các Context nghiệp vụ phụ thuộc sâu vào identity và authorization, nhưng Capability Specification này không tự kích hoạt Sprint hoặc cho phép code trước khi IAM Context Pack và current Sprint Pack đạt Definition of Ready.
