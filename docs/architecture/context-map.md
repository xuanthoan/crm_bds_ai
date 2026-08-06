# CRM_BDS_AI — CONTEXT MAP

**Document ID:** `ARCH-CTX-001`  
**Canonical path:** `docs/architecture/context-map.md`  
**Product:** `crm_bds_ai`  
**Version:** `1.0.0`  
**Status:** `Ready for Review`  
**Owner:** `Architecture Owner`  
**Reviewers:** `Product Owner, Technical Owner, Security Owner, QA Owner`  
**Last reviewed:** `2026-08-05`  
**Classification:** `INTERNAL`


# 1. Mục tiêu

Khóa quan hệ upstream/downstream và integration style giữa 16 Bounded Contexts của Modular Monolith.

# 2. Contexts

```text
platform, iam, party, lead, product, matching, transaction, contract,
revenue, activity, marketing, analytics, documents, audit, integration, operations
```

# 3. Nguyên tắc bản đồ

- Không Shared Database ownership xuyên Context.
- Không import repository/ORM model của Context khác.
- Không cross-schema business writes.
- Published API/Event là contract boundary.
- Integration dùng Anti-Corruption Layer với provider models.
- Analytics là downstream read model.
- Audit là append-only evidence sink.
- Operations là runtime orchestration, không phải super-context.

# 4. Quan hệ canonical

| Upstream/Owner | Downstream/Consumer | Integration style | Quy tắc |
|---|---|---|---|
| `platform` | `iam` | Published configuration/API | IAM dùng Legal Entity, calendar và policy definitions; không ghi Platform state. |
| `platform` | `lead/activity/marketing/contract/revenue` | Published definitions/events | Workflow/SLA/numbering definitions được tham chiếu theo version. |
| `iam` | `mọi Context` | Authorization service/read contract | Authenticated principal, scope, grants, delegation; downstream không tự mở rộng quyền. |
| `party` | `lead` | API/Event | Lead resolve/link Party khi conversion; Lead không sở hữu identity. |
| `party` | `matching` | Read contract/Event | Matching dùng Requirement/Financial Profile snapshots theo scope. |
| `lead` | `party` | Process Manager | Lead Conversion tạo/link Customer relationship qua Party. |
| `marketing` | `lead` | Command/Event | Marketing gửi idempotent Lead intake evidence; Lead quyết định official Lead. |
| `product` | `matching` | Read contract/Event | Matching dùng Listing/Price/Availability snapshots. |
| `matching` | `transaction` | Reference/Event | Transaction dùng shortlist/match lineage; không coi match là lock. |
| `transaction` | `product` | Command/Result Event | Hold process yêu cầu Product Commercial Lock; Product quyết định lock. |
| `transaction` | `contract` | Handoff command/result | Booking/Transaction Case handoff; Contract validate và chấp nhận. |
| `contract` | `product` | Decision request/Event | Contract effectiveness/cancellation tạo inventory-impact request; Product quyết định availability. |
| `contract` | `revenue` | Events/read contract | Revenue dùng Contract/Payment/Allocation/Receipt/Refund facts. |
| `transaction` | `revenue` | Events/read contract | Revenue dùng participants, co-sale agreement và responsibility snapshots. |
| `activity` | `mọi business Context` | Command/Event | Activity ghi Task/Interaction outcomes; business transition vẫn do owner quyết định. |
| `marketing` | `activity` | Command/Event | Marketing gửi message/task intent; Activity sở hữu canonical Interaction. |
| `documents` | `business Contexts` | API/Event | Business Context giữ Document references; Documents sở hữu artifacts. |
| `integration` | `business Contexts` | ACL/API/Event | Integration chuẩn hóa provider facts; owner quyết định business outcome. |
| `business Contexts` | `analytics` | Events/read contracts | Analytics ingest governed facts; read-only với source. |
| `mọi Context` | `audit` | Audit fact append | Audit ghi evidence bất biến; không thay operational state. |
| `operations` | `mọi Context` | Operational orchestration | Jobs/alerts/incidents/repair; không direct-write business schema. |

# 5. Context relationship patterns

- **Open Host Service + Published Language:** API/OpenAPI và Event/JSON Schema.
- **Customer/Supplier:** downstream nêu nhu cầu nhưng upstream giữ model authority.
- **Anti-Corruption Layer:** `integration` bảo vệ domain khỏi provider payload.
- **Conformist:** chỉ dùng cho read-only projection khi accepted contract đã ổn định.
- **Shared Kernel:** mặc định cấm; chỉ cho technical primitives có ADR.

# 6. Luồng trọng yếu

## 6.1. Lead Conversion

```text
lead → party → lead conversion result → activity/analytics
```

## 6.2. Hold Activation

```text
transaction Hold Request → product Commercial Lock → transaction Active Hold
```

## 6.3. Booking to Contract

```text
transaction Booking → contract Handoff → contract Accepted/Rejected
```

## 6.4. Cash to Revenue

```text
contract Payment/Allocation/Receipt → revenue Payment Application/Entitlement
```

## 6.5. Marketing outbound

```text
marketing intent → party consent check → activity eligibility → integration delivery
```

# 7. Prohibited relations

- `transaction` ghi Product lock table.
- `revenue` tạo Payment/Receipt.
- `marketing` tạo Customer identity hoặc official Lead trực tiếp.
- `analytics` sửa source aggregate.
- `operations` sửa business data bằng universal repository.
- `documents` tự chuyển Contract state.
