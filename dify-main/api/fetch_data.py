import os
import json
from dotenv import load_dotenv
from supabase import create_client, Client

# Tải các biến môi trường từ file .env
load_dotenv()

# Lấy thông tin kết nối Supabase từ các biến môi trường
# Chúng ta sử dụng SERVICE_ROLE_KEY để có toàn quyền truy cập dữ liệu (bỏ qua RLS)
url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")

# Kiểm tra xem các biến đã được tải chưa
if not url or not key:
    print("Lỗi: Không tìm thấy SUPABASE_URL hoặc SUPABASE_SERVICE_ROLE_KEY trong file .env.")
    exit()

print("✅ Đã tải thông tin cấu hình thành công.")
print(f"Đang kết nối đến Supabase URL: {url[:30]}...")

try:
    # Khởi tạo Supabase client
    supabase: Client = create_client(url, key)
    print("✅ Kết nối đến Supabase thành công!")

    # --- THỰC HIỆN TRUY VẤN DỮ LIỆU ---
    # GHI CHÚ: 'messages' là tên bảng phổ biến trong Dify.
    # Nếu không có dữ liệu, bạn có thể thử các tên bảng khác như:
    # 'apps', 'datasets', 'documents', 'users'
    table_to_query = 'error_logs'
    
    print(f"\n🚀 Đang truy vấn 10 dòng đầu tiên từ bảng '{table_to_query}'...")
    
    # Lấy tất cả các cột (*), giới hạn 10 kết quả
    response = supabase.table(table_to_query).select("*").limit(10).execute()

    # Kiểm tra và in kết quả
    if response.data:
        print(f"\n🎉 Tìm thấy {len(response.data)} bản ghi. Dưới đây là dữ liệu:")
        # In dữ liệu ra màn hình dưới dạng JSON cho dễ đọc
        for i, record in enumerate(response.data):
            print(f"\n--- Bản ghi #{i+1} ---")
            print(json.dumps(record, indent=2, ensure_ascii=False))
    else:
        print(f"\n⚠️ Không tìm thấy dữ liệu nào trong bảng '{table_to_query}'.")
        print("Mẹo: Hãy thử đổi tên bảng trong biến `table_to_query` thành 'apps' hoặc 'datasets'.")

except Exception as e:
    print(f"\n❌ Đã xảy ra lỗi nghiêm trọng: {e}")
    print("Vui lòng kiểm tra lại thông tin kết nối trong file .env và chắc chắn rằng bảng bạn truy vấn tồn tại.")