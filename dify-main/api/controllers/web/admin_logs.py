import os
import logging
from datetime import datetime
from functools import wraps
from flask import Blueprint, request, jsonify
from sqlalchemy import text
from redis import Redis
import psycopg2
from configs import dify_config
from extensions.ext_database import db
from extensions.ext_redis import redis_client

# Create admin logs blueprint
admin_logs_bp = Blueprint('admin_logs', __name__, url_prefix='/admin')

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        admin_key = request.headers.get('X-Admin-Key')
        
        if not admin_key:
            return jsonify({'error': 'Admin Key required'}), 401
            
        if admin_key != dify_config.ADMIN_API_KEY:
            return jsonify({'error': 'Invalid Admin Key'}), 401
            
        return f(*args, **kwargs)
    return decorated_function

@admin_logs_bp.route('/verify', methods=['POST'])
@admin_required
def verify_admin():
    """Verify admin key"""
    return jsonify({'success': True})

@admin_logs_bp.route('/logs', methods=['GET'])
@admin_required
def get_logs():
    """Get system logs"""
    try:
        # Mock logs for now - you can replace with actual log reading logic
        logs = [
            {
                'id': f'log_{i}',
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'level': 'info' if i % 3 == 0 else 'error' if i % 4 == 0 else 'warning',
                'message': f'System message {i}',
                'module': 'api' if i % 2 == 0 else 'database',
                'error_details': 'Stack trace details...' if i % 4 == 0 else None
            }
            for i in range(1, 21)
        ]
        
        return jsonify({
            'logs': logs,
            'total': len(logs)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_logs_bp.route('/system-info', methods=['GET'])
@admin_required
def get_system_info():
    """Get system information including database and service status"""
    try:
        system_info = {
            'database_status': 'disconnected',
            'redis_status': 'disconnected',
            'supabase_status': 'not_configured',
            'api_status': 'active',
            'total_logs': 0,
            'error_count': 0
        }
        
        # Check database connection
        try:
            with db.engine.connect() as conn:
                result = conn.execute(text("SELECT 1"))
                if result:
                    system_info['database_status'] = 'connected'
        except Exception as e:
            logging.error(f"Database connection error: {e}")
            system_info['database_status'] = f'error: {str(e)}'
        
        # Check Redis connection
        try:
            if redis_client:
                redis_client.ping()
                system_info['redis_status'] = 'connected'
        except Exception as e:
            logging.error(f"Redis connection error: {e}")
            system_info['redis_status'] = f'error: {str(e)}'
        
        # Check Supabase configuration
        supabase_url = os.getenv('SUPABASE_URL', '')
        supabase_key = os.getenv('SUPABASE_API_KEY', '')
        
        if supabase_url and supabase_key:
            if supabase_url != 'your-server-url' and supabase_key != 'your-access-key':
                system_info['supabase_status'] = 'configured'
                # You can add actual connection test here
            else:
                system_info['supabase_status'] = 'not_configured'
        else:
            system_info['supabase_status'] = 'not_configured'
        
        # Get log counts (mock data for now)
        system_info['total_logs'] = 150
        system_info['error_count'] = 12
        
        return jsonify(system_info)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_logs_bp.route('/supabase-test', methods=['GET'])
@admin_required
def test_supabase_connection():
    """Test Supabase connection"""
    try:
        supabase_url = os.getenv('SUPABASE_URL', '')
        supabase_key = os.getenv('SUPABASE_API_KEY', '')
        
        if not supabase_url or not supabase_key:
            return jsonify({
                'status': 'error',
                'message': 'Supabase credentials not configured',
                'config': {
                    'url_configured': bool(supabase_url),
                    'key_configured': bool(supabase_key)
                }
            })
        
        if supabase_url == 'your-server-url' or supabase_key == 'your-access-key':
            return jsonify({
                'status': 'error',
                'message': 'Supabase credentials are placeholder values',
                'config': {
                    'url': supabase_url,
                    'key_masked': supabase_key[:10] + '...' if len(supabase_key) > 10 else 'short_key'
                }
            })
        
        # Here you would add actual Supabase connection test
        # For now, just return configured status
        return jsonify({
            'status': 'configured',
            'message': 'Supabase credentials are configured',
            'config': {
                'url': supabase_url,
                'key_masked': supabase_key[:10] + '...' if len(supabase_key) > 10 else 'short_key'
            }
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@admin_logs_bp.route('/database-config', methods=['GET'])
@admin_required
def get_database_config():
    """Get database configuration information"""
    try:
        config_info = {
            'database': {
                'host': os.getenv('DB_HOST', 'localhost'),
                'port': os.getenv('DB_PORT', '5432'),
                'database': os.getenv('DB_DATABASE', 'dify'),
                'username': os.getenv('DB_USERNAME', 'postgres')
            },
            'supabase': {
                'url': os.getenv('SUPABASE_URL', 'not_configured'),
                'bucket': os.getenv('SUPABASE_BUCKET_NAME', 'not_configured'),
                'configured': bool(
                    os.getenv('SUPABASE_URL') and 
                    os.getenv('SUPABASE_API_KEY') and
                    os.getenv('SUPABASE_URL') != 'your-server-url'
                )
            },
            'redis': {
                'host': os.getenv('REDIS_HOST', 'localhost'),
                'port': os.getenv('REDIS_PORT', '6379'),
                'db': os.getenv('REDIS_DB', '0')
            }
        }
        
        return jsonify(config_info)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
