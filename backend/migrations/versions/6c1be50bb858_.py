"""empty message

Revision ID: 6c1be50bb858
Revises: 5a064f9c14d0
Create Date: 2021-08-14 16:15:45.794601

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6c1be50bb858'
down_revision = '5a064f9c14d0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('recipe', sa.Column('suggestion_score', sa.Integer(), server_default='0', nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('recipe', 'suggestion_score')
    # ### end Alembic commands ###
