# CRM_BDS_AI — DEVELOPER COMMAND CONTRACT

**Document ID:** `IMPL-DEV-CMD-001`  
**Canonical path:** `docs/implementation/dev-command-contract.md`  
**Product:** `crm_bds_ai`  
**Version:** `1.0.0`  
**Status:** `Ready for Review / Foundation Baseline`  
**Owner:** `Engineering Owner`  
**Effective date:** `2026-08-05`  
**Last reviewed:** `2026-08-05`  
**Classification:** `INTERNAL`

---

# 1. Single entry point

Repository phải có một documented command entry point, ví dụ:

```text
python scripts/dev.py <command>
```

# 2. Required commands

| Command concept | Outcome |
|---|---|
| `setup` | validate tools and locked install |
| `up` / `down` | local environment lifecycle |
| `migrate` | upgrade database to head |
| `check` | full mandatory local quality gates |
| `test` | test suites with explicit selectors |
| `openapi` | generate/validate OpenAPI |
| `events` | validate JSON Schema/AsyncAPI |
| `docs-check` | links/metadata/drift/security |
| `architecture-check` | dependency/context boundaries |
| `smoke` | local end-to-end health verification |

# 3. Rules

Commands fail non-zero, print actionable errors, avoid hidden destructive behavior và work on supported developer OS.
