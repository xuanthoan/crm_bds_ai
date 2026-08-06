# CRM_BDS_AI — OBSERVABILITY ARCHITECTURE

**Document ID:** `ARCH-OBS-001`  
**Canonical path:** `docs/architecture/observability-architecture.md`  
**Product:** `crm_bds_ai`  
**Version:** `1.0.0`  
**Status:** `Ready for Review / Foundation Baseline`  
**Owner:** `Operations Owner`  
**Effective date:** `2026-08-05`  
**Last reviewed:** `2026-08-05`  
**Classification:** `INTERNAL`

---

# 1. Signals

- Structured logs.
- Metrics.
- Distributed traces.
- Health/readiness.
- Business process telemetry.
- Audit facts tách khỏi operational telemetry.

# 2. Correlation

Request ID, Correlation ID, Causation ID, trace context, job ID, Event ID và aggregate reference phải truyền qua API, Outbox, broker, Inbox và worker.

# 3. Redaction

Không ghi secrets, raw tokens, full phone, identity numbers, bank accounts, signed documents hoặc restricted payload.

# 4. Minimum dashboards

API health/latency/error, worker/broker, database, cache, outbox/inbox lag, provider delivery, object storage, data quality, backup/restore, incident/release.

# 5. Alerting

Alert phải actionable, có owner, severity, runbook, deduplication và escalation. Alert không đồng nghĩa Audit hoặc Customer Interaction.
