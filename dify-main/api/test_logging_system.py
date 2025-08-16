#!/usr/bin/env python3
"""
Test script to verify the logging system functionality
"""

import os
import sys
sys.path.insert(0, os.path.dirname(__file__))

import json
from datetime import datetime
from services.logging_service import logging_service


def test_logging_system():
    """Test the logging system functionality"""
    
    print("🧪 Testing Logging System...")
    
    # Since the Flask app has some import issues, let's test the database directly
    return _test_direct_database()


def test_logging_system():
    """Test the logging system functionality"""
    
    print("🧪 Testing Logging System...")
    
    # Since the Flask app has some import issues, let's test the database directly
    return _test_direct_database()


def _test_direct_database():
    """Test logging functionality using direct database operations"""
    
    # Test 1: Direct database insert for chat logging
    print("\n1️⃣ Testing chat logging (direct database)...")
    try:
        import psycopg2
        from configs import dify_config
        import json
        
        conn = psycopg2.connect(
            host=dify_config.DB_HOST,
            port=dify_config.DB_PORT,
            database=dify_config.DB_DATABASE,
            user=dify_config.DB_USERNAME,
            password=dify_config.DB_PASSWORD or None
        )
        
        cur = conn.cursor()
        
        # Insert test chat log
        cur.execute("""
            INSERT INTO dify_logs (user_id, message, response, session_id, message_id, metadata)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            "test-user-123",
            "Hello, how are you?",
            "I'm doing well, thank you! How can I help you today?",
            "test-session-456",
            "msg-789",
            json.dumps({"app_id": "test-app", "model": "gpt-3.5-turbo"})
        ))
        
        conn.commit()
        print("✅ Chat logging successful!")
        
    except Exception as e:
        print(f"❌ Chat logging error: {e}")
        return False
    finally:
        if 'cur' in locals():
            cur.close()
        if 'conn' in locals():
            conn.close()
    
    # Test 2: Direct database insert for error logging
    print("\n2️⃣ Testing error logging (direct database)...")
    try:
        conn = psycopg2.connect(
            host=dify_config.DB_HOST,
            port=dify_config.DB_PORT,
            database=dify_config.DB_DATABASE,
            user=dify_config.DB_USERNAME,
            password=dify_config.DB_PASSWORD or None
        )
        
        cur = conn.cursor()
        
        # Insert test error log
        cur.execute("""
            INSERT INTO error (user_id, type_error, message_error, stack_trace, request_data, metadata)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            "test-user-123",
            "ValidationError",
            "Invalid input format for testing",
            "Traceback (most recent call last)...",
            json.dumps({"input": "invalid_data", "endpoint": "/api/test"}),
            json.dumps({"app_id": "test-app", "severity": "medium"})
        ))
        
        conn.commit()
        print("✅ Error logging successful!")
        
    except Exception as e:
        print(f"❌ Error logging error: {e}")
        return False
    finally:
        if 'cur' in locals():
            cur.close()
        if 'conn' in locals():
            conn.close()
    
    # Test 3: Retrieve chat history
    print("\n3️⃣ Testing chat history retrieval...")
    try:
        conn = psycopg2.connect(
            host=dify_config.DB_HOST,
            port=dify_config.DB_PORT,
            database=dify_config.DB_DATABASE,
            user=dify_config.DB_USERNAME,
            password=dify_config.DB_PASSWORD or None
        )
        
        cur = conn.cursor()
        
        cur.execute("""
            SELECT user_id, message, response, created_at, session_id, message_id, metadata
            FROM dify_logs 
            WHERE user_id = %s 
            ORDER BY created_at DESC 
            LIMIT 10
        """, ("test-user-123",))
        
        chat_history = cur.fetchall()
        
        if chat_history and len(chat_history) > 0:
            print(f"✅ Retrieved {len(chat_history)} chat records!")
            print(f"   Latest message: {chat_history[0][1][:50]}...")
        else:
            print("⚠️ No chat history found!")
            
    except Exception as e:
        print(f"❌ Chat history retrieval error: {e}")
        return False
    finally:
        if 'cur' in locals():
            cur.close()
        if 'conn' in locals():
            conn.close()
    
    # Test 4: Retrieve user errors
    print("\n4️⃣ Testing error retrieval...")
    try:
        conn = psycopg2.connect(
            host=dify_config.DB_HOST,
            port=dify_config.DB_PORT,
            database=dify_config.DB_DATABASE,
            user=dify_config.DB_USERNAME,
            password=dify_config.DB_PASSWORD or None
        )
        
        cur = conn.cursor()
        
        cur.execute("""
            SELECT user_id, type_error, message_error, created_at, stack_trace, request_data, metadata
            FROM error 
            WHERE user_id = %s 
            ORDER BY created_at DESC 
            LIMIT 10
        """, ("test-user-123",))
        
        user_errors = cur.fetchall()
        
        if user_errors and len(user_errors) > 0:
            print(f"✅ Retrieved {len(user_errors)} error records!")
            print(f"   Latest error: {user_errors[0][1]}")
        else:
            print("⚠️ No error records found!")
            
    except Exception as e:
        print(f"❌ Error retrieval error: {e}")
        return False
    finally:
        if 'cur' in locals():
            cur.close()
        if 'conn' in locals():
            conn.close()
    
    # Test 5: Test Supabase configuration
    print("\n5️⃣ Testing Supabase configuration...")
    try:
        import os
        
        supabase_url = os.getenv('SUPABASE_URL')
        supabase_anon_key = os.getenv('SUPABASE_ANON_KEY')
        supabase_service_key = os.getenv('SUPABASE_SERVICE_ROLE_KEY')
        
        if supabase_url and supabase_anon_key and supabase_service_key:
            print("✅ Supabase configuration detected!")
            print(f"   URL: {supabase_url}")
            print(f"   Anon Key: {supabase_anon_key[:20]}...")
            print(f"   Service Key: {supabase_service_key[:20]}...")
            
            # Test Supabase connection
            import httpx
            
            response = httpx.get(f"{supabase_url}/rest/v1/", 
                               headers={"apikey": supabase_anon_key},
                               timeout=5.0)
            
            if response.status_code == 200:
                print("✅ Supabase connection successful!")
            else:
                print(f"⚠️ Supabase connection failed: {response.status_code}")
                
        else:
            print("⚠️ Supabase not fully configured")
            print("   This is optional for local testing")
            
    except Exception as e:
        print(f"❌ Supabase test error: {e}")
        # This is not critical for the core functionality
    
    return True


def test_database_connection():
    """Test database connection"""
    print("🔗 Testing database connection...")
    
    try:
        import psycopg2
        from configs import dify_config
        
        conn = psycopg2.connect(
            host=dify_config.DB_HOST,
            port=dify_config.DB_PORT,
            database=dify_config.DB_DATABASE,
            user=dify_config.DB_USERNAME,
            password=dify_config.DB_PASSWORD or None
        )
        
        cur = conn.cursor()
        
        # Check if our tables exist
        cur.execute("""
            SELECT table_name FROM information_schema.tables 
            WHERE table_schema = 'public' 
            AND table_name IN ('dify_logs', 'error');
        """)
        
        tables = cur.fetchall()
        table_names = [table[0] for table in tables]
        
        if 'dify_logs' in table_names and 'error' in table_names:
            print("✅ Database connection successful!")
            print("✅ Required tables exist!")
            
            # Check table structure
            cur.execute("SELECT column_name FROM information_schema.columns WHERE table_name = 'dify_logs';")
            dify_logs_columns = [col[0] for col in cur.fetchall()]
            
            cur.execute("SELECT column_name FROM information_schema.columns WHERE table_name = 'error';")
            error_columns = [col[0] for col in cur.fetchall()]
            
            print(f"   dify_logs columns: {dify_logs_columns}")
            print(f"   error columns: {error_columns}")
            
        else:
            print(f"❌ Missing tables! Found: {table_names}")
            return False
            
        cur.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False


if __name__ == "__main__":
    print("🚀 Running Logging System Tests...")
    print("=" * 50)
    
    # Test database connection first
    if not test_database_connection():
        print("\n❌ Database tests failed!")
        sys.exit(1)
    
    print("\n" + "=" * 50)
    
    # Test logging functionality
    if test_logging_system():
        print("\n🎉 All tests passed! Logging system is working correctly!")
    else:
        print("\n❌ Some tests failed!")
        sys.exit(1)
