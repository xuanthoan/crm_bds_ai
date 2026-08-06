# CRM_BDS_AI — BACKUP AND RESTORE RUNBOOK

## Runbook sao lưu, xác minh và khôi phục bắt buộc cho toàn bộ hệ thống `crm_bds_ai`

**Document ID:** `RUNBOOK-BACKUP-RESTORE-001`  
**Canonical path:** `docs/runbooks/backup-and-restore.md`  
**Product:** `crm_bds_ai`  
**Version:** `1.0.0`  
**Status:** `Accepted / Mandatory for Production Readiness`  
**Canonical:** `Yes` đối với quy trình backup, verification, restore và restore drill  
**Owner:** `Operations Owner`  
**Technical owner:** `Database and Platform Reliability Owner`  
**Reviewers:** `Architecture Owner`, `Security Owner`, `Database Owner`, `Documents Owner`, `Audit Owner`, `Integration Owner`, `QA Owner`, `Business Continuity Owner`  
**Effective date:** `2026-08-05`  
**Last reviewed:** `2026-08-05`  
**Review frequency:** Hàng quý và sau mỗi thay đổi topology, storage, database, deployment hoặc retention policy  
**Classification:** `RESTRICTED`  
**Related documents:**

```text
docs/operations/service-level-objectives.md
docs/operations/capacity-model.md
docs/runbooks/disaster-recovery.md
docs/runbooks/production-incident-response.md
docs/runbooks/database-failure.md
docs/runbooks/rabbitmq-failure.md
docs/runbooks/data-repair.md
docs/engineering/database-standards.md
docs/engineering/security-standards.md
docs/engineering/testing-standards.md
docs/security/privacy-and-retention.md
docs/security/secret-management.md
docs/architecture/environment-topology.md
docs/deployment/release-and-rollback-strategy.md
```

> Lưu ý: Runbook này là tài liệu vận hành. Các lệnh mẫu phải được tham số hóa theo môi trường thực tế. Không ghi secret, password, token hoặc private key vào tài liệu, terminal history, CI log hoặc ticket.

---

# 1. Mục đích

Runbook này quy định cách:

1. Xác định dữ liệu cần sao lưu.
2. Lập lịch sao lưu.
3. Mã hóa và lưu trữ bản sao lưu.
4. Xác minh backup có thể sử dụng.
5. Khôi phục từng thành phần.
6. Khôi phục toàn hệ thống.
7. Khôi phục theo thời điểm bằng PostgreSQL PITR.
8. Khôi phục dữ liệu bị xóa hoặc thay đổi nhầm.
9. Khôi phục trong môi trường kiểm thử cô lập.
10. Thực hiện restore drill định kỳ.
11. Đo RPO và RTO thực tế.
12. Ghi nhận bằng chứng vận hành.
13. Xử lý backup thất bại hoặc backup bị nghi ngờ.
14. Ngăn backup trở thành nguồn rò rỉ dữ liệu.
15. Bảo đảm AI Agent hoặc operator không thực hiện restore phá hủy ngoài kiểm soát.

---

# 2. Nguyên tắc tối cao

```text
A backup is not valid until it has been restored and verified.
```

Thứ tự ưu tiên:

```text
Data Integrity
> Security
> Recoverability
> Auditability
> Business Continuity
> Speed
> Operator Convenience
```

Các nguyên tắc bắt buộc:

- Không coi job `SUCCESS` là bằng chứng backup dùng được.
- Không restore trực tiếp lên production nếu chưa có phê duyệt.
- Không overwrite production khi chưa có snapshot/checkpoint mới.
- Không bỏ qua object storage khi restore document-related workflows.
- Không coi RabbitMQ hoặc Valkey là nguồn chân lý dài hạn.
- Không dùng backup cũ hơn retention/RPO mà không nêu rõ data loss.
- Không khôi phục một phần dữ liệu nghiệp vụ bằng SQL ad-hoc nếu chưa có kế hoạch reconciliation.
- Không dùng production backup trong non-production nếu chưa được anonymize hoặc có kiểm soát truy cập tương đương.
- Mọi restore production phải có Incident hoặc Approved Change Record.
- Mọi restore phải có evidence và verification report.

---

# 3. Phạm vi hệ thống

Runbook áp dụng cho các thành phần:

```text
PostgreSQL
Object Storage
RabbitMQ definitions and durable state metadata
Valkey configuration and selected recoverable data
Application configuration
Feature flags and workflow definitions
OIDC/service configuration references
Secrets references and secret recovery procedures
Alembic migration state
Audit integrity material
Event Outbox/Inbox state
Integration mappings and cursors
Operations jobs and incident records
Deployment manifests and infrastructure configuration
Generated business documents and evidence
```

---

# 4. Nguồn chân lý và mức độ khôi phục

| Thành phần | Vai trò | Nguồn chân lý | Bắt buộc backup | Ghi chú |
|---|---|---:|---:|---|
| PostgreSQL | Operational data | Có | Có | Thành phần quan trọng nhất |
| Object Storage | Files/documents/evidence | Có | Có | Phải nhất quán với metadata DB |
| RabbitMQ | Message transport | Không phải business SoT | Một phần | Backup definitions; queue recovery theo policy |
| Valkey | Cache/locks/ephemeral state | Không | Có chọn lọc | Không phục hồi cache như business truth |
| Outbox | Reliable event source trong retention | Có tính kỹ thuật | Có qua PostgreSQL | Không phụ thuộc broker history |
| Inbox | Consumer deduplication | Có tính kỹ thuật | Có qua PostgreSQL | Quan trọng khi replay |
| Audit | Append-only evidence | Có | Có | Phải kiểm tra integrity |
| Secrets | Security material | Có trong secret manager | Theo secret system | Không export secret vào bundle chung |
| Deployment manifests | Reproducible environment | Có | Có | Lưu trong Git/artifact registry |
| Metrics/logs/traces | Observability | Không phải business SoT | Theo retention | Không dùng thay Audit |

---

# 5. Mục tiêu RPO và RTO

## 5.1. Baseline production targets

```text
RPO mục tiêu: ≤ 15 phút
RTO mục tiêu: ≤ 4 giờ
```

Các giá trị cuối cùng phải được khóa trong `service-level-objectives.md`.

## 5.2. Diễn giải

### RPO

Lượng dữ liệu tối đa có thể mất tính từ thời điểm sự cố.

Ví dụ:

- Sự cố lúc 10:40.
- Điểm phục hồi gần nhất 10:30.
- RPO thực tế = 10 phút.

### RTO

Thời gian từ lúc tuyên bố khôi phục đến khi hệ thống vượt qua verification và được phép phục vụ.

## 5.3. Mức độ ưu tiên

| Thành phần | RPO baseline | RTO baseline |
|---|---:|---:|
| PostgreSQL operational | 15 phút | 4 giờ |
| Audit data | 15 phút | 4 giờ |
| Object Storage | 15–60 phút tùy replication | 4 giờ |
| Integration mappings/config | 24 giờ hoặc thấp hơn | 4 giờ |
| RabbitMQ definitions | 24 giờ | 2 giờ |
| Valkey cache | Không áp dụng | 30 phút |
| Deployment manifests | Mỗi release | 1 giờ |

## 5.4. Không tự tuyên bố đạt RPO/RTO

RPO/RTO chỉ được công nhận khi restore drill đo được trong topology tương đương production.

---

# 6. Vai trò và trách nhiệm

## Incident Commander

- Điều phối restore production.
- Quyết định ưu tiên.
- Phê duyệt communication.
- Không tự thao tác kỹ thuật nếu không cần.

## Restore Lead

- Sở hữu kế hoạch restore.
- Điều phối Database, Storage, Application và Verification.
- Duy trì timeline.

## Database Operator

- PostgreSQL backup/PITR/restore.
- Kiểm tra migration, consistency và performance.

## Storage Operator

- Object Storage backup/restore.
- Kiểm tra hash, version, lifecycle và signed access.

## Application Owner

- Kiểm tra application compatibility.
- Chạy smoke và critical journey tests.
- Bật/tắt workers/traffic.

## Security Owner

- Kiểm tra quyền truy cập, encryption, secret rotation và evidence.
- Đánh giá backup có bị compromise không.

## Audit Owner

- Xác minh audit integrity.
- Kiểm tra chuỗi seal/hash nếu triển khai.

## Business Validator

- Xác minh dữ liệu nghiệp vụ quan trọng.
- Không trực tiếp chỉnh dữ liệu.

## Communications Owner

- Cập nhật status page/internal stakeholders.
- Ghi thời gian và quyết định.

---

# 7. Điều kiện bắt buộc trước production

Production không được go-live nếu thiếu:

1. Automated PostgreSQL backups.
2. Continuous WAL archiving hoặc managed PITR.
3. Object Storage versioning/replication hoặc backup.
4. Backup encryption.
5. Offsite/independent copy.
6. Retention policy.
7. Monitoring và alerts.
8. Restore test thành công.
9. Restore credentials và access path.
10. Runbook được diễn tập.
11. Defined RPO/RTO.
12. Audit evidence.
13. Owner/on-call rõ.
14. Recovery environment capacity.
15. Dependency configuration backup.

---

# 8. Phân loại backup

## 8.1. PostgreSQL physical base backup

Dùng cho:

- Full cluster restore.
- PITR.
- Production-scale recovery.

## 8.2. WAL archive

Dùng cho:

- Continuous recovery.
- Point-in-time restore.
- RPO thấp.

## 8.3. PostgreSQL logical backup

Dùng cho:

- Additional defense.
- Schema inspection.
- Selective extraction trong môi trường cô lập.
- Migration validation.

Không thay physical/PITR ở production.

## 8.4. Object Storage backup

Dùng:

- Versioning.
- Cross-region/account replication.
- Backup copy.
- Immutable retention khi cần.

## 8.5. Configuration backup

Bao gồm:

- Deployment manifests.
- Environment templates không chứa secret.
- RabbitMQ definitions.
- Feature flag exports.
- Provider configuration references.
- Infrastructure-as-Code.
- Alembic revision.

## 8.6. Secret recovery

Theo secret manager:

- Replication.
- Version history.
- Break-glass recovery.
- Rotation.

Không đóng gói secret plaintext với database backup.

---

# 9. Backup consistency model

## 9.1. PostgreSQL và Outbox/Inbox

Outbox, Inbox, Audit và operational state cùng nằm PostgreSQL nên được phục hồi nhất quán theo database transaction timeline.

## 9.2. PostgreSQL và Object Storage

File upload flow phải có states rõ:

```text
UPLOAD_INTENT
UPLOADED
PENDING_SCAN
CLEAN
COMPLETED
LINKED
```

Restore có thể tạo:

- DB metadata trỏ object chưa restore.
- Object tồn tại nhưng metadata chưa có.
- Version mismatch.

Sau restore bắt buộc chạy object-reference reconciliation.

## 9.3. PostgreSQL và RabbitMQ

RabbitMQ không phải source of truth.

Sau restore:

- Outbox chưa published phải publish lại.
- Inbox ngăn duplicate.
- Broker queues có thể được dựng lại.
- Không cố restore broker state để thay database truth.

## 9.4. PostgreSQL và Valkey

Valkey cache được flush/rebuild.

Không restore stale cache nếu có nguy cơ dữ liệu quyền hoặc trạng thái cũ.

---

# 10. Backup schedule baseline

| Backup type | Tần suất | Retention baseline |
|---|---:|---:|
| PostgreSQL WAL archive | Liên tục | Theo PITR window |
| PostgreSQL base backup | Hàng ngày | 7–35 ngày |
| PostgreSQL logical backup | Hàng ngày hoặc hàng tuần | 14–90 ngày |
| Object Storage replication | Gần thời gian thực | Theo object retention |
| Object Storage inventory/hash report | Hàng ngày | 90 ngày |
| RabbitMQ definitions | Sau thay đổi + hàng ngày | 30–90 ngày |
| Deployment manifests | Mỗi release | Không xóa release được hỗ trợ |
| Feature/config export | Hàng ngày + sau thay đổi | 90 ngày |
| Audit integrity report | Hàng ngày | Theo audit retention |
| Restore drill | Hàng quý | Lưu report dài hạn |

Retention cuối cùng phải phù hợp pháp lý, privacy và chi phí.

---

# 11. Backup naming convention

Backup artifact phải dùng format:

```text
<environment>/<component>/<yyyy>/<mm>/<dd>/<timestamp>-<backup-type>-<release>-<checksum>
```

Ví dụ:

```text
production/postgresql/2026/07/24/20260724T180000Z-base-crm-1.0.0-<sha256>
production/postgresql/2026/07/24/20260724T180000Z-logical-crm-1.0.0-<sha256>.dump
production/rabbitmq/2026/07/24/20260724T180000Z-definitions.json
```

Không dùng:

```text
backup-final
backup-new
db-copy
latest.sql
```

---

# 12. Backup metadata manifest

Mỗi backup phải có manifest:

```json
{
  "backup_id": "uuid",
  "environment": "production",
  "component": "postgresql",
  "backup_type": "physical_base",
  "started_at": "2026-07-24T18:00:00Z",
  "completed_at": "2026-07-24T18:15:00Z",
  "source_cluster_id": "logical-reference",
  "database_version": "18.x",
  "application_release": "crm-bds-next-1.0.0",
  "alembic_revision": "revision-id",
  "size_bytes": 0,
  "sha256": "hex",
  "encrypted": true,
  "encryption_key_reference": "secret-reference",
  "retention_until": "2026-08-24T00:00:00Z",
  "verification_status": "VERIFIED",
  "verification_run_id": "uuid",
  "operator": "service-or-user-key"
}
```

Manifest không chứa secret.

---

# 13. Backup encryption

Backup phải:

- Mã hóa khi truyền.
- Mã hóa khi lưu.
- Dùng key từ managed key service.
- Có rotation.
- Có access audit.
- Không dùng password hard-coded.
- Không dùng cùng một key cho mọi environment nếu policy cấm.

Phải biết:

- Key nào mã hóa backup.
- Key có thể phục hồi không.
- Ai có quyền decrypt.
- Key rotation ảnh hưởng backup cũ thế nào.

---

# 14. Backup storage isolation

Bản backup phải:

- Nằm ngoài failure domain chính.
- Tách quyền với runtime app.
- Không cho application production xóa backup.
- Có immutable retention hoặc object lock khi phù hợp.
- Có versioning.
- Có access log.
- Có lifecycle policy.

Không lưu backup duy nhất cùng disk/cluster với nguồn.

---

# 15. Quyền truy cập backup

Principle:

```text
Backup operators may create backups without automatically receiving broad read access to business data.
```

Access model:

- Backup writer.
- Backup verifier.
- Restore operator.
- Security approver.
- Auditor.

Decrypt/restore production backup cần approval và audit.

---

# 16. PostgreSQL backup architecture

Production nên dùng một trong:

- Managed PostgreSQL automated backups + PITR.
- `pgBackRest`.
- `Barman`.
- Approved enterprise backup solution.

Không xây cron `pg_dump` đơn lẻ rồi coi là đủ production.

---

# 17. PostgreSQL pre-backup checks

Trước base/logical backup, kiểm tra:

```text
Database reachable
Replication/PITR status healthy
WAL archive healthy
Disk capacity healthy
No failed migration
No long-running blocking transaction
Backup destination reachable
Encryption key available
Clock synchronized
```

Ví dụ truy vấn kiểm tra:

```sql
SELECT version();
SELECT current_database();
SELECT current_setting('server_version');
SELECT pg_is_in_recovery();
SELECT now();
```

Kiểm tra Alembic revision qua application/migration command, không tự suy từ tên file.

---

# 18. PostgreSQL physical backup

## 18.1. Managed service

Sử dụng snapshot/base backup mechanism của provider.

Phải lưu:

- Snapshot ID.
- Start/end time.
- WAL/PITR range.
- Encryption key.
- Region/account.
- Verification.

## 18.2. Self-managed example

Công cụ cụ thể phải được khóa trong environment topology.

Không chạy lệnh mẫu trực tiếp khi chưa xác nhận config.

Ví dụ conceptual:

```bash
pgbackrest --stanza=crm_bds_ai --type=full backup
pgbackrest --stanza=crm_bds_ai info
pgbackrest --stanza=crm_bds_ai check
```

Không đưa credentials vào command line.

---

# 19. WAL archiving

WAL archive phải:

- Liên tục.
- Mã hóa.
- Có checksum.
- Có monitoring.
- Có retention phù hợp base backup.
- Không purge WAL cần cho backup còn hiệu lực.
- Có alert khi archive thất bại.

Critical alert:

```text
WAL archive delay > RPO threshold
```

---

# 20. PostgreSQL logical backup

Logical backup là lớp bảo vệ bổ sung.

Ví dụ:

```bash
pg_dump \
  --format=custom \
  --no-owner \
  --no-acl \
  --verbose \
  --file="<secure-path>/crm_bds_ai.dump" \
  "<connection-reference>"
```

Hoặc toàn cluster roles/globals:

```bash
pg_dumpall --globals-only > globals.sql
```

Lưu ý:

- Không đưa password vào lệnh.
- Không log connection string có secret.
- Logical dump lớn có thể không đáp ứng RTO.
- `--no-owner --no-acl` chỉ dùng nếu restore grants bằng IaC/migrations.
- Phải test extensions, schemas, sequences, constraints và large objects.

---

# 21. PostgreSQL backup scope

Backup phải bao gồm:

```text
All Context schemas
infra schema
Alembic version table
Audit schema
Outbox/Inbox
Idempotency records within retention
Integration mappings/cursors
Operations records
Database functions/triggers approved
Extensions required
Roles/grants definitions through separate controlled artifact
```

Không bỏ schema vì cho rằng “chỉ technical”.

---

# 22. PostgreSQL verification levels

## Level 1 — Artifact verification

- Backup exists.
- Size plausible.
- Checksum valid.
- Encryption valid.
- Manifest complete.

## Level 2 — Tool verification

- Backup tool integrity check.
- WAL chain valid.
- Required base backup present.

## Level 3 — Restore verification

- Restore to isolated environment.
- Start PostgreSQL.
- Run migrations/status checks.
- Run integrity queries.
- Run application smoke tests.

Chỉ Level 3 chứng minh restore thực tế.

---

# 23. Object Storage backup

Phải bảo vệ:

- Uploaded documents.
- Generated contracts.
- Receipts.
- Evidence packages.
- OCR sources/results nếu object-based.
- Export artifacts trong retention.
- Signature evidence.
- Audit evidence attachments.

---

# 24. Object Storage strategy

Khuyến nghị:

```text
Versioning
+ Cross-account or cross-region replication
+ Lifecycle retention
+ Inventory
+ Hash verification
+ Restricted restore
```

Không chỉ sync một chiều có thể propagate deletion ngay lập tức mà không version retention.

---

# 25. Object metadata backup

Database chứa:

```text
object_key
bucket_reference
sha256
size
mime_type
classification
scan_status
version_id
retention_class
```

Object Storage inventory phải đối chiếu với metadata này.

---

# 26. Object Storage verification

Hàng ngày hoặc định kỳ:

1. Generate inventory.
2. Sample object retrieval.
3. Verify checksum.
4. Verify versioning.
5. Verify encryption.
6. Verify no public ACL.
7. Verify replication lag.
8. Verify lifecycle policy.
9. Compare orphan/missing references.

---

# 27. Object restore modes

## Single object restore

Dùng khi một file bị xóa/corrupt.

## Prefix/resource restore

Dùng cho dossier/project/time window.

## Full bucket restore

Dùng cho regional/account failure.

## Version rollback

Dùng object versioning để lấy version trước.

Không restore object vào production key trước khi xác minh hash và authorization.

---

# 28. RabbitMQ backup

RabbitMQ là transport, không phải event archive.

Backup cần:

- Exchanges.
- Queues.
- Bindings.
- Policies.
- Users/permissions references.
- Virtual hosts.
- Definitions.
- Plugin configuration.

Ví dụ conceptual:

```bash
rabbitmqctl export_definitions /secure-path/rabbitmq-definitions.json
```

Không lưu password plaintext trong artifact.

---

# 29. RabbitMQ restore principle

Sau broker loss:

1. Recreate RabbitMQ infrastructure.
2. Restore definitions.
3. Restore permissions từ secret/IaC.
4. Start consumers.
5. Start Outbox publishers.
6. Republish pending/retry Outbox.
7. Use Inbox for duplicate safety.
8. Monitor lag/DLQ.

Không cố coi queue message snapshot là authoritative business history.

---

# 30. Valkey backup

Valkey chứa:

- Cache.
- Rate limit counters.
- Temporary locks.
- Ephemeral sessions nếu architecture.
- Short-lived job acceleration.

Baseline restore:

```text
Flush and rebuild
```

Chỉ backup data classes được phê duyệt.

Không restore:

- Stale authorization cache.
- Stale Commercial Lock truth.
- Stale numbering counter.
- Stale availability truth.

---

# 31. Application configuration backup

Backup:

- Environment templates không chứa secret.
- Feature flags.
- Workflow definitions.
- Approval policies.
- Numbering/Calendar config đã nằm DB.
- Deployment manifests.
- Queue names.
- Provider mapping references.
- Alert rules.
- Dashboard definitions nếu không nằm DB.

Git và artifact registry là nguồn chính cho code/IaC.

---

# 32. Secrets recovery

Secret manager phải có:

- Backup/replication.
- Version history.
- Recovery access.
- Rotation procedure.
- Audit.

Restore database không tự động restore secret values.

Sau compromise, phải rotate secret trước khi mở traffic.

---

# 33. Audit data backup

Audit backup phải:

- Theo PostgreSQL backup.
- Có integrity verification.
- Có retention dài hạn.
- Không editable.
- Có restricted access.
- Có restore check.

Sau restore:

- Verify row counts by time range.
- Verify seal/hash chain nếu triển khai.
- Verify latest sequence/checkpoint.
- Raise incident nếu mismatch.

---

# 34. Backup job observability

Metrics tối thiểu:

```text
backup_run_total
backup_run_failed_total
backup_duration_seconds
backup_size_bytes
backup_age_seconds
wal_archive_delay_seconds
object_replication_lag_seconds
backup_verification_failed_total
restore_drill_duration_seconds
restore_drill_failed_total
```

Labels low-cardinality:

- environment.
- component.
- backup_type.
- result.

Không label backup path có sensitive metadata nếu không cần.

---

# 35. Backup alerts

Critical:

- Không có successful backup trong window.
- WAL archive vượt RPO.
- Backup checksum fail.
- Encryption fail.
- Backup storage unavailable.
- Backup deletion/tampering.
- Restore verification fail.
- Object replication lag vượt threshold.
- Backup key unavailable.
- Retention policy disabled.

---

# 36. Daily backup checklist

```text
[ ] PostgreSQL base backup thành công
[ ] WAL archive current
[ ] Logical backup thành công nếu scheduled
[ ] Object Storage replication healthy
[ ] Object inventory generated
[ ] Backup manifests complete
[ ] Checksums valid
[ ] Encryption confirmed
[ ] No retention policy drift
[ ] RabbitMQ definitions current
[ ] Config artifacts current
[ ] Alerts clear
[ ] Verification sample passed
```

---

# 37. Weekly backup checklist

```text
[ ] Restore sample PostgreSQL logical backup
[ ] Restore sample object versions
[ ] Verify role/grants artifact
[ ] Verify Alembic revision
[ ] Verify audit integrity sample
[ ] Review backup growth
[ ] Review retention/deletion
[ ] Review access logs
[ ] Review failed/retried jobs
```

---

# 38. Monthly checklist

```text
[ ] Full isolated restore
[ ] Critical smoke tests
[ ] RPO measurement
[ ] RTO measurement
[ ] Object reconciliation
[ ] Outbox/Inbox behavior verification
[ ] Security access review
[ ] Key recovery check
[ ] Capacity review
[ ] Runbook drift review
```

---

# 39. Quarterly restore drill

Bắt buộc:

1. Chọn backup ngẫu nhiên trong retention.
2. Restore PostgreSQL.
3. Restore object subset/full according drill.
4. Recreate RabbitMQ.
5. Rebuild Valkey.
6. Deploy matching application release.
7. Run migration compatibility check.
8. Run critical journeys.
9. Measure RPO/RTO.
10. Produce report.
11. Open corrective actions.

Không dùng backup mới nhất cho mọi drill; phải kiểm tra backup cũ hợp lệ.

---

# 40. Restore authorization

Restore production cần:

- Incident ID hoặc Change ID.
- Incident Commander.
- Restore Lead.
- Security approval.
- Database/Storage operator.
- Business validation owner.
- Target time.
- Accepted data loss statement.
- Communication plan.

Không bắt đầu destructive restore chỉ qua chat message không record.

---

# 41. Restore decision tree

```text
Is production data corrupted?
├─ No → restore to isolated environment for inspection/extraction
└─ Yes
   ├─ Is corruption limited to one object?
   │  └─ Restore object version after validation
   ├─ Is corruption limited to derived projection?
   │  └─ Rebuild projection; do not restore primary DB
   ├─ Is corruption limited to specific business records?
   │  └─ Isolated restore + canonical repair/import process
   ├─ Is database unavailable but storage intact?
   │  └─ Full PostgreSQL restore/PITR
   └─ Is whole environment unavailable?
      └─ Disaster Recovery runbook
```

---

# 42. Restore modes

## Mode A — Isolated forensic restore

Mục tiêu:

- Điều tra.
- So sánh.
- Trích xuất.
- Không phục vụ users.

## Mode B — Component restore

Mục tiêu:

- Một object.
- RabbitMQ definitions.
- Configuration.
- Projection rebuild.

## Mode C — Full environment restore

Mục tiêu:

- Database + object storage + runtime.

## Mode D — Point-in-time restore

Mục tiêu:

- Quay về trước destructive/corrupting event.

## Mode E — Selective business recovery

Mục tiêu:

- Trích dữ liệu từ isolated restore.
- Apply qua canonical commands/data repair.
- Không overwrite toàn production.

---

# 43. Pre-restore checklist

```text
[ ] Incident/Change approved
[ ] Target environment confirmed
[ ] Restore point confirmed
[ ] Accepted RPO/data loss documented
[ ] Source backup verified
[ ] Encryption key accessible
[ ] Application release identified
[ ] Alembic revision identified
[ ] Object Storage state identified
[ ] Current production snapshot/checkpoint created
[ ] Writes stopped or isolated
[ ] Workers stopped
[ ] Traffic disabled
[ ] Communication sent
[ ] Verification plan ready
[ ] Rollback/fallback plan ready
```

---

# 44. Freeze writes

Trước restore production:

- Put application in maintenance/read-only mode.
- Stop API writes.
- Stop workers.
- Stop Outbox publisher.
- Stop integrations/webhook processing hoặc buffer safely.
- Stop schedulers.
- Preserve inbound requests if architecture supports.
- Record exact freeze time.

Không chỉ tắt frontend; backend/internal workers cũng phải dừng.

---

# 45. Capture current state before restore

Ngay cả khi production đang lỗi, tạo:

- Current DB snapshot nếu possible.
- Current object inventory.
- Current broker definitions.
- Current logs/metrics timeline.
- Current deployment version.
- Current secret versions references.

Mục đích:

- Forensics.
- Recover later records.
- Compare.
- Rollback restore attempt.

---

# 46. Full PostgreSQL restore — high-level

1. Provision isolated/new PostgreSQL cluster.
2. Match required engine/extensions.
3. Configure storage/encryption/network.
4. Restore base backup.
5. Replay WAL to target.
6. Stop recovery at target time.
7. Verify database starts.
8. Verify schemas/extensions.
9. Verify Alembic revision.
10. Verify data integrity.
11. Deploy compatible app.
12. Keep traffic disabled.
13. Run smoke/critical checks.
14. Promote/cut over.
15. Monitor.

Ưu tiên restore sang cluster mới thay vì overwrite in place.

---

# 47. Point-in-time restore

## 47.1. Xác định target time

Target time phải:

- Trước destructive event.
- Có timezone UTC.
- Có evidence từ audit/log.
- Có safety margin.
- Được business owner chấp nhận.

Ví dụ:

```text
Corrupting command: 2026-07-24T10:15:42Z
Target recovery time: 2026-07-24T10:15:30Z
```

## 47.2. Không dùng thời gian ước đoán mơ hồ

Không:

```text
Khoảng 10 giờ sáng
```

Phải dùng UTC exact time hoặc transaction/WAL marker nếu công cụ hỗ trợ.

---

# 48. PITR verification

Sau PITR:

- Corrupting transaction không tồn tại.
- Valid transactions trước target tồn tại.
- Alembic revision đúng.
- Outbox/Inbox state nhất quán.
- Audit timeline dừng tại target.
- Object references được đối chiếu.
- Latest business numbers hợp lệ.
- No sequence reuse.
- No duplicate locks/allocations.

---

# 49. Post-PITR data gap handling

Transactions sau target có thể mất khỏi restored DB.

Không tự replay từ logs.

Options:

- Recover from current failed snapshot.
- Reprocess external provider events.
- Replay approved inbound data.
- Apply canonical data repair.
- Contact business users.
- Document unrecoverable gap.

Mọi recovery sau PITR phải tránh duplicate.

---

# 50. Logical restore — isolated use

Ví dụ conceptual:

```bash
createdb crm_restore_validation
pg_restore \
  --clean \
  --if-exists \
  --no-owner \
  --no-acl \
  --dbname=crm_restore_validation \
  "<secure-path>/crm_bds_ai.dump"
```

Không chạy `--clean` vào production database.

Phải kiểm tra target connection trước lệnh destructive.

---

# 51. Restore safety guard

Mọi restore script phải yêu cầu:

```text
TARGET_ENVIRONMENT
TARGET_CLUSTER
BACKUP_ID
CONFIRMATION_TOKEN
```

Production cần confirmation mạnh:

```text
I_UNDERSTAND_THIS_WILL_REPLACE_PRODUCTION_DATA
```

Không dựa chỉ vào hostname màu terminal.

---

# 52. Schema and extension verification

Sau restore:

```sql
SELECT nspname
FROM pg_namespace
ORDER BY nspname;
```

Kiểm tra:

```text
infra
platform
iam
party
lead
product
matching
transaction
contract
revenue
activity
marketing
analytics
documents
audit
integration
operations
```

Kiểm tra extension cần thiết và không có object business trong `public`.

---

# 53. Alembic verification

Chạy canonical command:

```bash
uv run alembic current
uv run alembic heads
uv run alembic history
```

Expected:

- Current revision compatible with application release.
- Không multiple unintended heads.
- Không tự upgrade ngay nếu target app version chưa xác nhận.

---

# 54. Database integrity verification

Kiểm tra:

- Constraints valid.
- Indexes valid.
- No invalid index.
- No obvious corruption.
- Row counts plausible.
- Foreign references nội Context.
- Unique invariants.
- Exclusion invariants.
- Sequence/numbering integrity.
- Financial totals.
- Audit integrity.

---

# 55. Required domain integrity checks

## Platform

- Enterprise/Legal Entity status consistency.
- Calendar published version overlap.
- Numbering sequence/issuance consistency.

## Party

- Canonical Customer redirects.
- Unique phone identity.
- Merge lineage.

## Product

- Active Commercial Lock conflicts.
- Listing availability consistency.
- Ownership/mandate periods.

## Transaction

- Booking status and lock references.
- No duplicate confirmed booking conflicts.

## Contract

- Receipt immutability.
- Payment allocation totals.
- Receivable balances.
- Refund lineage.

## Revenue

- Entitlement/recognition/collection consistency.
- Commission payable/payout limits.

## Events

- Outbox status.
- Inbox processed state.
- No hash mismatch.

---

# 56. Financial reconciliation after restore

Phải chạy:

```text
Payment total
Allocation total
Unallocated total
Receivable outstanding
Receipt issued total
Refund total
Revenue entitlement
Revenue recognition
Revenue collection
Commission payable
Commission paid
Clawback balance
```

Bất kỳ mismatch nào phải block traffic cho financial workflows.

---

# 57. Business number verification

Sau PITR/restore:

- Issued numbers không bị reuse.
- Sequence current value >= highest issuance.
- Gaps được chấp nhận.
- Không reset sai period.
- Idempotency issuance records consistent.

Nếu uncertain, advance sequence; không tái sử dụng number.

---

# 58. Outbox recovery

Sau restore:

1. Inspect `PENDING`, `RETRY`, stale `PUBLISHING`.
2. Reset stale claims theo runbook.
3. Verify payload schema/hash.
4. Start consumers before publisher nếu appropriate.
5. Start publisher gradually.
6. Monitor duplicates/lag/DLQ.

Không mark Outbox `PUBLISHED` thủ công để giảm backlog.

---

# 59. Inbox recovery

- Preserve processed records.
- Reset stale `PROCESSING`.
- Do not delete Inbox to force replay.
- Use approved replay workflow.
- Verify handler versions.
- Monitor duplicate metric.

---

# 60. RabbitMQ restore procedure

High-level:

1. Provision broker.
2. Configure TLS.
3. Restore vhost/exchanges/queues/bindings/policies.
4. Restore users/permissions via secret/IaC.
5. Verify DLQ/retry topology.
6. Start consumers.
7. Verify health.
8. Start Outbox publisher.
9. Monitor queue depth and errors.

---

# 61. Valkey recovery procedure

1. Provision secure Valkey.
2. Apply config.
3. Do not load stale cache snapshot by default.
4. Start application with empty cache.
5. Warm selected safe reference caches.
6. Verify rate limiting behavior.
7. Verify no authorization fail-open.
8. Monitor memory/eviction.

---

# 62. Object Storage restore procedure

1. Identify required bucket/prefix/version.
2. Verify source backup/replica.
3. Verify encryption access.
4. Restore to isolated prefix/bucket first.
5. Verify hashes/metadata.
6. Reconcile DB references.
7. Copy/promote to target.
8. Verify access policies.
9. Verify no public ACL.
10. Run sample download/scan checks.

---

# 63. Single-object restore

Required inputs:

```text
document_id
object_key
expected_sha256
expected_version_id
classification
approved requester
```

Procedure:

1. Reauthorize request.
2. Retrieve previous version into quarantine.
3. Verify hash/MIME/size.
4. Malware scan if needed.
5. Compare metadata.
6. Restore object version.
7. Record Audit.
8. Verify document access.
9. Close recovery ticket.

---

# 64. Orphan object handling

Object exists, DB metadata missing:

- Do not auto-link.
- Quarantine or record finding.
- Identify source.
- Restore metadata only through canonical recovery process.
- Purge only after retention/review.

---

# 65. Missing object handling

DB metadata exists, object missing:

- Mark reconciliation finding.
- Attempt restore from version/replica/backup.
- Do not change document to CLEAN/AVAILABLE until restored.
- Block dependent workflow.
- Alert owner.

---

# 66. Application restore

Deploy exact compatible release first.

Do not deploy latest code blindly onto old restored schema.

Verification:

```text
Application release
Alembic revision
Feature flags
Workflow definitions
Permission registry
Error registry
Event schemas
```

---

# 67. Configuration restore

Restore:

- Feature flags.
- Runtime config references.
- Alert rules.
- Integration endpoints.
- Queue names.
- Scheduled jobs.

Validate environment-specific values.

Không copy production config sang UAT mà giữ production provider endpoints.

---

# 68. Secret restoration and rotation

Nếu restore do infrastructure failure, có thể reuse valid secrets theo policy.

Nếu restore do compromise:

- Rotate DB credentials.
- Rotate service tokens.
- Rotate webhook secrets.
- Rotate object storage credentials.
- Rotate signing keys if impacted.
- Revoke sessions.
- Reissue certificates if needed.

Không mở traffic trước security approval.

---

# 69. Traffic cutover

Trước cutover:

```text
[ ] Database healthy
[ ] Object Storage healthy
[ ] Broker healthy
[ ] Valkey healthy
[ ] Secrets valid
[ ] App deployed
[ ] Migrations compatible
[ ] Critical integrity checks pass
[ ] Smoke tests pass
[ ] Security checks pass
[ ] Monitoring active
[ ] Rollback path ready
```

Cutover nên:

- Cập nhật endpoint/DNS/load balancer.
- Giữ old environment isolated.
- Monitor error/latency/queue.
- Không xóa old environment ngay.

---

# 70. Post-restore smoke tests

Minimum:

1. Liveness/readiness.
2. Authentication.
3. Permission resolution.
4. Enterprise/Legal Entity read.
5. Customer scoped read.
6. Listing scoped read.
7. Safe draft write.
8. Outbox publish.
9. Consumer Inbox process.
10. Object download.
11. Dashboard basic query.
12. Audit event creation.
13. Job execution.
14. No public data leak.

---

# 71. Critical journey verification

Theo mức độ sự cố, chạy:

- Lead intake.
- Customer resolution.
- Commercial Lock.
- Booking confirmation in test data.
- Contract draft.
- Payment test flow.
- Receipt test flow không ảnh hưởng legal numbering production.
- Revenue projection.
- Commission projection.
- Document upload/download.
- Export.
- Reconciliation.

Production verification phải dùng dedicated test tenant/data và tránh tạo evidence pháp lý thật.

---

# 72. Security verification after restore

- Runtime roles least privilege.
- Public schema locked.
- TLS valid.
- Secrets not logged.
- Buckets private.
- Broker management restricted.
- CORS correct.
- OIDC issuer/audience correct.
- Break-glass disabled unless incident.
- Audit writer/readers correct.
- Backup artifacts still protected.

---

# 73. Performance verification

Sau restore:

- DB connection pool.
- Query latency.
- Index validity.
- Autovacuum/analyze.
- Cache warm-up.
- Queue lag.
- Object latency.
- CPU/memory/disk.

Có thể cần:

```sql
ANALYZE;
```

theo restore tool/provider guidance.

Không chạy VACUUM FULL tùy tiện.

---

# 74. Post-restore monitoring window

Hypercare tối thiểu:

```text
4–24 giờ tùy severity
```

Monitor:

- API errors.
- DB errors/deadlocks.
- Queue backlog.
- Outbox/Inbox.
- Object missing.
- Audit integrity.
- Financial anomalies.
- Authentication failures.
- Integration duplicates.
- Backup resumption.

---

# 75. Restore completion criteria

Restore chỉ hoàn thành khi:

1. Target RPO được đo.
2. Target RTO được đo.
3. Database integrity pass.
4. Object reconciliation pass.
5. Audit integrity pass.
6. Security pass.
7. Critical journeys pass.
8. Workers/events stable.
9. Stakeholders chấp nhận data gap.
10. Backup jobs hoạt động lại.
11. Incident/change record cập nhật.
12. Evidence lưu đầy đủ.

---

# 76. Restore rollback

Nếu restored environment fail verification:

- Không mở traffic.
- Quay về previous environment nếu safe.
- Restore từ backup khác.
- Chọn target time khác.
- Escalate Incident.
- Preserve failed restore for investigation.

Không sửa dữ liệu tùy tiện để “làm cho pass”.

---

# 77. Selective data recovery

Không restore một table trực tiếp vào production.

Safe process:

1. Restore full backup vào isolated environment.
2. Identify records.
3. Validate ownership/lineage.
4. Export safe structured data.
5. Review.
6. Apply through canonical command/import/data-repair tool.
7. Audit.
8. Reconcile.
9. Test no duplicates.

---

# 78. Customer-specific recovery

Khôi phục Customer/Lead riêng lẻ có rủi ro:

- Duplicate identity.
- Merge redirect.
- Cross-context references.
- Scope/access.
- Timeline.
- Documents.
- Deals/contracts.

Phải dùng Customer recovery plan, không copy rows đơn lẻ.

---

# 79. Financial record recovery

Không insert/update trực tiếp:

- Payment.
- Allocation.
- Receipt.
- Refund.
- Revenue Recognition.
- Commission Payout.

Financial recovery cần:

- Finance owner.
- Audit.
- Reversal/adjustment/canonical repair.
- Reconciliation.
- SoD approval.

---

# 80. Audit record recovery

Audit record mất/corrupt là security incident.

Không recreate Audit bằng suy đoán mà không đánh dấu recovery evidence.

Phải:

- Preserve source evidence.
- Restore from backup.
- Verify integrity.
- Document gap.
- Escalate compliance.

---

# 81. Restore drill environment

Drill environment phải:

- Network isolated.
- No production provider delivery.
- No outbound email/SMS/webhooks.
- Separate OIDC client.
- Separate object bucket/prefix.
- Separate RabbitMQ vhost.
- Separate Valkey namespace.
- Restricted access.
- Automatic cleanup after retention.

---

# 82. Non-production restore from production backup

Chỉ được khi:

- Approved.
- Access controls tương đương.
- Egress blocked.
- Data anonymized hoặc necessity documented.
- Provider calls disabled.
- User sessions invalidated.
- Secrets replaced.
- Retention short.
- Cleanup verified.

---

# 83. Anonymization after restore

Non-production anonymization phải xử lý:

- Names.
- Phone.
- Email.
- Addresses.
- Identity numbers.
- Bank references.
- Documents.
- Free text.
- Audit actor references.
- File contents.
- Search indexes/caches.

Không chỉ mask database fields trong khi object files vẫn còn PII.

---

# 84. Backup compromise response

Nếu backup bị nghi truy cập trái phép:

1. Declare security incident.
2. Freeze deletion/rotation evidence.
3. Identify backup IDs.
4. Identify encryption key exposure.
5. Revoke credentials.
6. Rotate keys/secrets.
7. Assess data classification.
8. Review access logs.
9. Legal/privacy escalation.
10. Validate backup integrity.
11. Create clean backup chain.
12. Document affected retention.

---

# 85. Backup corruption response

Nếu checksum/restore fail:

- Mark backup `INVALID`.
- Prevent automatic selection.
- Alert.
- Test adjacent backups.
- Verify WAL chain.
- Create new backup.
- Assess RPO risk.
- Open incident if coverage gap.
- Do not delete corrupt artifact before investigation.

---

# 86. Missed backup response

Nếu missed backup vượt threshold:

1. Alert on-call.
2. Determine cause.
3. Create immediate backup if safe.
4. Verify WAL/object replication.
5. Calculate current RPO exposure.
6. Notify stakeholders if SLO breached.
7. Fix root cause.
8. Perform restore verification.
9. Record incident/problem.

---

# 87. Capacity management

Backup storage planning phải tính:

- Database growth.
- WAL volume.
- Object growth.
- Retention.
- Replication.
- Encryption overhead.
- Restore workspace.
- Temporary extraction.
- Drill environment.

Cần ít nhất đủ capacity để restore without deleting valid backups.

---

# 88. Retention policy

Retention phải cân bằng:

- Legal.
- Audit.
- Privacy.
- RPO/PITR.
- Cost.
- Incident forensics.
- Release support.

Không giữ backup vô thời hạn mặc định.

Không xóa backup đang legal hold hoặc incident hold.

---

# 89. Backup deletion

Backup deletion phải:

- Theo lifecycle policy.
- Respect retention/legal hold.
- Auditable.
- Không do runtime app.
- Có protection against mass deletion.
- Có alert khi manual deletion.

---

# 90. Backup immutability

Critical backups nên dùng:

- Object Lock.
- WORM.
- Immutable snapshots.
- Separate account/project.

Operator có quyền restore không nhất thiết có quyền xóa immutable backup.

---

# 91. Backup test automation

Automated verification pipeline:

1. Select backup.
2. Provision ephemeral environment.
3. Restore.
4. Verify checksum.
5. Start services.
6. Run schema/integrity tests.
7. Run smoke tests.
8. Generate report.
9. Destroy environment.
10. Alert on failure.

Automation không thay quarterly human-led drill.

---

# 92. Verification query catalog

Phải có scripts versioned:

```text
scripts/operations/backup/verify_backup_manifest.py
scripts/operations/restore/verify_schema.py
scripts/operations/restore/verify_domain_integrity.py
scripts/operations/restore/verify_financial_integrity.py
scripts/operations/restore/verify_object_references.py
scripts/operations/restore/verify_audit_integrity.py
scripts/operations/restore/run_smoke_tests.py
```

Scripts không chứa secret.

---

# 93. Restore tooling safety

Tooling phải:

- Dry-run.
- Target allowlist.
- Environment banner.
- Confirmation.
- Audit logs.
- Structured output.
- Non-zero exit on failure.
- No implicit production default.
- No destructive wildcard.

Default target phải là `NONE`, không phải production.

---

# 94. Evidence package

Mỗi restore/drill tạo package:

```text
restore-request.md
backup-manifest.json
restore-plan.md
command-transcript-sanitized.txt
verification-results.json
rpo-rto-report.md
integrity-report.md
security-report.md
issues-and-actions.md
approval-record.md
```

Không lưu secret trong transcript.

---

# 95. Restore report template

```markdown
# Restore Report

## Identification

- Restore Run ID:
- Incident/Change ID:
- Environment:
- Backup ID:
- Target recovery time:
- Application release:
- Alembic revision:

## Timeline

## Reason

## Accepted Data Loss

## Restore Steps

## PostgreSQL Verification

## Object Storage Verification

## RabbitMQ Verification

## Valkey Verification

## Security Verification

## Audit Verification

## Financial Reconciliation

## Smoke Tests

## Critical Journeys

## RPO Result

## RTO Result

## Issues

## Corrective Actions

## Final Decision

## Approvals
```

---

# 96. Communication templates

## Backup failure

```text
Backup verification failed for <component> in <environment>.
Current recovery coverage is under investigation.
Incident: <id>
No action is required from business users unless separately notified.
```

## Restore started

```text
A controlled restore has started for <environment>.
Write traffic is paused.
Target recovery point: <UTC timestamp>.
Incident/Change: <id>.
```

## Restore completed

```text
Restore verification completed.
Measured RPO: <duration>.
Measured RTO: <duration>.
Known data gap: <summary>.
Service status: <status>.
```

---

# 97. Runbook commands policy

Mọi command trong incident phải:

- Được paste vào incident log trước hoặc sau execution.
- Sanitize secret.
- Ghi operator.
- Ghi timestamp.
- Ghi result.
- Không copy production token.

Không chạy lệnh destructive từ memory nếu runbook có command wrapper.

---

# 98. Manual verification checklist

```text
[ ] Correct environment
[ ] Correct backup ID
[ ] Correct recovery time
[ ] Correct application release
[ ] Correct schema revision
[ ] Correct encryption key
[ ] Correct object bucket
[ ] Correct broker vhost
[ ] Correct OIDC config
[ ] External providers disabled during validation
[ ] No production user traffic
```

---

# 99. Common failure modes

## Backup job reports success but artifact empty

Action:

- Mark invalid.
- Investigate permissions/storage.
- Create new backup.
- Test restore.

## WAL archive gap

Action:

- Assess PITR window.
- Create new base backup.
- Alert RPO breach.
- Do not purge previous valid chain.

## Restore starts but database cannot open

Check:

- PostgreSQL version.
- Extensions.
- WAL completeness.
- Encryption.
- File ownership.
- Recovery config.

## App starts but errors on schema

Check:

- Alembic revision.
- Release compatibility.
- Environment variables.
- Search path.
- Extensions.

## Documents missing

Run object reconciliation.

## Queue duplicates increase

Check Inbox and restored broker state.

## Financial totals mismatch

Keep financial flows disabled and escalate.

---

# 100. Troubleshooting — checksum mismatch

1. Verify transfer completed.
2. Verify checksum algorithm.
3. Compare source/destination.
4. Check encryption/decryption layer.
5. Re-download from independent copy.
6. Mark artifact invalid if mismatch persists.
7. Do not restore.

---

# 101. Troubleshooting — restore too slow

Check:

- Storage throughput.
- Network.
- Compression.
- Parallel restore options.
- Index creation.
- WAL replay speed.
- Resource limits.
- Provider quota.

Không bỏ verification để đạt RTO.

---

# 102. Troubleshooting — object replication lag

- Determine affected time range.
- Use primary version history if intact.
- Delay cutover or restore missing objects separately.
- Mark documents unavailable until complete.
- Measure actual RPO for object data.

---

# 103. Troubleshooting — stale Outbox after restore

- Identify claimed rows.
- Verify publisher instances stopped.
- Reset only via approved command.
- Preserve attempts/errors.
- Restart gradually.
- Monitor duplicates.

---

# 104. Troubleshooting — Idempotency after PITR

PITR có thể loại bỏ idempotency record nhưng external client may retry old command.

Mitigations:

- Provider idempotency.
- Business unique constraints.
- Restore/extract idempotency rows if safe.
- Temporary reconciliation window.
- Monitor duplicate conflicts.

Không assume old requests will not retry.

---

# 105. Troubleshooting — external provider state ahead of DB

Examples:

- Provider accepted payment/signature.
- Restored DB is before callback.

Action:

1. Query provider.
2. Persist recovery case.
3. Process through canonical reconciliation.
4. Deduplicate provider reference.
5. Audit.
6. Do not resend irreversible request.

---

# 106. Backup and release coordination

Trước destructive/high-risk migration:

- Create verified backup.
- Verify PITR.
- Record backup ID.
- Confirm restore compatibility.
- Prepare rollback/forward fix.
- Keep old application artifact.

Sau release:

- Create new backup.
- Verify Alembic revision.
- Update manifest.
- Test restore in next scheduled cycle.

---

# 107. Backup before data import

Large import requires:

- Pre-import backup/checkpoint.
- Import run ID.
- Staging.
- Dry run.
- Post-import reconciliation.
- Rollback strategy.

Không dùng full DB restore để sửa lỗi import nếu canonical compensation đủ an toàn.

---

# 108. Backup before data repair

Data repair requires:

- Current snapshot.
- Target rows.
- Script hash.
- Dry run.
- Approval.
- Post-repair backup.
- Verification.

---

# 109. Legal and privacy considerations

Backup chứa dữ liệu cá nhân phải:

- Tuân retention.
- Tuân legal hold.
- Không dùng ngoài mục đích recovery.
- Có access log.
- Có secure deletion.
- Có breach response.

Data subject deletion có thể không xóa ngay immutable backup nếu policy/legal cho phép, nhưng restore procedure phải reapply deletion/anonymization tombstones trước reopening.

---

# 110. Reapply post-backup deletions

Sau restore backup cũ:

- Reapply legal deletion/anonymization ledger.
- Reapply consent withdrawal/suppression.
- Reapply revoked access.
- Reapply compromised credential revocations.
- Reapply legal holds.

Không mở traffic trước khi các security/privacy deltas được áp dụng.

---

# 111. Access and permission restoration

Sau restore:

- Verify active users.
- Verify revoked users.
- Verify role assignments.
- Verify delegations expiry.
- Verify break-glass expiry.
- Verify service credentials.
- Verify access-review decisions after backup timestamp.

PITR có thể khôi phục quyền đã bị thu hồi; phải reapply revocation ledger.

---

# 112. Feature flag restoration

Feature flags sau restore phải được so sánh với current approved state.

Không vô tình bật feature deprecated hoặc chưa production-ready chỉ vì backup cũ.

---

# 113. Integration cursor restoration

PITR có thể làm cursor lùi.

Nguy cơ:

- Re-import duplicate.
- Re-send outbound data.
- Reprocess webhook.

Phải:

- Use provider IDs/idempotency.
- Reconcile cursor.
- Start integrations in paused mode.
- Resume one by one.

---

# 114. Scheduler restoration

Sau restore:

- Disable all schedulers initially.
- Inspect missed jobs.
- Classify catch-up safe/unsafe.
- Re-enable in controlled order.
- Avoid duplicate billing/notification/import.

---

# 115. Notification restoration

Không tự resend notifications từ restored queue.

Notification consumer phải:

- Use Inbox.
- Check delivery record.
- Check current resource/recipient permission.
- Respect suppression/consent.
- Skip expired notifications.

---

# 116. Export artifacts

Expired exports không cần restore trừ audit/legal requirement.

Do not restore old signed URLs.

Regenerate authorized exports if needed.

---

# 117. Search and analytics rebuild

Derived systems should be rebuilt from source:

- Search index.
- Analytics projections.
- Timeline projections.
- Cached dashboards.

Mark stale until rebuild/reconciliation complete.

---

# 118. Restore order

Recommended order:

```text
Infrastructure
→ PostgreSQL
→ Object Storage
→ Secrets/Configuration
→ RabbitMQ
→ Valkey
→ Application API
→ Consumers
→ Outbox Publisher
→ Schedulers
→ Integrations
→ Frontend Traffic
```

Order có thể thay đổi theo incident nhưng phải documented.

---

# 119. Start-up order rationale

- Source of truth trước.
- Durable storage trước consumers.
- Consumers trước Outbox publisher để tránh backlog spike.
- Integrations cuối để tránh external side effects.
- Traffic cuối sau verification.

---

# 120. Stop order

Recommended:

```text
Traffic
→ Schedulers
→ Integrations
→ Outbox Publisher
→ Consumers
→ API
→ Valkey/RabbitMQ
→ Database/Object Storage
```

Phải drain hoặc persist inbound work.

---

# 121. Restore drill scenarios

## Scenario 1

Accidental table data corruption, PITR.

## Scenario 2

Full PostgreSQL cluster loss.

## Scenario 3

Object Storage object deletion.

## Scenario 4

Region/account outage.

## Scenario 5

Backup encryption key recovery.

## Scenario 6

RabbitMQ total loss.

## Scenario 7

Compromised credentials and restore.

## Scenario 8

Bad migration rollback/forward recovery.

## Scenario 9

Provider state ahead of restored DB.

## Scenario 10

Audit integrity failure.

---

# 122. Drill success criteria

- Restore completes.
- RPO/RTO measured.
- No data corruption.
- Security controls restored.
- Critical journeys pass.
- Backup chain validated.
- Corrective actions assigned.
- Runbook updated.

---

# 123. Drill failure criteria

- Cannot decrypt.
- Cannot locate backup.
- WAL gap.
- Restore exceeds hard limit without plan.
- Object metadata mismatch unresolved.
- Security roles wrong.
- Audit integrity fail.
- Financial reconciliation fail.
- Operators lack access.
- Commands undocumented.
- External provider side effects occur.

---

# 124. Training requirements

Operators phải được đào tạo:

- Backup architecture.
- PostgreSQL PITR.
- Object versioning.
- Broker rebuild.
- Security.
- Incident command.
- Evidence handling.
- Verification scripts.
- Selective recovery constraints.

Không để một người duy nhất biết restore.

---

# 125. Access readiness test

Hàng quý kiểm tra:

- Restore account works.
- MFA works.
- Secret recovery works.
- Encryption key accessible.
- Backup storage reachable.
- Runbook accessible offline.
- Required tools available.
- Contact list current.

Không thực hiện decryption production data nếu drill không yêu cầu.

---

# 126. Offline runbook availability

Runbook và critical contacts phải có secure offline copy.

Không phụ thuộc hoàn toàn vào cùng hệ thống đang bị sự cố.

---

# 127. Tool version pinning

Restore tools phải tương thích:

- PostgreSQL.
- pgBackRest/Barman/provider.
- Encryption tools.
- Object CLI.
- RabbitMQ.

Tool versions được ghi trong environment/toolchain docs.

---

# 128. Change management

Mọi thay đổi backup topology cần:

- Design review.
- Security review.
- Cost/capacity review.
- Migration plan.
- Dual-run period.
- Restore test.
- Runbook update.
- Approval.

Không tắt hệ thống cũ trước khi restore mới pass.

---

# 129. Backup provider migration

Khi đổi provider/tool:

1. Inventory current backups.
2. Define retention obligations.
3. Enable new backups.
4. Run parallel.
5. Restore test new.
6. Confirm RPO/RTO.
7. Preserve old backups until expiry.
8. Decommission old safely.

---

# 130. Metrics and SLO reporting

Monthly report:

- Backup success rate.
- Verification success rate.
- Oldest valid backup.
- PITR coverage.
- Restore drill result.
- Measured RPO/RTO.
- Storage growth.
- Failed alerts.
- Outstanding corrective actions.

---

# 131. Definition of Ready cho backup setup

Backup setup Ready khi:

1. Inventory complete.
2. Owners assigned.
3. RPO/RTO defined.
4. Storage selected.
5. Encryption selected.
6. Retention defined.
7. Access model defined.
8. Monitoring designed.
9. Restore plan designed.
10. Security reviewed.
11. Capacity funded.

---

# 132. Definition of Done cho backup setup

Backup setup Done khi:

1. Automated jobs active.
2. WAL/PITR active.
3. Object protection active.
4. Encryption verified.
5. Offsite copy active.
6. Alerts active.
7. Manifests generated.
8. Restore test pass.
9. RPO/RTO measured.
10. Runbook approved.
11. Operators trained.
12. Evidence stored.

---

# 133. Definition of Done cho restore

Restore Done khi:

1. Approved request.
2. Verified backup.
3. Restore completed.
4. Database integrity pass.
5. Object reconciliation pass.
6. Audit pass.
7. Financial reconciliation pass.
8. Security pass.
9. Smoke/E2E pass.
10. Traffic restored.
11. Backup resumed.
12. Hypercare complete.
13. Report approved.
14. Corrective actions tracked.

---

# 134. AI Agent protocol

AI Agent hỗ trợ backup/restore phải:

1. Xác định environment.
2. Không assume production.
3. Không tự chạy destructive command.
4. Không yêu cầu secret trong chat/log.
5. Dùng placeholders.
6. Xác định backup ID/recovery point.
7. Đề xuất isolated restore trước.
8. Bảo vệ object/audit/financial integrity.
9. Yêu cầu verification.
10. Ghi rõ commands chưa chạy.
11. Không tạo fake evidence.
12. Không tuyên bố restore thành công nếu chưa có kết quả thật.

---

# 135. AI Agent prohibited behaviors

AI Agent không được:

1. Chạy `DROP DATABASE` không approval.
2. Restore đè production trực tiếp.
3. Dùng backup chưa verify.
4. Bỏ current-state snapshot.
5. Ghi secret vào command.
6. Dùng production backup trong dev tùy tiện.
7. Bỏ object storage.
8. Xóa Inbox để replay.
9. Mark Outbox published thủ công.
10. Insert financial rows trực tiếp.
11. Reuse business number.
12. Bỏ privacy revocations sau PITR.
13. Bật integrations trước verification.
14. Báo RPO/RTO đạt khi chưa đo.
15. Bịa kết quả command.

---

# 136. Anti-patterns bị cấm

1. Chỉ dùng `pg_dump` làm production strategy.
2. Backup cùng disk với database.
3. Không mã hóa.
4. Runtime app có quyền xóa backup.
5. Không PITR.
6. Không object versioning/replication.
7. Không restore drill.
8. Chỉ kiểm tra file tồn tại.
9. Không lưu manifest/checksum.
10. Restore latest code lên old schema.
11. Overwrite production in-place đầu tiên.
12. Restore stale cache.
13. Restore RabbitMQ như business SoT.
14. Không reapply revoked access/privacy actions.
15. Không reconcile provider state.
16. Không financial reconciliation.
17. Dùng ad-hoc SQL selective restore.
18. Không ghi evidence.
19. Shared restore credentials.
20. Backup không retention/immutability.

---

# 137. Quick reference — backup failure

```text
1. Alert on-call
2. Confirm failure
3. Preserve logs
4. Check previous valid recovery point
5. Create immediate backup if safe
6. Calculate RPO exposure
7. Open incident if threshold breached
8. Repair
9. Restore-verify
10. Document
```

---

# 138. Quick reference — production restore

```text
1. Declare incident/change
2. Freeze writes
3. Capture current state
4. Verify backup
5. Provision new target
6. Restore DB/PITR
7. Restore objects/config
8. Recreate broker/cache
9. Deploy compatible app
10. Reconcile
11. Verify security/financial/audit
12. Smoke/E2E
13. Cut over
14. Hypercare
15. Report
```

---

# 139. Quick reference — single document

```text
1. Approve
2. Identify object/version/hash
3. Restore into quarantine
4. Verify hash/MIME/scan
5. Restore target version
6. Reconcile metadata
7. Audit
8. Validate access
```

---

# 140. Required runbook files

```text
docs/runbooks/backup-and-restore.md
docs/runbooks/disaster-recovery.md
docs/runbooks/database-failure.md
docs/runbooks/object-storage-failure.md
docs/runbooks/rabbitmq-failure.md
docs/runbooks/outbox-backlog.md
docs/runbooks/event-dlq.md
docs/runbooks/data-repair.md
docs/runbooks/security-incident-response.md
```

---

# 141. Change Log

## Version 1.0.0 — 2026-07-24

- Thiết lập backup inventory.
- Thiết lập baseline RPO/RTO.
- Khóa PostgreSQL physical/logical/PITR strategy.
- Khóa Object Storage protection và reconciliation.
- Khóa RabbitMQ/Valkey recovery behavior.
- Khóa encryption, retention, isolation và access.
- Khóa restore modes, decision tree và prechecks.
- Khóa full restore, PITR và selective recovery.
- Khóa financial, audit, event và privacy verification.
- Khóa restore drill, evidence và reporting.
- Khóa AI Agent protocol và prohibited behaviors.

---

# 142. Kết luận

Backup và Restore của `crm_bds_ai` phải tạo ra khả năng phục hồi có thể chứng minh, không phải cảm giác an toàn.

Công thức bắt buộc:

```text
Automated Backup
+ Continuous Recovery Coverage
+ Encryption
+ Independent Storage
+ Integrity Verification
+ Isolated Restore Testing
+ Domain Reconciliation
+ Security Validation
+ Measured RPO/RTO
```

Nguyên tắc cuối cùng:

> Không có bản backup nào được coi là hợp lệ cho đến khi nó được khôi phục thành công, vượt qua kiểm tra dữ liệu, bảo mật, nghiệp vụ và có bằng chứng rõ ràng.
