"""Add email log table

Revision ID: add_email_log
Revises: 
Create Date: 2024-01-15 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers
revision = 'add_email_log'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # Create email_logs table
    op.create_table('email_logs',
        sa.Column('id', sa.String(length=50), nullable=False),
        sa.Column('recipient', sa.String(length=255), nullable=False),
        sa.Column('subject', sa.String(length=255), nullable=False),
        sa.Column('template', sa.String(length=100), nullable=False),
        sa.Column('status', sa.String(length=20), nullable=False),
        sa.Column('sent_at', sa.DateTime(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('error_message', sa.Text(), nullable=True),
        sa.Column('retry_count', sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create indexes
    op.create_index('ix_email_logs_status', 'email_logs', ['status'])
    op.create_index('ix_email_logs_created_at', 'email_logs', ['created_at'])
    op.create_index('ix_email_logs_recipient', 'email_logs', ['recipient'])

def downgrade():
    op.drop_index('ix_email_logs_recipient', table_name='email_logs')
    op.drop_index('ix_email_logs_created_at', table_name='email_logs')
    op.drop_index('ix_email_logs_status', table_name='email_logs')
    op.drop_table('email_logs')
