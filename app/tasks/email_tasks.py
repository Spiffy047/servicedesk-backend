from celery import Celery
from app.services.email_service import EmailService
from app.models.email_log import EmailLog
from app import db
import uuid
from datetime import datetime

celery = Celery('email_tasks')

@celery.task(bind=True, max_retries=3)
def send_email_async(self, to_emails, subject, template, **kwargs):
    """Async task to send emails"""
    try:
        email_service = EmailService()
        success = email_service.send_email(to_emails, subject, template, **kwargs)
        
        # Log email attempt
        log_entry = EmailLog(
            id=str(uuid.uuid4()),
            recipient=', '.join(to_emails),
            subject=subject,
            template=template,
            status='sent' if success else 'failed',
            sent_at=datetime.utcnow() if success else None,
            error_message=None if success else 'Failed to send email'
        )
        
        db.session.add(log_entry)
        db.session.commit()
        
        return {'status': 'success' if success else 'failed'}
        
    except Exception as exc:
        # Log failed attempt
        log_entry = EmailLog(
            id=str(uuid.uuid4()),
            recipient=', '.join(to_emails),
            subject=subject,
            template=template,
            status='failed',
            error_message=str(exc)
        )
        
        db.session.add(log_entry)
        db.session.commit()
        
        # Retry the task
        raise self.retry(exc=exc, countdown=60)

@celery.task
def send_new_ticket_email(ticket_data, recipient_email):
    """Send new ticket notification email"""
    return send_email_async.delay(
        [recipient_email],
        f"New Ticket Created: {ticket_data['title']}",
        'new_ticket.html',
        ticket=ticket_data
    )

@celery.task
def send_status_change_email(ticket_data, old_status, new_status, recipient_email):
    """Send status change notification email"""
    return send_email_async.delay(
        [recipient_email],
        f"Ticket Status Updated: {ticket_data['id']}",
        'status_change.html',
        ticket=ticket_data,
        old_status=old_status,
        new_status=new_status
    )

@celery.task
def send_sla_warning_email(ticket_data, recipient_email):
    """Send SLA warning email"""
    return send_email_async.delay(
        [recipient_email],
        f"SLA Warning: {ticket_data['id']}",
        'sla_warning.html',
        ticket=ticket_data
    )

@celery.task
def send_new_message_email(ticket_data, message_data, recipient_email):
    """Send new message notification email"""
    return send_email_async.delay(
        [recipient_email],
        f"New Message on Ticket: {ticket_data['id']}",
        'new_message.html',
        ticket=ticket_data,
        message=message_data
    )
