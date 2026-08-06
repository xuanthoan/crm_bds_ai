# CRM_BDS_AI — SPRINT 0 PREPARATION PACK

## Documentation, Architecture and AI-Agent Readiness Gate

**Document ID:** `SPRINT-000-PREPARATION-PACK`  
**Canonical path:** `docs/sprints/sprint-000/sprint-000-preparation-pack.md`  
**Product:** `crm_bds_ai`  
**Version:** `1.0.0`  
**Status:** `Ready for Readiness Review / Current Preparation Gate`  
**Project implementation state:** `NOT STARTED`  
**Sprint type:** `Documentation and Architecture Readiness Gate`  
**Primary owner:** `Architecture Owner`  
**Co-owners:** `Product Owner`, `Engineering Owner`  
**Reviewers:** `Domain Owners`, `Security Owner`, `Database Owner`, `API Owner`, `Event Architecture Owner`, `Frontend Owner`, `QA Owner`, `Operations Owner`  
**Effective date:** `2026-08-05`  
**Supersedes:** `None — Greenfield baseline`  
**Next state on PASS:** `Sprint 1 may be activated`  
**Classification:** `INTERNAL`

---

# 1. Mục đích

Sprint 0 là cổng kiểm tra cuối cùng trước khi Goose hoặc Opencode tạo source code cho `crm_bds_ai`.

Sprint này không phải Sprint xây tính năng. Sprint này bảo đảm rằng:

- Bộ tài liệu canonical đủ rõ để điều khiển dự án Greenfield.
- Mỗi loại thông tin có đúng một nguồn chân lý.
- Tài liệu cũ hoặc superseded không cạnh tranh với tài liệu mới.
- Goose hiểu đúng vai trò Tech Lead/Orchestrator.
- Opencode chỉ nhận micro-task đã qua preflight.
- Toolchain đủ rõ để Sprint 1 không tự chọn lại stack.
- Chỉ một Sprint được đánh dấu active.
- Các quyết định chưa có bằng chứng không bị biến thành implementation mặc định.

Kết quả của Sprint 0 là một quyết định có bằng chứng:

```text
READY_FOR_SPRINT_001
hoặc
BLOCKED_BY_DOCUMENTATION_OR_DECISION_GAPS
```

---

# 2. Phạm vi thẩm quyền

Tài liệu này là nguồn chuẩn cho:

- Readiness checklist trước khi bắt đầu repository.
- Deliverables của giai đoạn chuẩn bị.
- Điều kiện kích hoạt Sprint 1.
- Bằng chứng Goose phải cung cấp cho cuộc review Sprint 0.

Tài liệu này không phải nguồn chuẩn cho:

- Product requirements chi tiết.
- Bounded Context ownership.
- Exact database, API, Event hoặc permission contracts.
- Exact package versions ngoài Toolchain Lock.
- Exact implementation của Sprint 1 trở đi.
- Trạng thái hoàn thành của Sprint sau.

---

# 3. Từ khóa quy chuẩn

- **MUST / PHẢI:** bắt buộc.
- **MUST NOT / KHÔNG ĐƯỢC:** bị cấm.
- **SHOULD / NÊN:** mặc định áp dụng; lệch chuẩn phải có lý do.
- **MAY / CÓ THỂ:** tùy chọn hợp lệ.
- **CANONICAL:** nguồn chính thức theo chủ đề.
- **SUPERSEDED:** chỉ giữ lịch sử, không dùng triển khai.
- **PENDING VALIDATION:** chưa đủ điều kiện trở thành implementation truth.
- **BLOCKER:** ngăn chuyển Sprint.

---

# 4. Trạng thái dự án tại thời điểm bắt đầu

```yaml
project: crm_bds_ai
project_type: greenfield
repository_initialized: false
production_data_exists: false
current_phase: documentation_preparation
current_gate: sprint_000
current_implementation_sprint: none
allowed_code_changes: false
```

Goose MUST xác minh trạng thái thực tế. Nếu repository hoặc code đã tồn tại, Goose phải dừng và lập báo cáo lệch trạng thái thay vì tiếp tục coi là Greenfield chưa khởi tạo.

---

# 5. Mandatory reading

Goose phải đọc theo `README.md` và tối thiểu các nguồn sau:

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

Không được dùng câu “đã đọc toàn bộ docs” làm bằng chứng. Báo cáo phải liệt kê file, version, status và vấn đề phát hiện.

---

# 6. In Scope

## 6.1. Canonical document inventory

Kiểm tra sự tồn tại, canonical path, version, status, owner và quan hệ supersede của tối thiểu:

### Product

- Product Charter.
- Product Overview.
- PRD.
- Domain Glossary.

### Architecture

- Architecture Overview.
- Context Map.
- Source of Truth Matrix.
- Accepted ADR set.
- Dependency rules hoặc nội dung tương đương được canonical hóa.

### Engineering

- AI Agent Engineering Constitution.
- Universal AI Engineering Orchestration Skill.
- Documentation Governance.
- Technology Toolchain Lock.
- Coding, Database, API, Event, Testing, Security, Frontend và Observability Standards.

### Execution

- Sprint Roadmap.
- Sprint 0 Preparation Pack.
- Sprint 1 Execution Pack.
- Future Sprint Packs phải ở trạng thái không active.

## 6.2. Authority and conflict audit

Goose phải tạo bảng:

| Chủ đề | Canonical source | Competing source | Kết luận |
|---|---|---|---|

Tối thiểu kiểm tra:

- Product scope.
- Terms.
- Context ownership.
- Architecture decisions.
- Tool versions.
- Database/API/Event exact contracts.
- Permissions, scopes, masking và errors.
- Current Sprint.
- Completion evidence.

Mọi xung đột BLOCKING phải được giải quyết hoặc chuyển thành quyết định có owner trước khi PASS.

## 6.3. Superseded document quarantine

Các tài liệu cũ không còn canonical MUST:

- Được xóa khỏi mandatory reading.
- Được chuyển vào `docs/historical/` khi cần giữ lịch sử.
- Có banner `SUPERSEDED / DO NOT USE FOR IMPLEMENTATION`.
- Không giữ cùng tên/path với canonical file mới.

Đặc biệt:

- Mega architecture cũ không được cạnh tranh với `architecture-overview.md`.
- Master Sprint 2–57 cũ không được dùng làm implementation contract.
- Sprint Pack cũ không được giữ trạng thái `Approved for Implementation` khi chưa active.
- Version matrix không được lặp trong Sprint Pack.

## 6.4. Toolchain readiness

Kiểm tra Toolchain Lock theo ba mức:

1. Exact core locks đã được phê duyệt.
2. Approved technology families nhưng exact patch còn phải pin.
3. Pending decisions bắt buộc giải quyết trước Sprint 1.

Sprint 0 MUST hoàn thiện:

- Runtime version files.
- Backend dependency manifest và lockfile.
- Frontend dependency manifest và lockfile.
- Container image tags hoặc digests.
- Local/CI compatibility matrix.
- Upgrade and exception workflow.

Không được chọn “latest” tại thời điểm chạy mà không cập nhật Toolchain Lock.

## 6.5. Goose–Opencode operating model

Xác minh:

- Goose là Orchestrator/Tech Lead.
- Opencode là Executor.
- Goose sở hữu preflight, decomposition, delegation, independent verification và acceptance recommendation.
- Opencode không tự mở rộng phạm vi, thay ADR hoặc chọn lại stack.
- Agent state chỉ là execution state, không phải Product/Sprint truth.
- Sprint Done chỉ đến từ Acceptance Report có evidence.

## 6.6. Repository initialization plan

Sprint 0 chỉ tạo kế hoạch Sprint 1, không tạo implementation.

Kế hoạch phải nêu:

- Repository boundaries.
- Required top-level areas.
- Local infrastructure capabilities.
- Quality command strategy.
- CI gates.
- Contract bootstrap.
- Documentation runtime artifacts.
- Risks và blockers.

## 6.7. Project control artifacts

Chuẩn bị hoặc xác nhận template cho:

```text
docs/project-status.md
docs/handoffs/current-handoff.md
docs/known-issues.md
docs/sprints/sprint-000/implementation-notes.md
docs/sprints/sprint-000/acceptance-report.md
.agent/project-profile.yaml
.agent/goose/state.json
.agent/goose/progress.md
```

Quy tắc:

- `.agent/goose/state.json` chỉ dùng resume orchestration.
- `.agent/goose/progress.md` là operational log.
- `docs/project-status.md` là trạng thái cấp dự án.
- `current-handoff.md` là bàn giao hiện tại.
- Acceptance Report là bằng chứng Sprint.
- Không artifact nào thay thế OpenAPI, Alembic, JSON Schema, AsyncAPI hoặc registries.

---

# 7. Out of Scope

Sprint 0 MUST NOT:

- Tạo backend/frontend application code.
- Tạo business table hoặc migration.
- Tạo API/Event business contracts.
- Tạo placeholder entity cho Sprint tương lai.
- Cài dependency ngoài thao tác kiểm chứng toolchain đã được phê duyệt.
- Tạo Docker stack production.
- Tạo compatibility layer.
- Quyết định chi tiết Context chưa đến thời điểm phân tích.
- Kích hoạt Sprint 2 hoặc Sprint 3.
- Tuyên bố software đã chạy.

---

# 8. Readiness workstream

## Workstream A — Document registry

Kết quả:

- Canonical inventory.
- Missing document list.
- Superseded list.
- Broken link list.
- Version/status anomalies.

## Workstream B — Authority audit

Kết quả:

- Subject-authority matrix.
- Conflict list.
- Resolution or decision owner.

## Workstream C — Toolchain validation

Kết quả:

- Resolved runtime/package/container locks.
- Unsupported alternatives.
- Environment prerequisites.

## Workstream D — Agent orchestration readiness

Kết quả:

- Project profile.
- State/log locations.
- Delegation template.
- Verification template.
- Stop conditions.

## Workstream E — Sprint 1 activation review

Kết quả:

- Sprint 1 scope understood.
- Dependencies met.
- No active blocker.
- Activation recommendation.

---

# 9. Required checks

Goose MUST perform checks equivalent to:

- File/path inventory.
- Duplicate canonical Document ID detection.
- Duplicate canonical path detection.
- Broken Markdown link/path detection where feasible.
- Search for obsolete architecture filename references.
- Search for active references to old master Sprint document.
- Search for multiple `current` or `Approved for Implementation` Sprint Packs.
- Search for exact tool versions duplicated outside Toolchain Lock.
- Search for `TODO`, `TBD`, `PLACEHOLDER`, `PENDING` in P0 documents and classify each occurrence.
- Confirm all 16 Context names are consistent.
- Confirm `infra` is technical namespace, not a seventeenth business Context.
- Confirm source-of-truth invariants are consistent across Product, Architecture and Sprint 1.

A script may automate checks, nhưng Goose phải đọc và đánh giá semantic conflicts; grep pass không đồng nghĩa readiness pass.

---

# 10. Blockers

Sprint 0 MUST fail hoặc remain blocked nếu có một trong các điều kiện:

- Product identity hoặc project name không thống nhất.
- Context Map và Source of Truth Matrix mâu thuẫn.
- Architecture Overview thiếu hoặc chưa Accepted.
- Constitution và orchestration Skill không xác định rõ Goose/Opencode.
- Toolchain có runtime bắt buộc nhưng chưa xác định family hoặc exact lock strategy.
- Có từ hai Sprint trở lên được đánh dấu active.
- Sprint 1 phụ thuộc tài liệu hoặc decision chưa có.
- Tài liệu superseded vẫn nằm trong mandatory reading.
- AI Agent được phép tự đoán exact DDL/API/Event/permission.
- Không có cách ghi Acceptance Report và handoff.

---

# 11. Deliverables

Sprint 0 phải tạo hoặc cập nhật:

```text
docs/sprints/sprint-000/implementation-notes.md
docs/sprints/sprint-000/readiness-review.md
docs/sprints/sprint-000/acceptance-report.md
docs/project-status.md
docs/handoffs/current-handoff.md
.agent/project-profile.yaml
.agent/goose/state.json
.agent/goose/progress.md
```

Acceptance Report phải ghi:

- Documents reviewed.
- Canonical inventory result.
- Conflict audit result.
- Superseded files handled.
- Toolchain validation result.
- Open decisions and owners.
- Commands/scripts used.
- Files changed.
- Limitations.
- Final status.

---

# 12. Definition of Ready for Sprint 0

Sprint 0 Ready khi:

1. Project directory xác định.
2. Bộ tài liệu hiện tại đã được đặt vào repository hoặc staging folder.
3. Product Owner xác nhận dự án chưa bắt đầu code.
4. Goose có quyền đọc/ghi tài liệu cần thiết.
5. Không yêu cầu triển khai business feature trong cùng nhiệm vụ.

---

# 13. Definition of Done

Sprint 0 chỉ PASS khi:

1. Canonical document inventory hoàn chỉnh.
2. Không có unresolved P0 conflict.
3. Superseded docs không còn active.
4. Toolchain đủ điều kiện kích hoạt Sprint 1.
5. Goose/Opencode operating model rõ.
6. Chỉ Sprint 0 là current gate.
7. Sprint 1 ở trạng thái planned, chưa tự chạy.
8. Project Status và Current Handoff phản ánh `NOT STARTED`.
9. Sprint 0 Acceptance Report có bằng chứng thật.
10. Architecture/Product/Security/Engineering owners hoặc Product Owner chấp thuận activation.

PASS không có nghĩa phần mềm đã được xây dựng. PASS chỉ có nghĩa bộ chuẩn bị đủ an toàn để bắt đầu Sprint 1.

---

# 14. Chỉ thị cho Goose

1. Không gọi Opencode để code application trong Sprint 0.
2. Có thể giao Opencode hoặc agent phụ thực hiện kiểm tra tĩnh tài liệu, nhưng Goose phải review kết quả.
3. Không tự sửa nghĩa Product/Architecture để làm tài liệu “pass”.
4. Không xóa tri thức cũ nếu cần audit; archive và gắn superseded banner.
5. Không biến open decision thành default implementation.
6. Không kích hoạt Sprint 1 trước Acceptance PASS.
7. Báo cáo trung thực các file chưa thể đọc hoặc kiểm chứng.

---

# 15. Kết luận

Sprint 0 bảo đảm dự án bắt đầu từ một bộ chỉ dẫn thống nhất, không phải từ một tập Markdown có thẩm quyền cạnh tranh.

```text
Canonical Documents Aligned
+ Toolchain Validated
+ One Active Gate
+ Goose/Opencode Roles Clear
+ No Unresolved P0 Conflict
= READY_FOR_SPRINT_001
```
