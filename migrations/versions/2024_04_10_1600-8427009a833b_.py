"""empty message

Revision ID: 8427009a833b
Revises: c23aa3acfc15
Create Date: 2024-04-10 16:00:47.994571

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8427009a833b'
down_revision: Union[str, None] = 'c23aa3acfc15'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('hashed_password', sa.String(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('role', sa.Enum('admin', 'user', name='roles'), nullable=False),
    sa.Column('grade', sa.Enum('grade_1', 'grade_2', 'grade_3', 'grade_4', 'grade_5', name='grade'), nullable=False),
    sa.Column('count', sa.Integer(), nullable=False),
    sa.Column('registered_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('is_deleted', sa.Boolean(), nullable=False),
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users')
    # ### end Alembic commands ###