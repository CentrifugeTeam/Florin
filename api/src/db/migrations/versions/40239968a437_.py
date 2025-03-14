"""empty message

Revision ID: 40239968a437
Revises: 8ac6552649ef
Create Date: 2025-02-26 18:36:51.542260

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = '40239968a437'
down_revision: Union[str, None] = '8ac6552649ef'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('plants', sa.Column('genus', sqlmodel.sql.sqltypes.AutoString(), nullable=False))
    op.drop_column('plants', 'genius')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('plants', sa.Column('genius', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.drop_column('plants', 'genus')
    # ### end Alembic commands ###
