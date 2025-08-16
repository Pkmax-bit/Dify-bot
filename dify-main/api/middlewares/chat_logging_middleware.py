import time
import traceback
from flask import Flask, request, g
from functools import wraps
from typing import Optional, Callable, Any

from services.logging_service import logging_service
from models.account import Account


class ChatLoggingMiddleware:
    def __init__(self, app: Flask = None):
        self.app = app
        if app:
            self.init_app(app)
    
    def init_app(self, app: Flask):
        app.before_request(self.before_request)
        app.after_request(self.after_request)
        app.teardown_appcontext(self.teardown_appcontext)
        
    def before_request(self):
        g.start_time = time.time()
        g.user_id = None
        g.app_id = getattr(request, 'view_args', {}).get('app_id')
        g.conversation_id = None
        
        # Lấy user_id từ token hoặc session
        try:
            if hasattr(g, 'current_user') and g.current_user:
                g.user_id = str(g.current_user.id)
        except:
            pass
            
    def after_request(self, response):
        # Chỉ log cho các API chat/completion
        if self._should_log_request():
            latency_ms = int((time.time() - g.start_time) * 1000)
            
            try:
                self._log_chat_interaction(response, latency_ms)
            except Exception as e:
                print(f"Error logging chat interaction: {e}")
                
        return response
    
    def teardown_appcontext(self, error):
        if error:
            self._log_error(error)
    
    def _should_log_request(self) -> bool:
        """Kiểm tra xem có nên log request này không"""
        path = request.path
        method = request.method
        
        # Chỉ log các endpoint chat/completion
        chat_endpoints = [
            '/v1/chat-messages',
            '/v1/completion-messages', 
            '/v1/workflows/run',
            '/v1/audio-to-text',
            '/v1/text-to-audio'
        ]
        
        return (method == 'POST' and 
                any(endpoint in path for endpoint in chat_endpoints))
    
    def _log_chat_interaction(self, response, latency_ms: int):
        """Ghi log tương tác chat"""
        try:
            # Lấy input từ request
            input_text = ""
            if request.is_json and request.json:
                input_text = str(request.json.get('query', '') or 
                               request.json.get('inputs', '') or
                               request.json.get('question', ''))
            
            # Lấy output từ response (nếu có thể)
            output_text = ""
            if response.is_json:
                try:
                    data = response.get_json()
                    if data:
                        output_text = str(data.get('answer', '') or
                                        data.get('data', {}).get('outputs', '') or
                                        data.get('text', ''))
                except:
                    pass
            
            # Lấy conversation_id từ request hoặc response
            conversation_id = g.conversation_id
            if not conversation_id and request.is_json:
                conversation_id = request.json.get('conversation_id')
            
            if not conversation_id and response.is_json:
                try:
                    data = response.get_json()
                    conversation_id = data.get('conversation_id')
                except:
                    pass
            
            # Log vào database
            logging_service.log_chat_interaction(
                app_id=g.app_id or 'unknown',
                conversation_id=conversation_id or 'unknown',
                user_id=g.user_id or 'anonymous',
                input_text=input_text[:4000],  # Giới hạn độ dài
                output_text=output_text[:4000],
                latency_ms=latency_ms,
                status_code=response.status_code,
                status='success' if response.status_code < 400 else 'error'
            )
            
        except Exception as e:
            print(f"Error in _log_chat_interaction: {e}")
    
    def _log_error(self, error):
        """Ghi log lỗi"""
        try:
            error_message = str(error)
            error_type = type(error).__name__
            
            # Lấy stack trace
            tb = traceback.format_exc()
            full_error = f"{error_message}\n\nStack trace:\n{tb}"
            
            # Log lỗi vào database và Supabase
            logging_service.log_error(
                type_error=error_type,
                error_message=full_error[:2000],  # Giới hạn độ dài
                user_id=g.user_id,
                node=request.endpoint if request else None
            )
            
        except Exception as e:
            print(f"Error in _log_error: {e}")


def log_chat_decorator(func: Callable) -> Callable:
    """
    Decorator để log các function chat cụ thể
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        
        try:
            result = func(*args, **kwargs)
            latency_ms = int((time.time() - start_time) * 1000)
            
            # Log thành công
            user_id = getattr(g, 'user_id', 'anonymous')
            
            logging_service.log_chat_interaction(
                app_id=kwargs.get('app_id', 'decorator'),
                conversation_id=kwargs.get('conversation_id', 'decorator'),
                user_id=user_id,
                input_text=str(kwargs.get('query', ''))[:4000],
                output_text=str(result)[:4000] if result else '',
                latency_ms=latency_ms,
                status_code=200,
                status='success'
            )
            
            return result
            
        except Exception as e:
            # Log lỗi
            logging_service.log_error(
                type_error=type(e).__name__,
                error_message=str(e)[:2000],
                user_id=getattr(g, 'user_id', 'anonymous'),
                node=func.__name__
            )
            raise
            
    return wrapper


# Khởi tạo middleware
chat_logging_middleware = ChatLoggingMiddleware()
