"""private_message

Revision ID: e72ff320d68f
Revises: 
Create Date: 2018-07-27 13:22:34.036683

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e72ff320d68f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=140), nullable=False),
    sa.Column('email', sa.String(length=140), nullable=False),
    sa.Column('password', sa.String(length=80), nullable=False),
    sa.Column('image', sa.String(length=120), nullable=False),
    sa.Column('resume', sa.String(length=120), nullable=False),
    sa.Column('name', sa.String(length=40), nullable=True),
    sa.Column('mobile', sa.String(length=14), nullable=True),
    sa.Column('phone', sa.String(length=14), nullable=True),
    sa.Column('dob', sa.String(length=20), nullable=True),
    sa.Column('address', sa.String(length=200), nullable=True),
    sa.Column('hobbies', sa.String(length=100), nullable=True),
    sa.Column('country', sa.String(length=30), nullable=True),
    sa.Column('city', sa.String(length=30), nullable=True),
    sa.Column('last_message_read_time', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_table('message',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('sender_id', sa.Integer(), nullable=True),
    sa.Column('recipient_id', sa.Integer(), nullable=True),
    sa.Column('body', sa.String(length=240), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['recipient_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['sender_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_message_timestamp'), 'message', ['timestamp'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_message_timestamp'), table_name='message')
    op.drop_table('message')
    op.drop_table('user')
    # ### end Alembic commands ###