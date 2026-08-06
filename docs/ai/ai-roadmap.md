# CRM_BDS_AI — AI DELIVERY ROADMAP

**Document ID:** `AI-RDM-001`  
**Canonical path:** `docs/ai/ai-roadmap.md`  
**Product:** `crm_bds_ai`  
**Version:** `1.0.0`  
**Status:** `Accepted / Foundation Baseline`  
**Owner:** `AI Architecture Owner`  
**Effective date:** `2026-08-05`  
**Last reviewed:** `2026-08-05`  
**Classification:** `INTERNAL`

---

# 1. Phase sequence

- AI-0: strategy, requirements, architecture, security and registries.
- AI-1: provider/model-agnostic Gateway, mock adapter and conformance harness.
- AI-2: auth/masking, jobs, Audit, resilience and cost controls.
- AI-3: permission-aware RAG and versioned embeddings.
- AI-4: Copilot MVP—summary, transcript, task/message draft, document extraction.
- AI-5: semantic search and matching.
- AI-6: Deal/Contract/Analytics copilots.
- AI-7: predictive models after data readiness.
- AI-8: approval-driven multi-step agents.

# 2. Integration rule

AI-ready hooks are built with the related Context, while production Copilot is enabled only after that Context passes Data/API/Security/Workflow/AI Readiness Gates.
