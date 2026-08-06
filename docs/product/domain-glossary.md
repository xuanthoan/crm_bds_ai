# CRM_BDS_AI — DOMAIN GLOSSARY

**Document ID:** `PROD-GLO-001`  
**Canonical path:** `docs/product/domain-glossary.md`  
**Product:** `crm_bds_ai`  
**Version:** `1.0.0`  
**Status:** `Ready for Review`  
**Owner:** `Product Owner`  
**Reviewers:** `Architecture Owner, Domain Owners, Data Governance Owner`  
**Last reviewed:** `2026-08-05`  
**Classification:** `INTERNAL`


# 1. Mục đích

Tài liệu này khóa nghĩa của các thuật ngữ xuyên suốt `crm_bds_ai`. Mọi Capability Specification, Context Pack, API, Event, Database và UI phải dùng đúng nghĩa tại đây hoặc tạo Change Request trước khi mở rộng nghĩa.

# 2. Quy tắc

- Một thuật ngữ chỉ có một owning Context.
- Không dùng cùng một từ cho hai aggregate khác nhau.
- UI label có thể thân thiện hơn nhưng không được làm mất domain meaning.
- Từ đồng nghĩa phải trỏ về canonical term.
- Exact codes nằm trong registry/machine contract; Glossary khóa business meaning.

# 3. Thuật ngữ canonical

| Thuật ngữ | Định nghĩa | Owner | Không đồng nghĩa |
|---|---|---|---|
| `Enterprise` | Nhóm doanh nghiệp vận hành một hoặc nhiều Legal Entities. | `platform` | Legal Entity |
| `Legal Entity` | Pháp nhân chịu trách nhiệm pháp lý, tài chính và phân quyền trong giao dịch. | `platform` | Department hoặc Project |
| `Business Calendar` | Lịch làm việc có ngày nghỉ, múi giờ và quy tắc tính thời hạn. | `platform` | Calendar UI |
| `Party` | Chủ thể pháp lý hoặc xã hội có thể là cá nhân hay tổ chức. | `party` | Customer |
| `Person` | Party loại cá nhân. | `party` | Workforce Subject |
| `Organization Party` | Party loại tổ chức. | `party` | IAM Organization Unit |
| `Customer Relationship` | Quan hệ nghiệp vụ giữa Enterprise và Party, cho phép Party đóng vai Customer. | `party` | Party identity |
| `Workforce Subject` | Tham chiếu Party/Person được doanh nghiệp sử dụng như nhân sự. | `iam` | Canonical Person identity |
| `Employment Assignment` | Quan hệ làm việc có hiệu lực giữa Workforce Subject, Legal Entity, Org Unit và Position. | `iam` | User Account |
| `User Account` | Danh tính đăng nhập và trạng thái truy cập hệ thống. | `iam` | Party |
| `Lead` | Tín hiệu hoặc cơ hội đầu vào chưa hoàn tất quá trình chuyển đổi thành Customer relationship phù hợp. | `lead` | Customer |
| `Lead Intake` | Quá trình nhận, chuẩn hóa, chống lặp intake và tạo/link Lead. | `lead` | Marketing Capture |
| `Lead Source Snapshot` | Nguồn Lead được Lead Context chấp nhận và đóng băng tại intake. | `lead` | Marketing Attribution |
| `Care Protection` | Quyền chăm sóc có thời hạn đối với Lead, không phải ownership của Customer toàn doanh nghiệp. | `lead` | Customer ownership |
| `Requirement` | Nhu cầu bất động sản có version của Customer/Party. | `party` | Matching Profile |
| `Financial Profile` | Thông tin tài chính phục vụ tư vấn và eligibility, có masking chặt chẽ. | `party` | Payment |
| `Stakeholder` | Party có ảnh hưởng hoặc vai trò trong quyết định của Customer. | `party` | Contract Party |
| `Phone Identity` | Danh tính số điện thoại đã chuẩn hóa dùng để chống trùng và shared-phone governance. | `party` | Contact Point raw |
| `Project` | Dự án bất động sản. | `product` | Sales Campaign |
| `Asset` | Tài sản bất động sản vật lý hoặc pháp lý. | `product` | Listing |
| `Ownership` | Quyền sở hữu của Party đối với Asset. | `product` | Selling Right |
| `Selling Right` | Quyền hợp lệ cho phép một bên chào bán Asset. | `product` | Ownership |
| `Listing` | Đề nghị thương mại đưa Asset ra thị trường theo quyền bán cụ thể. | `product` | Asset |
| `Inventory` | Tập hợp Listing/Asset được quản lý khả dụng cho giao dịch. | `product` | Analytics inventory metric |
| `Availability` | Trạng thái authoritative cho biết Listing có thể tham gia hành động thương mại hay không. | `product` | UI status |
| `Commercial Lock` | Khóa thương mại authoritative bảo vệ Listing khỏi xung đột bán/giữ. | `product` | Hold |
| `Matching Profile` | Biểu diễn chuẩn hóa của Requirement phục vụ Matching. | `matching` | Requirement source |
| `Match Result` | Kết quả eligibility, score, confidence và explanation của một Matching Run. | `matching` | Deal |
| `Shortlist` | Danh sách lựa chọn tư vấn; không giữ hoặc khóa Listing. | `matching` | Commercial Lock |
| `Deal` | Cơ hội thương mại tổng quát với Customer. | `transaction` | Transaction Case |
| `Transaction Case` | Hồ sơ điều phối giao dịch cho một Product/Listing cụ thể. | `transaction` | Contract |
| `Proposal` | Đề xuất thương mại có version gửi cho Customer. | `transaction` | Contract |
| `Negotiation` | Quá trình trao đổi điều khoản trước cam kết. | `transaction` | Amendment |
| `Hold` | Business process yêu cầu và theo dõi Product Commercial Lock. | `transaction` | Commercial Lock aggregate |
| `Booking` | Cam kết tiền hợp đồng và hồ sơ đặt chỗ; không phải Contract. | `transaction` | Contract |
| `Deposit Commitment` | Nghĩa vụ/ý định đặt cọc do Transaction quản lý; không phải Payment hoặc Receipt. | `transaction` | Payment |
| `Contract` | Hồ sơ pháp lý của giao dịch. | `contract` | Booking |
| `Contract Version` | Phiên bản nội dung hợp đồng; bản đã ký phải bất biến. | `contract` | Document Version |
| `Payment Plan` | Kế hoạch nghĩa vụ thanh toán theo Contract. | `contract` | Payment Transaction |
| `Receivable` | Khoản phải thu phát sinh từ căn cứ hợp lệ. | `contract` | Revenue Receivable |
| `Payment Transaction` | Biểu diễn giao dịch tiền trong CRM được xác minh từ nguồn được phép. | `contract` | Receipt |
| `Payment Allocation` | Phân bổ Payment vào một hoặc nhiều nghĩa vụ. | `contract` | Revenue Payment Application |
| `Receipt` | Chứng từ thu có numbering và vòng đời bất biến sau phát hành. | `contract` | Payment |
| `Refund` | Quy trình hoàn tiền có quyết định, thực thi và reconciliation. | `contract` | Payment reversal |
| `Transaction Settlement` | Đối soát và thanh toán tiền giao dịch cho Owner/Developer/Partner. | `contract` | Revenue Recognition |
| `Revenue Arrangement` | Căn cứ thương mại xác định công ty được hưởng doanh thu/phí. | `revenue` | Contract |
| `Revenue Entitlement` | Quyền hưởng doanh thu hình thành theo Arrangement và milestone. | `revenue` | Collected Revenue |
| `Operational Revenue Recognition` | Ghi nhận vận hành trong CRM; không phải bút toán pháp định. | `revenue` | Statutory recognition |
| `Revenue Receivable` | Khoản phải thu doanh thu từ Counterparty. | `revenue` | Buyer Receivable |
| `Commission Entitlement` | Quyền hưởng hoa hồng của Beneficiary theo Plan và Participant Snapshot. | `revenue` | Commission Paid |
| `Vesting` | Điều kiện làm quyền hoa hồng trở nên đủ điều kiện giữ lại. | `revenue` | Recognition |
| `Payable` | Khoản Commission đủ điều kiện đưa vào payout. | `revenue` | Paid |
| `Clawback` | Điều chỉnh/thu hồi quyền lợi đã ghi nhận hoặc đã trả. | `revenue` | Xóa payout history |
| `Task` | Kế hoạch công việc. | `activity` | Interaction |
| `Appointment` | Kế hoạch cuộc gặp. | `activity` | Attendance |
| `Interaction` | Tương tác thực tế với Party/Customer qua một kênh. | `activity` | Marketing Message Intent |
| `Unified Timeline` | Projection permission-aware tổng hợp facts; không phải source of truth. | `activity` | Audit Log |
| `SLA Instance` | Đồng hồ SLA runtime có Definition/Calendar Version. | `activity` | Due date đơn lẻ |
| `Next Best Action` | Khuyến nghị hành động đã qua permission, consent và workflow gates. | `activity` | Autonomous execution |
| `Campaign` | Đơn vị quản trị hoạt động Marketing. | `marketing` | Lead Source Snapshot |
| `Marketing Capture` | Dữ liệu đầu vào từ form, event, partner hoặc platform. | `marketing` | Official Lead |
| `Marketing Touchpoint` | Bằng chứng tiếp xúc Marketing tại một thời điểm. | `marketing` | Canonical Interaction |
| `Audience` | Tập thành viên được đánh giá theo Definition Version và suppression policy. | `marketing` | File số điện thoại |
| `Journey` | Quy trình automation Marketing có version và safety gates. | `marketing` | Business process manager của Context khác |
| `Marketing Attribution` | Phân tích influence/sourcing của Campaign. | `marketing` | Sales Attribution |
| `Semantic Metric` | Định nghĩa Metric có grain, formula, time, access và version. | `analytics` | Widget formula |
| `Analytics Snapshot` | Bản ghi as-of/period-end có lock và restatement. | `analytics` | Source business state |
| `Forecast` | Dự báo có model version, cutoff, horizon và approval state. | `analytics` | Actual |
| `File Object` | Binary object trong Object Storage. | `documents` | Document |
| `Document` | Hồ sơ có meaning, classification và versions. | `documents` | Contract |
| `Document Version` | Phiên bản bất biến của nội dung tài liệu. | `documents` | Contract Version |
| `Dossier` | Tập hồ sơ và checklist phục vụ một mục đích nghiệp vụ. | `documents` | Folder tùy ý |
| `Signature Evidence` | Bằng chứng ký và certificate/provider evidence. | `documents` | Contract effectiveness |
| `Audit Fact` | Bằng chứng bất biến về hành động nhạy cảm hoặc thay đổi nghiệp vụ. | `audit` | Technical log |
| `Connection` | Cấu hình liên kết tới external provider, chỉ lưu secret reference. | `integration` | Credential plain text |
| `Mapping Version` | Phiên bản chuyển đổi dữ liệu provider ↔ canonical contract. | `integration` | Arbitrary transformation code |
| `Webhook Receipt` | Bằng chứng nhận webhook đã verify signature/replay. | `integration` | Business aggregate |
| `Operational Alert` | Signal vận hành cần xử lý. | `operations` | Customer Notification |
| `Notification Orchestration` | Điều phối thông báo sau khi policy/consent hợp lệ. | `operations` | Provider delivery |
| `Data Repair` | Quy trình điều phối sửa dữ liệu có dry run, approval và reconciliation. | `operations` | SQL tùy tiện |
| `Break-glass Session` | Phiên truy cập khẩn cấp có scope, expiry, MFA và review. | `operations` | Emergency authorization grant |

# 4. Quy trình thay đổi

1. Domain Owner tạo đề xuất.
2. Xác định Context owner và impact.
3. Kiểm tra PRD, Capability, Context Pack, API/Event/Database.
4. Review bởi Product Owner và Architecture Owner.
5. Tăng version và cập nhật consumers.

# 5. Acceptance criteria

- Không còn thuật ngữ mơ hồ giữa Hold và Commercial Lock.
- Không đồng nhất Party, Customer, Lead và User Account.
- Không đồng nhất Payment, Receipt, Revenue và Commission.
- Không dùng Timeline hoặc Analytics projection làm source business truth.
