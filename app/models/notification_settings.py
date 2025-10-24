from app import db
from datetime import datetime

class NotificationSettings(db.Model):
    __tablename__ = 'notification_settings'
    
    id = db.Column(db.String(50), primary_key=True)
    user_id = db.Column(db.String(50), db.ForeignKey('users.id'), nullable=False)
    email_enabled = db.Column(db.Boolean, default=True)
    sms_enabled = db.Column(db.Boolean, default=False)
    push_enabled = db.Column(db.Boolean, default=True)
    
    # Email notification types
    new_ticket_email = db.Column(db.Boolean, default=True)
    status_change_email = db.Column(db.Boolean, default=True)
    new_message_email = db.Column(db.Boolean, default=True)
    sla_warning_email = db.Column(db.Boolean, default=True)
    assignment_email = db.Column(db.Boolean, default=True)
    
    # Frequency settings
    digest_frequency = db.Column(db.String(20), default='immediate')  # 'immediate', 'daily', 'weekly'
    quiet_hours_start = db.Column(db.Time, nullable=True)
    quiet_hours_end = db.Column(db.Time, nullable=True)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', backref='notification_settings')
    
    def __repr__(self):
        return f'<NotificationSettings {self.user_id}>'
