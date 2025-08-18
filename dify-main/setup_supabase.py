#!/usr/bin/env python3
"""
Script to setup Supabase storage bucket for Dify
"""
import psycopg2
import sys

# Database connection parameters
DB_HOST = "db.nuadflxsgwazllqiswfo.supabase.co"
DB_PORT = "5432"
DB_NAME = "postgres"
DB_USER = "postgres"
DB_PASSWORD = "n2c7JW3L9pZXMs@"

def connect_to_database():
    """Connect to the Supabase PostgreSQL database"""
    try:
        connection = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        print("✅ Successfully connected to Supabase database!")
        return connection
    except Exception as e:
        print(f"❌ Error connecting to database: {e}")
        return None

def enable_extensions(connection):
    """Enable required PostgreSQL extensions"""
    try:
        cursor = connection.cursor()
        
        # Enable pgvector extension for vector operations
        cursor.execute("CREATE EXTENSION IF NOT EXISTS vector;")
        print("✅ Enabled vector extension")
        
        # Enable uuid-ossp for UUID generation
        cursor.execute("CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\";")
        print("✅ Enabled uuid-ossp extension")
        
        connection.commit()
        cursor.close()
        return True
    except Exception as e:
        print(f"❌ Error enabling extensions: {e}")
        connection.rollback()
        return False

def setup_storage_policies(connection):
    """Setup storage policies for Supabase"""
    try:
        cursor = connection.cursor()
        
        # Create storage bucket if not exists (this is usually done via Supabase dashboard)
        storage_sql = """
        -- Insert storage bucket if not exists
        INSERT INTO storage.buckets (id, name, public)
        VALUES ('dify-files', 'dify-files', false)
        ON CONFLICT (id) DO NOTHING;
        
        -- Allow authenticated users to upload files
        CREATE POLICY IF NOT EXISTS "Allow authenticated uploads" ON storage.objects
        FOR INSERT WITH CHECK (auth.role() = 'authenticated');
        
        -- Allow authenticated users to view their files
        CREATE POLICY IF NOT EXISTS "Allow authenticated reads" ON storage.objects
        FOR SELECT USING (auth.role() = 'authenticated');
        
        -- Allow authenticated users to update their files
        CREATE POLICY IF NOT EXISTS "Allow authenticated updates" ON storage.objects
        FOR UPDATE USING (auth.role() = 'authenticated');
        
        -- Allow authenticated users to delete their files
        CREATE POLICY IF NOT EXISTS "Allow authenticated deletes" ON storage.objects
        FOR DELETE USING (auth.role() = 'authenticated');
        """
        
        cursor.execute(storage_sql)
        connection.commit()
        cursor.close()
        print("✅ Storage policies configured")
        return True
    except Exception as e:
        print(f"⚠️  Storage policy setup (might need manual setup in Supabase dashboard): {e}")
        connection.rollback()
        return False

def test_connection(connection):
    """Test database connection and show available tables"""
    try:
        cursor = connection.cursor()
        
        # Test basic query
        cursor.execute("SELECT version();")
        version = cursor.fetchone()
        print(f"✅ PostgreSQL version: {version[0][:50]}...")
        
        # Count tables
        cursor.execute("""
            SELECT COUNT(*) 
            FROM information_schema.tables 
            WHERE table_schema = 'public';
        """)
        table_count = cursor.fetchone()[0]
        print(f"✅ Found {table_count} tables in public schema")
        
        # Check if required tables exist
        required_tables = ['accounts', 'tenants', 'apps', 'conversations', 'messages', 'dify_logs', 'error']
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' 
            AND table_name = ANY(%s);
        """, (required_tables,))
        
        existing_tables = [row[0] for row in cursor.fetchall()]
        print(f"✅ Required tables found: {', '.join(existing_tables)}")
        
        missing_tables = set(required_tables) - set(existing_tables)
        if missing_tables:
            print(f"⚠️  Missing tables: {', '.join(missing_tables)}")
        else:
            print("✅ All required tables are present!")
        
        cursor.close()
        return True
    except Exception as e:
        print(f"❌ Error testing connection: {e}")
        return False

def main():
    print("🚀 Setting up Supabase for Dify...")
    
    # Connect to database
    connection = connect_to_database()
    if not connection:
        sys.exit(1)
    
    # Test connection
    if not test_connection(connection):
        connection.close()
        sys.exit(1)
    
    # Enable extensions
    if not enable_extensions(connection):
        print("⚠️  Failed to enable some extensions")
    
    # Setup storage (optional, might need manual setup)
    setup_storage_policies(connection)
    
    # Close connection
    connection.close()
    print("\n🎉 Supabase setup completed!")
    print("\n📋 Next steps:")
    print("1. Create storage bucket 'dify-files' in Supabase dashboard")
    print("2. Update environment variables if needed")
    print("3. Start the Dify application")

if __name__ == "__main__":
    main()
