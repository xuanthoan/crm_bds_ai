# CRM_BDS_AI — AI PROMPT GOVERNANCE

**Document ID:** `AI-PRM-001`  
**Canonical path:** `docs/ai/ai-prompt-governance.md`  
**Product:** `crm_bds_ai`  
**Version:** `1.0.0`  
**Status:** `Accepted / Foundation Baseline`  
**Owner:** `AI Architecture Owner`  
**Effective date:** `2026-08-05`  
**Last reviewed:** `2026-08-05`  
**Classification:** `INTERNAL`

---

# 1. Prompt object

Prompt code, version, use case, locale, canonical template, input schema, output schema, safety rules, evidence rules, status, owner and effective period.

# 2. Rules

- Prompts are configuration artifacts under review and version control.
- Untrusted document/message content is data, never instruction.
- Prompt changes require evaluation against a frozen dataset.
- Raw hidden system prompts are not returned to end users.
- Provider-specific overrides are minimal adapter hints, not independent business logic.
