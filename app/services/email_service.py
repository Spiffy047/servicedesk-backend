"""
Email Service Module
Basic email service for ServiceDesk notifications
"""

class EmailService:
    """Basic email service class"""
    
    def __init__(self):
        self.templates = {}
    
    def send_email(self, recipient, subject, message):
        """Send basic email notification"""
        print(f"EMAIL: To={recipient}, Subject={subject}")
        return True