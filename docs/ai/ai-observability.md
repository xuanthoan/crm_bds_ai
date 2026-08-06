# CRM_BDS_AI — AI OBSERVABILITY

**Document ID:** `AI-OBS-001`  
**Canonical path:** `docs/ai/ai-observability.md`  
**Product:** `crm_bds_ai`  
**Version:** `1.0.0`  
**Status:** `Accepted / Foundation Baseline`  
**Owner:** `AI Architecture Owner`  
**Effective date:** `2026-08-05`  
**Last reviewed:** `2026-08-05`  
**Classification:** `INTERNAL`

---

# 1. Metrics

Request count, latency, provider/model errors, token/unit usage, cost, validation failures, fallbacks, circuit state, suggestion acceptance/edit/rejection, groundedness reports, RAG no-result and tool failures.

# 2. Tracing

Trace IDs span UI request, AI job, retrieval, provider call, tool calls and final business command, while sensitive content is referenced rather than copied.

# 3. SLO separation

AI SLO is separate from Core CRM SLO. AI outage must not reduce core transactional availability.
