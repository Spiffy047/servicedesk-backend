# SLA Service - Service Level Agreement monitoring and compliance
# 💡 PRESENTATION HINT: "Real-time SLA tracking with priority-based thresholds"
from datetime import datetime, timedelta
from typing import Dict, List
import logging

logger = logging.getLogger(__name__)

class SLAService:
    """Service for SLA calculations and violation detection
    💡 PRESENTATION HINT: "Automated SLA monitoring prevents service level breaches"
    """
    
    def __init__(self):
        # Priority-based SLA thresholds
        self.sla_thresholds = {
            'critical': timedelta(hours=4),   # Mission-critical issues
            'high': timedelta(hours=8),       # High-impact problems
            'medium': timedelta(hours=24),    # Standard requests
            'low': timedelta(hours=72)        # Low-priority items
        }
    
    def calculate_sla_status(self, ticket_data: Dict) -> Dict:
        """Calculate SLA status for a ticket
        💡 PRESENTATION HINT: "Real-time SLA calculation based on priority and timestamps"
        """
        priority = ticket_data.get('priority', 'medium').lower()
        created_at = datetime.fromisoformat(ticket_data['created_at'])
        resolved_at = ticket_data.get('resolved_at')
        
        # Get priority-specific threshold
        threshold = self.sla_thresholds.get(priority, self.sla_thresholds['medium'])
        
        # Calculate violation status
        if resolved_at:
            # Closed ticket - check final resolution time
            resolved_time = datetime.fromisoformat(resolved_at)
            resolution_time = resolved_time - created_at
            is_violated = resolution_time > threshold
        else:
            # Open ticket - check current elapsed time
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
        """Calculate overall SLA metrics
        💡 PRESENTATION HINT: "Comprehensive SLA dashboard metrics for management reporting"
        """
        total_tickets = len(tickets)
        if total_tickets == 0:
            return {'total': 0, 'violations': 0, 'compliance_rate': 100.0}
        
        # Calculate violations and compliance rate
        violations = self.detect_violations(tickets)
        violation_count = len(violations)
        compliance_rate = ((total_tickets - violation_count) / total_tickets) * 100
        
        return {
            'total_tickets': total_tickets,
            'violations': violation_count,
            'compliance_rate': round(compliance_rate, 2),
            'violation_details': violations
        }
