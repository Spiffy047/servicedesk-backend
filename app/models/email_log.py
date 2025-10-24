from app import db
from datetime import datetime

class EmailLog(db.Model):
    __tablename__ = 'email_logs'
    
    id = db.Column(db.String(50), primary_key=True)
    recipient = db.Column(db.String(255), nullable=False)
    subject = db.Column(db.String(255), nullable=False)
    template = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(20), nullable=False)  # 'sent', 'failed', 'pending'
    sent_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    error_message = db.Column(db.Text, nullable=True)
    retry_count = db.Column(db.Integer, default=0)
    
    def __repr__(self):
        return f'<EmailLog {self.id}>'
