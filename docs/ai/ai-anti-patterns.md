# CRM_BDS_AI — AI ANTI-PATTERNS

**Document ID:** `AI-ANT-001`  
**Canonical path:** `docs/ai/ai-anti-patterns.md`  
**Product:** `crm_bds_ai`  
**Version:** `1.0.0`  
**Status:** `Accepted / Foundation Baseline`  
**Owner:** `AI Architecture Owner`  
**Effective date:** `2026-08-05`  
**Last reviewed:** `2026-08-05`  
**Classification:** `INTERNAL`

---

# 1. Prohibited patterns

- Provider SDK imported inside business Context.
- Model ID/base URL/API key hard-coded.
- One global model assumed to support every capability.
- Raw business data sent before authorization/masking.
- Automatic cloud fallback for restricted data.
- Free-form output written directly to aggregates.
- Model receives SQL/repository/shell tools.
- RAG/vector index treated as current business truth.
- Prompt/model/tool changes without version/evaluation.
- Embedding model changed in-place.
- AI required for core transaction completion.
- Hidden tool action without preview/evidence/Audit.
- Open Decision silently implemented by AI.

# 2. Enforcement

Coding standards, architecture tests, secret scanning, contract tests, provider conformance, negative security tests and Sprint acceptance must prove these patterns are absent.
