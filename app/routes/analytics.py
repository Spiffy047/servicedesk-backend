from flask import Blueprint, jsonify
from app import db
from app.models.ticket import Ticket
from app.models.user import Agent
from sqlalchemy import func, case

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

@analytics_bp.route('/agent-workload', methods=['GET'])
def get_agent_workload():
    """Get current workload distribution across agents"""
    workload = db.session.query(
        Agent.id,
        Agent.name,
        Agent.email,
        func.count(case((Ticket.status != 'Closed', Ticket.id))).label('active_tickets'),
        func.count(case((Ticket.status == 'Closed', Ticket.id))).label('closed_tickets')
    ).outerjoin(Ticket, Agent.id == Ticket.assigned_to)\
     .group_by(Agent.id, Agent.name, Agent.email)\
     .all()
    
    result = []
    for agent_id, name, email, active, closed in workload:
        result.append({
            'agent_id': agent_id,
            'name': name,
            'email': email,
            'active_tickets': active or 0,
            'closed_tickets': closed or 0
        })
    
    return jsonify(result)

@analytics_bp.route('/dashboard', methods=['GET'])
def get_dashboard_analytics():
    """Get dashboard analytics"""
    total_tickets = Ticket.query.count()
    open_tickets = Ticket.query.filter(Ticket.status.in_(['New', 'Open', 'Pending'])).count()
    closed_tickets = Ticket.query.filter_by(status='Closed').count()
    
    priority_counts = db.session.query(
        Ticket.priority, 
        func.count(Ticket.id)
    ).group_by(Ticket.priority).all()
    
    sla_violations = Ticket.query.filter_by(sla_violated=True).count()
    
    return jsonify({
        'total_tickets': total_tickets,
        'open_tickets': open_tickets,
        'closed_tickets': closed_tickets,
        'sla_violations': sla_violations,
        'priority_breakdown': dict(priority_counts)
    })