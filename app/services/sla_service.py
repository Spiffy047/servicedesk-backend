from datetime import datetime, timedelta
from typing import Dict, List
import logging

logger = logging.getLogger(__name__)

class SLAService:
    """Service for SLA calculations and violation detection"""
    
    def __init__(self):
        self.sla_thresholds = {
            'critical': timedelta(hours=4),
            'high': timedelta(hours=8),
            'medium': timedelta(hours=24),
            'low': timedelta(hours=72)
        }
    
    def calculate_sla_status(self, ticket_data: Dict) -> Dict:
        """Calculate SLA status for a ticket"""
        priority = ticket_data.get('priority', 'medium').lower()
        created_at = datetime.fromisoformat(ticket_data['created_at'])
        resolved_at = ticket_data.get('resolved_at')
        
        threshold = self.sla_thresholds.get(priority, self.sla_thresholds['medium'])
        
        if resolved_at:
            resolved_time = datetime.fromisoformat(resolved_at)
            resolution_time = resolved_time - created_at
            is_violated = resolution_time > threshold
        else:
            elapsed_time = datetime.utcnow() - created_at
            is_violated = elapsed_time > threshold
            resolution_time = elapsed_time
        
        return {
            'ticket_id': ticket_data['id'],
            'sla_threshold': threshold.total_seconds(),
            'resolution_time': resolution_time.total_seconds(),
            'is_violated': is_violated,
            'status': 'violated' if is_violated else 'within_sla'
        }
    
    def detect_violations(self, tickets: List[Dict]) -> List[Dict]:
        """Detect SLA violations across multiple tickets"""
        violations = []
        for ticket in tickets:
            sla_status = self.calculate_sla_status(ticket)
            if sla_status['is_violated']:
                violations.append(sla_status)
        return violations
    
    def get_sla_metrics(self, tickets: List[Dict]) -> Dict:
        """Calculate overall SLA metrics"""
        total_tickets = len(tickets)
        if total_tickets == 0:
            return {'total': 0, 'violations': 0, 'compliance_rate': 100.0}
        
        violations = self.detect_violations(tickets)
        violation_count = len(violations)
        compliance_rate = ((total_tickets - violation_count) / total_tickets) * 100
        
        return {
            'total_tickets': total_tickets,
            'violations': violation_count,
            'compliance_rate': round(compliance_rate, 2),
            'violation_details': violations
        }