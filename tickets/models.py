from django.db import models
from django.conf import settings
from django.utils import timezone

class Ticket(models.Model):
    STATUS_CHOICES = [
        ('New', 'New'),
        ('Open', 'Open'),
        ('In Progress', 'In Progress'),
        ('Pending', 'Pending'),
        ('Resolved', 'Resolved'),
        ('Closed', 'Closed'),
    ]
    
    PRIORITY_CHOICES = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
        ('Critical', 'Critical'),
    ]
    
    ticket_id = models.CharField(max_length=20, unique=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='New')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES)
    category = models.CharField(max_length=50)
    created_by = models.IntegerField()
    assigned_to = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    sla_violated = models.BooleanField(default=False)
    image_url = models.URLField(max_length=500, null=True, blank=True)
    
    class Meta:
        db_table = 'tickets'
        managed = False
    
    def __str__(self):
        return f"{self.ticket_id}: {self.title}"

class Message(models.Model):
    ticket_id = models.IntegerField()
    sender_id = models.IntegerField()
    message = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        db_table = 'messages'
        managed = False
    
    def __str__(self):
        return f"Message on {self.ticket.ticket_id}"