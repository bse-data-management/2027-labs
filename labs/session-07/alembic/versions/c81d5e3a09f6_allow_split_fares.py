"""allow split fares

Session 4's change, labs/session-04/sql/split_fares.sql: a rider may split a fare
across several cards, so one trip may now have several payments.

Revision ID: c81d5e3a09f6
Revises: 4f2a9c1e7b30
Create Date: 2026-10-06 10:00:00.000000

"""

from collections.abc import Sequence

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "c81d5e3a09f6"
down_revision: str | None = "4f2a9c1e7b30"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.execute("ALTER TABLE payments DROP CONSTRAINT payments_trip_id_key")


def downgrade() -> None:
    # Fails once any trip has two payments, which is to say as soon as the data
    # this revision allows has arrived. Going back means first deciding what to do
    # with those payments, and no migration can decide that.
    op.execute(
        "ALTER TABLE payments ADD CONSTRAINT payments_trip_id_key UNIQUE (trip_id)"
    )
