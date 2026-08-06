# CRM_BDS_AI — SPRINT 3 EXECUTION PACK

## Enterprise, Legal Entity, Business Calendar and Numbering Foundation

**Document ID:** `SPRINT-003-EXECUTION-PACK`  
**Canonical path:** `docs/sprints/sprint-003/sprint-003-execution-pack.md`  
**Product:** `crm_bds_ai`  
**Version:** `1.0.0`  
**Status:** `Planned / Not Active`  
**Activation condition:** `Sprint 0, Sprint 1 and Sprint 2 Acceptance Reports = PASS`  
**Sprint type:** `Platform Business Foundation`  
**Primary Context:** `platform`  
**Supporting Contexts:** `audit`, `operations`; `iam` only through approved bootstrap/security contracts, not full IAM implementation  
**Owner:** `Platform Context Owner`  
**Reviewers:** `Product Owner`, `Architecture Owner`, `Security Owner`, `Database Owner`, `API Owner`, `Event Architecture Owner`, `Frontend Owner`, `QA Owner`  
**Effective date:** `2026-08-05`  
**Supersedes:** `None — Greenfield baseline`  
**Classification:** `INTERNAL`

---

# 1. Mục đích

Sprint 3 triển khai capability nền tảng của Platform Context:

- Enterprise root theo tenancy decision đã được chấp nhận.
- Legal Entity.
- Timezone/currency references.
- Business Calendar.
- Numbering foundation.

Sprint Pack này không tự quyết định hệ thống hỗ trợ một hay nhiều Enterprise trong một deployment. Exact tenancy semantics phải đến từ Product/Architecture/ADR được phê duyệt trước khi Sprint active.

---

# 2. Sprint Goal

> Xây dựng Platform foundation có lifecycle, effective versioning, concurrency safety, authorization hooks, audit, events và machine-readable contracts để các Context sau sử dụng Enterprise/Legal Entity, business time và business numbering nhất quán.

---

# 3. Authority and mandatory reading

```text
README.md
docs/product/product-overview.md
docs/product/PRD.md
docs/product/domain-glossary.md
docs/architecture/architecture-overview.md
docs/architecture/context-map.md
docs/architecture/source-of-truth-matrix.md
docs/engineering/ai-agent-engineering-constitution.md
.skills/universal-ai-engineering-orchestration/SKILL.md
docs/engineering/documentation-governance.md
docs/engineering/technology-toolchain-lock.md
Relevant Accepted ADRs
Relevant Engineering Standards
Relevant Context Implementation Pack
Current Sprint Execution Pack
Current Project Status and Handoff, when they exist
Existing machine-readable contracts, migrations, code and tests, when they exist
```

Bắt buộc thêm:

```text
docs/contexts/platform/ relevant accepted Context Implementation Pack
docs/engineering/database-standards.md
docs/engineering/api-standards.md
docs/engineering/event-standards.md
docs/engineering/testing-standards.md
docs/engineering/security-standards.md
docs/engineering/frontend-standards.md when UI is enabled
Relevant design-system and navigation documents when UI is enabled
Sprint 2 Acceptance Report
```

Exact authority:

- Platform invariants/state machines: Platform Context Pack.
- Exact DDL: Alembic.
- Exact APIs: OpenAPI.
- Exact Events: JSON Schema + AsyncAPI.
- Exact permissions/scopes/errors: registries/matrices.
- Exact UI routes/components: Navigation/Design System/code.
- Exact runtime values: configuration/policy.

---

# 4. Preconditions and blocking decisions

Before activation, Goose MUST verify:

1. Sprint 2 Acceptance Report is `PASS`.
2. Platform Context Pack is accepted for Sprint 3 scope.
3. Enterprise tenancy/root semantics are formally approved.
4. Legal Entity identity and uniqueness semantics are approved.
5. Currency/timezone reference policy is approved.
6. Numbering gap/reuse/legal constraints are classified; no unapproved promise of gapless numbering.
7. Bootstrap access/security mechanism is approved for any exposed API/UI.
8. Permission/error registry process exists.
9. Design System/Navigation prerequisites exist if production UI is in scope.
10. Current Sprint pointer is Sprint 3 and no future Sprint is active.

If no approved authentication/bootstrap mechanism exists, production-exposed administration API/UI is BLOCKED. The Agent MUST NOT bypass authorization merely because full IAM is scheduled later.

---

# 5. In Scope

## 5.1. Enterprise root

Implement Enterprise according to accepted tenancy decision, including only approved capabilities such as:

- Canonical identity/code/display metadata.
- Lifecycle commands.
- Version/concurrency behavior.
- Status/effective history where required.
- Audit and Integration Events.
- Read models needed by Sprint 3.

Do not assume:

- Multiple Enterprise per deployment.
- Cross-Enterprise administration.
- Enterprise-level base currency.
- Archive/reactivate transitions.

unless Platform Context Pack explicitly defines them.

## 5.2. Legal Entity

Implement:

- Legal identity and business code semantics.
- Relationship to Enterprise root.
- Timezone and base/functional currency reference required by product decision.
- Lifecycle and effective period.
- Readiness/activation validation.
- Audit and Events.
- Version/concurrency control.

Exact registration/tax/address fields are Context-specific and MUST NOT be invented from examples.

## 5.3. Currency and timezone reference policy

Sprint 3 MUST establish:

- IANA timezone storage/validation policy.
- ISO currency-code reference policy.
- UTC storage and local-time interpretation boundaries.
- No implicit cross-currency arithmetic.
- No automatic exchange-rate integration.

Exact supported currencies/countries remain Product/Policy decisions.

## 5.4. Business Calendar

Implement capability for:

- Calendar identity and ownership scope.
- Versioned definitions.
- Weekly working pattern.
- Holidays/non-working exceptions.
- Approved special working exceptions.
- Effective dating.
- Publish/activate semantics.
- Deterministic working-day and business-duration calculations.
- Immutability of published/effective versions according to Context Pack.
- Overlap/conflict validation.
- Audit and Events.

Exact break rules, calendars, holiday datasets and default hours are configuration, not hard-coded product truth.

## 5.5. Numbering foundation

Implement capability for:

- Numbering Scheme identity and ownership scope.
- Versioned format policy.
- Validation and preview.
- Effective/published version.
- Concurrency-safe issuance.
- Idempotent issuance.
- Durable issuance ledger.
- No reuse of an issued business number.
- Audit and Events.
- Internal application port for future Contexts.

Mandatory boundaries:

- Không dùng `count + 1`, `max + 1` hoặc timestamp-only.
- Không execute arbitrary code/SQL expressions in format.
- Không promise contiguous/gapless numbering unless legal/product policy explicitly requires and architecture supports it.
- Number reservation, issuance and transaction coupling must be defined in Platform Context Pack; Agent không tự chọn.

## 5.6. APIs

Provide application/internal APIs for approved Platform capabilities.

Requirements:

- REST/domain intent according to API Standards.
- Dedicated commands for sensitive lifecycle transitions.
- Backend authorization and scope hooks.
- Idempotency/concurrency where required.
- Stable errors from registry.
- OpenAPI 3.1 exact contract.
- No generic PATCH to bypass state machines.

Exact paths, methods and payloads are created in OpenAPI during Sprint.

## 5.7. Events

Publish only approved facts for Platform changes.

Requirements:

- Outbox in same transaction.
- JSON Schema and AsyncAPI.
- Minimal payload, reference over unnecessary snapshot.
- Versioning and compatibility.
- Correlation/causation/actor context.
- No speculative Events for future Contexts.

Exact Event names and payloads are not defined by this Sprint Pack.

## 5.8. Authorization, scope and audit

- Deny by default.
- Backend enforcement.
- Enterprise/Legal Entity scope according to approved tenancy model.
- Field masking for sensitive legal data.
- Audit sensitive transitions and numbering operations.
- No trust in client-supplied Enterprise/Legal Entity ownership.
- No production bootstrap superuser shortcut without approved, time-bound, audited mechanism.

Exact permissions, role baselines and masking rules belong to registries/matrices.

## 5.9. Administration UI — conditional

Production UI is included only when:

- Approved access mechanism exists.
- Design System and navigation prerequisites are ready.
- Sprint activation review explicitly marks UI `ENABLED`.

When enabled, UI may include approved management flows for Enterprise, Legal Entity, Calendar and Numbering.

UI MUST:

- Reflect backend state/permission.
- Support loading, empty, error, conflict, permission and processing states.
- Use generated API client.
- Avoid calculating official business time or issuing numbers client-side.

When prerequisites are absent, UI is `DEFERRED`, not replaced by insecure local-only production route. Domain/application/API work may proceed only if independently safe and accepted.

## 5.10. Contracts, migrations, tests and docs

Create/update:

- Platform Context documentation.
- Alembic migrations.
- OpenAPI.
- Event schemas/AsyncAPI.
- Permission/error registries.
- Unit/integration/concurrency/contract/security tests.
- UI tests when UI enabled.
- Runbooks for numbering and calendar diagnostics.
- Sprint implementation notes and Acceptance Report.

---

# 6. Out of Scope

Sprint 3 MUST NOT implement:

- Organization Units, positions, employees or workforce assignments.
- OIDC authentication.
- Full User/Role/Permission/Scope administration.
- Delegation or access review.
- Configuration Registry.
- Generic Workflow Engine.
- Approval Policy Engine.
- Feature Flags.
- Business-specific SLA runtime.
- Accounting ledger, chart of accounts or invoice/e-invoice.
- Exchange-rate provider.
- Tax engine.
- Project/asset/listing numbering policies.
- Arbitrary template/expression execution.
- Cross-Enterprise consolidation.
- Production holiday-provider integration.
- Future Context entities/tables/events.

---

# 7. Delegated decisions matrix

| Subject | Owner/source | Sprint behavior |
|---|---|---|
| One vs multiple Enterprise | Product/ADR | Must be resolved before activation |
| Enterprise/Legal Entity state machine | Platform Context Pack | Implement exactly |
| Exact legal fields | Platform Context Pack/PRD | Do not invent |
| Exact DDL/indexes | Alembic | Create and test |
| Exact API | OpenAPI | Generate/commit |
| Exact Events | JSON Schema + AsyncAPI | Generate/commit |
| Permissions/scope/masking/errors | Registries/matrices | Add approved entries |
| Calendar hours/holidays | Configuration | No universal hard-code |
| Number format/reset/gap policy | Platform policy/config | Versioned and approved |
| UI routes/components | Navigation/Design System | Only if UI enabled |
| Concurrency test volume | Test plan/NFR | Overlapping real transactions required |

---

# 8. Suggested micro-task graph

1. Resolve/verify blocking Product and Architecture decisions.
2. Platform exact domain/state design review.
3. Enterprise/Legal Entity domain and tests.
4. Enterprise/Legal Entity persistence/migrations.
5. Calendar domain algorithms and property/boundary tests.
6. Calendar persistence/migrations.
7. Numbering domain/issuance concurrency design.
8. Numbering persistence and concurrency tests.
9. Application commands/queries and authorization hooks.
10. OpenAPI, permissions and errors.
11. Events/Outbox contracts.
12. Conditional UI implementation.
13. Full security/concurrency/contract/E2E verification.
14. Runbooks, docs and Acceptance Report.

Database migrations affecting shared Platform tables MUST be serialized; Goose should not parallelize conflicting migration tasks.

---

# 9. Test matrix

## 9.1. Enterprise and Legal Entity

- Valid lifecycle transitions.
- Invalid transition rejection.
- Uniqueness according to approved scope.
- Optimistic concurrency conflict.
- Activation readiness validation.
- Unauthorized/out-of-scope access.
- Sensitive-field masking.
- Audit and Event atomicity.

## 9.2. Business Calendar

- Weekly working patterns.
- Holiday and special-working exceptions.
- Timezone/DST boundaries using approved IANA zones.
- Effective-version selection.
- Overlapping version rejection.
- Published/effective immutability.
- Deterministic calculations.
- Invalid configuration rejection.

Do not bake a particular country's holiday calendar into universal tests unless policy requires it.

## 9.3. Numbering

- Scheme validation/preview.
- Effective version selection.
- Concurrent issuance with separate transactions/sessions.
- Same idempotency request does not issue twice.
- Issued number is never reused.
- Failure windows and retry behavior.
- Unauthorized issuance.
- Audit and Event evidence.
- No `max + 1`/`count + 1` implementation.

## 9.4. Contracts and security

- OpenAPI deterministic/valid.
- Event schemas/AsyncAPI valid/compatible.
- Permissions/errors registered.
- Scope tampering rejected.
- Mass assignment rejected.
- Internal APIs not publicly exposed by accident.
- No production access bypass.

## 9.5. UI when enabled

- Permission states.
- Loading/empty/error/conflict.
- Form validation aligned backend.
- Calendar preview semantics.
- Number preview not treated as issued number.
- Accessibility and production build.

---

# 10. Security and privacy

- Legal Entity tax/registration/address fields classified and minimized.
- Backend authorization required.
- No client-controlled scope/ownership.
- No raw sensitive fields in logs/events.
- Number issuance/reconfiguration is audited.
- Published/effective configuration changes require approved control policy.
- Bootstrap administration is time-bound/audited or unavailable; never silently permanent.

---

# 11. Observability

Signals SHOULD cover:

- Lifecycle command success/failure/conflict.
- Calendar calculation errors/config conflicts.
- Number issuance success/conflict/latency and anomaly.
- Event Outbox status.
- Authorization denials and sensitive changes.

Exact metrics/labels/alerts belong to catalogs/SLO.

---

# 12. Risks

| Risk | Control |
|---|---|
| Sprint assumes wrong tenancy model | Blocking ADR/Product decision |
| Admin UI bypasses not-yet-built IAM | Conditional UI and approved bootstrap mechanism |
| Calendar time/DST errors | IANA timezone + deterministic boundary tests |
| Duplicate business numbers | Database concurrency + idempotency + ledger |
| Promise of gapless numbering without legal design | Explicit policy decision, no assumption |
| Published config mutated | Immutability and versioned replacement |
| Future Context scope leaks into Platform | Out of Scope and architecture review |

---

# 13. Definition of Ready

Sprint 3 Ready when:

1. Sprint 2 PASS.
2. Platform Context Pack accepted.
3. Tenancy/Enterprise decision accepted.
4. Numbering policy boundaries accepted.
5. Security bootstrap/exposure decision accepted.
6. Machine-contract and registry owners assigned.
7. Test environment supports concurrency/timezone tests.
8. UI prerequisites resolved or UI explicitly deferred.
9. Goose has task graph and allowed-file boundaries.

---

# 14. Definition of Done

Sprint 3 only Done when:

1. Approved Enterprise/Legal Entity behavior implemented.
2. Business Calendar behavior/versioning verified.
3. Numbering issuance is concurrency-safe, idempotent and non-reusing.
4. Alembic constraints/indexes and PostgreSQL tests pass.
5. OpenAPI/Event schemas/AsyncAPI/registries align.
6. Backend authorization/scope/masking tests pass.
7. Audit/Outbox atomicity verified.
8. Conditional UI either passes all gates or is explicitly deferred in accepted scope.
9. Full repository quality/CI pass.
10. Docs/runbooks/handoff updated.
11. Acceptance Report has real evidence.
12. Organization/IAM/Workflow future scope was not implemented early.

---

# 15. Acceptance Report

`docs/sprints/sprint-003/acceptance-report.md` MUST include:

- Approved tenancy/Platform decisions used.
- Commit range/hash.
- Migration revisions.
- Domain/state evidence.
- Calendar timezone/effective-version tests.
- Numbering concurrency/idempotency evidence.
- API/Event/permission/error contract results.
- Security/scope/masking evidence.
- UI status and evidence when enabled.
- Operational signals/runbooks.
- Deviations, exceptions and limitations.
- Final status/sign-off.

---

# 16. Chỉ thị cho Goose và Opencode

## Goose

- Do not accept old exact fields/state/API/Event inventories without comparing Platform Context Pack.
- Stop on unresolved tenancy or access-control decisions.
- Require real concurrent database tests for numbering.
- Treat UI as conditional, not justification for an auth bypass.
- Independently inspect migrations and machine contracts.

## Opencode

- Implement only approved Platform scope.
- Do not build Organization/IAM/Workflow early.
- Do not invent legal/tax fields.
- Do not use unsafe number generation.
- Do not place business calculation in frontend.
- Report exact evidence and unresolved decisions.

---

# 17. Kết luận

```text
Approved Enterprise Boundary
+ Trusted Legal Entity Identity
+ Versioned Business Time
+ Concurrency-Safe Numbering
+ Backend Security Hooks
+ Audit and Reliable Events
= PLATFORM_FOUNDATION_READY
```
