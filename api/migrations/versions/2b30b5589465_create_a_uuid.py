"""Create a uuid

Revision ID: 2b30b5589465
Revises: dd5e334d3619
Create Date: 2023-06-06 15:44:16.878774

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '2b30b5589465'
down_revision = 'dd5e334d3619'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.alter_column('id',
               existing_type=mysql.INTEGER(),
               type_=sa.String(length=36),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.alter_column('id',
               existing_type=sa.String(length=36),
               type_=mysql.INTEGER(),
               existing_nullable=False)

    # ### end Alembic commands ###