"""empty message

Revision ID: 736259f5d11a
Revises: 6b20ac84f556
Create Date: 2023-05-10 21:12:51.604893

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '736259f5d11a'
down_revision = '6b20ac84f556'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('t_users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('update_time', sa.DateTime(), nullable=True))
        batch_op.drop_column('uodate_time')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('t_users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('uodate_time', mysql.DATETIME(), nullable=True))
        batch_op.drop_column('update_time')

    # ### end Alembic commands ###