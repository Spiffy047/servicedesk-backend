from app import db

class Agent(db.Model):
    __tablename__ = 'agents'
    
    id = db.Column(db.String(50), primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    max_tickets = db.Column(db.Integer, default=10)
    
    def __repr__(self):
        return f'<Agent {self.username}>'