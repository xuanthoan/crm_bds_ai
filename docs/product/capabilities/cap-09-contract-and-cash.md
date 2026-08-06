# CRM_BDS_AI — CAPABILITY 09: CONTRACT AND CASH

## Contract, Multi-Party Transaction, Payment Schedule, Receivable, Payment, Allocation, Receipt, Refund, Settlement, Cancellation and Adjustment

**Document ID:** `PROD-CAP-CON-001`
**Canonical path:** `docs/product/capabilities/cap-09-contract-and-cash.md`
**Product:** `crm_bds_ai`
**Version:** `1.0.0`  
**Status:** `Accepted / Product Capability Baseline`
**Document type:** `Product Capability Specification`
**Primary capability code:** `CAP-CON`
**Primary owning Context:** `contract`
**Owner:** `Product Owner`
**Co-owner:** `Contract Domain Owner`
**Reviewers:** `Architecture Owner`, `Party Domain Owner`, `Product Domain Owner`, `Transaction Domain Owner`, `Revenue Domain Owner`, `Documents Owner`, `Integration Owner`, `Activity Domain Owner`, `Analytics Owner`, `Audit Owner`, `Security Owner`, `Database Owner`, `API Owner`, `Event Architecture Owner`, `Operations Owner`, `QA Owner`
**Effective date:** `2026-08-05`  
**Last reviewed:** `2026-08-05`  
**Classification:** `INTERNAL`

---

# 0. Phạm vi thẩm quyền và quan hệ tài liệu

Tài liệu này là nguồn canonical cho:

- Product outcomes của Contract and Cash Capability.
- Business meanings của Contract, Contract Party, Payment Plan, Receivable, Payment Transaction, Allocation, Receipt, Refund, Credit Balance, Transfer, Offset và transaction Settlement.
- Contract amendment, cancellation, termination, replacement, completion và reconciliation.
- Capability boundaries, invariants, acceptance outcomes và anti-patterns.
- Đầu vào phân tích cho Contract Context Implementation Pack.

Tài liệu này không phải nguồn exact cho:

- Physical database schema hoặc DDL.
- Exact API paths, request/response payloads.
- Exact Event names, envelope hoặc payloads.
- Exact permission codes, scopes, masking hoặc role matrix.
- Exact state machines, status codes, numbering rules, formulas hoặc tolerance.
- Exact Document/File storage, signature-provider runtime hoặc generated-document format.
- Exact bank/provider integration, accounting entries hoặc statutory reporting.
- Exact Revenue/Commission recognition, payable, payout hoặc clawback calculations.
- Exact screen routes, certified Metrics, queue, retry, retention hoặc deployment configuration.

Nguồn exact tương ứng:

| Chủ đề | Nguồn canonical |
|---|---|
| Thuật ngữ | Domain Glossary |
| Product requirements | PRD |
| Context ownership | Source of Truth Matrix |
| Architecture boundaries | Architecture Overview, Context Map và Accepted ADRs |
| Contract behavior chi tiết | Contract Context Implementation Pack |
| Database | Contract Context DB Specification và Alembic historical imports |
| API | OpenAPI |
| Events | JSON Schema, AsyncAPI và Event Registry |
| Permissions/scopes/masking/SoD | Security registries và matrices |
| Customer/Party identity | Party Context contracts |
| Listing/Ownership/Selling Right/Availability | Product Context contracts |
| Deal/Booking/Deposit Commitment | Transaction Context contracts |
| Revenue/Commission | Revenue Context contracts |
| File/Document/Version/signature evidence | Documents Context contracts |
| Bank/provider/ERP transport | Integration Context contracts |
| Operational Tasks/SLA instances | Activity Context contracts |
| Certified financial/contract Metrics | Analytics Context và Metric Registry |
| Immutable Audit facts | Audit Context |
| Runtime jobs/incidents | Operations Context |
| Công việc hiện tại | Current Sprint Detailed Execution Pack |

**Capability không đồng nghĩa Bounded Context.** Capability này chủ yếu được thực hiện bởi `contract` Context. Nó quản lý legal/cash transaction records trong phạm vi CRM, nhưng không được direct-write `party`, `product`, `transaction`, `revenue`, `documents`, `integration`, `analytics` hoặc `audit`.

Các phần candidate lifecycle, data model, operations, permissions, Events, screens và reports chỉ là design input. Chúng không được dùng thay machine-readable contracts hoặc Context Packs đã được chấp nhận.

---
# 1. Mục tiêu của capability

Contract and Cash Capability quản lý giai đoạn pháp lý và dòng tiền giao dịch kể từ khi Transaction Case hoặc Booking được Contract Context chấp nhận cho đến khi Contract được hoàn thành, chấm dứt hoặc xử lý reconciliation đầy đủ.

Capability phải trả lời được:

- Contract nào được tạo từ Transaction Case, Booking hoặc approved legal intake nào.
- Contract type, Contract Group, version, legal status và effectiveness là gì.
- Buyer, Seller, Owner, Payer, Signer, Representative và Beneficiary là những Party nào.
- Ownership, payment obligation và actual contribution khác nhau ra sao.
- Product, Price, Policy, Party và commercial versions nào đã được snapshot.
- Payment Plan và Receivables nào đã phát sinh.
- Payment Transaction nào đã được xác minh.
- Payment được phân bổ vào nghĩa vụ nào.
- Receipt nào đã phát hành, hủy hoặc thay thế.
- Outstanding, overdue, overpayment và Credit Balance là bao nhiêu.
- Refund, Transfer, Offset hoặc Settlement nào đang chờ xử lý.
- Khoản nào là principal, fee, collected-on-behalf, escrow hoặc beneficiary proceeds.
- Contract cancellation/adjustment ảnh hưởng Product, Transaction và Revenue thế nào.
- Hợp đồng có đủ điều kiện completion hay chưa.
- Mọi thay đổi có thể tái tạo từ versions, documents, approvals, allocations và evidence hay không.

Capability phải hỗ trợ:

- Nhiều Transaction Models và Contract Types.
- Nhiều Buyer, Seller, Owner, Payer, Signer và Beneficiary.
- Contract Group, Appendix, Amendment, Replacement, Termination và Liquidation.
- Payment Plan nhiều version và milestones.
- Receivable, adjustment, waiver, penalty và aging.
- Payment import/manual finance entry có kiểm soát.
- Unidentified Payment và matching suggestion.
- Many-to-many Payment Allocation.
- Partial payment, overpayment, underpayment và Credit Balance.
- Immutable Receipt issuance/cancellation/replacement.
- Refund, forfeiture, transfer và offset.
- Owner/Developer/Partner transaction Settlement.
- Contract/Product/Party/Area/Price adjustments.
- Reconciliation và Contract completion.
- Multi-Legal Entity, maker–checker–approver và Segregation of Duties.
- Full versioning, traceability và Audit evidence.
- Integration với accounting/ERP mà không biến CRM thành statutory accounting system.

Nguyên tắc canonical:

> Contract, Payment Plan, Receivable, Payment Transaction, Allocation, Receipt, Refund, Settlement và Revenue là các lớp dữ liệu riêng. Contract Context quản lý legal/cash transaction truth trong phạm vi CRM; Revenue Context quyết định Revenue/Commission; Documents Context sở hữu File/Document evidence; accounting/ERP vẫn là nguồn pháp định khi doanh nghiệp sử dụng.

---
# 2. Vị trí của capability trong kiến trúc

Contract Context sử dụng:

- `platform`: Workflow/Approval/SLA definitions, Business Calendar, Numbering, templates/configuration references.
- `iam`: authenticated identity, effective access context, delegation, authorization và SoD decisions.
- `party`: canonical Party/Customer identity và redirect.
- `lead`: attribution/source references khi cần downstream lineage.
- `product`: Project, Asset, Listing, Ownership, Selling Right, Price/Policy snapshots và authoritative inventory decisions.
- `matching`: Match/Shortlist references khi cần lineage.
- `transaction`: Deal, Transaction Case, Booking, parties, commercial snapshots và Deposit Commitment.
- `documents`: Contract/Appendix/Receipt/Settlement Documents, versions, hashes và signature evidence.
- `integration`: bank/provider/ERP transport, external payment/contract confirmations và delivery evidence.
- `activity`: Task, Appointment, Interaction và operational SLA instances.
- `audit`: immutable evidence của sensitive/legal/financial actions.
- `operations`: batch, reconciliation jobs và incident runtime.

Contract Context cung cấp:

- Cho `transaction`: accepted/rejected handoff, Contract status và governed deposit-payment projections.
- Cho `product`: Contract/inventory decision requests và accepted legal facts; Product vẫn quyết định Listing Availability.
- Cho `revenue`: Contract value components, effective/cancellation facts, valid allocations/receipts, fees, forfeitures và settlement references.
- Cho `analytics`: governed Contract/Cash facts; Analytics vẫn sở hữu certified Metrics.
- Cho `documents`: document-generation/signature requests và legal relationships.
- Cho accounting/ERP qua `integration`: payment, receipt, refund, settlement và reconciliation references.

Luồng khái quát:

```text
Transaction Handoff
→ Contract Preparation/Review/Signing
→ Contract Effectiveness
→ Payment Plan
→ Receivable
→ Payment Transaction
→ Allocation
→ Receipt
→ Reconciliation
→ Refund/Settlement khi cần
→ Completion/Termination
```

Cross-context propagation sử dụng local transactions, Transactional Outbox, idempotent commands/consumers, Process Manager và reconciliation. Không dùng distributed transaction hoặc cross-schema business writes.

---
# 3. Ranh giới sở hữu dữ liệu

## 3.1. Contract Context sở hữu

- Contract Group, Contract, Contract Version và legal/commercial/product/party snapshots.
- Contract parties, official ownership/payment-obligation allocations và contribution projections.
- Contract approval, signing requirements/state references, effectiveness và completion.
- Amendment, Appendix, Replacement, Cancellation, Termination và Liquidation.
- Payment Plan, versions, milestones và due-date resolution.
- Receivable, adjustment, waiver, penalty, aging và payment notice intent.
- Payment Transaction representation trong CRM, verification/identification/allocation state.
- Unidentified Payment và payment-matching candidates.
- Payment Allocation và Reversal.
- Receipt business record, numbering, issuance, cancellation và replacement.
- Deposit conversion.
- Credit Balance, Payment Transfer và Offset.
- Refund request/decision/payment reference và reconciliation state.
- Owner/Seller/Developer/Partner transaction Settlement.
- Reconciliation Case.
- Contract handoff intake và completion checklist.
- Contract-originated business facts và Audit requests.

## 3.2. Contract Context không sở hữu

- Canonical Party, Customer, Customer Identity hoặc Customer profile truth: `party`.
- Project, Asset, Listing, Ownership, Selling Right, Availability hoặc Commercial Lock: `product`.
- Deal, Transaction Case, Booking hoặc Deposit Commitment source: `transaction`.
- Revenue Entitlement, Revenue Recognition, Commission, payout hoặc clawback: `revenue`.
- Binary File, Document, Document Version, OCR/extraction hoặc signature evidence: `documents`.
- Bank statement, payment-provider, signature-provider, ERP transport, credentials, retry hoặc provider reconciliation runtime: `integration`.
- Task, Appointment, Interaction hoặc operational Timeline facts: `activity`.
- Certified Metrics và analytical snapshots: `analytics`.
- Immutable Audit facts: `audit`.
- General Ledger, double-entry accounting, tax ledgers hoặc statutory financial statements: accounting/ERP system.
- Job, queue, DLQ hoặc incident runtime: `operations`.

## 3.3. Contract records và Documents

Contract owns legal relationships, version references, signing requirements và legal status.

Documents owns:

- Binary object.
- File metadata.
- Document và Document Version.
- Generated artifacts.
- Document hash evidence.
- Signature evidence/certificate artifact.
- Access/retention/legal-hold controls.

Contract chỉ giữ `document_id`, `document_version_id`, approved hash snapshot/reference và legal relationship metadata. Permanent URLs không phải canonical document identity.

## 3.4. Payment representation và bank/ERP boundary

Contract Context có thể sở hữu Payment Transaction representation cần cho transaction reconciliation.

`integration` sở hữu:

- Bank/provider connection.
- Authentication/credentials.
- Raw statement/webhook transport.
- Delivery attempts, retries và provider payload references.
- ERP synchronization runtime.

Bank hoặc approved payment provider là nguồn của external money movement. CRM verification/allocation không biến CRM thành bank ledger hoặc General Ledger.

## 3.5. Settlement và Revenue

Transaction Settlement trong Contract Context xác định cash payable/transferable cho Owner, Seller, Developer hoặc Partner trong một giao dịch.

Revenue Context sở hữu:

- Revenue entitlement.
- Recognition.
- Revenue receivable từ đối tác.
- Commission entitlement/calculation.
- Payable/payout.
- Adjustment/clawback.

Gross funds, Receipt hoặc Settlement không mặc định là Revenue.

## 3.6. Product inventory sau Contract change

Contract chỉ tạo inventory-impact decision/request.

Product Context quyết định:

- Contracted/Sold/Release Pending/Released.
- Relist eligibility.
- Availability.
- Commercial Lock lifecycle.

Contract cancellation không tự mở lại Listing.

---
# 4. Các lớp dữ liệu bắt buộc phải tách biệt

## 4.1. Contract

Văn bản và quan hệ pháp lý giữa các bên.

## 4.2. Payment Plan

Kế hoạch nghĩa vụ thanh toán theo thời gian.

## 4.3. Receivable

Khoản phải thu thực tế được sinh ra từ Payment Plan và điều kiện hợp đồng.

## 4.4. Payment Transaction

Sự kiện tiền thực tế được ghi nhận từ ngân hàng, tiền mặt, cổng thanh toán hoặc nguồn khác.

## 4.5. Payment Allocation

Cách một khoản tiền được phân bổ vào một hoặc nhiều Receivable.

## 4.6. Receipt

Chứng từ nghiệp vụ xác nhận việc nhận tiền hoặc phân bổ tiền theo quy định doanh nghiệp.

## 4.7. Settlement

Quá trình xác định và thanh toán số tiền ròng phải chuyển cho Owner, Seller, Developer hoặc Partner.

## 4.8. Revenue

Khoản công ty được hưởng.

Revenue thuộc Revenue Context và không được đồng nhất với tiền nhận trong Contract Context.

---

# 5. Nguyên tắc thiết kế cốt lõi

## 5.1. Không ghi đè hợp đồng đã ký

Hợp đồng đã ký không được sửa nội dung trực tiếp.

Thay đổi phải thông qua:

* Amendment.
* Appendix.
* Correction agreement.
* Replacement contract.
* Termination agreement.
* Cancellation workflow.

## 5.2. Không sửa phiếu thu đã duyệt

Phiếu thu approved/issued không được sửa.

Nếu sai:

1. Tạo yêu cầu hủy.
2. Nêu lý do.
3. Phê duyệt.
4. Hủy phiếu cũ.
5. Tạo phiếu thay thế.
6. Liên kết hai phiếu.
7. Giữ lịch sử đầy đủ.

## 5.3. Receivable phải được sinh từ nguồn nghiệp vụ

Không cho user tự nhập một khoản công nợ không có căn cứ.

Nguồn hợp lệ:

* Payment milestone.
* Contract amendment.
* Penalty/fee decision.
* Refund recovery.
* Approved adjustment.
* Settlement reconciliation.

## 5.4. Payment không đồng nghĩa Receipt

Có thể có:

* Tiền đã vào tài khoản nhưng chưa xác định.
* Tiền đã xác định nhưng chưa phát hành phiếu thu.
* Phiếu thu nháp nhưng tiền chưa đối soát.
* Phiếu thu đã hủy.
* Khoản thu hộ không phải doanh thu.

## 5.5. Một Payment có thể phân bổ nhiều Receivable

Ví dụ Customer chuyển một khoản thanh toán cho:

* Đợt 1.
* Phí dịch vụ.
* Phí hồ sơ.

## 5.6. Một Receivable có thể được thanh toán bởi nhiều Payment

Ví dụ:

* Customer chính thanh toán một phần.
* Co-buyer thanh toán phần còn lại.
* Ngân hàng giải ngân bổ sung.

## 5.7. Không mở lại Listing ngay khi hủy hợp đồng

Hủy hợp đồng chỉ tạo yêu cầu đánh giá inventory.

Listing chỉ được mở lại khi:

* Hợp đồng chấm dứt hợp lệ.
* Lock được xử lý.
* Refund/forfeit đủ điều kiện.
* Legal xác nhận.
* Inventory xác nhận.
* Không còn tranh chấp.
* Product, Asset, Listing and Inventory Capability thực hiện transition.

## 5.8. Tiền công ty giữ hộ không mặc định là doanh thu

Mọi khoản tiền phải có financial nature:

* Principal purchase payment.
* Deposit.
* Brokerage fee.
* Service fee.
* Tax/fee collected on behalf.
* Owner proceeds.
* Developer proceeds.
* Escrow.
* Refundable amount.
* Other.

---

# 6. Contract models và business scenarios

## 6.1. Công ty tự phát triển và trực tiếp bán

Đặc điểm:

* Seller là Legal Entity nội bộ.
* Buyer thanh toán cho Legal Entity nội bộ hoặc tài khoản được ủy quyền.
* Customer receivable thuộc công ty.
* Tiền bán bất động sản có thể là doanh thu bán hàng.
* Revenue Context ghi nhận Revenue theo accepted policy và Contract facts.
* Internal Commission có thể dựa trên ngân sách bán hàng.

## 6.2. Pháp nhân dự án nội bộ bán

Đặc điểm:

* Seller là Project Legal Entity.
* CRM Enterprise có thể gồm nhiều Legal Entity.
* Payment Receiver có thể khác Seller nhưng phải có authority.
* Revenue/commission cần xác định đúng Legal Entity.

## 6.3. Phân phối dự án chủ đầu tư ngoài

Đặc điểm:

* Hợp đồng mua bán có thể ký trực tiếp giữa Buyer và Developer.
* Công ty có thể chỉ giữ bản sao hoặc theo dõi trạng thái hợp đồng.
* Buyer payment chủ yếu trả Developer.
* Công ty có thể thu Booking/Deposit theo quyền.
* Revenue của công ty là Distribution Commission, không phải toàn bộ tiền Buyer trả.
* Receivable của công ty đối với Developer thuộc Revenue and Commission Capability.

## 6.4. Tài sản công ty sở hữu bán lại

Đặc điểm:

* Owner và Seller có thể là cùng hoặc khác Legal Entity nội bộ.
* Có thể cần settlement nội bộ.
* Giá bán và payment schedule do công ty quản lý.

## 6.5. Customer ký gửi hoặc bán lại

Đặc điểm:

* Seller là Customer Owner hoặc nhiều Co-owner.
* Buyer thanh toán cho Owner, công ty hoặc escrow tùy mandate.
* Brokerage Fee là khoản riêng.
* Purchase money không mặc định là revenue công ty.
* Owner Settlement cần xác định tiền gộp, khấu trừ và số ròng.

## 6.6. Partner-owned resale

Tương tự Customer resale nhưng Owner là Partner hoặc tổ chức ngoài.

## 6.7. Đất nền và đất riêng lẻ

Phải hỗ trợ:

* Giá theo diện tích tạm tính.
* Giá theo diện tích chính thức.
* Điều chỉnh khi đo đạc.
* Nhiều thửa/lô.
* Điều kiện tách thửa.
* Mốc bàn giao ranh giới.
* Nghĩa vụ hoàn thiện pháp lý.
* Tax/fee allocation giữa các bên.

---

# 7. Candidate Contract Type vocabulary — Context-specific, pending validation

> Exact codes, legal meaning và applicability thuộc Contract Context Pack.

```text
PROPERTY_SALE_CONTRACT
PROPERTY_TRANSFER_CONTRACT
LAND_TRANSFER_CONTRACT
DEPOSIT_AGREEMENT
BOOKING_AGREEMENT
RESERVATION_AGREEMENT
BROKERAGE_AGREEMENT
CONSIGNMENT_AGREEMENT
SERVICE_AGREEMENT
COOPERATION_AGREEMENT
LEASE_CONTRACT
PAYMENT_AGREEMENT
SETTLEMENT_AGREEMENT
TERMINATION_AGREEMENT
LIQUIDATION_MINUTES
CONTRACT_APPENDIX
OTHER
```

Một Transaction Case có thể có nhiều Contract document khác nhau.

Ví dụ:

* Booking Agreement.
* Deposit Agreement.
* Sale Contract.
* Appendix.
* Liquidation Minutes.

---

# 8. Contract Group

## 8.1. Khái niệm

Contract Group gom tất cả tài liệu pháp lý thuộc cùng một giao dịch.

Ví dụ:

```text
Contract Group
├── Deposit Agreement
├── Property Sale Contract
├── Appendix 01
├── Price Adjustment Appendix
└── Liquidation Minutes
```

## 8.2. Mục tiêu

* Theo dõi tài liệu gốc.
* Theo dõi phụ lục.
* Xác định tài liệu đang có hiệu lực.
* Không làm mất lịch sử.
* Hỗ trợ thay thế và chấm dứt.

---

# 9. Nguồn tạo Contract

Contract có thể được tạo từ:

* Transaction Case.
* Booking.
* Deposit Commitment.
* External Developer Contract.
* Manual legal intake có quyền.
* Approved historical Contract intake, khi có phạm vi riêng.
* Contract replacement.
* Approved amendment workflow.

Nguồn chính phải lưu:

* Transaction Case ID.
* Deal ID.
* Booking ID.
* Listing ID.
* Asset ID.
* Customer ID.
* External Contract ID.
* Source system.

---

# 10. Điều kiện tạo Contract

Điều kiện tối thiểu có thể gồm:

1. Transaction Case hợp lệ.
2. Listing và Asset xác định.
3. Transaction Model xác định.
4. Seller/Buyer parties xác định.
5. Internal Legal Entity xác định.
6. Commercial snapshot khóa.
7. Booking/Deposit trạng thái phù hợp nếu bắt buộc.
8. Mandate và legal readiness phù hợp.
9. Không có identity conflict Critical.
10. Không có contract duplicate.
11. User có quyền.
12. Stage gate hoàn tất.

Có thể tạo Contract Draft khi chưa đủ hồ sơ, nhưng không được chuyển Review/Signing nếu thiếu điều kiện bắt buộc.

---

# 11. Contract Code và số hợp đồng

## 11.1. Contract Code

Mã hệ thống nội bộ, không thay đổi.

Ví dụ:

```text
CTR-2026-000123
```

## 11.2. Contract Number

Số hợp đồng pháp lý hiển thị trên văn bản.

Có thể theo:

* Legal Entity.
* Project.
* Contract type.
* Năm.
* Sequence.
* External Developer format.

## 11.3. External Contract Number

Dùng khi hợp đồng do Developer/Partner phát hành.

## 11.4. Không tái sử dụng số đã hủy

Số hợp đồng đã cấp không được dùng lại, trừ quy định đặc biệt có audit.

---

# 12. Candidate Contract lifecycle — pending validation

> Exact states, transitions, guards và terminal semantics thuộc Contract Context Implementation Pack.

```text
DRAFT
COLLECTING_INFORMATION
PENDING_DOCUMENTS
PENDING_INTERNAL_REVIEW
PENDING_LEGAL_REVIEW
PENDING_FINANCE_REVIEW
PENDING_APPROVAL
APPROVED_FOR_SIGNING
PENDING_SIGNATURE
PARTIALLY_SIGNED
FULLY_SIGNED
PENDING_EFFECTIVENESS
EFFECTIVE
PERFORMING
PAYMENT_COMPLETED
HANDOVER_PENDING
COMPLETED
AMENDMENT_PENDING
SUSPENDED
CANCELLATION_REQUESTED
TERMINATION_PENDING
TERMINATED
CANCELLED
LIQUIDATED
REPLACED
ARCHIVED
DISPUTED
```

---

# 13. Candidate Contract status dimensions — pending validation

> Workflow, legal, payment, receivable, document, inventory projection và completion là các dimensions riêng; exact codes thuộc machine contracts.

Không sử dụng một status duy nhất cho toàn bộ giao dịch.

## 13.1. Workflow Status

* Draft.
* Review.
* Approval.
* Signing.
* Effective.
* Completed.
* Cancelled.

## 13.2. Legal Status

```text
NOT_REVIEWED
UNDER_REVIEW
LEGALLY_READY
LEGALLY_READY_WITH_CONDITIONS
SIGNED
EFFECTIVE
SUSPENDED
DISPUTED
TERMINATED
```

## 13.3. Payment Status

```text
NOT_STARTED
PAYMENT_PENDING
PARTIALLY_PAID
CURRENT
OVERDUE
FULLY_PAID
OVERPAID
REFUND_PENDING
REFUNDED
DISPUTED
```

## 13.4. Receivable Status

```text
NO_RECEIVABLE
OPEN
PARTIALLY_SETTLED
OVERDUE
CLOSED
CANCELLED
ADJUSTED
```

## 13.5. Document Status

```text
INCOMPLETE
COMPLETE
SIGNATURE_PENDING
FULLY_EXECUTED
SUPERSEDED
ARCHIVED
```

## 13.6. Inventory Status Projection

* Contract Lock.
* Contracted.
* Sold Pending Completion.
* Sold.
* Release Pending.
* Released.

Nguồn chân lý inventory thuộc Product, Asset, Listing and Inventory Capability.

## 13.7. Completion Status

```text
NOT_STARTED
IN_PROGRESS
PAYMENT_COMPLETE
HANDOVER_COMPLETE
SETTLEMENT_COMPLETE
FULLY_COMPLETE
```

---

# 14. Contract Stage Gate

## 14.1. Approved for Signing

Yêu cầu có thể gồm:

* Buyer/Seller đủ.
* Identity verification.
* Commercial snapshot.
* Contract value.
* Payment Plan.
* Legal checklist.
* Mandate.
* Ownership.
* Approval.
* Document template hợp lệ.

## 14.2. Fully Signed

Yêu cầu:

* Tất cả required signers đã ký.
* Signature record hợp lệ.
* Không có signature rejection.
* Document hash khớp.

## 14.3. Effective

Yêu cầu theo Contract:

* Fully signed.
* Deposit/payment condition.
* External approval.
* Effective date.
* Legal condition.
* Document issuance.

## 14.4. Completed

Không chỉ dựa trên Fully Paid.

Có thể yêu cầu:

* Payment completed.
* Handover completed.
* Settlement completed.
* Documents delivered.
* No unresolved dispute.
* Revenue and Commission Capability reconciliation hoặc trigger hoàn tất khi policy yêu cầu.

---

# 15. Contract Parties

Một Contract có thể có nhiều Party.

Các vai trò chuẩn:

```text
PRIMARY_BUYER
CO_BUYER
BUYER_REPRESENTATIVE
PRIMARY_SELLER
CO_SELLER
LEGAL_SELLER
OWNER
CO_OWNER
SELLER_REPRESENTATIVE
PAYER
CO_PAYER
BORROWER
CO_BORROWER
GUARANTOR
PAYMENT_RECEIVER
BENEFICIARY
DEVELOPER
DISTRIBUTOR
BROKER
INTERNAL_LEGAL_ENTITY
ESCROW_AGENT
WITNESS
NOTARY
AUTHORIZED_SIGNER
OTHER
```

---

# 16. Buyer, Owner, Payer và Signer phải độc lập

Một người có thể đồng thời là:

* Buyer.
* Payer.
* Signer.
* Owner sau giao dịch.

Nhưng hệ thống không được tự suy ra các vai trò là giống nhau.

Ví dụ:

* Cha mẹ là Payer.
* Con là Buyer.
* Người đại diện ký thay.
* Hai Buyer nhưng chỉ một người thanh toán.
* Công ty mua, giám đốc là Signer.

---

# 17. Tỷ lệ Ownership, Payment Obligation và Contribution

Phải tách ba khái niệm:

## 17.1. Ownership Percentage

Tỷ lệ sở hữu chính thức hoặc dự kiến theo Contract.

## 17.2. Payment Obligation Percentage

Tỷ lệ nghĩa vụ thanh toán mà mỗi Party chịu.

## 17.3. Actual Contribution Percentage

Tỷ lệ tiền thực tế mỗi Party đã đóng.

Ba tỷ lệ có thể khác nhau.

Ví dụ:

* Hai người sở hữu 50/50.
* Một người chịu nghĩa vụ 100%.
* Người thứ ba thanh toán thay một phần.

---

# 18. Kiểm tra tổng tỷ lệ

## 18.1. Ownership

Khi hợp đồng yêu cầu tỷ lệ:

* Tổng active Ownership Percentage phải bằng 100%.

## 18.2. Payment Obligation

Có thể:

* Tổng bằng 100%.
* Hoặc dùng joint-and-several obligation không chia tỷ lệ.

## 18.3. Actual Contribution

Được tính từ Payment Allocation, không nhập tay làm nguồn chân lý.

---

# 19. Party Identity Snapshot

Khi Contract được ký, phải snapshot:

* Tên pháp lý.
* Party type.
* Identity document metadata.
* Tax code nếu tổ chức.
* Address.
* Representative.
* Authorization.
* Contact.
* Role.
* Verification status.

Customer Profile thay đổi sau đó không được làm thay đổi nội dung hợp đồng lịch sử.

---

# 20. Thay đổi Party trước và sau khi ký

## 20.1. Trước khi ký

Có thể cập nhật Draft qua version.

## 20.2. Sau khi ký

Không được sửa trực tiếp.

Phải tạo:

* Party Change Amendment.
* Transfer Agreement.
* Replacement Contract.
* Correction Appendix.
* Termination and Re-contract workflow.

## 20.3. Sửa lỗi đánh máy

Dù chỉ là lỗi nhỏ, nếu tài liệu đã ký phải dùng correction process phù hợp.

---

# 21. Contract Product Snapshot

Phải snapshot:

* Project.
* Asset.
* Listing.
* Listing version.
* Asset characteristics.
* Unit/plot/parcel.
* Area.
* Legal description.
* Seller.
* Owner.
* Mandate.
* Transaction Model.
* Internal Legal Entity.
* Price version.
* Policy version.
* Booking.
* External IDs.
* Physical/legal status tại thời điểm ký.

---

# 22. Contract Commercial Snapshot

Phải lưu:

* Base price.
* Agreed price.
* Discount.
* Tax.
* Fees.
* Brokerage/service fee.
* Maintenance fee.
* Optional items.
* Currency.
* Rounding.
* Payment schedule.
* Deposit already paid.
* Amount credited.
* Refundability.
* Special conditions.
* Approval references.
* Offer/Proposal/Booking versions.

Không chỉ lưu một trường `contract_value`.

---

# 23. Giá trị Contract

Có thể gồm:

* Gross Contract Value.
* Net Property Value.
* Tax Amount.
* Fees.
* Deposit Credit.
* Amount Payable.
* Amount Collected on Behalf.
* Brokerage Fee.
* Service Fee.
* Owner Net Amount.
* Developer Payable.
* Other Financial Components.

Mỗi component phải có financial nature.

---

# 24. Candidate Contract Financial Component vocabulary — pending validation

> Exact financial-nature codes và Revenue mappings thuộc Contract/Revenue contracts.

Các loại tham khảo:

```text
PROPERTY_PRINCIPAL
LAND_VALUE
CONSTRUCTION_VALUE
VAT
MAINTENANCE_FEE
BROKERAGE_FEE
SERVICE_FEE
ADMIN_FEE
TRANSFER_FEE
NOTARY_ESTIMATE
REGISTRATION_ESTIMATE
PENALTY
DISCOUNT
REBATE
DEPOSIT_CREDIT
OWNER_PROCEEDS
DEVELOPER_PROCEEDS
ESCROW_AMOUNT
COLLECTED_ON_BEHALF
OTHER
```

Mỗi component xác định:

* Người phải trả.
* Người được nhận.
* Có phải revenue công ty hay không.
* Có phải khoản thu hộ hay không.
* Có được chiết khấu không.
* Có hoàn lại không.
* Có chịu thuế hay không.
* Revenue and Commission Capability classification reference.

---

# 25. Contract Version

## 25.1. Draft Version

Có thể chỉnh sửa trước khi ký.

## 25.2. Approved Version

Khóa nội dung để ký.

## 25.3. Signed Version

Bất biến.

## 25.4. Superseded Version

Bị thay thế bởi Appendix hoặc Contract mới nhưng vẫn giữ lịch sử.

## 25.5. Version chứa

* Snapshot JSON.
* Template version.
* Commercial version.
* Party version.
* Payment Plan version.
* Document hash.
* Approval.
* Effective dates.
* Change reason.

---

# 26. Contract Template

Template được cấu hình theo:

* Contract type.
* Transaction Model.
* Project.
* Legal Entity.
* Seller type.
* Jurisdiction.
* Language.
* Customer type.
* Effective date.

Contract phải lưu Template Version được sử dụng.

---

# 27. Tạo tài liệu Contract

Quy trình:

1. Chọn Template.
2. Resolve dữ liệu.
3. Validate required fields.
4. Generate draft.
5. Legal review.
6. Commercial review.
7. Finance review.
8. Approval.
9. Freeze version.
10. Generate signing document.
11. Lưu document hash.
12. Gửi signing request qua Documents/Integration contracts.
13. Theo dõi legal signing state từ accepted Documents/Integration facts.

---

# 28. Contract Document Reference Metadata

Mỗi tài liệu lưu:

* Contract.
* Contract version.
* Document type.
* Document ID và Document Version ID.
* Document reference.
* Document hash.
* Mime type.
* Page count nếu có.
* Language.
* Generated/manual.
* Signed/unsigned.
* Signature status.
* Access policy.
* Created at.
* Effective at.
* Superseded at.

Documents Context quản lý File/Document/Version trong approved Object Storage. Contract chỉ giữ Document references và legal relationship metadata.

---

# 29. Signing requirements, state và Documents/Integration boundary

> Contract sở hữu signing requirements và legal signing state. Documents sở hữu signature evidence artifacts; Integration sở hữu signature-provider transport.

## 29.1. Signature Method

```text
WET_SIGNATURE
ELECTRONIC_SIGNATURE
DIGITAL_SIGNATURE
EXTERNAL_PLATFORM
NOTARIZED
OTHER
```

## 29.2. Signature Record

* Contract version.
* Signer Party.
* Signer role.
* Method.
* Signed at.
* Location.
* External signature ID.
* Certificate metadata.
* Document hash.
* Status.
* Evidence Document reference.

## 29.3. Partial Signature

Contract có thể có nhiều người ký.

Trạng thái chỉ Fully Signed khi đủ required signer.

---

# 30. Contract Effectiveness

Hợp đồng có thể có hiệu lực:

* Ngay khi ký đủ.
* Tại ngày cụ thể.
* Khi nhận Deposit.
* Khi Developer xác nhận.
* Khi hoàn tất thủ tục.
* Khi đáp ứng điều kiện tiên quyết.

Phải lưu:

* Effectiveness rule.
* Required events.
* Satisfied at.
* Effective date.
* Verification.

---

# 31. External Contract

Trong mô hình Developer ngoài:

* CRM có thể không tạo hợp đồng chính.
* Lưu External Contract reference.
* Lưu bản sao.
* Lưu parties.
* Lưu value.
* Lưu payment plan.
* Lưu signing/effectiveness status.
* Lưu data confidence.
* Lưu source.

Không tự coi external contract effective chỉ vì file được upload.

---

# 32. Contract Amendment

> Amendment types dưới đây là candidate vocabulary; exact legal workflows thuộc Contract Context Pack.

## 32.1. Loại Amendment

```text
PRICE_CHANGE
PAYMENT_SCHEDULE_CHANGE
PARTY_CHANGE
PRODUCT_CHANGE
AREA_ADJUSTMENT
TERM_EXTENSION
FEE_CHANGE
POLICY_CHANGE
LEGAL_CORRECTION
REPRESENTATIVE_CHANGE
OTHER
```

## 32.2. Amendment phải lưu

* Contract gốc.
* Amendment code.
* Loại.
* Before.
* After.
* Reason.
* Financial impact.
* Inventory impact.
* Revenue impact.
* Commission impact trigger.
* Approval.
* Signatures.
* Effective date.

---

# 33. Contract Appendix

Appendix là tài liệu bổ sung hoặc thay đổi một phần hợp đồng.

Không được:

* Xóa nội dung gốc.
* Ghi đè Signed Version.
* Thay đổi Payment Plan âm thầm.

Sau khi Appendix effective:

* Tạo Payment Plan Version mới nếu cần.
* Điều chỉnh Receivable.
* Tạo reconciliation.
* Gửi event Revenue and Commission Capability.

---

# 34. Contract Duplicate Check

Kiểm tra theo:

* Booking.
* Transaction Case.
* Listing.
* Buyer.
* Seller.
* Contract type.
* External Contract Number.
* Active status.

Không chặn:

* Appendix.
* Deposit Agreement và Sale Contract cùng group.
* Replacement contract có workflow.

---

# 35. Payment Plan

## 35.1. Khái niệm

Payment Plan là lịch nghĩa vụ thanh toán theo hợp đồng.

## 35.2. Nguồn

* Booking commercial snapshot.
* Sales Policy.
* Negotiated terms.
* Contract template.
* External Developer schedule.
* Amendment.

## 35.3. Một Contract có nhiều Payment Plan Version

Version mới được tạo khi:

* Thay đổi giá.
* Thay đổi thời hạn.
* Thay đổi milestone.
* Chuyển sản phẩm.
* Điều chỉnh diện tích.
* Phụ lục.

---

# 36. Payment Milestone

Mỗi milestone gồm:

* Milestone code.
* Name.
* Sequence.
* Due rule.
* Due date.
* Percentage.
* Fixed amount.
* Currency.
* Financial component.
* Payer.
* Receiver.
* Condition.
* Grace period.
* Penalty rule.
* Status.

---

# 37. Candidate Due Rule vocabulary — pending validation

> Exact due-rule types, source facts và date-resolution algorithms thuộc Contract contracts.

Có thể dựa trên:

```text
FIXED_DATE
DAYS_AFTER_SIGNING
DAYS_AFTER_EFFECTIVE
DAYS_AFTER_BOOKING
DAYS_AFTER_NOTICE
CONSTRUCTION_MILESTONE
HANDOVER_MILESTONE
DOCUMENT_MILESTONE
CUSTOM_EVENT
```

Mỗi lần resolve due date phải lưu:

* Rule.
* Source event.
* Resolved date.
* Rule version.
* Người xác nhận nếu thủ công.

---

# 38. Payment Plan Validation

Phải kiểm tra:

* Tổng amount.
* Tổng percentage.
* Currency.
* Deposit credit.
* Tax/fee.
* Final amount.
* Payer.
* Receiver.
* Due dates.
* Milestone order.
* Không âm.
* Rounding.
* Contract value reconciliation.

Sai lệch vượt tolerance phải chặn approval.

---

# 39. Deposit Conversion

Deposit từ Deal and Transaction Capability có thể được xử lý:

* Credit vào đợt 1.
* Credit vào giá mua.
* Giữ là khoản riêng.
* Hoàn lại.
* Chuyển thành phí.
* Chuyển sang Contract khác.

Phải có Deposit Conversion record:

* Source Deposit Commitment.
* Receipt/Payment Allocation.
* Target Contract.
* Target Receivable.
* Amount.
* Decision.
* Approval.

Không sửa Receipt gốc.

---

# 40. Receivable

## 40.1. Khái niệm

Receivable là nghĩa vụ phải thu được sinh ra khi Payment Milestone đạt điều kiện phát sinh.

## 40.2. Receivable không nhất thiết sinh toàn bộ ngay khi ký

Tùy policy:

* Sinh toàn bộ Payment Plan khi Contract effective.
* Sinh từng đợt theo milestone.
* Sinh khi phát hành Payment Notice.
* Sinh khi external notice nhận được.

## 40.3. Receivable phải có Source

* Payment Milestone.
* Amendment.
* Penalty.
* Fee.
* Adjustment.
* Refund recovery.
* Settlement correction.

---

# 41. Candidate Receivable lifecycle — pending validation

> Exact statuses/transitions thuộc Contract Context Pack.

```text
DRAFT
PENDING_ACTIVATION
OPEN
PARTIALLY_PAID
PAID
OVERDUE
DISPUTED
SUSPENDED
WAIVED
CANCELLED
ADJUSTED
WRITTEN_OFF
REFUND_CREDITED
```

---

# 42. Receivable Amounts

Mỗi Receivable phải tách:

* Original Amount.
* Adjustment Amount.
* Waived Amount.
* Paid Amount.
* Reversed Amount.
* Refunded Amount.
* Outstanding Amount.
* Overdue Amount.
* Penalty Amount.

Outstanding được tính, không nhập tay.

---

# 43. Receivable Party

Phải xác định:

* Debtor/Payer Party.
* Contract Buyer.
* Receiver Party.
* Internal Legal Entity.
* Financial nature.
* Payment responsibility.

Một Receivable có thể:

* Gắn một Payer cụ thể.
* Cho phép nhiều Payer thanh toán.
* Là joint obligation.

---

# 44. Payment Notice

Có thể phát hành thông báo thanh toán:

* Số tiền.
* Đợt.
* Hạn.
* Tài khoản nhận.
* Nội dung chuyển khoản.
* Contract.
* Customer.
* Penalty warning.
* QR/reference code.

Payment Notice không phải Receipt.

---

# 45. Công nợ

## 45.1. Công nợ hợp đồng

Tính từ Receivable:

```text
Outstanding
=
Original Amount
+ Approved Adjustments
+ Penalties
− Waivers
− Valid Allocations
− Credits
```

## 45.2. Không lưu công nợ bằng một trường nhập tay

Có thể lưu projection để tối ưu nhưng phải tái tính được.

## 45.3. Công nợ theo Party

Theo dõi:

* Contract.
* Buyer.
* Payer.
* Legal Entity.
* Project.
* Currency.
* Milestone.

---

# 46. Candidate Aging Bucket vocabulary — pending validation

> Exact buckets, timezone và Business Calendar semantics thuộc certified policy/Metric contracts.

```text
NOT_DUE
DUE_TODAY
1_7_DAYS_OVERDUE
8_30_DAYS_OVERDUE
31_60_DAYS_OVERDUE
61_90_DAYS_OVERDUE
OVER_90_DAYS
```

Business Calendar có thể được dùng để tính ngày làm việc nếu policy áp dụng.

---

# 47. Overdue

Khi quá hạn:

* Receivable chuyển Overdue.
* Contract Payment Status cập nhật.
* Tạo alert.
* Có thể sinh penalty theo rule.
* Không tự hủy Contract.
* Không tự phạt nếu cần approval.
* Không tự giải phóng Listing.

---

# 48. Penalty và Late Fee

Phải có:

* Penalty rule.
* Grace period.
* Base amount.
* Rate/fixed amount.
* Maximum.
* Effective date.
* Approval.
* Waiver process.

Penalty có thể được:

* Tính tự động.
* Chờ approval.
* Tạo Receivable riêng.

---

# 49. Waiver và giảm nghĩa vụ

Không sửa Original Amount.

Tạo:

* Waiver Request.
* Approved Waiver.
* Reason.
* Authority.
* Amount.
* Effective date.
* Impact.
* Audit.

---

# 50. Payment Transaction

## 50.1. Khái niệm

Payment Transaction đại diện cho một sự kiện tiền thực tế.

Nguồn:

* Bank transfer.
* Cash.
* Card.
* Payment gateway.
* Escrow.
* Bank disbursement.
* Internal transfer.
* Refund reversal.
* Other.

## 50.2. Payment Transaction representation không được tạo tùy tiện bởi Sale

Nguồn phải đến từ authorized Finance entry, approved cash process hoặc accepted Integration facts từ bank/payment provider. Raw transport, credentials và provider retries thuộc Integration Context.

---

# 51. Payment Transaction Fields

* Transaction ID.
* Source.
* External transaction reference.
* Bank account.
* Value date.
* Posting date.
* Amount.
* Currency.
* Sender name.
* Sender account masked.
* Receiver.
* Transfer content.
* Payment reference.
* Evidence.
* Reconciliation status.
* Identified Party.
* Identified Contract.
* Status.

---

# 52. Candidate Payment lifecycle dimensions — pending validation

> Exact verification, identification, allocation và reversal states thuộc Contract machine contracts.

```text
IMPORTED
PENDING_VERIFICATION
VERIFIED
UNIDENTIFIED
PARTIALLY_IDENTIFIED
ALLOCATED
PARTIALLY_ALLOCATED
FULLY_ALLOCATED
REVERSED
REFUNDED
REJECTED
DUPLICATE
DISPUTED
```

---

# 53. Duplicate Payment Detection

Dựa trên:

* External transaction ID.
* Bank account.
* Amount.
* Currency.
* Value date.
* Sender.
* Reference.
* Payload hash.

Không tự kết luận duplicate chỉ vì cùng amount/date nếu nguồn không đủ.

---

# 54. Unidentified Payment

Khi tiền vào nhưng chưa xác định:

* Lưu Payment Transaction.
* Status `UNIDENTIFIED`.
* Không phát hành Receipt chính thức cho Contract chưa xác định.
* Không tự allocate.
* Đưa vào queue.
* Có SLA xử lý.
* Có masked search và evidence.

---

# 55. Payment Matching

Hệ thống có thể gợi ý Contract/Receivable dựa trên:

* Payment reference.
* Contract code.
* Booking code.
* Customer phone.
* Payer account.
* Amount.
* Due date.
* Deposit instruction code.

Gợi ý không tự allocate khi confidence thấp.

---

# 56. Payment Allocation

## 56.1. Khái niệm

Allocation gắn Payment Transaction với Receivable hoặc financial purpose.

## 56.2. Một Allocation gồm

* Payment.
* Contract.
* Receivable.
* Booking/Deposit nếu có.
* Amount.
* Currency.
* Allocation purpose.
* Payer.
* Receiver.
* Allocated by.
* Approved by.
* Effective date.
* Status.

---

# 57. Allocation Rule

Có thể phân bổ theo:

* Customer instruction.
* Contract rule.
* Oldest due first.
* Specific milestone.
* Deposit conversion.
* Finance decision.
* Proportional distribution.

Rule phải lưu version và reason.

---

# 58. Partial Allocation

Payment lớn hơn hoặc nhỏ hơn Receivable đều được hỗ trợ.

Ví dụ:

* Payment 500 triệu.
* Receivable đợt 1: 300 triệu.
* Receivable đợt 2: 200 triệu.

Hoặc:

* Receivable 500 triệu.
* Payment A: 200 triệu.
* Payment B: 300 triệu.

---

# 59. Overpayment

Khi Payment vượt nghĩa vụ:

Phần thừa có thể:

* Để Credit Balance.
* Allocate cho đợt tiếp theo.
* Refund.
* Chuyển Contract khác.
* Giữ chờ chỉ dẫn.
* Offset fee khác.

Không tự coi là revenue.

---

# 60. Underpayment

Khi thiếu:

* Receivable giữ `PARTIALLY_PAID`.
* Outstanding được tính.
* Không phát hành trạng thái Fully Paid.
* Có thể phát hành Receipt cho phần thực nhận.
* SLA tiếp tục.

---

# 61. Payment Allocation Reversal

Không sửa Allocation đã approved.

Nếu sai:

1. Tạo Reversal Request.
2. Xác định Receipt impact.
3. Approval.
4. Reverse Allocation.
5. Recalculate Receivable.
6. Cancel/replace Receipt nếu cần.
7. Reallocate đúng.
8. Audit.

---

# 62. Receipt

## 62.1. Khái niệm

Receipt là chứng từ nghiệp vụ xác nhận doanh nghiệp hoặc bên được ủy quyền đã nhận một khoản tiền cụ thể.

## 62.2. Receipt có thể được tạo cho

* Contract payment.
* Deposit.
* Booking fee.
* Brokerage fee.
* Service fee.
* Refund recovery.
* Other approved purpose.

## 62.3. Receipt không phải Payment Transaction

Receipt dựa trên Payment đã xác minh hoặc quy trình thu tiền mặt hợp lệ.

---

# 63. Candidate Receipt lifecycle — pending validation

> Exact states/transitions và numbering issuance guards thuộc Contract Context Pack.

```text
DRAFT
PENDING_REVIEW
PENDING_APPROVAL
APPROVED
ISSUED
DELIVERED
CANCELLATION_REQUESTED
CANCELLED
REPLACED
VOID
ARCHIVED
```

---

# 64. Receipt Numbering

Số Receipt có thể theo:

* Legal Entity.
* Receipt type.
* Năm.
* Branch.
* Payment method.
* Sequence.

Receipt Number đã cấp không được tái sử dụng.

---

# 65. Receipt Party

Phải xác định:

* Payer.
* Buyer/Customer.
* Receiver Legal Entity/Party.
* Contract.
* Booking/Deposit.
* Payment transaction.
* Allocation.

Payer có thể khác Buyer.

---

# 66. Receipt Item

Một Receipt có thể có nhiều item:

* Principal.
* Deposit.
* Fee.
* Tax.
* Penalty.
* Service.
* Other.

Mỗi item có:

* Amount.
* Financial nature.
* Receivable.
* Contract component.
* Allocation.
* Description.

---

# 67. Điều kiện phát hành Receipt

1. Payment Transaction verified hoặc cash process hợp lệ.
2. Receiver đúng.
3. Amount đúng.
4. Currency đúng.
5. Payer xác định.
6. Contract/Booking/purpose xác định.
7. Allocation hợp lệ.
8. Không duplicate.
9. Maker–checker phù hợp.
10. Numbering thành công.

---

# 68. Receipt Correction

Không sửa Receipt issued.

Quy trình:

```text
Receipt sai
→ Cancellation Request
→ Finance Review
→ Approval
→ Receipt Cancelled
→ Allocation Reversal/Correction nếu cần
→ Replacement Receipt
```

Replacement Receipt phải lưu:

* Replaces Receipt ID.
* Cancelled Receipt ID.
* Reason.
* Approval.
* Corrected data.

---

# 69. Hủy Receipt

Chỉ cho phép khi:

* Sai Payer.
* Sai Contract.
* Sai amount.
* Sai purpose.
* Duplicate.
* Payment reversed.
* Refund.
* Legal requirement.
* Other approved reason.

Không được hủy để che giấu giao dịch.

---

# 70. Receipt delivery intent, Documents and Integration boundary

> Contract sở hữu delivery intent/business state; Documents sở hữu Receipt Document; Integration sở hữu channel transport.

Lưu:

* Recipient.
* Channel.
* Sent at.
* Delivered at.
* Downloaded/viewed.
* Document reference.
* Consent.
* Delivery status.

---

# 71. Cash Receipt

Nếu hỗ trợ tiền mặt:

Phải có:

* Cashier.
* Cash location.
* Cash session.
* Drawer/reference.
* Witness/checker nếu policy.
* Receipt.
* Deposit-to-bank reconciliation.
* Cash discrepancy.

Sale không được tự xác nhận tiền mặt nếu không có role.

---

# 72. Bank reconciliation business outcomes và Integration boundary

> Integration sở hữu bank transport/raw statements; Contract sở hữu transaction matching/allocation/reconciliation decisions.

Đối soát:

* Bank transaction.
* Payment Transaction.
* Allocation.
* Receipt.
* Contract.
* Receiver account.
* Amount.
* Date.
* Reference.

Kết quả:

```text
MATCHED
AMOUNT_MISMATCH
DATE_MISMATCH
REFERENCE_MISMATCH
DUPLICATE
UNIDENTIFIED
MISSING_BANK_ENTRY
MISSING_RECEIPT
REQUIRES_REVIEW
```

---

# 73. Payment Reversal

Khi ngân hàng reverse hoặc giao dịch bị chargeback:

* Payment status `REVERSED`.
* Allocation reversal.
* Receipt cancellation/replacement.
* Receivable mở lại.
* Deposit status cập nhật Deal and Transaction Capability.
* Contract payment status cập nhật.
* Revenue/Commission reversal trigger Revenue and Commission Capability.
* Audit.

---

# 74. Refund

## 74.1. Refund Decision

Contract and Cash Capability quản lý quyết định và xử lý tài chính refund.

Nguồn yêu cầu có thể từ:

* Booking cancellation.
* Contract cancellation.
* Overpayment.
* Payment error.
* Product change.
* Deposit refundable.
* Settlement correction.

## 74.2. Refund không được thực hiện chỉ vì Sale yêu cầu

Phải có:

* Refund basis.
* Amount.
* Recipient.
* Source payment.
* Contract/Booking.
* Fee/penalty deduction.
* Legal review nếu cần.
* Finance approval.
* Payment execution reference.

---

# 75. Candidate Refund lifecycle — pending validation

> Exact states, payment execution guards và provider confirmation semantics thuộc Contract contracts.

```text
DRAFT
PENDING_REVIEW
PENDING_APPROVAL
APPROVED
PAYMENT_PENDING
PARTIALLY_REFUNDED
REFUNDED
REJECTED
CANCELLED
FAILED
DISPUTED
```

---

# 76. Refund Calculation

Có thể gồm:

```text
Refundable Amount
=
Eligible Paid Amount
− Forfeiture
− Approved Penalties
− Non-refundable Fees
− Amount Already Transferred/Consumed
± Approved Adjustments
```

Phải hiển thị từng component.

---

# 77. Refund Payment

Lưu reference:

* Payment instruction.
* Bank transaction.
* Receiver account masked.
* Executed amount.
* Currency.
* Executed at.
* Finance user.
* Approval.
* Reconciliation.

---

# 78. Forfeiture

Khoản tiền bị giữ lại phải có:

* Legal/business basis.
* Contract clause.
* Amount.
* Approval.
* Financial nature.
* Revenue classification trigger.
* Customer notification.
* Dispute status.

Không tự coi toàn bộ Deposit là forfeited.

---

# 79. Payment Transfer giữa giao dịch

Khi chuyển tiền sang Contract/Booking khác:

* Source Payment không bị sửa.
* Source Allocation được reverse hoặc chuyển.
* Tạo Transfer record.
* Target Receivable.
* Amount.
* Approval.
* Payer consent.
* Finance review.
* Audit.

---

# 80. Credit Balance

Nếu Customer có số dư chưa phân bổ:

* Credit Balance.
* Contract/Customer context.
* Currency.
* Source Payment.
* Available amount.
* Restricted amount.
* Expiry nếu có.
* Allowed uses.
* Status.

Credit Balance không tự được dùng cho giao dịch mới.

---

# 81. Offset và Netting

Có thể dùng khi:

* Customer vừa phải trả vừa được hoàn.
* Owner settlement có khoản phải khấu trừ.
* Hai nghĩa vụ trong cùng giao dịch.
* Internal Legal Entity settlement.

Phải có:

* Offset agreement.
* Amount.
* Source obligations.
* Target obligations.
* Approval.
* Legal basis.
* Audit.

---

# 82. Settlement

## 82.1. Khái niệm

Settlement xác định số tiền ròng phải chuyển cho một bên sau khi:

* Đã nhận tiền.
* Xác định khoản thuộc bên đó.
* Khấu trừ phí.
* Khấu trừ hoàn tiền.
* Khấu trừ thuế/phí nếu có.
* Đối soát giao dịch.

## 82.2. Settlement không phải Revenue Recognition

Settlement là dòng tiền phải trả hoặc chuyển.

Revenue Context xác định Revenue của công ty riêng.

---

# 83. Owner Settlement

Trong giao dịch ký gửi/resale:

```text
Owner Net Payable
=
Gross Buyer Funds Eligible for Settlement
− Brokerage Fee
− Service Fee
− Owner-borne Tax/Fee
− Refund/Adjustment
− Other Approved Deductions
```

Phải tách rõ:

* Buyer purchase money.
* Brokerage fee.
* Company service fee.
* Owner proceeds.
* Amount already paid to Owner.
* Remaining payable.

---

# 84. Developer/Partner Settlement

Trong trường hợp công ty thu hộ:

* Gross funds collected.
* Amount owed to Developer/Partner.
* Company fee retained.
* Tax/fee.
* Refund reserve.
* Settlement payable.
* Paid.
* Remaining.

Nếu Buyer thanh toán trực tiếp Developer, Contract and Cash Capability chỉ lưu confirmation/reference, không tạo settlement giả.

---

# 85. Settlement Party

Có thể là:

* Owner Customer.
* Co-owner.
* Developer.
* Partner.
* Seller.
* Internal Legal Entity.
* Escrow.
* Other beneficiary.

Một Contract có thể có nhiều Settlement.

---

# 86. Candidate Settlement lifecycle — pending validation

> Exact states, approval and execution guards thuộc Contract Context Pack.

```text
DRAFT
PENDING_RECONCILIATION
PENDING_REVIEW
PENDING_APPROVAL
APPROVED
PAYMENT_PENDING
PARTIALLY_PAID
PAID
ON_HOLD
CANCELLED
ADJUSTED
DISPUTED
```

---

# 87. Settlement Statement

Phải hiển thị:

* Gross amount.
* Source payments.
* Contract.
* Period.
* Beneficiary.
* Deductions.
* Fees.
* Taxes/estimates.
* Refund reserve.
* Net payable.
* Paid amount.
* Remaining.
* Supporting documents.
* Approval.

---

# 88. Settlement Deduction

Các loại:

```text
BROKERAGE_FEE
SERVICE_FEE
TAX
LEGAL_FEE
NOTARY_FEE
REFUND_RESERVE
PENALTY
ADVANCE_RECOVERY
OTHER
```

Mỗi deduction phải có:

* Basis.
* Amount.
* Beneficiary.
* Approval.
* Revenue reference nếu là phí công ty.
* Revenue and Commission Capability linkage.

---

# 89. Settlement Payment

Contract and Cash Capability lưu:

* Payment instruction.
* Payee.
* Bank account reference.
* Amount.
* Currency.
* Approval.
* Executed payment reference.
* Executed date.
* Reconciliation status.

Không tự đánh dấu Paid khi chỉ tạo instruction.

---

# 90. Co-owner Settlement

Khi nhiều Owner:

* Settlement theo tỷ lệ.
* Hoặc theo thỏa thuận riêng.
* Tách người nhận.
* Tách bank account.
* Tách deductions nếu khác nhau.
* Kiểm tra tổng bằng Owner Net.

Không tự chia theo Ownership Percentage nếu hợp đồng quy định khác.

---

# 91. Contract Cancellation

## 91.1. Khái niệm

Cancellation áp dụng khi hợp đồng bị vô hiệu hóa hoặc hủy theo quy trình trước/hoặc sau hiệu lực tùy loại.

## 91.2. Cancellation không phải xóa Contract

Contract được giữ nguyên cùng trạng thái `CANCELLED`.

---

# 92. Contract Termination

Termination áp dụng khi:

* Hợp đồng đã có hiệu lực.
* Một bên chấm dứt.
* Các bên thỏa thuận chấm dứt.
* Vi phạm.
* Điều kiện pháp lý.

Termination có thể cần:

* Termination Agreement.
* Effective date.
* Financial settlement.
* Inventory decision.
* Revenue/commission reversal.

---

# 93. Contract Liquidation

Liquidation ghi nhận:

* Nghĩa vụ đã hoàn tất.
* Công nợ còn lại.
* Refund/settlement.
* Tài liệu bàn giao.
* Tranh chấp.
* Ngày kết thúc.

Không bắt buộc mọi Contract phải có Liquidation nếu business model không yêu cầu.

---

# 94. Cancellation Request

Phải có:

* Contract.
* Requester.
* Reason.
* Initiating Party.
* Requested effective date.
* Legal basis.
* Paid amount.
* Outstanding.
* Refund/forfeit proposal.
* Inventory impact.
* Settlement impact.
* Revenue impact.
* Commission impact.
* Approval route.
* Evidence.

---

# 95. Cancellation Impact Analysis

Trước approval phải phân tích:

* Contract status.
* Signed/effective.
* Listing/Asset.
* Active Receivables.
* Paid amounts.
* Receipts.
* Refund.
* Deposit.
* Settlement.
* Owner/Developer funds already transferred.
* Revenue recognized.
* Commission recognized/paid.
* Inventory release.
* External system impact.
* Tax/accounting impact reference.

---

# 96. Candidate inventory-impact decisions sau Contract change

> Đây là request/decision vocabulary của Contract; Product Context mới quyết định Product state.

Các kết quả:

```text
KEEP_BLOCKED
RELEASE_PENDING_REFUND
RELEASE_PENDING_LEGAL
RELEASE_PENDING_OWNER_CONFIRMATION
READY_TO_RELIST
NOT_ELIGIBLE_TO_RELIST
RECONCILIATION_REQUIRED
```

Contract Context gửi inventory-impact request/fact cho Product Context.

Product Context mới quyết định trạng thái Listing.

---

# 97. Contract Cancellation và Receivable

Khi hủy:

* Receivable chưa đến hạn có thể Cancel.
* Receivable đã paid không được xóa.
* Receivable overdue giữ lịch sử.
* Tạo Refund/Credit/Forfeit adjustment.
* Payment Allocations giữ lịch sử.
* Receipt giữ hoặc hủy theo bản chất.
* Reconciliation bắt buộc.

---

# 98. Contract Cancellation và Revenue/Commission

Contract Context phát governed cancellation facts với:

* Contract.
* Effective cancellation date.
* Contract value impact.
* Refund.
* Forfeit.
* Settlement.
* Reversal basis.

Revenue Context quyết định:

* Revenue reversal.
* Commission reversal.
* Clawback.
* Adjustment.

---

# 99. Product Change

## 99.1. Trước Contract ký

Xử lý chủ yếu tại Deal and Transaction Capability.

## 99.2. Sau Contract ký

Phải có:

* Contract Amendment hoặc Replacement.
* Old Asset.
* New Asset.
* Price difference.
* Payment credit.
* Refund/extra receivable.
* Inventory impact.
* Seller/Owner approval.
* Legal approval.
* Settlement impact.

Không sửa Asset ID trực tiếp trên Signed Contract.

---

# 100. Area Adjustment

Đặc biệt với đất hoặc sản phẩm theo diện tích thực tế:

* Contracted area.
* Final measured area.
* Price per m².
* Tolerance.
* Adjustment amount.
* New Receivable hoặc Refund.
* Amendment.
* Approval.
* Revenue impact.

---

# 101. Price Adjustment

Sau ký chỉ được thực hiện khi:

* Contract cho phép.
* Có Appendix/Amendment.
* Có authority.
* Có reason.
* Có Payment Plan Version mới.
* Receivable adjustment.
* Settlement adjustment.
* Revenue and Commission Capability event.

---

# 102. Party Change

Có thể gồm:

* Thêm Co-buyer.
* Xóa Co-buyer.
* Chuyển Buyer.
* Thay Representative.
* Thay Payer.
* Thay Seller.
* Chuyển nhượng quyền.

Sau ký phải có tài liệu pháp lý phù hợp.

Không sửa trực tiếp Contract Party record đang effective.

---

# 103. Contract Replacement

Dùng khi:

* Sai nghiêm trọng.
* Thay đổi cấu trúc lớn.
* External Developer cấp Contract mới.
* Chuyển Transaction Model.
* Contract cũ bị void.

Replacement phải:

* Link Contract cũ.
* Lưu reason.
* Xác định hiệu lực.
* Chuyển Payment Plan/Receivable có kiểm soát.
* Không nhân đôi công nợ.
* Reconciliation.
* Audit.

---

# 104. Correction Workflow

Dùng cho lỗi dữ liệu hoặc chứng từ:

* Contract correction.
* Receipt correction.
* Payment allocation correction.
* Party correction.
* Settlement correction.

Mỗi correction phải xác định:

* Lỗi gì.
* Dữ liệu đúng.
* Ảnh hưởng pháp lý.
* Ảnh hưởng tài chính.
* Ảnh hưởng báo cáo.
* Approval.
* Replacement records.

---

# 105. Reconciliation Case

> Status codes dưới đây là candidate vocabulary; exact workflow thuộc Contract Context Pack.

## 105.1. Khi nào tạo

* Contract value không khớp Payment Plan.
* Payment không khớp Receipt.
* Allocation vượt Payment.
* Receipt vượt Payment.
* Receivable âm.
* Booking Deposit không khớp Contract credit.
* Owner Settlement không khớp nguồn tiền.
* External Developer status mâu thuẫn.
* Refund không khớp cancellation.
* Contract cancelled nhưng Listing chưa xử lý.
* Revenue/Commission event thiếu.

## 105.2. Status

```text
NEW
UNDER_REVIEW
PENDING_INFORMATION
PENDING_FINANCE
PENDING_LEGAL
PENDING_EXTERNAL_CONFIRMATION
RESOLVED
ACCEPTED_DIFFERENCE
CANCELLED
```

---

# 106. Contract Completion

Contract Completion có thể cần:

* Fully signed.
* Effective.
* Payment complete.
* Handover complete.
* Documents complete.
* Settlement complete.
* No open refund.
* No critical reconciliation.
* No active dispute.
* Inventory status completed.

Không nên dùng một nút “Hoàn thành” bỏ qua checklist.

---

# 107. Handover và bàn giao tài sản

Contract and Cash Capability có thể quản lý:

* Handover notice.
* Handover appointment.
* Handover checklist.
* Handover minutes.
* Defect notes.
* Key/document delivery.
* Accepted/rejected.
* Handover date.

Quản lý vận hành hậu mãi chi tiết có thể thuộc capability mở rộng.

---

# 108. Contract Handover từ Deal and Transaction Capability

Khi Deal and Transaction Capability gửi Contract Handoff:

Contract Context phải nhận:

* Transaction Case.
* Booking.
* Deal.
* Customer.
* Parties.
* Listing/Asset.
* Commercial snapshot.
* Price/Policy version.
* Deposit.
* Receipt links.
* Co-sale snapshot.
* Approvals.
* Checklist.
* External references.

Contract Context phải validate lại tại trusted boundary, không tin payload frontend.

---

# 109. Candidate Contract Handoff lifecycle — pending validation

> Exact states, errors và retry/reconciliation behavior thuộc Contract machine contracts.

```text
NOT_RECEIVED
RECEIVED
VALIDATING
MISSING_INFORMATION
ACCEPTED
REJECTED
CONTRACT_CREATED
```

Nếu rejected:

* Trả reason.
* Không tự sửa Deal and Transaction Capability.
* Tạo Task/alert.

---

# 110. Dòng tiền theo Transaction Model

## 110.1. Buyer to Company

* Company/Internal Legal Entity là Receiver.
* Payment Transaction nằm trong Contract and Cash Capability.
* Receivable trực tiếp.
* Receipt do công ty phát hành.
* Revenue classification thuộc Revenue Context.

## 110.2. Buyer to Developer

* CRM có thể theo dõi external payment confirmation.
* Không tạo bank payment nội bộ nếu tiền không qua công ty.
* Có thể lưu External Receipt.
* Company Revenue là Distribution Commission riêng.

## 110.3. Buyer to Owner

* CRM theo dõi confirmation và evidence.
* Nếu công ty không nhận tiền, không phát hành Receipt nhận principal.
* Brokerage Fee Receivable có thể riêng.

## 110.4. Buyer to Escrow

* Payment Transaction liên kết Escrow.
* Settlement chỉ sau release.
* Không coi tiền escrow là cash available của công ty.

## 110.5. Buyer Split Payment

Một số tiền trả:

* Company.
* Developer.
* Owner.
* Tax/fee recipient.

Phải tách Receivable và Receiver.

## 110.6. Company Collects on Behalf

* Company nhận tiền.
* Receipt phải ghi bản chất thu hộ nếu cần.
* Settlement payable phát sinh.
* Không tự coi gross receipt là Revenue.

---

# 111. External Payment Confirmation qua Integration ACL

Khi tiền trả ngoài công ty:

Lưu:

* External payer.
* External receiver.
* Amount.
* Currency.
* Date.
* Reference.
* Evidence.
* External receipt.
* Verification.
* Source.
* Confidence.

Chỉ authorized Contract/Finance workflow mới xác minh; provider transport/evidence retrieval đi qua Integration ACL.

---

# 112. Brokerage Fee Receivable

Trong resale/ký gửi:

Brokerage Fee có thể do:

* Seller trả.
* Buyer trả.
* Hai bên chia.
* Khấu trừ từ Owner proceeds.
* Thanh toán riêng.

Phải là Receivable riêng, không trộn với Property Principal.

---

# 113. Service Fee Receivable

Tương tự Brokerage Fee nhưng có nature khác.

Revenue Context nhận governed facts để quyết định Revenue khi đủ điều kiện.

---

# 114. Payment Allocation Priority

Có thể cấu hình:

1. Tax/mandatory fee.
2. Penalty.
3. Oldest principal.
4. Current principal.
5. Service fee.
6. Future installment.

Hoặc theo Contract.

Mọi auto-allocation phải giải thích được và có thể review.

---

# 115. Currency and monetary precision principles

> Exact currency support, exchange-rate sources, precision và rounding thuộc accepted financial standards/configuration.

## 115.1. Contract Currency

Mỗi Contract có currency chính.

## 115.2. Multi-currency Payment

Nếu cho phép:

* Payment currency.
* Contract currency.
* Exchange rate.
* Rate source.
* Rate date.
* Converted amount.
* FX difference.

## 115.3. Không dùng floating point

Dùng Decimal và rounding policy.

---

# 116. Tax và Fee

Contract and Cash Capability lưu nghiệp vụ:

* Tax amount.
* Fee amount.
* Người chịu.
* Người thu.
* Dự kiến/chính thức.
* Payment status.
* Document reference.

Không thay hệ thống tính thuế pháp định nếu không tích hợp đầy đủ.

---

# 117. Contract Access

Quyền truy cập phải dựa trên:

* Contract participant context.
* Deal/Transaction Case.
* Legal Entity.
* Project.
* Finance assignment.
* Legal assignment.
* Share Grant.
* Scope.
* Field policy.

Project Access không tự cho xem:

* Identity document.
* Bank account.
* Receipt.
* Owner Settlement.
* Contract internal terms.

---

# 118. Field Masking

Các trường nhạy cảm:

* Identity document.
* Tax code cá nhân.
* Bank account.
* Payment sender account.
* Owner bank account.
* Floor Price.
* Internal deduction.
* Refund account.
* Signature evidence.
* Financial documents.

Có thể hiển thị:

* Full.
* Partial mask.
* Summary.
* Hidden.

---

# 119. Segregation of Duties

## 119.1. Maker

Tạo:

* Contract.
* Payment Plan.
* Receipt draft.
* Refund request.
* Settlement draft.

## 119.2. Checker

Kiểm tra:

* Party.
* Amount.
* Bank transaction.
* Allocation.
* Legal document.
* Settlement basis.

## 119.3. Approver

Duyệt:

* Contract.
* Receipt cancellation.
* Refund.
* Settlement.
* Waiver.
* Adjustment.

## 119.4. Không tự duyệt

User không được tự duyệt record mình tạo nếu policy yêu cầu SoD.

---

# 120. Quyền vai trò tham khảo

## 120.1. Sale

Được:

* Xem Contract summary của Deal mình.
* Theo dõi ký.
* Xem payment status summary.
* Gửi nhắc thanh toán được duyệt.
* Xem Receipt summary.

Không được:

* Tạo Payment Transaction.
* Xác nhận tiền.
* Duyệt Receipt.
* Hủy Receipt.
* Duyệt Refund.
* Duyệt Settlement.
* Xem toàn bộ bank details.
* Sửa Contract đã ký.

## 120.2. Transaction Coordinator

Được:

* Chuẩn bị Contract.
* Thu thập hồ sơ.
* Quản lý checklist.
* Theo dõi legal signing state từ accepted Documents/Integration facts.
* Handover.

## 120.3. Legal

Được:

* Review Contract.
* Review parties.
* Review amendment/cancellation.
* Review legal readiness.
* Quản lý legal documents.

## 120.4. Accounting

Được:

* Tạo/kiểm tra Payment.
* Phân bổ.
* Phát hành Receipt.
* Đối soát.
* Theo dõi công nợ.

## 120.5. Finance

Được:

* Review dòng tiền.
* Refund.
* Settlement.
* Receivable adjustment.
* Cash planning.

## 120.6. Director

Được:

* Approve ngoại lệ.
* Xem all theo quyền.
* Export có audit.
* Duyệt hủy/điều chỉnh lớn.

---

# 121. SLA policy inputs

> Các giá trị dưới đây là recommended baselines để validation, không phải hardcoded SLO/SLA contract.

Các SLA:

* Contract handoff validation.
* Contract draft preparation.
* Legal review.
* Finance review.
* Approval.
* Signature collection.
* Payment notice issuance.
* Payment allocation.
* Receipt issuance.
* Unidentified payment resolution.
* Overdue follow-up.
* Refund approval.
* Refund execution.
* Settlement approval.
* Settlement payment.
* Cancellation review.
* Reconciliation resolution.

Giá trị tham khảo:

| Nghiệp vụ                    |     SLA tham khảo |
| ---------------------------- | ----------------: |
| Validate Contract Handoff    |    4 giờ làm việc |
| Tạo Contract Draft           |   1 ngày làm việc |
| Legal Review                 |   1 ngày làm việc |
| Receipt sau payment verified |        Trong ngày |
| Unidentified Payment         |   1 ngày làm việc |
| Allocation Review            |    4 giờ làm việc |
| Refund Approval              | 1–3 ngày làm việc |
| Settlement Review            |   1 ngày làm việc |
| Critical Reconciliation      |             2 giờ |

SLA definitions phải được quản trị qua Platform Configuration và Business Calendar; operational SLA instances thuộc Activity/owning Context theo Context Pack.

---

# 122. Notification

## 122.1. Sale

* Contract Draft sẵn sàng.
* Thiếu hồ sơ Buyer.
* Contract chờ ký.
* Payment sắp đến hạn.
* Payment quá hạn.
* Receipt được phát hành.
* Contract amendment.
* Cancellation status.
* Contract completed.

## 122.2. Legal

* Contract chờ review.
* Party conflict.
* Ownership issue.
* Amendment.
* Cancellation.
* Dispute.
* External Contract cần xác minh.

## 122.3. Accounting

* Payment mới.
* Payment chưa xác định.
* Allocation pending.
* Receipt pending.
* Receipt cancellation.
* Receivable overdue.
* Bank mismatch.

## 122.4. Finance

* Refund.
* Settlement.
* Overpayment.
* Credit Balance.
* Payment transfer.
* High-value overdue.
* Cash shortfall.

## 122.5. Inventory

* Contract effective.
* Contract cancelled.
* Release pending.
* Product change.
* Reconciliation Required.

## 122.6. Director

* Contract giá trị lớn.
* High overdue.
* Refund lớn.
* Settlement lớn.
* Receipt cancellation bất thường.
* Cancellation high impact.

---

# 123. Candidate user experiences — không phải frontend contract canonical

> Exact routes, screens, components và responsive behavior thuộc Navigation/IA, Design System và Current Sprint Pack.

## 123.1. Contract List

Bộ lọc:

* Contract type.
* Status.
* Legal Entity.
* Project.
* Listing.
* Customer.
* Buyer.
* Seller.
* Sale.
* Signing status.
* Payment status.
* Overdue.
* Completion.
* Cancellation.
* External/internal.

## 123.2. Contract Workspace

Các tab:

1. Overview.
2. Parties.
3. Product.
4. Commercial Terms.
5. Documents.
6. Approval.
7. Signature.
8. Payment Plan.
9. Receivables.
10. Payments.
11. Receipts.
12. Refunds.
13. Settlement.
14. Amendments.
15. Cancellation.
16. Handover.
17. Reconciliation.
18. Timeline.
19. Audit.

## 123.3. Payment Plan Workspace

* Versions.
* Milestones.
* Due dates.
* Amount.
* Payer.
* Receiver.
* Status.
* Source event.
* Adjustments.

## 123.4. Receivable Center

* Open.
* Due.
* Overdue.
* Partially paid.
* Paid.
* Disputed.
* Waived.
* Adjusted.

## 123.5. Payment Inbox

* Bank transactions.
* Unidentified.
* Suggested matches.
* Duplicate warning.
* Allocation.
* Evidence.
* Reconciliation.

## 123.6. Receipt Center

* Draft.
* Pending approval.
* Issued.
* Delivered.
* Cancellation.
* Replacement.
* Numbering.

## 123.7. Refund Center

* Requests.
* Eligible amount.
* Deductions.
* Approval.
* Payment.
* Reconciliation.

## 123.8. Settlement Center

* Owner.
* Developer.
* Partner.
* Gross.
* Deductions.
* Net.
* Paid.
* Remaining.
* Supporting payments.

## 123.9. Reconciliation Center

* Contract mismatch.
* Payment mismatch.
* Receipt mismatch.
* Settlement mismatch.
* Inventory mismatch.
* External mismatch.
* SLA.

---

# 124. Analytics cho Sale

* Contract chờ hồ sơ.
* Contract chờ ký.
* Payment đến hạn.
* Payment quá hạn.
* Receipt mới.
* Contract amendment.
* Cancellation pending.
* Contract completed.

Sale chỉ thấy summary theo quyền.

---

# 125. Analytics cho Accounting

* Payment received today.
* Unidentified payments.
* Pending allocations.
* Receipt pending.
* Receipt cancellations.
* Due receivables.
* Overdue.
* Bank mismatches.
* Cash discrepancies.

---

# 126. Analytics cho Finance

* Cash collected.
* Refund payable.
* Settlement payable.
* Credit balances.
* Overpayments.
* Large overdue.
* Cash by Legal Entity.
* Funds collected on behalf.
* Funds available for settlement.

---

# 127. Analytics cho Legal

* Contract pending review.
* Missing identity.
* Missing ownership.
* Contract pending signature.
* Amendment.
* Cancellation.
* Dispute.
* Contract expiration/termination.

---

# 128. Analytics cho Director

* Contract value.
* Signed value.
* Effective value.
* Cash collected.
* Outstanding receivable.
* Overdue.
* Refund.
* Settlement.
* Cancellation rate.
* Contract cycle time.
* Legal Entity comparison.
* Project comparison.
* Transaction Model comparison.

---

# 129. Candidate analytical questions — không phải certified hoặc statutory reports

> Exact grain, formulas, snapshots, certification và access thuộc Analytics Context; statutory reporting thuộc accounting/ERP khi áp dụng.

* Contract master.
* Contract by type.
* Contract by status.
* Contract by Project.
* Contract by Listing.
* Contract by Legal Entity.
* Contract by Buyer/Seller.
* Multi-buyer Contract.
* Contract value.
* Contract signed/effective.
* Contract amendment.
* Contract cancellation.
* Contract termination.
* Payment Plan.
* Receivable.
* Receivable aging.
* Due today.
* Overdue.
* Payment Transaction.
* Payment source.
* Unidentified Payment.
* Payment Allocation.
* Partial Payment.
* Overpayment.
* Credit Balance.
* Receipt.
* Receipt cancellation.
* Receipt replacement.
* Refund.
* Refund aging.
* Settlement.
* Owner Settlement.
* Developer/Partner Settlement.
* Funds collected on behalf.
* Brokerage Fee Receivable.
* Service Fee Receivable.
* Deposit conversion.
* Product change.
* Party change.
* Area adjustment.
* Reconciliation.
* Contract completion.
* Handover.
* Bank mismatch.
* Cash reconciliation.

Operational views phải drill-down đúng scope và field policy. Certified Metrics thuộc Analytics Context; statutory reports thuộc accounting/ERP khi áp dụng.

---

# 130. Candidate data model — không phải physical schema canonical

> **Classification:** `CONTEXT-SPECIFIC DESIGN INPUT / PENDING VALIDATION`
> Exact tables, columns, constraints, indexes và references chỉ có hiệu lực khi được khóa trong Contract Context DB Specification và Alembic migrations. Cross-context references không mặc định tạo cross-schema business foreign keys.

## 130.1. Contract Group

### `contract_groups`

* `id`
* `contract_group_code`
* `enterprise_id`
* `legal_entity_id`
* `transaction_case_id`
* `deal_id`
* `booking_id`
* `customer_id`
* `listing_id`
* `asset_id`
* `transaction_model`
* `status`
* `created_by`
* `created_at`
* `updated_at`

---

## 130.2. Contract

### `contracts`

* `id`
* `contract_code`
* `contract_number`
* `external_contract_number`
* `contract_group_id`
* `contract_type`
* `enterprise_id`
* `legal_entity_id`
* `transaction_case_id`
* `deal_id`
* `booking_id`
* `customer_id`
* `listing_id`
* `asset_id`
* `project_id`
* `transaction_model`
* `seller_party_id`
* `primary_buyer_party_id`
* `payment_receiver_party_id`
* `currency`
* `gross_contract_value`
* `net_property_value`
* `amount_payable`
* `workflow_status`
* `legal_status`
* `payment_status`
* `receivable_status`
* `document_status`
* `completion_status`
* `current_version`
* `signed_at`
* `effective_at`
* `completed_at`
* `terminated_at`
* `cancelled_at`
* `source_type`
* `source_id`
* `created_by`
* `created_at`
* `updated_at`
* `version`

### `contract_status_history`

* `id`
* `contract_id`
* `status_group`
* `from_status`
* `to_status`
* `reason`
* `source_type`
* `source_id`
* `changed_by`
* `created_at`

---

## 130.3. Contract Version

### `contract_versions`

* `id`
* `contract_id`
* `version`
* `template_id`
* `template_version`
* `party_snapshot_json`
* `product_snapshot_json`
* `commercial_snapshot_json`
* `legal_terms_snapshot_json`
* `payment_plan_version_id`
* `document_hash`
* `valid_from`
* `valid_to`
* `status`
* `change_reason`
* `created_by`
* `reviewed_by`
* `approved_by`
* `created_at`

---

## 130.4. Contract Party

### `contract_parties`

* `id`
* `contract_id`
* `contract_version_id`
* `party_id`
* `customer_id`
* `party_role`
* `identity_snapshot_json`
* `ownership_percentage`
* `payment_obligation_percentage`
* `joint_obligation`
* `signing_required`
* `representative_party_id`
* `verification_status`
* `effective_from`
* `effective_to`
* `status`
* `created_at`

### `contract_party_contribution_summaries`

* `id`
* `contract_id`
* `party_id`
* `allocated_payment_amount`
* `refunded_amount`
* `net_contribution_amount`
* `contribution_percentage`
* `calculated_at`

Đây là projection từ Payment Allocation.

---

## 130.5. Contract Financial Components

### `contract_financial_components`

* `id`
* `contract_version_id`
* `component_code`
* `financial_nature`
* `payer_party_id`
* `receiver_party_id`
* `amount`
* `currency`
* `is_revenue_candidate`
* `is_collected_on_behalf`
* `is_refundable`
* `is_discountable`
* `tax_treatment_reference`
* `source_type`
* `source_id`
* `created_at`

---

## 130.6. Documents và Signatures

### `contract_document_references`

* `id`
* `contract_id`
* `contract_version_id`
* `document_type`
* `title`
* `document_version_id`
* `document_id`
* `document_hash`
* `language_code`
* `is_signed_document`
* `signature_status`
* `access_policy_id`
* `effective_from`
* `superseded_at`
* `created_by`
* `created_at`

### `contract_signature_requirements`

* `id`
* `contract_version_id`
* `party_id`
* `signer_role`
* `signing_order`
* `required`
* `status`
* `created_at`

### `contract_signature_records`

* `id`
* `contract_version_id`
* `party_id`
* `signer_role`
* `signature_method`
* `external_signature_id`
* `signed_at`
* `document_hash`
* `certificate_metadata_json`
* `evidence_document_id`
* `status`
* `created_at`

---

## 130.7. Amendment

### `contract_amendments`

* `id`
* `amendment_code`
* `contract_id`
* `amendment_type`
* `current_version`
* `before_snapshot_json`
* `after_snapshot_json`
* `financial_impact_json`
* `inventory_impact_json`
* `revenue_impact_json`
* `commission_impact_json`
* `status`
* `effective_at`
* `created_by`
* `reviewed_by`
* `approved_by`
* `created_at`

### `contract_amendment_document_references`

* `id`
* `contract_amendment_id`
* `document_id`
* `document_hash`
* `signature_status`
* `created_at`

---

## 130.8. Payment Plan

### `payment_plans`

* `id`
* `payment_plan_code`
* `contract_id`
* `current_version`
* `currency`
* `status`
* `created_at`
* `updated_at`

### `payment_plan_versions`

* `id`
* `payment_plan_id`
* `version`
* `contract_version_id`
* `total_amount`
* `deposit_credit_amount`
* `rounding_adjustment`
* `effective_from`
* `effective_to`
* `change_reason`
* `status`
* `created_by`
* `reviewed_by`
* `approved_by`
* `created_at`

### `payment_milestones`

* `id`
* `payment_plan_version_id`
* `milestone_code`
* `sequence_number`
* `name`
* `due_rule_type`
* `due_rule_json`
* `resolved_due_date`
* `percentage`
* `fixed_amount`
* `currency`
* `financial_component_code`
* `payer_party_id`
* `receiver_party_id`
* `grace_period_days`
* `penalty_rule_id`
* `activation_condition_json`
* `status`
* `created_at`

---

## 130.9. Deposit Conversion

### `deposit_conversions`

* `id`
* `source_deposit_commitment_id`
* `source_payment_allocation_id`
* `target_contract_id`
* `target_receivable_id`
* `conversion_type`
* `amount`
* `currency`
* `status`
* `approved_by`
* `created_at`

---

## 130.10. Receivable

### `receivables`

* `id`
* `receivable_code`
* `contract_id`
* `payment_milestone_id`
* `source_type`
* `source_id`
* `debtor_party_id`
* `receiver_party_id`
* `financial_nature`
* `currency`
* `original_amount`
* `adjustment_amount`
* `waived_amount`
* `paid_amount`
* `reversed_amount`
* `refunded_amount`
* `outstanding_amount`
* `penalty_amount`
* `due_date`
* `grace_until`
* `status`
* `aging_bucket`
* `activated_at`
* `paid_at`
* `created_at`
* `updated_at`
* `version`

### `receivable_adjustments`

* `id`
* `receivable_id`
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

### `receivable_status_history`

* `id`
* `receivable_id`
* `from_status`
* `to_status`
* `reason`
* `source_type`
* `source_id`
* `created_by`
* `created_at`

---

## 130.11. Payment Notice

### `payment_notices`

* `id`
* `notice_code`
* `contract_id`
* `receivable_id`
* `payer_party_id`
* `amount`
* `currency`
* `due_date`
* `receiver_account_reference`
* `payment_reference_code`
* `document_id`
* `status`
* `issued_by`
* `issued_at`
* `delivered_at`
* `created_at`

---

## 130.12. Payment Transaction

### `payment_transactions`

* `id`
* `payment_transaction_code`
* `legal_entity_id`
* `source_type`
* `external_transaction_id`
* `bank_account_reference`
* `value_date`
* `posting_date`
* `amount`
* `currency`
* `sender_name`
* `sender_account_masked`
* `receiver_party_id`
* `transfer_content`
* `payment_reference`
* `payload_hash`
* `verification_status`
* `identification_status`
* `allocation_status`
* `reconciliation_status`
* `status`
* `evidence_document_id`
* `created_by`
* `verified_by`
* `created_at`
* `updated_at`

### `payment_transaction_candidates`

* `id`
* `payment_transaction_id`
* `candidate_type`
* `candidate_id`
* `confidence_score`
* `match_reasons_json`
* `status`
* `created_at`

---

## 130.13. Payment Allocation

### `payment_allocations`

* `id`
* `allocation_code`
* `payment_transaction_id`
* `contract_id`
* `receivable_id`
* `booking_id`
* `deposit_commitment_id`
* `payer_party_id`
* `receiver_party_id`
* `allocation_purpose`
* `amount`
* `currency`
* `allocation_rule_code`
* `status`
* `allocated_by`
* `reviewed_by`
* `approved_by`
* `effective_at`
* `created_at`
* `version`

### `payment_allocation_reversals`

* `id`
* `payment_allocation_id`
* `reason`
* `reversal_amount`
* `status`
* `requested_by`
* `reviewed_by`
* `approved_by`
* `effective_at`
* `created_at`

---

## 130.14. Receipt

### `receipts`

* `id`
* `receipt_code`
* `receipt_number`
* `legal_entity_id`
* `receipt_type`
* `contract_id`
* `booking_id`
* `deposit_commitment_id`
* `payer_party_id`
* `customer_id`
* `receiver_party_id`
* `payment_transaction_id`
* `currency`
* `total_amount`
* `status`
* `issued_at`
* `delivered_at`
* `replaces_receipt_id`
* `cancelled_receipt_id`
* `created_by`
* `reviewed_by`
* `approved_by`
* `created_at`
* `updated_at`

### `receipt_items`

* `id`
* `receipt_id`
* `payment_allocation_id`
* `receivable_id`
* `financial_component_code`
* `description`
* `amount`
* `currency`
* `created_at`

### `receipt_cancellation_requests`

* `id`
* `receipt_id`
* `reason_code`
* `reason`
* `replacement_required`
* `allocation_impact_json`
* `status`
* `requested_by`
* `reviewed_by`
* `approved_by`
* `created_at`
* `resolved_at`

### `receipt_document_references`

* `id`
* `receipt_id`
* `document_id`
* `document_hash`
* `document_status`
* `created_at`

---

## 130.15. Credit Balance

### `customer_credit_balances`

* `id`
* `customer_id`
* `party_id`
* `legal_entity_id`
* `contract_id`
* `currency`
* `original_amount`
* `available_amount`
* `restricted_amount`
* `source_payment_transaction_id`
* `allowed_use_policy`
* `status`
* `created_at`
* `updated_at`

---

## 130.16. Refund

### `refund_requests`

* `id`
* `refund_code`
* `contract_id`
* `booking_id`
* `deposit_commitment_id`
* `customer_id`
* `recipient_party_id`
* `source_payment_transaction_id`
* `source_receipt_id`
* `currency`
* `eligible_amount`
* `forfeiture_amount`
* `deduction_amount`
* `requested_amount`
* `approved_amount`
* `reason_code`
* `calculation_snapshot_json`
* `status`
* `requested_by`
* `finance_reviewed_by`
* `legal_reviewed_by`
* `approved_by`
* `created_at`
* `resolved_at`

### `refund_payments`

* `id`
* `refund_request_id`
* `payment_instruction_reference`
* `external_payment_id`
* `amount`
* `currency`
* `executed_at`
* `reconciliation_status`
* `status`
* `executed_by`
* `created_at`

---

## 130.17. Payment Transfer và Offset

### `payment_transfer_requests`

* `id`
* `source_contract_id`
* `source_payment_allocation_id`
* `target_contract_id`
* `target_receivable_id`
* `amount`
* `currency`
* `reason`
* `customer_consent_reference`
* `status`
* `requested_by`
* `reviewed_by`
* `approved_by`
* `created_at`

### `financial_offsets`

* `id`
* `contract_id`
* `offset_code`
* `source_obligation_type`
* `source_obligation_id`
* `target_obligation_type`
* `target_obligation_id`
* `amount`
* `currency`
* `basis_reference`
* `status`
* `approved_by`
* `created_at`

---

## 130.18. Settlement

### `transaction_settlements`

* `id`
* `settlement_code`
* `contract_id`
* `transaction_case_id`
* `beneficiary_party_id`
* `settlement_type`
* `currency`
* `gross_eligible_amount`
* `total_deductions`
* `net_payable_amount`
* `paid_amount`
* `remaining_amount`
* `status`
* `period_from`
* `period_to`
* `created_by`
* `reviewed_by`
* `approved_by`
* `created_at`
* `updated_at`

### `transaction_settlement_sources`

* `id`
* `settlement_id`
* `payment_transaction_id`
* `payment_allocation_id`
* `eligible_amount`
* `created_at`

### `transaction_settlement_deductions`

* `id`
* `settlement_id`
* `deduction_type`
* `amount`
* `currency`
* `basis_reference`
* `revenue_entitlement_reference`
* `description`
* `created_at`

### `transaction_settlement_payments`

* `id`
* `settlement_id`
* `payment_instruction_reference`
* `external_payment_id`
* `amount`
* `currency`
* `executed_at`
* `reconciliation_status`
* `status`
* `executed_by`
* `created_at`

### `transaction_settlement_parties`

* `id`
* `settlement_id`
* `party_id`
* `settlement_role`
* `allocation_percentage`
* `allocated_amount`
* `bank_account_reference`
* `status`
* `created_at`

---

## 130.19. Contract Cancellation

### `contract_cancellation_requests`

* `id`
* `cancellation_code`
* `contract_id`
* `initiating_party_id`
* `reason_code`
* `reason`
* `requested_effective_at`
* `legal_basis_reference`
* `paid_amount_snapshot`
* `outstanding_amount_snapshot`
* `refund_proposal_json`
* `forfeiture_proposal_json`
* `inventory_impact_json`
* `settlement_impact_json`
* `revenue_impact_json`
* `commission_impact_json`
* `status`
* `requested_by`
* `finance_reviewed_by`
* `legal_reviewed_by`
* `inventory_reviewed_by`
* `approved_by`
* `created_at`
* `resolved_at`

### `contract_termination_events`

* `id`
* `contract_id`
* `cancellation_request_id`
* `termination_type`
* `effective_at`
* `termination_document_id`
* `inventory_decision`
* `created_at`

---

## 130.20. Product/Party Change

### `contract_product_change_requests`

* `id`
* `contract_id`
* `old_asset_id`
* `old_listing_id`
* `new_asset_id`
* `new_listing_id`
* `price_difference`
* `payment_credit_amount`
* `new_receivable_amount`
* `refund_amount`
* `inventory_impact_json`
* `status`
* `requested_by`
* `reviewed_by`
* `approved_by`
* `created_at`

### `contract_party_change_requests`

* `id`
* `contract_id`
* `change_type`
* `old_party_snapshot_json`
* `new_party_snapshot_json`
* `payment_impact_json`
* `ownership_impact_json`
* `legal_document_reference`
* `status`
* `requested_by`
* `reviewed_by`
* `approved_by`
* `created_at`

---

## 130.21. Reconciliation

### `transaction_reconciliation_cases`

* `id`
* `case_code`
* `contract_id`
* `payment_transaction_id`
* `receipt_id`
* `settlement_id`
* `reconciliation_type`
* `risk_level`
* `expected_snapshot_json`
* `actual_snapshot_json`
* `difference_json`
* `status`
* `assigned_user_id`
* `due_at`
* `resolution_code`
* `resolution_notes`
* `created_at`
* `resolved_at`

---

## 130.22. Handover và Completion

### `contract_handover_intakes`

* `id`
* `transaction_case_id`
* `booking_id`
* `handover_payload_version`
* `handover_snapshot_json`
* `validation_result_json`
* `status`
* `received_at`
* `validated_by`
* `created_contract_id`
* `created_at`

### `contract_completion_checklists`

* `id`
* `contract_id`
* `checklist_code`
* `required`
* `status`
* `evidence_reference`
* `assigned_user_id`
* `completed_by`
* `completed_at`
* `created_at`

---

# 131. Candidate application operations — không phải OpenAPI canonical

> Các operations dưới đây là capability inventory. Exact paths, methods, payloads, errors, idempotency và authorization metadata thuộc OpenAPI.

## Contract Handoff

```text
POST   /contract-handoffs
GET    /contract-handoffs/{id}
POST   /contract-handoffs/{id}/validate
POST   /contract-handoffs/{id}/accept
POST   /contract-handoffs/{id}/reject
POST   /contract-handoffs/{id}/create-contract
```

## Contract

```text
GET    /contracts
POST   /contracts
GET    /contracts/{id}
PATCH  /contracts/{id}
POST   /contracts/{id}/versions
GET    /contract-versions/{id}
POST   /contract-versions/{id}/validate
POST   /contract-versions/{id}/submit-review
POST   /contract-versions/{id}/approve
POST   /contract-versions/{id}/prepare-signing
POST   /contract-versions/{id}/send-for-signature
POST   /contracts/{id}/mark-effective
POST   /contracts/{id}/complete
POST   /contracts/{id}/archive
GET    /contracts/{id}/history
GET    /contracts/{id}/access-explanation
```

## Contract Parties

```text
GET    /contracts/{id}/parties
POST   /contracts/{id}/parties
PATCH  /contract-parties/{id}
POST   /contract-parties/{id}/verify
POST   /contract-parties/{id}/end
```

Các API update chỉ áp dụng Draft/Version hợp lệ.

## Documents và Signature

```text
GET    /contracts/{id}/documents
POST   /contracts/{id}/documents
GET    /contract-documents/{id}

GET    /contract-versions/{id}/signature-requirements
POST   /contract-versions/{id}/signature-records
POST   /contract-signature-records/{id}/verify
POST   /contract-versions/{id}/refresh-signature-status
```

## Amendment

```text
GET    /contracts/{id}/amendments
POST   /contracts/{id}/amendments
GET    /contract-amendments/{id}
POST   /contract-amendments/{id}/analyze-impact
POST   /contract-amendments/{id}/submit-review
POST   /contract-amendments/{id}/approve
POST   /contract-amendments/{id}/prepare-signing
POST   /contract-amendments/{id}/activate
```

## Payment Plan

```text
GET    /contracts/{id}/payment-plans
POST   /contracts/{id}/payment-plans
GET    /payment-plans/{id}
POST   /payment-plans/{id}/versions
GET    /payment-plan-versions/{id}
POST   /payment-plan-versions/{id}/validate
POST   /payment-plan-versions/{id}/approve
POST   /payment-plan-versions/{id}/activate
POST   /payment-plan-versions/{id}/generate-receivables
```

## Receivables

```text
GET    /receivables
GET    /receivables/{id}
POST   /receivables/{id}/activate
POST   /receivables/{id}/adjustment-requests
POST   /receivables/{id}/waiver-requests
POST   /receivables/{id}/suspend
POST   /receivables/{id}/recalculate
GET    /contracts/{id}/receivables
GET    /customers/{id}/receivables
```

## Payment Notices

```text
POST   /receivables/{id}/payment-notices
GET    /payment-notices/{id}
POST   /payment-notices/{id}/issue
POST   /payment-notices/{id}/send
POST   /payment-notices/{id}/cancel
```

## Payments

```text
GET    /payment-transactions
POST   /payment-transactions
GET    /payment-transactions/{id}
POST   /payment-transactions/{id}/verify
POST   /payment-transactions/{id}/identify
POST   /payment-transactions/{id}/mark-duplicate
POST   /payment-transactions/{id}/mark-reversed
GET    /payment-transactions/{id}/candidates
POST   /payment-transactions/{id}/refresh-candidates
```

## Allocation

```text
GET    /payment-allocations
POST   /payment-allocations
GET    /payment-allocations/{id}
POST   /payment-allocations/{id}/submit-review
POST   /payment-allocations/{id}/approve
POST   /payment-allocations/{id}/reversal-requests
POST   /payment-allocation-reversals/{id}/approve
```

## Receipts

```text
GET    /receipts
POST   /receipts
GET    /receipts/{id}
POST   /receipts/{id}/validate
POST   /receipts/{id}/submit-review
POST   /receipts/{id}/approve
POST   /receipts/{id}/issue
POST   /receipts/{id}/deliver
POST   /receipts/{id}/cancellation-requests
POST   /receipt-cancellation-requests/{id}/approve
POST   /receipts/{id}/create-replacement
GET    /receipts/{id}/history
```

## Refund

```text
GET    /refund-requests
POST   /refund-requests
GET    /refund-requests/{id}
POST   /refund-requests/{id}/calculate
POST   /refund-requests/{id}/submit-review
POST   /refund-requests/{id}/approve
POST   /refund-requests/{id}/reject
POST   /refund-requests/{id}/create-payment-instruction
POST   /refund-requests/{id}/confirm-payment
```

## Payment Transfer/Credit

```text
GET    /customer-credit-balances
GET    /customer-credit-balances/{id}

POST   /payment-transfer-requests
GET    /payment-transfer-requests/{id}
POST   /payment-transfer-requests/{id}/review
POST   /payment-transfer-requests/{id}/approve
POST   /payment-transfer-requests/{id}/execute

POST   /financial-offsets
POST   /financial-offsets/{id}/approve
```

## Settlement

```text
GET    /transaction-settlements
POST   /transaction-settlements
GET    /transaction-settlements/{id}
POST   /transaction-settlements/{id}/calculate
POST   /transaction-settlements/{id}/reconcile
POST   /transaction-settlements/{id}/submit-review
POST   /transaction-settlements/{id}/approve
POST   /transaction-settlements/{id}/create-payment-instruction
POST   /transaction-settlements/{id}/confirm-payment
POST   /transaction-settlements/{id}/adjust
```

## Cancellation/Termination

```text
GET    /contract-cancellation-requests
POST   /contracts/{id}/cancellation-requests
GET    /contract-cancellation-requests/{id}
POST   /contract-cancellation-requests/{id}/analyze-impact
POST   /contract-cancellation-requests/{id}/submit-review
POST   /contract-cancellation-requests/{id}/approve
POST   /contract-cancellation-requests/{id}/reject
POST   /contract-cancellation-requests/{id}/execute
POST   /contracts/{id}/liquidation
```

## Product/Party Change

```text
POST   /contracts/{id}/product-change-requests
GET    /contract-product-change-requests/{id}
POST   /contract-product-change-requests/{id}/analyze
POST   /contract-product-change-requests/{id}/approve
POST   /contract-product-change-requests/{id}/execute

POST   /contracts/{id}/party-change-requests
GET    /contract-party-change-requests/{id}
POST   /contract-party-change-requests/{id}/analyze
POST   /contract-party-change-requests/{id}/approve
POST   /contract-party-change-requests/{id}/execute
```

## Reconciliation

```text
GET    /transaction-reconciliation-cases
POST   /transaction-reconciliation-cases
GET    /transaction-reconciliation-cases/{id}
POST   /transaction-reconciliation-cases/{id}/assign
POST   /transaction-reconciliation-cases/{id}/resolve
POST   /transaction-reconciliation-cases/{id}/accept-difference
POST   /transaction-reconciliation-cases/{id}/recheck
```

Backend phải tự enforce:

* Authenticated user.
* Legal Entity.
* Contract access context.
* Project/Listing scope.
* Permission.
* Field masking.
* Workflow.
* Approval.
* Maker–checker–approver.
* Idempotency.
* Optimistic locking.
* Contract version.
* Payment/Receipt status.
* Financial tolerance.
* Business Calendar.
* Audit.

---

# 132. Candidate permission vocabulary — không phải Permission Registry canonical

> Exact permission codes, scopes, role mappings, SoD, concealment và field masking thuộc security registries/matrices.

## Contract

```text
contract.view
contract.view_summary
contract.view_sensitive
contract.create
contract.update_draft
contract.create_version
contract.validate
contract.submit_review
contract.legal_review
contract.finance_review
contract.approve
contract.prepare_signing
contract.send_signing
contract.mark_effective
contract.complete
contract.archive
contract.view_audit
contract.export
```

## Contract Party

```text
contract_party.view
contract_party.view_identity
contract_party.add
contract_party.update_draft
contract_party.verify
contract_party.change_request
contract_party.view_contribution
```

## Documents và Signature

```text
contract_document.view
contract_document.view_sensitive
contract_document.create
contract_document.generate
contract_document.archive
contract_signature.view
contract_signature.manage
contract_signature.verify
```

## Amendment

```text
contract_amendment.view
contract_amendment.create
contract_amendment.analyze
contract_amendment.review
contract_amendment.approve
contract_amendment.activate
```

## Payment Plan và Receivable

```text
payment_plan.view
payment_plan.create
payment_plan.create_version
payment_plan.validate
payment_plan.review
payment_plan.approve
payment_plan.activate

receivable.view
receivable.view_detail
receivable.activate
receivable.adjust_request
receivable.adjust_review
receivable.adjust_approve
receivable.waive_request
receivable.waive_approve
receivable.suspend
receivable.recalculate
receivable.export
```

## Payment

```text
payment_transaction.view
payment_transaction.view_sensitive
payment_transaction.create_manual
payment_transaction.import
payment_transaction.verify
payment_transaction.identify
payment_transaction.mark_duplicate
payment_transaction.reverse
payment_transaction.view_audit

payment_allocation.view
payment_allocation.create
payment_allocation.review
payment_allocation.approve
payment_allocation.reverse_request
payment_allocation.reverse_approve
```

## Receipt

```text
receipt.view
receipt.view_sensitive
receipt.create
receipt.review
receipt.approve
receipt.issue
receipt.deliver
receipt.cancel_request
receipt.cancel_review
receipt.cancel_approve
receipt.create_replacement
receipt.view_audit
receipt.export
```

## Refund

```text
refund.view
refund.create
refund.calculate
refund.review
refund.legal_review
refund.approve
refund.reject
refund.create_payment_instruction
refund.confirm_payment
refund.view_audit
```

## Settlement

```text
settlement.view
settlement.view_sensitive
settlement.create
settlement.calculate
settlement.reconcile
settlement.review
settlement.approve
settlement.create_payment_instruction
settlement.confirm_payment
settlement.adjust
settlement.export
```

## Cancellation và Adjustment

```text
contract_cancellation.view
contract_cancellation.request
contract_cancellation.analyze
contract_cancellation.finance_review
contract_cancellation.legal_review
contract_cancellation.inventory_review
contract_cancellation.approve
contract_cancellation.execute

contract_product_change.request
contract_product_change.review
contract_product_change.approve
contract_product_change.execute

contract_party_change.request
contract_party_change.review
contract_party_change.approve
contract_party_change.execute
```

## Reconciliation

```text
transaction_reconciliation.view
transaction_reconciliation.create
transaction_reconciliation.assign
transaction_reconciliation.resolve
transaction_reconciliation.accept_difference
transaction_reconciliation.recheck
```

Các quyền kết hợp với:

```text
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

# 133. Candidate business facts — không phải Event contracts canonical

> Exact Event names, versions, payloads, channels và consumers thuộc JSON Schema, AsyncAPI và Event Registry.

Contract and Cash Capability phát:

```text
contract_handoff.received
contract_handoff.accepted
contract_handoff.rejected

contract.created
contract.version_created
contract.submitted_review
contract.approved
contract.sent_for_signature
contract.partially_signed
contract.fully_signed
contract.effective
contract.payment_completed
contract.completed
contract.suspended
contract.disputed
contract.cancel_requested
contract.cancelled
contract.terminated
contract.liquidated
contract.replaced

contract.amendment_created
contract.amendment_approved
contract.amendment_effective
contract.party_changed
contract.product_changed
contract.price_adjusted
contract.area_adjusted

payment_plan.created
payment_plan.version_created
payment_plan.activated
payment_milestone.due_resolved

receivable.created
receivable.activated
receivable.partially_paid
receivable.paid
receivable.overdue
receivable.adjusted
receivable.waived
receivable.cancelled
receivable.reopened

payment_transaction.received
payment_transaction.verified
payment_transaction.unidentified
payment_transaction.identified
payment_transaction.reversed
payment_transaction.refunded

payment_allocation.created
payment_allocation.approved
payment_allocation.reversed

receipt.created
receipt.approved
receipt.issued
receipt.delivered
receipt.cancel_requested
receipt.cancelled
receipt.replaced

deposit.converted_to_contract_payment
deposit.payment_confirmed
deposit.payment_reversed

refund.requested
refund.approved
refund.payment_initiated
refund.partially_paid
refund.paid
refund.failed

customer_credit.created
customer_credit.used
customer_credit.refunded

settlement.created
settlement.calculated
settlement.approved
settlement.partially_paid
settlement.paid
settlement.adjusted

contract.inventory_release_requested
contract.inventory_relist_ready
contract.revenue_adjustment_required
contract.commission_adjustment_required

transaction_reconciliation.created
transaction_reconciliation.resolved
```

Consumer phải idempotent.

---

# 134. Candidate Platform configuration references

> Exact configuration keys, schemas, scopes và resolution strategies thuộc Platform Context contracts.

```text
contract.default_workflow
contract.workflow_by_type
contract.numbering_scheme
contract.template_resolution_policy
contract.required_party_policy
contract.party_verification_policy
contract.signing_policy
contract.effectiveness_policy
contract.completion_policy
contract.document_policy
contract.retention_policy

contract_amendment.workflow
contract_amendment.approval_policy
contract_cancellation.workflow
contract_cancellation.approval_policy
contract_liquidation.policy
contract_product_change.policy
contract_party_change.policy

payment_plan.default_policy
payment_plan.validation_policy
payment_plan.rounding_policy
payment_plan.receivable_generation_policy
payment_milestone.due_resolution_policy

receivable.activation_policy
receivable.aging_policy
receivable.penalty_policy
receivable.waiver_policy
receivable.adjustment_policy

payment_transaction.import_policy
payment_transaction.verification_policy
payment_transaction.duplicate_policy
payment_transaction.identification_policy
payment_matching.rule_set

payment_allocation.policy
payment_allocation.auto_allocation_policy
payment_allocation.reversal_policy

receipt.workflow
receipt.numbering_scheme
receipt.approval_policy
receipt.cancellation_policy
receipt.replacement_policy
receipt.delivery_policy

refund.workflow
refund.calculation_policy
refund.approval_policy
refund.payment_policy
forfeiture.approval_policy

settlement.workflow
settlement.calculation_policy
settlement.deduction_policy
settlement.approval_policy
settlement.payment_policy

bank_reconciliation.policy
transaction_reconciliation.policy

contract.sla_policy
contract.notification_policy
contract.export_approval_policy
contract.field_access_policy
```

Mỗi configuration definition phải công bố schema, allowed scopes, resolution strategy, owner, version, effective period, approval và Audit requirements khi phù hợp.

---

# 135. System invariant

Các quy tắc sau không được cấu hình tắt:

1. Contract đã ký không được sửa trực tiếp.
2. Contract Version đã ký phải bất biến.
3. Receipt đã issued không được sửa trực tiếp.
4. Receipt sai phải hủy và thay thế.
5. Payment Transaction và Receipt là hai thực thể khác nhau.
6. Receivable phải có nguồn nghiệp vụ hợp lệ.
7. Outstanding Amount phải được tính.
8. Payment Allocation phải có Payment và purpose.
9. Allocation không được vượt Available Payment Amount.
10. Valid Allocation không được vượt Receivable Outstanding trừ Credit/Advance policy.
11. Một Payment có thể phân bổ nhiều Receivable.
12. Một Receivable có thể nhận nhiều Payment.
13. Deposit Confirmed phải dựa trên Payment/Allocation hợp lệ.
14. Payment reversed phải mở lại nghĩa vụ liên quan.
15. Receipt cancellation không được xóa lịch sử.
16. Contract cancellation không được xóa Contract.
17. Contract cancellation không tự mở lại Listing.
18. Settlement không đồng nghĩa Revenue.
19. Gross funds collected không mặc định là Revenue.
20. Collected-on-behalf funds phải được tách.
21. Contract Parties phải snapshot identity tại thời điểm ký.
22. Customer profile update không thay Signed Contract.
23. Party change sau ký phải có Amendment/Replacement.
24. Product change sau ký không được sửa Asset ID trực tiếp.
25. Payment Plan active không được sửa trực tiếp.
26. Payment Plan thay đổi phải tạo version.
27. Refund phải có approved basis.
28. Refund payment không được xác nhận từ frontend.
29. Settlement Paid phải có payment execution reference.
30. Sale không được xác nhận tiền.
31. User không được tự duyệt record mình tạo khi SoD áp dụng.
32. Backend phải enforce Legal Entity và field scope.
33. Contract Value, Payment Plan và Receivable phải reconcile.
34. Audit tài chính và hợp đồng không được sửa.
35. Revenue and Commission Capability mới quyết định Revenue và Commission.

---

# 136. Rule nghiệp vụ bắt buộc

1. Contract phải gắn Transaction Case hoặc nguồn hợp lệ.
2. Contract phải có Transaction Model.
3. Contract phải có Seller.
4. Contract phải có Buyer tối thiểu khi loại hợp đồng yêu cầu.
5. Contract có thể có nhiều Buyer.
6. Contract có thể có nhiều Seller.
7. Contract có thể có nhiều Payer.
8. Buyer, Payer và Signer phải tách biệt.
9. Ownership Percentage phải tách Payment Obligation.
10. Actual Contribution phải tính từ Allocation.
11. Contract Party phải dùng canonical Party.
12. Merged Customer source không được tạo Contract mới.
13. Contract phải snapshot identity.
14. Contract phải snapshot Asset/Listing.
15. Contract phải snapshot Price/Policy.
16. Contract phải snapshot Booking/Proposal/Offer source.
17. Contract Number không được tái sử dụng.
18. External Contract phải giữ external reference.
19. Contract Draft có thể sửa qua version.
20. Contract Approved for Signing phải khóa nội dung.
21. Signed Version không được sửa.
22. Amendment không ghi đè Contract gốc.
23. Appendix phải có effective date.
24. Contract Replacement phải link Contract cũ.
25. Contract Effective phải qua Effectiveness Rule.
26. Fully Signed không mặc định Effective nếu có điều kiện.
27. Contract Completion không chỉ dựa Fully Paid.
28. Contract cancellation không xóa Payment lịch sử.
29. Contract cancellation không xóa Receipt.
30. Contract cancellation phải phân tích Refund.
31. Contract cancellation phải phân tích Settlement.
32. Contract cancellation phải phân tích Inventory.
33. Contract cancellation phải phát Revenue/Commission impact event.
34. Listing không tự Available sau cancellation.
35. Product change sau ký phải có Amendment/Replacement.
36. Party change sau ký phải có Amendment/Replacement.
37. Price change sau ký phải có approved document.
38. Area adjustment phải có calculation.
39. Payment Plan phải có currency.
40. Payment Plan phải reconcile Contract Value.
41. Payment Milestone phải có payer/receiver hoặc rule xác định.
42. Due date phải được resolve có nguồn.
43. Payment Plan active không sửa trực tiếp.
44. Receivable phải sinh từ Milestone/Adjustment hợp lệ.
45. User không tự tạo receivable không có source.
46. Receivable Amount không được âm.
47. Outstanding được tính.
48. Aging được tính từ due date.
49. Overdue không tự hủy Contract.
50. Penalty cần rule.
51. Penalty có thể cần approval.
52. Waiver không sửa Original Amount.
53. Payment phải có external/internal source.
54. Sale không tạo verified Payment.
55. Payment duplicate phải được phát hiện.
56. Unidentified Payment không tự allocate.
57. Payment candidate chỉ là gợi ý.
58. Payment Allocation cần amount/currency.
59. Allocation không vượt Payment Available.
60. Allocation phải xác định purpose.
61. Allocation approved không sửa trực tiếp.
62. Allocation sai phải reverse.
63. Reversal phải cập nhật Receivable.
64. Reversal phải cập nhật Receipt.
65. Overpayment không tự là Revenue.
66. Overpayment phải tạo Credit/Refund/Advance.
67. Underpayment không được coi Paid.
68. Payment Receiver phải đúng Transaction Model.
69. Receipt chỉ phát hành cho Payment hợp lệ.
70. Receipt Number unique.
71. Receipt issued không sửa.
72. Receipt sai phải cancellation.
73. Replacement Receipt phải link phiếu cũ.
74. Receipt cancellation cần approval.
75. Receipt cancellation không được che giao dịch.
76. Cash receipt cần cashier process.
77. Bank reconciliation phải có status.
78. Payment reversal mở lại Receivable.
79. Payment reversal cập nhật Deposit Deal and Transaction Capability.
80. Refund cần source payment.
81. Refund cần eligible amount.
82. Refund phải tách forfeiture/deductions.
83. Refund approval và payment là hai bước.
84. Refund Paid cần external payment reference.
85. Forfeiture cần legal/business basis.
86. Payment Transfer không sửa source Payment.
87. Payment Transfer cần consent/approval.
88. Credit Balance không tự dùng.
89. Offset cần basis.
90. Settlement chỉ dùng tiền đủ điều kiện.
91. Settlement phải xác định beneficiary.
92. Settlement phải tách gross/deductions/net.
93. Owner Settlement không mặc định theo Ownership Percentage.
94. Settlement Paid phải có payment proof.
95. Settlement adjustment không sửa record Paid trực tiếp.
96. Gross Buyer Funds không mặc định Revenue.
97. Buyer-to-Developer payment không tạo internal receipt giả.
98. Buyer-to-Owner payment cần external confirmation nếu không qua công ty.
99. Company Collects on Behalf phải tạo settlement liability.
100. Brokerage Fee phải là component riêng.
101. Service Fee phải là component riêng.
102. Tax/Fee collected on behalf phải tách.
103. Multi-Legal Entity phải dùng đúng Receiver.
104. Cross-entity payment cần authority.
105. Project Access không tự mở Receipt.
106. Deal Access không tự mở bank details.
107. Sale chỉ xem payment summary.
108. Accounting/Finance view theo scope.
109. View không đồng nghĩa Export.
110. Export cần audit.
111. Field masking phải backend enforce.
112. User inactive không được approve.
113. Delegation phải kiểm tra authority.
114. Maker không tự Approver khi SoD áp dụng.
115. Handover không làm mất Contract history.
116. Handover không thay Party.
117. Customer merge không thay Contract snapshot.
118. External payment confirmation cần evidence.
119. Contract duplicate phải được cảnh báo.
120. Deposit conversion không sửa Receipt.
121. Deposit conversion phải link target Receivable.
122. Partial deposit không tự Effective nếu policy yêu cầu đủ.
123. Receipt reversal phải gửi event Deal and Transaction Capability.
124. Contract effective phải gửi event Product, Asset, Listing and Inventory Capability/8/10.
125. Contract cancellation phải gửi adjustment event.
126. Reconciliation Case không tự đóng khi chưa xử lý nguồn.
127. Accepted Difference cần authority.
128. Contract archive không xóa.
129. Payment/Receipt/Settlement audit không xóa.
130. Capability không thay thế hệ thống kế toán pháp định.

---

# 137. Cảnh báo và phát hiện bất thường

Hệ thống cần cảnh báo khi:

* Contract không có Transaction Case.
* Contract không có Seller.
* Contract không có Buyer.
* Contract Party dùng merged Customer.
* Ownership percentage không bằng 100%.
* Payment obligation mâu thuẫn.
* Contract Value không khớp Payment Plan.
* Payment Plan percentage không bằng 100%.
* Deposit Credit vượt Deposit Confirmed.
* Contract Fully Signed nhưng document hash không khớp.
* Contract Effective thiếu điều kiện.
* Contract đang Performing nhưng Listing chưa Contracted.
* Contract Cancelled nhưng Listing tự Available.
* Signed Contract bị update trực tiếp.
* Amendment không có impact analysis.
* Payment Milestone không có due date.
* Receivable không có source.
* Receivable outstanding âm.
* Receivable paid vượt original + adjustment.
* Payment duplicate.
* Payment không có receiver.
* Payment amount bằng 0 hoặc âm.
* Unidentified Payment quá SLA.
* Payment Allocation vượt available amount.
* Allocation vượt Receivable trái rule.
* Payment Fully Allocated nhưng còn available amount.
* Receivable Paid nhưng Allocation bị reversed.
* Receipt issued không có Payment.
* Receipt amount không khớp Allocation.
* Receipt duplicate.
* Receipt cancelled nhưng replacement required chưa tạo.
* Payment reversed nhưng Receipt còn active.
* Refund approved vượt eligible amount.
* Refund Paid không có payment reference.
* Refund kéo dài quá SLA.
* Credit Balance âm.
* Settlement Net không bằng Gross trừ Deductions.
* Settlement Paid vượt Net Payable.
* Settlement không có source payment.
* Owner Settlement sai tổng co-owner.
* Collected-on-behalf funds không có settlement liability.
* Brokerage Fee bị trộn vào property principal.
* External payment marked confirmed không có evidence.
* Contract cancellation thiếu refund analysis.
* Cancellation thiếu inventory decision.
* Product change không có new lock/inventory reference.
* Party change không identity check.
* Contract completed còn Receivable open.
* Contract completed còn Refund pending.
* Contract completed còn Settlement open.
* Contract archived còn dispute.
* User tạo và tự duyệt Receipt.
* Sale truy cập bank details.
* Bulk receipt cancellation.
* Receipt sequence gap bất thường.
* Payment import duplicate rate cao.
* Same idempotency key khác payload.
* External Contract Number trùng.
* Reconciliation Case quá SLA.
* Revenue and Commission Capability không nhận Revenue/Commission impact event.

---

# 138. Audit requirements và evidence

> Audit Context sở hữu immutable Audit facts. Contract Context phát sinh audit-worthy facts/references; operational logs không thay Audit.

## 138.1. Thao tác bắt buộc

* Contract handoff.
* Contract create/update draft/version.
* Party add/change.
* Product snapshot.
* Commercial snapshot.
* Contract review/approval.
* Document generation.
* Signature.
* Contract effective.
* Contract completion.
* Amendment.
* Cancellation/termination/liquidation.
* Payment Plan create/version.
* Receivable create/adjust/waive.
* Payment import/create/verify.
* Payment identification.
* Payment allocation/reversal.
* Receipt create/approve/issue/cancel/replace.
* Refund create/calculate/approve/pay.
* Credit Balance use.
* Payment transfer.
* Offset.
* Settlement create/calculate/approve/pay.
* Product change.
* Party change.
* Reconciliation.
* Sensitive view.
* Export.

## 138.2. Nội dung

* Actor.
* Role.
* Legal Entity.
* Customer.
* Contract.
* Contract Version.
* Transaction Case.
* Booking.
* Asset/Listing.
* Payment.
* Allocation.
* Receipt.
* Refund.
* Settlement.
* Before.
* After.
* Reason.
* Source.
* Approval.
* Workflow version.
* Template version.
* IP.
* Device.
* Request ID.
* Correlation ID.
* Idempotency key.
* Timestamp.
* Result.

---

# 139. Phạm vi MVP

## 139.1. Bắt buộc

* Contract Handoff.
* Contract Group.
* Contract.
* Contract Version.
* Contract types chính.
* Contract Parties.
* Multiple buyers.
* Multiple sellers.
* Buyer/Payer separation.
* Ownership/payment obligation percentages.
* Product snapshot.
* Commercial snapshot.
* Contract document URL.
* Contract approval.
* Manual signature tracking.
* Contract effectiveness.
* Payment Plan.
* Payment Plan Version.
* Milestones.
* Receivable generation.
* Receivable status.
* Aging.
* Payment Notice.
* Payment Transaction manual/import.
* Payment verification.
* Unidentified Payment.
* Payment matching suggestion.
* Payment Allocation.
* Partial Payment.
* Overpayment/Credit Balance.
* Deposit Conversion.
* Receipt.
* Receipt approval.
* Receipt issuance.
* Receipt cancellation.
* Replacement Receipt.
* Refund Request.
* Refund approval/payment reference.
* Settlement.
* Owner Settlement.
* Collected-on-behalf handling.
* Contract Amendment.
* Contract Cancellation.
* Inventory Release Request.
* Product Change.
* Party Change.
* Reconciliation.
* Scope.
* Field masking.
* Maker–checker–approver.
* Audit.
* Analytics.
* Domain events.

## 139.2. Giai đoạn nâng cao

* E-signature integration.
* Digital signature certificate validation.
* Automated bank reconciliation.
* Payment gateway integration.
* Real-time bank webhook.
* Cash drawer management.
* Multi-currency.
* FX accounting reference.
* Escrow integration.
* Automated penalty.
* Advanced collection workflow.
* Customer payment portal.
* Owner settlement portal.
* Developer reconciliation portal.
* Notary integration.
* External legal registry.
* Automated contract generation with clause rules.
* OCR/extraction for external contract.
* Advanced tax integration.
* ERP/General Ledger integration.
* Automated handover management.
* Contract renewal.
* Lease management.
* Installment restructuring.
* Chargeback handling.

---

# 140. Tiêu chí nghiệm thu

Capability được xem là đạt khi:

1. Nhận được Contract Handoff từ Deal and Transaction Capability.
2. Validate Handoff được.
3. Reject Handoff có reason.
4. Tạo Contract từ Handoff được.
5. Contract giữ Transaction Case.
6. Contract giữ Booking.
7. Contract giữ Deal.
8. Contract giữ Listing/Asset.
9. Contract có Transaction Model.
10. Contract có Legal Entity.
11. Contract có Seller.
12. Contract có Buyer.
13. Contract có Contract Code.
14. Contract Number unique.
15. External Contract Number được lưu.
16. Tạo được Contract Group.
17. Group chứa nhiều document/contract.
18. Tạo được nhiều Contract Type.
19. Contract có workflow status.
20. Contract có legal status.
21. Contract có payment status.
22. Contract có receivable status.
23. Contract có document status.
24. Contract có completion status.
25. Stage gate hoạt động.
26. Contract Draft được sửa qua version.
27. Approved Version được khóa.
28. Signed Version không sửa được.
29. Customer update không sửa snapshot Contract.
30. Tạo được nhiều Buyer.
31. Tạo được nhiều Seller.
32. Tạo được Payer riêng.
33. Tạo được Representative.
34. Tạo được Guarantor.
35. Ownership Percentage được lưu.
36. Payment Obligation Percentage được lưu.
37. Actual Contribution được tính từ Allocation.
38. Ownership total được validate.
39. Identity Snapshot được lưu.
40. Product Snapshot được lưu.
41. Listing Version được lưu.
42. Price Version được lưu.
43. Policy Version được lưu.
44. Mandate snapshot được lưu.
45. Commercial components được lưu.
46. Tách Principal và Fee.
47. Tách Collected on Behalf.
48. Tách Brokerage Fee.
49. Tách Owner Proceeds.
50. Tạo được Contract Document.
51. Lưu document hash.
52. Tạo Signature Requirement.
53. Ghi Signature Record.
54. Theo dõi partial signature.
55. Chuyển Fully Signed đúng.
56. Effectiveness Rule hoạt động.
57. Fully Signed không tự Effective trái rule.
58. Tạo được Contract Amendment.
59. Amendment có before/after.
60. Amendment có financial impact.
61. Amendment không sửa Contract gốc.
62. Tạo được Contract Appendix.
63. Appendix có effective date.
64. Tạo được Contract Replacement.
65. Replacement link Contract cũ.
66. Tạo Payment Plan.
67. Payment Plan có version.
68. Payment Plan có currency.
69. Tạo nhiều Milestone.
70. Milestone có due rule.
71. Resolve due date được.
72. Payment Plan reconcile Contract Value.
73. Sai tổng bị chặn.
74. Tạo Deposit Conversion.
75. Deposit Conversion link Payment Allocation.
76. Deposit Conversion link Receivable.
77. Tạo Receivable từ Milestone.
78. Receivable có source.
79. Receivable có debtor.
80. Receivable có receiver.
81. Receivable có original amount.
82. Outstanding tự tính.
83. Paid amount tự tính.
84. Aging bucket hoạt động.
85. Overdue hoạt động.
86. Overdue không tự hủy Contract.
87. Tạo Penalty được.
88. Tạo Waiver Request được.
89. Waiver không sửa Original Amount.
90. Tạo Payment Notice.
91. Payment Notice có account/reference.
92. Payment Notice không phải Receipt.
93. Tạo Payment Transaction.
94. Import Payment được.
95. Verify Payment được.
96. Duplicate Payment được phát hiện.
97. Unidentified Payment được lưu.
98. Suggested match hoạt động.
99. Gợi ý thấp không auto allocate.
100. Tạo Payment Allocation.
101. Một Payment phân bổ nhiều Receivable.
102. Một Receivable nhận nhiều Payment.
103. Partial allocation hoạt động.
104. Allocation không vượt Payment.
105. Allocation approved không sửa.
106. Tạo Allocation Reversal.
107. Reversal mở lại Receivable.
108. Overpayment tạo Credit Balance.
109. Underpayment giữ Partially Paid.
110. Tạo Receipt Draft.
111. Receipt có Legal Entity.
112. Receipt có Payer.
113. Receipt có Receiver.
114. Receipt có Payment Transaction.
115. Receipt có Allocation.
116. Receipt có nhiều item.
117. Receipt Number unique.
118. Receipt approval hoạt động.
119. Receipt issued không sửa.
120. Receipt delivery được lưu.
121. Tạo Receipt Cancellation Request.
122. Sale không tự hủy Receipt.
123. Cancellation có approval.
124. Receipt cũ giữ lịch sử.
125. Tạo Replacement Receipt.
126. Replacement link Receipt cũ.
127. Payment reversed cập nhật Receipt.
128. Payment reversed cập nhật Receivable.
129. Payment reversed cập nhật Deposit Deal and Transaction Capability.
130. Tạo Refund Request.
131. Refund calculate được.
132. Refund tách forfeiture.
133. Refund tách deduction.
134. Refund không vượt eligible amount.
135. Refund approval hoạt động.
136. Refund payment reference được lưu.
137. Refund Paid không dựa frontend.
138. Tạo Payment Transfer.
139. Transfer không sửa source Payment.
140. Transfer cần target Receivable.
141. Tạo Credit Balance.
142. Credit không tự dùng.
143. Tạo Offset.
144. Offset có basis.
145. Tạo Owner Settlement.
146. Settlement có beneficiary.
147. Settlement có source payment.
148. Settlement có gross.
149. Settlement có deductions.
150. Settlement có net.
151. Net được tính đúng.
152. Settlement hỗ trợ nhiều co-owner.
153. Co-owner allocation tổng đúng.
154. Settlement approval hoạt động.
155. Settlement Paid có payment reference.
156. Collected-on-behalf tạo Settlement liability.
157. Buyer-to-Developer external payment được lưu.
158. Không tạo internal Receipt giả cho external payment.
159. Buyer-to-Owner external confirmation được lưu.
160. Tạo Contract Cancellation Request.
161. Cancellation có reason.
162. Cancellation có impact analysis.
163. Cancellation tính paid/outstanding.
164. Cancellation tính refund/forfeit.
165. Cancellation có inventory decision.
166. Cancellation có revenue/commission impact.
167. Cancellation không xóa Contract.
168. Cancellation không tự mở Listing.
169. Gửi inventory release request cho Product, Asset, Listing and Inventory Capability.
170. Tạo Termination Event.
171. Tạo Liquidation record/checklist.
172. Tạo Product Change Request.
173. Product Change không sửa Asset ID trực tiếp.
174. Product Change tính price difference.
175. Product Change xử lý payment credit.
176. Tạo Party Change Request.
177. Party mới identity check.
178. Party Change không sửa Signed Version.
179. Tạo Area Adjustment.
180. Area Adjustment tính chênh lệch.
181. Tạo Reconciliation Case.
182. Contract value mismatch được phát hiện.
183. Payment/Receipt mismatch được phát hiện.
184. Settlement mismatch được phát hiện.
185. Reconciliation có SLA.
186. Accepted Difference cần quyền.
187. Contract Completion có checklist.
188. Contract không complete khi còn Receivable open.
189. Contract không complete khi còn Refund pending.
190. Contract không complete khi còn Settlement open.
191. Công ty tự phát triển được hỗ trợ.
192. Pháp nhân dự án nội bộ được hỗ trợ.
193. Phân phối Developer ngoài được hỗ trợ.
194. Tài sản công ty sở hữu được hỗ trợ.
195. Customer ký gửi được hỗ trợ.
196. Partner-owned resale được hỗ trợ.
197. Đất nền dự án được hỗ trợ.
198. Đất riêng lẻ được hỗ trợ.
199. Buyer-to-Company được hỗ trợ.
200. Buyer-to-Developer được hỗ trợ.
201. Buyer-to-Owner được hỗ trợ.
202. Buyer-to-Escrow được hỗ trợ.
203. Split Payment được hỗ trợ.
204. Company Collects on Behalf được hỗ trợ.
205. Sale chỉ xem summary đúng scope.
206. Accounting xem payment/receipt đúng scope.
207. Finance xem refund/settlement đúng scope.
208. Legal xem Contract đúng scope.
209. Director xem all theo quyền.
210. Backend enforce Legal Entity.
211. Backend enforce field masking.
212. Sửa URL không mở rộng quyền.
213. View không cho Export.
214. Export có audit.
215. Maker không tự Approver trái policy.
216. User inactive không approve được.
217. Audit lưu before/after.
218. Audit lưu Contract Version.
219. Audit lưu Payment/Allocation.
220. Audit lưu Receipt cancellation.
221. Audit lưu Refund.
222. Audit lưu Settlement.
223. Idempotency hoạt động.
224. Same key khác payload báo conflict.
225. Domain events được phát.
226. Event consumer idempotent.
227. Deal and Transaction Capability nhận Deposit Confirmed event.
228. Product, Asset, Listing and Inventory Capability nhận Contract/Inventory event.
229. Revenue and Commission Capability nhận Revenue/Commission trigger.
230. Capability quản lý đầy đủ hợp đồng và dòng tiền giao dịch mà không biến CRM thành hệ thống kế toán pháp định.

---

# 141. Quan hệ canonical với các Context liên quan

## 141.1. Party Context

Contract sử dụng canonical Party/Customer references và lưu immutable identity snapshots cho Contract versions.

Customer profile hoặc merge redirect không được sửa nội dung Contract đã ký. Giao dịch mới phải resolve canonical Party hiện hành.

## 141.2. Product Context

Contract sử dụng Asset, Listing, Ownership, Selling Right và Product snapshots.

Contract chỉ phát inventory-impact facts/requests. Product Context quyết định Availability, Contracted/Sold/Released và relist eligibility.

## 141.3. Matching Context

Contract có thể giữ Match/Shortlist references cho lineage.

Matching Result không phải bằng chứng Price/Policy/Availability hiện hành.

## 141.4. Transaction Context

Contract nhận versioned handoff, Booking, parties, commercial snapshot và Deposit Commitment references.

Contract trả handoff result và governed Payment/Receipt facts. Contract không sửa Booking history hoặc Transaction aggregates.

## 141.5. Revenue Context

Contract cung cấp:

- Effective/cancelled Contract facts.
- Contract financial components.
- Valid Payment/Allocation/Receipt facts.
- Brokerage/service-fee components.
- Refund/forfeiture/settlement/adjustment facts.

Revenue Context quyết định Revenue Entitlement, Recognition, Commission, payout và clawback.

## 141.6. Documents, Integration và Audit Contexts

- Documents sở hữu File/Document/Version/signature evidence.
- Integration sở hữu bank/provider/ERP/signature transport runtime.
- Audit sở hữu immutable Audit facts.
- Contract giữ governed references và local process state.

---

# 142. Anti-patterns và canonical requirements

## AP-CON-001 — Một `payment_status` và `paid_amount` thay toàn bộ dòng tiền

**Không được áp dụng**

Dùng vài fields trên Contract để đại diện Payment Plan, Receivable, Payment, Allocation, Receipt và Refund.

**Canonical requirement**

Mỗi lớp phải có record, lifecycle, source, reconciliation và Audit riêng; summary chỉ là rebuildable projection.

## AP-CON-002 — Buyer, Payer, Signer và Owner là cùng một người

**Không được áp dụng**

Tự suy luận các roles từ primary Customer.

**Canonical requirement**

Mỗi Party role phải được khai báo, xác minh và snapshot riêng; ownership, obligation và contribution là các dimensions độc lập.

## AP-CON-003 — Sửa Contract đã ký

**Không được áp dụng**

PATCH nội dung Signed Contract hoặc Signed Version.

**Canonical requirement**

Thay đổi sau ký phải dùng Amendment, Appendix, Correction, Replacement, Termination hoặc approved legal process; signed version giữ bất biến.

## AP-CON-004 — Sửa Receipt đã phát hành

**Không được áp dụng**

Ghi đè payer, amount, purpose hoặc Contract trên issued Receipt.

**Canonical requirement**

Sai sót phải qua cancellation/reversal-impact review và replacement Receipt có liên kết đầy đủ.

## AP-CON-005 — Payment đồng nghĩa Receipt

**Không được áp dụng**

Có bank transaction thì tự tạo issued Receipt, hoặc có Receipt draft thì coi tiền đã nhận.

**Canonical requirement**

Payment verification, Allocation và Receipt issuance là các bước riêng với guards và SoD.

## AP-CON-006 — Receivable nhập tay không có nguồn

**Không được áp dụng**

User tạo công nợ tùy ý để điều chỉnh số dư.

**Canonical requirement**

Receivable phải phát sinh từ Payment Milestone, Amendment, penalty/fee decision, refund recovery, settlement correction hoặc approved adjustment.

## AP-CON-007 — Outstanding nhập tay

**Không được áp dụng**

Lưu outstanding như một số có thể sửa độc lập.

**Canonical requirement**

Outstanding phải được tính từ original amount, adjustments, waivers, valid allocations, reversals, refunds và credits; projection phải tái tạo được.

## AP-CON-008 — Hủy Contract tự mở lại Listing

**Không được áp dụng**

Contract cancellation trực tiếp chuyển Listing sang Available.

**Canonical requirement**

Contract phát inventory-impact request/fact; Product Context đánh giá legal, lock, refund, dispute và relist conditions rồi quyết định.

## AP-CON-009 — Mọi tiền công ty nhận là Revenue

**Không được áp dụng**

Gross Receipt được dùng trực tiếp làm company revenue.

**Canonical requirement**

Financial nature phải tách principal, deposit, collected-on-behalf, escrow, Owner/Developer proceeds, fee và other components. Revenue Context quyết định Revenue.

## AP-CON-010 — Settlement đồng nghĩa Revenue Recognition

**Không được áp dụng**

Owner/Developer payable hoặc settlement payment được coi là revenue event của công ty.

**Canonical requirement**

Settlement là transaction cash-liability process. Revenue recognition và Commission thuộc Revenue Context.

## AP-CON-011 — External payment tạo internal Payment/Receipt giả

**Không được áp dụng**

Buyer trả trực tiếp Developer/Owner nhưng CRM tạo bank Payment hoặc Receipt như thể công ty đã nhận tiền.

**Canonical requirement**

Lưu external confirmation/evidence và source confidence. Chỉ tạo internal Payment/Receipt khi receiver/process thực tế cho phép.

## AP-CON-012 — Product/Party change bằng sửa IDs trên Signed Contract

**Không được áp dụng**

Sửa `asset_id`, `listing_id`, `customer_id` hoặc effective Contract Party trực tiếp.

**Canonical requirement**

Dùng approved Amendment/Replacement/Transfer process, impact analysis, new snapshots, financial reconciliation và inventory request.

## AP-CON-013 — Allocation đã duyệt vẫn sửa tại chỗ

**Không được áp dụng**

Thay amount, purpose hoặc Receivable của approved Allocation.

**Canonical requirement**

Tạo Reversal, tính lại Receivable/Receipt impact, phê duyệt và reallocate bằng records mới.

## AP-CON-014 — Refund/Settlement `PAID` từ frontend

**Không được áp dụng**

Frontend hoặc maker tự đánh dấu payment execution hoàn tất.

**Canonical requirement**

Paid state cần authorized execution reference, reconciliation và SoD; provider/ERP confirmation đi qua Integration ACL.

## AP-CON-015 — Contract Context sở hữu File và provider runtime

**Không được áp dụng**

Lưu permanent URL/credentials/raw webhook attempts trong Contract aggregate.

**Canonical requirement**

Documents sở hữu File/Document/Version/signature evidence; Integration sở hữu provider transport. Contract giữ governed references.

## AP-CON-016 — Operational tables là certified financial reporting

**Không được áp dụng**

Dùng Contract/Receivable/Payment tables trực tiếp làm executive/statutory reports không semantic governance.

**Canonical requirement**

Analytics sở hữu certified CRM Metrics; accounting/ERP sở hữu statutory books/reports khi áp dụng.

## AP-CON-017 — Candidate examples là exact contracts

**Không được áp dụng**

Dùng table names, endpoints, statuses, Events hoặc permissions trong tài liệu này để code trực tiếp.

**Canonical requirement**

Exact database, API, Event, lifecycle, permission, error và accounting-integration contracts phải được khóa trong nguồn canonical tương ứng.

## AP-CON-018 — Mặc định tồn tại hệ thống tiền nhiệm

**Không được áp dụng**

Tự thiết kế old-contract aliases, compatibility layer hoặc historical mappings khi chưa có approved scope.

**Canonical requirement**

`crm_bds_ai` là Greenfield. Historical import chỉ tồn tại khi có scope, source mapping, security review, reconciliation và acceptance criteria riêng.

---

# 143. Kết luận

Contract and Cash Capability là lớp pháp lý và dòng tiền giao dịch của `crm_bds_ai`.

Capability phải bảo đảm:

- Contract handoff được validate tại trusted boundary.
- Signed Contract Version bất biến.
- Buyer, Seller, Owner, Payer, Signer và Beneficiary độc lập.
- Ownership, payment obligation và actual contribution không bị đồng nhất.
- Product, Party, Price, Policy và commercial terms được snapshot đúng version.
- Payment Plan có version và reconcile với Contract components.
- Receivable có nguồn hợp lệ và outstanding được tính.
- Payment, Allocation và Receipt là các records riêng.
- Issued Receipt không sửa trực tiếp; cancellation/replacement giữ lịch sử.
- Unidentified, partial, overpayment, reversal, Credit, Transfer và Offset được quản lý có kiểm soát.
- Refund và Settlement cần basis, approval, execution evidence và reconciliation.
- Collected-on-behalf funds không bị ghi nhận nhầm là Revenue.
- Contract cancellation không tự mở Listing.
- Product/Party/Price/Area changes dùng approved legal process.
- Documents, Integration, Revenue, Analytics và Audit ownership được tôn trọng.
- Cross-context orchestration dùng local transaction, Outbox, idempotency và reconciliation.
- CRM không giả vờ thay thế General Ledger hoặc statutory accounting system.

> Contract Context sở hữu legal/cash transaction truth trong CRM; nó không sở hữu Product availability, Revenue/Commission, binary Documents, provider transport hoặc statutory accounting.
