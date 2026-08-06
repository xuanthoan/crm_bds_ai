# CRM_BDS_AI — AI CAPABILITY REGISTRY

**Document ID:** `AI-CAP-001`  
**Canonical path:** `docs/ai/ai-capability-registry.md`  
**Product:** `crm_bds_ai`  
**Version:** `1.0.0`  
**Status:** `Accepted / Foundation Baseline`  
**Owner:** `AI Architecture Owner`  
**Effective date:** `2026-08-05`  
**Last reviewed:** `2026-08-05`  
**Classification:** `INTERNAL`

---

# 1. Canonical capabilities

`CHAT`, `REASONING`, `STRUCTURED_OUTPUT`, `STREAMING`, `TOOL_CALLING`, `EMBEDDING`, `RERANKING`, `VISION`, `DOCUMENT_UNDERSTANDING`, `OCR`, `SPEECH_TO_TEXT`, `TEXT_TO_SPEECH`, `MODERATION`, `BATCH`.

# 2. Negotiation

Use cases declare required and optional capabilities. Routing filters models that cannot satisfy all required capabilities. Capability claims must be verified by conformance tests, not trusted from marketing descriptions.

# 3. Levels

Capabilities may have support level `NONE`, `BASIC`, `CONFORMANT`, `ADVANCED`. Structured output and tool calling require schema-conformance scores before production use.
