# Application Configuration - Environment-based settings management
# 💡 PRESENTATION HINT: "Centralized config with environment variables for security"
import os
from datetime import timedelta

class Config:
    """Base configuration class with common settings
    💡 PRESENTATION HINT: "Environment-driven configuration for security and flexibility"
    """
    # Core Flask settings
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///servicedesk.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # JWT Authentication settings
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'jwt-secret-key'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)    # Short-lived for security
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)   # Longer refresh cycle
    
    # Redis Configuration
    REDIS_URL = os.environ.get('REDIS_URL') or 'redis://localhost:6379/0'
    
    # File Upload Configuration
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER') or 'uploads'
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'doc', 'docx', 'xls', 'xlsx'}
    
    # AWS S3 Configuration (for future use)
    AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
    AWS_S3_BUCKET = os.environ.get('AWS_S3_BUCKET')
    AWS_S3_REGION = os.environ.get('AWS_S3_REGION') or 'us-east-1'
    
    # Email Configuration (for future use)
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 587)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() in ['true', 'on', '1']
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    
    # SLA Configuration - Priority-based response times
    SLA_TARGETS = {
        'Critical': 4,   # 4 hours - Mission critical
        'High': 8,       # 8 hours - High impact
        'Medium': 24,    # 24 hours - Standard requests
        'Low': 72        # 72 hours - Low priority
    }
    
    # Celery Configuration (for future async tasks)
    CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL') or 'redis://localhost:6379/0'
    CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND') or 'redis://localhost:6379/0'

class DevelopmentConfig(Config):
    """Development configuration with debug enabled"""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or 'sqlite:///servicedesk_dev.db'

class TestingConfig(Config):
    """Testing configuration with in-memory database"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'  # Fast in-memory testing
    WTF_CSRF_ENABLED = False

class ProductionConfig(Config):
    """Production configuration with enhanced security
    💡 PRESENTATION HINT: "Production-hardened settings with security best practices"
    """
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    
    # Production security settings
    SESSION_COOKIE_SECURE = True      # HTTPS only
    SESSION_COOKIE_HTTPONLY = True    # Prevent XSS
    SESSION_COOKIE_SAMESITE = 'Lax'   # CSRF protection

# Configuration mapping for easy environment switching
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
