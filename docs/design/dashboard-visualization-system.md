# CRM_BDS_AI — DASHBOARD VISUALIZATION SYSTEM

**Document ID:** `DES-DAS-001`  
**Canonical path:** `docs/design/dashboard-visualization-system.md`  
**Product:** `crm_bds_ai`  
**Version:** `1.0.0`  
**Status:** `Ready for Review`  
**Owner:** `Analytics Design Owner`  
**Reviewers:** `Analytics Owner, Product Design Owner, Accessibility Owner`  
**Last reviewed:** `2026-08-05`  
**Classification:** `INTERNAL`


# Rules

- Widget tham chiếu Semantic Metric Version; không nhúng official formula.
- Hiển thị data cutoff, freshness, scope và filters.
- Forecast, Target, Actual và Restatement có visual distinction.
- Color không là tín hiệu duy nhất.
- Drill-down permission tách aggregate/detail/export.

# Chart guidance

- KPI card: single governed metric.
- Line: trend/time-series.
- Bar: category comparison.
- Funnel: ordered lifecycle với explicit cohort/period.
- Table: precise operational details.
- Avoid pie khi nhiều categories hoặc so sánh nhỏ.

# Financial labeling

Contract Value, Buyer Payment, Revenue, Collected Revenue, Commission Payable và Paid phải ghi rõ basis.
