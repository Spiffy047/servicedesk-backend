from app import ma
from app.models.user import User, Agent
from marshmallow import fields

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True

class AgentSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Agent
        load_instance = True
    
    ticket_count = fields.Integer(dump_only=True)
    closed_tickets = fields.Integer(dump_only=True)
    average_handle_time = fields.Float(dump_only=True)
    sla_violations = fields.Integer(dump_only=True)

# Schema instances
user_schema = UserSchema()
users_schema = UserSchema(many=True)
agent_schema = AgentSchema()
agents_schema = AgentSchema(many=True)