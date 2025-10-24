import unittest
import json
from app import create_app, db
from app.models.notification_settings import NotificationSettings

class TestNotificationSettingsAPI(unittest.TestCase):
    
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
        db.create_all()
    
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

if __name__ == '__main__':
    unittest.main()