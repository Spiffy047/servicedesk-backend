from flask import Blueprint, request, jsonify
from app import db
from app.models.email_log import EmailLog
from app.schemas.email_log import email_log_schema, email_logs_schema
from datetime import datetime, timedelta

emails_bp = Blueprint('emails', __name__)

@emails_bp.route('/logs', methods=['GET'])
def get_email_logs():
    """Get email logs with filtering"""
    status = request.args.get('status')
    recipient = request.args.get('recipient')
    days = request.args.get('days', 7, type=int)
    
    query = EmailLog.query
    
    # Filter by date range
    start_date = datetime.utcnow() - timedelta(days=days)
    query = query.filter(EmailLog.created_at >= start_date)
    
    if status:
        query = query.filter(EmailLog.status == status)
    if recipient:
        query = query.filter(EmailLog.recipient.contains(recipient))
    
    logs = query.order_by(EmailLog.created_at.desc()).all()
    return jsonify(email_logs_schema.dump(logs))

@emails_bp.route('/logs/<log_id>', methods=['GET'])
def get_email_log(log_id):
    """Get specific email log"""
    log = EmailLog.query.get_or_404(log_id)
    return jsonify(email_log_schema.dump(log))

@emails_bp.route('/stats', methods=['GET'])
def get_email_stats():
    """Get email statistics"""
    days = request.args.get('days', 7, type=int)
    start_date = datetime.utcnow() - timedelta(days=days)
    
    total_emails = EmailLog.query.filter(EmailLog.created_at >= start_date).count()
    sent_emails = EmailLog.query.filter(
        EmailLog.created_at >= start_date,
        EmailLog.status == 'sent'
    ).count()
    failed_emails = EmailLog.query.filter(
        EmailLog.created_at >= start_date,
        EmailLog.status == 'failed'
    ).count()
    
    success_rate = (sent_emails / total_emails * 100) if total_emails > 0 else 0
    
    return jsonify({
        'total_emails': total_emails,
        'sent_emails': sent_emails,
        'failed_emails': failed_emails,
        'success_rate': round(success_rate, 2),
        'period_days': days
    })
