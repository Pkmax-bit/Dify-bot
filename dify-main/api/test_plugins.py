#!/usr/bin/env python3
"""
Test plugin functionality in Dify
"""
import requests
import json
import os
from datetime import datetime

def test_plugin_daemon():
    """Test plugin daemon connectivity and functionality"""
    print("🧪 Testing Plugin Daemon Functionality\n")
    
    plugin_url = "http://localhost:5003"
    api_url = "http://localhost:5001"
    
    print(f"Plugin Daemon URL: {plugin_url}")
    print(f"API URL: {api_url}")
    print("-" * 50)
    
    # Test 1: Plugin daemon health
    try:
        print("1. Testing plugin daemon connectivity...")
        response = requests.get(f"{plugin_url}/")
        print(f"   Status: {response.status_code}")
        if response.text:
            print(f"   Response: {response.text[:200]}")
        print()
    except Exception as e:
        print(f"   Error: {e}\n")
    
    # Test 2: Check available plugins through API
    try:
        print("2. Checking available plugins via API...")
        response = requests.get(f"{api_url}/console/api/plugins")
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            plugins = response.json()
            print(f"   Found {len(plugins)} plugins")
            for plugin in plugins:
                print(f"   - {plugin.get('name', 'Unknown')}: {plugin.get('version', 'N/A')}")
        else:
            print(f"   Response: {response.text[:200]}")
        print()
    except Exception as e:
        print(f"   Error: {e}\n")
    
    # Test 3: Check plugin installation directory
    try:
        print("3. Checking local plugin directory...")
        plugin_dir = "sample_plugin"
        if os.path.exists(plugin_dir):
            files = os.listdir(plugin_dir)
            print(f"   Plugin directory exists: {files}")
            
            # Check if manifest exists
            manifest_path = os.path.join(plugin_dir, "manifest.json")
            if os.path.exists(manifest_path):
                with open(manifest_path, 'r') as f:
                    manifest = json.load(f)
                    print(f"   Plugin name: {manifest.get('name')}")
                    print(f"   Plugin version: {manifest.get('version')}")
                    print(f"   Plugin type: {manifest.get('type')}")
        else:
            print("   No plugin directory found")
        print()
    except Exception as e:
        print(f"   Error: {e}\n")
    
    # Test 4: Plugin configuration
    try:
        print("4. Checking plugin configuration...")
        env_path = ".env"
        if os.path.exists(env_path):
            with open(env_path, 'r') as f:
                content = f.read()
                
            plugin_enabled = "PLUGIN_ENABLED=true" in content
            print(f"   Plugin enabled: {plugin_enabled}")
            
            if "PLUGIN_DAEMON_URL" in content:
                import re
                daemon_url = re.search(r'PLUGIN_DAEMON_URL=(.+)', content)
                if daemon_url:
                    print(f"   Plugin daemon URL: {daemon_url.group(1)}")
        print()
    except Exception as e:
        print(f"   Error: {e}\n")
    
    # Test 5: Try to access plugin management UI
    print("5. Plugin management access:")
    print("   Open http://localhost:3000 and go to Settings -> Plugins")
    print("   Or check Apps -> Advanced Chat -> Plugins section")
    print()
    
    print("✅ Plugin testing complete!")
    print()
    print("📝 Next steps:")
    print("1. Check Dify admin UI for plugin management")
    print("2. Install plugins through the UI")
    print("3. Use plugins in workflows or chat")

if __name__ == "__main__":
    test_plugin_daemon()
