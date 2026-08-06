# CRM_BDS_AI — AI SUGGESTIONS ARE NOT BUSINESS TRUTH

**Document ID:** `ADR-023`  
**Canonical path:** `docs/adr/adr-023-ai-suggestions-not-business-truth.md`  
**Product:** `crm_bds_ai`  
**Version:** `1.0.0`  
**Status:** `Accepted`  
**Owner:** `Architecture Owner`  
**Effective date:** `2026-08-05`  
**Last reviewed:** `2026-08-05`  
**Classification:** `INTERNAL`

---
# Context

`crm_bds_ai` requires pluggable AI without provider/model dependency and without weakening business authority.


## Decision

AI output is stored as suggestion, draft, extraction, ranking, forecast or explanation. Only an authorized owning-Context command can change business state. High-impact commands require explicit human approval according to the approval matrix.

## Consequences

UI needs diff/evidence/accept/reject flows and Audit lineage, but hallucinations cannot silently become source of truth.

## Rejected alternatives

- Provider SDKs inside each module.
- One globally hard-coded model.
- Direct AI database writes.
- Unconditional cloud fallback.
