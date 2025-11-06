#!/usr/bin/env python3
"""
Test script to create sample notifications for testing the notification bell
"""
import os
import sys
import django
from django.utils import timezone

# Add the project directory to Python path
sys.path.append('/home/samuel/Development/code/phase-4/servicedesk-backend')

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'servicedesk.settings')
django.setup()

from notifications.models import Alert
from users.models import User
from tickets.models import Ticket

def create_test_notifications():
    """Create test notifications for all users"""
    
    # Get all users
    users = User.objects.all()
    print(f"Found {users.count()} users")
    
    # Get a sample ticket
    ticket = Ticket.objects.first()
    ticket_id = ticket.id if ticket else 1
    
    for user in users:
        print(f"Creating notifications for user: {user.name} (ID: {user.id})")
        
        # Create different types of notifications
        notifications = [
            {
                'alert_type': 'assignment',
                'title': f'New Assignment: TKT-0001',
                'message': f'You have been assigned to ticket TKT-0001: Sample Support Request'
            },
            {
                'alert_type': 'status_change',
                'title': f'Status Update: TKT-0001',
                'message': f'Ticket TKT-0001 status changed from New to In Progress'
            },
            {
                'alert_type': 'sla_violation',
                'title': f'SLA Alert: TKT-0001',
                'message': f'Ticket TKT-0001 is approaching SLA deadline'
            }
        ]
        
        for i, notif in enumerate(notifications):
            Alert.objects.create(
                user_id=user.id,
                ticket_id=ticket_id,
                alert_type=notif['alert_type'],
                title=notif['title'],
                message=notif['message'],
                is_read=i == 2,  # Mark last one as read
                created_at=timezone.now()
            )
        
        print(f"Created 3 notifications for {user.name}")
    
    print("\nTest notifications created successfully!")
    print("You can now test the notification bell in the frontend.")

if __name__ == '__main__':
    create_test_notifications()