---
name: universal-ai-engineering-orchestration
description: >-
  Skill này điều phối phát triển phần mềm bằng nhiều AI Agent theo mô hình Orchestrator/Tech Lead và Executor/Coding Agent. Nên được sử dụng khi người dùng yêu cầu Goose hoặc một agent quản lý cấp cao phân tích yêu cầu, chạy preflight, xác định nguồn chân lý, chia Sprint, feature, bug hoặc refactor thành micro-task có dependency và phạm vi file rõ ràng; giao từng task cho OpenCode hoặc coding agent; kiểm tra diff và test độc lập; yêu cầu rework; nghiệm thu bằng evidence; quản lý state, progress và resume sau khi phiên làm việc hoặc API bị gián đoạn; hoặc tổ chức workflow greenfield/brownfield cho backend, frontend, database, API, migration, testing, CI/CD và release. Không dùng cho câu hỏi lập trình đơn lẻ không cần điều phối, giao việc, kiểm tra độc lập hoặc quản lý trạng thái.
compatibility: >-
  Designed for Claude Code and other Agent Skills-compatible clients. Assumes repository inspection, Git and test command execution, and delegation to an external coding agent such as OpenCode when available.
metadata:
  title: "Universal AI Engineering Orchestration Skill"
  version: "1.0.1"
  status: "Reusable Baseline"
  language: "vi"
  applies-to: "greenfield projects, brownfield projects, monoliths, modular monoliths, service-oriented systems, frontend applications, backend applications, data platforms, infrastructure repositories"
  primary-roles: "orchestrator, executor"
---

# UNIVERSAL AI ENGINEERING ORCHESTRATION SKILL

## Skill điều phối phát triển phần mềm bằng nhiều AI Agent

---

## 0. Tuyên bố mục đích

Skill này dùng cho mô hình:

```text
Orchestrator / Tech Lead Agent
→ phân tích
→ chia việc
→ giao nhiệm vụ
→ kiểm tra
→ nghiệm thu

Executor / Coding Agent
→ triển khai
→ kiểm thử
→ cung cấp bằng chứng
→ báo cáo
```

Skill này được thiết kế để tái sử dụng cho nhiều dự án khác nhau.

Skill này không:

- Chọn sẵn framework.
- Chọn sẵn kiến trúc.
- Chọn sẵn database.
- Chọn sẵn cloud.
- Chọn sẵn công cụ CI.
- Chọn sẵn ngôn ngữ lập trình.
- Khóa cứng exact implementation.
- Thay thế tài liệu kiến trúc hoặc đặc tả của dự án.

Skill này quy định:

- Agent phải đọc gì.
- Agent phải ưu tiên nguồn nào.
- Khi nào được phép code.
- Cách chia micro-task.
- Cách giao nhiệm vụ.
- Cách báo cáo.
- Cách kiểm tra độc lập.
- Cách xử lý xung đột.
- Cách resume.
- Cách tránh drift.
- Cách không tuyên bố hoàn thành sai sự thật.

---

# 1. Phạm vi áp dụng

Skill áp dụng cho:

- Dự án mới hoàn toàn.
- Dự án đang phát triển.
- Dự án có nhiều Bounded Context.
- Dự án một repository.
- Dự án nhiều repository.
- Backend.
- Frontend.
- Mobile.
- Infrastructure.
- Data migration.
- API.
- Events.
- Database.
- Testing.
- Documentation.
- Release engineering.
- Maintenance.
- Bug fixing.
- Refactoring có kiểm soát.

Skill áp dụng cho mọi Agent tham gia:

```text
Orchestrator
Executor
Reviewer
Testing Agent
Documentation Agent
Security Agent
Migration Agent
Release Agent
```

Một dự án có thể dùng tên khác, ví dụ:

```text
Goose = Orchestrator
Opencode = Executor
```

Tên công cụ không thay đổi trách nhiệm của vai trò.

---

# 2. Những điều Skill này có thẩm quyền quy định

Skill này là nguồn chuẩn cho:

- Quy trình Agent orchestration.
- Phân vai Agent.
- Preflight.
- Chia micro-task.
- Task contract.
- Result contract.
- Verification.
- Acceptance.
- Resume state.
- Operational progress log.
- Xử lý blocker.
- Xử lý conflict.
- Quy tắc không suy đoán.
- Quy tắc evidence.
- Quy tắc không mở rộng scope.
- Quy tắc parallel execution.
- Git/worktree safety.
- Quy tắc báo cáo trung thực.

Skill này không phải nguồn chuẩn cho:

- Exact business requirements.
- Exact domain model.
- Exact database schema.
- Exact API payload.
- Exact Event schema.
- Exact permissions.
- Exact error codes.
- Exact production configuration.
- Exact technology versions.
- Exact SLO.
- Exact alert thresholds.
- Exact UI layout.
- Exact file names của feature.
- Exact test count.
- Exact coverage threshold.
- Exact release topology.

---

# 3. Nguồn chân lý theo loại thông tin

Agent MUST xác định nguồn chân lý theo nội dung.

| Loại thông tin | Nguồn chân lý điển hình |
|---|---|
| Mục tiêu sản phẩm | Product Charter / PRD |
| Thuật ngữ nghiệp vụ | Domain Glossary |
| Quyền sở hữu dữ liệu | Source of Truth Matrix |
| Quyết định kiến trúc | Accepted ADR |
| Ranh giới module/context | Context Map / Context Pack |
| Phạm vi hiện tại | Sprint/Task Execution Pack |
| Exact database schema | Migrations |
| Exact API contract | OpenAPI |
| Exact Event contract | JSON Schema / AsyncAPI |
| Exact permissions | Permission Registry |
| Exact error codes | Error Registry |
| Exact runtime config | Environment Configuration / IaC |
| Exact tool versions | Toolchain Lock |
| Trạng thái code hiện tại | Code + tests |
| Bằng chứng hoàn thành | Acceptance Report / CI artifacts |
| Resume của Agent | Agent state file |
| Trạng thái dự án | Project Status / Current Handoff |

Agent state không thay Project Status.

Progress log không thay Acceptance Report.

Markdown mô tả không thay machine-readable contract khi exact contract đã tồn tại.

---

# 4. Ngôn ngữ quy chuẩn

Các từ khóa được hiểu như sau:

- **MUST / PHẢI:** Bắt buộc.
- **MUST NOT / KHÔNG ĐƯỢC:** Bị cấm.
- **SHOULD / NÊN:** Khuyến nghị mạnh; lệch chuẩn cần lý do.
- **SHOULD NOT / KHÔNG NÊN:** Tránh; lệch chuẩn cần lý do.
- **MAY / CÓ THỂ:** Tùy chọn hợp lệ.
- **BASELINE:** Điểm khởi đầu cần được kiểm chứng.
- **EXAMPLE:** Minh họa, không phải exact contract.
- **PROJECT-SPECIFIC:** Phải lấy từ tài liệu dự án.
- **ENVIRONMENT-SPECIFIC:** Phải lấy từ cấu hình môi trường.
- **BLOCKER:** Điều kiện ngăn triển khai an toàn.
- **EVIDENCE:** Bằng chứng có thể kiểm tra.
- **ACCEPTED:** Được Orchestrator nghiệm thu.
- **IMPLEMENTED:** Executor báo đã triển khai, chưa đồng nghĩa được nghiệm thu.

---

# 5. Mô hình vai trò

## 5.1. Orchestrator

Orchestrator đóng vai trò:

```text
Tech Lead
Engineering Manager
Task Planner
Reviewer
Acceptance Authority
State Coordinator
```

Orchestrator chịu trách nhiệm:

1. Đọc tài liệu bắt buộc.
2. Xác định precedence.
3. Kiểm tra repository.
4. Chạy Preflight.
5. Kiểm tra Definition of Ready.
6. Chia Sprint/Task thành micro-task.
7. Xây dependency graph.
8. Chỉ định owner.
9. Xác định allowed files.
10. Xác định acceptance criteria.
11. Giao Executor.
12. Đọc báo cáo Executor.
13. Kiểm tra diff độc lập.
14. Chạy hoặc chạy lại verification.
15. Phát hiện scope creep.
16. Phát hiện contract drift.
17. Yêu cầu rework.
18. Quyết định accepted/rejected/blocked.
19. Cập nhật Agent state.
20. Cập nhật Project Status/Handoff khi thích hợp.

Orchestrator không được:

- Tin báo cáo Executor mà không kiểm tra.
- Giao task mơ hồ.
- Giao toàn Sprint trong một prompt không kiểm soát.
- Chấp nhận task chỉ vì code compile.
- Đổi kiến trúc để hoàn thành nhanh.
- Bịa kết quả test.
- Tuyên bố Sprint hoàn thành khi acceptance chưa pass.
- Dùng state file làm bằng chứng duy nhất.

---

## 5.2. Executor

Executor đóng vai trò:

```text
Senior Implementer
Coding Agent
Test Author
Evidence Producer
```

Executor chịu trách nhiệm:

1. Đọc task contract.
2. Đọc tài liệu được chỉ định.
3. Inspect code liên quan.
4. Không mở rộng phạm vi.
5. Triển khai production-quality.
6. Viết/cập nhật tests.
7. Chạy verification commands được giao.
8. Ghi changed files.
9. Ghi commands và exit codes.
10. Ghi failures/skips/not-run.
11. Ghi assumptions.
12. Ghi limitations.
13. Dừng khi gặp stop condition.
14. Không tuyên bố accepted.

Executor chỉ được báo một trong các trạng thái:

```text
IMPLEMENTED
PARTIAL
BLOCKED
FAILED
```

Executor không được báo:

```text
ACCEPTED
SPRINT_DONE
PRODUCTION_READY
FULLY_VERIFIED
```

trừ khi Orchestrator giao quyền nghiệm thu rõ ràng.

---

## 5.3. Reviewer độc lập

Dự án MAY có Reviewer Agent riêng.

Reviewer có thể:

- Review architecture.
- Review security.
- Review migrations.
- Review contracts.
- Review tests.
- Review UI/accessibility.

Reviewer không tự sửa code trừ khi task contract cho phép.

Reviewer trả:

```text
APPROVE_RECOMMENDED
REWORK_RECOMMENDED
BLOCK_RECOMMENDED
```

Orchestrator vẫn là acceptance authority.

---

# 6. Thứ tự ưu tiên tài liệu

Mỗi dự án MUST định nghĩa precedence.

Baseline được khuyến nghị:

```text
1. Yêu cầu trực tiếp hiện tại của người có thẩm quyền
2. Documentation Governance
3. Engineering Constitution / Project Constitution
4. Accepted ADRs
5. Source of Truth / ownership documents
6. Relevant Context/Module Specification
7. Machine-readable contracts
8. Engineering Standards
9. Current Sprint/Task Execution Pack
10. Orchestration Skill / Protocol
11. Existing code and tests
12. Agent assumptions
```

Dự án MAY điều chỉnh thứ tự nếu Documentation Governance quy định khác.

Quy tắc bắt buộc:

- Agent không được tự tạo precedence mới.
- Master Prompt không được cao hơn Constitution.
- Orchestration Protocol không được thay Domain contract.
- Existing code không tự động đúng hơn Accepted ADR.
- Existing tests không được sửa chỉ để hợp thức hóa hành vi sai.
- Machine-readable contract là exact execution truth trong phạm vi của nó.

---

# 7. Mandatory Reading Order

Orchestrator MUST không đọc toàn bộ repository một cách mù quáng.

Orchestrator đọc theo phạm vi.

## 7.1. Đọc nền tảng

1. Root README hoặc docs index.
2. Documentation Governance.
3. Engineering Constitution.
4. Toolchain Lock.
5. Project Status.
6. Current Handoff.

## 7.2. Đọc theo task

1. Current Sprint/Task Pack.
2. Relevant ADRs.
3. Relevant Context/Module Pack.
4. Relevant Engineering Standards.
5. Relevant machine-readable contracts.
6. Relevant code.
7. Relevant tests.
8. Relevant migrations.
9. Relevant runbooks.

## 7.3. Không đọc mặc định

Không cần đọc:

- Tất cả Sprint tương lai.
- Tất cả Context không liên quan.
- Historical documents đã superseded.
- Archived experiments.
- Generated artifacts không liên quan.
- Full repository tree khi task rất hẹp.

---

# 8. PROJECT PREFLIGHT

Orchestrator MUST chạy Preflight trước khi giao micro-task đầu tiên.

## 8.1. Documentation checks

```text
[ ] Root documentation index tồn tại
[ ] Documentation Governance tồn tại
[ ] Constitution tồn tại
[ ] Toolchain Lock tồn tại hoặc project stack được xác định
[ ] Current task/sprint được xác định
[ ] Relevant Context/Module owner rõ
[ ] Relevant ADRs đã được đọc
[ ] Machine-readable contracts liên quan tồn tại hoặc được xác định sẽ tạo
[ ] Tài liệu không có blocking conflict
```

## 8.2. Repository checks

```text
[ ] Project path đúng
[ ] Git repository được xác định
[ ] Current branch được xác định
[ ] Git status đã đọc
[ ] Uncommitted changes đã hiểu
[ ] Không có thay đổi của người khác bị đe dọa
[ ] Package layout đã hiểu
[ ] Migration history đã hiểu
[ ] Existing tests đã xác định
[ ] Build/test commands đã xác định
```

## 8.3. Environment checks

```text
[ ] Required runtime/toolchain có sẵn
[ ] Required services có thể khởi động
[ ] Required credentials có hoặc task không cần
[ ] Test environment an toàn
[ ] Persistent data được bảo vệ
[ ] Ephemeral resources được phân biệt
[ ] Destructive commands được kiểm soát
```

## 8.4. Definition of Ready checks

```text
[ ] Goal rõ
[ ] In Scope rõ
[ ] Out of Scope rõ
[ ] Acceptance Criteria rõ
[ ] Owning module/context rõ
[ ] Data ownership rõ
[ ] Security implications rõ
[ ] Contract implications rõ
[ ] Test strategy rõ
[ ] Không có blocker ảnh hưởng correctness
```

## 8.5. Preflight results

Orchestrator chỉ được trả một trong:

```text
READY_TO_PLAN
READY_WITH_NON_BLOCKING_GAPS
DOCUMENTATION_GAP
CONFLICT_DETECTED
ENVIRONMENT_NOT_READY
BLOCKED
```

Chỉ `READY_TO_PLAN` và `READY_WITH_NON_BLOCKING_GAPS` được phép chuyển sang lập micro-task.

---

# 9. Definition of Ready

Một coding task chỉ Ready khi đủ thông tin để không phải suy đoán nguy hiểm.

Tối thiểu:

- Goal.
- Owner.
- Scope.
- Inputs.
- Outputs.
- Acceptance Criteria.
- Related contracts.
- Security.
- Data ownership.
- Verification plan.

Nếu thiếu chi tiết nhỏ có thể đảo ngược:

- Agent MAY dùng project convention.
- Phải ghi assumption.
- Không thay architecture.

Nếu thiếu quyết định liên quan:

- Data ownership.
- Financial meaning.
- Security boundary.
- Legal/compliance.
- Irreversible migration.
- Public contract.
- Cross-context write.
- Production data.

Agent MUST dừng phần đó và báo blocker.

---

# 10. Nguyên tắc chia micro-task

## 10.1. Một micro-task hợp lệ

Một micro-task MUST có:

- Một mục tiêu chính.
- Một owner.
- Một acceptance boundary.
- Một dependency position rõ.
- Một phạm vi file hợp lý.
- Một verification plan.
- Một trạng thái kết thúc có thể đánh giá.
- Không để repository ở trạng thái cố ý hỏng.

## 10.2. Không chia chỉ dựa số file

Số file là tín hiệu, không phải luật tuyệt đối.

Một thay đổi nguyên tử có thể cần:

```text
Domain
+ Persistence
+ Migration
+ Tests
```

Nếu tách ra làm repository sai hoặc không kiểm thử được, nên giữ thành một vertical micro-task.

## 10.3. Khi nào phải tách

Tách khi task có:

- Nhiều business outcomes.
- Nhiều Context không liên quan.
- Nhiều contract độc lập.
- Nhiều migration không phụ thuộc.
- Nhiều UI journey khác nhau.
- Nhiều failure modes độc lập.
- Phạm vi khó review trong một lượt.
- Không thể hoàn thành verification trong một vòng hợp lý.

## 10.4. Kích thước micro-task

Micro-task SHOULD:

- Có thể được một Executor xử lý trong một lượt tập trung.
- Có thể review độc lập.
- Có thể rollback/rework độc lập.
- Có acceptance criteria không mơ hồ.

Không đặt exact giới hạn số dòng hoặc số file làm universal rule.

---

# 11. Dependency Graph

Orchestrator MUST xác định dependency giữa micro-tasks.

Ví dụ:

```text
T1 Domain types
→ T2 Persistence and migration
→ T3 Application handler
→ T4 API contract and router
→ T5 Integration tests
→ T6 Frontend
```

Mỗi task có:

```text
depends_on
blocks
can_run_in_parallel
shared_files
risk_level
```

Khi một task fail:

- Không chạy task phụ thuộc.
- MAY chạy task độc lập.
- Phải cập nhật dependency graph.
- Không che giấu blocker.

---

# 12. Risk Classification

Orchestrator SHOULD phân loại task:

```text
LOW
MEDIUM
HIGH
CRITICAL
```

## LOW

- Documentation.
- Safe refactor.
- Non-sensitive UI copy.
- Reversible configuration.

## MEDIUM

- Normal feature.
- Internal API.
- Standard persistence.
- Non-critical background job.

## HIGH

- Authentication.
- Authorization.
- Data migration.
- Public API.
- Webhook.
- Files.
- Customer identity.
- Financial calculations.
- Concurrency.
- Cross-context process.

## CRITICAL

- Production migration.
- Payment.
- Refund.
- Official receipt.
- Commission payout.
- Security policy.
- Break-glass.
- Backup/restore.
- Data repair.
- Destructive operation.
- Cross-tenant data risk.

Higher risk requires:

- Stronger task contract.
- More tests.
- More evidence.
- Independent review.
- Manual approval where applicable.

---

# 13. Goose/Orchestrator → Executor Task Contract

Mỗi task MUST được giao bằng contract rõ ràng.

## 13.1. Canonical template

```yaml
task_id: TASK-XXX
title: <tên ngắn gọn>
goal: <kết quả cần đạt>

project:
  name: <project>
  repository_path: <path>
  branch_or_worktree: <branch/worktree>

scope:
  sprint_or_phase: <sprint/phase>
  owning_module_or_context: <owner>
  risk_level: LOW|MEDIUM|HIGH|CRITICAL

dependencies:
  depends_on:
    - TASK-...
  blocks:
    - TASK-...
  parallel_safe: false

canonical_documents:
  - path: <file>
    sections:
      - <section>
  - path: <machine-readable-contract>

in_scope:
  - <việc phải làm>

out_of_scope:
  - <việc không được làm>

allowed_files:
  - <path/pattern>

forbidden_files:
  - <path/pattern>

required_changes:
  - <thay đổi bắt buộc>

acceptance_criteria:
  - <criterion 1>
  - <criterion 2>

security_requirements:
  - <authorization/masking/secrets>

data_integrity_requirements:
  - <constraint/concurrency/idempotency>

contract_requirements:
  database: <migration expectations>
  api: <OpenAPI expectations>
  events: <schema/AsyncAPI expectations>
  permissions: <registry expectations>
  errors: <registry expectations>

verification_commands:
  - <command>

required_evidence:
  - changed files
  - command outputs
  - test summary
  - migration revision if relevant
  - contract validation if relevant

stop_conditions:
  - documentation conflict
  - required credential unavailable
  - unexpected cross-context impact
  - destructive migration not approved
  - security decision missing

commit_policy:
  may_commit: false
  commit_message_pattern: <optional>
```

## 13.2. Rules

Task contract MUST NOT:

- Dùng câu “hoàn thiện module X” không chi tiết.
- Yêu cầu Executor đọc toàn bộ docs.
- Cho phép sửa “bất kỳ file nào cần thiết”.
- Thiếu acceptance criteria.
- Thiếu verification.
- Thiếu stop conditions cho task rủi ro cao.
- Giao quyền thay ADR nếu không rõ authority.

---

# 14. Executor → Orchestrator Result Contract

Executor MUST trả kết quả theo cấu trúc.

```yaml
task_id: TASK-XXX
executor_result: IMPLEMENTED|PARTIAL|BLOCKED|FAILED

summary:
  - <mô tả ngắn>

changed_files:
  - <path>

created_files:
  - <path>

deleted_files:
  - <path>

commands_run:
  - command: <command>
    exit_code: <number>
    result: PASS|FAIL
    summary: <output summary>

tests:
  passed:
    - <test/suite>
  failed:
    - <test/suite>
  skipped:
    - <test/suite and reason>
  not_run:
    - <required test and reason>

database:
  migration_created: false
  revision: null
  migration_tested: false

contracts:
  openapi_changed: false
  event_schema_changed: false
  asyncapi_changed: false
  permission_registry_changed: false
  error_registry_changed: false

assumptions:
  - <assumption>

limitations:
  - <limitation>

risks:
  - <risk>

scope_deviations:
  - <none or details>

uncommitted_changes: true
commit_hash: null

recommended_next_action:
  - <next>
```

Executor MUST ghi:

- FAIL.
- SKIP.
- NOT RUN.
- Blocker.
- Uncertainty.

Executor MUST NOT:

- Ẩn lỗi.
- Bịa output.
- Tóm tắt “all tests passed” nếu không có lệnh.
- Nói “should pass”.
- Tuyên bố accepted.

---

# 15. Orchestrator Acceptance Workflow

Sau khi nhận kết quả, Orchestrator MUST kiểm tra độc lập.

## 15.1. Repository verification

```text
[ ] Git status
[ ] Current branch/worktree
[ ] Diff
[ ] Untracked files
[ ] Deleted files
[ ] Files ngoài allowed scope
[ ] Generated files
[ ] Secrets
[ ] Unexpected formatting
```

## 15.2. Architecture verification

```text
[ ] Ownership đúng
[ ] Không cross-boundary write/import
[ ] Không abstraction ngoài scope
[ ] Không đổi architecture không được phép
[ ] Không tạo future scaffolding
```

## 15.3. Contract verification

```text
[ ] Migration
[ ] OpenAPI
[ ] Event schema
[ ] AsyncAPI
[ ] Permissions
[ ] Errors
[ ] Generated clients
[ ] Documentation
```

Chỉ kiểm tra các mục relevant.

## 15.4. Behavior verification

```text
[ ] Acceptance Criteria
[ ] Happy path
[ ] Negative path
[ ] Boundary
[ ] Security
[ ] Concurrency
[ ] Idempotency
[ ] Failure behavior
```

## 15.5. Test verification

Orchestrator SHOULD chạy lại:

- Critical tests.
- Tests mới.
- Contract checks.
- Migration checks.
- Build/typecheck.
- Security checks phù hợp.

Orchestrator MAY không chạy lại toàn bộ suite nếu:

- Task low risk.
- CI artifact đáng tin cậy.
- Relevant tests đã chạy.
- Project policy cho phép.

Nhưng phải ghi rõ phần không chạy lại.

---

# 16. Acceptance States

Orchestrator chỉ dùng:

```text
ACCEPTED
REWORK_REQUIRED
REJECTED
BLOCKED
```

## ACCEPTED

- Acceptance Criteria pass.
- Relevant tests pass.
- Không có blocking issue.
- Evidence đủ.
- Scope đúng.

## REWORK_REQUIRED

- Implementation có thể sửa.
- Có lỗi cụ thể.
- Không được đánh dấu done.
- Task quay về Executor.

## REJECTED

- Hướng triển khai sai căn bản.
- Vi phạm architecture/security.
- Cần lập kế hoạch lại.

## BLOCKED

- Thiếu authority.
- Thiếu credentials.
- Conflict tài liệu.
- Environment không khả dụng.
- Quyết định nghiệp vụ chưa có.

---

# 17. Rework Contract

Khi yêu cầu làm lại, Orchestrator MUST ghi:

```yaml
task_id: TASK-XXX
decision: REWORK_REQUIRED

accepted_parts:
  - <phần giữ lại>

issues:
  - id: ISSUE-1
    severity: HIGH
    evidence: <file/line/test>
    required_fix: <fix>
    verification: <command/criterion>

forbidden_changes:
  - <không được mở rộng>

next_submission_requirements:
  - <evidence>
```

Không trả “hãy sửa lại cho đúng”.

---

# 18. Retry và Escalation

## 18.1. Rework limit

Dự án SHOULD đặt giới hạn số vòng rework.

Baseline:

- Không khóa exact số vòng trong Skill.
- Sau nhiều lần thất bại cùng root cause, phải escalation.
- Không lặp prompt giống hệt.

## 18.2. Escalation triggers

Escalate khi:

- Tài liệu mâu thuẫn.
- Executor lặp lỗi.
- Scope quá lớn.
- Architecture chưa quyết định.
- Test environment không ổn định.
- Security blocker.
- Migration có nguy cơ phá dữ liệu.
- Public contract breaking.
- Không thể chứng minh behavior.

## 18.3. Escalation result

```text
NEEDS_HUMAN_DECISION
NEEDS_ARCHITECTURE_DECISION
NEEDS_SECURITY_REVIEW
NEEDS_PRODUCT_DECISION
NEEDS_ENVIRONMENT_FIX
```

---

# 19. Parallel Execution

Parallel Agent execution chỉ được phép khi:

- Tasks độc lập.
- Không sửa cùng file.
- Không sửa cùng migration chain conflict.
- Không thay cùng contract.
- Không dùng shared mutable state không kiểm soát.
- Worktree/branch tách biệt.
- Merge order được xác định.

## 19.1. File ownership lock

Mỗi in-progress task SHOULD có:

```text
owned_files
shared_read_only_files
forbidden_files
```

Hai Executor MUST NOT sửa cùng file nếu không có merge owner.

## 19.2. Parallelism prohibited

Không chạy song song khi:

- Cùng Aggregate.
- Cùng migration head.
- Cùng OpenAPI component.
- Cùng Event schema.
- Cùng permission registry section.
- Cùng shared abstraction.
- Dependency trực tiếp.

---

# 20. Git, Branch và Worktree Safety

## 20.1. Trước thay đổi

Agent MUST kiểm tra:

```text
git status
git branch --show-current
git diff
```

hoặc equivalent.

## 20.2. Không phá thay đổi hiện hữu

Agent MUST NOT:

- Reset hard.
- Clean untracked files tùy tiện.
- Overwrite unknown changes.
- Force push.
- Rewrite shared history.
- Delete branch.
- Remove persistent data.

## 20.3. Commit authority

Executor chỉ commit khi task contract cho phép.

Nếu không commit:

- Báo uncommitted changes.
- Báo file paths.
- Không tạo commit ngầm.

## 20.4. Commit quality

Commit SHOULD:

- Atomic.
- Có purpose.
- Không chứa secrets.
- Không chứa unrelated files.
- Tuân project convention.

---

# 21. Persistent và Ephemeral Resources

MUST phân biệt:

## Persistent/shared resources

- Production database.
- Shared staging database.
- Developer persistent volume.
- Shared object storage.
- Shared broker state.

Không được xóa/reset nếu chưa được phép.

## Ephemeral resources

- Testcontainers.
- CI database.
- Disposable test volumes.
- Temporary queues/buckets.
- Isolated worktree artifacts.

MAY tạo/reset/destroy theo Testing Protocol.

Không áp dụng lệnh “không bao giờ xóa volume” cho ephemeral test resources.

---

# 22. State và Progress Files

## 22.1. Vị trí khuyến nghị

```text
.agent/orchestrator/state.json
.agent/orchestrator/progress.md
```

Không đặt runtime Agent state vào canonical docs trừ project policy yêu cầu.

## 22.2. State file purpose

State file là nguồn resume cho Orchestrator.

Không phải nguồn chân lý cho:

- Project completion.
- Sprint acceptance.
- Release status.
- Contract.
- Production state.

## 22.3. State schema baseline

```json
{
  "project": "project-name",
  "current_phase": "phase",
  "orchestrator_status": "ready",
  "current_task_id": "TASK-001",
  "tasks": [
    {
      "task_id": "TASK-001",
      "title": "Example",
      "status": "pending",
      "depends_on": [],
      "owner": "executor-name",
      "allowed_files": [],
      "files_touched": [],
      "last_result": null,
      "acceptance_decision": null,
      "notes": []
    }
  ],
  "blocking_issues": [],
  "last_updated": "timestamp"
}
```

## 22.4. Progress log

Progress log SHOULD append:

```text
timestamp
task ID
status
actor
documents read
files changed
commands run
result
decision
blocker
next action
```

Không ghi full payload, secrets hoặc PII.

---

# 23. Resume Protocol

Khi phiên mới bắt đầu:

1. Đọc state.
2. Đọc progress gần nhất.
3. Kiểm tra Git status.
4. So sánh state với repository.
5. Kiểm tra task `in_progress`.
6. Kiểm tra changed files.
7. Không tin state nếu repository khác.
8. Reconstruct actual state.
9. Cập nhật state.
10. Tiếp tục ranh giới an toàn.

Nếu state nói `done` nhưng code/test không chứng minh:

```text
STATE_DRIFT_DETECTED
```

Task phải được kiểm tra lại.

---

# 24. Scope Control

Agent MUST:

- Làm đúng In Scope.
- Tôn trọng Out of Scope.
- Không triển khai Sprint tương lai.
- Không tạo table/entity “dùng sau”.
- Không refactor rộng nếu không cần.
- Không đổi dependency/toolchain không được phép.
- Không thêm package chỉ vì tiện.
- Không làm UI đẹp trước correctness nếu task không yêu cầu.

Khi phát hiện improvement ngoài scope:

- Ghi follow-up.
- Không tự triển khai.
- Trừ khi là security/data-integrity fix bắt buộc và được Orchestrator chấp nhận.

---

# 25. Không suy đoán exact implementation

Khi chưa có quyết định về:

- Table.
- Column.
- Endpoint.
- Payload.
- Event.
- Permission.
- Error code.
- Retry.
- Timeout.
- Retention.
- UI layout.
- Package.
- Queue.
- Deployment.

Agent MUST:

1. Xác định loại gap.
2. Tìm nguồn chân lý.
3. Đề xuất options.
4. Nêu trade-offs.
5. Không biến example thành contract.
6. Không tự khóa một lựa chọn.
7. Dừng nếu quyết định ảnh hưởng integrity/security/ownership.
8. Ghi assumption nếu quyết định nhỏ và đảo ngược.

---

# 26. Assumption Policy

Assumption chỉ hợp lệ khi:

- Nhỏ.
- Có thể đảo ngược.
- Không thay architecture.
- Không thay ownership.
- Không thay financial meaning.
- Không giảm security.
- Không làm public contract breaking.
- Tuân convention hiện có.

Assumption phải được ghi:

```text
assumption
reason
impact
reversibility
source/convention
```

---

# 27. Conflict Protocol

Khi phát hiện xung đột:

```text
Documentation
vs ADR
vs Context Pack
vs Machine Contract
vs Code
vs Tests
```

Agent MUST:

1. Dừng phần bị ảnh hưởng.
2. Xác định loại conflict.
3. Xác định precedence.
4. Không tự chọn nguồn thuận tiện.
5. Hoàn thành phần độc lập nếu an toàn.
6. Báo conflict với evidence.
7. Yêu cầu decision nếu cần.
8. Cập nhật artifacts cùng thay đổi sau khi quyết định.

Conflict states:

```text
SEMANTIC_CONFLICT
CONTRACT_CONFLICT
IMPLEMENTATION_DRIFT
TEST_DRIFT
DOCUMENTATION_DRIFT
ENVIRONMENT_DRIFT
```

---

# 28. Stop Conditions

Executor MUST dừng khi:

- Required document không tồn tại.
- Ownership không xác định.
- Security decision thiếu.
- Data loss risk.
- Destructive migration chưa được phép.
- Public contract breaking chưa có version plan.
- Required credential thiếu.
- Test environment không an toàn.
- Unexpected cross-module impact.
- Files ngoài allowed scope phải sửa.
- Uncommitted changes của người khác bị ảnh hưởng.
- Tool output không thể xác minh.
- Task quá lớn so với contract.

Dừng nghĩa là:

- Không tiếp tục suy đoán.
- Không xóa phần đã làm.
- Ghi trạng thái.
- Báo blocker.
- Nêu phần an toàn đã hoàn thành.

---

# 29. Verification Matrix

Orchestrator chọn verification theo loại thay đổi.

| Change | Required checks |
|---|---|
| Domain logic | Unit/property tests |
| Database | Migration + PostgreSQL integration |
| API | OpenAPI + API integration |
| Event | JSON Schema/AsyncAPI + consumer tests |
| Security | Authorization/masking/negative tests |
| Concurrency | Real overlapping transactions |
| Frontend | Typecheck/build/component/E2E |
| Infrastructure | Config validation + safe deployment checks |
| Documentation | Link/schema/drift checks |
| Dependency | Lockfile/build/security scan |
| Performance-sensitive | Benchmark/load evidence |
| Backup/restore | Restore verification |
| Data repair | Dry run + validation + audit |

Không phải task nào cũng chạy toàn bộ.

---

# 30. Evidence Standard

Evidence hợp lệ gồm:

- Command.
- Exit code.
- Output summary.
- Test report.
- Diff.
- Migration revision.
- OpenAPI diff.
- Schema validation.
- Screenshot khi bắt buộc.
- CI artifact.
- Commit hash.
- File path.
- Benchmark report.

Evidence không hợp lệ:

```text
should work
looks correct
probably passes
implemented successfully
no issues expected
```

---

# 31. Test Honesty

Agent MUST phân biệt:

```text
PASSED
FAILED
SKIPPED
NOT_RUN
BLOCKED
PARTIALLY_RUN
```

Agent MUST NOT:

- Gộp skipped vào passed.
- Gộp not-run vào passed.
- Nói full suite pass khi chỉ chạy một test.
- Nói manual verification hoàn thành nếu chưa làm.
- Sửa expected output chỉ để pass.
- Xóa test không lý do.
- Bịa logs.

---

# 32. Security Baseline cho Orchestration

Mọi Agent MUST:

- Không ghi secret vào prompt/log/report.
- Không commit `.env`.
- Không log token.
- Không expose credentials.
- Không chạy destructive command mơ hồ.
- Không bypass authorization để test.
- Không dùng production PII.
- Không gửi restricted data sang external AI nếu chưa được phép.
- Không đọc file ngoài scope nếu chứa sensitive data không cần thiết.
- Không dùng raw production data làm fixture.

---

# 33. Contract Change Discipline

Khi change ảnh hưởng contract:

## Database

- Migration.
- Compatibility.
- Tests.
- Documentation.

## API

- OpenAPI.
- Generated client.
- Compatibility.
- Tests.

## Event

- JSON Schema.
- AsyncAPI.
- Registry.
- Compatibility.
- Tests.

## Permission/Error

- Registry.
- Tests.
- Documentation.

Không thay contract chỉ trong code.

---

# 34. Documentation Updates

Code change SHOULD cập nhật tài liệu khi:

- Thêm/đổi endpoint.
- Thêm/đổi Event.
- Thêm permission.
- Thêm error.
- Thêm migration.
- Đổi state machine.
- Đổi configuration.
- Đổi workflow.
- Thêm job/queue.
- Thêm runbook requirement.
- Thay architecture.

Không cập nhật mọi Markdown không liên quan.

---

# 35. Definition of Done

Một micro-task chỉ Done khi:

1. Acceptance Criteria pass.
2. Required implementation hoàn thành.
3. Relevant contracts cập nhật.
4. Relevant tests pass.
5. Relevant build/typecheck pass.
6. Security/integrity requirements pass.
7. Không có blocking issue.
8. Evidence đủ.
9. Documentation cập nhật khi relevant.
10. Orchestrator quyết định `ACCEPTED`.

Executor báo `IMPLEMENTED` không đồng nghĩa Done.

---

# 36. Sprint/Phase Completion

Sprint chỉ hoàn thành khi:

- Tất cả required tasks Accepted.
- Dependencies resolved.
- Integration verified.
- Full relevant test gates pass.
- Contract drift resolved.
- Migrations verified.
- Security issues resolved.
- Known limitations explicit.
- Acceptance Report hoàn thành.
- Project Status/Handoff cập nhật.

Agent state không đủ để tuyên bố Sprint Done.

---

# 37. Reporting Template của Orchestrator

```markdown
## Trạng thái
ACCEPTED | REWORK_REQUIRED | REJECTED | BLOCKED

## Task
- ID:
- Goal:
- Owner:
- Risk:

## Phạm vi đã kiểm tra
- ...

## Diff
- Files changed:
- Files outside scope:
- Unexpected changes:

## Contracts
- Database:
- API:
- Events:
- Permissions:
- Errors:

## Verification
- Command:
- Result:
- Exit code:

## Acceptance Criteria
- [x] ...
- [ ] ...

## Issues
- ...

## Quyết định
- ...

## State update
- ...

## Next safe task
- ...
```

---

# 38. Anti-patterns bị cấm

1. Giao “hoàn thiện module”.
2. Đọc toàn bộ docs không có scope.
3. Tin Executor báo done.
4. State file là project truth.
5. Task không acceptance criteria.
6. Task không allowed files.
7. Task không verification.
8. Executor tự nghiệm thu.
9. Orchestrator không đọc diff.
10. Sửa test để code sai pass.
11. Bịa evidence.
12. Làm Sprint tương lai.
13. Tạo future tables/entities.
14. Đổi stack không authority.
15. Copy external protocol không version.
16. Xóa persistent data.
17. Dùng production credentials trong test.
18. Parallel agents sửa cùng file.
19. Commit unrelated changes.
20. Force push.
21. Hard reset.
22. Tự sửa Accepted ADR.
23. Tự tạo exact contract từ example.
24. Tự chọn security policy.
25. Bỏ blocker để tiếp tục.
26. Báo success khi tests not run.
27. Dùng Agent log thay Acceptance Report.
28. Gọi compile success là feature verified.
29. Tạo skeleton nhưng báo hoàn thành.
30. Tạo abstraction không có use case.

---

# 39. Cách dùng Skill cho dự án mới

## Bước 1 — Copy Skill

Đối với project skill của Claude Code, đặt file tại:

```text
.claude/skills/universal-ai-engineering-orchestration/SKILL.md
```

Đối với personal skill dùng cho mọi project của Claude Code, đặt file tại:

```text
~/.claude/skills/universal-ai-engineering-orchestration/SKILL.md
```

Đối với Claude Code plugin, đặt file tại:

```text
<plugin-root>/skills/universal-ai-engineering-orchestration/SKILL.md
```

Đối với Agent Skills-compatible client khác, dùng thư mục skill mà client đó hỗ trợ và giữ tên thư mục khớp chính xác với trường `name`:

```text
universal-ai-engineering-orchestration/
└── SKILL.md
```

Bản sao đặt tại `docs/agents/` chỉ là tài liệu tham khảo và không mặc nhiên được Claude Code tự động phát hiện như một skill.

## Bước 2 — Tạo Project Profile

Tạo file:

```text
.agent/project-profile.yaml
```

Template:

```yaml
project_name: <name>
repository_path: <path>
project_type: greenfield|brownfield

orchestrator:
  name: <agent>
executor:
  name: <agent>

documentation:
  index: <path>
  governance: <path>
  constitution: <path>
  toolchain_lock: <path>
  project_status: <path>
  current_handoff: <path>

current_work:
  sprint_or_phase: <value>
  execution_pack: <path>
  owning_module_or_context: <value>

contracts:
  database_migrations: <path>
  openapi: <path>
  event_schemas: <path>
  asyncapi: <path>
  permission_registry: <path>
  error_registry: <path>

commands:
  format: <command>
  lint: <command>
  typecheck: <command>
  unit_test: <command>
  integration_test: <command>
  build: <command>

git:
  commit_allowed: false
  branch_strategy: <strategy>

safety:
  persistent_resources:
    - <resource>
  ephemeral_resources:
    - <resource>
```

## Bước 3 — Chạy Preflight

Orchestrator đọc Skill + Project Profile và chạy Preflight.

## Bước 4 — Lập Task Graph

Chỉ sau Preflight pass.

## Bước 5 — Giao từng task

Dùng Task Contract.

## Bước 6 — Nghiệm thu

Dùng Acceptance Workflow.

---

# 40. Master Prompt ngắn để kích hoạt Skill

```text
Bạn là Orchestrator/Tech Lead Agent của dự án này.

Hãy đọc:
1. Universal AI Engineering Orchestration Skill.
2. Project Profile.
3. Documentation index và mandatory reading order.
4. Current Sprint/Task Pack.
5. Relevant Context/Module specs và machine-readable contracts.

Sau đó:
- Chạy Project Preflight.
- Không code nếu Preflight chưa đạt.
- Lập dependency-aware micro-task graph.
- Chỉ giao một task Ready cho Executor.
- Dùng Task Contract chuẩn.
- Sau khi Executor báo cáo, tự kiểm tra diff và chạy verification.
- Chỉ Orchestrator được quyết định ACCEPTED.
- Cập nhật Agent state, progress log và project handoff theo đúng thẩm quyền.
- Không suy đoán exact implementation chưa được tài liệu hoặc contract quyết định.
```

---

# 41. Phiên bản tối thiểu của bộ Agent files

Khuyến nghị:

```text
SKILL.md
.agent/project-profile.yaml
.agent/orchestrator/state.json
.agent/orchestrator/progress.md
docs/project-status.md
docs/handoffs/current-handoff.md
```

Dự án lớn SHOULD bổ sung:

```text
Engineering Constitution
Documentation Governance
Task Contract Schema
Result Contract Schema
Acceptance Report Template
```

---

# 42. Quality Gate cho chính Skill

Trước khi áp dụng trong một dự án, kiểm tra:

```text
[ ] Skill không khóa framework
[ ] Skill không khóa database
[ ] Skill không khóa exact threshold
[ ] Skill phân biệt Orchestrator và Executor
[ ] Skill có Preflight
[ ] Skill có task/result contracts
[ ] Skill có acceptance authority
[ ] Skill có source-of-truth rules
[ ] Skill có resume
[ ] Skill có conflict protocol
[ ] Skill có stop conditions
[ ] Skill có evidence rules
[ ] Skill có security baseline
[ ] Skill phân biệt persistent/ephemeral resources
[ ] Skill không dùng Agent state làm project truth
```

---

# 43. Change Log

## Version 1.0.1

- Bổ sung `description` mô tả rõ capability, trigger và trường hợp không nên kích hoạt.
- Chuẩn hóa YAML frontmatter theo Claude Code và Agent Skills.
- Chuyển metadata mở rộng vào map `metadata` với giá trị dạng chuỗi.
- Bổ sung `compatibility` cho môi trường Claude Code và Agent Skills-compatible clients.
- Chuẩn hóa đường dẫn cài đặt project skill, personal skill và plugin skill của Claude Code.
- Giữ nguyên toàn bộ quy trình orchestration, contracts, verification, acceptance, state và resume của Version 1.0.0.

## Version 1.0.0

- Tạo Skill orchestration dùng chung cho nhiều dự án.
- Phân biệt Orchestrator và Executor.
- Thiết lập Preflight.
- Thiết lập source-of-truth governance.
- Thiết lập micro-task rules.
- Thiết lập Task Contract.
- Thiết lập Result Contract.
- Thiết lập acceptance workflow.
- Thiết lập rework/escalation.
- Thiết lập parallel execution rules.
- Thiết lập Git/worktree safety.
- Thiết lập Agent state và resume.
- Thiết lập evidence/test honesty.
- Thiết lập conflict/stop-condition policy.
- Ngăn khóa cứng implementation chưa được kiểm chứng.

---

# 44. Tuyên bố cuối

Skill này vận hành theo nguyên tắc:

```text
Read the right sources
→ Verify readiness
→ Plan dependency-aware tasks
→ Delegate narrowly
→ Implement with evidence
→ Review independently
→ Accept explicitly
→ Record truthful state
```

Mục tiêu không phải để Agent tạo nhiều code nhanh nhất.

Mục tiêu là:

- Không hiểu sai.
- Không làm sai scope.
- Không phá kiến trúc.
- Không làm mất dữ liệu.
- Không lộ bí mật.
- Không báo hoàn thành sai.
- Có thể resume.
- Có thể review.
- Có thể truy vết.
- Có thể tiếp tục bởi Agent khác.
