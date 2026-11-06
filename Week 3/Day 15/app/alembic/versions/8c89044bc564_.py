"""empty message

Revision ID: 8c89044bc564
Revises: 909e08e11a15
Create Date: 2026-11-06 13:42:27.561713

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8c89044bc564'
down_revision: Union[str, Sequence[str], None] = '909e08e11a15'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
