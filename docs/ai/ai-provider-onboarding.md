# CRM_BDS_AI — AI PROVIDER ONBOARDING

**Document ID:** `AI-ONB-001`  
**Canonical path:** `docs/ai/ai-provider-onboarding.md`  
**Product:** `crm_bds_ai`  
**Version:** `1.0.0`  
**Status:** `Accepted / Foundation Baseline`  
**Owner:** `AI Architecture Owner`  
**Effective date:** `2026-08-05`  
**Last reviewed:** `2026-08-05`  
**Classification:** `INTERNAL`

---

# 1. Gate sequence

Connection test → authentication test → capability probes → structured-output/tool conformance → security/privacy review → data-classification allowance → benchmark/evaluation → cost/quota review → approval → limited rollout → ACTIVE.

# 2. Required evidence

Adapter manifest, owner, data-flow diagram, secret handling, retention policy, outage behavior, conformance results, evaluation scores, rollback procedure and approval record.

# 3. Deactivation

Security incident, quality regression, policy breach, excessive cost or provider deprecation may move a provider/model to SUSPENDED without business-code changes.
