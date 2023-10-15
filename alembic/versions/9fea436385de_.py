"""empty message

Revision ID: 9fea436385de
Revises: 
Create Date: 2023-09-21 06:24:47.593471

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9fea436385de'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('menus',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('title', sa.String(length=30), nullable=False),
    sa.Column('description', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('title')
    )
    op.create_table('submenus',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('title', sa.String(length=30), nullable=False),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('menu_id', sa.UUID(), nullable=False),
    sa.ForeignKeyConstraint(['menu_id'], ['menus.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('title')
    )
    op.create_table('dishes',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('title', sa.String(length=30), nullable=False),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('price', sa.Numeric(precision=10, scale=2), nullable=False),
    sa.Column('submenu_id', sa.UUID(), nullable=False),
    sa.ForeignKeyConstraint(['submenu_id'], ['submenus.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('title')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('dishes')
    op.drop_table('submenus')
    op.drop_table('menus')
    # ### end Alembic commands ###