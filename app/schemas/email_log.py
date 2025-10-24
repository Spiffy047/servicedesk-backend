from app import ma
from app.models.email_log import EmailLog
from marshmallow import fields

class EmailLogSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = EmailLog
        load_instance = True
        include_fk = True
    
    sent_at = fields.DateTime(format='%Y-%m-%d %H:%M:%S', allow_none=True)
    created_at = fields.DateTime(format='%Y-%m-%d %H:%M:%S')

# Schema instances
email_log_schema = EmailLogSchema()
email_logs_schema = EmailLogSchema(many=True)
