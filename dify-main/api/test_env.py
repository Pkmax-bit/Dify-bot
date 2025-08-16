import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

print("Testing environment variables:")
print(f"SUPABASE_URL: {os.getenv('SUPABASE_URL')}")
print(f"SUPABASE_ANON_KEY: {os.getenv('SUPABASE_ANON_KEY')}")
print(f"SUPABASE_SERVICE_ROLE_KEY: {os.getenv('SUPABASE_SERVICE_ROLE_KEY')}")

# Test Supabase service
from services.supabase_service import SupabaseService

s = SupabaseService()
print(f"\nSupabase Service:")
print(f"URL: {s.url}")
print(f"Keys loaded: {bool(s.anon_key and s.service_role_key)}")

# Test connection
result = s.test_connection()
print(f"\nConnection test: {result}")
