"""Sprint 1 Alembic baseline (empty/technical revision).

Revision ID: 0001_baseline
Revises:
Create Date: 2026-08-06

This revision deliberately creates NO business schema or table (Lead, Party,
Product, Contract, Revenue, ... are Sprint 2+). It only creates the technical
`infra` schema mandated by ADR-003 (PostgreSQL schema per Context + `infra`).
"""

from __future__ import annotations

from alembic import op

revision = "0001_baseline"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Technical schema for infrastructure-owned tables (Sprint 2 reliability
    # foundation will place outbox/inbox/idempotency machinery here).
    op.execute("CREATE SCHEMA IF NOT EXISTS infra")


def downgrade() -> None:
    # CASCADE is safe here because no business data can exist under `infra` yet.
    op.execute("DROP SCHEMA IF EXISTS infra CASCADE")
