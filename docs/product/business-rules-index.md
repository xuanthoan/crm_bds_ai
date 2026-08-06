# CRM_BDS_AI — BUSINESS RULES INDEX

**Document ID:** `PROD-BRI-001`  
**Canonical path:** `docs/product/business-rules-index.md`  
**Product:** `crm_bds_ai`  
**Version:** `1.0.0`  
**Status:** `Ready for Review / Foundation Baseline`  
**Owner:** `Product Owner`  
**Effective date:** `2026-08-05`  
**Last reviewed:** `2026-08-05`  
**Classification:** `INTERNAL`

---

# 1. Mục đích

Index này giúp Goose tìm nhanh rule; nguồn đầy đủ vẫn là PRD, Capability Specification và owning Context Pack.

# 2. Rules cấp cao

| ID | Rule | Owner |
|---|---|---|
| BR-PAR-001 | Customer identity là enterprise-global; không tạo Customer master theo team/project. | `party` |
| BR-PAR-002 | Duplicate authority dựa trên Phone Identity; email/Zalo/Facebook/tên/địa chỉ không tự kết luận duplicate. | `party` |
| BR-SEC-001 | Sale chỉ thấy Lead/Customer trong effective scope của mình; Team Lead thấy team; manager thấy department; Director thấy enterprise theo grant. | `iam` + owning Context |
| BR-SEC-002 | Sale, Team Lead và Sales Manager không export customer/project/property datasets; Director và Accounting được export khi có grant và Audit. | Security policy |
| BR-PRO-001 | Product Context là authority duy nhất cho Availability và Commercial Lock. | `product` |
| BR-TRA-001 | Selected Listing hoặc Shortlist không tự tạo Commercial Lock. | `transaction`/`matching` |
| BR-TRA-002 | Một Customer có thể Booking nhiều Listing khi mỗi Booking vượt invariant độc lập. | `transaction` |
| BR-CON-001 | Payment, Allocation và Receipt là records riêng; issued Receipt không sửa tại chỗ. | `contract` |
| BR-CON-002 | Booking không phải Contract; Fully Signed không mặc định Effective; Fully Paid không mặc định Completed. | `contract` |
| BR-REV-001 | Gross funds, Revenue, Commission Entitlement, Payable và Paid là các lớp riêng. | `revenue` |
| BR-REV-002 | Commission ghi nhận theo milestone được phê duyệt; payout phụ thuộc funding/collection policy và external execution confirmation. | `revenue` |
| BR-REV-003 | Co-sale dùng structured Agreement Version; không suy ra từ Activity. | `transaction`/`revenue` |
| BR-ACT-001 | Task là kế hoạch; completion không tự tạo Interaction hoặc business transition. | `activity` |
| BR-MAR-001 | Outbound phải re-check consent, restriction, suppression, frequency, quiet hours và workflow tại execution. | `party`/`marketing`/`activity` |
| BR-ANA-001 | Analytics read-only đối với business truth; Snapshot/Forecast không sửa source aggregates. | `analytics` |
| BR-AUD-001 | Audit append-only; correction tạo fact mới. | `audit` |
| BR-DOC-001 | Signed/verified Document Version bất biến; binary thuộc Documents/Object Storage. | `documents` |
| BR-INT-001 | Integration vận chuyển/chuẩn hóa; không tự quyết định business source of truth. | `integration` |

# 3. SLA baseline

Các giá trị dưới đây là baseline configurable, không hard-code:

- Lead mới: 2 giờ.
- Lịch hẹn sắp tới: 24 giờ tới ngay.
- Deal đang hoạt động: 24 giờ.
- Booking/cọc/hợp đồng trong ngày.
- Dữ liệu còn lại: 3 ngày.

Exact Definition Version thuộc Platform và Activity runtime.
