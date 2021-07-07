"""empty message

Revision ID: c3c05bb3b3d4
Revises: 73e7a80503e9
Create Date: 2021-07-07 18:44:26.281090

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'c3c05bb3b3d4'
down_revision = '73e7a80503e9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('log',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('token', sa.String(), nullable=False),
    sa.Column('proctoring_logs', sa.JSON(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_log_token'), 'log', ['token'], unique=False)
    op.drop_table('logs')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('logs',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('proctoring_logs', postgresql.JSON(astext_type=sa.Text()), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='logs_pkey')
    )
    op.drop_index(op.f('ix_log_token'), table_name='log')
    op.drop_table('log')
    # ### end Alembic commands ###
