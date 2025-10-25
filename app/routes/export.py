from flask import Blueprint, request, jsonify, send_file
from datetime import datetime
import csv
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import tempfile

export_bp = Blueprint('export', __name__)

@export_bp.route('/csv', methods=['GET'])
def export_csv():
    """Export tickets to CSV with date range filters"""
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    tickets = [
        {'id': 1, 'title': 'Login Issue', 'priority': 'high', 'status': 'open', 'created_at': '2024-01-15'},
        {'id': 2, 'title': 'Email Problem', 'priority': 'medium', 'status': 'resolved', 'created_at': '2024-01-14'}
    ]
    
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=['id', 'title', 'priority', 'status', 'created_at'])
    writer.writeheader()
    writer.writerows(tickets)
    
    return jsonify({
        'csv_data': output.getvalue(),
        'record_count': len(tickets),
        'date_range': f"{start_date} to {end_date}" if start_date and end_date else "all"
    })

@export_bp.route('/pdf', methods=['GET'])
def export_pdf():
    """Export tickets to PDF report"""
    template = request.args.get('template', 'standard')
    
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')
    
    c = canvas.Canvas(temp_file.name, pagesize=letter)
    width, height = letter
    
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 50, "Service Desk Report")
    
    c.setFont("Helvetica", 12)
    y_position = height - 100
    
    tickets = [
        "Ticket #1: Login Issue - High Priority",
        "Ticket #2: Email Problem - Medium Priority"
    ]
    
    for ticket in tickets:
        c.drawString(50, y_position, ticket)
        y_position -= 20
    
    c.save()
    temp_file.close()
    
    return jsonify({
        'message': 'PDF generated successfully',
        'template': template,
        'file_path': temp_file.name
    })

@export_bp.route('/template-report', methods=['POST'])
def generate_template_report():
    """Generate report using custom template"""
    data = request.get_json()
    template_name = data.get('template', 'default')
    filters = data.get('filters', {})
    
    report_config = {
        'template': template_name,
        'filters_applied': filters,
        'generated_at': datetime.utcnow().isoformat(),
        'sections': ['summary', 'details', 'charts']
    }
    
    return jsonify({
        'report_id': f"RPT_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}",
        'config': report_config,
        'status': 'generated'
    })

def _optimize_csv_generation(data, chunk_size=1000):
    """Optimize CSV generation for large datasets"""
    for i in range(0, len(data), chunk_size):
        yield data[i:i + chunk_size]