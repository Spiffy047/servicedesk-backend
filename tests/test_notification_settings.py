import unittest
import json
from app import create_app, db
from app.models.notification_settings import NotificationSettings
from app.models.user import User

class TestNotificationSettingsAPI(unittest.TestCase):
    
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
        db.create_all()
        
        # Create test user
        self.test_user = User(
            id='user1',
            name='Test User',
            email='test@example.com',
            role='Normal User'
        )
        db.session.add(self.test_user)
        db.session.commit()
    
    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
    
    def test_get_notification_settings_creates_default(self):
        """Test getting notification settings creates default if none exist"""
        response = self.client.get('/api/notification_settings/user1')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        
        self.assertEqual(data['user_id'], 'user1')
        self.assertTrue(data['email_enabled'])
        self.assertTrue(data['new_ticket_email'])
    
    def test_update_notification_settings(self):
        """Test updating notification settings"""
        update_data = {
            'email_enabled': False,
            'new_ticket_email': False,
            'digest_frequency': 'daily'
        }
        
        response = self.client.put(
            '/api/notification_settings/user1',
            data=json.dumps(update_data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        
        self.assertFalse(data['email_enabled'])
        self.assertFalse(data['new_ticket_email'])
        self.assertEqual(data['digest_frequency'], 'daily')
    
    def test_reset_notification_settings(self):
        """Test resetting notification settings to defaults"""
        # First update settings
        settings = NotificationSettings(
            id='settings1',
            user_id='user1',
            email_enabled=False
        )
        db.session.add(settings)
        db.session.commit()
        
        # Reset settings
        response = self.client.delete('/api/notification_settings/user1')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        
        self.assertTrue(data['email_enabled'])  # Should be back to default

if __name__ == '__main__':
    unittest.main()
