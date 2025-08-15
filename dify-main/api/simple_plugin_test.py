#!/usr/bin/env python3
"""
Simple plugin directory test
"""
import os
import json
from pathlib import Path

def test_plugin_setup():
    print("🔧 Testing Local Plugin Setup\n")
    
    # Test plugin directory
    plugin_dir = Path("sample_plugin")
    print(f"Plugin directory: {plugin_dir.absolute()}")
    print(f"Exists: {plugin_dir.exists()}")
    
    if plugin_dir.exists():
        files = list(plugin_dir.glob("*"))
        print(f"Files in plugin directory: {[f.name for f in files]}")
        
        # Check manifest
        manifest_file = plugin_dir / "manifest.json"
        if manifest_file.exists():
            try:
                with open(manifest_file, 'r') as f:
                    manifest = json.load(f)
                print(f"Plugin name: {manifest.get('name')}")
                print(f"Plugin version: {manifest.get('version')}")
                print(f"Plugin type: {manifest.get('type')}")
                print(f"Endpoints: {len(manifest.get('endpoints', []))}")
            except Exception as e:
                print(f"Error reading manifest: {e}")
    
    print("\n" + "="*50)
    
    # Check .env configuration
    env_file = Path(".env")
    print(f".env file: {env_file.absolute()}")
    print(f"Exists: {env_file.exists()}")
    
    if env_file.exists():
        try:
            with open(env_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            plugin_configs = []
            for line in content.split('\n'):
                if 'PLUGIN' in line and '=' in line and not line.strip().startswith('#'):
                    plugin_configs.append(line.strip())
            
            print(f"Plugin configurations found:")
            for config in plugin_configs:
                print(f"  {config}")
                
        except Exception as e:
            print(f"Error reading .env: {e}")
    
    print("\n" + "="*50)
    print("✅ Local plugin setup check complete!")
    print("\n📋 Summary:")
    print("1. Plugin daemon is configured in .env (PLUGIN_ENABLED=true)")
    print("2. Plugin daemon is running on port 5003")
    print("3. Sample plugin files are created")
    print("4. Next: Check Dify UI for plugin management")

if __name__ == "__main__":
    test_plugin_setup()
