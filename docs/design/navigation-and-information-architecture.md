# CRM_BDS_AI — NAVIGATION AND INFORMATION ARCHITECTURE

**Document ID:** `DES-NAV-001`  
**Canonical path:** `docs/design/navigation-and-information-architecture.md`  
**Product:** `crm_bds_ai`  
**Version:** `1.0.0`  
**Status:** `Ready for Review`  
**Owner:** `Product Design Owner`  
**Reviewers:** `Product Owner, Frontend Owner, Accessibility Owner`  
**Last reviewed:** `2026-08-05`  
**Classification:** `INTERNAL`


# Primary work areas

- Home/My Work.
- Leads.
- Customers.
- Products/Inventory.
- Matching.
- Deals/Transactions.
- Contracts/Cash.
- Revenue/Commission.
- Marketing.
- Analytics.
- Documents.
- Administration/Operations theo quyền.

# Rules

- Navigation visibility không thay backend authorization.
- Resource workspace dùng Overview, Activity, Documents, Related, Audit tabs theo quyền.
- Deep link phải re-authorize.
- Breadcrumb phản ánh business hierarchy, không database hierarchy.
- Global search trả masked, scope-filtered results.

# Role landing

Sale → My Work/Leads; Team Lead → Team Work/Pipeline; Finance → Receivables/Payments; Director → Executive Analytics; Operations → Health/Incidents.
