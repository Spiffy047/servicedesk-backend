from flask import Blueprint

analytics_bp = Blueprint('analytics', __name__)

@analytics_bp.route('/health', methods=['GET'])
def health_check():
    """Basic health check for analytics module"""
    return {'status': 'analytics module initialized'}