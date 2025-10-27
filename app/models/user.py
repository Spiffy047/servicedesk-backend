# User Model - Core user management for the ServiceDesk system
# 💡 PRESENTATION HINT: "Simple user model with role-based access control"
from app import db
from datetime import datetime

class User(db.Model):
    """User model for authentication and role management"""
    __tablename__ = 'users'
    
    # Primary identifiers
    id = db.Column(db.String(50), primary_key=True)  # UUID format
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)  # Unique constraint for login
    
    # Access control
    role = db.Column(db.String(20), default='user')  # 'admin', 'agent', 'user'
    is_active = db.Column(db.Boolean, default=True)  # Soft delete flag
    
    # Audit timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<User {self.name}>'
