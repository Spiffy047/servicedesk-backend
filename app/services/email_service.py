"""
Email Service Module
Enhanced email service combining SendGrid integration with template functionality
"""

import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

class EmailService:
    """Enhanced email service class with SendGrid and template support"""
    
    def __init__(self):
        self.sg = SendGridAPIClient(api_key=os.environ.get('SENDGRID_API_KEY'))
        self.from_email = os.environ.get('SENDGRID_FROM_EMAIL', 'mwanikijoe1@gmail.com')
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
    
    def send_ticket_notification(self, to_email, ticket_id, ticket_title, message_type='created'):
        """Send ticket notification using SendGrid"""
        subject_map = {
            'created': f'New Ticket Created: {ticket_id}',
            'assigned': f'Ticket Assigned: {ticket_id}',
            'updated': f'Ticket Updated: {ticket_id}',
            'closed': f'Ticket Resolved: {ticket_id}'
        }
        
        content_map = {
            'created': f'A new support ticket has been created.\n\nTicket ID: {ticket_id}\nTitle: {ticket_title}\n\nYou can view and track this ticket in your dashboard.',
            'assigned': f'A ticket has been assigned to you.\n\nTicket ID: {ticket_id}\nTitle: {ticket_title}\n\nPlease review and take action as needed.',
            'updated': f'Your ticket has been updated.\n\nTicket ID: {ticket_id}\nTitle: {ticket_title}\n\nCheck your dashboard for the latest updates.',
            'closed': f'Your ticket has been resolved.\n\nTicket ID: {ticket_id}\nTitle: {ticket_title}\n\nThank you for using our support system.'
        }
        
        message = Mail(
            from_email=self.from_email,
            to_emails=to_email,
            subject=subject_map.get(message_type, f'Ticket Notification: {ticket_id}'),
            plain_text_content=content_map.get(message_type, f'Ticket {ticket_id} notification.')
        )
        
        try:
            response = self.sg.send(message)
            self._log_email(to_email, subject_map.get(message_type), message_type, 'sent')
            return True
        except Exception as e:
            print(f"Email send error: {e}")
            self._log_email(to_email, subject_map.get(message_type), message_type, 'failed')
            return False
    
    def send_sla_violation_alert(self, to_email, ticket_id, ticket_title):
        """Send SLA violation alert"""
        message = Mail(
            from_email=self.from_email,
            to_emails=to_email,
            subject=f'SLA Violation Alert: {ticket_id}',
            plain_text_content=f'URGENT: SLA violation detected.\n\nTicket ID: {ticket_id}\nTitle: {ticket_title}\n\nImmediate attention required.'
        )
        
        try:
            response = self.sg.send(message)
            self._log_email(to_email, f'SLA Violation Alert: {ticket_id}', 'sla_violation', 'sent')
            return True
        except Exception as e:
            print(f"SLA alert email error: {e}")
            self._log_email(to_email, f'SLA Violation Alert: {ticket_id}', 'sla_violation', 'failed')
            return False