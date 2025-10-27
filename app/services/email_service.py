from flask import current_app
from flask_mail import Mail, Message
from typing import List, Dict, Optional
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