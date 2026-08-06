# CRM_BDS_AI — AI MODEL REGISTRY

**Document ID:** `AI-MDL-001`  
**Canonical path:** `docs/ai/ai-model-registry.md`  
**Product:** `crm_bds_ai`  
**Version:** `1.0.0`  
**Status:** `Accepted / Foundation Baseline`  
**Owner:** `AI Architecture Owner`  
**Effective date:** `2026-08-05`  
**Last reviewed:** `2026-08-05`  
**Classification:** `INTERNAL`

---

# 1. Model profile

Fields: internal model code, provider reference, provider model ID, capabilities, deployment type, context/input/output limits, supported media, tool/structured-output level, embedding dimension, cost/latency/quality profile, allowed classification, status and version.

# 2. No hard-coding

Use cases reference routing policy and capabilities, not provider model IDs. Model replacement is configuration plus evaluation and rollout, not a business-code change.

# 3. Evaluation binding

ACTIVE models must point to accepted evaluation results for each production use case class.
