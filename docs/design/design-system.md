# CRM_BDS_AI — DESIGN SYSTEM

## Hệ thống thiết kế chuẩn bắt buộc cho toàn bộ giao diện `crm_bds_ai`

**Document ID:** `DESIGN-SYSTEM-001`  
**Canonical path:** `docs/design/design-system.md`  
**Product:** `crm_bds_ai`  
**Version:** `1.0.0`  
**Status:** `Accepted / Mandatory`  
**Canonical:** `Yes` đối với nền tảng thiết kế, component semantics, interaction states, visual consistency và accessibility  
**Owner:** `Design System Owner`  
**Reviewers:** `Product Owner`, `Frontend Architecture Owner`, `UX Owner`, `Accessibility Owner`, `Security Owner`, `QA Owner`, `Context Owners`  
**Effective date:** `2026-08-05`  
**Last reviewed:** `2026-08-05`  
**Next review:** Khi design language, component library, accessibility baseline, brand system hoặc frontend architecture thay đổi  
**Supersedes:** `None — Greenfield baseline`  
**Superseded by:** Không

---

# 1. Mục đích

Tài liệu này định nghĩa hệ thống thiết kế chuẩn cho toàn bộ `crm_bds_ai`.

Mục tiêu:

1. Tạo giao diện nhất quán giữa 14 module và 16 Bounded Context.
2. Giảm sai lệch giữa thiết kế, frontend và nghiệp vụ.
3. Bảo đảm mỗi trạng thái nghiệp vụ được trình bày rõ ràng.
4. Bảo đảm accessibility theo chuẩn enterprise.
5. Bảo đảm AI Agent và developer không tự tạo style, component hoặc interaction riêng.
6. Bảo đảm các màn hình dữ liệu lớn, workflow dài và nghiệp vụ tài chính vẫn dễ đọc và dễ thao tác.
7. Bảo đảm responsive behavior có hệ thống.
8. Bảo đảm mọi component có đầy đủ loading, empty, error, disabled, read-only và permission states.
9. Bảo đảm design token có thể dùng thống nhất trong code.
10. Bảo đảm giao diện có thể mở rộng lâu dài mà không phân mảnh.

Tài liệu này phải được đọc cùng:

```text
docs/design/design-tokens.md
docs/design/navigation-and-information-architecture.md
docs/design/dashboard-visualization-system.md
docs/engineering/frontend-standards.md
docs/engineering/security-standards.md
docs/engineering/testing-standards.md
docs/security/permission-registry.md
docs/security/field-masking-matrix.md
Relevant Context Implementation Pack
Current Sprint Execution Pack
```

---

# 2. Design principles

## 2.1. Clarity over decoration

Mọi thành phần giao diện phải ưu tiên:

- Dễ đọc.
- Dễ hiểu.
- Dễ phân biệt trạng thái.
- Dễ tìm hành động tiếp theo.

Không dùng decorative effect làm giảm khả năng đọc.

## 2.2. Domain truth over visual convenience

UI phải phản ánh chính xác trạng thái nghiệp vụ.

Không đơn giản hóa sai meaning chỉ để giao diện “gọn”.

Ví dụ:

- `SIGNED` khác `EFFECTIVE`.
- `PAYMENT_RECEIVED` khác `PAYMENT_ALLOCATED`.
- `REVENUE_RECOGNIZED` khác `REVENUE_COLLECTED`.
- `COMMISSION_VESTED` khác `COMMISSION_PAID`.

## 2.3. Consistency over local preference

Một component đã có trong Design System phải được tái sử dụng.

Không tạo phiên bản riêng trong từng module.

## 2.4. Progressive disclosure

Hiển thị thông tin quan trọng trước.

Chi tiết nâng cao nằm trong:

- Tabs.
- Expandable sections.
- Drawers.
- Secondary actions.
- Context panels.

## 2.5. Accessible by default

Accessibility không phải tính năng bổ sung.

Mọi component phải:

- Keyboard usable.
- Screen-reader compatible.
- Có contrast.
- Có focus visible.
- Không phụ thuộc màu.

## 2.6. Enterprise density

CRM có dữ liệu dày đặc.

Thiết kế phải:

- Gọn.
- Có hierarchy.
- Không quá nhiều khoảng trống.
- Không làm mất khả năng đọc.

## 2.7. Explicit system status

Người dùng luôn phải biết:

- Dữ liệu đang tải.
- Dữ liệu đã lưu.
- Có lỗi.
- Có xung đột.
- Có quyền hay không.
- Có pending process.
- Dữ liệu có stale không.

## 2.8. Safe actions

Critical actions phải:

- Có xác nhận.
- Có consequence.
- Có reason khi cần.
- Có permission.
- Có loading.
- Không double-submit.

---

# 3. Design language

Design language của `crm_bds_ai` phải mang các đặc tính:

```text
Professional
Structured
Calm
Reliable
Dense but Readable
Modern Enterprise
Operationally Transparent
```

Không hướng đến:

```text
Playful consumer app
Heavy gradients
Overly decorative cards
Excessive motion
Glassmorphism
Random shadows
Color-driven meaning only
```

---

# 4. Visual hierarchy

Mỗi màn hình nên có hierarchy:

```text
Page Context
→ Primary Status
→ Primary Action
→ Summary
→ Main Content
→ Secondary Details
→ Related History
```

Không để mọi phần có cùng visual weight.

---

# 5. Design tokens

Canonical token groups:

```text
color
spacing
typography
radius
shadow
border
motion
breakpoint
z-index
size
opacity
```

Feature code không hard-code giá trị tùy ý nếu token tương ứng đã tồn tại.

---

# 6. Color system

## 6.1. Neutral colors

Dùng cho:

- Background.
- Surface.
- Border.
- Text.
- Disabled.
- Secondary labels.

Neutral palette phải có đủ mức cho light/dark nếu hỗ trợ.

## 6.2. Brand colors

Brand color dùng cho:

- Primary actions.
- Active navigation.
- Focus accents.
- Selected state.

Không dùng brand color cho mọi element.

## 6.3. Semantic colors

```text
success
warning
error
info
neutral
```

Mỗi semantic color phải có:

- Background.
- Border.
- Text.
- Icon.
- Strong variant.
- Subtle variant.

## 6.4. Financial colors

Không dùng:

- Green = always good.
- Red = always bad.

trong financial context nếu meaning khác nhau.

Ví dụ:

- Refund có thể là red warning.
- Negative adjustment có thể neutral/attention tùy context.
- Collected revenue có thể positive.
- Outstanding receivable có thể warning.

## 6.5. Chart colors

Chart palette phải:

- Distinguishable.
- Accessible.
- Stable by series meaning.
- Không quá nhiều màu.
- Có legend.
- Không dùng gradient để che data.

---

# 7. Status colors

Status color không được dùng làm semantic authority.

Mỗi status cần:

- Text label.
- Optional icon.
- Semantic color.
- Tooltip/description khi cần.

Example mapping:

```text
DRAFT → neutral
PENDING → info
ACTIVE → success
SUSPENDED → warning
BLOCKED → error
CANCELLED → neutral/error depending context
ARCHIVED → neutral
FAILED → error
COMPLETED → success
```

Không hard-code status color trong feature.

Dùng centralized status registry.

---

# 8. Typography

## 8.1. Font family

Dùng font đã được phê duyệt trong Design Tokens.

Không thêm font riêng theo feature.

## 8.2. Type scale

Canonical roles:

```text
display
page-title
section-title
subsection-title
body
body-strong
caption
label
code
numeric
```

## 8.3. Numeric typography

Money, percentage và KPI nên dùng:

- Tabular numerals.
- Right alignment trong table.
- Clear unit/currency.
- Consistent decimal precision.

## 8.4. Line height

Line height phải bảo đảm:

- Readability.
- Dense tables.
- Multi-line labels.
- Vietnamese diacritics.

---

# 9. Spacing system

Spacing dùng token-based scale.

Baseline conceptual scale:

```text
0
1
2
3
4
6
8
10
12
16
20
24
32
40
48
64
```

Không tạo random spacing như `13px`, `17px` nếu không có token.

---

# 10. Radius

Radius dùng nhất quán.

Recommended categories:

```text
none
small
medium
large
pill
```

Enterprise UI không dùng quá nhiều rounded cards.

Pill chỉ dùng cho:

- Status.
- Tags.
- Filters.
- Compact chips.

---

# 11. Shadows

Shadow chỉ dùng để phân tầng:

- Popover.
- Modal.
- Drawer.
- Floating menu.

Không dùng shadow nặng cho mọi card.

---

# 12. Borders

Borders giúp:

- Group.
- Separate.
- Indicate focus.
- Show validation.

Không dùng border quá đậm gây nhiễu.

---

# 13. Motion

Motion phải:

- Ngắn.
- Có purpose.
- Respect reduced motion.
- Không cản thao tác.

Use cases:

- Dialog open/close.
- Drawer.
- Collapse.
- Skeleton transition.
- Toast.

Không animate critical financial number thay đổi theo cách khó đọc.

---

# 14. Breakpoints

Breakpoints phải theo Design Tokens.

Conceptual tiers:

```text
mobile
tablet
desktop
wide
```

Không định nghĩa breakpoint riêng trong feature.

---

# 15. Z-index

Z-index phải dùng token.

Recommended layers:

```text
base
sticky
dropdown
popover
drawer
modal
toast
critical-overlay
```

Không dùng giá trị `9999` tùy ý.

---

# 16. Layout grid

Desktop application layout:

```text
Sidebar
+ Topbar
+ Main Content
+ Optional Context Panel
```

Main content có max width linh hoạt theo screen type.

Data-heavy screens có thể full-width.

Forms có width giới hạn để dễ đọc.

---

# 17. Page anatomy

Một page chuẩn gồm:

```text
Page Header
Breadcrumb
Title
Status
Primary Actions
Summary/Context
Main Content
Secondary Panels
Timeline/Audit
```

Không bắt buộc mọi page có tất cả.

---

# 18. Page header

Page Header phải hỗ trợ:

- Title.
- Subtitle.
- Status.
- Primary action.
- Secondary actions.
- Breadcrumb.
- Metadata.
- Back navigation khi cần.

Primary action không nên vượt quá một hành động nổi bật.

---

# 19. Cards

Card dùng để nhóm nội dung có boundary rõ.

Không dùng card cho mọi section.

Card variants:

```text
default
subtle
outlined
interactive
metric
warning
```

Interactive card phải keyboard accessible.

---

# 20. Panels

Panel dùng cho:

- Context summary.
- Readiness.
- Timeline.
- Related resources.
- Filters.
- Diagnostics.

Panel có header rõ và action scope rõ.

---

# 21. Sections

Section cần:

- Heading.
- Optional description.
- Optional actions.
- Content.

Không tạo heading hierarchy sai.

---

# 22. Navigation

Navigation components:

- Sidebar.
- Top navigation.
- Breadcrumbs.
- Tabs.
- Sub-navigation.
- Command palette.
- Pagination.

Navigation state phải rõ.

---

# 23. Sidebar

Sidebar phải:

- Collapsible.
- Permission-driven.
- Grouped by domain.
- Support active state.
- Support tooltips khi collapsed.
- Responsive.

Không hiện menu user không có quyền.

Nhưng backend vẫn là security boundary.

---

# 24. Topbar

Topbar có thể chứa:

- Global search.
- Notifications.
- Quick actions.
- User/session menu.
- Legal Entity context.
- Environment indicator.

Không nhồi quá nhiều actions.

---

# 25. Breadcrumbs

Breadcrumb phải:

- Reflect route hierarchy.
- Có accessible navigation.
- Không quá dài.
- Collapse intermediate levels khi cần.
- Không expose unauthorized parent labels.

---

# 26. Tabs

Tabs dùng cho các views ngang hàng trong cùng resource.

Không dùng tabs cho workflow tuần tự.

Tabs phải:

- Keyboard accessible.
- Deep-linkable khi cần.
- Preserve selected state qua URL.
- Không vượt quá số lượng hợp lý.

---

# 27. Stepper

Stepper dùng cho workflow tuần tự.

Step states:

```text
upcoming
current
completed
error
blocked
```

Không dùng stepper cho random tabs.

---

# 28. Buttons

Button variants:

```text
primary
secondary
outline
ghost
destructive
link
```

Button sizes:

```text
small
medium
large
icon
```

Button states:

```text
default
hover
active
focus
disabled
loading
```

---

# 29. Primary action

Mỗi page/dialog nên có tối đa một primary action nổi bật.

Nhiều hành động quan trọng nên chuyển secondary/menu.

---

# 30. Destructive actions

Destructive action phải:

- Dùng destructive style.
- Có consequence.
- Có confirmation.
- Có reason khi required.
- Không đặt cạnh primary action dễ nhầm.
- Không auto-focus destructive button trong dialog.

---

# 31. Icon buttons

Icon button phải có:

- Accessible name.
- Tooltip khi meaning không rõ.
- Focus state.
- Touch target đủ lớn.

Không dùng icon-only cho critical action nếu người dùng khó hiểu.

---

# 32. Links

Link dùng cho navigation.

Button dùng cho action.

Không dùng button style để link nếu semantics bị sai.

External link cần indicator nếu phù hợp.

---

# 33. Inputs

Input component phải hỗ trợ:

- Label.
- Placeholder.
- Description.
- Required.
- Error.
- Disabled.
- Read-only.
- Prefix/suffix.
- Masked.
- Clear action.
- Character count.

---

# 34. Labels

Label phải:

- Luôn visible cho critical form.
- Không thay hoàn toàn bằng placeholder.
- Liên kết input.
- Có required indicator.
- Có help text khi cần.

---

# 35. Placeholder

Placeholder chỉ là ví dụ/hint.

Không dùng placeholder làm label.

---

# 36. Help text

Help text giải thích:

- Format.
- Business meaning.
- Consequence.
- Privacy.
- Validation.

Không dài quá mức.

---

# 37. Validation messages

Validation message phải:

- Specific.
- Actionable.
- Không chỉ “Invalid”.
- Không expose internal rule không cần thiết.
- Gắn đúng field.
- Accessible.

---

# 38. Read-only fields

Read-only field phải khác disabled field.

Read-only:

- Có thể copy.
- Không chỉnh sửa.
- Vẫn readable.

Disabled:

- Không thể tương tác.
- Có lý do khi cần.

---

# 39. Select

Select dùng khi options nhỏ/vừa.

Large options dùng:

- Combobox.
- Searchable select.
- Async lookup.

Không render hàng nghìn options cùng lúc.

---

# 40. Combobox

Combobox phải hỗ trợ:

- Search.
- Keyboard.
- Loading.
- Empty.
- Clear.
- Selected state.
- Async results.
- Scope-aware options.

---

# 41. Multi-select

Multi-select dùng cho bounded selections.

Không dùng multi-select nếu business relationship cần form riêng hoặc table.

---

# 42. Date picker

Date picker phải phân biệt:

- Business date.
- Instant.
- Date range.
- Effective period.

Không convert business date sang timezone instant sai meaning.

---

# 43. Time picker

Time picker cần:

- Local time context.
- Timezone label.
- 24-hour or locale format.
- Validation.

---

# 44. Money input

Money input phải:

- Hiển thị currency.
- Không dùng float.
- Có thousand separators.
- Preserve precision.
- Parse safely.
- Validate min/max.
- Align right khi phù hợp.

---

# 45. Percentage input

Phải rõ representation:

```text
15%
```

không ambiguity giữa `15` và `0.15`.

---

# 46. Phone input

Phone input:

- Country code.
- Normalization.
- Verification state.
- Masking.
- Duplicate warning.
- Privacy notice khi cần.

---

# 47. Address input

Address nên chia field có cấu trúc.

Không nhét toàn bộ vào một textarea nếu cần query/validation.

---

# 48. Textarea

Textarea có:

- Character count.
- Max length.
- Auto-resize optional.
- Validation.
- No rich text nếu không cần.

---

# 49. Rich text

Chỉ dùng khi business cần.

Phải:

- Sanitize.
- Limit formatting.
- No script.
- No arbitrary embed.
- Accessible output.

---

# 50. Checkbox

Checkbox dùng cho boolean independent choices.

Không dùng checkbox cho single-selection options.

---

# 51. Radio group

Radio dùng cho mutually exclusive options.

Options phải có descriptive labels.

---

# 52. Switch

Switch dùng cho immediate binary settings.

Không dùng switch cho destructive/complex action.

Không dùng switch nếu save không tức thời.

---

# 53. Form groups

Group fields theo:

- Business concept.
- Privacy.
- Workflow step.
- Data ownership.

Không group chỉ theo database table.

---

# 54. Form layout

Desktop:

- 1–2 columns.
- Critical forms ưu tiên 1 column.
- Related compact fields có thể same row.

Mobile:

- Single column.

---

# 55. Inline edit

Inline edit chỉ cho:

- Small low-risk fields.
- Clear save/cancel.
- Version conflict handling.
- Permission.

Không dùng inline edit cho financial, contract hoặc approval-critical fields.

---

# 56. Tables

Table là component trọng yếu.

Phải hỗ trợ:

- Header.
- Sorting.
- Filtering.
- Pagination.
- Selection.
- Actions.
- Loading.
- Empty.
- Error.
- Sticky columns.
- Responsive fallback.
- Accessibility.

---

# 57. Table density

Density modes:

```text
comfortable
compact
```

Không tạo custom density per feature.

---

# 58. Table alignment

- Text: left.
- Numbers: right.
- Status: left/center tùy system.
- Date/time: left.
- Actions: right.
- Checkbox: center.

---

# 59. Table sorting

Sortable column phải có:

- Visual indicator.
- Keyboard action.
- Clear current order.
- Stable sorting.
- Server-side behavior.

---

# 60. Table filters

Filters có thể nằm:

- Toolbar.
- Column header.
- Side panel.

Active filters phải visible.

Có clear all.

---

# 61. Table row actions

Row actions:

- Primary inline action nếu rất thường dùng.
- Secondary trong overflow menu.
- Permission-aware.
- State-aware.
- Destructive separated.

---

# 62. Bulk actions

Bulk toolbar chỉ xuất hiện khi selection > 0.

Hiển thị:

- Count.
- Selected scope.
- Available actions.
- Clear selection.

---

# 63. Empty table

Empty state phân biệt:

```text
No records
No results
No permission
Not configured
Loading sync
```

---

# 64. Responsive tables

Trên mobile:

- Priority columns.
- Horizontal scroll.
- Card representation.
- Expand details.
- Sticky identifiers.

Không cố hiển thị tất cả columns nhỏ xíu.

---

# 65. Lists

List dùng cho:

- Timeline.
- Notifications.
- Search results.
- Activity feed.
- Mobile representation.

List item có hierarchy rõ.

---

# 66. Status badge

Status Badge component phải lấy config từ centralized registry.

Props concept:

```text
status
label
tone
icon
size
```

Feature không tự định nghĩa màu.

---

# 67. Tags

Tags dùng cho metadata ngắn.

Không dùng tag thay status nếu status có workflow meaning.

---

# 68. Chips

Chips dùng cho:

- Active filters.
- Selected values.
- Compact categories.

Removable chip phải keyboard accessible.

---

# 69. Tooltips

Tooltip dùng để giải thích ngắn.

Không dùng tooltip để chứa thông tin bắt buộc.

Tooltip phải accessible và không chỉ hover.

---

# 70. Popovers

Popover dùng cho:

- Filters.
- Date picker.
- Small context details.
- Quick actions.

Không dùng popover cho workflow dài.

---

# 71. Dialogs

Dialog có:

- Title.
- Description.
- Content.
- Actions.
- Focus trap.
- Close behavior.
- Keyboard.

Critical dialog không close khi click outside nếu có nguy cơ mất dữ liệu.

---

# 72. Drawers

Drawer có:

- Clear purpose.
- Header.
- Scrollable body.
- Footer actions.
- Close.
- Responsive size.

---

# 73. Toasts

Toast variants:

```text
success
info
warning
error
```

Toast phải:

- Có concise message.
- Auto-dismiss hợp lý.
- Persistent khi critical.
- Không chứa PII.
- Có action nếu cần.

---

# 74. Alerts

Inline Alert dùng khi message liên quan context/page.

Variants:

```text
info
success
warning
error
```

Critical block phải persistent.

---

# 75. Banners

Banner dùng cho:

- Environment.
- Break-glass.
- Maintenance.
- Security notice.
- System degradation.

Không dùng banner cho message nhỏ.

---

# 76. Skeletons

Skeleton phải gần layout thật.

Không dùng spinner nếu skeleton tốt hơn.

Không animate quá mạnh.

---

# 77. Progress

Progress types:

- Determinate.
- Indeterminate.
- Step progress.
- Job progress.

Nếu process async, hiển thị:

- Status.
- Percentage khi có.
- Current step.
- Estimated/last update khi phù hợp.
- Failure action.

---

# 78. Empty states

Empty state anatomy:

```text
Title
Description
Primary next action
Secondary guidance
Optional illustration
```

Không dùng decorative illustration quá lớn trong enterprise UI.

---

# 79. Error states

Error state anatomy:

```text
What happened
What user can do
Correlation ID
Retry/Back action
Support guidance
```

Không hiển thị stack trace.

---

# 80. Permission-denied states

Permission denied phải:

- Giải thích ngắn.
- Không lộ resource details.
- Có request-access action nếu flow tồn tại.
- Có back navigation.
- Không giả là generic server error.

---

# 81. Not-found states

Not found không phân biệt unauthorized/existing nếu concealment policy.

Message an toàn.

---

# 82. Conflict states

Conflict UI phải:

- Nêu dữ liệu đã thay đổi.
- Cho refresh.
- Cho compare nếu applicable.
- Preserve safe draft.
- Không auto-overwrite.

---

# 83. Stale data states

UI cần hiển thị:

- Last updated.
- Freshness.
- Refresh.
- Sync pending.
- Projection lag nếu relevant.

---

# 84. Readiness panels

Readiness component hiển thị:

- Passed checks.
- Blocking checks.
- Warnings.
- Missing documents.
- Missing permissions.
- Recommended next action.

---

# 85. Approval panels

Approval UI phải có:

- Action.
- Requester.
- Resource.
- Amount/risk.
- Policy.
- Evidence.
- Decision controls.
- Reason.
- SoD warning.

---

# 86. Timeline

Timeline entry gồm:

- Event type.
- Title.
- Time.
- Actor.
- Summary.
- Source link.
- Status.
- Classification.

Không hiển thị full sensitive event payload.

---

# 87. Audit views

Audit screen phải:

- Restricted.
- Filterable.
- Paginated.
- Masked.
- Show correlation.
- Show action/outcome.
- Not expose raw secret.

---

# 88. Dashboard system

Dashboard dùng riêng design rules trong `dashboard-visualization-system.md`.

Design System chỉ định common primitives:

- KPI Card.
- Chart Container.
- Legend.
- Filter Bar.
- Drill-down Table.
- Freshness Indicator.
- Alert Widget.

---

# 89. KPI card

KPI Card anatomy:

```text
Label
Primary value
Unit/currency
Comparison
Trend
Period
Freshness
Drill action
```

Không hiển thị số không có context.

---

# 90. Charts

Charts phải:

- Có title.
- Có unit.
- Có period.
- Có legend.
- Có accessible summary.
- Có tooltip.
- Có empty/error/loading.
- Không misleading axis.
- Không 3D.

---

# 91. Data tables in dashboards

Dashboard table vẫn phải:

- Scope-aware.
- Paginated khi lớn.
- Export permission.
- Drill-down.
- Freshness.

---

# 92. Map components

Nếu có map:

- Không auto-load heavy map trên mọi page.
- Privacy review.
- Accessible alternative.
- Location precision theo permission.
- No exact sensitive address exposure.

---

# 93. Calendar components

Calendar views:

- Day.
- Week.
- Month.
- Agenda.

Phải hiển thị timezone.

Appointments có status and ownership.

Không dùng màu duy nhất để phân biệt.

---

# 94. Kanban

Kanban chỉ dùng khi pipeline semantics rõ.

Requirements:

- Keyboard alternative.
- Drag confirmation khi critical.
- Server mutation.
- State validation.
- Optimistic update chỉ khi safe.
- Accessible list alternative.

---

# 95. Command palette

Command palette có:

- Search navigation.
- Safe quick actions.
- Permission filtering.
- Keyboard shortcut.
- No critical direct execution without confirmation.

---

# 96. Global search

Global search component:

- Scope-aware.
- Debounced.
- Grouped by type.
- Masked results.
- Keyboard navigation.
- Safe recent history.

---

# 97. Notifications center

Notification item:

- Type.
- Title.
- Summary.
- Time.
- Read state.
- Resource link.
- Action.
- Safe content.

---

# 98. User menu

User menu có:

- Profile.
- Active role/context.
- Preferences.
- Security/session.
- Logout.

Không hiển thị sensitive token info.

---

# 99. Environment indicator

Non-production phải hiển thị environment rõ.

Break-glass session phải có persistent banner.

---

# 100. Responsive design

## Mobile

- Single-column.
- Bottom actions khi cần.
- Drawers.
- Compact navigation.
- Simplified tables.

## Tablet

- Collapsible sidebar.
- Two-column forms khi phù hợp.
- Responsive detail panels.

## Desktop

- Full navigation.
- Dense data tables.
- Multi-panel layout.

---

# 101. Touch targets

Interactive target tối thiểu theo accessibility/mobile standards.

Không tạo icon button quá nhỏ.

---

# 102. Accessibility

Baseline:

```text
WCAG 2.1 AA
```

Mọi component phải:

- Semantic HTML.
- Keyboard usable.
- Screen-reader labels.
- Focus visible.
- Contrast.
- Error announcements.
- Reduced motion.

---

# 103. Focus states

Focus phải:

- Rõ.
- Không bị remove.
- Dùng token.
- Không phụ thuộc browser default nếu không đủ.

---

# 104. Keyboard patterns

- Button: Enter/Space.
- Link: Enter.
- Dialog: Escape.
- Tabs: Arrow keys.
- Menu: Arrow keys/Escape.
- Combobox: Arrow/Enter/Escape.
- Table selection: keyboard accessible.

---

# 105. Screen-reader labels

Icon-only controls cần `aria-label`.

Inputs cần label.

Status change cần live region khi relevant.

---

# 106. Color contrast

Text, controls, icons và status cần đạt contrast baseline.

Disabled content vẫn phải readable.

---

# 107. Reduced motion

Respect:

```css
@media (prefers-reduced-motion: reduce)
```

Không bắt buộc user xem animation.

---

# 108. Content design principles

Content phải:

- Ngắn.
- Chính xác.
- Dùng domain terms.
- Actionable.
- Không mơ hồ.
- Không technical jargon không cần.

---

# 109. Button labels

Dùng động từ cụ thể:

```text
Tạo khách hàng
Xác nhận booking
Phát hành biên nhận
Phê duyệt hoàn tiền
```

Không dùng:

```text
OK
Submit
Process
Do it
```

---

# 110. Error copy

Error message:

- Nói điều gì xảy ra.
- Tại sao nếu safe.
- Người dùng làm gì tiếp.
- Không đổ lỗi.
- Không technical.

---

# 111. Confirmation copy

Confirmation phải nêu consequence.

Ví dụ:

```text
Sau khi phát hành, biên nhận không thể chỉnh sửa. Bạn vẫn muốn tiếp tục?
```

---

# 112. Empty-state copy

Phân biệt:

- Chưa có record.
- Không khớp filter.
- Chưa cấu hình.
- Không có quyền.

---

# 113. Localization

UI language đầu tiên:

```text
Vietnamese
```

Identifiers/code vẫn English.

Tất cả reusable strings phải qua localization architecture.

---

# 114. Date and time copy

Display:

- Exact datetime.
- Timezone.
- Relative time optional.

Không dùng “hôm nay” nếu dễ gây ambiguity trong cross-timezone context mà không có exact time.

---

# 115. Money copy

Luôn hiển thị currency.

Không chỉ hiển thị:

```text
1.000.000
```

mà không biết VND/USD.

---

# 116. Status labels

Status code và display label tách riêng.

Code:

```text
PARTIALLY_PAID
```

Label:

```text
Đã thanh toán một phần
```

---

# 117. Permission copy

Không hiển thị internal permission code cho end user trừ admin diagnostics.

User-facing:

```text
Bạn không có quyền phát hành biên nhận.
```

Admin diagnostics có thể xem:

```text
contract.receipt.issue
```

---

# 118. Design-system component API

Mỗi shared component phải có:

- Clear props.
- Variants.
- Sizes.
- States.
- Accessibility contract.
- Usage examples.
- Do/Don’t.
- Tests.
- Story/catalog entry.

---

# 119. Component variants governance

Không thêm variant chỉ cho một screen nếu có thể compose.

Variant mới phải:

- Reusable.
- Named semantically.
- Reviewed.
- Token-based.
- Tested.

---

# 120. Component ownership

Shared Design System owner duy trì:

- Button.
- Input.
- Select.
- Dialog.
- Table primitives.
- Badge.
- Alert.
- Toast.
- Tabs.
- Pagination.
- Skeleton.
- Layout primitives.

Feature owner duy trì business components:

- Booking Readiness Panel.
- Payment Allocation Summary.
- Customer Identity Resolution Panel.

---

# 121. Primitive vs business component

Primitive:

```text
Button
Input
Badge
Dialog
```

Business component:

```text
CommercialLockStatusPanel
ContractApprovalSummary
CommissionVestingTable
```

Không đưa business component vào primitive package.

---

# 122. Design System package structure

```text
frontend/design-system/
├── src/
│   ├── components/
│   ├── primitives/
│   ├── tokens/
│   ├── icons/
│   ├── hooks/
│   ├── utilities/
│   └── index.ts
├── stories/
├── tests/
└── README.md
```

---

# 123. Styling standards

- Tailwind CSS theo tokens.
- Utility composition hợp lý.
- No arbitrary values nếu token tồn tại.
- No inline styles trừ dynamic computed style.
- No CSS leakage.
- No global feature styles.

---

# 124. Component classes

Class composition dùng approved utility.

Không hard-code long duplicated class strings trong nhiều nơi.

---

# 125. Dark mode

Chỉ triển khai nếu Product/Design Scope phê duyệt.

Nếu có:

- Tokens phải đầy đủ.
- Contrast tests.
- Charts.
- Forms.
- Tables.
- Images.
- System preference.

Không làm dark mode nửa vời.

---

# 126. Print styles

Cần cho:

- Contract preview.
- Receipt.
- Reports.
- Evidence.

Print layout phải:

- Hide navigation.
- Preserve table headers.
- Show pagination/page breaks.
- No interactive controls.
- Classification/watermark nếu required.

---

# 127. PDF/export appearance

UI preview và generated export có thể khác.

Generated document thuộc Documents/Reporting contracts.

Không dùng browser screenshot làm official document nếu không approved.

---

# 128. Loading strategy

Use:

- Skeleton cho layout.
- Spinner cho small inline action.
- Progress cho jobs.
- Deferred loading cho secondary panels.

Không block whole page nếu chỉ một widget loading.

---

# 129. Empty/loading/error consistency

Mọi data component phải implement cùng patterns.

Không để mỗi feature tự viết message/layout riêng.

---

# 130. Permission-driven actions

Action component có thể nhận:

```text
allowed
reason
loading
disabled
```

Nhưng không thay backend security.

---

# 131. Destructive confirmation patterns

Levels:

```text
Low risk → simple confirm
Medium risk → consequence + confirm
High risk → reason + reauthentication + approval
```

---

# 132. Sensitive-data reveal

Nếu hỗ trợ reveal masked value:

- Separate permission.
- Reauthentication nếu required.
- Time-bound.
- Audit.
- No persistent cache.
- Clear visual state.

---

# 133. Copy-to-clipboard

Copy sensitive data phải:

- Permission-aware.
- Audit nếu required.
- Show success.
- Avoid exposing hidden field.
- Clear clipboard cannot be guaranteed; warn when relevant.

---

# 134. Drag and drop

Drag/drop phải có:

- Keyboard alternative.
- Clear drop target.
- Undo/confirm khi important.
- Server validation.
- No inaccessible-only behavior.

---

# 135. Inline notifications

Use inline status for:

- Auto-save.
- Sync.
- Validation.
- Process state.

Không dùng toast cho mọi auto-save.

---

# 136. Auto-save

Auto-save chỉ cho safe drafts.

Requirements:

- Show saving/saved/error.
- Debounce.
- Version conflict.
- Retry.
- No silent loss.
- Not for issued/approved/financial records.

---

# 137. Unsaved changes

Warn when:

- User navigates away.
- Closes dialog.
- Session expires.
- Switches tabs/routes.

Không warn nếu no changes.

---

# 138. Session timeout

UI phải:

- Warn.
- Allow reauth.
- Preserve safe non-sensitive draft.
- Clear sensitive state.
- Avoid duplicate submission.

---

# 139. Offline/network degradation

Show:

- Offline indicator.
- Retry.
- Read-only cached data label.
- No critical offline mutation.

---

# 140. Data freshness

Freshness indicator:

```text
Updated 2 minutes ago
Real-time
Delayed
Syncing
Stale
```

Official dashboards phải hiển thị freshness.

---

# 141. Eventual consistency UX

Khi cross-context process:

- Show pending.
- Show current step.
- Show failed/retry.
- Show reconciliation required.
- Do not show final success too early.

---

# 142. Process status component

Common statuses:

```text
QUEUED
RUNNING
WAITING
COMPLETED
FAILED
CANCELLED
```

Component có icon/tone/label.

---

# 143. Security indicators

UI có thể hiển thị:

- Restricted data icon.
- Break-glass banner.
- Audit-required action.
- Masked field.
- External sharing warning.
- Export classification.

Không dùng fear-inducing copy quá mức.

---

# 144. Environment banners

Non-production:

```text
LOCAL
TEST
STAGING
UAT
```

Production không cần banner mặc định.

Break-glass banner luôn hiển thị.

---

# 145. Design System testing

Phải có:

- Unit tests.
- Component tests.
- Accessibility tests.
- Visual regression.
- Keyboard tests.
- Responsive stories.
- Theme tests nếu applicable.

---

# 146. Story catalog

Mỗi shared component cần stories cho:

```text
default
variants
sizes
disabled
loading
error
long content
empty
responsive
accessibility
```

---

# 147. Visual regression

Baseline cho:

- Buttons.
- Inputs.
- Dialogs.
- Tables.
- Alerts.
- Navigation.
- Dashboard primitives.
- Responsive layouts.

Không update snapshot mù.

---

# 148. Accessibility testing

Automated:

- axe.
- Semantic roles.
- Labels.
- Contrast where possible.

Manual:

- Keyboard.
- Screen reader.
- Zoom 200%.
- Reduced motion.
- High contrast mode nếu supported.

---

# 149. Cross-browser testing

Critical Design System components test trên:

- Chrome.
- Edge.
- Firefox.
- Safari.

---

# 150. Performance testing

Components phải tránh:

- Excessive rerender.
- Heavy DOM.
- Large CSS.
- Unnecessary JS.
- Blocking fonts.
- Huge icon packages.

Tables/charts cần performance benchmark.

---

# 151. Design QA checklist

## Visual

- Tokens?
- Spacing?
- Typography?
- Alignment?
- Status colors?

## Interaction

- Hover?
- Focus?
- Disabled?
- Loading?
- Error?
- Conflict?

## Responsive

- Mobile?
- Tablet?
- Desktop?

## Accessibility

- Keyboard?
- Screen reader?
- Contrast?
- Labels?

## Domain

- Correct status?
- Correct action?
- No misleading UI?
- Permission?
- Masking?

---

# 152. Design review checklist

1. Có dùng component hiện có?
2. Có tạo duplicate pattern?
3. Có hierarchy rõ?
4. Có primary action rõ?
5. Có loading/empty/error?
6. Có accessibility?
7. Có responsive?
8. Có permission/masking?
9. Có consequence cho critical action?
10. Có design tokens?
11. Có test/stories?
12. Có docs?

---

# 153. Design anti-patterns bị cấm

1. Hard-coded colors.
2. Random spacing.
3. Duplicate button/input.
4. Feature-specific modal style.
5. Color-only status.
6. Placeholder thay label.
7. Clickable div.
8. Tiny touch target.
9. No focus state.
10. Generic “No data”.
11. Toast-only form error.
12. Generic status dropdown.
13. Overuse cards.
14. Heavy gradients.
15. 3D charts.
16. Hidden destructive action consequence.
17. Non-responsive table.
18. Hard-coded Vietnamese in reusable component when localization required.
19. Inaccessible drag/drop.
20. Inconsistent status colors.
21. Arbitrary z-index.
22. `9999`.
23. Overuse animation.
24. Duplicate design token.
25. Business meaning simplified incorrectly.

---

# 154. AI Agent Design System protocol

Trước khi tạo hoặc sửa UI, AI Agent phải:

1. Đọc Design System.
2. Kiểm tra component có sẵn.
3. Xác định semantic purpose.
4. Xác định variants/states.
5. Xác định accessibility.
6. Xác định responsive behavior.
7. Xác định permission/masking.
8. Dùng tokens.
9. Viết tests/stories.
10. Review visual consistency.
11. Không tự tạo style riêng.
12. Update docs nếu thêm pattern mới.

---

# 155. AI Agent prohibited design behaviors

AI Agent không được:

1. Tạo component trùng.
2. Hard-code color/spacing.
3. Tự thêm design library.
4. Bỏ accessibility.
5. Bỏ error/loading states.
6. Tự đổi status color.
7. Tự thêm variant chỉ cho một screen.
8. Tạo random animation.
9. Dùng decorative effect quá mức.
10. Báo Done khi visual/accessibility tests fail.
11. Tự thay domain label.
12. Tự rút gọn trạng thái làm sai meaning.

---

# 156. Definition of Ready cho Design System change

Change chỉ Ready khi:

1. Use case rõ.
2. Component ownership rõ.
3. Existing component gap rõ.
4. Variant/state rõ.
5. Tokens rõ.
6. Accessibility rõ.
7. Responsive rõ.
8. Test/story plan rõ.
9. No duplicate pattern.
10. Design Owner review khi required.

---

# 157. Definition of Done cho Design System change

Change chỉ Done khi:

1. Component implemented.
2. Tokens used.
3. Variants complete.
4. States complete.
5. Accessibility pass.
6. Responsive pass.
7. Tests pass.
8. Stories complete.
9. Visual regression reviewed.
10. Documentation updated.
11. No duplicate component.
12. Frontend build pass.
13. Acceptance evidence recorded.

---

# 158. Component documentation template

```markdown
# Component Name

## Purpose

## When to Use

## When Not to Use

## Anatomy

## Variants

## Sizes

## States

## Props

## Accessibility

## Responsive Behavior

## Content Guidelines

## Examples

## Do

## Don’t

## Tests
```

---

# 159. Governance

Design System changes phải:

- Có owner.
- Có review.
- Có changelog.
- Có migration plan nếu breaking.
- Không đổi visual semantics âm thầm.
- Không remove component khi consumers chưa migrate.

---

# 160. Versioning

Design System package dùng semantic versioning.

Breaking changes:

- Rename prop.
- Remove variant.
- Change behavior.
- Change token meaning.
- Change status semantics.
- Change accessibility contract.

---

# 161. Deprecation

Deprecated component/prop phải có:

- Replacement.
- Warning.
- Migration guide.
- Sunset version.
- Consumer inventory.

Không giữ deprecated component vô thời hạn.

---

# 162. Design System metrics

Có thể theo dõi:

- Component reuse.
- Duplicate components.
- Accessibility defects.
- Visual regressions.
- Bundle size.
- Deprecated usage.
- Design QA defects.
- Time to implement screens.

---

# 163. Required design documentation

```text
docs/design/design-system.md
docs/design/design-tokens.md
docs/design/navigation-and-information-architecture.md
docs/design/dashboard-visualization-system.md
docs/design/accessibility-guidelines.md
docs/design/content-guidelines.md
docs/design/component-inventory.md
docs/design/design-system-changelog.md
```

---

# 164. Change Log

## Version 1.0.0 — 2026-07-24

- Thiết lập design principles và visual language.
- Khóa tokens, colors, typography, spacing và motion.
- Khóa layout, navigation và page anatomy.
- Khóa forms, tables, feedback và overlays.
- Khóa dashboard, timeline, approval và readiness patterns.
- Khóa responsive và accessibility.
- Khóa content design và localization.
- Khóa Design System component governance.
- Khóa testing, visual regression và AI Agent protocol.
- Khóa Definition of Ready và Definition of Done.

---

# 165. Kết luận

Design System của `crm_bds_ai` phải giúp toàn bộ sản phẩm vận hành như một hệ thống thống nhất:

```text
Consistent Visual Language
+ Accurate Domain Representation
+ Accessible Interaction
+ Predictable Components
+ Safe Critical Actions
+ Responsive Enterprise Workflows
+ Reusable Design Tokens
```

Nguyên tắc tối cao:

> Mọi màn hình phải giống như cùng một sản phẩm, mọi trạng thái phải dễ hiểu, mọi hành động quan trọng phải an toàn và mọi component phải accessible ngay từ đầu.
