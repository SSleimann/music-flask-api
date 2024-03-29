"""admin

Revision ID: 07f69502fe51
Revises: 05220f32d603
Create Date: 2023-08-05 15:00:05.186353

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '07f69502fe51'
down_revision = '05220f32d603'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('admin', sa.Boolean(), nullable=True))
        batch_op.drop_column('is_admin')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('is_admin', sa.BOOLEAN(), nullable=True))
        batch_op.drop_column('admin')

    # ### end Alembic commands ###
