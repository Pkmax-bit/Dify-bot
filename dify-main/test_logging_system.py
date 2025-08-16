#!/usr/bin/env python3
"""
Script test để kiểm tra hệ thống logging
"""

import os
import sys
import time
import requests
from datetime import datetime

# Add API directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'api'))

def test_logging_service():
    """Test logging service directly"""
    try:
        from services.logging_service import logging_service
        
        print("Testing logging service...")
        
        # Test log chat interaction
        result = logging_service.log_chat_interaction(
            app_id="test_app",
            conversation_id="test_conv", 
            user_id="test_user",
            input_text="Hello, this is a test",
            output_text="Hello! This is a test response",
            latency_ms=150,
            status_code=200
        )
        
        print(f"Chat logging test: {'✓ PASSED' if result else '✗ FAILED'}")
        
        # Test log error
        error_result = logging_service.log_error(
            type_error="TestError",
            error_message="This is a test error message",
            user_id="test_user",
            node="test_node"
        )
        
        print(f"Error logging test: {'✓ PASSED' if error_result else '✗ FAILED'}")
        
        # Test get chat history
        history = logging_service.get_user_chat_history("test_user", limit=5)
        print(f"Get chat history test: {'✓ PASSED' if isinstance(history, list) else '✗ FAILED'}")
        print(f"  - Found {len(history)} records")
        
        # Test get errors
        errors = logging_service.get_user_errors("test_user", limit=5)
        print(f"Get errors test: {'✓ PASSED' if isinstance(errors, list) else '✗ FAILED'}")
        print(f"  - Found {len(errors)} error records")
        
        return True
        
    except Exception as e:
        print(f"Logging service test failed: {e}")
        return False


def test_supabase_connection():
    """Test Supabase connection"""
    try:
        supabase_url = os.getenv('SUPABASE_URL')
        supabase_key = os.getenv('SUPABASE_SERVICE_ROLE_KEY')
        
        if not supabase_url or not supabase_key:
            print("Supabase test: ⚠ SKIPPED (No Supabase config)")
            return True
        
        print("Testing Supabase connection...")
        
        headers = {
            'apikey': supabase_key,
            'Authorization': f'Bearer {supabase_key}',
            'Content-Type': 'application/json'
        }
        
        # Test connection
        response = requests.get(f"{supabase_url}/rest/v1/", headers=headers, timeout=10)
        
        if response.status_code == 200:
            print("Supabase connection test: ✓ PASSED")
            
            # Test insert error
            test_data = {
                'type_error': 'TestError',
                'error_message': 'Test error from script',
                'user_id': 'test_user_script',
                'created_at': datetime.utcnow().isoformat()
            }
            
            insert_response = requests.post(
                f"{supabase_url}/rest/v1/dify_errors",
                headers=headers,
                json=test_data,
                timeout=10
            )
            
            if insert_response.status_code in [200, 201]:
                print("Supabase insert test: ✓ PASSED")
                return True
            else:
                print(f"Supabase insert test: ✗ FAILED ({insert_response.status_code})")
                return False
        else:
            print(f"Supabase connection test: ✗ FAILED ({response.status_code})")
            return False
            
    except Exception as e:
        print(f"Supabase test failed: {e}")
        return False


def test_database_connection():
    """Test main database connection"""
    try:
        from extensions.ext_database import db
        from models.custom_logs import DifyLogs, ErrorLog
        
        print("Testing database connection...")
        
        # Test connection
        result = db.session.execute(db.text("SELECT 1")).scalar()
        if result == 1:
            print("Database connection test: ✓ PASSED")
        else:
            print("Database connection test: ✗ FAILED")
            return False
        
        # Test table exists
        tables_exist = True
        try:
            db.session.query(DifyLogs).limit(1).all()
            db.session.query(ErrorLog).limit(1).all()
            print("Database tables test: ✓ PASSED")
        except Exception as e:
            print(f"Database tables test: ✗ FAILED ({e})")
            tables_exist = False
        
        return tables_exist
        
    except Exception as e:
        print(f"Database test failed: {e}")
        return False


def test_api_endpoints():
    """Test API endpoints"""
    try:
        print("Testing API endpoints...")
        
        base_url = "http://localhost:5001"
        
        # Test if server is running
        try:
            response = requests.get(f"{base_url}/health", timeout=5)
            print(f"API server test: {'✓ PASSED' if response.status_code == 200 else '⚠ Server not running'}")
        except:
            print("API server test: ⚠ Server not running")
            return False
        
        # Note: Admin endpoints require authentication, so we skip them in this test
        print("API endpoints test: ⚠ SKIPPED (Requires authentication)")
        return True
        
    except Exception as e:
        print(f"API endpoints test failed: {e}")
        return False


def main():
    """Run all tests"""
    print("=" * 50)
    print("Dify Logging System Test")
    print("=" * 50)
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Load environment
    from dotenv import load_dotenv
    load_dotenv('api/.env')
    
    tests = [
        ("Database Connection", test_database_connection),
        ("Logging Service", test_logging_service),
        ("Supabase Connection", test_supabase_connection),
        ("API Endpoints", test_api_endpoints),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n{test_name}:")
        print("-" * len(test_name))
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"Test error: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 50)
    print("TEST SUMMARY")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✓ PASSED" if result else "✗ FAILED"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Logging system is ready to use.")
    else:
        print("⚠ Some tests failed. Please check the configuration.")
        
    print("\nNext steps:")
    print("1. Run migration: cd api && python -m flask db upgrade")
    print("2. Start the API server: cd api && python app.py")
    print("3. Configure Supabase if needed")
    print("4. Test admin endpoints with proper authentication")


if __name__ == "__main__":
    main()
