# ADR-012: Enterprise-global Party and Customer Identity

**Document ID:** `ADR-012`  
**Canonical path:** `docs/adr/adr-012-enterprise-global-party-and-customer-identity.md`  
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

Party identity dùng chung toàn Enterprise.

# Rationale

Tránh Customer masters cạnh tranh.

# Consequences

Visibility vẫn theo authorized scope.

# Compliance

- Context Pack, code, tests và machine contracts phải tuân ADR này.
- Exception cần ADR mới hoặc waiver có owner/expiry.

# Supersedes

Không.
