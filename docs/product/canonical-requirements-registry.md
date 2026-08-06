# CRM_BDS_AI — CANONICAL REQUIREMENTS REGISTRY

**Document ID:** `PROD-CRR-001`  
**Canonical path:** `docs/product/canonical-requirements-registry.md`  
**Product:** `crm_bds_ai`  
**Version:** `1.0.0`  
**Status:** `Accepted / Foundation Baseline`  
**Owner:** `Product Owner`  
**Effective date:** `2026-08-05`  
**Last reviewed:** `2026-08-05`  
**Classification:** `INTERNAL`

---

# 1. Requirement hierarchy

```text
Product Overview / PRD
→ Canonical Business Rules
→ Capability Specifications
→ Context Implementation Packs
→ Accepted ADRs and registries
→ Exact machine contracts
→ Sprint execution pack
→ automated/manual acceptance evidence
```

# 2. Canonical requirements

| Requirement ID | Requirement | Canonical source | Exact implementation source | Acceptance evidence |
|---|---|---|---|---|
| `CBR-001` | Customer identity là enterprise-global; không tạo Customer master theo team, dự án hoặc chiến dịch. | `canonical-business-rules.md` + relevant PRD/Capability | Context Pack + OpenAPI/Alembic/AsyncAPI/registry | Positive test + anti-pattern negative test + Audit where applicable |
| `CBR-002` | Phone Identity là authority chính thức để xác định duplicate; email, Zalo, Facebook, tên hoặc địa chỉ chỉ tạo review signal. | `canonical-business-rules.md` + relevant PRD/Capability | Context Pack + OpenAPI/Alembic/AsyncAPI/registry | Positive test + anti-pattern negative test + Audit where applicable |
| `CBR-003` | Một Customer có danh sách số điện thoại mở rộng; không giới hạn cứng hai số. | `canonical-business-rules.md` + relevant PRD/Capability | Context Pack + OpenAPI/Alembic/AsyncAPI/registry | Positive test + anti-pattern negative test + Audit where applicable |
| `CBR-004` | Customer thuộc doanh nghiệp; quyền nhìn thấy và chăm sóc được giải quyết bằng effective scope và assignment/protection policy. | `canonical-business-rules.md` + relevant PRD/Capability | Context Pack + OpenAPI/Alembic/AsyncAPI/registry | Positive test + anti-pattern negative test + Audit where applicable |
| `CBR-005` | Authorization, scope và field masking phải được enforce ở backend cho mọi API, job, export và AI use case. | `canonical-business-rules.md` + relevant PRD/Capability | Context Pack + OpenAPI/Alembic/AsyncAPI/registry | Positive test + anti-pattern negative test + Audit where applicable |
| `CBR-006` | Sale, Team Lead và Sales Manager không được export customer/project/property datasets; Director và Accounting chỉ export khi có grant và Audit. | `canonical-business-rules.md` + relevant PRD/Capability | Context Pack + OpenAPI/Alembic/AsyncAPI/registry | Positive test + anti-pattern negative test + Audit where applicable |
| `CBR-007` | Mọi export phải ghi mục đích, loại dữ liệu, scope, người yêu cầu, thời gian, kết quả và evidence. | `canonical-business-rules.md` + relevant PRD/Capability | Context Pack + OpenAPI/Alembic/AsyncAPI/registry | Positive test + anti-pattern negative test + Audit where applicable |
| `CBR-008` | SLA baseline là cấu hình versioned: Lead mới 2 giờ; lịch hẹn sắp tới trong 24 giờ; Deal hoạt động 24 giờ; Booking/cọc/hợp đồng trong ngày; dữ liệu còn lại 3 ngày. | `canonical-business-rules.md` + relevant PRD/Capability | Context Pack + OpenAPI/Alembic/AsyncAPI/registry | Positive test + anti-pattern negative test + Audit where applicable |
| `CBR-009` | Một Customer có thể Booking nhiều Listing khi từng Booking vượt invariant độc lập. | `canonical-business-rules.md` + relevant PRD/Capability | Context Pack + OpenAPI/Alembic/AsyncAPI/registry | Positive test + anti-pattern negative test + Audit where applicable |
| `CBR-010` | Hold duration, điều kiện tiền để lock, quyền force-release và discount authority là Open Decisions; Agent không được tự chọn. | `canonical-business-rules.md` + relevant PRD/Capability | Context Pack + OpenAPI/Alembic/AsyncAPI/registry | Positive test + anti-pattern negative test + Audit where applicable |
| `CBR-011` | Product Context là authority duy nhất cho Availability và Commercial Lock. | `canonical-business-rules.md` + relevant PRD/Capability | Context Pack + OpenAPI/Alembic/AsyncAPI/registry | Positive test + anti-pattern negative test + Audit where applicable |
| `CBR-012` | Shortlist, selected Listing, Proposal hoặc AI recommendation không tự tạo Commercial Lock. | `canonical-business-rules.md` + relevant PRD/Capability | Context Pack + OpenAPI/Alembic/AsyncAPI/registry | Positive test + anti-pattern negative test + Audit where applicable |
| `CBR-013` | Booking không phải Contract; Fully Signed không mặc định Effective; Fully Paid không mặc định Completed. | `canonical-business-rules.md` + relevant PRD/Capability | Context Pack + OpenAPI/Alembic/AsyncAPI/registry | Positive test + anti-pattern negative test + Audit where applicable |
| `CBR-014` | Payment, Payment Allocation và Receipt là records khác nhau với lineage rõ ràng. | `canonical-business-rules.md` + relevant PRD/Capability | Context Pack + OpenAPI/Alembic/AsyncAPI/registry | Positive test + anti-pattern negative test + Audit where applicable |
| `CBR-015` | Issued Receipt và signed/verified records bất biến; correction tạo record/version mới có liên kết. | `canonical-business-rules.md` + relevant PRD/Capability | Context Pack + OpenAPI/Alembic/AsyncAPI/registry | Positive test + anti-pattern negative test + Audit where applicable |
| `CBR-016` | Gross funds, Revenue, Commission Entitlement, Payable và Paid là các lớp nghiệp vụ riêng. | `canonical-business-rules.md` + relevant PRD/Capability | Context Pack + OpenAPI/Alembic/AsyncAPI/registry | Positive test + anti-pattern negative test + Audit where applicable |
| `CBR-017` | Commission được ghi nhận theo milestone được phê duyệt; payout phụ thuộc funding/collection policy và external execution confirmation. | `canonical-business-rules.md` + relevant PRD/Capability | Context Pack + OpenAPI/Alembic/AsyncAPI/registry | Positive test + anti-pattern negative test + Audit where applicable |
| `CBR-018` | Co-sale dùng Agreement Version có tỷ lệ, hiệu lực, phê duyệt và evidence; không suy ra từ Activity hoặc ghi chú. | `canonical-business-rules.md` + relevant PRD/Capability | Context Pack + OpenAPI/Alembic/AsyncAPI/registry | Positive test + anti-pattern negative test + Audit where applicable |
| `CBR-019` | Xử lý commission khi khách hủy là Open Decision; chưa có quyết định thì không tự clawback/waive. | `canonical-business-rules.md` + relevant PRD/Capability | Context Pack + OpenAPI/Alembic/AsyncAPI/registry | Positive test + anti-pattern negative test + Audit where applicable |
| `CBR-020` | Task là kế hoạch; Task completion không tự tạo Interaction hoặc business transition. | `canonical-business-rules.md` + relevant PRD/Capability | Context Pack + OpenAPI/Alembic/AsyncAPI/registry | Positive test + anti-pattern negative test + Audit where applicable |
| `CBR-021` | Outbound phải re-check consent, restriction, suppression, frequency, quiet hours và workflow tại thời điểm thực thi. | `canonical-business-rules.md` + relevant PRD/Capability | Context Pack + OpenAPI/Alembic/AsyncAPI/registry | Positive test + anti-pattern negative test + Audit where applicable |
| `CBR-022` | Analytics read-only đối với business truth; Snapshot, Forecast và Dashboard không sửa source aggregates. | `canonical-business-rules.md` + relevant PRD/Capability | Context Pack + OpenAPI/Alembic/AsyncAPI/registry | Positive test + anti-pattern negative test + Audit where applicable |
| `CBR-023` | Audit append-only; correction tạo fact mới, không sửa/xóa fact cũ. | `canonical-business-rules.md` + relevant PRD/Capability | Context Pack + OpenAPI/Alembic/AsyncAPI/registry | Positive test + anti-pattern negative test + Audit where applicable |
| `CBR-024` | Integration vận chuyển, chuẩn hóa và reconcile; không tự quyết định source of truth hoặc business transition. | `canonical-business-rules.md` + relevant PRD/Capability | Context Pack + OpenAPI/Alembic/AsyncAPI/registry | Positive test + anti-pattern negative test + Audit where applicable |
| `CBR-025` | Legal Entity hỗ trợ mô hình môi giới phân phối, chủ đầu tư nội bộ, bán hộ và đất nền; rule khác biệt phải cấu hình/version. | `canonical-business-rules.md` + relevant PRD/Capability | Context Pack + OpenAPI/Alembic/AsyncAPI/registry | Positive test + anti-pattern negative test + Audit where applicable |
| `CBR-026` | Accounting và Finance có thể gộp hoặc tách theo cấu hình tổ chức; quyền không được gắn cứng vào một chức danh. | `canonical-business-rules.md` + relevant PRD/Capability | Context Pack + OpenAPI/Alembic/AsyncAPI/registry | Positive test + anti-pattern negative test + Audit where applicable |
| `CBR-AI-001` | AI là năng lực hỗ trợ xuyên Context; AI không sở hữu business truth và không tạo Bounded Context thay thế owning Context. | `canonical-business-rules.md` + relevant PRD/Capability | Context Pack + OpenAPI/Alembic/AsyncAPI/registry | Positive test + anti-pattern negative test + Audit where applicable |
| `CBR-AI-002` | Business code phụ thuộc AI capability/use case contract, không phụ thuộc provider, model, SDK hoặc endpoint cụ thể. | `canonical-business-rules.md` + relevant PRD/Capability | Context Pack + OpenAPI/Alembic/AsyncAPI/registry | Positive test + anti-pattern negative test + Audit where applicable |
| `CBR-AI-003` | Provider và model được đăng ký động qua Provider Registry, Model Registry và Adapter Manifest. | `canonical-business-rules.md` + relevant PRD/Capability | Context Pack + OpenAPI/Alembic/AsyncAPI/registry | Positive test + anti-pattern negative test + Audit where applicable |
| `CBR-AI-004` | AI chỉ đọc dữ liệu sau authorization, scope, purpose và masking; cloud/local routing tuân thủ data-classification policy. | `canonical-business-rules.md` + relevant PRD/Capability | Context Pack + OpenAPI/Alembic/AsyncAPI/registry | Positive test + anti-pattern negative test + Audit where applicable |
| `CBR-AI-005` | AI output là suggestion/draft/extraction/forecast; high-impact command bắt buộc human approval và backend invariant check. | `canonical-business-rules.md` + relevant PRD/Capability | Context Pack + OpenAPI/Alembic/AsyncAPI/registry | Positive test + anti-pattern negative test + Audit where applicable |
| `CBR-AI-006` | AI không truy cập database/repository trực tiếp; tool call đi qua Tool Guard và canonical Context API. | `canonical-business-rules.md` + relevant PRD/Capability | Context Pack + OpenAPI/Alembic/AsyncAPI/registry | Positive test + anti-pattern negative test + Audit where applicable |
| `CBR-AI-007` | Mọi structured output phải validate schema, allowed values, references, evidence và confidence trước khi sử dụng. | `canonical-business-rules.md` + relevant PRD/Capability | Context Pack + OpenAPI/Alembic/AsyncAPI/registry | Positive test + anti-pattern negative test + Audit where applicable |
| `CBR-AI-008` | AI provider/model failure không được làm dừng Core CRM; phải có timeout, circuit breaker, manual fallback và feature flag. | `canonical-business-rules.md` + relevant PRD/Capability | Context Pack + OpenAPI/Alembic/AsyncAPI/registry | Positive test + anti-pattern negative test + Audit where applicable |
| `CBR-AI-009` | RAG do CRM kiểm soát permission-aware retrieval; dữ liệu thời gian thực phải query owning Context, không suy từ vector index. | `canonical-business-rules.md` + relevant PRD/Capability | Context Pack + OpenAPI/Alembic/AsyncAPI/registry | Positive test + anti-pattern negative test + Audit where applicable |
| `CBR-AI-010` | Embedding model, dimension, chunking và index phải version; đổi model tạo index mới và có rollback. | `canonical-business-rules.md` + relevant PRD/Capability | Context Pack + OpenAPI/Alembic/AsyncAPI/registry | Positive test + anti-pattern negative test + Audit where applicable |
| `CBR-AI-011` | Prompt, tool, model, provider, routing policy và output schema đều versioned và audit được. | `canonical-business-rules.md` + relevant PRD/Capability | Context Pack + OpenAPI/Alembic/AsyncAPI/registry | Positive test + anti-pattern negative test + Audit where applicable |
| `CBR-AI-012` | Provider mới phải qua conformance, security, privacy, quality và cost gates trước ACTIVE. | `canonical-business-rules.md` + relevant PRD/Capability | Context Pack + OpenAPI/Alembic/AsyncAPI/registry | Positive test + anti-pattern negative test + Audit where applicable |

# 3. Change control

Thay đổi requirement phải cập nhật đồng thời: rule ID, affected capabilities, owning Context, Open Decision/ADR khi cần, migrations/contracts, tests, roadmap và change log. Không được đổi nghĩa bằng cách chỉ sửa prompt AI, UI copy hoặc code branch.
