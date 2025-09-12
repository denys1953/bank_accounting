"""Add relationships

Revision ID: 7c76411a6e58
Revises: db73a20724a9
Create Date: 2025-09-12 15:00:44.726982

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7c76411a6e58'
down_revision: Union[str, Sequence[str], None] = 'db73a20724a9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
