from flask import Blueprint, jsonify
from app import db
from app.models.ticket import Ticket
from sqlalchemy import func

analytics_bp = Blueprint('analytics', __name__)

@analytics_bp.route('/ticket-status-counts', methods=['GET'])
def get_ticket_status_counts():
    """Get count of tickets by status"""
    status_counts = db.session.query(
        Ticket.status,
        func.count(Ticket.id).label('count')
    ).group_by(Ticket.status).all()
    
    result = {status: count for status, count in status_counts}
    return jsonify(result)