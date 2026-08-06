# ADR-010: Process Managers instead of Distributed Transactions

**Document ID:** `ADR-010`  
**Canonical path:** `docs/adr/adr-010-process-managers-instead-of-distributed-transactions.md`  
**Product:** `crm_bds_ai`  
**Version:** `1.0.0`  
**Status:** `Accepted`  
**Owner:** `Architecture Owner`  
**Reviewers:** `Product Owner, Technical Owner, Domain Owners`  
**Last reviewed:** `2026-08-05`  
**Classification:** `INTERNAL`


# Context

Greenfield `crm_bds_ai` cần một quyết định nền tảng nhất quán cho mọi Sprint và AI Agent.

# Decision

Long-running cross-context flows dùng process manager.

# Rationale

Cho phép timeout/retry/reconciliation.

# Consequences

Compensation là business action.

# Compliance

- Context Pack, code, tests và machine contracts phải tuân ADR này.
- Exception cần ADR mới hoặc waiver có owner/expiry.

# Supersedes

Không.
