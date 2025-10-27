from flask import Blueprint, jsonify

export_bp = Blueprint('export', __name__)

@export_bp.route('/templates', methods=['GET'])
def get_export_templates():
    """Get available export templates"""
    templates = [
        {'id': 'summary', 'name': 'Summary Report', 'formats': ['csv']},
        {'id': 'detailed', 'name': 'Detailed Report', 'formats': ['csv']}
    ]
    return jsonify(templates)