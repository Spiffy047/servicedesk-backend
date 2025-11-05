from django.utils import timezone
from .models import Alert

class NotificationService:
    """Service class for creating and managing notifications"""
    
    @staticmethod
    def create_assignment_notification(user_id, ticket_id, ticket_title, ticket_number):
        """Create notification when ticket is assigned to user"""
        return Alert.objects.create(
            user_id=user_id,
            ticket_id=ticket_id,
            alert_type='assignment',
            title=f'New Assignment: {ticket_number}',
            message=f'You have been assigned to ticket {ticket_number}: {ticket_title}',
            is_read=False,
            created_at=timezone.now()
        )
    
    @staticmethod
    def create_status_change_notification(user_id, ticket_id, ticket_number, old_status, new_status):
        """Create notification when ticket status changes"""
        return Alert.objects.create(
            user_id=user_id,
            ticket_id=ticket_id,
            alert_type='status_change',
            title=f'Status Update: {ticket_number}',
            message=f'Ticket {ticket_number} status changed from {old_status} to {new_status}',
            is_read=False,
            created_at=timezone.now()
        )
    
    @staticmethod
    def create_sla_violation_notification(user_id, ticket_id, ticket_number):
        """Create notification for SLA violation"""
        return Alert.objects.create(
            user_id=user_id,
            ticket_id=ticket_id,
            alert_type='sla_violation',
            title=f'SLA Violation: {ticket_number}',
            message=f'Ticket {ticket_number} has violated its SLA target',
            is_read=False,
            created_at=timezone.now()
        )
    
    @staticmethod
    def create_escalation_notification(user_id, ticket_id, ticket_number):
        """Create notification for ticket escalation"""
        return Alert.objects.create(
            user_id=user_id,
            ticket_id=ticket_id,
            alert_type='escalation',
            title=f'Ticket Escalated: {ticket_number}',
            message=f'Ticket {ticket_number} has been escalated and requires attention',
            is_read=False,
            created_at=timezone.now()
        )
    
    @staticmethod
    def create_custom_notification(user_id, ticket_id, alert_type, title, message):
        """Create custom notification"""
        return Alert.objects.create(
            user_id=user_id,
            ticket_id=ticket_id,
            alert_type=alert_type,
            title=title,
            message=message,
            is_read=False,
            created_at=timezone.now()
        )
    
    @staticmethod
    def get_user_notification_count(user_id):
        """Get unread notification count for user"""
        return Alert.objects.filter(user_id=user_id, is_read=False).count()
    
    @staticmethod
    def mark_all_read(user_id):
        """Mark all notifications as read for user"""
        return Alert.objects.filter(user_id=user_id, is_read=False).update(is_read=True)