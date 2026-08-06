# CRM_BDS_AI — FRONTEND STANDARDS

## Quy chuẩn frontend bắt buộc cho toàn bộ hệ thống `crm_bds_ai`

**Document ID:** `ENG-FE-001`  
**Canonical path:** `docs/engineering/frontend-standards.md`  
**Product:** `crm_bds_ai`  
**Version:** `1.0.0`  
**Status:** `Accepted / Mandatory`  
**Canonical:** `Yes` đối với kiến trúc, coding conventions, UI behavior, accessibility, security, performance và kiểm thử frontend  
**Owner:** `Frontend Architecture Owner`  
**Reviewers:** `Architecture Owner`, `Technical Owner`, `Design System Owner`, `Security Owner`, `QA Owner`, `API Owner`, `Context Owners`, `Product Owner`  
**Effective date:** `2026-08-05`  
**Last reviewed:** `2026-08-05`  
**Next review:** Khi Next.js, React, TypeScript, Design System, API client, browser support hoặc frontend architecture thay đổi  
**Supersedes:** `None — Greenfield baseline`  
**Superseded by:** Không

---

# 1. Mục đích

Tài liệu này quy định cách thiết kế, tổ chức, triển khai, kiểm thử, tối ưu và vận hành toàn bộ frontend của `crm_bds_ai`.

Mục tiêu:

1. Bảo đảm frontend phản ánh đúng domain và state machine.
2. Bảo đảm frontend không trở thành source of truth.
3. Bảo đảm authorization vẫn được enforce ở backend.
4. Bảo đảm UI nhất quán giữa 14 module và 16 Bounded Context.
5. Bảo đảm mọi màn hình có loading, empty, error, conflict và permission states.
6. Bảo đảm frontend hỗ trợ dữ liệu lớn, bảng phức tạp và workflow nghiệp vụ dài.
7. Bảo đảm accessibility, responsive behavior và localization.
8. Bảo đảm API types được generate từ OpenAPI.
9. Bảo đảm frontend không tự tính KPI chính thức hoặc financial truth.
10. Bảo đảm AI Agent có thể tiếp tục xây dựng mà không tự tạo kiến trúc hoặc style riêng.

Tài liệu này phải được đọc cùng:

```text
docs/engineering/coding-standards.md
docs/engineering/api-standards.md
docs/engineering/testing-standards.md
docs/engineering/security-standards.md
docs/design/design-system.md
docs/design/design-tokens.md
docs/design/navigation-and-information-architecture.md
docs/design/dashboard-visualization-system.md
docs/security/permission-registry.md
docs/security/field-masking-matrix.md
Relevant Context Implementation Pack
Current Sprint Execution Pack
```

---

# 2. Nguyên tắc tối cao

```text
Correct Domain Representation
> Accessibility
> Security
> Consistency
> Reliability
> Performance
> Visual Polish
> Developer Convenience
```

Frontend đẹp nhưng hiển thị sai trạng thái, sai quyền hoặc sai số liệu là không chấp nhận được.

---

# 3. Frontend technology baseline

Technology versions theo Technology Toolchain Lock.

Baseline:

```text
Next.js 16.x
React 19.x
TypeScript 6.x
TanStack Query
TanStack Table
React Hook Form
Zod
Tailwind CSS
Radix UI
Recharts cho Dashboard được phê duyệt
Playwright
Vitest hoặc test runner được khóa
Testing Library
MSW
```

Không thêm:

- Redux.
- MobX.
- Zustand.
- Formik.
- Axios.
- Chart library khác.
- Component library khác.

nếu chưa có ADR/approval.

---

# 4. Frontend architecture principles

Frontend được tổ chức theo:

```text
Application Shell
+ Route Segments
+ Feature Modules
+ Shared Design System
+ Generated API Client
+ Shared Infrastructure
```

Frontend không được tổ chức chỉ theo loại file toàn cục như:

```text
components/
pages/
services/
utils/
```

mà thiếu feature ownership.

---

# 5. Recommended repository structure

```text
apps/web/
├── app/
│   ├── (auth)/
│   ├── (app)/
│   ├── (admin)/
│   ├── api/
│   ├── error.tsx
│   ├── global-error.tsx
│   ├── layout.tsx
│   ├── loading.tsx
│   └── not-found.tsx
│
├── components/
│   ├── app-shell/
│   ├── navigation/
│   ├── feedback/
│   └── layout/
│
├── features/
│   ├── platform/
│   ├── iam/
│   ├── party/
│   ├── lead/
│   ├── product/
│   ├── matching/
│   ├── transaction/
│   ├── contract/
│   ├── revenue/
│   ├── activity/
│   ├── marketing/
│   ├── analytics/
│   ├── documents/
│   ├── audit/
│   ├── integration/
│   └── operations/
│
├── hooks/
├── lib/
├── providers/
├── styles/
├── types/
└── tests/

frontend/
├── api-client/
├── auth/
├── design-system/
├── localization/
├── observability/
└── shared/
```

---

# 6. Feature module structure

Mỗi feature nên có:

```text
features/<context>/<feature>/
├── api/
├── components/
├── hooks/
├── schemas/
├── tables/
├── forms/
├── pages/
├── state/
├── types/
├── utils/
└── __tests__/
```

Không bắt buộc tạo thư mục rỗng.

Không đặt cross-feature component vào một feature nếu thực sự dùng chung.

---

# 7. Dependency direction

```text
app routes
    ↓
feature pages
    ↓
feature components/hooks
    ↓
generated API client + shared design system
```

Bị cấm:

- Design System import feature code.
- Shared layer import feature.
- Feature A import internals Feature B.
- Component trực tiếp import backend code.
- Feature import raw OpenAPI JSON.

Cross-feature interaction dùng:

- Shared typed contract.
- Route navigation.
- Public feature API.
- Server-provided composition DTO.

---

# 8. Public API của feature

Mỗi feature nên expose qua:

```text
features/<context>/<feature>/index.ts
```

Chỉ export:

- Public page component.
- Public hook.
- Public type.
- Public command helper.

Không import internal path sâu từ feature khác.

Sai:

```typescript
import { InternalLeadTableRow } from "@/features/lead/list/internal/types";
```

Đúng:

```typescript
import { LeadSummary } from "@/features/lead";
```

---

# 9. TypeScript strictness

Bắt buộc:

```text
strict: true
noImplicitAny: true
strictNullChecks: true
noUncheckedIndexedAccess: true
exactOptionalPropertyTypes: true
useUnknownInCatchVariables: true
```

nếu toolchain/project config cho phép.

Không dùng:

```typescript
any
as any
// @ts-ignore
```

trừ approved local exception.

---

# 10. TypeScript naming

| Thành phần | Quy tắc | Ví dụ |
|---|---|---|
| Component | PascalCase | `CustomerDetailPage` |
| Hook | `use...` | `useCustomerDetail` |
| Function | camelCase | `formatMoney` |
| Type | PascalCase | `CustomerSummary` |
| Enum-like constant | UPPER_SNAKE_CASE | `BOOKING_STATUS_LABELS` |
| File component | kebab-case | `customer-detail-page.tsx` |
| File hook | kebab-case | `use-customer-detail.ts` |
| Test | `.test.tsx` | `customer-detail-page.test.tsx` |

Không dùng tên mơ hồ:

```text
Data
Item
Thing
Helper
Common
Manager
```

---

# 11. Type ownership

## Generated API types

Source:

```text
contracts/openapi/openapi.json
```

Không handwrite duplicate API response types.

## Domain presentation types

Chỉ tạo frontend-specific type khi:

- UI state.
- Form model.
- Table column state.
- View composition.
- Local interaction state.

Không đổi meaning của backend fields.

---

# 12. `any` policy

`any` bị cấm.

Khi dữ liệu chưa biết:

```typescript
unknown
```

sau đó validate/narrow.

Ví dụ:

```typescript
function parseUnknownError(error: unknown): ProblemDetails {
  ...
}
```

Không cast mù để compiler im lặng.

---

# 13. Type assertions

Type assertion chỉ khi:

- Runtime invariant đã được validate.
- Library typing limitation.
- Generated contract mismatch đã có issue.

Mỗi assertion không hiển nhiên cần comment.

Không dùng:

```typescript
value as Customer
```

khi chưa validate.

---

# 14. Null and optional semantics

Phân biệt:

- `undefined`: field chưa được cung cấp.
- `null`: field có chủ đích không có giá trị.
- Empty string: input rỗng.
- Empty array: không có items.

Form mapping phải rõ.

Không dùng `||` nếu giá trị `0`, `false` hợp lệ.

Ưu tiên:

```typescript
value ?? fallback
```

---

# 15. React component principles

Component phải:

- Có một trách nhiệm rõ.
- Nhận typed props.
- Không chứa business truth.
- Không tự quyết định authorization.
- Không mutate props.
- Không side effect trong render.
- Có accessible markup.
- Có test khi critical.

---

# 16. Component size

Component lớn phải được tách khi:

- Có nhiều interaction không liên quan.
- Có nhiều data sources.
- Có nhiều conditional branches.
- Khó test.
- Vượt khoảng 200–300 dòng mà không có lý do.

Không tách thành nhiều component vô nghĩa chỉ để giảm dòng.

Tách theo responsibility.

---

# 17. Server Components

Server Component là mặc định khi:

- Không cần browser APIs.
- Không cần client interaction.
- Có thể render server-side an toàn.
- Data fetch server phù hợp architecture.

Lợi ích:

- Giảm bundle.
- Giảm client code.
- Bảo vệ server-only logic.
- Cải thiện first render.

---

# 18. Client Components

Chỉ dùng `"use client"` khi cần:

- Event handlers.
- Browser APIs.
- React state/effects.
- TanStack Query client hooks.
- Form interactions.
- Drag/drop.
- Complex interactive tables/charts.

Không đánh dấu toàn page client chỉ vì một button.

---

# 19. Server-only code

Dùng server-only boundary cho:

- Secret.
- Server session.
- Internal API credentials.
- Server transformations nhạy cảm.
- Direct backend network logic.

Không import server-only module vào client component.

---

# 20. React state categories

Phân loại state:

```text
Server State
URL State
Form State
Local UI State
Authentication/Session State
Application Shell State
```

Mỗi loại dùng công cụ phù hợp.

---

# 21. Server state

Dùng TanStack Query hoặc server-fetch architecture được phê duyệt.

Server state không copy sang global store không cần thiết.

Server state gồm:

- API responses.
- List data.
- Detail data.
- Dashboard data.
- Job status.
- Lookup data.

---

# 22. URL state

Filters, sorting, tabs, pagination và selected view nên nằm URL khi:

- Cần share/bookmark.
- Back/forward.
- Refresh.
- Deep-link.

Không giữ toàn bộ table state trong component nếu UX cần persistence.

---

# 23. Form state

Dùng React Hook Form.

Form state không đưa vào global store.

Long multi-step workflow có thể dùng dedicated form context hoặc draft resource từ backend.

Không giữ HIGHLY_RESTRICTED form data trong localStorage.

---

# 24. Local UI state

Dùng `useState`/`useReducer` cho:

- Modal.
- Expanded row.
- Temporary selection.
- UI mode.
- Local step.

Không dùng global state cho modal đơn giản.

---

# 25. Global state

Global state chỉ cho:

- App shell.
- Theme.
- Locale.
- Auth presentation.
- Global navigation.
- Cross-route UI preference.

Không dùng global state làm cache server data.

---

# 26. TanStack Query

## Query keys

Dùng query-key factory.

Ví dụ:

```typescript
const customerKeys = {
  all: ["customers"] as const,
  lists: () => [...customerKeys.all, "list"] as const,
  list: (params: CustomerListParams) =>
    [...customerKeys.lists(), normalizeCustomerListParams(params)] as const,
  detail: (customerId: string) =>
    [...customerKeys.all, "detail", customerId] as const,
};
```

## Requirements

- Stable.
- Serializable.
- Include filters.
- Include resource ID.
- Include access/scope context nếu cache có thể khác.
- Không chứa function/object mutable.

---

# 27. Query stale time

Stale time theo data semantics:

- Reference data: dài hơn.
- Detail mutable: ngắn.
- Dashboard: theo freshness.
- Job status: polling.
- Permission/session: controlled.

Không dùng một stale time cho toàn app.

---

# 28. Query retry

Retry read query chỉ lỗi retryable.

Không retry:

- 401.
- 403.
- 404.
- Validation.
- Business conflict.

Retry có bounded count/backoff.

---

# 29. Mutations

Mutation phải:

- Dùng generated API client.
- Có Idempotency-Key khi required.
- Có If-Match khi required.
- Map Problem Details.
- Update/invalidate cache rõ.
- Handle pending state.
- Prevent double submit.
- Surface correlation ID.

---

# 30. Optimistic UI

Không dùng optimistic update mặc định cho:

- Financial data.
- Contract status.
- Booking confirmation.
- Commercial Lock.
- Receipt.
- Refund.
- Payout.
- Permission grants.
- Customer merge.

Có thể optimistic cho:

- Local preferences.
- Non-critical UI state.
- Reordering draft items khi reversible.

Critical state phải chờ server confirmation.

---

# 31. Cache invalidation

Sau mutation:

- Invalidate affected list/detail.
- Update exact cache nếu response authoritative.
- Không invalidation toàn app tùy tiện.
- Không assume event side effects đã hoàn tất.

Cross-context eventual consistency cần pending/sync status.

---

# 32. API client

Generated client phải hỗ trợ:

- Authentication.
- Correlation ID.
- Problem Details.
- Idempotency-Key.
- ETag.
- If-Match.
- Timeouts.
- Cancellation.
- Typed responses.

Không dùng raw fetch rải rác trong components.

---

# 33. Error normalization

Mọi API error map về typed structure:

```typescript
type AppError =
  | ValidationAppError
  | AuthorizationAppError
  | ConflictAppError
  | NetworkAppError
  | UnexpectedAppError;
```

Không hiển thị `error.message` thô từ server/provider.

---

# 34. Problem Details UI mapping

Map theo:

- `error_code`.
- HTTP status.
- Field errors.
- Correlation ID.
- Retryable.

UI phải:

- Hiển thị safe message.
- Map field errors.
- Cho retry khi phù hợp.
- Hiển thị correlation ID cho support.

---

# 35. Loading states

Mỗi data-driven screen phải có:

- Initial loading.
- Background refresh.
- Mutation pending.
- Partial loading.
- Lazy section loading.

Không dùng một spinner toàn trang cho mọi tình huống.

Dùng skeleton phù hợp layout.

---

# 36. Empty states

Empty state phải phân biệt:

- Không có dữ liệu.
- Không có kết quả filter.
- Không có quyền.
- Chưa cấu hình.
- Dữ liệu đang đồng bộ.
- Feature chưa available.

Không dùng chung “No data”.

---

# 37. Error states

Phân loại:

- Network.
- Server.
- Validation.
- Permission.
- Not found.
- Conflict.
- Stale version.
- Dependency unavailable.
- Partial failure.

Mỗi loại có action phù hợp.

---

# 38. Conflict states

HTTP `409` hoặc `412` phải có UX rõ:

- Giải thích dữ liệu đã thay đổi.
- Cho refresh.
- Cho compare khi cần.
- Không silently overwrite.
- Preserve unsaved input nếu an toàn.
- Không retry tự động critical mutation.

---

# 39. Permission states

UI có thể:

- Hide action.
- Disable action.
- Show explanation.
- Request access link nếu flow tồn tại.

UI không được:

- Fetch full data rồi hide.
- Assume hidden action = secure.
- Derive permission từ role label.
- Allow action khi permission metadata chưa load.

---

# 40. Field masking in UI

Frontend chỉ hiển thị đúng dữ liệu backend trả.

Không tự reconstruct full value.

Masked field phải có visual indication phù hợp.

Không cache full value trong browser nếu user mất permission.

---

# 41. Navigation architecture

Primary navigation theo approved information architecture.

Menu:

- Permission-driven.
- Context-aware.
- Stable.
- Searchable khi lớn.
- Responsive.

Không thêm route/menu tùy feature mà không update navigation docs.

---

# 42. Route naming

URL dùng lowercase kebab-case.

Examples:

```text
/leads
/customers
/product/listings
/transactions/bookings
/contracts
/finance/payments
/revenue/commissions
/admin/platform/legal-entities
```

Không dùng internal database terminology nếu khác user language.

---

# 43. Dynamic routes

Use semantic params:

```text
customers/[customerId]
listings/[listingId]
contracts/[contractId]
```

Không expose PII trong path.

Business number có thể dùng search/display, technical route vẫn ưu tiên UUID.

---

# 44. Breadcrumbs

Screens sâu cần breadcrumbs.

Breadcrumbs:

- Reflect hierarchy.
- Accessible.
- Not leak unauthorized parent.
- Use safe labels.

---

# 45. Page titles

Mỗi route có:

- Unique title.
- Resource context.
- Status khi cần.
- No sensitive PII in browser title nếu policy cấm.

---

# 46. Layout

Application shell:

- Sidebar.
- Top bar.
- Content area.
- Command/action area.
- Responsive drawer.
- Global notifications.
- User/session indicator.

Không để mỗi module tự tạo app shell riêng.

---

# 47. Responsive behavior

Target:

- Desktop primary.
- Tablet supported.
- Mobile hỗ trợ workflows phù hợp.

Không chỉ “shrink desktop”.

Responsive rules:

- Tables chuyển card/list khi cần.
- Sidebars collapse.
- Actions accessible.
- Forms stack.
- Dialogs fit viewport.
- Touch targets đủ lớn.

---

# 48. Design System

Mọi UI phải dùng Design System.

Không tự tạo:

- Button style.
- Input style.
- Badge style.
- Dialog.
- Toast.
- Table.
- Card.
- Tabs.
- Status colors.

nếu component đã có.

---

# 49. Design tokens

Dùng tokens cho:

- Color.
- Spacing.
- Radius.
- Typography.
- Shadow.
- Motion.
- Breakpoints.
- Z-index.

Không hard-code arbitrary values trong feature.

---

# 50. Color usage

Color phải semantic:

- Success.
- Warning.
- Error.
- Info.
- Neutral.
- Status-specific.

Không chỉ dùng màu để truyền nghĩa.

Status có text/icon.

---

# 51. Typography

Use approved scale.

Không tạo font size tùy ý.

Heading hierarchy phải semantic.

Không dùng text quá nhỏ cho dense table.

---

# 52. Spacing

Dùng spacing tokens.

Không mix random `px` values.

Dense enterprise UI vẫn phải readable.

---

# 53. Icons

Dùng approved icon library.

Icon:

- Có accessible label nếu interactive.
- Không thay text ở critical action nếu meaning không rõ.
- Không mix nhiều styles.

---

# 54. Buttons

Button variants:

- Primary.
- Secondary.
- Destructive.
- Ghost.
- Link.

Critical destructive action cần confirmation.

Không dùng icon-only nếu không có tooltip/accessible name.

---

# 55. Forms

Form phải:

- Có label.
- Help text khi cần.
- Required indication.
- Client structural validation.
- Server error mapping.
- Accessible error association.
- Disabled/pending state.
- Preserve input on failure.
- Unsaved changes warning.

---

# 56. Form schema

Zod schema cho frontend structural validation.

Không duplicate business invariant chỉ ở frontend.

Backend vẫn là authority.

Schema names:

```text
createLegalEntityFormSchema
updateCustomerRequirementFormSchema
```

---

# 57. Form submit

Submit flow:

1. Validate client structure.
2. Disable duplicate submit.
3. Create/reuse Idempotency-Key đúng policy.
4. Send ETag/If-Match.
5. Handle validation.
6. Handle conflict.
7. Update cache.
8. Show success.
9. Navigate/retain state.

---

# 58. Multi-step forms

Multi-step workflow phải:

- Có progress.
- Có save draft nếu dài.
- Preserve server draft.
- Validate per step và final.
- Handle stale version.
- Show missing requirements.
- Avoid local-only state cho critical data.

---

# 59. Sensitive forms

Không lưu trong browser persistence:

- Identity number.
- Bank account.
- Payment evidence.
- Financial Profile.
- Contract confidential terms.
- Secret.

Clear sensitive state khi leave/logout.

---

# 60. Tables

TanStack Table là baseline.

Table phải hỗ trợ tùy use case:

- Server pagination.
- Sorting.
- Filtering.
- Column visibility.
- Pinned columns.
- Selection.
- Bulk actions.
- Saved views.
- Export.
- Empty/loading/error.
- Accessible keyboard behavior.

---

# 61. Table data model

Rows dùng stable ID.

Không dùng array index làm key.

Column definitions typed.

Không chứa business calculations official trong cell.

---

# 62. Server-side table behavior

Large operational tables:

- Server filtering.
- Server sorting.
- Cursor pagination.
- Page size limit.
- Scope enforced backend.

Không tải toàn bộ rồi filter/sort client.

---

# 63. Table filters

Filters:

- Typed.
- URL-backed khi cần.
- Allowlist.
- Clear/reset.
- Show active filters.
- Preserve on navigation nếu UX yêu cầu.

Không gửi arbitrary filter expression.

---

# 64. Bulk actions

Bulk action phải:

- Separate permission.
- Explicit selection count.
- Confirm scope.
- Handle partial results.
- Use async job khi lớn.
- Audit.
- Clear selection after completion.

Không chạy một request/row trong browser loop cho khối lượng lớn.

---

# 65. Saved views

Saved view chứa:

- Filters.
- Sort.
- Columns.
- Density.
- Ownership/sharing.
- Version.

Không lưu sensitive values nếu policy cấm.

---

# 66. Detail pages

Detail page nên có:

- Header.
- Identity.
- Status.
- Primary actions.
- Summary.
- Tabs/sections.
- Related resources.
- Timeline.
- Audit link nếu permitted.
- Conflict status.
- Sync state.

Không hiển thị mọi field trong một form khổng lồ.

---

# 67. Status transitions

UI action phải:

- Chỉ show allowed action.
- Có readiness preview khi cần.
- Có reason input khi required.
- Có confirmation.
- Có permission.
- Handle async process.
- Show updated state.

Không có generic status dropdown.

---

# 68. Readiness checks

Critical activation/confirmation flows phải hiển thị:

- Passed checks.
- Blocking checks.
- Warnings.
- Missing permissions.
- Suggested action.

UI không tự tính readiness nếu backend có endpoint/policy.

---

# 69. Approval UI

Approval screen phải hiển thị:

- Requested action.
- Resource.
- Requested by.
- Amount/risk.
- Policy/version.
- SoD warning.
- Supporting evidence.
- Approve/reject reason.
- Audit context.

Không cho self-approval khi backend policy cấm.

---

# 70. Timeline UI

Timeline:

- Read-only projection.
- Sorted by event time.
- Source link.
- Type/filter.
- Masking.
- Pagination.
- Merge redirect support.
- Freshness.

Không xem Timeline là source of truth.

---

# 71. Dashboard UI

Dashboard widgets chỉ dùng certified API metrics.

Mỗi widget phải hiển thị:

- Metric name.
- Value.
- Unit/currency.
- Period.
- Comparison.
- Freshness.
- Filter context.
- Drill-down.
- Metric version nếu cần.

Frontend không tự tính KPI chính thức.

---

# 72. Chart standards

Charts:

- Dùng Recharts trong approved analytics/dashboard layer.
- Không import Recharts trực tiếp trong arbitrary feature.
- Có accessible summary.
- Có tooltip.
- Có legend.
- Có empty/loading/error.
- Không 3D.
- Không misleading axis.
- Không excessive colors.
- Time series dùng correct timezone/period.

---

# 73. KPI cards

KPI card phải có:

- Label.
- Value.
- Unit.
- Comparison.
- Trend.
- Period.
- Freshness.
- Drill action.

Không chỉ hiển thị một số không context.

---

# 74. Funnel charts

Funnel phải:

- Có stage definitions.
- Có counts.
- Có conversion rates.
- Có period.
- Có scope.
- Không mix cohorts không cùng definition.
- Drill-down.

---

# 75. Money display

Dùng shared formatter.

Input:

```text
amount string/Decimal-safe representation
currency
locale
```

Không parse money qua `Number` nếu có precision risk.

Không hard-code `₫` hoặc currency trong feature.

---

# 76. Date/time display

- Store/receive UTC.
- Display theo Legal Entity/user timezone policy.
- Show timezone khi ambiguity.
- Use shared formatter.
- Relative time chỉ cho convenience, exact time accessible.
- Business date không convert như instant.

---

# 77. Localization

UI strings qua localization system.

Không hard-code Vietnamese trong reusable components nếu localization architecture yêu cầu.

Keys phải semantic:

```text
customer.detail.title
booking.actions.confirm
```

Không dùng full sentence làm key nếu project standard không cho.

---

# 78. Locale formatting

Use locale-aware:

- Date.
- Time.
- Number.
- Currency.
- Percentage.

Do not manually concatenate separators.

---

# 79. Accessibility target

Baseline:

```text
WCAG 2.1 AA
```

Mọi critical workflow phải keyboard usable.

---

# 80. Semantic HTML

Dùng:

- `button` cho action.
- `a` cho navigation.
- `label` cho input.
- `table` cho tabular data.
- `nav`, `main`, `header`, `section`.
- Heading hierarchy.

Không dùng clickable `div` thay button.

---

# 81. Keyboard navigation

Phải hỗ trợ:

- Tab order.
- Enter/Space.
- Escape đóng modal.
- Arrow keys theo component pattern.
- Focus visible.
- Skip link.
- Table/action keyboard access.

---

# 82. Focus management

- Modal trap focus.
- Return focus after close.
- Focus first invalid field.
- Route transition focus heading.
- No focus loss after mutation.
- Destructive confirmation focus safe.

---

# 83. ARIA

ARIA chỉ dùng khi semantic HTML không đủ.

Không thêm ARIA sai.

Interactive custom components phải theo WAI-ARIA pattern.

---

# 84. Screen reader

Test:

- Labels.
- Error announcements.
- Status changes.
- Loading announcements.
- Dialog titles/descriptions.
- Table headers.
- Chart summaries.

---

# 85. Color contrast

Text/control/status phải đạt contrast baseline.

Không dùng màu nhạt khó đọc chỉ để đẹp.

---

# 86. Motion

- Respect `prefers-reduced-motion`.
- Không animation dài.
- Không motion gây distraction.
- Critical status không chỉ animation.

---

# 87. Toasts

Toast dùng cho:

- Success.
- Non-blocking info.
- Background completion.

Không dùng toast thay inline error cho form.

Critical error phải persistent.

---

# 88. Dialogs

Dialog dùng khi:

- Confirmation.
- Focused form.
- Critical decision.
- Small detail.

Không dùng modal cho workflow dài.

Destructive dialogs phải nêu consequence.

---

# 89. Drawers

Drawer phù hợp:

- Quick detail.
- Filters.
- Secondary action.
- Mobile navigation.

Không nhồi full edit workflow vào drawer nếu phức tạp.

---

# 90. Notifications

In-app notification UI:

- Unread state.
- Classification.
- Resource link.
- Timestamp.
- Safe content.
- Mark read.
- Pagination.
- Permission recheck.

Notification không thay business state.

---

# 91. Search UI

Global search:

- Debounce.
- Minimum length.
- Scope-aware.
- Masked.
- Type grouped.
- Keyboard navigation.
- Recent searches chỉ khi safe.
- No PII persistence.

Search result phải reauthorize backend.

---

# 92. Command palette

Command palette có thể hỗ trợ navigation/actions.

Actions phải permission-aware.

Không execute critical action trực tiếp không confirmation.

---

# 93. Authentication UI

Auth UI phải:

- Không expose token.
- Handle expiry.
- Handle session revoked.
- Handle MFA.
- Handle disabled user.
- Redirect safely.
- Preserve intended route nếu safe.
- Avoid open redirect.

---

# 94. Session expiry UX

- Warning before expiry nếu available.
- Reauthenticate.
- Preserve unsaved non-sensitive work khi possible.
- Clear sensitive state.
- No infinite refresh loop.

---

# 95. Logout

Logout phải:

- Revoke/clear session.
- Clear query cache.
- Clear sensitive local state.
- Redirect.
- No stale protected page via back navigation if possible.

---

# 96. Frontend security

Frontend không chứa:

- Secret.
- Service token.
- Private key.
- Database URL.
- Provider credentials.
- Server-only configuration.

`NEXT_PUBLIC_*` chỉ cho public config.

---

# 97. Browser storage

Allowed:

- Theme.
- Locale.
- Non-sensitive UI preferences.

Disallowed:

- Access/refresh token nếu architecture không approved.
- Customer PII.
- Contract content.
- Financial Profile.
- Payment evidence.
- Signed URLs.
- Secret.

---

# 98. XSS prevention

- React escaping.
- Avoid `dangerouslySetInnerHTML`.
- Sanitize approved rich text.
- Validate URLs.
- CSP.
- No arbitrary script.
- No unsafe markdown rendering.

---

# 99. CSRF and cookies

Nếu auth cookie:

- SameSite.
- CSRF token.
- Origin validation.
- Secure/HttpOnly.
- No state-changing GET.

Frontend API wrapper phải hỗ trợ CSRF token architecture.

---

# 100. CORS awareness

Frontend không được dựa vào CORS như authorization.

CORS errors phải được xử lý rõ trong environment diagnostics.

---

# 101. URL security

Không đưa vào URL:

- Token.
- Full phone/email.
- Identity number.
- Bank data.
- Secret.
- Sensitive form data.

Query filters có PII cần review.

---

# 102. File upload UI

Upload UI phải:

- Show size/type rules.
- Validate client for UX.
- Server remains authority.
- Use upload intent.
- Show progress.
- Handle retry.
- Handle scan status.
- Handle quarantine.
- Prevent duplicate submit.
- Never expose raw object key.

---

# 103. File download UI

Download action:

- Reauthorize via backend.
- Show classification warning when required.
- Handle signed URL expiry.
- Audit is backend concern.
- No permanent link caching.

---

# 104. Third-party scripts

Không thêm third-party script không review.

Tag Manager/data layer phải allowlist.

Không capture PII/form content.

Sensitive routes có thể disable analytics.

---

# 105. Performance goals

Frontend targets theo NFR.

Baseline:

- Fast shell render.
- Route-level code splitting.
- Minimize client bundle.
- Avoid unnecessary rerenders.
- Efficient tables.
- Lazy load heavy charts/editors.
- Image optimization.
- Cache safe data.

---

# 106. Bundle size

Phải monitor:

- Initial JS.
- Route chunk.
- Shared chunk.
- Third-party packages.

Dependency mới cần bundle impact review.

Không import entire utility library nếu chỉ dùng một function.

---

# 107. Code splitting

Use:

- Route-level split.
- Dynamic import.
- Lazy heavy editors/charts.
- Client-only widgets.

Không lazy-load tiny critical controls gây flicker.

---

# 108. Images

Use Next Image hoặc approved abstraction.

Requirements:

- Correct dimensions.
- Responsive sizes.
- Lazy loading.
- Alt text.
- No sensitive images cached publicly.
- Signed URLs handled safely.

---

# 109. Fonts

Use approved fonts.

- Self-host/managed according policy.
- Preload critical.
- Avoid layout shift.
- No arbitrary font per feature.

---

# 110. Rendering performance

Avoid:

- Large client component trees.
- Unnecessary context providers.
- Passing unstable objects.
- Excessive effects.
- Rendering thousands of rows without virtualization.
- Recharts on every route.

---

# 111. Memoization

`useMemo`/`useCallback` chỉ khi:

- Expensive calculation.
- Stable dependency needed.
- Measured rerender problem.
- Library identity requirement.

Không memoize mọi thứ.

---

# 112. React effects

Effects dùng cho synchronization với external systems.

Không dùng effect để derive state có thể tính trong render.

Không suppress dependencies tùy tiện.

Cleanup required.

---

# 113. Avoid derived duplicated state

Sai:

```typescript
const [filteredCustomers, setFilteredCustomers] = useState([]);
useEffect(() => setFilteredCustomers(filter(customers)), [customers, filters]);
```

Đúng:

```typescript
const filteredCustomers = useMemo(...);
```

hoặc backend filter.

---

# 114. Table performance

- Server pagination.
- Virtualization khi rows lớn.
- Memoized columns.
- Stable row IDs.
- Avoid heavy cell components.
- Lazy row actions.
- Debounced filters.

---

# 115. Dashboard performance

- Fetch aggregated endpoints.
- Parallelize independent queries.
- Avoid one endpoint per cell.
- Lazy non-critical widgets.
- Show freshness.
- Cache according metric policy.
- Abort stale requests.

---

# 116. Network behavior

- Cancel obsolete requests.
- Debounce search.
- Avoid duplicate fetch.
- Use prefetch selectively.
- Avoid waterfall.
- Respect API rate limits.
- Async jobs for bulk.

---

# 117. Offline behavior

CRM không mặc định offline-first.

Không cache critical mutation offline.

Network loss phải:

- Show status.
- Preserve safe draft locally only if policy.
- Avoid duplicate submit.
- Retry read when restored.

---

# 118. Error boundaries

Phải có:

- Global error boundary.
- Route error boundaries.
- Feature-level boundaries cho heavy independent widgets khi cần.

Error boundary không nuốt error im lặng.

Có correlation/support action.

---

# 119. Not-found behavior

`not-found.tsx` phải:

- Không leak resource existence.
- Provide navigation.
- Distinguish generic not found.
- Not reveal unauthorized details.

---

# 120. Observability

Frontend logs/events phải:

- Structured.
- Minimal.
- No PII.
- Correlation.
- Route.
- Operation.
- Error code.
- Browser/environment metadata safe.

Không console.log production.

---

# 121. Frontend error reporting

Error reporter phải:

- Redact sensitive data.
- Group errors.
- Attach release/version.
- Attach route.
- Attach correlation ID.
- Respect privacy/consent.
- Avoid full DOM/form capture on sensitive pages.

---

# 122. Web vitals

Monitor:

- LCP.
- INP.
- CLS.
- TTFB.
- Route transition.
- JS errors.

Segment by route category, not user ID.

---

# 123. Analytics telemetry

Product analytics events phải:

- Allowlist.
- No PII.
- No financial values unless approved aggregate.
- No contract/customer IDs if linkable.
- Consent-aware.
- Versioned.

---

# 124. Frontend testing taxonomy

- Unit.
- Component.
- Integration.
- Accessibility.
- Visual regression.
- E2E.
- Performance.
- Security.
- Browser compatibility.

---

# 125. Unit tests

Test:

- Formatters.
- Query keys.
- Zod schemas.
- Reducers.
- Pure transforms.
- Permission presentation helper.
- URL state parsing.

Không test trivial implementation.

---

# 126. Component tests

Dùng Testing Library.

Test như user:

- Role.
- Label.
- Text.
- Interaction.
- Focus.
- Error.
- Loading.
- Permission.
- Conflict.

Không test internal state.

---

# 127. Network integration tests

Dùng MSW hoặc approved network mock.

Test:

- API success.
- Validation Problem Details.
- 401.
- 403.
- 404.
- 409.
- 412.
- 429.
- 503.
- Retryable network error.
- Idempotency replay.

Không mock hook internals nếu mục tiêu là integration.

---

# 128. Accessibility tests

Automated:

- axe hoặc approved tool.
- Semantic roles.
- Labels.
- Contrast where tooling.
- Keyboard flows.

Manual:

- Screen reader critical flows.
- Keyboard-only.
- Zoom.
- Reduced motion.

---

# 129. Visual regression

Use cho:

- Design System.
- Critical layouts.
- Tables.
- Forms.
- Dashboard widgets.
- Responsive states.

Không update baseline mù.

Review diff.

---

# 130. E2E tests

Playwright phải test:

- Real routes.
- Real frontend build.
- API/database.
- Auth test setup.
- Critical business journeys.

Không mock toàn backend trong core E2E.

---

# 131. Frontend E2E critical scenarios

1. Login and session expiry.
2. Enterprise/Legal Entity setup.
3. Lead list/filter/detail.
4. Customer create/duplicate handling.
5. Listing activation readiness.
6. Matching shortlist.
7. Hold/Booking conflict.
8. Contract approval/signature status.
9. Payment Allocation/Receipt.
10. Dashboard drill-down.
11. Export.
12. File upload/quarantine.
13. Permission-denied paths.
14. Optimistic concurrency conflict.
15. Async job progress/failure.

---

# 132. E2E selectors

Ưu tiên:

1. Role.
2. Label.
3. Text.
4. Accessible name.
5. Stable `data-testid` khi cần.

Không dùng brittle CSS chain.

---

# 133. Browser matrix

Test theo Browser Support Policy:

- Chrome stable.
- Edge stable.
- Firefox stable.
- Safari stable hoặc supported runner.

Critical flows cross-browser.

---

# 134. Frontend security tests

Test:

- No secret in bundle.
- No PII local storage.
- XSS payload escaped.
- Open redirect blocked.
- Unauthorized action hidden/denied.
- Full masked fields not present.
- CSRF behavior if cookie auth.
- CSP violations.
- Signed URL expiry.
- File name sanitization.

---

# 135. Performance tests

Measure:

- Bundle.
- LCP.
- INP.
- CLS.
- Large table.
- Dashboard.
- Route transition.
- Search.
- Memory usage.
- Long session.

---

# 136. Flaky test policy

Flaky test là defect.

Không:

- Add arbitrary wait.
- Retry unlimited.
- Disable test.
- Update snapshot mù.

Phải có owner/issue/expiry.

Critical E2E không được quarantine dài hạn.

---

# 137. Test data

- Fake.
- No production PII.
- Deterministic.
- Stable IDs.
- Role/scope fixtures.
- Timezone/currency variation.
- Different resource states.

---

# 138. Storybook/component catalog

Nếu Design System dùng Storybook hoặc equivalent:

- Mỗi shared component có stories.
- States.
- Sizes.
- Accessibility.
- Dark/light nếu supported.
- Error/disabled/loading.
- Visual regression.

Feature-specific business pages không bắt buộc story nếu E2E/component tests đủ.

---

# 139. Code review checklist

## Architecture

- Đúng feature?
- Có import internals feature khác?
- Server/client boundary hợp lý?
- API types generated?

## Domain representation

- State đúng?
- No frontend source of truth?
- No official KPI calculation?
- No generic status edit?

## Security

- Permission UX?
- Masking?
- No secret?
- No PII storage/log?
- Safe URLs?

## UX

- Loading?
- Empty?
- Error?
- Conflict?
- Accessibility?
- Responsive?

## Performance

- Bundle?
- Fetch waterfall?
- Table strategy?
- Memoization hợp lý?

## Testing

- Unit/component/integration/E2E?
- Accessibility?
- Security?
- No flaky wait?

---

# 140. Frontend anti-patterns bị cấm

1. `"use client"` toàn app.
2. `any`.
3. Raw fetch rải rác.
4. Duplicate API types.
5. Business truth trong frontend.
6. Official KPI tính ở client.
7. Permission từ role label.
8. Full data fetch rồi hide.
9. Generic status dropdown.
10. Client-side filtering cho large official list.
11. LocalStorage chứa PII/token.
12. Hard-coded colors/style.
13. Copy Design System component.
14. Arbitrary chart library.
15. `dangerouslySetInnerHTML` không sanitize.
16. Console logging production.
17. Arbitrary sleeps in E2E.
18. Index làm React key.
19. Giant component/service file.
20. Global state cho mọi thứ.
21. Optimistic update critical financial state.
22. Silent conflict overwrite.
23. Unbounded table.
24. Hard-coded Vietnamese text trong reusable package nếu localization required.
25. No accessibility states.

---

# 141. AI Agent frontend protocol

Trước khi triển khai UI, AI Agent phải:

1. Đọc Context Pack và Sprint Pack.
2. Xác định user persona.
3. Xác định route/navigation.
4. Xác định permissions/scopes/masking.
5. Xác định API contracts.
6. Xác định server/client component boundary.
7. Xác định loading/empty/error/conflict states.
8. Xác định responsive/accessibility behavior.
9. Xác định tests.
10. Dùng Design System.
11. Generate/use API types.
12. Run lint/typecheck/tests/build.
13. Update docs/evidence.

---

# 142. AI Agent prohibited frontend behaviors

AI Agent không được:

1. Tự tạo design style mới.
2. Tự thêm dependency.
3. Dùng `any`.
4. Handwrite API DTO duplicate.
5. Tính permission ở client.
6. Tính official KPI.
7. Bỏ loading/error/conflict.
8. Bỏ accessibility.
9. Lưu PII/token ở browser storage.
10. Dùng raw fetch nếu client có sẵn.
11. Bỏ E2E cho critical path.
12. Báo Done khi build/typecheck fail.
13. Tạo fake backend response trong production code.
14. Tự đổi route architecture.
15. Tự expose sensitive field.

---

# 143. Definition of Ready cho frontend feature

Frontend feature chỉ Ready khi:

1. User/persona rõ.
2. Business flow rõ.
3. API contract rõ.
4. Permission/scope rõ.
5. Field masking rõ.
6. UI states rõ.
7. Design System components rõ.
8. Responsive/accessibility rõ.
9. Test plan rõ.
10. No unresolved API/domain conflict.

---

# 144. Definition of Done cho frontend feature

Feature chỉ Done khi:

1. Route/page implemented.
2. Generated API client used.
3. TypeScript strict pass.
4. Loading/empty/error/conflict states.
5. Permission UX.
6. Field masking respected.
7. Responsive.
8. Accessibility baseline.
9. Unit/component/integration tests.
10. E2E critical path.
11. Security tests relevant.
12. Performance acceptable.
13. Lint/typecheck/build pass.
14. Documentation updated.
15. Acceptance evidence recorded.

---

# 145. Frontend completion report

```markdown
## Frontend Summary

### Routes

### Components

### Server/Client Boundaries

### API Operations

### Query Keys and Cache

### Forms

### Tables

### Permissions and Masking

### Loading/Empty/Error/Conflict States

### Responsive Behavior

### Accessibility

### Security

### Performance

### Tests

### Build Results

### Known Limitations
```

---

# 146. Frontend exception process

Ngoại lệ cần:

```text
docs/engineering/frontend-exceptions/EXC-FE-XXX.md
```

Nội dung:

- Rule.
- Feature/route.
- Reason.
- UX impact.
- Accessibility impact.
- Security impact.
- Performance impact.
- Mitigation.
- Owner.
- Expiry.
- Approval.

Không có ngoại lệ vô thời hạn không owner.

---

# 147. Change Log

## Version 1.0.0 — 2026-07-24

- Thiết lập frontend architecture.
- Khóa Next.js Server/Client Component rules.
- Khóa TypeScript strictness và type ownership.
- Khóa TanStack Query, forms, tables và API client.
- Khóa loading, error, conflict, permission và masking UX.
- Khóa Design System, tokens, accessibility và responsive behavior.
- Khóa Dashboard/chart standards.
- Khóa frontend security, performance và observability.
- Khóa testing, review checklist và AI Agent protocol.
- Khóa Definition of Ready và Definition of Done.

---

# 148. Kết luận

Frontend của `crm_bds_ai` là lớp tương tác nghiệp vụ, không phải nguồn chân lý.

Mục tiêu:

```text
Accurate Domain Representation
+ Consistent Design System
+ Backend-Enforced Security
+ Accessible Workflows
+ Reliable Data Fetching
+ Explicit Error and Conflict Handling
+ Scalable Enterprise Tables
+ Certified Dashboard Presentation
```

Nguyên tắc tối cao:

> Frontend phải giúp người dùng hiểu đúng trạng thái và thực hiện đúng hành động, nhưng không được tự quyết định business truth, authorization hoặc official metrics.
