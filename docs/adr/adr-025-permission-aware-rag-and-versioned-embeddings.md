# CRM_BDS_AI — PERMISSION-AWARE RAG AND VERSIONED EMBEDDINGS

**Document ID:** `ADR-025`  
**Canonical path:** `docs/adr/adr-025-permission-aware-rag-and-versioned-embeddings.md`  
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

RAG is controlled by CRM retrieval with security metadata and evidence. Vector indexes are derived/versioned; embedding model changes create new indexes. Current business truth is queried from owning Contexts.

## Consequences

Requires index lifecycle and rebuild support, but prevents cross-scope leakage and vector-store source-of-truth errors.

## Rejected alternatives

- Provider SDKs inside each module.
- One globally hard-coded model.
- Direct AI database writes.
- Unconditional cloud fallback.
