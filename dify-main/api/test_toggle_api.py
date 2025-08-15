#!/usr/bin/env python3
import requests
import json
import sys

# API configuration
BASE_URL = "http://localhost:5001"
CONSOLE_API_URL = f"{BASE_URL}/console/api"

def test_app_endpoints():
    """Test the new app toggle endpoints"""
    print("🔧 Testing App Enable/Disable API Endpoints")
    print("=" * 50)
    
    try:
        # 1. Get app list first
        print("📋 Step 1: Getting app list...")
        apps_response = requests.get(f"{CONSOLE_API_URL}/apps")
        
        if apps_response.status_code != 200:
            print(f"❌ Failed to get apps: {apps_response.status_code}")
            print(f"Response: {apps_response.text}")
            return
        
        apps_data = apps_response.json()
        apps = apps_data.get('data', [])
        
        if not apps:
            print("⚠️ No apps found")
            return
            
        print(f"✅ Found {len(apps)} apps")
        
        # Use first app for testing
        test_app = apps[0]
        app_id = test_app['id']
        app_name = test_app['name']
        
        print(f"🎯 Testing with app: {app_name} (ID: {app_id})")
        print(f"Current status - Site: {test_app.get('enable_site', False)}, API: {test_app.get('enable_api', False)}")
        
        # 2. Test Site Enable
        print("\n🌐 Step 2: Testing Site Enable endpoint...")
        site_enable_payload = {"enable_site": True}
        
        site_response = requests.post(
            f"{CONSOLE_API_URL}/apps/{app_id}/site-enable",
            json=site_enable_payload,
            headers={'Content-Type': 'application/json'}
        )
        
        print(f"Site Enable Response: {site_response.status_code}")
        if site_response.status_code == 200:
            print("✅ Site enable endpoint works!")
            result = site_response.json()
            print(f"New site status: {result.get('enable_site', 'Unknown')}")
        else:
            print(f"❌ Site enable failed: {site_response.text}")
        
        # 3. Test API Enable
        print("\n🔗 Step 3: Testing API Enable endpoint...")
        api_enable_payload = {"enable_api": True}
        
        api_response = requests.post(
            f"{CONSOLE_API_URL}/apps/{app_id}/api-enable",
            json=api_enable_payload,
            headers={'Content-Type': 'application/json'}
        )
        
        print(f"API Enable Response: {api_response.status_code}")
        if api_response.status_code == 200:
            print("✅ API enable endpoint works!")
            result = api_response.json()
            print(f"New API status: {result.get('enable_api', 'Unknown')}")
        else:
            print(f"❌ API enable failed: {api_response.text}")
        
        # 4. Test disable
        print("\n❌ Step 4: Testing disable endpoints...")
        
        # Disable site
        site_disable_response = requests.post(
            f"{CONSOLE_API_URL}/apps/{app_id}/site-enable",
            json={"enable_site": False},
            headers={'Content-Type': 'application/json'}
        )
        
        if site_disable_response.status_code == 200:
            print("✅ Site disable works!")
        else:
            print(f"❌ Site disable failed: {site_disable_response.status_code}")
        
        # Disable API
        api_disable_response = requests.post(
            f"{CONSOLE_API_URL}/apps/{app_id}/api-enable",
            json={"enable_api": False},
            headers={'Content-Type': 'application/json'}
        )
        
        if api_disable_response.status_code == 200:
            print("✅ API disable works!")
        else:
            print(f"❌ API disable failed: {api_disable_response.status_code}")
        
        print("\n🎉 API endpoint testing completed!")
        print("✨ Now you can use the toggle buttons in Quick Chat V2")
        
    except Exception as e:
        print(f"❌ Error during testing: {str(e)}")

if __name__ == "__main__":
    test_app_endpoints()
