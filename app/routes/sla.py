"""
SLA Routes Module
Provides endpoints for SLA monitoring, violation tracking, and performance metrics.
"""

from flask import Blueprint, request, jsonify
from app.services.sla_service import SLAService
from app.models.ticket import Ticket
from datetime import datetime, timedelta

# Create SLA blueprint
sla_bp = Blueprint('sla', __name__)

# Initialize SLA service
sla_service = SLAService()

@sla_bp.route('/dashboard', methods=['GET'])
def get_sla_dashboard():
    """
    Get comprehensive SLA dashboard metrics
    Returns overall adherence rates and priority breakdowns
    """
    dashboard_data = SLAService.get_sla_dashboard()
    return jsonify(dashboard_data)

@sla_bp.route('/violations', methods=['GET'])
def get_sla_violations():
    """
    Get current SLA violations
    Returns list of tickets that have violated their SLA targets
    """
    violations = sla_service.check_sla_violations()
    
    # Format violation data for response
    violation_data = []
    for ticket in violations:
        violation_data.append({
            'ticket_id': ticket.id,
            'title': ticket.title,
            'priority': ticket.priority,
            'created_at': ticket.created_at.isoformat(),
            'hours_elapsed': (datetime.utcnow() - ticket.created_at).total_seconds() / 3600,
            'sla_target': SLAService.get_sla_target(ticket.priority),
            'assigned_to': ticket.assigned_to
        })
    
    return jsonify({
        'violations': violation_data,
        'total_count': len(violation_data)
    })

@sla_bp.route('/forecast', methods=['GET'])
def get_sla_forecast():
    """
    Get SLA violation forecast for upcoming hours
    Predicts which tickets are at risk of violating SLA
    """
    hours_ahead = request.args.get('hours', 24, type=int)
    at_risk_tickets = sla_service.get_violation_forecast(hours_ahead)
    
    # Format forecast data
    forecast_data = []
    for ticket in at_risk_tickets:
        target_hours = SLAService.get_sla_target(ticket.priority)
        deadline = ticket.created_at + timedelta(hours=target_hours)
        hours_remaining = (deadline - datetime.utcnow()).total_seconds() / 3600
        
        forecast_data.append({
            'ticket_id': ticket.id,
            'title': ticket.title,
            'priority': ticket.priority,
            'deadline': deadline.isoformat(),
            'hours_remaining': max(0, hours_remaining),
            'risk_level': 'high' if hours_remaining < 2 else 'medium'
        })
    
    return jsonify({
        'forecast': forecast_data,
        'hours_ahead': hours_ahead,
        'at_risk_count': len(forecast_data)
    })

@sla_bp.route('/trends', methods=['GET'])
def get_sla_trends():
    """
    Get SLA adherence trends over time
    Shows historical SLA performance data
    """
    days = request.args.get('days', 30, type=int)
    trends = sla_service.get_sla_trends(days)
    
    return jsonify({
        'trends': trends,
        'period_days': days
    })

@sla_bp.route('/targets', methods=['GET'])
def get_sla_targets():
    """
    Get SLA targets for all priority levels
    Returns the configured SLA targets in hours
    """
    targets = {
        'Critical': SLAService.get_sla_target('Critical'),
        'High': SLAService.get_sla_target('High'),
        'Medium': SLAService.get_sla_target('Medium'),
        'Low': SLAService.get_sla_target('Low')
    }
    
    return jsonify({
        'targets': targets,
        'unit': 'hours'
    })