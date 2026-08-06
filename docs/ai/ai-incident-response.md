# CRM_BDS_AI — AI INCIDENT RESPONSE

**Document ID:** `AI-INC-001`  
**Canonical path:** `docs/ai/ai-incident-response.md`  
**Product:** `crm_bds_ai`  
**Version:** `1.0.0`  
**Status:** `Accepted / Foundation Baseline`  
**Owner:** `AI Architecture Owner`  
**Effective date:** `2026-08-05`  
**Last reviewed:** `2026-08-05`  
**Classification:** `INTERNAL`

---

# 1. Incident classes

Provider outage, quality regression, harmful/unsupported output, suspected data leak, prompt injection, runaway tool loop, cost spike, index corruption and model deprecation.

# 2. Immediate controls

Disable feature/use case/model/provider via feature flags, open circuit breaker, revoke secret, stop jobs, preserve evidence and switch to manual workflow.

# 3. Recovery

Determine affected requests/subjects, notify owners, remediate configuration/data, rerun evaluation, approve reactivation and document RCA.
