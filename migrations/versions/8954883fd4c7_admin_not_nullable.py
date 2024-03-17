"""admin not nullable

Revision ID: 8954883fd4c7
Revises: c938b355e1d5
Create Date: 2024-03-17 04:04:31.510972

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8954883fd4c7'
down_revision = 'c938b355e1d5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.alter_column('is_admin',
               existing_type=sa.BOOLEAN(),
               nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.alter_column('is_admin',
               existing_type=sa.BOOLEAN(),
               nullable=True)

    # ### end Alembic commands ###