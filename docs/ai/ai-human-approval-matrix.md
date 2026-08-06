# CRM_BDS_AI — AI HUMAN APPROVAL MATRIX

**Document ID:** `AI-HITL-001`  
**Canonical path:** `docs/ai/ai-human-approval-matrix.md`  
**Product:** `crm_bds_ai`  
**Version:** `1.0.0`  
**Status:** `Accepted / Foundation Baseline`  
**Owner:** `AI Architecture Owner`  
**Effective date:** `2026-08-05`  
**Last reviewed:** `2026-08-05`  
**Classification:** `INTERNAL`

---

# 1. Approval levels

- L0: read-only explanation; no approval.
- L1: draft/suggestion; user may accept/edit/reject.
- L2: business command preview; explicit confirmation and backend validation.
- L3: dual control/segregation of duties.
- L4: AI prohibited from initiating.

# 2. Examples

Summary/RAG = L0. Task/message draft = L1. Requirement update or assignment proposal = L2. Refund/commission approval/data repair = L3 or L4. Receipt issuance, permission grant, production SQL and legal verification final authority = L4 by default.

# 3. Decision evidence

Record suggestion version, diff, evidence, human actor, edit, decision, command result and timestamp.
