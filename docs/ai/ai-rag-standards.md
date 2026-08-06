# CRM_BDS_AI — AI RAG STANDARDS

**Document ID:** `AI-RAG-001`  
**Canonical path:** `docs/ai/ai-rag-standards.md`  
**Product:** `crm_bds_ai`  
**Version:** `1.0.0`  
**Status:** `Accepted / Foundation Baseline`  
**Owner:** `AI Architecture Owner`  
**Effective date:** `2026-08-05`  
**Last reviewed:** `2026-08-05`  
**Classification:** `INTERNAL`

---

# 1. Canonical pipeline

Source artifact → scan/classify → extract/OCR → chunk → metadata → embedding profile → versioned index → permission-aware retrieval → evidence citations → model generation.

# 2. Source of truth

Vector stores are derived indexes and rebuildable. Current Availability, Lock, Payment, Receipt, Consent, Permission and Commission status must be queried from owning Context APIs.

# 3. Retrieval filters

Legal Entity, tenant, effective scope, document status/version, classification, purpose, time validity and deletion/legal-hold state.

# 4. Answer policy

No supported evidence means return insufficient evidence; never fabricate a citation.
