import os
import requests
import json
from datetime import datetime
from typing import Optional, Dict, Any

from models.custom_logs import DifyLogs, ErrorLog
from extensions.ext_database import db


class LoggingService:
    def __init__(self):
        self.supabase_url = os.getenv('SUPABASE_URL')
        self.supabase_key = os.getenv('SUPABASE_ANON_KEY')
        self.supabase_service_key = os.getenv('SUPABASE_SERVICE_ROLE_KEY')
        
    def log_chat_interaction(self, 
                           app_id: str,
                           conversation_id: str,
                           user_id: str,
                           input_text: str,
                           output_text: str,
                           latency_ms: int = None,
                           status_code: int = 200,
                           dialog_count: int = None,
                           work_run_id: str = None,
                           status: str = "success",
                           template: str = None,
                           bot_name: str = None) -> bool:
        """
        Ghi lịch sử chat vào database
        """
        try:
            log_entry = DifyLogs(
                app_id=app_id,
                conversation_id=conversation_id,
                user_id=user_id,
                input_text=input_text,
                output_text=output_text,
                latency_ms=latency_ms,
                status_code=status_code,
                dialog_count=dialog_count,
                work_run_id=work_run_id,
                status=status,
                template=template,
                Bot=bot_name
            )
            
            db.session.add(log_entry)
            db.session.commit()
            return True
            
        except Exception as e:
            db.session.rollback()
            print(f"Error logging chat interaction: {e}")
            return False
    
    def log_error(self, 
                  type_error: str,
                  error_message: str,
                  user_id: str = None,
                  node: str = None,
                  send_to_supabase: bool = True) -> bool:
        """
        Ghi lỗi vào database local và gửi lên Supabase
        """
        try:
            # Ghi vào database local
            error_entry = ErrorLog(
                type_error=type_error,
                node=node,
                error_message=error_message,
                user_id=user_id
            )
            
            db.session.add(error_entry)
            db.session.commit()
            
            # Gửi lên Supabase nếu được yêu cầu
            if send_to_supabase and self.supabase_url and self.supabase_service_key:
                self._send_error_to_supabase({
                    'type_error': type_error,
                    'node': node,
                    'error_message': error_message,
                    'user_id': user_id,
                    'created_at': datetime.utcnow().isoformat(),
                    'local_error_id': error_entry.id
                })
            
            return True
            
        except Exception as e:
            db.session.rollback()
            print(f"Error logging error: {e}")
            return False
    
    def _send_error_to_supabase(self, error_data: Dict[str, Any]) -> bool:
        """
        Gửi thông tin lỗi lên Supabase
        """
        try:
            headers = {
                'apikey': self.supabase_service_key,
                'Authorization': f'Bearer {self.supabase_service_key}',
                'Content-Type': 'application/json',
                'Prefer': 'return=minimal'
            }
            
            url = f"{self.supabase_url}/rest/v1/dify_errors"
            
            response = requests.post(url, headers=headers, json=error_data)
            
            if response.status_code in [200, 201]:
                print(f"Error sent to Supabase successfully")
                return True
            else:
                print(f"Failed to send error to Supabase: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            print(f"Error sending to Supabase: {e}")
            return False
    
    def get_user_chat_history(self, user_id: str, limit: int = 50, offset: int = 0) -> list:
        """
        Lấy lịch sử chat của user
        """
        try:
            logs = db.session.query(DifyLogs).filter(
                DifyLogs.user_id == user_id
            ).order_by(DifyLogs.created_at.desc()).limit(limit).offset(offset).all()
            
            return [{
                'id': log.id,
                'app_id': log.app_id,
                'conversation_id': log.conversation_id,
                'input_text': log.input_text,
                'output_text': log.output_text,
                'latency_ms': log.latency_ms,
                'status_code': log.status_code,
                'created_at': log.created_at.isoformat() if log.created_at else None,
                'dialog_count': float(log.dialog_count) if log.dialog_count else None,
                'status': log.status,
                'bot_name': log.Bot
            } for log in logs]
            
        except Exception as e:
            print(f"Error getting chat history: {e}")
            return []
    
    def get_user_errors(self, user_id: str = None, limit: int = 50, offset: int = 0) -> list:
        """
        Lấy danh sách lỗi (cho admin)
        """
        try:
            query = db.session.query(ErrorLog)
            
            if user_id:
                query = query.filter(ErrorLog.user_id == user_id)
            
            errors = query.order_by(ErrorLog.created_at.desc()).limit(limit).offset(offset).all()
            
            return [{
                'id': error.id,
                'type_error': error.type_error,
                'node': error.node,
                'error_message': error.error_message,
                'user_id': error.user_id,
                'created_at': error.created_at.isoformat() if error.created_at else None
            } for error in errors]
            
        except Exception as e:
            print(f"Error getting error logs: {e}")
            return []


# Singleton instance
logging_service = LoggingService()
