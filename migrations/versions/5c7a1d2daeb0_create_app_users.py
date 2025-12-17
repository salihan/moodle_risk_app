from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "abcd1234abcd"   # <-- put the real hash from the filename here
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "app_users",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("username", sa.String(length=80), nullable=False),
        sa.Column("password_hash", sa.String(length=255), nullable=False),
        sa.Column(
            "role",
            sa.String(length=50),
            nullable=False,
            server_default="advisor",
        ),
        sa.UniqueConstraint("username"),
    )


def downgrade():
    op.drop_table("app_users")
