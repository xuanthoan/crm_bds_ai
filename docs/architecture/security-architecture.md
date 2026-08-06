# CRM_BDS_AI — SECURITY ARCHITECTURE

**Document ID:** `ARCH-SEC-001`  
**Canonical path:** `docs/architecture/security-architecture.md`  
**Product:** `crm_bds_ai`  
**Version:** `1.0.0`  
**Status:** `Ready for Review`  
**Owner:** `Security Owner`  
**Reviewers:** `Architecture Owner, IAM Domain Owner, Operations Owner, QA Owner`  
**Last reviewed:** `2026-08-05`  
**Classification:** `INTERNAL`


# 1. Trust boundaries

- Browser/client là untrusted.
- API boundary xác thực principal và request metadata.
- Mỗi Context enforce authorization tại application command/query.
- Provider payload đi qua Integration ACL.
- Analytics/export/BI là separate data-exfiltration boundaries.

# 2. Authentication

- User Account và Service Account thuộc IAM.
- Session/token validation tập trung nhưng authorization theo resource ở backend.
- MFA/re-auth cho grant, export, receipt, payout, data repair và break-glass.

# 3. Authorization model

```text
Decision = Permission ∩ Effective Scope ∩ Resource Policy ∩ Field Policy ∩ SoD ∩ Workflow Gate
```

- Deny by default.
- Frontend chỉ hỗ trợ UX.
- Delegation có scope, period và reason.
- Historical access không suy ra từ current organization.

# 4. Sensitive data

- Phone/Email: masked theo role và purpose.
- Financial Profile, identity documents, bank data: `HIGHLY_RESTRICTED`.
- Signed documents chỉ qua short-lived authorized access.
- Exports được log và có policy.

# 5. Segregation of Duties

Maker, checker, approver và executor phải tách khi áp dụng cho:

- Permission grants.
- Contract approval.
- Payment verification và Receipt issuance/cancellation.
- Refund/Settlement.
- Commission/Payout.
- Data Repair và Break-glass.

# 6. Application security controls

- Input validation theo typed schema.
- SQL parameterization.
- CSRF/session controls theo deployment.
- Rate limit và abuse detection.
- Idempotency key binding với payload hash.
- Secure headers và CSP.

# 7. Secrets và integration

- Không commit secret.
- Database chỉ giữ secret reference.
- Webhook signature, timestamp và replay protection.
- Provider credentials least privilege và rotation.

# 8. Audit và incident

- Audit Fact append-only.
- Sensitive read/export/approval/break-glass có evidence.
- Incident runbook, containment, notification và postmortem.

# 9. Security tests

- Horizontal/vertical privilege escalation.
- Scope bypass qua URL/query/body.
- Masking bypass qua export/cache/report.
- Replay/idempotency attacks.
- Provider webhook forgery.
- SoD violations.
