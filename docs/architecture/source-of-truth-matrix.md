# CRM_BDS_AI — SOURCE OF TRUTH MATRIX

**Document ID:** `ARCH-SOT-001`  
**Canonical path:** `docs/architecture/source-of-truth-matrix.md`  
**Product:** `crm_bds_ai`  
**Version:** `1.0.0`  
**Status:** `Ready for Review`  
**Owner:** `Architecture Owner`  
**Reviewers:** `Product Owner, Technical Owner, Security Owner, QA Owner`  
**Last reviewed:** `2026-08-05`  
**Classification:** `INTERNAL`


# 1. Quy tắc

- Mỗi business concept có một write authority.
- Context khác chỉ giữ reference, snapshot hoặc projection có lineage.
- Source of Truth không được suy ra từ UI, route, table name hoặc Sprint Pack.
- Khi matrix và code mâu thuẫn, implementation phải block và tạo Documentation Conflict.

# 2. Matrix

| Concept | Write authority | Canonical write path | Consumers | Prohibition/Note |
|---|---|---|---|---|
| Enterprise | `platform` | Platform commands/API | iam, analytics | Không tạo ở IAM |
| Legal Entity | `platform` | Platform commands/API | mọi Context | Scope không thay master |
| Business Calendar | `platform` | Versioned definition | activity, contract, revenue | Runtime instance thuộc consumer |
| Workforce Subject Reference | `iam` | IAM command | activity, revenue | Canonical Person thuộc party |
| Employment Assignment | `iam` | IAM command | lead, activity, revenue | Snapshot khi tính lịch sử |
| User Account / Service Account | `iam` | IAM command | mọi Context | Không đồng nghĩa Party |
| Role / Permission / Access Grant | `iam` | Security registry + IAM | mọi Context | Frontend không cấp quyền |
| Party / Person / Organization identity | `party` | Party commands | lead, contract, marketing | Enterprise-global identity |
| Customer Relationship | `party` | Party commands | lead, matching, transaction | Không phải Lead owner |
| Phone Identity / Contact Point | `party` | Party commands | lead, marketing, activity | Phone-only dedup rule |
| Requirement / Financial Profile | `party` | Party commands | matching | AI suggestion không tự sửa |
| Consent / Contact Restriction | `party` | Party commands | marketing, activity | Re-check trước outbound |
| Lead / Lead Assignment / Protection | `lead` | Lead commands | activity, analytics | Customer identity không thuộc Lead |
| Lead Source Snapshot | `lead` | Lead intake acceptance | marketing, analytics | Campaign mới không ghi đè |
| Project / Asset / Listing | `product` | Product commands | matching, transaction, analytics | Không thuộc Marketing |
| Ownership / Selling Right | `product` | Product commands | contract, transaction | Activation cần validation |
| Availability / Commercial Lock | `product` | Atomic Product commands | transaction, analytics | UI/cache không authority |
| Matching Rule / Run / Result / Shortlist | `matching` | Matching commands | transaction, analytics | Shortlist không lock |
| Deal / Transaction Case | `transaction` | Transaction commands | activity, analytics | Không phải Contract |
| Proposal / Negotiation / Hold / Booking | `transaction` | Transaction commands | product, contract | Hold khác Commercial Lock |
| Deposit Commitment | `transaction` | Transaction commands | contract | Không phải Payment |
| Contract / Contract Version / Parties | `contract` | Contract commands | product, revenue, documents | Signed version immutable |
| Payment Plan / Buyer Receivable | `contract` | Contract commands | revenue, analytics | Khác Revenue Receivable |
| Payment / Allocation / Receipt | `contract` | Finance commands | revenue, analytics | Receipt immutable |
| Refund / Credit / Transfer / Settlement | `contract` | Finance commands | revenue, product | Không tự mở Listing |
| Revenue Arrangement / Entitlement | `revenue` | Revenue commands | analytics | Gross funds không mặc định Revenue |
| Commission Plan / Entitlement / Payout | `revenue` | Revenue commands | analytics, integration | Approved batch không đồng nghĩa Paid |
| Task / Appointment / Interaction | `activity` | Activity commands | mọi Context | Task completed không business transition |
| Timeline / SLA / NBA | `activity` | Projection/runtime commands | analytics | Timeline không Audit |
| Campaign / Capture / Touchpoint | `marketing` | Marketing commands | lead, analytics | Capture không official Lead |
| Audience / Journey / Message Intent | `marketing` | Marketing commands | activity, integration | Intent không delivery |
| Marketing Attribution / Operational Spend | `marketing` | Marketing commands | analytics | Không thay Sales Attribution |
| Dataset / Projection / Metric / Dashboard | `analytics` | Analytics commands | users/BI | Read-only source |
| Snapshot / Forecast / DQ / Reconciliation | `analytics` | Analytics commands | management | Không sửa source |
| File / Document / Version / Dossier | `documents` | Documents commands | business Contexts | URL không canonical identity |
| Signature Envelope / Evidence | `documents` | Documents commands | contract, integration | Không tự effective Contract |
| Audit Fact / Seal / Chain | `audit` | Append API/Event | security/review | Không update/delete |
| Connection / Mapping / Webhook / Sync | `integration` | Integration commands | business Contexts | Provider payload qua ACL |
| Delivery Attempt / DLQ / Replay | `integration` | Integration runtime | operations | Idempotency bắt buộc |
| Job / Alert / Incident / Maintenance | `operations` | Operations commands | operators | Không business owner |
| Backup / Restore / DR / Data Repair | `operations` | Operations commands | audit | Repair qua owning Context |

# 3. Cross-context reference policy

- Dùng opaque identifier + accepted snapshot khi cần lịch sử.
- Không cross-schema business foreign key mặc định.
- Không cascade delete xuyên Context.
- Merge/redirect được xử lý bằng Event và resolver.
- Projection có thể stale nhưng phải công bố freshness.

# 4. Review gate

Mọi migration, API, Event hoặc Context Pack phải chỉ ra từng field/aggregate thuộc dòng nào trong matrix này.


# AI source-of-truth extension

| Information | Canonical authority |
|---|---|
| AI Use Case, Prompt, Model and Routing definitions | Platform registries |
| Provider connection and adapter configuration | Integration |
| AI jobs, attempts, health, usage and evaluation runs | Operations |
| AI transcript/extraction/generated artifacts | Documents |
| AI request/route/decision evidence | Audit |
| Accepted business state | Owning business Context only |
