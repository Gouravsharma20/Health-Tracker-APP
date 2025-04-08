"""Add benefits to Membership

Revision ID: 1dde5311a6e8
Revises: dad7556c629a
Create Date: 2025-04-08 13:22:56.886250

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1dde5311a6e8'
down_revision: Union[str, None] = 'dad7556c629a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('memberships', sa.Column('benefits', sa.JSON(), nullable=False))
    op.add_column('memberships', sa.Column('owner_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'memberships', 'owners', ['owner_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'memberships', type_='foreignkey')
    op.drop_column('memberships', 'owner_id')
    op.drop_column('memberships', 'benefits')
    # ### end Alembic commands ###
