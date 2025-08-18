import redis
import os

redis_client = redis.Redis(
    host=os.getenv("REDIS_HOST", "localhost"),
    port=int(os.getenv("REDIS_PORT", 6379)),
    db=int(os.getenv("REDIS_DB", 0))
)

try:
    redis_client.ping()
    print("Kết nối Redis thành công!")
except redis.ConnectionError:
    print("Không thể kết nối Redis.")
