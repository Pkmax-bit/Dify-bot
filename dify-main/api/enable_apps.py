#!/usr/bin/env python3
"""
Script to enable API/Site access for all apps in Dify
"""
import requests
import json
import sys
import os

# API Configuration
BASE_URL = "http://localhost:5001"
CONSOLE_API_URL = f"{BASE_URL}/console/api"
API_KEY = "app-o1Lld5KMDsmTKQZjyDBp7J83"

# Headers for authentication
HEADERS = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {API_KEY}',
    'User-Agent': 'Dify-Apps-Enabler/1.0'
}

def get_apps():
    """Get all apps from the API"""
    try:
        print("🔐 Using API key for authentication...")
        response = requests.get(f"{CONSOLE_API_URL}/apps?page=1&limit=100", headers=HEADERS)
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"❌ Failed to get apps: {response.status_code}")
            if response.text:
                try:
                    error_data = response.json()
                    print(f"   Error: {error_data}")
                except:
                    print(f"   Response: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Error getting apps: {e}")
        return None

def enable_app_access(app_id, app_name):
    """Enable API and Site access for an app"""
    try:
        print(f"🔧 Enabling access for: {app_name}")
        
        # Get current app config
        response = requests.get(f"{CONSOLE_API_URL}/apps/{app_id}", headers=HEADERS)
        if response.status_code != 200:
            print(f"❌ Failed to get app {app_name}: {response.status_code}")
            return False
        
        app_data = response.json()
        
        # Update app to enable API and Site access
        update_data = {
            "enable_api": True,
            "enable_site": True,
            "api_rpm": 1000,
            "api_rph": 10000
        }
        
        response = requests.put(
            f"{CONSOLE_API_URL}/apps/{app_id}",
            json=update_data,
            headers=HEADERS
        )
        
        if response.status_code == 200:
            print(f"✅ Successfully enabled access for: {app_name}")
            return True
        else:
            print(f"❌ Failed to enable access for {app_name}: {response.status_code}")
            if response.text:
                try:
                    error_data = response.json()
                    print(f"   Error: {error_data}")
                except:
                    print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error enabling access for {app_name}: {e}")
        return False

def main():
    print("🚀 Starting Dify Apps Enabler...")
    print(f"📡 API Base URL: {BASE_URL}")
    
    # Get all apps
    print("\n📋 Getting all apps...")
    apps_response = get_apps()
    if not apps_response:
        sys.exit(1)
    
    apps = apps_response.get('data', [])
    print(f"📦 Found {len(apps)} apps")
    
    if not apps:
        print("ℹ️  No apps found")
        return
    
    # Display current status
    print("\n📊 Current app status:")
    for app in apps:
        site_status = "✅" if app.get('enable_site') else "❌"
        api_status = "✅" if app.get('enable_api') else "❌"
        print(f"  • {app['name']} ({app['mode']}) - Site: {site_status}, API: {api_status}")
    
    print("\n🔧 Enabling access for all apps...")
    
    # Enable access for all apps
    success_count = 0
    for app in apps:
        if enable_app_access(app['id'], app['name']):
            success_count += 1
    
    print(f"\n🎉 Summary: {success_count}/{len(apps)} apps successfully enabled")
    
    # Verify results
    print("\n🔍 Verifying results...")
    apps_response = get_apps()
    if apps_response:
        apps = apps_response.get('data', [])
        published_apps = [app for app in apps if app.get('enable_site') or app.get('enable_api')]
        print(f"📊 Published apps: {len(published_apps)}/{len(apps)}")
        
        print("\n✨ Final status:")
        for app in apps:
            site_status = "✅" if app.get('enable_site') else "❌"
            api_status = "✅" if app.get('enable_api') else "❌"
            print(f"  • {app['name']} ({app['mode']}) - Site: {site_status}, API: {api_status}")

if __name__ == "__main__":
    main()
