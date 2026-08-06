# CRM_BDS_AI — AI SECURITY AND PRIVACY

**Document ID:** `AI-SEC-001`  
**Canonical path:** `docs/ai/ai-security-and-privacy.md`  
**Product:** `crm_bds_ai`  
**Version:** `1.0.0`  
**Status:** `Accepted / Foundation Baseline`  
**Owner:** `AI Architecture Owner`  
**Effective date:** `2026-08-05`  
**Last reviewed:** `2026-08-05`  
**Classification:** `INTERNAL`

---

# 1. Pre-prompt control chain

Authenticate → resolve permission/scope → load only authorized fields → purpose check → classification/provider policy → masking/redaction → prompt construction.

# 2. Threats

Prompt injection, cross-tenant retrieval, data exfiltration through tools, secret leakage, malicious files, output-schema bypass, recursive tool loops, cost exhaustion and stale suggestion replay.

# 3. Privacy

Default provider use must not train on CRM data unless an explicitly approved agreement says otherwise. Retention, deletion, legal hold, region and subprocessors are provider-profile controls.

# 4. Logging

Do not log raw restricted prompts/responses by default. Store hashes, references and minimal metadata; sensitive artifact storage follows Documents and retention policy.
