"""Add created and updated at fields to userpubli

Revision ID: 28f8db198b0c
Revises: 0a4c1b32d1bc
Create Date: 2024-12-03 16:04:05.817148

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '28f8db198b0c'
down_revision: Union[str, None] = '0a4c1b32d1bc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
