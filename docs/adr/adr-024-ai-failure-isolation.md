# CRM_BDS_AI — AI FAILURE ISOLATION FROM CORE CRM

**Document ID:** `ADR-024`  
**Canonical path:** `docs/adr/adr-024-ai-failure-isolation.md`  
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

AI calls execute outside core transactions with timeout, circuit breaker, queue isolation, feature flags and manual fallback. AI unavailability cannot block valid CRM commands.

## Consequences

Some Copilot functions may degrade or pause, while transactional CRM remains available.

## Rejected alternatives

- Provider SDKs inside each module.
- One globally hard-coded model.
- Direct AI database writes.
- Unconditional cloud fallback.
