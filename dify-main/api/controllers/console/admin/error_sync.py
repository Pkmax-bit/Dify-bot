import logging
from flask import Blueprint, request, jsonify
from flask_restful import Resource, Api
from services.error_sync_service import error_sync_service
from configs import dify_config

logger = logging.getLogger(__name__)

bp = Blueprint('error_sync', __name__, url_prefix='/console/api/admin')
api = Api(bp)

def simple_admin_required(f):
    """Simple admin authorization decorator"""
    from functools import wraps
    
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Skip authentication in development mode
        if dify_config.DEBUG:
            return f(*args, **kwargs)
            
        admin_key = request.headers.get('X-Admin-Key')
        
        if not admin_key:
            return jsonify({'error': 'Admin Key required'}), 401
            
        if admin_key != dify_config.ADMIN_API_KEY:
            return jsonify({'error': 'Invalid Admin Key'}), 401
            
        return f(*args, **kwargs)
    return decorated_function

@bp.route('/error-sync/start', methods=['POST'])
@simple_admin_required
def start_error_sync():
    """Bắt đầu đồng bộ errors liên tục"""
    try:
        error_sync_service.start_continuous_sync()
        return jsonify({
            'success': True,
            'message': 'Error sync service started successfully',
            'status': error_sync_service.get_sync_status()
        })
    except Exception as e:
        logger.error(f"Error starting error sync: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@bp.route('/error-sync/stop', methods=['POST'])
@simple_admin_required
def stop_error_sync():
    """Dừng đồng bộ errors liên tục"""
    try:
        error_sync_service.stop_continuous_sync()
        return jsonify({
            'success': True,
            'message': 'Error sync service stopped successfully'
        })
    except Exception as e:
        logger.error(f"Error stopping error sync: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@bp.route('/error-sync/manual', methods=['POST'])
@simple_admin_required
def manual_error_sync():
    """Đồng bộ errors thủ công"""
    try:
        result = error_sync_service.manual_sync()
        
        if result['success']:
            return jsonify({
                'success': True,
                'message': 'Manual error sync completed successfully',
                'result': result
            })
        else:
            return jsonify({
                'success': False,
                'error': result['error']
            }), 500
            
    except Exception as e:
        logger.error(f"Error in manual error sync: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@bp.route('/error-sync/status', methods=['GET'])
@simple_admin_required
def error_sync_status():
    """Lấy trạng thái đồng bộ errors"""
    try:
        status = error_sync_service.get_sync_status()
        return jsonify({
            'success': True,
            'status': status
        })
    except Exception as e:
        logger.error(f"Error getting error sync status: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@bp.route('/errors', methods=['GET'])
@simple_admin_required
def get_errors():
    """Lấy danh sách error logs trực tiếp từ Supabase (với fallback mock data)"""
    try:
        import os
        
        # Get query parameters
        limit = request.args.get('limit', 100, type=int)
        offset = request.args.get('offset', 0, type=int)
        
        # Try to connect to Supabase
        try:
            from supabase import create_client, Client
            
            # Initialize Supabase client
            supabase_url = os.getenv('SUPABASE_URL')
            supabase_key = os.getenv('SUPABASE_ANON_KEY')
            
            if not supabase_url or not supabase_key:
                raise Exception('Supabase credentials not configured')
            
            supabase: Client = create_client(supabase_url, supabase_key)
            
            # Query error table from Supabase directly
            response = supabase.table('error').select('*').order('created_at', desc=True).range(offset, offset + limit - 1).execute()
            
            # Get total count
            count_response = supabase.table('error').select('id', count='exact').execute()
            total_count = count_response.count if hasattr(count_response, 'count') else len(response.data)
            
            # Convert to expected format
            error_list = []
            for error in response.data:
                error_dict = {
                    'id': error.get('id'),
                    'message': error.get('message'),
                    'level': error.get('level'),
                    'created_at': error.get('created_at'),
                    'stack_trace': error.get('stack_trace'),
                    'user_id': error.get('user_id'),
                    'request_id': error.get('request_id'),
                    'endpoint': error.get('endpoint'),
                    'method': error.get('method'),
                    'status_code': error.get('status_code')
                }
                error_list.append(error_dict)
            
            return jsonify({
                'success': True,
                'errors': error_list,
                'total': total_count,
                'limit': limit,
                'offset': offset,
                'source': 'supabase'
            })
            
        except Exception as supabase_error:
            logger.warning(f"Could not connect to Supabase: {str(supabase_error)}")
            
            # Fallback to mock data for testing
            from datetime import datetime, timedelta
            
            mock_errors = []
            for i in range(min(limit, 10)):  # Generate up to 10 mock errors
                mock_errors.append({
                    'id': i + 1 + offset,
                    'message': f'Mock error message {i + 1 + offset}',
                    'level': 'ERROR' if i % 2 == 0 else 'WARNING',
                    'created_at': (datetime.now() - timedelta(hours=i)).isoformat(),
                    'stack_trace': f'Mock stack trace for error {i + 1 + offset}',
                    'user_id': f'user_{i + 1}',
                    'request_id': f'req_{i + 1 + offset}',
                    'endpoint': f'/api/test/{i + 1}',
                    'method': 'GET' if i % 2 == 0 else 'POST',
                    'status_code': 500 if i % 2 == 0 else 400
                })
            
            return jsonify({
                'success': True,
                'errors': mock_errors,
                'total': 50,  # Mock total
                'limit': limit,
                'offset': offset,
                'source': 'mock',
                'note': 'Using mock data because Supabase connection failed'
            })
        
    except Exception as e:
        logger.error(f"Error fetching error logs: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
