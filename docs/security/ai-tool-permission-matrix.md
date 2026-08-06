# CRM_BDS_AI — AI TOOL PERMISSION MATRIX

**Document ID:** `SEC-AI-002`  
**Canonical path:** `docs/security/ai-tool-permission-matrix.md`  
**Product:** `crm_bds_ai`  
**Version:** `1.0.0`  
**Status:** `Accepted / Foundation Baseline`  
**Owner:** `Security Owner`  
**Effective date:** `2026-08-05`  
**Last reviewed:** `2026-08-05`  
**Classification:** `INTERNAL`

---

| Tool class | Default | Approval |
|---|---|---|
| Read scoped data | deny until explicit allowlist | none after backend permission |
| Create draft/suggestion | allow by use-case permission | user review |
| Business command | deny by default | explicit approval + invariant check |
| Financial/legal/security command | prohibited or dual control | policy-specific |
| SQL/repository/shell/permission grant | prohibited | not available to model |
