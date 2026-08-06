# CRM_BDS_AI — SEGREGATION OF DUTIES

**Document ID:** `SEC-SOD-001`  
**Canonical path:** `docs/security/segregation-of-duties.md`  
**Product:** `crm_bds_ai`  
**Version:** `1.0.0`  
**Status:** `Ready for Review`  
**Owner:** `Security Owner`  
**Reviewers:** `Product Owner, Finance Owner, IAM Owner, Audit Owner`  
**Last reviewed:** `2026-08-05`  
**Classification:** `INTERNAL`


# 1. Matrix

| Process | Maker | Checker/Approver | Constraint |
|---|---|---|---|
| IAM access grant | Requester | Approver | Same user may not grant own high-risk permission |
| Contract approval | Contract maker | Legal/authorized approver | No self-approval above authority |
| Payment verification | Finance maker | Finance checker | Independent evidence |
| Receipt cancellation | Requester | Authorized approver | Issued Receipt immutable |
| Refund | Requester | Approver | Executor confirmation separate |
| Settlement | Maker | Approver | External execution separate |
| Commission plan/entitlement | Calculator | Approver | Beneficiary cannot approve own exception |
| Payout | Batch maker | Approver | External confirmation separate |
| Data Repair | Requester/analyst | Approver | Executor and validator recorded |
| Break-glass | Requester | Emergency approver | Post-review mandatory |

# 2. Enforcement

SoD được enforce backend bằng principal identity, role/relationship, workflow state và immutable history. Delegation không được phá conflict rules.

# 3. Exceptions

Chỉ qua approved emergency policy, reason, expiry, Audit và post-review.
