#!/usr/bin/env python3
"""
Tạo demo app tự động cho Quick Chat V2
"""
import os
import json
import time
from pathlib import Path

def create_demo_app():
    """Tạo demo app configuration"""
    print("🎯 Tạo demo app cho Quick Chat V2...")
    
    # Tạo demo model configuration
    demo_config = {
        "system_instruction_template": "You are a helpful AI assistant. Answer questions clearly and concisely.",
        "model_config": {
            "provider": "openai",
            "name": "gpt-3.5-turbo",
            "mode": "chat",
            "completion_params": {
                "temperature": 0.7,
                "max_tokens": 1000
            }
        },
        "user_input_form": [
            {
                "paragraph": {
                    "label": "Query",
                    "variable": "query",
                    "required": True,
                    "default": ""
                }
            }
        ],
        "dataset_configs": {
            "retrieval": {
                "search": {
                    "enabled": False
                }
            }
        }
    }
    
    # Lưu demo configuration
    config_path = Path("demo_app_config.json")
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(demo_config, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Demo app config đã tạo: {config_path}")
    
    # Hướng dẫn setup model
    print("\n📋 Để sử dụng Quick Chat:")
    print("1. Mở Dify: http://localhost:3000")
    print("2. Đăng nhập/Đăng ký")
    print("3. Tạo App mới:")
    print("   - Chọn 'Chatflow' hoặc 'Agent'") 
    print("   - Cấu hình Model (OpenAI, Anthropic, etc.)")
    print("   - Publish app (bật API và Site)")
    print("4. Truy cập Quick Chat: http://localhost:3000/quick-chat-v2")
    print("5. App sẽ xuất hiện trong danh sách để chat!")
    
    return True

def check_model_providers():
    """Kiểm tra model providers có sẵn"""
    print("\n🔍 Model Providers có thể sử dụng:")
    print("- OpenAI (cần API key)")
    print("- Anthropic (cần API key)")  
    print("- Azure OpenAI (cần cấu hình)")
    print("- Local models (Ollama, etc.)")
    print("- Google (Gemini)")
    
    # Kiểm tra .env có API keys chưa
    env_path = Path(".env")
    if env_path.exists():
        with open(env_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        api_keys = [
            "OPENAI_API_KEY",
            "ANTHROPIC_API_KEY", 
            "GOOGLE_API_KEY",
            "AZURE_OPENAI_API_KEY"
        ]
        
        print("\n🔑 API Keys trong .env:")
        for key in api_keys:
            if key in content and f"{key}=" in content:
                # Check if not empty
                lines = content.split('\n')
                for line in lines:
                    if line.startswith(f"{key}=") and len(line.split('=', 1)[1].strip()) > 0:
                        print(f"   ✅ {key} đã cấu hình")
                        break
                else:
                    print(f"   ⚠️ {key} chưa có giá trị")
            else:
                print(f"   ❌ {key} chưa cấu hình")

if __name__ == "__main__":
    create_demo_app()
    check_model_providers()
