# CRM_BDS_AI — SPRINT 1 EXECUTION PACK

## Repository and Local Engineering Platform Foundation

**Document ID:** `SPRINT-001-EXECUTION-PACK`  
**Canonical path:** `docs/sprints/sprint-001/sprint-001-execution-pack.md`  
**Product:** `crm_bds_ai`  
**Version:** `1.0.0`  
**Status:** `Planned / Not Active`  
**Activation condition:** `Sprint 0 Acceptance Report = PASS`  
**Sprint type:** `Engineering Foundation`  
**Primary owner:** `Engineering Owner`  
**Reviewers:** `Architecture Owner`, `Security Owner`, `Database Owner`, `Frontend Owner`, `QA Owner`, `Operations Owner`  
**Effective date:** `2026-08-05`  
**Supersedes:** `None — Greenfield baseline`  
**Classification:** `INTERNAL`

---

# 1. Mục đích

Sprint 1 tạo repository có thể cài đặt, chạy, kiểm thử và tiếp tục phát triển một cách có kiểm soát.

Sprint này xây engineering platform tối thiểu cho:

- Backend application shell.
- Frontend application shell.
- Worker và scheduler shell.
- Local infrastructure.
- Configuration and secret boundaries.
- Migration bootstrap.
- Contract bootstrap.
- Structured logging và correlation.
- Automated quality gates.
- Documentation runtime artifacts.

Sprint 1 không triển khai business domain của bất kỳ Bounded Context nào.

---

# 2. Sprint Goal

> Tạo repository Greenfield reproducible, có toolchain được khóa, local runtime đáng tin cậy, CI baseline và architectural guardrails để Sprint 2 có thể xây database/event reliability foundation mà không phải sửa lại nền móng.

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

Sprint Pack này chỉ khóa phạm vi Sprint 1. Nó không được override Product, Architecture, ADR, Toolchain Lock hoặc Engineering Standards.

Exact dependency versions MUST được lấy từ Technology Toolchain Lock và project lockfiles, không chép lại trong file này.

---

# 4. Preconditions

Goose MUST xác minh:

1. Sprint 0 Acceptance Report là `PASS`.
2. Sprint 1 được chỉ định là current implementation Sprint.
3. Toolchain Lock không còn blocker cho repository initialization.
4. Git repository state được hiểu rõ.
5. Project directory không chứa source code ngoài phạm vi Greenfield đã được phê duyệt.
6. Required local tools có thể cài hoặc đã có.
7. Không có secrets thật trong tài liệu hoặc repository.
8. Architecture Overview, Context Map và Source of Truth Matrix là các bản canonical mới.
9. Old master Sprint document không nằm trong mandatory reading.
10. Goose đã tạo micro-task graph và verification plan.

Nếu có code tồn tại, Goose phải inspect và lập drift report; không được xóa hoặc ghi đè mù quáng.

---

# 5. In Scope

## 5.1. Repository governance

Thiết lập:

- Root README và developer quick start.
- License/classification theo quyết định Product Owner.
- `.gitignore`, `.editorconfig` và line-ending policy.
- Branch/commit/PR conventions theo Git Standards khi đã tồn tại.
- CODEOWNERS hoặc ownership mechanism phù hợp.
- Dependency update policy.
- Secret scanning baseline.
- Generated-artifact policy.

## 5.2. Top-level structure

Repository MUST có các vùng trách nhiệm rõ ràng, tối thiểu tương đương:

```text
backend/
frontend/
contracts/
infra/
scripts/
tests/
docs/
.agent/
.skills/
```

Đây là Sprint-level repository decision. Exact internal tree phải được ghi trong `implementation-notes.md` và code review.

Quy tắc:

- Không tạo 16 Context packages rỗng chỉ để trang trí.
- Chỉ tạo package có code hoặc contract thực sự thuộc Sprint.
- Không tạo `legacy`, `v1`, compatibility hoặc future-feature folders.
- Shared code phải có ownership và tiêu chí admission.

## 5.3. Backend shell

Backend shell MUST cung cấp:

- Application bootstrap.
- Typed configuration loading.
- Environment validation.
- Dependency composition boundary.
- Health/liveness/readiness capability.
- Structured logging.
- Request ID và Correlation ID propagation.
- Standard error boundary.
- OpenAPI bootstrap.
- Graceful startup/shutdown.
- Test harness.

Backend shell MUST NOT có:

- Business aggregate.
- Business table.
- Customer/Lead/Product sample CRUD.
- IAM/authentication implementation.
- Cross-context repository.

## 5.4. Frontend shell

Frontend shell MUST cung cấp:

- Application bootstrap.
- Design-system integration boundary.
- Typed environment boundary.
- Generated API-client integration point.
- Global error/loading/not-found behavior phù hợp framework đã khóa.
- Accessibility baseline.
- Observability integration point.
- Component test và production build foundation.

Frontend shell MUST NOT:

- Tự định nghĩa business permission.
- Tạo dashboard giả với official KPI.
- Tạo business routes/screens ngoài Sprint.
- Hard-code API response types độc lập OpenAPI.

## 5.5. Worker and scheduler shell

Thiết lập:

- Worker bootstrap.
- Scheduler bootstrap hoặc scheduling adapter theo Toolchain Lock.
- Typed configuration.
- Structured logs/correlation.
- Health/diagnostic capability.
- Graceful shutdown.
- Minimal technical smoke task không chứa business behavior.

Exact queues, routing keys, retry counts và timeouts thuộc Toolchain/Environment configuration và Sprint 2 contracts; Sprint 1 không được tự khóa bằng ví dụ.

## 5.6. Local infrastructure

Local environment MUST cung cấp các capability đã được phê duyệt:

- PostgreSQL.
- RabbitMQ.
- Valkey.
- S3-compatible object storage hoặc approved local substitute.
- Backend, frontend và worker runtime.

Local stack MUST:

- Có health checks.
- Có named/declared persistence rõ.
- Không chứa production secret.
- Có startup/shutdown instructions.
- Phân biệt persistent developer data và disposable test resources.
- Không yêu cầu xóa persistent/shared data để chạy test.

Ephemeral test resources MAY được reset theo Testing Standards.

## 5.7. Database migration bootstrap

Thiết lập Alembic foundation:

- Migration configuration.
- Empty/baseline revision strategy.
- Transactional migration policy phù hợp PostgreSQL.
- Upgrade/downgrade verification harness.
- Không tạo business schemas/tables của Sprint 2 sớm.

Exact database thực thi sau này thuộc Alembic migrations.

## 5.8. Contract bootstrap

Thiết lập:

```text
contracts/openapi/
contracts/events/
contracts/asyncapi/
```

Yêu cầu:

- Valid OpenAPI 3.1 baseline generated từ application.
- Valid AsyncAPI baseline hoặc approved placeholder contract có status rõ.
- JSON Schema validation tooling.
- Deterministic generation/check commands.
- Contract drift check.
- Generated clients không được chỉnh tay.

Không tạo business endpoint hoặc business Event để “chuẩn bị trước”.

## 5.9. Quality tooling

Repository MUST có một documented quality entry point tương đương:

```text
python scripts/dev.py check
```

Tên lệnh cuối cùng phải được ghi trong README và CI. Nó phải orchestration được tối thiểu:

- Formatting check.
- Lint.
- Static type check.
- Unit tests.
- Architecture tests hiện có.
- Contract validation.
- Frontend type/lint/test/build.
- Secret scan baseline.

Tool-specific commands lấy từ Toolchain Lock và repository configuration.

## 5.10. CI baseline

CI MUST:

- Chạy từ clean checkout.
- Dùng locked dependencies.
- Cache an toàn, không biến cache thành source of truth.
- Chạy backend quality gates.
- Chạy frontend quality gates.
- Validate migrations/contracts.
- Build production artifacts.
- Không cần production deployment trong Sprint 1.
- Không bỏ qua failed step để báo green.

## 5.11. Architecture guardrails

Thiết lập test hoặc static checks ngăn tối thiểu:

- Domain phụ thuộc web/ORM/broker framework khi domain code xuất hiện.
- Cross-context repository/ORM import.
- Presentation gọi database trực tiếp.
- Frontend tự tạo business contract thay generated client.
- Secrets committed.
- Business tables trong `public` khi Sprint 2 bắt đầu.

Sprint 1 có thể tạo architecture test framework và test fixtures kỹ thuật, không cần tạo fake business contexts.

## 5.12. Documentation runtime

Tạo hoặc cập nhật:

```text
docs/project-status.md
docs/handoffs/current-handoff.md
docs/known-issues.md
docs/sprints/sprint-001/implementation-notes.md
docs/sprints/sprint-001/acceptance-report.md
.agent/project-profile.yaml
.agent/goose/state.json
.agent/goose/progress.md
```

Execution state không được dùng để tuyên bố Sprint Done.

---

# 6. Out of Scope

Sprint 1 MUST NOT triển khai:

- PostgreSQL schemas per Context; thuộc Sprint 2.
- Outbox, Inbox hoặc Idempotency business runtime; thuộc Sprint 2.
- Audit append-only store; thuộc Sprint 2.
- Enterprise, Legal Entity, Calendar hoặc Numbering; thuộc Sprint 3.
- Organization, workforce, IAM, OIDC, permissions hoặc scopes.
- Customer, Lead, Product, Booking, Contract, Payment, Revenue hoặc Commission.
- Business UI.
- Production topology.
- Production SLO/RPO/RTO.
- Microservices.
- Kubernetes hoặc cloud-specific platform nếu chưa có approved deployment decision.
- Future tables, routes, Events hoặc permissions.

---

# 7. Required artifacts

Exact file names may follow approved tooling, nhưng repository phải có bằng chứng tương đương cho:

- Backend dependency manifest và lockfile.
- Frontend dependency manifest và lockfile.
- Runtime version pins.
- Local compose/configuration.
- Backend bootstrap.
- Frontend bootstrap.
- Worker/scheduler bootstrap.
- Migration configuration.
- OpenAPI/AsyncAPI/JSON Schema validation.
- CI workflows.
- Quality scripts.
- Test configuration.
- Root and developer documentation.

`implementation-notes.md` MUST map conceptual artifact → exact path created.

---

# 8. Suggested micro-task graph

Goose SHOULD delegate in dependency order:

1. Repository metadata and version pins.
2. Backend manifest/lock and bootstrap.
3. Backend configuration/logging/health.
4. Frontend manifest/lock and bootstrap.
5. Worker/scheduler bootstrap.
6. Local infrastructure.
7. Alembic bootstrap.
8. Contract bootstrap.
9. Test and architecture-check foundation.
10. CI pipeline.
11. Documentation and end-to-end smoke verification.

Mỗi micro-task phải có:

- Allowed files.
- Forbidden files.
- Inputs.
- Expected outputs.
- Commands to verify.
- Acceptance criteria.
- Rollback/rework instructions.

Goose MUST independently inspect diffs and run relevant checks before accepting Opencode report.

---

# 9. Testing and verification

## 9.1. Clean setup

Từ clean checkout phải chứng minh:

- Locked dependency installation succeeds.
- Local infrastructure starts.
- Backend starts.
- Frontend starts/builds.
- Worker starts.
- Health checks respond.
- No business data seed is required.

## 9.2. Configuration

Test:

- Missing required production-like config fails fast.
- Local safe defaults chỉ xuất hiện ở local profile.
- Secrets không xuất hiện trong logs.
- Invalid values produce actionable errors.

## 9.3. Logging/correlation

Test:

- Request ID được tạo hoặc chấp nhận theo policy.
- Correlation ID propagate qua technical flow.
- Logs structured và redacted.
- Health checks không log excessive noise.

## 9.4. Contracts

Test:

- OpenAPI valid và deterministic.
- AsyncAPI/JSON Schema validation command pass.
- Generated artifacts không drift.

## 9.5. Migration

Test:

- Clean database upgrade tới head.
- Downgrade strategy thực thi hoặc có approved non-reversible note theo Database Standards.
- Re-upgrade pass.
- Không có business table ngoài scope.

## 9.6. CI

CI run phải có evidence:

- Exact commit.
- Jobs and results.
- No hidden allow-failure for mandatory gates.
- Artifacts/build result.

---

# 10. Security requirements

- Không commit secret, token, private key hoặc real PII.
- Dev credentials phải explicit local-only.
- Container ports không được coi là production exposure policy.
- Dependency admission tuân Security Standards.
- Health/diagnostic output không lộ config hoặc dependency credentials.
- CORS/CSRF/CSP exact policy không được đoán; environment/security config sở hữu.
- Debug mode không được mặc định cho production profile.

---

# 11. Observability requirements

Sprint 1 phải có foundation cho:

- Structured logs.
- Request/correlation identifiers.
- Basic process health.
- Startup/shutdown events.
- Build/version identity.
- Error capture boundary.

Exact metric names, alert thresholds, sampling và retention thuộc Observability Catalog/SLO/Environment configuration.

---

# 12. Risks

| Risk | Control |
|---|---|
| Toolchain version drift | Lockfiles, version files, CI clean install |
| Shell becomes business architecture | Strict Out of Scope and architecture tests |
| Local-only shortcuts leak to production | Typed environment profiles and fail-fast validation |
| Multiple quality commands diverge | One documented orchestration entry point |
| Generated contracts drift | Deterministic generation and CI diff checks |
| Goose accepts executor claim without evidence | Independent verification and Acceptance Report |
| Empty future scaffolding creates false ownership | Create only used packages/directories |

---

# 13. Definition of Ready

Sprint 1 Ready khi:

1. Sprint 0 PASS.
2. Toolchain ready.
3. Repository path and Git policy clear.
4. No unresolved P0 architecture conflict.
5. Local environment prerequisites known.
6. Quality and acceptance plan approved.
7. Goose has micro-task graph.

---

# 14. Definition of Done

Sprint 1 chỉ Done khi:

1. Clean checkout setup được chứng minh.
2. Backend, frontend và worker/scheduler shells chạy.
3. Local infrastructure healthy.
4. Migration bootstrap verified.
5. OpenAPI/Event contract tooling valid.
6. Formatting/lint/typecheck/tests/build pass.
7. CI green trên exact commit.
8. Architecture/security baseline checks pass.
9. Không có business code ngoài scope.
10. Documentation, Project Status và Handoff cập nhật.
11. Acceptance Report ghi command và kết quả thật.
12. Sprint 2 chưa được tự kích hoạt; chỉ có activation recommendation.

---

# 15. Acceptance Report

`docs/sprints/sprint-001/acceptance-report.md` MUST ghi:

- Commit range/hash.
- Created architecture and paths.
- Toolchain and lock evidence.
- Local setup commands/results.
- Service health evidence.
- Migration checks.
- Contract checks.
- Backend/frontend/worker quality results.
- CI result.
- Security/secret scan result.
- Deviations and approved exceptions.
- Known limitations.
- Final status and sign-off.

---

# 16. Chỉ thị cho Goose và Opencode

## Goose

- Chỉ kích hoạt sau Sprint 0 PASS.
- Chia một micro-task tại một thời điểm trừ khi independence được chứng minh.
- Không cho Opencode tự chọn stack hoặc đổi version.
- Inspect diff và rerun checks.
- Không chấp nhận “works on my machine” không có clean setup evidence.

## Opencode

- Chỉ sửa allowed files.
- Không tạo business feature.
- Không thêm dependency không được duyệt.
- Không sửa test để che lỗi.
- Báo cáo exact commands, outputs và phần chưa xác minh.

---

# 17. Kết luận

```text
Reproducible Repository
+ Locked Toolchain
+ Runnable Shells
+ Local Infrastructure
+ Contract and Migration Bootstrap
+ Automated Quality Gates
= FOUNDATION_READY_FOR_SPRINT_002
```
