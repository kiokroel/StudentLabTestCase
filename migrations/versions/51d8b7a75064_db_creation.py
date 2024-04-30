"""DB creation

Revision ID: 51d8b7a75064
Revises: 
Create Date: 2024-04-30 21:42:54.243170

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '51d8b7a75064'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=30), nullable=False),
    sa.Column('username', sa.String(length=30), nullable=False),
    sa.Column('password', sa.LargeBinary(), nullable=False),
    sa.Column('date_registration', sa.TIMESTAMP(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=False)
    op.create_table('forms',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=20), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('creator_id', sa.Integer(), nullable=True),
    sa.Column('is_published', sa.Boolean(), nullable=True),
    sa.Column('data_create', sa.TIMESTAMP(), nullable=True),
    sa.Column('data_change', sa.TIMESTAMP(), nullable=True),
    sa.ForeignKeyConstraint(['creator_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_forms_title'), 'forms', ['title'], unique=False)
    op.create_table('form_fields',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('field_type', sa.String(), nullable=True),
    sa.Column('form_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['form_id'], ['forms.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('form_responses',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('form_id', sa.Integer(), nullable=True),
    sa.Column('response_time', sa.TIMESTAMP(), nullable=True),
    sa.ForeignKeyConstraint(['form_id'], ['forms.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_form_responses_response_time'), 'form_responses', ['response_time'], unique=False)
    op.create_table('form_answers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('field_id', sa.Integer(), nullable=True),
    sa.Column('response_id', sa.Integer(), nullable=True),
    sa.Column('answer', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['field_id'], ['form_fields.id'], ),
    sa.ForeignKeyConstraint(['response_id'], ['form_responses.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('form_field_options',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('field_id', sa.Integer(), nullable=True),
    sa.Column('option', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['field_id'], ['form_fields.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('form_field_options')
    op.drop_table('form_answers')
    op.drop_index(op.f('ix_form_responses_response_time'), table_name='form_responses')
    op.drop_table('form_responses')
    op.drop_table('form_fields')
    op.drop_index(op.f('ix_forms_title'), table_name='forms')
    op.drop_table('forms')
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
    # ### end Alembic commands ###