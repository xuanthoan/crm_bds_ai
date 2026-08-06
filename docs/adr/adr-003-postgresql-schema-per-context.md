# ADR-003: PostgreSQL Schema per Context

**Document ID:** `ADR-003`  
**Canonical path:** `docs/adr/adr-003-postgresql-schema-per-context.md`  
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

Mỗi Context có PostgreSQL schema riêng; technical schema `infra`.

# Rationale

Thể hiện ownership và chuẩn bị khả năng tách.

# Consequences

Không cross-schema business writes.

# Compliance

- Context Pack, code, tests và machine contracts phải tuân ADR này.
- Exception cần ADR mới hoặc waiver có owner/expiry.

# Supersedes

Không.
