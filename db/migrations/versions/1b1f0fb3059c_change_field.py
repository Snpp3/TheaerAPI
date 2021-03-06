"""change field

Revision ID: 1b1f0fb3059c
Revises: a5b53f3163ad
Create Date: 2020-12-20 22:52:52.403809

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '1b1f0fb3059c'
down_revision = 'a5b53f3163ad'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('contracts', sa.Column('salary', sa.FLOAT(), nullable=False))
    op.drop_column('contracts', 'salary_per_year')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('contracts', sa.Column('salary_per_year', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=False))
    op.drop_column('contracts', 'salary')
    # ### end Alembic commands ###
