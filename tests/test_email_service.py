import unittest
from unittest.mock import patch, MagicMock
from app import create_app, db
from app.services.email_service import EmailService

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

if __name__ == '__main__':
    unittest.main()