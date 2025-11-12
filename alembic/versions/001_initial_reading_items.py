from collections.abc import Sequence

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

revision: str = "001_initial"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.execute(
        """
        CREATE TYPE status_enum AS ENUM ('todo', 'in_progress', 'done')
    """
    )

    op.create_table(
        "reading_items",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(length=120), nullable=False),
        sa.Column("url", sa.String(length=2048), nullable=True),
        sa.Column("tags", sa.JSON(), nullable=False),
        sa.Column("priority", sa.Integer(), nullable=False),
        sa.Column(
            "status",
            postgresql.ENUM(
                "todo", "in_progress", "done", name="status_enum", create_type=False
            ),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_reading_items_id"), "reading_items", ["id"], unique=False)
    op.create_index(
        op.f("ix_reading_items_status"), "reading_items", ["status"], unique=False
    )
    op.create_index(
        op.f("ix_reading_items_title"), "reading_items", ["title"], unique=False
    )


def downgrade() -> None:
    op.drop_index(op.f("ix_reading_items_title"), table_name="reading_items")
    op.drop_index(op.f("ix_reading_items_status"), table_name="reading_items")
    op.drop_index(op.f("ix_reading_items_id"), table_name="reading_items")
    op.drop_table("reading_items")
    op.execute("DROP TYPE status_enum")
