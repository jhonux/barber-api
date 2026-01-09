"""fix null is_active values

Revision ID: 668af6a66a46
Revises: 95abf48842be
Create Date: 2026-01-07 23:09:05.803757

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '668af6a66a46'
down_revision: Union[str, Sequence[str], None] = '95abf48842be'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
