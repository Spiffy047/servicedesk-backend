"""Add notification settings table

Revision ID: add_notification_settings
Revises: add_email_log
Create Date: 2024-01-15 11:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers
revision = 'add_notification_settings'
down_revision = 'add_email_log'
branch_labels = None
depends_on = None

def upgrade():
    # Create notification_settings table
    op.create_table('notification_settings',
        sa.Column('id', sa.String(length=50), nullable=False),
        sa.Column('user_id', sa.String(length=50), nullable=False),
        sa.Column('email_enabled', sa.Boolean(), nullable=True),
        sa.Column('new_ticket_email', sa.Boolean(), nullable=True),
        sa.Column('status_change_email', sa.Boolean(), nullable=True),
        sa.Column('new_message_email', sa.Boolean(), nullable=True),
        sa.Column('sla_warning_email', sa.Boolean(), nullable=True),
        sa.Column('digest_frequency', sa.String(length=20), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create indexes
    op.create_index('ix_notification_settings_user_id', 'notification_settings', ['user_id'])

def downgrade():
    op.drop_index('ix_notification_settings_user_id', table_name='notification_settings')
    op.drop_table('notification_settings')