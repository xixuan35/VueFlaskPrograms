"""empty message

Revision ID: 87cd2aab2270
Revises: c6b96b2c1007
Create Date: 2023-05-20 17:45:43.014109

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '87cd2aab2270'
down_revision = 'c6b96b2c1007'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('t_roles',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=32), nullable=False),
    sa.Column('desc', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('t_roles')
    # ### end Alembic commands ###
