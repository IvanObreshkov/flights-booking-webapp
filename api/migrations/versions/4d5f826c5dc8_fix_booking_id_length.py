"""Fix booking_id length

Revision ID: 4d5f826c5dc8
Revises: 3902dc5837e2
Create Date: 2023-06-18 01:03:44.775096

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '4d5f826c5dc8'
down_revision = '3902dc5837e2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user_bookings', schema=None) as batch_op:
        batch_op.alter_column('booking_id',
               existing_type=mysql.VARCHAR(length=10),
               type_=sa.String(length=255),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user_bookings', schema=None) as batch_op:
        batch_op.alter_column('booking_id',
               existing_type=sa.String(length=255),
               type_=mysql.VARCHAR(length=10),
               existing_nullable=False)

    # ### end Alembic commands ###