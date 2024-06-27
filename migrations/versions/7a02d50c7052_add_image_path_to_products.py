"""Add image_path to Products

Revision ID: 7a02d50c7052
Revises: 35208eedc4fb
Create Date: 2024-06-27 11:05:58.279849

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7a02d50c7052'
down_revision = 'bf84e241b907'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('Products', schema=None) as batch_op:
        batch_op.add_column(sa.Column('image_path', sa.String(length=255), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('Products', schema=None) as batch_op:
        batch_op.drop_column('image_path')

    # ### end Alembic commands ###
