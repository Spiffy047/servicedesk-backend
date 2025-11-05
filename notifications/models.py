from django.db import models
from django.conf import settings
from django.utils import timezone

class Alert(models.Model):
    ALERT_TYPE_CHOICES = [
        ('assignment', 'Assignment'),
        ('status_change', 'Status Change'),
        ('sla_violation', 'SLA Violation'),
        ('escalation', 'Escalation'),
    ]
    
    user_id = models.IntegerField()
    ticket_id = models.IntegerField()
    alert_type = models.CharField(max_length=50, choices=ALERT_TYPE_CHOICES)
    title = models.CharField(max_length=200)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        db_table = 'alerts'
        managed = False
    
    def __str__(self):
        return f"Alert for {self.user.username}: {self.title}"