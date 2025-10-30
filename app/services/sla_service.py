"""
SLA Service Module
Basic SLA monitoring for ServiceDesk
"""

from datetime import datetime, timedelta

class SLAService:
    """Basic SLA service"""
    
    @staticmethod
    def get_sla_target(priority):
        """Get SLA target hours for priority"""
        targets = {
            'Critical': 4,
            'High': 8,
            'Medium': 24,
            'Low': 72
        }
        return targets.get(priority, 24)
    
    @staticmethod
    def check_sla_violation(ticket):
        """Check if ticket violates SLA"""
        if ticket.status == 'Closed':
            return False
            
        target_hours = SLAService.get_sla_target(ticket.priority)
        elapsed_hours = (datetime.utcnow() - ticket.created_at).total_seconds() / 3600
        
        return elapsed_hours > target_hours