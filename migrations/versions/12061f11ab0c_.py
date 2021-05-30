"""empty message

Revision ID: 12061f11ab0c
Revises: 16eb6f75cdfc
Create Date: 2021-05-30 02:48:03.292299

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '12061f11ab0c'
down_revision = '16eb6f75cdfc'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('session_user', sa.Column('submitted', sa.Boolean(), nullable=False, server_default="false"))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('session_user', 'submitted')
    # ### end Alembic commands ###