"""
Email Service Module
Basic email service for ServiceDesk notifications
"""

class EmailService:
    """Enhanced email service class"""
    
    def __init__(self):
        self.templates = {
            'ticket_created': 'New ticket {ticket_id} created: {title}',
            'ticket_assigned': 'Ticket {ticket_id} assigned to you: {title}',
            'status_changed': 'Ticket {ticket_id} status changed to {status}'
        }
    
    def send_email(self, recipient, subject, message):
        """Send email notification with logging"""
        try:
            print(f"EMAIL: To={recipient}, Subject={subject}, Message={message}")
            
            # Log email attempt
            self._log_email(recipient, subject, 'notification', 'sent')
            return True
        except Exception as e:
            print(f"Failed to send email: {str(e)}")
            self._log_email(recipient, subject, 'notification', 'failed')
            return False
    
    def _log_email(self, recipient, subject, template, status):
        """Log email attempt to database"""
        try:
            from app.models.email_log import EmailLog
            from app import db
            import uuid
            
            log_entry = EmailLog(
                id=str(uuid.uuid4()),
                recipient=recipient,
                subject=subject,
                template=template,
                status=status
            )
            db.session.add(log_entry)
            db.session.commit()
        except Exception as e:
            print(f"Failed to log email: {str(e)}")
    
    def send_template_email(self, recipient, template_name, data):
        """Send email using template"""
        if template_name not in self.templates:
            return False
        
        message = self.templates[template_name].format(**data)
        subject = f"ServiceDesk: {template_name.replace('_', ' ').title()}"
        
        return self.send_email(recipient, subject, message)