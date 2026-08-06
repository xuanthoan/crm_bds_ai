# CRM_BDS_AI — RUNBOOK — EXTERNAL PROVIDER OUTAGE

**Document ID:** `RUN-PROVIDER-001`  
**Canonical path:** `docs/runbooks/provider-outage.md`  
**Product:** `crm_bds_ai`  
**Version:** `1.0.0`  
**Status:** `Ready for Review / Foundation Baseline`  
**Owner:** `Integration Owner`  
**Effective date:** `2026-08-05`  
**Last reviewed:** `2026-08-05`  
**Classification:** `INTERNAL`

---

# Scope

Email/SMS/Zalo, telephony, signature, bank/payment, ERP, ad platform, object storage provider or identity provider.

# Steps

1. Confirm provider and affected connections.
2. Stop unsafe retries/circuit-break if needed.
3. Preserve idempotency and payload references.
4. Degrade user workflow with explicit status; do not fake success.
5. Notify internal owners.
6. Resume/replay under controlled batch.
7. Reconcile provider and business state.
8. Close incident with timeline and preventive actions.
