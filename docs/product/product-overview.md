# CRM_BDS_AI — PRODUCT OVERVIEW

## Tổng quan sản phẩm CRM và nền tảng điều hành kinh doanh bất động sản hợp nhất

**Document ID:** `PROD-OVERVIEW-001`  
**Canonical path:** `docs/product/product-overview.md`  
**Product:** `crm_bds_ai`  
**Version:** `1.0.0`  
**Status:** `Accepted / Product Direction`  
**Owner:** `Product Owner`  
**Reviewers:** `Domain Owner`, `Architecture Owner`, `Operations Owner`, `Finance Owner`, `Legal Owner`, `Security Owner`  
**Effective date:** `2026-08-05`  
**Last reviewed:** `2026-08-05`  
**Supersedes:** `None — Greenfield baseline`  
**Classification:** `INTERNAL`

---

# 1. Mục đích tài liệu

Tài liệu này xác định:

- Sản phẩm là gì.
- Sản phẩm phục vụ ai.
- Những mô hình kinh doanh bất động sản nào phải được hỗ trợ.
- Những vấn đề nghiệp vụ nào sản phẩm phải giải quyết.
- Những năng lực sản phẩm cốt lõi.
- Những khái niệm nghiệp vụ không được hiểu sai.
- Những business invariants cấp cao không được vi phạm.
- Những nội dung không thuộc phạm vi thẩm quyền của Product Overview.

Tài liệu này không định nghĩa:

- Exact Bounded Context ownership.
- Exact database schema.
- Exact table hoặc column.
- Exact API path, payload hoặc response envelope.
- Exact Event inventory hoặc Event payload.
- Exact permission code hoặc role matrix.
- Exact UI layout.
- Exact technology stack.
- Exact Sprint implementation.
- Exact migration hoặc compatibility mechanism.

Các nội dung exact phải được lấy từ tài liệu và machine-readable contract tương ứng.

---

# 2. Nguồn chân lý theo loại thông tin

| Nội dung | Nguồn chân lý |
|---|---|
| Tầm nhìn và phạm vi sản phẩm | Product Charter + tài liệu này |
| Thuật ngữ nghiệp vụ | Domain Glossary |
| Business invariant chi tiết | Context Implementation Pack |
| Data ownership | Source of Truth Matrix |
| Kiến trúc | Accepted ADRs + Architecture Overview |
| Exact database | Alembic migrations |
| Exact API | OpenAPI |
| Exact Event | JSON Schema + AsyncAPI |
| Exact permission | Permission Registry |
| Exact state machine | Context Pack |
| Exact Sprint scope | Sprint Detailed Execution Pack |
| Trạng thái hoàn thành | Sprint Acceptance Report |

Khi nội dung trong tài liệu này khác Context Pack hoặc machine-readable contract đã được chấp nhận, phải áp dụng Documentation Governance và xử lý conflict rõ ràng.

---

# 3. Định nghĩa sản phẩm

`crm_bds_ai` là một hệ thống CRM và nền tảng điều hành kinh doanh bất động sản hợp nhất.

Sản phẩm phải hỗ trợ toàn bộ hành trình:

```text
Marketing
→ Lead
→ Customer
→ Requirement
→ Asset và Listing
→ Matching
→ Deal
→ Hold hoặc Reservation
→ Booking
→ Contract
→ Payment
→ Revenue
→ Commission
→ Activity
→ Analytics
→ Documents
→ Audit
→ Operations
```

Sản phẩm không chỉ là:

- CRM môi giới.
- CRM chủ đầu tư.
- Phần mềm quản lý bảng hàng.
- Phần mềm quản lý Lead.
- Phần mềm kế toán.
- Phần mềm quản lý hoa hồng.

Sản phẩm là nền tảng thống nhất để doanh nghiệp bất động sản vận hành nhiều mô hình kinh doanh trong cùng một hệ thống dữ liệu, cùng một Customer 360 và cùng một cơ chế kiểm soát quyền truy cập.

---

# 4. Tầm nhìn sản phẩm

Mục tiêu dài hạn của `crm_bds_ai` là trở thành nguồn dữ liệu nghiệp vụ trung tâm của doanh nghiệp bất động sản.

Hệ thống phải giúp trả lời đáng tin cậy:

- Customer này là ai.
- Customer có những vai trò nào.
- Customer đang muốn mua, bán, ký gửi, cho thuê hay đầu tư.
- Customer đang làm việc với sale hoặc team nào.
- Customer có những nhu cầu nào đang active.
- Những Listing nào đã được đề xuất.
- Tại sao một Listing được đánh giá phù hợp.
- Tài sản vật lý thuộc sở hữu của ai.
- Công ty có quyền bán dựa trên căn cứ nào.
- Công ty đóng vai trò gì trong giao dịch.
- Ai là bên mua.
- Ai là bên bán.
- Ai đang thu tiền.
- Ai là người nhận tiền cuối cùng.
- Khoản tiền công ty nhận có bản chất gì.
- Công ty được hưởng doanh thu từ đâu.
- Hoa hồng nội bộ được tài trợ từ nguồn nào.
- Sale, co-sale và quản lý được hưởng bao nhiêu.
- Khoản hoa hồng đang ở trạng thái dự kiến, ghi nhận, khả dụng, đã duyệt hay đã trả.
- Trách nhiệm tiếp theo thuộc về ai.
- Giao dịch đang có rủi ro, thiếu hồ sơ hoặc quá SLA ở bước nào.
- Ai đã thay đổi dữ liệu, thay đổi gì và vì sao.

---

# 5. Các vấn đề sản phẩm phải giải quyết

Sản phẩm phải giảm tối đa:

- Dữ liệu phân tán trong Excel, Zalo, điện thoại cá nhân và tài liệu rời rạc.
- Một người được nhiều sale tạo thành nhiều Customer khác nhau.
- Một tài sản vật lý bị tạo trùng vì có nhiều nguồn bán.
- Một tài sản bị nhầm với một lần đưa tài sản ra thị trường.
- Hai sale cùng giữ hoặc bán một Listing.
- Không xác định được ai chịu trách nhiệm chăm sóc.
- Không biết công ty có quyền bán dựa trên căn cứ nào.
- Không phân biệt tiền doanh thu, tiền thu hộ và tiền phải hoàn trả.
- Không xác định được nguồn hình thành doanh thu.
- Không xác định được nguồn tài trợ hoa hồng.
- Không có lịch sử khi thay đổi giá, người mua, bên bán, co-sale hoặc hợp đồng.
- Phiếu thu hoặc chứng từ đã phát hành bị sửa trực tiếp.
- Dashboard tính cùng một chỉ số theo nhiều công thức khác nhau.
- Export Customer và bảng hàng không được kiểm soát.
- Giao dịch liên Context bị treo nhưng người dùng không biết đang chờ bước nào.
- Không có bằng chứng Audit cho hành động nhạy cảm.

---

# 6. Phạm vi doanh nghiệp sử dụng

Sản phẩm được thiết kế trước hết cho một doanh nghiệp hoặc một nhóm doanh nghiệp bất động sản nội bộ.

Hệ thống có thể quản lý:

- Nhiều Legal Entity.
- Nhiều chi nhánh.
- Nhiều phòng ban.
- Nhiều phòng kinh doanh.
- Nhiều team.
- Nhiều dự án.
- Nhiều kho sản phẩm.
- Nhiều mô hình giao dịch.
- Nhiều vai trò nội bộ.
- Nhiều nguồn doanh thu.
- Nhiều chính sách hoa hồng.

Sản phẩm không mặc định là SaaS đa khách hàng độc lập.

Khái niệm Enterprise, Legal Entity và tenancy boundary phải được xác định trong Domain Glossary và ADR tương ứng.

---

# 7. Nhóm người dùng chính

## 7.1. Sale

Nhu cầu chính:

- Quản lý Lead.
- Quản lý Customer.
- Ghi nhận nhu cầu.
- Tìm và đề xuất Listing.
- Theo dõi Deal.
- Tạo Hold hoặc Booking.
- Theo dõi hợp đồng.
- Theo dõi công việc.
- Theo dõi hoa hồng cá nhân.

## 7.2. Team Lead và Trưởng phòng

Nhu cầu chính:

- Phân bổ Lead.
- Theo dõi quyền chăm sóc.
- Kiểm soát pipeline.
- Kiểm soát SLA.
- Quản lý co-sale.
- Theo dõi hiệu suất team.
- Theo dõi tồn kho và Booking.
- Xử lý tranh chấp và handover.

## 7.3. Quản lý kho và kinh doanh dự án

Nhu cầu chính:

- Quản lý Project.
- Quản lý Asset.
- Quản lý Listing.
- Quản lý giá và chính sách.
- Quản lý bảng hàng.
- Kiểm soát availability.
- Quản lý Commercial Lock.
- Kiểm soát quyền phân phối.

## 7.4. Kế toán

Nhu cầu chính:

- Ghi nhận Payment.
- Phân bổ Payment.
- Phát hành Receipt.
- Quản lý Receivable.
- Đối soát.
- Kiểm soát chứng từ.
- Quản lý hoàn tiền và điều chỉnh.

## 7.5. Tài chính

Nhu cầu chính:

- Dòng tiền.
- Hạn mức.
- Settlement.
- Refund.
- Revenue receivable.
- Commission payable.
- Payout.
- Clawback.
- Forecast tài chính.

## 7.6. Pháp chế và hồ sơ

Nhu cầu chính:

- Xác minh tài sản.
- Xác minh quyền bán.
- Quản lý hợp đồng.
- Quản lý phụ lục.
- Quản lý hồ sơ.
- Theo dõi chữ ký.
- Quản lý legal hold.

## 7.7. Marketing

Nhu cầu chính:

- Campaign.
- Source.
- Form.
- Lead attribution.
- Audience.
- Journey.
- Suppression.
- Conversion.
- Spend và ROI.

## 7.8. Ban giám đốc

Nhu cầu chính:

- Toàn cảnh pipeline.
- Tồn kho.
- Doanh thu.
- Dòng tiền.
- Commission.
- Hiệu suất tổ chức.
- Rủi ro.
- Cảnh báo.
- Forecast.
- Drill-down có kiểm soát.

---

# 8. Các mô hình kinh doanh bắt buộc

## 8.1. Công ty tự phát triển hoặc là bên bán

Đặc điểm:

- Công ty hoặc Legal Entity nội bộ sở hữu hoặc phát triển sản phẩm.
- Công ty kiểm soát giá và bảng hàng.
- Customer ký Booking hoặc Contract với công ty.
- Customer thanh toán cho công ty hoặc tài khoản được chỉ định.
- Khoản thanh toán có thể hình thành doanh thu bán bất động sản.
- Hoa hồng nội bộ được tài trợ từ ngân sách bán hàng hoặc chính sách nội bộ.

Luồng nghiệp vụ cấp cao:

```text
Project
→ Asset
→ Listing
→ Customer Requirement
→ Matching
→ Deal
→ Commercial Lock
→ Booking
→ Contract
→ Payment
→ Revenue
→ Internal Commission
```

## 8.2. Công ty phân phối dự án của chủ đầu tư ngoài

Đặc điểm:

- Chủ đầu tư hoặc đối tác sở hữu sản phẩm.
- Công ty có quyền phân phối hoặc môi giới.
- Customer có thể thanh toán trực tiếp cho chủ đầu tư.
- Công ty có thể thu hộ theo thỏa thuận.
- Công ty được hưởng phí phân phối hoặc hoa hồng.
- Hoa hồng nội bộ có thể phụ thuộc phần doanh thu đã đủ điều kiện hoặc đã thu.

Luồng nghiệp vụ cấp cao:

```text
External Project
→ Distribution Mandate
→ Inventory/Listings
→ Customer Requirement
→ Matching
→ Deal
→ Booking
→ Contract with external seller
→ Revenue entitlement
→ Collection
→ Internal Commission
```

## 8.3. Công ty nhận bán hộ hoặc ký gửi

Đặc điểm:

- Customer hoặc một nhóm Party là chủ tài sản.
- Công ty xác minh ownership và quyền bán.
- Công ty ký consignment, brokerage hoặc mandate.
- Asset được đưa ra thị trường bằng Listing.
- Buyer và Seller thực hiện giao dịch.
- Công ty được hưởng phí môi giới hoặc phí dịch vụ.
- Hoa hồng nội bộ có thể phân bổ cho đội seller-side và buyer-side.

Luồng nghiệp vụ cấp cao:

```text
Seller Lead
→ Customer/Owner
→ Asset verification
→ Listing acquisition
→ Consignment/Mandate
→ Active Listing
→ Buyer Matching
→ Deal
→ Reservation/Deposit
→ Contract
→ Settlement
→ Brokerage Revenue
→ Internal Commission
```

## 8.4. Công ty bán tài sản thuộc sở hữu công ty

Tài sản có thể:

- Do công ty mua lại.
- Nhận để xử lý công nợ.
- Là tài sản đầu tư.
- Là tài sản cố định được bán.

Sản phẩm phải hỗ trợ:

- Ownership rõ.
- Giá vốn và nguồn gốc tài sản.
- Approval giá.
- Listing.
- Transaction.
- Revenue.
- Financial reporting.

## 8.5. Công ty bán tài sản của đối tác

Quyền của công ty có thể gồm:

- Bán độc quyền.
- Bán không độc quyền.
- Tiếp thị.
- Nhận Booking.
- Thu hộ.
- Đàm phán trong hạn mức.

Mỗi quyền phải có:

- Grantor.
- Grantee.
- Asset hoặc Listing scope.
- Effective period.
- Exclusivity.
- Collection rights.
- Contractual basis.

## 8.6. Đất nền và tài sản riêng lẻ

Đất nền là một loại Asset, không phải một CRM riêng.

Sản phẩm cần hỗ trợ thuộc tính đặc thù như:

- Số thửa.
- Tờ bản đồ.
- Diện tích pháp lý.
- Diện tích thực tế.
- Mục đích sử dụng.
- Thời hạn sử dụng.
- Hình thức sử dụng.
- Mặt tiền.
- Chiều sâu.
- Đường tiếp cận.
- Quy hoạch.
- Lộ giới.
- Khả năng tách thửa.
- Thế chấp.
- Tranh chấp.
- Hạn chế chuyển nhượng.
- Giấy chứng nhận.
- Tài sản gắn liền với đất.

Exact field inventory thuộc Product Context Pack.

---

# 9. Nguyên tắc hợp nhất sản phẩm

## 9.1. Không tạo nhiều CRM tách biệt theo mô hình kinh doanh

Không xây riêng:

- CRM chủ đầu tư.
- CRM phân phối.
- CRM môi giới.
- CRM ký gửi.

Các mô hình phải dùng chung:

- Party.
- Customer.
- Lead.
- Requirement.
- Asset.
- Listing.
- Deal.
- Activity.
- Permission.
- Audit.
- Analytics.

Sự khác biệt được biểu hiện bằng business model, role của công ty, source of ownership, source of selling rights, payment flow và revenue model.

## 9.2. Không dùng một Boolean để mô tả toàn bộ mô hình

Một cờ như `is_company_project` không đủ để xác định:

- Ai sở hữu Asset.
- Ai là Seller.
- Ai thu tiền.
- Ai nhận tiền.
- Công ty đóng vai trò gì.
- Khoản tiền là revenue hay collected-on-behalf.
- Hoa hồng được tài trợ từ đâu.

Các chiều nghiệp vụ phải được mô hình hóa độc lập.

---

# 10. Party, Customer và vai trò

## 10.1. Party

Party là cá nhân hoặc tổ chức tham gia vào quan hệ nghiệp vụ.

Party cá nhân có thể là:

- Customer.
- Buyer.
- Seller.
- Owner.
- Co-owner.
- Payer.
- Representative.
- Authorized person.
- Referrer.
- Collaborator.

Party tổ chức có thể là:

- Công ty vận hành CRM.
- Legal Entity.
- Project Company.
- Developer.
- Distributor.
- Broker.
- Partner.
- Bank.
- Corporate Buyer.
- Service Provider.

## 10.2. Customer

Customer là quan hệ thương mại giữa Party và doanh nghiệp.

Một Party có thể đồng thời:

- Muốn mua.
- Muốn bán.
- Là owner.
- Là payer.
- Là referrer.
- Là representative.

Không tạo nhiều Customer chỉ vì cùng một Party có nhiều vai trò.

## 10.3. Customer là dữ liệu dùng chung toàn Enterprise

Customer không thuộc sở hữu vĩnh viễn của một sale.

Quyền truy cập Customer phụ thuộc:

- Assignment.
- Lead.
- Requirement.
- Deal.
- Listing.
- Booking.
- Contract.
- Task.
- Organizational scope.
- Field policy.

Exact scope rules thuộc Scope Resolution Specification.

---

# 11. Customer Identity

## 11.1. Identity toàn Enterprise

Customer identity phải được quản trị thống nhất trong phạm vi Enterprise đã được định nghĩa.

## 11.2. Chống trùng cá nhân

Quy tắc chống trùng cá nhân dựa trên normalized phone overlap theo chiến lược identity đã được chấp nhận.

Các dữ liệu như:

- Email.
- Họ tên.
- Ngày sinh.
- Địa chỉ.
- Social account.
- Identity document.

có thể hỗ trợ tìm kiếm hoặc review nhưng không mặc định thay chiến lược duplicate canonical.

## 11.3. Nhiều số điện thoại

Một Customer có thể có nhiều phone identities.

Mỗi phone identity cần có lifecycle, verification, source và primary-state phù hợp.

## 11.4. Số dùng chung

Shared phone exception phải:

- Có lý do.
- Có relationship.
- Có requester.
- Có approver.
- Có effective period nếu cần.
- Có Audit.

## 11.5. Merge

Customer merge phải:

- Không hard-delete nguồn.
- Giữ lineage.
- Tạo canonical redirect.
- Thông báo các Context liên quan.
- Có reconciliation.
- Có Audit.

Exact merge workflow thuộc Party Context Pack.

---

# 12. Asset, Ownership, Selling Right và Listing

## 12.1. Asset khác Listing

```text
Property Asset ≠ Property Listing
```

Asset là tài sản vật lý có identity ổn định.

Listing là một lần Asset được đưa ra thị trường với:

- Seller.
- Owner.
- Selling right.
- Price.
- Terms.
- Effective period.
- Commercial status.

Một Asset có thể có nhiều Listing theo thời gian hoặc theo selling channel.

## 12.2. Ownership khác Selling Right

Owner không đồng nghĩa với seller hoặc distributor.

Công ty có thể có quyền:

- Distribute.
- Broker.
- Consign.
- Market.
- Receive Booking.
- Collect money.
- Negotiate.

Selling right phải có căn cứ và hiệu lực.

## 12.3. Inventory khác Listing

Inventory là một tập hợp hoặc phiên bản các Listing được phép bán trong một thời điểm, kênh hoặc chính sách.

Không đồng nhất Inventory với Asset hoặc Listing.

---

# 13. Availability và Commercial Lock

Product phải chống double booking và double sale.

Business invariant:

```text
Một Listing chỉ có thể có một Commercial Lock có hiệu lực
làm mất khả dụng tại một thời điểm,
trừ khi Context Pack xác định một mô hình khác có kiểm soát.
```

Cơ chế phải được enforce ở backend và database.

Frontend không phải source of truth cho availability.

Nếu hai yêu cầu cạnh tranh:

- Chỉ một yêu cầu được thành công.
- Yêu cầu còn lại nhận conflict rõ.
- Không tạo duplicate Booking.
- Không dựa cache làm final authority.

Exact locking strategy thuộc Product Context Pack, Database Standards và ADR.

---

# 14. Requirement và Matching

## 14.1. Requirement

Requirement mô tả nhu cầu của Customer.

Có thể bao gồm:

- Mục đích.
- Loại Asset.
- Vị trí.
- Ngân sách.
- Financial readiness.
- Hard criteria.
- Soft preferences.
- Time horizon.
- Stakeholders.

## 14.2. Matching

Matching thực hiện trên:

```text
Requirement
→ Active Listing
→ Property Asset
```

Matching có thể trả:

- Rất phù hợp.
- Phù hợp.
- Phù hợp có điều kiện.
- Phương án thay thế.
- Không phù hợp.
- Lý do chấm điểm.

Matching không được:

- Tạo Booking.
- Tạo Commercial Lock.
- Sửa Requirement.
- Mở rộng quyền truy cập.
- Tuyên bố chắc chắn Customer được vay.
- Trở thành source of truth cho availability.

---

# 15. Deal và Transaction Case

## 15.1. Deal

Deal là một cơ hội kinh doanh cụ thể.

Có thể là:

- Buyer-side Deal.
- Seller-side Deal.
- Listing Acquisition Deal.
- Dual-side Deal.
- Partnership Deal.
- Distribution Deal.

## 15.2. Transaction Case

Transaction Case là hồ sơ giao dịch cấp cao liên kết:

- Asset.
- Listing.
- Buyer-side Deal.
- Seller-side Deal.
- Buyer Parties.
- Seller Parties.
- Company role.
- Payment flow.
- Revenue model.
- Contracts.
- Settlement.

Transaction Case không đồng nhất với Deal hoặc Contract.

---

# 16. Sale chính, co-sale và responsibility

Mỗi Deal có một primary sale tại một thời điểm.

Có thể có nhiều collaborators như:

- Lead source.
- Customer care.
- Project specialist.
- Site visit support.
- Closing.
- Legal support.
- Loan support.
- Seller-side sale.
- Buyer-side sale.

Co-sale allocation phải:

- Có version.
- Có approver khi cần.
- Có effective milestone.
- Có history.
- Không suy luận tự động từ số lượng activity.

---

# 17. Hold, Reservation, Booking và Deposit

Không ép mọi transaction model dùng một workflow giống nhau.

Có thể có:

- Internal Hold.
- External availability confirmation.
- Reservation.
- Offer.
- Booking.
- Deposit Commitment.
- Deposit.
- Seller confirmation.

Workflow chi tiết phụ thuộc transaction model.

Business invariants:

- Không xác nhận Booking khi Commercial Lock không hợp lệ.
- Không tạo duplicate Booking từ retry.
- Không bỏ qua dossier/readiness gate đã được cấu hình.
- Không silently overwrite conflict.

---

# 18. Contract và Parties

Contract có thể có:

- Nhiều Buyers.
- Nhiều Sellers.
- Nhiều Owners.
- Representatives.
- Authorized persons.
- Payers.
- Company Party.
- External Developer hoặc Partner.

Contract đã signed/effective không được sửa trực tiếp.

Thay đổi phải thông qua:

- Amendment.
- Replacement.
- Cancellation.
- Termination.
- Correction process có Audit.

Exact Contract state machine thuộc Contract Context Pack.

---

# 19. Payment, Receivable và Receipt

## 19.1. Payment không mặc định là Revenue

Payment có thể là:

- Tiền mua bất động sản.
- Deposit.
- Tiền thu hộ.
- Tiền giữ tạm.
- Khoản phải settlement.
- Phí môi giới.
- Phí phân phối.
- Khoản hoàn trả.

Mỗi khoản phải có business nature rõ.

## 19.2. Receivable

Receivable phải được hình thành từ nghĩa vụ có căn cứ.

Không nhập công nợ tùy ý không có adjustment hoặc source.

## 19.3. Receipt

Receipt đã phát hành phải immutable theo policy.

Nếu sai:

- Cancel hoặc revoke theo quy trình.
- Tạo replacement.
- Giữ lineage.
- Có reason và Audit.

---

# 20. Settlement

Khi công ty thu hộ hoặc giữ tiền cho Seller/Partner, hệ thống phải xác định:

- Gross transaction amount.
- Amount received.
- Amount held.
- Brokerage fee.
- Approved deductions.
- Tax/fee deductions.
- Amount payable to owner.
- Amount paid.
- Outstanding amount.
- Reconciliation status.

Khoản phải trả Owner không phải revenue của công ty.

---

# 21. Revenue

Revenue Engine xác định công ty có quyền được hưởng khoản gì.

Các loại revenue có thể gồm:

- Doanh thu bán bất động sản.
- Distribution fee.
- Brokerage fee.
- Service fee.
- Referral fee.
- Marketing fee.
- Management fee.
- Other approved revenue.

Mỗi revenue entitlement cần xác định:

- Transaction.
- Payer.
- Beneficiary Legal Entity.
- Basis.
- Formula.
- Amount.
- Recognition milestone.
- Collection status.
- Policy/version.
- Lineage.

---

# 22. Internal Commission

Internal Commission Engine xác định khoản phân bổ cho:

- Primary sale.
- Co-sale.
- Seller-side sale.
- Buyer-side sale.
- Team Lead.
- Department manager.
- Referrer.
- Project manager.
- Support team.
- Collaborator.

Nguồn tài trợ có thể là:

- Distribution fee.
- Brokerage fee.
- Sales budget.
- Company budget.
- Marketing fund.
- Incentive fund.
- Other approved source.

Phải phân biệt:

- Estimated.
- Accrued/recognized.
- Funded.
- Available.
- Approved for payment.
- Paid.
- Held.
- Clawback.

---

# 23. Clawback

Clawback có thể phát sinh khi:

- Contract cancelled.
- Transaction terminated.
- Contract value reduced.
- Asset changed.
- Revenue reversed.
- Distribution fee recovered.
- Brokerage fee refunded.
- Co-sale dispute resolved.
- Incentive withdrawn.

Không xóa Commission đã paid.

Phần đã trả có thể tạo:

- Negative balance.
- Recovery plan.
- Offset.
- Approved waiver.

---

# 24. Activity, Timeline và SLA

Activity là năng lực dùng chung cho:

- Task.
- Appointment.
- Call.
- Interaction.
- Timeline.
- Follow-up.
- Escalation.
- SLA.

Task có thể gắn với bất kỳ business resource phù hợp.

SLA là configuration.

Các giá trị thời gian trong tài liệu sản phẩm chỉ là ví dụ hoặc baseline, không phải exact implementation.

Quá SLA không tự động:

- Approve.
- Cancel transaction.
- Release listing.
- Refund.
- Pay commission.

---

# 25. Marketing

Marketing hỗ trợ:

- Campaign.
- Channel.
- Source.
- Form.
- Tracking.
- Touchpoint.
- Audience.
- Suppression.
- Journey.
- Conversion.
- Attribution.
- Spend.

Marketing phải tôn trọng:

- Customer scope.
- Consent.
- Suppression.
- Field masking.
- Data minimization.
- Export restrictions.

---

# 26. Analytics và Dashboard

Dashboard phải theo:

- Persona.
- Scope.
- Metric definition.
- Currency.
- Timezone.
- Freshness.
- Metric version.

Analytics không được tự trở thành source of truth cho nghiệp vụ vận hành.

Official KPI phải đến từ certified metric hoặc approved read model.

Dashboard phải hỗ trợ drill-down đúng phạm vi.

---

# 27. Documents

Documents phải hỗ trợ:

- File object.
- Document metadata.
- Document version.
- Verification.
- OCR/extraction.
- Signature evidence.
- Dossier.
- Secure share.
- Retention.
- Legal hold.

File binary không lưu trực tiếp trong relational database trừ khi có quyết định riêng.

Database lưu metadata và storage reference.

---

# 28. Audit và kiểm soát nội bộ

Sensitive actions phải có Audit.

Các nhóm hành động có thể gồm:

- Customer identity changes.
- Shared phone exception.
- Assignment và transfer.
- Ownership changes.
- Selling-right changes.
- Listing activation.
- Price changes.
- Commercial Lock.
- Booking.
- Contract.
- Payment allocation.
- Receipt issue/cancel-replace.
- Refund.
- Settlement.
- Revenue.
- Commission.
- Clawback.
- Export.
- Break-glass.
- Data repair.

Exact Audit event inventory thuộc Audit Context Pack.

---

# 29. Security và bảo vệ dữ liệu

Nguyên tắc:

- Backend là security boundary.
- Deny by default.
- Least privilege.
- Scope enforce ở backend và database query.
- Field masking trước serialization.
- Export là permission riêng.
- Sensitive reveal có thể cần reauthentication.
- Không tin client-supplied scope, owner, approval hoặc availability.
- Không log secrets hoặc restricted PII.
- Không dùng frontend hiding làm security control.

Exact permission và masking thuộc Registry/Matrix tương ứng.

---

# 30. Cảnh báo và anomaly

Sản phẩm phải có khả năng phát hiện hoặc hỗ trợ reconciliation cho:

- Duplicate Customer.
- Shared phone chưa approved.
- Duplicate Asset.
- Invalid simultaneous Listings.
- Expired mandate.
- Commercial Lock conflict.
- Price/policy hết hiệu lực.
- Contract không khớp Booking.
- Payment over-allocation.
- Collected-on-behalf bị ghi nhầm revenue.
- Invalid settlement.
- Revenue thiếu căn cứ.
- Commission vượt nguồn.
- Co-sale allocation conflict.
- Duplicate payout.
- Unresolved clawback.
- Unauthorized access attempt.
- Abnormal export.
- Self-approval trái policy.

Exact detection mechanism thuộc Context Pack, Observability Catalog và Operations runbooks.

---

# 31. Yêu cầu phi chức năng cấp sản phẩm

## 31.1. Correctness

Critical financial và commercial operations phải bảo toàn integrity.

## 31.2. Idempotency

Critical side-effect operations phải chống duplicate retry.

## 31.3. Concurrency

Commercial Lock, Booking, Payment Allocation, Receipt và các critical state transitions phải có concurrency protection.

## 31.4. Auditability

Sensitive operations phải truy vết được.

## 31.5. Availability và recoverability

Hệ thống phải có backup, restore, reconciliation và incident handling phù hợp.

## 31.6. Performance

Hệ thống phải hỗ trợ:

- Customer search.
- Large inventory filtering.
- Matching.
- Scope-aware dashboards.
- Batch imports.
- Financial reconciliation.

Exact targets thuộc NFR/SLO.

## 31.7. Extensibility

Kiến trúc phải cho phép mở rộng sang:

- Rental.
- Property management.
- Resale.
- Shared investment.
- Multiple currencies.
- Additional Legal Entities.
- Customer portal.
- E-signature.
- Banking integration.
- Accounting integration.
- External inventory integration.

---

# 32. Non-goals

Trong baseline hiện tại, sản phẩm không mặc định:

- Là SaaS multi-tenant cho nhiều doanh nghiệp độc lập.
- Thay thế hoàn toàn ERP hoặc accounting ledger.
- Tự động quyết định tín dụng.
- Tự động phê duyệt financial transaction.
- Dùng AI làm final authority cho matching, permission hoặc financial calculation.
- Xây microservices ngay từ đầu.
- Giữ backward compatibility với CRM cũ nếu không có migration/integration scope được duyệt.
- Lưu mọi binary file trong database.
- Cho phép generic status update với sensitive workflows.

---

# 33. Greenfield và legacy compatibility

`crm_bds_ai` là Greenfield.

Điều đó có nghĩa:

- Repository mới.
- Database mới.
- Migration history mới.
- API contract mới.
- Event contract mới.
- Không mặc định giữ bảng, endpoint, status hoặc alias cũ.
- Không tự tạo compatibility layer.

Legacy data hoặc system cũ chỉ được xử lý khi có:

- Approved migration scope.
- Integration contract.
- Mapping specification.
- Reconciliation plan.
- Acceptance criteria.

Việc tham chiếu tài liệu cũ chỉ nhằm bảo toàn tri thức nghiệp vụ, không tạo nghĩa vụ backward compatibility.

---

# 34. Capability map

Các capability sản phẩm chính:

```text
Platform Configuration
Identity and Access
Party and Customer
Lead Management
Product, Asset and Listing
Matching
Transaction
Contract and Cash
Revenue and Commission
Activity and SLA
Marketing
Analytics
Documents
Audit and Control
Integration
Operations
```

Capability name là stable business/technical identifier.

Không dùng module number làm identity chính.

---

# 35. Acceptance cấp sản phẩm

Một feature chỉ phù hợp với Product Direction khi:

- Phục vụ một use case rõ.
- Không phá business invariant.
- Có owner.
- Có security behavior.
- Có data lineage.
- Có failure behavior.
- Có Audit khi nhạy cảm.
- Có acceptance criteria.
- Không tạo source of truth cạnh tranh.
- Không đưa legacy assumption vào Greenfield core.

---

# 36. Conflict protocol

Khi Product Overview xung đột với:

- Product Charter.
- Domain Glossary.
- Context Pack.
- Source of Truth Matrix.
- ADR.
- OpenAPI.
- Database migration.
- Event contract.

Phải:

1. Dừng thay đổi bị ảnh hưởng.
2. Xác định loại conflict.
3. Áp dụng Documentation Governance.
4. Không tự chọn nguồn thuận tiện.
5. Ghi decision hoặc ADR nếu semantics thay đổi.
6. Cập nhật các artifacts liên quan cùng thay đổi.
7. Ghi resolution trong Acceptance Report.

---

# 37. Change Log

## Version 2.1.0 — 2026-07-26

- Tách rõ Product Overview khỏi Architecture và implementation contracts.
- Bỏ module numbering làm identity chính.
- Làm rõ Greenfield không mặc định backward compatibility.
- Giữ các mô hình kinh doanh và business invariants cốt lõi.
- Chuyển exact scope, database, API, Event và Sprint về nguồn canonical tương ứng.
- Làm rõ Enterprise/Legal Entity cần được định nghĩa trong Domain Glossary/ADR.
- Bổ sung non-goals, conflict protocol và source-of-truth matrix.

## Version 2.0

- Mô tả nền tảng CRM bất động sản hợp nhất.
- Bổ sung nhiều mô hình kinh doanh.
- Tách Asset và Listing.
- Tách Ownership và Selling Right.
- Tách Payment, Revenue và Commission.
- Mở rộng Customer 360, Transaction Case và Settlement.

---

# 38. Kết luận

`crm_bds_ai` là một nền tảng điều hành bất động sản hợp nhất, trong đó:

- Một Party có thể có nhiều vai trò.
- Một Customer có thể vừa mua vừa bán.
- Asset có identity độc lập với Listing.
- Ownership độc lập với Selling Right.
- Công ty có thể là developer, seller, distributor, broker hoặc collection agent.
- Transaction có thể có cả buyer-side và seller-side.
- Payment không mặc định là revenue.
- Revenue tách khỏi Internal Commission.
- Receipt đã phát hành được bảo vệ khỏi sửa trực tiếp.
- Customer merge giữ lineage.
- Backend enforce security và commercial integrity.
- Audit, history và reconciliation là bắt buộc đối với nghiệp vụ nhạy cảm.

Tài liệu này trả lời:

> Sản phẩm phải giải quyết vấn đề gì và các business truths nào không được phép hiểu sai.

Tài liệu này không trả lời:

> Exact implementation được xây như thế nào.


# AI product posture

`crm_bds_ai` is AI-ready and Copilot-first while remaining provider/model agnostic. AI augments every relevant capability through controlled use cases, evidence and human approval; owning Contexts remain the only business authorities.
