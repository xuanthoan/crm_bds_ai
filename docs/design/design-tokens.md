# CRM_BDS_AI — DESIGN TOKENS

**Document ID:** `DES-TOK-001`  
**Canonical path:** `docs/design/design-tokens.md`  
**Product:** `crm_bds_ai`  
**Version:** `1.0.0`  
**Status:** `Ready for Review`  
**Owner:** `Design System Owner`  
**Reviewers:** `Frontend Owner, Accessibility Owner`  
**Last reviewed:** `2026-08-05`  
**Classification:** `INTERNAL`


# Principles

Semantic tokens trước component tokens; không hard-code màu/khoảng cách trong feature.

# Token groups

- Color: surface, text, border, action, status, chart semantic.
- Typography: family, size, weight, line height.
- Spacing: 4px base scale.
- Radius, shadow, z-index, motion, breakpoints.
- Density: comfortable/compact cho enterprise tables.

# Status semantics

Success, warning, error, info, neutral không dùng màu đơn độc; luôn có icon/text.

# Implementation

Tokens là source generated cho CSS variables/TypeScript/theme. CI kiểm tra unknown token và direct color literals.
