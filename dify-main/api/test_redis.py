import redis

# Kết nối tới Redis ở localhost, cổng 6379
r = redis.Redis(host='localhost', port=6379, db=0)

# Ví dụ: lưu và lấy dữ liệu
r.set('foo', 'bar')
print(r.get('foo'))  # b'bar'