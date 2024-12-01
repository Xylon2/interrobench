"""count api calls

Revision ID: c9766e6a02b8
Revises: fb084adcc574
Create Date: 2024-12-01 10:20:52.674053

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c9766e6a02b8'
down_revision: Union[str, None] = 'fb084adcc574'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('runs', sa.Column('total_api_calls', sa.Integer(), nullable=True))
    op.add_column('attempts', sa.Column('api_calls', sa.Integer(), nullable=True))

def downgrade() -> None:
    op.drop_column('runs', 'total_api_calls')
    op.drop_column('attempts', 'api_calls')
