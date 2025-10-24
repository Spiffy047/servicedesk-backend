import unittest
from unittest.mock import patch, MagicMock
from app import create_app, db
from app.services.email_service import EmailService
from app.models.email_log import EmailLog

class TestEmailService(unittest.TestCase):
    
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        
        self.email_service = EmailService(self.app)
    
    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
    
    @patch('app.services.email_service.Mail.send')
    def test_send_email_success(self, mock_send):
        """Test successful email sending"""
        mock_send.return_value = True
        
        result = self.email_service.send_email(
            to=['test@example.com'],
            subject='Test Subject',
            template='new_ticket.html',
            ticket={'id': 'TKT-001', 'title': 'Test Ticket'}
        )
        
        self.assertTrue(result)
        mock_send.assert_called_once()
    
    @patch('app.services.email_service.Mail.send')
    def test_send_email_failure(self, mock_send):
        """Test email sending failure"""
        mock_send.side_effect = Exception('SMTP Error')
        
        result = self.email_service.send_email(
            to=['test@example.com'],
            subject='Test Subject',
            template='new_ticket.html',
            ticket={'id': 'TKT-001', 'title': 'Test Ticket'}
        )
        
        self.assertFalse(result)
    
    def test_send_new_ticket_notification(self):
        """Test new ticket notification"""
        ticket_data = {
            'id': 'TKT-001',
            'title': 'Test Ticket',
            'priority': 'High',
            'status': 'New'
        }
        
        with patch.object(self.email_service, 'send_email') as mock_send:
            mock_send.return_value = True
            
            result = self.email_service.send_new_ticket_notification(
                ticket_data, 'test@example.com'
            )
            
            self.assertTrue(result)
            mock_send.assert_called_once_with(
                to=['test@example.com'],
                subject='New Ticket Created: Test Ticket',
                template='new_ticket.html',
                ticket=ticket_data
            )

if __name__ == '__main__':
    unittest.main()
