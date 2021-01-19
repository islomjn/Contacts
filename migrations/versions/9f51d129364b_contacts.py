"""Contacts

Revision ID: 9f51d129364b
Revises: 
Create Date: 2021-01-18 20:42:19.522784

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9f51d129364b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
      'contacts',
      sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
      sqlalchemy.Column("name", sqlalchemy.String),
      sqlalchemy.Column("number", sqlalchemy.String),
    )

def downgrade():
    op.drop_table('conctacts')