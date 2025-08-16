import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_supabase_connection():
    try:
        from supabase import create_client, Client
        
        # Get Supabase credentials
        supabase_url = os.getenv('SUPABASE_URL')
        supabase_key = os.getenv('SUPABASE_ANON_KEY')
        
        print(f"Supabase URL: {supabase_url}")
        print(f"Supabase Key: {supabase_key[:20]}..." if supabase_key else "No key")
        
        if not supabase_url or not supabase_key:
            print("ERROR: Supabase credentials not found in environment")
            return False
        
        # Create client
        supabase: Client = create_client(supabase_url, supabase_key)
        print("✅ Supabase client created successfully")
        
        # Test connection by querying error table
        response = supabase.table('error').select('*').limit(1).execute()
        print(f"✅ Successfully connected to Supabase. Found {len(response.data)} records")
        
        if response.data:
            print(f"Sample record: {response.data[0]}")
        
        return True
        
    except ImportError as e:
        print(f"ERROR: Supabase library not found: {e}")
        return False
    except Exception as e:
        print(f"ERROR: Failed to connect to Supabase: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("Testing Supabase connection...")
    success = test_supabase_connection()
    if success:
        print("✅ Supabase connection test passed")
    else:
        print("❌ Supabase connection test failed")
        sys.exit(1)
