"""Make email non-unique in clients

Revision ID: 396deb5904a3
Revises: dfd28bee5964
Create Date: 2025-04-07 15:03:31.977216
"""

from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '396deb5904a3'
down_revision: Union[str, None] = 'dfd28bee5964'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with op.batch_alter_table("clients") as batch_op:
        batch_op.alter_column("email", existing_type=sa.String(length=255), nullable=True)
        # Uncomment the next line only if this constraint exists in the DB
        # batch_op.drop_constraint("uq_clients_email", type_="unique")
        batch_op.create_index("ix_clients_email", ["email"])


def downgrade() -> None:
    with op.batch_alter_table("clients") as batch_op:
        batch_op.drop_index("ix_clients_email")
        batch_op.create_unique_constraint("uq_clients_email", ["email"])
