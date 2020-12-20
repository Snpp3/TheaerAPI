"""salary to actor

Revision ID: a5b53f3163ad
Revises: c53763444cb5
Create Date: 2020-12-20 21:17:42.275492

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a5b53f3163ad'
down_revision = 'c53763444cb5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('actors', sa.Column('salary', sa.FLOAT(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('actors', 'salary')
    # ### end Alembic commands ###