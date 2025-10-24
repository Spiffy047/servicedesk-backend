from flask import Blueprint, request, jsonify
from app import db
from app.models.notification_settings import NotificationSettings
from app.schemas.notification_settings import notification_settings_schema
import uuid

notification_settings_bp = Blueprint('notification_settings', __name__)

@notification_settings_bp.route('/<user_id>', methods=['GET'])
def get_notification_settings(user_id):
    """Get user notification settings"""
    settings = NotificationSettings.query.filter_by(user_id=user_id).first()
    
    if not settings:
        # Create default settings
        settings = NotificationSettings(
            id=str(uuid.uuid4()),
            user_id=user_id
        )
        db.session.add(settings)
        db.session.commit()
    
    return jsonify(notification_settings_schema.dump(settings))

@notification_settings_bp.route('/<user_id>', methods=['PUT'])
def update_notification_settings(user_id):
    """Update user notification settings"""
    settings = NotificationSettings.query.filter_by(user_id=user_id).first()
    
    if not settings:
        settings = NotificationSettings(
            id=str(uuid.uuid4()),
            user_id=user_id
        )
    
    data = request.get_json()
    
    # Update settings
    for field in ['email_enabled', 'sms_enabled', 'push_enabled', 
                  'new_ticket_email', 'status_change_email', 'new_message_email',
                  'sla_warning_email', 'assignment_email', 'digest_frequency']:
        if field in data:
            setattr(settings, field, data[field])
    
    if not settings.id:
        db.session.add(settings)
    
    db.session.commit()
    
    return jsonify(notification_settings_schema.dump(settings))

@notification_settings_bp.route('/<user_id>', methods=['DELETE'])
def reset_notification_settings(user_id):
    """Reset notification settings to defaults"""
    settings = NotificationSettings.query.filter_by(user_id=user_id).first()
    
    if settings:
        db.session.delete(settings)
        db.session.commit()
    
    # Create new default settings
    new_settings = NotificationSettings(
        id=str(uuid.uuid4()),
        user_id=user_id
    )
    db.session.add(new_settings)
    db.session.commit()
    
    return jsonify(notification_settings_schema.dump(new_settings))
