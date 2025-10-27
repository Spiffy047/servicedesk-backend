from flask import Blueprint, jsonify, request, make_response
from app.models.ticket import Ticket
import csv
from io import StringIO
from datetime import datetime

export_bp = Blueprint('export', __name__)

@export_bp.route('/templates', methods=['GET'])
def get_export_templates():
    """Get available export templates"""
    templates = [
        {'id': 'summary', 'name': 'Summary Report', 'formats': ['csv']},
        {'id': 'detailed', 'name': 'Detailed Report', 'formats': ['csv']}
    ]
    return jsonify(templates)

@export_bp.route('/tickets/csv', methods=['GET'])
def export_tickets_csv():
    """Export tickets to CSV format"""
    status = request.args.get('status')
    priority = request.args.get('priority')
    
    query = Ticket.query
    if status:
        query = query.filter(Ticket.status == status)
    if priority:
        query = query.filter(Ticket.priority == priority)
    
    tickets = query.order_by(Ticket.created_at.desc()).all()
    
    output = StringIO()
    writer = csv.writer(output)
    
    writer.writerow(['ID', 'Title', 'Status', 'Priority', 'Created At'])
    
    for ticket in tickets:
        writer.writerow([
            ticket.id,
            ticket.title,
            ticket.status,
            ticket.priority,
            ticket.created_at.strftime('%Y-%m-%d %H:%M')
        ])
    
    response = make_response(output.getvalue())
    response.headers['Content-Disposition'] = f'attachment; filename=tickets_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
    response.headers['Content-Type'] = 'text/csv'
    
    return response