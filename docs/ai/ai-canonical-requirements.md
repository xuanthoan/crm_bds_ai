# CRM_BDS_AI — AI CANONICAL REQUIREMENTS

**Document ID:** `AI-REQ-001`  
**Canonical path:** `docs/ai/ai-canonical-requirements.md`  
**Product:** `crm_bds_ai`  
**Version:** `1.0.0`  
**Status:** `Accepted / Foundation Baseline`  
**Owner:** `AI Architecture Owner`  
**Effective date:** `2026-08-05`  
**Last reviewed:** `2026-08-05`  
**Classification:** `INTERNAL`

---

# 1. Requirements

- `AI-REQ-001`: All business modules call a canonical AI use-case port.
- `AI-REQ-002`: Provider/model selection is registry and policy driven.
- `AI-REQ-003`: Adapter boundary normalizes requests, responses, usage and errors.
- `AI-REQ-004`: Capability negotiation precedes route selection.
- `AI-REQ-005`: Authorization, scope, purpose and masking precede prompt construction.
- `AI-REQ-006`: Structured output validation precedes suggestion creation.
- `AI-REQ-007`: High-impact changes require human approval and owning-Context command.
- `AI-REQ-008`: Tool calls use canonical Tool Registry and Tool Guard.
- `AI-REQ-009`: RAG retrieval is permission-aware and evidence-bearing.
- `AI-REQ-010`: Embedding/index/prompt/model/routing/tool artifacts are versioned.
- `AI-REQ-011`: AI failure is isolated from Core CRM.
- `AI-REQ-012`: Every production use case has evaluation, observability, quota and rollback.
- `AI-REQ-013`: Provider onboarding requires conformance/security/privacy/quality approval.
- `AI-REQ-014`: Frontend labels AI output and supports accept/edit/reject where applicable.
- `AI-REQ-015`: Audit records route, versions, evidence, validation and human decision without exposing secrets.

# 2. Acceptance

Each requirement needs architecture/unit/contract/security/evaluation evidence. Configuration-only claims are insufficient without runtime conformance tests.
