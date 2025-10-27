from app import db
from datetime import datetime

class FileAttachment(db.Model):
    """File attachment model for tickets and messages"""
    __tablename__ = 'file_attachments'
    
    # Primary identifiers
    id = db.Column(db.String(50), primary_key=True)
    ticket_id = db.Column(db.String(20), db.ForeignKey('tickets.id'), nullable=False)
    message_id = db.Column(db.String(50), db.ForeignKey('ticket_messages.id'), nullable=True)  # Optional for ticket-level attachments
    
    # File metadata
    filename = db.Column(db.String(255), nullable=False)  # Sanitized filename
    original_filename = db.Column(db.String(255), nullable=False)  # User's original filename
    file_size = db.Column(db.BigInteger, nullable=False)  # Size in bytes
    mime_type = db.Column(db.String(100), nullable=False)
    
    # Storage configuration
    storage_path = db.Column(db.String(500), nullable=False)  # S3 key or local path
    storage_provider = db.Column(db.String(20), default='local')  # 'local', 's3', 'gcs'
    
    # Upload tracking
    uploaded_by = db.Column(db.String(50), nullable=False)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Security scanning
    is_scanned = db.Column(db.Boolean, default=False)
    scan_result = db.Column(db.String(20), default='pending')  # 'clean', 'infected', 'pending'
    
    # Relationships
    ticket = db.relationship('Ticket', backref='file_attachments')
    message = db.relationship('TicketMessage', backref='file_attachments')
    
    def __repr__(self):
        return f'<FileAttachment {self.filename}>'
    
    @property
    def file_size_mb(self):
        """Convert file size from bytes to MB"""
        return round(self.file_size / (1024 * 1024), 2)
    
    def get_download_url(self):
        """Generate download URL based on storage provider"""
        if self.storage_provider == 's3':
            # Generate presigned URL for S3
            return f"/api/files/{self.id}/download"
        return f"/api/files/{self.id}/download"