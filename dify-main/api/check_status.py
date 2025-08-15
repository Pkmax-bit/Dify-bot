#!/usr/bin/env python3
"""
Simple script to check app status and provide manual instructions
"""
import requests
import json

def check_api_status():
    """Check what we can access"""
    base_url = "http://localhost:5001"
    
    print("🚀 Checking Dify API Status...")
    print(f"📡 Base URL: {base_url}")
    
    # Test endpoints
    endpoints = [
        ("/health", "Health Check"),
        ("/console/api/apps", "Console Apps"),
        ("/v1/apps", "Public Apps"),
        ("/api/apps", "API Apps")
    ]
    
    for endpoint, description in endpoints:
        try:
            response = requests.get(f"{base_url}{endpoint}")
            status = "✅" if response.status_code == 200 else f"❌ ({response.status_code})"
            print(f"  {description}: {status}")
            
            if response.status_code == 200 and 'apps' in endpoint:
                try:
                    data = response.json()
                    if isinstance(data, dict) and 'data' in data:
                        apps_count = len(data['data']) if data['data'] else 0
                        print(f"    -> Found {apps_count} apps")
                except:
                    pass
                    
        except Exception as e:
            print(f"  {description}: ❌ (Error: {e})")
    
    print("\n" + "="*60)
    print("📋 MANUAL STEPS TO ENABLE APPS:")
    print("="*60)
    print("1. 🌐 Open browser and go to: http://localhost:3000/apps")
    print("2. 🔑 Login if prompted")
    print("3. 📱 For each app you want to enable:")
    print("   a) Click on the app")
    print("   b) Look for 'Publish' or 'Settings' button")
    print("   c) Enable 'API Access' or 'Website Access'")
    print("   d) Click 'Save' or 'Publish'")
    print("4. 🔄 Go back to Quick Chat V2 and refresh")
    print("5. ✅ Your apps should now appear as published!")
    print("="*60)

if __name__ == "__main__":
    check_api_status()
