# CRM_BDS_AI — AI DOCUMENTATION INDEX

**Document ID:** `AI-IDX-001`  
**Canonical path:** `docs/ai/README.md`  
**Product:** `crm_bds_ai`  
**Version:** `1.0.0`  
**Status:** `Accepted / Foundation Baseline`  
**Owner:** `AI Architecture Owner`  
**Effective date:** `2026-08-05`  
**Last reviewed:** `2026-08-05`  
**Classification:** `INTERNAL`

---

# 1. Canonical reading order

1. `ai-product-strategy.md`
2. `ai-canonical-requirements.md`
3. `ai-architecture.md`
4. `ai-provider-abstraction.md`
5. registries and routing documents
6. security, approval and tool governance
7. RAG/embedding/evaluation/observability
8. roadmap and sprint integration

# 2. Non-negotiable decision

`crm_bds_ai` is provider-agnostic and model-agnostic. Local, on-premise, private cloud, public cloud and future runtimes are installable through configuration or isolated adapters. No business Context depends on a named AI provider/model.

# 3. Canonical machine contracts

See `contracts/ai/`. Machine files are baseline schemas/examples and become production authority only after Sprint acceptance and implementation validation.
