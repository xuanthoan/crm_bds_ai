# CRM_BDS_AI — SECURITY STANDARDS

## Quy chuẩn bảo mật bắt buộc cho toàn bộ hệ thống `crm_bds_ai`

**Document ID:** `ENG-SEC-001`  
**Canonical path:** `docs/engineering/security-standards.md`  
**Product:** `crm_bds_ai`  
**Version:** `1.0.0`  
**Status:** `Accepted / Mandatory`  
**Canonical:** `Yes` đối với tiêu chuẩn bảo mật trong thiết kế, phát triển, kiểm thử, triển khai và vận hành  
**Owner:** `Security Architecture Owner`  
**Reviewers:** `Architecture Owner`, `Technical Owner`, `IAM Owner`, `Database Owner`, `Frontend Owner`, `Operations Owner`, `QA Owner`, `Privacy Owner`, `Context Owners`  
**Effective date:** `2026-08-05`  
**Last reviewed:** `2026-08-05`  
**Next review:** Khi threat model, authentication, authorization, cryptography, deployment topology, data classification, legal requirements hoặc major dependencies thay đổi  
**Supersedes:** `None — Greenfield baseline`  
**Superseded by:** Không

---

# 1. Mục đích

Tài liệu này quy định tiêu chuẩn bảo mật bắt buộc cho toàn bộ `crm_bds_ai`.

Mục tiêu:

1. Bảo vệ dữ liệu khách hàng, hợp đồng, thanh toán, doanh thu, hoa hồng và tài liệu.
2. Bảo đảm mọi quyền truy cập được enforce ở backend.
3. Ngăn vượt scope, IDOR/BOLA, mass assignment và privilege escalation.
4. Bảo đảm secret, token, credentials và khóa mã hóa được quản lý an toàn.
5. Bảo đảm API, frontend, database, events, files và integrations đều có security controls.
6. Bảo đảm privacy, retention, audit và legal hold được thực thi nhất quán.
7. Bảo đảm mọi thay đổi có threat review và security tests tương ứng.
8. Bảo đảm production có monitoring, incident response và break-glass có kiểm soát.
9. Bảo đảm AI Agent không tự hạ tiêu chuẩn bảo mật để làm task nhanh hơn.
10. Bảo đảm mọi release có security evidence rõ ràng.

Tài liệu này phải được đọc cùng:

```text
docs/architecture/security-architecture.md
docs/security/threat-model.md
docs/security/data-classification.md
docs/security/permission-registry.md
docs/security/role-baseline-matrix.md
docs/security/scope-resolution.md
docs/security/field-masking-matrix.md
docs/security/segregation-of-duties.md
docs/security/privacy-and-retention.md
docs/security/secret-management.md
docs/security/webhook-security.md
docs/security/file-security.md
docs/engineering/coding-standards.md
docs/engineering/database-standards.md
docs/engineering/api-standards.md
docs/engineering/event-standards.md
docs/engineering/testing-standards.md
Relevant Context Implementation Pack
Current Sprint Execution Pack
```

---

# 2. Nguyên tắc tối cao

```text
Deny by Default
> Least Privilege
> Data Minimization
> Explicit Authorization
> Strong Authentication
> Auditable Access
> Secure Failure
> Recoverability
> Convenience
```

Không được đánh đổi security boundary để đơn giản hóa UI, API hoặc workflow.

---

# 3. Security objectives

Hệ thống phải bảo đảm:

## Confidentiality

Chỉ actor được phép mới đọc được dữ liệu.

## Integrity

Dữ liệu không bị sửa sai, sửa trái phép hoặc mất lineage.

## Availability

Dịch vụ quan trọng có khả năng chống lỗi, phục hồi và vận hành liên tục.

## Authenticity

Actor, service, provider và message được xác thực đúng nguồn.

## Accountability

Mọi hành động nhạy cảm có thể truy vết tới actor và lý do.

## Non-repudiation

Các hành động tài chính, hợp đồng, biên nhận và phê duyệt phải có bằng chứng phù hợp.

## Privacy

Dữ liệu cá nhân được thu thập, sử dụng, lưu giữ và xóa theo policy.

---

# 4. Security scope

Tiêu chuẩn này áp dụng cho:

- Backend APIs.
- Internal APIs.
- Public APIs.
- Webhooks.
- Frontend.
- PostgreSQL.
- RabbitMQ.
- Valkey.
- Object Storage.
- Background jobs.
- Event consumers.
- CI/CD.
- Source control.
- Container images.
- Dependencies.
- Logs.
- Metrics.
- Traces.
- Backups.
- Exports.
- Imports.
- Admin tools.
- Data repair.
- Break-glass.
- Third-party integrations.
- AI Agent workflows.

---

# 5. Threat model baseline

Các threat category tối thiểu:

```text
Spoofing
Tampering
Repudiation
Information Disclosure
Denial of Service
Elevation of Privilege
```

Ngoài ra phải đánh giá:

- IDOR/BOLA.
- Mass assignment.
- Broken access control.
- Injection.
- SSRF.
- XSS.
- CSRF.
- Clickjacking.
- Session fixation.
- Credential stuffing.
- Brute force.
- Token replay.
- Webhook replay.
- File upload abuse.
- Malware.
- Data exfiltration.
- Supply-chain compromise.
- Dependency confusion.
- Secret leakage.
- Misconfiguration.
- Insider threat.
- Break-glass abuse.
- Backup theft.
- Event spoofing.
- Queue poisoning.
- Cache leakage.
- Analytics overexposure.
- Export abuse.
- Privilege escalation.
- Cross-Enterprise data leakage.

---

# 6. Security ownership

## Security Architecture Owner

- Duy trì standards.
- Phê duyệt exceptions.
- Review threat model.
- Review critical designs.
- Định nghĩa release gates.

## Context Owner

- Chịu trách nhiệm security của Context.
- Định nghĩa permissions/scopes/masking.
- Duy trì tests.
- Xử lý findings.

## IAM Owner

- Authentication.
- Authorization foundation.
- Roles.
- Scopes.
- Delegation.
- Access review.

## Operations Owner

- Secrets.
- Infrastructure hardening.
- Monitoring.
- Incident response.
- Backup/restore.

## QA Owner

- Security test coverage.
- Release evidence.
- Regression control.

## AI Agent

- Không được tự tạo security exception.
- Không được bỏ test.
- Không được thay đổi security behavior ngoài scope mà không approval.

---

# 7. Data classification

Canonical levels:

```text
PUBLIC
INTERNAL
CONFIDENTIAL
RESTRICTED
HIGHLY_RESTRICTED
```

## PUBLIC

Dữ liệu được phê duyệt công khai.

## INTERNAL

Dữ liệu nội bộ, không dành cho công chúng.

## CONFIDENTIAL

Dữ liệu business nhạy cảm.

## RESTRICTED

PII, hợp đồng, audit, thông tin pháp lý.

## HIGHLY_RESTRICTED

Tài chính nhạy cảm, payment evidence, bank information, secrets, break-glass records.

---

# 8. Data classification examples

| Dữ liệu | Phân loại |
|---|---|
| Tên Project công khai | PUBLIC hoặc INTERNAL |
| Enterprise code | INTERNAL |
| Legal Entity registration details | CONFIDENTIAL |
| Customer phone/email | RESTRICTED |
| Customer identity document | HIGHLY_RESTRICTED |
| Financial Profile | HIGHLY_RESTRICTED |
| Contract document | RESTRICTED |
| Payment evidence | HIGHLY_RESTRICTED |
| Receipt | RESTRICTED |
| Commission payout | HIGHLY_RESTRICTED |
| Audit event | RESTRICTED |
| Access token | HIGHLY_RESTRICTED |
| Secret reference | RESTRICTED |
| Secret value | HIGHLY_RESTRICTED |

---

# 9. Data minimization

Mỗi API, Event, Log, Export và UI chỉ được sử dụng dữ liệu tối thiểu cần thiết.

Không truyền full Customer object nếu chỉ cần:

```text
customer_id
display_name_masked
```

Không publish full PII trong Event khi consumer có thể query owner.

Không log full payload.

Không đưa PII vào URL/query string nếu tránh được.

---

# 10. Authentication architecture

## 10.1. User authentication

Canonical:

```text
OIDC / OAuth 2.0
```

User authentication không tự xây password system nếu không có ADR.

## 10.2. Token validation

Backend phải validate:

- Signature.
- Issuer.
- Audience.
- Expiration.
- Not-before.
- Token type.
- Authorized party/client.
- Key ID.
- JWKS freshness.
- Algorithm allowlist.

Không chấp nhận:

- `alg=none`.
- Algorithm downgrade.
- Unknown issuer.
- Audience mismatch.
- Expired token.
- Unsigned token.

## 10.3. Clock skew

Clock skew có bounded tolerance.

Không mở tolerance quá rộng.

## 10.4. Token source

Bearer token chỉ lấy từ trusted header/cookie architecture.

Không lấy token từ query parameter.

---

# 11. Service authentication

Internal service calls phải dùng:

- mTLS.
- Workload identity.
- Service token.
- Approved signed internal credential.

Không dùng shared static API key toàn hệ thống.

Service identity phải:

- Unique.
- Rotatable.
- Scoped.
- Auditable.
- Environment-specific.

---

# 12. Session security

Nếu dùng browser session/cookie:

- `HttpOnly`.
- `Secure`.
- `SameSite`.
- Short idle timeout.
- Absolute timeout.
- Rotation after privilege change.
- Revocation support.
- Session fixation prevention.
- Reauthentication cho sensitive action.

Không lưu refresh token trong `localStorage`.

---

# 13. Multi-factor authentication

MFA bắt buộc cho:

- Platform Admin.
- IAM Admin.
- Security Admin.
- Finance roles.
- Commission Admin.
- Operations Admin.
- Break-glass.
- Production access.

MFA policy final theo IAM/Security docs.

---

# 14. Reauthentication

Reauthentication bắt buộc hoặc khuyến nghị mạnh cho:

- Change sensitive role.
- Break-glass activation.
- Export HIGHLY_RESTRICTED data.
- Issue/cancel Receipt.
- Execute Refund.
- Confirm Payout.
- Change bank information.
- Rotate secrets.
- Data repair.
- Delete/archive critical resource.
- Change security policy.

---

# 15. Authorization model

Effective authorization:

```text
Authenticated Actor
∩ Capability
∩ Scope
∩ Enterprise Access
∩ Legal Entity Access
∩ Project Access
∩ Resource Relationship
∩ Effective Dates
∩ Field Policy
∩ Segregation of Duties
∩ Approval Limits
∩ Break-glass Constraints
```

Không dùng role name đơn giản làm final authorization.

---

# 16. Deny by default

Nếu permission/scope/policy không rõ:

```text
DENY
```

Không dùng fallback allow.

Feature mới không có permission registry entry phải bị deny.

---

# 17. Permission registry

Mỗi permission phải có:

- Stable code.
- Context.
- Resource.
- Action.
- Allowed scopes.
- Sensitive fields.
- Approval requirements.
- SoD conflicts.
- Audit category.
- Risk class.

Permission code không được tự tạo trong router.

---

# 18. Scope enforcement

Scope phải enforce trong backend query.

Không:

```python
rows = list_all()
return [row for row in rows if allowed(row)]
```

Không tin:

- `owner_id`.
- `sale_id`.
- `enterprise_id`.
- `legal_entity_id`.
- `project_id`.

từ request như authorization truth.

Các values này chỉ là filter/request context và phải intersect với EffectiveScope.

---

# 19. Resource-level authorization

Mỗi detail/action phải kiểm tra:

- Resource tồn tại.
- Resource thuộc Enterprise/Legal Entity/Project nào.
- Actor có quyền với resource đó.
- Actor có đúng relationship không.
- Resource state có cho phép action không.

Không chỉ check permission code.

---

# 20. Field-level authorization

Sensitive fields phải:

- Omit.
- Mask.
- Redact.
- Aggregate.

Backend quyết định trước serialization.

Không trả full field rồi yêu cầu frontend ẩn.

---

# 21. Field masking

Ví dụ:

```text
Phone: ***1234
Email: a***@example.com
Identity number: ********1234
Bank account: ********7890
```

Masking algorithm phải:

- Deterministic theo policy.
- Không làm lộ quá nhiều.
- Không dùng cho crypto.
- Không thay authorization.

---

# 22. Concealment policy

Ngoài scope có thể trả:

```text
404 Not Found
```

để chống enumeration.

Policy phải nhất quán giữa:

- List.
- Detail.
- Search.
- Export.
- Related resources.
- Error messages.

---

# 23. Segregation of Duties

SoD phải được enforce cho:

- Maker/Checker/Approver.
- Contract approval.
- Refund approval/execution.
- Receipt cancel/replace.
- Commission payout approval/payment.
- Data repair.
- Break-glass approval/use.
- Role grant review.
- Secret rotation.

Không self-approve nếu policy cấm.

---

# 24. Delegation

Delegation phải:

- Time-bound.
- Scope-bound.
- Permission-bound.
- Approved.
- Audited.
- Revocable.
- Không vượt quyền delegator.
- Không bypass SoD.

---

# 25. Break-glass

Break-glass phải có:

- Explicit request.
- Justification.
- Approval.
- MFA/reauthentication.
- Limited scope.
- Short expiry.
- Session banner.
- Enhanced audit.
- Alert.
- Post-use review.

Không dùng shared emergency password.

Không dùng break-glass làm daily admin path.

---

# 26. Access reviews

Periodic access review:

- Privileged roles.
- Finance.
- Operations.
- External contractors.
- Dormant users.
- Delegations.
- Break-glass grants.
- Service identities.

Findings phải tracked và resolved.

---

# 27. API security

Mọi API phải:

- Authentication nếu không public.
- Authorization.
- Input validation.
- Output minimization.
- Rate limiting.
- Request size limit.
- Safe errors.
- Idempotency khi critical.
- ETag khi mutable.
- Audit.
- Observability.

---

# 28. IDOR/BOLA prevention

Tests phải chứng minh:

- User A không đọc resource của User B.
- Team A không đọc Team B.
- Legal Entity A không đọc Legal Entity B.
- Project A không đọc Project B.
- Changing path ID không bypass.
- Changing body owner ID không bypass.
- Search/export không leak.

---

# 29. Mass assignment prevention

Request schemas phải reject unknown/system fields.

Không cho client set:

```text
status
created_by
updated_by
approved_by
row_version
enterprise authorization scope
audit metadata
system flags
```

Dùng explicit command mapping.

---

# 30. Injection prevention

## SQL Injection

- Parameterized queries.
- SQLAlchemy binds.
- Filter/sort allowlist.
- No user-controlled identifiers.
- No string concatenation.

## Command Injection

- Không shell command từ user input.
- Không pass untrusted data vào shell.
- Use argument arrays.
- Avoid shell entirely.

## Template Injection

- Variable allowlist.
- No arbitrary expressions.
- No `eval`.

## LDAP/NoSQL Injection

Nếu provider có use case, dùng safe SDK và allowlist.

---

# 31. XSS prevention

Frontend phải:

- Escape by default.
- Không `dangerouslySetInnerHTML` nếu không sanitize.
- Sanitize rich text bằng approved library.
- No inline untrusted script.
- Content Security Policy.
- Safe URL validation.
- Avoid DOM sinks.

Backend không trả raw HTML từ untrusted data nếu không có policy.

---

# 32. Content Security Policy

Production CSP nên hạn chế:

- `default-src`.
- `script-src`.
- `style-src`.
- `img-src`.
- `connect-src`.
- `frame-ancestors`.
- `object-src 'none'`.
- `base-uri`.
- `form-action`.

Không dùng `unsafe-eval`.

`unsafe-inline` chỉ khi có migration plan/nonce strategy.

---

# 33. CSRF

Nếu dùng cookie-based authentication:

- Anti-CSRF token.
- SameSite.
- Origin/Referer validation.
- No state-changing GET.
- Double-submit hoặc framework-approved pattern.

CORS không thay CSRF protection.

---

# 34. CORS

- Approved origins only.
- No wildcard with credentials.
- Environment-specific.
- Minimal methods/headers.
- Public API reviewed separately.

Không mirror arbitrary `Origin`.

---

# 35. Clickjacking

Use:

```text
frame-ancestors
X-Frame-Options nếu cần compatibility
```

Admin UI không được embed tùy tiện.

---

# 36. Open redirect prevention

Redirect target phải:

- Internal allowlist.
- Relative URL.
- Validated origin.

Không redirect trực tiếp theo query parameter tùy ý.

---

# 37. SSRF prevention

External URL fetching phải:

- Allowlist providers/domains.
- Block localhost/private/link-local/metadata addresses.
- Validate redirects.
- Restrict protocols.
- Set timeout.
- Limit response size.
- Resolve DNS safely.
- Revalidate final destination.

Không cho user nhập URL tùy ý rồi server fetch nếu không có security design.

---

# 38. Rate limiting

Áp dụng cho:

- Login/auth-sensitive.
- Public form.
- Search.
- Export.
- File upload intent.
- Webhooks.
- Password/MFA workflows.
- Expensive analytics.
- Internal APIs nếu abuse risk.

Rate key có thể gồm:

- Actor.
- Service.
- IP.
- Enterprise.
- Endpoint.

Không chỉ dựa IP.

---

# 39. Abuse prevention

Public forms cần:

- Rate limiting.
- Bot/spam detection.
- Duplicate detection.
- Consent.
- Payload limits.
- Safe validation.
- Quarantine.

Không tạo Lead trực tiếp từ raw request mà không validation/intake policy.

---

# 40. Webhook security

Webhook inbound phải:

1. Capture raw body.
2. Verify signature.
3. Verify timestamp.
4. Enforce replay window.
5. Deduplicate provider event ID.
6. Validate content type.
7. Persist safe receipt/reference.
8. Return quickly.
9. Process async.
10. Reconcile provider state.

Không trust source IP như control duy nhất.

---

# 41. Webhook secret rotation

Phải hỗ trợ:

- Current secret.
- Previous secret overlap window.
- Rotation audit.
- Provider coordination.
- Expiry.

Không hard-code secret.

---

# 42. Outbound webhook security

- HTTPS only.
- Subscriber secret.
- Signed payload.
- Timestamp.
- Replay-resistant signature.
- Retry.
- DLQ.
- Delivery audit.
- SSRF-safe endpoint validation.
- Subscriber verification.

---

# 43. File upload security

File upload phải kiểm tra:

- Upload intent.
- Auth/scope.
- Size.
- Extension.
- MIME.
- Magic bytes.
- Hash.
- Malware scan.
- Quarantine.
- Filename sanitize.
- Object key generated by server.
- Storage classification.
- Retention.

Không tin MIME từ client.

---

# 44. File storage security

Object Storage:

- Private buckets.
- No public ACL.
- Encryption at rest.
- TLS.
- Bucket policies.
- Short-lived signed URLs.
- Environment separation.
- Object versioning/retention khi cần.
- Access logs.
- Lifecycle rules.

Không lưu permanent public URL trong database.

---

# 45. File download security

Mỗi download phải:

- Reauthorize.
- Check classification.
- Check resource relationship.
- Generate short-lived signed URL.
- Audit sensitive downloads.
- Safe filename.
- Correct content disposition.
- No path traversal.

---

# 46. File malware handling

Statuses:

```text
PENDING_SCAN
CLEAN
QUARANTINED
INFECTED
SCAN_FAILED
```

Chỉ file `CLEAN` mới được dùng business flow nếu policy yêu cầu.

Scan failure không được mặc định allow.

---

# 47. Path traversal prevention

Không dùng client filename/path làm filesystem path.

Normalize/validate.

Object key generated server-side.

Không expose local absolute paths.

---

# 48. Secrets management

Secret values phải nằm trong:

- Secret manager.
- CI secret store.
- Platform-approved encrypted store.

Không nằm trong:

- Source code.
- Markdown docs.
- `.env.example`.
- Logs.
- Database business tables.
- Frontend bundle.
- Error messages.
- Test fixtures committed.

---

# 49. Secret references

Application config có thể lưu:

```text
secret_reference
credential_reference
```

Không lưu secret value.

Secret reference cũng là sensitive metadata.

---

# 50. Secret rotation

Mỗi secret phải có:

- Owner.
- Rotation frequency.
- Rotation procedure.
- Overlap strategy.
- Revocation.
- Audit.
- Incident path.

Critical secrets rotate sau incident/suspected exposure.

---

# 51. Secret scanning

CI phải scan:

- Git history/diff.
- Source code.
- Config files.
- Docker files.
- Documentation.
- Test fixtures.

Finding critical phải block merge/release.

Không chỉ delete secret khỏi latest commit; phải rotate và xử lý history.

---

# 52. Cryptography

Chỉ dùng approved standard library/managed service.

Không tự viết crypto.

Approved patterns phải xác định:

- Algorithm.
- Key size.
- Mode.
- Nonce.
- Key management.
- Rotation.
- Compatibility.

Không dùng:

- MD5 cho security.
- SHA-1 cho signature.
- ECB.
- Static IV.
- Hard-coded key.
- Homegrown encryption.

---

# 53. Password handling

Nếu hệ thống có local secret/password use case đặc biệt:

- Argon2id hoặc approved password hashing.
- Unique salt.
- Parameter tuning.
- No reversible storage.
- No logging.
- Breached-password checks nếu applicable.

Baseline user authentication vẫn qua OIDC.

---

# 54. Hashing and HMAC

Use hash cho:

- Integrity.
- Dedup.
- Content address.
- Request canonical hash.

Use HMAC khi cần authenticity với shared secret.

Không dùng unsalted hash để “ẩn” low-entropy PII.

---

# 55. Encryption at rest

Production phải dùng:

- Database storage encryption.
- Object storage encryption.
- Backup encryption.
- Secret storage encryption.

Field-level encryption chỉ khi threat model yêu cầu và key lifecycle rõ.

---

# 56. Encryption in transit

- TLS 1.2+ hoặc policy hiện hành.
- Internal traffic protected theo topology.
- Certificate validation bắt buộc.
- Không disable verification.
- mTLS cho selected internal paths.

---

# 57. Certificate management

- Managed issuance.
- Rotation.
- Expiry alerts.
- No shared wildcard nếu unnecessary.
- Private keys protected.
- No certificate in source repo.

---

# 58. Database security

- Least privilege roles.
- No app superuser.
- No public schema CREATE.
- Explicit search path.
- TLS.
- Parameterized SQL.
- Schema ownership.
- Read-only roles.
- Audit writer restricted.
- Backups protected.
- Manual write restricted.

---

# 59. Cross-context database security

Mỗi Context runtime chỉ write schema của mình và shared infra through approved ports.

Không direct-write schema khác.

Cross-context read cũng phải theo architecture approval.

---

# 60. Row-Level Security

RLS không phải baseline mặc định.

Nếu dùng:

- ADR.
- Policies.
- Role semantics.
- Tests.
- Operational support.
- No bypass via owner role.
- App authorization vẫn cần.

---

# 61. Audit security

Audit Context:

- Append-only.
- Restricted writer.
- Restricted reader.
- No update/delete.
- Integrity seal.
- Retention.
- Sensitive access logging.
- Export controls.

Audit không lưu secret hoặc full raw payload.

---

# 62. Event security

Events phải:

- Có producer identity.
- Schema validation.
- Integrity hash.
- PII minimization.
- Queue ACL.
- Consumer allowlist.
- Versioning.
- Inbox deduplication.
- Replay controls.
- DLQ access restrictions.

Không broadcast HIGHLY_RESTRICTED data.

---

# 63. Event spoofing prevention

- Broker authentication.
- Producer ACL.
- Exchange permissions.
- Service identity.
- Schema/registry validation.
- Producer Context validation.

Consumer không trust event chỉ vì routing key đúng.

---

# 64. Event replay security

Replay:

- Restricted permission.
- Approval for sensitive flows.
- Audit.
- Dry run.
- Scope.
- Rate limit.
- Side-effect policy.
- No irreversible financial replay by default.

---

# 65. Queue security

RabbitMQ:

- TLS.
- Per-service credentials.
- Vhost separation nếu topology.
- Least privilege exchange/queue permissions.
- No default guest remote access.
- Durable queues.
- Management interface restricted.
- Credential rotation.
- Monitoring.

---

# 66. Valkey security

- Not publicly exposed.
- Authentication/TLS according topology.
- No sensitive full payload.
- TTL.
- Namespace.
- No source of truth.
- No authorization decision cache without safe invalidation.
- No business-number counter truth.

---

# 67. Cache security

Cache key không chứa raw PII.

Cached response phải include access-policy dimension nếu needed.

Không share unmasked response giữa actors/scopes.

Cache failure không được chuyển thành allow.

---

# 68. Frontend security

Frontend phải:

- Không chứa secret.
- Không trust client state cho authorization.
- Không expose source maps production nếu policy cấm.
- Sanitize rich text.
- Use secure cookies/token strategy.
- No unsafe eval.
- No dynamic script injection.
- Validate redirects.
- Use CSP.
- Avoid PII in local/session storage.

---

# 69. Browser storage

Không lưu trong localStorage/sessionStorage:

- Access token nếu architecture không cho phép.
- Refresh token.
- Customer PII.
- Payment data.
- Contract content.
- Financial Profile.
- Signed URLs.
- Secrets.

Có thể lưu non-sensitive UI preferences.

---

# 70. Frontend permission behavior

Frontend có thể:

- Hide.
- Disable.
- Explain.

Frontend không:

- Grant access.
- Derive scope authority.
- Fetch full data rồi hide.
- Compute sensitive permission locally.

---

# 71. Dependency security

Mỗi dependency phải:

- Có version lock.
- Có security scan.
- Có license review.
- Có maintenance status.
- Có owner.
- Không duplicate capability.

Không thêm abandoned package cho critical path.

---

# 72. Supply-chain security

Controls:

- Lockfiles.
- Integrity hashes.
- Trusted registries.
- Dependency pinning.
- Container image pinning/digests.
- SBOM.
- Signature/provenance nếu available.
- Restricted CI tokens.
- Protected branches.
- Review.
- Secret scanning.

---

# 73. Dependency confusion prevention

- Private package namespace.
- Registry configuration.
- No implicit public fallback.
- Package name ownership.
- CI install from approved source.
- Lockfile verification.

---

# 74. Container security

Images phải:

- Minimal.
- Non-root.
- No unnecessary package.
- Pinned digest/tag strategy.
- Scanned.
- Read-only filesystem where possible.
- Drop capabilities.
- Health checks.
- No secret baked into image.
- Separate build/runtime stages.

---

# 75. Runtime hardening

- Non-root user.
- Read-only root filesystem.
- No privileged mode.
- No Docker socket mount.
- Minimal network access.
- Resource limits.
- Seccomp/AppArmor where available.
- Temporary filesystem restrictions.
- Secret mounts.
- Egress control where possible.

---

# 76. CI/CD security

CI phải:

- Least privilege tokens.
- Protected secrets.
- No secret echo.
- Branch protection.
- Required reviews.
- Signed artifacts/provenance where possible.
- Environment approval.
- Separate deploy credentials.
- Audit logs.
- No pull-request-from-fork secret exposure.

---

# 77. Source control security

- Protected main/release branches.
- Required reviews.
- No force-push.
- CODEOWNERS for security-critical paths.
- Signed commits/tags if policy.
- Secret scanning.
- Dependency update review.
- No binary secret files.
- No production data.

---

# 78. Environment separation

Local, Test, CI, Staging, UAT, Production phải tách:

- Credentials.
- Databases.
- Buckets.
- Queues.
- Domains.
- OIDC clients.
- Provider accounts.
- Secrets.
- Logs.
- Backups.

Không dùng production credentials ở non-production.

---

# 79. Production access

Production access:

- Named accounts.
- MFA.
- Least privilege.
- Time-bound.
- Audited.
- Approved.
- No shared account.
- No routine superuser.
- Session recording where appropriate.

---

# 80. Logging security

Logs không chứa:

- Password.
- Token.
- Authorization header.
- Cookie.
- Identity document.
- Bank account.
- Full phone/email nếu không cần.
- Full request/response body.
- Signed URL.
- Secret.
- Raw file content.

Structured logs có correlation và safe references.

---

# 81. Metrics security

Metrics không chứa high-cardinality/sensitive labels:

- Customer ID.
- Phone.
- Email.
- Contract number nếu sensitive.
- Actor ID.
- Token.
- Bank reference.

---

# 82. Tracing security

Trace attributes:

- Route template.
- Operation.
- Context.
- Status.
- Safe resource type.

Không attach payload/PII.

Sampling policy phải xem xét sensitive flows.

---

# 83. Error handling security

Errors phải:

- Safe.
- Stable.
- Không expose stack trace.
- Không expose SQL.
- Không expose provider raw response.
- Không expose internal hostname.
- Không expose permission internals quá mức.

Unexpected error:

```text
500
correlation_id
generic message
```

Chi tiết chỉ trong protected logs.

---

# 84. Fail secure

Khi dependency security-critical fail:

- Authorization resolver unavailable → deny/fail closed.
- Approval policy unavailable → không bypass.
- File scan unavailable → quarantine.
- Signature verification unavailable → reject/defer.
- Secret provider unavailable → fail startup/operation.
- Masking policy unavailable → deny sensitive response.

Không mặc định allow.

---

# 85. Availability and DoS protection

Controls:

- Rate limiting.
- Timeouts.
- Request size limits.
- Pagination.
- Async jobs.
- Queue backpressure.
- Connection pool limits.
- Circuit breakers.
- Resource quotas.
- Upload limits.
- Search complexity limits.

---

# 86. Circuit breaker

External providers:

- Timeout.
- Failure threshold.
- Open/half-open.
- Metrics.
- Fallback.
- No fallback that corrupts business truth.

---

# 87. Resource exhaustion prevention

- Max page size.
- Max export range.
- Max upload size.
- Max search length.
- Max filter count.
- Max bulk items.
- Max synchronous business calendar range.
- Max template size.
- Max event payload.

---

# 88. Privacy principles

- Purpose limitation.
- Data minimization.
- Accuracy.
- Storage limitation.
- Security.
- Accountability.
- Consent where applicable.
- Rights handling where legally required.

---

# 89. Consent

Consent records cần:

- Purpose.
- Channel.
- Source.
- Version.
- Granted/withdrawn.
- Timestamp.
- Evidence.
- Scope.
- Expiry nếu applicable.

Marketing suppression phải override journey send.

---

# 90. Retention

Retention theo data class và legal requirements.

Purge/anonymization phải:

- Policy-driven.
- Audited.
- Respect legal hold.
- Preserve financial/legal evidence.
- Be tested.

Không giữ dữ liệu vô thời hạn nếu không có lý do.

---

# 91. Legal hold

Legal hold:

- Blocks deletion/anonymization.
- Has owner/reason.
- Effective dates.
- Audit.
- Release approval.

---

# 92. Data subject requests

Nếu applicable, quy trình phải hỗ trợ:

- Access.
- Correction.
- Restriction.
- Deletion/anonymization.
- Consent withdrawal.
- Export.

Phải kiểm tra legal/contractual exceptions.

Không tự xóa financial/legal evidence.

---

# 93. Export security

Export:

- Separate permission.
- Reauthorize.
- Masking.
- Async.
- Expiring file.
- Audit.
- Rate limit.
- Approval for HIGHLY_RESTRICTED.
- Watermark/classification where needed.

Không cho client export toàn bộ bằng cách paginate silently.

---

# 94. Import security

Import:

- File scan.
- Staging.
- Validation.
- Mapping allowlist.
- Dry run.
- Canonical commands.
- Scope.
- Audit.
- No direct DB insert.
- Formula/macro risk review.

---

# 95. Spreadsheet security

CSV/XLSX exports phải phòng:

- Formula injection.
- DDE.
- Dangerous leading characters.
- Hidden sheets/macros.
- PII exposure.

Sanitize cells bắt đầu bằng:

```text
=
+
-
@
```

theo policy phù hợp.

---

# 96. Email and notification security

- No secrets.
- Minimal PII.
- No sensitive full data.
- Signed/expiring links.
- Recipient reauthorization where needed.
- Template allowlist.
- HTML sanitization.
- Suppression/consent.
- Delivery audit.

---

# 97. Authentication events

Security events:

- Login success/failure.
- MFA challenge/failure.
- Session revoked.
- Token validation failure.
- Suspicious IP/device.
- Privilege change.
- Break-glass.
- Access denied spike.

Không log password/token.

---

# 98. Security audit events

Audit categories:

```text
AUTHENTICATION
AUTHORIZATION
PRIVILEGE_CHANGE
SENSITIVE_ACCESS
EXPORT
DOWNLOAD
BREAK_GLASS
SECRET_ROTATION
DATA_REPAIR
SECURITY_CONFIGURATION
INCIDENT_RESPONSE
```

---

# 99. Anomaly detection

Monitor:

- Repeated authorization denials.
- Cross-Enterprise access attempts.
- Mass export.
- Unusual download volume.
- Privileged action outside hours.
- Repeated webhook signature failure.
- Token replay.
- Queue poisoning.
- Secret access anomalies.
- Break-glass usage.
- Data repair.

---

# 100. Security incident response

Phases:

```text
Detect
→ Triage
→ Contain
→ Eradicate
→ Recover
→ Notify
→ Review
```

Incident runbook phải có:

- Severity.
- Roles.
- Communication.
- Evidence preservation.
- Credential rotation.
- Data impact assessment.
- Legal/privacy escalation.
- Recovery verification.
- Postmortem.

---

# 101. Evidence preservation

Khi incident:

- Preserve logs.
- Preserve audit.
- Preserve relevant database snapshots.
- Preserve access records.
- Hash artifacts.
- Restrict access.
- Track chain of custody.

Không “dọn log” trước investigation.

---

# 102. Vulnerability management

Findings có:

- Severity.
- Affected components.
- Exploitability.
- Data impact.
- Owner.
- SLA.
- Fix.
- Verification.
- Exception nếu cần.

Critical/High phải block release theo policy.

---

# 103. Severity model

Baseline:

```text
CRITICAL
HIGH
MEDIUM
LOW
INFORMATIONAL
```

Severity dựa:

- Exploitability.
- Privilege.
- Data sensitivity.
- Blast radius.
- Business impact.
- Detectability.
- Availability impact.

---

# 104. Patch management

- Critical patches expedited.
- Dependency/container scans.
- Staging verification.
- Rollback plan.
- Emergency change process.
- Post-deploy validation.

Không trì hoãn critical patch không có approved exception.

---

# 105. Secure SDLC

Mỗi feature phải trải qua:

1. Security requirements.
2. Threat assessment.
3. Secure design.
4. Implementation standards.
5. Security tests.
6. Code review.
7. Scan.
8. Release gate.
9. Monitoring.
10. Post-release review.

---

# 106. Threat modeling triggers

Threat model bắt buộc khi:

- New authentication flow.
- New role/scope.
- New public API.
- New webhook/provider.
- New file upload.
- New financial flow.
- New export.
- New cross-context process.
- New data classification.
- New secret/crypto use.
- New deployment topology.
- New external storage.
- New AI/automation feature.

---

# 107. Security design review checklist

## Identity

- Actor/service/provider xác thực thế nào?
- Session/token lifecycle?
- MFA/reauthentication?

## Authorization

- Permission?
- Scope?
- Resource relationship?
- Field masking?
- SoD?

## Data

- Classification?
- Minimization?
- Retention?
- Encryption?
- Export?

## Interfaces

- API?
- Webhook?
- File?
- Event?
- SSRF/input risks?

## Operations

- Logs?
- Alerts?
- Incident?
- Break-glass?
- Backup?

---

# 108. Secure coding rules

Bị cấm:

- `eval`.
- `exec`.
- Unsafe deserialization.
- Pickle from untrusted input.
- Dynamic SQL.
- Shell command from user input.
- Hard-coded credentials.
- Disable TLS verification.
- Trust client role/scope.
- Return ORM directly.
- Log full request.
- Store token in localStorage without architecture approval.
- Public bucket.
- Arbitrary URL fetch.
- Arbitrary template expression.

---

# 109. Input validation

Mọi untrusted input:

- Type.
- Length.
- Format.
- Range.
- Enum.
- Character set.
- Cross-field.
- Business validation.
- Normalization.

Không chỉ validate ở frontend.

---

# 110. Output encoding

Encode theo context:

- HTML.
- JavaScript.
- URL.
- CSV.
- JSON.
- SQL parameters.

Không reuse one sanitizer cho mọi context.

---

# 111. Safe serialization

- No arbitrary object serialization.
- `additionalProperties: false`.
- Stable schemas.
- No secret fields.
- Decimal/time formats.
- No executable payload.

---

# 112. Deserialization

Reject unknown types/fields.

Không instantiate arbitrary class từ input.

No polymorphic deserialization without allowlist.

---

# 113. Security headers

Web responses cần xem xét:

```text
Content-Security-Policy
X-Content-Type-Options
Referrer-Policy
Permissions-Policy
Strict-Transport-Security
Cross-Origin-Opener-Policy
Cross-Origin-Resource-Policy
```

Final set theo deployment/frontend architecture.

---

# 114. HSTS

Production HTTPS phải dùng HSTS khi domain ready.

Không enable preload tùy tiện trước khi xác nhận toàn bộ subdomain.

---

# 115. Referrer policy

Dùng restrictive policy để tránh URL data leakage.

Không đưa PII/token vào URL.

---

# 116. Third-party scripts

Third-party scripts trên frontend phải:

- Approved.
- Minimal.
- CSP allowlist.
- Privacy review.
- Integrity/subresource controls khi possible.
- No access to sensitive pages if avoidable.

Không tự thêm analytics script vào secure admin pages mà không review.

---

# 117. Tag Manager

Google Tag Manager hoặc tương tự:

- Không được đọc HIGHLY_RESTRICTED data.
- Không được capture form values chứa PII.
- Không được chạy trên sensitive routes nếu policy cấm.
- Data layer phải allowlist.
- Consent management.
- Security/privacy review.

---

# 118. Client-side analytics

Không gửi:

- Phone.
- Email.
- Customer ID nếu linkable.
- Contract ID nếu sensitive.
- Payment data.
- Commission data.
- Document names.
- Search strings chứa PII.

---

# 119. AI and automation security

AI Agent hoặc AI feature không được:

- Nhận secret không cần thiết.
- Truy cập production tự do.
- Direct-write database.
- Bypass approval.
- Generate unreviewed security policy.
- Include PII in prompt/log.
- Execute arbitrary code from model output.
- Trust model output as authorization decision.

AI-generated code phải qua same CI/security gates.

---

# 120. Prompt/data security

Nếu tích hợp AI:

- Data minimization.
- Provider terms/privacy.
- No secret.
- No HIGHLY_RESTRICTED unless approved.
- Retention settings.
- Redaction.
- Audit.
- Human review for critical actions.

---

# 121. Security testing taxonomy

Bắt buộc:

- Authentication tests.
- Authorization matrix.
- IDOR/BOLA.
- Mass assignment.
- Field masking.
- Input validation.
- Injection.
- XSS.
- CSRF.
- CORS.
- SSRF.
- Rate limiting.
- Webhook security.
- File security.
- Secret scanning.
- Dependency scanning.
- Container scanning.
- Infrastructure config scanning.
- Event security.
- Logging/PII tests.
- Break-glass tests.
- Backup access tests.

---

# 122. Authentication tests

Test:

- Valid token.
- Missing token.
- Expired token.
- Wrong issuer.
- Wrong audience.
- Unknown key.
- Invalid signature.
- Algorithm downgrade.
- Clock skew.
- Revoked session.
- Disabled user.
- User without active assignment.
- MFA-required flow.

---

# 123. Authorization tests

Test matrix:

```text
Capability
× Scope
× Enterprise
× Legal Entity
× Project
× Resource relationship
× State
× Field policy
× SoD
```

Không chỉ test admin/user.

---

# 124. IDOR/BOLA tests

- Change path ID.
- Change nested resource ID.
- Change query filter.
- Change export scope.
- Change file/document ID.
- Change process/job ID.
- Change dashboard drill-down ID.
- Guess sequential business number.

Expected:

- 404/403 according policy.
- No side effect.
- No existence leak.
- Audit/metrics where required.

---

# 125. Mass assignment tests

Send:

- `status`.
- `approved_by`.
- `created_by`.
- `owner_id`.
- `enterprise_id`.
- `row_version`.
- `is_admin`.
- `permission_codes`.

Expected:

- Rejected/ignored only if contract says, ưu tiên reject.
- No persisted unauthorized change.

---

# 126. Injection tests

Test payloads cho:

- SQL injection.
- Template injection.
- Command injection.
- CSV injection.
- Path traversal.
- Header injection.
- Log injection.
- SSRF.
- XSS.

Use safe test payloads, không gây hại thật.

---

# 127. Webhook security tests

- Valid signature.
- Invalid signature.
- Expired timestamp.
- Replay.
- Duplicate event.
- Modified body.
- Wrong secret.
- Rotation overlap.
- Oversized body.
- Unsupported content type.
- Unknown event type.

---

# 128. File security tests

- Extension mismatch.
- MIME mismatch.
- Magic bytes mismatch.
- Oversized file.
- Archive bomb safe fixture.
- Path traversal filename.
- Malware test fixture theo standard an toàn.
- Public ACL denial.
- Signed URL expiry.
- Unauthorized download.
- Quarantine behavior.

---

# 129. Secret tests

CI tests:

- No hard-coded secret patterns.
- No `.env` committed.
- No private key.
- No token in docs.
- No secret in image layer.
- No secret in frontend bundle.
- No secret in logs.

---

# 130. Dependency and container scanning

CI phải chạy:

- SCA.
- Vulnerability scan.
- License scan.
- Container scan.
- SBOM generation.
- IaC/config scan nếu applicable.

Critical/High findings block theo policy.

---

# 131. Dynamic security testing

Staging/UAT có thể chạy:

- DAST.
- Authenticated scans.
- API scans.
- Header/CORS checks.
- Rate limit checks.

Không chạy destructive scan production không approval.

---

# 132. Penetration testing

Trước production và định kỳ:

- External/internal scope.
- Auth.
- Authorization.
- API.
- Webhooks.
- Files.
- Admin.
- Infrastructure.
- Social/operational controls nếu scope.

Findings phải remediated/accepted formally.

---

# 133. Security regression tests

Mọi vulnerability fix cần regression test.

Không đóng finding chỉ bằng code change không verification.

---

# 134. Security observability tests

Test:

- Denial metric.
- Suspicious login alert.
- Webhook signature failure alert.
- Break-glass alert.
- Export audit.
- Secret access audit.
- No PII in logs.
- Trace sanitization.

---

# 135. Security release gates

Release bị block nếu:

- Critical vulnerability.
- High broken access control.
- Missing security tests.
- Secret leak.
- Public bucket.
- Invalid TLS/certificate.
- Unapproved dependency risk.
- Failed backup encryption.
- Missing audit for critical action.
- Authorization regression.
- Webhook signature bypass.
- File scan fail-open.
- Break-glass uncontrolled.

---

# 136. Security incident drill

Drill tối thiểu:

- Credential leak.
- Unauthorized export.
- Broken access control.
- Malware upload.
- Webhook spoofing.
- Database compromise suspicion.
- Audit integrity failure.
- Ransomware/backup recovery.
- Supply-chain compromise.

---

# 137. Backup security

Backups:

- Encrypted.
- Access controlled.
- Immutable/isolated where possible.
- Rotated credentials.
- Monitored.
- Restore tested.
- Retention policy.
- No public access.

Backup operator không mặc định có business data access beyond need.

---

# 138. Restore security

Restore:

- Approved.
- Isolated.
- Access controlled.
- Audit.
- Secret rotation if incident.
- Validate permissions/grants.
- Validate audit integrity.
- Sanitize non-production restore.

---

# 139. Data repair security

Data repair:

- Separate permission.
- Approval.
- Dry run.
- Backup/checkpoint.
- Script hash/version.
- Limited scope.
- Audit.
- Verification.
- No ad-hoc hidden SQL.

---

# 140. Security exceptions

Exception chỉ được chấp nhận khi:

- Business need rõ.
- No safer alternative.
- Risk assessed.
- Mitigation.
- Owner.
- Expiry.
- Approval.
- Tracking.
- Review.

Không có permanent exception không owner.

---

# 141. Exception document

```text
docs/engineering/security-exceptions/EXC-SEC-XXX.md
```

Fields:

```text
Rule
Scope
Reason
Threat
Data classification
Impact
Likelihood
Mitigation
Monitoring
Owner
Expiry
Removal plan
Approvals
```

---

# 142. Security documentation requirements

Phải có:

```text
docs/architecture/security-architecture.md
docs/security/threat-model.md
docs/security/data-classification.md
docs/security/permission-registry.md
docs/security/role-baseline-matrix.md
docs/security/scope-resolution.md
docs/security/field-masking-matrix.md
docs/security/segregation-of-duties.md
docs/security/privacy-and-retention.md
docs/security/secret-management.md
docs/security/webhook-security.md
docs/security/file-security.md
docs/runbooks/security-incident-response.md
docs/runbooks/break-glass.md
docs/runbooks/credential-rotation.md
docs/runbooks/data-breach.md
```

---

# 143. Security review checklist

## Authentication

- OIDC/JWT?
- Token validation?
- MFA?
- Session?
- Reauthentication?

## Authorization

- Permission?
- Scope?
- Resource?
- Field?
- SoD?
- Concealment?

## Data

- Classification?
- Minimization?
- Encryption?
- Retention?
- Export?
- Audit?

## Interface

- Input validation?
- Rate limit?
- Webhook?
- File?
- SSRF?
- CORS/CSRF?

## Operations

- Secrets?
- Logs?
- Alerts?
- Incident?
- Backup?
- Break-glass?

---

# 144. Security anti-patterns bị cấm

1. Frontend authorization là security boundary.
2. Trust client-supplied scope/owner.
3. Shared admin account.
4. Hard-coded secret.
5. Secret trong `.env.example`.
6. Token trong URL.
7. Public object bucket.
8. Disable TLS verification.
9. `eval`/`exec`.
10. Dynamic SQL.
11. Log full request/response.
12. Store PII in localStorage.
13. Webhook không signature/replay.
14. File scan fail-open.
15. Generic admin sees all PII by default.
16. Break-glass không expiry.
17. Self-approval trái SoD.
18. Event chứa full sensitive payload.
19. Cache unmasked response across users.
20. Direct DB write cross-context.
21. Security exception không expiry.
22. Ignore High finding không approval.
23. Use production data in tests.
24. Return raw stack trace.
25. Open CORS wildcard with credentials.

---

# 145. AI Agent security protocol

Trước khi triển khai feature, AI Agent phải:

1. Xác định data classification.
2. Xác định actors.
3. Xác định permissions/scopes.
4. Xác định field masking.
5. Xác định SoD/approval.
6. Xác định threat vectors.
7. Xác định secrets/crypto.
8. Xác định API/webhook/file/event controls.
9. Xác định audit/alerts.
10. Xác định security tests.
11. Update threat model/docs.
12. Run scans/tests.
13. Ghi evidence.
14. Không tự hạ tiêu chuẩn.

---

# 146. AI Agent prohibited security behaviors

AI Agent không được:

1. Bypass authorization để test pass.
2. Hard-code admin allow.
3. Tin role từ frontend.
4. Tắt TLS.
5. Log token/PII.
6. Thêm secret vào code/docs.
7. Bỏ webhook signature.
8. Bỏ file scan.
9. Tạo public bucket.
10. Tự cho system admin xem tất cả.
11. Tự tạo exception.
12. Tự bỏ security test.
13. Tự suppress critical scan.
14. Báo secure khi chưa test.
15. Tạo fake security evidence.

---

# 147. Definition of Ready cho security-sensitive change

Change chỉ Ready khi:

1. Threats rõ.
2. Data classification rõ.
3. Actors rõ.
4. Authentication rõ.
5. Permission/scope rõ.
6. Field masking rõ.
7. Secrets/crypto rõ.
8. Audit/alert rõ.
9. Test plan rõ.
10. No unresolved critical risk.
11. Security Owner review khi required.

---

# 148. Definition of Done cho security-sensitive change

Change chỉ Done khi:

1. Controls implemented.
2. Permission registry updated.
3. Scope enforced backend.
4. Field masking implemented.
5. SoD/approval implemented.
6. Audit implemented.
7. Secrets managed.
8. API/webhook/file/event controls pass.
9. Security tests pass.
10. Scans pass.
11. No Critical/High unapproved finding.
12. Threat model updated.
13. Runbooks updated.
14. Evidence recorded.
15. Acceptance Report updated.

---

# 149. Security completion report

```markdown
## Security Summary

### Data Classification

### Authentication

### Authorization

### Permissions and Scopes

### Field Masking

### Segregation of Duties

### Secrets and Cryptography

### API Security

### Webhook Security

### File Security

### Event Security

### Database Security

### Logging and Audit

### Security Tests

### Vulnerability Scans

### Threat Model Updates

### Known Risks

### Exceptions

### Final Result
```

---

# 150. Change Log

## Version 1.0.0 — 2026-07-24

- Thiết lập security objectives và threat baseline.
- Khóa authentication, service identity và session security.
- Khóa authorization, scope, masking và SoD.
- Khóa API, webhook, file và frontend security.
- Khóa secrets, cryptography, database, events và cache security.
- Khóa privacy, retention, export/import và audit.
- Khóa supply-chain, container, CI/CD và environment security.
- Khóa monitoring, incident response và vulnerability management.
- Khóa security testing, release gates và AI Agent protocol.

---

# 151. Kết luận

Security trong `crm_bds_ai` không phải là một middleware hoặc một checklist cuối Sprint.

Security phải tồn tại trong toàn bộ lifecycle:

```text
Requirements
→ Threat Model
→ Design
→ Implementation
→ Testing
→ Deployment
→ Monitoring
→ Incident Response
→ Continuous Improvement
```

Nguyên tắc tối cao:

> Mọi quyền truy cập phải được xác thực, mọi dữ liệu nhạy cảm phải được giảm thiểu, mọi hành động quan trọng phải được audit và mọi failure của security control phải mặc định fail closed.


# AI security constraints

Prompt construction occurs only after backend authorization, effective scope, purpose and masking. Untrusted content is data, tool access is allowlisted, secrets never enter prompts/logs, and provider trust/classification policy is enforced before routing.
