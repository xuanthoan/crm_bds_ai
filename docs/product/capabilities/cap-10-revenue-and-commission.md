# CRM_BDS_AI — CAPABILITY 10: REVENUE AND COMMISSION

## Transaction Revenue, Distribution/Brokerage Fees, Internal Commission, Reconciliation, Payout Orchestration and Clawback

**Document ID:** `PROD-CAP-REV-001`
**Canonical path:** `docs/product/capabilities/cap-10-revenue-and-commission.md`
**Product:** `crm_bds_ai`
**Version:** `1.0.0`  
**Status:** `Accepted / Product Capability Baseline`
**Document type:** `Product Capability Specification`
**Primary capability code:** `CAP-REV`
**Primary owning Context:** `revenue`
**Owner:** `Product Owner`
**Co-owner:** `Revenue Domain Owner`
**Reviewers:** `Architecture Owner`, `Contract Domain Owner`, `Transaction Domain Owner`, `IAM Domain Owner`, `Party Domain Owner`, `Product Domain Owner`, `Documents Owner`, `Integration Owner`, `Analytics Owner`, `Audit Owner`, `Security Owner`, `Database Owner`, `API Owner`, `Event Architecture Owner`, `Operations Owner`, `QA Owner`
**Effective date:** `2026-08-05`  
**Last reviewed:** `2026-08-05`  
**Classification:** `INTERNAL`

---

# 0. Phạm vi thẩm quyền và quan hệ tài liệu

Tài liệu này là nguồn canonical cho:

- Product outcomes của Revenue and Commission Capability.
- Business meanings của Revenue Arrangement, Revenue Entitlement, operational Revenue Recognition, Revenue Receivable, Revenue Payment Application và Revenue Reconciliation.
- Business meanings của Commission Plan, Participant Snapshot, Commission Entitlement, Recognition, Vesting, Payable, Payout orchestration, Advance, Clawback và Negative Balance.
- Capability boundaries, invariants, acceptance outcomes và anti-patterns.
- Đầu vào phân tích cho Revenue Context Implementation Pack.

Tài liệu này không phải nguồn exact cho:

- Physical database schema hoặc DDL.
- Exact API paths, request/response payloads.
- Exact Event names, envelope hoặc payloads.
- Exact permission codes, scopes, masking hoặc role matrix.
- Exact state machines, status codes, formula syntax, rates, tiers, milestones hoặc rounding.
- Exact Contract, Payment, Receipt, Allocation hoặc Settlement behavior.
- Exact bank/payroll/ERP payout execution.
- Exact tax, withholding, General Ledger hoặc statutory accounting treatment.
- Exact certified Revenue/Commission Metrics hoặc predictive forecast.
- Exact screen routes, queue, retry, retention hoặc deployment configuration.

Nguồn exact tương ứng:

| Chủ đề | Nguồn canonical |
|---|---|
| Thuật ngữ | Domain Glossary |
| Product requirements | PRD |
| Context ownership | Source of Truth Matrix |
| Architecture boundaries | Architecture Overview, Context Map và Accepted ADRs |
| Revenue behavior chi tiết | Revenue Context Implementation Pack |
| Database | Revenue Context DB Specification và Alembic historical imports |
| API | OpenAPI |
| Events | JSON Schema, AsyncAPI và Event Registry |
| Permissions/scopes/masking/SoD | Security registries và matrices |
| Contract/Payment/Receipt/Allocation/Settlement | Contract Context contracts |
| Deal/participant/co-sale agreement | Transaction Context contracts |
| Workforce/employment/organization | IAM Context contracts |
| Party/beneficiary/referrer identity | Party Context contracts |
| Product/Project/Listing/Selling Right | Product Context contracts |
| File/Document/statement evidence | Documents Context contracts |
| Bank/payroll/ERP/provider execution | Integration Context contracts |
| Certified Revenue/Commission Metrics | Analytics Context và Metric Registry |
| Immutable Audit facts | Audit Context |
| Runtime jobs/incidents | Operations Context |
| Công việc hiện tại | Current Sprint Detailed Execution Pack |

**Capability không đồng nghĩa Bounded Context.** Capability này chủ yếu được thực hiện bởi `revenue` Context. Nó tính toán và quản trị quyền lợi thương mại cùng hoa hồng nội bộ, nhưng không được direct-write dữ liệu thuộc `contract`, `transaction`, `iam`, `party`, `product`, `documents`, `integration`, `analytics` hoặc `audit`.

Các phần candidate lifecycle, data model, operations, permissions, Events, screens, formulas và reports chỉ là design input. Chúng không được dùng thay machine-readable contracts hoặc Context Packs đã được chấp nhận.

---
# 1. Mục tiêu của capability

Revenue and Commission Capability quản lý hai lớp tài chính thương mại độc lập nhưng liên hệ chặt chẽ:

## 1.1. Revenue Management

Xác định:

- Công ty có quyền hưởng khoản doanh thu, phí hoặc lợi ích thương mại nào.
- Quyền hưởng phát sinh từ Contract, Agreement, Mandate, service hoặc milestone nào.
- Legal Entity nào là beneficiary.
- Counterparty nào có nghĩa vụ thanh toán.
- Calculation base, rate, tier, formula và version nào được sử dụng.
- Khi nào Revenue Entitlement hình thành.
- Khi nào đủ điều kiện operational recognition trong CRM.
- Khi nào trở thành Revenue Receivable.
- Contract Payment Allocation nào được áp dụng vào Revenue Receivable.
- Khoản nào đang holdback, overdue, disputed hoặc cần reconciliation.
- Khi nào phải adjustment, reversal hoặc reclassification.

## 1.2. Internal Commission Management

Xác định:

- Beneficiary nào được hưởng Commission.
- Participant role và co-sale agreement nào là căn cứ.
- Funding Source nào tài trợ Commission.
- Commission Plan, base, rate, pool, tier và milestone nào được sử dụng.
- Khi nào Entitlement được calculated, recognized, vested và payable.
- Khoản nào đã được đưa vào payout period/batch.
- Payout execution nào đã được external system xác nhận.
- Khoản nào bị holdback, disputed, clawed back hoặc tạo Negative Balance.
- Advance được thu hồi hoặc offset như thế nào.
- Offboarding ảnh hưởng quyền lợi đã hình thành ra sao.

Capability phải trả lời được:

- Gross transaction funds khác company Revenue như thế nào.
- Financial nature nào là property principal, fee, collected-on-behalf, escrow hoặc beneficiary proceeds.
- Một Contract tạo những Revenue Models nào.
- Revenue Arrangement và Rule Version nào áp dụng.
- Revenue Entitlement, Recognition, Receivable và Collected Revenue đang ở mức nào.
- Partner Statement và internal calculation chênh lệch ra sao.
- Revenue Adjustment ảnh hưởng Commission nào.
- Commission Plan và Funding Source nào áp dụng.
- Participant Snapshot nào được dùng.
- Handover hoặc organization change có làm thay quyền lợi lịch sử không.
- Payout approval khác payment execution như thế nào.
- Clawback tác động phần unpaid và paid ra sao.
- Toàn bộ calculation có tái tạo được từ source versions, snapshots và Events hay không.

Capability phải hỗ trợ:

- Property Sales Revenue của công ty tự phát triển hoặc sở hữu tài sản.
- Distribution Commission.
- Brokerage, Service, Referral, Marketing và Management Fees.
- Project/volume/performance bonus.
- Nhiều Revenue Models cho một giao dịch.
- Nhiều Legal Entities và counterparties.
- Percentage, fixed, tiered, milestone, formula và hybrid calculations.
- Holdback, dispute, adjustment, reversal và reconciliation.
- Revenue Receivable và many-to-many Revenue Payment Application.
- Sale, co-sale, management, referral và support commissions.
- Role pools, tiers, funding budgets và multiple milestones.
- Recognition, Vesting, Payable và Payout tách biệt.
- Advance, partial payout, holdback, dispute và Clawback.
- Negative Balance, future offset, repayment và approved waiver.
- Multi-Legal Entity payout orchestration.
- Full versioning, traceability, SoD và Audit evidence.
- Integration với payroll/bank/ERP mà không thay các hệ thống pháp định.

Nguyên tắc canonical:

> Gross transaction funds, company Revenue, Revenue Receivable, collected Revenue, Commission Entitlement, Commission Payable và executed Payout là các lớp dữ liệu riêng. Revenue Context chỉ tạo quyền lợi từ căn cứ có version và không được sửa dữ liệu nguồn hoặc giả lập bank/payroll/accounting truth.

---
# 2. Vị trí của capability trong kiến trúc

Revenue Context sử dụng:

- `platform`: configuration, Workflow/Approval/SLA definitions, Business Calendar, formula governance và effective-dating policy.
- `iam`: canonical Workforce/Employment/Organization assignments, authenticated identity, authorization, delegation và SoD decisions.
- `party`: canonical Party identity cho Counterparty, Beneficiary, Referrer và External Collaborator.
- `lead`: source/attribution references khi được công bố.
- `product`: Project, Listing, Transaction Model, Company Role và Selling Right references.
- `matching`: conversion references khi cần analytical lineage.
- `transaction`: Deal, Transaction Case, Booking, primary responsibility, participants và approved Co-sale Agreement Version.
- `contract`: Contract, Contract Version, financial components, Payment/Allocation/Receipt, Refund, Forfeiture, Settlement, Cancellation và Reversal facts.
- `documents`: Partner Statement, Commission Statement và supporting-document references.
- `integration`: payroll/bank/ERP/provider transport, payout instructions, external confirmations và reconciliation evidence.
- `analytics`: certified Revenue/Commission metrics và predictive forecasts.
- `audit`: immutable evidence của governed financial actions.
- `operations`: batch calculation, period closing, retries và incident runtime.

Revenue Context cung cấp:

- Cho `transaction`: governed Revenue/Commission summaries; không sửa Deal hoặc co-sale agreement.
- Cho `contract`: Revenue/Commission impact facts; không sửa Payment, Receipt, Refund hoặc Settlement.
- Cho `analytics`: versioned Revenue/Commission facts; Analytics định nghĩa certified metrics.
- Cho payroll/bank/ERP qua `integration`: approved payout instructions và references.
- Cho beneficiaries: permission-aware statements và explanations.
- Cho management: operational projections có freshness/version metadata.

Luồng Revenue:

```text
Contract/Agreement/Mandate facts
→ Revenue Arrangement Resolution
→ Revenue Entitlement
→ Operational Recognition
→ Revenue Receivable
→ Contract Payment Application
→ Partner Reconciliation
→ Adjustment/Reversal khi cần
```

Luồng Commission:

```text
Transaction/Contract/Revenue facts
→ Commission Plan Resolution
→ Participant Snapshot
→ Commission Entitlement
→ Recognition
→ Vesting
→ Payable
→ Payout Period/Batch
→ Integration Payment Confirmation
```

Luồng Clawback:

```text
Contract/Payment/Refund/Revenue Adjustment Fact
→ Commission Impact Analysis
→ Clawback Case
→ Reverse Unpaid / Offset / Recovery
→ Reconciliation
```

Cross-context propagation dùng local transactions, Transactional Outbox, idempotent commands/consumers, Process Manager và reconciliation. Không dùng distributed transaction hoặc cross-schema business writes.

---
# 3. Ranh giới sở hữu dữ liệu

## 3.1. Revenue Context sở hữu

### Revenue

- Revenue Arrangement, Version và Rule Set/Version.
- Revenue Model và calculation policy references.
- Revenue Entitlement, components và calculation snapshots.
- Revenue Milestone và operational Recognition.
- Revenue Receivable, adjustments, holdback và reversal.
- Revenue Payment Application tham chiếu Contract Payment Allocation.
- Unallocated Revenue Fund representation trong Revenue domain.
- Partner/Developer Revenue Statement business record và versions.
- Revenue Reconciliation Case và Revenue Dispute.
- Revenue Attribution và operational Forecast inputs/projections.
- Revenue-originated business facts và Audit requests.

### Internal Commission

- Commission Plan, Version, rules, tiers và role pools.
- Commission Participant Snapshot được tạo từ published source facts.
- Commission Entitlement, components và calculation snapshots.
- Commission Milestone, Recognition, Vesting, Holdback và Payable.
- Commission Adjustment, Dispute và Statement.
- Payout Period, Payout Batch, allocations và payout-instruction intent.
- External payout-confirmation projection/reference.
- Commission Advance và recovery state.
- Clawback Case, items, recovery và Negative Balance.
- Commission-originated business facts và Audit requests.

## 3.2. Revenue Context không sở hữu

- Contract, Contract Financial Component, Payment Transaction, Allocation, Receipt, Refund, Forfeiture source hoặc Transaction Settlement: `contract`.
- Deal, Transaction Case, Booking, responsibility, participant source hoặc Co-sale Agreement: `transaction`.
- Workforce, Employment Assignment, Organization hierarchy hoặc user lifecycle: `iam`.
- Canonical Party/Customer identity: `party`.
- Project, Asset, Listing, Selling Right hoặc Availability: `product`.
- Binary File, Document, Document Version hoặc signed statement evidence: `documents`.
- Payroll, bank, ERP, payment-provider transport, credentials, instruction delivery hoặc external execution truth: `integration`/external system.
- Certified Revenue/Commission KPIs, predictive forecast hoặc profitability metrics: `analytics`.
- Immutable Audit facts: `audit`.
- General Ledger, payroll master, statutory tax calculation hoặc statutory statements: external accounting/payroll/tax systems.
- Job, queue, retry/DLQ hoặc incident runtime: `operations`.

## 3.3. Source data immutability

Revenue Context không được:

- Sửa Contract Value hoặc Contract financial components.
- Sửa Payment, Allocation, Receipt, Refund hoặc Settlement.
- Sửa Deal responsibility hoặc Co-sale Agreement.
- Sửa Lead attribution.
- Sửa Workforce/Employment history.
- Sửa Product hoặc Party identity.

Khi nguồn sai, Revenue tạo Source Correction Request, Reconciliation Case hoặc governed Adjustment/Clawback dựa trên accepted source corrections.

## 3.4. Revenue Payment Application

Payment Transaction và Payment Allocation thuộc Contract Context.

Revenue Context chỉ tạo Revenue Payment Application:

- Tham chiếu accepted Payment Allocation.
- Phân bổ amount vào Revenue Receivable.
- Giữ idempotency, reversal và reconciliation state.
- Không sao chép bank transaction thành source mới.
- Không tự xác nhận money movement.

## 3.5. Payout execution boundary

Revenue Context sở hữu:

- Payout eligibility.
- Period/batch calculation.
- Approval state.
- Payout instruction intent.
- Reconciliation state.
- External confirmation reference.

Integration/payroll/bank/ERP sở hữu:

- Instruction transport.
- Beneficiary account delivery.
- Provider response.
- External payment execution.
- Payroll posting.
- Bank transaction truth.

Batch `APPROVED` hoặc instruction `CREATED` không đồng nghĩa `PAID`.

## 3.6. Analytics và statutory boundaries

Revenue Context có thể tạo operational forecasts và projections.

Analytics Context sở hữu certified Revenue, Commission, payout, clawback và profitability Metrics.

Accounting/payroll/tax systems sở hữu statutory recognition, General Ledger, payroll truth, withholding/tax calculations và official reporting khi áp dụng.

---
# 4. Các lớp dữ liệu bắt buộc phải tách

## 4.1. Gross Transaction Value

Tổng giá trị giao dịch bất động sản.

Không mặc định là doanh thu công ty.

## 4.2. Revenue Entitlement

Quyền thương mại của công ty được hưởng một khoản tiền.

Ví dụ:

* Công ty được hưởng 3% giá trị hợp đồng.
* Công ty được hưởng phí môi giới 100 triệu đồng.
* Công ty được hưởng doanh thu bán bất động sản.
* Công ty được hưởng phí Marketing.

## 4.3. Revenue Recognition

Sự kiện nghiệp vụ xác định một phần hoặc toàn bộ Revenue Entitlement đã đủ điều kiện được ghi nhận trong CRM.

Đây là ghi nhận vận hành, không mặc định là ghi nhận kế toán pháp định.

## 4.4. Revenue Receivable

Khoản đối tác, Customer hoặc bên khác phải trả cho công ty.

## 4.5. Revenue Payment

Tiền thực tế đã nhận và được phân bổ cho Revenue Receivable.

Payment nguồn thuộc Contract and Cash Capability.

## 4.6. Internal Commission Entitlement

Quyền nội bộ của sale, co-sale hoặc beneficiary được hưởng hoa hồng.

## 4.7. Commission Payable

Khoản hoa hồng đã đủ điều kiện thanh toán.

## 4.8. Commission Payout

Khoản tiền hoa hồng thực tế đã được chi.

## 4.9. Clawback

Khoản hoa hồng đã ghi nhận hoặc đã chi cần được hoàn nhập, bù trừ hoặc thu hồi.

---

# 5. Thuật ngữ chuẩn

## 5.1. Revenue Arrangement

Căn cứ thương mại xác định công ty được hưởng doanh thu như thế nào.

Nguồn có thể là:

* Distribution Agreement.
* Brokerage Agreement.
* Consignment Agreement.
* Cooperation Agreement.
* Project sales policy.
* Internal sales budget policy.
* Service Agreement.
* Referral Agreement.
* Contract Financial Component.

## 5.2. Revenue Entitlement

Kết quả tính quyền hưởng cho một giao dịch hoặc một kỳ.

## 5.3. Revenue Recognition Basis

Sự kiện làm cho doanh thu đủ điều kiện ghi nhận nghiệp vụ.

## 5.4. Commission Plan

Bộ rule xác định hoa hồng nội bộ.

## 5.5. Commission Entitlement

Khoản hoa hồng dự kiến hoặc đã hình thành cho một beneficiary.

## 5.6. Beneficiary

Người hoặc tổ chức được hưởng hoa hồng:

* Employee.
* User.
* Sale.
* Manager.
* External collaborator.
* Referrer.
* Partner.

## 5.7. Funding Source

Nguồn tài chính được dùng để chi hoa hồng.

## 5.8. Recognition

Đủ điều kiện ghi nhận quyền hưởng.

## 5.9. Vesting

Quyền hưởng trở nên không còn phụ thuộc một số điều kiện nhất định, trừ clawback.

## 5.10. Payable

Đủ điều kiện đưa vào kỳ chi trả.

---

# 6. Transaction models và Revenue scenarios

## 6.1. Công ty tự phát triển và bán sản phẩm

```text
Transaction Model:
OWN_DEVELOPMENT_SALE

Revenue Model:
PROPERTY_SALES_REVENUE

Revenue Payer:
Buyer

Revenue Beneficiary:
Seller/Developer Legal Entity nội bộ

Internal Commission Funding:
PROPERTY_SALES_BUDGET
```

Đặc điểm:

* Gross Contract Value có thể là nguồn doanh thu bán hàng.
* Các khoản thu hộ, thuế, phí không thuộc doanh thu phải tách riêng.
* Internal Commission không chờ một Developer bên ngoài thanh toán phí.
* Hoa hồng có thể phụ thuộc Contract, Payment Milestone hoặc ngân sách bán hàng.

## 6.2. Phân phối dự án chủ đầu tư bên ngoài

```text
Transaction Model:
THIRD_PARTY_PRIMARY_DISTRIBUTION

Revenue Model:
DISTRIBUTION_COMMISSION

Revenue Payer:
Developer / Master Agent / Partner

Revenue Beneficiary:
Internal Legal Entity

Internal Commission Funding:
EXTERNAL_DISTRIBUTION_COMMISSION
```

Đặc điểm:

* Buyer money trả Developer không phải doanh thu của công ty.
* Công ty có Revenue Entitlement riêng từ Developer.
* Revenue Recognition có thể phụ thuộc Contract, Buyer payment hoặc Developer confirmation.
* Commission nội bộ có thể chỉ payable sau khi công ty nhận được tiền.

## 6.3. Customer ký gửi hoặc bán lại

```text
Transaction Model:
SECONDARY_CONSIGNMENT_SALE

Revenue Model:
BROKERAGE_FEE / SERVICE_FEE

Revenue Payer:
Seller, Buyer hoặc cả hai

Revenue Beneficiary:
Internal Legal Entity

Internal Commission Funding:
BROKERAGE_FEE
```

Đặc điểm:

* Buyer purchase money chủ yếu thuộc Owner/Seller.
* Brokerage Fee phải tách khỏi Owner Proceeds.
* Nếu công ty thu hộ toàn bộ tiền, phần Owner Proceeds không phải Revenue.
* Hoa hồng có thể chia buyer-side, seller-side và closing-side.

## 6.4. Tài sản công ty sở hữu

```text
Revenue Model:
PROPERTY_SALES_REVENUE

Funding Source:
COMPANY_SALES_BUDGET
```

Có thể có:

* Seller Legal Entity khác Owner Legal Entity.
* Intercompany allocation.
* Internal sales budget.

## 6.5. Tài sản Partner

Có thể phát sinh:

* Brokerage Fee.
* Distribution Fee.
* Service Fee.
* Referral Fee.
* Profit-sharing.

## 6.6. Brokerage-only

Công ty chỉ giới thiệu hoặc kết nối.

Không quản lý toàn bộ Buyer payment.

Revenue có thể là:

* Fixed referral fee.
* Percentage fee.
* Success fee.

---

# 7. Candidate Revenue Model vocabulary — Context-specific, pending validation

> Exact model codes, tax/accounting mapping và applicability thuộc Revenue Context Pack.

Các mã chuẩn:

```text
PROPERTY_SALES_REVENUE
DISTRIBUTION_COMMISSION
BROKERAGE_FEE
SERVICE_FEE
REFERRAL_FEE
MARKETING_FEE
MANAGEMENT_FEE
SUCCESS_FEE
CONSULTING_FEE
PROJECT_BONUS
SALES_VOLUME_BONUS
PERFORMANCE_BONUS
PARTNER_INCENTIVE
FORFEITURE_REVENUE
OTHER_REVENUE
```

Một Contract hoặc Transaction Case có thể tạo nhiều Revenue Model.

Ví dụ:

* Brokerage Fee.
* Service Fee.
* Documentation Fee.

---

# 8. Financial Nature và Revenue Candidate

Accepted Contract Financial Component fact có thể cung cấp:

```text
is_revenue_candidate = true/false
```

Tuy nhiên `is_revenue_candidate=true` không tự tạo Revenue Recognition.

Revenue Context phải:

1. Resolve Revenue Arrangement.
2. Kiểm tra rule.
3. Tính Revenue Entitlement.
4. Kiểm tra milestone.
5. Ghi nhận theo workflow.

---

# 9. Revenue Arrangement

## 9.1. Nội dung

* Arrangement code.
* Internal Legal Entity.
* Counterparty.
* Project.
* Transaction Model.
* Revenue Model.
* Agreement reference.
* Mandate reference.
* Effective dates.
* Currency.
* Calculation method.
* Recognition basis.
* Receivable basis.
* Payment terms.
* Holdback.
* Bonus rules.
* Adjustment rules.
* Tax/withholding references.
* Status.
* Version.

## 9.2. Scope

Revenue Arrangement có thể áp dụng cho:

* Toàn Partner.
* Một Project.
* Một Sales Launch.
* Một Listing group.
* Một Contract type.
* Một Legal Entity.
* Một kênh.
* Một thời kỳ.
* Một Deal cụ thể.

## 9.3. Không mặc định dùng Agreement mới cho giao dịch cũ

Phải resolve theo:

* Contract date.
* Booking date.
* Revenue milestone date.
* Effective date policy.

---

# 10. Candidate Revenue Arrangement lifecycle — pending validation

> Exact states, transitions và activation guards thuộc Revenue Context Implementation Pack.

```text
DRAFT
PENDING_REVIEW
PENDING_APPROVAL
ACTIVE
SUSPENDED
EXPIRED
TERMINATED
REPLACED
ARCHIVED
```

Revenue Entitlement mới không được tạo từ Arrangement không active, trừ approved correction or historical-import workflow.

---

# 11. Candidate Revenue calculation methods — pending validation

> Exact methods và formula contracts thuộc versioned Revenue Rule definitions.

```text
PERCENTAGE_OF_CONTRACT_VALUE
PERCENTAGE_OF_NET_PROPERTY_VALUE
PERCENTAGE_OF_COLLECTED_AMOUNT
PERCENTAGE_OF_OWNER_PROCEEDS
PERCENTAGE_OF_BROKERAGE_BASE
FIXED_AMOUNT
FIXED_AMOUNT_PER_UNIT
TIERED_PERCENTAGE
MARGINAL_TIER
CUMULATIVE_VOLUME_TIER
FORMULA_BASED
MANUAL_APPROVED
PROFIT_SHARE
MILESTONE_BASED
HYBRID
```

---

# 12. Candidate Revenue calculation bases — pending validation

> Exact base definitions, included/excluded financial components và source contracts thuộc Revenue Rule Registry.

Các base chuẩn:

```text
GROSS_CONTRACT_VALUE
NET_PROPERTY_VALUE
PROPERTY_PRINCIPAL
NET_OF_TAX
NET_OF_DISCOUNT
NET_OF_REFUND
NET_OF_OWNER_DEDUCTION
BROKERAGE_FEE_BASE
SERVICE_FEE_BASE
ACTUAL_COLLECTED_AMOUNT
ELIGIBLE_COLLECTED_AMOUNT
SETTLED_OWNER_PROCEEDS
UNIT_COUNT
AREA
FIXED_BUDGET
CUSTOM_FORMULA
```

Mỗi calculation snapshot phải ghi rõ base được dùng.

---

# 13. Illustrative percentage calculation — không phải production formula

> Công thức minh họa chỉ thể hiện principle; exact precision, rounding, caps và adjustments thuộc Rule Version.

Illustrative formula:

```text
Revenue Entitlement
=
Eligible Base
× Revenue Rate
```

Phải lưu:

* Eligible Base.
* Rate.
* Rounding.
* Currency.
* Minimum.
* Maximum.
* Cap.
* Adjustment.
* Version.

---

# 14. Doanh thu theo bậc

Ví dụ:

* Dưới 10 sản phẩm: 2%.
* Từ 10 đến 20 sản phẩm: 2,5%.
* Trên 20 sản phẩm: 3%.

Phải phân biệt:

## 14.1. Whole-volume tier

Khi đạt bậc, toàn bộ doanh số được áp dụng tỷ lệ mới.

## 14.2. Marginal tier

Mỗi phần doanh số áp dụng tỷ lệ khác nhau.

## 14.3. Retroactive tier

Đạt ngưỡng mới tạo adjustment cho giao dịch trước.

Không được áp dụng hồi tố nếu Agreement không quy định.

---

# 15. Bonus theo doanh số

Có thể tính theo:

* Số Contract.
* Tổng giá trị.
* Tổng Buyer payment.
* Tổng Revenue.
* Tỷ lệ hấp thụ.
* Thời hạn.
* Project.
* Team.
* Legal Entity.

Bonus phải là Revenue Entitlement riêng, không ghi đè commission cơ bản.

---

# 16. Revenue Calculation Snapshot

Mọi Revenue Entitlement phải lưu:

* Source Contract.
* Contract Version.
* Transaction Case.
* Deal.
* Project.
* Listing.
* Internal Legal Entity.
* Counterparty.
* Arrangement Version.
* Calculation method.
* Base.
* Rate.
* Tier.
* Formula.
* Gross amount.
* Deductions.
* Net entitlement.
* Currency.
* Rounding.
* Calculation timestamp.
* Calculation engine version.

---

# 17. Revenue Entitlement

## 17.1. Khái niệm

Revenue Entitlement là quyền công ty được hưởng một khoản doanh thu.

## 17.2. Có thể tạo khi

* Contract effective.
* Contract signed.
* Booking confirmed.
* Buyer payment đạt milestone.
* Owner Settlement được tính.
* Developer confirmation.
* Sales volume threshold đạt.
* Service hoàn thành.
* Approved manual adjustment.

## 17.3. Revenue Entitlement không đồng nghĩa Receivable

Entitlement có thể:

* Chưa đến hạn thu.
* Chờ xác nhận đối tác.
* Chờ milestone.
* Bị holdback.

---

# 18. Candidate Revenue Entitlement lifecycle — pending validation

> Exact states/transitions thuộc Revenue Context Pack.

```text
DRAFT
CALCULATED
PENDING_VALIDATION
PENDING_EXTERNAL_CONFIRMATION
PENDING_APPROVAL
APPROVED
PARTIALLY_RECOGNIZED
FULLY_RECOGNIZED
ON_HOLD
DISPUTED
ADJUSTMENT_PENDING
REVERSED
CANCELLED
CLOSED
```

---

# 19. Revenue Entitlement Component

Một Entitlement có thể gồm:

* Base commission.
* Additional bonus.
* Marketing fee.
* Service fee.
* Retention.
* Holdback.
* Tax deduction reference.
* Adjustment.

Không gộp mọi khoản thành một amount không giải thích.

---

# 20. Candidate Revenue Milestone vocabulary — pending validation

> Exact milestones và source Event contracts thuộc Revenue Context Pack và Event Registry.

Các milestone tham khảo:

```text
CONTRACT_SIGNED
CONTRACT_EFFECTIVE
DEPOSIT_CONFIRMED
BUYER_PAYMENT_PERCENT_REACHED
BUYER_PAYMENT_AMOUNT_REACHED
FIRST_INSTALLMENT_PAID
FULL_PAYMENT_RECEIVED
HANDOVER_COMPLETED
OWNER_SETTLEMENT_COMPLETED
DEVELOPER_CONFIRMED
DEVELOPER_STATEMENT_APPROVED
INVOICE_ISSUED
REVENUE_PAYMENT_RECEIVED
SERVICE_COMPLETED
CUSTOM_MILESTONE
```

---

# 21. Revenue Recognition Policy

Revenue Recognition trong CRM có thể dựa trên:

* Một milestone.
* Nhiều milestone.
* Tỷ lệ từng phần.
* Actual payment.
* External confirmation.
* Approved statement.

Ví dụ:

```text
30% recognized khi Contract effective.
40% recognized khi Buyer thanh toán 30%.
30% recognized khi công ty nhận phí từ Developer.
```

---

# 22. Candidate operational Revenue Recognition lifecycle — pending validation

> Đây là CRM operational recognition, không phải statutory accounting lifecycle.

```text
PENDING
ELIGIBLE
PENDING_REVIEW
RECOGNIZED
PARTIALLY_REVERSED
FULLY_REVERSED
SUSPENDED
DISPUTED
```

## 22.1. Operational recognition

Phải gắn nhãn rõ:

```text
CRM_OPERATIONAL_RECOGNITION
```

Không mặc định đồng nghĩa accounting revenue recognition.

---

# 23. Revenue Receivable

## 23.1. Khái niệm

Khoản phải thu doanh thu từ:

* Developer.
* Owner.
* Buyer.
* Partner.
* Internal Legal Entity.
* Other payer.

## 23.2. Nguồn

* Recognized Revenue.
* Agreement billing milestone.
* Approved Partner Statement.
* Brokerage Fee.
* Service Fee.
* Bonus.
* Adjustment.

---

# 24. Candidate Revenue Receivable lifecycle — pending validation

> Exact states, aging và write-off guards thuộc Revenue Context contracts.

```text
DRAFT
PENDING_ACTIVATION
OPEN
PARTIALLY_PAID
PAID
OVERDUE
ON_HOLD
DISPUTED
SUSPENDED
ADJUSTED
CANCELLED
WRITTEN_OFF
```

---

# 25. Revenue Receivable Amounts

* Original amount.
* Adjustment amount.
* Withheld amount.
* Paid amount.
* Reversed amount.
* Outstanding amount.
* Overdue amount.
* Disputed amount.
* Write-off amount.

Outstanding phải được tính.

---

# 26. Revenue Payment Application

Contract Context sở hữu Payment Transaction và Payment Allocation.

Revenue Context tạo Revenue Payment Application để tham chiếu:

* Payment Allocation ID.
* Revenue Receivable.
* Revenue Entitlement.
* Amount.
* Currency.
* Applied at.
* Status.

Không sao chép Payment Transaction hoặc Allocation thành source of truth mới.

---

# 27. Một Payment cho nhiều Revenue Receivable

Ví dụ Developer chuyển một khoản cho:

* Commission tháng 1.
* Commission tháng 2.
* Project bonus.

Phải hỗ trợ nhiều Revenue Payment Application.

---

# 28. Một Revenue Receivable nhận nhiều Payment

Ví dụ:

* Developer thanh toán 50%.
* Thanh toán phần còn lại ở kỳ sau.

Receivable giữ trạng thái `PARTIALLY_PAID`.

---

# 29. Unallocated Revenue Fund

Khi tiền nhận được xác định là doanh thu nhưng chưa xác định Entitlement:

* Lưu reference Payment.
* Counterparty.
* Amount.
* Currency.
* Received date.
* Evidence.
* Candidate Entitlements.
* Status.
* SLA.
* Assigned user.

Không tự coi là doanh thu đã đối soát.

---

# 30. Revenue Holdback

## 30.1. Khái niệm

Một phần Revenue Entitlement bị giữ lại do:

* Developer retention.
* Warranty.
* Contract risk.
* Pending documentation.
* Pending cancellation period.
* Pending settlement.
* Policy.

## 30.2. Holdback phải có

* Amount/rate.
* Reason.
* Release condition.
* Expected release date.
* Status.
* Source agreement.
* Approval.

---

# 31. Revenue Adjustment

## 31.1. Trigger

* Contract value change.
* Product change.
* Area adjustment.
* Discount change.
* Refund.
* Contract cancellation.
* Receipt reversal.
* Developer statement correction.
* Fee dispute.
* Tier threshold change.
* Manual error correction.

## 31.2. Không sửa Entitlement cũ

Tạo Adjustment record:

* Positive.
* Negative.
* Full reversal.
* Reclassification.
* Transfer.

---

# 32. Revenue Reversal

Revenue Reversal phải xác định:

* Original Entitlement.
* Original Recognition.
* Original Receivable.
* Amount reversed.
* Effective date.
* Source event.
* Refund/Contract cancellation.
* Impact on Commission.
* Approval.

---

# 33. Revenue Dispute

> Status codes dưới đây là candidate vocabulary; exact workflow thuộc Revenue Context Pack.

Có thể phát sinh khi:

* Developer không công nhận giao dịch.
* Owner tranh chấp phí.
* Buyer phản đối Service Fee.
* Sai tỷ lệ.
* Sai Contract value.
* Sai period.
* Duplicate transaction.
* Giao dịch hủy.

Status:

```text
NEW
UNDER_REVIEW
PENDING_INTERNAL_INFORMATION
PENDING_COUNTERPARTY
NEGOTIATING
RESOLVED_IN_FAVOR
RESOLVED_PARTIAL
RESOLVED_AGAINST
CANCELLED
```

---

# 34. Revenue Reconciliation

> Result codes dưới đây là candidate vocabulary; exact matching/tolerance rules thuộc Revenue contracts.

## 34.1. Mục tiêu

Đối chiếu giữa:

* Contract nội bộ.
* Revenue Entitlement.
* Developer/Partner statement.
* Invoice/reference.
* Payment.
* Receipt.
* Settlement.
* Cancellation.

## 34.2. Kết quả

```text
MATCHED
MISSING_INTERNAL_ENTITLEMENT
MISSING_COUNTERPARTY_RECORD
AMOUNT_MISMATCH
RATE_MISMATCH
BASE_MISMATCH
CONTRACT_STATUS_MISMATCH
PAYMENT_MISMATCH
DUPLICATE
HELD_BY_COUNTERPARTY
DISPUTED
REQUIRES_REVIEW
```

---

# 35. Partner Revenue Statement

Statement có thể theo:

* Partner.
* Project.
* Period.
* Contract list.
* Revenue Model.
* Currency.

Mỗi line gồm:

* Contract.
* Buyer.
* Listing.
* Contract value.
* Eligible base.
* Rate.
* Expected revenue.
* Partner-confirmed revenue.
* Difference.
* Status.

---

# 36. Revenue Statement Version

Statement đã gửi hoặc đã duyệt không sửa trực tiếp.

Thay đổi phải tạo version hoặc adjustment statement.

---

# 37. Operational Revenue forecast inputs và Analytics boundary

> Revenue Context có thể giữ operational projections. Certified forecast formulas, snapshots và predictive models thuộc Analytics Context.

Forecast có thể dựa trên:

* Active Deal.
* Booking.
* Contract pending.
* Contract effective.
* Buyer payment milestone.
* Partner payment schedule.
* Revenue recognition probability.

Phải phân biệt:

```text
PIPELINE_REVENUE
EXPECTED_ENTITLEMENT
RECOGNIZED_REVENUE
RECEIVABLE_REVENUE
COLLECTED_REVENUE
```

---

# 38. Internal Commission Engine – nguyên tắc

## 38.1. Hoa hồng nội bộ không phải Revenue

Công ty có thể:

* Có Revenue nhưng chưa đủ điều kiện trả commission.
* Trả commission từ Sales Budget trước khi Revenue thu được.
* Trả commission nhiều hơn hoặc ít hơn một tỷ lệ trực tiếp của Revenue.
* Chi commission cho nhiều vai trò.

## 38.2. Commission phải có Funding Source

Không được tạo Commission Entitlement không xác định nguồn.

---

# 39. Candidate Commission Funding Source vocabulary — pending validation

> Exact codes, budget authority và accounting references thuộc Commission Plan/financial governance contracts.

```text
EXTERNAL_DISTRIBUTION_COMMISSION
BROKERAGE_FEE
SERVICE_FEE
PROPERTY_SALES_BUDGET
COMPANY_SALES_BUDGET
PROJECT_SALES_BUDGET
MARKETING_BUDGET
MANAGEMENT_BUDGET
REFERRAL_BUDGET
PARTNER_INCENTIVE
OTHER_INTERNAL_FUND
```

---

# 40. Commission Plan

## 40.1. Nội dung

* Plan code.
* Plan name.
* Legal Entity.
* Scope.
* Transaction Model.
* Project.
* Revenue Model.
* Funding Source.
* Beneficiary types.
* Calculation base.
* Rule.
* Tiers.
* Milestones.
* Holdback.
* Clawback.
* Payout policy.
* Effective dates.
* Version.
* Status.

## 40.2. Commission Plan không được dùng hồi tố tùy tiện

Phải resolve theo:

* Deal created date.
* Booking date.
* Contract signed date.
* Contract effective date.
* Revenue recognition date.
* Policy cấu hình.

---

# 41. Candidate Commission Plan lifecycle — pending validation

> Exact states/transitions thuộc Revenue Context Pack.

```text
DRAFT
PENDING_REVIEW
PENDING_APPROVAL
SCHEDULED
ACTIVE
SUSPENDED
EXPIRED
REPLACED
ARCHIVED
```

---

# 42. Candidate Commission Beneficiary types — pending validation

> Exact identity and eligibility semantics thuộc Party/IAM/Revenue contracts.

```text
EMPLOYEE
USER
PRIMARY_SALE
CO_SALE
TEAM_LEAD
DEPARTMENT_HEAD
PROJECT_MANAGER
TRANSACTION_COORDINATOR
SELLER_SIDE_AGENT
BUYER_SIDE_AGENT
REFERRER
EXTERNAL_COLLABORATOR
PARTNER
OTHER
```

---

# 43. Commission Participant Snapshot

Tại thời điểm tính, phải snapshot:

* User/Party.
* Employee ID.
* Organization.
* Branch.
* Department.
* Team.
* Position.
* Deal role.
* Co-sale role.
* Primary sale status.
* Assignment history.
* Employment status.
* Legal Entity.
* Plan version.
* Effective date.

Việc user chuyển team sau đó không được sửa snapshot lịch sử.

---

# 44. Nguồn xác định participant

* Deal primary responsibility.
* Co-sale Agreement đã approved/locked.
* Referral record.
* Transaction Case role.
* Organization hierarchy tại milestone.
* Approved manual participant adjustment.

Activity đơn thuần không tự tạo Commission Participant.

---

# 45. Candidate Commission calculation methods — pending validation

> Exact formula semantics thuộc versioned Commission Plan rules.

```text
PERCENTAGE_OF_REVENUE_ENTITLEMENT
PERCENTAGE_OF_RECOGNIZED_REVENUE
PERCENTAGE_OF_COLLECTED_REVENUE
PERCENTAGE_OF_CONTRACT_VALUE
PERCENTAGE_OF_NET_PROPERTY_VALUE
PERCENTAGE_OF_BROKERAGE_FEE
FIXED_AMOUNT
FIXED_AMOUNT_PER_UNIT
TIERED_PERCENTAGE
ROLE_POOL_ALLOCATION
POINT_BASED
BUDGET_BASED
MILESTONE_BASED
FORMULA_BASED
HYBRID
```

---

# 46. Candidate Commission calculation bases — pending validation

> Exact included/excluded amounts và source contracts thuộc Plan Version.

Các base chuẩn:

```text
GROSS_CONTRACT_VALUE
NET_PROPERTY_VALUE
ELIGIBLE_REVENUE_ENTITLEMENT
RECOGNIZED_REVENUE
COLLECTED_REVENUE
BROKERAGE_FEE
SERVICE_FEE
PROPERTY_SALES_BUDGET
PROJECT_SALES_BUDGET
NET_OF_REFUND
NET_OF_CLAWBACK
UNIT_COUNT
FIXED_BASE
CUSTOM_FORMULA
```

---

# 47. Hoa hồng công ty tự phát triển

Có thể tính theo:

* Contract Value.
* Net Property Value.
* Sales Budget.
* Payment Milestones.
* Contract stage.

Không bắt buộc chờ Revenue Payment từ bên ngoài.

Ví dụ:

```text
50% commission recognized khi Contract effective.
30% khi Buyer thanh toán 30%.
20% khi bàn giao.
```

---

# 48. Hoa hồng phân phối chủ đầu tư ngoài

Có thể phụ thuộc:

* Contract effective.
* Buyer payment.
* Developer confirmation.
* Revenue Receivable.
* Công ty thực nhận Distribution Commission.

Ví dụ:

```text
Entitlement tính khi Contract effective.
Recognition 50% khi Developer xác nhận.
Payable 100% khi công ty nhận đủ commission.
```

---

# 49. Hoa hồng ký gửi

Có thể chia thành:

* Seller-side commission.
* Buyer-side commission.
* Closing support.
* Transaction coordination.
* Referral.

Base có thể là Brokerage Fee thực nhận.

---

# 50. Commission Pool

Một giao dịch có thể có tổng pool:

```text
Commission Pool
=
Eligible Funding Base
× Pool Rate
```

Sau đó phân bổ:

* Primary sale.
* Co-sale.
* Manager.
* Support.
* Referral.

Tổng allocation không được vượt Pool, trừ plan có additional budget.

---

# 51. Role Pool Allocation

Ví dụ:

* Primary Sale Pool: 60%.
* Co-sale Pool: 20%.
* Management Pool: 10%.
* Closing Pool: 5%.
* Referral Pool: 5%.

Mỗi pool có thể tiếp tục chia giữa nhiều participant.

---

# 52. Co-sale Allocation

Phải sử dụng accepted Co-sale Agreement Version từ Transaction Context.

## 52.1. Nếu Agreement dùng tỷ lệ

Phân bổ theo tỷ lệ approved.

## 52.2. Nếu Agreement dùng role

Commission Plan xác định tỷ lệ theo role.

## 52.3. Nếu Agreement chưa khóa

Có thể:

* Không tạo Entitlement.
* Tạo provisional entitlement.
* Chặn Booking/Contract milestone theo policy.
* Đưa vào reconciliation.

## 52.4. Không tự chia đều

Trừ khi plan quy định rõ.

---

# 53. Manager Override Commission

Có thể tính cho:

* Team Lead.
* Department Head.
* Branch Director.
* Project Manager.

Phải xác định:

* Dựa trên organization snapshot tại ngày nào.
* Có cần trực tiếp quản lý sale không.
* Có bị cap không.
* Có tính khi manager thay đổi giữa giao dịch không.
* Có chia theo thời gian hay milestone không.

Không dùng cơ cấu hiện tại để viết lại quyền lợi lịch sử.

---

# 54. Referral Commission

Người giới thiệu có thể là:

* Customer.
* Employee.
* External collaborator.
* Partner.

Phải có:

* Referral record.
* Referral agreement.
* Identity.
* Eligibility.
* Consent.
* Amount/rate.
* Milestone.
* Payment method.
* Tax/withholding reference.
* Approval.

Không trả referral chỉ dựa trên note tự do.

---

# 55. External Collaborator

Nếu beneficiary không phải employee:

* Party identity.
* Agreement.
* Payment beneficiary profile.
* Bank/payment reference.
* Tax document reference.
* Eligibility.
* Approval.
* Restricted access.

---

# 56. Commission Tier

Có thể theo:

* Số lượng giao dịch.
* Contract Value.
* Revenue.
* Collected Revenue.
* Period.
* Project.
* Individual.
* Team.
* Department.

Phải phân biệt:

* Tier tính riêng từng giao dịch.
* Tier cộng dồn theo kỳ.
* Tier retroactive.
* Tier marginal.

---

# 57. Commission Eligibility

Điều kiện có thể gồm:

* Deal role hợp lệ.
* Co-sale approved.
* Contract effective.
* Customer payment đạt mức.
* Revenue recognized.
* Revenue collected.
* Không có dispute.
* Không có policy violation.
* Hồ sơ hoàn tất.
* Employee status phù hợp.
* Không có clawback hold.

---

# 58. Nhân sự nghỉ việc

Không tự động xóa Commission Entitlement đã hình thành.

Policy phải xác định:

* Entitlement đã recognized có giữ không.
* Unvested entitlement có bị hủy không.
* Payable nhưng chưa trả xử lý thế nào.
* Clawback recovery thực hiện ra sao.
* Payment method sau offboarding.
* Approval.

Handover không đồng nghĩa từ bỏ commission.

---

# 59. Candidate Commission Milestone vocabulary — pending validation

> Exact milestones/source facts thuộc Revenue Context Pack và Event Registry.

```text
DEAL_QUALIFIED
BOOKING_ACTIVE
DEPOSIT_CONFIRMED
CONTRACT_SIGNED
CONTRACT_EFFECTIVE
BUYER_PAYMENT_PERCENT_REACHED
REVENUE_RECOGNIZED
REVENUE_COLLECTED
HANDOVER_COMPLETED
PROJECT_SETTLEMENT_COMPLETED
CUSTOM_MILESTONE
```

---

# 60. Commission Entitlement

## 60.1. Khái niệm

Khoản hoa hồng tính toán cho một beneficiary.

## 60.2. Entitlement có thể là

* Provisional.
* Calculated.
* Recognized.
* Vested.
* Payable.
* Paid.
* Reversed.

---

# 61. Candidate Commission Entitlement lifecycle — pending validation

> Exact states, transitions and amount invariants thuộc Revenue Context Pack.

```text
DRAFT
CALCULATED
PROVISIONAL
PENDING_VALIDATION
PENDING_APPROVAL
APPROVED
PARTIALLY_RECOGNIZED
FULLY_RECOGNIZED
PARTIALLY_VESTED
FULLY_VESTED
PARTIALLY_PAYABLE
FULLY_PAYABLE
PARTIALLY_PAID
PAID
ON_HOLD
DISPUTED
ADJUSTMENT_PENDING
PARTIALLY_CLAWED_BACK
FULLY_CLAWED_BACK
CANCELLED
CLOSED
```

---

# 62. Commission Calculation Snapshot

Phải lưu:

* Contract.
* Contract Version.
* Deal.
* Transaction Case.
* Booking.
* Revenue Entitlement.
* Revenue Recognition.
* Beneficiary.
* Participant role.
* Co-sale Agreement Version.
* Organization snapshot.
* Plan Version.
* Funding Source.
* Calculation Base.
* Base Amount.
* Rate.
* Tier.
* Fixed amount.
* Pool.
* Allocation.
* Gross Commission.
* Holdback.
* Deduction reference.
* Net Entitlement.
* Currency.
* Calculation engine version.
* Timestamp.

---

# 63. Commission Recognition

Commission có thể được recognized từng phần.

Ví dụ:

* 30% khi Contract effective.
* 30% khi Revenue recognized.
* 40% khi Revenue collected.

Mỗi recognition phải:

* Tham chiếu milestone.
* Lưu amount.
* Có effective date.
* Có rule version.
* Có source event.

---

# 64. Commission Vesting

Vesting có thể phụ thuộc:

* Hết thời gian hủy.
* Buyer thanh toán đủ tỷ lệ.
* Revenue đã thu.
* Không có dispute.
* Hồ sơ hoàn chỉnh.
* Employee đáp ứng điều kiện.

Vesting không loại bỏ hoàn toàn clawback nếu policy cho phép clawback sau đó.

---

# 65. Commission Holdback

Một phần commission có thể bị giữ:

* Đến khi Developer thanh toán.
* Đến khi hết thời gian hủy.
* Đến khi Contract đủ payment.
* Đến khi hoàn tất handover.
* Đến khi đóng reconciliation.
* Do dispute.

Holdback phải có release condition.

---

# 66. Commission Payable

Commission chuyển Payable khi:

* Recognized đủ.
* Vested đủ.
* Không bị Hold.
* Không có dispute.
* Beneficiary hợp lệ.
* Payment profile hợp lệ.
* Payout period mở.
* Approval hoàn tất.

---

# 67. Commission Statement

Mỗi beneficiary có statement theo kỳ:

* Opening balance.
* New entitlement.
* Recognized.
* Payable.
* Paid.
* Holdback.
* Adjustments.
* Clawback.
* Tax/withholding reference.
* Closing balance.
* Negative balance.

Statement đã phát hành không sửa trực tiếp.

---

# 68. Commission Dispute

Beneficiary có thể tranh chấp:

* Sai participant.
* Sai tỷ lệ.
* Sai base.
* Sai milestone.
* Thiếu giao dịch.
* Sai clawback.
* Sai payout.
* Sai organization role.

Dispute workflow:

1. Submit.
2. Validate.
3. Freeze affected amount nếu cần.
4. Review source.
5. Decision.
6. Adjustment.
7. Statement correction.

---

# 69. Candidate Payout Period lifecycle — pending validation

> Exact period-lock/reopen rules thuộc Revenue Context contracts.

Có thể theo:

* Tháng.
* Quý.
* Project cycle.
* Custom period.
* Contract milestone.

Period có trạng thái:

```text
OPEN
CALCULATING
PENDING_REVIEW
LOCKED
PAYOUT_PROCESSING
CLOSED
REOPENED_FOR_ADJUSTMENT
```

---

# 70. Payout Batch

Payout Batch gom Commission Payable theo:

* Legal Entity.
* Currency.
* Payment method.
* Period.
* Beneficiary type.
* Payroll/non-payroll.

---

# 71. Candidate Payout Batch lifecycle — pending validation

> Exact states/transitions and external confirmation mapping thuộc Revenue/Integration contracts.

```text
DRAFT
CALCULATED
PENDING_REVIEW
PENDING_APPROVAL
APPROVED
PAYMENT_INSTRUCTION_CREATED
PAYMENT_PROCESSING
PARTIALLY_PAID
PAID
FAILED
CANCELLED
RECONCILIATION_REQUIRED
CLOSED
```

---

# 72. Payout Batch Item

Mỗi item gồm:

* Beneficiary.
* Commission Entitlements.
* Gross payable.
* Holdback.
* Clawback offset.
* Advance recovery.
* Other deductions.
* Withholding reference.
* Net payable.
* Payment method.
* Payment reference.
* Status.

---

# 73. Payout không đồng nghĩa Entitlement

Có thể:

* Entitlement đã recognized nhưng chưa payable.
* Payable nhưng chưa đưa vào batch.
* Batch approved nhưng chưa chuyển tiền.
* Payment thực hiện một phần.
* Payment thất bại.

---

# 74. Payout Instruction

Có thể gửi đến:

* Payroll.
* Bank payment system.
* ERP.
* Manual payment process.

Revenue giữ payout-instruction intent/reference:

* Destination system.
* Beneficiary account reference.
* Amount.
* Currency.
* Instruction ID.
* Sent at.
* Status.
* Response.
* Idempotency key.

---

# 75. External Payout Confirmation Projection

Chỉ chuyển Paid projection khi nhận authenticated, idempotently-consumed confirmation từ:

* Payroll confirmation.
* Bank payment confirmation.
* Finance confirmation có evidence.
* External transaction reference.

Không đánh dấu Paid chỉ vì batch approved.

---

# 76. Partial Payout

Nếu chi một phần:

* Item `PARTIALLY_PAID`.
* Remaining payable giữ lại.
* Không sửa gross entitlement.
* Có nhiều payment references.

---

# 77. Commission Advance

## 77.1. Khái niệm

Tạm ứng hoa hồng trước khi đủ điều kiện Payable.

## 77.2. Yêu cầu

* Advance policy.
* Maximum rate.
* Eligible milestone.
* Approval.
* Recovery method.
* Clawback acknowledgement.
* Beneficiary consent nếu cần.

## 77.3. Advance không phải Entitlement mới

Được theo dõi như khoản advance cần offset khi commission payable.

---

# 78. Advance Recovery

Khi commission trở thành payable:

```text
Net Payout
=
Gross Payable
− Advance Outstanding
```

Nếu giao dịch hủy trước khi đủ commission:

* Advance trở thành recovery balance.
* Xử lý theo clawback policy.

---

# 79. Withholding và deduction

Có thể theo dõi:

* Tax withholding reference.
* Insurance/payroll deduction reference.
* Advance recovery.
* Clawback offset.
* Court/authorized deduction nếu có.
* Other approved deduction.

Revenue and Commission Capability không tự tính thuế pháp định hoàn chỉnh nếu không có tax engine.

---

# 80. Clawback

> Clawback is a governed adjustment/recovery process; exact lifecycle thuộc Revenue Context Pack.

## 80.1. Khái niệm

Clawback là việc hoàn nhập hoặc thu hồi Commission đã recognized, vested, payable hoặc paid khi căn cứ giao dịch thay đổi.

## 80.2. Không sửa Commission Entitlement cũ

Tạo Clawback Case và Adjustment.

---

# 81. Candidate Clawback Trigger vocabulary — pending validation

> Exact triggers phải ánh xạ tới accepted Contract/Revenue/Transaction facts.

```text
CONTRACT_CANCELLED
CONTRACT_TERMINATED
CONTRACT_VALUE_REDUCED
PRODUCT_CHANGED
AREA_REDUCED
DISCOUNT_INCREASED
REFUND_ISSUED
PAYMENT_REVERSED
REVENUE_REVERSED
REVENUE_REDUCED
DEVELOPER_REJECTED
BROKERAGE_FEE_DISPUTED
OWNER_FEE_REFUNDED
DUPLICATE_TRANSACTION
INVALID_COMMISSION
CO_SALE_CORRECTION
PARTICIPANT_INELIGIBLE
POLICY_VIOLATION
FRAUD_CONFIRMED
MANUAL_APPROVED
OTHER
```

---

# 82. Clawback Scope

Clawback có thể áp dụng:

* Chỉ phần chưa paid.
* Phần paid.
* Một participant.
* Tất cả participant.
* Một milestone.
* Toàn giao dịch.
* Chỉ phần giảm giá trị.
* Chỉ phần refunded.

---

# 83. Clawback Calculation

Ví dụ proportional:

```text
Clawback Amount
=
Original Commission
× Revenue Reduction Ratio
```

Hoặc:

```text
Clawback Amount
=
Commission Attributable to Reversed Revenue
```

Phải lưu:

* Original amount.
* Remaining unpaid.
* Paid amount.
* Reduction base.
* Formula.
* Calculated clawback.
* Approved clawback.
* Currency.
* Effective date.

---

# 84. Candidate Clawback recovery methods — pending validation

> Actual recovery must comply with approved policy, employment/contract terms and applicable law.

```text
REVERSE_UNPAID_ENTITLEMENT
REDUCE_PAYABLE
OFFSET_CURRENT_PAYOUT
OFFSET_FUTURE_PAYOUT
CREATE_NEGATIVE_BALANCE
REQUEST_REPAYMENT
PAYROLL_RECOVERY_REFERENCE
BANK_REPAYMENT_REFERENCE
WAIVE_APPROVED
PARTIAL_RECOVERY
```

Việc khấu trừ thực tế phải tuân thủ policy và quy định áp dụng.

---

# 85. Negative Commission Balance

Nếu Clawback vượt Commission chưa trả:

* Tạo negative balance.
* Gắn beneficiary.
* Currency.
* Source clawback.
* Opening amount.
* Recovered.
* Waived.
* Remaining.

Không sửa lịch sử payout đã thực hiện.

---

# 86. Clawback Recovery

Có thể thu hồi qua:

* Offset kỳ sau.
* Voluntary repayment.
* Payroll instruction.
* Bank transfer.
* Final settlement khi offboarding.
* Approved waiver.

Mỗi recovery cần payment/reference.

---

# 87. Clawback và nhân sự nghỉ việc

Phải xử lý:

* Beneficiary inactive.
* Không còn payout tương lai.
* Recovery contact.
* Final payroll reference.
* Repayment agreement.
* Legal/HR review nếu cần.
* Write-off/waiver approval.

Không xóa số dư âm vì user inactive.

---

# 88. Clawback Dispute

Beneficiary có thể tranh chấp:

* Trigger không hợp lệ.
* Sai amount.
* Sai tỷ lệ.
* Sai participant.
* Revenue chưa thực sự reversed.
* Refund không liên quan commission.

Khoản tranh chấp có thể bị hold đến khi giải quyết.

---

# 89. Revenue Adjustment → Commission Impact

Mỗi Revenue Adjustment phải chạy impact analysis:

* Commission Plan nào bị ảnh hưởng.
* Entitlement nào bị ảnh hưởng.
* Milestone nào bị vô hiệu.
* Amount nào chưa paid.
* Amount nào đã paid.
* Clawback cần tạo.
* Statement kỳ nào cần điều chỉnh.

---

# 90. Contract Cancellation Impact

Khi nhận accepted Contract cancellation fact:

```text
contract.cancelled
```

Revenue Context phải:

1. Xác định Revenue Entitlements.
2. Xác định Revenue Recognition.
3. Xác định Revenue Receivables.
4. Xác định Payment đã thu.
5. Xác định Refund/Forfeiture.
6. Tính Revenue Reversal.
7. Xác định Commission Entitlements.
8. Tính Clawback.
9. Tạo Reconciliation Case.
10. Không sửa dữ liệu gốc.

---

# 91. Refund và Revenue

Refund có thể:

* Giảm Property Sales Revenue.
* Giảm Brokerage Fee.
* Không ảnh hưởng Revenue nếu refund là tiền thu hộ.
* Tạo forfeiture revenue.
* Tạo Revenue Reclassification.

Phải dùng Financial Nature và Revenue Rule.

---

# 92. Forfeiture Revenue

Khoản bị giữ lại chỉ trở thành Revenue khi:

* Có legal/business basis.
* Contract and Cash Capability xác nhận forfeiture.
* Revenue Arrangement cho phép.
* Approval.
* Không còn dispute.

Không tự coi Deposit forfeited là revenue.

---

# 93. Product Change Impact

Khi đổi sản phẩm:

* Contract Value thay đổi.
* Revenue Base thay đổi.
* Revenue Entitlement điều chỉnh.
* Commission Entitlement điều chỉnh.
* Payout/Clawback tính chênh lệch.

Không tạo toàn bộ entitlement mới mà bỏ entitlement cũ không liên kết.

---

# 94. Co-sale Correction

Nếu co-sale agreement được điều chỉnh hợp lệ:

* Không sửa allocation cũ.
* Tạo Commission Adjustment.
* Reallocate chênh lệch.
* Nếu đã paid, tạo transfer/clawback tương ứng.
* Có dispute workflow.

---

# 95. Multi-Legal Entity

## 95.1. Revenue Legal Entity

Mỗi Revenue Entitlement phải thuộc một Legal Entity beneficiary.

## 95.2. Commission Paying Entity

Có thể khác Revenue Legal Entity nếu có policy/intercompany arrangement.

## 95.3. Cross-entity

Phải xác định:

* Source Legal Entity.
* Beneficiary Legal Entity.
* Paying Legal Entity.
* Intercompany reference.
* Approval.
* Currency.
* Settlement.

Không dùng một commission pool toàn Enterprise không rõ pháp nhân.

---

# 96. Intercompany Allocation

Trong Enterprise có nhiều pháp nhân:

* Project Entity có doanh thu.
* Holding Company quản lý sale.
* Service Entity chi hoa hồng.

Có thể tạo Intercompany Allocation reference.

Revenue Context chỉ quản lý nghiệp vụ vận hành; bút toán intercompany thuộc ERP.

---

# 97. Revenue Attribution

Revenue có thể được phân bổ báo cáo theo:

* Legal Entity.
* Project.
* Sales Launch.
* Branch.
* Department.
* Team.
* Sale.
* Channel.
* Campaign.
* Source.
* Transaction Model.

Attribution không thay Revenue Beneficiary pháp lý.

---

# 98. Commission Attribution

Commission phải tham chiếu:

* Deal attribution.
* Participant snapshot.
* Co-sale agreement.
* Commission plan.
* Organization snapshot.

Không tính lại theo user hiện đang sở hữu Customer.

---

# 99. Segregation of Duties

## 99.1. Revenue

* Maker: tạo/kiểm tra Entitlement.
* Checker: kiểm tra Contract/Arrangement.
* Approver: duyệt Entitlement/Adjustment.
* Collector: xác nhận payment từ Contract and Cash Capability.
* Reconciler: đối soát Partner.

## 99.2. Commission

* Maker: tính commission.
* Checker: kiểm tra participant và formula.
* Approver: duyệt entitlement/payable.
* Payout Maker: tạo batch.
* Payout Approver: duyệt batch.
* Payment Executor: thực hiện chi.
* Reconciler: xác nhận payout.

## 99.3. Không tự duyệt

User không được tự:

* Duyệt Revenue Adjustment mình tạo.
* Duyệt Commission Entitlement mình là beneficiary.
* Tạo và duyệt Payout Batch cùng lúc.
* Duyệt Clawback mình là đối tượng.

---

# 100. Revenue Workflow

Các workflow chính:

* Revenue Arrangement approval.
* Revenue Entitlement calculation.
* Revenue Entitlement approval.
* Revenue Recognition.
* Revenue Receivable activation.
* Partner statement approval.
* Revenue adjustment.
* Revenue reversal.
* Revenue dispute.
* Revenue reconciliation.
* Revenue write-off.

---

# 101. Commission Workflow

* Commission Plan approval.
* Entitlement calculation.
* Participant validation.
* Commission approval.
* Recognition.
* Vesting.
* Payable release.
* Statement issuance.
* Dispute.
* Payout Batch approval.
* Payout execution.
* Clawback.
* Negative balance recovery.
* Commission adjustment.

---

# 102. SLA policy inputs

> Các giá trị dưới đây là recommended baselines để validation, không phải hardcoded SLO/SLA contract.

Các SLA:

* Revenue Entitlement calculation.
* Partner statement review.
* Revenue discrepancy resolution.
* Revenue Receivable activation.
* Revenue payment allocation.
* Commission calculation.
* Commission review.
* Commission dispute.
* Payout Batch approval.
* Payout execution.
* Clawback review.
* Recovery.
* External confirmation.

Giá trị tham khảo:

| Nghiệp vụ                                      |        SLA tham khảo |
| ---------------------------------------------- | -------------------: |
| Tạo Revenue Entitlement sau Contract milestone |           Trong ngày |
| Review Partner Statement                       |      1 ngày làm việc |
| Resolve amount mismatch                        |      2 ngày làm việc |
| Commission calculation sau milestone           |           Trong ngày |
| Commission review                              |      1 ngày làm việc |
| Payout Batch approval                          |    1–2 ngày làm việc |
| Payout confirmation                            | Theo lịch kỳ chi trả |
| Clawback impact analysis                       |         Trong 1 ngày |
| Commission dispute                             |    3–5 ngày làm việc |

SLA definitions phải được quản trị qua Platform Configuration và Business Calendar; operational SLA instances thuộc Activity/owning Context theo Context Pack.

---

# 103. Notification

## 103.1. Sale/Beneficiary

* Commission Entitlement được tạo.
* Commission recognized.
* Commission payable.
* Commission bị hold.
* Statement phát hành.
* Payout approved.
* Payout completed.
* Adjustment.
* Clawback.
* Dispute result.

## 103.2. Team Lead/Manager

* Commission của team.
* Co-sale conflict.
* Deal thiếu participant.
* Commission bất thường.
* Clawback lớn.
* Payout pending.

## 103.3. Revenue/Finance

* Revenue Entitlement pending.
* Partner statement mới.
* Revenue overdue.
* Payment chưa allocate.
* Revenue mismatch.
* Revenue reversal.
* High-value dispute.

## 103.4. Director

* Revenue forecast thay đổi lớn.
* Revenue overdue lớn.
* Payout batch lớn.
* Clawback bất thường.
* Commission-to-revenue ratio vượt ngưỡng.
* Cross-entity mismatch.

---

# 104. Candidate user experiences — Revenue Center

> Exact routes, screens, components và responsive behavior thuộc Navigation/IA, Design System và Current Sprint Pack.

Các tab:

1. Revenue Overview.
2. Revenue Arrangements.
3. Revenue Entitlements.
4. Revenue Recognition.
5. Revenue Receivables.
6. Revenue Payments.
7. Partner Statements.
8. Reconciliation.
9. Disputes.
10. Adjustments.
11. Forecast.
12. Audit.

---

# 105. Revenue Entitlement Workspace

Hiển thị:

* Contract.
* Transaction Model.
* Revenue Model.
* Arrangement.
* Calculation.
* Base.
* Rate.
* Components.
* Milestones.
* Recognition.
* Receivable.
* Payment.
* Adjustment.
* Commission impact.
* Audit.

---

# 106. Partner Reconciliation Workspace

* Partner.
* Project.
* Period.
* Statement version.
* Contract lines.
* Internal expected amount.
* Partner confirmed amount.
* Difference.
* Payment.
* Dispute.
* Assigned user.
* SLA.

---

# 107. Candidate user experiences — Commission Center

> Exact routes, screens, components và responsive behavior thuộc frontend canonical sources.

Các tab:

1. Commission Plans.
2. Entitlements.
3. Participants.
4. Recognition.
5. Vesting.
6. Payable.
7. Statements.
8. Payout Batches.
9. Advances.
10. Clawback.
11. Disputes.
12. Negative Balances.
13. Audit.

---

# 108. Beneficiary Commission Statement

Hiển thị:

* Kỳ.
* Giao dịch.
* Vai trò.
* Base.
* Rate.
* Entitlement.
* Recognized.
* Payable.
* Paid.
* Holdback.
* Clawback.
* Remaining.
* Explanation.
* Rule version.

Field nhạy cảm của beneficiary khác phải được che.

---

# 109. Payout Workspace

* Payout period.
* Legal Entity.
* Beneficiary.
* Gross payable.
* Deductions.
* Clawback offset.
* Net payout.
* Payment method.
* Approval.
* Execution.
* Failure.
* Reconciliation.

---

# 110. Clawback Center

* Trigger.
* Contract.
* Original Commission.
* Beneficiary.
* Paid/unpaid.
* Calculated clawback.
* Approved clawback.
* Recovery method.
* Negative balance.
* Dispute.
* Recovery status.
* Audit.

---

# 111. Analytics cho Sale

* Entitlement dự kiến.
* Entitlement recognized.
* Payable.
* Paid trong kỳ.
* Holdback.
* Clawback.
* Dispute.
* Giao dịch chưa đủ điều kiện.
* Statement mới.

Sale chỉ xem dữ liệu của mình.

---

# 112. Analytics cho Team Lead

* Commission team.
* Revenue team attribution.
* Co-sale allocation.
* Payable.
* Payout.
* Clawback.
* Deal chưa đủ milestone.
* Commission dispute.
* Commission-to-revenue ratio.

---

# 113. Analytics cho Revenue/Finance

* Revenue Entitlement.
* Recognized Revenue.
* Revenue Receivable.
* Collected Revenue.
* Overdue Revenue.
* Partner statement mismatch.
* Unallocated Revenue Fund.
* Holdback.
* Adjustments.
* Reversals.
* Payout liability.
* Upcoming payout.
* Negative commission balance.

---

# 114. Analytics cho Director

* Revenue theo Transaction Model.
* Revenue theo Legal Entity.
* Revenue theo Project.
* Property Sales Revenue.
* Distribution Commission.
* Brokerage Fee.
* Service Fee.
* Recognized/Collected gap.
* Revenue overdue.
* Commission expense.
* Commission-to-revenue ratio.
* Payout forecast.
* Clawback rate.
* Project profitability operational view.
* Partner performance.
* Team performance.

---

# 115. Candidate analytical questions — không phải certified hoặc statutory reports

> Exact grain, formulas, snapshots, certification và access thuộc Analytics Context; statutory reports thuộc accounting/payroll/tax systems.

## Revenue

* Revenue Arrangement.
* Revenue Entitlement.
* Revenue Recognition.
* Revenue Receivable.
* Revenue Aging.
* Revenue Payment.
* Revenue by Project.
* Revenue by Legal Entity.
* Revenue by Transaction Model.
* Revenue by Revenue Model.
* Revenue by Partner.
* Revenue by Contract.
* Revenue by period.
* Revenue holdback.
* Revenue adjustment.
* Revenue reversal.
* Partner reconciliation.
* Revenue dispute.
* Revenue forecast.
* Collected-on-behalf versus Revenue.

## Commission

* Commission Plan.
* Commission Entitlement.
* Commission by beneficiary.
* Commission by role.
* Commission by Project.
* Commission by Team.
* Commission by Legal Entity.
* Commission by Funding Source.
* Commission recognized.
* Commission payable.
* Commission paid.
* Commission holdback.
* Co-sale allocation.
* Manager override.
* Referral commission.
* Advance commission.
* Payout batch.
* Payout failure.
* Commission dispute.
* Clawback.
* Negative balance.
* Recovery.
* Commission-to-revenue ratio.

Operational views phải drill-down đúng scope. Certified Metrics thuộc Analytics Context; statutory reports thuộc external accounting/payroll/tax systems.

---

# 116. Candidate data model — không phải physical schema canonical

> **Classification:** `CONTEXT-SPECIFIC DESIGN INPUT / PENDING VALIDATION`
> Exact tables, columns, constraints, indexes và references chỉ có hiệu lực khi được khóa trong Revenue Context DB Specification và Alembic migrations. Cross-context references không mặc định tạo cross-schema business foreign keys.

## 116.1. Revenue Arrangement

### `revenue_arrangements`

* `id`
* `arrangement_code`
* `enterprise_id`
* `legal_entity_id`
* `counterparty_party_id`
* `project_id`
* `transaction_model`
* `revenue_model`
* `agreement_type`
* `agreement_reference`
* `sales_mandate_id`
* `currency`
* `calculation_method`
* `recognition_policy_code`
* `receivable_policy_code`
* `payment_terms_json`
* `holdback_policy_json`
* `effective_from`
* `effective_to`
* `status`
* `current_version`
* `created_by`
* `created_at`
* `updated_at`

### `revenue_arrangement_versions`

* `id`
* `revenue_arrangement_id`
* `version`
* `scope_json`
* `calculation_rules_json`
* `recognition_rules_json`
* `receivable_rules_json`
* `holdback_rules_json`
* `adjustment_rules_json`
* `tax_reference_json`
* `effective_from`
* `effective_to`
* `status`
* `created_by`
* `reviewed_by`
* `approved_by`
* `created_at`

---

## 116.2. Revenue Rule

### `revenue_rule_sets`

* `id`
* `rule_set_code`
* `name`
* `scope_type`
* `scope_id`
* `status`
* `current_version`
* `created_at`

### `revenue_rule_versions`

* `id`
* `revenue_rule_set_id`
* `version`
* `calculation_method`
* `base_definition_json`
* `formula_expression`
* `tier_rules_json`
* `milestone_rules_json`
* `rounding_policy_id`
* `effective_from`
* `effective_to`
* `status`
* `created_by`
* `reviewed_by`
* `approved_by`
* `created_at`

---

## 116.3. Revenue Entitlement

### `revenue_entitlements`

* `id`
* `entitlement_code`
* `enterprise_id`
* `legal_entity_id`
* `contract_id`
* `contract_version_id`
* `transaction_case_id`
* `deal_id`
* `booking_id`
* `project_id`
* `listing_id`
* `counterparty_party_id`
* `revenue_arrangement_id`
* `revenue_arrangement_version_id`
* `revenue_rule_version_id`
* `revenue_model`
* `currency`
* `gross_entitlement_amount`
* `holdback_amount`
* `adjustment_amount`
* `net_entitlement_amount`
* `recognized_amount`
* `receivable_amount`
* `paid_amount`
* `outstanding_amount`
* `status`
* `created_by`
* `approved_by`
* `created_at`
* `updated_at`
* `version`

### `revenue_entitlement_components`

* `id`
* `revenue_entitlement_id`
* `component_type`
* `financial_nature`
* `calculation_base_amount`
* `rate`
* `fixed_amount`
* `tier_code`
* `gross_amount`
* `deduction_amount`
* `net_amount`
* `currency`
* `source_component_id`
* `created_at`

### `revenue_calculation_snapshots`

* `id`
* `revenue_entitlement_id`
* `contract_snapshot_json`
* `arrangement_snapshot_json`
* `base_snapshot_json`
* `formula_snapshot_json`
* `tier_snapshot_json`
* `calculation_result_json`
* `engine_version`
* `calculated_at`
* `created_at`

---

## 116.4. Revenue Milestone và Recognition

### `revenue_milestones`

* `id`
* `revenue_entitlement_id`
* `milestone_code`
* `source_event_type`
* `source_event_id`
* `required_percentage`
* `recognition_percentage`
* `recognition_amount`
* `status`
* `eligible_at`
* `satisfied_at`
* `created_at`

### `revenue_recognitions`

* `id`
* `recognition_code`
* `revenue_entitlement_id`
* `revenue_milestone_id`
* `recognition_type`
* `amount`
* `currency`
* `recognition_basis`
* `operational_recognition_date`
* `status`
* `source_event_type`
* `source_event_id`
* `reviewed_by`
* `approved_by`
* `created_at`

### `revenue_recognition_reversals`

* `id`
* `revenue_recognition_id`
* `amount`
* `reason`
* `source_event_type`
* `source_event_id`
* `status`
* `approved_by`
* `effective_at`
* `created_at`

---

## 116.5. Revenue Receivable

### `revenue_receivables`

* `id`
* `revenue_receivable_code`
* `revenue_entitlement_id`
* `legal_entity_id`
* `debtor_party_id`
* `receiver_party_id`
* `currency`
* `original_amount`
* `adjustment_amount`
* `withheld_amount`
* `paid_amount`
* `reversed_amount`
* `outstanding_amount`
* `disputed_amount`
* `due_date`
* `status`
* `aging_bucket`
* `created_at`
* `updated_at`
* `version`

### `revenue_receivable_adjustments`

* `id`
* `revenue_receivable_id`
* `adjustment_type`
* `amount`
* `reason`
* `source_type`
* `source_id`
* `status`
* `requested_by`
* `reviewed_by`
* `approved_by`
* `effective_at`
* `created_at`

### `revenue_payment_applications`

* `id`
* `revenue_receivable_id`
* `revenue_entitlement_id`
* `payment_transaction_id`
* `payment_allocation_id`
* `amount`
* `currency`
* `status`
* `applied_by`
* `approved_by`
* `applied_at`
* `created_at`

### `unallocated_revenue_funds`

* `id`
* `payment_transaction_id`
* `counterparty_party_id`
* `legal_entity_id`
* `amount`
* `currency`
* `candidate_entitlements_json`
* `status`
* `assigned_user_id`
* `due_at`
* `created_at`
* `resolved_at`

---

## 116.6. Revenue Adjustment

### `revenue_adjustments`

* `id`
* `adjustment_code`
* `revenue_entitlement_id`
* `contract_id`
* `adjustment_type`
* `amount`
* `currency`
* `reason_code`
* `reason`
* `source_event_type`
* `source_event_id`
* `commission_impact_required`
* `status`
* `requested_by`
* `reviewed_by`
* `approved_by`
* `effective_at`
* `created_at`

### `revenue_holdbacks`

* `id`
* `revenue_entitlement_id`
* `holdback_type`
* `amount`
* `currency`
* `reason`
* `release_condition_json`
* `expected_release_at`
* `released_amount`
* `status`
* `created_at`

---

## 116.7. Partner Statement và Reconciliation

### `revenue_statements`

* `id`
* `statement_code`
* `counterparty_party_id`
* `legal_entity_id`
* `project_id`
* `period_from`
* `period_to`
* `currency`
* `current_version`
* `internal_expected_amount`
* `counterparty_confirmed_amount`
* `difference_amount`
* `status`
* `created_by`
* `reviewed_by`
* `approved_by`
* `created_at`

### `revenue_statement_versions`

* `id`
* `revenue_statement_id`
* `version`
* `source_reference`
* `source_document_id`
* `source_document_version_id`
* `source_file_hash_snapshot`
* `statement_snapshot_json`
* `status`
* `created_at`

### `revenue_statement_lines`

* `id`
* `revenue_statement_version_id`
* `contract_id`
* `revenue_entitlement_id`
* `eligible_base`
* `expected_rate`
* `expected_amount`
* `confirmed_rate`
* `confirmed_amount`
* `difference_amount`
* `reconciliation_status`
* `created_at`

### `revenue_reconciliation_cases`

* `id`
* `case_code`
* `revenue_statement_line_id`
* `revenue_entitlement_id`
* `revenue_receivable_id`
* `counterparty_party_id`
* `reconciliation_type`
* `expected_snapshot_json`
* `actual_snapshot_json`
* `difference_json`
* `risk_level`
* `status`
* `assigned_user_id`
* `due_at`
* `resolution_code`
* `resolution_notes`
* `created_at`
* `resolved_at`

### `revenue_disputes`

* `id`
* `dispute_code`
* `revenue_entitlement_id`
* `revenue_receivable_id`
* `counterparty_party_id`
* `dispute_type`
* `disputed_amount`
* `currency`
* `reason`
* `evidence_json`
* `status`
* `assigned_user_id`
* `created_at`
* `resolved_at`

---

## 116.8. Commission Plan

### `commission_plans`

* `id`
* `plan_code`
* `name`
* `enterprise_id`
* `legal_entity_id`
* `project_id`
* `transaction_model`
* `revenue_model`
* `funding_source_code`
* `scope_type`
* `scope_id`
* `status`
* `current_version`
* `created_at`
* `updated_at`

### `commission_plan_versions`

* `id`
* `commission_plan_id`
* `version`
* `participant_rules_json`
* `eligibility_rules_json`
* `calculation_rules_json`
* `milestone_rules_json`
* `vesting_rules_json`
* `holdback_rules_json`
* `payout_rules_json`
* `clawback_rules_json`
* `effective_from`
* `effective_to`
* `status`
* `created_by`
* `reviewed_by`
* `approved_by`
* `created_at`

### `commission_plan_tiers`

* `id`
* `commission_plan_version_id`
* `tier_code`
* `threshold_from`
* `threshold_to`
* `rate`
* `fixed_amount`
* `tier_method`
* `created_at`

### `commission_role_pools`

* `id`
* `commission_plan_version_id`
* `role_pool_code`
* `beneficiary_role`
* `pool_percentage`
* `pool_fixed_amount`
* `allocation_method`
* `created_at`

---

## 116.9. Commission Participant

### `commission_participant_snapshots`

* `id`
* `contract_id`
* `deal_id`
* `transaction_case_id`
* `cosale_agreement_id`
* `cosale_agreement_version`
* `beneficiary_party_id`
* `beneficiary_user_id`
* `employee_id`
* `participant_role`
* `organization_snapshot_json`
* `employment_snapshot_json`
* `eligibility_snapshot_json`
* `effective_at`
* `created_at`

---

## 116.10. Commission Entitlement

### `commission_entitlements`

* `id`
* `commission_entitlement_code`
* `enterprise_id`
* `legal_entity_id`
* `contract_id`
* `contract_version_id`
* `deal_id`
* `transaction_case_id`
* `booking_id`
* `revenue_entitlement_id`
* `revenue_recognition_id`
* `beneficiary_party_id`
* `beneficiary_user_id`
* `commission_plan_id`
* `commission_plan_version_id`
* `commission_participant_snapshot_id`
* `participant_role`
* `funding_source_code`
* `currency`
* `gross_entitlement_amount`
* `holdback_amount`
* `adjustment_amount`
* `recognized_amount`
* `vested_amount`
* `payable_amount`
* `paid_amount`
* `clawback_amount`
* `remaining_amount`
* `status`
* `created_at`
* `updated_at`
* `version`

### `commission_entitlement_components`

* `id`
* `commission_entitlement_id`
* `component_type`
* `calculation_base_code`
* `calculation_base_amount`
* `rate`
* `fixed_amount`
* `tier_code`
* `role_pool_code`
* `gross_amount`
* `holdback_amount`
* `net_amount`
* `created_at`

### `commission_calculation_snapshots`

* `id`
* `commission_entitlement_id`
* `source_snapshot_json`
* `participant_snapshot_json`
* `plan_snapshot_json`
* `base_snapshot_json`
* `formula_snapshot_json`
* `result_snapshot_json`
* `engine_version`
* `calculated_at`
* `created_at`

---

## 116.11. Commission Milestone, Recognition và Vesting

### `commission_milestones`

* `id`
* `commission_entitlement_id`
* `milestone_code`
* `source_event_type`
* `source_event_id`
* `recognition_percentage`
* `vesting_percentage`
* `payable_percentage`
* `status`
* `eligible_at`
* `satisfied_at`
* `created_at`

### `commission_recognitions`

* `id`
* `commission_entitlement_id`
* `commission_milestone_id`
* `amount`
* `currency`
* `status`
* `recognized_at`
* `source_event_type`
* `source_event_id`
* `created_at`

### `commission_vestings`

* `id`
* `commission_entitlement_id`
* `commission_milestone_id`
* `amount`
* `currency`
* `status`
* `vested_at`
* `created_at`

### `commission_holdbacks`

* `id`
* `commission_entitlement_id`
* `holdback_type`
* `amount`
* `currency`
* `release_condition_json`
* `expected_release_at`
* `released_amount`
* `status`
* `created_at`

---

## 116.12. Commission Adjustment và Dispute

### `commission_adjustments`

* `id`
* `adjustment_code`
* `commission_entitlement_id`
* `adjustment_type`
* `amount`
* `currency`
* `reason_code`
* `reason`
* `source_type`
* `source_id`
* `status`
* `requested_by`
* `reviewed_by`
* `approved_by`
* `effective_at`
* `created_at`

### `commission_disputes`

* `id`
* `dispute_code`
* `commission_entitlement_id`
* `beneficiary_party_id`
* `dispute_type`
* `disputed_amount`
* `currency`
* `reason`
* `evidence_json`
* `status`
* `submitted_by`
* `assigned_user_id`
* `created_at`
* `resolved_at`

---

## 116.13. Commission Statement

### `commission_statements`

* `id`
* `statement_code`
* `beneficiary_party_id`
* `beneficiary_user_id`
* `legal_entity_id`
* `period_from`
* `period_to`
* `currency`
* `opening_balance`
* `new_entitlement_amount`
* `recognized_amount`
* `payable_amount`
* `paid_amount`
* `holdback_amount`
* `clawback_amount`
* `negative_balance_amount`
* `closing_balance`
* `status`
* `issued_at`
* `created_at`

### `commission_statement_items`

* `id`
* `commission_statement_id`
* `commission_entitlement_id`
* `item_type`
* `amount`
* `currency`
* `description`
* `created_at`

---

## 116.14. Payout

### `commission_payout_periods`

* `id`
* `period_code`
* `legal_entity_id`
* `period_from`
* `period_to`
* `status`
* `opened_at`
* `locked_at`
* `closed_at`
* `created_at`

### `commission_payout_batches`

* `id`
* `payout_batch_code`
* `payout_period_id`
* `legal_entity_id`
* `currency`
* `beneficiary_type`
* `payment_method`
* `gross_payable_amount`
* `deduction_amount`
* `clawback_offset_amount`
* `advance_recovery_amount`
* `net_payable_amount`
* `paid_amount`
* `status`
* `created_by`
* `reviewed_by`
* `approved_by`
* `created_at`
* `updated_at`

### `commission_payout_batch_items`

* `id`
* `payout_batch_id`
* `beneficiary_party_id`
* `beneficiary_user_id`
* `gross_payable_amount`
* `holdback_amount`
* `clawback_offset_amount`
* `advance_recovery_amount`
* `other_deduction_amount`
* `withholding_reference_amount`
* `net_payable_amount`
* `paid_amount`
* `status`
* `created_at`

### `commission_payout_allocations`

* `id`
* `payout_batch_item_id`
* `commission_entitlement_id`
* `allocated_amount`
* `currency`
* `created_at`

### `commission_payout_instructions`

* `id`
* `payout_batch_item_id`
* `destination_system`
* `beneficiary_payment_profile_reference`
* `amount`
* `currency`
* `idempotency_key`
* `external_instruction_id`
* `status`
* `sent_at`
* `external_response_reference`
* `created_at`

### `commission_payout_payments`

* `id`
* `payout_batch_item_id`
* `external_payment_reference`
* `amount`
* `currency`
* `executed_at`
* `reconciliation_status`
* `status`
* `created_at`

---

## 116.15. Commission Advance

### `commission_advances`

* `id`
* `advance_code`
* `beneficiary_party_id`
* `beneficiary_user_id`
* `commission_entitlement_id`
* `currency`
* `approved_amount`
* `paid_amount`
* `recovered_amount`
* `outstanding_amount`
* `recovery_policy_json`
* `status`
* `requested_by`
* `approved_by`
* `created_at`

---

## 116.16. Clawback

### `commission_clawback_cases`

* `id`
* `clawback_code`
* `contract_id`
* `revenue_adjustment_id`
* `trigger_type`
* `trigger_source_type`
* `trigger_source_id`
* `currency`
* `total_calculated_amount`
* `total_approved_amount`
* `total_recovered_amount`
* `status`
* `requested_by`
* `reviewed_by`
* `approved_by`
* `created_at`
* `resolved_at`

### `commission_clawback_items`

* `id`
* `clawback_case_id`
* `commission_entitlement_id`
* `beneficiary_party_id`
* `beneficiary_user_id`
* `original_commission_amount`
* `unpaid_amount`
* `paid_amount`
* `reduction_base`
* `calculated_clawback_amount`
* `approved_clawback_amount`
* `recovery_method`
* `recovered_amount`
* `remaining_amount`
* `status`
* `created_at`

### `commission_negative_balances`

* `id`
* `beneficiary_party_id`
* `beneficiary_user_id`
* `legal_entity_id`
* `currency`
* `opening_amount`
* `recovered_amount`
* `waived_amount`
* `remaining_amount`
* `status`
* `created_at`
* `updated_at`

### `commission_clawback_recoveries`

* `id`
* `clawback_item_id`
* `negative_balance_id`
* `recovery_type`
* `source_payout_batch_item_id`
* `external_payment_reference`
* `amount`
* `currency`
* `status`
* `recovered_at`
* `created_at`

---

# 117. Candidate application operations — không phải OpenAPI canonical

> Các operations dưới đây là capability inventory. Exact paths, methods, payloads, errors, idempotency và authorization metadata thuộc OpenAPI.

## Revenue Arrangement

```text
GET    /revenue-arrangements
POST   /revenue-arrangements
GET    /revenue-arrangements/{id}
PATCH  /revenue-arrangements/{id}
POST   /revenue-arrangements/{id}/versions
GET    /revenue-arrangement-versions/{id}
POST   /revenue-arrangement-versions/{id}/validate
POST   /revenue-arrangement-versions/{id}/submit-review
POST   /revenue-arrangement-versions/{id}/approve
POST   /revenue-arrangement-versions/{id}/activate
POST   /revenue-arrangements/{id}/suspend
```

## Revenue Entitlement

```text
GET    /revenue-entitlements
POST   /contracts/{id}/calculate-revenue-entitlements
GET    /revenue-entitlements/{id}
POST   /revenue-entitlements/{id}/recalculate
POST   /revenue-entitlements/{id}/validate
POST   /revenue-entitlements/{id}/submit-review
POST   /revenue-entitlements/{id}/approve
POST   /revenue-entitlements/{id}/hold
POST   /revenue-entitlements/{id}/release
GET    /revenue-entitlements/{id}/calculation
GET    /revenue-entitlements/{id}/history
```

## Revenue Recognition

```text
GET    /revenue-recognitions
POST   /revenue-entitlements/{id}/evaluate-milestones
POST   /revenue-entitlements/{id}/recognitions
POST   /revenue-recognitions/{id}/approve
POST   /revenue-recognitions/{id}/reverse
```

## Revenue Receivable

```text
GET    /revenue-receivables
POST   /revenue-entitlements/{id}/receivables
GET    /revenue-receivables/{id}
POST   /revenue-receivables/{id}/activate
POST   /revenue-receivables/{id}/adjustment-requests
POST   /revenue-receivables/{id}/hold
POST   /revenue-receivables/{id}/release
POST   /revenue-receivables/{id}/mark-disputed
GET    /revenue-receivables/{id}/payment-applications
```

## Revenue Payment

```text
GET    /unallocated-revenue-funds
POST   /revenue-payment-applications
POST   /revenue-payment-applications/{id}/approve
POST   /revenue-payment-applications/{id}/reverse
POST   /unallocated-revenue-funds/{id}/resolve
```

## Revenue Statement và Reconciliation

```text
GET    /revenue-statements
POST   /revenue-statements
GET    /revenue-statements/{id}
POST   /revenue-statements/{id}/versions
POST   /revenue-statement-versions/{id}/validate
POST   /revenue-statement-versions/{id}/reconcile
POST   /revenue-statements/{id}/approve

GET    /revenue-reconciliation-cases
GET    /revenue-reconciliation-cases/{id}
POST   /revenue-reconciliation-cases/{id}/assign
POST   /revenue-reconciliation-cases/{id}/resolve
POST   /revenue-reconciliation-cases/{id}/accept-difference
```

## Revenue Adjustment

```text
POST   /revenue-entitlements/{id}/adjustment-requests
GET    /revenue-adjustments/{id}
POST   /revenue-adjustments/{id}/analyze-impact
POST   /revenue-adjustments/{id}/review
POST   /revenue-adjustments/{id}/approve
POST   /revenue-adjustments/{id}/execute
```

## Commission Plan

```text
GET    /commission-plans
POST   /commission-plans
GET    /commission-plans/{id}
POST   /commission-plans/{id}/versions
GET    /commission-plan-versions/{id}
PATCH  /commission-plan-versions/{id}
POST   /commission-plan-versions/{id}/validate
POST   /commission-plan-versions/{id}/simulate
POST   /commission-plan-versions/{id}/submit-review
POST   /commission-plan-versions/{id}/approve
POST   /commission-plan-versions/{id}/activate
```

## Commission Entitlement

```text
GET    /commission-entitlements
POST   /contracts/{id}/calculate-commission-entitlements
GET    /commission-entitlements/{id}
POST   /commission-entitlements/{id}/recalculate
POST   /commission-entitlements/{id}/validate-participant
POST   /commission-entitlements/{id}/submit-review
POST   /commission-entitlements/{id}/approve
POST   /commission-entitlements/{id}/hold
POST   /commission-entitlements/{id}/release
GET    /commission-entitlements/{id}/calculation
GET    /commission-entitlements/{id}/history
```

## Commission Milestone

```text
POST   /commission-entitlements/{id}/evaluate-milestones
POST   /commission-entitlements/{id}/recognitions
POST   /commission-entitlements/{id}/vestings
POST   /commission-entitlements/{id}/release-payable
```

## Commission Adjustment và Dispute

```text
POST   /commission-entitlements/{id}/adjustment-requests
POST   /commission-entitlements/{id}/disputes
GET    /commission-disputes
GET    /commission-disputes/{id}
POST   /commission-disputes/{id}/assign
POST   /commission-disputes/{id}/resolve
```

## Commission Statement

```text
GET    /commission-statements
POST   /commission-statements/generate
GET    /commission-statements/{id}
POST   /commission-statements/{id}/issue
POST   /commission-statements/{id}/close
```

## Payout

```text
GET    /commission-payout-periods
POST   /commission-payout-periods
POST   /commission-payout-periods/{id}/calculate
POST   /commission-payout-periods/{id}/lock

GET    /commission-payout-batches
POST   /commission-payout-batches
GET    /commission-payout-batches/{id}
POST   /commission-payout-batches/{id}/recalculate
POST   /commission-payout-batches/{id}/submit-review
POST   /commission-payout-batches/{id}/approve
POST   /commission-payout-batches/{id}/create-instructions
POST   /commission-payout-batches/{id}/confirm-payments
POST   /commission-payout-batches/{id}/reconcile
POST   /commission-payout-batches/{id}/close
```

## Advance

```text
GET    /commission-advances
POST   /commission-advances
GET    /commission-advances/{id}
POST   /commission-advances/{id}/review
POST   /commission-advances/{id}/approve
POST   /commission-advances/{id}/confirm-payment
POST   /commission-advances/{id}/recover
```

## Clawback

```text
GET    /commission-clawback-cases
POST   /commission-clawback-cases
GET    /commission-clawback-cases/{id}
POST   /commission-clawback-cases/{id}/calculate
POST   /commission-clawback-cases/{id}/analyze-impact
POST   /commission-clawback-cases/{id}/submit-review
POST   /commission-clawback-cases/{id}/approve
POST   /commission-clawback-cases/{id}/execute
POST   /commission-clawback-items/{id}/recover
POST   /commission-clawback-items/{id}/waive
GET    /commission-negative-balances
```

Backend phải tự enforce:

* Authenticated user.
* Legal Entity.
* Contract scope.
* Revenue scope.
* Beneficiary scope.
* Permission.
* Field masking.
* Workflow.
* Approval.
* Segregation of Duties.
* Rule version.
* Formula version.
* Idempotency.
* Optimistic locking.
* Payout period lock.
* Audit.

---

# 118. Candidate permission vocabulary — không phải Permission Registry canonical

> Exact permission codes, scopes, role mappings, SoD, concealment và field masking thuộc security registries/matrices.

## Revenue Arrangement và Rule

```text
revenue_arrangement.view
revenue_arrangement.view_sensitive
revenue_arrangement.create
revenue_arrangement.update_draft
revenue_arrangement.create_version
revenue_arrangement.validate
revenue_arrangement.review
revenue_arrangement.approve
revenue_arrangement.activate
revenue_arrangement.suspend

revenue_rule.view
revenue_rule.create
revenue_rule.update_draft
revenue_rule.validate
revenue_rule.simulate
revenue_rule.review
revenue_rule.approve
revenue_rule.activate
```

## Revenue Entitlement

```text
revenue_entitlement.view
revenue_entitlement.view_calculation
revenue_entitlement.calculate
revenue_entitlement.recalculate
revenue_entitlement.validate
revenue_entitlement.review
revenue_entitlement.approve
revenue_entitlement.hold
revenue_entitlement.release
revenue_entitlement.view_audit
```

## Recognition và Receivable

```text
revenue_recognition.view
revenue_recognition.create
revenue_recognition.review
revenue_recognition.approve
revenue_recognition.reverse

revenue_receivable.view
revenue_receivable.create
revenue_receivable.activate
revenue_receivable.adjust_request
revenue_receivable.adjust_approve
revenue_receivable.hold
revenue_receivable.release
revenue_receivable.mark_disputed
```

## Revenue Payment và Reconciliation

```text
revenue_payment.view
revenue_payment.apply
revenue_payment.review
revenue_payment.approve
revenue_payment.reverse

revenue_statement.view
revenue_statement.create
revenue_statement.import
revenue_statement.reconcile
revenue_statement.review
revenue_statement.approve

revenue_reconciliation.view
revenue_reconciliation.assign
revenue_reconciliation.resolve
revenue_reconciliation.accept_difference
```

## Commission Plan

```text
commission_plan.view
commission_plan.view_sensitive
commission_plan.create
commission_plan.update_draft
commission_plan.create_version
commission_plan.validate
commission_plan.simulate
commission_plan.review
commission_plan.approve
commission_plan.activate
commission_plan.suspend
```

## Commission Entitlement

```text
commission_entitlement.view_self
commission_entitlement.view_team
commission_entitlement.view_all
commission_entitlement.view_calculation
commission_entitlement.calculate
commission_entitlement.recalculate
commission_entitlement.validate_participant
commission_entitlement.review
commission_entitlement.approve
commission_entitlement.hold
commission_entitlement.release
commission_entitlement.adjust_request
commission_entitlement.adjust_approve
```

## Commission Statement và Dispute

```text
commission_statement.view_self
commission_statement.view_team
commission_statement.generate
commission_statement.issue
commission_statement.close

commission_dispute.create
commission_dispute.view
commission_dispute.assign
commission_dispute.resolve
```

## Payout

```text
commission_payout.view_self
commission_payout.view
commission_payout_period.create
commission_payout_period.calculate
commission_payout_period.lock
commission_payout_batch.create
commission_payout_batch.recalculate
commission_payout_batch.review
commission_payout_batch.approve
commission_payout_instruction.create
commission_payout_payment.confirm
commission_payout.reconcile
commission_payout.close
```

## Advance và Clawback

```text
commission_advance.view
commission_advance.request
commission_advance.review
commission_advance.approve
commission_advance.confirm_payment
commission_advance.recover

commission_clawback.view
commission_clawback.create
commission_clawback.calculate
commission_clawback.review
commission_clawback.approve
commission_clawback.execute
commission_clawback.recover
commission_clawback.waive
commission_negative_balance.view
```

Các quyền kết hợp với:

```text
self
mine
team
department
branch
legal_entity
project
assigned
shared
all
```

---

# 119. Candidate role baseline — không phải Role/Permission Registry canonical

> Role descriptions chỉ mô tả product intent. Backend authority phải được resolve từ IAM/Security canonical sources.

## 119.1. Sale

Được:

* Xem Commission Statement của mình.
* Xem cách tính ở mức được phép.
* Gửi dispute.
* Xem payout của mình.
* Xem clawback của mình.
* Xem Revenue summary của Deal mình nếu policy cho phép.

Không được:

* Xem commission của sale khác.
* Sửa Commission Entitlement.
* Tự tạo payout.
* Tự duyệt dispute của mình.
* Xem Arrangement nhạy cảm.
* Xem Revenue margin toàn Project.

## 119.2. Team Lead

Được:

* Xem commission team theo quyền.
* Review participant/co-sale.
* Xem Revenue attribution team.
* Xem dispute team.
* Không mặc định xem bank account beneficiary.

## 119.3. Revenue Operations

Được:

* Quản lý Arrangement.
* Tính Entitlement.
* Reconciliation.
* Partner statement.
* Revenue adjustment.

## 119.4. Accounting

Được:

* Xem Payment Application.
* Xác nhận Payment source từ Contract and Cash Capability.
* Reconcile Revenue Receivable.
* Payout payment reference tùy quyền.

## 119.5. Finance

Được:

* Review Revenue.
* Approve Payout.
* Review clawback.
* Forecast cash.
* Manage holdback.
* Không tự sửa source Contract.

## 119.6. HR/Payroll

Nếu tích hợp:

* Nhận Payout Instruction.
* Xác nhận payroll payment.
* Xem withholding/deduction theo quyền.
* Không xem toàn bộ Contract detail.

## 119.7. Director

Được:

* Xem scope toàn quyền được cấp.
* Approve ngoại lệ.
* Approve Plan/Rule.
* Approve Payout Batch lớn.
* Approve waiver/clawback đặc biệt.
* Export có audit.

---

# 120. Candidate business facts — không phải Event contracts canonical

> Exact Event names, versions, payloads, channels và consumers thuộc JSON Schema, AsyncAPI và Event Registry.

Revenue and Commission Capability phát:

```text
revenue_arrangement.created
revenue_arrangement.version_created
revenue_arrangement.activated
revenue_arrangement.suspended

revenue_entitlement.calculated
revenue_entitlement.approved
revenue_entitlement.held
revenue_entitlement.released
revenue_entitlement.adjusted
revenue_entitlement.reversed

revenue_milestone.satisfied
revenue.recognized
revenue.recognition_reversed

revenue_receivable.created
revenue_receivable.activated
revenue_receivable.partially_paid
revenue_receivable.paid
revenue_receivable.overdue
revenue_receivable.disputed
revenue_receivable.adjusted

revenue_payment.applied
revenue_payment.reversed
revenue_fund.unallocated
revenue_fund.resolved

revenue_statement.created
revenue_statement.reconciled
revenue_reconciliation.created
revenue_reconciliation.resolved
revenue_dispute.created
revenue_dispute.resolved

commission_plan.created
commission_plan.version_created
commission_plan.activated

commission_entitlement.calculated
commission_entitlement.approved
commission_entitlement.recognized
commission_entitlement.vested
commission_entitlement.payable
commission_entitlement.held
commission_entitlement.released
commission_entitlement.adjusted

commission_statement.generated
commission_statement.issued
commission_dispute.created
commission_dispute.resolved

commission_payout_period.locked
commission_payout_batch.created
commission_payout_batch.approved
commission_payout_instruction.created
commission_payout.partially_paid
commission_payout.paid
commission_payout.failed

commission_advance.approved
commission_advance.paid
commission_advance.recovered

commission_clawback.created
commission_clawback.calculated
commission_clawback.approved
commission_clawback.executed
commission_clawback.recovered
commission_negative_balance.created
commission_negative_balance.cleared
```

Consumer phải idempotent.

---

# 121. Candidate Platform configuration references

> Exact configuration keys, schemas, scopes và resolution strategies thuộc Platform Context contracts.

```text
revenue.arrangement_workflow
revenue.arrangement_resolution_policy
revenue.calculation_rule_set
revenue.recognition_policy
revenue.receivable_policy
revenue.holdback_policy
revenue.adjustment_policy
revenue.reversal_policy
revenue.dispute_policy
revenue.reconciliation_policy
revenue.statement_policy
revenue.forecast_policy

commission.plan_workflow
commission.plan_resolution_policy
commission.participant_policy
commission.eligibility_policy
commission.calculation_policy
commission.role_pool_policy
commission.tier_policy
commission.milestone_policy
commission.recognition_policy
commission.vesting_policy
commission.holdback_policy
commission.payable_policy
commission.statement_policy
commission.dispute_policy

commission.payout_period_policy
commission.payout_batch_policy
commission.payout_approval_policy
commission.payout_instruction_policy
commission.payout_reconciliation_policy

commission.advance_policy
commission.clawback_policy
commission.negative_balance_policy
commission.recovery_policy
commission.waiver_policy

revenue_commission.sla_policy
revenue_commission.notification_policy
revenue_commission.field_access_policy
revenue_commission.export_approval_policy
revenue_commission.retention_policy
```

Mỗi configuration definition phải công bố schema, allowed scopes, resolution strategy, owner, version, effective period, approval và Audit requirements khi phù hợp.

---

# 122. System invariant

Các quy tắc sau không được cấu hình tắt:

1. Gross Transaction Value không mặc định là Revenue.
2. Collected-on-behalf funds không mặc định là Revenue.
3. Revenue Entitlement và Revenue Payment là hai lớp khác nhau.
4. Revenue Recognition và Revenue Receivable là hai lớp khác nhau.
5. Revenue và Internal Commission là hai lớp khác nhau.
6. Commission Entitlement và Commission Payout là hai lớp khác nhau.
7. Mọi Revenue Entitlement phải có Arrangement hoặc approved basis.
8. Mọi Commission Entitlement phải có Commission Plan hoặc approved exception.
9. Mọi Commission Entitlement phải có Funding Source.
10. Contract/Receipt/Payment nguồn không được sửa bởi Revenue and Commission Capability.
11. Revenue Entitlement approved không được sửa trực tiếp.
12. Commission Entitlement approved không được sửa trực tiếp.
13. Revenue Adjustment phải tạo record riêng.
14. Commission Adjustment phải tạo record riêng.
15. Payout Paid phải có payment confirmation.
16. Clawback không được xóa payout lịch sử.
17. Negative balance không bị xóa khi beneficiary inactive.
18. Handover không tự thay Commission Participant.
19. Activity không tự tạo Commission Entitlement.
20. Co-sale phải dùng Agreement Version hợp lệ.
21. Commission Plan active không được sửa trực tiếp.
22. Revenue Arrangement active không được sửa trực tiếp.
23. Rule mới không áp dụng hồi tố trái policy.
24. Sale không được tự duyệt commission của mình.
25. Payout Maker và Payout Approver phải tách khi SoD áp dụng.
26. Commission không được tính trên Revenue chưa đủ base nếu rule không cho phép.
27. Revenue reversal phải chạy Commission Impact Analysis.
28. Contract cancellation phải chạy Revenue và Commission Adjustment.
29. Backend phải enforce Legal Entity.
30. Audit Revenue, Commission, Payout và Clawback không được sửa.
31. Revenue and Commission Capability không thay thế General Ledger.
32. Revenue and Commission Capability không thay thế Payroll source of truth.

---

# 123. Rule nghiệp vụ bắt buộc

1. Một Contract có thể tạo nhiều Revenue Entitlement.
2. Một Revenue Entitlement chỉ thuộc một Revenue Model chính.
3. Revenue Entitlement phải có Legal Entity beneficiary.
4. Revenue Entitlement phải có Counterparty khi có bên trả.
5. Revenue Arrangement phải có effective dates.
6. Arrangement hết hạn không áp dụng giao dịch mới.
7. Arrangement mới không tự sửa Entitlement cũ.
8. Calculation phải lưu base.
9. Calculation phải lưu rate/formula.
10. Calculation phải lưu version.
11. Tier method phải được xác định.
12. Retroactive tier chỉ dùng khi Agreement cho phép.
13. Revenue Bonus phải là Entitlement riêng.
14. Recognition phải có milestone.
15. Operational Recognition không mặc định là accounting recognition.
16. Revenue Receivable phải có debtor.
17. Revenue Receivable phải có receiver.
18. Revenue Receivable outstanding phải được tính.
19. Revenue Payment phải tham chiếu Payment Allocation Contract and Cash Capability.
20. Revenue and Commission Capability không tự tạo bank transaction.
21. Unallocated Revenue Fund không tự phân bổ khi confidence thấp.
22. Revenue Payment Application approved không sửa trực tiếp.
23. Payment Application sai phải reverse.
24. Revenue Holdback phải có release condition.
25. Revenue Adjustment không sửa Original Entitlement.
26. Revenue Reversal phải có source event.
27. Revenue Dispute phải có disputed amount.
28. Revenue Statement phải có version.
29. Statement approved không sửa trực tiếp.
30. Reconciliation difference phải có resolution.
31. Accepted Difference cần authority.
32. Commission Plan phải có Funding Source.
33. Commission Plan phải có effective dates.
34. Plan active không sửa trực tiếp.
35. Plan mới không tự áp dụng Deal cũ.
36. Participant phải lấy từ nguồn có cấu trúc.
37. Activity không tạo quyền commission.
38. Co-sale phải tham chiếu Agreement.
39. Co-sale chưa approved không tạo final entitlement.
40. Participant snapshot không đổi khi user chuyển team.
41. Handover không tự đổi commission.
42. User nghỉ việc không tự mất recognized entitlement.
43. User inactive không được phê duyệt.
44. Commission Calculation phải lưu base.
45. Commission Calculation phải lưu rate/tier/pool.
46. Commission Pool allocation không vượt pool.
47. Additional budget phải ghi nguồn riêng.
48. Manager override phải dùng organization snapshot.
49. Referral commission phải có referral record.
50. External collaborator phải có Party.
51. Entitlement có thể provisional.
52. Provisional không mặc định payable.
53. Recognition phải có milestone.
54. Vesting phải tách recognition.
55. Payable phải tách vesting.
56. Paid phải tách payable.
57. Commission Holdback phải có release condition.
58. Commission Entitlement approved không sửa trực tiếp.
59. Adjustment phải tạo record riêng.
60. Statement issued không sửa trực tiếp.
61. Dispute không tự sửa Entitlement.
62. Payout Period phải khóa trước payout.
63. Locked period không nhận entitlement mới trái policy.
64. Late adjustment phải vào kỳ adjustment.
65. Payout Batch phải theo Legal Entity.
66. Payout Batch phải theo currency.
67. Payout Batch approved không sửa trực tiếp.
68. Payout Instruction phải idempotent.
69. Payout Paid phải có external confirmation.
70. Partial payout không coi Paid toàn bộ.
71. Advance phải có recovery policy.
72. Advance không tạo thêm entitlement.
73. Advance phải offset khi payable.
74. Clawback phải có trigger hợp lệ.
75. Clawback phải có calculation snapshot.
76. Clawback không sửa payout cũ.
77. Clawback unpaid có thể reverse entitlement.
78. Clawback paid phải tạo recovery.
79. Negative balance phải được theo dõi theo currency.
80. Negative balance không tự bù trừ cross-currency.
81. Recovery phải có reference.
82. Waiver clawback phải có approval.
83. Beneficiary có quyền dispute clawback.
84. Revenue Adjustment phải đánh giá Commission Impact.
85. Refund không mặc định giảm toàn bộ Revenue.
86. Forfeiture không mặc định là Revenue.
87. Product change phải tính delta.
88. Contract value reduction phải tính proportional impact theo rule.
89. Co-sale correction sau payout phải tạo adjustment.
90. Multi-Legal Entity phải xác định paying entity.
91. Cross-entity payout phải có authority.
92. Revenue attribution không thay beneficiary pháp lý.
93. Commission attribution không dựa vào owner hiện tại.
94. View không đồng nghĩa Export.
95. Sale chỉ xem commission của mình.
96. Team Lead chỉ xem team theo quyền.
97. Revenue Arrangement nhạy cảm phải field-mask.
98. Beneficiary bank detail phải field-mask.
99. Payout data phải backend enforce.
100. User không tự duyệt entitlement mình hưởng.
101. Payout Maker không tự approve batch trái SoD.
102. Clawback subject không tự approve case.
103. Rule simulation không ghi production.
104. Formula phải được validate.
105. Formula không được thực thi mã tùy ý.
106. Decimal phải được dùng cho tiền và tỷ lệ.
107. Currency bắt buộc.
108. Rounding rule phải version.
109. Same idempotency key cùng payload trả cùng kết quả.
110. Same key khác payload phải conflict.
111. Event consumer phải idempotent.
112. Contract cancellation event lặp không tạo clawback trùng.
113. Payment confirmation lặp không tạo payout trùng.
114. Commission statement phải tái tạo được.
115. Revenue calculation phải tái tạo được.
116. Payout phải reconcile.
117. Unreconciled payout không được close.
118. Revenue Receivable paid không đồng nghĩa Contract completed.
119. Commission paid không đồng nghĩa Revenue collected đầy đủ.
120. Capability không thay thế accounting/payroll pháp định.

---

# 124. Cảnh báo và phát hiện bất thường

Hệ thống cần cảnh báo khi:

* Revenue Entitlement không có Arrangement.
* Revenue Entitlement không có Contract.
* Revenue Model không phù hợp Transaction Model.
* Buyer payment bị tính nhầm là Distribution Revenue.
* Owner Proceeds bị tính nhầm là Revenue.
* Collected-on-behalf funds không có settlement liability.
* Revenue base vượt Contract Value trái rule.
* Revenue rate vượt Arrangement.
* Revenue Entitlement duplicate.
* Recognition vượt Net Entitlement.
* Revenue Receivable vượt Recognized Amount trái policy.
* Revenue Payment vượt Receivable.
* Revenue Payment Application trùng.
* Unallocated Revenue Fund quá SLA.
* Revenue overdue.
* Partner Statement thiếu Contract.
* Statement amount mismatch lớn.
* Revenue reversed nhưng Receivable vẫn open sai.
* Contract cancelled nhưng Revenue chưa điều chỉnh.
* Refund issued nhưng Revenue không được đánh giá.
* Commission Entitlement không có Plan.
* Commission Entitlement không có Funding Source.
* Participant không có Deal role.
* Co-sale Agreement chưa approved.
* Tổng allocation vượt Commission Pool.
* Commission base vượt Revenue/Contract base trái rule.
* Commission rate vượt plan.
* Manager override dùng organization hiện tại thay vì snapshot.
* User nghỉ việc bị xóa entitlement.
* Recognized Amount vượt Gross Entitlement.
* Vested Amount vượt Recognized.
* Payable Amount vượt Vested.
* Paid Amount vượt Payable.
* Payout Batch net âm không giải thích.
* Payout Instruction trùng.
* Payout Paid không có external reference.
* Payout Batch approved bởi creator trái SoD.
* Beneficiary tự duyệt commission.
* Commission paid khi Revenue milestone chưa đủ trái plan.
* Holdback được release không đủ condition.
* Clawback trigger thiếu source.
* Clawback vượt original commission.
* Negative balance âm ngược hoặc sai currency.
* Contract cancellation không tạo clawback analysis.
* Revenue reversal không tạo commission impact.
* Payment reversal không cập nhật commission milestone.
* Co-sale correction không adjustment payout.
* Payout period reopened không approval.
* Statement issued không khớp payout.
* Commission dispute quá SLA.
* Clawback dispute chưa xử lý nhưng recovery tiếp tục trái policy.
* Cross-entity payout không có authority.
* Revenue/Commission ratio vượt threshold.
* Project commission expense vượt budget.
* Export commission dữ liệu hàng loạt.
* Sale truy cập commission người khác.
* Beneficiary account bị truy cập bất thường.
* Same idempotency key khác payload.
* Formula result khác simulation vượt tolerance.
* Rule version không active nhưng dùng cho transaction mới.

---

# 125. Audit requirements và evidence

> Audit Context sở hữu immutable Audit facts. Revenue Context phát sinh audit-worthy facts/references; operational logs không thay Audit.

## 125.1. Thao tác bắt buộc

* Revenue Arrangement create/version/review/approve/activate.
* Revenue Rule create/simulate/activate.
* Revenue Entitlement calculate/recalculate/approve.
* Revenue Recognition/reversal.
* Revenue Receivable create/adjust.
* Revenue Payment Application.
* Revenue Holdback/release.
* Revenue Statement import/version/approval.
* Revenue Reconciliation.
* Revenue Dispute.
* Revenue Adjustment/Reversal.
* Commission Plan create/version/simulate/activate.
* Participant snapshot.
* Commission Entitlement calculate/recalculate/approve.
* Recognition/Vesting/Payable.
* Holdback/release.
* Commission Adjustment.
* Commission Dispute.
* Statement generation/issuance.
* Payout Period lock.
* Payout Batch create/approve.
* Payout Instruction.
* Payout confirmation.
* Advance.
* Clawback.
* Negative balance.
* Recovery.
* Waiver.
* Sensitive view.
* Export.

## 125.2. Nội dung

* Actor.
* Role.
* Legal Entity.
* Contract.
* Deal.
* Transaction Case.
* Revenue Entitlement.
* Revenue Arrangement Version.
* Revenue Rule Version.
* Commission Entitlement.
* Commission Plan Version.
* Beneficiary.
* Payout Batch.
* Clawback.
* Before.
* After.
* Formula.
* Base.
* Rate.
* Reason.
* Source event.
* Approval.
* Workflow version.
* IP.
* Device.
* Request ID.
* Correlation ID.
* Idempotency key.
* Timestamp.
* Result.

---

# 126. Phạm vi MVP

## 126.1. Revenue Engine bắt buộc

* Revenue Arrangement.
* Arrangement Version.
* Revenue Model.
* Percentage/fixed calculation.
* Revenue Entitlement.
* Calculation Snapshot.
* Revenue Milestone.
* Revenue Recognition.
* Revenue Receivable.
* Revenue Payment Application từ Contract and Cash Capability.
* Unallocated Revenue Fund.
* Revenue Holdback cơ bản.
* Revenue Adjustment.
* Revenue Reversal.
* Partner Statement.
* Reconciliation Case.
* Revenue Dispute.
* Revenue Forecast cơ bản.
* Multi-Legal Entity.
* Scope.
* Approval.
* Audit.

## 126.2. Commission Engine bắt buộc

* Commission Plan.
* Plan Version.
* Funding Source.
* Percentage/fixed calculation.
* Role Pool.
* Co-sale Agreement integration.
* Participant Snapshot.
* Commission Entitlement.
* Calculation Snapshot.
* Commission Milestone.
* Recognition.
* Vesting cơ bản.
* Payable.
* Holdback.
* Statement.
* Dispute.
* Payout Period.
* Payout Batch.
* Payout Instruction.
* Payout confirmation.
* Advance cơ bản.
* Clawback.
* Negative Balance.
* Recovery.
* Scope.
* Field masking.
* SoD.
* Audit.
* Analytics.
* Domain events.

## 126.3. Giai đoạn nâng cao

* Complex tiering.
* Retroactive volume bonus.
* Profit-share.
* Multi-currency payout.
* Automated ERP integration.
* Payroll integration.
* Tax engine.
* Bank payout integration.
* Partner self-service portal.
* Sale commission portal.
* Advanced profitability.
* Budget control.
* Predictive Revenue Forecast.
* AI anomaly detection.
* Automated dispute comparison.
* Complex intercompany allocation.
* Project-level commission budget.
* Deferred commission.
* Equity-like incentive.
* Complex clawback repayment plans.
* Revenue invoice integration.
* Statutory revenue recognition integration.

---

# 127. Tiêu chí nghiệm thu

Capability được xem là đạt khi:

1. Tạo được Revenue Arrangement.
2. Arrangement có Legal Entity.
3. Arrangement có Counterparty.
4. Arrangement có Revenue Model.
5. Arrangement có Transaction Model.
6. Arrangement có effective dates.
7. Tạo được Arrangement Version.
8. Active Version không sửa trực tiếp.
9. Arrangement hết hạn không áp dụng giao dịch mới.
10. Resolve đúng Arrangement theo Contract date.
11. Tạo được Revenue Rule.
12. Rule có calculation base.
13. Rule có formula/rate.
14. Rule có rounding.
15. Rule có version.
16. Simulation không ghi production.
17. Tạo Revenue Entitlement từ Contract.
18. Một Contract tạo nhiều Entitlement.
19. Entitlement có Legal Entity beneficiary.
20. Entitlement có Counterparty payer.
21. Entitlement lưu Contract Version.
22. Entitlement lưu Arrangement Version.
23. Entitlement lưu Rule Version.
24. Tính phần trăm Contract Value được.
25. Tính phần trăm Net Property Value được.
26. Tính Fixed Amount được.
27. Tính theo Unit Count được.
28. Tính Tier cơ bản được.
29. Gross Transaction Value không tự thành Revenue.
30. Buyer payment to Developer không thành Revenue công ty.
31. Owner Proceeds không thành Revenue.
32. Brokerage Fee thành Revenue candidate đúng.
33. Service Fee được tách riêng.
34. Collected-on-behalf được loại khỏi Revenue.
35. Calculation Snapshot tái tạo được.
36. Calculation dùng Decimal.
37. Currency bắt buộc.
38. Rounding đúng policy.
39. Entitlement approval hoạt động.
40. Approved Entitlement không sửa trực tiếp.
41. Tạo Revenue Milestone.
42. Contract Effective milestone hoạt động.
43. Buyer Payment milestone hoạt động.
44. Developer Confirmation milestone hoạt động.
45. Nhận biết Revenue Recognition từng phần.
46. Recognition không vượt Entitlement.
47. Operational Recognition được gắn nhãn.
48. Tạo Revenue Receivable.
49. Receivable có debtor.
50. Receivable có receiver.
51. Receivable có due date.
52. Outstanding tự tính.
53. Revenue Receivable overdue hoạt động.
54. Tạo Revenue Payment Application.
55. Application tham chiếu Payment Allocation Contract and Cash Capability.
56. Một Payment phân bổ nhiều Revenue Receivable.
57. Một Receivable nhận nhiều Payment.
58. Partial Payment hoạt động.
59. Payment Application không vượt available amount.
60. Unallocated Revenue Fund được tạo.
61. Fund không tự phân bổ confidence thấp.
62. Revenue Holdback được tạo.
63. Holdback có release condition.
64. Release Holdback có approval.
65. Tạo Revenue Adjustment.
66. Adjustment không sửa Entitlement gốc.
67. Tạo Revenue Reversal.
68. Reversal có source event.
69. Reversal cập nhật Recognition/Receivable đúng.
70. Tạo Partner Statement.
71. Statement có version.
72. Statement approved không sửa.
73. Statement có Contract lines.
74. Internal Expected và Counterparty Confirmed được so sánh.
75. Tạo Reconciliation Case.
76. Amount mismatch được phát hiện.
77. Rate mismatch được phát hiện.
78. Base mismatch được phát hiện.
79. Accepted Difference cần quyền.
80. Tạo Revenue Dispute.
81. Revenue Forecast phân biệt Pipeline/Recognized/Collected.
82. Tạo Commission Plan.
83. Plan có Legal Entity.
84. Plan có Funding Source.
85. Plan có effective dates.
86. Tạo Plan Version.
87. Active Plan không sửa.
88. Resolve Plan theo milestone date đúng policy.
89. Tạo Commission Role Pool.
90. Tạo Commission Tier cơ bản.
91. Tạo Participant Snapshot.
92. Snapshot giữ organization lịch sử.
93. Snapshot giữ Deal role.
94. Snapshot giữ co-sale version.
95. Activity không tự tạo Participant.
96. Handover không tự đổi Participant.
97. User chuyển team không sửa snapshot.
98. Tạo Commission Entitlement.
99. Entitlement có beneficiary.
100. Entitlement có Funding Source.
101. Entitlement có Plan Version.
102. Entitlement có Contract.
103. Entitlement có Deal.
104. Tính phần trăm Revenue được.
105. Tính phần trăm Contract Value được.
106. Tính phần trăm Brokerage Fee được.
107. Tính theo Budget được.
108. Tính Fixed Amount được.
109. Tính Role Pool được.
110. Primary Sale allocation đúng.
111. Co-sale allocation đúng Agreement.
112. Manager override dùng snapshot.
113. Referral commission cần referral record.
114. External collaborator dùng Party.
115. Commission Pool không vượt nguồn.
116. Additional budget phải tách.
117. Calculation Snapshot tái tạo được.
118. Entitlement có Provisional status.
119. Provisional không Payable.
120. Tạo Commission Milestone.
121. Contract Effective milestone hoạt động.
122. Revenue Recognized milestone hoạt động.
123. Revenue Collected milestone hoạt động.
124. Recognition từng phần hoạt động.
125. Recognition không vượt entitlement.
126. Vesting hoạt động.
127. Vesting không vượt recognized.
128. Payable không vượt vested.
129. Holdback hoạt động.
130. Holdback có release condition.
131. User nghỉ việc không tự mất recognized entitlement.
132. Tạo Commission Statement.
133. Statement có opening/closing balance.
134. Statement có Entitlement items.
135. Statement issued không sửa.
136. Sale xem statement của mình.
137. Sale không xem statement người khác.
138. Tạo Commission Dispute.
139. Dispute freeze amount theo policy.
140. Resolve Dispute tạo adjustment.
141. Tạo Payout Period.
142. Lock Payout Period được.
143. Locked Period chặn thay đổi trái policy.
144. Tạo Payout Batch.
145. Batch theo Legal Entity.
146. Batch theo Currency.
147. Batch tính Gross Payable.
148. Batch tính Holdback.
149. Batch tính Clawback Offset.
150. Batch tính Advance Recovery.
151. Batch tính Net Payable.
152. Maker không tự Approver trái policy.
153. Tạo Payout Instruction.
154. Payout Instruction idempotent.
155. Batch approved không tự Paid.
156. Xác nhận Payout Payment được.
157. Partial Payout hoạt động.
158. Payout failure được lưu.
159. Payout reconciliation hoạt động.
160. Tạo Commission Advance.
161. Advance có approval.
162. Advance có recovery policy.
163. Advance không tạo Entitlement mới.
164. Advance được offset khi payout.
165. Tạo Clawback Case từ Contract cancellation.
166. Tạo Clawback từ Revenue reversal.
167. Tạo Clawback từ Refund.
168. Tạo Clawback từ Payment reversal.
169. Clawback có Calculation Snapshot.
170. Clawback không vượt original commission.
171. Reverse unpaid entitlement hoạt động.
172. Offset current payout hoạt động.
173. Offset future payout hoạt động.
174. Tạo Negative Balance.
175. Negative Balance theo Currency.
176. Beneficiary inactive vẫn giữ Negative Balance.
177. Tạo Recovery.
178. Recovery có payment/reference.
179. Waiver cần approval.
180. Tạo Clawback Dispute.
181. Revenue Adjustment chạy Commission Impact.
182. Product Change tính delta commission.
183. Contract Value reduction tính adjustment.
184. Co-sale correction tạo adjustment.
185. Multi-Legal Entity Revenue được hỗ trợ.
186. Paying Entity riêng được hỗ trợ.
187. Cross-entity cần authority.
188. Revenue Attribution theo Project được.
189. Revenue Attribution theo Team được.
190. Commission Attribution không dựa owner hiện tại.
191. Sale chỉ xem self.
192. Team Lead xem team.
193. Department Head xem department.
194. Finance xem legal entity.
195. Director xem all theo quyền.
196. Backend enforce scope.
197. Backend enforce field masking.
198. Sửa URL không mở rộng quyền.
199. View không cho Export.
200. Export có audit.
201. Sensitive Arrangement được mask.
202. Beneficiary account được mask.
203. Formula không chạy mã tùy ý.
204. Same idempotency key cùng payload trả cùng kết quả.
205. Same key khác payload báo conflict.
206. Contract cancellation event lặp không tạo clawback trùng.
207. Payment event lặp không tạo recognition trùng.
208. Payout event lặp không trả hai lần.
209. Audit lưu before/after.
210. Audit lưu Arrangement Version.
211. Audit lưu Plan Version.
212. Audit lưu Formula/Base/Rate.
213. Audit lưu Payout.
214. Audit lưu Clawback.
215. Domain event được phát.
216. Event consumer idempotent.
217. Analytics Revenue drill-down đúng scope.
218. Analytics Commission drill-down đúng scope.
219. Capability hỗ trợ công ty tự phát triển.
220. Capability hỗ trợ phân phối Developer ngoài.
221. Capability hỗ trợ tài sản công ty sở hữu.
222. Capability hỗ trợ Customer ký gửi.
223. Capability hỗ trợ Partner-owned resale.
224. Capability hỗ trợ Brokerage-only.
225. Capability tách Gross Funds và Revenue.
226. Capability tách Revenue và Commission.
227. Capability tách Entitlement, Payable và Paid.
228. Capability hỗ trợ Adjustment không ghi đè lịch sử.
229. Capability hỗ trợ Clawback sau payout.
230. Capability quản lý doanh thu và hoa hồng vận hành mà không thay thế kế toán hoặc payroll pháp định.

---

# 128. Quan hệ canonical với các Context liên quan

## 128.1. Lead Context

Revenue chỉ sử dụng published source/attribution facts khi business rule yêu cầu.

Revenue không thay Lead ownership, assignment hoặc care protection.

## 128.2. Party Context

Counterparty, Beneficiary, Referrer và External Collaborator phải tham chiếu canonical Party.

Party merge không sửa Revenue/Commission snapshots lịch sử; giao dịch mới resolve canonical redirect.

## 128.3. Product Context

Revenue sử dụng Project, Listing, Transaction Model, Company Role và Selling Right references.

Revenue không sửa Product records hoặc suy luận Product availability.

## 128.4. Transaction Context

Revenue sử dụng Deal, Transaction Case, Booking, participant facts và approved Co-sale Agreement Version.

Activity hoặc handover không tự tạo/thay Commission Participant. Co-sale correction phải đến từ accepted Transaction fact.

## 128.5. Contract Context

Revenue sử dụng Contract, financial components, Payment Allocation, Receipt, Refund, Forfeiture, Settlement, Cancellation và Reversal facts.

Revenue không sửa Contract/Cash records. Revenue Payment Application chỉ tham chiếu accepted Contract Payment Allocation.

## 128.6. IAM Context

Workforce, employment status, organization hierarchy và effective assignments thuộc IAM.

Revenue snapshot các facts cần thiết tại milestone; organization hiện tại không được viết lại quyền lợi lịch sử.

## 128.7. Documents, Integration, Analytics và Audit

- Documents sở hữu Statement/File/Document/Version evidence.
- Integration sở hữu payroll/bank/ERP/provider transport và execution confirmation.
- Analytics sở hữu certified Metrics và predictive forecasts.
- Audit sở hữu immutable Audit facts.

---

# 129. Anti-patterns và canonical requirements

## AP-REV-001 — Một trường `revenue` hoặc `commission` thay toàn bộ vòng đời

**Không được áp dụng**

Lưu một số tiền duy nhất trên Contract/Deal và coi đó là Entitlement, Recognition, Receivable, Payable và Paid.

**Canonical requirement**

Revenue Arrangement, Entitlement, Recognition, Receivable, Payment Application, Commission Entitlement, Vesting, Payable, Payout và Clawback phải là các lớp riêng.

## AP-REV-002 — Gross transaction funds là company Revenue

**Không được áp dụng**

Dùng toàn bộ Buyer payment, Receipt hoặc Owner proceeds làm doanh thu công ty.

**Canonical requirement**

Phải phân loại financial nature, Legal Entity beneficiary, Counterparty và Revenue Arrangement; collected-on-behalf/escrow/beneficiary proceeds bị loại khỏi company Revenue trừ căn cứ riêng.

## AP-REV-003 — Operational recognition là statutory recognition

**Không được áp dụng**

Dùng `CRM_OPERATIONAL_RECOGNITION` như bút toán hoặc báo cáo pháp định.

**Canonical requirement**

Operational recognition phải được gắn nhãn rõ. Statutory accounting thuộc ERP/General Ledger và policy pháp định.

## AP-REV-004 — Revenue Context tự tạo hoặc sửa Payment

**Không được áp dụng**

Revenue tạo bank transaction, sửa Allocation/Receipt hoặc đánh dấu đã thu tiền.

**Canonical requirement**

Contract Context sở hữu Payment/Allocation/Receipt; Revenue chỉ tạo idempotent Payment Application từ accepted source facts.

## AP-REV-005 — Commission luôn là phần trăm Revenue đã thu

**Không được áp dụng**

Áp một công thức duy nhất cho mọi Transaction Model.

**Canonical requirement**

Commission phải resolve Commission Plan và Funding Source; có thể dựa Contract Value, Revenue, Brokerage Fee, Budget, role pool hoặc milestones.

## AP-REV-006 — Activity hoặc handover tự tạo quyền Commission

**Không được áp dụng**

User thực hiện call/task hoặc nhận handover thì tự trở thành beneficiary.

**Canonical requirement**

Participant phải đến từ structured Transaction/IAM/Party facts và approved Co-sale/Referral/exception process.

## AP-REV-007 — Organization hiện tại viết lại lịch sử Commission

**Không được áp dụng**

Tính manager override hoặc allocation theo team/manager hiện tại.

**Canonical requirement**

Commission Participant Snapshot và Organization Snapshot tại applicable milestone phải được giữ bất biến.

## AP-REV-008 — Nhân sự nghỉ việc mất Entitlement đã hình thành

**Không được áp dụng**

Deactivate user rồi xóa recognized/payable Commission hoặc Negative Balance.

**Canonical requirement**

Offboarding xử lý theo Plan/policy; historical entitlement và recovery obligations vẫn được giữ.

## AP-REV-009 — Sửa approved Entitlement hoặc Statement tại chỗ

**Không được áp dụng**

Ghi đè amount/rate/base/participant trên approved Revenue/Commission records hoặc issued Statement.

**Canonical requirement**

Tạo Adjustment, Reversal, corrected Statement Version hoặc Clawback có liên kết và Audit.

## AP-REV-010 — Batch approved đồng nghĩa đã trả tiền

**Không được áp dụng**

Chuyển Payout sang `PAID` khi batch được duyệt hoặc instruction được tạo.

**Canonical requirement**

Paid state cần authenticated external payroll/bank/ERP confirmation, payment reference và reconciliation.

## AP-REV-011 — Clawback xóa payout lịch sử

**Không được áp dụng**

Sửa `paid_amount` cũ về 0 hoặc xóa Payout khi giao dịch bị hủy.

**Canonical requirement**

Giữ payout history; tạo Clawback Adjustment, recovery/offset/Negative Balance records và reconciliation.

## AP-REV-012 — Plan/Arrangement mới áp dụng hồi tố âm thầm

**Không được áp dụng**

Dùng active version hiện tại để tính lại giao dịch lịch sử.

**Canonical requirement**

Resolution phải theo effective-date policy và lưu exact Arrangement/Plan/Rule versions; retroactive adjustment chỉ khi agreement/policy và approval cho phép.

## AP-REV-013 — Co-sale correction sửa allocation cũ

**Không được áp dụng**

Ghi đè participant/rate sau khi Entitlement hoặc Payout đã phát sinh.

**Canonical requirement**

Accepted Transaction correction tạo Commission Adjustment; phần đã trả xử lý bằng transfer/clawback/recovery phù hợp.

## AP-REV-014 — Revenue Context sở hữu payroll/bank/ERP runtime

**Không được áp dụng**

Lưu credentials, raw provider retries hoặc coi internal instruction là external execution truth.

**Canonical requirement**

Integration sở hữu transport và provider confirmation; Revenue giữ business intent, state và governed references.

## AP-REV-015 — Operational forecasts là certified Metrics

**Không được áp dụng**

Dùng Revenue Context projections trực tiếp làm executive KPI mà không semantic governance.

**Canonical requirement**

Revenue phát governed facts; Analytics Context sở hữu certified grain, formulas, snapshots, access và predictive forecast.

## AP-REV-016 — Formula Engine thực thi mã tùy ý

**Không được áp dụng**

Cho formula/rule chạy arbitrary code hoặc truy cập dữ liệu ngoài approved inputs.

**Canonical requirement**

Formula language phải sandboxed, typed, versioned, deterministic, validated, simulated và bounded bởi approved data contract.

## AP-REV-017 — Candidate examples là exact contracts

**Không được áp dụng**

Dùng table names, endpoints, statuses, Events, permissions, rates hoặc formula examples trong tài liệu này để code trực tiếp.

**Canonical requirement**

Exact database, API, Event, lifecycle, permission, formula và integration contracts phải được khóa trong nguồn canonical tương ứng.

## AP-REV-018 — Mặc định tồn tại hệ thống tiền nhiệm

**Không được áp dụng**

Tự thiết kế old-plan aliases, compatibility layer hoặc historical mappings khi chưa có approved scope.

**Canonical requirement**

`crm_bds_ai` là Greenfield. Historical import chỉ tồn tại khi có scope, source mapping, security review, reconciliation và acceptance criteria riêng.

---

# 130. Kết luận

Revenue and Commission Capability quản trị quyền lợi thương mại của công ty và quyền lợi hoa hồng nội bộ trong `crm_bds_ai`.

Capability phải bảo đảm:

- Gross transaction funds không bị nhầm với Revenue.
- Collected-on-behalf, escrow và beneficiary proceeds được tách.
- Mỗi Revenue Entitlement có Legal Entity, Counterparty, Arrangement/Rule Version và calculation snapshot.
- Operational Recognition, Revenue Receivable và collected Revenue là các lớp riêng.
- Revenue Payment Application chỉ tham chiếu Contract Payment Allocation.
- Revenue và Internal Commission là hai lớp độc lập.
- Mọi Commission Entitlement có Plan, Funding Source, Participant Snapshot và versioned calculation.
- Recognition, Vesting, Payable và Paid được tách biệt.
- Co-sale sử dụng accepted Agreement Version.
- Activity, handover hoặc organization hiện tại không tự thay quyền lợi.
- Offboarding không xóa quyền lợi hoặc Negative Balance lịch sử.
- Payout approval không đồng nghĩa payment execution.
- Advance không tạo Entitlement mới.
- Adjustment và Clawback không xóa lịch sử.
- Multi-Legal Entity và cross-entity funding có authority rõ.
- Formula/rules deterministic, versioned, sandboxed và tái tạo được.
- Documents, Integration, Analytics, Audit và external statutory-system ownership được tôn trọng.
- Cross-context orchestration dùng local transaction, Outbox, idempotency và reconciliation.
- Revenue Context không thay General Ledger, payroll hoặc tax system.

> Revenue Context sở hữu commercial entitlement và internal commission lifecycle; nó không sở hữu Contract cash truth, Deal responsibility, Workforce truth, bank/payroll execution, certified analytics hoặc statutory accounting.
