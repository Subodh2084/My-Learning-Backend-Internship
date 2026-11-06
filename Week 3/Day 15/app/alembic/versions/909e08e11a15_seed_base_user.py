"""seed base user

Revision ID: 909e08e11a15
Revises: a374e4784d00
Create Date: 2026-11-06 13:41:26.461749

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '909e08e11a15'
down_revision: Union[str, Sequence[str], None] = 'a374e4784d00'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
