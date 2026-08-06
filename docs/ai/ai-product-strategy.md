# CRM_BDS_AI — AI PRODUCT STRATEGY

**Document ID:** `AI-STR-001`  
**Canonical path:** `docs/ai/ai-product-strategy.md`  
**Product:** `crm_bds_ai`  
**Version:** `1.0.0`  
**Status:** `Accepted / Foundation Baseline`  
**Owner:** `AI Architecture Owner`  
**Effective date:** `2026-08-05`  
**Last reviewed:** `2026-08-05`  
**Classification:** `INTERNAL`

---

# 1. Mục tiêu

AI trong `crm_bds_ai` phải giảm nhập liệu, tóm tắt lịch sử, tìm kiếm ngữ nghĩa, ghép khách–sản phẩm, đọc tài liệu, giải thích số liệu và hỗ trợ vận hành mà không chiếm quyền business authority.

# 2. Product principles

1. Copilot-first; autonomous agent last.
2. Provider/model agnostic.
3. Local, private cloud và public cloud đều là deployment choices.
4. AI là optional enhancement; Core CRM phải chạy khi AI unavailable.
5. Human review tỷ lệ thuận với impact.
6. Evidence, confidence, schema validation và Audit là mặc định.
7. Không gửi dữ liệu vượt purpose hoặc data classification policy.

# 3. Delivery waves

- Wave A: RAG nội bộ, Lead/Customer/Deal summary, transcript, task/message draft.
- Wave B: extraction, semantic product search, matching và reverse matching.
- Wave C: Deal risk, Next Best Action, document/contract review, Analytics Copilot.
- Wave D: predictive models sau khi có dữ liệu đủ chất lượng.
- Wave E: approval-driven multi-step agents với tool allowlist.

# 4. Success metrics

Task-time reduction, acceptance rate, human edit rate, unsupported-claim rate, schema-validity rate, evidence precision, cost/use case, latency, security incidents và CRM availability độc lập AI.
