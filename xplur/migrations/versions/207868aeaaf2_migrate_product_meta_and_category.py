"""migrate product_meta and category

Revision ID: 207868aeaaf2
Revises: 
Create Date: 2021-10-13 18:43:32.464490

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '207868aeaaf2'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('category',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('product',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('SKU', sa.String(length=50), nullable=True),
    sa.Column('name', sa.String(length=120), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('category_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['category_id'], ['category.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('SKU')
    )
    op.create_table('product_meta',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('small_image_url', sa.Text(), nullable=True),
    sa.Column('large_image_url', sa.Text(), nullable=True),
    sa.Column('product_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['product_id'], ['product.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('product_meta')
    op.drop_table('product')
    op.drop_table('category')
    # ### end Alembic commands ###
