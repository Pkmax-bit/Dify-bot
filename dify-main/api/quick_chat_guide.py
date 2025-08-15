#!/usr/bin/env python3
"""
Hướng dẫn setup Quick Chat V2 với demo data
"""

def show_setup_guide():
    print("🚀 HƯỚNG DẪN SETUP QUICK CHAT V2")
    print("=" * 50)
    
    print("\n1️⃣ CÁC CÁCH SETUP MODEL:")
    print("   🅰️ Sử dụng API Keys:")
    print("      - Thêm OPENAI_API_KEY vào .env")
    print("      - Hoặc ANTHROPIC_API_KEY")
    print("      - Hoặc GOOGLE_API_KEY")
    
    print("\n   🅱️ Sử dụng Local Model (Ollama):")
    print("      - Tải Ollama: https://ollama.com/")
    print("      - Chạy: ollama pull llama2")
    print("      - Dify sẽ tự detect Ollama")
    
    print("\n2️⃣ SETUP QUICK CHAT:")
    print("   ✅ Mở: http://localhost:3000")
    print("   ✅ Đăng nhập/Đăng ký tài khoản")
    print("   ✅ Tạo App mới:")
    print("      - Studio → Create App")
    print("      - Chọn Agent hoặc Chatflow") 
    print("      - Cấu hình model trong Model Settings")
    print("      - Publish app (switch on API và Site)")
    
    print("\n3️⃣ SỬ DỤNG QUICK CHAT:")
    print("   ✅ Truy cập: http://localhost:3000/quick-chat-v2")
    print("   ✅ App sẽ xuất hiện trong danh sách")
    print("   ✅ Click vào app để chat!")
    
    print("\n" + "=" * 50)
    print("🔧 TROUBLESHOOTING:")
    print("   ❌ Không thấy apps? → Chưa publish apps")
    print("   ❌ Không chat được? → Chưa cấu hình model")
    print("   ❌ Lỗi model? → Cần API key hoặc local model")
    
    print("\n🎯 DEMO NHANH:")
    print("   1. Cài Ollama: https://ollama.com/")
    print("   2. Chạy: ollama pull llama2")
    print("   3. Vào Dify → Model Providers → Ollama")
    print("   4. Tạo app với Ollama model")
    print("   5. Publish và chat thôi!")
    
    print("\n✅ Cấu hình API và Storage đã sẵn sàng!")
    
if __name__ == "__main__":
    show_setup_guide()
