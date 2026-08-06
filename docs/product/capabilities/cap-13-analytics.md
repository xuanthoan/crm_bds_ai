# CRM_BDS_AI — CAPABILITY 13: ANALYTICS

## Management Reporting, Semantic Metrics, KPI, Dashboard, Forecast, Drill-down, Snapshot and Analytics Authorization

**Document ID:** `PROD-CAP-ANA-001`
**Canonical path:** `docs/product/capabilities/cap-13-analytics.md`
**Product:** `crm_bds_ai`
**Version:** `1.0.0`  
**Status:** `Accepted / Product Capability Baseline`
**Document type:** `Product Capability Specification`
**Primary capability code:** `CAP-ANA`
**Primary owning Context:** `analytics`
**Owner:** `Product Owner`
**Co-owner:** `Analytics Domain Owner`
**Reviewers:** `Architecture Owner`, `Platform Domain Owner`, `IAM Domain Owner`, `Lead Domain Owner`, `Party Domain Owner`, `Product Domain Owner`, `Matching Domain Owner`, `Transaction Domain Owner`, `Contract Domain Owner`, `Revenue Domain Owner`, `Activity Domain Owner`, `Marketing Domain Owner`, `Documents Owner`, `Integration Owner`, `Audit Owner`, `Operations Owner`, `Security Owner`, `Database Owner`, `API Owner`, `Event Architecture Owner`, `Data Governance Owner`, `QA Owner`
**Effective date:** `2026-08-05`  
**Last reviewed:** `2026-08-05`  
**Classification:** `INTERNAL`

---

# 0. Phạm vi thẩm quyền và quan hệ tài liệu

Tài liệu này là nguồn canonical cho:

- Product outcomes của Analytics Capability.
- Business meanings của Dataset, Projection, Semantic Metric, KPI, Dashboard, Report, Snapshot, Forecast, Scenario, Drill-down, Drill-through, Analytical Access Policy, Data Freshness, Data Quality, Reconciliation, Alert và Anomaly.
- Nguyên tắc analytical read-only, metric governance, as-of reporting, scope intersection, aggregate/detail separation và controlled export.
- Capability boundaries, invariants, acceptance outcomes và anti-patterns.
- Đầu vào phân tích cho Analytics Context Implementation Pack.

Tài liệu này không phải nguồn exact cho:

- Physical database schema hoặc DDL.
- Exact API paths, request/response payloads hoặc error contracts.
- Exact Event names, envelopes, channels hoặc payloads.
- Exact permission codes, scope expressions, masking rules hoặc role matrix.
- Exact Metric formulas, Dataset schemas, Forecast models, thresholds hoặc reconciliation tolerances.
- Exact source extraction, CDC, warehouse, cache, scheduler, queue hoặc deployment topology.
- Exact generated Report/Export file format, binary storage hoặc retention implementation.
- Exact BI connector, credential hoặc external publication transport.
- Exact statutory accounting, General Ledger, payroll hoặc bank reporting.
- Exact production SLO, capacity, query budget hoặc recovery configuration.

Nguồn exact tương ứng:

| Chủ đề | Nguồn canonical |
|---|---|
| Thuật ngữ | Domain Glossary |
| Product requirements | PRD |
| Context ownership | Source of Truth Matrix |
| Architecture boundaries | Architecture Overview, Context Map và Accepted ADRs |
| Analytics behavior chi tiết | Analytics Context Implementation Pack |
| Database | Analytics Context DB Specification và Alembic migrations |
| API | OpenAPI |
| Events | JSON Schema, AsyncAPI và Event Registry |
| Permissions/scopes/masking/SoD | Security registries và matrices |
| Source business facts | Owning Context contracts |
| User/workforce/organization/access context | IAM Context contracts |
| Generated Report/Export artifacts | Documents Context contracts |
| BI/warehouse/provider transport | Integration Context contracts |
| Immutable Audit facts | Audit Context |
| Runtime jobs, queues, retries và incidents | Operations Context |
| Metric definitions/certification | Analytics Metric Registry |
| Công việc hiện tại | Current Sprint Detailed Execution Pack |

**Capability không đồng nghĩa Bounded Context.** Capability này chủ yếu được thực hiện bởi `analytics` Context.

**Analytics là read-only đối với business truth.** Analytics được phép tạo projections, aggregates, Metric results, Snapshots, Forecasts và analytical adjustments, nhưng không được direct-write aggregate nghiệp vụ thuộc `platform`, `iam`, `lead`, `party`, `product`, `matching`, `transaction`, `contract`, `revenue`, `activity` hoặc `marketing`.

Các phần candidate lifecycle, data model, operations, permissions, Events, screens, formulas, thresholds và reports chỉ là design input. Chúng không được dùng thay machine-readable contracts hoặc Context Packs đã được chấp nhận.

---
# 1. Mục tiêu của capability

Analytics Capability là lớp semantic analytics và management reporting thống nhất của `crm_bds_ai`.

Capability hợp nhất governed facts từ các Context nguồn để cung cấp:

- Operational và Executive Dashboards.
- Semantic Metrics và KPI Scorecards.
- Funnel, Pipeline, Cohort, Trend và Time-series analysis.
- Current, as-of, Snapshot và Restated views.
- Forecast, Scenario, Target và Variance.
- Drill-down và Drill-through.
- Data Freshness, Data Quality và Reconciliation.
- Alert và Anomaly signals.
- Scheduled Reports và controlled exports.
- Governed publication cho external BI.

Capability phải trả lời được:

- Mỗi con số đang dùng Metric Version và Dataset Version nào.
- Grain, formula, filters, time field, currency policy và deduplication rule là gì.
- Dữ liệu phản ánh current state, as-of state, original Snapshot hay Restatement.
- Dữ liệu được biết tại thời điểm nào và phát sinh nghiệp vụ tại thời điểm nào.
- Scope nào được backend áp dụng.
- User có quyền xem aggregate, breakdown, detail, source resource hay export hay không.
- Field nào bị hidden, masked hoặc aggregate-only.
- Source Context, source resource, source Event và data cutoff nào tạo ra kết quả.
- Dữ liệu real-time, near-real-time, scheduled hay stale.
- Projection có reconcile với source trong tolerance không.
- Forecast nào là system, user, manager, approved hoặc locked.
- Forecast dùng input snapshot, model version và assumptions nào.
- Forecast trước đây chính xác và biased ra sao.
- Contract Value, Buyer Payment, Revenue, Revenue Collected và Commission khác nhau thế nào.
- Marketing sourced/influenced và Revenue basis được phân biệt ra sao.
- Snapshot cuối kỳ có thể tái tạo và restate mà không xóa bản gốc hay không.
- External BI nhận Dataset nào, fields nào, scope nào và đến khi nào.
- Alert hoặc Anomaly dựa trên baseline nào và có cần điều tra hay không.

Capability phải hỗ trợ:

- Multi-Legal Entity, Multi-Project, Multi-Branch và organization-as-of reporting.
- Dataset Registry và versioned Projection metadata.
- Certified Semantic Metrics.
- KPI, Target, Scorecard và variance.
- Dashboard/Widget versioning.
- Reports, subscriptions và secure delivery.
- Snapshot lock, Restatement và bitemporal/as-of queries.
- Rule-based, statistical và externally referenced Forecast models.
- Scenario planning.
- Row-, field-, metric-, dimension-, aggregate-, detail- và time-level analytical access.
- Scope-aware caching và backend-enforced drill-down.
- Export policy, watermark, expiry và Audit.
- Data Freshness, Data Quality, Reconciliation, Alert và Anomaly.
- Controlled BI/Data Warehouse publication.
- Full lineage, versioning, idempotency, observability và Audit evidence.

Nguyên tắc canonical:

> Analytics định nghĩa, tổng hợp, lưu projection, Snapshot và Forecast để giải thích dữ liệu; Analytics không trở thành nguồn chân lý nghiệp vụ thứ hai, không sửa dữ liệu nguồn và mọi kết quả phải truy ngược được về Metric Version, Dataset Version, source lineage, data cutoff, freshness và enforced scope.

---
# 2. Vị trí của capability trong kiến trúc

Analytics Context sử dụng governed facts từ:

- `platform`: configuration definitions, Business Calendar, Reporting Calendar, workflows và policy versions.
- `iam`: User, Workforce, organization, Legal Entity, Project Access, delegation, assignment history và effective authorization.
- `lead`: Lead, assignment, source snapshot, qualification, SLA và conversion facts.
- `party`: Party/Customer, Requirement, role, identity merge và contactability facts.
- `product`: Partner, Project, Asset, Listing, Price, Availability, Commercial Lock, Ownership và Selling Right facts.
- `matching`: Matching Run, Match Result, Shortlist, Feedback và conversion facts.
- `transaction`: Deal, stage history, Proposal, Hold, Booking, Deposit Commitment và operational forecast inputs.
- `contract`: Contract, Payment Plan, Receivable, Payment, Allocation, Receipt, Refund, Settlement, Cancellation và completion facts.
- `revenue`: Revenue Entitlement, Recognition, Receivable, Collection, Commission, Payout và Clawback facts.
- `activity`: Task, Appointment, Call, Interaction, SLA Instance và Next Best Action facts.
- `marketing`: Campaign, source evidence, Audience, Spend, Conversion và Attribution facts.
- `documents`: generated Report/Export Document references.
- `integration`: external ERP, payroll, bank, benchmark, warehouse và BI transport facts.
- `operations`: refresh/rebuild/report/export/forecast runtime state.
- `audit`: immutable Audit evidence references.

Analytics Context cung cấp:

- Permission-aware Dashboards, Reports, Metrics, Snapshots và Forecasts.
- Versioned analytical facts cho Operating Review và executive decision support.
- Data Quality/Reconciliation findings và source-correction requests.
- Governed aggregate datasets cho external BI qua Integration.
- Drill-through references về API/workspace của owning Context.
- Scope/masking/freshness/lineage explanations.

Kiến trúc logic:

```text
Owning Contexts
→ Published Events / Read Contracts / Approved Extraction
→ Analytics Projection Layer
→ Semantic Metric Layer
→ Snapshot / Forecast / Target Layer
→ Dashboard / Report / Alert / Export
→ Drill-through to owning Context API
```

Analytics không direct-write source aggregates. Cross-context propagation dùng durable Events, read contracts, idempotent consumers và reconciliation. Không dùng distributed transaction xuyên Contexts.

---
# 3. Ranh giới sở hữu dữ liệu

## 3.1. Analytics Context sở hữu

- Analytics Data Source Registry và Dataset Definition/Version.
- Projection metadata, offsets, rebuild/reconciliation state và lineage.
- Semantic Metric, Metric Version, formula metadata, dimensions, dependencies, validation và certification.
- KPI Definition, Target, Scorecard và analytical status.
- Dashboard, Version, Widget, Filter, Layout, sharing metadata và personal preferences.
- Report Definition, Version, Run, Subscription và delivery intent.
- Analytics Snapshot, Version, Item, Lock và Restatement.
- Forecast Model/Version, Run, Item, Override, Lock, Scenario và accuracy result.
- Drill-down/Drill-through definitions và analytical access policies.
- Aggregate access, minimum-group-size và export policies.
- Data Freshness status, Data Quality tests/results và Metric Reconciliation.
- Analytics Alert và Anomaly Detection Result.
- Analytical Query/Export domain records và Audit requests.
- External BI Dataset publication metadata.
- Analytical adjustments tách biệt khỏi source business facts.

## 3.2. Analytics Context không sở hữu

- Platform configuration source: `platform`.
- User, Workforce, organization, permission hoặc authenticated scope: `iam`.
- Lead, assignment, source snapshot hoặc care protection: `lead`.
- Party/Customer identity, Requirement hoặc consent: `party`.
- Project, Asset, Listing, Availability hoặc Commercial Lock: `product`.
- Match Results hoặc Matching rules: `matching`.
- Deal, Booking, Sales Attribution hoặc transaction responsibility: `transaction`.
- Contract, Payment, Receipt, Refund hoặc Settlement: `contract`.
- Revenue, Commission, Payout hoặc Clawback: `revenue`.
- Task, Interaction, SLA Instance hoặc Timeline: `activity`.
- Campaign, operational Spend, Conversion hoặc Attribution source: `marketing`.
- Generated Report/Export binary artifact: `documents`.
- BI/warehouse/ERP/payroll/bank connection, credentials và transport: `integration`.
- Immutable Audit facts: `audit`.
- Queue, scheduler, retry/DLQ hoặc incident runtime: `operations`.
- General Ledger, statutory accounting, payroll hoặc bank truth: external systems.

## 3.3. Read-only business boundary

Dashboard, Report, Alert, Anomaly, Forecast Override hoặc Data Quality result không được trực tiếp:

- Sửa Lead status/owner.
- Sửa Customer/Party.
- Sửa Listing Availability.
- Sửa Deal stage/probability.
- Xác nhận Booking hoặc Deposit.
- Sửa Contract.
- Xác nhận Payment/Receipt.
- Ghi nhận Revenue.
- Duyệt Commission/Payout.
- Sửa Campaign source.

Hành động nghiệp vụ phải điều hướng hoặc gửi command đến owning Context, nơi permission, workflow và invariants được kiểm tra.

## 3.4. Projection, Snapshot và source truth

Projection có thể denormalize, aggregate và precompute để query nhanh nhưng phải giữ lineage.

Snapshot là analytical record được khóa theo reporting process, không phải source business state.

Reporting Adjustment hoặc Restatement chỉ thay analytical presentation có version; không sửa source facts.

## 3.5. Documents và Integration boundaries

Analytics sở hữu Report/Export job, version, scope, filters, hash và Document reference.

Documents Context sở hữu generated PDF/XLSX/CSV artifact, binary object, retention và Legal Hold.

Integration Context sở hữu external BI/warehouse delivery, credentials, connector runtime và publication transport.

## 3.6. IAM, security và analytical policy

Analytics có thể sở hữu analytical access-policy definitions như aggregate/detail/drill/export eligibility.

IAM/Security sources vẫn quyết định authenticated principal, effective roles, scopes, grants, delegation và masking authorities.

Analytics không tạo permission universe song song hoặc tin scope do frontend gửi.

## 3.7. Audit boundary

Analytics ghi operational query/export records phục vụ product behavior.

Audit Context sở hữu immutable Audit facts cho sensitive query, export, Metric certification, Snapshot lock, Forecast approval và access-policy change.

---
# 4. Nguyên tắc “không tạo nguồn chân lý thứ hai”

## 4.1. Projection không phải nguồn chân lý

Analytics Projection có thể chứa:

* Bản sao trường cần thiết.
* Dữ liệu denormalized.
* Aggregate.
* Precomputed metric.
* Search index.
* Snapshot.

Nhưng mọi projection phải có:

* Source Context.
* Source resource ID.
* Source event.
* Source version.
* Extracted at.
* Effective at.
* Projection version.
* Lineage.

## 4.2. Không sửa dữ liệu nguồn tại projection

Khi dữ liệu sai:

```text id="m13-source-correction"
Analytics phát hiện sai
→ Tạo Data Quality/Reconciliation Case
→ Gửi Source Correction Request
→ Owning Context xử lý
→ Domain Event mới
→ Projection được cập nhật
```

Không cho analyst sửa số trực tiếp trong projection persistence để “khớp báo cáo”.

## 4.3. Manual analytical adjustment phải tách biệt

Nếu cần điều chỉnh báo cáo quản trị:

* Tạo Reporting Adjustment.
* Có reason.
* Có scope.
* Có amount/count delta.
* Có effective period.
* Có approval.
* Không sửa source.
* Báo cáo phải ghi “Adjusted/Restated”.

## 4.4. Drill-through phải quay về owning Context

Từ một Contract metric, user phải được chuyển đến Contract API/Workspace Contract and Cash Capability, không mở một Contract bản sao có thể chỉnh sửa trong Analytics Capability.

---

# 5. Kiến trúc dữ liệu phân tích

Analytics Capability có thể triển khai theo bốn tầng:

## 5.1. Source Layer

Dữ liệu từ owning Contexts.

## 5.2. Projection Layer

Các read model tối ưu cho query:

* Lead analytics fact.
* Customer activity fact.
* Inventory snapshot fact.
* Deal pipeline fact.
* Contract fact.
* Receivable fact.
* Revenue fact.
* Commission fact.
* Marketing fact.
* Activity fact.

## 5.3. Semantic Layer

Định nghĩa metric, dimension, filter, time logic và access.

## 5.4. Presentation Layer

Dashboard, Report, Scorecard, Alert, Forecast và Export.

---

# 6. Candidate ingestion modes — architecture input, pending validation

Có thể sử dụng:

```text id="m13-ingestion-modes"
DOMAIN_EVENT
OUTBOX_EVENT
CHANGE_DATA_CAPTURE
SCHEDULED_INCREMENTAL_EXTRACT
FULL_REBUILD
MATERIALIZED_VIEW_REFRESH
EXTERNAL_DATA_IMPORT
MANUAL_APPROVED_SNAPSHOT
```

## 6.1. Domain Event

Ưu tiên cho near-real-time update.

## 6.2. CDC

Có thể dùng cho warehouse hoặc projection ngoài transaction database.

## 6.3. Incremental Extract

Dùng khi owning Context chưa phát đủ event.

## 6.4. Full Rebuild

Dùng để:

* Khôi phục projection.
* Kiểm tra reconciliation.
* Approved projection backfill hoặc schema transition.
* Metric backfill.

Full rebuild không được làm mất hoặc ghi đè Snapshot đã khóa.

---

# 7. Event Time và Processing Time

Phải tách:

* `occurred_at`: sự kiện nghiệp vụ thực tế.
* `recorded_at`: hệ thống nguồn ghi nhận.
* `ingested_at`: analytics nhận dữ liệu.
* `processed_at`: projection xử lý.
* `available_at`: dữ liệu sẵn sàng cho query.

Điều này giúp phân biệt:

* Late-arriving data.
* Backdated event.
* Processing delay.
* Reporting cutoff.

---

# 8. Late-arriving Data

Khi sự kiện đến trễ:

* Projection hiện tại được cập nhật.
* Snapshot chưa khóa có thể refresh.
* Snapshot đã khóa không bị ghi đè.
* Có thể tạo Restatement.
* Forecast accuracy phải ghi nhận dữ liệu đã biết tại thời điểm dự báo.

---

# 9. Candidate Dataset vocabulary — pending validation

Dataset là cấu trúc dữ liệu phục vụ một nhóm phân tích.

Ví dụ:

```text id="m13-dataset-types"
LEAD_FUNNEL
CUSTOMER_360_ANALYTICS
INVENTORY_ANALYTICS
MATCHING_ANALYTICS
DEAL_PIPELINE
BOOKING_ANALYTICS
CONTRACT_ANALYTICS
RECEIVABLE_ANALYTICS
CASH_COLLECTION_ANALYTICS
REVENUE_ANALYTICS
COMMISSION_ANALYTICS
ACTIVITY_ANALYTICS
SLA_ANALYTICS
MARKETING_ANALYTICS
ORGANIZATION_ANALYTICS
DATA_QUALITY_ANALYTICS
```

---

# 10. Dataset Version

Dataset Version phải lưu:

* Schema.
* Source mappings.
* Join logic.
* Grain.
* Primary keys.
* Time fields.
* Dimensions.
* Measures.
* Effective dates.
* Build method.
* Retention.
* Access policy.
* Version.

Dataset Version active không sửa trực tiếp.

---

# 11. Grain

Mỗi Dataset phải công bố grain rõ ràng.

Ví dụ:

```text id="m13-grain-examples"
Một dòng trên Lead
Một dòng trên Lead Assignment Period
Một dòng trên Customer
Một dòng trên Listing tại một ngày
Một dòng trên Deal Snapshot Date
Một dòng trên Contract
Một dòng trên Receivable
Một dòng trên Payment Allocation
Một dòng trên Revenue Entitlement
Một dòng trên Commission Entitlement
Một dòng trên Campaign-Date-Channel
```

Không được join các Dataset khác grain mà không có aggregation rule rõ.

---

# 12. Fact và Dimension

## 12.1. Fact

* Lead event.
* Deal stage event.
* Payment.
* Revenue.
* Commission.
* Interaction.
* Marketing spend.
* Conversion.

## 12.2. Dimension

* Date.
* User.
* Team.
* Department.
* Branch.
* Legal Entity.
* Project.
* Campaign.
* Customer Segment.
* Lead Source.
* Transaction Model.
* Listing.
* Contract Type.

## 12.3. Slowly Changing Dimension

Các dimension thay đổi theo thời gian phải hỗ trợ:

* Current view.
* As-of-event view.
* As-of-snapshot view.

Ví dụ sale chuyển Team không được viết lại Team của Contract lịch sử nếu báo cáo yêu cầu organization snapshot tại thời điểm Contract.

---

# 13. Semantic Metric

Semantic Metric là định nghĩa duy nhất, có version, dùng chung cho Dashboard, Report và API.

Một Metric phải có:

* Metric code.
* Business name.
* Technical name.
* Description.
* Owner.
* Steward.
* Domain.
* Metric type.
* Dataset.
* Grain.
* Formula.
* Numerator.
* Denominator.
* Filters.
* Dimensions.
* Time field.
* Time grain.
* Currency behavior.
* Null behavior.
* Deduplication.
* Scope policy.
* Effective dates.
* Version.
* Certification status.
* Lineage.
* Examples.

---

# 14. Candidate Metric Type vocabulary — pending validation

```text id="m13-metric-types"
COUNT
DISTINCT_COUNT
SUM
AVERAGE
MEDIAN
MINIMUM
MAXIMUM
RATIO
PERCENTAGE
RATE
DURATION
BALANCE
FLOW
SNAPSHOT
CUMULATIVE
MOVING_AVERAGE
CONVERSION
RETENTION
COHORT
INDEX
SCORE
FORECAST
VARIANCE
CUSTOM
```

---

# 15. Candidate Metric lifecycle — pending validation

```text id="m13-metric-status"
DRAFT
IN_DEVELOPMENT
PENDING_VALIDATION
PENDING_REVIEW
PENDING_APPROVAL
CERTIFIED
DEPRECATED
REPLACED
SUSPENDED
ARCHIVED
```

Chỉ Metric `CERTIFIED` được dùng mặc định trong Executive Dashboard.

---

# 16. Metric Certification

Certification phải xác nhận:

* Business definition.
* Formula.
* Dataset grain.
* Source lineage.
* Access policy.
* Data quality.
* Reconciliation.
* Performance.
* Sample validation.
* Edge cases.
* Owner.
* Effective dates.

---

# 17. Metric Versioning

Metric đang Certified không được sửa trực tiếp.

Thay đổi phải tạo Version mới khi:

* Formula thay đổi.
* Filter thay đổi.
* Source thay đổi.
* Time logic thay đổi.
* Currency logic thay đổi.
* Deduplication thay đổi.
* Attribution model thay đổi.
* Business meaning thay đổi.

---

# 18. Metric change classification

Phân loại thay đổi:

```text id="m13-metric-change"
PATCH
MINOR
MAJOR
```

## 18.1. Patch

Sửa mô tả hoặc metadata không đổi kết quả.

## 18.2. Minor

Bổ sung dimension hoặc tối ưu source nhưng kết quả giữ trong tolerance.

## 18.3. Major

Thay formula hoặc ý nghĩa.

Major Version phải:

* Có effective date.
* Có consumer-impact và transition note.
* Có dashboard impact analysis.
* Không âm thầm thay lịch sử.

---

# 19. Metric Alias và Deprecated Metric

Khi đổi Metric:

* Metric cũ có thể Deprecated.
* Alias có thể redirect query mới.
* Dashboard lịch sử vẫn giữ Metric Version cũ.
* User được cảnh báo metric đã Deprecated.

---

# 20. Metric Dependency Graph

Metric có thể phụ thuộc metric khác.

Ví dụ:

```text id="m13-metric-dependency"
Lead-to-Contract Conversion
=
Valid Contracts
/
Valid Leads
```

Dependency Graph phải:

* Phát hiện cycle.
* Hiển thị upstream/downstream.
* Tính impact khi Metric thay đổi.
* Hỗ trợ lineage.

---

# 21. Metric Formula Engine

Formula Engine phải hỗ trợ:

* Arithmetic.
* Aggregation.
* Conditional logic.
* Date difference.
* Window functions được kiểm soát.
* Currency conversion reference.
* Safe division.
* Null handling.
* Percentile.
* Cohort.
* Moving window.

Không cho chạy mã tùy ý.

---

# 22. Safe Division

Metric ratio phải định nghĩa khi denominator bằng 0:

```text id="m13-zero-denominator"
RETURN_NULL
RETURN_ZERO
RETURN_NOT_APPLICABLE
RAISE_DATA_QUALITY_WARNING
```

Không tự trả 0 nếu có thể gây hiểu nhầm.

---

# 23. Null và Unknown

Phải phân biệt:

* `NULL`: không có dữ liệu.
* `UNKNOWN`: chưa xác định.
* `NOT_APPLICABLE`: không áp dụng.
* `ZERO`: giá trị bằng 0.

Dashboard không được hiển thị tất cả thành 0.

---

# 24. Currency

Metric tiền phải xác định:

* Transaction currency.
* Reporting currency.
* Exchange rate source.
* Rate date.
* Conversion method.
* Rounding.
* Original amount.
* Converted amount.

Không cộng nhiều currency trực tiếp.

---

# 25. Candidate Currency Conversion modes — pending validation

```text id="m13-fx-modes"
NO_CONVERSION
TRANSACTION_DATE_RATE
RECOGNITION_DATE_RATE
PAYMENT_DATE_RATE
SNAPSHOT_DATE_RATE
PERIOD_AVERAGE_RATE
PERIOD_END_RATE
APPROVED_CUSTOM_RATE
```

Analytics Capability lưu reference, không thay ERP FX accounting.

---

# 26. Time Dimension

Metric phải xác định ngày nào được dùng:

* Lead created date.
* Lead assigned date.
* Deal created date.
* Booking date.
* Contract signed date.
* Contract effective date.
* Payment date.
* Revenue recognition date.
* Revenue collection date.
* Commission payable date.
* Campaign spend date.

Không dùng một trường `created_at` cho mọi báo cáo.

---

# 27. Time Zone

Query phải xác định:

* User timezone.
* Enterprise timezone.
* Legal Entity timezone.
* Project timezone.
* UTC.

Executive reporting mặc định theo Enterprise hoặc Legal Entity policy.

---

# 28. Reporting Calendar

Hỗ trợ:

* Calendar month.
* Calendar quarter.
* Fiscal month.
* Fiscal quarter.
* Sales period.
* Marketing period.
* Project launch period.
* Custom reporting period.

Reporting Calendar phải version.

---

# 29. Business Calendar và Reporting Calendar

Business Calendar dùng tính SLA/ngày làm việc.

Reporting Calendar dùng nhóm kỳ báo cáo.

Hai loại không được đồng nhất.

---

# 30. Candidate certified Metric catalog — Lead

Các Metric bắt buộc:

```text id="m13-lead-metrics"
LEADS_CREATED
VALID_LEADS
INVALID_LEADS
SPAM_LEADS
DUPLICATE_LEADS
UNASSIGNED_LEADS
ASSIGNED_LEADS
ACCEPTED_LEADS
REJECTED_LEADS
CONTACTED_LEADS
MEANINGFULLY_CONTACTED_LEADS
QUALIFIED_LEADS
NURTURE_LEADS
CLOSED_LOST_LEADS
CONVERTED_LEADS
FIRST_RESPONSE_WITHIN_SLA
FIRST_RESPONSE_BREACH
LEAD_ACCEPTANCE_RATE
LEAD_CONTACT_RATE
LEAD_QUALIFICATION_RATE
LEAD_CONVERSION_RATE
```

---

# 31. Định nghĩa Valid Lead

Một Lead được tính `VALID_LEAD` khi:

* Không phải spam confirmed.
* Không phải test.
* Không phải invalid.
* Có identity/contact đủ theo policy.
* Không bị loại khỏi báo cáo vì duplicate source record.

Duplicate Lead có thể vẫn đại diện một nhu cầu mới nhưng phải theo Lead Management Capability rule.

Metric Version phải nêu cách xử lý.

---

# 32. Lead Conversion Rate

Có thể có nhiều biến thể:

```text id="m13-lead-conversion-variants"
Lead → Qualified Lead
Lead → Appointment
Lead → Deal
Lead → Booking
Lead → Contract
Lead → Revenue
```

Không dùng một metric tên chung `conversion_rate` không có stage.

---

# 33. Candidate certified Metric catalog — Customer

```text id="m13-customer-metrics"
CUSTOMERS_CREATED
ACTIVE_CUSTOMERS
CUSTOMERS_WITH_ACTIVE_REQUIREMENT
CUSTOMERS_WITH_ACTIVE_DEAL
CUSTOMERS_WITH_CONTRACT
BUYER_CUSTOMERS
SELLER_CUSTOMERS
OWNER_CUSTOMERS
MULTI_ROLE_CUSTOMERS
CUSTOMER_DUPLICATE_CASES
CUSTOMER_MERGES
SHARED_PHONE_CASES
CUSTOMER_DATA_COMPLETENESS
CUSTOMER_CONTACTABLE_RATE
```

---

# 34. Active Customer

Phải định nghĩa theo policy, ví dụ:

* Có Lead/Requirement/Deal/Contract hoạt động.
* Có Interaction trong N ngày.
* Không Archived.
* Không chỉ dựa trên `updated_at`.

Có thể có các Metric riêng:

* Operational Active Customer.
* Marketing Active Customer.
* Commercial Active Customer.

---

# 35. Candidate certified Metric catalog — Requirement và Matching

```text id="m13-requirement-metrics"
ACTIVE_REQUIREMENTS
COMPLETE_REQUIREMENTS
REQUIREMENT_COMPLETENESS_RATE
MATCHING_RUNS
MATCH_RESULTS
HIGH_FIT_MATCHES
SHORTLISTS_CREATED
SHORTLIST_ACCEPTANCE_RATE
MATCH_TO_APPOINTMENT_RATE
MATCH_TO_DEAL_RATE
STALE_MATCH_RESULTS
```

---

# 36. Candidate certified Metric catalog — Inventory

```text id="m13-inventory-metrics"
TOTAL_ASSETS
TOTAL_LISTINGS
ACTIVE_LISTINGS
AVAILABLE_LISTINGS
HELD_LISTINGS
BOOKED_LISTINGS
CONTRACTED_LISTINGS
SOLD_LISTINGS
BLOCKED_LISTINGS
EXPIRED_LISTINGS
LISTING_VALUE
AVAILABLE_INVENTORY_VALUE
INVENTORY_ABSORPTION_RATE
AVERAGE_DAYS_ON_MARKET
LISTING_AVAILABILITY_CONFLICTS
DOUBLE_SELL_RISK_COUNT
```

---

# 37. Available Listing

Phải sử dụng trạng thái và rule Product, Asset, Listing and Inventory Capability:

* Listing active.
* Within effective dates.
* Không có Commercial Lock xung đột.
* Không Sold/Contracted.
* Mandate còn hiệu lực.
* Legal/operational readiness phù hợp.

Không chỉ dựa trên một boolean `available=true`.

---

# 38. Inventory Absorption Rate

Ví dụ:

```text id="m13-absorption"
Net Sold Units in Period
/
Available Units at Period Start + New Units Added
```

Phải nêu rõ:

* Gross hay Net Sold.
* Cancellation treatment.
* Start inventory.
* New supply.
* Period.

---

# 39. Candidate certified Metric catalog — Deal Pipeline

```text id="m13-deal-metrics"
OPEN_DEALS
DEALS_CREATED
DEALS_WON
DEALS_LOST
DEAL_PIPELINE_VALUE
WEIGHTED_PIPELINE_VALUE
DEAL_STAGE_CONVERSION
AVERAGE_DEAL_AGE
AVERAGE_SALES_CYCLE
DEALS_WITHOUT_NEXT_ACTION
STALE_DEALS
PROPOSALS_SENT
PROPOSAL_ACCEPTANCE_RATE
NEGOTIATION_SUCCESS_RATE
HOLDS_ACTIVE
HOLDS_EXPIRING
BOOKINGS_CREATED
BOOKINGS_ACTIVE
BOOKINGS_CANCELLED
DEPOSITS_CONFIRMED
BOOKING_TO_CONTRACT_RATE
```

---

# 40. Pipeline Value

Phải tách:

```text id="m13-pipeline-value-types"
GROSS_PIPELINE_VALUE
ELIGIBLE_PIPELINE_VALUE
WEIGHTED_PIPELINE_VALUE
COMMITTED_PIPELINE_VALUE
BEST_CASE_PIPELINE_VALUE
```

Không gọi tất cả là “Doanh số”.

---

# 41. Weighted Pipeline

```text id="m13-weighted-pipeline"
Weighted Pipeline
=
Σ Eligible Deal Value × Stage Probability
```

Stage Probability phải:

* Có version.
* Có effective dates.
* Có thể theo Project/Transaction Model.
* Không sửa lịch sử Forecast đã khóa.

---

# 42. Deal Stage Conversion

Phải dựa trên stage entry/exit events, không chỉ trạng thái hiện tại.

Ví dụ:

* Qualified → Proposal.
* Proposal → Negotiation.
* Negotiation → Booking.
* Booking → Contract.

---

# 43. Candidate certified Metric catalog — Contract

```text id="m13-contract-metrics"
CONTRACTS_CREATED
CONTRACTS_APPROVED
CONTRACTS_SIGNED
CONTRACTS_EFFECTIVE
CONTRACTS_COMPLETED
CONTRACTS_CANCELLED
CONTRACTS_TERMINATED
GROSS_CONTRACT_VALUE
NET_CONTRACT_VALUE
EFFECTIVE_CONTRACT_VALUE
CANCELLED_CONTRACT_VALUE
NET_ACTIVE_CONTRACT_VALUE
AVERAGE_CONTRACT_VALUE
BOOKING_TO_CONTRACT_RATE
CONTRACT_CANCELLATION_RATE
CONTRACT_CYCLE_TIME
```

---

# 44. Contract Value

Phải tách:

* Gross Contract Value.
* Net Property Value.
* Amount Payable.
* Effective Contract Value.
* Cancelled Contract Value.
* Adjusted Contract Value.

Không đồng nhất Contract Value với Revenue.

---

# 45. Candidate certified Metric catalog — Payment và Receivable

```text id="m13-payment-metrics"
BUYER_RECEIVABLE_AMOUNT
BUYER_PAID_AMOUNT
BUYER_OUTSTANDING_AMOUNT
BUYER_OVERDUE_AMOUNT
PAYMENT_COLLECTION_RATE
PAYMENTS_RECEIVED
PAYMENTS_UNIDENTIFIED
PAYMENTS_UNALLOCATED
RECEIPTS_ISSUED
RECEIPTS_CANCELLED
REFUND_REQUESTED_AMOUNT
REFUND_PAID_AMOUNT
OWNER_SETTLEMENT_PAYABLE
OWNER_SETTLEMENT_PAID
```

---

# 46. Collection Rate

Có thể định nghĩa:

```text id="m13-collection-rate"
Paid Amount
/
Activated Receivable Amount
```

Hoặc:

```text id="m13-due-collection-rate"
Paid Amount for Due Receivables
/
Due Receivable Amount
```

Hai metric phải có mã riêng.

---

# 47. Candidate certified Metric catalog — Revenue

```text id="m13-revenue-metrics"
REVENUE_ENTITLEMENT_AMOUNT
REVENUE_RECOGNIZED_AMOUNT
REVENUE_RECEIVABLE_AMOUNT
REVENUE_COLLECTED_AMOUNT
REVENUE_OUTSTANDING_AMOUNT
REVENUE_OVERDUE_AMOUNT
REVENUE_HOLDBACK_AMOUNT
REVENUE_ADJUSTMENT_AMOUNT
REVENUE_REVERSAL_AMOUNT
NET_RECOGNIZED_REVENUE
NET_COLLECTED_REVENUE
REVENUE_COLLECTION_RATE
```

---

# 48. Revenue không đồng nghĩa tiền nhận

Dashboard phải hiển thị riêng:

* Gross funds received.
* Buyer payments.
* Collected-on-behalf funds.
* Revenue Collected.
* Owner proceeds.
* Developer proceeds.
* Brokerage fee.
* Service fee.

---

# 49. Net Recognized Revenue

Ví dụ:

```text id="m13-net-recognized-revenue"
Recognized Revenue
+ Positive Adjustments
− Recognition Reversals
```

Phải dựa trên Revenue and Commission Capability.

---

# 50. Candidate certified Metric catalog — Commission

```text id="m13-commission-metrics"
COMMISSION_ENTITLEMENT_AMOUNT
COMMISSION_RECOGNIZED_AMOUNT
COMMISSION_VESTED_AMOUNT
COMMISSION_PAYABLE_AMOUNT
COMMISSION_PAID_AMOUNT
COMMISSION_HOLDBACK_AMOUNT
COMMISSION_CLAWBACK_AMOUNT
COMMISSION_NEGATIVE_BALANCE
COMMISSION_PAYOUT_RATE
COMMISSION_TO_REVENUE_RATIO
```

---

# 51. Commission-to-Revenue Ratio

Phải xác định denominator:

* Recognized Revenue.
* Collected Revenue.
* Revenue Entitlement.

Không dùng Contract Value trừ khi metric được đặt tên rõ là Commission-to-Contract-Value.

---

# 52. Candidate certified Metric catalog — Activity và SLA

```text id="m13-activity-metrics"
TASKS_CREATED
TASKS_COMPLETED
TASKS_OVERDUE
TASK_COMPLETION_RATE
AVERAGE_TASK_COMPLETION_TIME
APPOINTMENTS_CREATED
APPOINTMENTS_CONFIRMED
APPOINTMENTS_COMPLETED
APPOINTMENT_NO_SHOW_RATE
CALLS_ATTEMPTED
CALLS_CONNECTED
CALL_CONNECT_RATE
MEANINGFUL_INTERACTIONS
FIRST_RESPONSE_TIME
SLA_INSTANCES
SLA_COMPLETED_WITHIN
SLA_BREACHED
SLA_COMPLIANCE_RATE
NBA_GENERATED
NBA_ACCEPTED
NBA_EXECUTED
NBA_COMPLETED
```

---

# 53. Meaningful Interaction

Không phải mọi message/call đều meaningful.

Definition có thể dựa trên:

* Call connected meaningful disposition.
* Customer reply.
* Meeting attended.
* Interaction outcome.
* User confirmation.

Metric phải version.

---

# 54. Candidate certified Metric catalog — Marketing

```text id="m13-marketing-metrics"
MARKETING_SPEND
IMPRESSIONS
REACH
CLICKS
VALID_LEADS_BY_CAMPAIGN
QUALIFIED_LEADS_BY_CAMPAIGN
MARKETING_SOURCED_DEALS
MARKETING_INFLUENCED_DEALS
MARKETING_SOURCED_CONTRACTS
MARKETING_INFLUENCED_CONTRACTS
ATTRIBUTED_CONTRACT_VALUE
ATTRIBUTED_RECOGNIZED_REVENUE
ATTRIBUTED_COLLECTED_REVENUE
CPL
CPQL
COST_PER_DEAL
COST_PER_BOOKING
COST_PER_CONTRACT
CAC
ROAS_CONTRACT_VALUE
ROAS_RECOGNIZED_REVENUE
ROAS_COLLECTED_REVENUE
ROMI_RECOGNIZED_REVENUE
ROMI_COLLECTED_REVENUE
```

---

# 55. Metric Naming Standard

Metric code phải:

* Có domain prefix.
* Có stage/basis.
* Không mơ hồ.
* Không dùng từ “Revenue” cho Contract Value.
* Không dùng “Sales” nếu không rõ là Contract, Revenue hay Collected Cash.

Ví dụ tốt:

```text id="m13-good-metric-codes"
sales.contract.effective_value
finance.buyer_receivable.overdue_amount
revenue.recognized.net_amount
commission.payable.amount
marketing.romi.collected_revenue
```

---

# 56. KPI

KPI là Metric được gắn:

* Target.
* Owner.
* Period.
* Scope.
* Direction.
* Threshold.
* Weight.
* Score.
* Status.

Không phải mọi Metric đều là KPI.

---

# 57. Candidate KPI Direction vocabulary — pending validation

```text id="m13-kpi-direction"
HIGHER_IS_BETTER
LOWER_IS_BETTER
TARGET_RANGE
EXACT_TARGET
BINARY
CUSTOM
```

---

# 58. Candidate KPI lifecycle — pending validation

```text id="m13-kpi-status"
NOT_STARTED
ON_TRACK
AT_RISK
OFF_TRACK
ACHIEVED
EXCEEDED
MISSED
NOT_APPLICABLE
DATA_UNAVAILABLE
```

---

# 59. KPI Target

Target có thể theo:

* Enterprise.
* Legal Entity.
* Branch.
* Department.
* Team.
* User.
* Project.
* Campaign.
* Period.

Target phải có:

* Metric Version.
* Target value.
* Currency/unit.
* Effective period.
* Approval.
* Stretch target nếu có.
* Minimum/maximum.
* Owner.

---

# 60. Target Versioning

Target đã approved không sửa trực tiếp.

Thay đổi phải tạo:

* Revised Target.
* Reason.
* Approval.
* Effective date.
* Original target giữ lịch sử.

---

# 61. KPI Score

Có thể tính:

```text id="m13-kpi-score"
Actual / Target × Weight
```

Hoặc custom rule.

Score phải cap/floor theo policy.

Không sử dụng KPI Score để tự động kỷ luật nhân sự nếu dữ liệu chưa được kiểm chứng.

---

# 62. KPI Scorecard

Scorecard có thể theo:

* User.
* Team.
* Department.
* Branch.
* Project.
* Legal Entity.
* Enterprise.

Scorecard gồm:

* KPI.
* Target.
* Actual.
* Forecast.
* Variance.
* Trend.
* Status.
* Weight.
* Data freshness.
* Comment.
* Action plan.

---

# 63. Dashboard

Dashboard là tập hợp Widget dùng Metric và Dataset có version.

Dashboard phải có:

* Dashboard code.
* Name.
* Audience.
* Owner.
* Domain.
* Default scope.
* Filters.
* Layout.
* Refresh policy.
* Version.
* Status.
* Access policy.

---

# 64. Candidate Dashboard Type vocabulary — pending validation

```text id="m13-dashboard-types"
EXECUTIVE
OPERATING_REVIEW
SALES
MARKETING
CUSTOMER
INVENTORY
DEAL_PIPELINE
CONTRACT
FINANCE_OPERATIONS
REVENUE
COMMISSION
ACTIVITY
SLA
DATA_QUALITY
PROJECT
LEGAL_ENTITY
PERSONAL
CUSTOM
```

---

# 65. Candidate Dashboard lifecycle — pending validation

```text id="m13-dashboard-status"
DRAFT
PENDING_REVIEW
PENDING_APPROVAL
PUBLISHED
SUSPENDED
DEPRECATED
REPLACED
ARCHIVED
```

Published Version không sửa trực tiếp.

---

# 66. Candidate Widget vocabulary — pending validation

Widget có thể là:

```text id="m13-widget-types"
KPI_CARD
NUMBER
TREND
LINE_CHART
BAR_CHART
STACKED_BAR
AREA_CHART
FUNNEL
PIPELINE
TABLE
PIVOT
HEATMAP
COHORT
WATERFALL
SCATTER
GAUGE
MAP
TIMELINE
FORECAST_CHART
VARIANCE_CHART
TEXT
ALERT_LIST
DRILLDOWN_TABLE
```

---

# 67. Widget Definition

Mỗi Widget phải có:

* Metric Version.
* Dataset Version.
* Dimensions.
* Filters.
* Time range.
* Comparison period.
* Scope.
* Sort.
* Limit.
* Visualization.
* Empty-state behavior.
* Data freshness display.
* Drill-down definition.
* Export policy.

---

# 68. Dashboard Global Filter

Có thể gồm:

* Date range.
* Legal Entity.
* Branch.
* Department.
* Team.
* User.
* Project.
* Campaign.
* Transaction Model.
* Lead Source.
* Contract Status.
* Revenue Model.
* Currency.

Filter không được mở rộng scope ngoài quyền user.

---

# 69. Filter Intersection

Query thực tế phải là:

```text id="m13-filter-intersection"
User Authorized Scope
∩ Dashboard Scope
∩ Widget Scope
∩ User-selected Filters
∩ Metric Access Policy
```

User filter chỉ được thu hẹp, không được mở rộng.

---

# 70. Default Scope

Dashboard không được mặc định `all`.

Ví dụ:

* Sale: `mine`.
* Team Lead: `team`.
* Department Head: `department`.
* Legal Entity Director: `legal_entity`.
* Enterprise Director: `all` nếu có quyền.

---

# 71. Personal Dashboard

User có thể tùy biến:

* Layout.
* Widget visibility.
* Saved filters.
* Favorite reports.

Không được:

* Tạo Metric tùy ý không kiểm soát.
* Mở scope.
* Bỏ field masking.
* Chia sẻ Dashboard vượt quyền.

---

# 72. Dashboard Sharing

Có thể chia sẻ với:

* User.
* Role.
* Team.
* Department.
* Legal Entity.
* Project.
* Public nội bộ có kiểm soát.

Share chỉ chia Dashboard definition, không cấp quyền dữ liệu.

---

# 73. Dashboard Embedding

Nếu embed vào portal hoặc màn hình capability:

* Phải dùng authenticated context.
* Có short-lived token.
* Scope-bound.
* Không chứa raw credentials.
* Audit.
* Không dùng public URL cho dữ liệu nhạy cảm.

---

# 74. Drill-down

Drill-down cho phép đi từ metric tổng hợp xuống cấp dimension thấp hơn.

Ví dụ:

```text id="m13-drilldown-example"
Revenue toàn Enterprise
→ Legal Entity
→ Project
→ Department
→ Team
→ Sale
→ Contract
```

---

# 75. Drill-through

Drill-through mở danh sách hoặc resource cụ thể từ owning Context.

Ví dụ:

* Overdue Receivable → danh sách Receivable Contract and Cash Capability.
* Contract Value → Contract Workspace.
* Revenue Recognized → Revenue Entitlement Revenue and Commission Capability.
* Lead SLA Breach → Lead List Lead Management Capability.
* Available Listing → Listing Product, Asset, Listing and Inventory Capability.

---

# 76. Drill-down Definition

Phải có:

* Source Metric.
* Allowed dimensions.
* Hierarchy.
* Target Dataset.
* Target API.
* Scope mapping.
* Field mapping.
* Maximum rows.
* Sensitive fields.
* Export rule.

---

# 77. Drill-down Scope

Drill-down phải enforce backend.

Ví dụ Team Lead mở Department metric từ URL:

* Backend vẫn giới hạn Team.
* Không tin `department_id` từ frontend.
* Không dùng owner/sale ID do client cung cấp để mở rộng scope.

---

# 78. Aggregate View không đồng nghĩa Detail View

User có thể được xem:

* Tổng số Contract của Legal Entity.

Nhưng không được xem:

* Danh sách Customer.
* Contract documents.
* Bank details.

Aggregate Access phải được định nghĩa riêng.

---

# 79. K-anonymity/Minimum Group Size

Với một số dữ liệu nhạy cảm, aggregate chỉ hiển thị khi nhóm đủ lớn.

Ví dụ:

* Commission trung bình.
* Financial Profile segment.
* Customer demographic analysis.

Nếu group nhỏ hơn threshold:

* Ẩn.
* Gộp “Other”.
* Hiển thị `Insufficient data`.

---

# 80. Row-Level Security

Dựa trên:

* User.
* Role.
* Organization.
* Legal Entity.
* Project Access.
* Resource relationship.
* Time-bound grants.
* Share Grant.
* Delegation.

Analytics query authorization phải resolve từ IAM/Security sources; implementation có thể dùng RLS hoặc policy-enforced query layer.

---

# 81. Field-Level Security

Các field nhạy cảm:

* Customer phone/email.
* Identity.
* Financial Profile.
* Bank information.
* Floor Price.
* Internal cost.
* Revenue Arrangement rate.
* Commission rate.
* Commission beneficiary.
* Contract private terms.
* Call transcript.

Phải hỗ trợ:

* Hidden.
* Masked.
* Aggregated only.
* Detail view.
* Export denied.

---

# 82. Metric-Level Access

Có thể cấp quyền:

* View metric.
* View aggregate.
* View breakdown.
* Drill-through.
* Export.
* View formula.
* View lineage.
* View sensitive components.

Ví dụ Sale xem `commission.payable.self`, nhưng không xem Commission Plan rate của người khác.

---

# 83. Dimension-Level Access

User có thể xem Metric nhưng không được group theo một dimension nhạy cảm.

Ví dụ:

* Marketing xem Revenue theo Campaign.
* Không xem Revenue theo individual sale nếu không được phép.

---

# 84. Time-Level Access

Có thể hạn chế:

* Chỉ kỳ hiện tại.
* N tháng gần nhất.
* Không xem dữ liệu trước ngày user gia nhập.
* Chỉ dữ liệu trong assignment period.
* Auditor có historical scope riêng.

---

# 85. Analytical Access Policy

Policy phải xác định:

* Dataset.
* Metric.
* Dimension.
* Aggregate/detail.
* Scope.
* Fields.
* Export.
* Time period.
* Minimum group size.
* Effective dates.

---

# 86. Access Explanation

Mỗi Dashboard/Metric/Drill-down có thể trả:

* Vì sao user thấy.
* Scope nào áp dụng.
* Filter nào được backend thêm.
* Field nào bị mask.
* Vì sao không drill-through được.
* Vì sao export bị chặn.

---

# 87. Export

Export có thể gồm:

* CSV.
* XLSX.
* PDF.
* Scheduled report.
* BI extract.
* API response.

Export phải là capability riêng.

---

# 88. Export Policy

Phải xác định:

* Dataset.
* Metric.
* Maximum rows.
* Fields.
* Masking.
* Aggregation.
* Reason required.
* Approval.
* Expiry.
* Watermark.
* Encryption.
* Download limit.
* Audit.
* Retention.

---

# 89. Export không mở rộng quyền

Export query phải sử dụng cùng hoặc chặt hơn:

* Row scope.
* Field masking.
* Metric scope.
* Time scope.

Không có API export riêng bỏ qua query authorization.

---

# 90. Export Watermark

File có thể chứa:

* User.
* Generated time.
* Scope.
* Confidentiality.
* Export ID.
* Expiry.
* “Internal Use Only”.

---

# 91. Scheduled Report

Report có thể chạy:

* Daily.
* Weekly.
* Monthly.
* Quarter-end.
* Custom schedule.
* After period close.
* After snapshot lock.

---

# 92. Report Subscription

Subscription gồm:

* Report Version.
* Recipient.
* Delivery channel.
* Schedule.
* Filters.
* Format.
* Data scope.
* Expiry.
* Status.

Recipient phải được re-authorize tại execution time.

---

# 93. Scheduled Report Security

Không dùng quyền của creator mãi mãi.

Mỗi lần chạy phải kiểm tra:

* Creator active.
* Recipient active.
* Current role.
* Current scope.
* Report permission.
* Export permission.
* Field masking.

---

# 94. Report Delivery

Có thể qua:

* In-app.
* Email link.
* Secure download.
* External storage.
* Approved webhook.

Không gửi file nhạy cảm trực tiếp nếu policy yêu cầu secure link.

---

# 95. Report Version

Report đã phát hành phải lưu:

* Metric Versions.
* Dataset Versions.
* Filters.
* Scope.
* Layout.
* Snapshot reference.
* Generated at.
* Data freshness.
* Hash.
* Recipient.

---

# 96. Snapshot

Snapshot là ảnh dữ liệu được cố định tại một thời điểm hoặc kỳ.

Snapshot dùng cho:

* Month-end.
* Quarter-end.
* Board report.
* Sales forecast baseline.
* Inventory opening.
* KPI scorecard.
* Revenue report.
* Commission statement comparison.

---

# 97. Candidate Snapshot Type vocabulary — pending validation

```text id="m13-snapshot-types"
POINT_IN_TIME
PERIOD_END
PERIOD_TO_DATE
MONTH_END
QUARTER_END
YEAR_END
FORECAST_BASELINE
PIPELINE_BASELINE
INVENTORY_OPENING
INVENTORY_CLOSING
KPI_SCORECARD
BOARD_REPORT
CUSTOM
```

---

# 98. Candidate Snapshot lifecycle — pending validation

```text id="m13-snapshot-status"
DRAFT
GENERATING
PENDING_VALIDATION
PENDING_REVIEW
PENDING_APPROVAL
LOCKED
RESTATED
SUPERSEDED
FAILED
ARCHIVED
```

---

# 99. Snapshot Content

Snapshot phải lưu:

* Snapshot code.
* As-of time.
* Reporting period.
* Timezone.
* Scope.
* Dataset Versions.
* Metric Versions.
* Currency policy.
* Source cutoff.
* Data freshness.
* Data quality status.
* Values.
* Dimension breakdown.
* Generated by.
* Approved by.
* Hash.

---

# 100. Snapshot Lock

Snapshot Locked không được sửa trực tiếp.

Nếu phát hiện sai:

* Tạo Restatement.
* Giữ Snapshot gốc.
* Nêu reason.
* Delta.
* Approval.
* Effective reporting period.

---

# 101. Snapshot Restatement

Restatement có thể do:

* Late-arriving Contract.
* Contract cancellation.
* Revenue reversal.
* Source correction.
* Identity merge.
* Metric bug.
* Currency correction.
* Reporting adjustment.

Phải phân biệt:

* Operational current view.
* Original reported snapshot.
* Latest restated snapshot.

---

# 102. As-of Query

Capability phải hỗ trợ:

* Current.
* As of date.
* As of snapshot.
* As originally reported.
* As restated.

Không dùng current state để giả lập lịch sử nếu thiếu history.

---

# 103. Historical State Reconstruction

Dựa trên:

* Status history.
* Versioned entities.
* Domain events.
* Effective dates.
* Assignment history.
* Organization snapshots.
* Snapshot facts.

Ví dụ Deal Pipeline ngày 31/03 phải dùng stage và value tại ngày 31/03, không dùng trạng thái Deal hiện tại.

---

# 104. Bitemporal Support

Với dữ liệu quan trọng có thể lưu:

* Valid time: dữ liệu đúng trong nghiệp vụ từ lúc nào.
* System time: hệ thống biết dữ liệu từ lúc nào.

Hỗ trợ phân tích:

* “Tại ngày 31/03, theo dữ liệu biết lúc đó”.
* “Tại ngày 31/03, theo dữ liệu đã được cập nhật đầy đủ sau này”.

---

# 105. Forecast concepts and value separation

Forecast là ước tính kết quả tương lai, không phải Actual.

Phải tách:

```text id="m13-forecast-categories"
SYSTEM_FORECAST
USER_FORECAST
MANAGER_FORECAST
COMMITTED_FORECAST
BEST_CASE_FORECAST
PIPELINE_FORECAST
REVENUE_FORECAST
CASH_COLLECTION_FORECAST
COMMISSION_PAYOUT_FORECAST
MARKETING_FORECAST
INVENTORY_FORECAST
```

---

# 106. Forecast Target

Forecast có thể dự báo:

* Lead volume.
* Qualified Lead.
* Appointment.
* Deal.
* Booking.
* Contract count.
* Contract Value.
* Revenue Entitlement.
* Recognized Revenue.
* Collected Revenue.
* Cash collection.
* Commission payout.
* Inventory absorption.
* Marketing Spend.
* Marketing conversion.

---

# 107. Forecast Horizon

* Daily.
* Weekly.
* Monthly.
* Quarterly.
* Project launch period.
* Custom horizon.

---

# 108. Candidate Forecast Model vocabulary — pending validation

Các loại:

```text id="m13-forecast-models"
RULE_BASED
WEIGHTED_PIPELINE
STAGE_PROBABILITY
HISTORICAL_CONVERSION
TIME_SERIES
COHORT_BASED
MILESTONE_BASED
CASH_SCHEDULE_BASED
MANUAL
HYBRID
EXTERNAL_MODEL_REFERENCE
```

MVP nên ưu tiên:

* Weighted Pipeline.
* Milestone-based Revenue.
* Receivable schedule.
* Historical conversion cơ bản.

---

# 109. Illustrative Pipeline Forecast — không phải production formula

Ví dụ:

```text id="m13-pipeline-forecast"
Forecast Contract Value
=
Committed Booking Value
+ Σ Open Deal Value × Stage Probability × Time Probability
```

Phải lưu:

* Deal snapshot.
* Stage probability version.
* Time probability.
* Exclusions.
* Model version.

---

# 110. Revenue Forecast

Có thể dựa trên:

* Contract effective.
* Revenue milestones.
* Revenue Arrangement.
* Partner confirmation probability.
* Revenue Receivable schedule.
* Historical payment delay.

Phải tách:

* Expected Entitlement.
* Expected Recognition.
* Expected Collection.

---

# 111. Cash Collection Forecast

Dựa trên:

* Buyer Payment Plan.
* Receivable due dates.
* Historical payment behavior.
* Overdue probability.
* Refund schedule.
* Settlement schedule.

Không đồng nghĩa Revenue Forecast.

---

# 112. Commission Payout Forecast

Dựa trên:

* Commission Entitlement.
* Recognition.
* Vesting.
* Payable policy.
* Payout calendar.
* Clawback.
* Holdback.

---

# 113. Forecast Run

Mỗi run lưu:

* Model Version.
* Run time.
* Data cutoff.
* Input Snapshot.
* Scope.
* Horizon.
* Scenario.
* Output.
* Confidence.
* Error/quality.
* Generated by.
* Status.

---

# 114. Forecast Confidence

Có thể dựa trên:

* Data completeness.
* Historical accuracy.
* Pipeline quality.
* Stage age.
* Next Action.
* Payment certainty.
* External confirmation.
* Model uncertainty.

Confidence không phải cam kết.

---

# 115. Forecast Override

Manager có thể override:

* Deal category.
* Expected close date.
* Forecast amount.
* Probability.
* Revenue timing.
* Cash timing.

Override phải có:

* Original value.
* New value.
* Reason.
* Evidence.
* User.
* Authority.
* Effective period.
* Expiry.
* Audit.

---

# 116. Forecast Hierarchy

Có thể tổng hợp:

```text id="m13-forecast-hierarchy"
Sale
→ Team
→ Department
→ Branch
→ Legal Entity
→ Enterprise
```

Manager có thể submit forecast cho scope của mình.

---

# 117. Candidate Forecast lifecycle — pending validation

Status:

```text id="m13-forecast-status"
DRAFT
CALCULATED
PENDING_REVIEW
SUBMITTED
APPROVED
LOCKED
SUPERSEDED
CANCELLED
```

---

# 118. Forecast Lock

Forecast đã dùng cho Operating Review hoặc Board Report phải được khóa.

Thay đổi sau đó tạo:

* New forecast version.
* Forecast update.
* Delta to prior forecast.

---

# 119. Forecast Accuracy

Phải đo:

* Forecast versus Actual.
* Bias.
* Absolute error.
* Percentage error.
* Accuracy by horizon.
* Accuracy by user/team/project/model.

Không dùng accuracy khi Actual chưa ổn định hoặc bị restated mà không ghi chú.

---

# 120. Forecast Bias

```text id="m13-forecast-bias"
Forecast − Actual
```

Phân tích:

* Consistent over-forecast.
* Consistent under-forecast.
* Late-stage slippage.
* Revenue collection delay.

Dùng cho coaching, không tự kết luận gian lận.

---

# 121. Candidate Scenario vocabulary — pending validation

Scenario:

```text id="m13-scenarios"
BASE
BEST_CASE
WORST_CASE
STRETCH
CONSERVATIVE
CUSTOM
```

Scenario có:

* Assumptions.
* Metric impacts.
* Scope.
* Horizon.
* Version.
* Owner.
* Approval.

---

# 122. Scenario Assumption

Ví dụ:

* Stage probability +10%.
* Contract cancellation +5%.
* Marketing Spend giảm 20%.
* Lead conversion tăng 3%.
* Partner payment delay thêm 15 ngày.
* Inventory bổ sung 100 Listing.

Scenario không sửa operational data.

---

# 123. Target versus Actual versus Forecast

Mọi Scorecard phải tách:

```text id="m13-value-types"
TARGET
ACTUAL_CURRENT
ACTUAL_SNAPSHOT
ACTUAL_RESTATED
FORECAST_SYSTEM
FORECAST_SUBMITTED
FORECAST_APPROVED
VARIANCE_TO_TARGET
VARIANCE_TO_PRIOR_PERIOD
```

---

# 124. Variance

Có thể tính:

* Actual − Target.
* Forecast − Target.
* Actual − Forecast.
* Current − Prior period.
* Restated − Original snapshot.

Phải ghi unit và direction.

---

# 125. Data Freshness

Mọi Dashboard/Widget phải hiển thị:

* Last source event time.
* Last ingestion time.
* Last successful refresh.
* Expected refresh frequency.
* Freshness status.
* Delayed sources.

---

# 126. Candidate Freshness Status vocabulary — pending validation

```text id="m13-freshness-status"
REAL_TIME
FRESH
SLIGHTLY_DELAYED
STALE
SEVERELY_STALE
UNAVAILABLE
UNKNOWN
```

---

# 127. Freshness policy inputs — không phải production SLO contract

Ví dụ:

* Lead: dưới 5 phút.
* Payment: dưới 5 phút.
* Revenue: dưới 15 phút.
* Marketing Spend: 24 giờ.
* Snapshot: theo kỳ.

Freshness SLA phải theo Dataset.

---

# 128. Dashboard Stale Behavior

Khi dữ liệu stale:

* Hiển thị cảnh báo.
* Không che giấu last refresh.
* Có thể disable export.
* Không tự hiển thị số cũ như real-time.
* Executive Dashboard có thể đánh dấu source bị lỗi.

---

# 129. Data Quality

Data Quality gồm:

* Completeness.
* Validity.
* Uniqueness.
* Consistency.
* Timeliness.
* Referential integrity.
* Reconciliation.
* Distribution anomaly.

---

# 130. Data Quality Test

Ví dụ:

```text id="m13-dq-tests"
Lead phải có Enterprise
Contract phải có Transaction Case hoặc approved source
Receipt issued phải có Payment
Revenue Recognition không vượt Entitlement
Commission Paid không vượt Payable
Available Listing không có active Contract Lock
Attribution credit tổng bằng 100%
Metric numerator không vượt logical maximum
Projection count khớp source count trong tolerance
```

---

# 131. Candidate Data Quality Severity vocabulary — pending validation

```text id="m13-dq-severity"
INFO
WARNING
HIGH
CRITICAL
```

---

# 132. Data Quality Result

Mỗi run lưu:

* Test Version.
* Dataset Version.
* Scope.
* Run time.
* Expected.
* Actual.
* Difference.
* Severity.
* Sample IDs.
* Status.
* Resolution.

---

# 133. Data Quality không tự sửa nguồn

Khi fail:

* Tạo issue/reconciliation.
* Gửi alert.
* Có thể chặn Metric Certification.
* Có thể chặn Snapshot Lock.
* Không tự sửa record nguồn.

---

# 134. Reconciliation

Analytics Capability phải đối soát:

* Projection versus source.
* Metric versus component.
* Snapshot versus report.
* Revenue versus Revenue Source.
* Commission versus Commission Source.
* Spend versus imported platform data.
* Attribution total.

---

# 135. Metric Reconciliation

Mỗi certified metric có thể có:

* Independent control query.
* Expected tolerance.
* Reconciliation frequency.
* Last result.
* Owner.

---

# 136. Cross-Metric Reconciliation

Ví dụ:

```text id="m13-cross-metric-reconciliation"
Effective Contracts
≥ Completed Contracts

Revenue Collected
≤ Revenue Receivable + Approved Advance/Unallocated exceptions

Commission Paid
≤ Commission Payable cumulative

Sold Listings
khớp Contracted/Sold transactions theo rule
```

---

# 137. Anomaly Detection

Có thể phát hiện:

* Lead volume tăng/giảm bất thường.
* Duplicate rate tăng.
* Conversion giảm.
* Pipeline giảm.
* Contract cancellation tăng.
* Receivable overdue tăng.
* Revenue collection giảm.
* Commission ratio tăng.
* Marketing Spend tăng không tương ứng Lead.
* SLA breach tăng.
* User activity bất thường.

---

# 138. Candidate Anomaly lifecycle — pending validation

```text id="m13-anomaly-status"
DETECTED
PENDING_REVIEW
ACKNOWLEDGED
INVESTIGATING
EXPLAINED
FALSE_POSITIVE
RESOLVED
CLOSED
```

---

# 139. Anomaly không phải kết luận gian lận

Hệ thống chỉ:

* Gắn signal.
* Nêu baseline.
* Nêu deviation.
* Cung cấp sample.
* Tạo Task kiểm tra.

Không tự gắn nhãn gian lận hoặc xử lý kỷ luật.

---

# 140. Analytics Alert

Alert có thể dựa trên:

* Threshold.
* Target variance.
* Forecast risk.
* Freshness.
* Data quality.
* Anomaly.
* SLA.
* Budget.
* Overdue.
* Inventory risk.

---

# 141. Alert Rule

Phải có:

* Metric Version.
* Condition.
* Scope.
* Time window.
* Threshold.
* Cooldown.
* Recipients.
* Escalation.
* Severity.
* Effective dates.
* Version.

---

# 142. Alert Deduplication

Không tạo alert lặp mỗi lần refresh.

Phải có:

* Alert fingerprint.
* Open incident.
* Cooldown.
* Escalation state.
* Resolution condition.

---

# 143. Alert Acknowledgement

Lưu:

* Acknowledged by.
* Time.
* Comment.
* Assigned owner.
* Related Task.
* Resolution.

---

# 144. Commentary và Annotation

User có thể thêm comment vào:

* Dashboard.
* Widget.
* KPI.
* Snapshot.
* Forecast.
* Anomaly.

Comment không sửa Metric.

Có thể có:

* Internal note.
* Executive note.
* Period explanation.
* Action plan.

---

# 145. Metric Commentary

Ví dụ:

> Revenue tháng này thấp hơn Forecast do ba Contract Project A chuyển ngày hiệu lực sang tháng sau.

Comment phải có:

* Author.
* Scope.
* Period.
* Visibility.
* Created at.
* Version nếu edited.

---

# 146. Dashboard Annotation

Có thể đánh dấu:

* Campaign launch.
* Price change.
* Project event.
* System outage.
* Policy change.
* Holiday.
* Large Contract.
* Cancellation wave.

Giúp giải thích trend.

---

# 147. Candidate Executive Dashboard composition — không phải frontend contract

Các nhóm:

## 147.1. Commercial

* Lead.
* Qualified Lead.
* Active Customer.
* Open Pipeline.
* Weighted Pipeline.
* Booking.
* Effective Contract Value.

## 147.2. Inventory

* Available units.
* Available value.
* Absorption.
* Held/Booked.
* Days on Market.

## 147.3. Cash và Receivable

* Buyer Receivable.
* Paid.
* Outstanding.
* Overdue.
* Refund.
* Settlement.

## 147.4. Revenue

* Entitlement.
* Recognized.
* Receivable.
* Collected.
* Net Revenue.

## 147.5. Commission

* Payable.
* Paid.
* Clawback.
* Commission-to-Revenue.

## 147.6. Marketing

* Spend.
* Valid Lead.
* CPL.
* Contracts.
* Attributed Revenue.
* ROMI.

## 147.7. Operations

* Task overdue.
* SLA compliance.
* Contract cycle.
* Payment processing delay.

---

# 148. Candidate Sales Dashboard composition — không phải frontend contract

* Leads assigned.
* Lead acceptance.
* First response SLA.
* Contact rate.
* Qualified Lead.
* Appointment.
* Site Visit.
* Shortlist.
* Proposal.
* Deal Pipeline.
* Weighted Pipeline.
* Holds.
* Bookings.
* Contracts.
* Conversion.
* Average sales cycle.
* Next Action compliance.
* Forecast.
* Commission summary cá nhân theo quyền.

---

# 149. Candidate Team Lead Dashboard composition — không phải frontend contract

* Team Lead volume.
* Workload distribution.
* First response.
* Qualification.
* Appointment.
* Pipeline.
* Deal aging.
* Stale Deals.
* Forecast by sale.
* Forecast accuracy.
* Contract.
* SLA.
* Commission aggregate theo quyền.
* Coaching signals.

---

# 150. Candidate Marketing Dashboard composition — không phải frontend contract

* Spend.
* Reach.
* Click.
* Form.
* Valid Lead.
* Qualified Lead.
* Lead quality.
* Campaign-sourced Deal.
* Campaign-influenced Contract.
* Contract Value.
* Recognized Revenue.
* Collected Revenue.
* CPL.
* CPQL.
* CAC.
* ROAS.
* ROMI.
* Attribution model.
* Data freshness.

---

# 151. Candidate Inventory Dashboard composition — không phải frontend contract

* Project.
* Asset.
* Listing.
* Available.
* Held.
* Booked.
* Contracted.
* Sold.
* Blocked.
* Expired.
* Inventory value.
* Price range.
* Days on Market.
* Absorption.
* Availability conflicts.
* Double-sell risk.

---

# 152. Candidate Contract Dashboard composition — không phải frontend contract

* Contract Draft.
* Pending Review.
* Pending Signature.
* Signed.
* Effective.
* Completed.
* Cancelled.
* Contract Value.
* Contract cycle time.
* Missing documents.
* Payment status.
* Amendment.
* Cancellation reasons.

---

# 153. Candidate Finance Operations Dashboard composition — không phải frontend contract

* Receivable.
* Due today.
* Overdue.
* Payments received.
* Unidentified payment.
* Unallocated payment.
* Receipts issued.
* Receipt cancellation.
* Refund.
* Settlement.
* Reconciliation cases.
* SLA.

---

# 154. Candidate Revenue Dashboard composition — không phải frontend contract

* Revenue Entitlement.
* Recognition.
* Receivable.
* Collected.
* Outstanding.
* Overdue.
* Holdback.
* Adjustment.
* Reversal.
* Partner reconciliation.
* Forecast.
* Legal Entity.
* Project.
* Revenue Model.

---

# 155. Candidate Commission Dashboard composition — không phải frontend contract

* Entitlement.
* Recognized.
* Vested.
* Payable.
* Paid.
* Holdback.
* Advances.
* Clawback.
* Negative balance.
* Payout batch.
* Dispute.
* Commission-to-Revenue ratio.

Sensitive detail phải theo scope.

---

# 156. Candidate SLA Dashboard composition — không phải frontend contract

* Running.
* Warning.
* At Risk.
* Breached.
* Compliance.
* Average response.
* Pause.
* Extension.
* Escalation.
* Root cause.
* Capability.
* Team.
* User.

---

# 157. Candidate Data Quality Dashboard composition — không phải frontend contract

* Failed tests.
* Critical issues.
* Stale datasets.
* Missing events.
* Projection lag.
* Source mismatch.
* Metric reconciliation.
* Unknown source rate.
* Duplicate rate.
* Orphan records.
* Resolution SLA.

---

# 158. Operating Review Pack

Có thể tự tạo gói:

1. Executive Summary.
2. KPI Scorecard.
3. Sales Pipeline.
4. Inventory.
5. Marketing.
6. Contract.
7. Cash và Receivable.
8. Revenue.
9. Commission.
10. SLA.
11. Risks.
12. Actions.

Pack phải tham chiếu Snapshot/Metric Versions.

---

# 159. Dashboard Performance

Yêu cầu:

* Cache có scope.
* Không cache chung dữ liệu nhạy cảm giữa user.
* Query timeout.
* Pagination.
* Pre-aggregation.
* Materialized views.
* Asynchronous report generation.
* Query budget.
* Concurrency control.

---

# 160. Cache Security

Cache key phải gồm tối thiểu:

* User/Access policy hash hoặc authorized scope hash.
* Metric Version.
* Filters.
* Time range.
* Currency.
* Data version.

Không dùng cache chỉ theo URL.

---

# 161. Query Budget

Giới hạn:

* Maximum date range.
* Maximum dimensions.
* Maximum rows.
* Maximum cardinality.
* Maximum concurrent query.
* Timeout.
* Export size.

User nâng cao có thể có quota riêng.

---

# 162. High-Cardinality Dimension

Các dimension như:

* Customer.
* Phone.
* Contract.
* Listing.
* Message ID.

không nên dùng mặc định trong chart tổng hợp.

Drill-through phải phân trang và enforce scope.

---

# 163. Data Masking trong Cache và Export

Dữ liệu được mask trước khi:

* Cache response.
* Export.
* Scheduled report.
* External BI publication.

Không cache raw rồi mask tại frontend.

---

# 164. Candidate Semantic Query operation contract

API phải nhận:

* Metric codes.
* Metric Versions nếu cần.
* Dimensions.
* Filters.
* Time range.
* Time grain.
* Currency.
* Comparison.
* Scope request.

Backend tự resolve authorized scope.

---

# 165. Query Explain

Có thể trả:

* Metric definition.
* Dataset.
* Formula.
* Filters.
* Scope.
* Freshness.
* Source lineage.
* Query execution time.
* Cache status.
* Warnings.

Không trả raw SQL cho user không có quyền kỹ thuật.

---

# 166. Candidate Semantic API — không phải OpenAPI canonical

> Exact paths, methods, payloads, errors, idempotency và authorization metadata thuộc OpenAPI.

Ví dụ:

```text id="m13-semantic-api"
POST /analytics/query
POST /analytics/query/explain
GET  /analytics/metrics
GET  /analytics/metrics/{code}
GET  /analytics/metrics/{code}/versions
GET  /analytics/dimensions
GET  /analytics/datasets
```

---

# 167. Candidate Dashboard API — không phải OpenAPI canonical

> Exact paths, methods, payloads, errors, idempotency và authorization metadata thuộc OpenAPI.

```text id="m13-dashboard-api"
GET    /analytics/dashboards
POST   /analytics/dashboards
GET    /analytics/dashboards/{id}
PATCH  /analytics/dashboards/{id}
POST   /analytics/dashboards/{id}/versions
GET    /analytics/dashboard-versions/{id}
POST   /analytics/dashboard-versions/{id}/validate
POST   /analytics/dashboard-versions/{id}/submit-review
POST   /analytics/dashboard-versions/{id}/approve
POST   /analytics/dashboard-versions/{id}/publish
POST   /analytics/dashboards/{id}/clone
POST   /analytics/dashboards/{id}/share
GET    /analytics/dashboards/{id}/access-explanation
```

---

# 168. Candidate Metric API — không phải OpenAPI canonical

> Exact paths, methods, payloads, errors, idempotency và authorization metadata thuộc OpenAPI.

```text id="m13-metric-api"
GET    /analytics/metrics
POST   /analytics/metrics
GET    /analytics/metrics/{id}
POST   /analytics/metrics/{id}/versions
PATCH  /analytics/metric-versions/{id}
POST   /analytics/metric-versions/{id}/validate
POST   /analytics/metric-versions/{id}/test
POST   /analytics/metric-versions/{id}/reconcile
POST   /analytics/metric-versions/{id}/submit-review
POST   /analytics/metric-versions/{id}/certify
POST   /analytics/metric-versions/{id}/deprecate
GET    /analytics/metric-versions/{id}/lineage
GET    /analytics/metric-versions/{id}/dependencies
```

---

# 169. Candidate KPI API — không phải OpenAPI canonical

> Exact paths, methods, payloads, errors, idempotency và authorization metadata thuộc OpenAPI.

```text id="m13-kpi-api"
GET    /analytics/kpis
POST   /analytics/kpis
GET    /analytics/kpis/{id}
POST   /analytics/kpis/{id}/targets
POST   /analytics/kpi-targets/{id}/submit-review
POST   /analytics/kpi-targets/{id}/approve
GET    /analytics/scorecards
POST   /analytics/scorecards/generate
GET    /analytics/scorecards/{id}
```

---

# 170. Candidate Report API — không phải OpenAPI canonical

> Exact paths, methods, payloads, errors, idempotency và authorization metadata thuộc OpenAPI.

```text id="m13-report-api"
GET    /analytics/reports
POST   /analytics/reports
GET    /analytics/reports/{id}
POST   /analytics/reports/{id}/versions
POST   /analytics/report-versions/{id}/validate
POST   /analytics/report-versions/{id}/publish
POST   /analytics/reports/{id}/run
GET    /analytics/report-runs/{id}
POST   /analytics/report-runs/{id}/export
POST   /analytics/report-subscriptions
PATCH  /analytics/report-subscriptions/{id}
POST   /analytics/report-subscriptions/{id}/pause
POST   /analytics/report-subscriptions/{id}/resume
```

---

# 171. Candidate Snapshot API — không phải OpenAPI canonical

> Exact paths, methods, payloads, errors, idempotency và authorization metadata thuộc OpenAPI.

```text id="m13-snapshot-api"
GET    /analytics/snapshots
POST   /analytics/snapshots
GET    /analytics/snapshots/{id}
POST   /analytics/snapshots/{id}/generate
POST   /analytics/snapshots/{id}/validate
POST   /analytics/snapshots/{id}/submit-review
POST   /analytics/snapshots/{id}/approve
POST   /analytics/snapshots/{id}/lock
POST   /analytics/snapshots/{id}/restatements
GET    /analytics/snapshots/{id}/compare
```

---

# 172. Candidate Forecast API — không phải OpenAPI canonical

> Exact paths, methods, payloads, errors, idempotency và authorization metadata thuộc OpenAPI.

```text id="m13-forecast-api"
GET    /analytics/forecast-models
POST   /analytics/forecast-models
POST   /analytics/forecast-models/{id}/versions
POST   /analytics/forecast-model-versions/{id}/validate
POST   /analytics/forecast-model-versions/{id}/approve

GET    /analytics/forecast-runs
POST   /analytics/forecast-runs
GET    /analytics/forecast-runs/{id}
POST   /analytics/forecast-runs/{id}/calculate
POST   /analytics/forecast-runs/{id}/submit
POST   /analytics/forecast-runs/{id}/approve
POST   /analytics/forecast-runs/{id}/lock
POST   /analytics/forecast-items/{id}/overrides
GET    /analytics/forecast-accuracy
```

---

# 173. Candidate Drill-down API — không phải OpenAPI canonical

> Exact paths, methods, payloads, errors, idempotency và authorization metadata thuộc OpenAPI.

```text id="m13-drill-api"
POST   /analytics/drill-down
POST   /analytics/drill-through
GET    /analytics/drill-definitions/{id}
GET    /analytics/drill-through/{id}/access-explanation
```

Backend không tin `scope=all` hoặc owner/organization identifiers từ frontend; effective scope được resolve từ authenticated IAM context.

---

# 174. Candidate Data Quality API — không phải OpenAPI canonical

> Exact paths, methods, payloads, errors, idempotency và authorization metadata thuộc OpenAPI.

```text id="m13-dq-api"
GET    /analytics/data-quality-tests
POST   /analytics/data-quality-tests
POST   /analytics/data-quality-tests/{id}/versions
POST   /analytics/data-quality-test-versions/{id}/run
GET    /analytics/data-quality-runs
GET    /analytics/data-quality-results
POST   /analytics/data-quality-results/{id}/assign
POST   /analytics/data-quality-results/{id}/resolve
POST   /analytics/data-quality-results/{id}/create-source-correction-request
```

---

# 175. Candidate Alert và Anomaly API — không phải OpenAPI canonical

> Exact paths, methods, payloads, errors, idempotency và authorization metadata thuộc OpenAPI.

```text id="m13-alert-api"
GET    /analytics/alert-rules
POST   /analytics/alert-rules
POST   /analytics/alert-rules/{id}/versions
POST   /analytics/alert-rule-versions/{id}/validate
POST   /analytics/alert-rule-versions/{id}/activate

GET    /analytics/alerts
POST   /analytics/alerts/{id}/acknowledge
POST   /analytics/alerts/{id}/assign
POST   /analytics/alerts/{id}/resolve
POST   /analytics/alerts/{id}/create-task

GET    /analytics/anomalies
POST   /analytics/anomalies/{id}/acknowledge
POST   /analytics/anomalies/{id}/mark-false-positive
POST   /analytics/anomalies/{id}/resolve
```

---

# 176. Candidate data model — không phải physical schema canonical

> **Classification:** `CONTEXT-SPECIFIC DESIGN INPUT / PENDING VALIDATION`
> Exact tables, columns, constraints, indexes, partitions và references chỉ có hiệu lực qua Analytics Context DB Specification và Alembic migrations. Cross-context references không mặc định tạo cross-schema business foreign keys.

## 176.1. Dataset Registry

### `analytics_datasets`

* `id`
* `dataset_code`
* `name`
* `domain_code`
* `owner_user_id`
* `steward_user_id`
* `grain_description`
* `refresh_mode`
* `freshness_sla_seconds`
* `retention_policy_id`
* `access_policy_id`
* `status`
* `current_version`
* `created_at`
* `updated_at`

### `analytics_dataset_versions`

* `id`
* `dataset_id`
* `version`
* `schema_json`
* `source_mappings_json`
* `grain_definition_json`
* `join_rules_json`
* `time_fields_json`
* `dimension_definitions_json`
* `measure_definitions_json`
* `build_strategy`
* `effective_from`
* `effective_to`
* `status`
* `created_by`
* `reviewed_by`
* `approved_by`
* `created_at`

### `analytics_dataset_sources`

* `id`
* `dataset_version_id`
* `source_context`
* `source_resource_type`
* `source_table_reference`
* `source_event_types_json`
* `incremental_key`
* `created_at`

---

## 176.2. Projection

### `analytics_projection_runs`

* `id`
* `run_code`
* `dataset_version_id`
* `run_type`
* `source_cutoff_at`
* `started_at`
* `completed_at`
* `input_record_count`
* `output_record_count`
* `error_count`
* `status`
* `created_at`

### `analytics_projection_offsets`

* `id`
* `dataset_version_id`
* `source_name`
* `partition_key`
* `last_event_offset`
* `last_event_at`
* `updated_at`

### `analytics_projection_errors`

* `id`
* `projection_run_id`
* `source_type`
* `source_id`
* `error_code`
* `error_message`
* `payload_reference`
* `status`
* `created_at`

---

## 176.3. Metric

### `semantic_metrics`

* `id`
* `metric_code`
* `business_name`
* `technical_name`
* `domain_code`
* `description`
* `owner_user_id`
* `steward_user_id`
* `metric_type`
* `unit_code`
* `currency_behavior`
* `status`
* `current_version`
* `created_at`
* `updated_at`

### `semantic_metric_versions`

* `id`
* `metric_id`
* `version`
* `dataset_version_id`
* `grain_definition_json`
* `formula_expression`
* `numerator_definition_json`
* `denominator_definition_json`
* `filter_definition_json`
* `time_field_code`
* `default_time_grain`
* `dimension_policy_json`
* `null_handling_policy`
* `zero_denominator_policy`
* `deduplication_policy_json`
* `currency_policy_json`
* `access_policy_id`
* `effective_from`
* `effective_to`
* `change_classification`
* `status`
* `created_by`
* `validated_by`
* `reviewed_by`
* `approved_by`
* `certified_at`
* `created_at`

### `semantic_metric_dependencies`

* `id`
* `metric_version_id`
* `depends_on_metric_version_id`
* `dependency_type`
* `created_at`

### `semantic_metric_dimensions`

* `id`
* `metric_version_id`
* `dimension_code`
* `allowed`
* `default_enabled`
* `sensitivity_level`
* `access_policy_id`
* `created_at`

### `semantic_metric_validation_results`

* `id`
* `metric_version_id`
* `validation_type`
* `test_input_json`
* `expected_result_json`
* `actual_result_json`
* `tolerance`
* `status`
* `executed_at`
* `created_at`

### `semantic_metric_reconciliations`

* `id`
* `metric_version_id`
* `control_query_reference`
* `expected_value`
* `actual_value`
* `difference_value`
* `tolerance`
* `period_from`
* `period_to`
* `status`
* `executed_at`
* `created_at`

---

## 176.4. KPI

### `analytics_kpis`

* `id`
* `kpi_code`
* `name`
* `metric_id`
* `metric_version_id`
* `direction`
* `weight`
* `owner_user_id`
* `status`
* `created_at`

### `analytics_kpi_targets`

* `id`
* `kpi_id`
* `scope_type`
* `scope_id`
* `period_id`
* `target_value`
* `stretch_target_value`
* `minimum_value`
* `maximum_value`
* `unit_code`
* `currency`
* `status`
* `version`
* `created_by`
* `reviewed_by`
* `approved_by`
* `created_at`

### `analytics_scorecards`

* `id`
* `scorecard_code`
* `scope_type`
* `scope_id`
* `period_id`
* `snapshot_id`
* `status`
* `generated_at`
* `approved_at`
* `created_at`

### `analytics_scorecard_items`

* `id`
* `scorecard_id`
* `kpi_id`
* `metric_version_id`
* `target_value`
* `actual_value`
* `forecast_value`
* `variance_value`
* `score_value`
* `status`
* `data_freshness_status`
* `created_at`

---

## 176.5. Dashboard

### `analytics_dashboards`

* `id`
* `dashboard_code`
* `name`
* `dashboard_type`
* `domain_code`
* `owner_user_id`
* `default_scope_type`
* `default_scope_id`
* `status`
* `current_version`
* `created_at`
* `updated_at`

### `analytics_dashboard_versions`

* `id`
* `dashboard_id`
* `version`
* `layout_json`
* `global_filters_json`
* `refresh_policy_json`
* `access_policy_id`
* `effective_from`
* `effective_to`
* `status`
* `created_by`
* `reviewed_by`
* `approved_by`
* `published_at`
* `created_at`

### `analytics_dashboard_widgets`

* `id`
* `dashboard_version_id`
* `widget_code`
* `widget_type`
* `title`
* `metric_version_ids_json`
* `dataset_version_id`
* `dimension_config_json`
* `filter_config_json`
* `time_config_json`
* `comparison_config_json`
* `visualization_config_json`
* `drill_definition_id`
* `export_policy_id`
* `position_json`
* `created_at`

### `analytics_dashboard_shares`

* `id`
* `dashboard_id`
* `principal_type`
* `principal_id`
* `share_role`
* `effective_from`
* `effective_to`
* `created_by`
* `created_at`

### `analytics_user_dashboard_preferences`

* `id`
* `user_id`
* `dashboard_id`
* `layout_override_json`
* `saved_filters_json`
* `favorite`
* `updated_at`

---

## 176.6. Report

### `analytics_reports`

* `id`
* `report_code`
* `name`
* `domain_code`
* `owner_user_id`
* `status`
* `current_version`
* `created_at`
* `updated_at`

### `analytics_report_versions`

* `id`
* `report_id`
* `version`
* `metric_version_ids_json`
* `dataset_version_ids_json`
* `filter_definition_json`
* `layout_definition_json`
* `snapshot_policy_json`
* `export_policy_id`
* `access_policy_id`
* `status`
* `created_by`
* `reviewed_by`
* `approved_by`
* `published_at`
* `created_at`

### `analytics_report_runs`

* `id`
* `report_run_code`
* `report_version_id`
* `requested_by`
* `executed_scope_json`
* `executed_filters_json`
* `metric_versions_json`
* `dataset_versions_json`
* `snapshot_id`
* `data_cutoff_at`
* `data_freshness_json`
* `output_document_id`
* `output_hash`
* `status`
* `started_at`
* `completed_at`
* `created_at`

### `analytics_report_subscriptions`

* `id`
* `report_id`
* `report_version_id`
* `subscriber_user_id`
* `delivery_channel`
* `schedule_rule`
* `filter_snapshot_json`
* `format_code`
* `effective_from`
* `effective_to`
* `status`
* `created_at`

---

## 176.7. Snapshot

### `analytics_snapshots`

* `id`
* `snapshot_code`
* `snapshot_type`
* `scope_type`
* `scope_id`
* `reporting_period_id`
* `as_of_at`
* `source_cutoff_at`
* `timezone`
* `currency_policy_json`
* `metric_versions_json`
* `dataset_versions_json`
* `data_freshness_json`
* `data_quality_status`
* `status`
* `current_restatement`
* `created_by`
* `reviewed_by`
* `approved_by`
* `locked_at`
* `created_at`

### `analytics_snapshot_items`

* `id`
* `snapshot_id`
* `metric_version_id`
* `dimension_key_json`
* `metric_value`
* `unit_code`
* `currency`
* `source_lineage_reference`
* `created_at`

### `analytics_snapshot_restatements`

* `id`
* `original_snapshot_id`
* `restatement_number`
* `reason_code`
* `reason`
* `delta_summary_json`
* `source_correction_references_json`
* `status`
* `created_by`
* `reviewed_by`
* `approved_by`
* `created_at`

---

## 176.8. Forecast

### `analytics_forecast_models`

* `id`
* `model_code`
* `name`
* `forecast_type`
* `target_metric_id`
* `scope_type`
* `status`
* `current_version`
* `created_at`

### `analytics_forecast_model_versions`

* `id`
* `forecast_model_id`
* `version`
* `model_type`
* `input_metric_versions_json`
* `formula_or_model_reference`
* `assumptions_json`
* `confidence_policy_json`
* `horizon_policy_json`
* `effective_from`
* `effective_to`
* `status`
* `created_by`
* `validated_by`
* `approved_by`
* `created_at`

### `analytics_forecast_runs`

* `id`
* `forecast_run_code`
* `forecast_model_version_id`
* `scope_type`
* `scope_id`
* `scenario_id`
* `data_cutoff_at`
* `input_snapshot_id`
* `horizon_from`
* `horizon_to`
* `status`
* `confidence_score`
* `created_by`
* `submitted_by`
* `approved_by`
* `locked_at`
* `created_at`

### `analytics_forecast_items`

* `id`
* `forecast_run_id`
* `target_period_id`
* `dimension_key_json`
* `system_forecast_value`
* `override_value`
* `approved_forecast_value`
* `confidence_score`
* `created_at`

### `analytics_forecast_overrides`

* `id`
* `forecast_item_id`
* `original_value`
* `override_value`
* `reason_code`
* `reason`
* `evidence_reference`
* `requested_by`
* `approved_by`
* `effective_at`
* `created_at`

### `analytics_forecast_accuracy_results`

* `id`
* `forecast_run_id`
* `forecast_item_id`
* `actual_metric_value`
* `absolute_error`
* `percentage_error`
* `bias_value`
* `actual_snapshot_id`
* `calculated_at`
* `created_at`

---

## 176.9. Scenario

### `analytics_scenarios`

* `id`
* `scenario_code`
* `name`
* `scenario_type`
* `scope_type`
* `scope_id`
* `horizon_from`
* `horizon_to`
* `status`
* `current_version`
* `created_at`

### `analytics_scenario_versions`

* `id`
* `scenario_id`
* `version`
* `assumptions_json`
* `metric_impacts_json`
* `effective_from`
* `effective_to`
* `status`
* `created_by`
* `reviewed_by`
* `approved_by`
* `created_at`

---

## 176.10. Drill-down

### `analytics_drill_definitions`

* `id`
* `drill_code`
* `source_metric_version_id`
* `drill_type`
* `dimension_hierarchy_json`
* `target_dataset_version_id`
* `target_resource_type`
* `target_api_reference`
* `scope_mapping_json`
* `field_mapping_json`
* `maximum_rows`
* `access_policy_id`
* `export_policy_id`
* `status`
* `created_at`

---

## 176.11. Access Policy

### `analytics_access_policies`

* `id`
* `policy_code`
* `name`
* `dataset_id`
* `metric_id`
* `dimension_code`
* `aggregate_access_level`
* `detail_access_level`
* `scope_rule_json`
* `field_policy_json`
* `time_policy_json`
* `minimum_group_size`
* `export_policy_id`
* `effective_from`
* `effective_to`
* `status`
* `version`
* `created_at`

### `analytics_export_policies`

* `id`
* `policy_code`
* `maximum_rows`
* `allowed_formats_json`
* `field_allowlist_json`
* `masking_policy_json`
* `reason_required`
* `approval_required`
* `watermark_required`
* `expiry_seconds`
* `download_limit`
* `status`
* `created_at`

---

## 176.12. Data Freshness và Quality

### `analytics_data_freshness_status`

* `id`
* `dataset_version_id`
* `last_source_event_at`
* `last_ingested_at`
* `last_processed_at`
* `expected_freshness_seconds`
* `actual_lag_seconds`
* `status`
* `checked_at`

### `analytics_data_quality_tests`

* `id`
* `test_code`
* `name`
* `dataset_id`
* `severity`
* `status`
* `current_version`
* `created_at`

### `analytics_data_quality_test_versions`

* `id`
* `data_quality_test_id`
* `version`
* `test_type`
* `test_definition_json`
* `threshold_json`
* `sample_policy_json`
* `effective_from`
* `effective_to`
* `status`
* `created_by`
* `reviewed_by`
* `approved_by`
* `created_at`

### `analytics_data_quality_runs`

* `id`
* `run_code`
* `dataset_version_id`
* `started_at`
* `completed_at`
* `status`
* `created_at`

### `analytics_data_quality_results`

* `id`
* `data_quality_run_id`
* `test_version_id`
* `scope_key_json`
* `expected_value_json`
* `actual_value_json`
* `difference_json`
* `sample_references_json`
* `severity`
* `status`
* `assigned_user_id`
* `resolved_at`
* `created_at`

---

## 176.13. Alert và Anomaly

### `analytics_alert_rules`

* `id`
* `alert_rule_code`
* `name`
* `metric_id`
* `scope_type`
* `scope_id`
* `status`
* `current_version`
* `created_at`

### `analytics_alert_rule_versions`

* `id`
* `alert_rule_id`
* `version`
* `metric_version_id`
* `condition_expression`
* `time_window_json`
* `threshold_json`
* `cooldown_seconds`
* `recipient_rules_json`
* `escalation_rules_json`
* `severity`
* `effective_from`
* `effective_to`
* `status`
* `created_by`
* `approved_by`
* `created_at`

### `analytics_alerts`

* `id`
* `alert_code`
* `alert_rule_version_id`
* `scope_key_json`
* `metric_value`
* `threshold_value`
* `fingerprint`
* `severity`
* `status`
* `first_triggered_at`
* `last_triggered_at`
* `acknowledged_by`
* `assigned_user_id`
* `resolved_at`
* `created_at`

### `analytics_anomalies`

* `id`
* `anomaly_code`
* `metric_version_id`
* `scope_key_json`
* `period_from`
* `period_to`
* `baseline_value`
* `actual_value`
* `deviation_score`
* `confidence_score`
* `explanation_json`
* `status`
* `assigned_user_id`
* `created_at`
* `resolved_at`

---

## 176.14. Query và Export Audit

### `analytics_query_audit_logs`

* `id`
* `user_id`
* `dashboard_id`
* `report_id`
* `metric_versions_json`
* `dimensions_json`
* `filters_json`
* `requested_scope_json`
* `enforced_scope_json`
* `field_masking_json`
* `row_count`
* `query_duration_ms`
* `cache_status`
* `request_id`
* `created_at`

### `analytics_export_jobs`

* `id`
* `export_code`
* `requested_by`
* `source_type`
* `source_id`
* `format_code`
* `requested_scope_json`
* `enforced_scope_json`
* `field_policy_json`
* `row_count`
* `reason`
* `approval_status`
* `output_document_id`
* `output_hash`
* `expires_at`
* `download_count`
* `status`
* `created_at`
* `completed_at`

---

# 177. Candidate permission vocabulary — không phải Permission Registry canonical

> Exact permission codes, scopes, role mappings, aggregate/detail permissions, SoD và masking thuộc security registries/matrices.

## Dataset và Metric

```text id="m13-permission-metric"
analytics_dataset.view
analytics_dataset.create
analytics_dataset.create_version
analytics_dataset.validate
analytics_dataset.approve
analytics_dataset.activate
analytics_dataset.rebuild

analytics_metric.view
analytics_metric.view_definition
analytics_metric.view_formula
analytics_metric.view_lineage
analytics_metric.create
analytics_metric.create_version
analytics_metric.validate
analytics_metric.test
analytics_metric.reconcile
analytics_metric.review
analytics_metric.certify
analytics_metric.deprecate
```

## Dashboard

```text id="m13-permission-dashboard"
analytics_dashboard.view
analytics_dashboard.create
analytics_dashboard.update_draft
analytics_dashboard.create_version
analytics_dashboard.validate
analytics_dashboard.review
analytics_dashboard.approve
analytics_dashboard.publish
analytics_dashboard.share
analytics_dashboard.clone
analytics_dashboard.customize_personal
```

## KPI

```text id="m13-permission-kpi"
analytics_kpi.view
analytics_kpi.create
analytics_kpi.create_target
analytics_kpi.review_target
analytics_kpi.approve_target
analytics_scorecard.view
analytics_scorecard.generate
analytics_scorecard.approve
```

## Report và Export

```text id="m13-permission-report"
analytics_report.view
analytics_report.create
analytics_report.create_version
analytics_report.publish
analytics_report.run
analytics_report.subscribe
analytics_report.manage_subscription

analytics_export.request
analytics_export.approve
analytics_export.download
analytics_export.view_audit
```

## Snapshot

```text id="m13-permission-snapshot"
analytics_snapshot.view
analytics_snapshot.create
analytics_snapshot.generate
analytics_snapshot.validate
analytics_snapshot.review
analytics_snapshot.approve
analytics_snapshot.lock
analytics_snapshot.restate
analytics_snapshot.compare
```

## Forecast

```text id="m13-permission-forecast"
analytics_forecast.view
analytics_forecast.create_model
analytics_forecast.create_model_version
analytics_forecast.validate_model
analytics_forecast.approve_model
analytics_forecast.run
analytics_forecast.override
analytics_forecast.submit
analytics_forecast.approve
analytics_forecast.lock
analytics_forecast.view_accuracy
```

## Drill-down

```text id="m13-permission-drill"
analytics_drill.aggregate
analytics_drill.breakdown
analytics_drill.detail
analytics_drill.source_resource
analytics_drill.sensitive
```

## Data Quality và Alert

```text id="m13-permission-quality"
analytics_data_quality.view
analytics_data_quality.create_test
analytics_data_quality.run
analytics_data_quality.assign
analytics_data_quality.resolve
analytics_data_quality.create_source_correction

analytics_alert.view
analytics_alert.create_rule
analytics_alert.approve_rule
analytics_alert.acknowledge
analytics_alert.assign
analytics_alert.resolve

analytics_anomaly.view
analytics_anomaly.review
analytics_anomaly.mark_false_positive
analytics_anomaly.resolve
```

## Administration

```text id="m13-permission-admin"
analytics_access_policy.view
analytics_access_policy.manage
analytics_export_policy.manage
analytics_cache.manage
analytics_projection.monitor
analytics_projection.rebuild
analytics_external_bi.publish
analytics_external_bi.revoke
analytics_query_audit.view
```

Candidate scope vocabulary dưới đây không phải exact Scope Registry:

```text id="m13-scopes"
self
mine
assigned
team
department
branch
legal_entity
project
shared
all
```

---

# 178. Candidate role baseline — không phải Role/Permission Registry canonical

> Role descriptions chỉ thể hiện product intent. Backend authority phải resolve từ IAM/Security canonical sources.

## 178.1. Sale

Được:

* Xem Personal Dashboard.
* Xem Lead, Task, Appointment, Pipeline của mình.
* Xem Contract summary của mình.
* Xem Commission self.
* Drill-through resource mình có quyền.
* Export hạn chế nếu được cấp.

Không được:

* Xem sale khác.
* Xem Commission Team.
* Xem full Customer export.
* Xem Revenue Arrangement nhạy cảm.
* Tự mở scope bằng filter.

## 178.2. Team Lead

Được:

* Team Dashboard.
* Team Pipeline.
* Team SLA.
* Team Forecast.
* Drill-down tới sale trong Team.
* Commission aggregate Team nếu được cấp.

Không mặc định:

* Xem full Contract financial details.
* Xem Customer ngoài Team.
* Xem Department khác.

## 178.3. Department Head

Được:

* Department KPI.
* Team comparison.
* Department Forecast.
* Pipeline và conversion.
* Drill-down trong Department.

## 178.4. Marketing

Được:

* Campaign.
* Lead source.
* Audience aggregate.
* Attribution.
* Spend.
* Contract/Revenue attribution theo Campaign.

Không mặc định:

* Xem Commission cá nhân.
* Xem full Customer Financial Profile.
* Xem Contract document.
* Xem bank data.

## 178.5. Inventory

Được:

* Project/Listing/Inventory Dashboard.
* Availability.
* Absorption.
* Contracted/Sold summary.
* Drill-through Listing theo Project Access.

## 178.6. Accounting

Được:

* Receivable.
* Payment.
* Receipt.
* Aging.
* Collection.
* Settlement.
* Relevant Contract summary.

## 178.7. Finance

Được:

* Cash.
* Revenue.
* Forecast.
* Refund.
* Settlement.
* Commission payout.
* Multi-Legal Entity view theo quyền.

## 178.8. Legal

Được:

* Contract status.
* Legal review SLA.
* Missing documents.
* Cancellation.
* Dispute.

Không mặc định xem Marketing Spend hoặc Commission cá nhân.

## 178.9. Director

Được:

* Executive Dashboard.
* Legal Entity hoặc Enterprise scope.
* Snapshot.
* Forecast.
* KPI.
* Export theo approval.
* Drill-down theo quyền.

## 178.10. Data Analyst

Được:

* Metric definitions.
* Certified datasets.
* Aggregate query.
* Data quality.
* Lineage.

Không mặc định có raw Customer PII.

## 178.11. Auditor

Được:

* Historical snapshots.
* Metric versions.
* Query/export audit.
* Lineage.
* Approved detail scope.

Không được sửa Metric hoặc operational data.

---

# 179. Candidate business facts — không phải Event contracts canonical

> Exact Event names, versions, payloads, channels và consumers thuộc JSON Schema, AsyncAPI và Event Registry.

Analytics Capability phát:

```text id="m13-events"
analytics_dataset.version_created
analytics_dataset.activated
analytics_projection.refresh_started
analytics_projection.refresh_completed
analytics_projection.refresh_failed
analytics_projection.stale

semantic_metric.created
semantic_metric.version_created
semantic_metric.validated
semantic_metric.certified
semantic_metric.deprecated
semantic_metric.reconciliation_failed

analytics_kpi.target_created
analytics_kpi.target_approved
analytics_scorecard.generated
analytics_scorecard.approved

analytics_dashboard.created
analytics_dashboard.version_created
analytics_dashboard.published
analytics_dashboard.suspended

analytics_report.run_started
analytics_report.run_completed
analytics_report.run_failed
analytics_report.delivered

analytics_snapshot.created
analytics_snapshot.generated
analytics_snapshot.locked
analytics_snapshot.restated

analytics_forecast.run_created
analytics_forecast.calculated
analytics_forecast.submitted
analytics_forecast.approved
analytics_forecast.locked
analytics_forecast.override_created

analytics_data_quality.failed
analytics_data_quality.resolved
analytics_data_freshness.stale
analytics_data_freshness.recovered

analytics_alert.triggered
analytics_alert.acknowledged
analytics_alert.resolved
analytics_anomaly.detected
analytics_anomaly.resolved

analytics_export.requested
analytics_export.approved
analytics_export.completed
analytics_export.expired
```

Consumer phải idempotent.

---

# 180. Candidate Platform configuration references

```text id="m13-configs"
analytics.dataset_workflow
analytics.dataset_version_policy
analytics.projection_refresh_policy
analytics.projection_retry_policy
analytics.projection_rebuild_policy

analytics.metric_workflow
analytics.metric_certification_policy
analytics.metric_naming_policy
analytics.metric_version_policy
analytics.metric_reconciliation_policy
analytics.metric_deprecation_policy

analytics.dashboard_workflow
analytics.dashboard_publish_policy
analytics.dashboard_sharing_policy
analytics.dashboard_refresh_policy
analytics.dashboard_cache_policy

analytics.kpi_workflow
analytics.kpi_target_policy
analytics.scorecard_policy

analytics.report_workflow
analytics.report_schedule_policy
analytics.report_delivery_policy
analytics.report_retention_policy

analytics.snapshot_workflow
analytics.snapshot_lock_policy
analytics.snapshot_restatement_policy
analytics.period_close_policy

analytics.forecast_workflow
analytics.forecast_model_policy
analytics.forecast_override_policy
analytics.forecast_lock_policy
analytics.forecast_accuracy_policy
analytics.scenario_policy

analytics.drilldown_policy
analytics.drillthrough_policy
analytics.aggregate_access_policy
analytics.minimum_group_size_policy

analytics.row_access_policy
analytics.field_access_policy
analytics.metric_access_policy
analytics.dimension_access_policy
analytics.time_access_policy

analytics.export_policy
analytics.export_approval_policy
analytics.export_watermark_policy
analytics.export_retention_policy

analytics.data_freshness_policy
analytics.data_quality_policy
analytics.reconciliation_policy
analytics.alert_policy
analytics.anomaly_policy

analytics.currency_policy
analytics.reporting_calendar_policy
analytics.timezone_policy
analytics.retention_policy
analytics.external_bi_policy
analytics.notification_policy
analytics.sla_policy
```

Mỗi configuration definition phải công bố schema, allowed scopes, resolution strategy, owner, version, effective period, approval và Audit requirements khi phù hợp.

---

# 181. System invariant

Các quy tắc sau không được cấu hình tắt:

1. Analytics Capability không được là nguồn chân lý nghiệp vụ thứ hai.
2. Projection không được sửa dữ liệu nguồn.
3. Dashboard không được sửa resource nguồn trực tiếp.
4. Metric Certified không được sửa trực tiếp.
5. Dataset Version active không được sửa trực tiếp.
6. Dashboard Published không được sửa trực tiếp.
7. Snapshot Locked không được sửa trực tiếp.
8. Forecast Locked không được sửa trực tiếp.
9. Restatement không được xóa Snapshot gốc.
10. Metric phải có Dataset Version.
11. Metric phải có grain.
12. Metric phải có time field.
13. Metric tiền phải có currency policy.
14. Metric ratio phải có zero denominator policy.
15. Metric phải có lineage.
16. Drill-down không được mở rộng scope.
17. Drill-through phải dùng API owning Context.
18. Aggregate access không tự cấp detail access.
19. Export không được rộng hơn quyền xem.
20. Scheduled Report phải re-authorize mỗi lần chạy.
21. Cache phải scope-aware.
22. Field masking phải thực hiện backend.
23. Dashboard filter chỉ được thu hẹp scope.
24. User parameter không được thay authenticated scope.
25. Current organization không được viết lại organization snapshot lịch sử.
26. Gross Contract Value không được gọi Revenue.
27. Revenue Collected phải lấy từ Revenue and Commission Capability.
28. Buyer Payment không mặc định là Revenue.
29. Commission Paid không được tính từ payout approved chưa có payment confirmation.
30. Marketing Influenced Revenue không được cộng dồn naïve.
31. Forecast không được hiển thị như Actual.
32. Target không được hiển thị như Forecast.
33. Snapshot phải lưu Metric Versions.
34. Snapshot phải lưu data cutoff.
35. Data stale phải được hiển thị.
36. Data quality fail Critical có thể chặn Snapshot Lock.
37. Anomaly không được tự kết luận gian lận.
38. Manual reporting adjustment phải tách khỏi source.
39. Audit query, export, snapshot và forecast không được sửa.
40. Analytics Capability không thay ERP, payroll, bank hoặc statutory source of truth. External BI là presentation/analysis consumer, không phải CRM business source.

---

# 182. Rule nghiệp vụ bắt buộc

1. Mỗi Dataset phải có grain.
2. Mỗi Dataset phải có owner.
3. Mỗi Dataset phải có source mapping.
4. Active Dataset Version không sửa.
5. Projection phải có source offset/cutoff.
6. Projection event lặp không tạo duplicate.
7. Full rebuild không xóa Locked Snapshot.
8. Late-arriving data phải được nhận biết.
9. Mỗi Metric phải có code unique.
10. Metric code không được mơ hồ.
11. Metric phải có business definition.
12. Metric phải có technical definition.
13. Metric phải có Dataset Version.
14. Metric phải có formula.
15. Metric phải có time field.
16. Metric phải có null policy.
17. Ratio phải có denominator policy.
18. Money metric phải có currency.
19. Metric phải có access policy.
20. Certified Metric phải qua validation.
21. Certified Metric phải qua reconciliation.
22. Certified Metric không sửa trực tiếp.
23. Major metric change phải tạo version mới.
24. Metric cũ phải giữ cho dashboard lịch sử.
25. Dependency cycle bị chặn.
26. Formula không chạy code tùy ý.
27. Safe division phải được áp dụng.
28. Null không tự biến thành zero.
29. Unknown không tự biến thành direct/zero.
30. Multi-currency không cộng trực tiếp.
31. Timezone phải được resolve.
32. Reporting Calendar phải version.
33. Business Calendar không thay Reporting Calendar.
34. Lead metric phải loại spam theo definition.
35. Duplicate Lead treatment phải ghi rõ.
36. Lead conversion phải nêu stage.
37. Active Customer phải có definition.
38. Available Listing phải dùng Product, Asset, Listing and Inventory Capability rule.
39. Inventory Absorption phải nêu denominator.
40. Weighted Pipeline phải có probability version.
41. Pipeline Value không được gọi Revenue.
42. Contract Value phải tách gross/net/effective.
43. Contract cancellation phải phản ánh gross/net.
44. Collection Rate phải nêu receivable basis.
45. Buyer Payment không tự thành Revenue.
46. Revenue metric phải lấy Revenue and Commission Capability.
47. Commission metric phải lấy Revenue and Commission Capability.
48. Meaningful Interaction phải có definition.
49. Marketing ROAS phải nêu numerator.
50. Influenced Revenue phải cảnh báo double counting.
51. KPI phải tham chiếu Metric Version.
52. KPI Target phải có period.
53. Target approved không sửa trực tiếp.
54. Scorecard phải tách Actual/Forecast/Target.
55. Dashboard phải có owner.
56. Dashboard phải có version.
57. Published Dashboard không sửa.
58. Widget phải tham chiếu Metric Version.
59. Widget phải hiển thị freshness.
60. Global filter không mở rộng scope.
61. User filter phải intersect scope.
62. Personal Dashboard không mở permission.
63. Dashboard Share không cấp data access.
64. Embedded Dashboard phải authenticated.
65. Drill-down phải có definition.
66. Drill-down phải enforce backend.
67. Drill-through phải gọi source API.
68. Aggregate view không tự cho detail.
69. Minimum group size phải được enforce khi cấu hình.
70. RLS phải đồng bộ Identity, Access and Organization Capability.
71. Field masking phải backend.
72. Metric-level access phải được enforce.
73. Dimension access phải được enforce.
74. Time access phải được enforce.
75. Access explanation phải phản ánh scope thực.
76. Export phải có policy.
77. Export không vượt field access.
78. Export không vượt row scope.
79. Export approval phải được kiểm tra.
80. Export file phải expiry khi policy yêu cầu.
81. Scheduled report phải re-authorize.
82. Inactive recipient không nhận report.
83. Report Version đã phát hành không sửa.
84. Report run phải lưu Metric Versions.
85. Report run phải lưu filters/scope.
86. Snapshot phải có as-of time.
87. Snapshot phải có source cutoff.
88. Snapshot phải có Metric Versions.
89. Snapshot Lock cần data quality phù hợp.
90. Snapshot Locked không sửa.
91. Restatement phải giữ original.
92. As-of query không dùng current state giả lịch sử.
93. Historical state phải dùng history/version.
94. Forecast phải có Model Version.
95. Forecast phải có data cutoff.
96. Forecast phải có horizon.
97. Forecast phải tách system/manual.
98. Override phải có reason.
99. Override không sửa source Deal.
100. Forecast Lock không sửa.
101. Forecast accuracy phải dùng actual phù hợp.
102. Restated actual phải được ghi chú khi đo accuracy.
103. Scenario không sửa operational data.
104. Scenario assumption phải version.
105. Data freshness phải hiển thị.
106. Stale data không được giả là real-time.
107. Critical stale source có thể chặn export.
108. Data Quality Test phải version.
109. Data Quality fail không tự sửa source.
110. Critical quality issue phải alert.
111. Reconciliation phải có tolerance.
112. Accepted difference cần quyền.
113. Anomaly phải có baseline.
114. Anomaly không phải fraud conclusion.
115. Alert phải chống trùng.
116. Alert resolution phải có actor.
117. Commentary không sửa metric.
118. Dashboard annotation phải có visibility.
119. Cache key phải có scope/access hash.
120. Cache không dùng chung raw sensitive data.
121. Query phải có timeout/quota.
122. High-cardinality drill phải phân trang.
123. Raw Customer identifiers không dùng chart mặc định.
124. Semantic API phải enforce auth.
125. Query Explain không lộ raw SQL trái quyền.
126. External BI publication phải có policy.
127. External BI dataset phải field-mask.
128. BI credential phải least privilege.
129. Same idempotency key cùng payload trả cùng kết quả.
130. Same key khác payload phải conflict.
131. Event lặp không tăng metric duplicate.
132. Rebuild phải tái tạo được projection.
133. Metric phải tái tạo được từ source/version.
134. Snapshot phải tái tạo được trong giới hạn retention.
135. Dashboard phải ghi data freshness.
136. Report phải ghi generated time.
137. Export phải audit.
138. Sensitive query phải audit.
139. User inactive không truy cập Dashboard.
140. Delegation chỉ áp dụng trong effective period.
141. Project Access không mở Customer detail.
142. Marketing Access không mở Commission detail.
143. Accounting Access không mở Interaction content mặc định.
144. Sale chỉ xem self/mine.
145. Team Lead chỉ xem team.
146. Department Head chỉ xem department.
147. Legal Entity scope phải backend enforce.
148. `all` không phải default.
149. URL filter không mở rộng quyền.
150. Capability không tạo nguồn chân lý thứ hai.

---

# 183. Cảnh báo và phát hiện bất thường

Hệ thống cần cảnh báo khi:

* Metric không có owner.
* Metric không có time field.
* Metric ratio không có zero policy.
* Metric tiền không có currency.
* Metric Certified nhưng reconciliation fail.
* Metric mới làm thay đổi Executive Dashboard lớn.
* Dashboard dùng Deprecated Metric.
* Dashboard không hiển thị freshness.
* Dashboard filter mở rộng scope.
* Cache trả dữ liệu scope khác.
* Drill-down count không khớp metric.
* Drill-through mở resource trái quyền.
* Aggregate nhỏ hơn minimum group size.
* Export vượt row limit.
* Scheduled Report gửi user inactive.
* Snapshot Lock khi source stale.
* Snapshot Lock khi Critical DQ fail.
* Restatement delta lớn.
* Forecast override quá nhiều.
* Forecast luôn cao hơn Actual.
* Forecast item không có source.
* Weighted Pipeline probability chưa version.
* Lead count projection lệch source.
* Available Listing metric có Contract Lock.
* Contract Value bị hiển thị là Revenue.
* Revenue Collected lớn hơn nguồn hợp lệ.
* Commission Paid vượt Payable.
* Marketing Influenced Revenue bị cộng trùng.
* Contract cancellation chưa giảm net conversion.
* Revenue reversal chưa cập nhật metric.
* Projection lag vượt SLA.
* Source event offset không tiến.
* Full rebuild output count lệch lớn.
* Data Quality fail liên tục.
* Anomaly volume tăng bất thường.
* Query cardinality quá lớn.
* Dashboard tải chậm.
* User export dữ liệu nhạy cảm hàng loạt.
* User query ngoài giờ bất thường.
* Same idempotency key khác payload.
* External BI dataset stale.
* External BI credential hết hạn.
* Metric lineage bị đứt.
* Snapshot không thể tái tạo.
* Report hash thay đổi không có version mới.
* Current data và snapshot chênh lớn không giải thích.
* Metric definition cùng tên nhưng khác formula.
* Dashboard khác nhau dùng metric tự tính riêng.

---

# 184. Audit requirements và evidence

> Audit Context sở hữu immutable Audit facts. Analytics giữ operational query/export records và phát audit-worthy facts/references.

## 184.1. Thao tác bắt buộc

* Dataset create/version/activate.
* Projection refresh/rebuild.
* Metric create/version/test/certify/deprecate.
* KPI Target.
* Dashboard create/version/publish/share.
* Report create/run/deliver.
* Subscription.
* Snapshot generate/lock/restate.
* Forecast calculate/override/submit/approve/lock.
* Scenario.
* Drill-down.
* Sensitive detail view.
* Data quality.
* Reconciliation.
* Alert.
* Anomaly.
* Export.
* External BI publication.
* Access policy change.
* Cache invalidation.

## 184.2. Nội dung

* Actor.
* Role.
* Legal Entity.
* Scope requested.
* Scope enforced.
* Dataset Version.
* Metric Version.
* Dashboard Version.
* Report Version.
* Snapshot.
* Forecast.
* Filters.
* Dimensions.
* Fields.
* Masking.
* Row count.
* Before.
* After.
* Reason.
* Approval.
* Data cutoff.
* Freshness.
* IP.
* Device.
* Request ID.
* Correlation ID.
* Idempotency key.
* Timestamp.
* Result.

---

# 185. Integration với BI ngoài

Analytics có thể công bố governed semantic dataset metadata; Integration thực hiện delivery tới:

* Power BI.
* Looker.
* Tableau.
* Metabase.
* Data Warehouse.
* Data Lake.
* Approved SQL endpoint.

## 185.1. Nguyên tắc

* Chỉ publish Certified Dataset.
* Có service account.
* Có row-level hoặc pre-filtered dataset.
* Có field masking.
* Có refresh SLA.
* Có access expiry.
* Có audit.
* Không cấp raw production-database access. Connector credentials và transport thuộc Integration Context.

## 185.2. BI Dataset Publication

Phải lưu:

* Dataset Version.
* Target system.
* Published schema.
* Fields.
* Filters.
* Scope.
* Integration credential reference.
* Refresh.
* Owner.
* Status.
* Revocation.

---

# 186. External Data

Analytics Capability có thể nhận dữ liệu ngoài:

* Market benchmark.
* Economic indicator.
* Competitor price.
* External media spend.
* ERP actual.
* Payroll actual.

Phải tách:

* Internal operational source.
* External source.
* Source confidence.
* Refresh.
* License.
* Version.

Không dùng external data làm nguồn chân lý CRM nếu không có reconciliation.

---

# 187. Data Retention

Retention theo:

* Projection.
* Query logs.
* Export.
* Snapshot.
* Forecast.
* Report.
* Dashboard cache.
* Data quality samples.
* Anomaly.
* External publication.

Snapshot Board/Legal có thể giữ lâu hơn projection tạm.

---

# 188. Purge

Purge phải:

* Theo policy.
* Không xóa Locked Snapshot trái quy định.
* Không xóa audit.
* Không làm đứt lineage.
* Không làm mất khả năng giải thích báo cáo cần giữ.
* Tôn trọng Legal Hold.

---

# 189. Backup và Recovery

Phải hỗ trợ:

* Dashboard definitions.
* Metric definitions.
* Dataset metadata.
* Snapshot.
* Forecast.
* Access policies.
* Query audit.
* Projection rebuild.

Projection có thể rebuild; Snapshot Locked phải backup như dữ liệu cần bảo toàn.

---

# 190. Observability

Theo dõi:

* Projection lag.
* Event backlog.
* Query latency.
* Cache hit.
* Failed queries.
* Export queue.
* Report duration.
* Snapshot generation.
* Forecast run.
* Data quality.
* External BI refresh.

---

# 191. Analytics operational SLO/SLA policy inputs

> Các giá trị minh họa dưới đây là design baselines để validation, không phải production SLO/SLA contract. Exact targets thuộc operations documents.

Các SLA:

* Projection refresh.
* Dashboard query.
* Report generation.
* Export generation.
* Snapshot generation.
* Metric validation.
* Data quality response.
* Critical stale recovery.
* Forecast calculation.
* Restatement review.

Ví dụ:

| Nghiệp vụ                      |     SLA tham khảo |
| ------------------------------ | ----------------: |
| Lead projection freshness      |            5 phút |
| Payment projection freshness   |            5 phút |
| Revenue projection freshness   |           15 phút |
| Standard dashboard query       |            3 giây |
| Complex report                 |            2 phút |
| Export nhỏ                     |            5 phút |
| Critical freshness incident    |           30 phút |
| Snapshot month-end             | Theo lịch đóng kỳ |
| Forecast recalculation         |        Trong ngày |
| Critical metric reconciliation |             4 giờ |

---

# 192. Notification

## Data/CRM Admin

* Projection failed.
* Dataset stale.
* Event backlog.
* Metric reconciliation failed.
* Dashboard error.
* Export failure.
* BI refresh failure.

## Metric Owner

* Metric pending review.
* Validation failed.
* Downstream impact.
* Deprecated metric still in use.
* Data quality issue.

## Manager

* KPI off track.
* Forecast risk.
* Pipeline drop.
* Revenue overdue.
* SLA breach spike.
* Inventory absorption issue.

## Director

* Executive KPI off track.
* Forecast variance lớn.
* Revenue reversal lớn.
* Snapshot restatement.
* Critical data quality issue.
* Export security incident.

---

# 193. Phạm vi MVP

## 193.1. Bắt buộc

* Dataset Registry.
* Dataset Version.
* Projection metadata.
* Semantic Metric.
* Metric Version.
* Formula.
* Dimensions.
* Time field.
* Currency policy.
* Metric certification.
* Lead canonical metrics.
* Customer canonical metrics.
* Inventory canonical metrics.
* Pipeline canonical metrics.
* Contract canonical metrics.
* Payment/Receivable metrics.
* Revenue metrics.
* Commission metrics.
* Activity/SLA metrics.
* Marketing metrics.
* KPI.
* Target.
* Scorecard.
* Dashboard.
* Dashboard Version.
* Widget.
* Global filters.
* Scope intersection.
* Drill-down.
* Drill-through.
* Aggregate access.
* Field masking.
* Row-level security.
* Export policy.
* Scheduled reports.
* Snapshot.
* Snapshot lock.
* Restatement.
* Weighted Pipeline Forecast.
* Revenue milestone Forecast.
* Cash Collection Forecast cơ bản.
* Forecast override.
* Forecast lock.
* Data freshness.
* Data quality tests.
* Metric reconciliation.
* Threshold alerts.
* Query audit.
* Export audit.
* Multi-Legal Entity.
* Multi-Project.
* External BI publication cơ bản.
* Domain events.

## 193.2. Giai đoạn nâng cao

* Full data warehouse.
* Bitemporal warehouse.
* Data catalog nâng cao.
* Natural language analytics.
* AI executive summaries.
* Predictive Forecast.
* Machine-learning anomaly detection.
* Cohort builder nâng cao.
* Self-service semantic exploration.
* Row-level security federation với BI.
* Incrementality analysis.
* Profitability model.
* Scenario simulation nâng cao.
* Board report automation.
* Data observability platform.
* Metric contracts.
* Data mesh/domain ownership.
* Column-level lineage tự động.
* Query acceleration.
* Embedded analytics cho partner portal.
* External benchmark marketplace.

---

# 194. Tiêu chí nghiệm thu

Capability được xem là đạt khi:

1. Tạo được Dataset.
2. Dataset có code.
3. Dataset có owner.
4. Dataset có grain.
5. Dataset có refresh mode.
6. Dataset có freshness SLA.
7. Tạo Dataset Version.
8. Version có schema.
9. Version có source mapping.
10. Version có time fields.
11. Active Version không sửa.
12. Projection Run được ghi.
13. Projection có source cutoff.
14. Projection có record counts.
15. Projection lỗi được ghi.
16. Event lặp không tạo duplicate.
17. Full rebuild hoạt động.
18. Full rebuild không xóa Snapshot Locked.
19. Tạo Semantic Metric.
20. Metric code unique.
21. Metric có business name.
22. Metric có description.
23. Metric có owner.
24. Metric có type.
25. Metric có Dataset Version.
26. Metric có grain.
27. Metric có formula.
28. Metric có filter.
29. Metric có time field.
30. Metric có time grain.
31. Metric có null policy.
32. Ratio có zero denominator policy.
33. Money metric có currency policy.
34. Metric có access policy.
35. Tạo Metric Version.
36. Active Metric Version không sửa.
37. Patch/Minor/Major được phân loại.
38. Metric dependency được lưu.
39. Dependency cycle bị chặn.
40. Metric test hoạt động.
41. Metric reconciliation hoạt động.
42. Metric Certified cần approval.
43. Metric Deprecated được cảnh báo.
44. Dashboard lịch sử giữ Metric Version cũ.
45. Lead Created metric đúng.
46. Valid Lead metric đúng.
47. Spam Lead bị loại.
48. Duplicate Lead treatment đúng definition.
49. Qualified Lead metric đúng.
50. Lead-to-Contract conversion đúng.
51. Active Customer metric có definition.
52. Customer with Requirement metric đúng.
53. Available Listing metric dùng Product, Asset, Listing and Inventory Capability rule.
54. Held/Booked/Contracted/Sold Listing đúng.
55. Inventory Value đúng currency.
56. Absorption Rate đúng denominator.
57. Open Deal metric đúng.
58. Pipeline Value đúng.
59. Weighted Pipeline dùng probability version.
60. Stale Deal metric đúng.
61. Booking metric đúng.
62. Deposit Confirmed metric đúng.
63. Contract Signed metric đúng.
64. Contract Effective metric đúng.
65. Contract Cancelled metric đúng.
66. Gross Contract Value được tách.
67. Net Contract Value được tách.
68. Contract Value không gọi Revenue.
69. Buyer Receivable đúng.
70. Buyer Paid đúng.
71. Overdue đúng.
72. Receipt Issued đúng.
73. Refund Paid đúng.
74. Revenue Entitlement đúng.
75. Recognized Revenue đúng.
76. Revenue Receivable đúng.
77. Revenue Collected đúng.
78. Revenue Reversal đúng.
79. Buyer Payment không thành Revenue.
80. Commission Entitlement đúng.
81. Commission Payable đúng.
82. Commission Paid đúng.
83. Clawback đúng.
84. Meaningful Interaction metric đúng.
85. SLA Compliance đúng.
86. Marketing Spend đúng.
87. CPL dùng Valid Lead.
88. CPQL đúng.
89. Attributed Contract Value tách Revenue.
90. Attributed Recognized Revenue đúng.
91. ROMI có basis.
92. Tạo KPI.
93. KPI tham chiếu Metric Version.
94. KPI có direction.
95. Tạo KPI Target.
96. Target có scope.
97. Target có period.
98. Target approved không sửa.
99. Revised Target giữ original.
100. Tạo Scorecard.
101. Scorecard có Actual.
102. Scorecard có Target.
103. Scorecard có Forecast.
104. Scorecard có Variance.
105. Scorecard có status.
106. Tạo Dashboard.
107. Dashboard có code.
108. Dashboard có owner.
109. Dashboard có type.
110. Dashboard có default scope.
111. Tạo Dashboard Version.
112. Published Version không sửa.
113. Tạo KPI Card.
114. Tạo trend chart.
115. Tạo funnel.
116. Tạo table.
117. Tạo forecast chart.
118. Widget tham chiếu Metric Version.
119. Widget hiển thị freshness.
120. Global filter hoạt động.
121. Date filter hoạt động.
122. Legal Entity filter hoạt động.
123. Project filter hoạt động.
124. Team filter hoạt động.
125. User filter không mở rộng scope.
126. Sale mặc định mine.
127. Team Lead mặc định team.
128. Department Head mặc định department.
129. Director dùng all khi có quyền.
130. Dashboard Share không cấp data access.
131. Personal layout hoạt động.
132. Personal layout không mở scope.
133. Tạo Drill-down Definition.
134. Drill từ Enterprise xuống Legal Entity.
135. Drill từ Department xuống Team.
136. Drill từ Team xuống Sale.
137. Drill từ Contract metric xuống Contract list.
138. Drill-through dùng Contract and Cash Capability API.
139. Overdue drill-through dùng Receivable API.
140. Revenue drill-through dùng Revenue and Commission Capability.
141. Marketing drill-through dùng Marketing Capability.
142. URL sửa scope không có tác dụng.
143. Backend enforce scope.
144. Aggregate access hoạt động.
145. Detail access tách biệt.
146. Minimum group size hoạt động.
147. Field masking hoạt động.
148. Metric-level access hoạt động.
149. Dimension-level access hoạt động.
150. Time-level access hoạt động.
151. Access Explanation hoạt động.
152. Tạo Export Policy.
153. Export có row limit.
154. Export có field allowlist.
155. Export có masking.
156. Export approval hoạt động.
157. Export watermark hoạt động.
158. Export expiry hoạt động.
159. Export không vượt scope.
160. Export audit đầy đủ.
161. Tạo Report.
162. Tạo Report Version.
163. Report Run lưu filters.
164. Report Run lưu scope.
165. Report Run lưu Metric Versions.
166. Tạo Subscription.
167. Subscription có schedule.
168. Subscription re-authorize mỗi run.
169. User inactive không nhận.
170. Secure delivery hoạt động.
171. Tạo Snapshot.
172. Snapshot có type.
173. Snapshot có as-of time.
174. Snapshot có source cutoff.
175. Snapshot có Metric Versions.
176. Snapshot có Dataset Versions.
177. Snapshot có freshness.
178. Snapshot có quality status.
179. Generate Snapshot được.
180. Validate Snapshot được.
181. Approve Snapshot được.
182. Lock Snapshot được.
183. Locked Snapshot không sửa.
184. Tạo Restatement.
185. Restatement giữ original.
186. Restatement có delta.
187. Compare Snapshot được.
188. Current/as-original/as-restated được tách.
189. Historical Deal Pipeline đúng as-of date.
190. Historical organization snapshot đúng.
191. Tạo Forecast Model.
192. Model có target metric.
193. Tạo Model Version.
194. Model Version có inputs.
195. Weighted Pipeline Forecast hoạt động.
196. Revenue Milestone Forecast hoạt động.
197. Cash Collection Forecast hoạt động.
198. Forecast Run có data cutoff.
199. Forecast Run có horizon.
200. Forecast có confidence.
201. Tạo Forecast Override.
202. Override có original/new value.
203. Override có reason.
204. Override không sửa Deal nguồn.
205. Submit Forecast được.
206. Approve Forecast được.
207. Lock Forecast được.
208. Locked Forecast không sửa.
209. Forecast accuracy được tính.
210. Forecast bias được tính.
211. Tạo Scenario.
212. Scenario có assumptions.
213. Scenario không sửa operational data.
214. Data Freshness được ghi.
215. Widget hiển thị last refresh.
216. Stale status hoạt động.
217. Stale warning hoạt động.
218. Critical stale có thể chặn export.
219. Tạo Data Quality Test.
220. Test có severity.
221. Test có version.
222. Completeness test hoạt động.
223. Uniqueness test hoạt động.
224. Referential integrity test hoạt động.
225. Revenue reconciliation test hoạt động.
226. Commission consistency test hoạt động.
227. Attribution total test hoạt động.
228. Fail result được ghi.
229. Fail không tự sửa source.
230. Tạo Source Correction Request.
231. Metric reconciliation có tolerance.
232. Cross-metric reconciliation hoạt động.
233. Tạo Alert Rule.
234. Alert có Metric Version.
235. Alert có threshold.
236. Alert có cooldown.
237. Alert chống trùng.
238. Alert acknowledge được.
239. Alert tạo Task được.
240. Tạo Anomaly.
241. Anomaly có baseline.
242. Anomaly có deviation.
243. Anomaly không tự kết luận gian lận.
244. False Positive được ghi.
245. Cache scope-aware.
246. Cache không rò dữ liệu user khác.
247. Query timeout hoạt động.
248. Row limit hoạt động.
249. High-cardinality query được kiểm soát.
250. Semantic Query API hoạt động.
251. Query Explain hiển thị definition.
252. Query Explain hiển thị scope.
253. Query Explain hiển thị freshness.
254. Query Explain không lộ SQL trái quyền.
255. External BI publish Certified Dataset được.
256. External BI field masking hoạt động.
257. External BI access expiry hoạt động.
258. BI refresh được theo dõi.
259. Query Audit lưu user.
260. Query Audit lưu scope requested/enforced.
261. Query Audit lưu filters.
262. Query Audit lưu Metric Versions.
263. Sensitive view được audit.
264. Same idempotency key cùng payload trả cùng kết quả.
265. Same key khác payload báo conflict.
266. Domain events được phát.
267. Event consumers idempotent.
268. Executive Dashboard đúng scope.
269. Sales Dashboard đúng scope.
270. Marketing Dashboard đúng scope.
271. Inventory Dashboard đúng scope.
272. Finance Dashboard đúng scope.
273. Revenue Dashboard đúng scope.
274. Commission Dashboard đúng scope.
275. SLA Dashboard đúng scope.
276. Data Quality Dashboard đúng scope.
277. Sale không xem sale khác.
278. Team Lead không xem Department ngoài Team.
279. Marketing không xem Commission cá nhân.
280. Accounting không xem Interaction content mặc định.
281. Project Access không mở Customer detail.
282. Export không vượt permission.
283. Snapshot báo cáo có thể tái tạo.
284. Forecast và Actual không bị trộn.
285. Target và Forecast không bị trộn.
286. Gross Contract Value và Revenue không bị trộn.
287. Buyer Payment và Revenue không bị trộn.
288. Marketing Sourced và Influenced không bị trộn.
289. Projection và source of truth không bị trộn.
290. Metric Version được truy vết đầy đủ.
291. Dashboard Version được truy vết đầy đủ.
292. Report Version được truy vết đầy đủ.
293. Snapshot Version được truy vết đầy đủ.
294. Forecast Version được truy vết đầy đủ.
295. Data cutoff được hiển thị.
296. Data freshness được hiển thị.
297. Data quality được hiển thị.
298. Scope được backend enforce.
299. Field masking được backend enforce.
300. Capability hợp nhất dữ liệu owning Contexts mà không tạo nguồn chân lý nghiệp vụ thứ hai.

---

# 195. Quan hệ canonical với các Context liên quan

## 195.1. Platform Context

Analytics sử dụng versioned configuration, Business Calendar, Reporting Calendar, workflow và policy definitions.

Platform sở hữu definitions; Analytics sở hữu analytical runtime instances và versions.

## 195.2. IAM Context

Analytics sử dụng authenticated identity, organization history, effective scope, delegation, Legal Entity/Project access và field authorities.

Analytics access policy không thay IAM permission source. Backend scope resolution không tin URL/client parameters.

## 195.3. Lead và Party Contexts

Analytics sử dụng accepted Lead/Party facts, source snapshots, identity redirects và histories.

Analytics không sửa Lead/Customer hoặc tạo identity cạnh tranh. Merge phải tránh duplicate Metrics và giữ lineage.

## 195.4. Product và Matching Contexts

Analytics sử dụng Product availability/lock facts và Matching outcomes.

Available Inventory phải theo Product rules; Matching score không tự đồng nghĩa Deal conversion.

## 195.5. Transaction Context

Analytics sử dụng Deal, stage history, Booking và operational forecast inputs.

Forecast Override trong Analytics không sửa Deal probability/source state.

## 195.6. Contract Context

Analytics sử dụng Contract, Receivable, Payment, Allocation, Receipt, Refund và Settlement facts.

Buyer Payment, gross funds và Contract Value không mặc định là Revenue.

## 195.7. Revenue Context

Revenue và Commission Metrics phải dựa trên accepted Revenue Context facts.

Analytics không tạo Revenue Entitlement, Recognition, Payable hoặc Payout truth.

## 195.8. Activity và Marketing Contexts

Analytics sử dụng Activity/SLA/NBA và Marketing Campaign/Spend/Attribution facts.

Dashboard không thay Activity workflow; Marketing influence không thay Sales Attribution hoặc Commission.

## 195.9. Documents, Integration, Operations và Audit

- Documents sở hữu Report/Export artifacts.
- Integration sở hữu BI/warehouse/ERP/provider transport.
- Operations sở hữu scheduler, queues, retries và incidents.
- Audit sở hữu immutable Audit facts.

---

# 196. Anti-patterns và canonical requirements

## AP-ANA-001 — Mỗi Dashboard tự viết công thức KPI

**Không được áp dụng**

Widget hoặc Report nhúng công thức riêng không có Metric Version và certification.

**Canonical requirement**

Dashboard/Report phải tham chiếu versioned Semantic Metric; formula, grain, filters, time, currency, access và lineage được quản trị tập trung.

## AP-ANA-002 — Analytics là nguồn chân lý nghiệp vụ thứ hai

**Không được áp dụng**

Projection hoặc Snapshot được dùng để sửa hoặc thay source aggregate.

**Canonical requirement**

Analytics là read-only đối với business truth. Source correction đi qua owning Context; analytical adjustment/restatement phải tách biệt.

## AP-ANA-003 — Sửa số trực tiếp để khớp báo cáo

**Không được áp dụng**

Analyst update projection, Snapshot item hoặc Metric output để đạt số mong muốn.

**Canonical requirement**

Sửa source qua governed request hoặc tạo approved Reporting Adjustment/Restatement có reason, delta và lineage.

## AP-ANA-004 — Dùng current state để giả lập lịch sử

**Không được áp dụng**

Lọc `created_at` trên trạng thái hiện tại để tái tạo Pipeline, organization hoặc Inventory quá khứ.

**Canonical requirement**

As-of reporting phải dùng history, effective dates, Events, bitemporal facts hoặc locked Snapshot.

## AP-ANA-005 — Frontend quyết định scope

**Không được áp dụng**

Tin `scope=all`, `owner_id`, `department_id` hoặc filters do client gửi để mở rộng dữ liệu.

**Canonical requirement**

Backend resolve authorized scope từ IAM và intersect với Dashboard, Widget, Metric và user-selected filters.

## AP-ANA-006 — Aggregate access đồng nghĩa detail/export access

**Không được áp dụng**

Xem tổng số Contract rồi tự được xem Customer list, documents hoặc export.

**Canonical requirement**

Aggregate, breakdown, detail, source-resource, sensitive-field và export permissions phải tách biệt.

## AP-ANA-007 — Dashboard share cấp data access

**Không được áp dụng**

Share Dashboard definition làm người nhận thấy dữ liệu ngoài quyền.

**Canonical requirement**

Mỗi query được authorize lại theo principal hiện tại; sharing chỉ chia definition/layout.

## AP-ANA-008 — Scheduled Report dùng quyền creator mãi mãi

**Không được áp dụng**

Subscription chạy theo quyền lịch sử của creator hoặc gửi cho recipient inactive.

**Canonical requirement**

Re-authorize creator/recipient, current scope, masking và export policy tại mỗi execution.

## AP-ANA-009 — Cache chỉ theo URL hoặc filter

**Không được áp dụng**

Cache response được dùng chung giữa users/scopes hoặc mask tại frontend.

**Canonical requirement**

Cache key phải chứa authorized-scope/access hash, Metric Version, filters, time, currency và data version; masking thực hiện trước cache.

## AP-ANA-010 — Snapshot Locked vẫn sửa hoặc xóa

**Không được áp dụng**

Late data hoặc correction ghi đè Snapshot/reporting period đã khóa.

**Canonical requirement**

Giữ original Snapshot; tạo Restatement/Superseding version với delta, reason, approval và effective reporting treatment.

## AP-ANA-011 — Forecast, Target và Actual là một con số

**Không được áp dụng**

Dashboard trộn pipeline forecast, approved forecast, target và actual.

**Canonical requirement**

Mỗi value phải có value type, model/Metric Version, cutoff, horizon, scenario và approval state rõ ràng.

## AP-ANA-012 — Contract Value, Buyer Payment và Revenue bị đồng nhất

**Không được áp dụng**

Gọi gross funds hoặc Contract Value là Revenue; tính Commission Paid từ approved payout chưa có confirmation.

**Canonical requirement**

Dùng accepted Contract/Revenue facts và Metric codes chỉ rõ basis: Contract, Receivable, Payment, Revenue Entitlement, Recognition, Collection, Commission Payable hoặc Paid.

## AP-ANA-013 — Influenced Revenue cộng dồn naïve

**Không được áp dụng**

Cộng Marketing-influenced value của nhiều Campaign như Revenue độc lập.

**Canonical requirement**

Influenced metrics phải công bố non-additivity/double-counting; sourced/allocated Metrics tuân Attribution Model Version.

## AP-ANA-014 — Data Quality hoặc Anomaly tự sửa/kết luận

**Không được áp dụng**

DQ test sửa source record hoặc anomaly gắn nhãn gian lận/kỷ luật.

**Canonical requirement**

Analytics tạo signal, evidence, issue hoặc source-correction request; owning process/human review quyết định hành động.

## AP-ANA-015 — Analytics sở hữu artifacts, provider runtime hoặc permissions

**Không được áp dụng**

Analytics lưu binary report, BI credentials, raw connector retries hoặc tạo permission universe cạnh tranh.

**Canonical requirement**

Documents sở hữu artifacts; Integration sở hữu transport; Operations sở hữu runtime; IAM/Security sở hữu principal và authorization sources.

## AP-ANA-016 — Candidate examples là exact contracts

**Không được áp dụng**

Dùng table names, endpoints, statuses, Events, permissions, formulas, SLA hoặc thresholds trong tài liệu này để code trực tiếp.

**Canonical requirement**

Exact database, API, Event, lifecycle, permission, Metric, Forecast, integration và operational contracts phải được khóa trong nguồn canonical tương ứng.

## AP-ANA-017 — Operational projections là statutory reporting

**Không được áp dụng**

Dùng CRM Analytics thay General Ledger, payroll, bank hoặc báo cáo pháp định mà không reconciliation và labeling.

**Canonical requirement**

Analytics chỉ cung cấp operational/management reporting; external statutory systems giữ source of truth tương ứng.

## AP-ANA-018 — Mặc định tồn tại hệ thống tiền nhiệm

**Không được áp dụng**

Tự thiết kế old-metric aliases, compatibility layer hoặc historical mappings khi chưa có approved scope.

**Canonical requirement**

`crm_bds_ai` là Greenfield. Historical import/backfill chỉ tồn tại khi có scope, source mapping, security review, reconciliation và acceptance criteria riêng.

---

# 197. Kết luận

Analytics Capability là lớp Semantic Analytics và Management Reporting thống nhất của `crm_bds_ai`.

Capability phải bảo đảm:

- Business truth vẫn thuộc owning Contexts.
- Analytics read-only đối với source aggregates.
- Projection, aggregate, Snapshot và Forecast không trở thành source truth thứ hai.
- Mỗi Dataset và Metric có version, grain, time, currency, access và lineage.
- Certified Metric, Published Dashboard, Locked Snapshot và Locked Forecast không sửa trực tiếp.
- Dashboard/Report chỉ dùng governed Metric Versions.
- Target, Actual, Snapshot, Restatement và Forecast được tách biệt.
- Contract Value, Buyer Payment, Revenue, Revenue Collected và Commission không bị đồng nhất.
- Backend resolve và intersect scope; frontend filter chỉ thu hẹp.
- Aggregate, breakdown, detail, source-resource và export access được tách.
- Field masking áp dụng trước cache, export, scheduled delivery và BI publication.
- Drill-through quay về API/workspace của owning Context.
- Snapshot giữ cutoff, versions, freshness, quality và original history.
- As-of reporting dùng history/effective-time/Event/Snapshot facts.
- Forecast có model version, input snapshot, cutoff, confidence, override, approval và lock.
- Data Freshness luôn được hiển thị.
- Data Quality, Reconciliation, Alert và Anomaly không tự sửa source hoặc kết luận gian lận.
- Scheduled Report re-authorize mỗi lần chạy.
- Report/Export artifacts thuộc Documents; BI transport thuộc Integration.
- Cache/query scope-aware và sensitive access có Audit.
- External BI chỉ nhận governed Dataset với least privilege, masking, expiry và traceability.
- CRM Analytics không thay ERP, payroll, bank hoặc statutory reporting.

> Analytics Context giải thích, tổng hợp và dự báo dữ liệu; nó không sở hữu hoặc thay đổi business truth của các Context nguồn.
