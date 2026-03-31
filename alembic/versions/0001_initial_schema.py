"""initial schema

Revision ID: 0001_initial_schema
Revises: 
Create Date: 2026-03-31 00:00:00.000000
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '0001_initial_schema'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'user',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('username', sa.String(length=150), nullable=False, unique=True),
        sa.Column('password_hash', sa.String(length=150), nullable=False),
        sa.Column('customer_id', sa.String(length=50), nullable=True),
    )

    op.create_table(
        'product',
        sa.Column('StockCode', sa.String(length=100), primary_key=True),
        sa.Column('Description', sa.String(length=255), nullable=True),
    )

    op.create_table(
        'interaction',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('user.id'), nullable=False),
        sa.Column('stock_code', sa.String(length=100), sa.ForeignKey('product.StockCode'), nullable=False),
        sa.Column('timestamp', sa.DateTime(), nullable=True),
    )


def downgrade():
    op.drop_table('interaction')
    op.drop_table('product')
    op.drop_table('user')
