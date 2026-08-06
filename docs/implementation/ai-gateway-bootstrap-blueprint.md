# CRM_BDS_AI — AI GATEWAY BOOTSTRAP BLUEPRINT

**Document ID:** `IMP-AI-001`  
**Canonical path:** `docs/implementation/ai-gateway-bootstrap-blueprint.md`  
**Product:** `crm_bds_ai`  
**Version:** `1.0.0`  
**Status:** `Accepted / Foundation Baseline`  
**Owner:** `Engineering Owner`  
**Effective date:** `2026-08-05`  
**Last reviewed:** `2026-08-05`  
**Classification:** `INTERNAL`

---

# 1. Package boundary

Create an `ai_runtime` application package/service containing ports, registries, router, adapters, policy guards, jobs and telemetry. Business contexts depend only on ports and use-case DTOs.

# 2. Bootstrap order

1. Canonical DTOs and error codes.
2. Mock/deterministic adapter.
3. Registry loading and validation.
4. Routing and capability negotiation.
5. Structured-output validator.
6. Permission/context builder.
7. Job runtime, timeout/retry/circuit breaker.
8. Audit and observability.
9. First read-only Copilot use case.

# 3. Acceptance

Architecture test proves no provider SDK import outside adapters. Contract tests run all adapters through the conformance suite. Core CRM tests pass with AI disabled.
