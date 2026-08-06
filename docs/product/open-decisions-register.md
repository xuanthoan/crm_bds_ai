# CRM_BDS_AI — OPEN DECISIONS REGISTER

**Document ID:** `PROD-ODR-001`  
**Canonical path:** `docs/product/open-decisions-register.md`  
**Product:** `crm_bds_ai`  
**Version:** `1.0.0`  
**Status:** `Ready for Review / Foundation Baseline`  
**Owner:** `Product Owner`  
**Effective date:** `2026-08-05`  
**Last reviewed:** `2026-08-05`  
**Classification:** `INTERNAL`

---

# 1. Mục đích

Register này khóa các quyết định chưa đủ dữ kiện. Open decision không được AI Agent tự chọn.

# 2. Status

`OPEN`, `PROPOSED`, `DECIDED`, `DEFERRED`, `REJECTED`, `SUPERSEDED`.

# 3. Decisions

| ID | Chủ đề | Câu hỏi cần quyết định | Context ảnh hưởng | Gate |
|---|---|---|---|---|
| ODR-TRA-001 | Hold duration | Thời gian giữ tối đa mặc định, giới hạn gia hạn và ngoại lệ theo Project/Policy? | `transaction`, `product`, `platform` | Trước Hold implementation |
| ODR-TRA-002 | Deposit lock condition | Có bắt buộc xác nhận tiền để chuyển Hold sang Booking Lock hay không; theo mô hình giao dịch nào? | `transaction`, `contract`, `product` | Trước Booking confirmation |
| ODR-PRO-001 | Lock release authority | Ai được release/force-release Commercial Lock; điều kiện dispute và emergency? | `product`, `iam`, `audit` | Trước Commercial Lock commands |
| ODR-TRA-003 | Discount approval | Ngưỡng giảm giá, authority theo role/Legal Entity/Project và floor-price concealment? | `transaction`, `platform`, `iam` | Trước Proposal/Negotiation |
| ODR-REV-001 | Cancellation commission | Commission đã recognized/paid khi khách hủy được reverse, clawback hay waive như thế nào? | `revenue`, `contract` | Trước Clawback |
| ODR-LEA-001 | Lead protection | Thời hạn bảo vệ Lead theo source, channel, SLA và trạng thái chăm sóc? | `lead`, `platform` | Trước Care Protection |
| ODR-LEA-002 | Lead transfer authority | Ai được chuyển Lead/Customer responsibility; notification, reason và approval nào? | `lead`, `iam`, `activity` | Trước Assignment transfer |
| ODR-PAR-001 | Merge authority | Role nào được merge Customer; threshold/evidence nào bắt buộc; rollback policy? | `party`, `audit` | Trước Customer Merge |
| ODR-CON-001 | Accounting integration | CRM operational cash truth đồng bộ ERP ở mức nào; ERP nào là statutory source? | `contract`, `revenue`, `integration` | Trước ERP connector |
| ODR-MAR-001 | Marketing lawful basis | Lawful basis/consent source cho từng purpose/channel và imported audiences? | `party`, `marketing`, `activity` | Trước outbound automation |

# 4. Decision record

Mỗi quyết định phải ghi: decision, rationale, alternatives, effective date, owner, affected requirements, ADR/config/registry updates và migration impact.
