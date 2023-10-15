"""empty message

Revision ID: 80f14c1b5bb8
Revises: 7451371decc6, a3174483ed2d
Create Date: 2023-10-15 08:39:14.102735

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '80f14c1b5bb8'
down_revision: Union[str, None] = ('7451371decc6', 'a3174483ed2d')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
