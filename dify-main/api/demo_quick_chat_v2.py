#!/usr/bin/env python3
"""
Demo Quick Chat V2 One-Stop Solution
- Tự động tạo sample apps để test
- Kiểm tra auto-setup functionality
- Demo workflow click-to-chat
"""

import requests
import json
import time
from datetime import datetime

# API Base URL
BASE_URL = "http://localhost:5001"

def create_sample_apps():
    """Tạo các sample apps để demo Quick Chat V2"""
    
    sample_apps = [
        {
            "name": "🤖 AI Assistant",
            "mode": "chat",
            "description": "General AI assistant for questions and tasks",
            "icon": "🤖",
            "icon_background": "#3B82F6"
        },
        {
            "name": "📚 Study Helper",
            "mode": "completion", 
            "description": "Help with studying and learning",
            "icon": "📚",
            "icon_background": "#10B981"
        },
        {
            "name": "🔍 Research Workflow",
            "mode": "workflow",
            "description": "Research and analysis workflow",
            "icon": "🔍", 
            "icon_background": "#F59E0B"
        },
        {
            "name": "💼 Business Advisor",
            "mode": "advanced-chat",
            "description": "Business strategy and advice",
            "icon": "💼",
            "icon_background": "#8B5CF6"
        }
    ]
    
    print("🚀 Creating sample apps for Quick Chat V2 demo...")
    
    for app_data in sample_apps:
        try:
            # Create app
            response = requests.post(f"{BASE_URL}/apps", json=app_data)
            if response.status_code in [200, 201]:
                app = response.json()
                app_id = app.get('id') or app.get('data', {}).get('id')
                print(f"✅ Created: {app_data['name']} (ID: {app_id})")
                time.sleep(0.5)
            else:
                print(f"❌ Failed to create {app_data['name']}: {response.status_code}")
                
        except Exception as e:
            print(f"⚠️ Error creating {app_data['name']}: {e}")
    
    print("\n🎯 Sample apps created! Go to Quick Chat V2 to see auto-setup in action.")

def check_quick_chat_status():
    """Kiểm tra trạng thái Quick Chat V2"""
    
    print("\n🔍 Checking Quick Chat V2 status...")
    
    try:
        # Check apps endpoint
        response = requests.get(f"{BASE_URL}/apps?page=1&limit=100")
        if response.status_code == 200:
            apps = response.json().get('data', [])
            print(f"📊 Total apps available: {len(apps)}")
            
            published_count = 0
            configured_count = 0
            
            for app in apps:
                if app.get('enable_site') or app.get('enable_api'):
                    published_count += 1
                if app.get('model_config'):
                    configured_count += 1
            
            print(f"📤 Published apps: {published_count}")
            print(f"⚙️ Configured apps: {configured_count}")
            print(f"🔧 Auto-setup candidates: {len(apps) - published_count}")
            
        else:
            print(f"❌ Apps endpoint error: {response.status_code}")
            
    except Exception as e:
        print(f"⚠️ Status check error: {e}")

def demo_auto_setup():
    """Demo auto-setup process"""
    
    print("\n🎭 Quick Chat V2 One-Stop Demo:")
    print("1. 🎯 Click any chatflow in the left panel")
    print("2. ⚡ Auto-setup will:")
    print("   - 🔄 Auto-publish (enable API & Site)")
    print("   - 🤖 Auto-configure model (GPT-3.5-turbo)")
    print("   - ✅ Show 'Ready for chat' status")
    print("3. 💬 Start chatting immediately!")
    print("4. 🚀 No need to go to workspace/studio")
    
    print("\n🔧 Features:")
    print("- ⚡ One-click setup")
    print("- 🤖 Auto model configuration") 
    print("- 📤 Auto publishing")
    print("- 💬 Direct chat without workspace")
    print("- 🔄 Multiple API fallback strategies")
    print("- 🎯 Works with all app types (chat/workflow/completion)")

def main():
    """Main demo function"""
    
    print("=" * 60)
    print("🚀 QUICK CHAT V2 ONE-STOP SOLUTION DEMO")
    print("=" * 60)
    
    # Check status first
    check_quick_chat_status()
    
    # Create sample apps
    create_sample_apps()
    
    # Show demo info
    demo_auto_setup()
    
    print("\n" + "=" * 60)
    print("🎯 Ready to test!")
    print("📱 Open: http://localhost:3000/quick-chat-v2")
    print("🎪 Click any chatflow to see auto-setup magic!")
    print("=" * 60)

if __name__ == "__main__":
    main()
