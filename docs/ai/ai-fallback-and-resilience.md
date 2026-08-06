# CRM_BDS_AI — AI FALLBACK AND RESILIENCE

**Document ID:** `AI-RES-001`  
**Canonical path:** `docs/ai/ai-fallback-and-resilience.md`  
**Product:** `crm_bds_ai`  
**Version:** `1.0.0`  
**Status:** `Accepted / Foundation Baseline`  
**Owner:** `AI Architecture Owner`  
**Effective date:** `2026-08-05`  
**Last reviewed:** `2026-08-05`  
**Classification:** `INTERNAL`

---

# 1. Controls

Timeout, bounded retry, idempotent job attempts, circuit breaker, bulkhead, queue limits, cancellation, provider health, manual fallback and feature flags.

# 2. Route fallback

Fallback must re-evaluate classification, deployment allowance, capabilities, quality threshold, cost and context constraints. Provider failure alone is not permission to change data boundary.

# 3. CRM isolation

Core commands commit independently of optional AI. Copilot errors return typed status and recovery guidance; they do not produce partial business writes.
