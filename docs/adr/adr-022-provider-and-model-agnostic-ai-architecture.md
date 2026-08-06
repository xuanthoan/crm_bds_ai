# CRM_BDS_AI — PROVIDER- AND MODEL-AGNOSTIC AI ARCHITECTURE

**Document ID:** `ADR-022`  
**Canonical path:** `docs/adr/adr-022-provider-and-model-agnostic-ai-architecture.md`  
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

Business Contexts depend only on canonical AI capability/use-case contracts. Provider/model connections are selected through registries, routing policy and adapters. Adding a compatible provider/model is configuration; a proprietary protocol requires only an isolated adapter.

## Consequences

More initial abstraction and conformance testing, but no vendor lock-in, easier local/cloud switching, safer fallback and testable provider boundaries.

## Rejected alternatives

- Provider SDKs inside each module.
- One globally hard-coded model.
- Direct AI database writes.
- Unconditional cloud fallback.
