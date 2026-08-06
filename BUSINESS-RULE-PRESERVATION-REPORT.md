# CRM_BDS_AI — BUSINESS RULE PRESERVATION REPORT

**Document ID:** `PKG-BRP-001`  
**Canonical path:** `BUSINESS-RULE-PRESERVATION-REPORT.md`  
**Product:** `crm_bds_ai`  
**Version:** `1.0.0`  
**Status:** `Accepted / Foundation Baseline`  
**Owner:** `Product Owner`  
**Effective date:** `2026-08-05`  
**Last reviewed:** `2026-08-05`  
**Classification:** `INTERNAL`

---

# 1. Phạm vi

Gói này được tạo từ baseline Greenfield trước đó, đổi tên sang `crm_bds_ai`, giữ nguyên 14 Product Capabilities, 16 Bounded Contexts và các business truths đã xác nhận; đồng thời bổ sung kiến trúc AI provider/model-agnostic.

# 2. Cơ chế bảo toàn

- Tài liệu capability và Context Pack gốc được giữ cấu trúc và chỉ đổi tên sản phẩm.
- `business-rules-index.md` được giữ lại.
- `canonical-business-rules.md` chuẩn hóa rule tích cực.
- `business-rule-anti-patterns.md` chuẩn hóa negative requirements.
- `canonical-requirements-registry.md` quy định traceability đến machine contract và test evidence.
- Open Decisions được giữ ở trạng thái mở; AI Agent không được tự chọn.

# 3. Coverage

- Tổng canonical rules trong registry mới: **38**.
- Rule IDs: `CBR-001, CBR-002, CBR-003, CBR-004, CBR-005, CBR-006, CBR-007, CBR-008, CBR-009, CBR-010, CBR-011, CBR-012, CBR-013, CBR-014, CBR-015, CBR-016, CBR-017, CBR-018, CBR-019, CBR-020, CBR-021, CBR-022, CBR-023, CBR-024, CBR-025, CBR-026, CBR-AI-001, CBR-AI-002, CBR-AI-003, CBR-AI-004, CBR-AI-005, CBR-AI-006, CBR-AI-007, CBR-AI-008, CBR-AI-009, CBR-AI-010, CBR-AI-011, CBR-AI-012`.
- AI rules bổ sung không thay thế owning business Context; chúng chỉ đặt guardrails cho AI Copilot/AI runtime.

# 4. Không được hiểu sai

Gói tài liệu này là baseline để code, không phải bằng chứng phần mềm đã chạy. Exact DDL, OpenAPI, AsyncAPI, permission machine registry và state machine vẫn phải được tạo/kiểm thử trong Sprint tương ứng.
