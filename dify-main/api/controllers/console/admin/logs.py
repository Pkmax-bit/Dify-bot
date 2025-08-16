import os
import logging
from datetime import datetime
from functools import wraps
from flask import Blueprint, request, jsonify
from flask_restful import Resource, Api
from sqlalchemy import text
from controllers.console.auth.error import UnauthorizedError
from controllers.console.wraps import setup_required, account_initialization_required
from controllers.console.admin import admin_required
from services.logging_service import logging_service
from services.supabase_service import supabase_service
from configs import dify_config
from extensions.ext_database import db
from extensions.ext_redis import redis_client


bp = Blueprint('admin_logs', __name__, url_prefix='/console/api/admin')
api = Api(bp)

def simple_admin_required(f):
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

# Simple endpoints for the new admin page
@bp.route('/verify', methods=['POST'])
@simple_admin_required
def verify_admin():
    """Verify admin key"""
    return jsonify({'success': True})

@bp.route('/system-info', methods=['GET'])
@simple_admin_required
def get_system_info():
    """Get system information including database and service status"""
    try:
        from models.custom_logs import DifyLogs, ErrorLog
        
        system_info = {
            'database_status': 'disconnected',
            'redis_status': 'disconnected',
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
                    
                    # Get real log statistics from local database
                    total_logs = db.session.query(DifyLogs).count()
                    error_count = db.session.query(ErrorLog).count()
                    
                    system_info['total_logs'] = total_logs
                    system_info['error_count'] = error_count
                    
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
        
        return jsonify(system_info)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/supabase-test', methods=['GET'])
@simple_admin_required
def test_supabase_connection():
    """Test Supabase connection and get table info"""
    try:
        result = supabase_service.test_connection()
        
        if result['status'] == 'connected':
            # Get sample data from both tables
            dify_logs_sample = supabase_service.get_dify_logs(limit=5)
            error_logs_sample = supabase_service.get_error_logs(limit=5)
            stats = supabase_service.get_log_stats()
            
            result['sample_data'] = {
                'dify_logs': dify_logs_sample,
                'error_logs': error_logs_sample,
                'statistics': stats
            }
        
        return jsonify(result)
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@bp.route('/logs/dify', methods=['GET'])
@simple_admin_required
def get_dify_logs_only():
    """Get only dify_logs table data from local database"""
    try:
        from models.custom_logs import DifyLogs
        
        page = request.args.get('page', 1, type=int)
        per_page = min(request.args.get('per_page', 20, type=int), 100)
        offset = (page - 1) * per_page
        
        # Query local database
        logs_query = db.session.query(DifyLogs).order_by(DifyLogs.created_at.desc())
        total_count = logs_query.count()
        logs = logs_query.offset(offset).limit(per_page).all()
        
        # Convert to dictionary
        logs_data = []
        for log in logs:
            logs_data.append({
                'id': log.id,
                'app_id': log.app_id,
                'conversation_id': log.conversation_id,
                'user_id': log.user_id,
                'input_text': log.input_text,
                'output_text': log.output_text,
                'latency_ms': log.latency_ms,
                'status_code': log.status_code,
                'created_at': log.created_at.isoformat() if log.created_at else None,
                'dialog_count': float(log.dialog_count) if log.dialog_count else None,
                'work_run_id': log.work_run_id,
                'status': log.status,
                'template': log.template,
                'bot': log.Bot
            })
        
        return jsonify({
            'logs': logs_data,
            'total': total_count,
            'page': page,
            'per_page': per_page,
            'type': 'dify_logs'
        })
    except Exception as e:
        logging.error(f"Error fetching dify logs: {e}")
        return jsonify({'error': str(e)}), 500

@bp.route('/logs/errors', methods=['GET'])
@simple_admin_required
def get_error_logs_only():
    """Get only error table data from local database"""
    try:
        from models.custom_logs import ErrorLog
        
        page = request.args.get('page', 1, type=int)
        per_page = min(request.args.get('per_page', 20, type=int), 100)
        offset = (page - 1) * per_page
        
        # Query local database
        errors_query = db.session.query(ErrorLog).order_by(ErrorLog.created_at.desc())
        total_count = errors_query.count()
        errors = errors_query.offset(offset).limit(per_page).all()
        
        # Convert to dictionary
        errors_data = []
        for error in errors:
            errors_data.append({
                'id': error.id,
                'type_error': error.type_error,
                'node': error.node,
                'error_message': error.error_message,
                'user_id': error.user_id,
                'created_at': error.created_at.isoformat() if error.created_at else None
            })
        
        return jsonify({
            'logs': errors_data,
            'total': total_count,
            'page': page,
            'per_page': per_page,
            'type': 'error_logs'
        })
    except Exception as e:
        logging.error(f"Error fetching error logs: {e}")
        return jsonify({'error': str(e)}), 500

@bp.route('/logs', methods=['GET'])
@simple_admin_required
def get_logs():
    """Get system logs from Supabase"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = min(request.args.get('per_page', 20, type=int), 100)
        log_type = request.args.get('type', 'all')  # 'all', 'dify', 'error'
        
        offset = (page - 1) * per_page
        
        if log_type == 'dify':
            logs = supabase_service.get_dify_logs(limit=per_page, offset=offset)
        elif log_type == 'error':
            logs = supabase_service.get_error_logs(limit=per_page, offset=offset)
        else:
            logs = supabase_service.get_combined_logs(limit=per_page)
        
        # Get stats
        stats = supabase_service.get_log_stats()
        
        return jsonify({
            'logs': logs,
            'total': len(logs),
            'page': page,
            'per_page': per_page,
            'stats': stats
        })
    except Exception as e:
        logging.error(f"Error fetching logs: {e}")
        return jsonify({'error': str(e)}), 500


class ChatLogsApi(Resource):
    @setup_required
    @account_initialization_required
    @admin_required
    def get(self):
        """
        Lấy danh sách logs chat (chỉ admin)
        """
        try:
            page = request.args.get('page', 1, type=int)
            per_page = min(request.args.get('per_page', 20, type=int), 100)
            user_id = request.args.get('user_id')
            
            offset = (page - 1) * per_page
            
            logs = logging_service.get_user_chat_history(
                user_id=user_id, 
                limit=per_page, 
                offset=offset
            )
            
            return {
                'data': logs,
                'page': page,
                'per_page': per_page,
                'has_more': len(logs) == per_page
            }
            
        except Exception as e:
            return {'error': str(e)}, 500


class ErrorLogsApi(Resource):
    @setup_required
    @account_initialization_required
    @admin_required
    def get(self):
        """
        Lấy danh sách error logs (chỉ admin)
        """
        try:
            page = request.args.get('page', 1, type=int)
            per_page = min(request.args.get('per_page', 20, type=int), 100)
            user_id = request.args.get('user_id')
            
            offset = (page - 1) * per_page
            
            errors = logging_service.get_user_errors(
                user_id=user_id,
                limit=per_page,
                offset=offset
            )
            
            return {
                'data': errors,
                'page': page,
                'per_page': per_page,
                'has_more': len(errors) == per_page
            }
            
        except Exception as e:
            return {'error': str(e)}, 500


class UserChatHistoryApi(Resource):
    @setup_required
    @account_initialization_required
    def get(self, user_id):
        """
        Lấy lịch sử chat của user (user chỉ xem được của mình, admin xem được tất cả)
        """
        try:
            from flask import g
            
            # Kiểm tra quyền: user chỉ xem được của mình, admin xem được tất cả
            if not g.current_user.is_admin() and str(g.current_user.id) != user_id:
                raise UnauthorizedError("You can only view your own chat history")
            
            page = request.args.get('page', 1, type=int)
            per_page = min(request.args.get('per_page', 20, type=int), 100)
            
            offset = (page - 1) * per_page
            
            logs = logging_service.get_user_chat_history(
                user_id=user_id,
                limit=per_page,
                offset=offset
            )
            
            return {
                'data': logs,
                'page': page,
                'per_page': per_page,
                'has_more': len(logs) == per_page
            }
            
        except UnauthorizedError:
            raise
        except Exception as e:
            return {'error': str(e)}, 500


class LogStatsApi(Resource):
    @setup_required
    @account_initialization_required
    @admin_required
    def get(self):
        """
        Lấy thống kê logs (chỉ admin)
        """
        try:
            from sqlalchemy import func, desc
            from models.custom_logs import DifyLogs, ErrorLog
            from extensions.ext_database import db
            
            # Thống kê chat logs
            total_chats = db.session.query(func.count(DifyLogs.id)).scalar() or 0
            
            # Top users với nhiều chat nhất
            top_users = db.session.query(
                DifyLogs.user_id,
                func.count(DifyLogs.id).label('chat_count')
            ).group_by(DifyLogs.user_id).order_by(
                desc('chat_count')
            ).limit(10).all()
            
            # Thống kê errors
            total_errors = db.session.query(func.count(ErrorLog.id)).scalar() or 0
            
            # Top error types
            top_errors = db.session.query(
                ErrorLog.type_error,
                func.count(ErrorLog.id).label('error_count')
            ).group_by(ErrorLog.type_error).order_by(
                desc('error_count')
            ).limit(10).all()
            
            return {
                'chat_stats': {
                    'total_chats': total_chats,
                    'top_users': [
                        {'user_id': user_id, 'chat_count': count}
                        for user_id, count in top_users
                    ]
                },
                'error_stats': {
                    'total_errors': total_errors,
                    'top_error_types': [
                        {'error_type': error_type, 'count': count}
                        for error_type, count in top_errors
                    ]
                }
            }
            
        except Exception as e:
            return {'error': str(e)}, 500


# Đăng ký routes
api.add_resource(ChatLogsApi, '/chat-logs')
api.add_resource(ErrorLogsApi, '/error-logs')
api.add_resource(UserChatHistoryApi, '/users/<string:user_id>/chat-history')
api.add_resource(LogStatsApi, '/log-stats')
