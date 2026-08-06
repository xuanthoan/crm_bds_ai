# CRM_BDS_AI — AI ROUTING POLICY

**Document ID:** `AI-RTE-001`  
**Canonical path:** `docs/ai/ai-routing-policy.md`  
**Product:** `crm_bds_ai`  
**Version:** `1.0.0`  
**Status:** `Accepted / Foundation Baseline`  
**Owner:** `AI Architecture Owner`  
**Effective date:** `2026-08-05`  
**Last reviewed:** `2026-08-05`  
**Classification:** `INTERNAL`

---

# 1. Inputs

Required capabilities, data classification, deployment restrictions, Legal Entity policy, purpose, language, context size, provider health, quota, latency target, cost ceiling and use-case evaluation score.

# 2. Selection

1. Reject routes violating classification/purpose.
2. Filter disabled/unhealthy/non-conformant models.
3. Require all mandatory capabilities.
4. Apply local/private/cloud preferences.
5. Rank by accepted quality, latency and cost policy.
6. Record route decision in Audit.

# 3. Fallback

Fallback is allowed only when policy explicitly permits the target deployment and data classification. `provider failed → send everything to cloud` is prohibited.
