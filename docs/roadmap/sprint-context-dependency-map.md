# CRM_BDS_AI — SPRINT–CONTEXT DEPENDENCY MAP

**Document ID:** `ROADMAP-DEP-001`  
**Canonical path:** `docs/roadmap/sprint-context-dependency-map.md`  
**Product:** `crm_bds_ai`  
**Version:** `1.0.0`  
**Status:** `Accepted / Planning Baseline`  
**Owner:** `Architecture Owner`  
**Effective date:** `2026-08-05`  
**Last reviewed:** `2026-08-05`  
**Classification:** `INTERNAL`

---

# Dependency principles

- Sprint 0–2 establish documentation, repository and reliability foundations.
- Platform and IAM precede business Contexts requiring configuration/authorization.
- Party identity precedes Lead conversion and Customer references.
- Product precedes Matching, Hold and Booking.
- Transaction precedes Contract; Contract precedes Revenue cash-dependent rules.
- Activity can start after IAM/Party foundations but integrates incrementally.
- Analytics consumes published facts and must not become source authority.
- Documents/Audit/Integration/Operations foundations are introduced JIT before dependent flows.

# Activation rule

Roadmap order plus dependency Acceptance Reports plus Context Readiness Gate determine activation. Sprint number alone never authorizes code.
