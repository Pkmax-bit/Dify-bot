#!/usr/bin/env python3
"""
Plugin Daemon Service for Dify Local Development
Chạy service này để hỗ trợ plugins local
"""

import os
import sys
import subprocess
import time
import requests
import json

def check_plugin_daemon():
    """Check if plugin daemon is running"""
    try:
        response = requests.get("http://localhost:5003/health", timeout=5)
        return response.status_code == 200
    except:
        return False

def start_plugin_daemon():
    """Start the plugin daemon service"""
    print("🔌 Starting Plugin Daemon Service...")
    
    # Set environment variables
    env = os.environ.copy()
    env.update({
        'PLUGIN_DAEMON_PORT': '5003',
        'PLUGIN_DAEMON_HOST': '127.0.0.1',
        'PLUGIN_DAEMON_KEY': 'lYkiYYT6owG+71oLerGzA7GXCgOT++6ovaezWAjpCjf+Sjc3ZtU+qUEi'
    })
    
    # Check if already running
    if check_plugin_daemon():
        print("✅ Plugin Daemon is already running on port 5003")
        return True
    
    try:
        # Try to start plugin daemon (this is a mock implementation)
        # In real Dify, this would be a separate service
        print("⚠️ Plugin Daemon service not found.")
        print("📝 For full plugin support, you would need:")
        print("   1. Dify Plugin Daemon binary")
        print("   2. Plugin runtime environment")
        print("   3. Plugin development tools")
        print("")
        print("💡 Alternative: You can create custom tools instead of plugins")
        print("   - Custom API tools")
        print("   - Custom workflow nodes")
        print("   - Custom model providers")
        
        return False
    except Exception as e:
        print(f"❌ Failed to start plugin daemon: {e}")
        return False

def create_sample_plugin():
    """Create a sample plugin structure"""
    plugin_dir = "sample_plugin"
    
    if not os.path.exists(plugin_dir):
        os.makedirs(plugin_dir)
        print(f"📁 Created plugin directory: {plugin_dir}")
    
    # Create plugin manifest
    manifest = {
        "name": "Sample Local Plugin",
        "version": "1.0.0",
        "description": "A sample plugin for local development",
        "author": "Local Developer",
        "icon": "🔧",
        "type": "tool",
        "endpoints": [
            {
                "name": "hello",
                "method": "POST",
                "path": "/hello",
                "description": "Say hello with custom message"
            }
        ]
    }
    
    manifest_path = os.path.join(plugin_dir, "manifest.json")
    with open(manifest_path, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)
    
    # Create plugin main file
    plugin_code = """
# Sample Plugin Implementation
import json

def hello_endpoint(request_data):
    \"\"\"
    Simple hello endpoint
    \"\"\"
    message = request_data.get('message', 'Hello from Plugin!')
    
    return {
        'status': 'success',
        'response': f"Plugin says: {message}",
        'timestamp': '2025-08-14T13:00:00Z'
    }

# Plugin entry point
def handle_request(endpoint, method, data):
    if endpoint == '/hello' and method == 'POST':
        return hello_endpoint(data)
    else:
        return {'error': 'Endpoint not found'}
"""
    
    plugin_file = os.path.join(plugin_dir, "main.py")
    with open(plugin_file, 'w', encoding='utf-8') as f:
        f.write(plugin_code)
    
    print(f"✅ Created sample plugin files:")
    print(f"   - {manifest_path}")
    print(f"   - {plugin_file}")

def show_plugin_info():
    """Show plugin development information"""
    print("\n🔌 Plugin Development Guide:")
    print("=" * 50)
    
    print("\n📋 Plugin Types:")
    print("  • Tool Plugins: Custom API tools")
    print("  • Model Plugins: Custom LLM providers")
    print("  • Workflow Plugins: Custom workflow nodes")
    
    print("\n🛠️ Plugin Structure:")
    print("  my_plugin/")
    print("  ├── manifest.json    # Plugin metadata")
    print("  ├── main.py          # Plugin logic")
    print("  ├── requirements.txt # Dependencies")
    print("  └── README.md        # Documentation")
    
    print("\n🚀 Development Steps:")
    print("  1. Create plugin directory")
    print("  2. Write manifest.json with plugin info")
    print("  3. Implement plugin logic in main.py")
    print("  4. Test plugin locally")
    print("  5. Install into Dify")
    
    print("\n💡 Alternative Approaches:")
    print("  • Custom API Tools: Add external APIs as tools")
    print("  • Custom Workflow Nodes: Extend workflow capabilities")
    print("  • Custom Model Providers: Add new LLM services")

if __name__ == "__main__":
    print("🔌 Dify Plugin Development Helper")
    print("=" * 40)
    
    # Create sample plugin
    create_sample_plugin()
    
    # Try to start daemon
    daemon_started = start_plugin_daemon()
    
    if not daemon_started:
        show_plugin_info()
    
    print("\n✨ Plugin development environment ready!")
    print("📖 Check the 'sample_plugin' directory for example code")
