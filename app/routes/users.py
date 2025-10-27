"""
Users Routes Module
Enhanced user management with notification preferences
"""

from flask import Blueprint, request, jsonify
from app import db
from app.models.user import User
from app.services.notification_service import NotificationService
from datetime import datetime

users_bp = Blueprint('users', __name__)

@users_bp.route('/', methods=['GET'])
def get_users():
    """Get all users with optional role filtering"""
    role = request.args.get('role')
    
    query = User.query
    if role:
        query = query.filter(User.role == role)
    
    users = query.order_by(User.name).all()
    return jsonify([{
        'id': user.id,
        'name': user.name,
        'email': user.email,
        'role': user.role
    } for user in users])

@users_bp.route('/<user_id>/notifications/preferences', methods=['GET'])
def get_notification_preferences(user_id):
    """Get user notification preferences"""
    user = User.query.get_or_404(user_id)
    
    preferences = {
        'user_id': user_id,
        'user_email': user.email,
        'email_enabled': True,
        'sms_enabled': False,
        'push_enabled': True,
        'frequency': 'immediate'
    }
    
    return jsonify(preferences)