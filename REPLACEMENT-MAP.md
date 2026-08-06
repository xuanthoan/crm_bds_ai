# CRM_BDS_AI — REPLACEMENT MAP

**Document ID:** `DOC-REPL-001`
**Canonical path:** `REPLACEMENT-MAP.md`
**Product:** `crm_bds_ai`
**Version:** `1.0.0`
**Status:** `Accepted / Foundation Baseline`
**Effective date:** `2026-08-05`
**Classification:** `INTERNAL`

---

# 1. Purpose

This file records the six primary replacements introduced by the
Synchronized Foundation Replacement Pack (`docs/sprints/README.md`)
and the supporting files that ship with it. It prevents reintroduction
of competing sources of truth.

# 2. Six primary replacements

| # | Superseded document | Replacement (canonical) |
|---|---|---|
| 1 | Old master Sprint / mega path | `docs/sprints/sprint-000/sprint-000-preparation-pack.md` |
| 2 | Old Sprint 1 material | `docs/sprints/sprint-001/sprint-001-execution-pack.md` |
| 3 | Old Sprint 2 material | `docs/sprints/sprint-002/sprint-002-execution-pack.md` |
| 4 | Old Sprint 3 material | `docs/sprints/sprint-003/sprint-003-execution-pack.md` |
| 5 | Old master roadmap | `docs/roadmap/sprint-roadmap.md` |
| 6 | Old toolchain list | `docs/engineering/technology-toolchain-lock.md` |

# 3. Supporting files

```text
docs/sprints/README.md
REPLACEMENT-MAP.md
docs/historical/README.md
manifest.json
```

# 4. Installation notes

1. Back up the six old files before removal.
2. Remove old files from the root `docs/` directory.
3. Copy the `docs/` tree into the project, preserving paths.
4. Move the old master Sprint file to `docs/historical/` only if historical retention is needed.
5. Add a `SUPERSEDED / DO NOT USE FOR IMPLEMENTATION` banner to any archived master.
6. Update `README.md` so mandatory reading uses the canonical paths above.
7. Do not start Sprint 1 before the Sprint 0 Acceptance Report is `PASS`.

# 5. Status of this pack

```text
Project: Greenfield / code not started
Sprint 0: READY_FOR_REVIEW
Sprint 1: PLANNED_NOT_ACTIVE
Sprint 2: PLANNED_NOT_ACTIVE
Sprint 3: PLANNED_NOT_ACTIVE
Sprint 4–57: ROADMAP_ONLY
```

# 6. Rules

- This pack does not modify other canonical documents.
- The old master is intentionally not included to avoid a competing source of truth.
- Historical documents must never be used for implementation.
