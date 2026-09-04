"""Create phone number for user column

Revision ID: 118bf04773bb
Revises: 
Create Date: 2026-09-03 12:47:36.488117

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '118bf04773bb'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('users',sa.Column('Phone_number', sa.String(),nullable=True))
    


def downgrade() -> None:
    op.drop_column('users','Phone_number')
