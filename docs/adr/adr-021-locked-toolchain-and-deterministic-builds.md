# ADR-021: Locked Toolchain and Deterministic Builds

**Document ID:** `ADR-021`  
**Canonical path:** `docs/adr/adr-021-locked-toolchain-and-deterministic-builds.md`  
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

Core versions/lockfiles/container digests được khóa và validate Sprint 0.

# Rationale

Reproducibility cho AI agents và CI.

# Consequences

Upgrade cần explicit change control.

# Compliance

- Context Pack, code, tests và machine contracts phải tuân ADR này.
- Exception cần ADR mới hoặc waiver có owner/expiry.

# Supersedes

Không.
