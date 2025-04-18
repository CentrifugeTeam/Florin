"""add unique

Revision ID: e6b1b233354e
Revises: 13208e8b4b71
Create Date: 2025-03-03 15:38:34.790152

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = 'e6b1b233354e'
down_revision: Union[str, None] = '13208e8b4b71'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'calendar_events', ['do_on', 'user_plant_id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'calendar_events', type_='unique')
    # ### end Alembic commands ###
