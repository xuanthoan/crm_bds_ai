# CRM_BDS_AI — AI DATA CONTRACTS

**Document ID:** `AI-DCT-001`  
**Canonical path:** `docs/ai/ai-data-contracts.md`  
**Product:** `crm_bds_ai`  
**Version:** `1.0.0`  
**Status:** `Accepted / Foundation Baseline`  
**Owner:** `AI Architecture Owner`  
**Effective date:** `2026-08-05`  
**Last reviewed:** `2026-08-05`  
**Classification:** `INTERNAL`

---

# 1. Canonical objects

`AIUseCaseDefinition`, `AIJob`, `AIJobAttempt`, `AISuggestion`, `AIEvidenceReference`, `AIProviderProfile`, `AIModelProfile`, `AIPromptVersion`, `AIToolDefinition`, `AIRoutingDecision`, `AIUsageRecord`, `AIEvaluationRun`.

# 2. Suggestion lifecycle

`GENERATED → VALIDATED → PRESENTED → ACCEPTED | REJECTED | EDITED_AND_ACCEPTED | EXPIRED | FAILED`.

# 3. Invariants

Suggestion cannot mutate business aggregates. Accepted suggestion produces a separate authorized command with idempotency key. Evidence references are immutable; output schema version is required.
