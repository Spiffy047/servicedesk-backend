from flask import Blueprint, request, jsonify
from app import db
from datetime import datetime, timedelta

analytics_bp = Blueprint('analytics', __name__)

@analytics_bp.route('/dashboard', methods=['GET'])
def get_dashboard():
    """Basic dashboard endpoint"""
    return jsonify({
        'message': 'Analytics dashboard',
        'timestamp': datetime.utcnow().isoformat()
    })