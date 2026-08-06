# CRM_BDS_AI — CANONICAL BUSINESS RULES

**Document ID:** `PROD-CBR-001`  
**Canonical path:** `docs/product/canonical-business-rules.md`  
**Product:** `crm_bds_ai`  
**Version:** `1.0.0`  
**Status:** `Accepted / Foundation Baseline`  
**Owner:** `Product Owner`  
**Effective date:** `2026-08-05`  
**Last reviewed:** `2026-08-05`  
**Classification:** `INTERNAL`

---

# 1. Mục đích

Tài liệu này là baseline tích cực của business truth cho `crm_bds_ai`. Mọi PRD, Capability, Context Pack, API, migration, event, test và AI use case phải truy vết về rule tương ứng.

# 2. Quy tắc giải thích

- Canonical requirement mô tả điều **phải đúng**.
- Anti-pattern mô tả cách triển khai hoặc cách hiểu **bị cấm**.
- Open Decision không được biến thành implementation assumption.
- Exact schema/API/event/permission/state machine thuộc machine contract hoặc Context Pack tương ứng.
- Khi tài liệu mâu thuẫn, Goose phải dừng, ghi conflict và yêu cầu Product/Architecture Owner quyết định; Opencode không được tự hòa giải.

# 3. Canonical rules

| ID | Canonical requirement | Authority | Prohibited anti-pattern |
|---|---|---|---|
| `CBR-001` | Customer identity là enterprise-global; không tạo Customer master theo team, dự án hoặc chiến dịch. | `party` | Customer master per team/project |
| `CBR-002` | Phone Identity là authority chính thức để xác định duplicate; email, Zalo, Facebook, tên hoặc địa chỉ chỉ tạo review signal. | `party` | Tự merge vì tên/email/địa chỉ giống nhau |
| `CBR-003` | Một Customer có danh sách số điện thoại mở rộng; không giới hạn cứng hai số. | `party` | Thiết kế phone_1/phone_2 cố định |
| `CBR-004` | Customer thuộc doanh nghiệp; quyền nhìn thấy và chăm sóc được giải quyết bằng effective scope và assignment/protection policy. | `party + lead + iam` | Gán quyền sở hữu tuyệt đối cho cá nhân/team |
| `CBR-005` | Authorization, scope và field masking phải được enforce ở backend cho mọi API, job, export và AI use case. | `iam + owning context` | Chỉ ẩn nút ở frontend |
| `CBR-006` | Sale, Team Lead và Sales Manager không được export customer/project/property datasets; Director và Accounting chỉ export khi có grant và Audit. | `iam + audit` | Cho export theo màn hình hoặc role suy đoán |
| `CBR-007` | Mọi export phải ghi mục đích, loại dữ liệu, scope, người yêu cầu, thời gian, kết quả và evidence. | `audit` | Export không audit hoặc chỉ log tên file |
| `CBR-008` | SLA baseline là cấu hình versioned: Lead mới 2 giờ; lịch hẹn sắp tới trong 24 giờ; Deal hoạt động 24 giờ; Booking/cọc/hợp đồng trong ngày; dữ liệu còn lại 3 ngày. | `platform + activity` | Hard-code SLA trong UI/service |
| `CBR-009` | Một Customer có thể Booking nhiều Listing khi từng Booking vượt invariant độc lập. | `transaction` | Giới hạn một Customer chỉ có một Booking |
| `CBR-010` | Hold duration, điều kiện tiền để lock, quyền force-release và discount authority là Open Decisions; Agent không được tự chọn. | `transaction + product + platform` | Tự đặt thời hạn hoặc người duyệt |
| `CBR-011` | Product Context là authority duy nhất cho Availability và Commercial Lock. | `product` | Transaction/Matching tự đổi availability |
| `CBR-012` | Shortlist, selected Listing, Proposal hoặc AI recommendation không tự tạo Commercial Lock. | `matching + transaction` | Chọn sản phẩm đồng nghĩa giữ căn |
| `CBR-013` | Booking không phải Contract; Fully Signed không mặc định Effective; Fully Paid không mặc định Completed. | `transaction + contract` | Gộp các trạng thái thành một boolean |
| `CBR-014` | Payment, Payment Allocation và Receipt là records khác nhau với lineage rõ ràng. | `contract` | Một bảng transaction tài chính chung |
| `CBR-015` | Issued Receipt và signed/verified records bất biến; correction tạo record/version mới có liên kết. | `contract + documents` | UPDATE/DELETE record đã phát hành |
| `CBR-016` | Gross funds, Revenue, Commission Entitlement, Payable và Paid là các lớp nghiệp vụ riêng. | `revenue` | Payment đồng nghĩa Revenue/Commission |
| `CBR-017` | Commission được ghi nhận theo milestone được phê duyệt; payout phụ thuộc funding/collection policy và external execution confirmation. | `revenue` | Ký hợp đồng là trả commission ngay |
| `CBR-018` | Co-sale dùng Agreement Version có tỷ lệ, hiệu lực, phê duyệt và evidence; không suy ra từ Activity hoặc ghi chú. | `transaction + revenue` | Đọc note để tính co-sale |
| `CBR-019` | Xử lý commission khi khách hủy là Open Decision; chưa có quyết định thì không tự clawback/waive. | `revenue + contract` | Agent tự chọn chính sách hủy |
| `CBR-020` | Task là kế hoạch; Task completion không tự tạo Interaction hoặc business transition. | `activity` | Hoàn thành task đồng nghĩa đã gọi/đã gặp |
| `CBR-021` | Outbound phải re-check consent, restriction, suppression, frequency, quiet hours và workflow tại thời điểm thực thi. | `party + marketing + activity` | Kiểm tra consent chỉ lúc tạo campaign |
| `CBR-022` | Analytics read-only đối với business truth; Snapshot, Forecast và Dashboard không sửa source aggregates. | `analytics` | Dashboard ghi ngược vào nghiệp vụ |
| `CBR-023` | Audit append-only; correction tạo fact mới, không sửa/xóa fact cũ. | `audit` | Cho phép sửa audit log |
| `CBR-024` | Integration vận chuyển, chuẩn hóa và reconcile; không tự quyết định source of truth hoặc business transition. | `integration` | Connector trực tiếp cập nhật state tùy ý |
| `CBR-025` | Legal Entity hỗ trợ mô hình môi giới phân phối, chủ đầu tư nội bộ, bán hộ và đất nền; rule khác biệt phải cấu hình/version. | `platform + product + transaction` | Hard-code một mô hình kinh doanh |
| `CBR-026` | Accounting và Finance có thể gộp hoặc tách theo cấu hình tổ chức; quyền không được gắn cứng vào một chức danh. | `iam + platform` | Hard-code role AccountingFinance |
| `CBR-AI-001` | AI là năng lực hỗ trợ xuyên Context; AI không sở hữu business truth và không tạo Bounded Context thay thế owning Context. | `platform + integration + operations + audit` | Tạo AI module sở hữu dữ liệu nghiệp vụ |
| `CBR-AI-002` | Business code phụ thuộc AI capability/use case contract, không phụ thuộc provider, model, SDK hoặc endpoint cụ thể. | `architecture` | Hard-code nhà cung cấp/model trong Lead/Customer/Deal |
| `CBR-AI-003` | Provider và model được đăng ký động qua Provider Registry, Model Registry và Adapter Manifest. | `platform + integration` | Tên model nằm trong source code |
| `CBR-AI-004` | AI chỉ đọc dữ liệu sau authorization, scope, purpose và masking; cloud/local routing tuân thủ data-classification policy. | `iam + security` | Đưa raw Customer 360 vào model |
| `CBR-AI-005` | AI output là suggestion/draft/extraction/forecast; high-impact command bắt buộc human approval và backend invariant check. | `owning context + audit` | AI tự merge, lock, pay, issue, approve hoặc delete |
| `CBR-AI-006` | AI không truy cập database/repository trực tiếp; tool call đi qua Tool Guard và canonical Context API. | `architecture + security` | Cấp SQL/database tool cho model |
| `CBR-AI-007` | Mọi structured output phải validate schema, allowed values, references, evidence và confidence trước khi sử dụng. | `operations + owning context` | Parse text tự do rồi ghi database |
| `CBR-AI-008` | AI provider/model failure không được làm dừng Core CRM; phải có timeout, circuit breaker, manual fallback và feature flag. | `operations` | Business transaction phụ thuộc bắt buộc vào AI |
| `CBR-AI-009` | RAG do CRM kiểm soát permission-aware retrieval; dữ liệu thời gian thực phải query owning Context, không suy từ vector index. | `documents + analytics + owning context` | Dùng vector store làm source of truth |
| `CBR-AI-010` | Embedding model, dimension, chunking và index phải version; đổi model tạo index mới và có rollback. | `documents + operations` | Đổi embedding model tại chỗ |
| `CBR-AI-011` | Prompt, tool, model, provider, routing policy và output schema đều versioned và audit được. | `platform + audit` | Prompt/model cấu hình vô danh |
| `CBR-AI-012` | Provider mới phải qua conformance, security, privacy, quality và cost gates trước ACTIVE. | `integration + security + operations` | Nhập URL/API key và dùng production ngay |

# 4. Acceptance rule

Một business feature không được ACCEPTED nếu:

1. Không trỏ tới ít nhất một canonical business rule hoặc requirement ID.
2. Chứa anti-pattern đã liệt kê.
3. Tự quyết định nội dung đang có trạng thái Open Decision.
4. Không có negative tests chứng minh anti-pattern bị chặn.
5. AI output được dùng như business truth mà không có validation/approval theo policy.
