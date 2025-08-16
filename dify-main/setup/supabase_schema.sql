-- Tạo bảng dify_errors trên Supabase để lưu thông tin lỗi
-- Chạy script này trên Supabase SQL Editor

CREATE TABLE IF NOT EXISTS public.dify_errors (
    id BIGSERIAL PRIMARY KEY,
    type_error VARCHAR,
    node VARCHAR,
    error_message TEXT,
    user_id VARCHAR(255),
    local_error_id BIGINT, -- ID từ database chính
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Tạo indexes cho performance
CREATE INDEX IF NOT EXISTS idx_dify_errors_user_id ON public.dify_errors(user_id);
CREATE INDEX IF NOT EXISTS idx_dify_errors_type_error ON public.dify_errors(type_error);
CREATE INDEX IF NOT EXISTS idx_dify_errors_created_at ON public.dify_errors(created_at);
CREATE INDEX IF NOT EXISTS idx_dify_errors_local_error_id ON public.dify_errors(local_error_id);

-- Bật Row Level Security (RLS)
ALTER TABLE public.dify_errors ENABLE ROW LEVEL SECURITY;

-- Tạo policy cho admin có thể đọc tất cả
CREATE POLICY "Admin can view all errors" ON public.dify_errors
    FOR SELECT USING (auth.role() = 'service_role');

-- Tạo policy cho service có thể insert
CREATE POLICY "Service can insert errors" ON public.dify_errors
    FOR INSERT WITH CHECK (true);

-- Tạo function để tự động update updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Tạo trigger cho auto update timestamp
CREATE TRIGGER update_dify_errors_updated_at 
    BEFORE UPDATE ON public.dify_errors 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();

-- Tạo view để thống kê lỗi theo ngày
CREATE OR REPLACE VIEW public.error_stats_daily AS
SELECT 
    DATE(created_at) as error_date,
    type_error,
    COUNT(*) as error_count,
    COUNT(DISTINCT user_id) as affected_users
FROM public.dify_errors 
GROUP BY DATE(created_at), type_error
ORDER BY error_date DESC, error_count DESC;

-- Tạo view để thống kê lỗi theo user
CREATE OR REPLACE VIEW public.error_stats_by_user AS
SELECT 
    user_id,
    COUNT(*) as total_errors,
    COUNT(DISTINCT type_error) as unique_error_types,
    MAX(created_at) as last_error_time,
    MIN(created_at) as first_error_time
FROM public.dify_errors 
WHERE user_id IS NOT NULL
GROUP BY user_id
ORDER BY total_errors DESC;

-- Grant permissions
GRANT SELECT ON public.error_stats_daily TO anon, authenticated;
GRANT SELECT ON public.error_stats_by_user TO anon, authenticated;
