# CRM_BDS_AI �?" SYNCHRONIZED FOUNDATION REPLACEMENT PACK

GA3i nA�y �`��"ng b��T sA�u tA�i li���u c�c v��>i Product Overview, PRD, Architecture Overview, AI Agent Engineering Constitution, Universal Orchestration Skill, Documentation Governance vA� Engineering Standards m��>i.

## Six primary replacements

```text
docs/sprints/sprint-000/sprint-000-preparation-pack.md
docs/sprints/sprint-001/sprint-001-execution-pack.md
docs/sprints/sprint-002/sprint-002-execution-pack.md
docs/sprints/sprint-003/sprint-003-execution-pack.md
docs/roadmap/sprint-roadmap.md
docs/engineering/technology-toolchain-lock.md
```

Supporting files:

```text
docs/sprints/README.md
REPLACEMENT-MAP.md
docs/historical/README.md
manifest.json
```

## Current project status encoded by this pack

```text
Project: Greenfield / code not started
Sprint 0: READY_FOR_REVIEW
Sprint 1: ACTIVE (Sprint 0 report PASS WITH CONDITIONS accepted 2026-08-06)
Sprint 2: PLANNED_NOT_ACTIVE
Sprint 3: PLANNED_NOT_ACTIVE
Sprint 4�?"57: ROADMAP_ONLY
```

## Installation

1. Back up the six old files.
2. Remove them from the root `docs/` directory.
3. Copy the `docs/` tree in this package into the project, preserving paths.
4. Move the old master Sprint file to `docs/historical/` only if historical retention is needed.
5. Add a `SUPERSEDED / DO NOT USE FOR IMPLEMENTATION` banner to the archived master.
6. Update `README.md` so mandatory reading uses:
   - `docs/architecture/architecture-overview.md`, not the old mega architecture path.
   - `docs/roadmap/sprint-roadmap.md`, not the old master.
   - `docs/sprints/README.md` for current Sprint status.
7. Do not start Sprint 1 before Sprint 0 Acceptance Report is PASS.

## Important

This package does not modify the other canonical documents. It expects those documents to be placed at their canonical paths.

The old master is not included to avoid reintroducing a competing source of truth.
