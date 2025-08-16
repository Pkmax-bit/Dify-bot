#!/usr/bin/env python3
"""
Test Supabase connection and schema setup
"""

import os
import sys
import httpx
import json


def test_supabase_connection():
    """Test Supabase connection with the provided keys"""
    
    print("🔗 Testing Supabase Connection...")
    
    # Use the keys provided by the user
    supabase_url = "https://fslacfqhvdakkxqcmuoiv.supabase.co"
    supabase_anon_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZzbGFjZnFodmRha2t4Y211b2l2Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTM3NzQzNzcsImV4cCI6MjA2OTM1MDM3N30.Hf0qVEMn9mTcAOBH63iorSkmUMf3jf8nJ2UjUPcYOhE"
    supabase_service_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZzbGFjZnFodmRha2t4Y211b2l2Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1Mzc3NDM3NywiZXhwIjoyMDY5MzUwMzc3fQ.PlL1viNr6nV2Uvt01Ps3vbnH1uFQW_UCyVwyhbdMd54"
    
    print(f"   URL: {supabase_url}")
    print(f"   Anon Key: {supabase_anon_key[:20]}...")
    print(f"   Service Key: {supabase_service_key[:20]}...")
    
    try:
        # Test 1: Basic API connection with anon key
        print("\n1️⃣ Testing basic API connection...")
        response = httpx.get(f"{supabase_url}/rest/v1/", 
                           headers={"apikey": supabase_anon_key},
                           timeout=10.0)
        
        if response.status_code == 200:
            print("✅ Basic API connection successful!")
        else:
            print(f"❌ Basic API connection failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Basic API connection error: {e}")
        return False
    
    try:
        # Test 2: Check if dify_errors table exists
        print("\n2️⃣ Checking if dify_errors table exists...")
        response = httpx.get(f"{supabase_url}/rest/v1/dify_errors?limit=1", 
                           headers={
                               "apikey": supabase_service_key,
                               "Authorization": f"Bearer {supabase_service_key}"
                           },
                           timeout=10.0)
        
        if response.status_code == 200:
            print("✅ dify_errors table exists and accessible!")
            data = response.json()
            print(f"   Response: {len(data)} records found")
        elif response.status_code == 404:
            print("⚠️ dify_errors table does not exist")
            print("   You need to run the setup/supabase_schema.sql in Supabase SQL Editor")
            return False
        else:
            print(f"❌ Table check failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Table check error: {e}")
        return False
    
    try:
        # Test 3: Test inserting a sample error record
        print("\n3️⃣ Testing error record insertion...")
        
        error_data = {
            "type_error": "TestError",
            "node": "test-node",
            "error_message": "This is a test error from the Dify logging system",
            "user_id": "test-user-123",
            "local_error_id": 999
        }
        
        response = httpx.post(f"{supabase_url}/rest/v1/dify_errors", 
                            headers={
                                "apikey": supabase_service_key,
                                "Authorization": f"Bearer {supabase_service_key}",
                                "Content-Type": "application/json"
                            },
                            json=error_data,
                            timeout=10.0)
        
        if response.status_code in [200, 201]:
            print("✅ Error record insertion successful!")
            print(f"   Response: {response.json()}")
        else:
            print(f"❌ Error record insertion failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error insertion error: {e}")
        return False
    
    try:
        # Test 4: Test retrieving error records
        print("\n4️⃣ Testing error record retrieval...")
        
        response = httpx.get(f"{supabase_url}/rest/v1/dify_errors?user_id=eq.test-user-123&order=created_at.desc&limit=5", 
                           headers={
                               "apikey": supabase_service_key,
                               "Authorization": f"Bearer {supabase_service_key}"
                           },
                           timeout=10.0)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Retrieved {len(data)} error records!")
            if data:
                print(f"   Latest error: {data[0].get('type_error', 'N/A')}")
                print(f"   Error message: {data[0].get('error_message', 'N/A')[:50]}...")
        else:
            print(f"❌ Error retrieval failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error retrieval error: {e}")
        return False
    
    return True


def show_setup_instructions():
    """Show instructions for setting up Supabase schema"""
    
    print("\n" + "=" * 60)
    print("📋 SUPABASE SETUP INSTRUCTIONS")
    print("=" * 60)
    print()
    print("If the dify_errors table doesn't exist, follow these steps:")
    print()
    print("1. Go to your Supabase project dashboard:")
    print("   https://app.supabase.com/project/fslacfqhvdakkxqcmuoiv")
    print()
    print("2. Navigate to 'SQL Editor' in the left sidebar")
    print()
    print("3. Create a new query and copy-paste the content from:")
    print("   D:\\Project\\dify-main\\dify-main\\setup\\supabase_schema.sql")
    print()
    print("4. Run the SQL script to create the dify_errors table and related objects")
    print()
    print("5. Re-run this test script to verify the setup")
    print()
    print("=" * 60)


if __name__ == "__main__":
    print("🚀 Testing Supabase Connection and Setup...")
    print("=" * 50)
    
    success = test_supabase_connection()
    
    if success:
        print("\n🎉 Supabase connection and functionality test passed!")
        print("✅ The logging system can successfully sync errors to Supabase!")
    else:
        print("\n❌ Supabase connection or setup issues detected!")
        show_setup_instructions()
