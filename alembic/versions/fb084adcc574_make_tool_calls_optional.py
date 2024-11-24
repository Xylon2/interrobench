"""make tool calls optional

Revision ID: fb084adcc574
Revises: 441cbfadb3eb
Create Date: 2024-11-24 15:24:57.602517

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fb084adcc574'
down_revision: Union[str, None] = '441cbfadb3eb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column('attempts', 'tool_calls', nullable=True)


def downgrade() -> None:
    op.alter_column('attempts', 'tool_calls', nullable=False)
