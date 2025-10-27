from celery import Celery
import os

def make_celery(app):
    celery = Celery(
        app.import_name,
        backend=app.config['CELERY_RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL']
    )
    
    celery.conf.update(app.config)
    
    class ContextTask(celery.Task):
        """Make celery tasks work with Flask app context."""
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)
    
    celery.Task = ContextTask
    return celery

# Celery configuration
class CeleryConfig:
    broker_url = os.environ.get('CELERY_BROKER_URL', 'redis://localhost:6379/0')
    result_backend = os.environ.get('CELERY_RESULT_BACKEND', 'redis://localhost:6379/0')
    
    # Task settings
    task_serializer = 'json'
    accept_content = ['json']
    result_serializer = 'json'
    timezone = 'UTC'
    enable_utc = True
    
    # Task routing
    task_routes = {
        'app.tasks.email_tasks.*': {'queue': 'email'},
        'app.tasks.webhook_tasks.*': {'queue': 'webhooks'},
    }
    
    # Task retry settings
    task_acks_late = True
    worker_prefetch_multiplier = 1
    
    # Beat schedule for periodic tasks
    beat_schedule = {
        'check-sla-violations': {
            'task': 'app.tasks.sla_tasks.check_sla_violations',
            'schedule': 300.0,  # Every 5 minutes
        },
        'send-daily-digest': {
            'task': 'app.tasks.email_tasks.send_daily_digest',
            'schedule': 86400.0,  # Daily
        },
    }
