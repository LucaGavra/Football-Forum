"""Add comment & voting models

Revision ID: c447612eef95
Revises: 4cad6464b2fc
Create Date: 2025-01-12 23:23:11.901417

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c447612eef95'
down_revision = '4cad6464b2fc'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('comments',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('content', sa.Text(), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('post_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['post_id'], ['posts.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('post_votes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('value', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('post_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['post_id'], ['posts.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('comment_votes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('value', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('comment_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['comment_id'], ['comments.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('comment_votes')
    op.drop_table('post_votes')
    op.drop_table('comments')
    # ### end Alembic commands ###
