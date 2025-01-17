"""empty message

Revision ID: 2cbeeca1e60a
Revises: 
Create Date: 2025-01-05 14:59:08.082922

"""

import datetime
from typing import Sequence, Union
from uuid import uuid4

from alembic import op
import sqlalchemy as sa

from src.auth.jwt import pwd_context
from src.core.models.default_values import get_current_time
from src.core.models.users import Roles, Grade
from src.project import settings

# revision identifiers, used by Alembic.
revision: str = "2cbeeca1e60a"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "tasks",
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("description", sa.String(), nullable=True),
        sa.Column("price", sa.Integer(), nullable=False),
        sa.Column("created_by", sa.String(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.Column("finished_by", sa.String(), nullable=True),
        sa.Column("finished_at", sa.DateTime(), nullable=True),
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    table_users = op.create_table(
        "users",
        sa.Column("username", sa.String(), nullable=False),
        sa.Column("hashed_password", sa.String(), nullable=False),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("role", sa.Enum("admin", "user", name="roles"), nullable=False),
        sa.Column(
            "grade",
            sa.Enum("Noobie", "Adept", "Expert", "Veteran", "Legend", name="grade"),
            nullable=False,
        ),
        sa.Column("count", sa.Integer(), nullable=False),
        sa.Column("registered_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.Column("is_deleted", sa.Boolean(), nullable=False),
        sa.Column("is_verified", sa.Boolean(), nullable=False),
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )

    op.bulk_insert(
        table_users,
        [
            {
                "username": settings.MASTER_ADM_NAME,
                "hashed_password": pwd_context.hash(settings.MASTER_ADM_PWD),
                "email": settings.MASTER_ADM_EMAIL,
                "role": "admin",
                "grade": "Legend",
                "count": 0,
                "registered_at": get_current_time(),
                "updated_at": None,
                "is_deleted": False,
                "is_verified": True,
                "id": uuid4(),
            }
        ],
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("users")
    op.drop_table("tasks")
    # ### end Alembic commands ###
