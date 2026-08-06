# CRM_BDS_AI — BUSINESS RULE ANTI-PATTERNS

**Document ID:** `PROD-ANT-001`  
**Canonical path:** `docs/product/business-rule-anti-patterns.md`  
**Product:** `crm_bds_ai`  
**Version:** `1.0.0`  
**Status:** `Accepted / Foundation Baseline`  
**Owner:** `Product Owner`  
**Effective date:** `2026-08-05`  
**Last reviewed:** `2026-08-05`  
**Classification:** `INTERNAL`

---

# 1. Mục đích

Danh mục này biến các cách hiểu sai phổ biến thành điều cấm có thể kiểm thử. Anti-pattern không phải backlog tùy chọn; chúng là negative requirements.

# 2. Anti-pattern registry

| Anti-pattern ID | Prohibited behavior | Canonical replacement | Required test evidence |
|---|---|---|---|
| `AP-001` | Customer master per team/project | Enforce `CBR-001`: Customer identity là enterprise-global; không tạo Customer master theo team, dự án hoặc chiến dịch. | Negative test + authorization/invariant/audit evidence as applicable |
| `AP-002` | Tự merge vì tên/email/địa chỉ giống nhau | Enforce `CBR-002`: Phone Identity là authority chính thức để xác định duplicate; email, Zalo, Facebook, tên hoặc địa chỉ chỉ tạo review signal. | Negative test + authorization/invariant/audit evidence as applicable |
| `AP-003` | Thiết kế phone_1/phone_2 cố định | Enforce `CBR-003`: Một Customer có danh sách số điện thoại mở rộng; không giới hạn cứng hai số. | Negative test + authorization/invariant/audit evidence as applicable |
| `AP-004` | Gán quyền sở hữu tuyệt đối cho cá nhân/team | Enforce `CBR-004`: Customer thuộc doanh nghiệp; quyền nhìn thấy và chăm sóc được giải quyết bằng effective scope và assignment/protection policy. | Negative test + authorization/invariant/audit evidence as applicable |
| `AP-005` | Chỉ ẩn nút ở frontend | Enforce `CBR-005`: Authorization, scope và field masking phải được enforce ở backend cho mọi API, job, export và AI use case. | Negative test + authorization/invariant/audit evidence as applicable |
| `AP-006` | Cho export theo màn hình hoặc role suy đoán | Enforce `CBR-006`: Sale, Team Lead và Sales Manager không được export customer/project/property datasets; Director và Accounting chỉ export khi có grant và Audit. | Negative test + authorization/invariant/audit evidence as applicable |
| `AP-007` | Export không audit hoặc chỉ log tên file | Enforce `CBR-007`: Mọi export phải ghi mục đích, loại dữ liệu, scope, người yêu cầu, thời gian, kết quả và evidence. | Negative test + authorization/invariant/audit evidence as applicable |
| `AP-008` | Hard-code SLA trong UI/service | Enforce `CBR-008`: SLA baseline là cấu hình versioned: Lead mới 2 giờ; lịch hẹn sắp tới trong 24 giờ; Deal hoạt động 24 giờ; Booking/cọc/hợp đồng trong ngày; dữ liệu còn lại 3 ngày. | Negative test + authorization/invariant/audit evidence as applicable |
| `AP-009` | Giới hạn một Customer chỉ có một Booking | Enforce `CBR-009`: Một Customer có thể Booking nhiều Listing khi từng Booking vượt invariant độc lập. | Negative test + authorization/invariant/audit evidence as applicable |
| `AP-010` | Tự đặt thời hạn hoặc người duyệt | Enforce `CBR-010`: Hold duration, điều kiện tiền để lock, quyền force-release và discount authority là Open Decisions; Agent không được tự chọn. | Negative test + authorization/invariant/audit evidence as applicable |
| `AP-011` | Transaction/Matching tự đổi availability | Enforce `CBR-011`: Product Context là authority duy nhất cho Availability và Commercial Lock. | Negative test + authorization/invariant/audit evidence as applicable |
| `AP-012` | Chọn sản phẩm đồng nghĩa giữ căn | Enforce `CBR-012`: Shortlist, selected Listing, Proposal hoặc AI recommendation không tự tạo Commercial Lock. | Negative test + authorization/invariant/audit evidence as applicable |
| `AP-013` | Gộp các trạng thái thành một boolean | Enforce `CBR-013`: Booking không phải Contract; Fully Signed không mặc định Effective; Fully Paid không mặc định Completed. | Negative test + authorization/invariant/audit evidence as applicable |
| `AP-014` | Một bảng transaction tài chính chung | Enforce `CBR-014`: Payment, Payment Allocation và Receipt là records khác nhau với lineage rõ ràng. | Negative test + authorization/invariant/audit evidence as applicable |
| `AP-015` | UPDATE/DELETE record đã phát hành | Enforce `CBR-015`: Issued Receipt và signed/verified records bất biến; correction tạo record/version mới có liên kết. | Negative test + authorization/invariant/audit evidence as applicable |
| `AP-016` | Payment đồng nghĩa Revenue/Commission | Enforce `CBR-016`: Gross funds, Revenue, Commission Entitlement, Payable và Paid là các lớp nghiệp vụ riêng. | Negative test + authorization/invariant/audit evidence as applicable |
| `AP-017` | Ký hợp đồng là trả commission ngay | Enforce `CBR-017`: Commission được ghi nhận theo milestone được phê duyệt; payout phụ thuộc funding/collection policy và external execution confirmation. | Negative test + authorization/invariant/audit evidence as applicable |
| `AP-018` | Đọc note để tính co-sale | Enforce `CBR-018`: Co-sale dùng Agreement Version có tỷ lệ, hiệu lực, phê duyệt và evidence; không suy ra từ Activity hoặc ghi chú. | Negative test + authorization/invariant/audit evidence as applicable |
| `AP-019` | Agent tự chọn chính sách hủy | Enforce `CBR-019`: Xử lý commission khi khách hủy là Open Decision; chưa có quyết định thì không tự clawback/waive. | Negative test + authorization/invariant/audit evidence as applicable |
| `AP-020` | Hoàn thành task đồng nghĩa đã gọi/đã gặp | Enforce `CBR-020`: Task là kế hoạch; Task completion không tự tạo Interaction hoặc business transition. | Negative test + authorization/invariant/audit evidence as applicable |
| `AP-021` | Kiểm tra consent chỉ lúc tạo campaign | Enforce `CBR-021`: Outbound phải re-check consent, restriction, suppression, frequency, quiet hours và workflow tại thời điểm thực thi. | Negative test + authorization/invariant/audit evidence as applicable |
| `AP-022` | Dashboard ghi ngược vào nghiệp vụ | Enforce `CBR-022`: Analytics read-only đối với business truth; Snapshot, Forecast và Dashboard không sửa source aggregates. | Negative test + authorization/invariant/audit evidence as applicable |
| `AP-023` | Cho phép sửa audit log | Enforce `CBR-023`: Audit append-only; correction tạo fact mới, không sửa/xóa fact cũ. | Negative test + authorization/invariant/audit evidence as applicable |
| `AP-024` | Connector trực tiếp cập nhật state tùy ý | Enforce `CBR-024`: Integration vận chuyển, chuẩn hóa và reconcile; không tự quyết định source of truth hoặc business transition. | Negative test + authorization/invariant/audit evidence as applicable |
| `AP-025` | Hard-code một mô hình kinh doanh | Enforce `CBR-025`: Legal Entity hỗ trợ mô hình môi giới phân phối, chủ đầu tư nội bộ, bán hộ và đất nền; rule khác biệt phải cấu hình/version. | Negative test + authorization/invariant/audit evidence as applicable |
| `AP-026` | Hard-code role AccountingFinance | Enforce `CBR-026`: Accounting và Finance có thể gộp hoặc tách theo cấu hình tổ chức; quyền không được gắn cứng vào một chức danh. | Negative test + authorization/invariant/audit evidence as applicable |
| `AP-027` | Tạo AI module sở hữu dữ liệu nghiệp vụ | Enforce `CBR-AI-001`: AI là năng lực hỗ trợ xuyên Context; AI không sở hữu business truth và không tạo Bounded Context thay thế owning Context. | Negative test + authorization/invariant/audit evidence as applicable |
| `AP-028` | Hard-code nhà cung cấp/model trong Lead/Customer/Deal | Enforce `CBR-AI-002`: Business code phụ thuộc AI capability/use case contract, không phụ thuộc provider, model, SDK hoặc endpoint cụ thể. | Negative test + authorization/invariant/audit evidence as applicable |
| `AP-029` | Tên model nằm trong source code | Enforce `CBR-AI-003`: Provider và model được đăng ký động qua Provider Registry, Model Registry và Adapter Manifest. | Negative test + authorization/invariant/audit evidence as applicable |
| `AP-030` | Đưa raw Customer 360 vào model | Enforce `CBR-AI-004`: AI chỉ đọc dữ liệu sau authorization, scope, purpose và masking; cloud/local routing tuân thủ data-classification policy. | Negative test + authorization/invariant/audit evidence as applicable |
| `AP-031` | AI tự merge, lock, pay, issue, approve hoặc delete | Enforce `CBR-AI-005`: AI output là suggestion/draft/extraction/forecast; high-impact command bắt buộc human approval và backend invariant check. | Negative test + authorization/invariant/audit evidence as applicable |
| `AP-032` | Cấp SQL/database tool cho model | Enforce `CBR-AI-006`: AI không truy cập database/repository trực tiếp; tool call đi qua Tool Guard và canonical Context API. | Negative test + authorization/invariant/audit evidence as applicable |
| `AP-033` | Parse text tự do rồi ghi database | Enforce `CBR-AI-007`: Mọi structured output phải validate schema, allowed values, references, evidence và confidence trước khi sử dụng. | Negative test + authorization/invariant/audit evidence as applicable |
| `AP-034` | Business transaction phụ thuộc bắt buộc vào AI | Enforce `CBR-AI-008`: AI provider/model failure không được làm dừng Core CRM; phải có timeout, circuit breaker, manual fallback và feature flag. | Negative test + authorization/invariant/audit evidence as applicable |
| `AP-035` | Dùng vector store làm source of truth | Enforce `CBR-AI-009`: RAG do CRM kiểm soát permission-aware retrieval; dữ liệu thời gian thực phải query owning Context, không suy từ vector index. | Negative test + authorization/invariant/audit evidence as applicable |
| `AP-036` | Đổi embedding model tại chỗ | Enforce `CBR-AI-010`: Embedding model, dimension, chunking và index phải version; đổi model tạo index mới và có rollback. | Negative test + authorization/invariant/audit evidence as applicable |
| `AP-037` | Prompt/model cấu hình vô danh | Enforce `CBR-AI-011`: Prompt, tool, model, provider, routing policy và output schema đều versioned và audit được. | Negative test + authorization/invariant/audit evidence as applicable |
| `AP-038` | Nhập URL/API key và dùng production ngay | Enforce `CBR-AI-012`: Provider mới phải qua conformance, security, privacy, quality và cost gates trước ACTIVE. | Negative test + authorization/invariant/audit evidence as applicable |

# 3. Agent protocol

- Goose phải đưa anti-pattern liên quan vào acceptance checklist.
- Opencode phải ghi test name/evidence cho từng anti-pattern chịu ảnh hưởng.
- Không được đánh dấu `IMPLEMENTED` khi chỉ có happy-path test.
- Không được đổi business rule để phù hợp code đã viết.
