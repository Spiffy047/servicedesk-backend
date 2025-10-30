"""
Notification Service for IT ServiceDesk
Handles alert creation, management, and delivery with enhanced functionality
"""

from datetime import datetime, timedelta
from app import db
from app.models import Alert, User, Ticket
from sqlalchemy import text

class NotificationService:
    """Enhanced notification service combining both alert management and basic notifications"""
    
    def __init__(self):
        self.templates = {
            'ticket_created': 'New ticket {ticket_id} created: {title}',
            'ticket_assigned': 'Ticket {ticket_id} assigned to you: {title}',
            'status_changed': 'Ticket {ticket_id} status changed to {status}'
        }
    
    @staticmethod
    def create_alert(user_id, ticket_id, alert_type, title, message):
        """Create a new alert with validation"""
        try:
            # Validate user exists
            user = User.query.get(user_id)
            if not user:
                raise ValueError(f"User {user_id} not found")
            
            # Validate ticket exists if provided
            if ticket_id:
                ticket = Ticket.query.get(ticket_id)
                if not ticket:
                    raise ValueError(f"Ticket {ticket_id} not found")
            
            alert = Alert(
                user_id=user_id,
                ticket_id=ticket_id,
                alert_type=alert_type,
                title=title,
                message=message
            )
            
            db.session.add(alert)
            db.session.commit()
            
            print(f"[SUCCESS] Alert created: {title} for user {user.name}")
            return alert
            
        except Exception as e:
            db.session.rollback()
            print(f"[ERROR] Alert creation failed: {e}")
            raise
    
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
    
    @staticmethod
    def create_assignment_alert(user_id, ticket_id, ticket_title, priority):
        """Create assignment alert with enhanced details"""
        title = f"New Ticket Assigned"
        message = f"You have been assigned ticket {ticket_id}: {ticket_title} (Priority: {priority})"
        
        return NotificationService.create_alert(
            user_id=user_id,
            ticket_id=ticket_id,
            alert_type='assignment',
            title=title,
            message=message
        )
    
    @staticmethod
    def get_user_alerts(user_id, limit=20, unread_only=False):
        """Get alerts for a specific user with enhanced filtering"""
        try:
            query = db.session.execute(text("""
                SELECT a.id, a.title, a.message, a.alert_type, a.is_read, a.created_at,
                       COALESCE(t.ticket_id, CAST(a.ticket_id AS VARCHAR)) as ticket_id,
                       t.status as ticket_status, t.priority as ticket_priority
                FROM alerts a
                LEFT JOIN tickets t ON a.ticket_id = t.id
                WHERE a.user_id = :user_id
                """ + (" AND a.is_read = false" if unread_only else "") + """
                ORDER BY a.created_at DESC
                LIMIT :limit
            """), {'user_id': user_id, 'limit': limit})
            
            alerts = []
            for row in query:
                alerts.append({
                    'id': row[0],
                    'title': row[1],
                    'message': row[2],
                    'alert_type': row[3],
                    'is_read': row[4],
                    'created_at': row[5].isoformat() + 'Z' if row[5] else None,
                    'ticket_id': row[6],
                    'ticket_status': row[7],
                    'ticket_priority': row[8],
                    'clickable': bool(row[6])  # Can click if has ticket_id
                })
            
            return alerts
            
        except Exception as e:
            print(f"[ERROR] Error fetching alerts for user {user_id}: {e}")
            return []
    
    @staticmethod
    def mark_alert_read(alert_id, user_id=None):
        """Mark specific alert as read with user validation"""
        try:
            query = Alert.query.filter_by(id=alert_id)
            if user_id:
                query = query.filter_by(user_id=user_id)
            
            alert = query.first()
            if not alert:
                return False
            
            alert.is_read = True
            db.session.commit()
            return True
            
        except Exception as e:
            db.session.rollback()
            print(f"[ERROR] Error marking alert {alert_id} as read: {e}")
            return False