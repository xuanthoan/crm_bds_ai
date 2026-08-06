# CRM_BDS_AI — AI ARCHITECTURE

**Document ID:** `AI-ARC-001`  
**Canonical path:** `docs/ai/ai-architecture.md`  
**Product:** `crm_bds_ai`  
**Version:** `1.0.0`  
**Status:** `Accepted / Foundation Baseline`  
**Owner:** `AI Architecture Owner`  
**Effective date:** `2026-08-05`  
**Last reviewed:** `2026-08-05`  
**Classification:** `INTERNAL`

---

# 1. Logical architecture

```text
Frontend / Background Workflow
→ Owning Context Application Service
→ AI Use Case Service
→ AI Policy and Context Builder
→ Provider/Model-Agnostic AI Gateway
→ Adapter selected by Routing Policy
→ Local/Private/Cloud inference runtime
```

Supporting components:

```text
Provider Registry | Model Registry | Capability Registry
Prompt Registry | Tool Registry | Output Schema Registry
RAG Retriever | PII/Secret Redactor | Tool Guard
Job Runtime | Circuit Breaker | Cost/Quota | Evaluation | Audit
```

# 2. Ownership

- Platform: use-case, prompt, model/routing/feature/quota definitions.
- IAM/Security: permission, scope, purpose, masking and provider trust.
- Integration: provider connections and adapters.
- Operations: jobs, health, retry, circuit breaker, usage and evaluation runs.
- Documents: transcript/extraction/generated artifacts and RAG sources.
- Audit: immutable AI request/decision facts.
- Owning Context: acceptance and final business command.

# 3. Dependency rule

Business Contexts may depend on canonical `AIUseCasePort`; they may not import provider SDKs, model identifiers, HTTP clients or adapter implementations.

# 4. Failure boundary

AI execution is outside the core business transaction. A failed AI request returns a typed unavailable/failed result and never rolls back a valid Lead, Booking, Payment or Contract command.
