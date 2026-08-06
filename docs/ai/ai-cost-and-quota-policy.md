# CRM_BDS_AI — AI COST AND QUOTA POLICY

**Document ID:** `AI-CST-001`  
**Canonical path:** `docs/ai/ai-cost-and-quota-policy.md`  
**Product:** `crm_bds_ai`  
**Version:** `1.0.0`  
**Status:** `Accepted / Foundation Baseline`  
**Owner:** `AI Architecture Owner`  
**Effective date:** `2026-08-05`  
**Last reviewed:** `2026-08-05`  
**Classification:** `INTERNAL`

---

# 1. Controls

Per use case, Legal Entity, user, provider/model and period: request count, input/output units, estimated cost, concurrency, context size and batch limits.

# 2. Behavior

Quota exhaustion must degrade gracefully: smaller context, lower-cost approved route, async processing or Copilot unavailable. It must not bypass classification or quality gates.

# 3. Accountability

Usage record includes route, model profile version, prompt version, units, estimated cost, cache/retry/fallback and business subject reference.
