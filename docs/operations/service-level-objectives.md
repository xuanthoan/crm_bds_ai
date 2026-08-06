# CRM_BDS_AI — SERVICE LEVEL OBJECTIVES

**Document ID:** `OPS-SLO-001`  
**Canonical path:** `docs/operations/service-level-objectives.md`  
**Product:** `crm_bds_ai`  
**Version:** `1.0.0`  
**Status:** `Ready for Review`  
**Owner:** `Operations Owner`  
**Reviewers:** `Architecture Owner, Product Owner, QA Owner`  
**Last reviewed:** `2026-08-05`  
**Classification:** `INTERNAL`


Exact numeric targets phải được validate bằng load/capacity tests trước production. SLI bắt buộc: API success/latency, queue lag, outbox age, inbox failures, provider delivery, job success, data freshness, backup age và restore validation.

SLO breach tạo Alert/Incident theo severity; không tự sửa business data.
