# CRM_BDS_AI — AI COPILOT MVP ACCEPTANCE CHECKLIST

**Document ID:** `IMP-AI-005`  
**Canonical path:** `docs/implementation/ai-copilot-mvp-acceptance-checklist.md`  
**Product:** `crm_bds_ai`  
**Version:** `1.0.0`  
**Status:** `Accepted / Foundation Baseline`  
**Owner:** `Engineering Owner`  
**Effective date:** `2026-08-05`  
**Last reviewed:** `2026-08-05`  
**Classification:** `INTERNAL`

---

- Provider/model can be switched by registry without business-code change.
- AI disabled leaves CRM fully operational.
- Permission/scope/masking negative tests pass.
- Output schema and evidence validation pass.
- Suggestion accept/edit/reject and Audit pass.
- Timeout/circuit breaker/manual fallback pass.
- Evaluation threshold met on accepted dataset.
- UI labels AI content and exposes data cutoff/evidence.
- No direct DB/provider SDK coupling in business modules.
