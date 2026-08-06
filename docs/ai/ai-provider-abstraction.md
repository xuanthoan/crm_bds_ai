# CRM_BDS_AI — AI PROVIDER ABSTRACTION

**Document ID:** `AI-ABS-001`  
**Canonical path:** `docs/ai/ai-provider-abstraction.md`  
**Product:** `crm_bds_ai`  
**Version:** `1.0.0`  
**Status:** `Accepted / Foundation Baseline`  
**Owner:** `AI Architecture Owner`  
**Effective date:** `2026-08-05`  
**Last reviewed:** `2026-08-05`  
**Classification:** `INTERNAL`

---

# 1. Objective

Any compatible local runtime, self-hosted server, private platform or cloud API can be installed without changing business modules.

# 2. Canonical adapter contract

Every adapter implements: `generate`, `embed` where supported, `rerank` where supported, `transcribe` where supported, `health`, `capabilities`, `usage_normalization` and `error_translation`.

# 3. Adapter families

- Generic HTTP chat/embedding adapter.
- Open-protocol-compatible adapter family.
- Native provider adapter for vendor-specific file, batch or multimodal features.
- Local runtime adapter.
- Composite adapter for specialized OCR/speech/rerank pipelines.

# 4. Forbidden coupling

No provider/model name in domain entities, use-case handlers, API routes, frontend components or business tests. Provider-specific response bodies never leave the adapter boundary.
