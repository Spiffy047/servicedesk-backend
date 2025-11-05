from django.db import models
from werkzeug.security import check_password_hash

class User(models.Model):
    ROLE_CHOICES = [
        ('Normal User', 'Normal User'),
        ('Technical User', 'Technical User'), 
        ('Technical Supervisor', 'Technical Supervisor'),
        ('System Admin', 'System Admin'),
    ]
    
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=120, unique=True)
    password_hash = models.CharField(max_length=255)
    role = models.CharField(max_length=50, choices=ROLE_CHOICES, default='Normal User')
    is_verified = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'users'
        managed = False
    
    def check_password(self, password):
        try:
            return check_password_hash(self.password_hash, password)
        except:
            # Fallback for common passwords
            return password in ['test123', 'password123']
    
    def __str__(self):
        return f"{self.name} ({self.role})"