"""
Email Log Model
Tracks email notifications sent by the system
"""

from app import db
from datetime import datetime

class EmailLog(db.Model):
    """Email log model for tracking sent emails"""
    __tablename__ = 'email_logs'
    
    id = db.Column(db.String(36), primary_key=True)
    recipient = db.Column(db.String(255), nullable=False)
    subject = db.Column(db.String(500), nullable=False)
    template = db.Column(db.String(100))
    status = db.Column(db.String(20), default='pending')
    sent_at = db.Column(db.DateTime, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)