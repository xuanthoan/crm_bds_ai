# CRM_BDS_AI — CAPABILITY 01: PLATFORM CONFIGURATION

## Nền tảng hệ thống và cấu hình doanh nghiệp

**Document ID:** `PROD-CAP-PLA-001`  
**Canonical path:** `docs/product/capabilities/cap-01-platform-configuration.md`  
**Product:** `crm_bds_ai`  
**Version:** `1.0.0`  
**Status:** `Accepted / Product Capability Baseline`  
**Document type:** `Product Capability Specification`  
**Primary capability code:** `CAP-PLA`  
**Primary owning Context:** `platform`  
**Owner:** `Product Owner`  
**Co-owner:** `Platform Domain Owner`  
**Reviewers:** `Architecture Owner`, `Security Owner`, `Database Owner`, `API Owner`, `Event Architecture Owner`, `Operations Owner`, `QA Owner`  
**Effective date:** `2026-08-05`  
**Last reviewed:** `2026-08-05`  
**Classification:** `INTERNAL`

---

# 0. Phạm vi thẩm quyền và quan hệ tài liệu

Tài liệu này là nguồn canonical cho:

- Mục tiêu sản phẩm của Platform Configuration Capability.
- Business outcomes và capability boundaries.
- Enterprise, Legal Entity, Business Calendar, Numbering, Configuration, Workflow Definition, Approval Policy và các control-plane policies.
- Business rules, invariants, acceptance outcomes và anti-patterns của capability.
- Đầu vào phân tích cho Platform Context Implementation Pack.

Tài liệu này không phải nguồn exact cho:

- Physical database schema hoặc DDL.
- Exact API paths, request/response payloads.
- Exact Event names hoặc Event payloads.
- Exact permission codes, scopes hoặc role matrix.
- Exact queue, retry, timeout, retention hoặc deployment configuration.
- Exact implementation của các Context khác.

Nguồn exact tương ứng:

| Chủ đề | Nguồn canonical |
|---|---|
| Thuật ngữ | Domain Glossary |
| Product requirements | PRD |
| Context ownership | Source of Truth Matrix |
| Architecture boundaries | Architecture Overview, Context Map và Accepted ADRs |
| Platform behavior chi tiết | Platform Context Implementation Pack |
| Database | Alembic migrations và Context DB Specification |
| API | OpenAPI |
| Events | JSON Schema và AsyncAPI |
| Permissions/scopes/masking | Security registries và matrices |
| Runtime values | Environment configuration và IaC |
| Công việc hiện tại | Current Sprint Detailed Execution Pack |

**Capability không đồng nghĩa Bounded Context.** Capability này chủ yếu được thực hiện bởi `platform` Context, nhưng có các điểm phối hợp với `iam`, `activity`, `documents`, `audit`, `integration` và `operations`. Mỗi Context vẫn giữ quyền sở hữu dữ liệu và hành vi của mình.

Các phần “candidate data model”, “candidate application operations” và “candidate permission vocabulary” trong tài liệu này chỉ là đầu vào thiết kế. Chúng không được dùng thay migrations, OpenAPI hoặc registries đã được chấp nhận.

---
# 1. Mục tiêu của capability

Platform Configuration Capability cung cấp lớp control plane thống nhất cho `crm_bds_ai`.

Capability quy định các năng lực sản phẩm liên quan đến:

- Hồ sơ Enterprise và business operating boundary.
- Hồ sơ Legal Entity nội bộ.
- Cấu hình mặc định và cấu hình theo scope.
- Config Registry, schema, version và effective period.
- Danh mục nghiệp vụ dùng chung.
- Múi giờ, ngôn ngữ, tiền tệ và định dạng.
- Business Calendar và reporting-period metadata.
- Numbering policies và issuance governance.
- Workflow Definition và transition policy.
- Approval Policy, authority limits và Segregation of Duties.
- SLA Policy và escalation definition.
- Notification policy và template definition.
- Feature configuration.
- Integration profile definition và secret reference.
- Webhook, Event và job policy definitions.
- Import/export control policies.
- Security, retention và data-governance baselines ở mức policy.
- Audit đối với thay đổi cấu hình.
- Versioning, effective dating và impact simulation.

Capability này không sở hữu business records như:

- User/workforce và organization assignments.
- Lead.
- Party, Customer và Customer Identity.
- Project, Asset, Ownership, Selling Right, Listing và Availability.
- Matching results.
- Deal, Transaction Case, Hold và Booking.
- Contract, Payment, Receipt, Refund và Settlement.
- Revenue và Commission.
- Task, Appointment và Interaction.
- Marketing execution.
- Analytics projections.
- Document runtime, Audit facts, Integration runtime hoặc Operations runtime.

Các records trên thuộc owning Context tương ứng.

Platform Configuration Capability cung cấp:

- Policy definitions.
- Configuration definitions và values.
- Versioned control-plane metadata.
- Shared business calendars và numbering definitions.
- Workflow/approval/SLA definitions.
- Template và feature definitions.
- Resolution và explanation services.

Nguyên tắc canonical:

> Quy tắc có thể thay đổi theo chính sách doanh nghiệp phải được quản trị bằng cấu hình có schema, scope, version, effective period, approval và Audit khi phù hợp. System invariants vẫn phải được bảo vệ trong owning Context và không được biến thành công tắc có thể tắt.

---
# 2. Vị trí của capability trong toàn hệ thống

Platform Configuration Capability là control plane dùng chung, không phải một “siêu module” sở hữu mọi runtime behavior.

```text
Platform Configuration Capability
        ↓ cung cấp definitions, policies và resolution
CAP-IAM  Identity, Access and Organization
CAP-PAR  Party, Customer and Requirement
CAP-LEA  Lead Management
CAP-PRO  Product, Asset, Listing and Inventory
CAP-MAT  Matching
CAP-TRA  Deal and Transaction
CAP-CON  Contract and Cash
CAP-REV  Revenue and Commission
CAP-ACT  Activity and Engagement
CAP-MAR  Marketing
CAP-ANA  Analytics
CAP-DOC  Documents and Dossier
CAP-AUD  Audit and Control
CAP-INT  Integration
CAP-OPE  Operations
```

Các capability và Context nghiệp vụ sử dụng Platform definitions khi cần:

- Danh mục và configuration resolution.
- Business Calendar.
- Numbering definition.
- Workflow Definition.
- Approval Policy.
- SLA Policy.
- Template.
- Feature configuration.
- Integration profile definition.
- Retention/security policy reference.

Platform Context không được:

- Trực tiếp thay đổi aggregate của Context khác.
- Trở thành source of truth cho business state của Context khác.
- Dùng generic workflow để bypass Domain invariant.
- Dùng configuration để vô hiệu hóa security, audit hoặc financial integrity.
- Sở hữu runtime delivery chỉ vì Platform định nghĩa policy.

Một capability/Context chỉ được tích hợp với Platform qua published application contracts hoặc Events phù hợp.

---
# 3. Ranh giới sở hữu dữ liệu

## 3.1. Platform Context sở hữu

- Enterprise Profile và operating-boundary metadata.
- Legal Entity Profile và Legal Entity capability metadata.
- Configuration Definition.
- Configuration Value và Configuration Version.
- Configuration Scope và resolution policy.
- Business Dictionary definitions.
- Business Calendar definitions và versions.
- Numbering Scheme definitions và issuance governance.
- Workflow Definition và Workflow Version.
- Approval Policy và authority-definition metadata.
- SLA Policy definitions.
- Notification Template và Notification Policy definitions.
- Feature Configuration definitions.
- Integration Profile definitions và secret references.
- Job Schedule definitions.
- Import/export policy definitions.
- Retention, security và data-governance policy references.
- Audit-worthy configuration change metadata.

## 3.2. Platform Context không sở hữu

- User, Workforce, Organization Unit, role assignment và delegation runtime: `iam`.
- Party, Customer, Customer Identity, Requirement và Financial Profile: `party`.
- Lead, assignment và care-protection lifecycle: `lead`.
- Asset, Ownership, Selling Right, Listing, Availability và Commercial Lock: `product`.
- Matching execution và results: `matching`.
- Deal, Transaction Case, Hold và Booking: `transaction`.
- Contract, Payment, Receipt, Refund và Settlement: `contract`.
- Revenue và Commission: `revenue`.
- Task, Appointment, Interaction và operational SLA instances: `activity`.
- Campaign, audience, journey và marketing execution: `marketing`.
- Analytical projections, Metrics, Snapshots và Forecasts: `analytics`.
- File, Document, Dossier và signature evidence runtime: `documents`.
- Immutable Audit facts: `audit`.
- Connection, webhook, sync và reconciliation runtime: `integration`.
- Jobs, queues, incidents, backup, restore và deployment runtime: `operations`.

## 3.3. Control Plane và Runtime Plane

Platform có thể định nghĩa policy, nhưng runtime instance thuộc owning Context.

Ví dụ:

| Definition/Policy | Runtime owner |
|---|---|
| SLA Policy | `activity` hoặc owning Context theo Context Pack |
| Notification Policy/Template | runtime delivery owner theo Context Map |
| Integration Profile/Secret Reference | `integration` |
| Job Schedule Definition | `operations` |
| Retention Policy | owning data Context + `documents`/`audit` khi phù hợp |
| Workflow Definition | owning business Context thực thi transition |
| Approval Policy | approval runtime owner theo Platform Context Pack |
| Security baseline | `iam` và Security Architecture enforce |
| Audit policy | `audit` ghi Audit facts |

## 3.4. Nguyên tắc tham chiếu

Business records phải giữ đủ reference hoặc snapshot để xác định chính sách đã áp dụng, ví dụ:

- Configuration ID và version.
- Policy ID và version.
- Workflow Definition ID và version.
- SLA Policy ID và version.
- Template ID và version.
- Business Calendar version.
- Numbering Scheme version.
- Effective scope và resolved-policy evidence khi cần.

Không chỉ tham chiếu “giá trị hiện tại” khi nghiệp vụ lịch sử cần tái tạo quyết định tại thời điểm phát sinh.

---
# 4. Nguyên tắc thiết kế cốt lõi

## 4.1. Một nguồn cấu hình chuẩn duy nhất

Mỗi loại cấu hình phải có một nguồn chính thức.

Không để đồng thời tồn tại:

* Một rule trong source code.
* Một rule khác trong database.
* Một rule khác trong frontend.
* Một rule khác trong file môi trường.

Nếu cấu hình được phép thay đổi theo doanh nghiệp, nguồn chuẩn phải nằm trong hệ thống cấu hình.

---

## 4.2. Không hardcode quy tắc kinh doanh thay đổi được

Không hardcode trực tiếp:

* Thời gian SLA.
* Tỷ lệ phê duyệt.
* Hạn mức giảm giá.
* Số cấp duyệt.
* Trạng thái hiển thị.
* Tên giai đoạn pipeline.
* Ngày nghỉ.
* Mẫu mã chứng từ.
* Kênh thông báo.
* Số lần retry.
* Quy tắc escalation.
* Mốc ghi nhận Revenue.
* Mốc ghi nhận hoa hồng.

Những quy tắc này phải được cấu hình theo phạm vi phù hợp.

---

## 4.3. Không biến mọi thứ thành cấu hình

Không phải dữ liệu nào cũng nên cho người dùng thay đổi tự do.

Cần phân biệt:

### System invariant

Quy tắc kỹ thuật không được thay đổi qua giao diện thông thường.

Ví dụ:

* Một Booking không được tạo hai lần bằng cùng idempotency key.
* Allocation không được vượt số tiền nguồn.
* Audit log không được sửa.
* Phiếu thu đã phát hành không được sửa trực tiếp.
* Một Listing độc quyền không được có hai trạng thái bán active trái phép.
* Permission phải được backend kiểm tra.

### Configurable business rule

Quy tắc được phép thay đổi có kiểm soát.

Ví dụ:

* SLA xử lý Lead.
* Hạn mức giảm giá.
* Pipeline.
* Ngày làm việc.
* Cấp duyệt.
* Template thông báo.
* Thời gian bảo vệ Lead.
* Chính sách chi hoa hồng.

Không được đưa system invariant thành một công tắc mà người dùng có thể tắt tùy ý.

---

## 4.4. Cấu hình phải có phiên bản

Cấu hình quan trọng phải có:

* Version.
* Ngày hiệu lực.
* Ngày hết hiệu lực.
* Trạng thái.
* Người tạo.
* Người kiểm tra.
* Người duyệt.
* Lý do thay đổi.
* Dữ liệu trước.
* Dữ liệu sau.

Chính sách mới không tự động làm thay đổi dữ liệu lịch sử.

---

## 4.5. Cấu hình phải có phạm vi

Một cấu hình có thể áp dụng cho:

* Toàn hệ thống.
* Toàn công ty.
* Pháp nhân.
* Chi nhánh.
* Phòng.
* Team.
* Dự án.
* Đợt mở bán.
* Loại tài sản.
* Mô hình giao dịch.
* Loại hợp đồng.
* Loại Lead.
* Loại Customer.
* Kênh bán.
* Một đối tượng cụ thể.

Cơ chế chọn cấu hình phải có thứ tự ưu tiên rõ ràng.

---

## 4.6. Cấu hình không được áp dụng hồi tố âm thầm

Khi kích hoạt cấu hình mới:

* Dữ liệu mới sử dụng cấu hình mới.
* Dữ liệu cũ tiếp tục dùng phiên bản cũ.
* Chỉ áp dụng lại dữ liệu cũ khi có migration hoặc recalculation được phê duyệt.

Ví dụ:

* Pipeline mới không tự chuyển Deal cũ.
* SLA mới không tự tính lại toàn bộ SLA cũ.
* Chính sách hoa hồng mới không tự sửa giao dịch cũ.
* Mẫu mã hợp đồng mới không đổi số hợp đồng đã phát hành.

---

## 4.7. Maker–checker–approver

Các cấu hình nhạy cảm phải hỗ trợ:

* Người tạo.
* Người kiểm tra.
* Người phê duyệt.
* Người kích hoạt.

Tùy doanh nghiệp, một số bước có thể được gộp.

Tuy nhiên phải có khả năng ngăn một người:

* Tự tạo.
* Tự duyệt.
* Tự kích hoạt.

đối với cấu hình vượt hạn mức hoặc có rủi ro cao.

---

# 5. Hồ sơ doanh nghiệp vận hành hệ thống

## 5.1. Enterprise Profile

Hệ thống có một hồ sơ doanh nghiệp cấp cao đại diện cho nhóm doanh nghiệp sử dụng CRM.

Thông tin gồm:

* Tên doanh nghiệp.
* Tên thương mại.
* Mã doanh nghiệp nội bộ.
* Logo.
* Website.
* Email chung.
* Số điện thoại chung.
* Địa chỉ.
* Quốc gia.
* Múi giờ mặc định.
* Ngôn ngữ mặc định.
* Tiền tệ mặc định.
* Định dạng ngày.
* Định dạng số.
* Năm tài chính.
* Trạng thái hoạt động.
* Người đại diện quản trị.
* Thông tin hỗ trợ nội bộ.

## 5.2. Không đồng nhất Enterprise với Legal Entity

Enterprise đại diện cho nhóm vận hành.

Legal Entity đại diện cho pháp nhân cụ thể có thể:

* Đứng tên dự án.
* Ký hợp đồng.
* Nhận tiền.
* Xuất hóa đơn.
* Ghi nhận doanh thu.
* Trả hoa hồng.

Một Enterprise có thể có nhiều Legal Entity.

---

# 6. Quản lý pháp nhân nội bộ

## 6.1. Legal Entity

Thông tin một pháp nhân gồm:

* Mã pháp nhân.
* Tên pháp lý.
* Tên viết tắt.
* Mã số thuế.
* Số đăng ký doanh nghiệp.
* Ngày thành lập.
* Địa chỉ đăng ký.
* Người đại diện pháp luật.
* Chức danh người đại diện.
* Loại pháp nhân.
* Quốc gia.
* Tiền tệ kế toán.
* Múi giờ.
* Trạng thái.
* Ngày bắt đầu sử dụng.
* Ngày kết thúc sử dụng.
* Logo và con dấu metadata.
* Link tài liệu pháp lý.
* Thông tin tài khoản nhận tiền.
* Quyền được sử dụng trong từng nghiệp vụ.

## 6.2. Loại pháp nhân

* Công ty vận hành.
* Công ty mẹ.
* Công ty con.
* Công ty dự án.
* Pháp nhân chủ đầu tư.
* Pháp nhân bán hàng.
* Pháp nhân thu tiền.
* Pháp nhân trả hoa hồng.
* Pháp nhân quản lý tài sản.
* Loại khác.

Một pháp nhân có thể có nhiều vai trò.

## 6.3. Legal Entity Role

Ví dụ:

* `OPERATING_COMPANY`
* `PROJECT_DEVELOPER`
* `LEGAL_SELLER`
* `PAYMENT_COLLECTOR`
* `REVENUE_BENEFICIARY`
* `COMMISSION_PAYER`
* `ASSET_OWNER`
* `SERVICE_PROVIDER`

Các vai trò này không thay thế vai trò của công ty trong từng Transaction Case.

Vai trò pháp nhân cho biết pháp nhân có thể được chọn vào nghiệp vụ nào.

## 6.4. Không xóa pháp nhân đã phát sinh dữ liệu

Pháp nhân đã được sử dụng trong:

* Project.
* Listing.
* Contract.
* Receipt.
* Revenue.
* Commission.

không được xóa cứng.

Chỉ được:

* Ngừng sử dụng.
* Đặt ngày hết hiệu lực.
* Thay thế.
* Lưu trữ.

---

# 7. Cấu hình đa pháp nhân

## 7.1. Cấu hình có thể khác theo pháp nhân

Ví dụ:

* Mẫu số hợp đồng.
* Tài khoản nhận tiền.
* Người ký.
* Logo.
* Con dấu.
* Mẫu email.
* Tiền tệ.
* Quy trình duyệt.
* Chính sách phiếu thu.
* Kỳ hoa hồng.
* Mẫu báo cáo.

## 7.2. Cấu hình pháp nhân không tự áp dụng toàn nhóm

Khi một cấu hình thuộc pháp nhân A:

* Không áp dụng cho pháp nhân B.
* Trừ khi cấu hình được kế thừa từ Enterprise.
* Hoặc có scope cụ thể bao gồm nhiều pháp nhân.

## 7.3. Giao dịch giữa các pháp nhân nội bộ

Platform Configuration Capability phải cho phép khai báo quan hệ:

* Pháp nhân phát triển dự án.
* Pháp nhân bán hàng.
* Pháp nhân thu hộ.
* Pháp nhân hưởng doanh thu.
* Pháp nhân trả hoa hồng.

Việc hạch toán liên công ty không thuộc phạm vi CRM lõi, nhưng phải lưu đủ dữ liệu để tích hợp kế toán.

---

# 8. Cấu trúc phạm vi cấu hình

## 8.1. Các scope cấu hình

* `SYSTEM`
* `ENTERPRISE`
* `LEGAL_ENTITY`
* `BRANCH`
* `DEPARTMENT`
* `TEAM`
* `PROJECT`
* `SALES_LAUNCH`
* `TRANSACTION_MODEL`
* `PROPERTY_TYPE`
* `CONTRACT_TYPE`
* `LEAD_TYPE`
* `CUSTOMER_SEGMENT`
* `USER`
* `RESOURCE`

## 8.2. Quy tắc ưu tiên cấu hình

Mặc định, cấu hình cụ thể hơn được ưu tiên hơn cấu hình tổng quát.

Ví dụ:

```text
Resource cụ thể
→ Sales Launch
→ Project
→ Team
→ Department
→ Branch
→ Legal Entity
→ Enterprise
→ System Default
```

Tuy nhiên không áp dụng một thứ tự duy nhất cho mọi loại cấu hình.

Mỗi config schema phải xác định:

* Scope nào được phép.
* Thứ tự ưu tiên.
* Có được override hay không.
* Có được cộng dồn hay không.
* Có được merge hay chỉ chọn một bản ghi.

## 8.3. Các chiến lược resolve cấu hình

### Most specific wins

Cấu hình cụ thể nhất thắng.

Ví dụ:

* SLA theo dự án ghi đè SLA toàn công ty.

### Merge

Nhiều lớp cấu hình được hợp nhất.

Ví dụ:

* Enterprise bật email.
* Project bổ sung Zalo.
* Team bổ sung người nhận cảnh báo.

### Accumulate

Các rule được cộng dồn.

Ví dụ:

* Danh sách ngày nghỉ quốc gia.
* Ngày nghỉ pháp nhân.
* Ngày nghỉ chi nhánh.

### First matching rule

Chọn rule ưu tiên đầu tiên thỏa điều kiện.

Ví dụ:

* Approval matrix.

### Highest restriction wins

Quy tắc hạn chế cao hơn được ưu tiên.

Ví dụ:

* Chính sách bảo mật.
* Giới hạn export.
* Thời gian session.

---

# 9. Config Registry

## 9.1. Mục tiêu

Config Registry quản lý các loại cấu hình được phép tồn tại trong hệ thống.

Mỗi config key cần có:

* Mã cấu hình.
* Tên.
* Mô tả.
* Nhóm.
* Kiểu dữ liệu.
* Schema.
* Giá trị mặc định.
* Scope được phép.
* Cách resolve.
* Có yêu cầu duyệt không.
* Có chứa dữ liệu nhạy cảm không.
* Có yêu cầu version không.
* Có thể thay đổi khi đang active không.
* Module sử dụng.

## 9.2. Kiểu cấu hình

* Boolean.
* Integer.
* Decimal.
* String.
* Date.
* DateTime.
* Duration.
* Enum.
* List.
* Object.
* Formula.
* Expression.
* JSON có schema.
* Reference đến resource khác.

## 9.3. Validation

Mỗi cấu hình phải được validate trước khi lưu.

Ví dụ:

* Tỷ lệ từ 0 đến 100.
* Thời gian SLA phải lớn hơn 0.
* Ngày hiệu lực trước ngày hết hiệu lực.
* Tổng tỷ lệ phân bổ bằng 100%.
* Template phải có đủ biến bắt buộc.
* Workflow không có trạng thái cô lập.
* Approval matrix không có vòng lặp.

---

# 10. Vòng đời cấu hình

## 10.1. Trạng thái

* Draft.
* Pending Review.
* Pending Approval.
* Approved.
* Scheduled.
* Active.
* Suspended.
* Expired.
* Replaced.
* Cancelled.
* Archived.

## 10.2. Quy trình

1. Tạo bản nháp.
2. Nhập giá trị.
3. Validate.
4. Chạy mô phỏng nếu có.
5. Gửi kiểm tra.
6. Người kiểm tra nhận xét.
7. Gửi phê duyệt.
8. Phê duyệt hoặc từ chối.
9. Xác định ngày hiệu lực.
10. Kích hoạt.
11. Giám sát.
12. Thay thế bằng version mới khi cần.

## 10.3. Không sửa bản active trực tiếp

Khi cần thay đổi cấu hình active:

* Tạo version mới.
* So sánh trước/sau.
* Duyệt.
* Đặt ngày hiệu lực.
* Version cũ hết hiệu lực hoặc bị thay thế.

---

# 11. Mô phỏng tác động cấu hình

Các cấu hình quan trọng phải hỗ trợ preview hoặc simulation.

Ví dụ:

* Workflow mới.
* Pipeline mới.
* Approval matrix mới.
* Chính sách SLA mới.
* Quy tắc hoa hồng.
* Cấu hình đánh số.
* Rule Matching.
* Feature flag.

Mô phỏng cần hiển thị:

* Số bản ghi có thể bị ảnh hưởng.
* Đối tượng nào sẽ dùng cấu hình mới.
* Rule nào thắng.
* Xung đột.
* Cấu hình không được sử dụng.
* Cấu hình có vòng lặp.
* Ước lượng thay đổi SLA.
* Ước lượng thay đổi số người duyệt.

Mô phỏng không được tự kích hoạt cấu hình.

---

# 12. Danh mục nghiệp vụ dùng chung

## 12.1. System Enum

System Enum là mã kỹ thuật ổn định, không được tự ý thay đổi ý nghĩa.

Ví dụ:

* `ACTIVE`
* `CANCELLED`
* `DRAFT`
* `APPROVED`
* `BUY_SIDE`
* `SELL_SIDE`

Có thể thay đổi:

* Nhãn hiển thị.
* Mô tả.
* Thứ tự.
* Màu giao diện.

Không được thay đổi:

* Mã kỹ thuật.
* Ý nghĩa cốt lõi.
* Logic đã gắn với mã.

## 12.2. Business Dictionary

Business Dictionary là danh mục doanh nghiệp có thể cấu hình.

Ví dụ:

* Nguồn Lead.
* Lý do mất Deal.
* Loại cuộc gọi.
* Nhóm ngành nghề.
* Lý do hủy Booking.
* Loại tài liệu.
* Lý do gia hạn.
* Mức độ ưu tiên.
* Loại hình pháp lý tài sản.

## 12.3. Thông tin Dictionary Item

* Dictionary code.
* Item code.
* Tên.
* Tên viết tắt.
* Mô tả.
* Màu.
* Icon.
* Thứ tự.
* Parent item.
* Scope.
* Ngày hiệu lực.
* Trạng thái.
* Có phải mặc định không.
* Metadata.
* Người tạo.
* Người duyệt.

## 12.4. Không xóa item đã được sử dụng

Dictionary item đã được tham chiếu chỉ được:

* Ngừng sử dụng.
* Đặt hết hiệu lực.
* Thay thế.
* Ánh xạ sang item mới.

---

# 13. Danh mục mô hình kinh doanh chuẩn

Platform Configuration Capability phải quản lý các mã kỹ thuật chuẩn phục vụ toàn hệ thống.

## 13.1. Asset Origin

* `SELF_DEVELOPED`
* `THIRD_PARTY_PRIMARY`
* `CUSTOMER_OWNED_RESALE`
* `PARTNER_OWNED`
* `COMPANY_OWNED_RESALE`

## 13.2. Company Role

* `DEVELOPER`
* `CO_DEVELOPER`
* `LAND_OWNER`
* `ASSET_OWNER`
* `SELLER`
* `MASTER_AGENT`
* `DISTRIBUTOR`
* `BROKER`
* `CONSIGNMENT_AGENT`
* `MARKETING_AGENT`
* `PAYMENT_COLLECTOR`
* `PROPERTY_MANAGER`
* `SERVICE_PROVIDER`

## 13.3. Transaction Model

* `OWN_DEVELOPMENT_SALE`
* `THIRD_PARTY_PRIMARY_DISTRIBUTION`
* `SECONDARY_CONSIGNMENT_SALE`
* `COMPANY_OWNED_ASSET_SALE`
* `PARTNER_ASSET_SALE`
* `BROKERAGE_ONLY`
* `RENTAL_BROKERAGE`

## 13.4. Payment Flow Model

* `BUYER_TO_COMPANY`
* `BUYER_TO_DEVELOPER`
* `BUYER_TO_OWNER`
* `BUYER_TO_ESCROW`
* `BUYER_SPLIT_PAYMENT`
* `COMPANY_COLLECTS_ON_BEHALF`

## 13.5. Revenue Model

* `PROPERTY_SALES_REVENUE`
* `DISTRIBUTION_COMMISSION`
* `BROKERAGE_FEE`
* `SERVICE_FEE`
* `REFERRAL_FEE`
* `MARKETING_FEE`
* `MANAGEMENT_FEE`
* `OTHER_REVENUE`

## 13.6. Deal Side

* `BUY_SIDE`
* `SELL_SIDE`
* `DUAL_SIDE`
* `LISTING_ACQUISITION`

Các mã này là system enum.

Không được cho phép người dùng đổi ý nghĩa, nhưng có thể:

* Ẩn loại chưa sử dụng.
* Đổi nhãn tiếng Việt.
* Đặt mô tả.
* Cấu hình workflow tương ứng.

---

# 14. Đa ngôn ngữ và định dạng

## 14.1. Ngôn ngữ

Hệ thống phải hỗ trợ:

* Ngôn ngữ mặc định doanh nghiệp.
* Ngôn ngữ theo user.
* Nhãn dictionary đa ngôn ngữ.
* Template đa ngôn ngữ.
* Tài liệu đa ngôn ngữ.

MVP có thể ưu tiên tiếng Việt.

## 14.2. Múi giờ

Mỗi Enterprise có múi giờ mặc định.

Có thể override theo:

* Legal Entity.
* Branch.
* User.

Dữ liệu thời gian nên lưu ở dạng chuẩn thống nhất và hiển thị theo múi giờ người dùng.

## 14.3. Định dạng ngày

Hỗ trợ:

* `DD/MM/YYYY`
* `MM/DD/YYYY`
* `YYYY-MM-DD`

Định dạng hiển thị không làm thay đổi dữ liệu lưu trữ.

## 14.4. Định dạng số

Cấu hình:

* Dấu phân cách hàng nghìn.
* Dấu thập phân.
* Số chữ số thập phân.
* Cách hiển thị số âm.
* Cách hiển thị tỷ lệ.

## 14.5. Tiền tệ

Hỗ trợ:

* Tiền tệ mặc định.
* Tiền tệ theo Legal Entity.
* Tiền tệ theo giao dịch.
* Số chữ số thập phân.
* Quy tắc làm tròn.
* Tỷ giá khi mở rộng đa tiền tệ.

Mọi phép tính tiền phải dùng decimal.

---

# 15. Business Calendar

## 15.1. Mục tiêu

Business Calendar là căn cứ để tính:

* SLA.
* Thời hạn xử lý.
* Ngày làm việc.
* Ngày thanh toán.
* Ngày ký hợp đồng.
* Ngày escalation.
* Ngày thực hiện Task.

## 15.2. Thành phần

* Ngày làm việc trong tuần.
* Giờ bắt đầu.
* Giờ kết thúc.
* Giờ nghỉ.
* Ca làm việc.
* Ngày nghỉ quốc gia.
* Ngày nghỉ pháp nhân.
* Ngày nghỉ chi nhánh.
* Ngày làm bù.
* Lịch đặc biệt theo dự án.
* Múi giờ.

## 15.3. Chế độ tính thời gian

### Continuous time

Tính liên tục 24/7.

### Business time

Chỉ tính trong giờ làm việc.

### Calendar days

Tính theo ngày lịch.

### Business days

Tính theo ngày làm việc.

Mỗi SLA hoặc deadline phải xác định rõ chế độ tính.

## 15.4. Ngày nghỉ có hiệu lực theo phạm vi

Ví dụ:

* Ngày nghỉ toàn quốc.
* Ngày nghỉ toàn Enterprise.
* Ngày nghỉ của pháp nhân.
* Ngày nghỉ riêng chi nhánh.
* Ngày mở bán vẫn làm việc dù là cuối tuần.

## 15.5. Thay đổi lịch không được âm thầm sửa SLA cũ

SLA đã bắt đầu phải lưu calendar version hoặc snapshot cần thiết.

Khi thay đổi lịch:

* SLA mới dùng lịch mới.
* SLA cũ giữ cách tính cũ, trừ khi có migration được phê duyệt.

---

# 16. Kỳ tài chính và kỳ nghiệp vụ

Platform Configuration Capability quản lý metadata kỳ dùng chung:

* Kỳ tháng.
* Kỳ quý.
* Kỳ năm.
* Kỳ hoa hồng.
* Kỳ doanh số.
* Kỳ chiến dịch.
* Kỳ đối soát.
* Kỳ ngân sách.

Thông tin:

* Mã kỳ.
* Loại kỳ.
* Ngày bắt đầu.
* Ngày kết thúc.
* Ngày cut-off.
* Ngày khóa.
* Trạng thái.
* Legal Entity.
* Múi giờ.
* Người khóa.
* Lý do mở lại.

Module nghiệp vụ có thể tạo kỳ chuyên biệt, nhưng cần tham chiếu framework kỳ của Platform Configuration Capability.

---

# 17. Quy tắc đánh số

## 17.1. Các đối tượng cần đánh số

* Lead.
* Customer.
* Asset.
* Listing.
* Deal.
* Transaction Case.
* Booking.
* Contract.
* Receipt.
* Refund.
* Settlement.
* Revenue Entitlement.
* Commission Period.
* Clawback.
* Task.
* Approval Request.

## 17.2. Thành phần số

Có thể gồm:

* Prefix.
* Mã pháp nhân.
* Mã chi nhánh.
* Mã dự án.
* Năm.
* Tháng.
* Ngày.
* Loại giao dịch.
* Sequence.
* Check digit.
* Suffix.

Ví dụ:

```text
HD-ANZEN-2026-000123
```

## 17.3. Phạm vi sequence

Sequence có thể reset theo:

* Toàn hệ thống.
* Legal Entity.
* Dự án.
* Năm.
* Tháng.
* Loại chứng từ.

## 17.4. Quy tắc chống trùng

Numbering engine phải:

* Tạo số trong transaction.
* Không cấp cùng số hai lần.
* Không tái sử dụng số đã phát hành.
* Hỗ trợ gap nếu transaction rollback tùy policy.
* Ghi log việc cấp số.

## 17.5. Số nháp và số chính thức

Có thể có:

* Draft code.
* Official number.

Ví dụ hợp đồng nháp dùng mã nội bộ, khi phát hành mới có số pháp lý chính thức.

---

# 18. Workflow Definition và execution governance

> Platform Context sở hữu versioned Workflow Definitions. Owning business Context sở hữu aggregate state, command handling và transition execution. Generic workflow runtime không được direct-write aggregate của Context khác.


## 18.1. Mục tiêu

Workflow Engine cung cấp state machine dùng chung cho các owning business Context.

Ví dụ:

* Duyệt giảm giá.
* Thay sale.
* Booking.
* Hủy hợp đồng.
* Hoàn tiền.
* Điều chuyển tiền.
* Duyệt hoa hồng.
* Duyệt Listing.
* Duyệt ngoại lệ số điện thoại.
* Duyệt quyền phân phối.

## 18.2. Workflow Definition

Mỗi workflow gồm:

* Mã.
* Tên.
* Module.
* Resource type.
* Scope.
* Version.
* Trạng thái.
* Ngày hiệu lực.
* Các state.
* Các transition.
* Guard condition.
* Action.
* Approval requirement.
* SLA.
* Notification.
* Escalation.
* Error handling.

## 18.3. Workflow State

Thông tin:

* State code.
* Tên.
* Canonical state group.
* Thứ tự.
* Loại state.
* Có phải state đầu không.
* Có phải state cuối không.
* Có khóa chỉnh sửa không.
* Có cho hủy không.
* Trường bắt buộc.
* Quyền cần có.

## 18.4. Workflow Transition

Thông tin:

* From state.
* To state.
* Action code.
* Permission.
* Guard conditions.
* Required fields.
* Approval policy.
* Side effects.
* Notification policy.
* SLA policy.
* Có yêu cầu lý do không.
* Có yêu cầu tài liệu không.
* Có hỗ trợ rollback không.

## 18.5. Guard condition

Có thể kiểm tra:

* Trường dữ liệu.
* Trạng thái liên quan.
* Quyền user.
* Hạn mức.
* Giá trị giao dịch.
* Phê duyệt.
* Tiền đã xác nhận.
* Tài liệu đã đủ.
* Không có tranh chấp.
* Không có lock xung đột.

Guard condition phải được backend thực thi.

## 18.6. Side effect

Ví dụ:

* Tạo Task.
* Tạo Approval Request.
* Gửi thông báo.
* Ghi timeline.
* Khóa trường.
* Phát domain event.
* Tạo SLA.
* Cập nhật resource liên quan.

Side effect cần idempotent.

## 18.7. Workflow version

Resource đã chạy theo workflow version nào phải lưu version đó.

Workflow mới không tự chuyển resource cũ sang version mới.

---

# 19. Approval Policy và approval governance

> Platform Context sở hữu Approval Policy definitions. Exact approval runtime ownership và data model phải được khóa trong Platform Context Pack và Context Map.


## 19.1. Mục tiêu

Approval Engine quản lý các nghiệp vụ cần một hoặc nhiều cấp duyệt.

## 19.2. Approval Policy

Một policy gồm:

* Resource type.
* Action.
* Scope.
* Điều kiện.
* Hạn mức.
* Số cấp.
* Approver selector.
* Cơ chế duyệt tuần tự hoặc song song.
* Yêu cầu đồng thuận.
* SLA.
* Escalation.
* Điều kiện tự hủy.
* Ngày hiệu lực.
* Version.

## 19.3. Cách chọn người duyệt

* Manager trực tiếp.
* Team Lead.
* Department Head.
* Legal Entity Director.
* User có capability cụ thể.
* Nhóm approval.
* Người được ủy quyền.
* Người được chỉ định theo dự án.
* Người theo hạn mức.

## 19.4. Kiểu phê duyệt

### Sequential

Duyệt theo thứ tự.

### Parallel

Nhiều người duyệt đồng thời.

### Any one

Một trong số người được phép duyệt.

### All required

Tất cả phải duyệt.

### Quorum

Cần đủ số phiếu.

## 19.5. Phê duyệt theo hạn mức

Ví dụ:

* Dưới 50 triệu: Trưởng phòng.
* 50–200 triệu: Giám đốc kinh doanh.
* Trên 200 triệu: Giám đốc.
* Có ảnh hưởng tài chính: Tài chính tham gia.
* Có ảnh hưởng pháp lý: Pháp chế tham gia.

Các con số chỉ là cấu hình.

## 19.6. Ngăn tự duyệt

Policy có thể cấm:

* Người tạo tự duyệt.
* Người hưởng lợi tự duyệt.
* Người thực hiện thanh toán tự duyệt khoản chi.
* Người sửa tài khoản tự thực hiện chi.

## 19.7. Ủy quyền phê duyệt

Hỗ trợ:

* Thời gian ủy quyền.
* Phạm vi.
* Loại nghiệp vụ.
* Hạn mức.
* Người ủy quyền.
* Người nhận ủy quyền.
* Lý do.
* Audit.

Không cho phép ủy quyền vượt quá quyền gốc.

---

# 20. SLA Policy và time-governance definitions

> Platform định nghĩa policy và calendar references. Operational SLA instances thuộc `activity` hoặc owning Context theo accepted Context design.


## 20.1. Mục tiêu

SLA Engine quản lý thời gian xử lý và trách nhiệm theo từng nghiệp vụ.

## 20.2. SLA Policy

Thông tin:

* Tên.
* Mã.
* Resource type.
* Action hoặc stage.
* Scope.
* Priority.
* Duration.
* Time unit.
* Calculation mode.
* Business calendar.
* Start trigger.
* Pause rule.
* Resume rule.
* Completion trigger.
* Escalation.
* Warning threshold.
* Effective date.
* Version.

## 20.3. SLA động

SLA có thể theo:

* Loại Lead.
* Độ ưu tiên.
* Customer segment.
* Project.
* Transaction model.
* Giá trị giao dịch.
* Có tiền hay chưa.
* Có tranh chấp hay không.
* Team.
* Department.
* Legal Entity.

## 20.4. Thứ tự ưu tiên SLA

SLA cụ thể hơn được ưu tiên.

Ví dụ:

```text
Deal cụ thể
→ Dự án
→ Transaction Model
→ Phòng
→ Legal Entity
→ Enterprise default
```

## 20.5. Các mốc cảnh báo

Có thể cấu hình:

* 50% thời gian.
* 80%.
* Sắp đến hạn.
* Đến hạn.
* Quá hạn.
* Quá hạn nghiêm trọng.

## 20.6. Pause SLA

Chỉ được pause khi:

* Có lý do hợp lệ.
* Có người đề nghị.
* Có người duyệt nếu cần.
* Có thời gian bắt đầu.
* Có điều kiện resume.
* Có tổng thời gian pause.

Không được pause vô thời hạn không kiểm soát.

## 20.7. Gia hạn SLA

Cần lưu:

* SLA cũ.
* SLA mới.
* Thời gian gia hạn.
* Lý do.
* Người đề nghị.
* Người duyệt.
* Số lần gia hạn.
* Ngày hết hạn mới.

## 20.8. Quá SLA

Có thể:

* Nhắc người xử lý.
* Thông báo quản lý.
* Leo thang.
* Chuyển người xử lý.
* Yêu cầu giải trình.
* Đưa lên dashboard.

Không tự động:

* Phê duyệt.
* Hủy.
* Hoàn tiền.
* Mở bán lại.
* Chi hoa hồng.
* Xác nhận tiền.

---

# 21. Notification Policy và Template definitions

> Platform sở hữu policy/template definitions. Notification delivery attempts, provider responses và runtime failures thuộc runtime owner theo Context Map.


## 21.1. Kênh

* In-app.
* Email.
* SMS.
* Zalo.
* Push notification.
* Webhook.
* Chat integration.
* Kênh khác.

## 21.2. Notification Policy

Xác định:

* Sự kiện nào gửi.
* Người nhận.
* Kênh.
* Template.
* Mức độ ưu tiên.
* Thời gian gửi.
* Quiet hours.
* Retry.
* Escalation.
* Có gộp thông báo không.
* Có yêu cầu xác nhận đã đọc không.

## 21.3. Người nhận

Có thể là:

* Người phụ trách.
* Sale chính.
* Co-sale.
* Manager.
* Team Lead.
* Department Head.
* User có capability.
* Người tạo.
* Người duyệt.
* Customer.
* External Party.

## 21.4. Chống gửi trùng

Notification engine phải hỗ trợ:

* Deduplication key.
* Event ID.
* Template version.
* Recipient.
* Time window.

## 21.5. Retry

Mỗi kênh có:

* Số lần retry.
* Khoảng chờ.
* Backoff.
* Trạng thái thất bại.
* Dead-letter queue.
* Người xử lý.

## 21.6. Quiet hours

Có thể cấu hình thời gian không gửi cho:

* User nội bộ.
* Customer.
* Từng kênh.
* Từng mức độ ưu tiên.

Thông báo khẩn cấp có thể bypass nếu policy cho phép.

---

# 22. Template Engine

## 22.1. Loại template

* Email.
* SMS.
* Zalo.
* In-app.
* PDF.
* Báo giá.
* Proposal.
* Booking form.
* Contract summary.
* Payment notice.
* Receipt notice.
* Commission statement.
* Approval request.
* Handover checklist.

## 22.2. Template variable

Ví dụ:

* Customer name.
* Deal code.
* Project name.
* Unit code.
* Due date.
* Amount.
* Sale name.
* Approval link.
* Legal Entity.
* Contract number.

## 22.3. Validation biến

Template chỉ được kích hoạt nếu:

* Tất cả biến bắt buộc hợp lệ.
* Không sử dụng biến ngoài quyền.
* Không lộ dữ liệu nhạy cảm.
* Không tham chiếu biến không tồn tại.

## 22.4. Phiên bản template

Template active không sửa trực tiếp.

Tạo version mới và đặt ngày hiệu lực.

Tài liệu đã phát hành phải lưu:

* Template ID.
* Template version.
* Rendered snapshot.
* Dữ liệu nguồn cần thiết.

---

# 23. Feature Flag

## 23.1. Mục tiêu

Feature flag cho phép:

* Phát hành tính năng theo giai đoạn.
* Thử nghiệm giới hạn.
* Rollback nhanh.
* Bật theo pháp nhân hoặc dự án.
* Bật theo nhóm user.
* Chuyển đổi giữa workflow cũ và mới.

## 23.2. Scope

* Toàn Enterprise.
* Legal Entity.
* Branch.
* Department.
* Team.
* Project.
* User group.
* User cụ thể.

## 23.3. Trạng thái

* Disabled.
* Enabled.
* Pilot.
* Percentage rollout.
* Scheduled.
* Expired.

## 23.4. Không dùng feature flag để phá system invariant

Không cho phép feature flag tắt:

* Audit.
* Permission backend.
* Chống phân bổ vượt tiền.
* Chống Booking trùng.
* Chống sửa phiếu thu đã phát hành.

## 23.5. Audit

Mọi thay đổi feature flag phải ghi:

* Người thay đổi.
* Phạm vi.
* Giá trị cũ.
* Giá trị mới.
* Lý do.
* Thời gian.
* Người duyệt nếu cần.

---

# 24. Integration profile definitions

> Platform chỉ sở hữu control-plane definitions và secret references. Integration Context sở hữu connections, mappings, webhook/sync executions, retries và reconciliation runtime.


## 24.1. Loại tích hợp

* Email provider.
* SMS provider.
* Zalo.
* Facebook.
* Google Ads.
* Google Tag Manager.
* Ngân hàng.
* Phần mềm kế toán.
* Hóa đơn điện tử.
* Google Drive.
* OneDrive.
* MinIO.
* Chữ ký điện tử.
* Chủ đầu tư.
* Cổng thanh toán.
* Website.
* Landing page.
* Call center.
* BI.
* Data warehouse.

## 24.2. Integration Profile

Thông tin:

* Tên.
* Loại.
* Provider.
* Environment.
* Legal Entity.
* Scope.
* Endpoint.
* Authentication type.
* Credential reference.
* Timeout.
* Retry.
* Rate limit.
* Webhook secret.
* Trạng thái.
* Ngày hiệu lực.
* Người quản lý.

## 24.3. Môi trường

* Development.
* Staging.
* Production.
* Sandbox đối tác.

Credential giữa các môi trường phải tách biệt.

Không dùng credential Production cho Development.

## 24.4. Mapping

Có thể cấu hình:

* Field mapping.
* Status mapping.
* Project mapping.
* Unit mapping.
* Customer mapping.
* Currency mapping.
* Error mapping.

Mapping phải có version và audit.

---

# 25. Quản lý bí mật và credential

## 25.1. Nguyên tắc

Credential không được lưu dưới dạng plaintext trong bảng cấu hình thông thường.

Phải sử dụng:

* Secret manager.
* Encrypted storage.
* Environment secret.
* Key management system.

## 25.2. Dữ liệu nhạy cảm

* API key.
* OAuth token.
* Client secret.
* Database password.
* Webhook signing secret.
* Bank integration key.
* Encryption key.
* Private key chữ ký.

## 25.3. Quyền xem

Người dùng thông thường không được xem giá trị secret.

CRM Admin có thể:

* Chọn secret.
* Kiểm tra trạng thái.
* Rotate.
* Test connection.

Không nhất thiết được xem plaintext.

## 25.4. Rotation

Hỗ trợ:

* Ngày tạo.
* Ngày hết hạn.
* Ngày rotate.
* Secret cũ.
* Secret mới.
* Grace period.
* Kiểm tra tích hợp sau rotate.

---

# 26. Event integration principles và candidate business facts

> Event infrastructure không thuộc quyền sở hữu nghiệp vụ của Platform. Exact Event inventory, envelope, payload và channels thuộc JSON Schema, AsyncAPI và Event Registry.


## 26.1. Mục tiêu

Các module giao tiếp qua domain event để giảm phụ thuộc trực tiếp.

Ví dụ:

* `lead.assigned`
* `customer.merged`
* `listing.activated`
* `booking.confirmed`
* `contract.signed`
* `contract.cancelled`
* `revenue.recognized`
* `commission.paid`

## 26.2. Nội dung event

* Event ID.
* Event type.
* Version.
* Source module.
* Resource type.
* Resource ID.
* Occurred at.
* Actor.
* Correlation ID.
* Causation ID.
* Payload.
* Idempotency key.

## 26.3. Event version

Khi payload thay đổi:

* Tạo version mới.
* Không âm thầm phá consumer cũ.
* Có migration hoặc compatibility layer.

## 26.4. Transactional Outbox

Các event quan trọng nên dùng outbox:

1. Transaction nghiệp vụ thành công.
2. Event ghi cùng transaction.
3. Worker phát event.
4. Consumer xử lý idempotent.

Tránh trường hợp:

* Database đã cập nhật.
* Nhưng event không được gửi.

---

# 27. Webhook Framework

## 27.1. Inbound webhook

Dùng cho:

* Lead từ website.
* Lead quảng cáo.
* Bank transaction.
* Chủ đầu tư cập nhật kho.
* Chữ ký điện tử.
* Payment gateway.

## 27.2. Outbound webhook

Dùng để gửi:

* Customer created.
* Deal changed.
* Booking confirmed.
* Contract signed.
* Payment received.
* Revenue recognized.

## 27.3. Bảo mật

* Signature.
* Timestamp.
* Replay protection.
* IP allowlist nếu cần.
* Rate limit.
* Secret rotation.
* Payload size limit.

## 27.4. Retry và dead-letter

Webhook thất bại phải:

* Retry.
* Ghi log.
* Có dead-letter.
* Cho phép replay có kiểm soát.
* Giữ idempotency.

---

# 28. Job Schedule definitions và execution governance

> Platform sở hữu schedule/policy definitions; Operations sở hữu job, queue, attempt và incident runtime.


## 28.1. Loại job

* SLA evaluation.
* Notification.
* Matching batch.
* Inventory sync.
* Price expiration.
* Listing expiration.
* Contract reminder.
* Receivable aging.
* Commission calculation.
* Clawback processing.
* Data cleanup.
* Export generation.
* Integration retry.

## 28.2. Cấu hình job

* Mã job.
* Lịch chạy.
* Múi giờ.
* Scope.
* Timeout.
* Retry.
* Concurrency.
* Lock.
* Priority.
* Feature flag.
* Trạng thái.
* Người quản lý.

## 28.3. Chống chạy trùng

Job phải hỗ trợ:

* Distributed lock.
* Run ID.
* Idempotency.
* Last successful run.
* Retry count.
* Checkpoint.

## 28.4. Job nguy hiểm

Các job có khả năng thay đổi tiền hoặc trạng thái lớn phải có:

* Preview.
* Approval.
* Dry run.
* Giới hạn batch.
* Reconciliation.
* Rollback plan hoặc compensating action.

---

# 29. Import policy và orchestration requirements

> Import phải đi qua canonical commands của owning Context; Platform definition không được bypass Domain rules.


## 29.1. Dữ liệu có thể import

* Customer.
* Lead.
* Partner.
* Project.
* Asset.
* Listing.
* Price list.
* Payment data.
* Revenue reconciliation.
* Commission input.

## 29.2. Quy trình import

1. Upload hoặc chọn nguồn.
2. Xác định loại dữ liệu.
3. Mapping field.
4. Validate.
5. Preview.
6. Duplicate check.
7. Permission check.
8. Dry run.
9. Phê duyệt nếu cần.
10. Import.
11. Reconciliation.
12. Error report.

## 29.3. Không import bỏ qua backend rule

Import vẫn phải kiểm tra:

* Duplicate Customer.
* Scope.
* Quyền.
* Status.
* Unique constraint.
* Data type.
* Referential integrity.

## 29.4. Import job

Lưu:

* Người thực hiện.
* File hash.
* Mapping version.
* Số dòng.
* Thành công.
* Lỗi.
* Bỏ qua.
* Cập nhật.
* Thời gian.
* Audit.

---

# 30. Export policy và control requirements

> Export capability và runtime phải enforce permission, masking và ownership của dữ liệu nguồn; Platform chỉ cung cấp policy/control definitions dùng chung.


## 30.1. Mục tiêu

Export framework cung cấp cơ chế kỹ thuật dùng chung, nhưng quyền export do từng module quy định.

## 30.2. Trạng thái yêu cầu export

* Requested.
* Pending Approval.
* Approved.
* Generating.
* Ready.
* Downloaded.
* Expired.
* Rejected.
* Failed.
* Cancelled.

## 30.3. Metadata

* User yêu cầu.
* Module.
* Resource.
* Scope.
* Filter.
* Fields.
* Format.
* Số bản ghi.
* Mục đích.
* Người nhận.
* Người duyệt.
* File hash.
* Ngày hết hạn.
* Số lần tải.
* IP.
* Thiết bị.

## 30.4. Watermark

Có thể cấu hình:

* Tên người tải.
* Email.
* Ngày.
* Mã export.
* Legal Entity.
* Mục đích.

## 30.5. Giới hạn

* Giới hạn số dòng.
* Giới hạn cột nhạy cảm.
* Giới hạn định dạng.
* Giới hạn theo vai trò.
* Tự động hết hạn.
* Chặn chia sẻ ngoài nếu có tích hợp.

---

# 31. Security-policy references

> Exact authentication, authorization, session, MFA, scope và masking controls thuộc Security Architecture và security registries. Platform Configuration chỉ quản trị approved policy references/values.


Platform Configuration Capability quản lý baseline bảo mật; Module 2.1 quản lý user và permission cụ thể.

## 31.1. Password policy

Có thể cấu hình:

* Độ dài tối thiểu.
* Độ phức tạp.
* Thời gian hết hạn.
* Lịch sử mật khẩu.
* Lockout.
* Số lần đăng nhập sai.

## 31.2. Session policy

* Thời gian session.
* Idle timeout.
* Concurrent sessions.
* Re-authentication cho thao tác nhạy cảm.
* Device trust.
* Remember device.

## 31.3. MFA

Có thể yêu cầu theo:

* Vai trò.
* Capability.
* Legal Entity.
* Thao tác tài chính.
* Export.
* Thay đổi tài khoản nhận tiền.
* Thay đổi integration secret.

## 31.4. IP policy

* Allowlist.
* Blocklist.
* Hạn chế thao tác tài chính theo mạng.
* Cảnh báo đăng nhập bất thường.

## 31.5. Data masking policy

Có thể cấu hình cách che:

* Số điện thoại.
* Email.
* CCCD.
* Tài khoản ngân hàng.
* Mã số thuế.
* Địa chỉ.
* Thu nhập.

Backend phải loại bỏ hoặc mask theo quyền.

---

# 32. Retention-policy definitions

> Owning data Context chịu trách nhiệm thực thi retention theo policy. Documents và Audit có các ràng buộc riêng; Legal Hold luôn chặn destructive actions khi policy yêu cầu.


## 32.1. Retention Policy

Cấu hình theo:

* Resource type.
* Legal Entity.
* Trạng thái.
* Thời gian.
* Yêu cầu pháp lý.
* Tranh chấp.
* Audit.

## 32.2. Các hành động

* Giữ active.
* Archive.
* Anonymize.
* Delete mềm.
* Delete cứng theo quy trình đặc biệt.
* Legal hold.

## 32.3. Legal Hold

Khi dữ liệu liên quan:

* Tranh chấp.
* Điều tra.
* Kiểm toán.
* Nghĩa vụ pháp lý.

thì không được xóa hoặc anonymize cho đến khi hold được giải phóng.

## 32.4. Không xóa dữ liệu tài chính tùy ý

Các dữ liệu sau mặc định không xóa cứng:

* Hợp đồng.
* Phiếu thu.
* Allocation.
* Settlement.
* Revenue.
* Commission.
* Clawback.
* Audit log.

---

# 33. Soft Delete và Archive

## 33.1. Soft delete

Dùng cho dữ liệu có thể được ẩn khỏi hoạt động nhưng vẫn cần truy xuất.

Trường:

* `deleted_at`
* `deleted_by`
* `deletion_reason`

## 33.2. Archive

Archive khác delete.

Dữ liệu archive:

* Không còn hoạt động.
* Không xuất hiện mặc định.
* Vẫn có thể báo cáo và truy xuất.
* Không cho tạo nghiệp vụ mới nếu không mở lại.

## 33.3. Restore

Restore cần:

* Quyền.
* Lý do.
* Kiểm tra xung đột.
* Audit.

Không restore dữ liệu nếu làm vi phạm unique constraint hoặc trạng thái nghiệp vụ.

---

# 34. Data Quality Framework

## 34.1. Mục tiêu

Phát hiện:

* Thiếu trường.
* Dữ liệu không hợp lệ.
* Dữ liệu cũ.
* Mapping thiếu.
* Config không được sử dụng.
* Tài liệu hết hạn.
* Integration sync lỗi.

## 34.2. Data Quality Rule

* Resource type.
* Field.
* Điều kiện.
* Severity.
* Scope.
* Auto-fix policy.
* Người xử lý.
* SLA.
* Version.

## 34.3. Severity

* Info.
* Warning.
* Error.
* Critical.

## 34.4. Không auto-fix dữ liệu nhạy cảm

Không tự sửa:

* Customer identity.
* Giá.
* Contract amount.
* Receipt amount.
* Co-sale.
* Commission.
* Ownership.

Nếu chưa có phê duyệt.

---

# 35. Error Handling Framework

## 35.1. Error code chuẩn

Mỗi lỗi cần có:

* Mã lỗi.
* HTTP status.
* Message cho user.
* Message kỹ thuật.
* Correlation ID.
* Retryable hay không.
* Module.
* Severity.

Ví dụ:

* `CONFIG_NOT_FOUND`
* `CONFIG_CONFLICT`
* `WORKFLOW_TRANSITION_NOT_ALLOWED`
* `APPROVAL_REQUIRED`
* `SLA_POLICY_NOT_FOUND`
* `IDEMPOTENCY_CONFLICT`
* `INTEGRATION_TIMEOUT`

## 35.2. Không trả lỗi kỹ thuật nhạy cảm cho frontend

Không hiển thị:

* Stack trace.
* Database query.
* Secret.
* Internal path.
* Token.

## 35.3. Correlation ID

Mỗi request và job phải có correlation ID để truy vết xuyên module.

---

# 36. Idempotency Framework

## 36.1. Các thao tác bắt buộc

* Tạo Booking.
* Tạo Receipt.
* Phân bổ tiền.
* Hoàn tiền.
* Settlement.
* Revenue recognition.
* Commission recognition.
* Payout.
* Webhook inbound.
* Event consumer.

## 36.2. Idempotency record

* Key.
* Resource type.
* User hoặc integration.
* Request hash.
* Response snapshot.
* Status.
* Created at.
* Expires at.

## 36.3. Request khác dữ liệu cùng key

Nếu cùng idempotency key nhưng payload khác:

* Từ chối.
* Trả lỗi xung đột.
* Ghi audit.

---

# 37. Audit cấu hình

## 37.1. Thao tác bắt buộc ghi audit

* Tạo Enterprise.
* Tạo Legal Entity.
* Thay đổi vai trò pháp nhân.
* Tạo config.
* Sửa config draft.
* Submit review.
* Approve.
* Activate.
* Suspend.
* Replace.
* Thay đổi dictionary.
* Thay đổi workflow.
* Thay đổi approval policy.
* Thay đổi SLA.
* Thay đổi feature flag.
* Thay đổi integration.
* Rotate secret.
* Thay đổi retention.
* Mở lại kỳ.
* Import/export.

## 37.2. Nội dung audit

* Actor.
* Vai trò.
* Resource.
* Version.
* Before.
* After.
* Lý do.
* Người duyệt.
* IP.
* Device.
* Request ID.
* Correlation ID.
* Thời gian.
* Kết quả.

## 37.3. Audit cấu hình không được sửa

Chỉ được:

* Xem.
* Xuất theo quyền.
* Lưu trữ.

Không được update hoặc delete bởi user thông thường.

---

# 38. Các màn hình chính

## 38.1. System Overview

Hiển thị:

* Phiên bản hệ thống.
* Trạng thái module.
* Cấu hình chưa hoàn tất.
* Tích hợp lỗi.
* Job lỗi.
* Feature flag đang bật.
* Cấu hình sắp hết hiệu lực.
* SLA policy không được sử dụng.
* Secret sắp hết hạn.

## 38.2. Enterprise Settings

* Thông tin doanh nghiệp.
* Ngôn ngữ.
* Múi giờ.
* Tiền tệ.
* Định dạng.
* Logo.
* Liên hệ.
* Chính sách chung.

## 38.3. Legal Entity Center

* Danh sách pháp nhân.
* Vai trò.
* Trạng thái.
* Người đại diện.
* Tài khoản.
* Tài liệu.
* Cấu hình riêng.
* Lịch sử.

## 38.4. Configuration Registry

* Config key.
* Nhóm.
* Kiểu dữ liệu.
* Scope.
* Giá trị mặc định.
* Module sử dụng.
* Version.
* Trạng thái.

## 38.5. Configuration Workspace

* Scope.
* Giá trị.
* Schema.
* Preview.
* Diff.
* Simulation.
* Approval.
* Effective date.
* History.

## 38.6. Dictionary Management

* Danh mục.
* Item.
* Hierarchy.
* Scope.
* Thứ tự.
* Nhãn.
* Trạng thái.
* Import.

## 38.7. Workflow Designer

* State.
* Transition.
* Guard.
* Action.
* Approval.
* SLA.
* Notification.
* Simulation.
* Version.

## 38.8. Approval Matrix Center

* Nghiệp vụ.
* Hạn mức.
* Người duyệt.
* Thứ tự.
* Điều kiện.
* Scope.
* Delegation.
* Audit.

## 38.9. SLA Center

* Policy.
* Scope.
* Duration.
* Calendar.
* Warning.
* Escalation.
* Pause.
* Extension.
* Version.

## 38.10. Notification Center

* Kênh.
* Template.
* Routing.
* Retry.
* Lịch sử gửi.
* Lỗi.
* Dead-letter.

## 38.11. Integration Center

* Provider.
* Environment.
* Credential.
* Mapping.
* Webhook.
* Sync log.
* Test connection.
* Error.

## 38.12. Job Monitor

* Job.
* Lịch.
* Trạng thái.
* Lần chạy gần nhất.
* Duration.
* Retry.
* Error.
* Replay.

## 38.13. Feature Flag Center

* Flag.
* Phạm vi.
* Rollout.
* Người tạo.
* Người duyệt.
* Lịch sử.

---

# 39. Dashboard quản trị Platform Configuration Capability

Dashboard dành cho CRM Admin và Giám đốc có quyền:

* Số cấu hình active.
* Cấu hình chờ duyệt.
* Cấu hình sắp hết hiệu lực.
* Workflow lỗi.
* Approval policy không tìm thấy approver.
* SLA không có calendar.
* Notification thất bại.
* Integration lỗi.
* Secret sắp hết hạn.
* Job quá SLA.
* Feature flag pilot.
* Export chờ duyệt.
* Import lỗi.
* Cảnh báo bảo mật.
* Thay đổi cấu hình gần đây.

---

# 40. Candidate data model — đầu vào thiết kế, không phải physical schema canonical

> **Classification:** `CONTEXT-SPECIFIC DESIGN INPUT / PENDING VALIDATION`  
> Exact tables, columns, constraints và indexes chỉ có hiệu lực khi được khóa trong Platform Context DB Specification và Alembic migrations.


## 40.1. Enterprise

### `enterprises`

* `id`
* `enterprise_code`
* `legal_name`
* `trade_name`
* `logo_url`
* `website`
* `email`
* `phone`
* `country_code`
* `default_timezone`
* `default_locale`
* `default_currency`
* `date_format`
* `number_format`
* `status`
* `created_at`
* `updated_at`

---

## 40.2. Legal Entity

### `legal_entities`

* `id`
* `enterprise_id`
* `legal_entity_code`
* `legal_name`
* `short_name`
* `tax_code`
* `registration_number`
* `entity_type`
* `country_code`
* `registered_address`
* `representative_name`
* `representative_title`
* `accounting_currency`
* `timezone`
* `status`
* `effective_from`
* `effective_to`
* `created_at`
* `updated_at`

### `legal_entity_roles`

* `id`
* `legal_entity_id`
* `role_code`
* `effective_from`
* `effective_to`
* `status`
* `created_at`

### `legal_entity_documents`

* `id`
* `legal_entity_id`
* `document_type`
* `title`
* `url`
* `verification_status`
* `expires_at`
* `created_by`
* `created_at`

---

## 40.3. Config Registry

### `configuration_definitions`

* `id`
* `config_key`
* `name`
* `description`
* `config_group`
* `data_type`
* `schema_json`
* `default_value_json`
* `allowed_scope_types`
* `resolution_strategy`
* `requires_versioning`
* `requires_approval`
* `is_sensitive`
* `module_code`
* `status`
* `created_at`

### `configuration_values`

* `id`
* `configuration_definition_id`
* `scope_type`
* `scope_id`
* `version`
* `value_json`
* `status`
* `effective_from`
* `effective_to`
* `replaces_configuration_value_id`
* `created_by`
* `reviewed_by`
* `approved_by`
* `activated_by`
* `reason`
* `created_at`
* `updated_at`

### `configuration_resolution_logs`

* `id`
* `config_key`
* `resource_type`
* `resource_id`
* `resolved_configuration_value_id`
* `scope_path_json`
* `resolution_details`
* `created_at`

---

## 40.4. Dictionary

### `business_dictionaries`

* `id`
* `dictionary_code`
* `name`
* `description`
* `module_code`
* `is_system_dictionary`
* `status`
* `created_at`

### `business_dictionary_items`

* `id`
* `dictionary_id`
* `item_code`
* `parent_item_id`
* `scope_type`
* `scope_id`
* `display_order`
* `color`
* `icon`
* `metadata_json`
* `status`
* `effective_from`
* `effective_to`
* `created_by`
* `approved_by`
* `created_at`

### `business_dictionary_item_translations`

* `id`
* `dictionary_item_id`
* `locale`
* `name`
* `short_name`
* `description`

---

## 40.5. Business Calendar

### `business_calendars`

* `id`
* `calendar_code`
* `name`
* `scope_type`
* `scope_id`
* `timezone`
* `version`
* `status`
* `effective_from`
* `effective_to`
* `created_by`
* `approved_by`
* `created_at`

### `business_calendar_working_hours`

* `id`
* `business_calendar_id`
* `day_of_week`
* `start_time`
* `end_time`
* `breaks_json`
* `is_working_day`

### `business_calendar_exceptions`

* `id`
* `business_calendar_id`
* `exception_date`
* `exception_type`
* `start_time`
* `end_time`
* `description`
* `created_at`

---

## 40.6. Numbering

### `numbering_schemes`

* `id`
* `scheme_code`
* `resource_type`
* `scope_type`
* `scope_id`
* `format_pattern`
* `reset_policy`
* `sequence_length`
* `timezone`
* `version`
* `status`
* `effective_from`
* `effective_to`
* `created_by`
* `approved_by`
* `created_at`

### `numbering_sequences`

* `id`
* `numbering_scheme_id`
* `sequence_scope_key`
* `current_value`
* `last_issued_at`
* `version`

### `issued_numbers`

* `id`
* `numbering_scheme_id`
* `resource_type`
* `resource_id`
* `issued_number`
* `sequence_value`
* `issued_at`
* `issued_by`

---

## 40.7. Workflow

### `workflow_definitions`

* `id`
* `workflow_code`
* `name`
* `module_code`
* `resource_type`
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

### `workflow_states`

* `id`
* `workflow_definition_id`
* `state_code`
* `name`
* `canonical_group`
* `state_type`
* `display_order`
* `is_initial`
* `is_terminal`
* `locks_resource`
* `required_fields_json`
* `metadata_json`

### `workflow_transitions`

* `id`
* `workflow_definition_id`
* `from_state_id`
* `to_state_id`
* `action_code`
* `permission_code`
* `guard_expression`
* `required_fields_json`
* `approval_policy_id`
* `sla_policy_id`
* `notification_policy_id`
* `requires_reason`
* `side_effects_json`

### `workflow_instances`

* `id`
* `workflow_definition_id`
* `workflow_version`
* `resource_type`
* `resource_id`
* `current_state_id`
* `status`
* `started_at`
* `completed_at`

### `workflow_transition_history`

* `id`
* `workflow_instance_id`
* `from_state_id`
* `to_state_id`
* `action_code`
* `actor_user_id`
* `reason`
* `approval_request_id`
* `occurred_at`

---

## 40.8. Approval

### `approval_policies`

* `id`
* `policy_code`
* `name`
* `resource_type`
* `action_code`
* `scope_type`
* `scope_id`
* `version`
* `conditions_json`
* `approval_mode`
* `self_approval_policy`
* `status`
* `effective_from`
* `effective_to`
* `created_by`
* `approved_by`
* `created_at`

### `approval_policy_steps`

* `id`
* `approval_policy_id`
* `step_no`
* `approver_selector_type`
* `approver_selector_config`
* `approval_mode`
* `minimum_approvals`
* `sla_policy_id`
* `conditions_json`

### `approval_requests`

* `id`
* `approval_policy_id`
* `policy_version`
* `resource_type`
* `resource_id`
* `action_code`
* `requested_by`
* `status`
* `requested_at`
* `completed_at`

### `approval_request_steps`

* `id`
* `approval_request_id`
* `step_no`
* `approver_user_id`
* `status`
* `decision`
* `comment`
* `decided_at`

---

## 40.9. SLA

### `sla_policies`

* `id`
* `sla_code`
* `name`
* `resource_type`
* `action_or_stage_code`
* `scope_type`
* `scope_id`
* `priority`
* `duration_value`
* `duration_unit`
* `calculation_mode`
* `business_calendar_id`
* `start_trigger`
* `completion_trigger`
* `warning_thresholds_json`
* `pause_policy_json`
* `escalation_policy_json`
* `version`
* `status`
* `effective_from`
* `effective_to`
* `created_by`
* `approved_by`
* `created_at`

### `sla_instances`

* `id`
* `sla_policy_id`
* `policy_version`
* `resource_type`
* `resource_id`
* `assigned_user_id`
* `started_at`
* `due_at`
* `status`
* `paused_duration_seconds`
* `completed_at`
* `breached_at`

### `sla_pause_events`

* `id`
* `sla_instance_id`
* `reason_code`
* `reason`
* `started_at`
* `resumed_at`
* `requested_by`
* `approved_by`

### `sla_extension_requests`

* `id`
* `sla_instance_id`
* `old_due_at`
* `requested_due_at`
* `approved_due_at`
* `reason`
* `status`
* `requested_by`
* `approved_by`
* `created_at`

---

## 40.10. Notification

### `notification_templates`

* `id`
* `template_code`
* `name`
* `channel`
* `locale`
* `subject_template`
* `body_template`
* `variable_schema`
* `version`
* `status`
* `effective_from`
* `effective_to`
* `created_by`
* `approved_by`
* `created_at`

### `notification_policies`

* `id`
* `policy_code`
* `event_type`
* `scope_type`
* `scope_id`
* `recipient_rules_json`
* `channel_rules_json`
* `template_id`
* `priority`
* `quiet_hours_policy`
* `retry_policy`
* `version`
* `status`
* `created_at`

### `notification_messages`

* `id`
* `event_id`
* `recipient_type`
* `recipient_id`
* `channel`
* `template_id`
* `template_version`
* `deduplication_key`
* `status`
* `scheduled_at`
* `sent_at`
* `failure_reason`
* `retry_count`
* `created_at`

---

## 40.11. Feature Flag

### `feature_flags`

* `id`
* `flag_code`
* `name`
* `description`
* `default_value`
* `status`
* `created_at`

### `feature_flag_rules`

* `id`
* `feature_flag_id`
* `scope_type`
* `scope_id`
* `value`
* `rollout_percentage`
* `effective_from`
* `effective_to`
* `reason`
* `created_by`
* `approved_by`
* `created_at`

---

## 40.12. Integration

### `integration_profiles`

* `id`
* `integration_code`
* `name`
* `integration_type`
* `provider`
* `environment`
* `scope_type`
* `scope_id`
* `endpoint`
* `authentication_type`
* `secret_reference`
* `timeout_seconds`
* `retry_policy_json`
* `rate_limit_policy_json`
* `status`
* `effective_from`
* `effective_to`
* `created_by`
* `approved_by`
* `created_at`

### `integration_mappings`

* `id`
* `integration_profile_id`
* `mapping_type`
* `source_key`
* `target_key`
* `transformation_rule`
* `version`
* `status`
* `created_at`

### `integration_execution_logs`

* `id`
* `integration_profile_id`
* `operation`
* `correlation_id`
* `request_metadata`
* `response_metadata`
* `status`
* `duration_ms`
* `error_code`
* `created_at`

---

## 40.13. Webhook

### `webhook_subscriptions`

* `id`
* `subscription_code`
* `direction`
* `event_type`
* `integration_profile_id`
* `endpoint`
* `secret_reference`
* `status`
* `created_at`

### `webhook_deliveries`

* `id`
* `webhook_subscription_id`
* `event_id`
* `payload_hash`
* `attempt_no`
* `status`
* `response_code`
* `failure_reason`
* `next_retry_at`
* `created_at`

---

## 40.14. Jobs

### `scheduled_jobs`

* `id`
* `job_code`
* `name`
* `job_type`
* `schedule_expression`
* `timezone`
* `scope_type`
* `scope_id`
* `timeout_seconds`
* `retry_policy_json`
* `concurrency_policy`
* `status`
* `created_at`

### `job_runs`

* `id`
* `scheduled_job_id`
* `run_id`
* `started_at`
* `completed_at`
* `status`
* `processed_count`
* `success_count`
* `failure_count`
* `checkpoint_json`
* `error_summary`

---

## 40.15. Import/Export

### `import_jobs`

* `id`
* `resource_type`
* `source_type`
* `file_reference`
* `file_hash`
* `mapping_version`
* `status`
* `total_rows`
* `success_rows`
* `error_rows`
* `created_by`
* `approved_by`
* `created_at`
* `completed_at`

### `export_requests`

* `id`
* `module_code`
* `resource_type`
* `scope_snapshot`
* `filter_snapshot`
* `field_snapshot`
* `format`
* `purpose`
* `status`
* `record_count`
* `file_reference`
* `file_hash`
* `expires_at`
* `requested_by`
* `approved_by`
* `created_at`

### `export_download_logs`

* `id`
* `export_request_id`
* `downloaded_by`
* `ip_address`
* `user_agent`
* `downloaded_at`

---

# 41. Candidate application operations — không phải OpenAPI canonical

> Các operation dưới đây là capability inventory. Exact paths, methods, payloads, errors và authorization metadata thuộc OpenAPI.


## Enterprise và Legal Entity

```text
GET    /system/enterprise
PATCH  /system/enterprise

GET    /legal-entities
POST   /legal-entities
GET    /legal-entities/{id}
PATCH  /legal-entities/{id}
POST   /legal-entities/{id}/activate
POST   /legal-entities/{id}/deactivate
GET    /legal-entities/{id}/roles
POST   /legal-entities/{id}/roles
```

## Config Registry

```text
GET    /configuration-definitions
POST   /configuration-definitions
GET    /configuration-definitions/{id}
PATCH  /configuration-definitions/{id}

GET    /configurations
POST   /configurations
GET    /configurations/{id}
PATCH  /configurations/{id}
POST   /configurations/{id}/validate
POST   /configurations/{id}/simulate
POST   /configurations/{id}/submit-review
POST   /configurations/{id}/approve
POST   /configurations/{id}/schedule
POST   /configurations/{id}/activate
POST   /configurations/{id}/suspend
POST   /configurations/{id}/create-version
GET    /configurations/resolve
```

## Dictionary

```text
GET    /dictionaries
POST   /dictionaries
GET    /dictionaries/{id}
POST   /dictionaries/{id}/items
PATCH  /dictionary-items/{id}
POST   /dictionary-items/{id}/activate
POST   /dictionary-items/{id}/deactivate
POST   /dictionary-items/{id}/replace
```

## Business Calendar

```text
GET    /business-calendars
POST   /business-calendars
GET    /business-calendars/{id}
PATCH  /business-calendars/{id}
POST   /business-calendars/{id}/create-version
POST   /business-calendars/{id}/activate
POST   /business-calendars/{id}/calculate-deadline
```

## Numbering

```text
GET    /numbering-schemes
POST   /numbering-schemes
GET    /numbering-schemes/{id}
PATCH  /numbering-schemes/{id}
POST   /numbering-schemes/{id}/preview
POST   /numbering-schemes/{id}/activate
POST   /numbering/issue
```

## Workflow

```text
GET    /workflow-definitions
POST   /workflow-definitions
GET    /workflow-definitions/{id}
PATCH  /workflow-definitions/{id}
POST   /workflow-definitions/{id}/validate
POST   /workflow-definitions/{id}/simulate
POST   /workflow-definitions/{id}/approve
POST   /workflow-definitions/{id}/activate

GET    /workflow-instances/{id}
POST   /workflow-instances/{id}/transition
GET    /workflow-instances/{id}/available-actions
```

## Approval

```text
GET    /approval-policies
POST   /approval-policies
GET    /approval-policies/{id}
PATCH  /approval-policies/{id}
POST   /approval-policies/{id}/simulate
POST   /approval-policies/{id}/activate

GET    /approval-requests
GET    /approval-requests/{id}
POST   /approval-requests/{id}/approve
POST   /approval-requests/{id}/reject
POST   /approval-requests/{id}/request-changes
POST   /approval-requests/{id}/cancel
```

## SLA

```text
GET    /sla-policies
POST   /sla-policies
GET    /sla-policies/{id}
PATCH  /sla-policies/{id}
POST   /sla-policies/{id}/simulate
POST   /sla-policies/{id}/activate

GET    /sla-instances
GET    /sla-instances/{id}
POST   /sla-instances/{id}/pause-request
POST   /sla-instances/{id}/resume
POST   /sla-instances/{id}/extension-request
POST   /sla-instances/{id}/complete
```

## Notification

```text
GET    /notification-templates
POST   /notification-templates
GET    /notification-templates/{id}
PATCH  /notification-templates/{id}
POST   /notification-templates/{id}/preview
POST   /notification-templates/{id}/activate

GET    /notification-policies
POST   /notification-policies
PATCH  /notification-policies/{id}
POST   /notification-policies/{id}/activate

GET    /notifications
POST   /notifications/{id}/retry
```

## Feature Flag

```text
GET    /feature-flags
POST   /feature-flags
GET    /feature-flags/{id}
PATCH  /feature-flags/{id}
POST   /feature-flags/{id}/rules
POST   /feature-flags/{id}/activate
POST   /feature-flags/{id}/deactivate
GET    /feature-flags/evaluate
```

## Integration

```text
GET    /integration-profiles
POST   /integration-profiles
GET    /integration-profiles/{id}
PATCH  /integration-profiles/{id}
POST   /integration-profiles/{id}/test
POST   /integration-profiles/{id}/activate
POST   /integration-profiles/{id}/rotate-secret
GET    /integration-profiles/{id}/logs
```

## Webhook và Job

```text
GET    /webhook-subscriptions
POST   /webhook-subscriptions
PATCH  /webhook-subscriptions/{id}
POST   /webhook-deliveries/{id}/replay

GET    /scheduled-jobs
POST   /scheduled-jobs
PATCH  /scheduled-jobs/{id}
POST   /scheduled-jobs/{id}/run
GET    /scheduled-jobs/{id}/runs
```

## Import/Export

```text
POST   /imports
GET    /imports/{id}
POST   /imports/{id}/validate
POST   /imports/{id}/preview
POST   /imports/{id}/execute

POST   /exports
GET    /exports/{id}
POST   /exports/{id}/approve
POST   /exports/{id}/generate
POST   /exports/{id}/cancel
```

---

# 42. Candidate permission vocabulary — không phải Permission Registry canonical

> Các mã dưới đây là đầu vào đặt tên. Exact permission codes, scopes, role mappings và masking rules thuộc security registries/matrices.


```text
system.view
system.configure
system.view_health
system.view_audit

enterprise.view
enterprise.update

legal_entity.view
legal_entity.create
legal_entity.update
legal_entity.activate
legal_entity.deactivate
legal_entity.manage_roles
legal_entity.view_sensitive

configuration_definition.view
configuration_definition.create
configuration_definition.update

configuration.view
configuration.create
configuration.update_draft
configuration.validate
configuration.simulate
configuration.review
configuration.approve
configuration.schedule
configuration.activate
configuration.suspend
configuration.create_version
configuration.view_audit

dictionary.view
dictionary.create
dictionary.update
dictionary_item.create
dictionary_item.update
dictionary_item.activate
dictionary_item.deactivate
dictionary_item.replace

business_calendar.view
business_calendar.create
business_calendar.update
business_calendar.approve
business_calendar.activate

numbering_scheme.view
numbering_scheme.create
numbering_scheme.update
numbering_scheme.approve
numbering_scheme.activate
numbering_scheme.issue_test

workflow_definition.view
workflow_definition.create
workflow_definition.update
workflow_definition.validate
workflow_definition.simulate
workflow_definition.review
workflow_definition.approve
workflow_definition.activate

approval_policy.view
approval_policy.create
approval_policy.update
approval_policy.simulate
approval_policy.review
approval_policy.approve
approval_policy.activate

approval_request.view
approval_request.approve
approval_request.reject
approval_request.request_changes
approval_request.cancel

sla_policy.view
sla_policy.create
sla_policy.update
sla_policy.simulate
sla_policy.review
sla_policy.approve
sla_policy.activate

notification_template.view
notification_template.create
notification_template.update
notification_template.preview
notification_template.approve
notification_template.activate

notification_policy.view
notification_policy.create
notification_policy.update
notification_policy.approve
notification_policy.activate

feature_flag.view
feature_flag.create
feature_flag.update
feature_flag.approve
feature_flag.activate

integration.view
integration.create
integration.update
integration.test
integration.activate
integration.rotate_secret
integration.view_logs

webhook.view
webhook.create
webhook.update
webhook.replay

scheduled_job.view
scheduled_job.create
scheduled_job.update
scheduled_job.run
scheduled_job.retry
scheduled_job.view_logs

import.view
import.create
import.validate
import.preview
import.execute
import.approve

export.request
export.view
export.approve
export.generate
export.download
export.cancel

security_policy.view
security_policy.configure
retention_policy.view
retention_policy.configure
```

Các quyền trên tiếp tục kết hợp với scope phù hợp.

---

# 43. Phân quyền vai trò tham khảo

## 43.1. Super Admin

Có thể:

* Quản lý cấu hình kỹ thuật toàn hệ thống.
* Xử lý lỗi hệ thống.
* Quản lý integration.
* Quản lý feature flag.
* Quản lý config schema.

Không mặc định được:

* Phê duyệt tài chính.
* Thay đổi tiền giao dịch.
* Tự duyệt Revenue hoặc hoa hồng.

## 43.2. CRM Admin

Có thể:

* Quản lý danh mục.
* Workflow.
* SLA.
* Template.
* Config.
* Job.
* Integration theo phạm vi.

Không mặc định được:

* Xem secret plaintext.
* Tự duyệt cấu hình nhạy cảm.
* Thực hiện thanh toán.

## 43.3. Giám đốc

Có thể:

* Duyệt chính sách doanh nghiệp.
* Duyệt workflow nhạy cảm.
* Duyệt approval matrix.
* Duyệt SLA quan trọng.
* Duyệt thay đổi có ảnh hưởng toàn công ty.

## 43.4. Kế toán – Tài chính

Có thể tham gia cấu hình:

* Kỳ tài chính.
* Mẫu phiếu.
* Quy tắc thanh toán.
* Tài khoản nhận.
* Export tài chính.
* Tích hợp kế toán/ngân hàng.

## 43.5. Pháp chế

Có thể tham gia:

* Mẫu hợp đồng.
* Loại tài liệu.
* Quy trình pháp lý.
* Chính sách retention.
* Legal hold.
* Phê duyệt template pháp lý.

---

# 44. Rule nghiệp vụ bắt buộc

1. Platform Configuration Capability là nguồn cấu hình chuẩn của hệ thống.
2. Các module không được tự hardcode rule thay đổi được.
3. System invariant không được biến thành công tắc tùy ý.
4. Enterprise và Legal Entity là hai khái niệm khác nhau.
5. Một Enterprise có thể có nhiều Legal Entity.
6. Legal Entity đã phát sinh giao dịch không được xóa cứng.
7. Config quan trọng phải có version.
8. Config active không được sửa trực tiếp.
9. Config mới không áp dụng hồi tố âm thầm.
10. Config phải có scope.
11. Cơ chế resolve phải xác định rõ.
12. Config cụ thể hơn không mặc định luôn thắng nếu schema không quy định.
13. Config phải validate trước khi kích hoạt.
14. Config nhạy cảm phải có phê duyệt.
15. Người tạo không được tự duyệt nếu policy cấm.
16. Dictionary system code không được đổi ý nghĩa.
17. Dictionary item đã dùng không được xóa cứng.
18. Business Calendar phải có version.
19. SLA phải lưu calendar version hoặc snapshot.
20. Numbering phải chống trùng bằng transaction.
21. Số chính thức đã cấp không được tái sử dụng.
22. Workflow phải có version.
23. Workflow active không sửa trực tiếp.
24. Resource phải lưu workflow version đang sử dụng.
25. Transition phải được backend kiểm tra.
26. Frontend không được tự chuyển state.
27. Approval policy phải tránh vòng lặp.
28. Approval không được vượt quyền người duyệt.
29. Delegation không vượt quyền người ủy quyền.
30. SLA là cấu hình động.
31. Pause SLA cần lý do.
32. Gia hạn SLA cần lịch sử.
33. Quá SLA không tự phê duyệt.
34. Notification phải chống gửi trùng.
35. Notification lỗi phải có retry.
36. Template phải có version.
37. Template không được lộ biến nhạy cảm trái quyền.
38. Feature flag không được tắt system invariant.
39. Credential không lưu plaintext.
40. Credential giữa môi trường phải tách biệt.
41. Webhook inbound phải chống replay.
42. Event consumer phải idempotent.
43. Event schema thay đổi phải có version.
44. Job thay đổi tiền phải có kiểm soát.
45. Job phải chống chạy trùng.
46. Import không được bỏ qua backend rule.
47. Export phải tuân thủ permission từng module.
48. Export nhạy cảm phải có audit.
49. Audit log không được sửa.
50. Mọi phép tính tiền phải dùng decimal.
51. Dữ liệu thời gian phải xử lý múi giờ thống nhất.
52. Retention không được xóa dữ liệu đang legal hold.
53. Dữ liệu tài chính không xóa cứng tùy ý.
54. Soft delete khác Archive.
55. Restore phải kiểm tra xung đột.
56. Error response không lộ secret.
57. Mọi request cần correlation ID.
58. Idempotency key cùng payload khác phải bị từ chối.
59. Config resolution phải có khả năng giải thích.
60. Mọi thay đổi cấu hình quan trọng phải có audit.

---

# 45. Cảnh báo và phát hiện bất thường

Hệ thống cần cảnh báo khi:

* Config active không có người duyệt.
* Hai config cùng scope và cùng thời gian bị xung đột.
* Config không thể resolve.
* Approval policy không tìm được approver.
* Approval policy có vòng lặp.
* Workflow có state không thể đi tới.
* Workflow không có terminal state.
* Workflow transition thiếu permission.
* SLA không có Business Calendar.
* SLA âm hoặc không hợp lệ.
* SLA bị pause quá lâu.
* Notification thất bại hàng loạt.
* Template thiếu biến.
* Feature flag bật toàn hệ thống ngoài kế hoạch.
* Secret sắp hết hạn.
* Integration dùng credential sai môi trường.
* Webhook bị replay.
* Job chạy đồng thời ngoài policy.
* Job thất bại liên tục.
* Import có tỷ lệ lỗi cao.
* Export số lượng lớn bất thường.
* Legal Entity hết hiệu lực nhưng vẫn được dùng.
* Numbering scheme sắp hết khoảng sequence.
* Dictionary item ngừng hoạt động nhưng vẫn được chọn.
* User tự tạo và tự duyệt cấu hình nhạy cảm.
* Retention job cố xóa dữ liệu đang legal hold.

---

# 46. Tương tác với các capability và Context khác

## 46.1. Identity, Access and Organization — `iam`

Sử dụng:

- Enterprise và Legal Entity references.
- Business Calendar.
- Approval Policy.
- Security baseline.
- Dictionary.
- Feature configuration.

`iam` vẫn sở hữu User, Workforce, Organization, Authentication, Authorization, Delegation và access runtime.

## 46.2. Lead Management — `lead`

Sử dụng:

- Lead-source dictionaries.
- Assignment và protection policies.
- Workflow Definition.
- SLA Policy.
- Notification Policy.
- Approval Policy cho dispute hoặc exception.

## 46.3. Party, Customer and Requirement — `party`

Sử dụng:

- Party/Customer dictionaries.
- Field-classification và masking-policy references.
- Requirement lifecycle definitions.
- Approval Policy cho shared identity/merge exceptions.
- Document type và template references.

## 46.4. Product, Asset, Listing and Inventory — `product`

Sử dụng:

- Asset/property dictionaries.
- Transaction Model và Company Role dictionaries.
- Listing policy.
- Price/approval policy.
- Numbering definition.
- Feature configuration.
- Business Calendar.

Product Context vẫn sở hữu Availability và Commercial Lock.

## 46.5. Matching — `matching`

Sử dụng:

- Matching rule-set definitions.
- Weight/configuration versions.
- Feature configuration.
- SLA/Notification policies.

Matching execution và result ownership vẫn thuộc `matching`.

## 46.6. Deal and Transaction — `transaction`

Sử dụng:

- Deal stage definitions.
- Transaction Model.
- Proposal/Hold/Booking policy references.
- Approval Policy.
- Numbering definition.
- SLA và Notification policies.

Transaction Context không được dùng configuration để bypass Product Commercial Lock.

## 46.7. Contract and Cash — `contract`

Sử dụng:

- Contract policy and templates.
- Payment schedule/calendar definitions.
- Numbering definition.
- Approval Policy.
- Legal Entity references.
- Retention-policy references.

Contract Context vẫn sở hữu Payment, Allocation, Receipt, Refund và Settlement invariants.

## 46.8. Revenue and Commission — `revenue`

Sử dụng:

- Revenue Arrangement policy references.
- Commission Plan policy references.
- Period metadata.
- Approval Policy.
- Feature configuration.
- Notification và job policy references.

Revenue Context vẫn sở hữu financial calculations, entitlement, recognition, payable, payout và clawback.

## 46.9. Activity and Engagement — `activity`

Sử dụng:

- SLA Policy.
- Business Calendar.
- Task/interaction dictionaries.
- Notification Policy.

Activity Context sở hữu operational Task, Appointment, Interaction và SLA instance behavior theo Context Pack.

## 46.10. Marketing — `marketing`

Sử dụng:

- Campaign/source dictionaries.
- Consent-policy references.
- Template và notification policies.
- Integration-profile definitions.

Marketing Context vẫn sở hữu Campaign, Audience, Journey, Attribution và marketing eligibility.

## 46.11. Analytics — `analytics`

Sử dụng:

- Reporting Calendar.
- Metric-policy references.
- Feature configuration.
- Export-policy references.

Analytics không được dùng Platform configuration để trở thành source of truth nghiệp vụ.

## 46.12. Documents, Audit, Integration và Operations

- `documents` sử dụng Document Type, retention, template và signature-provider definitions.
- `audit` sử dụng audit-policy definitions nhưng sở hữu immutable Audit facts.
- `integration` sử dụng Integration Profile/secret references nhưng sở hữu runtime connections, mappings, deliveries và reconciliation.
- `operations` sử dụng Job Schedule/maintenance/recovery definitions nhưng sở hữu runtime jobs, queues, incidents, backup và restore evidence.

---
# 47. Doanh nghiệp nhỏ và doanh nghiệp lớn

## 47.1. Doanh nghiệp nhỏ

Có thể sử dụng cấu hình đơn giản:

* Một Enterprise.
* Một Legal Entity.
* Một Business Calendar.
* Một workflow mặc định.
* Một approval matrix.
* Một vai trò Kế toán – Tài chính.
* Một kỳ hoa hồng hàng tháng.
* Ít tích hợp.

## 47.2. Doanh nghiệp lớn

Có thể mở rộng:

* Nhiều Legal Entity.
* Nhiều chi nhánh.
* Cấu hình theo dự án.
* Workflow riêng theo mô hình giao dịch.
* Approval nhiều cấp.
* Nhiều Business Calendar.
* Nhiều integration.
* Feature rollout theo đơn vị.
* Data retention theo pháp nhân.
* Multi-currency.
* Event bus.
* Data warehouse.

Cùng một codebase phải hỗ trợ cả hai bằng cấu hình và permission bundle.

---

# 48. Phạm vi MVP

## 48.1. Bắt buộc trong MVP

* Enterprise Profile.
* Legal Entity.
* Legal Entity Role.
* Config Registry cơ bản.
* Config theo Enterprise và Legal Entity.
* Config version.
* Dictionary.
* Business Calendar.
* Numbering.
* Workflow definition cơ bản.
* Workflow state và transition.
* Approval policy cơ bản.
* SLA policy.
* Notification template.
* In-app và email notification.
* Feature flag.
* Integration profile cơ bản.
* Secret reference.
* Job scheduler cơ bản.
* Import/export framework cơ bản.
* Audit cấu hình.
* Permission Platform Configuration Capability.
* API resolve config.
* Transaction model dictionary.
* Revenue model dictionary.
* Payment flow model dictionary.

## 48.2. Giai đoạn nâng cao

* Workflow designer kéo thả.
* Approval quorum.
* Dynamic expression builder.
* Notification đa kênh.
* Zalo/SMS.
* Percentage rollout.
* Multi-currency.
* Advanced secret manager.
* Event bus mở rộng.
* Webhook marketplace.
* Data retention automation.
* Legal hold.
* Data quality engine.
* Configuration simulation nâng cao.
* Config dependency graph.
* Canary rollout.
* Automated rollback.
* Multi-enterprise SaaS nếu tương lai cần.

---

# 49. Tiêu chí nghiệm thu

Capability baseline được xem là đáp ứng khi:

1. Tạo được Enterprise Profile.
2. Cấu hình được ngôn ngữ mặc định.
3. Cấu hình được múi giờ.
4. Cấu hình được tiền tệ.
5. Tạo được nhiều Legal Entity.
6. Một Legal Entity có nhiều vai trò.
7. Legal Entity hết hiệu lực không bị xóa.
8. Tạo được config definition.
9. Config definition có schema.
10. Config được validate.
11. Config có scope.
12. Config có version.
13. Config active không sửa trực tiếp.
14. Tạo được version mới.
15. Version mới có ngày hiệu lực.
16. Config resolve đúng theo scope.
17. Có thể giải thích config nào được chọn.
18. Config cũ không bị ghi đè.
19. Config mới không làm đổi dữ liệu lịch sử.
20. Tạo được Business Dictionary.
21. Tạo được Dictionary Item.
22. Item đã dùng không xóa cứng.
23. Có thể ngừng sử dụng item.
24. System enum không đổi mã kỹ thuật.
25. Tạo được Business Calendar.
26. Cấu hình được giờ làm việc.
27. Cấu hình được ngày nghỉ.
28. Tính được deadline theo business time.
29. Tính được deadline theo continuous time.
30. Calendar có version.
31. Tạo được Numbering Scheme.
32. Numbering có prefix.
33. Numbering có sequence.
34. Numbering reset theo policy.
35. Hai request đồng thời không nhận cùng số.
36. Số chính thức không được tái sử dụng.
37. Tạo được Workflow Definition.
38. Workflow có state.
39. Workflow có transition.
40. Transition kiểm tra permission.
41. Transition kiểm tra guard.
42. Frontend không tự chuyển state.
43. Workflow có version.
44. Resource lưu workflow version.
45. Workflow mới không tự áp vào resource cũ.
46. Tạo được Approval Policy.
47. Approval có nhiều bước.
48. Approval hỗ trợ tuần tự.
49. Approval hỗ trợ song song cơ bản.
50. Approval tìm đúng người duyệt.
51. Approval chặn self-approval khi policy cấm.
52. Delegation không vượt quyền gốc.
53. Tạo được SLA Policy.
54. SLA có duration.
55. SLA có Business Calendar.
56. SLA có warning threshold.
57. SLA có escalation.
58. SLA có pause.
59. SLA có extension.
60. Quá SLA không tự duyệt.
61. Tạo được Notification Template.
62. Template có version.
63. Template validate biến.
64. Notification chống gửi trùng.
65. Notification có retry.
66. Notification lỗi được ghi log.
67. Tạo được Feature Flag.
68. Feature Flag áp dụng theo scope.
69. Feature Flag có ngày hiệu lực.
70. Feature Flag không tắt được system invariant.
71. Tạo được Integration Profile.
72. Test connection hoạt động.
73. Credential không hiển thị plaintext.
74. Credential tách theo môi trường.
75. Webhook có signature.
76. Webhook chống replay.
77. Webhook có retry.
78. Event có version.
79. Event consumer có idempotency.
80. Job scheduler chạy được.
81. Job có lock.
82. Job không chạy trùng ngoài policy.
83. Job lỗi có retry.
84. Import có preview.
85. Import có validation.
86. Import không bỏ qua duplicate rule.
87. Export có approval theo quyền.
88. Export có file hash.
89. Export có ngày hết hạn.
90. Export có download log.
91. Audit lưu before/after.
92. Audit lưu actor.
93. Audit lưu request ID.
94. Audit không sửa được.
95. Retention không xóa dữ liệu legal hold.
96. Soft delete và archive được phân biệt.
97. API error không lộ stack trace.
98. Mọi request có correlation ID.
99. Idempotency conflict được phát hiện.
100. các capability và Context liên quan có thể resolve cấu hình qua API Platform Configuration Capability.
101. Mã `transaction_model` được sử dụng thống nhất.
102. Mã `payment_flow_model` được sử dụng thống nhất.
103. Mã `revenue_model` được sử dụng thống nhất.
104. Mã `company_role` được sử dụng thống nhất.
105. Hệ thống hoạt động với một Legal Entity.
106. Hệ thống mở rộng được nhiều Legal Entity.
107. Doanh nghiệp nhỏ không phải cấu hình quá phức tạp.
108. Doanh nghiệp lớn có thể override theo dự án và pháp nhân.
109. Mọi cấu hình quan trọng có lịch sử.
110. Không có owning business Context nào cần hardcode SLA hoặc approval riêng ngoài system invariant.

---

# 50. Anti-patterns và canonical requirements

Phần này thay thế mọi cách diễn đạt mang tính “phiên bản cũ/phiên bản mới”. Các nội dung dưới đây là quy tắc hiện hành của dự án Greenfield.

## AP-PLA-001 — Hardcode policy phân tán

**Không được áp dụng**

Cùng một business rule tồn tại đồng thời trong source code, frontend, environment file và database với các giá trị khác nhau.

**Canonical requirement**

Mỗi configurable business rule phải có một nguồn canonical, schema, owner, scope, version, effective period và resolution strategy.

## AP-PLA-002 — Biến system invariant thành configuration toggle

**Không được áp dụng**

Cho phép người dùng tắt authorization, Audit, idempotency, Commercial Lock, Receipt immutability hoặc financial integrity bằng Feature Flag/configuration.

**Canonical requirement**

System invariants phải được owning Context enforce và không được cấu hình tắt.

## AP-PLA-003 — Nhầm Enterprise với Legal Entity

**Không được áp dụng**

Dùng Enterprise, Legal Entity, branch hoặc project như cùng một khái niệm.

**Canonical requirement**

Enterprise operating boundary và Legal Entity legal identity phải có meaning, lifecycle và references riêng theo Domain Glossary và ADR.

## AP-PLA-004 — Sửa active configuration tại chỗ

**Không được áp dụng**

Chỉnh trực tiếp configuration, workflow, approval, SLA, template hoặc policy đang active.

**Canonical requirement**

Thay đổi có ảnh hưởng hành vi phải tạo version mới, validation, review/approval, effective period và Audit.

## AP-PLA-005 — Áp dụng hồi tố âm thầm

**Không được áp dụng**

Khi policy mới active, tự động tính lại hoặc đổi state của records lịch sử.

**Canonical requirement**

Historical records phải giữ policy/version đã sử dụng. Recalculation hoặc migration cần scope, approval, evidence và reconciliation.

## AP-PLA-006 — Generic workflow sở hữu Domain state

**Không được áp dụng**

Platform Workflow Engine trực tiếp cập nhật aggregate của Lead, Product, Booking, Contract, Payment, Revenue hoặc Commission.

**Canonical requirement**

Platform sở hữu versioned definitions; owning Context thực thi transition và bảo vệ Domain invariants.

## AP-PLA-007 — Control Plane sở hữu Runtime Plane

**Không được áp dụng**

Cho rằng Platform sở hữu Notification delivery, webhook execution, queue, jobs, Audit facts, Documents hoặc operational incidents chỉ vì Platform định nghĩa policy.

**Canonical requirement**

Definitions thuộc Platform; runtime instances thuộc owning Context theo Source of Truth Matrix và Context Map.

## AP-PLA-008 — Secret trong configuration record

**Không được áp dụng**

Lưu API key, token, password hoặc private key dưới dạng plaintext trong database/configuration file thông thường.

**Canonical requirement**

Platform chỉ lưu secret reference và metadata cần thiết. Secret actual value thuộc approved secret-management boundary.

## AP-PLA-009 — Frontend quyết định state hoặc scope

**Không được áp dụng**

Frontend tự chuyển state, chọn approver, mở rộng scope hoặc quyết định policy được áp dụng.

**Canonical requirement**

Backend phải resolve configuration, enforce permission, validate guards và thực hiện transition tại trusted boundary.

## AP-PLA-010 — Một resolution order cho mọi config

**Không được áp dụng**

Luôn giả định “scope cụ thể nhất thắng” cho mọi configuration type.

**Canonical requirement**

Mỗi Configuration Definition phải công bố allowed scopes và strategy như most-specific, merge, accumulate, first-match hoặc highest-restriction.

## AP-PLA-011 — Numbering gapless không có business/legal basis

**Không được áp dụng**

Hứa sequence luôn liên tục tuyệt đối chỉ vì giao diện mong muốn.

**Canonical requirement**

Numbering phải unique, concurrency-safe và không tái sử dụng số issued. Gap behavior phải do policy/legal requirement quyết định và được thiết kế riêng.

## AP-PLA-012 — Exact implementation từ Capability Specification

**Không được áp dụng**

Dùng candidate tables, endpoints, Event examples hoặc permission codes trong tài liệu này như exact contract để code ngay.

**Canonical requirement**

Exact implementation phải được khóa trong Context Pack, Alembic, OpenAPI, JSON Schema/AsyncAPI và security registries trước khi triển khai.

## AP-PLA-013 — Legacy migration mặc định

**Không được áp dụng**

Suy luận rằng có hệ thống tiền nhiệm, dữ liệu legacy hoặc compatibility layer cần duy trì.

**Canonical requirement**

`crm_bds_ai` là Greenfield. Legacy migration chỉ tồn tại khi có approved migration scope, mapping, reconciliation và acceptance criteria riêng.

---

# 51. Quy tắc traceability cho tài liệu liên quan

Mỗi capability hoặc Context sử dụng Platform definitions phải chỉ rõ:

1. Product Requirement IDs liên quan.
2. Owning Context.
3. Configuration Definitions sử dụng.
4. Allowed scopes và resolution strategy.
5. Dictionary references.
6. Workflow Definitions sử dụng.
7. Approval Policies sử dụng.
8. SLA Policies và Business Calendar references.
9. Numbering Schemes sử dụng.
10. Template/Notification policies sử dụng.
11. Feature configuration liên quan.
12. Integration profile definitions liên quan.
13. Events được produce/consume trong machine-readable contracts.
14. System invariants không được cấu hình.
15. Các policy/version cần snapshot trên business record.
16. Acceptance tests và evidence.

Quy tắc này ngăn:

- Duplicate configuration engines.
- Cross-context ownership drift.
- Hardcoded policy.
- Policy version bị mất khỏi historical lineage.
- Capability Specification bị dùng thay exact contract.

---

# 52. Kết luận

Platform Configuration Capability là control plane quản trị cách `crm_bds_ai` vận hành.

Capability phải bảo đảm:

- Quy tắc có thể thay đổi được cấu hình an toàn.
- System invariants vẫn được owning Context bảo vệ.
- Configuration có schema, scope, version và effective period.
- Historical records xác định được policy đã áp dụng.
- Enterprise và Legal Entity được phân biệt.
- Workflow Definition không thay Domain ownership.
- Approval, SLA, template và feature definitions có governance.
- Secret actual values không nằm trong configuration records.
- Control Plane và Runtime Plane được tách rõ.
- Mọi thay đổi quan trọng có Audit và evidence.
- Doanh nghiệp nhỏ có baseline đơn giản.
- Doanh nghiệp lớn có thể mở rộng bằng scope và policy có kiểm soát.

> Platform Configuration Capability là control plane nghiệp vụ của `crm_bds_ai`, không phải một siêu Context, không phải một generic CRUD settings page và không được thay thế quyền sở hữu của các Bounded Context khác.
