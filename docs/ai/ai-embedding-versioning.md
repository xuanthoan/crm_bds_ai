# CRM_BDS_AI — AI EMBEDDING VERSIONING

**Document ID:** `AI-EMB-001`  
**Canonical path:** `docs/ai/ai-embedding-versioning.md`  
**Product:** `crm_bds_ai`  
**Version:** `1.0.0`  
**Status:** `Accepted / Foundation Baseline`  
**Owner:** `AI Architecture Owner`  
**Effective date:** `2026-08-05`  
**Last reviewed:** `2026-08-05`  
**Classification:** `INTERNAL`

---

# 1. Embedding profile

Provider/model reference, dimension, distance metric, normalization, language, chunking version, index version and source-version policy.

# 2. Migration

New model/dimension creates a new index. Re-embed, evaluate recall/precision, dual-read or shadow-test, cut over behind feature flag, retain rollback window, then retire old index.

# 3. Prohibition

Vectors from incompatible models or dimensions must never be mixed in one logical index version.
