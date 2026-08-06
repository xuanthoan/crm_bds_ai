# CRM_BDS_AI — AI CAPABILITY INTEGRATION MATRIX

**Document ID:** `AI-MAP-001`  
**Canonical path:** `docs/ai/ai-capability-integration-matrix.md`  
**Product:** `crm_bds_ai`  
**Version:** `1.0.0`  
**Status:** `Accepted / Foundation Baseline`  
**Owner:** `AI Architecture Owner`  
**Effective date:** `2026-08-05`  
**Last reviewed:** `2026-08-05`  
**Classification:** `INTERNAL`

---

# 1. Capability mapping

| Product capability | Initial AI use cases | Required readiness |
|---|---|---|
| Platform Configuration | use-case/model/prompt/routing policy admin | versioning, approval, feature flags |
| IAM/Organization | AI permissions, provider trust and scope | backend enforcement, masking |
| Lead | summary, enrichment, SLA suggestion | stable Lead APIs/events |
| Customer 360 | timeline/requirement summary | Party read model, consent |
| Identity Governance | duplicate review candidate | Phone Identity and merge workflow |
| Product/Inventory | semantic search, description extraction | structured attributes, authority APIs |
| Matching | ranking/explanation/reverse matching | hard rules + Availability recheck |
| Deal/Transaction | Deal risk, proposal draft, NBA | stable state machine and Activity |
| Contract/Cash | document extraction, checklist | Documents, immutable cash records |
| Revenue/Commission | explanation/anomaly candidate | accepted financial invariants |
| Activity/Engagement | transcript, summary, task draft | recording policy and timeline |
| Marketing | content draft and campaign analysis | consent execution checks |
| Analytics | natural-language explanation | semantic metrics, lineage, scope |
| Runtime Support | incident/log copilot | observability and runbooks |

# 2. Rule

AI-readiness tasks may run with each capability; production enablement waits for the relevant readiness gate.
