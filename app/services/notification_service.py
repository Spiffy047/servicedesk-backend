"""
Notification Service Module
Basic notification service for ServiceDesk
"""

class NotificationService:
    """Enhanced notification service"""
    
    def __init__(self):
        self.templates = {
            'ticket_created': 'New ticket {ticket_id} created: {title}',
            'ticket_assigned': 'Ticket {ticket_id} assigned to you: {title}',
            'status_changed': 'Ticket {ticket_id} status changed to {status}'
        }
    
    @staticmethod
    def send_notification(recipient, message):
        """Send basic notification"""
        print(f"NOTIFICATION: To={recipient}, Message={message}")
        return True
    
    @staticmethod
    def notify_ticket_assignment(ticket, agent):
        """Notify agent about ticket assignment"""
        message = f"Ticket {ticket.id} assigned to {agent.name}"
        print(f"ASSIGNMENT: {message}")
        return True
    
    @staticmethod
    def notify_status_change(ticket, old_status, new_status):
        """Notify about status change"""
        message = f"Ticket {ticket.id} changed from {old_status} to {new_status}"
        print(f"STATUS CHANGE: {message}")
        return True
    
    @staticmethod
    def notify_sla_violation(ticket):
        """Notify about SLA violation"""
        message = f"SLA VIOLATION: Ticket {ticket.id} has violated SLA"
        print(f"SLA ALERT: {message}")
        return True