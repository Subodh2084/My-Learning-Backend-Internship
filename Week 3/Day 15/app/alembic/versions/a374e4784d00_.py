"""empty message

Revision ID: a374e4784d00
Revises: fc05391c7d56
Create Date: 2026-11-06 13:41:22.356576

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a374e4784d00'
down_revision: Union[str, Sequence[str], None] = 'fc05391c7d56'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
