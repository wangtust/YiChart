"""init tables

Revision ID: d9dd8f16a1ce
Revises: 
Create Date: 2026-04-30 02:33:21.193487

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd9dd8f16a1ce'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('username', sa.String(length=50), nullable=False),
        sa.Column('email', sa.String(length=100), nullable=False),
        sa.Column('hashed_password', sa.String(length=128), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=True)
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)

    op.create_table(
        'bazi_records',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.Column('birth_date', sa.String(length=10), nullable=False),
        sa.Column('birth_time', sa.String(length=5), nullable=False),
        sa.Column('gender', sa.String(length=10), nullable=False),
        sa.Column('is_lunar', sa.Integer(), nullable=True),
        sa.Column('bazi_result', sa.JSON(), nullable=True),
        sa.Column('wuxing_result', sa.JSON(), nullable=True),
        sa.Column('shengxiao', sa.String(length=5), nullable=True),
        sa.Column('nayin', sa.String(length=10), nullable=True),
        sa.Column('ai_analysis', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id']),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(op.f('ix_bazi_records_id'), 'bazi_records', ['id'], unique=False)

    op.create_table(
        'ziwei_records',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.Column('birth_date', sa.String(length=10), nullable=False),
        sa.Column('birth_time', sa.String(length=5), nullable=False),
        sa.Column('gender', sa.String(length=10), nullable=False),
        sa.Column('palaces', sa.JSON(), nullable=True),
        sa.Column('sihua', sa.JSON(), nullable=True),
        sa.Column('ming_gong', sa.String(length=5), nullable=True),
        sa.Column('shen_gong', sa.String(length=5), nullable=True),
        sa.Column('ai_analysis', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id']),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(op.f('ix_ziwei_records_id'), 'ziwei_records', ['id'], unique=False)

    op.create_table(
        'liuyao_records',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.Column('question', sa.String(length=200), nullable=False),
        sa.Column('yao_lines', sa.JSON(), nullable=True),
        sa.Column('ben_gua', sa.JSON(), nullable=True),
        sa.Column('bian_gua', sa.JSON(), nullable=True),
        sa.Column('gua_name', sa.String(length=20), nullable=True),
        sa.Column('bian_gua_name', sa.String(length=20), nullable=True),
        sa.Column('shi_yao', sa.Integer(), nullable=True),
        sa.Column('ying_yao', sa.Integer(), nullable=True),
        sa.Column('liu_qin', sa.JSON(), nullable=True),
        sa.Column('ai_analysis', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id']),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(op.f('ix_liuyao_records_id'), 'liuyao_records', ['id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_liuyao_records_id'), table_name='liuyao_records')
    op.drop_table('liuyao_records')
    op.drop_index(op.f('ix_ziwei_records_id'), table_name='ziwei_records')
    op.drop_table('ziwei_records')
    op.drop_index(op.f('ix_bazi_records_id'), table_name='bazi_records')
    op.drop_table('bazi_records')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_table('users')
