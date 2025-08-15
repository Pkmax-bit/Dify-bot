#!/usr/bin/env python3
"""
Debug Quick Chat V2 - Tại sao không chat được
"""
import json

def debug_quick_chat():
    print("🔍 DEBUG QUICK CHAT V2 - TẠI SAO KHÔNG CHAT ĐƯỢC?")
    print("=" * 60)
    
    print("\n📋 CÁC VẤN ĐỀ THƯỜNG GẶP:")
    print("1. 🚫 Không có Apps:")
    print("   - Chưa tạo app nào trong Dify")
    print("   - Giải pháp: Tạo app mới trong Studio")
    
    print("\n2. 🚫 Apps chưa được Publish:")
    print("   - App có nhưng chưa bật API hoặc Site")
    print("   - Giải pháp: Vào Apps → Settings → Enable API/Site")
    
    print("\n3. 🚫 Apps thiếu Model Config:")
    print("   - App publish nhưng chưa cấu hình model")
    print("   - Giải pháp: Apps → Model Settings → Chọn model")
    
    print("\n4. 🚫 Authentication Error:")
    print("   - Chưa đăng nhập vào Dify")
    print("   - Giải pháp: Đăng nhập http://localhost:3000")
    
    print("\n5. 🚫 API Keys chưa cấu hình:")
    print("   - Model provider chưa có API key")
    print("   - Giải pháp: Settings → Model Providers → Add keys")
    
    print("\n" + "=" * 60)
    print("🎯 CÁCH FIX NHANH:")
    print("1. Mở http://localhost:3000 → Đăng nhập")
    print("2. Studio → Create App → Agent")
    print("3. Model Settings → Chọn OpenAI GPT-3.5")
    print("4. Publish → Bật API và Site")
    print("5. Quick Chat → Chọn app → Chat!")
    
    print("\n🔧 KIỂM TRA DEBUG:")
    print("- Mở Browser Dev Tools (F12)")
    print("- Vào Quick Chat V2")
    print("- Xem Console logs và Network requests")
    print("- Debug info sẽ hiển thị ở cuối trang")
    
    print("\n✅ Quick Chat V2 đã được cập nhật với:")
    print("- Better error messages")
    print("- Published API support") 
    print("- Detailed debug info")
    print("- Token authentication handling")

if __name__ == "__main__":
    debug_quick_chat()
