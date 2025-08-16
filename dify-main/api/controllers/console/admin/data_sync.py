import logging
from flask import Blueprint, request, jsonify
from flask_restful import Resource, Api
from services.data_sync_service import data_sync_service
from configs import dify_config

logger = logging.getLogger(__name__)

bp = Blueprint('data_sync', __name__, url_prefix='/console/api/admin')
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

@bp.route('/sync/start', methods=['POST'])
@simple_admin_required
def start_sync():
    """Bắt đầu đồng bộ liên tục"""
    try:
        data_sync_service.start_continuous_sync()
        return jsonify({
            'success': True,
            'message': 'Data sync service started successfully',
            'status': data_sync_service.get_sync_status()
        })
    except Exception as e:
        logger.error(f"Error starting sync: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@bp.route('/sync/stop', methods=['POST'])
@simple_admin_required
def stop_sync():
    """Dừng đồng bộ liên tục"""
    try:
        data_sync_service.stop_continuous_sync()
        return jsonify({
            'success': True,
            'message': 'Data sync service stopped successfully'
        })
    except Exception as e:
        logger.error(f"Error stopping sync: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@bp.route('/sync/manual', methods=['POST'])
@simple_admin_required
def manual_sync():
    """Đồng bộ thủ công"""
    try:
        result = data_sync_service.manual_sync()
        
        if result['success']:
            return jsonify({
                'success': True,
                'message': 'Manual sync completed successfully',
                'result': result
            })
        else:
            return jsonify({
                'success': False,
                'error': result['error']
            }), 500
            
    except Exception as e:
        logger.error(f"Error in manual sync: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@bp.route('/sync/status', methods=['GET'])
@simple_admin_required
def sync_status():
    """Lấy trạng thái đồng bộ"""
    try:
        status = data_sync_service.get_sync_status()
        return jsonify({
            'success': True,
            'status': status
        })
    except Exception as e:
        logger.error(f"Error getting sync status: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@bp.route('/sync/config', methods=['GET', 'POST'])
@simple_admin_required
def sync_config():
    """Lấy/cập nhật cấu hình đồng bộ"""
    if request.method == 'GET':
        try:
            return jsonify({
                'success': True,
                'config': {
                    'sync_interval_minutes': data_sync_service.sync_interval_minutes,
                    'is_running': data_sync_service.is_running,
                    'last_sync_time': data_sync_service.last_sync_time.isoformat() if data_sync_service.last_sync_time else None
                }
            })
        except Exception as e:
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500
    
    elif request.method == 'POST':
        try:
            data = request.get_json()
            new_interval = data.get('sync_interval_minutes')
            
            if new_interval and isinstance(new_interval, int) and new_interval > 0:
                data_sync_service.sync_interval_minutes = new_interval
                
                # Restart service nếu đang chạy
                if data_sync_service.is_running:
                    data_sync_service.stop_continuous_sync()
                    data_sync_service.start_continuous_sync()
                
                return jsonify({
                    'success': True,
                    'message': f'Sync interval updated to {new_interval} minutes',
                    'config': {
                        'sync_interval_minutes': data_sync_service.sync_interval_minutes,
                        'is_running': data_sync_service.is_running
                    }
                })
            else:
                return jsonify({
                    'success': False,
                    'error': 'Invalid sync_interval_minutes value'
                }), 400
                
        except Exception as e:
            logger.error(f"Error updating sync config: {str(e)}")
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500
