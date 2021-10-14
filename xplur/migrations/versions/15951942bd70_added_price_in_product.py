"""added price in product

Revision ID: 15951942bd70
Revises: fc56ead196cf
Create Date: 2021-10-14 15:32:08.624675

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '15951942bd70'
down_revision = 'fc56ead196cf'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('product', sa.Column('price', sa.Float(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('product', 'price')
    # ### end Alembic commands ###