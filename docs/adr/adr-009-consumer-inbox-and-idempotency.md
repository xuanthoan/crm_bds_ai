# ADR-009: Consumer Inbox and Idempotency

**Document ID:** `ADR-009`  
**Canonical path:** `docs/adr/adr-009-consumer-inbox-and-idempotency.md`  
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

Consumers lưu message identity/result trước side effect.

# Rationale

Duplicate delivery là bình thường.

# Consequences

Payload-hash conflict cho idempotent commands.

# Compliance

- Context Pack, code, tests và machine contracts phải tuân ADR này.
- Exception cần ADR mới hoặc waiver có owner/expiry.

# Supersedes

Không.
