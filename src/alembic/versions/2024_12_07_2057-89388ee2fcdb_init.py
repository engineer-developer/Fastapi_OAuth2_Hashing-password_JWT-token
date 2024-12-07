"""Init

Revision ID: 89388ee2fcdb
Revises: 
Create Date: 2024-12-07 20:57:09.186502

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "89388ee2fcdb"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    passwords_table = op.create_table(
        "passwords",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("hashed_password", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_passwords")),
    )
    users_table = op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("username", sa.String(), nullable=True),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column(
            "roles",
            postgresql.ARRAY(
                postgresql.ENUM(
                    "user",
                    "super_user",
                    "teacher",
                    "moderator",
                    "admin",
                    "super_admin",
                    name="role",
                )
            ),
            nullable=False,
        ),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("password_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["password_id"],
            ["passwords.id"],
            name=op.f("fk_users_password_id_passwords"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_users")),
        sa.UniqueConstraint("email", name=op.f("uq_users_email_")),
        sa.UniqueConstraint("password_id", name=op.f("uq_users_password_id_")),
    )

    def insert_value_in_table(table, value: dict):
        op.bulk_insert(table, [value])

    password_value = {
        "hashed_password": "$2b$12$aToTBlTJQXc4np906GD9KO2ckSvVO5dj3x9ZxAi58MxVFa7wOaBmO",
    }
    user_value = {
        "username": "Admin Bob",
        "email": "admin@example.com",
        "roles": ["super_admin"],
        "is_active": True,
        "password_id": 1,
    }
    insert_value_in_table(passwords_table, password_value)
    insert_value_in_table(users_table, user_value)


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("users")
    op.drop_table("passwords")
    op.execute("DROP TYPE role;")
