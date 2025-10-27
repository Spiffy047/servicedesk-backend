"""
Notification Service Module
Basic notification service for ServiceDesk
"""

class NotificationService:
    """Basic notification service"""
    
    def __init__(self):
        self.templates = {}
    
    @staticmethod
    def send_notification(recipient, message):
        """Send basic notification"""
        print(f"NOTIFICATION: To={recipient}, Message={message}")
        return True