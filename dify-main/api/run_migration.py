#!/usr/bin/env python3
"""
Simple migration runner that bypasses the complex Flask app initialization.
This directly creates the logging tables needed for our logging system.
"""

import os
import sys
sys.path.insert(0, os.path.dirname(__file__))

import psycopg2
from configs import dify_config


def run_migration():
    """Run the migration to create logging tables"""
    
    # Database connection using the same config as the app
    conn = psycopg2.connect(
        host=dify_config.DB_HOST,
        port=dify_config.DB_PORT,
        database=dify_config.DB_DATABASE,
        user=dify_config.DB_USERNAME,
        password=dify_config.DB_PASSWORD or None
    )
    
    cur = conn.cursor()
    
    try:
        print("Creating logging tables...")
        
        # Create dify_logs table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS dify_logs (
                id SERIAL PRIMARY KEY,
                user_id VARCHAR(255),
                message TEXT,
                response TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                session_id VARCHAR(255),
                message_id VARCHAR(255),
                metadata JSONB
            );
        """)
        
        # Create error table  
        cur.execute("""
            CREATE TABLE IF NOT EXISTS error (
                id SERIAL PRIMARY KEY,
                user_id VARCHAR(255),
                type_error VARCHAR(255),
                message_error TEXT,
                stack_trace TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                request_data JSONB,
                metadata JSONB
            );
        """)
        
        # Create indexes for better performance
        cur.execute("""
            CREATE INDEX IF NOT EXISTS idx_dify_logs_user_id ON dify_logs(user_id);
        """)
        
        cur.execute("""
            CREATE INDEX IF NOT EXISTS idx_dify_logs_created_at ON dify_logs(created_at);
        """)
        
        cur.execute("""
            CREATE INDEX IF NOT EXISTS idx_dify_logs_session_id ON dify_logs(session_id);
        """)
        
        cur.execute("""
            CREATE INDEX IF NOT EXISTS idx_error_user_id ON error(user_id);
        """)
        
        cur.execute("""
            CREATE INDEX IF NOT EXISTS idx_error_created_at ON error(created_at);
        """)
        
        cur.execute("""
            CREATE INDEX IF NOT EXISTS idx_error_type_error ON error(type_error);
        """)
        
        conn.commit()
        print("✅ Logging tables created successfully!")
        
        # Verify tables exist
        cur.execute("""
            SELECT table_name FROM information_schema.tables 
            WHERE table_schema = 'public' 
            AND table_name IN ('dify_logs', 'error');
        """)
        
        tables = cur.fetchall()
        print(f"✅ Verified tables exist: {[table[0] for table in tables]}")
        
    except Exception as e:
        print(f"❌ Error creating tables: {e}")
        conn.rollback()
        return False
    finally:
        cur.close()
        conn.close()
    
    return True


if __name__ == "__main__":
    print("🚀 Running logging system migration...")
    success = run_migration()
    if success:
        print("✅ Migration completed successfully!")
    else:
        print("❌ Migration failed!")
        sys.exit(1)
