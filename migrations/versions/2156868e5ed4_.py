"""empty message

Revision ID: 2156868e5ed4
Revises: f573a21e8609
Create Date: 2023-11-23 08:44:49.107015

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2156868e5ed4'
down_revision = 'f573a21e8609'
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