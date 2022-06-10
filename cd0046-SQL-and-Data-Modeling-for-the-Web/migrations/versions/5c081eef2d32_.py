"""empty message

Revision ID: 5c081eef2d32
Revises: 314ccbd65043
Create Date: 2022-06-10 21:22:10.641262

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5c081eef2d32'
down_revision = '314ccbd65043'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Artist', sa.Column('description', sa.String(length=200), nullable=True))
    op.add_column('Artist', sa.Column('website', sa.String(length=120), nullable=True))
    op.add_column('Artist', sa.Column('talent', sa.Boolean(), nullable=True))
    op.add_column('Venue', sa.Column('website', sa.String(length=120), nullable=True))
    op.add_column('Venue', sa.Column('talent', sa.Boolean(), nullable=True))
    op.add_column('Venue', sa.Column('description', sa.String(length=120), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Venue', 'description')
    op.drop_column('Venue', 'talent')
    op.drop_column('Venue', 'website')
    op.drop_column('Artist', 'talent')
    op.drop_column('Artist', 'website')
    op.drop_column('Artist', 'description')
    # ### end Alembic commands ###
