#!/usr/bin/env python3
"""
Tự động setup cấu hình cho Quick Chat V2
"""
import os
import sys
from pathlib import Path

def setup_quick_chat():
    """Setup cấu hình cần thiết cho Quick Chat"""
    print("🚀 Tự động setup Quick Chat V2...")
    print("=" * 50)
    
    # 3. Kiểm tra cấu hình .env
    print("\n3. Kiểm tra cấu hình .env...")
    env_path = Path(".env")
    if env_path.exists():
        with open(env_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        configs_to_check = [
            ("SECRET_KEY", "dify-secret-key"),
            ("STORAGE_TYPE", "opendal"),
            ("OPENDAL_SCHEME", "fs"),
            ("OPENDAL_FS_ROOT", "storage"),
            ("DB_HOST", "localhost"),
            ("REDIS_HOST", "localhost")
        ]
        
        for config, expected in configs_to_check:
            if config in content:
                print(f"   ✅ {config} đã cấu hình")
            else:
                print(f"   ⚠️ {config} chưa cấu hình")
    
    # 4. Tạo thư mục storage nếu chưa có
    print("\n4. Tạo thư mục storage...")
    storage_path = Path("storage")
    if not storage_path.exists():
        storage_path.mkdir()
        print("   ✅ Đã tạo thư mục storage")
    else:
        print("   ✅ Thư mục storage đã tồn tại")
    
    # 5. Hướng dẫn sử dụng
    print("\n" + "=" * 50)
    print("📋 Hướng dẫn sử dụng Quick Chat V2:")
    print("1. Mở trình duyệt: http://localhost:3000")
    print("2. Đăng nhập vào Dify (nếu chưa có tài khoản thì tạo)")
    print("3. Tạo Apps (Chatflow hoặc Workflow)")
    print("4. Publish apps (bật API và Site)")
    print("5. Truy cập Quick Chat V2: http://localhost:3000/quick-chat-v2")
    print("6. Chọn app và bắt đầu chat!")
    
    print("\n✅ Setup hoàn tất!")
    print("🔧 Nếu vẫn không chat được, hãy kiểm tra:")
    print("   - Đã đăng nhập vào Dify chưa?")
    print("   - Có apps nào được publish chưa?")
    print("   - Model configuration có đầy đủ chưa?")
    
    return True

if __name__ == "__main__":
    setup_quick_chat()
