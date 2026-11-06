"""empty message

Revision ID: fc05391c7d56
Revises: 9485b04a57c8
Create Date: 2026-11-06 13:41:15.732090

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fc05391c7d56'
down_revision: Union[str, Sequence[str], None] = '9485b04a57c8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
