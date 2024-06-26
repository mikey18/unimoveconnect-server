"""added mobolity constrained in ride model

Revision ID: b2598f5d1fb9
Revises: 
Create Date: 2024-03-24 22:53:05.156668

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b2598f5d1fb9'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('ride', sa.Column('mobility_constrained', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('ride', 'mobility_constrained')
    # ### end Alembic commands ###
