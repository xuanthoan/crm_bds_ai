# CRM_BDS_AI — CAPABILITY 06: PRODUCT, ASSET, LISTING AND INVENTORY

## Partner supply profile, Project, Property Asset, Ownership, Selling Right, Listing, Inventory, Pricing, Availability and Commercial Lock

**Document ID:** `PROD-CAP-PRO-001`  
**Canonical path:** `docs/product/capabilities/cap-06-product-asset-listing-inventory.md`  
**Product:** `crm_bds_ai`  
**Version:** `1.0.0`  
**Status:** `Accepted / Product Capability Baseline`  
**Document type:** `Product Capability Specification`  
**Primary capability code:** `CAP-PRO`  
**Primary owning Context:** `product`  
**Owner:** `Product Owner`  
**Co-owner:** `Product Domain Owner`  
**Reviewers:** `Architecture Owner`, `Party Domain Owner`, `Transaction Domain Owner`, `Contract Domain Owner`, `Revenue Domain Owner`, `Security Owner`, `Database Owner`, `API Owner`, `Event Architecture Owner`, `Documents Owner`, `Integration Owner`, `Operations Owner`, `QA Owner`  
**Effective date:** `2026-08-05`  
**Last reviewed:** `2026-08-05`  
**Classification:** `INTERNAL`

---

# 0. Phạm vi thẩm quyền và quan hệ tài liệu

Tài liệu này là nguồn canonical cho:

- Product outcomes của Product, Asset, Listing and Inventory Capability.
- Business meanings của Project, Property Asset, Ownership, Selling Right, Listing, Inventory, Price, Sales Policy, Availability và Commercial Lock.
- Capability boundaries, invariants, acceptance outcomes và anti-patterns.
- Đầu vào phân tích cho Product Context Implementation Pack.

Tài liệu này không phải nguồn exact cho:

- Physical database schema hoặc DDL.
- Exact API paths, request/response payloads.
- Exact Event names, envelope hoặc payloads.
- Exact permission codes, scopes, masking hoặc role matrix.
- Exact state machines, status codes, retry, timeout hoặc retention.
- Exact screen routes, component contracts hoặc certified Metrics.
- Provider-specific integration runtime.
- Contract, Payment, Revenue hoặc Commission calculations.

Nguồn exact tương ứng:

| Chủ đề | Nguồn canonical |
|---|---|
| Thuật ngữ | Domain Glossary |
| Product requirements | PRD |
| Context ownership | Source of Truth Matrix |
| Architecture boundaries | Architecture Overview, Context Map và Accepted ADRs |
| Product behavior chi tiết | Product Context Implementation Pack |
| Database | Product Context DB Specification và Alembic historical imports |
| API | OpenAPI |
| Events | JSON Schema, AsyncAPI và Event Registry |
| Permissions/scopes/masking | Security registries và matrices |
| Documents/File | Documents Context Pack và object-storage contracts |
| Provider transport/integration | Integration Context Pack |
| Runtime jobs/incidents | Operations Context Pack |
| Công việc hiện tại | Current Sprint Detailed Execution Pack |

**Capability không đồng nghĩa Bounded Context.** Capability này chủ yếu được thực hiện bởi `product` Context, nhưng sử dụng Party identity từ `party`, access decisions từ `iam`, policies từ `platform`, documents từ `documents`, provider transport từ `integration`, jobs từ `operations`, và phối hợp qua contracts/Events với `matching`, `transaction`, `contract`, `revenue`, `marketing`, `activity`, `analytics` và `audit`.

Các phần candidate lifecycle, data model, operations, permissions, Events, screens và reports chỉ là design input. Chúng không được dùng thay machine-readable contracts hoặc Context Packs đã được chấp nhận.

---
# 1. Mục tiêu của capability

Product, Asset, Listing and Inventory Capability là nguồn nghiệp vụ chuẩn cho nguồn cung bất động sản của `crm_bds_ai`.

Capability phải trả lời được:

- Bất động sản vật lý hoặc pháp lý nào đang được quản lý.
- Tài sản thuộc Project hay là tài sản độc lập.
- Party nào là Owner, Co-owner, Developer, Seller, Representative hoặc Partner.
- Ownership đã được xác minh ở mức nào.
- Asset có encumbrance hoặc legal restriction nào.
- Legal Entity nội bộ có quyền Marketing, Hold, Booking, thu tiền hoặc ký kết dựa trên căn cứ nào.
- Selling Right có phạm vi, tính độc quyền, thời hạn và authority gì.
- Asset đang được đưa ra thị trường qua Listing nào.
- Listing, Price List, Sales Policy và Inventory version nào đang có hiệu lực.
- Availability tại thời điểm request là gì và vì sao.
- Commercial Lock nào đang bảo vệ Listing.
- External source có còn đáng tin cậy và đủ mới hay không.
- Giá, policy, ownership, selling right và availability đã thay đổi như thế nào.
- Người dùng nào được xem Owner details, floor price, legal evidence hoặc private location.

Capability phải hỗ trợ:

- Công ty tự phát triển dự án.
- Legal Entity nội bộ sở hữu hoặc bán tài sản.
- Phân phối dự án của chủ đầu tư bên ngoài.
- Môi giới hoặc ký gửi tài sản của Customer.
- Partner-owned inventory.
- Project units/plots và standalone assets.
- Nhiều co-owners và nhiều Selling Rights.
- Nhiều Sales Launches, Inventory Lists, Price Lists và channels.
- External inventory feeds có reconciliation.
- Commercial Lock có thời hạn và concurrency protection.
- Listing bán; rental/lease chỉ khi được đưa vào approved scope.

Nguyên tắc canonical:

> Property Asset, Ownership, Selling Right và Listing là các lớp dữ liệu khác nhau. Giao dịch chỉ được tiếp tục khi Product Context xác nhận Listing, Selling Right, Price/Policy, legal/commercial readiness và Commercial Lock phù hợp trong trusted backend boundary.

---
# 2. Vị trí của capability trong kiến trúc

Product Capability nhận hoặc tham chiếu dữ liệu từ:

- `platform`: dictionary, Business Calendar, Numbering, Workflow/Approval/SLA definitions và configuration.
- `iam`: authenticated identity, effective access context và authorization results.
- `party`: canonical Party, Customer, Organization Identity, Seller Objective và declared ownership claims.
- `lead`: seller/consignment acquisition facts và conversion references.
- `documents`: Document/File IDs, versions, verification evidence và legal-hold state.
- `integration`: authenticated provider transport, mappings, raw payload references và delivery state.
- `operations`: job, batch, incident và reconciliation execution controls.

Product Capability cung cấp contracts/facts cho:

- `matching`: eligible Listing candidates, price/policy snapshots và availability.
- `transaction`: Product availability checks, Commercial Lock commands/results và commercial snapshots.
- `contract`: Asset/Listing/Selling Right snapshots và commercial/legal references.
- `revenue`: product-side commercial basis references; Revenue Context vẫn quyết định entitlement/recognition.
- `activity`: verification, renewal, reconciliation và operational task references.
- `marketing`: publishable Listing data và usage-right constraints.
- `analytics`: governed supply facts, versions và freshness metadata.
- Public/partner channels thông qua `integration` và approved public API contracts.

Luồng nguồn cung khái quát:

```text
Canonical Party/Partner
→ Project hoặc Standalone Property Asset
→ Ownership
→ Selling Right
→ Listing
→ Inventory/Channel Assignment
→ Price and Sales Policy
→ Availability and Commercial Lock
→ Matching
→ Deal/Booking
→ Contract
```

Luồng ký gửi:

```text
Seller Lead
→ Canonical Customer/Party
→ Declared Asset Claim
→ Product Asset Verification
→ Verified Ownership
→ Consignment/Brokerage Selling Right
→ Listing
```

Product Context không được trực tiếp tạo hoặc sửa Deal, Booking, Contract, Payment, Receipt, Revenue hoặc Commission.

---
# 3. Ranh giới sở hữu dữ liệu

## 3.1. Product Context sở hữu

- Supply-side Partner Profile gắn với canonical Party reference.
- Project, Project hierarchy và Sales Launch.
- Property Asset và Asset identity.
- Physical, legal và product-verification state.
- Ownership records, co-owner participation và ownership history.
- Encumbrance và Product-side legal-readiness evaluation.
- Selling Right, bao gồm developer, distribution, brokerage, consignment và collection/negotiation authority.
- Listing, Listing versions, visibility, commercial terms và readiness.
- Inventory Lists, versions, items và channel assignments.
- Price Lists, versions, items và price components ở product/commercial layer.
- Sales Policy definitions/versions trong Product domain.
- Product Availability.
- Commercial Lock và Waitlist semantics.
- Accepted external-inventory observations và Product-side reconciliation decisions.
- Asset/Listing duplicate candidates.
- Product-side media usage metadata và Document references.
- Product business history và Product-originated Audit requests/facts.

## 3.2. Product Context không sở hữu

- Canonical Party, Customer, Customer Identity hoặc Organization Identity: `party`.
- User, Workforce, role/permission/scope definitions: `iam`.
- Lead, attribution hoặc care protection: `lead`.
- Matching score, Match Run hoặc Shortlist: `matching`.
- Deal, Proposal, Negotiation, Hold business record, Booking hoặc Deposit Commitment: `transaction`.
- Contract, Payment Schedule, Receivable, Payment, Allocation, Receipt, Refund hoặc Settlement: `contract`.
- Revenue, Commission, Collection hoặc Payout: `revenue`.
- Task, Appointment hoặc Interaction: `activity`.
- Campaign, Audience, Journey hoặc Attribution: `marketing`.
- Certified Metrics, analytical projections hoặc dashboards: `analytics`.
- Binary File, Document, Document Version, dossier hoặc signature evidence: `documents`.
- Immutable Audit facts: `audit`.
- Provider connection, webhook transport, credential, retry/DLQ hoặc raw provider payload runtime: `integration`.
- Job, queue, incident, backup/restore hoặc deployment runtime: `operations`.

## 3.3. Commercial Lock và Transaction boundaries

Product Context sở hữu authoritative availability và Commercial Lock.

Transaction Context sở hữu:

- Deal.
- Transaction Case.
- Proposal/Negotiation.
- Hold business process.
- Booking.
- Deposit Commitment.

Transaction phải gọi published Product application contracts để:

- Kiểm tra availability.
- Yêu cầu tạo Lock.
- Yêu cầu gia hạn hoặc chuyển đổi Lock.
- Giải phóng Lock.
- Nhận conflict/result.
- Yêu cầu Product reclassify availability sau accepted business facts.

Transaction không được direct-write Product tables. Product không được direct-write Transaction tables.

## 3.4. Documents, media và legal evidence

Product giữ:

- `document_id` hoặc evidence reference.
- Verification summary.
- Access-policy reference.
- Usage-right metadata.
- Effective period.
- Product-side relationship tới Project/Asset/Ownership/Selling Right/Listing.

`documents` sở hữu:

- Binary object.
- File metadata.
- Document và Document Version.
- Verification evidence.
- OCR/extraction.
- Signature evidence.
- Legal Hold.

Product không lưu permanent public URLs làm canonical identity của restricted files.

## 3.5. External inventory boundary

`integration` sở hữu provider-specific transport, authentication, credentials, delivery attempts, retries, raw payload references và provider ACL.

`product` sở hữu:

- Mapping từ accepted external supply identity sang internal Project/Asset/Listing khi được thiết kế như Product-domain mapping.
- External observation đã được chuẩn hóa và chấp nhận.
- Availability impact.
- Business reconciliation case và resolution.

Không Context nào được để provider payload trở thành Product Domain Model canonical một cách trực tiếp.

---
# 4. Nguyên tắc thiết kế cốt lõi

## 4.1. Tách Property Asset và Listing

### Property Asset

Là bất động sản vật lý hoặc pháp lý có danh tính ổn định.

Ví dụ:

* Căn A1205.
* Lô LK-03-12.
* Thửa đất 125, tờ bản đồ 08.
* Nhà số 18 đường X.

### Listing

Là một lần tài sản được chào bán hoặc cho thuê trên thị trường.

Một tài sản có thể:

* Được mở bán lần đầu.
* Tạm dừng.
* Bị rút khỏi bảng hàng.
* Được mở bán lại.
* Được chủ mới ký gửi.
* Được chào bán bởi một đối tác khác.
* Có nhiều Listing lịch sử.

Do đó:

```text
Property Asset ≠ Listing
```

## 4.2. Tách Ownership và Sales Mandate

Người sở hữu tài sản chưa chắc là người trực tiếp bán.

Công ty chỉ được đưa Listing vào giao dịch khi có:

* Quyền sở hữu trực tiếp.
* Vai trò chủ đầu tư.
* Quyền phân phối.
* Hợp đồng môi giới.
* Hợp đồng ký gửi.
* Ủy quyền.
* Căn cứ hợp lệ khác.

## 4.3. Tách trạng thái vật lý, pháp lý và thương mại

Một căn có thể:

* Đang xây dựng về vật lý.
* Đủ điều kiện mở bán về pháp lý.
* Đang được giữ về thương mại.

Không sử dụng một trường `status` duy nhất cho tất cả.

## 4.4. Tách giá hiện tại và lịch sử giá

Không ghi đè giá cũ.

Mọi giá được sử dụng trong Proposal, Booking hoặc Contract phải tham chiếu hoặc snapshot đúng version.

## 4.5. Tách Listing Availability và Asset Status

Asset có thể tồn tại và hợp lệ nhưng Listing đã hết hạn.

Listing có thể active nhưng tạm thời không khả dụng vì đang bị lock.

## 4.6. Backend là nơi quyết định khả dụng

Frontend không được tự kết luận:

```text
available = true
```

Backend phải kiểm tra:

* Listing active.
* Mandate active.
* Price active.
* Policy active.
* Legal restriction.
* Existing lock.
* Booking.
* Version.
* External source status.
* User access.
* Transaction model.

## 4.7. Không bán trùng dựa vào giao diện

Ẩn nút “Giữ chỗ” không đủ.

Phải có:

* Database transaction.
* Lock.
* Unique constraint.
* Version check.
* Idempotency.
* State transition validation.

## 4.8. Không cập nhật hồi tố âm thầm

Giá, chính sách và trạng thái mới không được thay đổi dữ liệu đã snapshot trong:

* Proposal.
* Hold.
* Booking.
* Contract.
* Revenue.
* Commission.

---

# 5. Các mô hình nguồn cung

## 5.1. Công ty tự phát triển dự án

Đặc điểm:

* Legal Entity nội bộ là developer hoặc seller.
* Công ty kiểm soát cấu trúc dự án.
* Công ty tạo các Unit hoặc Plot.
* Công ty quyết định giá và chính sách.
* Availability được kiểm soát nội bộ.
* Customer thanh toán theo mô hình của công ty.

Mã nguồn gốc:

```text
SELF_DEVELOPED
```

## 5.2. Phân phối dự án chủ đầu tư ngoài

Đặc điểm:

* Developer là Partner ngoài.
* Công ty có Distribution Mandate.
* Bảng hàng có thể do đối tác cung cấp.
* Availability có thể cần đồng bộ.
* Giá và chính sách do chủ đầu tư ban hành.
* Công ty có thể chỉ giữ mềm nội bộ trước khi xác nhận ngoài.

Mã nguồn gốc:

```text
THIRD_PARTY_PRIMARY
```

## 5.3. Tài sản Customer ký gửi

Đặc điểm:

* Owner là Customer hoặc nhiều Customer.
* Cần Asset Verification.
* Cần Ownership Verification.
* Cần Brokerage/Consignment Mandate.
* Listing có thể độc quyền hoặc không độc quyền.
* Giá và quyền đàm phán theo thỏa thuận chủ tài sản.

Mã nguồn gốc:

```text
CUSTOMER_OWNED_RESALE
```

## 5.4. Tài sản công ty sở hữu

Đặc điểm:

* Legal Entity nội bộ là owner.
* Tài sản có thể không do công ty phát triển.
* Cần quản lý giá vốn tham chiếu nếu tích hợp tài chính.
* Công ty là seller hoặc chỉ định pháp nhân bán.

Mã nguồn gốc:

```text
COMPANY_OWNED_RESALE
```

## 5.5. Tài sản đối tác

Đặc điểm:

* Owner là Partner.
* Có mandate hoặc agreement.
* Có thể độc quyền hoặc theo từng kênh.
* Bảng hàng có thể được đồng bộ ngoài.

Mã nguồn gốc:

```text
PARTNER_OWNED
```

---

# 6. Mô hình thực thể tổng quát

```text
Party/Partner
    ↓
Project hoặc Standalone Property
    ↓
Property Asset
    ↓
Ownership[]
    ↓
Sales Mandate[]
    ↓
Listing[]
    ↓
Inventory List / Channel
    ↓
Price List + Sales Policy
    ↓
Availability + Lock
```

Một Asset có thể thuộc dự án hoặc là tài sản riêng lẻ.

Một Listing luôn phải liên kết với một Asset hoặc một nhóm Asset hợp lệ.

---

# 7. Partner Business Profile

## 7.1. Khái niệm

Partner Business Profile mở rộng Party tổ chức từ Customer 360 Capability để sử dụng trong nguồn cung.

Partner có thể là:

* Chủ đầu tư.
* Đồng chủ đầu tư.
* Chủ đất.
* Chủ sở hữu tài sản.
* Tổng đại lý.
* Đại lý phân phối.
* Đối tác môi giới.
* Đối tác Marketing.
* Đơn vị quản lý dự án.
* Đơn vị quản lý vận hành.
* Ngân hàng.
* Nhà thầu.
* Đơn vị pháp lý.
* Đơn vị định giá.

## 7.2. Thông tin Partner

* Party ID.
* Partner code.
* Partner type.
* Legal name.
* Trade name.
* Tax code.
* Registration.
* Country.
* Address.
* Representative.
* Contact persons.
* Status.
* Risk status.
* Verification status.
* Contracting status.
* Effective dates.
* External IDs.
* Documents.
* Notes.

## 7.3. Không tạo Partner trùng

Organization Identity phải kiểm tra theo Customer Identity Governance Capability:

* Tax code.
* Registration number.
* Registry namespace.
* Legal entity relationship.

Hotline hoặc tên giống không đủ để tự merge Partner.

---

# 8. Loại Partner

```text
DEVELOPER
CO_DEVELOPER
LAND_OWNER_PARTNER
ASSET_OWNER_PARTNER
MASTER_AGENT
DISTRIBUTION_PARTNER
BROKERAGE_PARTNER
MARKETING_PARTNER
PROPERTY_MANAGER
CONSTRUCTION_PARTNER
LEGAL_PARTNER
FINANCIAL_PARTNER
OTHER
```

Một Partner có thể có nhiều type.

---

# 9. Xác minh Partner

## 9.1. Trạng thái

```text
UNVERIFIED
DOCUMENT_RECEIVED
UNDER_REVIEW
VERIFIED
VERIFIED_WITH_CONDITIONS
SUSPENDED
REJECTED
EXPIRED
```

## 9.2. Nội dung xác minh

* Tư cách pháp lý.
* Người đại diện.
* Tax code.
* Quyền đối với dự án/tài sản.
* Hợp đồng hợp tác.
* Tài khoản nhận tiền.
* Khả năng cung cấp bảng hàng.
* Rủi ro.
* Hạn sử dụng tài liệu.

## 9.3. Không tự kích hoạt nguồn cung khi Partner chưa đủ điều kiện

Tùy policy, Partner chưa verified có thể:

* Tạo draft Project.
* Tạo draft Asset.
* Không được active Listing.
* Không được nhận Booking.

---

# 10. Quan hệ giữa Partner và Legal Entity nội bộ

Mỗi quan hệ hợp tác cần xác định:

* Legal Entity nội bộ.
* Partner.
* Relationship type.
* Agreement.
* Project scope.
* Asset scope.
* Territory.
* Channel.
* Effective dates.
* Exclusivity.
* Revenue model.
* Payment flow model.
* Status.

Không mặc định toàn Enterprise có cùng quyền với mọi Partner.

---

# 11. Project

## 11.1. Khái niệm

Project là một tập hợp tài sản bất động sản được phát triển, quản lý hoặc bán trong một cấu trúc thống nhất.

Project có thể:

* Do công ty phát triển.
* Do pháp nhân dự án phát triển.
* Do chủ đầu tư ngoài phát triển.
* Do nhiều bên hợp tác.
* Là dự án đất nền.
* Là khu căn hộ.
* Là khu đô thị.
* Là khu nghỉ dưỡng.
* Là dự án thương mại.

## 11.2. Project không bắt buộc cho tài sản riêng lẻ

Một căn nhà hoặc thửa đất ký gửi có thể có:

```text
project_id = null
```

---

# 12. Thông tin Project

* Project code.
* Project name.
* Trade name.
* Legal name.
* Project type.
* Asset origin.
* Transaction model.
* Developer Party.
* Internal Legal Entity.
* Seller Legal Entity.
* Payment collector.
* Revenue beneficiary.
* Address.
* Geography.
* Coordinates.
* Total area.
* Total units.
* Development stage.
* Legal status.
* Sales status.
* Construction status.
* Expected launch.
* Expected handover.
* Effective dates.
* Status.
* Documents.
* Media.
* External IDs.

---

# 13. Project Type

```text
APARTMENT_PROJECT
URBAN_AREA
LAND_PLOT_PROJECT
TOWNSHIP
VILLA_PROJECT
TOWNHOUSE_PROJECT
COMMERCIAL_PROJECT
OFFICE_PROJECT
RESORT_PROJECT
INDUSTRIAL_PROJECT
MIXED_USE_PROJECT
OTHER
```

---

# 14. Project Parties và vai trò

Một Project có thể có nhiều Party:

* Developer.
* Co-developer.
* Land owner.
* Legal owner.
* Seller.
* Payment collector.
* Distributor.
* Master agent.
* Property manager.
* Construction contractor.
* Bank.
* Legal advisor.

Mỗi quan hệ phải có:

* Party.
* Role.
* Effective dates.
* Agreement.
* Scope.
* Verification.
* Status.

Không chỉ lưu một trường `developer_id`.

---

# 15. Project Hierarchy

## 15.1. Cấu trúc linh hoạt

```text
Project
→ Phase
→ Zone/Subdivision
→ Building/Tower
→ Floor/Row
→ Unit/Plot
```

Không phải dự án nào cũng dùng đủ các cấp.

## 15.2. Node Type

```text
PROJECT
PHASE
ZONE
SUBDIVISION
TOWER
BLOCK
BUILDING
FLOOR
ROW
CLUSTER
OTHER
```

## 15.3. Cây hierarchy có version

Khi thay đổi:

* Không xóa node cũ đã dùng.
* Tạo version hoặc lịch sử.
* Giữ Asset link.

---

# 16. Development Stage

```text
PLANNING
LAND_ACQUISITION
LEGAL_PREPARATION
CONSTRUCTION_PREPARATION
UNDER_CONSTRUCTION
PARTIALLY_COMPLETED
COMPLETED
HANDED_OVER
OPERATING
SUSPENDED
CANCELLED
```

Development Stage không đồng nghĩa Sales Status.

---

# 17. Project Legal Status

Có thể gồm:

* Chưa xác minh.
* Đang hoàn thiện thủ tục.
* Có chấp thuận đầu tư.
* Có quy hoạch.
* Có giấy phép xây dựng.
* Đủ điều kiện mở bán.
* Hạn chế mở bán.
* Đang tranh chấp.
* Tạm dừng.
* Hoàn tất pháp lý.

Chi tiết và mã danh mục phải cấu hình theo loại dự án và pháp luật áp dụng.

---

# 18. Sales Launch

## 18.1. Khái niệm

Sales Launch là một đợt mở bán hoặc đợt phân phối cụ thể.

Một Project có thể có nhiều đợt.

## 18.2. Thông tin

* Launch code.
* Project.
* Tên đợt.
* Legal Entity.
* Partner.
* Start/end.
* Channel.
* Target segment.
* Inventory scope.
* Price list.
* Policy.
* Booking workflow.
* Payment flow model.
* Status.
* Approval.

## 18.3. Trạng thái

```text
DRAFT
PREPARING
PENDING_APPROVAL
SCHEDULED
ACTIVE
PAUSED
CLOSED
CANCELLED
ARCHIVED
```

## 18.4. Launch không thay Asset hoặc Listing

Một Listing có thể tham gia nhiều Sales Launch theo thời gian nhưng không đồng thời trái policy.

---

# 19. Property Asset

## 19.1. Khái niệm

Property Asset là thực thể bất động sản có danh tính ổn định.

## 19.2. Asset có thể là

* Một căn hộ.
* Một căn biệt thự.
* Một nhà phố.
* Một shophouse.
* Một lô đất.
* Một thửa đất.
* Một tòa nhà.
* Một tầng.
* Một văn phòng.
* Một kho.
* Một tài sản thương mại.
* Một phần tài sản nếu pháp lý cho phép.

## 19.3. Asset phải có Asset Code

Mã được cấp qua Numbering Engine hoặc mã nguồn bên ngoài được chuẩn hóa.

---

# 20. Loại Property Asset

```text
APARTMENT
STUDIO
PENTHOUSE
DUPLEX
TOWNHOUSE
VILLA
SHOPHOUSE
LAND_PLOT
LAND_PARCEL
HOUSE
OFFICE
RETAIL
WAREHOUSE
INDUSTRIAL
HOTEL_UNIT
RESORT_VILLA
PARKING
OTHER
```

Danh mục có thể mở rộng nhưng phải map về canonical type.

---

# 21. Thuộc tính chung của Asset

* Asset code.
* Project.
* Hierarchy node.
* Asset type.
* Name.
* Unit number.
* Plot number.
* Floor.
* Block.
* Address.
* Coordinates.
* Gross area.
* Net usable area.
* Land area.
* Construction area.
* Frontage.
* Depth.
* Bedrooms.
* Bathrooms.
* Orientation.
* View.
* Balcony.
* Handover standard.
* Furnishing.
* Construction status.
* Usage status.
* Legal profile.
* Verification status.
* Status.
* External IDs.

---

# 22. Thuộc tính căn hộ và nhà xây sẵn

Có thể gồm:

* Tòa.
* Tầng.
* Số căn.
* Loại căn.
* Tim tường.
* Thông thủy.
* Số phòng ngủ.
* Số phòng tắm.
* Logia.
* Hướng cửa.
* Hướng ban công.
* View.
* Nội thất.
* Tình trạng bàn giao.
* Phí quản lý.
* Chỗ đỗ xe.
* Tình trạng sử dụng.

---

# 23. Thuộc tính đất nền và thửa đất

Bắt buộc hỗ trợ:

* Số thửa.
* Số tờ bản đồ.
* Mã lô.
* Diện tích pháp lý.
* Diện tích thực tế.
* Diện tích sử dụng riêng.
* Diện tích sử dụng chung.
* Mục đích sử dụng đất.
* Thời hạn sử dụng.
* Nguồn gốc sử dụng.
* Mặt tiền.
* Chiều sâu.
* Hình dạng.
* Đường tiếp cận.
* Lộ giới.
* Hạ tầng.
* Quy hoạch.
* Chỉ giới xây dựng.
* Mật độ xây dựng.
* Khả năng tách thửa.
* Hạn chế chuyển nhượng.
* Thế chấp.
* Tranh chấp.
* Tài sản gắn liền với đất.
* Tọa độ polygon nếu có.

---

# 24. Asset Identity và chống tạo tài sản trùng

## 24.1. Trong dự án

Khóa nhận diện có thể dựa trên:

* Project.
* Hierarchy.
* Unit/plot code.
* External source ID.

## 24.2. Tài sản riêng lẻ

Có thể dựa trên:

* Country/province/district.
* Parcel number.
* Map sheet.
* Legal document.
* Địa chỉ chuẩn hóa.
* Tọa độ.
* Owner evidence.

## 24.3. Không auto-merge Asset chỉ bằng địa chỉ giống

Hai căn trong cùng địa chỉ có thể khác nhau.

## 24.4. Asset duplicate candidate

Hệ thống tạo candidate khi:

* Cùng Project + Unit code.
* Cùng parcel/map sheet trong cùng địa giới.
* Cùng external asset ID.
* Cùng legal certificate identifier.
* Import trùng.

## 24.5. Asset merge

Phải qua workflow riêng, không dùng Customer merge.

---

# 25. Asset Verification

## 25.1. Nguồn

* Declared Asset từ Customer 360 Capability.
* Import dự án.
* Partner feed.
* CRM Admin.
* Inventory team.
* Survey.

## 25.2. Trạng thái

```text
DRAFT
DECLARED
PENDING_DOCUMENTS
UNDER_VERIFICATION
VERIFIED
VERIFIED_WITH_CONDITIONS
REJECTED
SUSPENDED
ARCHIVED
```

## 25.3. Nội dung xác minh

* Asset tồn tại.
* Vị trí.
* Đặc điểm.
* Chủ sở hữu.
* Hồ sơ pháp lý.
* Hạn chế.
* Tình trạng thực tế.
* Trùng Asset.
* Quyền giao dịch.

## 25.4. Sale không tự xác minh Asset pháp lý

Sale có thể thu thập dữ liệu.

Inventory, Legal hoặc Data Steward mới xác minh theo capability.

---

# 26. Ownership

## 26.1. Khái niệm

Ownership mô tả Party nào sở hữu hoặc có quyền hợp pháp đối với Asset trong một khoảng thời gian.

## 26.2. Một Asset có thể có

* Một owner.
* Nhiều co-owner.
* Owner tổ chức.
* Owner cá nhân.
* Legal owner.
* Beneficial owner.
* Declarant.
* Authorized representative.

## 26.3. Ownership status

```text
DECLARED
DOCUMENT_RECEIVED
UNDER_VERIFICATION
VERIFIED
VERIFIED_WITH_CONDITIONS
DISPUTED
EXPIRED
TRANSFERRED
REJECTED
```

## 26.4. Ownership source

* Project developer record.
* Legal document.
* Contract.
* Customer declaration.
* Partner confirmation.
* External registry.
* Internal acquisition.

---

# 27. Ownership Record

Mỗi record gồm:

* Asset.
* Party.
* Customer nếu có.
* Ownership role.
* Ownership percentage.
* Declared percentage.
* Verified percentage.
* Effective from/to.
* Verification status.
* Legal basis.
* Document.
* Representative.
* Restrictions.
* Created by.
* Verified by.
* Approval.
* Status.

## 27.1. Tổng tỷ lệ

Đối với verified ownership có tỷ lệ:

* Tổng active verified percentage phải bằng 100%, trừ loại quyền không dùng tỷ lệ.
* Cho phép `unknown` khi đang xác minh.
* Không ép 100% ở trạng thái declared.

---

# 28. Ownership History

Khi tài sản chuyển chủ:

* Kết thúc record cũ.
* Tạo record mới.
* Không overwrite.
* Liên kết transaction hoặc document.
* Giữ lịch sử Listing và Contract cũ.

Thay owner không tự động đổi seller của Listing đang active.

Listing phải được review hoặc tạo version mới.

---

# 29. Co-owner

Mỗi co-owner có thể:

* Là Customer chính thức.
* Là Party.
* Là Related Party Stub trong giai đoạn thu thập.
* Có tỷ lệ.
* Có quyền ký.
* Có người đại diện.
* Có consent.

Listing không được active nếu policy yêu cầu toàn bộ co-owner đồng ý nhưng chưa đủ xác nhận.

---

# 30. Encumbrance và hạn chế tài sản

Các loại:

* Mortgage.
* Lien.
* Legal dispute.
* Seizure.
* Transfer restriction.
* Planning restriction.
* Co-owner dispute.
* Lease in force.
* Existing booking/contract.
* Other.

Mỗi encumbrance có:

* Type.
* Source.
* Description.
* Effective dates.
* Severity.
* Status.
* Evidence.
* Resolution.
* Blocking actions.

---

# 31. Asset Legal Readiness

Có thể tính:

```text
NOT_ASSESSED
INSUFFICIENT_DOCUMENTS
UNDER_REVIEW
ELIGIBLE_TO_MARKET
ELIGIBLE_TO_BOOK
ELIGIBLE_TO_CONTRACT
ELIGIBLE_WITH_CONDITIONS
NOT_ELIGIBLE
SUSPENDED
```

## 31.1. Không thay thế tư vấn pháp lý chính thức

Đây là trạng thái nghiệp vụ CRM dựa trên rule và review.

## 31.2. Explanation

Phải giải thích:

* Rule version.
* Tài liệu.
* Hạn chế.
* Người xác minh.
* Điều kiện còn thiếu.

---

# 32. Sales Mandate

## 32.1. Khái niệm

Sales Mandate xác định công ty có quyền thực hiện hoạt động nào đối với Asset hoặc Project.

## 32.2. Các loại

```text
DEVELOPER_RIGHT
OWNER_DIRECT_SALE
DISTRIBUTION_RIGHT
MASTER_AGENCY
BROKERAGE_MANDATE
CONSIGNMENT_MANDATE
MARKETING_ONLY
INTRODUCTION_ONLY
PAYMENT_COLLECTION_AUTHORITY
BOOKING_COLLECTION_AUTHORITY
NEGOTIATION_AUTHORITY
OTHER
```

## 32.3. Mandate không phải Listing

Mandate là căn cứ quyền.

Listing là sản phẩm thương mại được phát hành dựa trên mandate.

---

# 33. Nội dung Mandate

* Mandate code.
* Grantor Party.
* Grantee Legal Entity.
* Mandate type.
* Project scope.
* Asset scope.
* Listing scope.
* Territory.
* Channel.
* Customer segment.
* Exclusivity.
* Marketing right.
* Proposal right.
* Negotiation right.
* Hold right.
* Booking right.
* Deposit collection right.
* Payment collection right.
* Contract signing right.
* Minimum price authority.
* Maximum discount authority.
* Revenue model.
* Fee model.
* Effective dates.
* Auto-renewal.
* Termination conditions.
* Documents.
* Verification.
* Status.

---

# 34. Mandate Scope

Có thể áp dụng cho:

* Toàn Project.
* Một phase.
* Một tower.
* Một danh sách Unit.
* Một Asset.
* Một vùng địa lý.
* Một kênh.
* Một nhóm Customer.
* Một Sales Launch.

Backend phải kiểm tra Asset/Listing nằm trong scope.

---

# 35. Độc quyền

## 35.1. Exclusive

Chỉ một mandate hoặc một nhóm được chỉ định có quyền thương mại trong scope.

## 35.2. Non-exclusive

Nhiều đơn vị có thể cùng bán.

## 35.3. Semi-exclusive

Độc quyền theo:

* Kênh.
* Khu vực.
* Customer segment.
* Thời gian.
* Asset subset.

## 35.4. Conflict

Hệ thống phải cảnh báo khi các mandate active chồng lấn trái điều kiện.

---

# 36. Trạng thái Mandate

```text
DRAFT
PENDING_DOCUMENTS
UNDER_REVIEW
PENDING_APPROVAL
ACTIVE
SUSPENDED
EXPIRED
TERMINATED
REVOKED
REJECTED
ARCHIVED
```

Listing không được active nếu mandate:

* Chưa active.
* Hết hạn.
* Bị suspend.
* Không bao phủ Asset.
* Không cho phép Marketing/bán theo action tương ứng.

---

# 37. Listing

## 37.1. Khái niệm

Listing là bản ghi thương mại xác định Asset đang được chào bán hoặc cho thuê theo một mandate cụ thể.

## 37.2. Một Asset có thể có nhiều Listing lịch sử

Nhưng số Listing active đồng thời phải tuân thủ:

* Exclusivity.
* Channel.
* Transaction model.
* Mandate.
* Anti-duplicate rule.

## 37.3. Listing Code

Cấp qua Numbering Engine.

---

# 38. Listing Type

```text
PRIMARY_SALE
RESALE
CONSIGNMENT_SALE
COMPANY_OWNED_SALE
PARTNER_ASSET_SALE
LAND_SALE
RENTAL
LEASE_OUT
PRE_LAUNCH
PRIVATE_LISTING
OFF_MARKET
```

---

# 39. Listing Source

* Project inventory.
* Partner feed.
* Customer Seller Objective.
* Company Asset Register.
* Manual verified entry.
* External integration.
* Approved historical import, khi có phạm vi riêng.

Listing phải giữ source reference và source version.

---

# 40. Bên sở hữu, bên bán và bên hưởng tiền

Listing phải phân biệt:

* Owner Party.
* Co-owner Parties.
* Seller Party.
* Legal Seller.
* Company Role.
* Payment Receiver.
* Revenue Beneficiary.
* Mandate Grantor.

Không mặc định Owner = Seller = Payment Receiver.

---

# 41. Thông tin Listing

* Listing code.
* Asset.
* Listing type.
* Transaction model.
* Mandate.
* Owner Parties.
* Seller Party.
* Internal Legal Entity.
* Sales Launch.
* Asking price.
* Minimum acceptable price.
* Currency.
* Negotiation range.
* Listing start/end.
* Exclusivity.
* Channel.
* Visibility.
* Marketing status.
* Availability status.
* Legal readiness.
* Commercial readiness.
* Responsible team.
* Listing manager.
* Source.
* External ID.
* Status.
* Version.

---

# 42. Listing Visibility

```text
PUBLIC
INTERNAL_ALL
INTERNAL_PROJECT
INTERNAL_TEAM
PRIVATE_NETWORK
MANAGEMENT_ONLY
OFF_MARKET
```

## 42.1. Public

Có thể hiển thị website/portal theo policy.

## 42.2. Internal Project

Chỉ user có Project Access.

## 42.3. Private Listing

Chỉ user có Listing Access hoặc Share Grant.

## 42.4. Không làm lộ Owner

Listing public không được mặc định hiển thị:

* Tên chủ tài sản.
* Phone.
* Legal document.
* Giá tối thiểu.
* Ghi chú nội bộ.
* Commission.
* Mandate details.

---

# 43. Listing Readiness

## 43.1. Commercial readiness

```text
NOT_READY
PENDING_PRICE
PENDING_POLICY
PENDING_MANDATE
PENDING_OWNER_CONFIRMATION
READY_TO_MARKET
READY_TO_HOLD
READY_TO_BOOK
READY_TO_CONTRACT
SUSPENDED
```

## 43.2. Các điều kiện có thể gồm

* Asset verified.
* Ownership đủ.
* Mandate active.
* Giá active.
* Policy active.
* Legal readiness.
* Media tối thiểu.
* Seller confirmation.
* Co-owner confirmation.
* Không có blocker.
* Inventory mapping hợp lệ.

## 43.3. Readiness phải có explanation

---

# 44. Candidate Listing lifecycle vocabulary — Context-specific, pending validation

> Exact states, transitions, guards và terminal semantics thuộc Product Context Implementation Pack và machine contracts.


```text
DRAFT
PENDING_VERIFICATION
PENDING_OWNER_CONFIRMATION
PENDING_APPROVAL
SCHEDULED
ACTIVE
TEMPORARILY_UNAVAILABLE
ON_HOLD
BOOKED
DEPOSITED
UNDER_CONTRACT
SOLD
WITHDRAWN
EXPIRED
SUSPENDED
CANCELLED
ARCHIVED
```

## 44.1. Canonical commercial group

* Preparation.
* Active Supply.
* Reserved.
* Transaction.
* Closed.
* Unavailable.

## 44.2. Workflow có thể khác theo Transaction Model

Listing ký gửi có thể cần owner confirmation.

Project listing có thể cần Sales Launch approval.

---

# 45. Kích hoạt Listing

Điều kiện tối thiểu:

1. Asset hợp lệ.
2. Không có Asset duplicate chưa giải quyết nghiêm trọng.
3. Ownership hoặc developer right phù hợp.
4. Mandate active.
5. Giá active.
6. Listing period hợp lệ.
7. Seller Party xác định.
8. Internal Legal Entity xác định.
9. Legal readiness đạt mức yêu cầu.
10. Không có commercial lock xung đột.
11. User có quyền.
12. Approval hoàn tất.

---

# 46. Listing hết hạn, gia hạn và rút bán

## 46.1. Hết hạn

Khi qua `listing_end_at`:

* Listing chuyển `EXPIRED`.
* Không cho tạo Hold mới.
* Lock hiện hữu xử lý theo policy.
* Gửi thông báo.
* Không tự tạo Listing mới.

## 46.2. Gia hạn

Cần:

* Owner/Partner confirmation.
* Mandate còn hiệu lực hoặc gia hạn.
* Giá/chính sách review.
* Effective date mới.
* Approval nếu cần.
* Version mới.

## 46.3. Owner rút bán

Chuyển `WITHDRAWN` qua workflow.

Phải kiểm tra:

* Active Hold.
* Booking.
* Deposit.
* Deal.
* Contract.
* Nghĩa vụ phí.

Không tự giải phóng mọi trạng thái mà không xử lý giao dịch đang tồn tại.

---

# 47. Listing Version

Bất kỳ thay đổi quan trọng nào phải tạo version:

* Giá chào.
* Giá tối thiểu.
* Seller.
* Owner scope.
* Mandate.
* Exclusivity.
* Thời hạn.
* Negotiation authority.
* Visibility.
* Payment flow.
* Sales terms.

Các thay đổi nhỏ như sửa mô tả có thể lưu history mà không tạo commercial version, tùy policy.

---

# 48. Inventory List – Bảng hàng

## 48.1. Khái niệm

Inventory List là tập hợp Listing hoặc Asset được phép bán trong một phạm vi cụ thể.

## 48.2. Bảng hàng có thể theo

* Project.
* Sales Launch.
* Legal Entity.
* Partner.
* Channel.
* Team.
* Branch.
* Campaign.
* Thời điểm.
* Customer segment.

## 48.3. Một Listing có thể xuất hiện trong nhiều bảng hàng

Nhưng availability vẫn dùng nguồn chung.

Không tạo bản sao Listing riêng cho từng bảng.

---

# 49. Inventory List Version

Mỗi bảng hàng phải có:

* Inventory list.
* Version.
* Effective from/to.
* Source.
* Imported file hash.
* Item count.
* Price list.
* Policy.
* Approval.
* Status.
* Reconciliation result.

Version mới không ghi đè version cũ.

---

# 50. Inventory Item

Mỗi item gồm:

* Inventory list version.
* Listing.
* Asset.
* Channel status.
* Allocation quantity nếu sản phẩm theo số lượng.
* External status.
* Internal status.
* Price reference.
* Policy reference.
* Sales Launch.
* Visibility.
* Effective dates.
* Source row.
* Mapping status.

---

# 51. Inventory Access

Dựa trên accepted IAM authorization contracts và security registries:

* Project Access.
* Sales Launch Access.
* Listing Access.
* Team assignment.
* Channel access.
* Field policy.

Một user có thể:

* Xem tổng số lượng.
* Xem Unit chi tiết.
* Xem giá bán.
* Không xem giá sàn.
* Được tạo Proposal.
* Không được tạo Hold.

---

# 52. Candidate status dimensions — Context-specific, pending validation

> Các vocabulary dưới đây bảo vệ việc tách dimensions, nhưng exact codes thuộc Product Context Pack và contracts.


## 52.1. Physical Status

```text
PLANNED
UNDER_CONSTRUCTION
STRUCTURE_COMPLETED
FINISHING
COMPLETED
HANDED_OVER
IN_USE
RENOVATING
DAMAGED
UNKNOWN
```

## 52.2. Legal Status

```text
NOT_VERIFIED
DOCUMENTS_INCOMPLETE
UNDER_REVIEW
ELIGIBLE
ELIGIBLE_WITH_CONDITIONS
RESTRICTED
MORTGAGED
DISPUTED
TRANSFER_RESTRICTED
SUSPENDED
```

## 52.3. Commercial Availability

```text
NOT_RELEASED
AVAILABLE
SOFT_HELD
HARD_HELD
BOOKING_PENDING
BOOKED
DEPOSIT_PENDING
DEPOSITED
CONTRACT_PENDING
CONTRACTED
SOLD
WITHDRAWN
BLOCKED
EXPIRED
UNKNOWN_EXTERNAL
```

## 52.4. Marketing Status

```text
NOT_PUBLISHED
READY_TO_PUBLISH
PUBLISHED
PAUSED
REMOVED
```

Không gộp bốn nhóm trên thành một trường.

---

# 53. Availability decision capability

> Exact result codes và calculation rules thuộc Product Context Pack. Product backend là authoritative decision boundary.


## 53.1. Mục tiêu

Tính trạng thái khả dụng thực tế tại thời điểm request.

## 53.2. Đầu vào

* Listing status.
* Listing period.
* Mandate.
* Asset legal blocker.
* Inventory item.
* External source status.
* Commercial lock.
* Booking.
* Deposit.
* Contract.
* User access.
* Sales Launch.
* Price/policy validity.
* Version.

## 53.3. Kết quả

```text
AVAILABLE
AVAILABLE_WITH_CONDITIONS
TEMPORARILY_LOCKED
UNAVAILABLE
EXTERNAL_CONFIRMATION_REQUIRED
UNKNOWN_REQUIRES_REFRESH
BLOCKED
```

## 53.4. Explanation

Phải trả:

* Kết quả.
* Lý do.
* Current lock.
* External status age.
* Price version.
* Listing version.
* Allowed actions.

---

# 54. Commercial Lock

> Exact lock taxonomy và lifecycle thuộc Product Context Pack. Mọi lock làm mất availability phải tuân database-backed concurrency invariant.


## 54.1. Khái niệm

Commercial Lock là khóa kỹ thuật/nghiệp vụ tạm thời ngăn sản phẩm được giữ hoặc bán bởi giao dịch khác.

## 54.2. Loại Lock

```text
SOFT_HOLD
HARD_HOLD
BOOKING_LOCK
DEPOSIT_LOCK
CONTRACT_LOCK
ADMIN_BLOCK
EXTERNAL_LOCK
RECONCILIATION_LOCK
```

## 54.3. Soft Hold

* Thời hạn ngắn.
* Có thể chỉ nội bộ.
* Có thể cần xác nhận nguồn ngoài.
* Không phải Booking.

## 54.4. Hard Hold

* Có phê duyệt hoặc điều kiện cao hơn.
* Khóa sản phẩm mạnh hơn.
* Có thời hạn.

## 54.5. Booking Lock

Được Product Context tạo hoặc chuyển đổi theo command hợp lệ từ Transaction Context khi Booking đạt điều kiện.

## 54.6. Admin Block

Dùng khi:

* Tranh chấp.
* Lỗi dữ liệu.
* Legal issue.
* Reconciliation.
* Owner yêu cầu dừng.

---

# 55. Nội dung Commercial Lock

* Lock ID.
* Listing.
* Asset.
* Lock type.
* Source Context.
* Source resource.
* Customer.
* Deal.
* User.
* Legal Entity.
* Started at.
* Expires at.
* Status.
* Priority.
* External confirmation.
* Idempotency key.
* Reason.
* Created by.
* Released by.
* Release reason.
* Version.

---

# 56. Candidate Commercial Lock lifecycle vocabulary — pending validation

> Exact statuses và transitions không được suy ra trực tiếp từ Capability Specification.


```text
REQUESTED
PENDING_EXTERNAL_CONFIRMATION
ACTIVE
EXTENSION_PENDING
CONVERTED
RELEASED
EXPIRED
REJECTED
CANCELLED
CONFLICTED
```

## 56.1. Lock hết hạn

Job có thể chuyển lock sang `EXPIRED`, nhưng phải:

* Dùng transaction.
* Kiểm tra chưa converted.
* Ghi event.
* Recalculate availability.

## 56.2. Không được gia hạn vô hạn

Policy quy định:

* Số lần gia hạn.
* Tổng thời gian.
* Approval.
* Lý do.
* Customer activity.

---

# 57. Chống bán trùng

## 57.1. System invariant

Tại một thời điểm, một Listing chỉ được có một active exclusive commercial lock thuộc nhóm làm mất khả dụng, trừ trường hợp policy cho phép waitlist không khóa.

## 57.2. Database enforcement

Khuyến nghị:

* Partial unique index theo `listing_id` và nhóm lock active.
* Transaction.
* Row-level lock.
* Optimistic version.
* Idempotency key.

## 57.3. Hai request đồng thời

Quy trình:

1. Request A và B cùng kiểm tra.
2. Database lock Listing.
3. Request A tạo lock thành công.
4. Request B phát hiện conflict.
5. Request B nhận `LISTING_LOCK_CONFLICT`.
6. Không tạo hai lock.

## 57.4. Không dùng cache làm nguồn duy nhất

Cache có thể hỗ trợ đọc nhưng database hoặc authoritative lock service là nguồn chuẩn.

---

# 58. Lock Priority

Có thể cấu hình:

```text
CONTRACT_LOCK
> DEPOSIT_LOCK
> BOOKING_LOCK
> HARD_HOLD
> SOFT_HOLD
```

Priority không cho phép lock mới chiếm lock cũ tùy ý.

Preemption chỉ được thực hiện qua workflow đặc biệt và approval.

---

# 59. Waitlist

Có thể cho phép nhiều Customer vào waitlist mà không khóa Listing.

Waitlist gồm:

* Customer.
* Requirement.
* Deal.
* Priority.
* Created at.
* Consent.
* Status.

Waitlist không được hiển thị là “đã giữ”.

---

# 60. External Inventory observations và Integration boundary

> Integration Context sở hữu provider connection, authentication, raw transport, retry/DLQ và provider-specific mapping. Product Context chỉ nhận accepted observations/references và quyết định Product-side availability/reconciliation.


## 60.1. Nguồn

* API chủ đầu tư.
* File Excel.
* Portal.
* Email file.
* Partner webhook.
* Manual confirmation.

## 60.2. External status không được ghi đè lịch sử nội bộ

Lưu:

* External source.
* External Asset ID.
* External Listing ID.
* External status.
* Observed at.
* Effective at.
* Source payload.
* Mapping.
* Confidence.

## 60.3. Staleness

Nếu trạng thái ngoài quá cũ:

```text
UNKNOWN_REQUIRES_REFRESH
```

Không tự coi là available.

---

# 61. External Inventory Mapping

Mapping gồm:

* External Project ID.
* External Unit ID.
* Internal Project.
* Internal Asset.
* Internal Listing.
* Source status mapping.
* Source price mapping.
* Version.
* Confidence.
* Status.

Mapping không chắc chắn phải manual review.

---

# 62. Đồng bộ kho qua Integration ACL

> Sync runtime thuộc Integration/Operations. Product xử lý canonical Product commands/facts; không nhận raw provider writes vào Product schema.


## 62.1. Quy trình

1. Nhận payload/file.
2. Authenticate source.
3. Validate schema.
4. Idempotency.
5. Map Project.
6. Map Asset.
7. Map Listing.
8. So sánh trạng thái.
9. So sánh giá.
10. Phát hiện conflict.
11. Dry run nếu batch.
12. Apply.
13. Reconciliation.
14. Alert.

## 62.2. Không tự hủy Booking nội bộ

Nếu nguồn ngoài báo sản phẩm không còn:

* Chuyển `RECONCILIATION_REQUIRED`.
* Block new hold.
* Thông báo.
* Kiểm tra Booking/Deal.
* Xử lý theo workflow.

---

# 63. Inventory Reconciliation

So sánh:

* Internal availability.
* External availability.
* Active locks.
* Booking.
* Deposit.
* Contract.
* Source timestamp.
* Price.
* Policy.

Kết quả:

```text
MATCHED
INTERNAL_AHEAD
EXTERNAL_AHEAD
STATUS_CONFLICT
PRICE_CONFLICT
MAPPING_CONFLICT
MISSING_INTERNAL
MISSING_EXTERNAL
REQUIRES_MANUAL_REVIEW
```

---

# 64. Giá

## 64.1. Các khái niệm

* Base price.
* Sales price.
* Asking price.
* Minimum acceptable price.
* Floor price.
* Promotional price.
* Net price.
* Gross price.
* Price per area.
* Owner net expectation.
* Company margin.
* Negotiated price.

Không phải user nào cũng được xem tất cả.

---

# 65. Price List

Price List là tập hợp giá theo:

* Project.
* Sales Launch.
* Asset group.
* Listing.
* Channel.
* Legal Entity.
* Customer segment.
* Effective period.

Một Project có thể có nhiều Price List.

---

# 66. Price List Version

Mỗi version gồm:

* Version code.
* Price list.
* Effective from/to.
* Currency.
* Tax inclusion.
* Rounding rule.
* Source.
* Approval.
* Status.
* Replaces version.
* Item count.
* Imported file hash.

Không sửa active version trực tiếp.

---

# 67. Price Item

Mỗi Price Item gồm:

* Asset/Listing.
* Base amount.
* Area basis.
* Price per unit.
* Price per square meter.
* Gross amount.
* Tax amount.
* Maintenance fee.
* Other fees.
* Currency.
* Rounding.
* Effective dates.
* Status.

---

# 68. Price Component

Có thể gồm:

* Land value.
* Construction value.
* VAT.
* Maintenance fee.
* Infrastructure fee.
* Furniture package.
* Parking.
* Service fee.
* Registration-related estimate.
* Other.

Price Component phải phân biệt:

* Bắt buộc.
* Tùy chọn.
* Được chiết khấu.
* Không được chiết khấu.
* Thu hộ.
* Doanh thu.
* Không phải doanh thu.

Price component chỉ mô tả Product-side commercial nature; Contract và Revenue Contexts sở hữu downstream cash/revenue interpretation.

---

# 69. Asking Price và Floor Price

## 69.1. Asking Price

Giá chào Customer.

## 69.2. Minimum Acceptable Price

Mức chủ tài sản hoặc công ty có thể xem xét.

## 69.3. Floor Price

Giá sàn nội bộ.

Quyền xem Floor Price phải hạn chế.

## 69.4. Seller-owned Listing

Cần tách:

* Owner asking price.
* Owner net expectation.
* Public asking price.
* Company fee.
* Negotiation authority.

---

# 70. Giá và quyền đàm phán

Mandate hoặc Listing Policy phải xác định:

* Sale có được đàm phán không.
* Biên độ.
* Ai duyệt.
* Giá nào cần owner confirmation.
* Giá nào cần Director approval.
* Giá nào làm thay đổi phí môi giới.

Product Context cung cấp Product-side price/policy facts; Transaction Context quản lý negotiation, còn Contract/Revenue Contexts quyết định downstream financial meaning.

Deal and Transaction Capability quản lý đề nghị giảm giá hoặc negotiation request.

---

# 71. Thuế, phí và cách hiển thị

Mỗi giá phải xác định:

* Đã gồm VAT hay chưa.
* Đã gồm phí bảo trì hay chưa.
* Đã gồm phí môi giới hay chưa.
* Đã gồm phí chuyển nhượng hay chưa.
* Ai chịu thuế/phí.
* Khoản nào chỉ là ước tính.

Không cho sale tự nhập một tổng giá không rõ cấu phần.

---

# 72. Tiền tệ và làm tròn

* Dùng decimal.
* Currency bắt buộc.
* Rounding rule lấy từ Platform Configuration Capability.
* Không dùng floating point.
* Giá theo m² và tổng giá phải xác định nguồn.
* Tỷ giá phải snapshot nếu đa tiền tệ.

---

# 73. Sales Policy

## 73.1. Khái niệm

Sales Policy là tập hợp điều kiện bán hàng áp dụng cho Listing hoặc nhóm Listing.

## 73.2. Có thể gồm

* Chiết khấu.
* Quà tặng.
* Hỗ trợ lãi suất.
* Lịch thanh toán.
* Điều kiện vay.
* Phí ưu đãi.
* Chính sách khách hàng cũ.
* Chính sách mua nhiều.
* Chính sách đại lý.
* Chính sách thanh toán sớm.
* Chính sách giới thiệu.
* Hạn sử dụng.
* Đối tượng áp dụng.

## 73.3. Policy không tự áp dụng mọi Customer

Phải kiểm tra eligibility.

---

# 74. Policy Eligibility

Có thể dựa trên:

* Customer segment.
* Sales Launch.
* Project.
* Listing.
* Payment method.
* Booking date.
* Contract date.
* Quantity.
* Existing Customer.
* Employee.
* Channel.
* Legal Entity.
* Approval.

## 74.1. Không dùng dữ liệu nhạy cảm không liên quan

Eligibility không được dựa vào thuộc tính cá nhân nhạy cảm không phục vụ nghiệp vụ hợp lệ.

---

# 75. Sales Policy Version

Mỗi version gồm:

* Policy code.
* Version.
* Scope.
* Conditions.
* Benefits.
* Effective dates.
* Stacking rules.
* Approval.
* Status.
* Replaces version.

## 75.1. Stacking

Phải xác định:

* Có được cộng nhiều ưu đãi không.
* Thứ tự áp dụng.
* Trần.
* Loại trừ.
* Funding source.

---

# 76. Snapshot giá và chính sách

Khi Matching, Deal and Transaction, cùng Contract and Cash Capabilities sử dụng dữ liệu, phải snapshot:

* Listing version.
* Price list version.
* Price item.
* Sales Policy version.
* Mandate version.
* Availability at time.
* Tax/fee rule.
* Currency.
* Rounding.

Sau đó giá/policy mới không đổi snapshot cũ.

---

# 77. Media và nội dung Marketing

## 77.1. Loại media

* Ảnh.
* Video.
* Floor plan.
* Master plan.
* Virtual tour.
* Map.
* Brochure.
* Render.
* Actual photo.

## 77.2. Metadata

* Asset/Project/Listing.
* Media type.
* URL.
* Provider.
* Copyright/usage rights.
* Visibility.
* Order.
* Verification.
* Effective dates.
* Expiry.
* Watermark policy.

## 77.3. Không dùng media khi hết quyền

Media có thể bị ngừng sử dụng khi:

* Listing hết hạn.
* Mandate kết thúc.
* Owner rút quyền.
* Bản quyền hết hạn.

---

# 78. Tài liệu pháp lý và hồ sơ ngoài hệ thống

Capability lưu metadata:

* Document type.
* Project/Asset/Ownership/Mandate/Listing.
* Title.
* URL.
* Storage provider.
* Document hash.
* Issuer.
* Issue date.
* Expiry.
* Verification.
* Access policy.
* Legal hold.
* Version.

Binary files phải được quản lý bởi Documents Context và approved Object Storage; Product chỉ giữ Document references và Product-side metadata.

---

# 79. Vị trí và dữ liệu địa lý

## 79.1. Project/Asset Geography

* Country.
* Province.
* District.
* Ward.
* Address.
* Coordinates.
* Polygon.
* Road.
* Landmark.
* Region tags.

## 79.2. Geocoding

Kết quả geocode phải lưu:

* Provider.
* Confidence.
* Timestamp.
* Manual correction.
* Version.

## 79.3. Không ghi đè địa chỉ pháp lý bằng địa chỉ Marketing

Tách:

* Legal address.
* Display address.
* Marketing location.
* Exact private location.

## 79.4. Listing riêng tư

Có thể chỉ hiển thị khu vực gần đúng, không hiển thị địa chỉ chính xác.

---

# 80. Bảo mật chủ tài sản và Partner

## 80.1. Sale Buyer-side có thể xem

* Thông tin Listing.
* Giá.
* Đặc điểm.
* Điều kiện giao dịch.

Không mặc định xem:

* Tên Owner.
* Phone Owner.
* Giá net Owner.
* Hợp đồng ký gửi.
* Phí môi giới.
* Legal document.

## 80.2. Seller-side team

Có thể xem Owner Profile theo context.

## 80.3. Finance/Legal

Chỉ xem khi có nhiệm vụ.

## 80.4. Public Listing

Không chứa dữ liệu chủ tài sản nếu chưa có consent.

---

# 81. Project và Listing Access

Dùng authorization contracts và registries do IAM/Security governance quản lý.

## 81.1. Cấp Project Access

Có thể cho phép:

* View Project.
* View inventory.
* View public price.
* View floor price.
* Create Proposal.
* Request Hold.
* Manage inventory.
* Approve status.
* Import.

## 81.2. Listing Access

Dùng cho:

* Private Listing.
* Seller-owned Listing.
* VIP Listing.
* Off-market Asset.

## 81.3. Project Access không tự mở Owner Profile

---

# 82. Export bảng hàng

## 82.1. Sale

Không được export toàn bảng hàng.

Có thể:

* Tạo Proposal giới hạn.
* Tạo PDF một số Listing.
* Tạo link có thời hạn.

## 82.2. Team Lead và Department Head

Không mặc định được bulk export.

## 82.3. Inventory Manager

Có thể export vận hành theo scope.

## 82.4. Director

Export có approval/audit theo policy.

## 82.5. Dữ liệu không được xuất cho sale

* Giá sàn.
* Owner contact.
* Margin.
* Full inventory.
* Internal notes.
* Commission.
* Mandate terms nhạy cảm.

---

# 83. Import Project và Inventory

## 83.1. Dữ liệu import

* Project.
* Hierarchy.
* Asset.
* Unit/Plot.
* Ownership.
* Listing.
* Inventory.
* Price.
* Policy.
* External mapping.

## 83.2. Quy trình

1. Upload.
2. Xác định source.
3. Mapping.
4. Validate.
5. Project duplicate check.
6. Asset duplicate check.
7. Partner check.
8. Price validation.
9. Policy validation.
10. Preview.
11. Dry run.
12. Approval.
13. Import.
14. Reconciliation.
15. Error report.

## 83.3. Không bỏ qua invariant

Import vẫn phải:

* Chống Asset trùng.
* Chống Listing trái mandate.
* Chống active price conflict.
* Chống availability conflict.
* Giữ version.
* Ghi source row.

---

# 84. Import bảng giá

Mỗi file import phải tạo Price List Version mới.

Không update trực tiếp giá từng Unit active mà không version.

Lưu:

* File hash.
* Sheet.
* Row.
* Mapping.
* Error.
* Approver.
* Effective date.

---

# 85. Kiểm soát dữ liệu source

Mỗi Asset/Listing có thể có:

* Source of truth.
* Source confidence.
* Last verified at.
* Source priority.
* Manual override.
* Override reason.
* Override expiry.

Manual override không xóa dữ liệu nguồn.

---

# 86. Workflow chính

Capability cần các workflow:

* Partner verification.
* Project creation.
* Project activation.
* Asset verification.
* Ownership verification.
* Mandate review.
* Listing creation.
* Listing activation.
* Listing renewal.
* Listing withdrawal.
* Price list approval.
* Policy approval.
* Inventory import.
* Availability override.
* Admin block.
* Reconciliation conflict.
* Asset merge.
* Project archive.

Tất cả dùng versioned Platform workflow definitions, nhưng owning Product aggregate vẫn thực thi transition và bảo vệ invariants.

---

# 87. SLA

## 87.1. Các SLA

* Partner verification.
* Project setup.
* Asset verification.
* Ownership review.
* Legal document review.
* Mandate approval.
* Listing activation.
* Price list approval.
* Policy approval.
* Inventory sync.
* Reconciliation.
* Lock confirmation.
* Owner confirmation.
* Listing renewal.
* Conflict resolution.

## 87.2. Giá trị khởi tạo tham khảo

| Nghiệp vụ                           |       SLA tham khảo |
| ----------------------------------- | ------------------: |
| Asset duplicate check               |            Tức thời |
| Project inventory import validation |         Trong 2 giờ |
| Ownership preliminary review        |     1 ngày làm việc |
| Listing activation review           |     1 ngày làm việc |
| External hold confirmation          |           5–30 phút |
| Inventory reconciliation conflict   |         Trong 2 giờ |
| Price list approval                 | Trong ngày làm việc |
| Listing expiry review               |        Trước 3 ngày |

Tất cả phải cấu hình.

## 87.3. Quá SLA

Có thể:

* Nhắc.
* Escalate.
* Block Listing.
* Chuyển reviewer.
* Đưa dashboard.

Không tự:

* Xác minh ownership.
* Kích hoạt Listing.
* Thay giá.
* Mở khóa.
* Hủy Booking.

---

# 88. Notification

## 88.1. Inventory team

* Asset cần xác minh.
* Import lỗi.
* Inventory conflict.
* Listing sắp hết hạn.
* Price sắp hết hiệu lực.
* External mapping lỗi.
* Lock bất thường.

## 88.2. Sale

* Listing available.
* Listing bị lock.
* Giá thay đổi.
* Policy thay đổi.
* Listing hết hạn.
* Hold bị từ chối.
* External confirmation pending.
* Sản phẩm được giải phóng.

## 88.3. Team Lead

* Không có sản phẩm phù hợp.
* Lock quá lâu.
* Listing conflict.
* Sale cố giữ ngoài quyền.
* Inventory stale.

## 88.4. Owner/Partner

Có thể gửi theo consent:

* Yêu cầu xác nhận Listing.
* Gia hạn.
* Giá.
* Offer.
* Withdrawal.

## 88.5. Legal/Finance

* Ownership conflict.
* Mandate hết hạn.
* Payment flow thay đổi.
* Contract-linked Listing conflict.

---

# 89. Candidate user experiences — không phải frontend contract canonical

> Exact routes, screen composition, components và responsive behavior thuộc Navigation/IA, Design System và Current Sprint Pack.


## 89.1. Partner Center

* Partner.
* Type.
* Verification.
* Agreements.
* Projects.
* Mandates.
* Contacts.
* Risk.
* Documents.
* Audit.

## 89.2. Project List

* Project.
* Developer.
* Internal Legal Entity.
* Transaction model.
* Stage.
* Legal status.
* Sales status.
* Inventory count.
* Active launches.

## 89.3. Project 360

Các tab:

1. Overview.
2. Parties.
3. Hierarchy.
4. Sales Launches.
5. Assets.
6. Inventory.
7. Prices.
8. Policies.
9. Mandates.
10. Legal.
11. Media.
12. Integrations.
13. Reconciliation.
14. Audit.

## 89.4. Asset Detail

* Identity.
* Location.
* Characteristics.
* Physical status.
* Legal status.
* Ownership.
* Encumbrance.
* Listings.
* Price history.
* Documents.
* Media.
* Timeline.
* Audit.

## 89.5. Ownership Workspace

* Owners.
* Percentages.
* Verification.
* Documents.
* Representatives.
* Encumbrances.
* History.

## 89.6. Mandate Center

* Grantor.
* Grantee.
* Scope.
* Rights.
* Exclusivity.
* Dates.
* Status.
* Revenue/payment flow.
* Documents.
* Conflicts.

## 89.7. Listing Workspace

* Asset.
* Seller/Owner.
* Mandate.
* Listing terms.
* Price.
* Policy.
* Availability.
* Lock.
* Visibility.
* Media.
* Access.
* History.

## 89.8. Inventory Board

Hiển thị dạng bảng:

* Unit/Plot.
* Type.
* Area.
* Price.
* Policy.
* Availability.
* Lock.
* Sale/Deal context theo quyền.
* Last synced.
* External status.

## 89.9. Price Center

* Price lists.
* Versions.
* Effective dates.
* Comparison.
* Import.
* Approval.
* Price history.

## 89.10. Policy Center

* Policy.
* Scope.
* Eligibility.
* Benefits.
* Stacking.
* Funding source.
* Effective dates.
* Approval.

## 89.11. Lock Monitor

* Listing.
* Lock type.
* Deal.
* Customer.
* User.
* Age.
* Expiry.
* External status.
* Conflict.
* Release.

## 89.12. Reconciliation Center

* Source.
* Project.
* Conflicts.
* Price mismatch.
* Status mismatch.
* Mapping.
* SLA.
* Resolution.

---

# 90. Dashboard cho Sale

* Listing mới.
* Listing phù hợp Project Access.
* Available inventory.
* Listing sắp hết hạn.
* Giá mới.
* Policy mới.
* Hold của mình.
* Hold sắp hết hạn.
* Sản phẩm vừa được giải phóng.
* Listing đã xem gần đây.
* Private Listing được chia sẻ.

---

# 91. Dashboard cho Team Lead

* Inventory theo team.
* Available/held/booked.
* Lock aging.
* Hold conversion.
* Listing stale.
* Project access gap.
* Price/policy changes.
* External confirmation delay.
* Inventory conflict.
* Sale hold rejection.

---

# 92. Dashboard cho Inventory Manager

* Tổng Asset.
* Verified/unverified.
* Active Listing.
* Listing sắp hết hạn.
* Mandate sắp hết hạn.
* Import status.
* External sync health.
* Reconciliation conflicts.
* Price versions.
* Lock conflicts.
* Asset duplicates.
* Ownership incomplete.

---

# 93. Dashboard cho Director

* Nguồn cung theo mô hình.
* Tài sản công ty.
* Dự án tự phát triển.
* Dự án phân phối.
* Ký gửi.
* Available inventory.
* Inventory value.
* Absorption.
* Aging.
* Price trend.
* Listing expiry.
* Mandate coverage.
* Ownership/legal risk.
* Supply-demand gap.
* External source risk.
* Double-sale prevention metrics.

---

# 94. Candidate analytical questions — không phải certified Metrics

> Exact definitions, formulas, grain, dimensions, access và certification thuộc Analytics Metric Registry và Analytics Context Pack.


* Partner.
* Developer.
* Project.
* Project Party Role.
* Project stage.
* Sales Launch.
* Asset count.
* Asset type.
* Asset verification.
* Asset duplicate.
* Ownership.
* Co-owner.
* Ownership verification.
* Encumbrance.
* Legal readiness.
* Mandate.
* Mandate expiry.
* Mandate conflict.
* Listing.
* Listing source.
* Listing type.
* Listing aging.
* Listing expiry.
* Listing withdrawal.
* Inventory list.
* Inventory version.
* Available/held/booked/sold.
* Lock.
* Lock expiry.
* Lock conflict.
* Price list.
* Price change.
* Floor price access.
* Policy.
* Incentive.
* External sync.
* Reconciliation.
* Data freshness.
* Project access.
* Listing access.
* Inventory export.
* Public Listing.
* Private Listing.
* Owner/Customer-supplied inventory.
* Company-owned assets.
* Third-party distribution inventory.
* Land plot inventory.
* Supply by geography.
* Supply by budget range.
* Supply by property type.

Mọi báo cáo phải drill-down đúng scope.

---

# 95. Candidate data model — không phải physical schema canonical

> **Classification:** `CONTEXT-SPECIFIC DESIGN INPUT / PENDING VALIDATION`  
> Exact tables, columns, constraints, indexes và ownership chỉ có hiệu lực khi được khóa trong Product Context DB Specification và Alembic migrations.


## 95.1. Partner Profile

### `partner_profiles`

* `id`
* `party_id`
* `partner_code`
* `partner_status`
* `verification_status`
* `risk_status`
* `primary_legal_entity_id`
* `effective_from`
* `effective_to`
* `created_at`
* `updated_at`

### `partner_types`

* `id`
* `partner_profile_id`
* `partner_type_code`
* `effective_from`
* `effective_to`
* `status`
* `created_at`

### `partner_relationships`

* `id`
* `partner_profile_id`
* `internal_legal_entity_id`
* `relationship_type`
* `agreement_reference`
* `territory_json`
* `channel_json`
* `effective_from`
* `effective_to`
* `status`
* `created_at`

---

## 95.2. Project

### `projects`

* `id`
* `project_code`
* `project_name`
* `trade_name`
* `project_type`
* `asset_origin`
* `transaction_model`
* `primary_developer_party_id`
* `internal_legal_entity_id`
* `seller_legal_entity_id`
* `payment_collector_party_id`
* `revenue_beneficiary_party_id`
* `country_code`
* `province_code`
* `district_code`
* `ward_code`
* `address_text`
* `latitude`
* `longitude`
* `total_area`
* `total_units`
* `development_stage`
* `legal_status`
* `sales_status`
* `construction_status`
* `expected_launch_at`
* `expected_handover_at`
* `status`
* `created_at`
* `updated_at`
* `version`

### `project_parties`

* `id`
* `project_id`
* `party_id`
* `project_role_code`
* `agreement_reference`
* `effective_from`
* `effective_to`
* `verification_status`
* `status`
* `created_at`

### `project_hierarchy_nodes`

* `id`
* `project_id`
* `parent_node_id`
* `node_type`
* `node_code`
* `name`
* `display_order`
* `effective_from`
* `effective_to`
* `status`
* `created_at`

---

## 95.3. Sales Launch

### `sales_launches`

* `id`
* `launch_code`
* `project_id`
* `name`
* `internal_legal_entity_id`
* `partner_id`
* `channel_code`
* `payment_flow_model`
* `start_at`
* `end_at`
* `status`
* `workflow_version`
* `created_by`
* `approved_by`
* `created_at`

### `sales_launch_scopes`

* `id`
* `sales_launch_id`
* `scope_type`
* `scope_id`
* `created_at`

---

## 95.4. Property Asset

### `property_assets`

* `id`
* `asset_code`
* `project_id`
* `hierarchy_node_id`
* `asset_type`
* `asset_origin`
* `name`
* `unit_number`
* `plot_number`
* `floor_number`
* `country_code`
* `province_code`
* `district_code`
* `ward_code`
* `address_text`
* `latitude`
* `longitude`
* `gross_area`
* `net_area`
* `land_area`
* `construction_area`
* `frontage`
* `depth`
* `bedrooms`
* `bathrooms`
* `orientation_code`
* `view_code`
* `physical_status`
* `legal_status`
* `verification_status`
* `status`
* `created_from_type`
* `created_from_id`
* `created_at`
* `updated_at`
* `version`

### `property_asset_land_details`

* `asset_id`
* `parcel_number`
* `map_sheet_number`
* `legal_area`
* `actual_area`
* `private_use_area`
* `common_use_area`
* `land_use_purpose`
* `land_use_term`
* `land_use_origin`
* `road_width`
* `planning_summary`
* `building_line`
* `construction_density`
* `subdivision_eligibility`
* `transfer_restriction_summary`
* `geometry_json`
* `updated_at`

### `property_asset_unit_details`

* `asset_id`
* `unit_type`
* `balcony_orientation`
* `door_orientation`
* `handover_standard`
* `furnishing_status`
* `management_fee`
* `parking_rights_json`
* `updated_at`

---

## 95.5. Asset Duplicate

### `property_asset_duplicate_candidates`

* `id`
* `asset_a_id`
* `asset_b_id`
* `match_type`
* `match_details_json`
* `risk_level`
* `status`
* `created_at`
* `resolved_at`

---

## 95.6. Ownership

### `property_ownership_records`

* `id`
* `asset_id`
* `party_id`
* `customer_id`
* `ownership_role_code`
* `declared_percentage`
* `verified_percentage`
* `verification_status`
* `legal_basis_type`
* `legal_basis_reference`
* `representative_party_id`
* `effective_from`
* `effective_to`
* `status`
* `created_by`
* `verified_by`
* `approved_by`
* `created_at`
* `updated_at`

### `property_ownership_history`

* `id`
* `ownership_record_id`
* `event_type`
* `before_snapshot`
* `after_snapshot`
* `reason`
* `source_resource_type`
* `source_resource_id`
* `actor_user_id`
* `created_at`

### `property_encumbrances`

* `id`
* `asset_id`
* `encumbrance_type`
* `severity`
* `description`
* `source_type`
* `source_id`
* `effective_from`
* `effective_to`
* `blocking_actions_json`
* `status`
* `created_by`
* `verified_by`
* `created_at`

---

## 95.7. Asset Verification

### `asset_verification_cases`

* `id`
* `verification_code`
* `asset_id`
* `declared_asset_id`
* `verification_type`
* `assigned_user_id`
* `status`
* `due_at`
* `result`
* `conditions_json`
* `created_by`
* `reviewed_by`
* `approved_by`
* `created_at`
* `completed_at`

---

## 95.8. Mandate

### `sales_mandates`

* `id`
* `mandate_code`
* `mandate_type`
* `grantor_party_id`
* `grantee_legal_entity_id`
* `project_id`
* `exclusivity_type`
* `marketing_right`
* `proposal_right`
* `negotiation_right`
* `hold_right`
* `booking_right`
* `deposit_collection_right`
* `payment_collection_right`
* `contract_signing_right`
* `minimum_price_authority`
* `maximum_discount_authority`
* `revenue_model`
* `payment_flow_model`
* `effective_from`
* `effective_to`
* `auto_renewal`
* `verification_status`
* `status`
* `created_by`
* `reviewed_by`
* `approved_by`
* `created_at`
* `version`

### `sales_mandate_scopes`

* `id`
* `sales_mandate_id`
* `scope_type`
* `scope_id`
* `territory_json`
* `channel_json`
* `customer_segment_json`
* `created_at`

### `sales_mandate_documents`

* `id`
* `sales_mandate_id`
* `document_type`
* `document_id`
* `document_hash`
* `effective_from`
* `expires_at`
* `verification_status`
* `created_at`

---

## 95.9. Listing

### `property_listings`

* `id`
* `listing_code`
* `asset_id`
* `listing_type`
* `transaction_model`
* `sales_mandate_id`
* `sales_launch_id`
* `internal_legal_entity_id`
* `seller_party_id`
* `payment_receiver_party_id`
* `revenue_beneficiary_party_id`
* `currency`
* `asking_price`
* `minimum_acceptable_price`
* `visibility`
* `marketing_status`
* `availability_status`
* `commercial_readiness_status`
* `legal_readiness_status`
* `listing_start_at`
* `listing_end_at`
* `responsible_team_id`
* `listing_manager_user_id`
* `source_type`
* `source_id`
* `external_listing_id`
* `status`
* `created_at`
* `updated_at`
* `version`

### `property_listing_parties`

* `id`
* `listing_id`
* `party_id`
* `customer_id`
* `listing_party_role`
* `ownership_percentage_snapshot`
* `verification_status`
* `status`
* `created_at`

### `property_listing_versions`

* `id`
* `listing_id`
* `version`
* `snapshot_json`
* `change_type`
* `change_reason`
* `effective_from`
* `effective_to`
* `created_by`
* `approved_by`
* `created_at`

### `property_listing_status_history`

* `id`
* `listing_id`
* `from_status`
* `to_status`
* `action_code`
* `reason`
* `actor_user_id`
* `source_resource_type`
* `source_resource_id`
* `created_at`

---

## 95.10. Inventory

### `inventory_lists`

* `id`
* `inventory_code`
* `name`
* `project_id`
* `sales_launch_id`
* `internal_legal_entity_id`
* `partner_id`
* `channel_code`
* `scope_type`
* `scope_id`
* `status`
* `created_at`

### `inventory_list_versions`

* `id`
* `inventory_list_id`
* `version`
* `source_type`
* `source_reference`
* `source_file_hash`
* `effective_from`
* `effective_to`
* `item_count`
* `price_list_version_id`
* `sales_policy_version_id`
* `reconciliation_status`
* `status`
* `created_by`
* `approved_by`
* `created_at`

### `inventory_items`

* `id`
* `inventory_list_version_id`
* `listing_id`
* `asset_id`
* `channel_status`
* `external_status`
* `internal_status`
* `price_item_id`
* `policy_version_id`
* `effective_from`
* `effective_to`
* `source_row_reference`
* `mapping_status`
* `created_at`

---

## 95.11. Availability

### `listing_availability_snapshots`

* `id`
* `listing_id`
* `availability_result`
* `reason_codes_json`
* `listing_version`
* `price_version`
* `policy_version`
* `external_status_at`
* `calculated_at`
* `calculation_version`

### `commercial_locks`

* `id`
* `listing_id`
* `asset_id`
* `lock_type`
* `source_context`
* `source_resource_type`
* `source_resource_id`
* `customer_id`
* `deal_id`
* `user_id`
* `legal_entity_id`
* `priority`
* `started_at`
* `expires_at`
* `external_confirmation_status`
* `status`
* `idempotency_key`
* `reason`
* `created_by`
* `released_by`
* `released_at`
* `release_reason`
* `created_at`
* `version`

### `commercial_lock_events`

* `id`
* `commercial_lock_id`
* `event_type`
* `from_status`
* `to_status`
* `old_expires_at`
* `new_expires_at`
* `reason`
* `actor_user_id`
* `created_at`

### `listing_waitlist_entries`

* `id`
* `listing_id`
* `customer_id`
* `requirement_id`
* `deal_id`
* `priority`
* `status`
* `created_at`
* `notified_at`

---

## 95.12. Price

### `price_lists`

* `id`
* `price_list_code`
* `name`
* `project_id`
* `sales_launch_id`
* `internal_legal_entity_id`
* `channel_code`
* `status`
* `created_at`

### `price_list_versions`

* `id`
* `price_list_id`
* `version`
* `currency`
* `tax_inclusion_policy`
* `rounding_policy_id`
* `effective_from`
* `effective_to`
* `source_type`
* `source_reference`
* `source_file_hash`
* `status`
* `created_by`
* `reviewed_by`
* `approved_by`
* `created_at`

### `price_items`

* `id`
* `price_list_version_id`
* `asset_id`
* `listing_id`
* `base_amount`
* `price_per_area`
* `area_basis`
* `gross_amount`
* `tax_amount`
* `maintenance_fee`
* `other_fee_amount`
* `currency`
* `effective_from`
* `effective_to`
* `status`
* `created_at`

### `price_components`

* `id`
* `price_item_id`
* `component_code`
* `component_type`
* `amount`
* `currency`
* `is_mandatory`
* `is_discountable`
* `financial_nature_code`
* `display_order`
* `created_at`

---

## 95.13. Sales Policy

### `sales_policies`

* `id`
* `policy_code`
* `name`
* `policy_type`
* `scope_type`
* `scope_id`
* `status`
* `created_at`

### `sales_policy_versions`

* `id`
* `sales_policy_id`
* `version`
* `conditions_json`
* `benefits_json`
* `stacking_rules_json`
* `funding_source_code`
* `effective_from`
* `effective_to`
* `status`
* `created_by`
* `reviewed_by`
* `approved_by`
* `created_at`

### `listing_policy_assignments`

* `id`
* `listing_id`
* `sales_policy_version_id`
* `priority`
* `effective_from`
* `effective_to`
* `status`
* `created_at`

---

## 95.14. External Inventory

### `external_inventory_sources`

* `id`
* `source_code`
* `partner_id`
* `integration_profile_id`
* `source_type`
* `status`
* `freshness_threshold_seconds`
* `created_at`

### `external_inventory_mappings`

* `id`
* `external_inventory_source_id`
* `external_project_id`
* `external_asset_id`
* `external_listing_id`
* `project_id`
* `asset_id`
* `listing_id`
* `mapping_confidence`
* `status`
* `created_at`
* `updated_at`

### `external_inventory_observations`

* `id`
* `external_inventory_source_id`
* `external_listing_id`
* `external_status`
* `external_price`
* `currency`
* `observed_at`
* `effective_at`
* `payload_hash`
* `payload_reference`
* `created_at`

### `inventory_sync_runs`

* `id`
* `external_inventory_source_id`
* `run_id`
* `started_at`
* `completed_at`
* `status`
* `received_count`
* `mapped_count`
* `conflict_count`
* `error_count`
* `checkpoint_json`
* `created_at`

### `inventory_reconciliation_cases`

* `id`
* `case_code`
* `project_id`
* `listing_id`
* `external_inventory_source_id`
* `conflict_type`
* `internal_snapshot_json`
* `external_snapshot_json`
* `risk_level`
* `status`
* `assigned_user_id`
* `due_at`
* `resolution`
* `created_at`
* `resolved_at`

---

## 95.15. Documents và Media

### `property_external_documents`

* `id`
* `project_id`
* `asset_id`
* `ownership_record_id`
* `sales_mandate_id`
* `listing_id`
* `document_type`
* `title`
* `document_id`
* `document_id`
* `document_hash`
* `issuer`
* `issued_at`
* `expires_at`
* `verification_status`
* `access_policy_id`
* `legal_hold_status`
* `created_by`
* `created_at`

### `property_media`

* `id`
* `project_id`
* `asset_id`
* `listing_id`
* `media_type`
* `title`
* `media_file_id`
* `thumbnail_file_id`
* `visibility`
* `usage_right_status`
* `effective_from`
* `expires_at`
* `display_order`
* `created_by`
* `created_at`

---

# 96. Candidate application operations — không phải OpenAPI canonical

> Các operation dưới đây là capability inventory. Exact paths, methods, payloads, errors, idempotency và authorization metadata thuộc OpenAPI.


## Partner

```text
GET    /partners
POST   /partners
GET    /partners/{id}
PATCH  /partners/{id}
POST   /partners/{id}/submit-verification
POST   /partners/{id}/verify
POST   /partners/{id}/suspend
GET    /partners/{id}/relationships
```

## Project

```text
GET    /projects
POST   /projects
GET    /projects/{id}
PATCH  /projects/{id}
POST   /projects/{id}/submit-review
POST   /projects/{id}/activate
POST   /projects/{id}/suspend
POST   /projects/{id}/archive

GET    /projects/{id}/hierarchy
POST   /projects/{id}/hierarchy-nodes
PATCH  /project-hierarchy-nodes/{id}

GET    /projects/{id}/parties
POST   /projects/{id}/parties
POST   /project-parties/{id}/end
```

## Sales Launch

```text
GET    /sales-launches
POST   /sales-launches
GET    /sales-launches/{id}
PATCH  /sales-launches/{id}
POST   /sales-launches/{id}/approve
POST   /sales-launches/{id}/activate
POST   /sales-launches/{id}/pause
POST   /sales-launches/{id}/close
```

## Asset

```text
GET    /property-assets
POST   /property-assets
GET    /property-assets/{id}
PATCH  /property-assets/{id}
POST   /property-assets/{id}/submit-verification
POST   /property-assets/{id}/verify
POST   /property-assets/{id}/suspend
POST   /property-assets/{id}/archive
GET    /property-assets/{id}/duplicate-candidates
GET    /property-assets/{id}/history
```

## Ownership

```text
GET    /property-assets/{id}/ownership
POST   /property-assets/{id}/ownership
PATCH  /property-ownership-records/{id}
POST   /property-ownership-records/{id}/submit-verification
POST   /property-ownership-records/{id}/verify
POST   /property-ownership-records/{id}/end
GET    /property-assets/{id}/encumbrances
POST   /property-assets/{id}/encumbrances
POST   /property-encumbrances/{id}/resolve
```

## Mandate

```text
GET    /sales-mandates
POST   /sales-mandates
GET    /sales-mandates/{id}
PATCH  /sales-mandates/{id}
POST   /sales-mandates/{id}/validate-scope
POST   /sales-mandates/{id}/submit-review
POST   /sales-mandates/{id}/approve
POST   /sales-mandates/{id}/activate
POST   /sales-mandates/{id}/suspend
POST   /sales-mandates/{id}/terminate
```

## Listing

```text
GET    /property-listings
POST   /property-listings
GET    /property-listings/{id}
PATCH  /property-listings/{id}
POST   /property-listings/{id}/validate-readiness
POST   /property-listings/{id}/submit-review
POST   /property-listings/{id}/activate
POST   /property-listings/{id}/create-version
POST   /property-listings/{id}/renew
POST   /property-listings/{id}/withdraw
POST   /property-listings/{id}/suspend
POST   /property-listings/{id}/archive
GET    /property-listings/{id}/history
```

## Inventory

```text
GET    /inventory-lists
POST   /inventory-lists
GET    /inventory-lists/{id}
POST   /inventory-lists/{id}/versions
GET    /inventory-list-versions/{id}
POST   /inventory-list-versions/{id}/validate
POST   /inventory-list-versions/{id}/preview
POST   /inventory-list-versions/{id}/approve
POST   /inventory-list-versions/{id}/activate
GET    /inventory-list-versions/{id}/items
```

## Availability và Lock

```text
GET    /property-listings/{id}/availability
POST   /property-listings/{id}/availability/check

POST   /property-listings/{id}/locks
GET    /commercial-locks/{id}
POST   /commercial-locks/{id}/confirm-external
POST   /commercial-locks/{id}/extend-request
POST   /commercial-locks/{id}/extend
POST   /commercial-locks/{id}/convert
POST   /commercial-locks/{id}/release
POST   /commercial-locks/{id}/cancel

GET    /property-listings/{id}/waitlist
POST   /property-listings/{id}/waitlist
```

## Price

```text
GET    /price-lists
POST   /price-lists
GET    /price-lists/{id}
POST   /price-lists/{id}/versions
GET    /price-list-versions/{id}
POST   /price-list-versions/{id}/validate
POST   /price-list-versions/{id}/compare
POST   /price-list-versions/{id}/approve
POST   /price-list-versions/{id}/activate
GET    /property-listings/{id}/effective-price
```

## Policy

```text
GET    /sales-policies
POST   /sales-policies
GET    /sales-policies/{id}
POST   /sales-policies/{id}/versions
GET    /sales-policy-versions/{id}
POST   /sales-policy-versions/{id}/simulate
POST   /sales-policy-versions/{id}/approve
POST   /sales-policy-versions/{id}/activate
GET    /property-listings/{id}/effective-policies
POST   /property-listings/{id}/policy-eligibility-check
```

## External Inventory

```text
GET    /external-inventory-sources
POST   /external-inventory-sources
POST   /external-inventory-sources/{id}/sync
GET    /external-inventory-sources/{id}/sync-runs
GET    /inventory-reconciliation-cases
GET    /inventory-reconciliation-cases/{id}
POST   /inventory-reconciliation-cases/{id}/resolve
POST   /inventory-reconciliation-cases/{id}/recheck
```

Backend phải tự enforce:

* Authenticated user.
* Legal Entity context.
* Project Access.
* Listing Access.
* Permission.
* Field masking.
* Mandate.
* Listing version.
* Price/policy version.
* Availability.
* Lock.
* Workflow.
* Approval.
* Idempotency.
* Database constraints.

---

# 97. Candidate permission vocabulary — không phải Permission Registry canonical

> Exact permission codes, scopes, role mappings, concealment và field masking thuộc security registries/matrices.


## Partner

```text
partner.view
partner.create
partner.update
partner.view_sensitive
partner.submit_verification
partner.review
partner.verify
partner.suspend
partner.view_audit
```

## Project

```text
project.view
project.view_sensitive
project.create
project.update
project.review
project.approve
project.activate
project.suspend
project.archive
project.manage_parties
project.manage_hierarchy
project.view_audit
project.export
```

## Sales Launch

```text
sales_launch.view
sales_launch.create
sales_launch.update
sales_launch.review
sales_launch.approve
sales_launch.activate
sales_launch.pause
sales_launch.close
```

## Asset

```text
property_asset.view
property_asset.view_sensitive
property_asset.create
property_asset.update
property_asset.submit_verification
property_asset.review
property_asset.verify
property_asset.suspend
property_asset.archive
property_asset.merge
property_asset.view_audit
property_asset.export
```

## Ownership

```text
property_ownership.view
property_ownership.view_sensitive
property_ownership.create
property_ownership.update
property_ownership.submit_verification
property_ownership.review
property_ownership.verify
property_ownership.end
property_ownership.view_documents

property_encumbrance.view
property_encumbrance.create
property_encumbrance.update
property_encumbrance.resolve
```

## Mandate

```text
sales_mandate.view
sales_mandate.view_sensitive
sales_mandate.create
sales_mandate.update
sales_mandate.validate
sales_mandate.review
sales_mandate.approve
sales_mandate.activate
sales_mandate.suspend
sales_mandate.terminate
sales_mandate.view_documents
```

## Listing

```text
property_listing.view
property_listing.view_owner
property_listing.view_sensitive_price
property_listing.create
property_listing.update
property_listing.validate_readiness
property_listing.review
property_listing.approve
property_listing.activate
property_listing.create_version
property_listing.renew
property_listing.withdraw
property_listing.suspend
property_listing.archive
property_listing.view_audit
property_listing.export
```

## Inventory

```text
inventory.view
inventory.view_summary
inventory.view_detail
inventory.create
inventory.import
inventory.validate
inventory.preview
inventory.review
inventory.approve
inventory.activate
inventory.reconcile
inventory.override_status
inventory.export
```

## Price

```text
price.view_public
price.view_sales
price.view_floor
price.view_margin
price_list.create
price_list.import
price_list.validate
price_list.compare
price_list.review
price_list.approve
price_list.activate
price_list.view_history
```

## Policy

```text
sales_policy.view
sales_policy.create
sales_policy.update
sales_policy.simulate
sales_policy.review
sales_policy.approve
sales_policy.activate
sales_policy.view_funding
```

## Lock

```text
commercial_lock.view
commercial_lock.request_soft
commercial_lock.request_hard
commercial_lock.confirm_external
commercial_lock.extend_request
commercial_lock.extend
commercial_lock.release
commercial_lock.override
commercial_lock.admin_block
commercial_lock.view_audit
```

## External Inventory

```text
external_inventory.view
external_inventory.configure
external_inventory.sync
external_inventory.map
external_inventory.reconcile
external_inventory.override
external_inventory.view_logs
```

Các quyền kết hợp với:

```text
mine
team
department
branch
legal_entity
project
shared
all
```

---

# 98. Candidate role baseline — không phải Role/Permission Registry canonical

> Role descriptions dưới đây chỉ mô tả product intent; backend authority phải được resolve từ accepted registries và policies.


## 98.1. Sale

Được:

* Xem Project được cấp.
* Xem Listing được phép.
* Xem giá bán.
* Xem chính sách áp dụng.
* Yêu cầu Hold.
* Tạo Proposal ở Deal and Transaction Capability.
* Xem trạng thái lock của mình.

Không mặc định được:

* Xem giá sàn.
* Xem Owner contact.
* Sửa Listing.
* Thay availability.
* Export bảng hàng.
* Override lock.
* Xem toàn bộ mandate.

## 98.2. Team Lead

Được:

* Xem inventory team/project.
* Theo dõi lock.
* Review một số hold exception.
* Xem giá theo policy.
* Quản lý Product Access trong phạm vi nếu được cấp.

## 98.3. Inventory Manager

Được:

* Tạo và quản lý Project/Asset/Listing.
* Import bảng hàng.
* Đồng bộ.
* Reconciliation.
* Quản lý availability.
* Không mặc định duyệt pháp lý hoặc thanh toán.

## 98.4. Legal

Được:

* Review Asset legal profile.
* Ownership.
* Mandate.
* Listing legal readiness.
* Encumbrance.
* Documents.

## 98.5. Finance

Được:

* Xem payment flow.
* Price component tài chính.
* Revenue-related terms theo quyền.
* Không mặc định sửa inventory.

## 98.6. Director

Được:

* Scope `all` theo quyền.
* Approve Project, mandate, price, policy và override nhạy cảm.
* Export có audit.

---

# 99. Candidate business facts — không phải Event contracts canonical

> Exact Event names, versions, payloads, channels và consumers thuộc JSON Schema, AsyncAPI và Event Registry.


Product, Asset, Listing and Inventory Capability phát:

```text
partner.created
partner.verified
partner.suspended

project.created
project.activated
project.updated
project.suspended
project.archived

sales_launch.created
sales_launch.activated
sales_launch.paused
sales_launch.closed

property_asset.created
property_asset.verification_requested
property_asset.verified
property_asset.suspended
property_asset.duplicate_detected

property_ownership.created
property_ownership.verified
property_ownership.changed
property_encumbrance.created
property_encumbrance.resolved

sales_mandate.created
sales_mandate.activated
sales_mandate.suspended
sales_mandate.expired
sales_mandate.terminated

property_listing.created
property_listing.activated
property_listing.updated
property_listing.renewed
property_listing.withdrawn
property_listing.expired
property_listing.suspended
property_listing.sold

inventory.version_created
inventory.version_activated
inventory.import_completed
inventory.reconciliation_required
inventory.reconciled

price_list.version_created
price_list.version_activated
property_price.changed

sales_policy.version_created
sales_policy.activated
sales_policy.expired

commercial_lock.requested
commercial_lock.activated
commercial_lock.extended
commercial_lock.converted
commercial_lock.released
commercial_lock.expired
commercial_lock.conflict_detected

external_inventory.synced
external_inventory.status_changed
external_inventory.conflict_detected
```

Consumer phải idempotent.

---

# 100. Candidate Platform configuration references

> Exact configuration keys, schemas, scopes và resolution strategies thuộc Platform Context contracts.


```text
partner.verification_workflow
partner.verification_sla_policy

project.default_workflow
project.activation_policy
project.hierarchy_policy
project.numbering_scheme

asset.default_workflow
asset.verification_policy
asset.duplicate_policy
asset.numbering_scheme
asset.legal_readiness_rule_set

ownership.verification_workflow
ownership.percentage_policy
ownership.required_document_policy
encumbrance.blocking_policy

mandate.default_workflow
mandate.approval_policy
mandate.scope_conflict_policy
mandate.expiration_policy

listing.default_workflow
listing.activation_policy
listing.readiness_rule_set
listing.expiration_policy
listing.renewal_policy
listing.visibility_policy
listing.numbering_scheme

inventory.import_policy
inventory.versioning_policy
inventory.reconciliation_policy
inventory.freshness_policy

availability.rule_set
commercial_lock.policy
commercial_lock.duration_policy
commercial_lock.extension_policy
commercial_lock.priority_policy
commercial_lock.expiration_policy

price.versioning_policy
price.approval_policy
price.rounding_policy
price.field_access_policy

sales_policy.workflow
sales_policy.stacking_policy
sales_policy.eligibility_policy

external_inventory.sync_policy
external_inventory.mapping_policy
external_inventory.retry_policy

property.document_policy
property.media_policy
property.export_approval_policy
```

Tất cả phải có scope, version và effective dates.

---

# 101. System invariant

Các quy tắc sau không được cấu hình tắt:

1. Property Asset và Listing là hai thực thể khác nhau.
2. Ownership và Sales Mandate là hai thực thể khác nhau.
3. Listing active phải liên kết Asset hợp lệ.
4. Listing active phải có Mandate hoặc quyền bán hợp lệ.
5. Listing active phải có Seller Party.
6. Listing không được active ngoài thời hạn Mandate.
7. Giá active không được sửa trực tiếp.
8. Price List phải có version.
9. Sales Policy phải có version.
10. Proposal/Booking/Contract phải snapshot version.
11. Backend phải xác nhận availability.
12. Frontend không được tự đặt availability.
13. Một Listing không có hai exclusive active locks trái rule.
14. Lock phải được tạo trong transaction.
15. Database phải hỗ trợ chống race condition.
16. Booking không được tạo nếu Lock không hợp lệ.
17. Customer/Owner contact không được lộ ngoài quyền.
18. Giá sàn không được trả ngoài field permission.
19. Asset Ownership đã xác minh không được overwrite mất lịch sử.
20. External status stale không được mặc định là available.
21. Import không được bỏ qua duplicate và mandate rule.
22. Listing hết hạn không nhận Hold mới.
23. Owner rút bán không tự hủy Contract hoặc Payment.
24. Asset duplicate không được auto-merge chỉ bằng địa chỉ.
25. Mandate hết hạn phải chặn nghiệp vụ mới.

---

# 102. Rule nghiệp vụ bắt buộc

1. Partner dùng Party identity từ Customer 360 và Customer Identity Governance Capabilities.
2. Partner tổ chức phải duplicate check.
3. Hotline giống không đủ merge Partner.
4. Project có thể thuộc công ty hoặc Partner.
5. Project phải xác định Transaction Model.
6. Project phải xác định các Party role quan trọng.
7. Project không chỉ lưu một developer.
8. Tài sản riêng lẻ không bắt buộc có Project.
9. Project hierarchy phải linh hoạt.
10. Hierarchy đã dùng không được xóa cứng.
11. Sales Launch không thay Project.
12. Một Project có nhiều Sales Launch.
13. Property Asset có identity ổn định.
14. Asset Code không dùng làm sole duplicate proof khi nguồn khác nhau.
15. Asset duplicate phải có review.
16. Địa chỉ giống không đủ auto-merge Asset.
17. Project + Unit Code trùng phải cảnh báo.
18. Parcel + map sheet trùng phải cảnh báo.
19. Declared Asset từ Customer 360 Capability chưa phải verified Asset.
20. Sale không tự verify legal Asset.
21. Ownership có history.
22. Ownership transfer không overwrite.
23. Co-owner phải quản lý riêng.
24. Verified percentage phải được kiểm tra.
25. Declared percentage không mặc định verified.
26. Encumbrance phải có blocking actions.
27. Asset Legal Readiness phải có explanation.
28. Legal Readiness không thay kết luận pháp lý chính thức.
29. Mandate là căn cứ quyền bán.
30. Mandate không phải Listing.
31. Mandate phải xác định grantor và grantee.
32. Mandate phải có effective dates.
33. Mandate scope phải được backend kiểm tra.
34. Mandate hết hạn không cho Listing mới.
35. Mandate suspend chặn action tương ứng.
36. Exclusivity conflict phải được phát hiện.
37. Listing phải liên kết một Asset.
38. Listing phải liên kết Mandate hoặc quyền sở hữu trực tiếp.
39. Listing phải xác định Seller Party.
40. Owner, Seller và Payment Receiver có thể khác nhau.
41. Listing public không lộ Owner contact.
42. Private Listing cần Listing Access.
43. Một Asset có thể có nhiều Listing lịch sử.
44. Nhiều Listing active phải tuân thủ exclusivity.
45. Listing active phải có giá.
46. Listing active phải có thời hạn.
47. Listing activation phải kiểm tra legal readiness.
48. Listing readiness phải có explanation.
49. Listing hết hạn không tự gia hạn.
50. Gia hạn cần owner/partner confirmation khi policy yêu cầu.
51. Listing withdrawal phải kiểm tra giao dịch active.
52. Listing version phải lưu thay đổi thương mại.
53. Inventory List không sao chép Listing.
54. Listing có thể nằm nhiều bảng hàng.
55. Availability dùng nguồn chung.
56. Inventory version không overwrite.
57. Import bảng hàng phải tạo version.
58. Inventory item phải giữ source row.
59. External status không ghi đè mất lịch sử.
60. External mapping phải có confidence/status.
61. Stale external data không được coi available.
62. External conflict phải block Hold mới nếu risk cao.
63. Reconciliation không tự hủy Booking.
64. Physical Status khác Legal Status.
65. Legal Status khác Commercial Availability.
66. Marketing Status khác Commercial Availability.
67. Backend phải tính availability tại request time.
68. Availability phải kiểm tra Listing period.
69. Availability phải kiểm tra Mandate.
70. Availability phải kiểm tra active lock.
71. Availability phải kiểm tra external freshness.
72. Lock phải có source resource.
73. Lock phải có expiry trừ Contract/Admin Block hợp lệ.
74. Soft Hold không phải Booking.
75. Hard Hold không phải Contract.
76. Lock không được gia hạn vô hạn.
77. Extension phải có policy và history.
78. Một Listing không có hai exclusive active lock.
79. Hai request đồng thời chỉ một thành công.
80. Cache không phải nguồn lock duy nhất.
81. Preemption cần workflow đặc biệt.
82. Waitlist không khóa Listing.
83. Waitlist không hiển thị là Hold.
84. Price List phải có currency.
85. Giá phải dùng decimal.
86. Base price và Floor Price khác nhau.
87. Asking Price và Owner Net khác nhau.
88. Giá sàn phải có field permission.
89. Giá thay đổi không sửa Proposal snapshot cũ.
90. Price component phải rõ bản chất.
91. Thuế/phí phải xác định đã gồm hay chưa.
92. Sale không tự nhập tổng giá không cấu phần khi policy cấm.
93. Sales Policy phải có effective dates.
94. Policy phải có eligibility.
95. Policy stacking phải rõ.
96. Policy mới không áp dụng hồi tố.
97. Media phải có usage rights.
98. Media hết quyền phải ngừng dùng.
99. Document phải có access policy.
100. Public Listing không hiển thị legal document nhạy cảm.
101. Exact location của private Listing phải được bảo vệ.
102. Project Access không mở Owner Profile.
103. Listing Access không mở Financial Profile Customer.
104. View không đồng nghĩa Export.
105. Sale không bulk export bảng hàng.
106. Team Lead không mặc định bulk export.
107. Import không bỏ qua permission.
108. Import không bỏ qua unique constraint.
109. Manual override phải có reason.
110. Override phải có expiry nếu tạm thời.
111. User inactive không được tạo lock.
112. User không có Project Access không được Hold.
113. User không có Listing Access không được xem private Listing.
114. Listing sold không được chuyển Available bằng edit thường.
115. Reopen Listing phải qua workflow.
116. Asset archive không được có Listing active.
117. Project archive không được có giao dịch active trái rule.
118. Ownership conflict Critical có thể chặn Contract.
119. Mandate conflict có thể chặn Listing.
120. Audit nguồn cung không được sửa.

---

# 103. Cảnh báo và phát hiện bất thường

Hệ thống cần cảnh báo khi:

* Partner trùng tax code.
* Partner hết verification.
* Project không có Developer/Seller role.
* Project có Payment Receiver không hợp lệ.
* Asset trùng Unit Code.
* Asset trùng parcel/map sheet.
* Asset không có vị trí.
* Asset verified nhưng Ownership chưa đủ.
* Verified ownership vượt hoặc thiếu 100%.
* Co-owner chưa xác nhận.
* Encumbrance Critical.
* Asset Legal Readiness mâu thuẫn legal status.
* Mandate scope không bao phủ Listing.
* Mandate hết hạn nhưng Listing active.
* Nhiều mandate exclusive chồng lấn.
* Listing active không có giá.
* Listing active không có Seller Party.
* Listing active ngoài thời hạn.
* Listing private bị user ngoài scope truy cập.
* Owner contact bị truy cập hàng loạt.
* Floor Price bị truy cập bất thường.
* Hai active Listing trái exclusivity.
* Listing hết hạn vẫn nhận Hold.
* Nhiều active lock trên một Listing.
* Lock hết hạn nhưng availability chưa cập nhật.
* Lock kéo dài bất thường.
* Sale giữ nhiều Listing nhưng không có activity.
* User không có Project Access tạo lock.
* Booking tồn tại nhưng lock bị giải phóng.
* External status sold nhưng nội bộ available.
* Internal sold nhưng external available.
* External data quá cũ.
* Mapping external sai.
* Giá internal khác external.
* Price version chồng lấn.
* Policy version chồng lấn.
* Giá sàn lớn hơn giá bán.
* Owner net lớn hơn public price.
* Giá không có currency.
* Import inventory giảm số lượng bất thường.
* Import tạo nhiều Asset duplicate.
* Reconciliation conflict quá SLA.
* Listing sold bị chuyển available không qua workflow.
* Project archived vẫn có Listing active.
* Asset archived vẫn có active lock.
* Media hết usage rights vẫn public.
* Mandate tài liệu hết hạn.
* Public Listing hiển thị exact private address.
* Export inventory bất thường.

---

# 104. Audit requirements và evidence

> Audit Context sở hữu immutable Audit facts. Product Context phát sinh audit-worthy facts/references; operational logs không thay Audit.


## 104.1. Thao tác bắt buộc

* Tạo/update Partner.
* Verify Partner.
* Tạo/update Project.
* Thay Project Party.
* Tạo hierarchy.
* Tạo Sales Launch.
* Tạo/update Asset.
* Verify Asset.
* Asset duplicate resolution.
* Tạo/update Ownership.
* Verify Ownership.
* Tạo/resolve Encumbrance.
* Tạo/update Mandate.
* Activate/suspend/terminate Mandate.
* Tạo/update/activate Listing.
* Renew/withdraw/suspend Listing.
* Import inventory.
* Activate inventory version.
* Create/activate Price Version.
* Create/activate Policy Version.
* Availability override.
* Create/extend/release lock.
* Lock conflict.
* External sync.
* External mapping.
* Reconciliation.
* Export.
* Sensitive owner/floor-price access.

## 104.2. Nội dung

* Actor.
* Role.
* Legal Entity.
* Project.
* Asset.
* Listing.
* Owner/Partner.
* Mandate.
* Price/policy version.
* Lock.
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

# 105. Phạm vi MVP

## 105.1. Bắt buộc

* Partner Profile.
* Developer/Owner/Distributor types.
* Project.
* Project Parties.
* Basic hierarchy.
* Sales Launch.
* Apartment, townhouse, villa và land plot assets.
* Standalone Asset.
* Asset duplicate check.
* Asset verification.
* Ownership.
* Co-owner.
* Ownership verification.
* Basic encumbrance.
* Sales Mandate.
* Distribution/Consignment/Owner Direct mandates.
* Mandate scope.
* Listing.
* Listing version.
* Public/Internal/Private visibility.
* Listing activation readiness.
* Inventory List.
* Inventory version.
* Inventory items.
* Price List.
* Price version.
* Base/asking/minimum/floor price.
* Basic price components.
* Sales Policy.
* Policy version.
* Availability Engine.
* Soft Hold.
* Hard Hold.
* Booking Lock integration point.
* Lock expiry.
* Anti-double-sale transaction.
* Database unique constraint.
* External inventory file import.
* Basic API sync.
* Reconciliation.
* Project Access.
* Listing Access.
* Field masking.
* Documents by URL.
* Media by URL.
* Audit.
* Dashboard.
* Alerts.
* Domain events.

## 105.2. Giai đoạn nâng cao

* Multi-currency.
* Full geospatial polygon.
* 3D/virtual tour.
* Automated legal registry integration.
* Automated land planning integration.
* Advanced external inventory API.
* Real-time owner portal.
* Public marketplace.
* Rental Listing.
* Property management.
* Dynamic pricing.
* AI data extraction.
* AI Asset duplicate support.
* Predictive absorption.
* Automated price recommendation.
* Multi-channel syndication.
* Digital mandate signing.
* Blockchain/notary integration nếu có giá trị thực tế.
* Complex asset subdivision/composition.
* Fractional ownership.
* Package/bundle inventory.
* Advanced waitlist allocation.

---

# 106. Tiêu chí nghiệm thu

Capability được xem là đạt khi:

1. Tạo được Partner.
2. Partner dùng Party ID.
3. Partner duplicate check theo Organization Identity.
4. Partner có nhiều type.
5. Partner có verification.
6. Partner chưa verified không active nguồn cung trái policy.
7. Tạo được Project công ty tự phát triển.
8. Tạo được Project chủ đầu tư ngoài.
9. Project có Transaction Model.
10. Project có Developer Party.
11. Project có Seller Legal Entity.
12. Project có Payment Receiver.
13. Project có nhiều Party role.
14. Tạo được hierarchy.
15. Hierarchy hỗ trợ Phase/Tower/Floor.
16. Hierarchy hỗ trợ Zone/Row/Plot.
17. Hierarchy giữ lịch sử.
18. Tạo được Sales Launch.
19. Một Project có nhiều Sales Launch.
20. Sales Launch có effective dates.
21. Tạo được Asset dự án.
22. Tạo được Asset riêng lẻ.
23. Tạo được Apartment.
24. Tạo được Villa/Townhouse.
25. Tạo được Land Plot.
26. Land Plot lưu parcel/map sheet.
27. Asset có Asset Code.
28. Asset có physical status.
29. Asset có legal status.
30. Asset có verification status.
31. Asset duplicate theo Project + Unit Code được phát hiện.
32. Asset duplicate đất được phát hiện.
33. Asset không auto-merge chỉ bằng address.
34. Asset verification hoạt động.
35. Sale không tự verify legal Asset.
36. Tạo được Ownership.
37. Ownership liên kết Party/Customer.
38. Tạo được nhiều co-owner.
39. Lưu được ownership percentage.
40. Declared và verified percentage tách biệt.
41. Ownership transfer giữ lịch sử.
42. Ownership verified tổng tỷ lệ được kiểm tra.
43. Tạo được Encumbrance.
44. Encumbrance có blocking actions.
45. Tính được Asset Legal Readiness.
46. Legal Readiness có explanation.
47. Tạo được Developer Right.
48. Tạo được Distribution Mandate.
49. Tạo được Consignment Mandate.
50. Tạo được Owner Direct Sale Mandate.
51. Mandate có grantor và grantee.
52. Mandate có scope.
53. Mandate có effective dates.
54. Mandate có rights.
55. Mandate có exclusivity.
56. Mandate hết hạn chặn Listing mới.
57. Mandate scope sai chặn Listing.
58. Mandate conflict được cảnh báo.
59. Tạo được Listing.
60. Listing liên kết Asset.
61. Listing liên kết Mandate.
62. Listing có Seller Party.
63. Listing có Internal Legal Entity.
64. Listing có Transaction Model.
65. Listing có start/end.
66. Listing có visibility.
67. Listing có readiness.
68. Listing active cần giá.
69. Listing active cần mandate hợp lệ.
70. Listing active cần legal readiness.
71. Listing version được lưu.
72. Thay giá tạo hoặc tham chiếu version mới.
73. Gia hạn Listing hoạt động.
74. Owner rút Listing qua workflow.
75. Listing hết hạn không nhận Hold.
76. Private Listing chỉ user được cấp xem.
77. Public Listing không lộ Owner contact.
78. Một Asset có nhiều Listing lịch sử.
79. Exclusivity ngăn Listing active trái phép.
80. Tạo được Inventory List.
81. Tạo được Inventory Version.
82. Inventory Version có source file hash.
83. Listing có thể nằm nhiều bảng hàng.
84. Availability vẫn dùng nguồn chung.
85. Import inventory có preview.
86. Import inventory có validation.
87. Import không tạo Asset trùng trái rule.
88. Tạo được Price List.
89. Tạo được Price Version.
90. Price Version có effective dates.
91. Giá dùng decimal.
92. Giá có currency.
93. Tạo được Price Component.
94. Tách được Base Price và Asking Price.
95. Tách được Floor Price.
96. Sale không xem Floor Price nếu không có quyền.
97. Tạo được Sales Policy.
98. Sales Policy có version.
99. Policy có eligibility.
100. Policy có stacking rule.
101. Policy mới không sửa snapshot cũ.
102. Availability API trả kết quả.
103. Availability có explanation.
104. Availability kiểm tra Listing status.
105. Availability kiểm tra Mandate.
106. Availability kiểm tra Price.
107. Availability kiểm tra active lock.
108. Availability kiểm tra external freshness.
109. Tạo được Soft Hold lock.
110. Tạo được Hard Hold lock.
111. Lock có expiry.
112. Lock có source Deal/Customer.
113. Lock có idempotency.
114. Hai request đồng thời chỉ một lock thành công.
115. Request còn lại nhận conflict rõ ràng.
116. Database constraint ngăn double lock.
117. Lock hết hạn được giải phóng.
118. Lock converted không bị job expire.
119. Lock extension có history.
120. Waitlist không khóa Listing.
121. External inventory source được tạo.
122. External mapping hoạt động.
123. External sync có idempotency.
124. External status được lưu lịch sử.
125. Stale external status không được coi available.
126. Reconciliation phát hiện status conflict.
127. Reconciliation không tự hủy Booking.
128. Price conflict được cảnh báo.
129. Inventory sync lỗi có retry.
130. Project Access giới hạn inventory.
131. Project Access không mở Owner Profile.
132. Listing Access giới hạn private Listing.
133. Backend enforce field masking.
134. Sửa URL không mở rộng quyền.
135. View không cho Export.
136. Sale không bulk export inventory.
137. Team Lead không bulk export mặc định.
138. Inventory Manager import được theo scope.
139. Director export có audit.
140. Product lưu Document references; Documents Context sở hữu File/Document/Version.
141. Media có visibility.
142. Media hết quyền được cảnh báo.
143. Public Listing không hiển thị legal document.
144. Exact private location được bảo vệ.
145. Dashboard drill-down đúng scope.
146. Audit lưu before/after.
147. Audit lưu price/policy version.
148. Audit lưu lock.
149. Domain events được phát.
150. Event consumer idempotent.
151. Capability hỗ trợ công ty tự làm chủ đầu tư.
152. Capability hỗ trợ phân phối chủ đầu tư ngoài.
153. Capability hỗ trợ tài sản công ty sở hữu.
154. Capability hỗ trợ Customer ký gửi.
155. Capability hỗ trợ Partner Asset.
156. Capability hỗ trợ đất nền dự án.
157. Capability hỗ trợ đất riêng lẻ.
158. Capability không đồng nhất Asset và Listing.
159. Capability không đồng nhất Owner và Seller.
160. Capability cung cấp nguồn cung chuẩn cho Matching và Deal.

---

# 107. Anti-patterns và canonical requirements

Phần này quy định các hành vi bị cấm và cách triển khai canonical cho dự án Greenfield.

## AP-PRO-001 — Mọi sản phẩm đều là Unit của Project

**Không được áp dụng**

Buộc mọi nguồn cung phải nằm trong Project hierarchy.

**Canonical requirement**

Property Asset có thể thuộc Project hoặc là standalone asset. Project relationship chỉ bắt buộc khi business reality yêu cầu.

## AP-PRO-002 — Đồng nhất Property Asset với Listing

**Không được áp dụng**

Dùng một record vừa đại diện tài sản vật lý/pháp lý vừa đại diện lần chào bán.

**Canonical requirement**

Property Asset có identity ổn định; Listing là commercial offering có Selling Right, period, price, policy, visibility và lifecycle riêng.

## AP-PRO-003 — Đồng nhất Owner, Developer, Seller và Payment Receiver

**Không được áp dụng**

Suy luận một Party hoặc Legal Entity giữ tất cả vai trò.

**Canonical requirement**

Owner, Co-owner, Developer, Seller, Mandate Grantor, Payment Receiver và Revenue Beneficiary là các roles độc lập, có effective scope và evidence.

## AP-PRO-004 — Ownership tự tạo Selling Right

**Không được áp dụng**

Cho rằng người sở hữu hoặc người khai báo Asset mặc định có quyền đưa Listing vào giao dịch qua công ty.

**Canonical requirement**

Selling Right phải được xác định riêng bằng developer right, ownership/direct-sale authority, distribution, brokerage, consignment, authorization hoặc căn cứ được chấp nhận.

## AP-PRO-005 — Một trường status cho mọi lớp trạng thái

**Không được áp dụng**

Gộp physical, legal, verification, marketing, listing lifecycle và commercial availability vào một field.

**Canonical requirement**

Các dimensions phải được quản trị riêng và chỉ tổng hợp qua governed readiness/availability decisions.

## AP-PRO-006 — Giá hiện tại nằm trực tiếp trên Asset

**Không được áp dụng**

Ghi đè một giá duy nhất trên Unit/Asset và dùng nó cho mọi giao dịch lịch sử.

**Canonical requirement**

Price và Sales Policy phải có version/effective period; Proposal, Booking và Contract phải giữ accepted references hoặc immutable snapshots.

## AP-PRO-007 — Frontend quyết định availability

**Không được áp dụng**

Dựa vào trạng thái đã tải trước đó hoặc nút bị ẩn để cho phép Hold/Booking.

**Canonical requirement**

Product backend phải tính và xác nhận availability tại request time, bao gồm Listing, Selling Right, policy, lock, version, external freshness và access context.

## AP-PRO-008 — Check rồi insert không có database guard

**Không được áp dụng**

Hai request cùng đọc “available” rồi cùng tạo Lock.

**Canonical requirement**

Commercial Lock phải atomic, idempotent, concurrency-safe và có database-level protection phù hợp.

## AP-PRO-009 — Cache là final lock authority

**Không được áp dụng**

Coi cache hoặc UI state là nguồn xác nhận cuối cùng cho Commercial Lock.

**Canonical requirement**

Database-backed Product invariant hoặc approved authoritative lock mechanism là final authority; cache chỉ hỗ trợ hiệu năng.

## AP-PRO-010 — Inventory List sao chép Listing

**Không được áp dụng**

Tạo một Listing record mới cho từng bảng hàng, team hoặc channel.

**Canonical requirement**

Inventory List/Version tham chiếu canonical Listing; availability vẫn dùng Product source chung.

## AP-PRO-011 — External feed ghi đè Product history

**Không được áp dụng**

Provider payload trực tiếp thay Product records và xóa lịch sử nội bộ.

**Canonical requirement**

Provider data đi qua Integration ACL, accepted observation, mapping, version/freshness và Product reconciliation.

## AP-PRO-012 — External conflict tự hủy Booking

**Không được áp dụng**

Khi provider báo unavailable, Product hoặc Integration tự xóa/hủy Booking.

**Canonical requirement**

Product block nghiệp vụ mới, tạo reconciliation fact/case và phối hợp với Transaction qua accepted workflow; Booking ownership vẫn thuộc `transaction`.

## AP-PRO-013 — Product trực tiếp sửa Transaction, Contract hoặc Revenue

**Không được áp dụng**

Product update Deal, Booking, Contract, Payment, Receipt, Revenue hoặc Commission để “đồng bộ trạng thái”.

**Canonical requirement**

Mỗi Context chỉ ghi local business state. Cross-context propagation dùng API, Events, Process Manager, retry và reconciliation.

## AP-PRO-014 — Document URL là legal evidence canonical

**Không được áp dụng**

Lưu một URL tùy ý trong Product table làm nguồn pháp lý cuối cùng.

**Canonical requirement**

Documents Context sở hữu File/Document/Version/evidence. Product chỉ giữ approved references, summaries và access/usage metadata.

## AP-PRO-015 — Project/Listing Access mở Owner Profile

**Không được áp dụng**

Cho rằng quyền xem Project hoặc Listing đồng nghĩa quyền xem Owner PII, legal documents, floor price hoặc mandate terms.

**Canonical requirement**

Resource access và field policy phải được backend enforce riêng; aggregate, detail, sensitive-field và export access là các quyền độc lập.

## AP-PRO-016 — Candidate examples là exact contracts

**Không được áp dụng**

Dùng các table names, endpoint examples, status codes, Event names hoặc permission codes trong tài liệu này để code mà không qua Context Pack/machine contracts.

**Canonical requirement**

Exact database, API, Event, permission và lifecycle contracts phải được khóa trong nguồn canonical tương ứng.

## AP-PRO-017 — Import bỏ qua Domain rules

**Không được áp dụng**

Import Project, Asset, Listing, Price hoặc Inventory bằng raw inserts.

**Canonical requirement**

Import phải có staging, validation, duplicate checks, dry run, canonical commands, idempotency, source lineage và reconciliation.

## AP-PRO-018 — Mặc định tồn tại hệ thống tiền nhiệm

**Không được áp dụng**

Tự thiết kế compatibility layer, migration mappings hoặc status aliases khi chưa có approved scope.

**Canonical requirement**

`crm_bds_ai` là Greenfield. Historical import hoặc migration chỉ tồn tại khi có scope, mapping, security review, reconciliation và acceptance criteria riêng.

---

# 108. Kết luận

Product, Asset, Listing and Inventory Capability là nguồn nghiệp vụ chuẩn cho nguồn cung bất động sản của `crm_bds_ai`.

Capability phải bảo đảm:

- Canonical Party identity được tham chiếu từ `party`.
- Project và standalone Asset đều được hỗ trợ.
- Property Asset khác Listing.
- Ownership khác Selling Right.
- Owner, Developer, Seller, Payment Receiver và Revenue Beneficiary là các roles riêng.
- Ownership, Selling Right, Price và Sales Policy có history/version.
- Listing chỉ active khi Asset, Selling Right, readiness, period và price/policy phù hợp.
- Product Context là authority cho availability và Commercial Lock.
- Concurrent requests không tạo conflicting Locks trái invariant.
- External supply đi qua Integration ACL và Product reconciliation.
- Product không direct-write Transaction, Contract hoặc Revenue.
- Restricted Documents và binary files thuộc Documents Context.
- Owner PII, floor price, private location và legal evidence được backend bảo vệ.
- Proposal, Booking và Contract sử dụng đúng commercial snapshots.
- Mọi thay đổi quan trọng có lineage, Audit request/facts, observability và evidence.

> Product Context sở hữu availability và Commercial Lock, nhưng không trở thành siêu Context sở hữu toàn bộ giao dịch. Ranh giới giữa Product, Transaction, Contract, Revenue, Documents và Integration phải được bảo vệ bằng published contracts và local transactions.
