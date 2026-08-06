# CRM_BDS_AI — TECHNOLOGY TOOLCHAIN LOCK

## Approved technology families, exact core locks and repository pinning rules

**Document ID:** `ENG-TOOLCHAIN-001`  
**Canonical path:** `docs/engineering/technology-toolchain-lock.md`  
**Product:** `crm_bds_ai`  
**Version:** `1.0.0`  
**Status:** `Accepted Baseline / Sprint 0 Validation Required`  
**Canonical scope:** Approved runtimes, frameworks, infrastructure technologies, package-management strategy and exact-version authority  
**Owner:** `Engineering Owner`  
**Reviewers:** `Architecture Owner`, `Security Owner`, `Database Owner`, `Frontend Owner`, `Operations Owner`, `QA Owner`  
**Effective date:** `2026-08-05`  
**Last reviewed:** `2026-08-05`  
**Supersedes:** `None — Greenfield baseline`  
**Classification:** `INTERNAL`

---

# 1. Mục đích

Toolchain Lock ngăn Goose, Opencode hoặc contributor tự chọn lại stack, tự nâng major version hoặc thêm công cụ cạnh tranh trong khi triển khai Sprint nghiệp vụ.

Tài liệu này là nguồn chuẩn cho:

- Approved runtime/framework/infrastructure families.
- Exact core versions đã được Product/Engineering baseline chấp nhận.
- Cách exact package versions được pin trong repository.
- Lockfiles và container-image authority.
- Unsupported/competing alternatives.
- Upgrade and exception workflow.

Tài liệu này không tuyên bố các version là “latest”. Đây là project-approved baseline.

---

# 2. Status vocabulary

| Status | Meaning |
|---|---|
| `EXACT_LOCK` | Exact version được chấp nhận; repository phải pin đúng |
| `APPROVED_FAMILY` | Technology được chấp nhận; exact patch phải pin trong Sprint 0 |
| `LOCKFILE_GOVERNED` | Exact transitive/direct package version lấy từ committed lockfile |
| `PENDING_VALIDATION` | Chưa được dùng để code cho tới khi Sprint 0 giải quyết |
| `ENVIRONMENT_SPECIFIC` | Giá trị thuộc deployment/configuration, không phải universal version |
| `PROHIBITED_WITHOUT_ADR` | Không được thêm/thay nếu không có ADR/approval |

---

# 3. Authority hierarchy

1. File này xác định approved technology and core locks.
2. Runtime version files pin exact local/CI runtime.
3. Backend/frontend lockfiles pin exact dependencies.
4. Container manifests/digests pin runtime images.
5. CI verifies clean installation and compatibility.
6. Sprint Packs reference Toolchain Lock; they MUST NOT duplicate version matrices.

Khi file này khác committed lockfile:

- Không tự chọn một bên.
- Treat as toolchain drift.
- Stop affected implementation.
- Resolve through Toolchain change process.

---

# 4. Exact core locks

Các version sau là project baseline đã được chọn, không phải claim về phiên bản mới nhất:

| Capability | Technology | Version | Status | Exact pin location expected |
|---|---|---:|---|---|
| Backend language | Python | `3.14.6` | `EXACT_LOCK` | runtime version file + CI/container |
| Backend web framework | FastAPI | `0.139.2` | `EXACT_LOCK` | backend manifest + lockfile |
| ORM/data mapper | SQLAlchemy | `2.0.51` | `EXACT_LOCK` | backend manifest + lockfile |
| Operational database | PostgreSQL | `18.4` | `EXACT_LOCK` | container/image/IaC |
| Message broker | RabbitMQ | `4.3.3` | `EXACT_LOCK` | container/image/IaC |
| Cache/coordination | Valkey | `9.1.0` | `EXACT_LOCK` | container/image/IaC |
| Frontend framework | Next.js | `16.2.11` | `EXACT_LOCK` | frontend manifest + lockfile |
| UI library | React | `19.2.8` | `EXACT_LOCK` | frontend manifest + lockfile |
| Frontend language | TypeScript | `6.0.0` | `EXACT_LOCK` | frontend manifest + lockfile |

A Sprint MUST NOT restate these versions. It should say: `Use the accepted Technology Toolchain Lock.`

---

# 5. Approved backend families

| Capability | Approved technology | Status before repository lock |
|---|---|---|
| Validation/settings | Pydantic ecosystem compatible with locked FastAPI | `APPROVED_FAMILY` |
| Migration | Alembic | `APPROVED_FAMILY` |
| PostgreSQL driver | Psycopg | `APPROVED_FAMILY` |
| Background task runtime | Celery | `APPROVED_FAMILY` |
| Structured logging | structlog-compatible approved stack | `APPROVED_FAMILY` |
| Telemetry | OpenTelemetry | `APPROVED_FAMILY` |
| HTTP client | approved async-capable client | `APPROVED_FAMILY` |
| Testing | pytest ecosystem | `APPROVED_FAMILY` |
| Formatting/lint | Ruff | `APPROVED_FAMILY` |
| Static typing | Pyright strict | `APPROVED_FAMILY` |
| Dependency management | one approved Python project manager/lock workflow | `PENDING_VALIDATION` |

Sprint 0 MUST resolve exact direct versions and the package-manager/lockfile workflow before Sprint 1 activation.

No backend dependency may be added solely for convenience. Admission requires purpose, license, security, maintenance, overlap and removal assessment.

---

# 6. Approved frontend families

| Capability | Approved technology | Status before repository lock |
|---|---|---|
| JavaScript runtime | Node.js `24 LTS` line | `APPROVED_FAMILY`; exact patch pending |
| Package manager | pnpm | `APPROVED_FAMILY`; exact version pending |
| Server state | TanStack Query | `APPROVED_FAMILY` |
| Enterprise tables | TanStack Table | `APPROVED_FAMILY` |
| Forms | React Hook Form | `APPROVED_FAMILY` |
| Client validation | Zod | `APPROVED_FAMILY` |
| Styling | Tailwind CSS | `APPROVED_FAMILY` |
| Accessible primitives | Radix UI | `APPROVED_FAMILY` |
| Approved analytics charts | Recharts or Design-System-approved wrapper | `APPROVED_FAMILY` |
| Unit/component tests | Vitest + Testing Library | `APPROVED_FAMILY` |
| API mocking | MSW | `APPROVED_FAMILY` |
| E2E | Playwright | `APPROVED_FAMILY` |

Exact versions MUST be committed in the frontend manifest/lockfile and copied back into the reviewed Toolchain inventory or generated manifest.

Frontend packages must also pass bundle, accessibility, maintenance and security review.

---

# 7. Approved infrastructure and interface standards

| Area | Baseline | Authority |
|---|---|---|
| Architecture | Modular Monolith first | Architecture Overview + ADR |
| Database layout | One PostgreSQL database, schema per Context + `infra` | Architecture/ADR/Alembic |
| Async transport | Celery over RabbitMQ baseline | ADR + Toolchain + environment config |
| Cache/coordination | Valkey, never business source of truth | Architecture + Toolchain |
| File binary | S3-compatible object storage | Architecture + environment decision |
| API | REST + OpenAPI `3.1` | API Standards + OpenAPI |
| Event schema | JSON Schema `2020-12` | Event Standards + schemas |
| Event documentation | AsyncAPI `3.x` | Event Standards + AsyncAPI |
| Errors | Problem Details baseline | API Standards + Error Registry |
| Money | Decimal/numeric policy, never binary float | Database/Coding Standards |
| Time | UTC persisted with timezone-aware types; business interpretation uses approved timezone | Database/Domain standards |
| Identifiers | UUID strategy only as approved by ADR/Database Standards | ADR + migrations |
| Containers | OCI-compatible images and Compose-compatible local environment | Environment/operations config |

Exact object-storage implementation, container engine patch, operating-system image, API path, queue name and topology are not invented by this file.

---

# 8. Required repository pins

Sprint 0 MUST resolve and Sprint 1 MUST commit:

## Runtime pins

- Python exact version file.
- Node.js exact patch/version file.
- pnpm exact version configuration.
- Container base image tags or digests.

## Backend

- Project manifest.
- Fully resolved lockfile.
- Hash/checksum verification when tooling supports it.
- Separate approved dependency groups for runtime/dev/test where appropriate.

## Frontend

- `package.json` with exact/range policy approved.
- `pnpm-lock.yaml` or canonical pnpm lockfile.
- Package-manager version pin.
- Deterministic clean install command.

## Infrastructure

- PostgreSQL, RabbitMQ and Valkey exact images.
- Object-storage image/version after Sprint 0 validation.
- Health-check compatibility evidence.

## CI

- Same runtime major/minor/patch where exact lock applies.
- Clean install from lockfiles.
- No implicit floating `latest` tags.

---

# 9. Pending Sprint 0 validations

The following are blockers for Sprint 1 until resolved:

1. Exact Python dependency manager and version.
2. Exact Pydantic, Alembic, Psycopg and Celery versions.
3. Exact logging/telemetry packages and versions.
4. Exact Node.js patch and pnpm version.
5. Exact TanStack/Form/Zod/Tailwind/Radix/Recharts/test package versions.
6. Exact S3-compatible local object-storage implementation and version.
7. Exact backend/frontend base container images.
8. Supported developer OS/architecture matrix.
9. CI runner/base-image compatibility.
10. License and security review for direct dependencies.

These are not invitations for Opencode to choose freely. Goose must prepare a Toolchain validation change and obtain approval.

---

# 10. Prohibited competing choices without ADR

Do not add or replace with a competing core technology without formal review, for example:

- Another backend web framework.
- Another ORM/migration stack.
- Another operational database.
- Kafka, NATS or another broker.
- Redis as an unreviewed replacement for Valkey.
- npm/yarn as a parallel package-manager workflow.
- Another frontend meta-framework.
- Another global state/form/table/component/chart stack that duplicates an approved capability.
- A second observability SDK stack.
- A second object-storage abstraction without need.

This is not a permanent ban. It is a prohibition on unreviewed duplication or replacement.

---

# 11. Dependency admission process

A new direct dependency requires:

- Problem/use case.
- Owning area.
- Alternatives considered.
- Existing capability overlap.
- License.
- Maintenance/community signal.
- Security history/current findings.
- Transitive dependency impact.
- Bundle/runtime size.
- Performance/operational impact.
- Accessibility impact for UI.
- Removal/migration strategy.
- Exact version and lockfile update.
- Tests.
- Approval level according to impact.

Small utility packages are not exempt if equivalent code is trivial or dependency risk exceeds value.

---

# 12. Upgrade policy

## Patch/minor

May be proposed through Toolchain maintenance work when:

- Compatibility is verified.
- Lockfiles updated.
- Changelog/security impact reviewed.
- Full relevant CI passes.
- Generated contracts/build artifacts remain deterministic.

## Major

Requires:

- ADR or architecture/toolchain review.
- Migration plan.
- Compatibility analysis.
- Rollback plan.
- Dedicated Sprint or approved scope.
- Documentation update.

Business Sprint MUST NOT silently upgrade major runtime/framework versions.

## Security emergency

Emergency upgrade still requires:

- Evidence of vulnerability/applicability.
- Minimum safe change.
- Test evidence.
- Exception/approval record.
- Follow-up normalization.

---

# 13. Container and supply-chain rules

- No floating `latest` in canonical CI/production manifests.
- Prefer immutable digest in production when operational policy supports it.
- Base images must be minimal, supported and scanned.
- Lockfiles are committed.
- Generated build/cache directories are not committed unless explicitly canonical.
- SBOM and dependency/container scans are release evidence when tooling is enabled.
- Secrets are injected, not baked into images.
- Build provenance/signing requirements belong to deployment/supply-chain policy.

---

# 14. Environment compatibility

Toolchain Lock distinguishes:

- Developer local.
- CI.
- Test/ephemeral integration.
- Staging/UAT.
- Production.

A technology may be approved but unavailable in one environment; this is an environment blocker, not permission to substitute a competing stack silently.

Exact resource limits, replicas, retention, network exposure, TLS and topology are environment-specific.

---

# 15. Verification requirements

Before Sprint 1 activation, evidence must show:

- Runtime version commands match pins.
- Backend lockfile resolves/install succeeds from clean environment.
- Frontend frozen install succeeds.
- Database/broker/cache/object-storage images start and become healthy.
- Backend/frontend/tooling compatibility tests pass.
- No floating core dependency.
- No duplicate package manager.
- Security/license scan reviewed.

Before each Sprint:

- No unapproved toolchain drift.
- Lockfiles unchanged unless task authorizes it.
- New dependency changes are explicitly reported.

---

# 16. AI Agent rules

Goose MUST:

- Read this file before task decomposition.
- Detect toolchain drift.
- Prevent version duplication in Sprint prompts.
- Require dependency justification.
- Stop unapproved major upgrades.
- Verify lockfile changes independently.

Opencode MUST NOT:

- Install “latest”.
- Add dependency because it is familiar.
- Switch package manager.
- Add competing framework/library stack.
- Rewrite lockfile unrelated to task.
- Claim version compatibility without running checks.

---

# 17. Definition of Ready for implementation

Toolchain is ready for Sprint 1 when:

1. All core runtime exact locks are pinned.
2. Approved-family direct dependencies have exact resolved versions.
3. Backend/frontend lockfile strategies are selected.
4. Node/pnpm/object-storage pending items are resolved.
5. Local/CI compatibility is verified.
6. No Critical/High unaccepted supply-chain blocker.
7. Toolchain Acceptance section in Sprint 0 report is PASS.

---

# 18. Definition of Done for a Toolchain change

A Toolchain change is Done when:

- File metadata/version/changelog updated.
- Manifests/lockfiles/runtime pins updated.
- Containers/CI updated.
- Compatibility/security/license analysis recorded.
- Full required tests pass.
- Migration/rollback documented.
- Sprint Packs do not duplicate old versions.
- Approval recorded.

---

# 19. Changelog

## Version 1.0.0 — 2026-07-26

- Established this rewritten file as the sole exact-version authority.
- Preserved accepted core locks.
- Separated exact locks, approved families and pending validation.
- Removed the expectation that Sprint Packs repeat version matrices.
- Added repository pinning, dependency admission, upgrade and supply-chain rules.
- Added Sprint 0 validation gate for unresolved exact versions.

---

# 20. Kết luận

```text
Approved Technology
+ Exact Repository Pins
+ Deterministic Lockfiles
+ Controlled Upgrades
+ No Competing Stack Drift
= REPRODUCIBLE TOOLCHAIN
```
