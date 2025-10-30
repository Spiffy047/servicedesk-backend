#!/usr/bin/env python3
"""
Test Script for Backend API Enhancements
Verifies that all new modules can be imported and basic functionality works.
"""

import sys
import os

# Add the app directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

def test_imports():
    """Test that all new modules can be imported successfully"""
    print("🧪 Testing module imports...")
    
    try:
        # Test analytics routes
        from app.routes.analytics import analytics_bp
        print("✅ Analytics routes imported successfully")
        
        # Test export routes  
        from app.routes.export import export_bp
        print("✅ Export routes imported successfully")
        
        # Test users routes
        from app.routes.users import users_bp
        print("✅ Users routes imported successfully")
        
        # Test SLA routes
        from app.routes.sla import sla_bp
        print("✅ SLA routes imported successfully")
        
        # Test SLA service
        from app.services.sla_service import SLAService
        print("✅ SLA service imported successfully")
        
        # Test notification service
        from app.services.notification_service import NotificationService
        print("✅ Notification service imported successfully")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def test_sla_service():
    """Test basic SLA service functionality"""
    print("\n🧪 Testing SLA Service...")
    
    try:
        from app.services.sla_service import SLAService
        
        # Test SLA target retrieval
        critical_target = SLAService.get_sla_target('Critical')
        assert critical_target == 4, f"Expected 4 hours for Critical, got {critical_target}"
        print("✅ SLA target calculation works")
        
        # Test SLA service initialization
        sla_service = SLAService()
        print("✅ SLA service initialization works")
        
        return True
        
    except Exception as e:
        print(f"❌ SLA service test failed: {e}")
        return False

def test_notification_service():
    """Test basic notification service functionality"""
    print("\n🧪 Testing Notification Service...")
    
    try:
        from app.services.notification_service import NotificationService
        
        # Test notification service initialization
        notification_service = NotificationService()
        print("✅ Notification service initialization works")
        
        # Test email template access
        templates = notification_service.email_templates
        assert 'ticket_created' in templates, "Missing ticket_created template"
        print("✅ Email templates loaded correctly")
        
        # Test preference retrieval
        prefs = NotificationService.get_notification_preferences('test_user')
        assert 'email_enabled' in prefs, "Missing email_enabled preference"
        print("✅ Notification preferences work")
        
        return True
        
    except Exception as e:
        print(f"❌ Notification service test failed: {e}")
        return False

def test_blueprint_registration():
    """Test that blueprints are properly configured"""
    print("\n🧪 Testing Blueprint Registration...")
    
    try:
        from app.routes.analytics import analytics_bp
        from app.routes.export import export_bp
        from app.routes.users import users_bp
        from app.routes.sla import sla_bp
        
        # Check blueprint names
        assert analytics_bp.name == 'analytics', f"Wrong analytics blueprint name: {analytics_bp.name}"
        assert export_bp.name == 'export', f"Wrong export blueprint name: {export_bp.name}"
        assert users_bp.name == 'users', f"Wrong users blueprint name: {users_bp.name}"
        assert sla_bp.name == 'sla', f"Wrong sla blueprint name: {sla_bp.name}"
        
        print("✅ All blueprints properly configured")
        return True
        
    except Exception as e:
        print(f"❌ Blueprint test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Starting Backend API Enhancement Tests\n")
    
    tests = [
        test_imports,
        test_sla_service,
        test_notification_service,
        test_blueprint_registration
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Implementation is ready.")
        return 0
    else:
        print("⚠️  Some tests failed. Please check the implementation.")
        return 1

if __name__ == "__main__":
    sys.exit(main())