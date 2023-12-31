"""empty message

Revision ID: 788475c071b8
Revises: 2156868e5ed4
Create Date: 2023-12-17 14:54:45.922485

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '788475c071b8'
down_revision = '2156868e5ed4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('admin', schema=None) as batch_op:
        batch_op.add_column(sa.Column('answer', sa.String(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('admin', schema=None) as batch_op:
        batch_op.drop_column('answer')

    # ### end Alembic commands ###
