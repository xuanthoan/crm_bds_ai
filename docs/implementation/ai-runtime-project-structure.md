# CRM_BDS_AI — AI RUNTIME PROJECT STRUCTURE

**Document ID:** `IMP-AI-003`  
**Canonical path:** `docs/implementation/ai-runtime-project-structure.md`  
**Product:** `crm_bds_ai`  
**Version:** `1.0.0`  
**Status:** `Accepted / Foundation Baseline`  
**Owner:** `Engineering Owner`  
**Effective date:** `2026-08-05`  
**Last reviewed:** `2026-08-05`  
**Classification:** `INTERNAL`

---

```text
backend/app/ai_runtime/
├── domain/          # registry/value objects only
├── application/     # use cases, router, evaluation orchestration
├── ports/           # provider, retrieval, audit, tools
├── adapters/        # isolated provider/runtime adapters
├── security/        # context builder, masking, injection guard
├── rag/             # retrieval/chunk/index orchestration
├── jobs/            # async execution and attempts
├── telemetry/       # metrics/traces/usage
└── api/             # internal/admin/copilot endpoints
```

No business aggregate or provider SDK belongs in `domain/` or owning Context packages.
