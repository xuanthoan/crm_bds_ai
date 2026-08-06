# CRM_BDS_AI — AI DEPLOYMENT MODES

**Document ID:** `AI-DEP-001`  
**Canonical path:** `docs/ai/ai-local-private-cloud-deployment.md`  
**Product:** `crm_bds_ai`  
**Version:** `1.0.0`  
**Status:** `Accepted / Foundation Baseline`  
**Owner:** `AI Architecture Owner`  
**Effective date:** `2026-08-05`  
**Last reviewed:** `2026-08-05`  
**Classification:** `INTERNAL`

---

# 1. Supported deployment types

`LOCAL_WORKSTATION`, `ON_PREMISE_SERVER`, `PRIVATE_CLOUD`, `PUBLIC_CLOUD`, `MANAGED_ENTERPRISE`.

# 2. Neutrality

Deployment mode is a Provider Profile attribute. The same use case may route differently by Legal Entity or classification without changing business code.

# 3. Network boundaries

Inference runtimes are not exposed directly to frontend or public Internet. Only AI Gateway/adapter workers reach them. Secrets and certificates use managed references.

# 4. Capacity

Context limits, concurrency, GPU/CPU/RAM, queueing and timeout are measured per model profile. Capacity shortfall degrades AI only, not Core CRM.
