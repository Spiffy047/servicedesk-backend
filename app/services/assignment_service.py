from app import db
from app.models.user import Agent
from app.models.ticket import Ticket

class AssignmentService:
    @staticmethod
    def auto_assign_ticket(ticket):
        agents = Agent.query.filter(Agent.is_active == True).all()
        if agents:
            ticket.assigned_to = agents[0].id
            return True
        return False