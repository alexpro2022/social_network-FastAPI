"""First migration

Revision ID: 75965a6c7155
Revises: 
Create Date: 2023-07-03 21:02:43.540710

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '75965a6c7155'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('email', sa.String(length=320), nullable=False),
    sa.Column('hashed_password', sa.String(length=1024), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.Column('is_superuser', sa.Boolean(), nullable=False),
    sa.Column('is_verified', sa.Boolean(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_user'))
    )
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_user_email'), ['email'], unique=True)
        batch_op.create_index(batch_op.f('ix_user_id'), ['id'], unique=False)

    op.create_table('post',
    sa.Column('title', sa.String(length=100), nullable=False),
    sa.Column('content', sa.Text(), nullable=False),
    sa.Column('created', sa.DateTime(), nullable=True),
    sa.Column('updated', sa.DateTime(), nullable=True),
    sa.Column('likes', sa.Integer(), nullable=True),
    sa.Column('dislikes', sa.Integer(), nullable=True),
    sa.Column('author_id', sa.Integer(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['author_id'], ['user.id'], name=op.f('fk_post_author_id_user')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_post')),
    sa.UniqueConstraint('title', name=op.f('uq_post_title'))
    )
    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_post_id'), ['id'], unique=False)

    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_post_id'))

    op.drop_table('post')
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_user_id'))
        batch_op.drop_index(batch_op.f('ix_user_email'))

    op.drop_table('user')
    # ### end Alembic commands ###