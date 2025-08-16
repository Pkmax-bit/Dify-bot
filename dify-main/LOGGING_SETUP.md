# Hướng dẫn cài đặt và sử dụng hệ thống logging

## 1. Cài đặt dependencies

```bash
cd api
pip install supabase postgrest
```

## 2. Cấu hình Supabase

### Bước 1: Tạo project trên Supabase
1. Truy cập https://supabase.com
2. Tạo project mới
3. Lấy URL và API keys từ Settings > API

### Bước 2: Cập nhật file .env
```env
SUPABASE_URL=https://your-project-id.supabase.co
SUPABASE_ANON_KEY=your-anon-key
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key
```

### Bước 3: Tạo bảng trên Supabase
- Chạy script `setup/supabase_schema.sql` trên Supabase SQL Editor

## 3. Chạy migration

```bash
cd api
python -m flask db upgrade
```

## 4. Kích hoạt middleware

Thêm vào file `app.py` hoặc `dify_app.py`:

```python
from middlewares.chat_logging_middleware import chat_logging_middleware

# Khởi tạo middleware
chat_logging_middleware.init_app(app)
```

## 5. Đăng ký blueprint cho admin APIs

Thêm vào file routes chính:

```python
from controllers.console.admin.logs import bp as admin_logs_bp

app.register_blueprint(admin_logs_bp)
```

## 6. Sử dụng decorator để log functions cụ thể

```python
from middlewares.chat_logging_middleware import log_chat_decorator

@log_chat_decorator
def your_chat_function(app_id, conversation_id, query, **kwargs):
    # Your chat logic here
    return response
```

## 7. API Endpoints cho Admin

### Xem chat logs
```
GET /console/api/admin/chat-logs?page=1&per_page=20&user_id=optional
```

### Xem error logs  
```
GET /console/api/admin/error-logs?page=1&per_page=20&user_id=optional
```

### Xem thống kê
```
GET /console/api/admin/log-stats
```

### Xem lịch sử chat của user
```
GET /console/api/admin/users/{user_id}/chat-history?page=1&per_page=20
```

## 8. Logging thủ công

```python
from services.logging_service import logging_service

# Log chat interaction
logging_service.log_chat_interaction(
    app_id="app_123",
    conversation_id="conv_456", 
    user_id="user_789",
    input_text="Hello AI",
    output_text="Hello! How can I help you?",
    latency_ms=150,
    status_code=200
)

# Log error
logging_service.log_error(
    type_error="ValidationError",
    error_message="Input validation failed",
    user_id="user_789",
    node="chat_endpoint"
)
```

## 9. Xem logs trên Supabase Dashboard

1. Truy cập Supabase Dashboard
2. Vào Table Editor > dify_errors
3. Có thể tạo dashboard để theo dõi lỗi real-time

## 10. Cấu hình bảo mật

- Chỉ admin mới xem được tất cả logs
- User chỉ xem được logs của mình
- Sử dụng RLS trên Supabase để bảo mật dữ liệu

## 11. Tối ưu performance

- Đã tạo indexes cho các trường thường query
- Giới hạn độ dài text để tránh database quá tải
- Sử dụng pagination cho API

## 12. Monitoring

- Theo dõi error rates qua Supabase
- Set up alerts cho error types quan trọng
- Regular cleanup old logs nếu cần
