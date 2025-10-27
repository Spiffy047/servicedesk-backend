# Email Service Documentation

## Overview
Complete email notification system for the ServiceDesk application with async processing, templates, and user preferences.

## Features
- ✅ Flask-Mail integration for email sending
- ✅ Celery async task processing
- ✅ Email templates with Jinja2
- ✅ User notification preferences
- ✅ Email delivery logging
- ✅ REST API for management
- ✅ Comprehensive test suite

## Components

### Services
- `EmailService` - Core email sending functionality
- `EmailTasks` - Celery async tasks

### Models
- `EmailLog` - Email delivery tracking
- `NotificationSettings` - User preferences

### API Endpoints
- `GET /api/emails/logs` - Email logs
- `GET /api/emails/stats` - Email statistics
- `GET /api/notification_settings/<user_id>` - Get settings
- `PUT /api/notification_settings/<user_id>` - Update settings

### Templates
- `base.html` - Base email template
- `new_ticket.html` - New ticket notifications
- `status_change.html` - Status change notifications
- `sla_warning.html` - SLA violation alerts
- `new_message.html` - New message notifications

## Usage
```python
from app.services.email_service import EmailService

email_service = EmailService()
email_service.send_email(
    to=['user@example.com'],
    subject='New Ticket',
    template='new_ticket.html',
    ticket=ticket_data
)
```

## Configuration
Set environment variables:
- `MAIL_SERVER` - SMTP server
- `MAIL_PORT` - SMTP port
- `MAIL_USERNAME` - Email username
- `MAIL_PASSWORD` - Email password
- `CELERY_BROKER_URL` - Redis URL for Celery

## Testing
Run tests: `python -m pytest tests/test_email_service.py`