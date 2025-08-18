#!/usr/bin/env python3
"""
Script to import Dify database schema to Supabase
"""
import psycopg2
import sys
import os

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

def execute_sql_file(connection, file_path):
    """Execute SQL commands from a file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            sql_content = file.read()
        
        cursor = connection.cursor()
        cursor.execute(sql_content)
        connection.commit()
        cursor.close()
        print(f"✅ Successfully executed SQL file: {file_path}")
        return True
    except Exception as e:
        print(f"❌ Error executing SQL file: {e}")
        connection.rollback()
        return False

def check_tables(connection):
    """Check what tables exist in the database"""
    try:
        cursor = connection.cursor()
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' 
            ORDER BY table_name;
        """)
        tables = cursor.fetchall()
        cursor.close()
        
        print(f"\n📊 Found {len(tables)} tables in the database:")
        for table in tables:
            print(f"  - {table[0]}")
        return len(tables)
    except Exception as e:
        print(f"❌ Error checking tables: {e}")
        return 0

def main():
    print("🚀 Starting Supabase schema import...")
    
    # Connect to database
    connection = connect_to_database()
    if not connection:
        sys.exit(1)
    
    # Check existing tables
    table_count_before = check_tables(connection)
    
    # Import schema
    schema_file = "supabase_complete_schema.sql"
    if os.path.exists(schema_file):
        print(f"\n📁 Importing schema from {schema_file}...")
        success = execute_sql_file(connection, schema_file)
        if success:
            print("✅ Schema import completed!")
        else:
            print("❌ Schema import failed!")
            connection.close()
            sys.exit(1)
    else:
        print(f"❌ Schema file {schema_file} not found!")
        connection.close()
        sys.exit(1)
    
    # Check tables after import
    print("\n🔍 Checking tables after import...")
    table_count_after = check_tables(connection)
    
    print(f"\n📈 Import summary:")
    print(f"  - Tables before: {table_count_before}")
    print(f"  - Tables after: {table_count_after}")
    print(f"  - Tables added: {table_count_after - table_count_before}")
    
    # Close connection
    connection.close()
    print("\n🎉 Database setup completed successfully!")

if __name__ == "__main__":
    main()
