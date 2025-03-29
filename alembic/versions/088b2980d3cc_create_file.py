"""create file

Revision ID: 088b2980d3cc
Revises: ba3a0455e77d
Create Date: 2025-03-29 15:28:09.870232

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = '088b2980d3cc'
down_revision: Union[str, None] = 'ba3a0455e77d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('post', 'media')
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('post', sa.Column('media', mysql.VARCHAR(length=255), nullable=True))
    # ### end Alembic commands ###
