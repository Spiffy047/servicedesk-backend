from app import ma
from app.models.notification_settings import NotificationSettings
from marshmallow import fields

class NotificationSettingsSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = NotificationSettings
        load_instance = True
        include_fk = True
    
    quiet_hours_start = fields.Time(format='%H:%M', allow_none=True)
    quiet_hours_end = fields.Time(format='%H:%M', allow_none=True)
    created_at = fields.DateTime(format='%Y-%m-%d %H:%M:%S')
    updated_at = fields.DateTime(format='%Y-%m-%d %H:%M:%S')

# Schema instances
notification_settings_schema = NotificationSettingsSchema()
notification_settings_list_schema = NotificationSettingsSchema(many=True)
