# CRM_BDS_AI — AI PROVIDER ADAPTER SDK

**Document ID:** `IMP-AI-002`  
**Canonical path:** `docs/implementation/ai-provider-adapter-sdk.md`  
**Product:** `crm_bds_ai`  
**Version:** `1.0.0`  
**Status:** `Accepted / Foundation Baseline`  
**Owner:** `Engineering Owner`  
**Effective date:** `2026-08-05`  
**Last reviewed:** `2026-08-05`  
**Classification:** `INTERNAL`

---

# 1. Required interface

`generate`, optional `embed/rerank/transcribe/synthesize`, `health`, `capabilities`, `normalize_usage`, `translate_error`.

# 2. Adapter responsibilities

Translate canonical messages/tools/schema to provider protocol; normalize response/tool calls/usage/errors; enforce request timeout; never authorize business access or execute tools directly.

# 3. Test kit

Fake server fixtures, timeout/rate-limit/malformed-response cases, capability probes, JSON-schema conformance, tool-call round trip and secret-redaction assertions.
