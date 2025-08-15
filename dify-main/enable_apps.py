#!/usr/bin/env python3
"""
Script để enable Site/API access cho tất cả apps
"""

import requests
import json

# API endpoints
BASE_URL = "http://localhost:5001"
CONSOLE_API = f"{BASE_URL}/console/api"

def get_apps():
    """Lấy danh sách tất cả apps"""
    try:
        response = requests.get(f"{CONSOLE_API}/apps?page=1&limit=100")
        if response.status_code == 200:
            data = response.json()
            return data.get('data', [])
        else:
            print(f"Error getting apps: {response.status_code}")
            print(response.text)
            return []
    except Exception as e:
        print(f"Exception getting apps: {e}")
        return []

def enable_app_access(app_id, app_name):
    """Enable Site và API access cho một app"""
    try:
        # Get app details first
        response = requests.get(f"{CONSOLE_API}/apps/{app_id}")
        if response.status_code != 200:
            print(f"Error getting app {app_name}: {response.status_code}")
            return False
            
        app_data = response.json()
        
        # Update app to enable site and api
        update_data = {
            "enable_site": True,
            "enable_api": True
        }
        
        response = requests.put(
            f"{CONSOLE_API}/apps/{app_id}/site",
            json=update_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            print(f"✅ Enabled access for: {app_name}")
            return True
        else:
            print(f"❌ Failed to enable access for {app_name}: {response.status_code}")
            print(response.text)
            return False
            
    except Exception as e:
        print(f"Exception enabling app {app_name}: {e}")
        return False

def main():
    print("🚀 Enabling Site/API access for all apps...")
    print("-" * 50)
    
    # Get all apps
    apps = get_apps()
    if not apps:
        print("❌ No apps found or error getting apps")
        return
    
    print(f"📱 Found {len(apps)} apps:")
    for app in apps:
        print(f"  • {app['name']} ({app['mode']}) - Site: {'✅' if app.get('enable_site') else '❌'}, API: {'✅' if app.get('enable_api') else '❌'}")
    
    print("\n🔧 Enabling access...")
    print("-" * 50)
    
    success_count = 0
    for app in apps:
        if not app.get('enable_site') and not app.get('enable_api'):
            if enable_app_access(app['id'], app['name']):
                success_count += 1
        else:
            print(f"⏭️  Skipped {app['name']} (already enabled)")
            success_count += 1
    
    print("\n" + "=" * 50)
    print(f"✨ Successfully enabled {success_count}/{len(apps)} apps")
    print("🎉 You can now see published apps in Quick Chat V2!")

if __name__ == "__main__":
    main()
