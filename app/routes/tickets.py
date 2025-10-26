from flask import Blueprint, jsonify
from app import db
from app.models.user import Agent
from app.models.ticket import Ticket

tickets_bp = Blueprint('tickets', __name__)

@tickets_bp.route('/', methods=['GET'])
def get_tickets():
    """Get all tickets"""
    tickets = Ticket.query.all()
    return jsonify([{'id': t.id, 'title': t.title, 'status': t.status} for t in tickets])

@tickets_bp.route('/<ticket_id>', methods=['GET'])
def get_ticket(ticket_id):
    """Get a specific ticket"""
    ticket = Ticket.query.get_or_404(ticket_id)
    return jsonify({'id': ticket.id, 'title': ticket.title, 'status': ticket.status})