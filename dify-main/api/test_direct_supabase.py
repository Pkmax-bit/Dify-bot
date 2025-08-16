import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_supabase_simple():
    try:
        print("Testing simple Supabase connection...")
        
        # Import required libraries
        import requests
        
        # Get environment variables
        supabase_url = os.getenv('SUPABASE_URL')
        supabase_key = os.getenv('SUPABASE_ANON_KEY')
        
        if not supabase_url or not supabase_key:
            print("❌ Supabase credentials not found")
            return False
        
        print(f"✅ Supabase URL: {supabase_url}")
        print(f"✅ Supabase Key: {supabase_key[:20]}...")
        
        # Test with direct HTTP request
        headers = {
            'apikey': supabase_key,
            'Authorization': f'Bearer {supabase_key}',
            'Content-Type': 'application/json'
        }
        
        url = f"{supabase_url}/rest/v1/error?limit=5"
        
        print(f"Testing URL: {url}")
        
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Success! Found {len(data)} error records")
            if data:
                print(f"Sample record: {data[0]}")
            return True
        else:
            print(f"❌ HTTP error: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_supabase_simple()
    if success:
        print("\n✅ Supabase connection works!")
    else:
        print("\n❌ Supabase connection failed!")
        sys.exit(1)
