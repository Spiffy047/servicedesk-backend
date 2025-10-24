from flask import current_app
from flask_mail import Mail, Message
from typing import List, Dict, Optional
import smtplib
from email.mime.text import MimeText
from email.mime.multipart import MimeMultipart
from jinja2 import Template
import os

class EmailService:
    """Email sending service for notifications"""
    
    def __init__(self, app=None):
        self.mail = None
        if app:
            self.init_app(app)
    
    def init_app(self, app):
        """Initialize email service with Flask app"""
        self.mail = Mail(app)
    
    def send_email(self, to: List[str], subject: str, template: str, **kwargs) -> bool:
        """Send email using template"""
        try:
            html_body = self._render_template(template, **kwargs)
            
            msg = Message(
                subject=subject,
                recipients=to,
                html=html_body,
                sender=current_app.config.get('MAIL_DEFAULT_SENDER')
            )
            
            self.mail.send(msg)
            return True
        except Exception as e:
            current_app.logger.error(f"Failed to send email: {str(e)}")
            return False
    
    def send_new_ticket_notification(self, ticket_data: Dict, recipient_email: str) -> bool:
        """Send new ticket notification"""
        return self.send_email(
            to=[recipient_email],
            subject=f"New Ticket Created: {ticket_data['title']}",
            template='new_ticket.html',
            ticket=ticket_data
        )
    
    def send_status_change_notification(self, ticket_data: Dict, old_status: str, new_status: str, recipient_email: str) -> bool:
        """Send ticket status change notification"""
        return self.send_email(
            to=[recipient_email],
            subject=f"Ticket Status Updated: {ticket_data['id']}",
            template='status_change.html',
            ticket=ticket_data,
            old_status=old_status,
            new_status=new_status
        )
    
    def send_sla_warning(self, ticket_data: Dict, recipient_email: str) -> bool:
        """Send SLA warning notification"""
        return self.send_email(
            to=[recipient_email],
            subject=f"SLA Warning: {ticket_data['id']}",
            template='sla_warning.html',
            ticket=ticket_data
        )
    
    def send_new_message_notification(self, ticket_data: Dict, message_data: Dict, recipient_email: str) -> bool:
        """Send new message notification"""
        return self.send_email(
            to=[recipient_email],
            subject=f"New Message on Ticket: {ticket_data['id']}",
            template='new_message.html',
            ticket=ticket_data,
            message=message_data
        )
    
    def _render_template(self, template_name: str, **kwargs) -> str:
        """Render email template"""
        template_path = os.path.join(
            current_app.root_path, 
            'templates', 
            'emails', 
            template_name
        )
        
        with open(template_path, 'r') as f:
            template_content = f.read()
        
        template = Template(template_content)
        return template.render(**kwargs)
