# CRM_BDS_AI — AI PROVIDER REGISTRY

**Document ID:** `AI-PRV-001`  
**Canonical path:** `docs/ai/ai-provider-registry.md`  
**Product:** `crm_bds_ai`  
**Version:** `1.0.0`  
**Status:** `Accepted / Foundation Baseline`  
**Owner:** `AI Architecture Owner`  
**Effective date:** `2026-08-05`  
**Last reviewed:** `2026-08-05`  
**Classification:** `INTERNAL`

---

# 1. Provider profile

Fields: provider code, adapter type, deployment type, base URL/connection reference, secret reference, region, data-processing policy, allowed classifications, health endpoint, timeout/retry/rate-limit, status and effective dates.

# 2. Lifecycle

`DRAFT → TESTING → APPROVED → ACTIVE → SUSPENDED → RETIRED`.

# 3. Secret policy

Registry stores only secret references. Plain API keys must not be returned to frontend, logs, prompts, Audit payloads or exported configuration.
