# CRM_BDS_AI — DOCUMENTATION GOVERNANCE

**Document ID:** `ENG-DOC-001`  
**Canonical path:** `docs/engineering/documentation-governance.md`  
**Product:** `crm_bds_ai`  
**Version:** `1.0.0`  
**Status:** `Ready for Review`  
**Owner:** `Architecture Owner`  
**Reviewers:** `Product Owner`, `Technical Owner`, `Security Owner`, `QA Owner`  
**Last reviewed:** `2026-08-05`  
**Classification:** `INTERNAL`

# 1. Mục tiêu

Khóa cách tạo, đặt tên, version, review, supersede, liên kết và kiểm tra tài liệu để AI Agent không tạo nguồn chân lý cạnh tranh.

# 2. Canonical entry point

Repository entry point duy nhất:

```text
README.md
```

Không tạo README entry point cạnh tranh bên trong thư mục `docs/`. README trong thư mục con chỉ được dùng làm index cục bộ và phải trỏ về root `README.md`.

# 3. Canonical directory structure

```text
crm_bds_ai/
├── README.md
├── .skills/
├── backend/                 # được tạo từ Sprint 1
├── frontend/                # được tạo từ Sprint 1
├── contracts/               # được tạo từ Sprint 1/2
├── infrastructure/          # được tạo từ Sprint 1
└── docs/
    ├── product/
    │   ├── product-overview.md
    │   ├── PRD.md
    │   ├── domain-glossary.md
    │   └── capabilities/
    ├── architecture/
    ├── adr/
    ├── engineering/
    ├── security/
    ├── design/
    ├── contexts/
    ├── operations/
    ├── runbooks/
    ├── roadmap/
    ├── sprints/
    ├── reviews/
    ├── releases/
    ├── incidents/
    └── historical/
```

# 4. Document classes

| Class | Purpose | Exact implementation authority |
|---|---|---|
| Product Overview | Product direction and non-negotiable truths | No |
| PRD | Product requirements and acceptance outcomes | No |
| Product Capability Specification | Business meaning, rules, boundaries and anti-patterns | No |
| Context Implementation Pack | Context behavior and implementation baseline | Partially; machine contracts still win |
| ADR | Accepted architecture decision | Yes for decision intent |
| Engineering/Security Standard | Cross-cutting rule | Yes within scope |
| Sprint Pack | Time-boxed execution scope | No ownership override |
| Alembic/OpenAPI/JSON Schema/AsyncAPI/Registry | Executable contract | Yes |
| Runbook | Operational procedure | Yes for procedure |
| Handoff/Project Status | Current work summary | No business authority |
| Historical | Evidence only | No |

# 5. Metadata

Canonical Markdown documents must include:

- Document ID.
- Canonical path.
- Product.
- Version.
- Status.
- Owner.
- Reviewers when relevant.
- Last reviewed.
- Classification.

# 6. Statuses

```text
Draft
In Review
Ready for Review
Accepted
Published
Planned
Not Active
Roadmap Only
Superseded
Retired
Historical
Template
```

`Accepted document` không chứng minh code đã tồn tại. `Planned Sprint` không phải active Sprint.

# 7. Versioning

- PATCH: path, wording, link hoặc clarification không đổi meaning.
- MINOR: thêm rules/sections hoặc thay governance đáng kể nhưng tương thích.
- MAJOR: thay meaning/ownership/contract không tương thích.
- Machine contracts theo compatibility rules riêng.

Canonical filename không chứa `v2`, `final`, `latest`, `new` hoặc `copy`.

# 8. Authority and precedence

Precedence được khóa trong root `README.md`. Tài liệu thấp hơn không được override ADR, Source of Truth, Glossary hoặc machine contract.

# 9. Product Capability versus Context

```text
Product Capability ≠ Bounded Context ≠ schema ≠ service
```

Capability files nằm tại `docs/product/capabilities/`. Context Packs nằm tại `docs/contexts/<context>/`.

Capability 14 là Composite Product Capability Overview cho `documents`, `audit`, `integration`, `operations`; không tạo `runtime_support` super-context.

# 10. Supersede and historical handling

- Không xóa evidence đã phát hành.
- File mới ghi `Supersedes`; file cũ ghi `Superseded by` và chuyển `docs/historical/` khi phù hợp.
- Historical documents phải có banner không được dùng cho implementation.
- Không copy nội dung canonical sang nhiều vị trí.

# 11. Change control

Thay đổi ownership, permission, financial invariant, Customer identity, Commercial Lock, immutable Receipt, Event/API hoặc Metric cần owner review và impact analysis.

# 12. Generated documentation

Generated files phải ghi `DO NOT EDIT MANUALLY`, nêu source/command và được CI drift-check.

# 13. Link and path rules

- Dùng repository-relative path.
- Không commit Windows absolute paths.
- Link phải tồn tại hoặc được đánh dấu `Planned / Not Yet Required` trong registry.
- Đổi path phải cập nhật root README, registries, Sprint Packs và companion artifacts.

# 14. Security

Không ghi credentials, token, private key, real Customer PII, bank details, signed URL hoặc raw provider payload nhạy cảm.

# 15. Validation

`docs-check` phải kiểm tra metadata, links, IDs, statuses, forbidden filenames, duplicate canonical subjects, stale paths, secret patterns, Sprint contradictions và generated drift.

# 16. Review gate

Tài liệu `Ready for Review` chỉ trở thành implementation authority sau review/acceptance phù hợp. Goose phải ghi rõ tài liệu nào đã được review trước khi giao Opencode code.

# 17. Change Log

## Version 1.1.0 — 2026-08-05

- Chuyển canonical entry point về root `README.md`.
- Thay Product Module directory bằng Product Capability directory.
- Khóa 14 Capabilities và 16 Context Pack convention.
- Đồng bộ ADR directory thành `docs/adr/` và Glossary thành `docs/product/domain-glossary.md`.
- Bổ sung rules cho Capability 14 composite overview và historical handling.
