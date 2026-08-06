# CRM_BDS_AI — AI EVALUATION FRAMEWORK

**Document ID:** `AI-EVL-001`  
**Canonical path:** `docs/ai/ai-evaluation-framework.md`  
**Product:** `crm_bds_ai`  
**Version:** `1.0.0`  
**Status:** `Accepted / Foundation Baseline`  
**Owner:** `AI Architecture Owner`  
**Effective date:** `2026-08-05`  
**Last reviewed:** `2026-08-05`  
**Classification:** `INTERNAL`

---

# 1. Evaluation layers

Adapter conformance, schema validity, task quality, groundedness/evidence, safety/privacy, tool correctness, latency, cost and user outcome.

# 2. Dataset governance

Evaluation datasets are versioned, access-controlled, de-identified where possible and separated from prompts. Each production use case has baseline, threshold and regression suite.

# 3. Release gate

No model, prompt, routing or retrieval change reaches production without accepted evaluation evidence and rollback plan. Shadow mode is preferred before traffic migration.

# 4. Online metrics

Acceptance rate, edit rate, unsupported claim reports, no-result rate, tool failure, business correction and incident rate.
